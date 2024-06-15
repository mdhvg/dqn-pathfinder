import pygame
import os


class Button:
    def __init__(self, x, y, width, height, clickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pass

    def is_clicked(self, x, y):
        return self.rect.collidepoint(x, y)


class TextButton(Button):
    def __init__(self, x, y, width, height, color, font: pygame.font.Font, text=""):
        super().__init__(
            x,
            y,
            width,
            height,
        )
        self.color = color
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(
            center=(x + width / 2, y + height / 2)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)


class ImageButton(Button):
    def __init__(self, x, y, image, width, height):
        super().__init__(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
