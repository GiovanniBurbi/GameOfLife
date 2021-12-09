from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage


def matrix_board_conversion(label, board, px_width, px_height):
    """
    Method for convert an numpy array to a label for the GUI.
    It updates the pixmap of the label passed as parameter to the method and
    scales it to the pixel dimensions required.
    """
    # Convert the np array in a QImage with RGB channel
    qimage = array2qimage(board)
    # Converts the Qimage in a Pixmap that can be used as a paint device.
    pixmap = QPixmap.fromImage(qimage)
    # Scale the pixmap to the pixel dimensions of the GUI's BoardLayout
    pixmap = pixmap.scaled(px_width, px_height)
    label.setPixmap(pixmap)
