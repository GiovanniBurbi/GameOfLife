from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem


def create_grid_over_scene(width, height, px_width, px_height, scene):
    """ Method that creates a gray grid as ItemGroup and adds it to a scene """
    pen = QPen(Qt.gray)
    grid = QGraphicsItemGroup()
    for x in range(1, width):
        xc = x * (px_width / width)
        line = QGraphicsLineItem(QLineF(xc, 0, xc, px_height))
        line.setPen(pen)
        grid.addToGroup(line)

    for y in range(1, height):
        yc = y * (px_height / height)
        line = QGraphicsLineItem(QLineF(0, yc, px_width, yc))
        line.setPen(pen)
        grid.addToGroup(line)

    scene.addItem(grid)
