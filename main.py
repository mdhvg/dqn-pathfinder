import os
import argparse
from MapEditor import MapEditor
from Map import Map, load_map, get_map_path
from globals import load_config, Config
from Trainer import Trainer

modes = ["map", "train", "test"]


def map_mode(args):
    config: Config = load_config(args.config)
    if os.path.exists(get_map_path(args.name, config.map_dir)):
        print("Loading existing map")
        map = load_map(
            get_map_path(args.name, config.map_dir),
            config.grid_width,
            config.grid_height,
        )
    else:
        map = Map(args.name, config.grid_width, config.grid_height, config.map_dir)
    editor = MapEditor(map, config)
    editor.run()


def train_mode(args):
    config: Config = load_config(args.config)
    if not os.path.exists(get_map_path(args.name, config.map_dir)):
        raise FileNotFoundError(f"Map {args.name} not found")
    map = load_map(
        get_map_path(args.name, config.map_dir),
        config.grid_width,
        config.grid_height,
    )
    trainer = Trainer(map, config)
    trainer.run()


def test_mode():
    print("Test mode")


def main():
    parser = argparse.ArgumentParser(
        description="Q-Learning pathfinding algorithm. Supports creating, loading, training, and testing maps"
    )
    parser.set_defaults(func=lambda args: parser.print_help())
    parser.add_argument("--name", required=True, help="Name of the map")
    parser.add_argument(
        "--config",
        type=str,
        default="config.ini",
        help="The path to the config file. Default: config.ini",
    )
    subparsers = parser.add_subparsers(
        dest="mode", help="Mode to run the script in", required=True
    )

    # Map mode
    map_parser = subparsers.add_parser(modes[0], help="Create or edit a map")
    map_parser.set_defaults(func=map_mode)

    # Train mode
    train_parser = subparsers.add_parser(
        modes[1], help="Train the Q-Learning model on a map"
    )
    train_parser.set_defaults(func=train_mode)

    # Test mode
    test_parser = subparsers.add_parser(
        modes[2], help="Test the Q-Learning model on a map"
    )
    test_parser.set_defaults(func=test_mode)

    args = parser.parse_args()
    args.func(args)

    # if option == 1:
    #     name = input("Enter the name of the map: ")
    #     width = int(input("Enter the width of the grid: "))
    #     height = int(input("Enter the height of the grid: "))
    #     map = Map(name, width, height)
    #     map.set_agent([0, 0])
    #     map.set_goal([width - 1, height - 1])
    #     map.build()
    #     map.save()
    # elif option == 2:
    #     maps = os.listdir("maps")
    #     for i, map in enumerate(maps):
    #         print(f"{i + 1}. {map[:-5]}")
    #     map = int(input("Select a map: ")) - 1
    #     map = load_map(f"maps/{maps[map]}", grid_width, grid_height)
    # elif option == 3:
    #     maps = os.listdir("maps")
    #     for i, map in enumerate(maps):
    #         print(f"{i + 1}. {map[:-5]}")
    #     map = int(input("Select a map: ")) - 1
    #     map = load_map(f"maps/{maps[map]}", grid_width, grid_height)
    #     qlearn = QLearn(map)
    #     qlearn.train()
    # elif option == 4:
    #     maps = os.listdir("maps")
    #     for i, map in enumerate(maps):
    #         print(f"{i + 1}. {map[:-5]}")
    #     map = int(input("Select a map: ")) - 1
    #     map = load_map(f"maps/{maps[map]}", grid_width, grid_height)
    #     qlearn = QLearn(map)
    #     qlearn.load()
    #     qlearn.test()
    # elif option == 5:
    #     exit()
    # else:
    #     print("Invalid option")
    #     exit()


if __name__ == "__main__":
    main()
