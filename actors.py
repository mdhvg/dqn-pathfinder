from globals import *
import pygame


class Rect:
    def __init__(
        self,
        x,
        y,
        w=1,
        h=1,
        color: tuple = (200, 200, 200),
        borderThickness: int = 1,
    ):
        self.x = x * cell_size
        self.y = y * cell_size
        self.w = w * cell_size
        self.h = h * cell_size
        self.fillColor = color
        self.borderThickness = borderThickness
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.fillColor, self.rect, self.borderThickness)


class Agent(Rect):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y, color=(0, 150, 0), borderThickness=0)

    def move(self, direction: int = 0):
        # 0 -> up
        # 1 -> right
        # 2 -> down
        # 3 -> left
        if direction == 0:
            self.y -= 1
        if direction == 1:
            self.x += 1
        if direction == 2:
            self.y += 1
        if direction == 3:
            self.x -= 1


class Wall(Rect):
    def __init__(self, x: int = 0, y: int = 0, width: int = 1, height: int = 1):
        super().__init__(x, y, width, height, color=(0, 0, 0), borderThickness=0)
