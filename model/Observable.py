from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class Observable(QObject):
    """ Class that implement the observable pattern"""
    valueChanged = pyqtSignal(object)
    errorChanged = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._value = None
        self._error = None

    # Register observers.
    def register(self, slot, error_slot):
        self.valueChanged.connect(slot)
        self.errorChanged.connect(error_slot)

    @pyqtProperty(object, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        self._value = newval
        self.valueChanged.emit(self.value)

    @pyqtProperty(object, notify=errorChanged)
    def error(self):
        return self._error

    @error.setter
    def error(self, newval):
        self._error = newval
        self.errorChanged.emit(self.error)
