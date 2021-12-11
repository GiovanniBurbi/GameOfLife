from PyQt5.QtWidgets import QMainWindow, QGraphicsScene

from view import BoardWidget, Ui_GameOfLife
from view.utilities import create_grid_over_scene, resize_grid_over_scene


class View(QMainWindow):
    """
    View component of the Model-View-Controller architecture.
    Setup and extends the GUI implemented with PyQT5 designer in Ui_GameOfLife.py

    Attributes:
        ui : User interface made with PyQt5 Designer. Access to all components of the GUI.
        board_widget : Custom widget, Graphic represent of the board.
        controller : Reference to an instance of the controller.
                     View delegates to this object any user's interaction with the GUI.
        overlay_grid : Item group that represent the grid over the board
        info_label_changed: flag to inform if the info label is changed
        max_board_width, max_board_height : max dimensions of the board matrix
        board_px_width, board_px_height : pixel dimensions of the board widget
    """

    def __init__(self):
        super().__init__()
        self._ui = Ui_GameOfLife()
        self._ui.setupUi(self)
        self.connect_events()
        self._overlay_grid = None
        self._board_widget = None
        self._controller = None
        self._info_label_changed = False
        self._board_px_height = None
        self._board_px_width = None
        self._max_board_height = None
        self._max_board_width = None
        self._ratio = None

    @property
    def ui(self):
        return self._ui

    def add_board_widget(self, board):
        """ Creates an instance of BoardWidget and adds it
        to the scene of graphic board into the GUI. Then call a method to create
         a gray grid over it."""
        # Retrieve pixel dimensions of the board widget
        self._board_px_height, self._board_px_width = self._ui.graphicBoard.maximumHeight(), self._ui.graphicBoard.maximumWidth()
        self._board_widget = BoardWidget(board, self._board_px_width, self._board_px_height, self)
        self._ui.graphicBoard.setScene(QGraphicsScene())
        self._ui.graphicBoard.scene().addWidget(self._board_widget)
        # Retrieve dimensions of the matrix representation of the board
        self._max_board_height, self._max_board_width = board.shape[:2]
        # Save ratio of the board matrix
        self._ratio = int(self._max_board_width / self._max_board_height)
        self._overlay_grid = create_grid_over_scene(self._max_board_width, self._max_board_height, self._board_px_width,
                                                    self._board_px_height, self._ui.graphicBoard.scene())

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
        self._ui.infoLabel.setText("Left click to set alive cells, Right click to kill alive cells")

    def connect_events(self):
        """ Method to connect GUI event to the handler """
        self._ui.zoomSlider.valueChanged.connect(self.set_scale)
        self._ui.clearButton.released.connect(self.clear_board)

    def set_scale(self):
        """ Handler of the board resize """
        value = self._ui.zoomSlider.value()
        self._controller.change_scale(value)
        # Calculate the new dimensions of the grid
        resized_height = self._max_board_height - self._ratio * value
        resized_width = self._max_board_width - (self._ratio * 2) * value
        self._overlay_grid = resize_grid_over_scene(resized_width, resized_height, self._board_px_width,
                                                    self._board_px_height, self._ui.graphicBoard.scene(),
                                                    self._overlay_grid)

    def clear_board(self):
        """ Handler of the clear command """
        self._controller.clear_board()
