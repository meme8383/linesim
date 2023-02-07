"""
Simulates a 2D robot test track for testing robot
sensing/pathfinding algorithms.
"""

import math
import os
from functools import total_ordering

import pygame


class LineSimulation:
    """Simulate a robot track with a robot and line sensors

    :param start: The start position of the robot,
        defaults to ``(50, 450)``.
    :type start: tuple, optional
    :param background: The included background to use,
        defaults to ``"blank"``
    :type background: str, optional
    :param custom_background: The path to a custom background image.
    :type custom_background: str, optional
    """

    def __init__(self, start: tuple = (30, 30), background="blank",
                 custom_background=None):
        """Initialize pygame and robot object"""
        self.running = True

        self.overlays = False

        starts = {"lines": (50, 450),
                  "maze": (30, 280),
                  "blank": (250, 250)}

        # Load background
        if custom_background:
            self.background = pygame.image.load(custom_background)
        else:
            start = starts[background]
            self.background = pygame.image.load(os.path.join(os.path.dirname(
                os.path.abspath(__file__)),
                f"assets/{background}.png"))
        self.size = self.background.get_size()

        # Initialize Window
        pygame.init()
        pygame.display.set_caption("Line Following")
        self.display = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.robot = Robot(start)

    def add_sensor(self, offset, sensor, angle=None):
        """Add a sensor to the robot

        :param offset: The sensor offset from the robot's center.
        :type offset: tuple
        :param sensor: The type of sensor
        :type sensor: str
        :param angle: The angle of an ultrasonic sensor
        :type angle: int
        :return: The sensor object.
        """
        if sensor.lower() == "line":
            sensor = Line(self, self.robot, offset)
        elif sensor.lower() == "ultrasonic":
            if angle is None:
                raise ValueError("Angle is a required parameter")
            sensor = Ultrasonic(self, self.robot, offset, angle)
        else:
            raise ValueError(f"No such sensor type: {sensor}")
        self.robot.sensors.append(sensor)
        return sensor

    def update(self, check_bounds=True, fps=30):
        """Update simulation

        Re-renders the simulation while checking events,
        the robot position, and maintaining a framerate.

        :param check_bounds: Check if the robot leaves the window,
            defaults to ``True``.
        :type check_bounds: bool, optional
        :param fps: The max framerate of the simulation,
            defaults to ``30``.
        :type fps: int
        """
        self.clock.tick(fps)  # Max fps
        self.render()

        # Quit game if robot touches red
        color = self.background.get_at(
            tuple(int(i) for i in self.robot.position))
        if color[0] > 230 and all(i < 50 for i in color[1:3]):
            self.quit()

        # Quit game if robot leaves window
        elif check_bounds and (
                (any(i - 30 < 0 for i in self.robot.position) or
                 any(map(lambda x, y: x + 30 > y, self.robot.position,
                         self.size)))):
            self.quit()

        else:
            # Check for exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

    def render(self):
        """Render background and all objects"""
        self.display.blit(self.background, (0, 0))

        # Render sensors
        to_render = [self.robot] + self.robot.sensors
        for item in to_render:
            surface = item.surface
            position = item.position
            self.display.blit(
                surface,
                (position[0] - surface.get_width() / 2,
                 position[1] - surface.get_height() / 2))

            if self.overlays and isinstance(item, Ultrasonic):
                overlay = item.line
                if overlay is not None:
                    self.display.blit(overlay, (0, 0))

        pygame.display.update()

    def quit(self):
        """Safe exit pygame"""
        self.running = False
        pygame.quit()


class Robot:
    """Player class

    Simulates a robot, which can have sensors.

    :param start: Start position of the robot.
    :type start: tuple
    """

    def __init__(self, start: tuple):
        """Constructor method"""
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets/robot.png"))

        # Initialize position
        self.position = list(start)
        self.angle = 0

        self.sensors = []

    def move(self, speed):
        """Move robot forward

        :param speed: Number of pixels to move forward.
        :type speed: int
        """
        self.position[0] += speed * math.cos(math.radians(self.angle))
        self.position[1] += speed * math.sin(math.radians(self.angle))

    def rotate(self, degrees):
        """Update robot rotation

        :param degrees: Degree change in rotation.
        :type degrees: int
        """
        self.angle += degrees

    @property
    def surface(self) -> pygame.Surface:
        """Rotate robot image

        :return: The rotated robot image.
        :rtype: pygame.Surface
        """
        return pygame.transform.rotate(self.image, -self.angle)


class Sensor:
    """Base sensor class

    :param sim: The robot simulation.
    :type sim: LineSimulation
    :param robot: The robot that the sensor is attached to.
    :type robot: Robot
    :param offset: The sensor's offset from the robot center.
    :type offset: tuple
    """

    def __init__(self, sim: LineSimulation, robot: Robot,
                 offset: tuple):
        """Initialize position"""
        self.offset = offset
        self.robot = robot
        self.sim = sim

    @property
    def position(self) -> tuple:
        """Calculate position of sensor

        :return: The (x, y) position of the sensor.
        :rtype: tuple
        """
        return (int(self.robot.position[0] +
                    self.offset[0] * math.cos(math.radians(self.robot.angle)) -
                    self.offset[1] * math.sin(math.radians(self.robot.angle))),
                int(self.robot.position[1] +
                    self.offset[1] * math.cos(math.radians(self.robot.angle)) +
                    self.offset[0] * math.sin(math.radians(self.robot.angle))))

    @property
    def surface(self) -> pygame.Surface:
        """Default sensor surface

        :return: Colored square representing the sensor.
        :rtype: pygame.Surface
        """
        image = pygame.Surface((5, 5))
        image.fill(pygame.Color("#000000"))
        return image


class Line(Sensor):
    """Robot Line Sensor

    :param sim: The robot simulation.
    :type sim: LineSimulation
    :param robot: The robot that the sensor is attached to.
    :type robot: Robot
    :param offset: The sensor's offset from the robot center.
    :type offset: tuple
    """

    def __init__(self, sim: LineSimulation, robot: Robot,
                 offset: tuple):
        """Initialize position and threshold"""
        super().__init__(sim, robot, offset)
        self.threshold = 50

    def read_line(self):
        """Read line under sensor

        Return True if the average RGB value under sensor
        is under the threshold (black line). Also returned by
        ``__bool__``.
        """
        try:
            value = self.sim.background.get_at(self.position)
            return sum(value[:3]) < (self.threshold * 3)
        except IndexError:
            return False

    def __bool__(self):
        return self.read_line()

    @property
    def surface(self) -> pygame.Surface:
        """Create sensor surface

        :return: Colored square representing the sensor.
        :rtype: pygame.Surface
        """
        image = pygame.Surface((5, 5))
        color = "#00ff00" if self else "#ff0000"
        image.fill(pygame.Color(color))
        return image


@total_ordering
class Ultrasonic(Sensor):
    """Robot Ultrasonic Sensor"""

    def __init__(self, sim: LineSimulation, robot: Robot,
                 offset: tuple, angle: int):
        super().__init__(sim, robot, offset)
        self.angle = angle
        self.overlay = pygame.Surface(self.sim.size)
        self.max_range = 100
        self.overlay = None

    def get_distance(self):
        """Get distance of wall from sensor

        :return: Distance from wall.
        :rtype: int
        """
        self.overlay = pygame.Surface(self.sim.size, pygame.SRCALPHA, 32)
        self.overlay.convert_alpha()
        for dist in range(self.max_range):
            location = [
                self.position[0] + dist * math.cos(
                    math.radians(self.angle + self.robot.angle)),
                self.position[1] + dist * math.sin(
                    math.radians(self.angle + self.robot.angle))
            ]
            location = [int(i) for i in location]

            try:
                value = self.sim.background.get_at(location)
                self.overlay.set_at(location, "#0000ff")
            except IndexError:
                pygame.draw.circle(self.overlay, "#ff0000", location, 3)
                return dist

            if value[2] > 220 and all(i < 50 for i in value[:2]):
                pygame.draw.circle(self.overlay, "#ff0000", location, 3)
                return dist
        return self.max_range

    @property
    def line(self):
        """Ultrasonic visibility overlay

        Only shown when a sensor value is retrieved.
        :return: Line to end of sensor path
        :rtype: pygame.Surface
        """
        overlay = self.overlay
        self.overlay = None
        return overlay

    def __int__(self):
        return self.get_distance()

    def __eq__(self, other):
        if isinstance(other, Ultrasonic):
            return self.get_distance() == other.get_distance()
        return self.get_distance() == other

    def __lt__(self, other):
        if isinstance(other, Ultrasonic):
            return self.get_distance() < other.get_distance()
        return self.get_distance() < other

    @property
    def surface(self) -> pygame.Surface:
        """Create sensor surface

        :return: Colored triangle representing the sensor.
        :rtype: pygame.Surface
        """
        image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        image.convert_alpha()
        angles = [0, 135, 225]
        angles = [self.robot.angle + self.angle + i for i in angles]
        positions = tuple((5 * math.cos(math.radians(i)) + 5,
                           5 * math.sin(math.radians(i)) + 5)
                          for i in angles)

        pygame.draw.polygon(image, "#0000ff", positions)
        return image
