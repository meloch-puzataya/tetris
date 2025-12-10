import pytests
from block import Block
from background import Background
from config import GRID_HEIGHT, GRID_WIDTH, RED


# test Block movement methods


def test_move_left_decreases_x():
    bg = Background()
    block = Block(bg)
    initial_x = block.x
    block.move_left()
    assert block.x < initial_x


def test_move_right_increases_x():
    bg = Background()
    block = Block(bg)
    initial_x = block.x
    block.move_right()
    assert block.x > initial_x


def test_move_down_increases_y():
    bg = Background()
    block = Block(bg)
    initial_y = block.y
    block.move_down()
    assert block.y > initial_y


def test_move_left_at_left_boundary():
    bg = Background()
    block = Block(bg)
    block.x = 0
    block.move_left()
    assert block.x == 0


def test_move_right_at_right_boundary():
    bg = Background()
    block = Block(bg)
    block.x = GRID_WIDTH - 1
    block.move_right()
    assert block.x == GRID_WIDTH - 1


# test Block rotation


def test_rotate_at_center_position():
    bg = Background()
    block = Block(bg)
    block.x = 2
    block.y = 7
    original_x = block.x
    original_y = block.y
    block.rotate()

    # Position should not change
    assert block.x == original_x
    assert block.y == original_y


# test Block position validation


def test_is_valid_position_at_center():
    bg = Background()
    block = Block(bg)
    assert block.is_valid_position() is True


def test_is_valid_position_left_boundary_violation():
    bg = Background()
    block = Block(bg)
    block.x = -1
    assert block.is_valid_position() is False


def test_is_valid_position_right_boundary_violation():
    bg = Background()
    block = Block(bg)
    block.x = GRID_WIDTH
    assert block.is_valid_position() is False


def test_is_valid_position_bottom_boundary_violation():
    bg = Background()
    block = Block(bg)
    block.y = GRID_HEIGHT
    assert block.is_valid_position() is False


def test_is_valid_position_with_filled_cell():
    bg = Background()
    bg.grid[5][5] = RED

    block = Block(bg)
    block.x = 5
    block.y = 5

    result = block.is_valid_position()
    assert result is False


# test Block collision detection


def test_move_left_blocked_by_wall():
    bg = Background()
    block = Block(bg)
    block.x = 0
    initial_x = block.x
    block.move_left()
    assert block.x == initial_x


def test_move_right_blocked_by_wall():
    bg = Background()
    block = Block(bg)
    block.x = GRID_WIDTH - 1
    initial_x = block.x
    block.move_right()
    assert block.x == initial_x


def test_move_down_passes():
    bg = Background()
    block = Block(bg)
    game_over = block.move_down()
    assert game_over is False


def test_move_down_ends_game():
    bg = Background()
    block = Block(bg)
    block.shape = [[1]]
    bg.grid[1][block.x] = RED
    game_over = block.move_down()
    assert game_over is True
