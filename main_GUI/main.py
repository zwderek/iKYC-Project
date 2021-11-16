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
import functions
import pics_ui_rc
from collections import OrderedDict

from functions import *
from FrontHelper import *


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
        loginWindow.close()
        signin_PasswordWindow.close()

        signin_username = self.lineEdit.text()
        signin_password = self.lineEdit_2.text()
        tmp = demo.password_login(signin_username, signin_password)
        #print(signin_username, signin_password, tmp)
        if tmp > 0:
            customer_InfoWindow.customer_id = tmp
            demo.create_history(tmp)
            customer_InfoWindow.initUi() #update
            customer_InfoWindow.addButton()
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
        loginWindow.close()
        signin_PasswordWindow.close()

        signup_username = self.lineEdit.text()
        signup_password_1 = self.lineEdit_2.text()
        signup_password_2 = self.lineEdit_3.text()

        if signup_password_1 == signup_password_2:  # 判断是否可以login 并创建用户
            tmp = demo.create_user(signup_username, signup_password_1)
            print(tmp)
            if tmp > 0:
                customer_InfoWindow.customer_id = tmp
                demo.create_history(tmp)
                customer_InfoWindow.initUi()
                customer_InfoWindow.addButton()
                customer_InfoWindow.show()
            if tmp == -2:
                self.lineEdit.setText("This name is already been used!")
        else:
            self.lineEdit_2.setText("Please reenter your password!")


class customer_InfoWindow(QWidget, Ui_customer_Info):
    customer_id = -1
    display_customer_info = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
    #   print(self.customer_id)

    def initUi(self):
        self.textBrowser.setText("Welcome! You can edit your own profile now!")
        result = demo.display_login_info(self.customer_id)
        self.display_customer_info = result["customer_and_login"]
        self.display_user_profile = result["profile"]
        if Util.isNotNone(self.display_customer_info):
            username = self.display_customer_info[0]
            login_time = self.display_customer_info[1]
            login_date = self.display_customer_info[2]
            to_pack = OrderedDict()
            to_pack["username"] = username
            to_pack["login_time"] = login_time
            to_pack["login_date"] = login_date
            # self.textBrowser_2.setText("username = " + username + "\nlogin_time = " + login_time + "\nlogin_date = " + login_time)
            self.textBrowser_2.setText(FrontHelper.dictionaryToInfostring(to_pack))
        if Util.isNotNone(self.display_user_profile):
            profile_name = self.display_user_profile[0]
            gender = self.display_user_profile[1] #tbd
            birthday = self.display_user_profile[2]
            email = self.display_user_profile[3]
            welcome_msg = self.display_user_profile[5]
            is_public = self.display_user_profile[6]
            to_pack = OrderedDict()
            to_pack["Welcome"] = welcome_msg
            to_pack["profile_name"] = profile_name
            to_pack["gender"] = FrontHelper.genderToString(gender)
            to_pack["birthday"] = birthday
            to_pack["email"] = email
            to_pack["Profile status"] = FrontHelper.ispublicToString(is_public)
            self.textBrowser.setText(FrontHelper.dictionaryToInfostring(to_pack))

        self.pushButton.clicked.connect(lambda: self.profile_edit())


    def addButton(self):
        account_list = demo.get_account_info(self.customer_id)
        self.btns = []
        print(account_list)
        for i in range(len(account_list)):
            current_account = account_list[i]
            self.btns.append( QtWidgets.QPushButton(self.verticalLayoutWidget))
            self.btns[i].setText("Account ID: " + str(current_account[2]))
            self.verticalLayout.addWidget((self.btns[i]))
            #self.btns[i].clicked.connect(lambda: self.account_Info(self.sender().text()))
            self.btns[i].clicked.connect(lambda: self.account_Info(self.sender().text()))

    def profile_edit(self):
        profile_editWindow.profile_customer_id = self.customer_id
        profile_editWindow.show()

    def account_Info(self, id):
        account_InfoWindow.account_id = int(id.strip("Account ID: "))
        account_InfoWindow.update()
        # print(account_InfoWindow.account_id)
        account_InfoWindow.show()

class profile_editWindow(QWidget, Ui_profile_edit):
    profile_customer_id = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.pushButton.clicked.connect(lambda: self.submit())
        customer_InfoWindow.initUi()

    def submit(self):
        edit_name = self.lineEdit.text()
        edit_gender = FrontHelper.StringToGender(self.comboBox.currentText())
        edit_birthday = self.dateEdit.date().toString("yyyy-MM-dd")
        edit_email = self.lineEdit_4.text()
        edit_msg = self.plainTextEdit.toPlainText()
        edit_is_public = FrontHelper.StringToIsPublic(self.comboBox_2.currentText())
        print(edit_name, edit_gender, edit_birthday, edit_email, edit_msg, edit_is_public)
        demo.update_profile(self.profile_customer_id, edit_name, edit_gender, edit_birthday, edit_email, edit_msg, None,edit_is_public)

        customer_InfoWindow.close()
        customer_InfoWindow.initUi()
        customer_InfoWindow.show()
        profile_editWindow.close()


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
    demo = functions.WeConnect()

    signin_FaceIDWindow = signin_FaceIDWindow()
    signin_PasswordWindow = signin_PasswordWindow()
    signupWindow = signupWindow()
    customer_InfoWindow = customer_InfoWindow()
    profile_editWindow = profile_editWindow()
    account_InfoWindow = account_InfoWindow()

    loginWindow.show()

    sys.exit(app.exec_())