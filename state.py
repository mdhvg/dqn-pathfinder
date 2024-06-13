import os
import json


class State:
    def __init__(
        self, name: str, grid_width: int, grid_height: int, dir: str = "states/"
    ):
        self.name = name
        self.agent: list[int] = [0, 0]
        self.goal: list[int] = [0, 0]
        self.walls: list[list[int]] = []
        self.grid_width = grid_width
        self.grid_height = grid_height
        if dir[-1] != "/":
            dir += "/"
        os.makedirs(dir, exist_ok=True)
        self.dir = dir
        self.state = {
            "name": self.name,
            "grid_width": grid_width,
            "grid_height": grid_height,
            "agent": self.agent,
            "goal": self.goal,
            "walls": [],
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
        self.state["agent"] = self.agent
        self.state["goal"] = self.goal
        self.state["walls"] = self.walls

    def save(self):
        filepath = f"{self.dir}{self.name}.json"
        tries = 1
        while os.path.exists(filepath):
            filepath = filepath[:-5] + f"_{tries}.json"
        with open(filepath, "w") as f:
            f.write(json.dumps(self.state, indent=4))


def load_state(filepath: str, grid_width: int, grid_height: int) -> State:
    state = State("", grid_width, grid_height)
    with open(filepath, "r") as f:
        state.state = json.loads(f.read())
    state.name = state.state["name"]
    state.agent = state.state["agent"]
    state.goal = state.state["goal"]
    state.walls = state.state["walls"]
    state.dir = os.path.dirname(filepath)

    if (
        state.state["grid_width"] != grid_width
        or state.state["grid_height"] != grid_height
    ):
        raise ValueError(
            f"The dimensions of the grid in state file do not match the dimensions of the grid.\nExpected: {grid_width}x{grid_height}\nGot: {state.state['grid_width']}x{state.state['grid_height']}"
        )

    return state
