# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProjectInfo.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *

class ProjectInfoWidget(QWidget):
    def __init__(self, project=None, project_status=True):
        super().__init__()
        self.project = project
        self.UI()
        self.show()

    def UI(self):
        self.setObjectName("project_info_widget")
        
        # Window sizing
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(640, 480))

        # Project details label
        self.project_label = QtWidgets.QLabel(self)
        self.project_label.setObjectName("project_label")

        # Project information list
        self.project_info = QtWidgets.QListWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_info.sizePolicy().hasHeightForWidth())
        self.project_info.setSizePolicy(sizePolicy)

        # Project information items - currently hardcoded, must call backend
        # to populate project info list
        self.project_info.setMinimumSize(QtCore.QSize(0, 0))
        self.project_info.setObjectName("project_info")
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.project_info.addItem(item)

        # Runner component button
        self.runner_button = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runner_button.sizePolicy().hasHeightForWidth())
        self.runner_button.setSizePolicy(sizePolicy)
        self.runner_button.setObjectName("runner_button")
        self.runner_button.clicked.connect(self.launchRunner)

        # Assumes project object has property "isNew" labling new project
        if not self.project or self.project.isNew:
            self.runner_button.setEnabled(False)

        # Builder component button
        self.builder_button = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.builder_button.sizePolicy().hasHeightForWidth())
        self.builder_button.setSizePolicy(sizePolicy)
        self.builder_button.setObjectName("builder_button")
        self.builder_button.clicked.connect(self.launchBuilder)

        # Close project button
        self.close_button = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        self.close_button.setObjectName("close_button")
        self.close_button.clicked.connect(self.closeRoutine)

        # Layout for buttons
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.close_button, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addWidget(self.builder_button, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.runner_button, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.horizontalLayout.setStretch(0, 1)

        # Widget layout
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.project_label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addWidget(self.project_info)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        
        self.setWindowTitle(_translate("Widget", "ABS - Project Information"))
        self.project_label.setText(_translate("Widget", "Project Details"))

        # This translation needs to be done programatically, create separate function
        __sortingEnabled = self.project_info.isSortingEnabled()
        self.project_info.setSortingEnabled(False)
        item = self.project_info.item(0)
        item.setText(_translate("Widget", "Salient Artifacts: 6"))
        item = self.project_info.item(1)
        item.setText(_translate("Widget", "Dependencies: 10"))
        item = self.project_info.item(2)
        item.setText(_translate("Widget", "Root Directory: /user/abs/x/proj1"))
        item = self.project_info.item(3)
        item.setText(_translate("Widget", "Imported Data Directory: /user/eceld/x/recording1"))
        item = self.project_info.item(4)
        item.setText(_translate("Widget", "Salient Artifact Directory: /user/abs/x/proj1/salientartifacts.txt"))
        self.project_info.setSortingEnabled(__sortingEnabled)

        self.runner_button.setText(_translate("Widget", "Launch Runner"))
        self.builder_button.setText(_translate("Widget", "Launch Builder"))
        self.close_button.setText(_translate("Widget", "Close Project"))

    def closeRoutine(self):
        #(TODO): SAVE PROJECT BEFORE CLOSING (call backend)
        self.close()

    #(TODO): REFACTOR THESE INTO 1 WITH SWITCH FOR WINDOW TYPE
    def launchBuilder(self):
        # self.builder = BuilderWidget()
        # self.builder.show()
        self.hide()

    def launchRunner(self):
        # self.runner = RunnerWidget()
        # self.runner.show()
        self.hide()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ProjectInfoWidget()
    ui.show()
    sys.exit(app.exec_())