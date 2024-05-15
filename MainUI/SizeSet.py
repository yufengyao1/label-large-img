
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SizeSet_form import Ui_SizeSetDlg
from DefinedUI import ColorBarWidget
from ColorDialog import ColorDialog
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Label import *
import pickle,copy

class SizeSetDlg(QDialog,Ui_SizeSetDlg):
    def __init__(self,parent=None):
        super(SizeSetDlg,self).__init__(parent)
        self.setupUi(self) 
        self.setWindowFlags(Qt.WindowCloseButtonHint |  Qt.Drawer | Qt.ApplicationModal)
        self.parent=parent
        self.horizontalSlider.valueChanged.connect(self.lineValueChange)
        self.horizontalSlider2.valueChanged.connect(self.pointValueChange)
        #self.horizontalSlider.setValue(2)
        linewidth=self.parent.settings.value("labellinewidth")
        if linewidth==None:
            linewidth=5
        pointwidth=self.parent.settings.value("labelpointwidth")
        if pointwidth==None:
            pointwidth=20
        self.horizontalSlider.setValue(float(linewidth)*2)
        self.horizontalSlider2.setValue(float(pointwidth)*2)


    def lineValueChange(self):
        self.lineEdit.setText(str(self.horizontalSlider.value()/2)+"像素")
        self.parent.sizeEdit.setText(str(int(self.horizontalSlider.value()/2)))
        self.parent.labelLineWidth=float(self.horizontalSlider.value()/2)
        self.parent.imgLabel.repaint()
        self.parent.imgLabelR.repaint()
        self.parent.settings.setValue("labellinewidth", float(self.horizontalSlider.value()/2))
        return
    def pointValueChange(self):
        self.pointEdit.setText(str(int(self.horizontalSlider2.value()/2))+"像素")
        self.parent.labelPointWidth=float(self.horizontalSlider2.value()/2)
        self.parent.imgLabel.repaint()
        self.parent.imgLabelR.repaint()
        self.parent.settings.setValue("labelpointwidth", float(self.horizontalSlider2.value()/2))
        return
    def event(self,event):
        if event.type() == QEvent.ActivationChange:
            if QApplication.activeWindow() != self:
                #self.hide()   
                self.parent.sizeEdit.setStyleSheet("background-image: url(img/sizeeditback2.png);")
                #self.parent.sizeDlgShowed=False
        return QDialog.event(self,event)