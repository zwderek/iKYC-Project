# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profile_edit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_profile_edit(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(852, 827)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(60, 30, 731, 741))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(0, 50, 731, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(0, 250, 731, 41))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 20, 151, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(0, 120, 151, 31))
        self.label_2.setObjectName("label_2")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(270, 150, 461, 41))
        self.dateEdit.setObjectName("dateEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(270, 120, 171, 31))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(0, 150, 241, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(0, 220, 181, 31))
        self.label_4.setObjectName("label_4")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 350, 731, 181))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(0, 320, 281, 31))
        self.label_5.setObjectName("label_5")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(0, 590, 141, 41))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(0, 560, 401, 31))
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(0, 680, 731, 51))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "Gender"))
        self.label_3.setText(_translate("Form", "Birthday"))
        self.comboBox.setItemText(0, _translate("Form", "Male"))
        self.comboBox.setItemText(1, _translate("Form", "Female"))
        self.comboBox.setItemText(2, _translate("Form", "Others"))
        self.label_4.setText(_translate("Form", "Email"))
        self.label_5.setText(_translate("Form", "Welcome message"))
        self.comboBox_2.setItemText(0, _translate("Form", "Public"))
        self.comboBox_2.setItemText(1, _translate("Form", "Private"))
        self.label_6.setText(_translate("Form", "Do you want to set this to be public?"))
        self.pushButton.setText(_translate("Form", "Submit"))
