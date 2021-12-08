from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QFrame

from view.utilities import matrix_board_conversion

""" 
Constants for pixel dimensions of the board widget.
Custom for this project specific GUI
"""
PIXEL_WIDTH = 650
PIXEL_HEIGHT = 400


class BoardWidget(QWidget):
    """
    Class that define a widget that represent the state of the game's board.
    It takes the Model as parameter.

    It is responsible to convert the board state of the model in an object
    that can be show in the graphic interface.

    Attributes:
        board : Numpy array, state of the board
        board_label : Conversion of the board array in a Qt graphic element.
        view : Reference to an instance of the view.
                Board widget is part of the view and delegates to it
                the user's interaction with the graphic board.
    """

    def __init__(self, board, view):
        QWidget.__init__(self)
        self._board = board
        self._view = view
        self._board_label = QLabel(self)
        self._board_label = matrix_board_conversion(self._board_label, board, PIXEL_WIDTH, PIXEL_HEIGHT)
        # Creates the outline of the label and soften its shadow
        self._board_label.setFrameShape(QFrame.Box)
        self._board_label.setFrameShadow(QFrame.Sunken)

        self._board_label.show()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """ Logic for the user's click interaction with the board.
        Delegates to the View the command to change cell's state
        Left click ---> set cell alive
        Right click ---> set cell dead
        """
        board_height, board_width = self._board.shape[:2]
        # Convert the widget coordinates into board-matrix indexes
        pos_x = int((board_width * event.x()) / PIXEL_WIDTH)
        pos_y = int((board_height * event.y()) / PIXEL_HEIGHT)
        # check that position (x, y) is != outline
        if (lambda y, x: True if y != board_height and x != board_width else False)(pos_y, pos_x):
            if event.button() == Qt.LeftButton:
                self._view.set_cell_alive(pos_x, pos_y)
                self._view.change_info_label()
            elif event.button() == Qt.RightButton:
                self._view.set_cell_dead(pos_x, pos_y)

    def update_board_state(self, board):
        """ Updates the graphic board with the new board passed
        as a numpy array """
        self._board_label = matrix_board_conversion(self._board_label, board, PIXEL_WIDTH, PIXEL_HEIGHT)
