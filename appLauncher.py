from PyQt5.QtWidgets import QApplication

from controller.Controller import Controller
from model.Model import Model
from view.View import View

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    model = Model()
    window = View()
    controller = Controller(model, window)
    controller.add_board_widget_to_ui()
    window.show()
    sys.exit(app.exec_())
