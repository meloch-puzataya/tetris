from random import random

from config import BLACK, COLORS, GRID_HEIGHT, GRID_WIDTH, SHAPES


class Background:
    def __init__(self):
        self.grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def lock_block(self, block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if block.shape[row][col]:
                    self.grid[block.y + row][block.x + col] = block.color
