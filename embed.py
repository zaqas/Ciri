import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QLineEdit, QWidget
from stegano import lsb
import result


class Embed(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi(os.path.join('ui_files', 'ciri_embed.ui'), self)
            self.setWindowIcon(QIcon(os.path.join('images', 'rabbit_small.png')))
            self.show()

            self.complete_page = None
            self.selected_carrier = None
            self.saved = None
            self.open = None
            self.input_file = None
            self.b_pass = None

            self.selectFileButton.clicked.connect(self.open_file)
            self.selectCarrierButton.clicked.connect(self.open_carrier)
            self.encryptButton.clicked.connect(self.set_password)
            self.embedButton.clicked.connect(self.embed_it)
        except Exception as e:
            print(e)

    def open_file(self):
        try:
            selected_file = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
            with open(selected_file[0], 'rb') as infi:
                self.input_file = infi.read()
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
            salt = get_random_bytes(32)
            key = scrypt(secret_key, salt=salt, key_len=32, N=2 ** 21, r=8, p=1)
            cipher = AES.new(key, AES.MODE_GCM)
            ct, tag = cipher.encrypt_and_digest(pt)
            return salt, ct, cipher.nonce, tag
        except Exception as e:
            print(e)

    def embed_it(self):
        try:
            encrypted_msg = self.encrypt_aes(self.b_pass, self.input_file)

            # Hide message inside carrier and save it
            secret_file = lsb.hide(self.selected_carrier[0], ''.join(str(encrypted_msg)))
            secret_file.save("nothing_suspicious.png")
            # If operation was a success, open complete operation page
            self.open_complete_page()

        except Exception as e:
            print(e)

    def open_complete_page(self):
        try:
            self.close()
            self.complete_page = result.FinalWindow()
            self.complete_page.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Ciri')
    window = Embed()
    window.show()
    sys.exit(app.exec())
