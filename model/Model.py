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
        ratio : matrix board ratio
        visible_board : submatrix of the board that is currently visible
    """

    def __init__(self, height=30, width=60):
        self._width = width
        self._height = height
        self._ratio = int(width / height)
        self._board = np.full((height, width, 3), 255)
        self._visible_board = self._board
        self._controller = None

    @property
    def visible_board(self):
        return self._visible_board

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

    def resize(self, value):
        """ Method that change the visible matrix according to a value """
        self._visible_board = self.get_submatrix(value)
        self._controller.update_board(self._visible_board)

    def get_submatrix(self, scale):
        """ Method to retrieve a centered submatrix of the board """
        height_shift = scale
        width_shift = scale * self._ratio
        return self._board[height_shift:self._height - height_shift, width_shift:self._width - width_shift]
