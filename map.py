import os
import json

# Blob
# 1. Empty: _
# 2. Wall: #
# 3. Agent: O
# 4. Goal: X


class Map:
    def __init__(
        self, name: str, grid_width: int, grid_height: int, dir: str = "maps/"
    ):
        self.name = name
        self.agent: list[int] = [0, 0]
        self.goal: list[int] = [1, 1]
        self.walls: list[list[int]] = []
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.dir = dir
        self.map = {
            "name": self.name,
            "grid_width": grid_width,
            "grid_height": grid_height,
            "blob": [],
        }

    def __str__(self):
        return self.name

    def set_agent(self, agent: list[int] = [0, 0]):
        self.agent = agent

    def set_goal(self, goal: list[int] = [0, 0]):
        self.goal = goal

    def set_walls(self, walls: list[list[int]] = []):
        self.walls = walls

    def build(self):
        for i in range(self.grid_height):
            row = ["_" for _ in range(self.grid_width)]
            self.map["blob"].append(row)
        self.map["blob"][self.agent[1]][self.agent[0]] = "O"
        self.map["blob"][self.goal[1]][self.goal[0]] = "X"
        for wall in self.walls:
            self.map["blob"][wall[1]][wall[0]] = "#"
        for i in range(self.grid_height):
            self.map["blob"][i] = "".join(self.map["blob"][i])

    def save(self):
        self.build()
        filepath = f"{self.dir}{self.name}.json"
        with open(filepath, "w") as f:
            f.write(json.dumps(self.map, indent=4))


def load_map(filepath: str, grid_width: int, grid_height: int) -> Map:
    map = Map("", grid_width, grid_height)
    with open(filepath, "r") as f:
        map.map = json.loads(f.read())

    if map.map["grid_width"] != grid_width or map.map["grid_height"] != grid_height:
        raise ValueError(
            f"The dimensions of the grid in map file do not match the dimensions of the grid.\nExpected: {grid_width}x{grid_height}\nGot: {map.map['grid_width']}x{map.map['grid_height']}"
        )

    map.name = map.map["name"]

    for i in range(map.grid_height):
        for j in range(map.grid_width):
            if map.map["blob"][j][i] == "O":
                map.agent = [j, i]
            elif map.map["blob"][j][i] == "X":
                map.goal = [j, i]
            elif map.map["blob"][j][i] == "#":
                map.walls.append([j, i])

    map.dir = os.path.dirname(filepath)

    # Cleanup for saving memory
    map.map["blob"].clear()

    return map
