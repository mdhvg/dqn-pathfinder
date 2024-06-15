import configparser
import os
import pygame

# Set the working directory to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Config:
    grid_width: int
    grid_height: int
    window_width: int
    window_height: int
    cell_size: int
    font: str
    font_size: int
    window_size: tuple[int, int]
    map_dir: str = "maps/"


def load_config(path: str = "config.ini") -> Config:
    # Read the config file
    configFile = configparser.ConfigParser()
    configFile.read("config.ini")
    config = Config()
    config.cell_size = int(configFile["Grid"]["cell_size"])
    config.grid_width = int(configFile["Grid"]["width"])
    config.grid_height = int(configFile["Grid"]["height"])
    config.window_width = config.grid_width * config.cell_size
    config.window_height = config.grid_height * config.cell_size
    config.font = configFile["Fonts"]["font"]
    config.font_size = int(configFile["Fonts"]["font_size"])
    config.window_size = (
        config.window_width,
        config.window_height + 50,
    )
    config.map_dir = configFile["Files"]["map_dir"]
    if config.map_dir[-1] != "/":
        config.map_dir += "/"
    os.makedirs(config.map_dir, exist_ok=True)
    return config


# Load image
