import numpy as np

class MultiLayerRouter:

    def __init__(self, width, height, layers=4):
        self.width = width
        self.height = height
        self.layers = layers
        self.grid = np.zeros((layers, width, height))

    def route(self, start, end):

        x1, y1 = start
        x2, y2 = end

        # Metal 1 (horizontal)
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.grid[0][x][y1] += 1

        # Metal 2 (vertical)
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.grid[1][x2][y] += 1

    def congestion_map(self):
        return np.sum(self.grid, axis=0) / self.layers