"""Module defining various beacon classes"""

import math
import pygame


class Beacon:
    """Detectable beacon placed on track"""

    def __init__(self, position: tuple, radius: int = 20,
                 color: str = "#ff0000"):
        """Initialize beacon

        :param position: The beacon's position on the board.
        :type position: tuple
        :param radius: The effect radius of the beacon
        :type radius: int, optional
        """
        self.position = position
        self.radius = radius
        self.color = color

    @property
    def surface(self) -> pygame.Surface:
        """Get beacon surface"""
        image = pygame.Surface((self.radius * 2,) * 2, pygame.SRCALPHA, 32)
        image.convert_alpha()
        pygame.draw.circle(image, self.color, (self.radius,) * 2, self.radius,
                           1)
        pygame.draw.rect(image, "#000000",
                         (self.radius - 2, self.radius - 2, 4, 4))
        return image

    def get_distance(self, coordinates: tuple) -> float:
        """Return power law representation of distance from sensor

        :param coordinates: Coordinates of location to check
        :type coordinates: tuple
        :return: The radius of the sensor divided by the distance from it
        :rtype: float
        """
        distance = math.sqrt((coordinates[0] - self.position[0]) ** 2 +
                             (coordinates[1] - self.position[1]) ** 2)

        if distance <= self.radius:
            return self.radius / distance
        return 0.0


class Magnet(Beacon):
    """Hall detectable beacon"""
    def __init__(self, position: tuple):
        super().__init__(position, 20, "#00ff00")


class Infrared(Beacon):
    """IR detectable beacon"""
    def __init__(self, position: tuple):
        super().__init__(position, 80, "#ff0000")
