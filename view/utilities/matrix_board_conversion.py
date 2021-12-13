import numpy as np
from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage

""" RGB Colors"""
LIGHT_BLUE = 0, 255, 255
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
ORANGE = 255, 125, 0
RED = 255, 0, 0


def matrix_board_conversion(label, board, px_width, px_height):
    """
    Method for convert an numpy array to a label for the GUI.
    It takes a 2D matrix, board, with elements of 0 or 1 nad translates it into an
    3 dimensions rgb matrix, then it updates the pixmap of the label passed as parameter
    and scales it to the pixel dimensions required.
    """
    # Convert board, 2d matrix, into a rgb matrix
    rgb_board = rgb_matrix(board)
    # Convert the np array in a QImage with RGB channel
    qimage = array2qimage(rgb_board)
    # Converts the Qimage in a Pixmap that can be used as a paint device.
    pixmap = QPixmap.fromImage(qimage)
    # Scale the pixmap to the pixel dimensions of the GUI's BoardLayout
    pixmap = pixmap.scaled(px_width, px_height)
    label.setPixmap(pixmap)


def rgb_matrix(board):
    """ Takes a 2D matrix with elements of value 0 or 1 and converts it into a
    3D rgb matrix. A cell with value 0 in the original 2D matrix is converted
    into a white cell, while, a cell with value 1 is converted into a
    light-blue cell.
     """
    # Initialize a 3D rgb matrix with all cells WHITE. rgb white = (255, 255, 255).
    rgb_board = np.full((board.shape[0], board.shape[1], 3), 255)
    for (x, y), value in np.ndenumerate(board):
        # If cell has value 1, then it's alive
        if value == 1:
            # Make that cell light-blue color
            rgb_board[x, y, 0:3] = LIGHT_BLUE
        elif value == 2:
            rgb_board[x, y, 0:3] = GREEN
        elif value == 3:
            rgb_board[x, y, 0:3] = YELLOW
        elif value == 4:
            rgb_board[x, y, 0:3] = ORANGE
        elif value >= 5:
            rgb_board[x, y, 0:3] = RED
    return rgb_board
