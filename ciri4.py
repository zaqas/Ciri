import ast
import os
import sys
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from PyQt5 import QtGui
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QLineEdit
from stegano import lsb
import ciri5


class Extract(QtWidgets.QMainWindow):
    def __init__(self):
        super(Extract, self).__init__()
        uic.loadUi(os.path.join('ui_files', 'steganoextract.ui'), self)
        self.setFixedSize(1161, 1022)
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'rabbit.png')))
        self.setWindowTitle('Ciri')
        self.show()

        self.open = None
        self.selected_carrier = None
        self.saved_file = None
        self.user_pass = None

        self.opencarrier_button.clicked.connect(self.open_carrier)
        self.decrypt_button.clicked.connect(self.get_password)
        self.browse_button.clicked.connect(self.set_extraction_loc)
        self.extract_button.clicked.connect(self.extract_it)

    def open_carrier(self):
        try:
            self.selected_carrier = QFileDialog.getOpenFileName(self, 'Open Carrier', '', 'Image Files (*.png)')
        except Exception as e:
            print(e)

    def set_extraction_loc(self):
        try:
            self.saved_file = QFileDialog.getSaveFileName(self, 'Save As', '.txt', 'Text files (*.txt)')
            self.lineEdit.setText(self.saved_file[0])
        except Exception as e:
            print(e)

    def get_password(self):
        try:
            text, ok = QInputDialog.getText(self, 'Password', 'Enter a password:', QLineEdit.Password)
            self.user_pass = text.encode()
        except Exception as e:
            print(e)

    def decrypt_aes(self, ciphertext, salt, nonce, authentication_tag, secret_key):
        private_key = scrypt(secret_key, salt=salt, key_len=32, N=2 ** 19, r=8, p=1)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, authentication_tag)
        return decrypted.decode('utf-8')

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
    window = Extract()
    window.show()
    sys.exit(app.exec())
