from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
from subprocess import Popen, PIPE
from src.Validator import Validator


import sys
import os
import subprocess, signal, time, ctypes
import re
import threading
from src.ProjectController import ProjectController

class RunnerWidget(QWidget):
    def __init__(self, project=None):
        super().__init__()
        self.setWindowTitle("Runner")
        self.setGeometry(50,50,482,432)
        self.UI()
        self.show()
        self.script_name = None

    def UI(self):
        # Grid layout
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")

        # Script display window
        self.script_display = QPlainTextEdit()
        self.script_display.setGeometry(QtCore.QRect(10,40,381,471))
        self.script_display.setReadOnly(True)

        # Load Script onto display window button/action
        self.load_script_button = QtWidgets.QPushButton(self)
        self.load_script_button.setGeometry(QtCore.QRect(370, 480, 151, 41))
        self.load_script_button.setObjectName("load_script_button")
        self.load_script_button.clicked.connect(self.display_script)

        # Script run button/script execution
        self.run_button = QtWidgets.QPushButton(self)
        self.run_button.setGeometry(QtCore.QRect(700,520,75,23))
        self.run_button.setObjectName("run_button")
        self.run_button.clicked.connect(self.execute_script)
        self.run_button.setEnabled(False)

        # Script stop button/stop script execution
        self.stop_button = QtWidgets.QPushButton(self)
        self.stop_button.setGeometry(QtCore.QRect(620,520,75,23))
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop_script)
        self.stop_button.setEnabled(False)

        # Progress terminal
        self.progress_terminal = QtWidgets.QTextEdit()
        self.progress_terminal.setGeometry(QtCore.QRect(400, 40, 381, 471))
        self.progress_terminal.setObjectName("progress_terminal")
        
        # Timeout
        self.script_timeout = QtWidgets.QSpinBox(self)
        self.script_timeout.setGeometry(QtCore.QRect(370, 450, 151, 22))
        self.script_timeout.setMinimum(1)
        self.script_timeout.setObjectName("script_timeout")
        
        # Widget layout
        self.gridLayout.addWidget(self.progress_terminal,1,3)
        self.gridLayout.addWidget(self.script_timeout,2,3)
        self.gridLayout.addWidget(self.run_button, 0,3)
        self.gridLayout.addWidget(self.stop_button, 3,3)
        self.gridLayout.addWidget(self.load_script_button,0,0)
        self.gridLayout.addWidget(self.script_display, 1, 0)
        self.setLayout(self.gridLayout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("RunnerTab", "Runner"))
        self.load_script_button.setText(_translate("RunnerTab", "Load Script"))
        self.run_button.setText(_translate("RunnerTab", "Run"))
        self.stop_button.setText(_translate("RunnerTab", "Stop"))

    # Creates an instance of the validator that executes the scripts along with ECELd for verification
    def execute_script(self):
        script_path = self.script_name.replace('.py', '')
        self.stop_button.setEnabled(True)
        self.run_button.setEnabled(False)
        self.validator = Validator(self.script_timeout.value(), script_path, self.progress_terminal)
        self.validator.validate()
        self.stop_script()

    # DIsplays string text on right window
    def print_progress(self, text):
        cursor = self.progress_terminal.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        
    # Prints to the program that the process has stopped
    def stop_script(self):
        self.print_progress("Program stopped\n")
        self.stop_button.setEnabled(False)
        self.run_button.setEnabled(True)

    # Loads python file contents onto the left window
    def display_script(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.script_name, _ = QFileDialog.getOpenFileName(self,"Open Script", "","Python Files (*.py)", options=options)
            with open(self.script_name, 'r') as f:
                self.script_display.setPlainText(f.read())
            self.run_button.setEnabled(True)
            self.progress_terminal.clear()
        except:
            pass
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = RunnerWidget()
    ui.show()
    sys.exit(app.exec_())
   