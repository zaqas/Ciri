import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QLineEdit
from stegano import lsb
import ciri5


class Embed(QtWidgets.QMainWindow):
    def __init__(self):
        super(Embed, self).__init__()
        uic.loadUi(os.path.join('ui_files', 'steganoembed.ui'), self)
        self.setFixedSize(1161, 1022)
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'rabbit.png')))
        self.setWindowTitle('Ciri')
        self.show()

        self.selected_carrier = None
        self.saved = None
        self.open = None
        self.input_file = None
        self.b_pass = None

        self.openfile_button.clicked.connect(self.open_file)
        self.opencarrier_button.clicked.connect(self.open_carrier)
        self.setpass_button.clicked.connect(self.set_password)
        self.browse_button.clicked.connect(self.set_location)
        self.embed_button.clicked.connect(self.embed_it)

    def open_file(self):
        try:
            selected_file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
            with open(selected_file[0], 'rb') as inf:
                self.input_file = inf.read()
        except Exception as e:
            print(e)

    def set_password(self):
        try:
            text, ok = QInputDialog.getText(self, 'Password', 'Enter a password:', QLineEdit.Password)
            self.b_pass = text.encode()
        except Exception as e:
            print(e)

    def open_carrier(self):
        try:
            self.selected_carrier = QFileDialog.getOpenFileName(self, 'Open Carrier', '', 'Image Files (*.png)')
        except Exception as e:
            print(e)

    def encrypt_aes(self, secret_key, pt):
        try:
            # 32 bytes = 256 bit
            salt = get_random_bytes(32)
            key = scrypt(secret_key, salt=salt, key_len=32, N=2 ** 19, r=8, p=1)
            cipher = AES.new(key, AES.MODE_GCM)
            ct, tag = cipher.encrypt_and_digest(pt)
            return salt, ct, cipher.nonce, tag
        except Exception as e:
            print(e)

    def set_location(self):
        try:
            self.saved = QFileDialog.getSaveFileName(self, 'Save As', '.png', 'Image Files (*.png)')
            self.lineEdit.setText(self.saved[0])
        except Exception as e:
            print(e)

    def embed_it(self):
        try:
            encrypted_msg = self.encrypt_aes(self.b_pass, self.input_file)

            # Hide message inside carrier and save it
            secret_file = lsb.hide(self.selected_carrier[0], ''.join(str(encrypted_msg)))
            secret_file.save(self.saved[0])

            # Open final window if the operation was successful
            self.open_final_window()

        except Exception as e:
            print(e)

    def open_final_window(self):
        try:
            self.close()
            self.open = ciri5.FinalWindow()
            self.open.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = Embed()
    window.show()
    sys.exit(app.exec())
