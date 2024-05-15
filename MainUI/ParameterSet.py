from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ParameterSet_form import Ui_Dialog
from DefinedUI import ColorBarWidget
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle,copy

class ParameterSetDlg(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super(ParameterSetDlg,self).__init__(parent)
        self.setupUi(self) 
        self.setWindowFlags(Qt.WindowCloseButtonHint |  Qt.Drawer | Qt.ApplicationModal)
        self.parent=parent
        self.okBtn.clicked.connect(self.okclicked)
        self.cancelBtn.clicked.connect(self.cancelclicked)
        self.loadDeaultPar()
        #self.radioButton1.setEnabled(False)
        #self.radioButton2.setEnabled(False)
    def loadDeaultPar(self):
         self.settings=QSettings("MainUI/config.ini", QSettings.IniFormat)
         tmpstr=self.settings.value("gridwidth")
         if tmpstr:
             self.lineEdit1.setText(tmpstr)
         else:
             self.lineEdit1.setText("320")
         tmpstr=self.settings.value("gridheight")
         if tmpstr:
             self.lineEdit2.setText(tmpstr)
         else:
             self.lineEdit2.setText("320")

         tmpstr=self.settings.value("labelgridwidth")
         if tmpstr:
             self.lineEdit01.setText(tmpstr)
         else:
             self.lineEdit01.setText("320")
         tmpstr=self.settings.value("labelgridheight")
         if tmpstr:
             self.lineEdit02.setText(tmpstr)
         else:
             self.lineEdit02.setText("320")

         tmpstr=self.settings.value("thumbmode")
         if tmpstr:
             if tmpstr=="0":
                 self.radioButton1.setChecked(True)
             else:
                 self.radioButton2.setChecked(True)
         else:
             self.radioButton1.setChecked(True)
    def okclicked(self):
        width=self.lineEdit1.text()
        height=self.lineEdit2.text()   
        self.parent.gridwidth=int(width)
        self.parent.gridheight=int(height)

        thumbmode=0
        if self.radioButton2.isChecked():
            thumbmode=1
            if hasattr(self.parent, 'mainImage'):
              self.parent.thumbImage=self.parent.thumbImageColor
              self.parent.initThumbnailLabel()
        else:
            if hasattr(self.parent, 'mainImage'):
              self.parent.thumbImage=self.parent.thumbImageOrigin
              self.parent.initThumbnailLabel()
        
        self.parent.thumbmode=thumbmode
        self.settings.setValue("gridwidth",width)
        self.settings.setValue("gridheight",height)
        self.settings.setValue("thumbmode",thumbmode)

        labelgridwidth=self.lineEdit01.text()
        labelgridheight=self.lineEdit02.text()   
        self.settings.setValue("labelgridwidth",labelgridwidth)
        self.settings.setValue("labelgridheight",labelgridheight)
        self.parent.labelGridWidth=int(labelgridwidth)
        self.parent.labelGridHeight=int(labelgridheight)
        self.close()
        return
    def cancelclicked(self):
        self.close()
        return