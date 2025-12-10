import pygame

from tetris_game import TetrisGame

pygame.init()
pygame.display.set_caption("Tetris")

if __name__ == "__main__":
    tetris_game = TetrisGame()
    tetris_game.run()
