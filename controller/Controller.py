from PyQt5.QtCore import QTimer


""" Constant for amplify rate values into millisec """
AMPLIFIER = 13
""" Constant for the default lifetime of a single generation """
DEFAULT_LIFETIME = 700


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
        generation_lifetime : current time between successive generations
    """

    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._generation_lifetime = DEFAULT_LIFETIME

        # Init list of patterns in the view and then connect events
        self._view.init_patterns_list(self._model.patterns)
        self._view.connect_events()

        # Register update_board method to receive the updates from the model about the board state
        model.register(self.update_board)

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

    def play_pause_game(self):
        """ Recursive method that decide the timing of the board evolutions, timing based on the current lifetime """
        if self._view.is_play_pressed:
            self._model.next_generation()
            QTimer.singleShot(self._generation_lifetime, self.play_pause_game)

    def change_rate(self, rate):
        """ Method that change the current lifetime based on a rate passed as parameter. """
        self._generation_lifetime = DEFAULT_LIFETIME + (rate * AMPLIFIER)

    def selected_pattern(self, pattern):
        """ Delegates to the model the load of a pattern """
        self._model.load_pattern(pattern)
