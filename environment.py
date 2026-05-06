import gymnasium as gym
from gymnasium import spaces
import numpy as np
import json

class DynamicChipEnv(gym.Env):

    def __init__(self, custom_data=None):
        super().__init__()

        if custom_data is None:
            with open("chip_input.json") as f:
                data = json.load(f)
        else:
            data = custom_data

        self.width, self.height = data["chip_size"]
        self.blocks = data["blocks"]
        self.connections = data["connections"]

        self.block_names = list(self.blocks.keys())

        self.action_space = spaces.Discrete(self.width * self.height)

        self.observation_space = spaces.Box(
            low=0, high=1,
            shape=(self.width, self.height),
            dtype=np.float32
        )

        self.reset()

    def reset(self, seed=None, options=None):
        self.layout = {}
        self.grid = np.zeros((self.width, self.height))
        self.current_block = 0
        return self.grid, {}

    # --------------------------------------------------
    # Correct Rectangle Overlap Check
    # --------------------------------------------------
    def legal_position(self, x, y, w, h):

        if x + w > self.width or y + h > self.height:
            return False

        for block_name, (bx, by) in self.layout.items():
            bw, bh = self.blocks[block_name]

            if not (x + w <= bx or
                    bx + bw <= x or
                    y + h <= by or
                    by + bh <= y):
                return False

        return True

    # --------------------------------------------------
    # Placement Step
    # --------------------------------------------------
    def step(self, action):

        x = action // self.width
        y = action % self.width   # FIXED

        block = self.block_names[self.current_block]
        w, h = self.blocks[block]

        reward = -1
        placed = False

        if self.legal_position(x, y, w, h):
            self.layout[block] = (x, y)
            reward += 20
            placed = True

        # Auto-legalization
        if not placed:
            for i in range(self.width):
                for j in range(self.height):
                    if self.legal_position(i, j, w, h):
                        self.layout[block] = (i, j)
                        placed = True
                        break
                if placed:
                    break

        if not placed:
            print(f"⚠ Could not place block {block}")

        self.current_block += 1
        done = self.current_block >= len(self.block_names)

        if done:
            reward -= self.total_wirelength() * 0.3

        return self.grid, reward, done, False, {}

    def total_wirelength(self):
        wl = 0
        for b1, b2 in self.connections:
            if b1 in self.layout and b2 in self.layout:
                x1, y1 = self.layout[b1]
                x2, y2 = self.layout[b2]
                wl += abs(x1 - x2) + abs(y1 - y2)
        return wl