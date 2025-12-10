import time
import pygame
from background import Background
from block import Block
from config import (
    BIG_FONT_SIZE,
    BLACK,
    FONT,
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
from score_processor import ScoreProcessor


class TetrisGame:
    def __init__(self):
        self.background = Background()
        self.current_block = Block(self.background)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.score = 0
        self.speed = SPEED
        self.best_score = ScoreProcessor().get_score()

    def update(self) -> bool:
        game_over = self.current_block.move_down()
        self.check_lines(game_over)
        return game_over

    def handle_input(self):
        for event in pygame.event.get():
            # quit game
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                quit()
            # move block
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_block.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.current_block.move_right()
                elif event.key == pygame.K_DOWN:
                    self.current_block.move_down()
                elif event.key == pygame.K_UP:
                    self.current_block.rotate()

    def check_lines(self, game_over: bool):
        rows_to_remove = []
        if game_over:
            # remove all rows
            rows_to_remove = list(range(GRID_HEIGHT))
        else:
            for y in range(GRID_HEIGHT):
                # full row
                if all(color != BLACK for color in self.background.grid[y]):
                    rows_to_remove.append(y)
                    self.score += 1
                    if self.score > self.best_score:
                        self.best_score = self.score
                        ScoreProcessor().save_score(self.score)
        for y in rows_to_remove:
            # delete rows and add empty rows on top
            del self.background.grid[y]
            self.background.grid.insert(0, [BLACK] * GRID_WIDTH)

    def draw(self, game_over: bool):
        self.window.fill(BLACK)
        # render background
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pygame.draw.rect(
                    self.window,
                    self.background.grid[row][col],
                    (col * NODE_SIZE, row * NODE_SIZE, NODE_SIZE, NODE_SIZE),
                )
        # render current block
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
        self.draw_game_over(int(INDENT * 4), int(WINDOW_HEIGHT / 4))
        pygame.display.flip()
        time.sleep(3)
        self.__init__()

    def draw_score(self, x: int, y: int):
        font = pygame.font.Font(FONT, int(BIG_FONT_SIZE / 2))
        text = font.render(
            f"Score: {self.score}  Best score : {self.best_score}", True, WHITE
        )
        self.window.blit(text, (x, y))

    def draw_game_over(self, x: int, y: int):
        game_over_font = pygame.font.Font(FONT, int(BIG_FONT_SIZE))
        game_over_text = game_over_font.render("Game Over", True, RED)
        notification_font = pygame.font.Font(FONT, int(SMALL_FONT_SIZE))
        notification_text = notification_font.render(
            "Press Esc to quit or wait for the game to restart", True, WHITE
        )
        self.window.blit(game_over_text, (x, y))
        self.window.blit(
            notification_text, (SMALL_FONT_SIZE, WINDOW_HEIGHT - SMALL_FONT_SIZE)
        )

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_input()
            self.draw(self.update())
            clock.tick(self.speed)
