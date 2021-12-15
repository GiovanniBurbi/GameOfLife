import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog, QMessageBox

from view import BoardWidget, Ui_GameOfLife
from view.utilities import create_grid_over_scene, resize_grid_over_scene

""" Info messages to show in the GUI """
ENTRY_INFO = "Draw alive cells or Load a pattern before starting the simulation"
DRAW_INFO = "Left click to set alive cells, right click to kill cells, hold scroll button for panning"


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
        ratio : ratio of the max dimensions of the board matrix
        board_px_width, board_px_height : pixel dimensions of the board widget
        play_pressed : flag to inform if the play button has been pressed
        default_framerate : default framerate value
    """

    def __init__(self):
        super().__init__()
        self._ui = Ui_GameOfLife()
        self._ui.setupUi(self)
        self._overlay_grid = None
        self._board_widget = None
        self._controller = None
        self._info_label_changed = False
        self._board_px_height = None
        self._board_px_width = None
        self._max_board_height = None
        self._max_board_width = None
        self._ratio = None
        self._play_pressed = False
        self._default_framerate = self._ui.framerateSlider.value()
        self._pattern_error = False

    @property
    def is_play_pressed(self):
        return self._play_pressed

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
            self.change_info_label(DRAW_INFO)

    def set_cell_dead(self, x, y):
        """ Delegates to the controller the change in the state of the cell """
        self._controller.state_cell_to_dead(x, y)

    def change_info_label(self, msg):
        """ Method to change info label"""
        self._ui.infoLabel.setText(msg)
        self._info_label_changed = not self._info_label_changed

    def connect_events(self):
        """ Method to connect GUI event to the handler """
        self._ui.zoomSlider.valueChanged.connect(self.set_scale)
        self._ui.clearButton.released.connect(self.clear_board)
        self._ui.playPauseButton.released.connect(self.play_pause)
        self._ui.framerateSlider.valueChanged.connect(self.set_rate)
        self._ui.selectPatternBox.currentIndexChanged.connect(self.choose_pattern)
        self._ui.historyButton.toggled.connect(self.history_switch)
        self._ui.loadButton.released.connect(self.load_pattern)

    def set_scale(self, value):
        """ Handler of the board resize """
        self._controller.change_scale(value)
        # Calculate the new dimensions of the grid
        resized_height = self._max_board_height - self._ratio * value
        resized_width = self._max_board_width - (self._ratio * 2) * value
        self._overlay_grid = resize_grid_over_scene(resized_width, resized_height, self._board_px_width,
                                                    self._board_px_height, self._ui.graphicBoard.scene(),
                                                    self._overlay_grid)

    def clear_board(self):
        """ Handler of the clear command.
         If the play button is pressed then it stops the simulation. """
        self._controller.clear_board()
        if self._play_pressed:
            self.play_pause()
        self.reset_pattern_selection()
        self.change_info_label(ENTRY_INFO)

    def play_pause(self):
        """ Handler of the play command """
        self.switch_play_pause_label()
        self._controller.play_pause_game()

    def switch_play_pause_label(self):
        """ Method to switch the play-pause button and the play pressed flag """
        if not self._play_pressed:
            self._ui.playPauseButton.setText("Pause")
            self._play_pressed = True
        else:
            self._ui.playPauseButton.setText("Play")
            self._play_pressed = False

    def set_rate(self, value):
        """ Handler of the changes of the framerate """
        variation = self._default_framerate - value
        self._controller.change_rate(variation)

    def choose_pattern(self, pattern_index):
        """ Handler of the newly selected option in the combo box, select pattern.
         It stops the simulation if it was running, change the info label to the initial one
         and reset the zoom of the board."""
        self.reset_zoom()
        if pattern_index != 0:
            if not self._info_label_changed:
                self.change_info_label(DRAW_INFO)
            if self._play_pressed:
                self.play_pause()
            # Take the data (path of pattern file) associate
            # with the item at the given index
            pattern = self._ui.selectPatternBox.itemData(pattern_index)
            self._controller.selected_pattern(pattern)

    def init_patterns_list(self, patterns_path):
        """ Method to set the list of the combo box and its element's font style """
        pattern_box = self._ui.selectPatternBox
        # Add info placeholder in combo box
        pattern_box.addItem("------ Select a Pattern -----")
        pattern_box.model().item(0).setEnabled(False)
        for path in patterns_path:
            # Extract name from file path
            pattern_name = re.split('[/.]', path)[-2]
            # Add pattern file path as data of item
            pattern_box.addItem(pattern_name, path)
        self.pattern_list_style()

    def pattern_list_style(self):
        """ Method to set the font of the elements in the combo box list """
        font = QFont()
        font.setBold(True)
        font.setPointSize(self._ui.selectPatternBox.font().pointSize())
        pattern_box = self._ui.selectPatternBox
        num_elements = pattern_box.count()
        [pattern_box.model().item(i + 1).setFont(font) for i in range(num_elements - 1)]

    def reset_pattern_selection(self):
        """ Method to reset to default the current text shown in the combo box """
        pattern_menu = self._ui.selectPatternBox
        if pattern_menu.currentText() != pattern_menu.model().item(0).text():
            pattern_menu.setCurrentText(pattern_menu.model().item(0).text())

    def reset_zoom(self):
        """ Method to reset the value of the zoom slider"""
        self._ui.zoomSlider.setValue(0)

    def history_switch(self, enabled):
        """ Handler change of state of the history radio button"""
        self._controller.history_switch(enabled)

    def panning_activated(self, x, y):
        """ Delegates to the controller the activation of the panning mode
         And changes the cursor to an open hand"""
        self._ui.graphicBoard.viewport().setCursor(QCursor(Qt.OpenHandCursor))
        self._controller.panning_activated(x, y)

    def panning(self, x, y):
        """ Delegates to the controller panning of the board """
        self._controller.panning(x, y)

    def cursor_moved(self):
        """ Method to change the cursor in a closed hand """
        self._ui.graphicBoard.viewport().setCursor(QCursor(Qt.ClosedHandCursor))

    def panning_deactivated(self):
        """ Delegates to the controller the deactivation of the panning mode
         and changes cursor back to the standard arrow"""
        self._ui.graphicBoard.viewport().setCursor(QCursor(Qt.ArrowCursor))
        self._controller.panning_deactivated()

    def load_pattern(self):
        """ Handler of press of load button.
        Pause the simulation if it was running and if select a valid file
        change info label, load the pattern and add the new pattern in the combo box"""
        if self._play_pressed:
            self.play_pause()
        file_name, filter_selected = QFileDialog.getOpenFileName(self, "Open Pattern File",
                                                                 filter="Rle file (*.rle)",
                                                                 options=QFileDialog.DontUseNativeDialog)
        # If selected a valid file..
        if file_name:
            self.reset_zoom()
            if not self._info_label_changed:
                self.change_info_label(DRAW_INFO)
            self._controller.selected_pattern(file_name)
            self.add_pattern_item(file_name)

    def add_pattern_item(self, pattern):
        """ Method to add to the combo box the item (name, path)
         representing the newly loaded pattern """
        if not self._pattern_error:
            # Extract pattern name from path without file extension
            pattern_name = re.split('/', pattern)[-1]
            pattern_name = ".".join(re.split('[.]', pattern_name)[:-1])
            pattern_box = self._ui.selectPatternBox
            # Flag to indicate if the pattern loaded is already listed in
            # the combo box
            duplicate = False
            # Look if this pattern is already in the combo box
            for i in range(pattern_box.count()):
                if pattern_box.model().item(i).text() == pattern_name:
                    duplicate = True
                    # set current position in the combo box to the position of the
                    # pattern found in the combo list
                    pattern_box.setCurrentIndex(i)
                    break
            if not duplicate:
                # Block pattern box currentIndexChanged signal while
                # adding a new item and set the current index to the new one
                pattern_box.blockSignals(True)
                pattern_box.addItem(pattern_name, pattern)
                pattern_box.setCurrentIndex(pattern_box.count() - 1)
                pattern_box.blockSignals(False)
        else:
            self._pattern_error = False

    def show_error(self, error_msg):
        self._pattern_error = True
        QMessageBox.about(self, "Pattern Error", error_msg)
