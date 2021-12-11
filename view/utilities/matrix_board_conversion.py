import numpy as np
from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage

""" RGB Colors"""
LIGHT_BLUE = 0, 255, 255
WHITE = 255, 255, 255


def matrix_board_conversion(label, board, px_width, px_height):
    """
    Method for convert an numpy array to a label for the GUI.
    It updates the pixmap of the label passed as parameter to the method and
    scales it to the pixel dimensions required.
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
    rgb_board = np.full((board.shape[0], board.shape[1], 3), 255)
    for (x, y), value in np.ndenumerate(board):
        if value == 1:
            rgb_board[x, y, 0] = 0
    return rgb_board
