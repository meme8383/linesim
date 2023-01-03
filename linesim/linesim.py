"""
Simulates a track of black lines on a white
background along with a robot with sensors.
"""

import math
import os
import pygame


class LineSimulation:
    """Simulate a robot track with a robot and line sensors

    :param start: The start position of the robot,
        defaults to ``(50, 450)``.
    :type start: tuple, optional
    :param background: The path to the background image,
        defaults to ``"assets/background.png"``.
    :type background: str, optional
    """

    def __init__(self, start: tuple = (50, 450),
                 background=os.path.join(os.path.dirname(
                     os.path.abspath(__file__)), "assets/background.png")):
        """Initialize pygame and robot object"""
        self.running = True

        # Load background
        self.background = pygame.image.load(background)
        self.size = self.background.get_size()

        # Initialize Window
        pygame.init()
        pygame.display.set_caption("Line Following")
        self.display = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.robot = Robot(start)

    def add_sensor(self, offset):
        """Add a sensor to the robot

        :param offset: The sensor offset from the robot's center.
        :type offset: tuple
        :return: The sensor object.
        :rtype: Sensor
        """
        sensor = Sensor(self, self.robot, offset)
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

        to_render = [self.robot] + self.robot.sensors
        for item in to_render:
            surface = item.surface
            position = item.position
            self.display.blit(
                surface,
                (position[0] - surface.get_width() / 2,
                 position[1] - surface.get_height() / 2))

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
    """Robot line sensor

    :param sim: The robot simulation.
    :type sim: LineSimulation
    :param robot: The robot that the sensor is attached to.
    :type robot: Robot
    :param offset: The sensor's offset from the robot center.
    :type offset: tuple
    """

    def __init__(self, sim: LineSimulation, robot: Robot,
                 offset: tuple):
        """Constructor method"""
        self.offset = offset
        self.robot = robot
        self.sim = sim

    def read_line(self, threshold=50):
        """Read line under sensor

        Return True if the average RGB value under sensor
        is under the threshold (black line).

        :param threshold: The required average RGB value,
            defaults to ``50``.
        :type threshold: int, optional
        """
        try:
            value = self.sim.background.get_at(self.position)
            return sum(value[:3]) < (threshold * 3)
        except IndexError:
            return False

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
        """Create sensor surface

        :return: Colored square representing the sensor.
        :rtype: pygame.Surface
        """
        image = pygame.Surface((5, 5))
        color = "#00ff00" if self.read_line() else "#ff0000"
        image.fill(pygame.Color(color))
        return image
