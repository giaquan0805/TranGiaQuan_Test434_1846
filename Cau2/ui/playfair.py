# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import requests


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1133, 844)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(440, 10, 281, 71))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 51, 71))
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.txtKey = QtWidgets.QLineEdit(self.centralwidget)
        self.txtKey.setGeometry(QtCore.QRect(250, 120, 501, 41))
        self.txtKey.setObjectName("txtKey")

        self.btnCreateMatrix = QtWidgets.QPushButton(self.centralwidget)
        self.btnCreateMatrix.setGeometry(QtCore.QRect(250, 190, 131, 41))
        self.btnCreateMatrix.setObjectName("btnCreateMatrix")

        # Dùng QTableWidget để setItem được
        self.tblMatrix = QtWidgets.QTableWidget(self.centralwidget)
        self.tblMatrix.setGeometry(QtCore.QRect(250, 240, 256, 192))
        self.tblMatrix.setObjectName("tblMatrix")
        self.tblMatrix.setRowCount(5)
        self.tblMatrix.setColumnCount(5)
        self.tblMatrix.horizontalHeader().setVisible(False)
        self.tblMatrix.verticalHeader().setVisible(False)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 470, 101, 41))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.txtPlainText = QtWidgets.QTextEdit(self.centralwidget)
        self.txtPlainText.setGeometry(QtCore.QRect(240, 460, 541, 71))
        self.txtPlainText.setObjectName("txtPlainText")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 580, 131, 51))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.txtCipherText = QtWidgets.QTextEdit(self.centralwidget)
        self.txtCipherText.setGeometry(QtCore.QRect(240, 560, 541, 71))
        self.txtCipherText.setObjectName("txtCipherText")

        self.btnEncrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btnEncrypt.setGeometry(QtCore.QRect(240, 670, 201, 51))
        self.btnEncrypt.setObjectName("btnEncrypt")

        self.btnDecrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btnDecrypt.setGeometry(QtCore.QRect(590, 670, 191, 51))
        self.btnDecrypt.setObjectName("btnDecrypt")

        self.txtDecryptedText = QtWidgets.QTextEdit(self.centralwidget)
        self.txtDecryptedText.setGeometry(QtCore.QRect(823, 460, 241, 171))
        self.txtDecryptedText.setObjectName("txtDecryptedText")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect button
        self.btnCreateMatrix.clicked.connect(self.create_matrix)
        self.btnEncrypt.clicked.connect(self.encrypt_text)
        self.btnDecrypt.clicked.connect(self.decrypt_text)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Playfair Cipher"))
        self.label.setText(_translate("MainWindow", "PLAYFAIR CIPHER"))
        self.label_2.setText(_translate("MainWindow", "KEY"))
        self.btnCreateMatrix.setText(_translate("MainWindow", "Create Matrix"))
        self.label_3.setText(_translate("MainWindow", "Plain text"))
        self.label_4.setText(_translate("MainWindow", "Cipher Text"))
        self.btnEncrypt.setText(_translate("MainWindow", "Encrypt"))
        self.btnDecrypt.setText(_translate("MainWindow", "Decrypt"))

    def create_matrix(self):
        try:
            key = self.txtKey.text()

            response = requests.post(
                "http://127.0.0.1:5000/api/playfair/creatematrix",
                json={"key": key}
            )

            matrix = response.json()["playfair_matrix"]

            for i in range(5):
                for j in range(5):
                    item = QtWidgets.QTableWidgetItem(str(matrix[i][j]))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tblMatrix.setItem(i, j, item)

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))

    def encrypt_text(self):
        try:
            key = self.txtKey.text()
            plain_text = self.txtPlainText.toPlainText()

            response = requests.post(
                "http://127.0.0.1:5000/api/playfair/encrypt",
                json={
                    "key": key,
                    "plain_text": plain_text
                }
            )

            encrypted_text = response.json()["encrypted_text"]
            self.txtCipherText.setPlainText(encrypted_text)

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))

    def decrypt_text(self):
        try:
            key = self.txtKey.text()
            cipher_text = self.txtCipherText.toPlainText()

            response = requests.post(
                "http://127.0.0.1:5000/api/playfair/decrypt",
                json={
                    "key": key,
                    "cipher_text": cipher_text
                }
            )

            decrypted_text = response.json()["decrypted_text"]
            self.txtDecryptedText.setPlainText(decrypted_text)

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", str(e))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())