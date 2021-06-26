import os
from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
import time
from PyQt5 import QtGui
import ciri2

LIMIT_TIME = 100


class MyTime(QThread):
    count_changed = pyqtSignal(int)

    def run(self):
        count = 0
        while count < LIMIT_TIME:
            count += 1
            time.sleep(0.03)
            self.count_changed.emit(count)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        # Load and display Ui
        uic.loadUi(os.path.join('ui_files', 'steganowelcome.ui'), self)
        self.show()
        self.open = None
        self.calc_progress = None
        # Window cannot be resized
        self.setFixedSize(1161, 1022)
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'rabbit.png')))
        self.setWindowTitle('Ciri')
        self.progressBar.setValue(0)
        self.at_start()

    def at_start(self):
        self.calc_progress = MyTime()
        self.calc_progress.count_changed.connect(self.count_changed_progress)
        self.calc_progress.start()

    def count_changed_progress(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            time.sleep(1)
            self.open_new_window()

    def open_new_window(self):
        self.close()
        self.open = ciri2.MainWindow()
        self.open.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = Ui()
    window.show()
    sys.exit(app.exec())
