import sys
from PyQt5 import QtCore, QtGui, QtWidgets
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
        self.setLayout(self.gridLayout)

        #Create search bar
        self.label = QLabel('Builder', self)
        self.label.setObjectName(u"label")
        self.label.setFont(QFont('MS Shell Dlg 2', 12))
        self.gridLayout.addWidget(self.label, 0, 1)

        self.search_button = QPushButton('Search', self)
        self.gridLayout.addWidget(self.search_button, 1,2,1,1)

        self.lineEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.lineEdit, 1,1,1,1)

        self.listrelationships = QTreeWidget()
        __qtreewidgetitem = QTreeWidgetItem(self.listrelationships)
        __qtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        __qtreewidgetitem1 = QTreeWidgetItem(self.listrelationships)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        __qtreewidgetitem2 = QTreeWidgetItem(self.listrelationships)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem2.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.listrelationships.setObjectName(u"treeWidget")
        ___qtreewidgetitem = self.listrelationships.headerItem()
        ___qtreewidgetitem.setText(2,"Content")
        ___qtreewidgetitem.setText(1,"Time")
        ___qtreewidgetitem.setText(0,"Type")

        __sortingEnabled = self.listrelationships.isSortingEnabled()
        self.listrelationships.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.listrelationships.topLevelItem(0)
        QTreeWidgetItem(___qtreewidgetitem1)
        ___qtreewidgetitem1.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        ___qtreewidgetitem1.setText(2,"Some text")
        ___qtreewidgetitem1.setText(1,"48498984")
        ___qtreewidgetitem1.setText(0,"keypresses")
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        QTreeWidgetItem(___qtreewidgetitem2)
        ___qtreewidgetitem2.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        ___qtreewidgetitem2.setText(2,"ping")
        ___qtreewidgetitem2.setText(1,"9494984856")
        ___qtreewidgetitem2.setText(0,"traffic")
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        QTreeWidgetItem(___qtreewidgetitem3)
        ___qtreewidgetitem3.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        ___qtreewidgetitem3.setText(2,"reply")
        ___qtreewidgetitem3.setText(1,"8978949495954")
        ___qtreewidgetitem3.setText(0,"traffic")
        ___qtreewidgetitem4 = self.listrelationships.topLevelItem(1)
        QTreeWidgetItem(___qtreewidgetitem4)
        ___qtreewidgetitem4.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        ___qtreewidgetitem4.setText(2,"Some info")
        ___qtreewidgetitem4.setText(1,"15151521")
        ___qtreewidgetitem4.setText(0,"Click")
        ___qtreewidgetitem5 = ___qtreewidgetitem4.child(0)
        QTreeWidgetItem(___qtreewidgetitem5)
        ___qtreewidgetitem5.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        ___qtreewidgetitem5.setText(2,"sopodvsopnv p idp j sdpjdspovj sdpovjpsdm")
        ___qtreewidgetitem5.setText(1,"515161")
        ___qtreewidgetitem5.setText(0,"traffic")
        self.listrelationships.setSortingEnabled(__sortingEnabled)
        self.listrelationships.setAcceptDrops(True)
        self.listrelationships.setTabKeyNavigation(True)
        self.listrelationships.setDragEnabled(True)
        self.listrelationships.setDragDropOverwriteMode(False)
        self.listrelationships.setDragDropMode(QAbstractItemView.DragDrop)
        self.listrelationships.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listrelationships.setSortingEnabled(True)
        self.listrelationships.setWordWrap(True)
        self.gridLayout.addWidget(self.listrelationships, 2, 1)

        self.listdependencies = QTreeWidget()
        __qtreewidgetitemt = QTreeWidgetItem(self.listdependencies)
        self.listdependencies.setObjectName(u"treeWidget")
        ___qtreewidgetitemt = self.listdependencies.headerItem()
        ___qtreewidgetitemt.setText(2,"Content")
        ___qtreewidgetitemt.setText(1,"Time")
        ___qtreewidgetitemt.setText(0,"Type")
        self.listdependencies.setSortingEnabled(True)
        self.listdependencies.setAcceptDrops(True)
        self.listdependencies.setTabKeyNavigation(True)
        self.listdependencies.setDragEnabled(True)
        self.listdependencies.setDragDropOverwriteMode(False)
        self.listdependencies.setDragDropMode(QAbstractItemView.DragDrop)
        self.listdependencies.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listdependencies.setSortingEnabled(True)
        self.listdependencies.setWordWrap(True)
        self.gridLayout.addWidget(self.listdependencies, 2, 2)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())