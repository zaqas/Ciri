import os
from PyQt5 import uic
import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGraphicsDropShadowEffect, QWidget
import time
import menu
LIMIT_TIME = 100


class MyTime(QThread):
    count_changed = pyqtSignal(int)

    def run(self):
        try:
            count = 0
            while count < LIMIT_TIME:
                count += 1
                time.sleep(0.03)
                self.count_changed.emit(count)
        except Exception as e:
            print(e)


class Ui(QWidget):
    def __init__(self):
        try:
            super().__init__()

            # Load and display Ui
            uic.loadUi(os.path.join('ui_files', 'splash_ciri.ui'), self)
            self.setWindowIcon(QIcon(os.path.join('images', 'rabbit_small.png')))
            self.open = None
            self.calc_progress = None

            # Remove window frame
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # Shadow effect
            self.shadow = QGraphicsDropShadowEffect(self)
            self.shadow.setBlurRadius(20)
            self.shadow.setOffset(0, 0)
            self.shadow.setColor(QColor(0, 0, 0, 60))
            self.setGraphicsEffect(self.shadow)

            self.progressBar.setValue(0)

            self.at_start()
            self.center_window()
            self.show()
        except Exception as e:
            print(e)

    def center_window(self):
        try:
            resolution = QDesktopWidget().screenGeometry()
            self.move(int(resolution.width() / 2) - int(self.frameSize().width() / 2),
                      int(resolution.height() / 2) - int(self.frameSize().height() / 2))
        except Exception as e:
            print(e)

    def at_start(self):
        try:
            self.calc_progress = MyTime()
            self.calc_progress.count_changed.connect(self.count_changed_progress)
            self.calc_progress.start()
        except Exception as e:
            print(e)

    def count_changed_progress(self, value):
        try:
            self.progressBar.setValue(value)
            if value == 100:
                time.sleep(1)
                self.open_new_window()
        except Exception as e:
            print(e)

    def open_new_window(self):
        try:
            self.close()
            self.open = menu.MainWindow()
            self.open.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = Ui()
    window.show()
    sys.exit(app.exec())
