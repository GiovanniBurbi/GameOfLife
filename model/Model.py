import os
import sys

import numpy as np
from scipy.ndimage import convolve

from model import Observable
from model.utilities import pattern_decoder

""" Value of not visible board, to give the impression of infinity"""
NOT_VISIBLE_DIM = 10


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
        kernel : convolution kernel. To calculate sum of the values of the adjacent cells
        pattern_location : path to the folder containing the rle files of preset patterns
        files : pattern files inside the patterns folder
        history_mode : flag activation history mode
        history_board : board with the ages of every alive cell
        height_shift, width_shift: offsets to center board after zoom
        pan_x, pan_y : keep track of the position where has been started the panning mode
        panning_mode : flag to indicate if the panning mode is active
        current_panning_x, current_panning_y : keep track how much panning over the axis has been produce
                                               in one panning session.

        panning_board : support board to save the state of the board after the panning.
    """

    def __init__(self, height_max=60, width_max=120):
        super().__init__()
        self._width_max = width_max
        self._height_max = height_max
        self._ratio = int(width_max / height_max)
        self._not_visible_w = NOT_VISIBLE_DIM * self._ratio
        self._not_visible_h = NOT_VISIBLE_DIM
        self._width = self._width_max - self._not_visible_w * self._ratio
        self._height = self._height_max - self._not_visible_h * self._ratio
        self._board = np.zeros((height_max, width_max), np.int8)
        self._kernel = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]])
        self._patterns_location = os.path.abspath(os.path.dirname(sys.argv[0])) + "/model/patterns/"
        self._files = sorted([f for f in os.listdir(self._patterns_location)], key=lambda f: f.lower())
        self._history_mode = False
        self._history_board = np.zeros((height_max, width_max), np.int8)
        self._height_shift = 0
        self._width_shift = 0
        self._pan_x = None
        self._pan_y = None
        self._panning_mode = False
        self._current_panning_x = 0
        self._current_panning_y = 0
        self._panning_board = np.zeros((height_max, width_max), np.int8)

    @property
    def patterns(self):
        """ Method to get the files in the pattern folder """
        return self._files

    @property
    def visible_board(self):
        """ Method that allows external element to get the visible board.
        It returns a copy so that the state of the board is not modifiable from
        outside."""
        if self._panning_mode:
            return np.copy(self._get_visible_panning_board())
        if self._history_mode:
            return np.copy(self._get_visible_history_board())
        return np.copy(self._get_visible_state_board())

    def alive_cell(self, x, y):
        """ Method to set alive a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self._adjust_coords(x, y)
        visible_state_board = self._get_visible_state_board()
        visible_history_board = self._get_visible_history_board()
        # If state board has a cell dead, also history board has the same cell dead
        if visible_state_board[pos_x, pos_y] == 0:
            visible_state_board[pos_x, pos_y] = 1
            visible_history_board[pos_x, pos_y] = 1
            self.value = self.visible_board

    def dead_cell(self, x, y):
        """ Method to set dead a cell in the board.
        Value 0 means that the cell is dead, value 1 the cell is alive.
        Then it publish the updated board. """
        pos_x, pos_y = self._adjust_coords(x, y)
        visible_state_board = self._get_visible_state_board()
        visible_history_board = self._get_visible_history_board()
        if visible_state_board[pos_x, pos_y] == 1:
            visible_state_board[pos_x, pos_y] = 0
            visible_history_board[pos_x, pos_y] = 0
            self.value = self.visible_board

    def resize(self, zoom):
        """ Method that change the visible matrix according to a value """
        self._height_shift = zoom
        self._width_shift = zoom * self._ratio
        self.value = self.visible_board

    def _get_visible_panning_board(self):
        """ Method to retrieve the visible submatrix of the panning board
        It returns the reference to the panning board, so changes to the returned matrix
        is reflected on the state of the panning board. """
        return self._panning_board[
               self._not_visible_h + self._height_shift:self._height_max - self._height_shift - self._not_visible_h,
               self._not_visible_w + self._width_shift:self._width_max - self._width_shift - self._not_visible_w]

    def _get_visible_state_board(self):
        """ Method to retrieve a centered submatrix of the state board.
        It returns the reference to the board, so changes to the returned matrix
        is reflected on the state of the board. """
        return self._board[
               self._not_visible_h + self._height_shift:self._height_max - self._height_shift - self._not_visible_h,
               self._not_visible_w + self._width_shift:self._width_max - self._width_shift - self._not_visible_w]

    def _get_visible_history_board(self):
        """ Method to retrieve a centered submatrix of the history board.
        It returns the reference to the board, so changes to the returned matrix
        is reflected on the state of the history board. """
        return self._history_board[
               self._not_visible_h + self._height_shift:self._height_max - self._height_shift - self._not_visible_h,
               self._not_visible_w + self._width_shift:self._width_max - self._width_shift - self._not_visible_w]

    def _adjust_coords(self, x, y):
        """ Method to adjust coordinates to the actual visible board """
        # Multiply coordinates for max size board (x,y) by the scale ratio
        # between dimensions of the visible board and the max size board.
        # state board and history board have the same dimensions
        # the division keep in account the not visible part of the board
        visible_state_board = self._get_visible_state_board()
        pos_x = int(y * (visible_state_board.shape[0] / (self._height_max - (self._not_visible_h * 2))))
        pos_y = int(x * (visible_state_board.shape[1] / (self._width_max - (self._not_visible_w * 2))))
        return pos_x, pos_y

    def clear(self):
        """ Method that set the boards to the initial state of all cells dead. """
        self._board = np.zeros((self._height_max, self._width_max))
        self._history_board = np.zeros((self._height_max, self._width_max))
        self.value = self.visible_board

    def _compute_neighbors(self):
        """ Method to calculate, for every cell, how many adjacent alive
        cells they have """
        return convolve(self._board, self._kernel, mode="constant", cval=0)

    def next_generation(self):
        """ Method to generate the next state of the boards according
        to Conway's Game Of Life rules. """
        neighbors = self._compute_neighbors()
        # Using numpy mechanism to make logical operations element-wise between
        # the matrix of the current state and the matrix of neighbors. Then
        # in the resulting matrix, representing the next state, False is converted
        # in 0, dead cell, and True is converted in 1, alive cell.
        self._board = (
                ((self._board == 1) & (neighbors > 1) & (neighbors < 4))
                | ((self._board == 0) & (neighbors == 3))).astype(np.uint8)
        # Sum history board with the new state board to compute the age of the cells
        self._history_board += self._board
        # Turn off cells in the history board that are dead in the new state board
        self._history_board[self._board == 0] = 0
        if self._panning_mode:
            self._panning_board = self._adjust_panning(self._board)
        self.value = self.visible_board

    def load_pattern(self, pattern_name):
        """ Method to load in the board a certain pattern, using
        its name passed as parameter"""
        board = np.zeros((self._height_max, self._width_max))
        # Open the requested file in the pattern folder
        with open(str(self._patterns_location + pattern_name)) as f:
            # Pass the pattern file to the pattern decoder function
            pattern_width, pattern_height, pattern_coords = pattern_decoder(f)
            offset_x, offset_y = self.compute_offsets(pattern_height, pattern_width, pattern_name)
            for x, y in pattern_coords:
                # Set alive the cells specified in the pattern file
                board[offset_y + y, offset_x + x] = 1
        # Update boards and notify
        self._board = board
        self._history_board = board
        self.value = self.visible_board

    def compute_offsets(self, pattern_height, pattern_width, pattern_name):
        """ Method to compute offset of loaded pattern """
        # Using the dimension of the pattern to calculate the coordinates offset from the center of the board.
        # Custom offset for some type of pattern to better show the evolutions or better centering
        if pattern_name in ["Diamond", "Pentadecathlon", "Queen bee shuttle"]:
            offset_x = int(self._width_max / 2 - pattern_width / 2)
            offset_y = int(self._height_max / 2 - pattern_height / 2)
        elif pattern_name == "Space rake":
            offset_x = int(self._width_max / 2 - pattern_width / 2) - 26
            offset_y = int(self._height_max / 2 - pattern_height / 2) + 8
        elif pattern_name in ["Schick engine", "Spaceship"]:
            offset_x = int(self._width_max / 2 - pattern_width / 2) + 30
            offset_y = int(self._height_max / 2 - pattern_height / 2)
        else:
            offset_x = int(self._width_max / 2 - pattern_width / 2) + 1
            offset_y = int(self._height_max / 2 - pattern_height / 2)
        return offset_x, offset_y

    def history_mode(self, enabled):
        """ Method to set the history mode """
        # If history mode is enabled, reset history board so that it will start
        # with a fresh history matrix. It will show the age of cells from this moment.
        if enabled:
            self._history_board = np.zeros((self._height_max, self._width_max))
        self._history_mode = enabled

    def panning_set(self, x, y):
        """ Method to activate flag panning mode and save the coords
        from where the panning mode has been activated"""
        self._pan_x, self._pan_y = self._adjust_coords(x, y)
        self._panning_mode = True
        self._panning_board = np.copy(self._board)

    def change_focus(self, x, y):
        """ Method to change the focus of the board. It implements the panning.
        Based on the variation of the pan coords it moves the living cells the
        appropriate distance by changing the coords of the living position on the board"""
        board = self._panning_board
        pan_x, pan_y = self._adjust_coords(x, y)
        # Don't change if pan coords have not changed
        if pan_x != self._pan_x or pan_y != self._pan_x:

            # Based on what changed, shift the board
            if pan_x - self._pan_x < 0:
                board = self._translation_x(board, 1)
            elif pan_x - self._pan_x > 0:
                board = self._translation_x(board, -1)
            if pan_y - self._pan_y < 0:
                board = self._translation_y(board, 1)
            elif pan_y - self._pan_y > 0:
                board = self._translation_y(board, -1)

            # updates actual coords of the panning
            self._pan_x = pan_x
            self._pan_y = pan_y
            # notify new panning board
            self._panning_board = board
            self.value = self.visible_board

    def panning_unset(self):
        """ Method to deactivated panning mode and reset current panning coords to zero.
        Updates state board to the last configuration of the panning board """
        self._panning_mode = False
        self._current_panning_x = 0
        self._current_panning_y = 0
        self._board = self._panning_board
        self.value = self.visible_board

    def _translation_x(self, board, value):
        """ Method that translate over axis x the position of living cells """
        dim_x, dim_y = board.shape
        # If there is living cells on the edge of the board
        # that are required to go over, then return unchanged board
        if sum(board[dim_x - 1, :]) != 0 and value > 0:
            return board
        if sum(board[0, :]) != 0 and value < 0:
            return board
        # If translation is admissible then update the current total panning over axis x
        self._current_panning_x += value
        # Return the new board with translated/shifted living cells over axis x
        return np.roll(board, value, axis=0)

    def _translation_y(self, board, value):
        """ Method that translate over axis y the position of living cells """
        dim_x, dim_y = board.shape
        # If there is living cells on the edge of the board
        # that are required to go over, then return unchanged board
        if sum(board[:, dim_y - 1]) != 0 and value > 0:
            return board
        if sum(board[:, 0]) != 0 and value < 0:
            return board
        # If translation is admissible then update the current total panning over axis y
        self._current_panning_y += value
        # Return the new board with translated/shifted living cells over axis y
        return np.roll(board, value, axis=1)

    def _adjust_panning(self, board):
        """ Method to shift the board positions according to the current panning pos from the center of the board. """
        dim_x, dim_y = board.shape
        # using the numpy api roll function one cell on the edge can go over board and appear on the other side :(
        # new = np.roll(board, (self._current_panning_x, self._current_panning_y), (0,1))
        new = np.zeros((dim_x, dim_y), np.int8)
        for i in range(dim_x):
            for j in range(dim_y):
                if board[i, j] == 1:
                    # If the alive element would go over board, modify current_panning pos to return on board
                    if i + self._current_panning_x < 0:
                        self._current_panning_x += 1
                    if j + self._current_panning_y < 0:
                        self._current_panning_y += 1
                    if i + self._current_panning_x > dim_x - 1:
                        self._current_panning_x -= 1
                    if j + self._current_panning_y > dim_y - 1:
                        self._current_panning_y -= 1
                    new[i + self._current_panning_x, j + self._current_panning_y] = board[i, j]
        return new
