from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget

from view.utilities import matrix_board_conversion

""" Sensibility updates of mouse position while padding the board """
SENSIBILITY = 2


class BoardWidget(QWidget):
    """
    Class that define a widget that represent the state of the game's board.
    It takes the Model as parameter.

    It is responsible to convert the board state of the model in an object
    that can be show in the graphic interface.

    Attributes:
        board : Numpy array representing the initial state of the board
        board_height, board_width : dimensions initial board
        board_label : Conversion of the board array in a Qt graphic element.
        view : Reference to an instance of the view.
               Board widget is part of the view and delegates to it
               the user's interaction with the graphic board.
        mouse_pos : keep track of the mouse position in the board
        px_width, px_height : pixel dimensions of the widget
        mouse_shift : flag to indicate if mouse has moved while in panning mode
    """

    def __init__(self, board, px_width, px_height, view):
        QWidget.__init__(self)
        self._board = board
        self._board_height, self._board_width = board.shape[:2]
        self._px_width = px_width
        self._px_height = px_height
        self._view = view
        self._mouse_pos = None
        self._board_label = QLabel(self)
        self._mouse_shift = False
        # Translate matrix in pixmap and set it to the board label
        matrix_board_conversion(self._board_label, board, px_width, px_height)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Logic for the user's click interaction with the board.
        Delegates to the View the logic to apply based on the button clicked
        Left click ---> set cell alive
        Right click ---> set cell dead
        Mid click ---> start panning mode
        """
        # Convert the widget coordinates into board-matrix indexes
        pos_y = self._board_height * event.y() / self._px_height
        pos_x = self._board_width * event.x() / self._px_width
        # save current mouse position
        self._mouse_pos = pos_x, pos_y
        if event.button() == Qt.LeftButton:
            self._view.set_cell_alive(pos_x, pos_y)
        elif event.button() == Qt.RightButton:
            self._view.set_cell_dead(pos_x, pos_y)
        elif event.button() == Qt.MidButton:
            self._view.panning_activated(pos_x, pos_y)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        Logic for the user's mouse movement interaction while inside the board.
        Delegates to the View the logic to apply based on the button clicked
        Left click ---> draw alive cells
        Right click ---> kill alive cells
        Mid click ---> Panning the board
        """
        # Convert the widget coordinates into board-matrix indexes
        pos_y = self._board_height * event.y() / self._px_height
        pos_x = self._board_width * event.x() / self._px_width
        # check that the position (x,y) is inside the board and is changed
        if (lambda y, x: True if 0 <= y < self._board_height and 0 <= x < self._board_width else False)(pos_y, pos_x) \
                and (pos_x, pos_y) != self._mouse_pos:
            # save current mouse position
            if event.buttons() == Qt.LeftButton:
                self._view.set_cell_alive(pos_x, pos_y)
                self._mouse_pos = pos_x, pos_y
            elif event.buttons() == Qt.RightButton:
                self._view.set_cell_dead(pos_x, pos_y)
                self._mouse_pos = pos_x, pos_y
            elif event.buttons() == Qt.MidButton:

                # To switch the cursor to a ClosedPalmCursor without delay from sensibility
                if not self._mouse_shift:
                    # To not call the method every time that the mouse is moved, only at the first movement
                    self._mouse_shift = True
                    self._view.cursor_moved()

                x_variation = pos_x - self._mouse_pos[0]
                y_variation = pos_y - self._mouse_pos[1]
                # Update only if the absolute variation is greater than sensibility
                if x_variation > SENSIBILITY or x_variation < -SENSIBILITY or y_variation > SENSIBILITY or y_variation < -SENSIBILITY:
                    self._view.panning(pos_x, pos_y)
                    self._mouse_pos = pos_x, pos_y

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        """ Logic for the user's release click interaction with the board.
        Delegates to the View the logic to apply based on the button clicked
        Mid button ---> end panning mode
        """
        if event.button() == Qt.MidButton:
            self._view.panning_deactivated()
            self._mouse_shift = False

    def update_board_state(self, board):
        """ Updates the graphic board with the new board passed
        as a numpy array """
        matrix_board_conversion(self._board_label, board, self._px_width, self._px_height)
