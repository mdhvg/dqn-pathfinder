import pygame
import numpy as np
import random
import os
from globals import *
from widgets import Button, ImageButton


class Mode:
    WALL = 0
    AGENT = 1
    GOAL = 2
    CLEAR = 3

    @staticmethod
    def get_name(mode: int) -> str:
        if mode == Mode.WALL:
            return "Wall"
        if mode == Mode.AGENT:
            return "Agent"
        if mode == Mode.GOAL:
            return "Goal"
        if mode == Mode.CLEAR:
            return "Clear"

        return "Unknown"

    # function to get the image of the mode
    @staticmethod
    def get_image(mode: int) -> pygame.Surface:
        if mode == Mode.WALL:
            return wall_image
        if mode == Mode.AGENT:
            return agent_image
        if mode == Mode.GOAL:
            return goal_image
        if mode == Mode.CLEAR:
            return clear_image

        return clear_image


# Game loop
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window
    window.fill((0, 0, 0))

    pygame.draw.rect(window, (255, 255, 255), (0, 0, grid_width, grid_height))

    # Draw the grid
    for x in range(0, grid_width, cell_size):
        for y in range(0, grid_height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(window, (200, 200, 200), rect, 1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # Draw the buttons
    save_button.draw(window)
    wall_button.draw(window)
    agent_button.draw(window)
    goal_button.draw(window)
    clear_button.draw(window)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
