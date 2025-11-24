import pygame

from tetris_game import TetrisGame

pygame.init()

score = 0  # TODO score reading and writing into file
pygame.display.set_caption("Tetris")

if __name__ == "__main__":
    tetris_game = TetrisGame(score)
    tetris_game.run()
