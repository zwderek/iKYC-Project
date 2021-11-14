import sys
from login import Ui_login
from signin_FaceID import Ui_signin_FaceID
from signin_Password import Ui_signin_Password
from signup import Ui_signup
from customer_Info import Ui_customer_Info
from profile_edit import Ui_profile_edit
from account_Info import Ui_account_Info
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
import pics_ui_rc



class loginWindow(QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
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
        self.initUi()

    def initUi(self):
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(lambda : self.signin())

    def signin(self):
        signin_username = self.lineEdit.text()
        signin_password = self.lineEdit_2.text()
        if True: #判断是否可以login
            customer_InfoWindow.customer_username = signin_username
            customer_InfoWindow.show()

class signupWindow(QWidget, Ui_signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(lambda: self.signup())

    def signup(self):
        signup_username = self.lineEdit.text()
        signup_password_1 = self.lineEdit_2.text()
        signup_password_2 = self.lineEdit_3.text()
        if True:  # 判断是否可以login 并创建用户
            customer_InfoWindow.customer_username = signup_username
            customer_InfoWindow.show()

class customer_InfoWindow(QWidget, Ui_customer_Info):
    customer_username = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
        username = None

    def initUi(self):

        self.textBrowser.setText("Welcome message and profile")
        self.textBrowser_2.setText("Login History")

        self.pushButton.clicked.connect(lambda: self.profile_edit())

        _translate = QtCore.QCoreApplication.translate

        self.btns = []

        for i in range(5):
            self.btns.append( QtWidgets.QPushButton(self.verticalLayoutWidget))
            self.btns[i].setText(str(i))
            self.verticalLayout.addWidget((self.btns[i]))
            #print(self.btns[i].text())
            self.btns[i].clicked.connect(lambda: self.account_Info(self.sender().text()))

    def profile_edit(self):
        profile_editWindow.profile_username =self.customer_username
        profile_editWindow.show()

    def account_Info(self, id):
        account_InfoWindow.account_id = id
        account_InfoWindow.update()
        # print(account_InfoWindow.account_id)
        account_InfoWindow.show()

class profile_editWindow(QWidget, Ui_profile_edit):
    profile_username = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.pushButton.clicked.connect(lambda: self.submit())

    def submit(self):
        edit_name = self.lineEdit.text()
        edit_gender = self.comboBox.currentText()
        edit_birthday = self.dateEdit.date()
        edit_email = self.lineEdit_4.text()
        edit_msg = self.plainTextEdit.toPlainText()
        edit_public = self.comboBox_2.currentText()
        #print(edit_name, edit_gender, edit_birthday, edit_email, edit_msg, edit_public)


class account_InfoWindow(QMainWindow, Ui_account_Info):
    account_id = -1

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(lambda: self.SearchOnClicked())
        self.pushButton_2.clicked.connect(lambda: self.DeleteOnClicked())

    def update(self):
        account_InfoWindow.lineEdit.setText(str(self.account_id))
        # fill in account_id
        account_InfoWindow.lineEdit_2.setText(str(self.account_id))
        # fill in customer_id
        account_InfoWindow.lineEdit_3.setText(str(self.account_id))
        # fill in type
        account_InfoWindow.lineEdit_4.setText(str(self.account_id))
        # fill in currency
        account_InfoWindow.lineEdit_5.setText(str(self.account_id))
        # fill in balance
        account_InfoWindow.lineEdit.setReadOnly(True)
        account_InfoWindow.lineEdit_2.setReadOnly(True)
        account_InfoWindow.lineEdit_3.setReadOnly(True)
        account_InfoWindow.lineEdit_4.setReadOnly(True)
        account_InfoWindow.lineEdit_5.setReadOnly(True)

        account_InfoWindow.pushButton_2.setEnabled(True)
        #if account 里有钱:
        account_InfoWindow.pushButton_2.setEnabled(False)
        # delete account
    def SearchOnClicked(self):
        month=self.comboBox.currentText()
        day=self.comboBox_2.currentText()
        time=self.comboBox_3.currentText()
        amount=self.comboBox_4.currentText()
        self.Search(month,day,time,amount)
    def DeleteOnClicked(self):
        print("delete")
    def Search(self,month,day,time,amount):
        print("search for it")
        print(month)
        print(day)
        print(time)
        print(amount)
        #不知道search函数最后怎么call，就先写成这样

if __name__ == '__main__':
    app = QApplication(sys.argv)

    loginWindow = loginWindow()

    signin_FaceIDWindow = signin_FaceIDWindow()
    signin_PasswordWindow = signin_PasswordWindow()
    signupWindow = signupWindow()
    customer_InfoWindow = customer_InfoWindow()
    profile_editWindow = profile_editWindow()
    account_InfoWindow = account_InfoWindow()

    loginWindow.show()

    sys.exit(app.exec_())