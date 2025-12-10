from block import Block
from config import BLACK, GRID_HEIGHT, GRID_WIDTH


class Background:
    def __init__(self):
        self.grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    # add block to the background, so it's no longer active
    def lock_block(self, block: Block):
        for row in range(len(block.shape)):
            for col in range(len(block.shape[row])):
                if block.shape[row][col]:
                    self.grid[block.y + row][block.x + col] = block.color
