import ast
import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QLineEdit, QWidget
from stegano import lsb
import result


class Extract(QWidget):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi(os.path.join('ui_files', 'ciri_extract.ui'), self)
            self.setWindowIcon(QIcon(os.path.join('images', 'rabbit_small.png')))
            self.show()

            self.complete_page = None
            self.open = None
            self.selected_carrier = None
            self.saved_file = None
            self.user_pass = None

            self.selectCarrier.clicked.connect(self.open_carrier)
            self.passwordButton.clicked.connect(self.get_password)
            self.locationButton.clicked.connect(self.set_extraction_loc)
            self.extractButton.clicked.connect(self.extract_it)
        except Exception as e:
            print(e)

    def open_carrier(self):
        try:
            self.selected_carrier = QFileDialog.getOpenFileName(self, 'Open Carrier', '', 'Image Files (*.png)')
        except Exception as e:
            print(e)

    def set_extraction_loc(self):
        try:
            self.saved_file = QFileDialog.getSaveFileName(self, 'Save As', '.txt', 'Text files (*.txt)')
        except Exception as e:
            print(e)

    def get_password(self):
        try:
            text, ok = QInputDialog.getText(self, 'Password', 'Enter a password:', QLineEdit.Password)
            self.user_pass = text.encode()
        except Exception as e:
            print(e)

    def decrypt_aes(self, ciphertext, salt, nonce, authentication_tag, secret_key):
        try:
            private_key = scrypt(secret_key, salt=salt, key_len=32, N=2 ** 21, r=8, p=1)
            cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, authentication_tag)
            return decrypted.decode('utf-8')
        except Exception as e:
            print(e)

    def reveal_lsb(self):
        try:
            encrypted_msg = lsb.reveal(self.selected_carrier[0])
            return encrypted_msg
        except Exception as e:
            print(e)

    def extract_it(self):
        try:
            # Retrieve encoded message from image
            msg = self.reveal_lsb()

            # Convert string into a tuple and access ciphertext, salt, tag and iv.
            encoded_tuple = ast.literal_eval(msg)
            salt = encoded_tuple[0]
            ct = encoded_tuple[1]
            iv = encoded_tuple[2]
            auth_tag = encoded_tuple[3]

            decrypted = self.decrypt_aes(ciphertext=ct, salt=salt, nonce=iv, authentication_tag=auth_tag,
                                         secret_key=self.user_pass)

            # Save plaintext in a txt file
            with open(self.saved_file[0], 'w') as sf:
                sf.write(decrypted)

            # If operation was a success, open complete page
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
    window = Extract()
    window.show()
    sys.exit(app.exec())
