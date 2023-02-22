"""Module defining various beacon classes"""

import math
import pygame


class Beacon:
    """Detectable beacon placed on track"""

    def __init__(self, sim, robot, position: tuple,
                 radius: int = 20):
        """Initialize position"""
        self.position = position
        self.robot = robot
        self.sim = sim
        self.radius = radius

    @property
    def surface(self) -> pygame.Surface:
        """Get beacon surface"""
        image = pygame.Surface((self.radius * 2,) * 2, pygame.SRCALPHA, 32)
        image.convert_alpha()
        pygame.draw.circle(image, "#ff0000", (self.radius,) * 2, self.radius,
                           1)
        pygame.draw.rect(image, "#000000",
                         (self.radius - 2, self.radius - 2, 4, 4))
        return image

    def get_distance(self, coordinates: tuple) -> float:
        """Return if location is within radius of beacon"""
        distance = math.sqrt((coordinates[0] - self.position[0]) ^ 2 +
                             (coordinates[1] - self.position[1]) ^ 2)

        if distance <= self.radius:
            return self.radius / distance
        return 0


class Magnet(Beacon):
    """Hall detectable beacon"""
