import os
import re
import sys

import numpy as np
from scipy.ndimage import convolve

from model import Observable
from model.utilities import pattern_decoder, translation_x, translation_y

""" Extensions of pattern files """
PATTERN_FILE_EXTENSION = ".rle"

""" Value to use to compute the dimensions of the max visible board """
NOT_VISIBLE_CONST = 10


class Model(Observable):
    """
    Model of the Model-View-Controller architecture

    This class is responsible for initialize and manage the board
    and all the methods that interact with it.
    It extends the Observable class to publish the updates of the visible board.

    Attributes:
        width_max, length_max : 2D dimensions of the board, including the invisible parts
        ratio : matrix board ratio
        not_visible_w, not_visible_h : dimensions of how much is not visible of the total board, divide per 2.
                                       Used to shift index when extracting visible board.
        width, height : dimensions of the max visible board.
        board : numpy array with 2 dimensions, represent current state of the cells.
                Initial state is a zero matrix, meaning all cells are dead.
        height_shift, width_shift: offsets to center board after zoom
        kernel : convolution kernel. To calculate sum of the values of the adjacent cells
        files : predefined pattern files paths
        history_mode : flag activation history mode
        pan_x, pan_y : keep track of the position of the mouse in the board while panning
        panning_mode : flag to indicate if the panning mode is active
    """

    def __init__(self, height=60, width=120):
        super().__init__()
        self._width = width
        self._height = height
        self._ratio = int(width / height)
        # Dimensions to compute the visible sub-board
        self._not_visible_w = NOT_VISIBLE_CONST * self._ratio
        self._not_visible_h = NOT_VISIBLE_CONST
        # Dimensions of the initial visible board
        self._visible_width = self._width - self._not_visible_w * self._ratio
        self._visible_height = self._height - self._not_visible_h * self._ratio
        self._board = np.zeros((height, width), np.int8)
        self._height_shift = 0
        self._width_shift = 0
        self._kernel = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        predefined_patterns_location = os.path.abspath(os.path.dirname(sys.argv[0])) + "/model/patterns/"
        self._files = sorted([f for f in os.listdir(predefined_patterns_location)], key=lambda f: f.lower())
        self._files = [predefined_patterns_location + x for x in self._files]
        self._history_mode = False
        self._pan_x = None
        self._pan_y = None
        self._panning_mode = False

    @property
    def predefinite_patterns(self):
        """ Method to get the files path of the files in the pattern folder """
        return self._files

    @property
    def visible_board(self):
        """ Method that allows external element to get the visible board.
        It returns a copy so that the state of the board is not modifiable from
        outside."""
        return np.copy(self._get_visible_board())

    def _get_visible_board(self):
        """ Method to retrieve a centered submatrix of the state board.
        It returns the reference to the board, so changes to the returned matrix
        is reflected on the state of the board. """
        return self._board[
               self._not_visible_h + self._height_shift:self._height - self._height_shift - self._not_visible_h,
               self._not_visible_w + self._width_shift:self._width - self._width_shift - self._not_visible_w]

    def resize(self, zoom):
        """ Method that change the visible matrix according to a value """
        self._height_shift = zoom
        self._width_shift = zoom * self._ratio
        self.value = self.visible_board

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self._adjust_coords(x, y)
        visible_board = self._get_visible_board()
        # If state board has a cell dead, also history board has the same cell dead
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

    def _adjust_coords(self, x, y):
        """ Method to adjust coordinates to the actual visible board """
        visible_board = self._get_visible_board()
        # Adjust x and y by multiply for the ratio between actual dimensions
        # of the visible board (zoom accounted) and the dimensions of the
        # maximum visible board
        pos_x = int(y * (visible_board.shape[0] / self._visible_height))
        pos_y = int(x * (visible_board.shape[1] / self._visible_width))
        return pos_x, pos_y

    def clear(self):
        """ Method that set the boards to the initial state of all cells dead. """
        self._board = np.zeros((self._height, self._width), np.int8)
        self.value = self.visible_board

    def open_pattern(self, pattern):
        """ Method to load in the board a certain pattern, using
        its name passed as parameter"""
        board = np.zeros((self._height, self._width), np.int8)
        # Open file given the path
        with open(pattern) as f:
            # Pass the pattern file to the pattern decoder function
            pattern_width, pattern_height, pattern_coords = pattern_decoder(f)
            pattern_name = re.split('[/.]', pattern)[-2]
            offset_x, offset_y = self.compute_offsets(pattern_height, pattern_width, pattern_name)
            for x, y in pattern_coords:
                # Set alive the cells specified in the pattern file
                board[offset_y + y, offset_x + x] = 1
        # Update boards and notify
        self._board = board
        self.value = self.visible_board

    def compute_offsets(self, pattern_height, pattern_width, pattern_name):
        """ Method to compute offset of loaded pattern """
        # Using the dimension of the pattern to calculate the coordinates offset from the center of the board.
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
        return offset_x, offset_y

    def _compute_neighbors(self):
        """ Method to calculate, for every cell, how many adjacent alive
        cells they have """
        board = self._normalize_board(self._board)
        return convolve(board, self._kernel, mode="constant", cval=0)

    def _normalize_board(self, board):
        """ Method to normalized to 1 all alive cells that may have >1 values
        if history mode has been activated """
        if self._history_mode:
            normalized_board = np.copy(board)
            normalized_board[normalized_board > 0] = 1
            return normalized_board
        else:
            return board

    def next_generation(self):
        """ Method to generate the next state of the boards according
        to Conway's Game Of Life rules. """
        neighbors = self._compute_neighbors()
        # Using numpy mechanism to make logical operations element-wise between
        # the matrix of the current state and the matrix of neighbors. Then
        # in the resulting matrix, representing the next state, False is converted
        # in 0, dead cell, and True is converted in 1, alive cell.
        state_board = (
                ((self._board > 0) & (neighbors > 1) & (neighbors < 4))
                | ((self._board == 0) & (neighbors == 3))).astype(np.uint8)
        if self._history_mode:
            # Compute ages and set to zero age of cells that are dead in the latest step
            ages = self._board + state_board
            ages[state_board == 0] = 0
            self._board = ages
        else:
            self._board = state_board
        self.value = self.visible_board

    def history_mode(self, enabled):
        """ Method to set the history mode """
        # If history mode is enabled, normalized board so that alive cells have value 1
        if self._history_mode:
            self._board = self._normalize_board(self._board)
        self._history_mode = enabled

    def set_panning_mode(self, enabled, x=None, y=None):
        """ Method to activate/deactivate flag panning mode and save the coords
        from where the panning mode has been activated"""
        if enabled:
            self._pan_x, self._pan_y = self._adjust_coords(x, y)
            self._panning_mode = True
        else:
            self._panning_mode = False

    def change_focus(self, x, y):
        """ Method to change the focus of the board. It implements the panning.
        Based on the variation of the pan coords it moves the living cells of the
        appropriate distance by changing the coords of the living position on the board"""
        pan_x, pan_y = self._adjust_coords(x, y)
        # Don't change if pan coords have not changed
        if pan_x != self._pan_x or pan_y != self._pan_x:

            # Based on what changed, shift the board
            if pan_x - self._pan_x < 0:
                self._board = translation_x(self._board, -1)
            elif pan_x - self._pan_x > 0:
                self._board = translation_x(self._board, 1)
            if pan_y - self._pan_y < 0:
                self._board = translation_y(self._board, -1)
            elif pan_y - self._pan_y > 0:
                self._board = translation_y(self._board, 1)

            # updates actual coords of the panning
            self._pan_x = pan_x
            self._pan_y = pan_y
            # notify changes
            self.value = self.visible_board
