import numpy as np


class Model(object):
    """
    Model of the Model-View-Controller architecture

    This class is responsible for initialize and manage the board
    and all the methods that interact with it.

    Attributes:
        width, length : 2D dimensions of the board
        board : numpy array with 3 dimension, RGB matrix. Represent current state.
                Initial state is a white board, all cell are dead.

    """

    def __init__(self, width=100, length=200):
        """ """
        self._width = width
        self._length = length
        self._board = np.full((width, length, 3), 255)

    def get_board_dimension(self):
        """ Return the width and length of the board """
        return self._width, self._length

    @property
    def board(self):
        return self._board
