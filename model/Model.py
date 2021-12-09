import numpy as np

""" RGB Colors"""
LIGHT_BLUE = 0, 255, 255
WHITE = 255, 255, 255


class Model(object):
    """
    Model of the Model-View-Controller architecture

    This class is responsible for initialize and manage the board
    and all the methods that interact with it.

    Attributes:
        width, length : 2D dimensions of the board
        board : numpy array with 3 dimension, RGB matrix. Represent current state.
                Initial state is a white board, all cell are dead.
        controller : reference to an instance of the controller.
                     Model delegates to this object any change to the board state.

    """

    def __init__(self, height=20, width=35):
        self._width = width
        self._height = height
        self._board = np.full((height, width, 3), 255)
        self._controller = None

    def get_board_dimension(self):
        """ Return the width and length of the board """
        return self._width, self._height

    @property
    def board(self):
        return self._board

    def set_controller(self, controller):
        self._controller = controller

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        To check the actual state it sums the rgb values of the cell.
        Then delegates to the controller the visual update of the board. """
        is_white_cell = \
            True if sum(self._board[y, x, 0:3]) == sum(WHITE) else False
        if is_white_cell:
            self._board[y, x, 0:3] = LIGHT_BLUE
            self._controller.update_board(self._board)

    def dead_cell(self, x, y):
        """ Method to set dead a cell in the board.
        To check the actual state it sums the rgb values of the cell.
        Then delegates to the controller the visual update of the board. """
        is_light_blue_cell = \
            True if sum(self._board[y, x, 0:3]) == sum(LIGHT_BLUE) else False
        if is_light_blue_cell:
            self._board[y, x, 0:3] = WHITE
            self._controller.update_board(self._board)
