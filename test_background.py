import pytest
from background import Background
from config import GREEN, RED, SHAPES


# mocks block for test isolation
class MockBlock:
    def __init__(self, x, y):
        self.shape = SHAPES[0]
        self.color = GREEN
        self.x = x
        self.y = y


# test Background.lock_block method


def test_lock_block_places_color_on_grid():
    bg = Background()
    block = MockBlock(0, 0)
    bg.lock_block(block)

    assert bg.grid[0][0] == GREEN
    assert bg.grid[0][1] == GREEN
    assert bg.grid[0][2] == GREEN
    assert bg.grid[1][1] == GREEN


def test_lock_block_preserves_other_cells():
    bg = Background()
    bg.grid[0][0] = RED
    block = MockBlock(2, 2)
    bg.lock_block(block)

    # original cell should be unchanged
    assert bg.grid[0][0] == RED
    # new cell should be colored
    assert bg.grid[2][2] == GREEN
