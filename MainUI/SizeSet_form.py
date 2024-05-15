# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SizeSet_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SizeSetDlg(object):
    def setupUi(self, SizeSetDlg):
        SizeSetDlg.setObjectName("SizeSetDlg")
        SizeSetDlg.setWindowModality(QtCore.Qt.WindowModal)
        SizeSetDlg.resize(306, 133)
        SizeSetDlg.setStyleSheet("background-color: rgb(96, 96, 96);\n"
"color: rgb(255, 255, 255);")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(SizeSetDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SizeSetDlg)
        self.label.setStyleSheet("font-size:12px;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lineEdit = QtWidgets.QLineEdit(SizeSetDlg)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setMinimumSize(QtCore.QSize(63, 19))
        self.lineEdit.setMaximumSize(QtCore.QSize(63, 19))
        self.lineEdit.setStyleSheet("background-color: rgb(58, 58, 58);\n"
"border:1px solid rgb(41, 41, 41);\n"
"font-size:12px;")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalSlider = QtWidgets.QSlider(SizeSetDlg)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(200)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(SizeSetDlg)
        self.label_2.setStyleSheet("font-size:12px;")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pointEdit = QtWidgets.QLineEdit(SizeSetDlg)
        self.pointEdit.setEnabled(False)
        self.pointEdit.setMinimumSize(QtCore.QSize(63, 19))
        self.pointEdit.setMaximumSize(QtCore.QSize(63, 19))
        self.pointEdit.setStyleSheet("background-color: rgb(58, 58, 58);\n"
"border:1px solid rgb(41, 41, 41);\n"
"font-size:12px;")
        self.pointEdit.setObjectName("pointEdit")
        self.horizontalLayout_2.addWidget(self.pointEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalSlider2 = QtWidgets.QSlider(SizeSetDlg)
        self.horizontalSlider2.setMinimum(1)
        self.horizontalSlider2.setMaximum(200)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName("horizontalSlider2")
        self.verticalLayout.addWidget(self.horizontalSlider2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(SizeSetDlg)
        QtCore.QMetaObject.connectSlotsByName(SizeSetDlg)

    def retranslateUi(self, SizeSetDlg):
        _translate = QtCore.QCoreApplication.translate
        SizeSetDlg.setWindowTitle(_translate("SizeSetDlg", "线条编辑器"))
        self.label.setText(_translate("SizeSetDlg", "线条："))
        self.label_2.setText(_translate("SizeSetDlg", "点："))
