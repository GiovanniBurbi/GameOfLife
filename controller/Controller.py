from PyQt5.QtCore import QTimer


class Controller(object):
    """
    Controller component of the Model-View-Controller architecture.
    It is responsible of connect the view with the model so that
    they can stay decoupled.
    It subscribes to the model so that it can receive the updated board at the
    moment of the modification.

    Attributes:
        model : Reference to an instance of the Model.
        view : Reference to an instance of the View.
        generation_lifetime : time between successive generations
        timer : timer that controls the rate of evolution of the board simulation
    """

    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._generation_lifetime = 1000
        self._timer = QTimer()

        # Register update_board method to receive the updates from the model about the board state
        model.register(self.update_board)
        # Connect timeout signal to the model's method that generate the next evolution of the board's state.
        self._timer.timeout.connect(self._model.next_generation)

    def add_board_widget_to_ui(self):
        """ Calls view's add board widget method
         passing the model's board"""
        self._view.add_board_widget(self._model.visible_board)

    def state_cell_to_alive(self, x, y):
        """ Delegates to the model the command to change a cell state
        passing its 2D coordinates."""
        self._model.alive_cell(x, y)

    def state_cell_to_dead(self, x, y):
        """ Delegates to the model the command to change a cell state
        passing its 2D coordinates."""
        self._model.dead_cell(x, y)

    def update_board(self, board):
        """ Delegates to the view the update of the board state
        passing the updated board as numpy array"""
        self._view.update_view(board)

    def change_scale(self, value):
        """ Delegates to the model the resize of the board """
        self._model.resize(value)

    def clear_board(self):
        """ Delegates to the model the clear of the board. """
        self._model.clear()

    def start_pause_game(self, play):
        """ Method to start and stop the timer of the game based on the boolean
        passed as parameter. """
        if play:
            # emit on start simulation
            self._timer.timeout.emit()
            # then set the timer with the interval between successive generations.
            self._timer.start(self._generation_lifetime)
        else:
            self._timer.stop()
