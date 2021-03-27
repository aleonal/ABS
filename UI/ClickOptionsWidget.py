import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *


class ClickOptionsWidget(QtWidgets.QDialog):
    def __init__(self, selectedItem=None):
        super().__init__()
        self.setGeometry(50, 50, 838, 633)
        self.scrollArea = QScrollArea (self)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.verticalLayoutWidget = QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLabel = QLabel(self.verticalLayoutWidget)
        self.imageLabel.setObjectName(u"image")
        self.verticalLayout.addWidget(self.imageLabel,0)

        self.horizontalLayoutWidget = QWidget(self.verticalLayoutWidget)
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.xCoor = QLabel(self.verticalLayoutWidget)
        self.xCoor.setObjectName(u"xCoor")

        self.horizontalLayout.addWidget(self.xCoor)

        self.xlineEdit = QLineEdit(self.verticalLayoutWidget)
        self.xlineEdit.setObjectName(u"xlineEdit")
        self.xlineEdit.setMinimumSize(QSize(10, 20))
        self.xlineEdit.setMaximumSize(QSize(200, 20))
        self.xlineEdit.setMaxLength(10)

        self.horizontalLayout.addWidget(self.xlineEdit)

        self.yCoor = QLabel(self.verticalLayoutWidget)
        self.yCoor.setObjectName(u"yCoor")

        self.horizontalLayout.addWidget(self.yCoor)

        self.ylineEdit = QLineEdit(self.verticalLayoutWidget)
        self.ylineEdit.setObjectName(u"ylineEdit")
        self.ylineEdit.setMinimumSize(QSize(10, 20))
        self.ylineEdit.setMaximumSize(QSize(200, 20))
        self.ylineEdit.setMaxLength(10)

        self.horizontalLayout.addWidget(self.ylineEdit)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.clickComboBox = QComboBox(self.verticalLayoutWidget)
        self.clickComboBox.addItem("")
        self.clickComboBox.addItem("")
        self.clickComboBox.addItem("")
        self.clickComboBox.setObjectName(u"clickComboBox")
        self.clickComboBox.setMinimumSize(QSize(300, 20))
        self.clickComboBox.setMaximumSize(QSize(400, 20))

        self.horizontalLayout.addWidget(self.clickComboBox)

        self.saveButton = QPushButton(self.verticalLayoutWidget)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(100, 20))
        self.saveButton.setMaximumSize(QSize(300, 20))
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.saveSettings)
        self.horizontalLayout.addWidget(self.saveButton)


        self.verticalLayout.addWidget(self.horizontalLayoutWidget,1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi()
        self.xlineEdit.textChanged[str].connect(self.xCoorChanged)
        self.ylineEdit.textChanged[str].connect(self.yCoorChanged)

        QMetaObject.connectSlotsByName(self)
        if selectedItem is not None:
            self.selectedItem = selectedItem
            self.loadImage(self.selectedItem.text(4))
        #test 
        else:
            self.loadImage(r"C:\Users\dgriv\OneDrive\Documents\GitHub\practicum\ECELdSample\Ping\ecel-export_1613199564\raw\pykeylogger\click_images\1613199453.5309389_qterminal_root.png")
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Click Options", u"Click Options", None))
        self.imageLabel.setText(QCoreApplication.translate("Click Options", u"Screenshot", None))
        self.xCoor.setText(QCoreApplication.translate("Click Options", u"X Coordinates", None))
        self.yCoor.setText(QCoreApplication.translate("Click Options", u"Y Coordinates", None))
        self.label_2.setText(QCoreApplication.translate("Click Options", u"Click Type", None))
        self.clickComboBox.setItemText(0, QCoreApplication.translate("Click Options", u"leftClick", None))
        self.clickComboBox.setItemText(1, QCoreApplication.translate("Click Options", u"rightClick", None))
        self.clickComboBox.setItemText(2, QCoreApplication.translate("Click Options", u"doubleClick", None))

        self.clickComboBox.setCurrentText(QCoreApplication.translate("Click Options", u"leftClick", None))
        self.saveButton.setText(QCoreApplication.translate("Click Options", u"Save", None))
    # retranslateUi

    def loadImage(self, img_file=None):
        if img_file is not None:
            image = QPixmap(img_file)
            self.resize(image.width()+100, image.height()+100)
            self.scrollArea.resize(image.width()+100, image.height()+100)
            self.scrollAreaWidgetContents.resize(image.width()+100, image.height()+100)
            self.verticalLayoutWidget.resize(image.width(), image.height() + self.horizontalLayoutWidget.height() + 30)
            self.horizontalLayoutWidget.setGeometry(0, image.height() + 10, image.width()/2, self.horizontalLayoutWidget.height())
            self.imageLabel.resize(image.width(), image.height()+20)
            self.imageLabel.setPixmap(image)
            self.imageLabel.mousePressEvent = self.getPos

    def getPos(self , event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.xlineEdit.setText(str(self.x))
        self.ylineEdit.setText(str(self.y))
        self.saveButton.setEnabled(True)
    
    def xCoorChanged(self, text):
        self.xlineEdit.setText(text)

    def yCoorChanged(self, text):
        self.ylineEdit.setText(text)

    def saveSettings(self):
        if self.selectedItem is not None:
            self.selectedItem.setText(1, self.clickComboBox.currentText())
            self.selectedItem.setText(3, "{ \"x\":" + str(self.x) + ", \"y\":" + str(self.y) + "}")
            self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClickOptionsWidget()
    window.show()
    sys.exit(app.exec())