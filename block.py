import random

from background import Background
from config import BLACK, COLORS, GRID_HEIGHT, GRID_WIDTH, SHAPES


class Block:
    def __init__(self, background: Background):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.background = background

    def move_left(self):
        self.x -= 1
        if not self.is_valid_position():
            self.x += 1

    def move_right(self):
        self.x += 1
        if not self.is_valid_position():
            self.x -= 1

    def move_down(self) -> bool:
        self.y += 1
        if not self.is_valid_position():
            self.y -= 1
            if self.y <= 0:
                return True
            else:
                self.background.lock_block(self)
                self.__init__(self.background)
        return False

    def rotate(self):
        old_shape = self.shape
        self.shape = list(zip(*reversed(self.shape)))
        if not self.is_valid_position():
            self.shape = old_shape

    def is_valid_position(self) -> bool:
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] and (
                    self.x + col < 0
                    or self.x + col >= GRID_WIDTH
                    or self.y + row >= GRID_HEIGHT
                    or self.background.grid[self.y + row][self.x + col] != BLACK
                ):
                    return False
        return True
