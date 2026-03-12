"""
Module to define the game class. The game class manages the player and AI moves and turn during the
game. It also provides a method to reset the game to its initial state. The Game class interacts
with the Board class to update the game state and with the RandomAI class to determine the AI's
moves.
"""

__title__: str = "game"
__version__: str = "1.0.0"
__author__: str = "Brice Petit"
__license__: str = "MIT"

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- IMPORTS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Imports standard libraries
import time

# Imports third party libraries
import pygame

# Imports from src
from ai import PlayerAI, QLearningAI
from board import Board
from constants import *

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- CLASSES ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

class Game:
    """
    Class representing the tic-tac-toe game. It manages the game state, player and AI moves, and
    handles user input and game events. The Game class interacts with the Board class to update the
    game state and with the RandomAI class to determine the AI's moves. It also provides
    functionality to reset the game and display the game board and symbols on the screen.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the Game class with the provided Pygame screen surface. It sets up the game
        board, initializes the current player, and creates an instance of the PlayerAI for the AI
        opponent.

        :param screen:  The Pygame surface on which the game will be drawn.
        """
        self.screen = screen
        self.board = Board()
        self.current_player = PLAYER
        self.player_symbol = None
        self.ai = PlayerAI(AI, "medium")
        self.ai_type = "player"
        self.ai_symbol = None
        self.winner = None
        self.want_to_quit = False
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    def reset(self) -> None:
        """
        Method to reset the game to its initial state. It reinitializes the board by creating a new
        Board instance, resets the current player to PLAYER, and resets the winner.
        """
        self.board = Board()
        self.current_player = PLAYER
        self.winner = None

    def player_move(self, row: int, col: int) -> bool:
        """
        Method to handle the player's move. It checks if the selected cell is empty and if so,
        marks the cell with the player's value (1) and switches the current player to AI.

        :param row: The row index where the player wants to make a move.
        :param col: The column index where the player wants to make a move.

        :return:    True if the move was successful, False if the cell was not empty.
        """
        if self.board.is_empty_cell(row, col):
            self.board.mark_cell(row, col, PLAYER)
            self.current_player = AI
            return True
        return False

    def ai_move(self):
        """
        Method to handle the AI's move. It uses the AI's make_move method to get a random move and
        marks the cell with the AI's value (2). After making the move, it switches the current
        player back to PLAYER.
        """
        if self.board.get_empty_cells():
            row, col = self.ai.make_move(self.board)
            self.board.mark_cell(row, col, AI)
            self.current_player = PLAYER

    def game_catch_events(self) -> None:
        """
        Method to catch and handle game events such as quitting the game, resetting the game, and
        making player moves. It listens for Pygame events and responds accordingly based on the type
        of event detected.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.want_to_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                    self.want_to_quit = True
            # Check for mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if it's the player's turn before allowing them to make a move and if there
                # is no winner yet
                if not self.winner:
                    x, y = event.pos
                    # Check if the click is within the game board area (below the UI area) before
                    # allowing the player to make a move
                    if y < UI_HEIGHT:
                        continue
                    # Calculate row and column indices based on the click
                    col = x // SQUARE_SIZE
                    row = (y - UI_HEIGHT) // SQUARE_SIZE
                    # Do the player move
                    if self.player_move(row, col):
                        if self.board.check_win(PLAYER):
                            self.winner = PLAYER
                        elif self.board.is_full():
                            self.winner = "draw"
                        # Do the AI move
                        if not self.winner:
                            self.ai_move()
                            if self.board.check_win(AI):
                                self.winner = AI
                            elif self.board.is_full():
                                self.winner = "draw"

    def play_game(self) -> None:
        """
        Method to start and manage the game loop. It continuously updates the game state, draws
        the game board and symbols, and checks for user input until the player decides to quit the
        game.
        """
        while not self.want_to_quit:
            self.screen.fill((0,0,0))
            # Draw the player and AI symbols
            self.draw_text("Player: " + self.player_symbol, 10, 10)
            self.draw_text("AI: " + self.ai_symbol, 10, 50)
            # Draw the reset instruction
            self.draw_text("Press <r> to reset the game", 10, 90)
            self.draw_text("Press <escape> to quit the game", 10, 130)
            # Display the winner if there is one
            if self.winner == PLAYER:
                self.draw_text("Player wins!", 10, 170)
            elif self.winner == AI:
                self.draw_text("AI wins!", 10, 170)
            elif self.winner == "draw":
                self.draw_text("It's a draw!", 10, 170)
            # Draw the game board and the symbols on the board
            self.draw_board()
            self.draw_figures()
            # Update the display after drawing everything
            pygame.display.flip()
            # Catch events after updating the display to ensure the game responds to user input
            self.game_catch_events()

    def select_circles_crosses_menu(self) -> None:
        """
        Method to display the player symbol selection menu. It allows the player to choose between
        "X" and "O" symbols before starting the game.
        """
        self.screen.fill((0,0,0))
        self.draw_text("Press <x> to play the crosses", WIDTH//2, HEIGHT//2 - 50, True)
        self.draw_text("Press <o> to play the circles", WIDTH//2, HEIGHT//2 + 50, True)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        self.player_symbol = "X"
                        self.ai_symbol = "O"
                        return
                    if event.key == pygame.K_o:
                        self.player_symbol = "O"
                        self.ai_symbol = "X"
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    def select_difficulty_menu(self) -> None:
        """
        Method to display the difficulty selection menu. It allows the player to choose between
        "easy", "medium", and "hard" difficulty levels for the AI opponent before starting the game.
        "easy" and "medium" use PlayerAI, "hard" uses QLearningAI.
        """
        self.screen.fill((0,0,0))
        self.draw_text(
            "Press <e> for easy difficulty (Random moves)", WIDTH//2, HEIGHT//2 - 100, True
        )
        self.draw_text(
            "Press <m> for medium difficulty (Heuristic)", WIDTH//2, HEIGHT//2 - 20, True
        )
        self.draw_text(
            "Press <h> for hard difficulty (Q-Learning)", WIDTH//2, HEIGHT//2 + 60, True
        )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.ai = PlayerAI(AI, "easy")
                        self.ai_type = "player"
                        return
                    if event.key == pygame.K_m:
                        self.ai = PlayerAI(AI, "medium")
                        self.ai_type = "player"
                        return
                    if event.key == pygame.K_h:
                        self.ai = QLearningAI(AI)
                        self.ai.load()
                        self.ai_type = "qlearning"
                        self.train_or_play_menu()
                        return

    def train_or_play_menu(self) -> None:
        """
        Menu to ask the user what they want to do with Q-Learning AI.
        Options: Load existing model, Train new model, or Play with default.
        """
        models = QLearningAI.list_models()
        self.screen.fill((0,0,0))
        self.draw_text("Q-Learning AI selected", WIDTH//2, HEIGHT//2 - 150, True)
        if models:
            self.draw_text("Available models found!", WIDTH//2, HEIGHT//2 - 80, True)
            self.draw_text("Press <l> to load an existing model", WIDTH//2, HEIGHT//2, True)
            self.draw_text("Press <t> to train a new model", WIDTH//2, HEIGHT//2 + 60, True)
            self.draw_text("Press <p> to play with default model", WIDTH//2, HEIGHT//2 + 120, True)
        else:
            self.draw_text("No saved models found", WIDTH//2, HEIGHT//2 - 50, True)
            self.draw_text(
                "Press <t> to train the AI (recommended)", WIDTH//2, HEIGHT//2 + 30, True
            )
            self.draw_text(
                "Press <p> to play with default", WIDTH//2, HEIGHT//2 + 90, True
            )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l and models:
                        self.select_model_menu(models)
                        return
                    if event.key == pygame.K_t:
                        self.train_qlearning_ai()
                        return
                    if event.key == pygame.K_p:
                        # Load default model if available, otherwise use untrained
                        if "q_table" in models:
                            self.ai.load("q_table")
                        return

    def select_model_menu(self, models: list) -> None:
        """
        Menu to select which model to load.

        :param models: List of available model names.
        """
        selected_index = 0
        while True:
            self.screen.fill((0,0,0))
            self.draw_text("Select a model to load", WIDTH//2, HEIGHT//2 - 150, True)
            # Display all models with selection highlight
            for i, model in enumerate(models):
                y_pos = HEIGHT//2 - 50 + i * 50
                prefix = "> " if i == selected_index else "  "
                self.draw_text(f"{prefix}{model}", WIDTH//2, y_pos, True)
            self.draw_text(
                "Use <arrow Up/Down> to navigate, <enter> to select", WIDTH//2, HEIGHT - 100, True
            )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(models)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(models)
                    elif event.key == pygame.K_RETURN:
                        self.ai.load(models[selected_index])
                        return

    def train_qlearning_ai(self, episodes: int = 1000000) -> None:
        """
        Method to train the Q-Learning AI by playing against a heuristic opponent for a specified
        number of episodes. The training progress is displayed with a progress bar and statistics
        on the screen. After training is complete, the user is prompted to save the trained model.

        :param episodes:    The number of training episodes to run.
        """
        ai = self.ai
        heuristic_ai = PlayerAI(PLAYER, difficulty="medium")
        start_time = time.time()
        for episode in range(1, episodes + 1):
            board = Board()
            # Decay epsilon over time to reduce exploration as training progresses
            ai.epsilon = 0.9 * (1 - episode / episodes)
            current_player = PLAYER
            while True:
                empty_cells = board.get_empty_cells()
                if not empty_cells:
                    # Draw - no reward
                    break
                if current_player == AI:
                    # Q-Learning AI plays
                    state = ai.get_state(board)
                    action = ai.choose_move(board)
                    row, col = action
                    board.mark_cell(row, col, AI)
                    if board.check_win(AI):
                        # Q-Learning AI wins - reward
                        next_state = ai.get_state(board)
                        ai.update(state, action, 1, next_state, [])
                        break
                    next_state = ai.get_state(board)
                    next_actions = board.get_empty_cells()
                    ai.update(state, action, 0, next_state, next_actions)
                else:
                    # Heuristic AI plays
                    action = heuristic_ai.make_move(board)
                    row, col = action
                    board.mark_cell(row, col, PLAYER)
                    if board.check_win(PLAYER):
                        # Heuristic AI wins
                        break
                current_player = PLAYER if current_player == AI else AI
            # Update progress bar every 0.1% of episodes
            if episode % max(1, episodes // 1000) == 0:
                self.draw_training_progress(episode, episodes, start_time)
        # Final update - show 100%
        elapsed_time = time.time() - start_time
        self.screen.fill((0, 0, 0))
        self.draw_text(f"Training Complete!", WIDTH//2, HEIGHT//2 - 100, True)
        self.draw_progress_bar(episodes, episodes)
        self.draw_text(f"Episodes: {episodes}", WIDTH//2, HEIGHT//2 + 100, True)
        self.draw_text(f"Time: {elapsed_time:.1f}s", WIDTH//2, HEIGHT//2 + 150, True)
        self.draw_text(f"Q-table size: {len(ai.q_table)}", WIDTH//2, HEIGHT//2 + 200, True)
        self.draw_text("Press any key to continue...", WIDTH//2, HEIGHT//2 + 280, True)
        pygame.display.flip()
        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
        # Ask for model name
        self.save_model_dialog(ai)

    def draw_training_progress(self, current: int, total: int, start_time) -> None:
        """
        Draw the training progress screen with a progress bar.

        :param current:     Current episode number.
        :param total:       Total number of episodes.
        :param start_time:  Time when training started (for ETA calculation).
        """
        self.screen.fill((0, 0, 0))
        self.draw_text("Training Q-Learning AI...", WIDTH//2, HEIGHT//2 - 150, True)
        # Progress bar
        self.draw_progress_bar(current, total)
        # Statistics
        percentage = (current / total) * 100
        elapsed_time = time.time() - start_time
        if current > 0:
            avg_time = elapsed_time / current
            eta = (total - current) * avg_time
        else:
            eta = 0
        self.draw_text(
            f"Progress: {current}/{total} ({percentage:.1f}%)", WIDTH//2, HEIGHT//2 + 100, True
        )
        self.draw_text(
            f"Elapsed: {elapsed_time:.1f}s | ETA: {eta:.1f}s", WIDTH//2, HEIGHT//2 + 150, True
        )
        pygame.display.flip()

    def draw_progress_bar(self, current: int, total: int) -> None:
        """
        Draw a progress bar on the screen.

        :param current: Current progress value.
        :param total:   Total progress value.
        """
        # Progress bar dimensions.
        bar_x = (WIDTH - PROGRESS_BAR_WIDTH) // 2
        bar_y = HEIGHT // 2
        # Draw background
        pygame.draw.rect(
            self.screen, PROGRESS_BAR_BG, (bar_x, bar_y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT)
        )
        # Draw fill
        if total > 0:
            fill_width = int((current / total) * PROGRESS_BAR_WIDTH)
        else:
            fill_width = 0
        pygame.draw.rect(
            self.screen, PROGRESS_BAR_FILL, (bar_x, bar_y, fill_width, PROGRESS_BAR_HEIGHT)
        )
        # Draw border
        pygame.draw.rect(
            self.screen, (255, 255, 255), (bar_x, bar_y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), 2
        )

    def save_model_dialog(self, ai: QLearningAI) -> None:
        """
        Dialog to allow the user to name and save the trained model.

        :param ai: The QLearningAI instance to save.
        """
        model_name = "q_table"
        typing = True
        while typing:
            self.screen.fill((0, 0, 0))
            self.draw_text("Save Model", WIDTH//2, HEIGHT//2 - 150, True)
            self.draw_text("Enter a name for the model:", WIDTH//2, HEIGHT//2 - 50, True)
            # Draw the input field
            input_box_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 40)
            pygame.draw.rect(self.screen, (200, 200, 200), input_box_rect, 2)
            # Draw the text
            font = pygame.font.Font(None, 28)
            text_surface = font.render(model_name, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))
            self.draw_text(
                "Press <enter> to save,\n<backspace> to delete,\n<escape> to cancel",
                WIDTH//2, HEIGHT//2 + 120, True
            )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ai.save(model_name)
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        model_name = model_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # Don't save, just return
                        return
                    elif len(model_name) < 30:
                        if event.unicode.isprintable():
                            model_name += event.unicode
        # Show confirmation
        self.screen.fill((0, 0, 0))
        self.draw_text(f"Model '{model_name}' saved successfully!", WIDTH//2, HEIGHT//2 - 50, True)
        self.draw_text("Ready to play!", WIDTH//2, HEIGHT//2 + 50, True)
        pygame.display.flip()
        # Wait a moment
        time.sleep(1)

    def draw_text(self, text, x, y, centered=False):
        """
        Method to draw text on the screen. It takes the screen surface, the text to be displayed,
        the x and y coordinates for the text position, and an optional parameter to center the
        text.

        :param text:        The text string to be displayed.
        :param x:           The x-coordinate for the text position.
        :param y:           The y-coordinate for the text position.
        :param centered:    A boolean indicating whether the text should be centered at the given
                            coordinates.
        """
        font = pygame.font.Font(None, TXT_MENU_SIZE)
        text = font.render(text, True, TXT_MENU_COLOR)
        if centered:
            text_rect = text.get_rect()
            text_rect.midtop = (x, y)
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(text, (x, y))

    def draw_board(self):
        """
        Method to draw the game board on the screen. It draws the horizontal and vertical lines to
        create the grid for the tic-tac-toe game based on the defined number of rows
        and columns. The grid is drawn below the UI area, allowing space for displaying player
        information and instructions at the top of the screen.
        """
        # Draw the horizontal lines to create the grid
        for i in range(1, ROW):
            y = UI_HEIGHT + i * SQUARE_SIZE
            pygame.draw.line(self.screen, BOARD_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)
        # Draw the vertical lines to create the grid
        for i in range(1, COL):
            x = i * SQUARE_SIZE
            pygame.draw.line(self.screen, BOARD_COLOR, (x, UI_HEIGHT), (x, HEIGHT), LINE_WIDTH)

    def draw_cross(self, row, col):
        """
        Method to draw a cross (X) on the screen at the specified row and column.

        :param row:     The row index where the cross should be drawn.
        :param col:     The column index where the cross should be drawn.
        """
        pygame.draw.line(
            self.screen,
            CROSS_COLOR,
            (col*SQUARE_SIZE+20, UI_HEIGHT + row*SQUARE_SIZE+20),
            (col*SQUARE_SIZE+SQUARE_SIZE-20, UI_HEIGHT + row*SQUARE_SIZE+SQUARE_SIZE-20),
            CROSS_WIDTH
        )
        pygame.draw.line(
            self.screen,
            CROSS_COLOR,
            (col*SQUARE_SIZE+SQUARE_SIZE-20, UI_HEIGHT + row*SQUARE_SIZE+20),
            (col*SQUARE_SIZE+20, UI_HEIGHT + row*SQUARE_SIZE+SQUARE_SIZE-20),
            CROSS_WIDTH
        )

    def draw_circle(self, row, col):
        """
        Method to draw a circle (O) on the screen at the specified row and column.

        :param row: The row index where the circle should be drawn.
        :param col: The column index where the circle should be drawn.
        """
        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = UI_HEIGHT + row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(
            self.screen,
            CIRCLE_COLOR,
            (center_x, center_y),
            CIRCLE_RADIUS,
            CIRCLE_WIDTH
        )

    def draw_figures(self):
        """
        Method to draw the player and AI symbols on the game board. It iterates through the game
        board and checks the value of each cell. If a cell is occupied by the player,
        it draws the player's symbol (cross or circle) based on the player's choice. If a cell is
        occupied by the AI, it draws the AI's symbol based on the AI's assigned symbol.
        """
        for r in range(ROW):
            for c in range(COL):
                if self.board.board[r][c] == PLAYER:
                    if self.player_symbol == "X":
                        self.draw_cross(r, c)
                    else:
                        self.draw_circle(r, c)
                elif self.board.board[r][c] == AI:
                    if self.ai_symbol == "X":
                        self.draw_cross(r, c)
                    else:
                        self.draw_circle(r, c)
