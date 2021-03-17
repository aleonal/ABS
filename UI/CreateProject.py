# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Create Project.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from UI.CausationExtractorWidget import CausationExtractorWidget
from src import ProjectController
from UI.ArtifactsTableWidget import SalientArtifactWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os

class CreateProjectWidget(QWidget):
    def __init__(self, projectInfo=None, project_status=True, previous_window=None):
        super().__init__()
        self.projectInfo = projectInfo
        self.previous_window = previous_window
        self.artifacts_window = SalientArtifactWindow()
        self.project_root = "C:\\Test\\Ping\\TestOutputCE"
        self.ECELD_root = r"C:\Test\Ping\ecel-export_1613199564"
        self.UI()
        self.show()
    def UI(self):
        self.setObjectName("Widget")
        self.resize(640, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(640, 480))
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 461))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.widget_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setObjectName("widget_layout")
        self.input_layout = QtWidgets.QGridLayout()
        self.input_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.input_layout.setContentsMargins(-1, -1, -1, 0)
        self.input_layout.setVerticalSpacing(0)
        self.input_layout.setObjectName("input_layout")
        self.root_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.root_text.setObjectName("root_text")
        self.input_layout.addWidget(self.root_text, 0, 0, 1, 1)
        self.timeframe_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.timeframe_field.setObjectName("timeframe_field")
        self.timeframe_field.textChanged[str].connect(self.onTimeframeChanged)
        self.input_layout.addWidget(self.timeframe_field, 2, 1, 1, 1)
        self.import_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.import_field.setObjectName("import_field")
        self.input_layout.addWidget(self.import_field, 1, 1, 1, 1)

        self.ECELD_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ECELD_button.sizePolicy().hasHeightForWidth())
        self.ECELD_button.setSizePolicy(sizePolicy)
        self.ECELD_button.setObjectName("ECELD_button")
        self.input_layout.addWidget(self.ECELD_button, 1, 2, 1, 1)
        self.ECELD_button.pressed.connect(self.GetECELDRoot)

        self.import_field.textChanged[str].connect(self.onECELDRootChanged)

        self.root_field = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.root_field.setObjectName("root_field")
        self.input_layout.addWidget(self.root_field, 0, 1, 1, 1)
        self.root_field.textChanged[str].connect(self.onProjectRootChanged)

        self.timeframe_text = QtWidgets.QLabel(self.verticalLayoutWidget)

        self.root_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.root_button.sizePolicy().hasHeightForWidth())
        self.root_button.setSizePolicy(sizePolicy)
        self.root_button.setObjectName("root_button")
        self.input_layout.addWidget(self.root_button, 0, 2, 1, 1)
        self.root_button.pressed.connect(self.GetProjectRoot)

        self.timeframe_text.setObjectName("timeframe_text")
        self.input_layout.addWidget(self.timeframe_text, 2, 0, 1, 1)
        self.import_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.import_text.setObjectName("import_text")
        self.input_layout.addWidget(self.import_text, 1, 0, 1, 1)
        self.input_layout.setRowStretch(0, 1)
        self.widget_layout.addLayout(self.input_layout)
        self.button_layout = QtWidgets.QGridLayout()
        self.button_layout.setObjectName("button_layout")
        
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button, 0, 0, 1, 1)
        self.cancel_button.pressed.connect(self.closeRoutine)
        
        self.salientart_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.salientart_button.sizePolicy().hasHeightForWidth())
        self.salientart_button.setSizePolicy(sizePolicy)
        self.salientart_button.setObjectName("salientart_button")
        self.button_layout.addWidget(self.salientart_button, 0, 1, 1, 1)
        self.salientart_button.pressed.connect(self.artifacts_window.show)
        
        self.create_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_button.sizePolicy().hasHeightForWidth())
        self.create_button.setSizePolicy(sizePolicy)
        self.create_button.setObjectName("create_button")
        self.button_layout.addWidget(self.create_button, 0, 2, 1, 1)
        self.widget_layout.addLayout(self.button_layout)

        self.create_button.pressed.connect(self.CausationExtractor)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Create Project", "Create Project"))
        self.root_text.setText(_translate("Widget", "Root Directory:\n"))
# "\n"
# "*If directory does not exist,\n"
# "it will be created"))
        self.timeframe_field.setText(_translate("Widget", "2000"))
        self.import_field.setText(_translate("Widget", self.ECELD_root))
        self.root_field.setText(_translate("Widget", self.project_root))
        self.root_button.setText(_translate("Widget", "..."))
        self.ECELD_button.setText(_translate("Widget", "..."))
        self.timeframe_text.setText(_translate("Widget", "Time Frame (in sec):"))
        self.import_text.setText(_translate("Widget", "Imported Data Directory:"))
        self.cancel_button.setText(_translate("Widget", "Cancel"))
        self.salientart_button.setText(_translate("Widget", "Edit Salient Artifacts"))
        self.create_button.setText(_translate("Widget", "Create Project"))
        self.setWindowIcon(QtGui.QIcon("A.png"))# A icon
    
    def CausationExtractor(self):
        ProjectController.ProjectController.create_project(self.import_field.text(), self.root_field.text(), "Test",self.timeframe_field.text())
        ProjectController.ProjectController.save_project()
        self.CEWidget = CausationExtractorWidget(previous_window=self)
        self.CEWidget.show()
        self.hide()

    def GetProjectRoot(self):
        self.project_root = QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.root_field.setText(self.project_root)

    def GetECELDRoot(self):
        self.ECELD_root = QFileDialog.getExistingDirectory(self, 'Open Directory')
        self.import_field.setText(self.ECELD_root)

    def onProjectRootChanged(self, text):
        self.root_field.setText(text)

    def onECELDRootChanged(self, text):
        self.import_field.setText(text)

    def onTimeframeChanged(self, text):
        self.timeframe_field.setText(text)

    def closeRoutine(self):
        #(TODO): show dialog confirming action. If yes, close, if not continue

        if self.previous_window:
            self.previous_window.show()
            self.hide()
        else:
            self.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = CreateProjectWidget()
    ui.UI()
    ui.show()
    sys.exit(app.exec_())