import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *


class DependencyOptionsWidget(QtWidgets.QDialog):
    def __init__(self, selectedItem=None):
        super().__init__()
        self.resize(402, 300)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(0, 0, 401, 301))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        self.type_label = QLabel(self.formLayoutWidget)
        self.type_label.setObjectName(u"type_label")
        self.type_label.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.type_label)

        self.type_comboBox = QComboBox(self.formLayoutWidget)
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.addItem("")
        self.type_comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.type_comboBox)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.subtype_comboBox = QComboBox(self.formLayoutWidget)
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.addItem("")
        self.subtype_comboBox.setObjectName(u"comboBox_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.subtype_comboBox)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.time_lineEdit = QLineEdit(self.formLayoutWidget)
        self.time_lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.time_lineEdit)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.attributes_textEdit = QTextEdit(self.formLayoutWidget)
        self.attributes_textEdit.setObjectName(u"textEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.attributes_textEdit)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.content_textEdit = QTextEdit(self.formLayoutWidget)
        self.content_textEdit.setObjectName(u"textEdit_2")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.content_textEdit)

        self.save_button = QPushButton(self.formLayoutWidget)
        self.save_button.setObjectName(u"save_button")
        self.save_button.clicked.connect(self.saveSettings)

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.save_button)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)
        
        if selectedItem is not None:
            self.selectedItem = selectedItem
            self.loadItem()
        #test 
        else:
            self.close()
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dependency Options", u"Dependency Options", None))
        self.type_label.setText(QCoreApplication.translate("Dependency Options", u"Type", None))
        self.type_comboBox.setItemText(0, QCoreApplication.translate("Dependency Options", u"keypresses_id", None))
        self.type_comboBox.setItemText(1, QCoreApplication.translate("Dependency Options", u"clicks_id", None))
        self.type_comboBox.setItemText(2, QCoreApplication.translate("Dependency Options", u"auditd_id", None))
        self.type_comboBox.setItemText(3, QCoreApplication.translate("Dependency Options", u"timed_id", None))
        self.type_comboBox.setItemText(4, QCoreApplication.translate("Dependency Options", u"traffic_all_id", None))
        self.type_comboBox.setItemText(5, QCoreApplication.translate("Dependency Options", u"traffic_xy_id", None))
        self.type_comboBox.setItemText(6, QCoreApplication.translate("Dependency Options", u"suricata_id", None))

        self.label.setText(QCoreApplication.translate("Dependency Options", u"Subtype", None))
        self.subtype_comboBox.setItemText(0, QCoreApplication.translate("Dependency Options", u"leftClick", None))
        self.subtype_comboBox.setItemText(1, QCoreApplication.translate("Dependency Options", u"rightClick", None))
        self.subtype_comboBox.setItemText(2, QCoreApplication.translate("Dependency Options", u"doubleClick", None))
        self.subtype_comboBox.setItemText(3, QCoreApplication.translate("Dependency Options", u"type", None))
        self.subtype_comboBox.setItemText(4, QCoreApplication.translate("Dependency Options", u"command", None))
        self.subtype_comboBox.setItemText(5, QCoreApplication.translate("Dependency Options", u"hotkey", None))
        self.subtype_comboBox.setItemText(6, QCoreApplication.translate("Dependency Options", u"keyDown", None))
        self.subtype_comboBox.setItemText(7, QCoreApplication.translate("Dependency Options", u"keyUp", None))

        self.label_2.setText(QCoreApplication.translate("Dependency Options", u"Time", None))
        self.time_lineEdit.setInputMask("")
        self.time_lineEdit.setPlaceholderText(QCoreApplication.translate("Dependency Options", u"YYYY-mm-ddTHH:MM:SS", None))
        self.label_3.setText(QCoreApplication.translate("Dependency Options", u"Attributes", None))
        self.label_4.setText(QCoreApplication.translate("Dependency Options", u"Content", None))
        self.save_button.setText(QCoreApplication.translate("Dependency Options", u"Save", None))
    # retranslateUi

    def timeChanged(self, text):
        self.time_lineEdit.setText(text)

    def attributesChanged(self, text):
        self.attributes_textEdit.setText(text)

    def contentChanged(self, text):
        self.content_textEdit.setText(text)

    def loadItem(self):
        typeindex = self.type_comboBox.findText(self.selectedItem.text(0))
        self.type_comboBox.setCurrentIndex(typeindex)
        subtypeindex = self.subtype_comboBox.findText(self.selectedItem.text(1))
        self.subtype_comboBox.setCurrentIndex(subtypeindex)
        self.time_lineEdit.setText(self.selectedItem.text(2))
        self.attributes_textEdit.setText(self.selectedItem.text(3))
        self.content_textEdit.setText(self.selectedItem.text(4))

    def saveSettings(self):
        if self.selectedItem is not None:
            self.selectedItem.setText(0, self.type_comboBox.currentText())
            self.selectedItem.setText(1, self.subtype_comboBox.currentText())
            self.selectedItem.setText(2, self.time_lineEdit.text())
            self.selectedItem.setText(3, self.attributes_textEdit.toPlainText())
            self.selectedItem.setText(4, self.content_textEdit.toPlainText())
            self.accept()