"""
Simulates a 2D robot test track for testing robot
sensing/pathfinding algorithms.
"""

import math
import os

import pygame
from .sensors import Line, Ultrasonic, Hall, IR
from .beacons import Magnet, Infrared


class LineSimulation:  # pylint: disable=too-many-instance-attributes
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

    def __init__(
            self, start: tuple = (30, 30), background="blank",
            custom_background=None
    ):
        """Initialize pygame and robot object"""
        self.running = True
        self.overlays = False

        starts = {"lines": (50, 450), "maze": (30, 280), "blank": (250, 250)}

        # Load background
        if custom_background:
            self.background = pygame.image.load(custom_background)
        else:
            start = starts[background]
            self.background = pygame.image.load(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    f"assets/{background}.png",
                )
            )
        self.size = self.background.get_size()

        # Initialize Window
        pygame.init()
        pygame.display.set_caption("LineSim")
        self.display = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.robot = Robot(start)
        self.assets = []

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
        elif sensor.lower() == "hall":
            sensor = Hall(self, self.robot, offset)
        elif sensor.lower() in ["ir", "infrared"]:
            sensor = IR(self, self.robot, offset)
        else:
            raise ValueError(f"No such sensor type: {sensor}")
        self.robot.sensors.append(sensor)
        return sensor

    def add_beacon(self, location, name):
        """Add beacon to course"""
        if name.lower() == "magnetic":
            beacon = Magnet(location)
        elif name.lower() == "infrared":
            beacon = Infrared(location)
        else:
            raise ValueError(f"No such beacon type: {name}")
        self.assets.append(beacon)

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
                (
                 any(i - 30 < 0 for i in self.robot.position)
                 or any(
                        map(lambda x, y: x + 30 > y, self.robot.position,
                            self.size))
                )
        ):
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
        to_render = [self.robot] + self.robot.sensors + self.assets
        for item in to_render:
            surface = item.surface
            position = item.position
            self.display.blit(
                surface,
                (
                    position[0] - surface.get_width() / 2,
                    position[1] - surface.get_height() / 2,
                ),
            )

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
                         "assets/robot.png")
        )

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
