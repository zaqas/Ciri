import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from extract import Extract
from embed import Embed


class MainWindow(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi(os.path.join('ui_files', 'ciri_menu.ui'), self)
            self.setWindowIcon(QIcon(os.path.join('images', 'rabbit_small.png')))
            self.setAttribute(Qt.WA_TranslucentBackground)

            self.extract = None
            self.embed = None
            self.show()

            # Menu page buttons
            self.revealButton.clicked.connect(self.open_extract_page)
            self.hideButton.clicked.connect(self.open_embed_page)
        except Exception as e:
            print(e)

    def open_extract_page(self):
        try:
            self.close()
            self.extract = Extract()
            self.extract.show()
        except Exception as e:
            print(e)


    def open_embed_page(self):
        try:
            self.close()
            self.embed = Embed()
            self.embed.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
