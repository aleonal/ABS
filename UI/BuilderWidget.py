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
from src.ScriptGen2 import ScriptGen2
from UI.ArtifactsTableWidget import SalientArtifactWindow

from UI.ClickSettings import ClickSettings
from UI.DependencyOptionsWidget import DependencyOptionsWidget


class BuilderWidget(QWidget):

    def __init__(self, project=None):
        super().__init__()
        self.setGeometry(50, 50, 482, 432)
        self.setWindowTitle("Builder")
        self.UI()
        self.artifacts_window = SalientArtifactWindow(previous_window=self)
        self.show()
        #self.script_file_path = None

    def UI(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.setLayout(self.gridLayout)
        self.setWindowIcon(QtGui.QIcon("A.png"))# A icons

        self.search_relationship_query = ""
        self.search_dependencies_query = ""

        self.search_dependencies_index = 0
        self.search_relationships_index = 0

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
        self.search_relationships_lineedit.textChanged.connect(self.relationshipQueryChanged)
        self.horizontalTopLeftLayout.addWidget(self.search_relationships_lineedit, 0)
        self.relationship_search_button = QPushButton('Search', self)
        self.horizontalTopLeftLayout.addWidget(self.relationship_search_button, 1)
        self.relationship_search_button.clicked.connect(self.searchRelationships)
        self.relationship_search_button.setEnabled(False)
        
        self.horizontalTopRightLayoutWidget = QWidget(self)
        self.horizontalTopRightLayoutWidget.setObjectName(u"horizontalTopRightLayoutWidget")
        self.horizontalTopRightLayout = QHBoxLayout(self.horizontalTopRightLayoutWidget)
        self.horizontalTopRightLayout.setObjectName(u"horizontalTopRightLayout")
        self.gridLayout.addWidget(self.horizontalTopRightLayoutWidget, 1, 3)

        self.search_dependency_lineedit = QLineEdit(self)
        self.search_dependency_lineedit.textChanged.connect(self.dependencyQueryChanged)
        self.horizontalTopRightLayout.addWidget(self.search_dependency_lineedit, 0)
        self.dependency_search_button = QPushButton('Search', self)
        self.dependency_search_button.clicked.connect(self.searchDependency)
        self.horizontalTopRightLayout.addWidget(self.dependency_search_button, 1)
        self.dependency_search_button.setEnabled(False)


        self.listrelationships = ABSRelationshipTreeWidget()
        self.gridLayout.addWidget(self.listrelationships, 2, 0)

        self.verticalCenterLayoutWidget = QWidget(self)
        self.verticalCenterLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalCenterLayout = QVBoxLayout(self.verticalCenterLayoutWidget)
        self.verticalCenterLayout.setObjectName(u"verticalLayout")
        self.gridLayout.addWidget(self.verticalCenterLayoutWidget, 2, 1)

        self.move_node_button = QPushButton('Move Node', self)
        self.verticalCenterLayout.addWidget(self.move_node_button)
        self.move_node_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.move_node_button.clicked.connect(self.moveNode)
        self.move_node_button.setEnabled(False)

        self.move_branch_button = QPushButton('Move Branch', self)
        self.verticalCenterLayout.addWidget(self.move_branch_button)
        self.move_branch_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.move_branch_button.clicked.connect(self.moveBranch)
        self.move_branch_button.setEnabled(False)

        self.move_tree_button = QPushButton('Move Tree', self)
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
        '''
        # View Relationship Info Button
        self.relationship_details_button = QPushButton('< Relationship Details', self)
        #self.verticalCenterLayout.addWidget(self.relationship_details_button)
        #self.relationship_details_button.setFixedSize(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.relationship_details_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.relationship_details_button.clicked.connect(self.openRelationship)
        self.relationship_details_button.setEnabled(False)
        '''
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
        self.load_button = QPushButton('Load Script', self)
        self.gridLayout.addWidget(self.load_button, 3, 2)
        self.load_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        self.load_button.setStyleSheet("background-color: lightblue")
        self.load_button.clicked.connect(self.load_script)
        self.load_button.setEnabled(False)

        # Save Button
        self.save_button = QPushButton('Save Script', self)
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
            self.move_branch_button.setEnabled(True)
            #self.relationship_details_button.setEnabled(True)
            if ProjectController.get_dependencies_file() != "":
                try:
                    self.loadDependencies()
                except:
                    pass

    def populateTrees(self):
        eventGroups = ProjectController.load_event_list()
        artifactList = ProjectController.get_salient_artifacts_json()
        keypressArtifacts = [i['artifact'] for i in artifactList if 'keypresses' in i['type']]
        clicksArtifacts = [i['artifact'] for i in artifactList if 'clicks' in i['type']]
        auditArtifacts = [i['artifact'] for i in artifactList if 'auditd' in i['type']]
        timedArtifacts = [i['artifact'] for i in artifactList if 'timed' in i['type']]
        trafficArtifacts = [i['artifact'] for i in artifactList if 'traffic' in i['type']]
        trafficThroughputArtifacts = [i['artifact'] for i in artifactList if 'trafficThroughput' in i['type']]


        for group in eventGroups:
            if len(group) < 1:
                continue
            parent = group[0]
            eventType = ""
            salientArtifactFlag=False
            if "keypresses_id" in parent.keys():
                eventType = "keypresses_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in keypressArtifacts):
                        salientArtifactFlag=True
        
            if "clicks_id" in parent.keys():
                eventType = "clicks_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in clicksArtifacts):
                        salientArtifactFlag=True

            if "auditd_id" in parent.keys():
                eventType = "audit_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in auditArtifacts):
                        salientArtifactFlag=True

            if "timed_id" in parent.keys():
                eventType = "timed_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in timedArtifacts):
                        salientArtifactFlag=True

            if "traffic_all_id" in parent.keys():
                eventType = "traffic_all_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in trafficArtifacts):
                        salientArtifactFlag=True
            if "traffic_xy_id" in parent.keys():
                eventType = "traffic_xy_id"
                if "content" in parent.keys():
                    if any(s in parent['content'] for s in trafficThroughputArtifacts):
                        salientArtifactFlag=True
            if "suricata_id" in parent.keys():
                eventType = "suricata_id"

            content = ""
            if "content" in parent.keys():
                content = parent['content']
            newNode = self.listrelationships.addNode(
                eventType, 
                parent['start'], 
                content,
                self.listrelationships, isSalientArtifact = salientArtifactFlag)
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
        self.listdependencies.clear()
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
        newItem = None
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            newItem = self.listdependencies.addNode("Type...", "00:00:00.00", "Content...", selectedItem, True)
        else:
            newItem = self.listdependencies.addNode("Type...", "00:00:00.00", "Content...", self.listdependencies, True)
        self.properties_window = DependencyOptionsWidget(newItem)
        self.properties_window.show()
    
    def moveBranch(self):
        if len(self.listrelationships.selectedItems()) > 0:
            selectedItem = self.listrelationships.selectedItems()[0]
            selectedIndex = self.listrelationships.indexFromItem(selectedItem)
            deltaTime = self.calcDeltaTime(node=selectedItem, index=selectedIndex)
            parent = self.listdependencies
            if len(self.listdependencies.selectedItems()) > 0:
                parent = self.listdependencies.selectedItems()[0]
                if parent.parent():
                    parent = parent.parent()

            newItem = self.listdependencies.addNode(selectedItem.text(0), deltaTime.__str__(), selectedItem.text(2), parent, True)
            if newItem.parent() is None:
                    parent = newItem
            for childIndex in range(selectedItem.childCount()):
                child = selectedItem.child(childIndex)
                child_index_obj = self.listrelationships.indexFromItem(child)
                deltaTime = self.calcDeltaTime(node=child, index=child_index_obj)
                self.listdependencies.addNode(child.text(0), deltaTime.__str__(), child.text(2), parent, True)
        else:
            QMessageBox.critical(self, "Project Error", "No node selected.")

    def moveNode(self):
        if len(self.listrelationships.selectedItems()) > 0:
            selectedItem = self.listrelationships.selectedItems()[0]
            selectedIndex = self.listrelationships.indexFromItem(selectedItem)
            deltaTime = self.calcDeltaTime(node=selectedItem, index=selectedIndex)
            parent = self.listdependencies
            if len(self.listdependencies.selectedItems()) > 0:
                parent = self.listdependencies.selectedItems()[0]
                if parent.parent():
                    parent = parent.parent()

            newItem = self.listdependencies.addNode(selectedItem.text(0), deltaTime.__str__(), selectedItem.text(2), parent, True)
        else:
            QMessageBox.critical(self, "Project Error", "No node selected.")

    def calcDeltaTime(self, node=None, index=None):
        if node is None or index is None:
            return datetime.time(0,0,1)
        else: 
            deltaTime = datetime.time(0,0,1)
            prevIndex = self.listrelationships.indexAbove(index)
            prevItem = self.listrelationships.itemAbove(node)
            if prevItem is not None:
                try:
                    prevTime = ProjectController.parse_timestamp(prevItem.text(1)).time()
                except:
                    return datetime.time(0,0,1)
            else:
                return datetime.time(0,0,1)
            try:
                deltaTime = ProjectController.parse_timestamp(node.text(1)).time()
            except:
                return datetime.time(0,0,1)
            if prevTime < deltaTime:
                delatDateTime = datetime.datetime.combine(datetime.datetime.today(),deltaTime) - datetime.datetime.combine(datetime.datetime.today(),prevTime)
                date = datetime.datetime.strptime("1900-01-01T00:00:00.000", "%Y-%m-%dT%H:%M:%S.%f") + delatDateTime
                deltaTime = date.time()
            return deltaTime

    def searchRelationships(self):
        query = self.search_relationships_lineedit.text()
        print("Searching relationship: " + query)
        results = self.listrelationships.findItems(query, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 2)
        if(query == self.search_relationship_query):
            self.search_relationships_index = self.search_relationships_index + 1 
            if self.search_relationships_index >= len(results):
                self.search_relationships_index = 0
        else:
            self.search_relationship_query = query
        print("Searching results lenght: " + len(results).__str__())
        if len(results) > 0:
            print(results[self.search_relationships_index].text(2))
            self.listrelationships.setCurrentItem(results[self.search_relationships_index])
            self.listrelationships.scrollTo(self.listrelationships.indexFromItem(results[self.search_relationships_index]))

    def searchDependency(self):
        query = self.search_dependency_lineedit.text()
        print("Searching dependencies: " + query)
        results = self.listdependencies.findItems(query, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 4)
        if(query == self.search_dependencies_query):
            self.search_dependencies_index = self.search_dependencies_index + 1 
            if self.search_dependencies_index >= len(results):
                self.search_dependencies_index = 0
        else:
            self.search_dependencies_query = query
        print("Searching dependencies results lenght: " + len(results).__str__())
        if len(results) > 0:
            print(results[self.search_dependencies_index].text(2))
            self.listdependencies.setCurrentItem(results[self.search_dependencies_index])
            self.listdependencies.scrollTo(self.listdependencies.indexFromItem(results[self.search_dependencies_index]))
    
    def populateBranch(self, children=None, parent=None):
        artifactList = ProjectController.get_salient_artifacts_json()
        keypressArtifacts = [i['artifact'] for i in artifactList if 'keypresses' in i['type']]
        clicksArtifacts = [i['artifact'] for i in artifactList if 'clicks' in i['type']]
        auditArtifacts = [i['artifact'] for i in artifactList if 'auditd' in i['type']]
        timedArtifacts = [i['artifact'] for i in artifactList if 'timed' in i['type']]
        trafficArtifacts = [i['artifact'] for i in artifactList if 'traffic' in i['type']]
        trafficThroughputArtifacts = [i['artifact'] for i in artifactList if 'trafficThroughput' in i['type']]
        
        for child in children:
            salientArtifactFlag=False
            eventType = ""
            if "keypresses_id" in child.keys():
                eventType = "keypresses_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in keypressArtifacts):
                        salientArtifactFlag=True
            if "clicks_id" in child.keys():
                eventType = "clicks_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in clicksArtifacts):
                        salientArtifactFlag=True
            if "auditd_id" in child.keys():
                eventType = "audit_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in auditArtifacts):
                        salientArtifactFlag=True
            if "timed_id" in child.keys():
                eventType = "timed_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in timedArtifacts):
                        salientArtifactFlag=True
            if "traffic_all_id" in child.keys():
                eventType = "traffic_all_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in trafficArtifacts):
                        salientArtifactFlag=True
            if "traffic_xy_id" in child.keys():
                eventType = "traffic_xy_id"
                if "content" in child.keys():
                    if any(s in child['content'] for s in trafficThroughputArtifacts):
                        salientArtifactFlag=True

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
                    parent, isSalientArtifact=salientArtifactFlag)
            
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
            if selectedItem.text(0) == "clicks_id" or selectedItem.text(0) == "timed_id":
                self.openClicks()
            else:
                self.properties_window = DependencyOptionsWidget(selectedItem)
                self.properties_window.show()

    def openRelationship(self):
        if len(self.listrelationships.selectedItems()) > 0:
            selectedItem = self.listrelationships.selectedItems()[0]
            print (selectedItem.text(0))
            if selectedItem.text(0) == "clicks_id" or selectedItem.text(0) == "timed_id":
                self.openClicks()
            else:
                self.properties_window = DependencyOptionsWidget(selectedItem)
                self.properties_window.show()

    def openClicks(self):
        if len(self.listdependencies.selectedItems()) > 0:
            selectedItem = self.listdependencies.selectedItems()[0]
            print (selectedItem.text(0))
            if selectedItem.text(0) == "clicks_id" or selectedItem.text(0) == "timed_id":
                self.clicks_window = ClickSettings(selectedItem)
                self.clicks_window.show()
            else:
                QMessageBox.critical(self, "Input Error", "Event is not a clicks_id type")

    def save_script(self):
        #if not self.script_file_path:
        new_file_path, filter_type = QFileDialog.getSaveFileName(self, "Save this script as...", "", ".json")
        if new_file_path:
            script_file_path = new_file_path
        else:
            self.invalid_path_alert_message()
            return False 
        ProjectController.set_dependencies_file(script_file_path + '.json')
        ProjectController.save_project()
        self.create_dependencies_json(script_file_path + '.json')

    def load_script(self):
        script_file = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if script_file:
            script_file_path = script_file
        else:
            self.invalid_path_alert_message()
            return False 
        ProjectController.set_dependencies_file(script_file_path)
        ProjectController.save_project()
        self.loadDependencies()

    def generate_script(self):
        filter = "json(*.json)"
        script_path, filter_type = QFileDialog.getOpenFileName(self, "Select script to generate...", "", filter)
        if script_path:
            script_file_path = script_path
        else:
            return False 
        try:
            ScriptGen2(script_path)
            self.script_gen_success()
        except:
            self.generateScriptError()
    
    def generateScriptError(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Error")
        messageBox.setText("Error: Missing Fields")
        messageBox.exec()
        
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

    def relationshipQueryChanged(self, text):
        self.search_relationships_lineedit.setText(text)
    
    def dependencyQueryChanged(self, text):
        self.search_dependency_lineedit.setText(text)

    def update_tables(self):
        self.listrelationships.clear()
        #self.listdependencies.clear()
        if ProjectController.is_project_loaded():
            self.populateTrees()
            if ProjectController.get_dependencies_file() != "":
                try:
                    self.loadDependencies()
                except:
                    pass

class ABSRelationshipTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        ___qtreewidgetitem = self.headerItem()
        ___qtreewidgetitem.setText(2,"Content")
        ___qtreewidgetitem.setText(1,"Time")
        ___qtreewidgetitem.setText(0,"Type")
        self.setAcceptDrops(False)
        self.setTabKeyNavigation(True)
        self.setDragEnabled(False)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setSortingEnabled(True)
        self.sortByColumn(1, QtCore.Qt.AscendingOrder)
        self.setWordWrap(True)
        self.setSortingEnabled(True)

    def addNode(self, _type=None, time=None, content=None, parent=None, canEdit=False, isSalientArtifact=False):
        if(parent is not None):
            tempQtreewidgetitem = QTreeWidgetItem(parent)
            if canEdit:
                tempQtreewidgetitem.setFlags(Qt.ItemIsEditable|Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            else:
                tempQtreewidgetitem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsDropEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
            
            if isSalientArtifact:
                tempQtreewidgetitem.setForeground(0,QtGui.QBrush(QtGui.QColor(ProjectController.get_artifact_color())))
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
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.TargetMoveAction)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setSortingEnabled(False)
        self.setWordWrap(True)

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
            if len(self.selectedItems()) > 0:
                row = self.selectedItems().pop()
                if row.parent(): 
                    parent = row.parent()
                    parent.removeChild(row)
                else:
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
        super().dropEvent(event)
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
    #             for j in range(5): # 3 columns in the tree
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
    #                     parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.BelowItem:
    #                 #something when being below an item
    #                 for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.OnItem:
    #                 #you're on an item, maybe add the current one as a child
    #                 parent = self.itemAt(dropIndex.row(), dropIndex.column())
    #                 for it in tree_items:
    #                     self.addNode(it.text(0), it.text(2), it.text(4), parent, True)
    #                 return
    #             elif dropIndicator == QAbstractItemView.OnViewport:
    #                 #you are not on your tree
    #                 return
            
    #         for it in tree_items:
    #                     parent = self.addNode(it.text(0), it.text(2), it.text(4), parent, True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BuilderWidget()
    sys.exit(app.exec())
