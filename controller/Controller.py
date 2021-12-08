class Controller(object):
    """
    Controller component of the Model-View-Controller architecture.
    It is responsible of connect the view with the model so that
    they can stay decoupled.
    """

    def __init__(self, model, view):
        self._model = model
        self._view = view

    def add_board_widget_to_ui(self):
        """ Calls view's add board widget method
         passing the model's board"""
        self._view.add_board_widget(self._model.board)

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
