from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import *
import sys

class ClickSettings(QMainWindow):

    def __init__(self, selectedItem=None):
        super().__init__()
        self.initUI(selectedItem)

    def initUI(self, selectedItem):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the image and coordinate bar
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        # load image
        self.label = QLabel(self)
        # For testing purposes, if there is no selected click or timed item from the Builder, it will load a preset image
        if selectedItem is not None:
            self.selectedItem = selectedItem
            pixmap = QPixmap(self.selectedItem.text(4))
        else:
            self.selectedItem = None
            pixmap = QPixmap(r"C:\Users\valma\OneDrive\Desktop\Capture2.png") # Pre-set image filepath to load for testing purposes
        self.label.setPixmap(pixmap)
        self.label.mousePressEvent = self.getPos
        self.vbox.addWidget(self.label)

        # Clicks coordinate widget setup
        self.coorBoxWidget = QWidget(self)
        self.coorBoxLayout = QHBoxLayout(self.coorBoxWidget)
        self.coorBoxLayout.addStretch(1)
        self.coorBoxLayout.setObjectName(u"coorBoxLayout")
        self.xCoor = QLabel(self)
        self.xCoor.setObjectName(u"xCoor")
        self.coorBoxLayout.addWidget(self.xCoor)
        self.xlineEdit = QLineEdit(self)
        self.xlineEdit.setObjectName(u"xlineEdit")
        self.coorBoxLayout.addWidget(self.xlineEdit)
        self.yCoor = QLabel(self)
        self.yCoor.setObjectName(u"yCoor")
        self.coorBoxLayout.addWidget(self.yCoor)
        self.ylineEdit = QLineEdit(self)
        self.ylineEdit.setObjectName(u"ylineEdit")
        self.coorBoxLayout.addWidget(self.ylineEdit)

        # Click option setup / leftClick, rightClick, doubleClick
        self.clickOptionsLabel = QLabel(self)
        self.clickOptionsLabel.setObjectName(u"clickOptionsLabel")
        self.coorBoxLayout.addWidget(self.clickOptionsLabel)
        self.clickComboBox = QComboBox(self)
        self.clickComboBox.addItem("")
        self.clickComboBox.addItem("")
        self.clickComboBox.addItem("")
        self.clickComboBox.setObjectName(u"clickComboBox")
        self.clickComboBox.setMinimumSize(QSize(300,20))
        self.clickComboBox.setMaximumSize(QSize(400,20))
        self.coorBoxLayout.addWidget(self.clickComboBox)

        # Save button setup
        self.saveButton = QPushButton(self)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(100,20))
        self.saveButton.setMaximumSize(QSize(300,20))
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.saveSettings)
        self.coorBoxLayout.addWidget(self.saveButton)

        # Adds the coordinate widget to the vbox
        self.vbox.addWidget(self.coorBoxWidget)
        # Adds the vbox to the widget
        self.widget.setLayout(self.vbox)

        #Scroll Area setup
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # Make the scroll area the central widget
        self.setCentralWidget(self.scroll)

        # Sets up window
        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Click Options')
        self.xCoor.setText(QCoreApplication.translate('Click Options',u"X Coordinates", None))
        self.yCoor.setText(QCoreApplication.translate('Click Options',u"Y Coordinates", None))
        self.clickOptionsLabel.setText(QCoreApplication.translate("Click Options",u"Click Type", None))
        self.clickComboBox.setItemText(0, QCoreApplication.translate("Click Options", u"leftClick", None))
        self.clickComboBox.setItemText(1, QCoreApplication.translate("Click Options", u"rightClick", None))
        self.clickComboBox.setItemText(2, QCoreApplication.translate("Click Options", u"doubleClick", None))
        self.clickComboBox.setCurrentText(QCoreApplication.translate("Click Options", u"leftClick", None))
        self.saveButton.setText(QCoreApplication.translate("Click Options", u"Save", None))

        # Displays window
        self.show()

    # Returns coordinate position of click
    def getPos(self, event):
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.xlineEdit.setText(str(self.x))
        self.ylineEdit.setText(str(self.y))
        self.saveButton.setEnabled(True)

    # Saves the coordinate position onto the click or timed event object and displays it on the Builder Custom Attributes field.
    def saveSettings(self):
        if self.selectedItem is not None:
            self.selectedItem.setText(1, self.clickComboBox.currentText())
            self.selectedItem.setText(3, "{\"x\":" + str(self.x) + ", \"y\":" + str(self.y) + "}")
            # Closes the window after updating the coordinates in the Custom Attributes field in the Builder
            self.close()
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = ClickSettings()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()