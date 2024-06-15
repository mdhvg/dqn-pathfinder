import os
import argparse
from MapEditor import MapEditor, Map
from globals import load_config, Config

modes = ["create", "load", "train", "test"]


def create_mode(args):
    config: Config = load_config(args.config)
    map = Map(args.name, config.grid_width, config.grid_height, config.map_dir)
    editor = MapEditor(map, config)
    editor.run()


def load_mode():
    print("Load mode")


def train_mode():
    print("Train mode")


def test_mode():
    print("Test mode")


def main():
    parser = argparse.ArgumentParser(
        description="Q-Learning pathfinding algorithm. Supports creating, loading, training, and testing maps"
    )
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument(
        "--config",
        type=str,
        default="config.ini",
        help="The path to the config file. Default: config.ini",
    )
    subparsers = parser.add_subparsers(
        dest="mode", help="Mode to run the script in", required=True
    )

    # Create mode
    create_parser = subparsers.add_parser(modes[0], help="Create a new map")
    create_parser.add_argument("--name", required=True, help="Name of the map")
    create_parser.set_defaults(func=create_mode)

    # Load mode
    load_parser = subparsers.add_parser(modes[1], help="Load a map for editing")
    load_parser.add_argument("--map", required=True, help="Path of the map")
    load_parser.set_defaults(func=load_mode)

    # Train mode
    train_parser = subparsers.add_parser(
        modes[2], help="Train the Q-Learning model on a map"
    )
    train_parser.add_argument("--map", required=True, help="Path of the map")
    train_parser.set_defaults(func=train_mode)

    # Test mode
    test_parser = subparsers.add_parser(
        modes[3], help="Test the Q-Learning model on a map"
    )
    test_parser.add_argument("--map", required=True, help="Path of the map")
    test_parser.set_defaults(func=test_mode)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
