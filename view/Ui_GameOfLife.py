# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GameOfLife(object):
    def setupUi(self, GameOfLife):
        GameOfLife.setObjectName("GameOfLife")
        GameOfLife.setEnabled(True)
        GameOfLife.resize(930, 646)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GameOfLife.sizePolicy().hasHeightForWidth())
        GameOfLife.setSizePolicy(sizePolicy)
        GameOfLife.setMinimumSize(QtCore.QSize(930, 646))
        GameOfLife.setMaximumSize(QtCore.QSize(930, 646))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        GameOfLife.setFont(font)
        GameOfLife.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        GameOfLife.setDocumentMode(False)
        GameOfLife.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(GameOfLife)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.configurationBox = QtWidgets.QGroupBox(self.centralwidget)
        self.configurationBox.setMaximumSize(QtCore.QSize(16777215, 65))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.configurationBox.setFont(font)
        self.configurationBox.setObjectName("configurationBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.configurationBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.historyButton = QtWidgets.QRadioButton(self.configurationBox)
        self.historyButton.setObjectName("historyButton")
        self.horizontalLayout.addWidget(self.historyButton, 0, QtCore.Qt.AlignLeft)
        self.loadPatternLabel = QtWidgets.QLabel(self.configurationBox)
        self.loadPatternLabel.setObjectName("loadPatternLabel")
        self.horizontalLayout.addWidget(self.loadPatternLabel, 0, QtCore.Qt.AlignRight)
        self.selectPatternBox = QtWidgets.QComboBox(self.configurationBox)
        self.selectPatternBox.setObjectName("selectPatternBox")
        self.horizontalLayout.addWidget(self.selectPatternBox)
        self.verticalLayout.addWidget(self.configurationBox)
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setMaximumSize(QtCore.QSize(16777215, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.infoLabel.setFont(font)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.BoardLayout = QtWidgets.QGridLayout()
        self.BoardLayout.setObjectName("BoardLayout")
        self.graphicBoard = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicBoard.sizePolicy().hasHeightForWidth())
        self.graphicBoard.setSizePolicy(sizePolicy)
        self.graphicBoard.setMaximumSize(QtCore.QSize(800, 400))
        self.graphicBoard.setBaseSize(QtCore.QSize(0, 0))
        self.graphicBoard.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicBoard.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicBoard.setObjectName("graphicBoard")
        self.BoardLayout.addWidget(self.graphicBoard, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.BoardLayout)
        self.controlsBox = QtWidgets.QGroupBox(self.centralwidget)
        self.controlsBox.setMinimumSize(QtCore.QSize(0, 100))
        self.controlsBox.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.controlsBox.setFont(font)
        self.controlsBox.setObjectName("controlsBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.controlsBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.playPauseButton = QtWidgets.QPushButton(self.controlsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playPauseButton.sizePolicy().hasHeightForWidth())
        self.playPauseButton.setSizePolicy(sizePolicy)
        self.playPauseButton.setMinimumSize(QtCore.QSize(180, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.playPauseButton.setFont(font)
        self.playPauseButton.setObjectName("playPauseButton")
        self.gridLayout_4.addWidget(self.playPauseButton, 0, 0, 1, 1)
        self.clearButton = QtWidgets.QPushButton(self.controlsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setMinimumSize(QtCore.QSize(0, 0))
        self.clearButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.clearButton.setFont(font)
        self.clearButton.setObjectName("clearButton")
        self.gridLayout_4.addWidget(self.clearButton, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 1, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.zoomLabel = QtWidgets.QLabel(self.controlsBox)
        self.zoomLabel.setObjectName("zoomLabel")
        self.gridLayout_6.addWidget(self.zoomLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.zoomSlider = QtWidgets.QSlider(self.controlsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomSlider.sizePolicy().hasHeightForWidth())
        self.zoomSlider.setSizePolicy(sizePolicy)
        self.zoomSlider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(8)
        self.zoomSlider.setSingleStep(1)
        self.zoomSlider.setProperty("value", 0)
        self.zoomSlider.setSliderPosition(0)
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.setObjectName("zoomSlider")
        self.gridLayout_6.addWidget(self.zoomSlider, 2, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.gridLayout_2.addLayout(self.gridLayout_6, 1, 4, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.framerateSlider = QtWidgets.QSlider(self.controlsBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framerateSlider.sizePolicy().hasHeightForWidth())
        self.framerateSlider.setSizePolicy(sizePolicy)
        self.framerateSlider.setMinimum(1)
        self.framerateSlider.setMaximum(100)
        self.framerateSlider.setSliderPosition(51)
        self.framerateSlider.setOrientation(QtCore.Qt.Horizontal)
        self.framerateSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.framerateSlider.setObjectName("framerateSlider")
        self.gridLayout_3.addWidget(self.framerateSlider, 1, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.framerateLabel = QtWidgets.QLabel(self.controlsBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.framerateLabel.setFont(font)
        self.framerateLabel.setObjectName("framerateLabel")
        self.gridLayout_3.addWidget(self.framerateLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.controlsBox)
        self.gridLayout.addLayout(self.verticalLayout, 4, 0, 1, 1)
        GameOfLife.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(GameOfLife)
        self.statusbar.setObjectName("statusbar")
        GameOfLife.setStatusBar(self.statusbar)

        self.retranslateUi(GameOfLife)
        QtCore.QMetaObject.connectSlotsByName(GameOfLife)

    def retranslateUi(self, GameOfLife):
        _translate = QtCore.QCoreApplication.translate
        GameOfLife.setWindowTitle(_translate("GameOfLife", "Conway\'s Game of Life"))
        self.configurationBox.setTitle(_translate("GameOfLife", "Configurations"))
        self.historyButton.setText(_translate("GameOfLife", "History"))
        self.loadPatternLabel.setText(_translate("GameOfLife", "Load Pattern:"))
        self.infoLabel.setText(_translate("GameOfLife", "Draw alive cells or Load a pattern and start the simulation"))
        self.controlsBox.setTitle(_translate("GameOfLife", "Controls"))
        self.playPauseButton.setText(_translate("GameOfLife", "Play"))
        self.clearButton.setText(_translate("GameOfLife", "Clear"))
        self.zoomLabel.setText(_translate("GameOfLife", "Zoom"))
        self.framerateLabel.setText(_translate("GameOfLife", "Framerate"))
