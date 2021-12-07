from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QFrame
from qimage2ndarray import array2qimage

""" 
Constants for geometry and alignment of the board widget.
Custom for this project specific GUI
"""
MARGIN_Y = 0
MARGIN_X = 11
PIXEL_WIDTH = 650
PIXEL_HEIGHT = 400


class BoardWidget(QWidget):
    """
    Class that define a widget that represent the state of the game's board.
    It takes the Model as parameter.

    It is responsible to convert the board state of the model in an object
    that can be show in the graphic interface.
    """

    def __init__(self, board):
        QWidget.__init__(self)
        self.array_board_conversion(board)

    def array_board_conversion(self, board):
        """
        Method for convert an numpy array to a label for the GUI.
        """
        # Convert the np array in a QImage with RGB channel
        qimage = array2qimage(board)
        # Converts the Qimage in a Pixmap that can be used as a paint device.
        pixmap = QPixmap.fromImage(qimage)
        # Scale the pixmap to the pixel dimensions of the GUI's BoardLayout
        pixmap = pixmap.scaled(PIXEL_WIDTH, PIXEL_HEIGHT)
        label = QLabel(self)
        label.setPixmap(pixmap)
        # To align the label in the center and set the form.
        label.setGeometry(QRect(MARGIN_X, MARGIN_Y, PIXEL_WIDTH, PIXEL_HEIGHT))
        # To create the outline of the rectangle and soften its shadow
        label.setFrameShape(QFrame.Box)
        label.setFrameShadow(QFrame.Sunken)
        label.show()
