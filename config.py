# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (165, 0, 255)
PINK = (255, 50, 165)
COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, PURPLE, ORANGE, PINK]

# tetromino shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

# window settings
WINDOW_WIDTH, WINDOW_HEIGHT = 300, 600
BIG_FONT_SIZE = WINDOW_WIDTH // 6
SMALL_FONT_SIZE = WINDOW_WIDTH // 24
INDENT = int(BIG_FONT_SIZE * 1.8)
NODE_SIZE = 20  # node size in grid
GRID_WIDTH, GRID_HEIGHT = WINDOW_WIDTH // NODE_SIZE, WINDOW_HEIGHT // NODE_SIZE
SPEED = 5
