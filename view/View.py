from PyQt5.QtWidgets import QMainWindow

from view import BoardWidget, Ui_GameOfLife


class View(QMainWindow):
    """
    View component of the Model-View-Controller architecture.
    Extend the GUI implemented with PyQT5 designer in Ui_GameOfLife.py
    """

    def __init__(self):
        super().__init__()
        self._ui = Ui_GameOfLife()
        self._ui.setupUi(self)
        self._board_widget = None

    @property
    def ui(self):
        return self._ui

    def add_board_widget(self, board):
        """ Creates an instance of BoardWidget and adds it
        to the BoardLayout of the user interface """
        self._board_widget = BoardWidget(board)
        self._ui.BoardLayout.addWidget(self._board_widget)
