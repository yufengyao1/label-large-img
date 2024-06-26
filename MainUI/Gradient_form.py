# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gradient_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GradientDlg(object):
    def setupUi(self, GradientDlg):
        GradientDlg.setObjectName("GradientDlg")
        GradientDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        GradientDlg.resize(475, 431)
        GradientDlg.setMinimumSize(QtCore.QSize(475, 431))
        GradientDlg.setMaximumSize(QtCore.QSize(475, 431))
        GradientDlg.setStyleSheet("background-color: rgb(237, 237, 237);")
        self.gridLayout_4 = QtWidgets.QGridLayout(GradientDlg)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cancelBtn = QtWidgets.QPushButton(GradientDlg)
        self.cancelBtn.setMinimumSize(QtCore.QSize(90, 23))
        self.cancelBtn.setMaximumSize(QtCore.QSize(90, 23))
        self.cancelBtn.setObjectName("cancelBtn")
        self.gridLayout.addWidget(self.cancelBtn, 1, 1, 1, 1)
        self.okBtn = QtWidgets.QPushButton(GradientDlg)
        self.okBtn.setMinimumSize(QtCore.QSize(90, 23))
        self.okBtn.setMaximumSize(QtCore.QSize(90, 23))
        self.okBtn.setObjectName("okBtn")
        self.gridLayout.addWidget(self.okBtn, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(GradientDlg)
        self.groupBox.setStyleSheet("border-color: rgb(158, 158, 158);")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setStyleSheet("border-color: rgb(179, 179, 179);\n"
"background-color: rgb(198, 198, 198);\n"
"")
        self.listWidget.setIconSize(QtCore.QSize(0, 0))
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 4, 1)
        self.delItemBtn = QtWidgets.QPushButton(GradientDlg)
        self.delItemBtn.setObjectName("delItemBtn")
        self.gridLayout.addWidget(self.delItemBtn, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(GradientDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(GradientDlg)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.createBtn = QtWidgets.QPushButton(GradientDlg)
        self.createBtn.setMinimumSize(QtCore.QSize(90, 23))
        self.createBtn.setMaximumSize(QtCore.QSize(90, 23))
        self.createBtn.setObjectName("createBtn")
        self.horizontalLayout.addWidget(self.createBtn)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(GradientDlg)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(420, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gradientLabel = QtWidgets.QLabel(self.groupBox_2)
        self.gradientLabel.setMinimumSize(QtCore.QSize(400, 27))
        self.gradientLabel.setMaximumSize(QtCore.QSize(800, 27))
        self.gradientLabel.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"margin: 0px 6px 0px 6px;\n"
"border:1px solid rgb(158,158,158);\n"
"\n"
"")
        self.gradientLabel.setText("")
        self.gradientLabel.setObjectName("gradientLabel")
        self.verticalLayout.addWidget(self.gradientLabel)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.colorLabel = QtWidgets.QLabel(self.groupBox_3)
        self.colorLabel.setMinimumSize(QtCore.QSize(54, 20))
        self.colorLabel.setMaximumSize(QtCore.QSize(54, 20))
        self.colorLabel.setStyleSheet("border: 1px solid rgb(158, 158, 158);\n"
"border-color: rgb(158, 158, 158);\n"
"background-color: rgb(255, 0, 0);")
        self.colorLabel.setText("")
        self.colorLabel.setObjectName("colorLabel")
        self.horizontalLayout_3.addWidget(self.colorLabel)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.positionEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.positionEdit.setMinimumSize(QtCore.QSize(56, 20))
        self.positionEdit.setMaximumSize(QtCore.QSize(56, 20))
        self.positionEdit.setStyleSheet("border:1px solid rgb(158,158,158);\n"
"background-color: rgb(255, 255, 255);")
        self.positionEdit.setObjectName("positionEdit")
        self.horizontalLayout_3.addWidget(self.positionEdit)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.delBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.delBtn.setMinimumSize(QtCore.QSize(90, 23))
        self.delBtn.setMaximumSize(QtCore.QSize(90, 23))
        self.delBtn.setObjectName("delBtn")
        self.horizontalLayout_3.addWidget(self.delBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.retranslateUi(GradientDlg)
        QtCore.QMetaObject.connectSlotsByName(GradientDlg)

    def retranslateUi(self, GradientDlg):
        _translate = QtCore.QCoreApplication.translate
        GradientDlg.setWindowTitle(_translate("GradientDlg", "渐变编辑器"))
        self.cancelBtn.setText(_translate("GradientDlg", "取消"))
        self.okBtn.setText(_translate("GradientDlg", "确定"))
        self.groupBox.setTitle(_translate("GradientDlg", "预设"))
        self.delItemBtn.setText(_translate("GradientDlg", "移除"))
        self.label.setText(_translate("GradientDlg", "名称(N):"))
        self.createBtn.setText(_translate("GradientDlg", "创建"))
        self.groupBox_2.setTitle(_translate("GradientDlg", "渐变"))
        self.groupBox_3.setTitle(_translate("GradientDlg", "色标"))
        self.label_3.setText(_translate("GradientDlg", "颜色(C):"))
        self.label_5.setText(_translate("GradientDlg", "位置(P):"))
        self.label_6.setText(_translate("GradientDlg", "%"))
        self.delBtn.setText(_translate("GradientDlg", "删除"))
