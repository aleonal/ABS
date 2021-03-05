import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
import os
import json
from src.ProjectController import ProjectController
from ArtifactsTableWidget import SalientArtifactWindow

class BuilderWidget(QWidget):

    def __init__(self, project=None):
        super().__init__()
        self.setGeometry(50, 50, 482, 432)
        self.setWindowTitle("Builder")
        self.UI()
        self.artifacts_window = SalientArtifactWindow()
        self.show()

    def UI(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")

        #Create search bar
        self.label = QLabel('Builder', self)
        self.label.setObjectName(u"label")
        self.label.setFont(QFont('MS Shell Dlg 2', 12))
        self.gridLayout.addWidget(self.label, 0, 1)

        self.search_button = QPushButton('Search', self)
        self.gridLayout.addWidget(self.search_button, 1,2,1,1)

        self.lineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.lineEdit, 1,1,1,1)

        self.listthing = QListWidget(self)
        self.gridLayout.addWidget(self.listthing, 2, 1)

        self.edit_artifacts_button = QPushButton('Edit Salient Artifacts', self)
        self.gridLayout.addWidget(self.edit_artifacts_button, 1, 0)
        self.edit_artifacts_button.clicked.connect(self.openArtifacts)

        self.save_button = QPushButton('Save Project', self)
        self.gridLayout.addWidget(self.save_button, 3, 2)

        self.setLayout(self.gridLayout)
    def openArtifacts(self):
        if ProjectController.is_project_loaded():
            self.artifacts_window.populate_table()
            self.artifacts_window.show()
        else:
            QMessageBox.critical(self, "Project Error", "No project is currently loaded.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())