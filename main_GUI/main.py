import sys
from login import Ui_login
from signin_FaceID import Ui_signin_FaceID
from signin_Password import Ui_signin_Password
from signup import Ui_signup
from customer_Info import Ui_customer_Info
from account_Info import Ui_account_Info
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
import pics_ui_rc

class loginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: signin_FaceIDWindow.show())
        self.pushButton_2.clicked.connect(lambda: signin_PasswordWindow.show())
        self.pushButton_3.clicked.connect(lambda: signupWindow.show())

class signin_FaceIDWindow(QWidget, Ui_signin_FaceID):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class signin_PasswordWindow(QWidget, Ui_signin_Password):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: customer_InfoWindow.show())
        #self.pushButton.clicked.connect(lambda: account_InfoWindow.show())

class signupWindow(QWidget, Ui_signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class customer_InfoWindow(QWidget, Ui_customer_Info):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        _translate = QtCore.QCoreApplication.translate
        self.pushButton_2.setText(_translate("Form", "Account1"))
        self.pushButton_2.clicked.connect(lambda: account_InfoWindow.show())
        self.pushButton_3.setText(_translate("Form", "Account2"))
        self.pushButton.setText(_translate("Form", "Account3"))

class account_InfoWindow(QMainWindow, Ui_account_Info):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    loginWindow = loginWindow()
    signin_FaceIDWindow = signin_FaceIDWindow()
    signin_PasswordWindow = signin_PasswordWindow()
    signupWindow = signupWindow()
    customer_InfoWindow = customer_InfoWindow()
    account_InfoWindow = account_InfoWindow()

    loginWindow.show()

    sys.exit(app.exec_())