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
        self.script_file_path = None

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
        self.save_button.clicked.connect(self.save_script)

        self.setLayout(self.gridLayout)
        
    def openArtifacts(self):
        if ProjectController.is_project_loaded():
            self.artifacts_window.populate_table()
            self.artifacts_window.show()
        else:
            QMessageBox.critical(self, "Project Error", "No project is currently loaded.")

    def save_script(self):
        if not self.script_file_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this script as...", "", "All files(*)")
            if new_file_path:
                self.script_file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False 
        #TODO: Write file into path (need to figure out format)
    
    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())