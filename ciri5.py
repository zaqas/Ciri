import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
import ciri2
from PyQt5 import QtGui


class FinalWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FinalWindow, self).__init__()
        uic.loadUi(os.path.join('ui_files', 'steganofinal.ui'), self)
        self.setFixedSize(1161, 1022)
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'rabbit.png')))
        self.setWindowTitle('Ciri')
        self.show()
        self.open = None
        self.pushButton_3.clicked.connect(self.go_back)

    def go_back(self):
        self.close()
        self.open = ciri2.MainWindow()
        self.open.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = FinalWindow()
    window.show()
    sys.exit(app.exec())
