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
