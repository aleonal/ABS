import sys
import time
from PyQt5 import QtGui, QtCore, QtWidgets
#from UI.StartWindow import ProjectInfoWidget
#from UI.ProjectInfoWidget import ProjectInfoWidget
from UI.UserInterface import Ui_MainWindow

def main():
    #app = QtWidgets.QApplication(argv)



    #splash = QtWidgets.QSplashScreen(QtGui.QPixmap('UI/ABS.png'))
        # self.splash.move(10,10)
    #splash.show()
    #QtCore.QTimer.singleShot(4000, splash.close)

    #time.sleep(4)
    #lbl = QtWidgets.QLabel('/UI/ABS.png')
    #lbl.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
   # lbl.show()

    #QTimer.singleShot(4000, lbl.close())

    # make a dialog that runs in its own event loop
    #dlg = ProjectInfoWidget()
    #if ( not dlg.exec_() ):  # in C++, this would be dlg->exec()
    #    sys.exit(0)

    #var1, var2, var3 = dlg.values()   

    app = QtWidgets.QApplication(sys.argv)


    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('UI/ABS.png'))
        # self.splash.move(10,10)
    splash.show()
    QtCore.QTimer.singleShot(4000, splash.close)

    time.sleep(4)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())     

    #window = Ui_MainWindow()
    #window.setPropertyOne(var1)
    #window.setPropertyTwo(var2)
    #window.setPropertyThree(var3)
    #window.show()

    #sys.exit(app.exec_())

if ( __name__ == '__main__' ):
    main()