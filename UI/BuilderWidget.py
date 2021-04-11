import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
import os
import json
import datetime
from src.ProjectController import ProjectController
from src import Event
from src.ScriptGenerator import ScriptGenerator
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
        self.move_node_button.clicked.connect(self.moveNode)
        self.move_node_button.setEnabled(False)

        self.move_tree_button = QPushButton('>>', self)
        self.verticalCenterLayout.addWidget(self.move_tree_button)
        self.move_tree_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.move_tree_button.clicked.connect(self.copyAllRelationships)
        self.move_tree_button.setEnabled(False)

        self.properties_button = QPushButton('Node Properties', self)
        self.verticalCenterLayout.addWidget(self.properties_button)
        self.properties_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.properties_button.clicked.connect(self.openProperties)
        self.properties_button.setEnabled(False)

        self.new_node_button = QPushButton('New Node >', self)
        self.verticalCenterLayout.addWidget(self.new_node_button)
        self.new_node_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.new_node_button.clicked.connect(self.newDependencyNode)
        self.new_node_button.setEnabled(False)

        self.verticalCenterLayout.setAlignment(Qt.AlignCenter)

        self.listdependencies = ABSDependencyTreeWidget()
        self.gridLayout.addWidget(self.listdependencies, 2, 2, 1, 2)

        self.edit_artifacts_button = QPushButton('Edit Salient Artifacts', self)
        self.gridLayout.addWidget(self.edit_artifacts_button, 3, 0)
        #self.edit_artifacts_button.setFixedSize(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.edit_artifacts_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.edit_artifacts_button.clicked.connect(self.openArtifacts)
        self.edit_artifacts_button.setEnabled(False)

        # Generate script button
        self.generate_script_button = QPushButton('Generate Script', self)
        self.gridLayout.addWidget(self.generate_script_button, 3, 1)
        self.generate_script_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.generate_script_button.clicked.connect(self.generate_script)
        self.generate_script_button.setEnabled(False)

        # Load Dependencies Button
        self.load_button = QPushButton('Load Project', self)
        self.gridLayout.addWidget(self.load_button, 3, 2)
        self.load_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.load_button.setStyleSheet("background-color: lightblue")
        self.load_button.clicked.connect(self.load_script)
        self.load_button.setEnabled(False)

        # Save Button
        self.save_button = QPushButton('Save Project', self)
        self.gridLayout.addWidget(self.save_button, 3, 3)
        self.save_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
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
            self.properties_button.setEnabled(True)
            self.generate_script_button.setEnabled(True)
            self.new_node_button.setEnabled(True)
            self.move_node_button.setEnabled(True)
            self.load_button.setEnabled(True)
            if ProjectController.get_dependencies_file() != "":
                self.loadDependencies()

    def populateTrees(self):
        eventGroups = ProjectController.load_event_list()
        for group in eventGroups:
            parent = group[0]
            eventType = ""
            if "keypresses_id" in parent.keys():
                eventType = "keypresses_id"
            if "clicks_id" in parent.keys():
                eventType = "clicks_id"
            if "audit_id" in parent.keys():
                eventType = "audit_id"
            if "timed_id" in parent.keys():
                eventType = "timed_id"
            if "traffic_all_id" in parent.keys():
                eventType = "traffic_all_id"
            if "traffic_xy_id" in parent.keys():
                eventType = "traffic_xy_id"
            if "suricata_id" in parent.keys():
                eventType = "suricata_id"

            content = ""
            if "content" in parent.keys():
                content = parent['content']
            newNode = self.listrelationships.addNode(
                eventType, 
                parent['start'], 
                content,
                self.listrelationships)
            self.populateBranch(group[1:], newNode)

    def copyAllRelationships(self):
        for index in range(self.listrelationships.topLevelItemCount()):
            item = self.listrelationships.topLevelItem(index)
            item_index = self.listrelationships.indexFromItem(item)
            deltaTime = self.calcDeltaTime(node=item, index=item_index)
            newItem = self.listdependencies.addNode(item.text(0), deltaTime.__str__(), item.text(2), self.listdependencies, True)
            for childIndex in range(item.childCount()):
                child = item.child(childIndex)
                child_index_obj = self.listrelationships.indexFromItem(child)
                deltaTime = self.calcDeltaTime(node=child, index=child_index_obj)
                self.listdependencies.addNode(child.text(0), deltaTime.__str__(), child.text(2), newItem, True)

    def loadDependencies(self):
        with open(ProjectController.get_dependencies_file()) as f:
            data = json.load(f)
            for node in data:
                tempQtreewidgetitem = QTreeWidgetItem(self.listdependencies)
                tempQtreewidgetitem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
                tempQtreewidgetitem.setText(4,node['Content'])
                tempQtreewidgetitem.setText(3,node['Attributes'])
                tempQtreewidgetitem.setText(2,node['Time'])
                tempQtreewidgetitem.setText(1,node['Subtype'])
                tempQtreewidgetitem.setText(0,node['Type'])
                for child in node['Children']:
                    childItem = QTreeWidgetItem(tempQtreewidgetitem)
                    childItem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
                    childItem.setText(4,child['Content'])
                    childItem.setText(3,child['Attributes'])
                    childItem.setText(2,child['Time'])
                    childItem.setText(1,child['Subtype'])
                    childItem.setText(0,child['Type'])


    def newDependencyNode(self):
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            newItem = self.listdependencies.addNode("Type...", "00:00:00.00", "Content...", selectedItem, True)
        else:
            newItem = self.listdependencies.addNode("Type...", "00:00:00.00", "Content...", self.listdependencies, True)
    
    def moveNode(self):
        if len(self.listrelationships.selectedItems()) > 0:
            selectedItem = self.listrelationships.selectedItems()[0]
            selectedIndex = self.listrelationships.selectedIndexes()[0]
            deltaTime = self.calcDeltaTime(node=selectedItem, index=selectedIndex)
            if len(self.listdependencies.selectedItems()) > 0:
                newItem = self.listdependencies.addNode(selectedItem.text(0), deltaTime.__str__(), selectedItem.text(2), self.listrelationships.selectedItems()[0], True)
            else:
                newItem = self.listdependencies.addNode(selectedItem.text(0), deltaTime.__str__(), selectedItem.text(2), self.listdependencies, True)
            for childIndex in range(selectedItem.childCount()):
                child = selectedItem.child(childIndex)
                child_index_obj = self.listrelationships.indexFromItem(child)
                deltaTime = self.calcDeltaTime(node=child, index=child_index_obj)
                self.listdependencies.addNode(child.text(0), deltaTime.__str__(), child.text(2), newItem, True)
        else:
            QMessageBox.critical(self, "Project Error", "No node selected.")


    def calcDeltaTime(self, node=None, index=None):
        if node is None or index is None:
            return datetime.time(0,0,2)
        else: 
            deltaTime = datetime.time(0,0,2)
            if(index.row()>0):
                prevItem = self.listrelationships.itemAt(index.row()-1, index.column())
                prevTime = datetime.datetime.strptime(prevItem.text(1), "%Y-%m-%dT%H:%M:%S").time()
                deltaTime = datetime.datetime.strptime(node.text(1), "%Y-%m-%dT%H:%M:%S").time()
                if prevTime < deltaTime:
                    delatDateTime = datetime.datetime.combine(datetime.datetime.today(),deltaTime) - datetime.datetime.combine(datetime.datetime.today(),prevTime)
                    date = datetime.datetime.strptime("1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S") + delatDateTime
                    deltaTime = date.time()
            return deltaTime
    
    def populateBranch(self, children=None, parent=None):
        for child in children:
            eventType = ""
            if "keypresses_id" in child.keys():
                eventType = "keypresses_id"
            if "clicks_id" in child.keys():
                eventType = "clicks_id"
            if "audit_id" in child.keys():
                eventType = "audit_id"
            if "timed_id" in child.keys():
                eventType = "timed_id"
            if "traffic_all_id" in child.keys():
                eventType = "traffic_all_id"
            if "traffic_xy_id" in child.keys():
                eventType = "traffic_xy_id"
            if "suricata_id" in child.keys():
                eventType = "suricata_id"

            content = ""
            if "content" in child.keys():
                content = child['content']
            if eventType != "traffic_xy_id":
                newNode = self.listrelationships.addNode(
                    eventType, 
                    child['start'], 
                    content,
                    parent)
            
    def openArtifacts(self):
        if ProjectController.is_project_loaded():
            self.artifacts_window.populate_table()
            self.artifacts_window.show()
        else:
            QMessageBox.critical(self, "Project Error", "No project is currently loaded.")


    def openProperties(self):
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            print (selectedItem.text(0))
            if selectedItem.text(0) == "clicks_id":
                self.openClicks()
            elif selectedItem.text(0) == "keypresses_id":
                    self.openKeypresses()
            else:
                QMessageBox.critical(self, "Input Error", "Event does not have editable properties")

    def openClicks(self):
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            print (selectedItem.text(0))
            if selectedItem.text(0) == "clicks_id":
                self.clicks_window = ClickOptionsWidget(selectedItem)
                self.clicks_window.show()
            else:
                QMessageBox.critical(self, "Input Error", "Event is not a clicks_id type")

    def openKeypresses(self):
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            print (selectedItem.text(0))
            if selectedItem.text(0) == "keypresses_id":
                QMessageBox.critical(self, "Input Error", "Opened Keypresses")
            else:
                QMessageBox.critical(self, "Input Error", "Event is not a keypresses_id type")

    def save_script(self):
        if not self.script_file_path:
            new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this script as...", "", ".json")
            if new_file_path:
                self.script_file_path = new_file_path
            else:
                self.invalid_path_alert_message()
                return False 
        ProjectController.set_dependencies_file(self.script_file_path + '.json')
        ProjectController.save_project()
        self.create_dependencies_json(self.script_file_path + '.json')

    def load_script(self):
        script_file = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if script_file:
            self.script_file_path = script_file
        else:
            self.invalid_path_alert_message()
            return False 
        ProjectController.set_dependencies_file(self.script_file_path)
        ProjectController.save_project()
        self.loadDependencies()

    def generate_script(self):
        script_path, filter_type = QFileDialog.getOpenFileName(self, "Select script to generate...", "")
        if script_path:
            self.script_file_path = script_path
        else:
            self.invalid_path_alert_message()
            return False 
        try:
            ScriptGenerator(script_path)
            self.script_gen_success()
        except:
            self.invalid_path_alert_message()
        
    def script_gen_success(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Success")
        messageBox.setText("Script Generated")
        messageBox.exec()

    def invalid_path_alert_message(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Invalid file")
        messageBox.setText("Selected filename or path is not valid. Please select a valid file.")
        messageBox.exec()

    def enable_clicks_button(self):
        self.click_button.setEnabled(True)

    def create_dependencies_json(self, filename):
        dependencies_list = []
        for index in range(self.listdependencies.topLevelItemCount()):
            item = self.listdependencies.topLevelItem(index)
            dep_dict = {}
            dep_dict["Type"] = item.text(0)
            dep_dict["Subtype"] = item.text(1)
            dep_dict["Time"] = item.text(2)
            dep_dict["Attributes"] = item.text(3)
            dep_dict["Content"] = item.text(4)
            dep_dict["Children"] = []
            for childIndex in range(item.childCount()):
                child = item.child(childIndex)
                child_dict = {}
                child_dict["Type"] = child.text(0)
                child_dict["Subtype"] = child.text(1)
                child_dict["Time"] = child.text(2)
                child_dict["Attributes"] = child.text(3)
                child_dict["Content"] = child.text(4)
                dep_dict["Children"].append(child_dict)
            dependencies_list.append(dep_dict)

        with open(filename, 'w') as outfile:
            json.dump(dependencies_list, outfile, indent=2)


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
        self.sortByColumn(1, QtCore.Qt.AscendingOrder)
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
            tempQtreewidgetitem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            tempQtreewidgetitem.setText(4,content)
            tempQtreewidgetitem.setText(2,time)
            tempQtreewidgetitem.setText(0,_type)
            return tempQtreewidgetitem
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete and self.state() != QTreeWidget.EditingState:
            row = self.selectedItems().pop()
            self.takeTopLevelItem(self.indexOfTopLevelItem(row))
        else:
            super().keyPressEvent(event)

    def dragEnterEvent (self, eventQDragEnterEvent):
        sourceQCustomTreeWidget = eventQDragEnterEvent.source()
        if isinstance(sourceQCustomTreeWidget, ABSDependencyTreeWidget):
            if self != sourceQCustomTreeWidget:
                eventQDragEnterEvent.accept()
            else:
                QTreeWidget.dragEnterEvent(self, eventQDragEnterEvent)
        else:
            QTreeWidget.dragEnterEvent(self, eventQDragEnterEvent)

    def dropEvent(self, event):
        md = event.mimeData()
        fmt = "application/x-qabstractitemmodeldatalist"
        dropIndex = self.indexAt(event.pos())
        dropIndicator = QAbstractItemView.dropIndicatorPosition(self)

        if md.hasFormat(fmt):
            encoded = md.data(fmt)
            stream = QtCore.QDataStream(encoded, QtCore.QIODevice.ReadOnly)
            tree_items = []
            parent = self

            while not stream.atEnd():
                it = QtWidgets.QTreeWidgetItem()
                # row and column where it comes from
                for j in range(3): # 3 columns in the tree
                    row = stream.readInt32()
                    column = stream.readInt32()
                    map_items = stream.readInt32()

                    for i in range(map_items):
                        role = stream.readInt32()
                        value = QtCore.QVariant()
                        stream >> value
                        it.setData(column, role, value)
                tree_items.append(it)

            if (not dropIndex.parent().isValid() and dropIndex.row() != -1):
                if dropIndicator == QAbstractItemView.AboveItem:
                    # manage a boolean for the case when you are above an item
                    for it in tree_items:
                        parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
                    return
                elif dropIndicator == QAbstractItemView.BelowItem:
                    #something when being below an item
                    for it in tree_items:
                        parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
                    return
                elif dropIndicator == QAbstractItemView.OnItem:
                    #you're on an item, maybe add the current one as a child
                    parent = self.itemAt(dropIndex.row(), dropIndex.column())
                    for it in tree_items:
                        self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
                    return
                elif dropIndicator == QAbstractItemView.OnViewport:
                    #you are not on your tree
                    return
            
            for it in tree_items:
                        parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())
