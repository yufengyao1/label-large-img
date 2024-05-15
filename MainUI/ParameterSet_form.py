# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParameterSet_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(365, 364)
        Dialog.setStyleSheet("background-color: rgb(237, 237, 237);")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.lineEdit1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"height:20px;\n"
"color: rgb(0, 0, 0);")
        self.lineEdit1.setObjectName("lineEdit1")
        self.horizontalLayout_7.addWidget(self.lineEdit1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.lineEdit2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"height:20px;\n"
"color: rgb(0, 0, 0);")
        self.lineEdit2.setObjectName("lineEdit2")
        self.horizontalLayout_8.addWidget(self.lineEdit2)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.radioButton1 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton1.setObjectName("radioButton1")
        self.horizontalLayout_3.addWidget(self.radioButton1)
        self.radioButton2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton2.setObjectName("radioButton2")
        self.horizontalLayout_3.addWidget(self.radioButton2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.lineEdit01 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit01.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"height:20px;\n"
"color: rgb(0, 0, 0);")
        self.lineEdit01.setObjectName("lineEdit01")
        self.horizontalLayout_9.addWidget(self.lineEdit01)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.lineEdit02 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit02.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"height:20px;\n"
"color: rgb(0, 0, 0);")
        self.lineEdit02.setObjectName("lineEdit02")
        self.horizontalLayout_10.addWidget(self.lineEdit02)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        spacerItem = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.okBtn = QtWidgets.QPushButton(Dialog)
        self.okBtn.setObjectName("okBtn")
        self.horizontalLayout_4.addWidget(self.okBtn)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_4.addWidget(self.cancelBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "配置"))
        self.groupBox.setTitle(_translate("Dialog", "热图"))
        self.label_6.setText(_translate("Dialog", "网格宽度："))
        self.label_7.setText(_translate("Dialog", "网格高度："))
        self.groupBox_2.setTitle(_translate("Dialog", "缩略图"))
        self.label_3.setText(_translate("Dialog", "模式："))
        self.radioButton1.setText(_translate("Dialog", "原图模式"))
        self.radioButton2.setText(_translate("Dialog", "叠加模式"))
        self.groupBox_3.setTitle(_translate("Dialog", "标记"))
        self.label_8.setText(_translate("Dialog", "网格宽度："))
        self.label_9.setText(_translate("Dialog", "网格高度："))
        self.okBtn.setText(_translate("Dialog", "确定"))
        self.cancelBtn.setText(_translate("Dialog", "取消"))
