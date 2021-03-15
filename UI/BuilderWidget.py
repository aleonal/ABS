import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
import os
import json
from src.ProjectController import ProjectController
from src import Event
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
        self.setLayout(self.gridLayout)
        self.setWindowIcon(QtGui.QIcon("A.png"))# A icons

        #Create search bar
        self.label = QLabel('Builder', self)
        self.label.setObjectName(u"label")
        self.label.setFont(QFont('MS Shell Dlg 2', 12))
        self.gridLayout.addWidget(self.label, 0, 1)

        self.search_button = QPushButton('Search', self)
        self.gridLayout.addWidget(self.search_button, 1,2,1,1)

        self.lineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.lineEdit, 1,1,1,1)

        self.listrelationships = ABSEventTreeWidget()
        self.gridLayout.addWidget(self.listrelationships, 2, 1)

        self.listdependencies = ABSEventTreeWidget()
        self.gridLayout.addWidget(self.listdependencies, 2, 2)

        self.populateTrees()

        self.edit_artifacts_button = QPushButton('Edit Salient Artifacts', self)
        self.gridLayout.addWidget(self.edit_artifacts_button, 1, 0)
        self.edit_artifacts_button.clicked.connect(self.openArtifacts)

        '''
        # Save Button
        self.save_button = QPushButton('Save Project', self)
        self.gridLayout.addWidget(self.save_button, 3, 2)
        self.save_button.clicked.connect(self.save_script)
        '''

        # Setup Menu Bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0,0,482,21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuEdit.setTitle("Edit")
        self.gridLayout.addWidget(self.menubar, 0,0)

        # Setup Menu Actions
        self.actionOpen_Script = QtWidgets.QAction(self, triggered=self.open_script)
        self.actionOpen_Script.setObjectName("actionOpen_Script")
        self.actionOpen_Script.setText("Open Script")
        self.menuFile.addAction(self.actionOpen_Script)
        self.actionSave_Script = QtWidgets.QAction(self)
        self.actionSave_Script.setObjectName("actionSave_Script")
        self.actionSave_Script.setText("Save Script")
        self.menuFile.addAction(self.actionSave_Script)
        self.actionSave_Script_As = QtWidgets.QAction(self, triggered=self.save_script)
        self.actionSave_Script_As.setObjectName("actionSave_Script_As")
        self.actionSave_Script_As.setText("Save Script As")
        self.menuFile.addAction(self.actionSave_Script_As)
        self.actionUndo = QtWidgets.QAction(self)
        self.actionUndo.setObjectName("actionUndo")
        self.actionUndo.setText("Undo") 
        self.menuEdit.addAction(self.actionUndo)
        self.actionRedo = QtWidgets.QAction(self)
        self.actionRedo.setObjectName("actionRedo")
        self.actionRedo.setText("Redo") 
        self.menuEdit.addAction(self.actionRedo)
        self.actionCopy = QtWidgets.QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCopy.setText("Copy") 
        self.menuEdit.addAction(self.actionCopy)
        self.actionPaste = QtWidgets.QAction(self)
        self.actionPaste.setObjectName("actionPaste")
        self.actionPaste.setText("Paste") 
        self.menuEdit.addAction(self.actionPaste)
        self.actionCut = QtWidgets.QAction(self)
        self.actionCut.setObjectName("actionCut")
        self.actionCut.setText("Cut") 
        self.menuEdit.addAction(self.actionCut)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

    def populateTrees(self):
        eventGroups = ProjectController.load_event_list()
        for group in eventGroups:
            parent = group[0]
            eventType = ""
            if "keypresses_id" in parent.keys():
                eventType = "keypresses_id"
            if "clicks_id" in parent.keys():
                eventType = "clicks_id"
            newNode = self.listrelationships.addNode(
                eventType, 
                parent['start'], 
                parent['content'],
                self.listrelationships)
            self.populateBranch(group[1:], newNode)
    
    def populateBranch(self, children=None, parent=None):
        if children == None or len(children) == 0:
            return
        else:
            eventType = ""
            if "keypresses_id" in children[0].keys():
                eventType = "keypresses_id"
            if "clicks_id" in children[0].keys():
                eventType = "clicks_id"
            if "audit_id" in children[0].keys():
                eventType = "audit_id"
            if "timed_id" in children[0].keys():
                eventType = "timed_id"
            if "traffic_all_id" in children[0].keys():
                eventType = "traffic_all_id"
            if "traffic_xy_id" in children[0].keys():
                eventType = "traffic_xy_id"
            if "suricata_id" in children[0].keys():
                eventType = "suricata_id"
            newNode = self.listrelationships.addNode(
                eventType, 
                children[0]['start'], 
                children[0]['content'],
                parent)
            self.populateBranch(children[1:], newNode)
            



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
    
    def open_script(self):
        if not self.script_file_path:
            new_file_path, filter_type = QFileDialog.getOpenFileName(self, "Save this script as...", "", "All files(*)")
            if new_file_path:
                self.script_file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False 
        #TODO: What to do with file (read it and write it in appropriate place)

    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()

class ABSEventTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(2,"Content")
        ___qtreewidgetitem.setText(1,"Time")
        ___qtreewidgetitem.setText(0,"Type")
        self.setAcceptDrops(True)
        self.setTabKeyNavigation(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(True)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.setSortingEnabled(False)

    def addNode(self, _type=None, time=None, content=None, parent=None, canEdit=False):
        tempQtreewidgetitem = QTreeWidgetItem(parent)
        #if canEdit:
        tempQtreewidgetitem.setFlags(Qt.ItemIsEditable)
        tempQtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        tempQtreewidgetitem.setText(2,content)
        tempQtreewidgetitem.setText(1,time)
        tempQtreewidgetitem.setText(0,_type)
        return tempQtreewidgetitem

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())