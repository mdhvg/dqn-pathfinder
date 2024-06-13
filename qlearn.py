import pygame
import numpy as np
import random
import os
from globals import *
from widgets import Button, ImageButton

# Initialize pygame
pygame.init()

# Create the window
window = pygame.display.set_mode(window_size)

# Buttons
save_button = Button(
    grid_width - 100 - 10,
    grid_height + 10,
    100,
    30,
    (0, 255, 0),
    "Save",
    font,
    font_size,
)
wall_button = ImageButton(10, grid_height + 10, "images/wall.png", 30, 30)
agent_button = ImageButton(50, grid_height + 10, "images/agent.png", 30, 30)
goal_button = ImageButton(90, grid_height + 10, "images/goal.png", 30, 30)
clear_button = ImageButton(130, grid_height + 10, "images/clear.png", 30, 30)

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
