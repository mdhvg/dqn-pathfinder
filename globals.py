import configparser
import os
import pygame

# Set the working directory to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# Set the dimensions of the grid
grid_width = int(config["Grid"]["width"])
grid_height = int(config["Grid"]["height"])
cell_size = int(config["Grid"]["cell_size"])

# Set the font
font = config["Fonts"]["font"]
font_size = int(config["Fonts"]["font_size"])

# Set the size of the windoww
grid_width = grid_width * cell_size
grid_height = grid_height * cell_size
window_size = (grid_width, grid_height + 50)

# Load image
wall_image = pygame.image.load("images/wall.png")
agent_image = pygame.image.load("images/agent.png")
goal_image = pygame.image.load("images/goal.png")
clear_image = pygame.image.load("images/clear.png")
