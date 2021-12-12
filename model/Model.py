import os
import sys

import numpy as np
from scipy.ndimage import convolve

from model import Observable
from model.utilities import pattern_decoder


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
        kernel : convolution kernel. To calculate sum of the values of the adjacent cells
        pattern_location : path to the folder containing the rle files of preset patterns
        files : pattern files inside the patterns folder
    """

    def __init__(self, height=40, width=80):
        super().__init__()
        self._width = width
        self._height = height
        self._ratio = int(width / height)
        self._board = np.zeros((height, width), np.int8)
        self._zoom = 0
        self._kernel = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        self._patterns_location = os.path.abspath(os.path.dirname(sys.argv[0])) + "/model/patterns/"
        self._files = sorted([f for f in os.listdir(self._patterns_location)], key=lambda f: f.lower())

    @property
    def patterns(self):
        return self._files

    @property
    def visible_board(self):
        """ Method that allows external element to get the visible board.
        It returns a copy so that the state of the board is not modifiable from
        outside."""
        return np.copy(self._get_visible_board())

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self._adjust_coords(x, y)
        visible_board = self._get_visible_board()
        if visible_board[pos_x, pos_y] == 0:
            visible_board[pos_x, pos_y] = 1
            self.value = self.visible_board

    def dead_cell(self, x, y):
        """ Method to set dead a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self._adjust_coords(x, y)
        visible_board = self._get_visible_board()
        if visible_board[pos_x, pos_y] == 1:
            visible_board[pos_x, pos_y] = 0
            self.value = self.visible_board

    def resize(self, value):
        """ Method that change the visible matrix according to a value """
        self._zoom = value
        self.value = self.visible_board

    def _get_visible_board(self):
        """ Method to retrieve a centered submatrix of the board.
        It returns the reference to the board, so changes to the returned matrix
        is reflected on the state of the board. """
        height_shift = self._zoom
        width_shift = self._zoom * self._ratio
        return self._board[height_shift:self._height - height_shift, width_shift:self._width - width_shift]

    def _adjust_coords(self, x, y):
        """ Method to adjust coordinates to the actual visible board """
        # Multiply coordinates for max size board (x,y) by the scale ratio
        # between dimensions of the visible board and the max size board
        visible_board = self._get_visible_board()
        pos_x = int(y * (visible_board.shape[0] / self._height))
        pos_y = int(x * (visible_board.shape[1] / self._width))
        return pos_x, pos_y

    def clear(self):
        """ Method that set the board to the initial state of all cells dead. """
        self._board = np.zeros((self._height, self._width))
        self.value = self.visible_board

    def _compute_neighbors(self):
        """ Method to calculate, for every cell, how many adjacent alive
        cells they have """
        return convolve(self._board, self._kernel, mode="constant", cval=0)

    def next_generation(self):
        """ Method to generate the next state of the board according
        to Conway's Game Of Life rules. """
        neighbors = self._compute_neighbors()
        # Using numpy mechanism to make logical operations element-wise between
        # the matrix of the current state and the matrix of neighbors. Then
        # in the resulting matrix, representing the next state, False is converted
        # in 0, dead cell, and True is converted in 1, alive cell.
        self._board = (
                ((self._board == 1) & (neighbors > 1) & (neighbors < 4))
                | ((self._board == 0) & (neighbors == 3))).astype(np.uint8)
        self.value = self.visible_board

    def load_pattern(self, pattern_name):
        """ Method to load in the board a certain pattern, using
        its name passed as parameter"""
        board = np.zeros((self._height, self._width))
        # Open the requested file in the pattern folder
        with open(str(self._patterns_location + pattern_name)) as f:
            # Pass the pattern file to the pattern decoder function
            pattern_width, pattern_height, pattern_coords = pattern_decoder(f)
            # Using the dimension of the pattern to calculate the coordinates offset
            # to then set the pattern in the center of the board
            # Custom offset for some type of pattern to better show the evolutions or better centering
            if pattern_name in ["Diamond", "Pentadecathlon", "Queen bee shuttle"]:
                offset_x = int(self._width / 2 - pattern_width / 2)
                offset_y = int(self._height / 2 - pattern_height / 2)
            elif pattern_name == "Space rake":
                offset_x = int(self._width / 2 - pattern_width / 2) - 26
                offset_y = int(self._height / 2 - pattern_height / 2) + 8
            elif pattern_name in ["Schick engine", "Spaceship"]:
                offset_x = int(self._width / 2 - pattern_width / 2) + 30
                offset_y = int(self._height / 2 - pattern_height / 2)
            else:
                offset_x = int(self._width / 2 - pattern_width / 2) + 1
                offset_y = int(self._height / 2 - pattern_height / 2)
            for x, y in pattern_coords:
                # Set alive the cells specified in the pattern file
                board[offset_y + y, offset_x + x] = 1
        # Update board and notify
        self._board = board
        self.value = self.visible_board
