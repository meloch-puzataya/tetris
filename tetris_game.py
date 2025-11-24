import time
import pygame
from background import Background
from block import Block
from config import (
    BIG_FONT_SIZE,
    BLACK,
    GRID_HEIGHT,
    GRID_WIDTH,
    INDENT,
    NODE_SIZE,
    RED,
    SMALL_FONT_SIZE,
    SPEED,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    SPEED,
)


class TetrisGame:
    def __init__(self, score):
        self.background = Background()
        self.current_block = Block(self.background)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.score = score
        self.speed = SPEED

    def update(self):
        game_over = self.current_block.move_down()
        self.check_lines(game_over)
        return game_over

    def handle_input(self):
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_block.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.current_block.move_right()
                elif event.key == pygame.K_DOWN:
                    self.current_block.move_down()
                elif event.key == pygame.K_UP:
                    self.current_block.rotate()

    def check_lines(self, game_over):
        rows_to_remove = []
        if game_over:
            for i in range(GRID_HEIGHT):
                rows_to_remove.append(i)
        else:
            for y in range(GRID_HEIGHT):
                if all(color != BLACK for color in self.background.grid[y]):
                    rows_to_remove.append(y)
                    self.score = self.score + 1
        for y in rows_to_remove:
            del self.background.grid[y]
            self.background.grid.insert(0, [BLACK] * GRID_WIDTH)

    def draw(self, game_over):
        self.window.fill(BLACK)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pygame.draw.rect(
                    self.window,
                    self.background.grid[row][col],
                    (col * NODE_SIZE, row * NODE_SIZE, NODE_SIZE, NODE_SIZE),
                )
        for row in range(len(self.current_block.shape)):
            for col in range(len(self.current_block.shape[row])):
                if self.current_block.shape[row][col]:
                    pygame.draw.rect(
                        self.window,
                        self.current_block.color,
                        (
                            (self.current_block.x + col) * NODE_SIZE,
                            (self.current_block.y + row) * NODE_SIZE,
                            NODE_SIZE,
                            NODE_SIZE,
                        ),
                    )
        if not game_over:
            self.draw_score(INDENT, 0)
        else:
            self.reset()
        pygame.display.flip()

    def reset(self):
        self.window.fill(BLACK)
        self.draw_score(int(INDENT), int(WINDOW_HEIGHT / 2))
        self.draw_game_over(int(INDENT / 2), int(WINDOW_HEIGHT / 4))
        pygame.display.flip()
        time.sleep(3)
        self.__init__()

    def draw_score(self, x, y):
        font = pygame.font.Font("ARCADE.ttf", int(BIG_FONT_SIZE / 1.5))
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.window.blit(text, (x, y))

    def draw_game_over(self, x, y):
        font = pygame.font.Font("ARCADE.ttf", int(BIG_FONT_SIZE))
        text = font.render("Game Over", True, RED)
        font2 = pygame.font.Font("ARCADE.ttf", int(SMALL_FONT_SIZE))
        text2 = font2.render(
            "Press Esc to quit or wait for the game to restart", True, WHITE
        )
        self.window.blit(text, (x, y))
        self.window.blit(text2, (SMALL_FONT_SIZE, WINDOW_HEIGHT - SMALL_FONT_SIZE))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_input()
            self.draw(self.update())
            clock.tick(self.speed)
