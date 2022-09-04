import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
import menu


class FinalWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi(os.path.join('ui_files', 'ciri_complete.ui'), self)
            self.setWindowIcon(QIcon(os.path.join('images', 'rabbit_small.png')))
            self.show()

            self.open_menu = None
            self.returnButton.clicked.connect(self.return_to_menu)
        except Exception as e:
            print(e)

    def return_to_menu(self):
        try:
            self.close()
            self.open_menu = menu.MainWindow()
            self.open_menu.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = FinalWindow()
    window.show()
    sys.exit(app.exec())
