from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UI.BuilderWidget import BuilderWidget
from UI.RunnerWidget import RunnerWidget
from UI.CreateProject import CreateProjectWidget
from UI.ProjectInfoWidget import ProjectInfoWidget
from src.ProjectController import ProjectController
from pathlib import Path
import os
import sys
import subprocess
import webbrowser
import pathlib


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(MainWindow)
        MainWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
        MainWindow.setDockNestingEnabled(True)
        self.layout = QtWidgets.QVBoxLayout()

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setLayout(self.layout)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 1101, 811))
        self.tabWidget.setObjectName("tabWidget")

        #Creating Project Info tab
        self.project_info_tab = ProjectInfoWidget()
        self.project_info_tab.setAccessibleName("ProjectInfoWidget")
        self.project_info_tab.setObjectName("project_info_tab")
        self.tabWidget.addTab(self.project_info_tab, "")

        #Creating Builder tab
        self.builder_tab = BuilderWidget()
        self.builder_tab.setAccessibleName("BuilderWidget")
        self.builder_tab.setObjectName("builder_tab")
        self.tabWidget.addTab(self.builder_tab, "")

        #Creating Runner tab
        self.runner_tab = RunnerWidget()
        self.runner_tab.setAccessibleName("RunnerWidget")
        self.runner_tab.setObjectName("runner_tab")
        self.tabWidget.addTab(self.runner_tab, "")
        
        #Add all our tabs into our main windows layout
        self.layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        #Setup menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 558, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        #Setup statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Setup actions
        self.actionNew_Project = QtWidgets.QAction(MainWindow, triggered=self.new_project)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionOpen_Project = QtWidgets.QAction(MainWindow, triggered=self.open_directory)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionHelp = QtWidgets.QAction(MainWindow, triggered=self.help_Openpdf)
        self.actionHelp.setObjectName("actionHelp")
        self.actionExit = QtWidgets.QAction(MainWindow, triggered=self.exit)
        self.actionExit.setObjectName("actionExit")
        self.actionCausation_Extractor = QtWidgets.QAction(MainWindow)
        self.actionCausation_Extractor.setObjectName("actionCausation_Extractor")
        self.actionOpen_Builder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Builder.setObjectName("actionOpen_Builder")
        self.actionOpen_Runner = QtWidgets.QAction(MainWindow)
        self.actionOpen_Runner.setObjectName("actionOpen_Runner")
        
        #Add actions to menu buttons
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionHelp)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def help_Openpdf(self):
        webbrowser.open_new(r'ABS_document.pdf')

    def new_project(self):
        self.project_window = CreateProjectWidget(previous_window=self)
        self.project_window.show()

    def open_directory(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QFileDialog(), "Select Directory", directory=os.path.realpath(os.getcwd())))

        full_directory = Path(directory)
        PATH = full_directory / 'project_config.json'
        # Check if user clicks on cancel
        if (len(directory) <= 0):
            return
        # Check if project_config exists in chosen directory
        elif (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
            print("File exists and is readable")
            ProjectController.load_project(directory)
            if(ProjectController.is_project_loaded):
                QMessageBox.information(self.centralwidget, "Success", "Project has been loaded successfully.")
                self.update_tabs()
        else:
            print("Either the file is missing or not readable")
            QMessageBox.critical(self.centralwidget, "Project Failure", "Project could not be loaded. Check that directory contains appropriate files")

    # Updates Builder tab when project is loaded
    def update_tabs(self):
        if(ProjectController.is_project_loaded):
            self.project_info_tab.update_project_display()
            #Remove builder tab and insert it again - updates information
            self.tabWidget.removeTab(1)
            self.tabWidget.insertTab(1, BuilderWidget(), "Builder")
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Agent Build System"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project_info_tab), _translate("MainWindow", "Project Info"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.builder_tab), _translate("MainWindow", "Builder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.runner_tab), _translate("MainWindow", "Runner"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "About ABS"))
        self.actionCausation_Extractor.setText(_translate("MainWindow", "Causation Extractor"))
        self.actionOpen_Builder.setText(_translate("MainWindow", "Open Builder"))
        self.actionOpen_Runner.setText(_translate("MainWindow", "Open Runner"))
    
    def close_window(self):
        print("Close Window")
        self.close()

    def closeEvent(self,event):
        print("Close Event")
        event.accept()
        sys.exit()

    def exit(self):
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
