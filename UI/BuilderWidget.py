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
from UI.ArtifactsTableWidget import SalientArtifactWindow
from UI.ClickOptionsWidget import ClickOptionsWidget

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
        self.gridLayout.addWidget(self.label, 0, 0)
        
        self.horizontalTopLeftLayoutWidget = QWidget(self)
        self.horizontalTopLeftLayoutWidget.setObjectName(u"horizontalTopLeftLayoutWidget")
        self.horizontalTopLeftLayout = QHBoxLayout(self.horizontalTopLeftLayoutWidget)
        self.horizontalTopLeftLayout.setObjectName(u"horizontalTopLayout")
        self.gridLayout.addWidget(self.horizontalTopLeftLayoutWidget, 1, 0)

        self.search_relationships_lineedit = QLineEdit(self)
        self.horizontalTopLeftLayout.addWidget(self.search_relationships_lineedit, 0)
        self.relationship_search_button = QPushButton('Search', self)
        self.horizontalTopLeftLayout.addWidget(self.relationship_search_button, 1)
        self.relationship_search_button.setEnabled(False)
        
        self.horizontalTopRightLayoutWidget = QWidget(self)
        self.horizontalTopRightLayoutWidget.setObjectName(u"horizontalTopRightLayoutWidget")
        self.horizontalTopRightLayout = QHBoxLayout(self.horizontalTopRightLayoutWidget)
        self.horizontalTopRightLayout.setObjectName(u"horizontalTopRightLayout")
        self.gridLayout.addWidget(self.horizontalTopRightLayoutWidget, 1, 3)

        self.search_dependency_lineedit = QLineEdit(self)
        self.horizontalTopRightLayout.addWidget(self.search_dependency_lineedit, 0)
        self.dependency_search_button = QPushButton('Search', self)
        self.horizontalTopRightLayout.addWidget(self.dependency_search_button, 1)
        self.dependency_search_button.setEnabled(False)


        self.listrelationships = ABSRelationshipTreeWidget()
        self.gridLayout.addWidget(self.listrelationships, 2, 0)

        self.verticalCenterLayoutWidget = QWidget(self)
        self.verticalCenterLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalCenterLayout = QVBoxLayout(self.verticalCenterLayoutWidget)
        self.verticalCenterLayout.setObjectName(u"verticalLayout")
        self.gridLayout.addWidget(self.verticalCenterLayoutWidget, 2, 1)

        self.move_node_button = QPushButton('>', self)
        self.verticalCenterLayout.addWidget(self.move_node_button)
        self.move_node_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        #self.move_node_button.clicked.connect(self.openArtifacts)
        self.move_node_button.setEnabled(False)

        self.move_tree_button = QPushButton('>>', self)
        self.verticalCenterLayout.addWidget(self.move_tree_button)
        self.move_tree_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        #self.move_tree_button.clicked.connect(self.openArtifacts)
        self.move_tree_button.setEnabled(False)

        self.click_button = QPushButton('Click Settings', self)
        self.verticalCenterLayout.addWidget(self.click_button)
        self.click_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.click_button.clicked.connect(self.openClicks)
        self.click_button.setEnabled(False)

        self.keypress_button = QPushButton('Keypress Settings', self)
        self.verticalCenterLayout.addWidget(self.keypress_button)
        self.keypress_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        #self.move_tree_button.clicked.connect(self.openArtifacts)
        self.keypress_button.setEnabled(False)

        self.verticalCenterLayout.setAlignment(Qt.AlignCenter)

        self.listdependencies = ABSDependencyTreeWidget()
        self.gridLayout.addWidget(self.listdependencies, 2, 2, 1, 2)

        self.edit_artifacts_button = QPushButton('Edit Salient Artifacts', self)
        self.gridLayout.addWidget(self.edit_artifacts_button, 3, 0)
        #self.edit_artifacts_button.setFixedSize(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.edit_artifacts_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.edit_artifacts_button.clicked.connect(self.openArtifacts)
        self.edit_artifacts_button.setEnabled(False)


        # Save Button
        self.save_button = QPushButton('Save Project', self)
        self.gridLayout.addWidget(self.save_button, 3, 3)
        self.save_button.setStyleSheet("background-color: lightblue")
        self.save_button.clicked.connect(self.save_script)
        self.save_button.setEnabled(False)

        # Loads events when project is loaded
        if ProjectController.is_project_loaded():
            self.populateTrees()
            self.save_button.setEnabled(True)
            self.edit_artifacts_button.setEnabled(True)
            self.relationship_search_button.setEnabled(True)
            self.dependency_search_button.setEnabled(True)
            self.move_tree_button.setEnabled(True)
            self.click_button.setEnabled(True)

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

    def openClicks(self):
        selectedRow = self.listdependencies.selectionModel().selectedRows(0)[0]
        selectedItem = self.listdependencies.itemAt(selectedRow.row(), selectedRow.column())
        print (selectedItem.text(0))
        if selectedItem.text(0) == "clicks_id":
            self.clicks_window = ClickOptionsWidget(selectedItem.text(2))
            self.clicks_window.show()
        else:
            QMessageBox.critical(self, "Input Error", "Event is not a clicks_id type")

    def save_script(self):
        if not self.script_file_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this script as...", "", "All files(*)")
            if new_file_path:
                self.script_file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False 
        #TODO: Write file into path (need to figure out file format)

    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()

    def enable_clicks_button(self):
        self.click_button.setEnabled(True)
    
    # def dependency_event_selection_changed(selectedItems, deselectedItems):
    #     if selectedItems[0][0] == "clicks_id":
    #         self.enable_clicks_button(True)

class ABSRelationshipTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(2,"Content")
        ___qtreewidgetitem.setText(1,"Time")
        ___qtreewidgetitem.setText(0,"Type")
        self.setAcceptDrops(True)
        self.setTabKeyNavigation(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.setSortingEnabled(True)

    def addNode(self, _type=None, time=None, content=None, parent=None, canEdit=False):
        if(parent is not None):
            tempQtreewidgetitem = QTreeWidgetItem(parent)
            if canEdit:
                tempQtreewidgetitem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            else:
                tempQtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            tempQtreewidgetitem.setText(2,content)
            tempQtreewidgetitem.setText(1,time)
            tempQtreewidgetitem.setText(0,_type)
            return tempQtreewidgetitem
    
    # def dropEvent(self, event):
    #     md = event.mimeData()
    #     fmt = "application/x-qabstractitemmodeldatalist"
    #     dropIndex = self.indexAt(event.pos())
    #     dropIndicator = QAbstractItemView.dropIndicatorPosition(self)

    #     if md.hasFormat(fmt):
    #         encoded = md.data(fmt)
    #         stream = QtCore.QDataStream(encoded, QtCore.QIODevice.ReadOnly)
    #         tree_items = []
    #         parent = self

    #         while not stream.atEnd():
    #             it = QtWidgets.QTreeWidgetItem()
    #             # row and column where it comes from
    #             for j in range(3): # 3 columns in the tree
    #                 row = stream.readInt32()
    #                 column = stream.readInt32()
    #                 map_items = stream.readInt32()

    #                 for i in range(map_items):
    #                     role = stream.readInt32()
    #                     value = QtCore.QVariant()
    #                     stream >> value
    #                     it.setData(column, role, value)
    #             tree_items.append(it)

    #         if (not dropIndex.parent().isValid() and dropIndex.row() != -1):
    #             if dropIndicator == QAbstractItemView.AboveItem:
    #                 # manage a boolean for the case when you are above an item
    #                 for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(1), it.text(2), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.BelowItem:
    #                 #something when being below an item
    #                 for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(1), it.text(2), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.OnItem:
    #                 #you're on an item, maybe add the current one as a child
    #                 parent = self.itemAt(dropIndex.row(), dropIndex.column())
    #                 for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(1), it.text(2), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.OnViewport:
    #                 #you are not on your tree
    #                 return
            
    #         for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(1), it.text(2), parent, True)

class ABSDependencyTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(4,"Match Content")
        ___qtreewidgetitem.setText(3,"Custom Attributes")
        ___qtreewidgetitem.setText(2,"Time")
        ___qtreewidgetitem.setText(1,"Event Subtype")
        ___qtreewidgetitem.setText(0,"Event Type")
        self.setAcceptDrops(True)
        self.setTabKeyNavigation(True)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.setSortingEnabled(True)

    def addNode(self, _type=None, time=None, content=None, parent=None, canEdit=False):
        if(parent is not None):
            tempQtreewidgetitem = QTreeWidgetItem(parent)
            if canEdit:
                tempQtreewidgetitem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            else:
                tempQtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            tempQtreewidgetitem.setText(4,content)
            tempQtreewidgetitem.setText(2,time)
            tempQtreewidgetitem.setText(0,_type)
            return tempQtreewidgetitem

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())
