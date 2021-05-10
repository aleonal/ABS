import sys
import time
from PyQt5 import QtGui, QtCore, QtWidgets
from UI.UserInterface import Ui_MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)

    #Splashscreen ABS Logo
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('UI/ABS.png'))
    splash.show()
    QtCore.QTimer.singleShot(4000, splash.close)
    time.sleep(4)

    #Open Main Window
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if (__name__ == '__main__'):
    main()