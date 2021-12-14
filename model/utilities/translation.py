import numpy as np


def translation_x(board, value):
    """ Method that translate over axis x the position of living cells """
    dim_x, dim_y = board.shape
    # If there is living cells on the edge of the board
    # that are required to go over, then return unchanged board
    if (sum(board[dim_x - 1, :]) != 0 and value > 0) or (sum(board[0, :]) != 0 and value < 0):
        return board
    # Return the new board with translated/shifted living cells over axis x
    return np.roll(board, value, axis=0)


def translation_y(board, value):
    """ Method that translate over axis y the position of living cells """
    dim_x, dim_y = board.shape
    # If there is living cells on the edge of the board
    # that are required to go over, then return unchanged board
    if (sum(board[:, dim_y - 1]) != 0 and value > 0) or (sum(board[:, 0]) != 0 and value < 0):
        return board
    # Return the new board with translated/shifted living cells over axis y
    return np.roll(board, value, axis=1)
