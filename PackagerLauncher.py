import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from UI.PackagerWidget import PackagerWidget

def main():

    #Open Packager Window
    app = QtWidgets.QApplication(sys.argv)
    
    #setup style sheet
    style = """
        QPushButton{
            color: #ffffff;
            background: #8f8f8f;
            border: 3px #000000 solid;
            padding: 5px 10px;
            border-radius: 2px;
            font-weight: plain;
            font-size: 9pt;
            outline: none;
        }
        QPushButton:hover{
            border: 3px #000000 solid;
            background: #80aaff;
        }
    """
    app.setStyleSheet(style)
    # # # # #end style
    ui = PackagerWidget()
    ui.show()
    sys.exit(app.exec_())


if (__name__ == '__main__'):
    main()