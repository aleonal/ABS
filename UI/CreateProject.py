from UI.CausationExtractorWidget import CausationExtractorWidget
from src.ProjectController import ProjectController
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
from tkinter import *
import tkinter.messagebox

class CreateProjectWidget(QWidget):

    def __init__(self, projectInfo=None, project_status=True, previous_window=None):
        super().__init__()
        self.projectInfo = projectInfo
        self.previous_window = previous_window
        self.project_root = os.getcwd()
        self.ECELD_root = None
        self.UI()
        self.show()

    def UI(self):
        # Widget Layout
        self.setObjectName("Widget")
        self.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(640, 480))
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.widget_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setObjectName("widget_layout")
        self.input_layout = QtWidgets.QGridLayout()
        self.input_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.input_layout.setContentsMargins(-1, -1, -1, 0)
        self.input_layout.setVerticalSpacing(0)
        self.input_layout.setObjectName("input_layout")
        self.root_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.root_text.setObjectName("root_text")
        self.input_layout.addWidget(self.root_text, 0, 0, 1, 1)
        self.timeframe_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.timeframe_field.setObjectName("timeframe_field")
        self.timeframe_field.textChanged[str].connect(self.onTimeframeChanged)
        self.input_layout.addWidget(self.timeframe_field, 2, 1, 1, 1)
        self.import_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.import_field.setObjectName("import_field")
        self.input_layout.addWidget(self.import_field, 1, 1, 1, 1)

        # ECELd Project directory
        self.ECELD_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ECELD_button.sizePolicy().hasHeightForWidth())
        self.ECELD_button.setSizePolicy(sizePolicy)
        self.ECELD_button.setObjectName("ECELD_button")
        self.input_layout.addWidget(self.ECELD_button, 1, 2, 1, 1)
        self.ECELD_button.pressed.connect(self.GetECELDRoot)
        self.import_field.textChanged[str].connect(self.onECELDRootChanged)

        # ABS Project directory
        self.root_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.root_field.setObjectName("root_field")
        self.input_layout.addWidget(self.root_field, 0, 1, 1, 1)
        self.root_field.textChanged[str].connect(self.onProjectRootChanged)
        self.root_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.root_button.sizePolicy().hasHeightForWidth())
        self.root_button.setSizePolicy(sizePolicy)
        self.root_button.setObjectName("root_button")
        self.input_layout.addWidget(self.root_button, 0, 2, 1, 1)
        self.root_button.pressed.connect(self.GetProjectRoot)

        # Time frame
        self.timeframe_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.timeframe_text.setObjectName("timeframe_text")
        self.input_layout.addWidget(self.timeframe_text, 2, 0, 1, 1)
        self.import_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.import_text.setObjectName("import_text")
        self.input_layout.addWidget(self.import_text, 1, 0, 1, 1)
        self.input_layout.setRowStretch(0, 1)
        self.widget_layout.addLayout(self.input_layout)
        self.button_layout = QtWidgets.QGridLayout()
        self.button_layout.setObjectName("button_layout")
        
        # Help
        self.help_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.help_button.sizePolicy().hasHeightForWidth())
        self.help_button.setSizePolicy(sizePolicy)
        self.help_button.setObjectName("help_button")
        self.button_layout.addWidget(self.help_button, 0, 0, 1, 1)
        self.help_button.pressed.connect(self.help_window)

        # Create Project
        self.create_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_button.sizePolicy().hasHeightForWidth())
        self.create_button.setSizePolicy(sizePolicy)
        self.create_button.setObjectName("create_button")
        self.button_layout.addWidget(self.create_button, 0, 2, 1, 1)
        self.widget_layout.addLayout(self.button_layout)
        self.create_button.pressed.connect(self.CausationExtractor)

        # Message popup
        msg = tkinter.Tk()
        msg.geometry('0x0')

        # Retranslate window
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Create Project", "Create Project"))
        self.root_text.setText(_translate("Widget", "ABS Project Directory:\n"))
        self.timeframe_field.setText(_translate("Widget", "00:00:00"))
        self.import_field.setText(_translate("Widget", self.ECELD_root))
        self.root_field.setText(_translate("Widget", self.project_root))
        self.root_button.setText(_translate("Widget", "..."))
        self.ECELD_button.setText(_translate("Widget", "..."))
        self.timeframe_text.setText(_translate("Widget", "Time Frame in HH:MM:SS :"))
        self.import_text.setText(_translate("Widget", "ECELd Project Directory:"))
        self.help_button.setText(_translate("Widget", "Help"))
        self.create_button.setText(_translate("Widget", "Create Project"))
        self.setWindowIcon(QtGui.QIcon("A.png"))# A icon

    # Error message for invalid ABS Project Directory
    def errorRootMsg(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Error")
        messageBox.setText("Not a valid ABS Project Directory")
        messageBox.exec()

    # Error message for invalid ECELd Project Directory
    def errorDataMsg(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Error")
        messageBox.setText("Not a valid ECELd Project Directory")
        messageBox.exec()

    # Calls Causation Extractor when create project button is pressed
    def CausationExtractor(self):
        check_datafolder = os.path.isdir(self.import_field.text())
        check_rootfolder = os.path.isdir(self.root_field.text())
        if not (check_rootfolder):
          print("Not a Valid ABS Project Directory")
          self.errorRootMsg()
        elif not(check_datafolder):
          print("Not a Valid ECELd Project Directory")
          self.errorDataMsg()
        else:
          ProjectController.create_project(self.import_field.text(), self.root_field.text(), "Test",self.timeframe_field.text())
          self.CEWidget = CausationExtractorWidget(previous_window=self)
          self.CEWidget.show()
          self.previous_window.update_tabs()
          self.hide()

    # Gets ABS Project Directory
    def GetProjectRoot(self):
        self.project_root = QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.root_field.setText(self.project_root)

    # Gets ECELd Project Directory
    def GetECELDRoot(self):
        self.ECELD_root = QFileDialog.getExistingDirectory(self, 'Open Directory')
        # If ECELd project directory does not contain the ecel-export folder with parsed data, it's invalid
        try:
            for root, subdirs, files in os.walk(self.ECELD_root):
                for d in subdirs:
                    if 'ecel-export' in d:
                        export = d
            self.ECELD_root = self.ECELD_root + "/" + export
        except:
            self.errorDataMsg()
            self.ECELD_root = None
        self.import_field.setText(self.ECELD_root)

    def onProjectRootChanged(self, text):
        self.root_field.setText(text)

    def onECELDRootChanged(self, text):
        self.import_field.setText(text)

    def onTimeframeChanged(self, text):
        self.timeframe_field.setText(text)

    def help_window(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Help")
        messageBox.setText("ABS Project Directory: Select folder to store ABS Project data.\n\n" +
                           "ECELd Project Directory: Select the folder that contains the ECELd Project recorded\n \tdata.\n" +
                           "\tA valid ECELd project file contains the ecel-export.. parsed data.\n\n" +
                           "Time Frame: Input the time in the format HH:MM:SS by which you would like the data\n \tto be separated in the Builder.\n\n" +
                           "Create Project: Select Create Project after filing out all of the fields above.\n\n" +
                           "Cancel by closing the window.")
        messageBox.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = CreateProjectWidget()
    ui.UI()
    ui.show()
    sys.exit(app.exec_())
