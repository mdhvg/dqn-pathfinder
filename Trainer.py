from Map import Map
from collections import deque
from Model import Linear_QNet, QTrainer
from globals import Config
import numpy as np
import torch
import random
import os
import time

# Fitness function
# A = Distance from agent to goal
# B = Number of steps taken * 10
# C = Hitting a wall * 10
# D = Retrace steps * 10

# E = Reaching the goal * 100

# Fitness = E - (A + B + C + D)


# State array
# All states are binary
# A = If there is wall in right
# B = If there is wall down
# C = If there is wall in left
# D = If there is wall up

# E = If step in right is taken before
# F = If step down is taken before
# G = If step in left is taken before
# H = If step up is taken before

# I = If goal is in right direction
# J = If goal is down direction
# K = If goal is in left direction
# L = If goal is up direction

# [A, B, C, D, E, F, G, H, I, J, K, L]


class Trainer:
    def __init__(self, map: Map, config: Config) -> None:
        self.map = map
        self.map_original = map.copy()
        self.config = config
        self.trail: list[list[int]] = []
        self.grid: dict[tuple[int, int], str] = self.create_grid()

        self.epsilon = 0  # randomness
        self.gamma = 0.3  # discount rate
        # TODO: Move to config
        self.memory = deque(maxlen=self.config.model_max_memory)

        # try loading the model with the highest number in model/model_{number}.pth
        self.model = Linear_QNet(12, 256, 4)
        models = [
            int(i[6 : i.index(".")])
            for i in os.listdir("model")
            if i.startswith("model") and i.endswith(".pth")
        ]
        if models:
            model_num = max(models)
            self.model.load_state_dict(torch.load(f"model/model_{model_num}.pth"))
            print(f"Loaded model/model_{model_num}.pth")
        else:
            print("No model found, initializing new model")
        self.trainer = QTrainer(self.model, self.config.model_lr, self.gamma)

        self.stop = False
        self.randoms = 0
        self.retrace = 0
        self.wall_hit = 0
        self.last_dist = 0
        self.new_pos = self.map.agent.copy()

    def create_grid(self) -> dict[tuple[int, int], str]:
        grid = {}
        grid[(self.map.agent[0], self.map.agent[1])] = "Agent"
        grid[(self.map.goal[0], self.map.goal[1])] = "Goal"
        for wall in self.map.walls:
            grid[(wall[0], wall[1])] = "Wall"
        for trail in self.trail:
            grid[(trail[0], trail[1])] = "Trail"
        return grid

    def get_state(self) -> np.ndarray:
        agent = self.map.agent
        goal = self.map.goal

        state = np.array(
            [
                # Check right
                (
                    1
                    if (
                        (agent[0] + 1, agent[1]) in self.grid
                        and self.grid[(agent[0] + 1, agent[1])] == "Wall"
                    )
                    or agent[0] + 1 >= self.config.grid_width
                    else 0
                ),
                # Check down
                (
                    1
                    if (
                        (agent[0], agent[1] + 1) in self.grid
                        and self.grid[(agent[0], agent[1] + 1)] == "Wall"
                    )
                    or agent[1] + 1 >= self.config.grid_height
                    else 0
                ),
                # Check left
                (
                    1
                    if (
                        (agent[0] - 1, agent[1]) in self.grid
                        and self.grid[(agent[0] - 1, agent[1])] == "Wall"
                    )
                    or agent[0] - 1 < 0
                    else 0
                ),
                # Check up
                (
                    1
                    if (
                        (agent[0], agent[1] - 1) in self.grid
                        and self.grid[(agent[0], agent[1] - 1)] == "Wall"
                    )
                    or agent[1] - 1 < 0
                    else 0
                ),
                # Check right
                (
                    1
                    if (agent[0] + 1, agent[1]) in self.grid
                    and self.grid[(agent[0] + 1, agent[1])] == "Trail"
                    else 0
                ),
                # Check down
                (
                    1
                    if (agent[0], agent[1] + 1) in self.grid
                    and self.grid[(agent[0], agent[1] + 1)] == "Trail"
                    else 0
                ),
                # Check left
                (
                    1
                    if (agent[0] - 1, agent[1]) in self.grid
                    and self.grid[(agent[0] - 1, agent[1])] == "Trail"
                    else 0
                ),
                # Check up
                (
                    1
                    if (agent[0], agent[1] - 1) in self.grid
                    and self.grid[(agent[0], agent[1] - 1)] == "Trail"
                    else 0
                ),
                # Check right
                1 if goal[0] > agent[0] else 0,
                # Check down
                1 if goal[1] > agent[1] else 0,
                # Check left
                1 if goal[0] < agent[0] else 0,
                # Check up
                1 if goal[1] < agent[1] else 0,
            ],
            dtype=np.int32,
        )
        return state

    def get_fitness(self) -> int:
        goal = self.map.goal

        steps = len(self.trail)
        hit_wall = (
            1
            if (self.new_pos[0], self.new_pos[1]) in self.grid
            and self.grid[(self.new_pos[0], self.new_pos[1])] == "Wall"
            else 0
        ) * 10
        retrace = (
            1
            if (self.new_pos[0], self.new_pos[1]) in self.grid
            and self.grid[(self.new_pos[0], self.new_pos[1])] == "Trail"
            else 0
        ) * 1
        d0 = abs(self.new_pos[0] - goal[0]) + abs(self.new_pos[1] - goal[1]) * 1

        if_goal = 100 if d0 == 0 else -100

        return if_goal - (d0 + hit_wall + retrace)

    def get_action(self, state) -> int:

        self.epsilon = 80 - len(self.trail)
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            self.randoms += 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = int(torch.argmax(prediction).item())

        # state0 = torch.tensor(state, dtype=torch.float)
        # prediction = self.model(state0)
        # move = int(torch.argmax(prediction).item())

        return move

    def move(self, action: int) -> None:
        self.new_pos = self.map.agent.copy()
        if action == 0:
            self.new_pos[0] += 1
        elif action == 1:
            self.new_pos[1] += 1
        elif action == 2:
            self.new_pos[0] -= 1
        elif action == 3:
            self.new_pos[1] -= 1
        if self.new_pos[0] < 0 or self.new_pos[0] >= self.config.grid_width:
            return
        if self.new_pos[1] < 0 or self.new_pos[1] >= self.config.grid_height:
            return
        if (self.new_pos[0], self.new_pos[1]) in self.grid and self.grid[
            (self.new_pos[0], self.new_pos[1])
        ] == "Wall":
            self.wall_hit += 1
            return
        if (self.new_pos[0], self.new_pos[1]) in self.grid and self.grid[
            (self.new_pos[0], self.new_pos[1])
        ] == "Trail":
            self.retrace += 1
        self.map.agent = self.new_pos

    def step(self, action: int) -> tuple[int, bool]:
        self.trail.append(self.map.agent.copy())

        self.move(action)

        self.grid = self.create_grid()
        fitness = self.get_fitness()
        done = self.map.agent == self.map.goal
        return fitness, done

    def reset(self) -> None:
        self.map = self.map_original.copy()
        self.trail.clear()
        self.grid = self.create_grid()

    # TODO: Fix this part to make it fast
    # Implement everything in pytorch data structures
    def train_long_memory(self) -> None:
        if len(self.memory) > self.config.model_batch_size:
            mini_sample = random.sample(
                self.memory, self.config.model_batch_size
            )  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(
            np.array(states), actions, rewards, np.array(next_states), dones
        )
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def make_blob(self) -> None:
        blob = []

        for i in range(self.config.grid_height):
            row = ["_" for _ in range(self.config.grid_width)]
            blob.append(row)
        for wall in self.map.walls:
            blob[wall[1]][wall[0]] = "\033[30m#\033[0m"
        for trail in self.trail:
            blob[trail[1]][trail[0]] = "\033[35m*\033[0m"
        # for d, points in self.distances.items():
        #     for point in points:
        #         blob[point[1]][point[0]] = "\033[34mD\033[0m"
        blob[self.map.goal[1]][self.map.goal[0]] = "\033[33mX\033[0m"
        blob[self.map.agent[1]][self.map.agent[0]] = "\033[32mO\033[0m"

        for i in range(self.config.grid_height):
            blob[i] = "".join(blob[i])
            print(blob[i])

    def show(self) -> None:
        self.make_blob()

    def run(self) -> None:
        tries = 0
        reset = 0
        while not self.stop:
            init_state = self.get_state()
            action = self.get_action(init_state)

            fitness, done = self.step(action)
            state_new = self.get_state()

            # train short memory
            self.train_short_memory(init_state, action, fitness, state_new, done)

            # remember
            self.remember(init_state, action, fitness, state_new, done)

            tries += 1

            if tries % 500 == 0:
                self.train_long_memory()
                self.reset()

            if done:
                # self.train_long_memory()
                self.model.save()
                self.stop = True

            if tries > 10498:
                self.stop = True
            # break

        print(self.get_state())
        self.show()
        print(fitness)
        print("Tries", tries)
        print("Retraces", self.retrace)
        print("Wall hits", self.wall_hit)
        print("Resets", reset)
        print("Randoms", self.randoms)
        # self.reset()

        # game.reset()
        # self.n_games += 1
        # self.train_long_memory()

        # if score > record:
        #     record = score
        #     self.model.save()

        # print("Game", self.n_games, "Score", score, "Record:", record)

        # plot_scores.append(score)
        # total_score += score
        # mean_score = total_score / self.n_games
        # plot_mean_scores.append(mean_score)
        # plot(plot_scores, plot_mean_scores)
