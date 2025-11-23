import pygame
import time
import random

from config import *

pygame.init()

score = 0  # TODO score reading and writing into file
grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")


class Block:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move_left(self):
        self.x -= 1
        if not self.is_valid_position():
            self.x += 1

    def move_right(self):
        self.x += 1
        if not self.is_valid_position():
            self.x -= 1

    def move_down(self):
        self.y += 1
        if not self.is_valid_position():
            self.y -= 1
            if self.y <= 0:
                return True
            else:
                self.lock()
                self.__init__()
        return False

    def rotate(self):
        old_shape = self.shape
        self.shape = list(zip(*reversed(self.shape)))
        if not self.is_valid_position():
            self.shape = old_shape

    def is_valid_position(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col] and (
                    self.x + col < 0
                    or self.x + col >= GRID_WIDTH
                    or self.y + row >= GRID_HEIGHT
                    or grid[self.y + row][self.x + col] != BLACK
                ):
                    return False
        return True

    def lock(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    grid[self.y + row][self.x + col] = self.color


class TetrisGame:
    def __init__(self):
        self.current_block = Block()
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
                if all(color != BLACK for color in grid[y]):
                    rows_to_remove.append(y)
                    self.score = self.score + 1
        for y in rows_to_remove:
            del grid[y]
            grid.insert(0, [BLACK] * GRID_WIDTH)

    def draw(self, game_over):
        window.fill(BLACK)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pygame.draw.rect(
                    window,
                    grid[row][col],
                    (col * NODE_SIZE, row * NODE_SIZE, NODE_SIZE, NODE_SIZE),
                )
        for row in range(len(self.current_block.shape)):
            for col in range(len(self.current_block.shape[row])):
                if self.current_block.shape[row][col]:
                    pygame.draw.rect(
                        window,
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
        window.fill(BLACK)
        self.draw_score(int(INDENT), int(WINDOW_HEIGHT / 2))
        self.draw_game_over(int(INDENT / 2), int(WINDOW_HEIGHT / 4))
        pygame.display.flip()
        time.sleep(3)
        self.__init__()

    def draw_score(self, x, y):
        font = pygame.font.Font("ARCADE.ttf", int(BIG_FONT_SIZE / 1.5))
        text = font.render(f"Score: {self.score}", True, WHITE)
        window.blit(text, (x, y))

    def draw_game_over(self, x, y):
        font = pygame.font.Font("ARCADE.ttf", int(BIG_FONT_SIZE))
        text = font.render("Game Over", True, RED)
        font2 = pygame.font.Font("ARCADE.ttf", int(SMALL_FONT_SIZE))
        text2 = font2.render(
            "Press Esc to quit or wait for the game to restart", True, WHITE
        )
        window.blit(text, (x, y))
        window.blit(text2, (SMALL_FONT_SIZE, WINDOW_HEIGHT - SMALL_FONT_SIZE))

    def run(self):
        while True:
            self.handle_input()
            self.draw(self.update())
            clock.tick(self.speed)


if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run()
