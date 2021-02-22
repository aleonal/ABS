import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
import os

class BuilderWidget(QWidget):

    def __init__(self):
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

        self.add_artifact_button = QPushButton('Add Salient Artifact', self)
        self.gridLayout.addWidget(self.add_artifact_button, 1, 0)
        self.add_artifact_button.clicked.connect(self.openArtifacts)

        self.save_button = QPushButton('Save Project', self)
        self.gridLayout.addWidget(self.save_button, 3, 2)

        self.setLayout(self.gridLayout)
    def openArtifacts(self):
        self.artifacts_window.show()

class SalientArtifactWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 482, 432)
        self.setWindowTitle("Salient Artifacts")
        self.UI()

    def UI(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        # Creating table
        self.reportTable = QTableWidget(0, 2, self)

        # Creating headers for columns in table
        lineNumHeader = QTableWidgetItem('Artifact Number')
        self.reportTable.setHorizontalHeaderItem(0, lineNumHeader)
        descriptionHeader = QTableWidgetItem('Description')
        self.reportTable.setHorizontalHeaderItem(1, descriptionHeader)

        emptyHeader = QTableWidgetItem()
        self.reportTable.horizontalHeader().setStretchLastSection(True)
        self.reportTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.gridLayout.addWidget(self.reportTable, 1, 0, 1, 4)

        self.enforcementLabel = QLabel('Salient Artifacts', self)
        self.enforcementLabel.setObjectName(u"artifactLabel")
        self.enforcementLabel.setFont(font)
        self.gridLayout.addWidget(self.enforcementLabel, 0, 1, 1, 1)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.clicked.connect(self.window().close)
        self.gridLayout.addWidget(self.cancelButton, 2, 4, 1, 2)
        self.setLayout(self.gridLayout)


    def close(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())