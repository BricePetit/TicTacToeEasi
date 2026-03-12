"""
This module contains the implementation of AI players for the Tic Tac Toe game, including a simple
random AI, an heuristic model, and a more complex Q-Learning AI. The Q-Learning AI can learn from
its interactions with the game environment and improve its performance over time. It also includes
functionality to save and load learned models, as well as to list available models for selection
in the game interface.
"""

__title__: str = "ai"
__version__: str = "1.0.0"
__author__: str = "Brice Petit"
__license__: str = "MIT"

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- IMPORTS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Imports standard libraries
import os
import pickle
import random

# Imports third party libraries

# Imports from src

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- CLASSES ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

class PlayerAI:
    """
    A simple AI that makes random moves.
    """
    def __init__(self, player: int, difficulty: str = "easy"):
        """
        Initializes the RandomAI with the specified player number.
        """
        self.player = player
        self.difficulty = difficulty

    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the difficulty level for the AI.

        :param difficulty: The difficulty level to set (e.g., "easy", "medium").
        """
        self.difficulty = difficulty

    def make_move(self, board: list) -> tuple:
        """
        Make a move on the board.

        :param board:   The current state of the game board.

        :return:        A tuple (row, col) representing the move made by the AI.
        """
        if self.difficulty == "easy":
            return self.random_move(board)
        elif self.difficulty == "medium":
            return self.heuristic_move(board)

    def random_move(self, board: list) -> tuple:
        """
        Make a random move on the board.

        :param board:   The current state of the game board.

        :return:        A tuple (row, col) representing the move made by the AI.
        """
        return random.choice(board.get_empty_cells())

    def heuristic_move(self, board: list) -> tuple:
        """
        Make a move based on a simple heuristic.

        :param board:   The current state of the game board.

        :return:        A tuple (row, col) representing the move made by the AI.
        """
        # Check if AI can win in the next move
        for cell in board.get_empty_cells():
            if board.is_winning_move(cell, self.player):
                return cell

        # Check if opponent can win in the next move and block it
        opponent = 1 if self.player == 2 else 2
        for cell in board.get_empty_cells():
            if board.is_winning_move(cell, opponent):
                return cell

        # Otherwise, make a random move
        return self.random_move(board)


class QLearningAI:
    """
    A placeholder for a Q-Learning AI implementation.
    """
    def __init__(self, player: int):
        self.player = player
        # Placeholder for Q-table and learning parameters
        self.q_table = {}
        # Learning hyperparameters
        # Learning rate (alpha), discount factor (gamma), and exploration rate (epsilon)
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.9

    def get_state(self, board: list) -> str:
        """
        Convert the current board state into a string representation for use as a key in
        the Q-table.

        :param board:   The current state of the game board.

        :return:        A string representation of the board state.
        """
        return str(board.board.flatten())

    def get_q_value(self, state: str, action: tuple) -> float:
        """
        Get the Q-value for a given state-action pair.

        :param state:   The current state of the game.
        :param action:  The action being evaluated.

        :return:        The Q-value for the state-action pair.
        """
        return self.q_table.get((state, action), 0.0)

    def make_move(self, board: list) -> tuple:
        """
        Make a move on the board using the learned Q-values (exploitation only, no exploration).

        :param board:   The current state of the game board.

        :return:        A tuple (row, col) representing the move made by the AI.
        """
        return self.choose_move(board)

    def choose_move(self, board: list) -> tuple:
        """
        Choose an action based on the current state of the board using an epsilon-greedy policy.

        :param board:   The current state of the game board.

        :return:        A tuple (row, col) representing the action chosen by the AI.
        """
        state = self.get_state(board)
        # Explore: choose a random action (epsilon-greedy)
        if random.random() < self.epsilon:
            return random.choice(board.get_empty_cells())
        # Exploit: choose the action with the highest Q-value
        q_values = {
            action: self.get_q_value(state, action) for action in board.get_empty_cells()
        }
        max_q = max(q_values.values())
        best_actions = [action for action, q in q_values.items() if q == max_q]
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state, next_actions) -> None:
        """
        Method to update the Q-table based on the action taken and the reward received.

        :param state:           The previous state of the game.
        :param action:          The action taken by the AI.
        :param reward:          The reward received after taking the action.
        :param next_state:      The new state of the game after taking the action.
        :param next_actions:    The possible actions in the new state.
        """
        old_q = self.get_q_value(state, action)
        max_next_q = max([self.get_q_value(next_state, a) for a in next_actions], default=0.0)
        # Q-learning update formula:
        # Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
        new_q = old_q + self.alpha * (reward + self.gamma * max_next_q - old_q)
        self.q_table[(state, action)] = new_q

    def save(self, model_name: str = "q_table") -> None:
        """
        Method to save the Q-table to a file using pickle.

        :param model_name: The name of the model file (without .pkl extension).
        """
        os.makedirs("QTables", exist_ok=True)
        filepath = f"QTables/{model_name}.pkl"
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)

    def load(self, model_name: str = "q_table") -> bool:
        """
        Method to load the Q-table from a file using pickle.

        :param model_name: The name of the model file (without .pkl extension).

        :return: True if the model was loaded successfully, False otherwise.
        """
        try:
            filepath = f"QTables/{model_name}.pkl"
            with open(filepath, "rb") as f:
                self.q_table = pickle.load(f)
            return True
        except FileNotFoundError:
            self.q_table = {}
            return False

    @staticmethod
    def list_models() -> list:
        """
        List all available Q-Learning models in the QTables directory.

        :return:    A list of model names (without .pkl extension).
        """
        models = []
        if os.path.exists("QTables"):
            for file in os.listdir("QTables"):
                if file.endswith(".pkl"):
                    models.append(file[:-4])
        return sorted(models)
