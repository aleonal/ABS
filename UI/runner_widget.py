# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *


class Ui_RunnerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Runner")
        self.UI()
        self.show()

    def UI(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setColumnStretch(1, 1)

        self.script_menu = QtWidgets.QComboBox(self)
        self.script_menu.setGeometry(QtCore.QRect(0, 0, 361, 22))
        self.script_menu.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.script_menu.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.script_menu.setAcceptDrops(True)
        self.script_menu.setEditable(True)
        self.script_menu.setObjectName("script_menu")
        self.script_menu.addItem("")
        self.script_menu.addItem("")
        self.script_menu.addItem("")

        self.script_display = QtWidgets.QGraphicsView(self)
        self.script_display.setGeometry(QtCore.QRect(0, 30, 361, 491))
        self.script_display.setObjectName("script_display")

        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setGeometry(QtCore.QRect(370, 480, 151, 41))
        self.run_button.setObjectName("run_button")

        self.script_progress_terminal = QtWidgets.QGraphicsView(self)
        self.script_progress_terminal.setGeometry(QtCore.QRect(370, 30, 151, 411))
        self.script_progress_terminal.setObjectName("script_progress_terminal")

        self.script_progress_bar = QtWidgets.QProgressBar(self)
        self.script_progress_bar.setGeometry(QtCore.QRect(370, 0, 161, 20))
        self.script_progress_bar.setProperty("value", 24)
        self.script_progress_bar.setObjectName("script_progress_bar")

        self.script_timeout = QtWidgets.QSpinBox(self)
        self.script_timeout.setGeometry(QtCore.QRect(370, 450, 151, 22))
        self.script_timeout.setMinimum(1)
        self.script_timeout.setObjectName("script_timeout")

        self.gridLayout.addWidget(self.script_progress_bar,0,3)
        self.gridLayout.addWidget(self.script_progress_terminal,1,3,1,1)
        self.gridLayout.addWidget(self.script_timeout,2,3)
        self.gridLayout.addWidget(self.run_button, 3, 3)
        self.gridLayout.addWidget(self.script_menu,0,0,1,2)
        self.gridLayout.addWidget(self.script_display, 1,0,1,2)

        self.setLayout(self.gridLayout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("RunnerTab", "Runner"))
        self.script_menu.setCurrentText(_translate("RunnerTab", "Script1"))
        self.script_menu.setItemText(0, _translate("RunnerTab", "Script1"))
        self.script_menu.setItemText(1, _translate("RunnerTab", "Script2"))
        self.script_menu.setItemText(2, _translate("RunnerTab", "Script3"))
        self.run_button.setText(_translate("RunnerTab", "Run"))


