"""Module defining various robot sensor classes"""

import math
from functools import total_ordering
import pygame

from .beacons import Magnet, Infrared


class Sensor:
    """Base sensor class

    :param sim: The robot simulation.
    :type sim: LineSimulation
    :param robot: The robot that the sensor is attached to.
    :type robot: Robot
    :param offset: The sensor's offset from the robot center.
    :type offset: tuple
    """

    def __init__(self, sim, robot, offset: tuple):
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
        return (
            int(
                self.robot.position[0]
                + self.offset[0] * math.cos(math.radians(self.robot.angle))
                - self.offset[1] * math.sin(math.radians(self.robot.angle))
            ),
            int(
                self.robot.position[1]
                + self.offset[1] * math.cos(math.radians(self.robot.angle))
                + self.offset[0] * math.sin(math.radians(self.robot.angle))
            ),
        )

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

    def __init__(self, sim, robot, offset: tuple):
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

    def __init__(self, sim, robot, offset: tuple,
                 angle: int):
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
                self.position[0]
                + dist * math.cos(math.radians(self.angle + self.robot.angle)),
                self.position[1]
                + dist * math.sin(math.radians(self.angle + self.robot.angle)),
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
        return int(self) == other

    def __lt__(self, other):
        return int(self) < other

    @property
    def surface(self) -> pygame.Surface:
        """Create sensor surface

        Draw a triangle inscribed in a circle that rotates
        with the robot and sensor angle.
        :return: Colored triangle representing the sensor.
        :rtype: pygame.Surface
        """
        image = pygame.Surface((10, 10), pygame.SRCALPHA, 32)
        image.convert_alpha()  # Transparency
        angles = [0, 135, 225]  # Isosceles triangle
        angles = [self.robot.angle + self.angle + i for i in angles]
        positions = tuple(
            (5 * math.cos(math.radians(i)) + 5,
             5 * math.sin(math.radians(i)) + 5)
            for i in angles
        )

        pygame.draw.polygon(image, "#0000ff", positions)
        return image


@total_ordering
class Hall(Sensor):
    """Hall effect sensor class"""

    def get_reading(self):
        """Get distance from all magnetic beacons"""
        value = 0
        for item in self.sim.assets:
            if isinstance(item, Magnet):
                value += item.get_distance(self.position)
        return value

    def __float__(self):
        return self.get_reading()

    def __eq__(self, other):
        return float(self) == other

    def __lt__(self, other):
        return float(self) < other


@total_ordering
class IR(Sensor):
    """IR sensor class"""

    def get_reading(self):
        """Get distance from all IR beacons"""
        value = 0
        for item in self.sim.assets:
            if isinstance(item, Infrared):
                value += item.get_distance(self.position)
        return value

    def __float__(self):
        return self.get_reading()

    def __eq__(self, other):
        return float(self) == other

    def __lt__(self, other):
        return float(self) < other
