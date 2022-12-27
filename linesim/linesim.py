"""
Simulates a track of black lines on a white
background along with a robot.
"""

import math
import os
import pygame


class LineSimulation:
    """
    Simulates a robot track
    """

    def __init__(self, start: tuple,
                 background=os.path.join(os.path.dirname(
                     os.path.abspath(__file__)), "assets/background.png")):
        """Initialize Game"""
        self.running = True

        # Load background
        self.background = pygame.image.load(
            background or os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/background.png"))
        self.size = self.background.get_size()

        # Initialize Window
        pygame.init()
        pygame.display.set_caption("Line Following")
        self.display = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.robot = Robot(start)

    def add_sensor(self, offset):
        sensor = Sensor(self, self.robot, offset)
        self.robot.sensors.append(sensor)
        return sensor

    def update(self, check_bounds=True):
        """Update simulation while checking for events"""
        # Check for quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return None

        # Quit game if robot leaves window
        if check_bounds and (
                (any(i - 30 < 0 for i in self.robot.position) or
                 any(map(lambda x, y: x + 30 > y, self.robot.position,
                         self.size)))):
            self.quit()
            return None

        # Quit game if robot touches red
        color = self.background.get_at(
            tuple(int(i) for i in self.robot.position))
        if color[0] > 230 and all(i < 50 for i in color[1:3]):
            self.quit()
            return None

        self.render()
        self.clock.tick(30)  # Max 30fps

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
        """Safe exit"""
        self.running = False
        pygame.quit()


class Robot:
    """Player class"""

    def __init__(self, start: tuple):
        """Initialize Robot"""
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/robot.png"))

        # Initialize position
        self.position = list(start)
        self.angle = 0

        self.sensors = []

    def move(self, speed):
        """Move robot forward"""
        self.position[0] += speed * math.cos(math.radians(self.angle))
        self.position[1] += speed * math.sin(math.radians(self.angle))

    def rotate(self, degrees):
        """Update robot rotation"""
        self.angle += degrees

    @property
    def surface(self) -> pygame.Surface:
        """Return rotated image"""
        return pygame.transform.rotate(self.image, -self.angle)


class Sensor:
    """Robot line sensor"""

    def __init__(self, sim: LineSimulation, robot: Robot,
                 offset: tuple):
        """Initialize sensor offset"""
        self.offset = offset
        self.robot = robot
        self.sim = sim

    def read_line(self, threshold=50):
        """
        Returns True if RGB value under sensor
        is under threshold (black line)
        """
        try:
            value = self.sim.background.get_at(self.position)
            return sum(value[:3]) < (threshold * 3)
        except IndexError:
            return False

    @property
    def position(self) -> tuple:
        """Calculate position of sensor"""
        return (int(self.robot.position[0] +
                    self.offset[0] * math.cos(math.radians(self.robot.angle)) -
                    self.offset[1] * math.sin(math.radians(self.robot.angle))),
                int(self.robot.position[1] +
                    self.offset[1] * math.cos(math.radians(self.robot.angle)) +
                    self.offset[0] * math.sin(math.radians(self.robot.angle))))

    @property
    def surface(self) -> pygame.Surface:
        """Sensor surface"""
        # Create surface
        image = pygame.Surface((5, 5))
        color = "#00ff00" if self.read_line() else "#ff0000"
        image.fill(pygame.Color(color))
        return image
