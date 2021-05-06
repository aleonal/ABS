from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
from src import CausationExtractor
from UI.ProjectInfoWidget import ProjectInfoWidget
from datetime import datetime
from src import ProjectController
import json

class CausationExtractorWidget(QWidget):

    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
        self.UI()
        self.show()
        self.startCE()

    def startCE(self):
        # Create instance of Causation Extractor
        self.progress.setProperty("value", 5)
        self.CE = CausationExtractor.CausationExtractor()
        # Set ECELd directory
        self.progress.setProperty("value", 10)
        self.CE.set_eceld_project_root(project_root=ProjectController.ProjectController.get_eceld_project_root())
        # Set ABS Project directory
        self.progress.setProperty("value", 15)
        self.CE.set_output_folder(output_folder=ProjectController.ProjectController.get_project_directory())
        # Set Time Frame
        self.progress.setProperty("value", 20)
        self.CE.set_time_frame(str(ProjectController.ProjectController.get_time_frame()))
        # Load salient artifacts
        self.progress.setProperty("value", 25)
        self.CE.load_salient_artifacts()
        # Import events from ECELd directory
        self.progress.setProperty("value", 35)
        self.CE.import_events()
        # Group Events by Time Frame
        self.progress.setProperty("value", 50)
        self.CE.group_by_time()
        # Group Events by Salient Artifact
        self.progress.setProperty("value", 75)
        self.CE.group_by_salient_artifacts()
        self.progress.setProperty("value", 100)
        

    def UI(self):
        # Widget setup
        self.setObjectName("Widget")
        self.resize(320, 240)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(320, 240))
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 301, 221))
        self.layoutWidget.setObjectName("layoutWidget")
        self.widget_layout = QtWidgets.QGridLayout(self.layoutWidget)
        self.widget_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setSpacing(0)
        self.widget_layout.setObjectName("widget_layout")

        # Progress Bar setup
        self.progress = QtWidgets.QProgressBar(self.layoutWidget)
        self.progress.setProperty("value", 0)
        self.progress.setObjectName("progress")
        self.widget_layout.addWidget(self.progress, 1, 0, 1, 1)

        # Continue button setup
        self.continueButton = QtWidgets.QPushButton(self.layoutWidget)
        self.continueButton.setSizePolicy(sizePolicy)
        self.continueButton.setCheckable(False)
        self.continueButton.setAutoDefault(False)
        self.continueButton.setDefault(False)
        self.continueButton.setFlat(False)
        self.continueButton.setObjectName("continueButton")
        self.widget_layout.addWidget(self.continueButton, 2, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.continueButton.clicked.connect(self.continueDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continueButton.sizePolicy().hasHeightForWidth())
    
        # Cancel button setup
        self.cancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.cancelButton.clicked.connect(self.closeRoutine)
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setCheckable(False)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setDefault(False)
        self.cancelButton.setFlat(False)
        self.cancelButton.setObjectName("cancelButton")
        self.widget_layout.addWidget(self.cancelButton, 2, 0, 1, 1, QtCore.Qt.AlignRight)

        # Progress Text setup
        self.progress_text = QtWidgets.QLabel(self.layoutWidget)
        self.progress_text.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_text.setObjectName("progress_text")
        self.widget_layout.addWidget(self.progress_text, 0, 0, 1, 1)

        # Retranslate
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Widget", "Causation Extractor"))
        self.continueButton.setText(_translate("Widget", "Continue"))
        self.cancelButton.setText(_translate("Widget", "Cancel"))
        self.progress_text.setText(_translate("Widget", "Causation Extractor Progress"))
        self.setWindowIcon(QtGui.QIcon("A.png")) # ABS logo

    # Continue notifies the user of events loaded and not loaded before closing the window
    def continueDialog(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Event information")
        messageBox.setText(self.CE.get_notify_events_loaded() + "\n" + self.CE.get_notify_events_not_loaded())
        messageBox.exec()
        self.close()

    # Cancel takes you back to Create Project window
    def closeRoutine(self):
        if self.previous_window:
            self.previous_window.show()
            self.hide()
        else:
            self.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = CausationExtractorWidget()
    ui.show()
    sys.exit(app.exec_())
