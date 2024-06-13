import pygame
import os


class Button:
    def __init__(
        self, x, y, width, height, color, text="", font: str | None = None, font_size=20
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        if font is not None and os.path.exists(font):
            self.font = pygame.font.Font(font, font_size)
        else:
            print(f"Warning: Font {font} not found, using default font")
            self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(
            center=(x + width / 2, y + height / 2)
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, x, y):
        return (
            self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        )


class ImageButton:
    def __init__(self, x, y, image, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, x, y):
        return self.rect.collidepoint(x, y)
