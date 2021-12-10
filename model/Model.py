import numpy as np

from model import Observable

""" RGB Colors"""
LIGHT_BLUE = 0, 255, 255
WHITE = 255, 255, 255


class Model(Observable):
    """
    Model of the Model-View-Controller architecture

    This class is responsible for initialize and manage the board
    and all the methods that interact with it.
    It extends the Observable class to publish the updates to the visible board.

    Attributes:
        width, length : 2D dimensions of the board
        board : numpy array with 3 dimension, RGB matrix. Represent current state.
                Initial state is a white board, all cell are dead.
        controller : reference to an instance of the controller.
                     Model delegates to this object any change to the board state.
        ratio : matrix board ratio
        zoom : zoom of the board selected
    """

    def __init__(self, height=30, width=60):
        super().__init__()
        self._width = width
        self._height = height
        self._ratio = int(width / height)
        self._board = np.full((height, width, 3), 255)
        self._zoom = 0
        self._controller = None

    @property
    def visible_board(self):
        return self.get_submatrix(self._zoom)

    def set_controller(self, controller):
        self._controller = controller

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        To check the actual state it sums the rgb values of the cell.
        Then it publish the updated board. """
        pos_x, pos_y = self.adjust_coords(x, y)
        is_white_cell = \
            True if sum(self.visible_board[pos_x, pos_y, 0:3]) == sum(WHITE) else False
        if is_white_cell:
            self.visible_board[pos_x, pos_y, 0:3] = LIGHT_BLUE
            self.value = self.visible_board

    def dead_cell(self, x, y):
        """ Method to set dead a cell in the board.
        To check the actual state it sums the rgb values of the cell.
        Then it publish the updated board. """
        pos_x, pos_y = self.adjust_coords(x, y)
        is_light_blue_cell = \
            True if sum(self.visible_board[pos_x, pos_y, 0:3]) == sum(LIGHT_BLUE) else False
        if is_light_blue_cell:
            self.visible_board[pos_x, pos_y, 0:3] = WHITE
            self.value = self.visible_board

    def resize(self, value):
        """ Method that change the visible matrix according to a value """
        self._zoom = value
        self.value = self.visible_board

    def get_submatrix(self, scale):
        """ Method to retrieve a centered submatrix of the board """
        height_shift = scale
        width_shift = scale * self._ratio
        return self._board[height_shift:self._height - height_shift, width_shift:self._width - width_shift]

    def adjust_coords(self, x, y):
        """ Method to adjust coordinates to the actual visible board """
        # Multiply coordinates for max size board (x,y) by the scale ratio
        # between dimensions of the visible board and the max size board
        pos_x = int(y * (self.visible_board.shape[0] / self._height))
        pos_y = int(x * (self.visible_board.shape[1] / self._width))
        return pos_x, pos_y
