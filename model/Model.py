import numpy as np

from model import Observable


class Model(Observable):
    """
    Model of the Model-View-Controller architecture

    This class is responsible for initialize and manage the board
    and all the methods that interact with it.
    It extends the Observable class to publish the updates of the visible board.

    Attributes:
        width, length : 2D dimensions of the board
        board : numpy array with 2 dimensions, represent current state of the cells.
                Initial state is a zero matrix, meaning all cells are dead.
        ratio : matrix board ratio
        zoom : zoom of the board selected
    """

    def __init__(self, height=30, width=60):
        super().__init__()
        self._width = width
        self._height = height
        self._ratio = int(width / height)
        self._board = np.zeros((height, width))
        self._zoom = 0

    @property
    def visible_board(self):
        return self.get_submatrix(self._zoom)

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self.adjust_coords(x, y)
        if self.visible_board[pos_x, pos_y] == 0:
            self.visible_board[pos_x, pos_y] = 1
            self.value = self.visible_board

    def dead_cell(self, x, y):
        """ Method to set dead a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self.adjust_coords(x, y)
        if self.visible_board[pos_x, pos_y] == 1:
            self.visible_board[pos_x, pos_y] = 0
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
