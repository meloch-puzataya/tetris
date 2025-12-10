import random

from config import BLACK, COLORS, GRID_HEIGHT, GRID_WIDTH, SHAPES


class Block:
    def __init__(self, background):
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
                # canvas is filled game over
                return True
            else:
                # lock block in the background
                self.background.lock_block(self)
                # reset to new block
                self.__init__(self.background)
        # successful move down
        return False

    def rotate(self):
        old_shape = self.shape
        # rotate shape clockwise
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
