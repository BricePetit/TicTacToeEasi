"""
Main entry point for the game.
"""

__title__: str = "main"
__version__: str = "1.0.0"
__author__: str = "Brice Petit"
__license__: str = "MIT"

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- IMPORTS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Imports standard libraries
import os

# Imports third party libraries
import pygame

# Imports from src
from constants import *
from game import Game

# ----------------------------------------------------------------------------------------------- #
# ---------------------------------------- MAIN FUNCTION ---------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

def main():
    """
    Main function to run the game
    """
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    while True:
        game = Game(screen)
        game.select_circles_crosses_menu()
        game.select_difficulty_menu()
        game.play_game()
        del game


if __name__ == "__main__":
    main()
