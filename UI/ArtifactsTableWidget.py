import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
from src.ProjectController import ProjectController

class SalientArtifactWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 482, 432)
        self.setWindowTitle("Salient Artifacts")
        self.setWindowIcon(QIcon("A.png"))#A icon
        self.UI()

    def UI(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")

        font = QFont()
        font.setPointSize(12)


        # Creating table with no rows
        self.artifactsTable = QTableWidget(0, 3, self)

        # Creating headers for columns in table
        type_header = QTableWidgetItem('Artifact Type')
        self.artifactsTable.setHorizontalHeaderItem(0, type_header)
        descriptionHeader = QTableWidgetItem('Description')
        self.artifactsTable.setHorizontalHeaderItem(1, descriptionHeader)

        emptyHeader = QTableWidgetItem('')
        self.artifactsTable.setHorizontalHeaderItem(2, emptyHeader)

        self.artifactsTable.horizontalHeader().setStretchLastSection(True)
        self.artifactsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.gridLayout.addWidget(self.artifactsTable, 1, 0)

        self.artifactsLabel = QLabel('Salient Artifacts List', self)
        self.artifactsLabel.setObjectName(u"artifactLabel")
        self.artifactsLabel.setFont(font)
        self.gridLayout.addWidget(self.artifactsLabel, 0, 0)

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.clicked.connect(self.close)
        self.gridLayout.addWidget(self.cancelButton, 3, 1)

        self.colorPickerButton = QPushButton('Select Color', self)
        self.colorPickerButton.setObjectName(u"colorPickerButton")
        self.colorPickerButton.clicked.connect(self.changeArtifactColor)
        self.gridLayout.addWidget(self.colorPickerButton, 2, 1)

        self.saveChangesButton = QPushButton('Save Changes', self)
        self.saveChangesButton.setObjectName(u"saveChangesButton")
        self.saveChangesButton.clicked.connect(self.saveArtifacts)
        self.gridLayout.addWidget(self.saveChangesButton, 1, 1)

        self.addArtifactButton = QPushButton('Add Artifact', self)
        self.addArtifactButton.setObjectName(u"saveChangesButton")
        self.addArtifactButton.clicked.connect(self.addArtifact)
        self.gridLayout.addWidget(self.addArtifactButton, 0, 1)

        self.setLayout(self.gridLayout)

    def changeArtifactColor(self):
        artifactColor = QColorDialog.getColor()
        ProjectController.set_artifact_color(artifactColor)

    def populate_table(self):
        artifacts_list = ProjectController.get_salient_artifacts_json()
        self.artifactsTable.setRowCount(len(artifacts_list))
        i=0
        for artifact in artifacts_list:
            artifactType = QComboBox()
            artifactType.addItems(["","traffic", "trafficThroughput", "clicks", "keypresses", "timed", "auditd"])
            index = artifactType.findText(artifact['type'])
            artifactType.setCurrentIndex(index)
            artifactDescription = QTableWidgetItem(str(artifact['artifact']))

            self.artifactsTable.setCellWidget(i, 0, artifactType)
            self.artifactsTable.setItem(i, 1, artifactDescription)

            deleteButton = QPushButton('Delete')
            deleteButton.clicked.connect(self.deleteRow)
            self.artifactsTable.setCellWidget(i, 2, deleteButton)
            i += 1

    def deleteRow(self):
        button = self.sender()
        if button:
            row = self.artifactsTable.indexAt(button.pos()).row()
            self.artifactsTable.removeRow(row)

    def saveArtifacts(self):
        artifactsList = ""
        #save whatever is in the table to json file in the correct format

    def addArtifact(self):
        self.artifactsTable.setRowCount(self.artifactsTable.rowCount()+1)
        current_row_pos = self.artifactsTable.rowCount()-1
        artifactType = QComboBox()
        artifactType.addItems(["","traffic", "trafficThroughput", "clicks", "keypresses", "timed", "auditd"])
        self.artifactsTable.setCellWidget(current_row_pos, 0, artifactType)
        self.artifactsTable.setItem(current_row_pos, 1, QTableWidgetItem("artifact Description"))

        deleteButton = QPushButton('Delete')
        deleteButton.clicked.connect(self.deleteRow)
        self.artifactsTable.setCellWidget(current_row_pos, 2, deleteButton)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #set style
    style = """
        QPushButton{
            color: #ffffff;
            background: #8f8f8f;
            border: 3px #000000 solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: plain;
            font-size: 9pt;
            outline: none;
        }
        QPushButton:hover{
            border: 3px #000000 solid;
            background: #80aaff;
        }
    """
    app.setStyleSheet(style)
    #end style
    window = SalientArtifactWindow()
    window.show()
    sys.exit(app.exec())