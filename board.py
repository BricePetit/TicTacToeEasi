"""
In this module, we define the Board class, which represents the game board for a tictactoe game.
The Board class provides methods for initializing the board, making moves, checking for wins,
and displaying the current state of the board. It serves as the core component for managing the
game state and facilitating interactions between players.
"""

__title__: str = "board"
__version__: str = "1.0.0"
__author__: str = "Brice Petit"
__license__: str = "MIT"

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- IMPORTS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Imports standard libraries
from typing import NoReturn

# Imports third party libraries
import numpy as np

# Imports from src
from constants import *

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- CLASSES ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

class Board:
    """
    Class representing the game board for tic-tac-toe.
    """
    def __init__(self):
        """
        Initializes the game board as a 2D list filled with empty spaces.
        """
        self.board = np.zeros((ROW, COL), dtype=int)

    def mark_cell(self, row: int, col: int, player: int) -> NoReturn:
        """
        Method to mark a cell on the board. It updates the board with the player's mark at the
        specified row and column.

        :param row:     The row index where the player wants to make a move.
        :param col:     The column index where the player wants to make a move.
        :param player:  The player number (1 or 2) making the move.
        """
        self.board[row][col] = player

    def is_full(self) -> bool:
        """
        Method to check if the board is full, meaning there are no 0 values left.

        :return:    True if the board is full, False otherwise.
        """
        return not np.any(self.board == EMPTY)

    def is_empty_cell(self, row: int, col: int) -> bool:
        """
        Method to check if a specific cell on the board is empty.

        :param row: The row index of the cell to check.
        :param col: The column index of the cell to check.

        :return:    True if the cell is empty, False otherwise.
        """
        return self.board[row][col] == EMPTY

    def get_empty_cells(self) -> list:
        """
        Method to get a list of empty cells on the board.

        :return:    A list of tuples representing the row and column indices of empty cells.
        """
        empty_cells = []
        for row in range(ROW):
            for col in range(COL):
                if self.board[row][col] == EMPTY:
                    empty_cells.append((row, col))
        return empty_cells

    def check_win(self, player: int) -> bool:
        """
        Method to check if the specified player has won the game by having three of their marks in
        a row, column, or diagonal.

        :param player:  The player number (1 or 2) to check for a win.

        :return:        True if the player has won, False otherwise.
        """
        # Check for a win in rows.
        for row in range(ROW):
            if np.all(self.board[row] == player):
                return True
        # Check for a win in columns.
        for col in range(COL):
            if np.all(self.board[:, col] == player):
                return True
        # Check the main diagonal.
        if np.all(np.diag(self.board) == player):
            return True
        # Check the anti-diagonal.
        if np.all(np.diag(np.fliplr(self.board)) == player):
            return True
        # If no win condition is met, return False.
        return False

    def is_winning_move(self, cell: tuple, player: int) -> bool:
        """
        Method to check if placing a mark in the specified cell would result in a win for the
        given player.

        :param cell:    A tuple (row, col) representing the cell to check.
        :param player:  The player number (1 or 2) to check for a winning move.

        :return:        True if placing a mark in the cell would result in a win, False otherwise.
        """
        row, col = cell
        # Temporarily mark the cell for the player.
        self.board[row][col] = player
        # Check if this move wins the game.
        win = self.check_win(player)
        # Reset the cell back to empty.
        self.board[row][col] = EMPTY
        return win
