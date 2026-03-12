"""
Constants used in the project.
"""

__title__: str = "constants"
__version__: str = "1.0.0"
__author__: str = "Brice Petit"
__license__: str = "MIT"

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- IMPORTS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Imports standard libraries

# Imports third party libraries

# Imports from src

# ----------------------------------------------------------------------------------------------- #
# ------------------------------------------- GLOBALS ------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Define the size of the image
HEIGHT: int = 900
WIDTH: int = 600

# Define the height of the UI area and the height of the board area
UI_HEIGHT: int = HEIGHT // 3
BOARD_HEIGHT: int = HEIGHT - UI_HEIGHT

# Define the number of rows and columns in the grid
ROW: int = 3
COL: int = 3

# Define the size of each square in the grid based on the width and number of columns
SQUARE_SIZE: int = BOARD_HEIGHT // ROW

# Define the width of the lines used to draw the grid and the symbols for the player's and AI's
LINE_WIDTH: int = 10
CIRCLE_RADIUS: int = SQUARE_SIZE // 3
CIRCLE_WIDTH: int = 10
CROSS_WIDTH: int = 15

# Define if a cell is empty, occupied by player 1, or occupied by player 2
EMPTY: int = 0
PLAYER: int = 1
AI: int = 2

# Define the size and color used in the game for the text
TXT_MENU_SIZE: int = 32
TXT_MENU_COLOR: tuple = (255, 255, 255)

# Define the color for crosses circles, and board
CROSS_COLOR: tuple = (255, 255, 255)
CIRCLE_COLOR: tuple = (255, 255, 255)
BOARD_COLOR: tuple = (255, 255, 255)

# Define the colors for the progress bar
PROGRESS_BAR_BG: tuple = (50, 50, 50)
PROGRESS_BAR_FILL: tuple = (0, 200, 0)
PROGRESS_BAR_HEIGHT: int = 30
PROGRESS_BAR_WIDTH: int = 400
