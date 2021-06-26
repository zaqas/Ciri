import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import ciri3
import ciri4


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join('ui_files', 'stegchoice.ui'), self)
        self.setFixedSize(1161, 1022)
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'rabbit.png')))
        self.setWindowTitle('Ciri')
        self.show()
        self.open = None
        # User has to choose between extract and embed
        self.pushButton_3.clicked.connect(self.open_extract_window)
        self.pushButton_4.clicked.connect(self.open_embed_window)

    def open_embed_window(self):
        # Close current window
        self.close()
        # Open embed window
        self.open = ciri3.Embed()
        self.open.show()

    def open_extract_window(self):
        self.close()
        self.open = ciri4.Extract()
        self.open.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
