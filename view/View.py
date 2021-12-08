from PyQt5.QtWidgets import QMainWindow

from view import BoardWidget, Ui_GameOfLife


class View(QMainWindow):
    """
    View component of the Model-View-Controller architecture.
    Setup and extends the GUI implemented with PyQT5 designer in Ui_GameOfLife.py

    Attributes:
        ui : User interface made with PyQt5 Designer. Access to all components of the GUI.
        board_widget : Custom widget, Graphic represent of the board.
        controller : Reference to an instance of the controller.
                     View delegates to this object any user's interaction with the GUI.
    """

    def __init__(self):
        super().__init__()
        self._ui = Ui_GameOfLife()
        self._ui.setupUi(self)
        self._board_widget = None
        self._controller = None
        self._info_label_changed = False

    @property
    def ui(self):
        return self._ui

    def add_board_widget(self, board):
        """ Creates an instance of BoardWidget and adds it
        to the BoardLayout of the user interface """
        self._board_widget = BoardWidget(board, self)
        self._ui.BoardLayout.addWidget(self._board_widget)

    def set_controller(self, controller):
        """ Setter of the controller instance. """
        self._controller = controller

    def update_view(self, board):
        """ Delegates to the board widget the update of the board graphic """
        self._board_widget.update_board_state(board)

    def set_cell_alive(self, x, y):
        """ Delegates to the controller the change in the state of the cell
         The first time that the user set a cell alive, changes the info label"""
        self._controller.state_cell_to_alive(x, y)
        if not self._info_label_changed:
            self.change_info_label()

    def set_cell_dead(self, x, y):
        """ Delegates to the controller the change in the state of the cell """
        self._controller.state_cell_to_dead(x, y)

    def change_info_label(self):
        """ Method to change info label"""
        self._info_label_changed = True
        self._ui.infoLabel.setText("Left click to set alive cells, Right click to set dead cells")
