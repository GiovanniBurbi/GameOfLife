import numpy as np
from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage

""" RGB Colors """
# First palette, palette = 1
LIGHT_BLUE = 0, 255, 255
BLUE = 0, 204, 204
DARK_BLUE = 0, 153, 153
DARKER_BLUE = 0, 102, 102

# Second palette, palette != 1
# LIGHT_BLUE = 0, 255, 255
GREEN = 0, 255, 0
ORANGE = 255, 128, 0
RED = 255, 0, 0


def matrix_board_conversion(label, board, px_width, px_height, palette=1):
    """
    Method for convert an numpy array to a label for the GUI.
    It takes a 2D matrix, board, with elements of 0 or 1 nad translates it into an
    3 dimensions rgb matrix, then it updates the pixmap of the label passed as parameter
    and scales it to the pixel dimensions required.
    """
    # Convert board, 2d matrix, into a rgb matrix
    rgb_board = rgb_matrix(board, palette)
    # Convert the np array in a QImage with RGB channel
    qimage = array2qimage(rgb_board)
    # Converts the Qimage in a Pixmap that can be used as a paint device.
    pixmap = QPixmap.fromImage(qimage)
    # Scale the pixmap to the pixel dimensions of the GUI's BoardLayout
    pixmap = pixmap.scaled(px_width, px_height)
    label.setPixmap(pixmap)


def rgb_matrix(board, palette):
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
            if palette == 1:
                rgb_board[x, y, 0:3] = LIGHT_BLUE
            else:
                rgb_board[x, y, 0:3] = LIGHT_BLUE
        elif value == 2:
            if palette == 1:
                rgb_board[x, y, 0:3] = BLUE
            else:
                rgb_board[x, y, 0:3] = GREEN
        elif value == 3:
            if palette == 1:
                rgb_board[x, y, 0:3] = DARK_BLUE
            else:
                rgb_board[x, y, 0:3] = ORANGE
        elif value >= 4:
            if palette == 1:
                rgb_board[x, y, 0:3] = DARKER_BLUE
            else:
                rgb_board[x, y, 0:3] = RED
    return rgb_board
