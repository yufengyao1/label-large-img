from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Gradient_form import Ui_GradientDlg
from DefinedUI import ColorBarWidget
from ColorDialog import ColorDialog
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from Label import *
import pickle,copy
class GradientDlg(QDialog,Ui_GradientDlg):
    def __init__(self,parent=None):
        super(GradientDlg,self).__init__()
        self.setupUi(self) 
        self.setWindowFlags(Qt.WindowCloseButtonHint |  Qt.Drawer| Qt.ApplicationModal)
        self.parent=parent
        self.currentColor=Qt.red
        self.resultList=[]#######################渐变结果集 位置-颜色
        self.allGradientList=[]
        self.colorLabel.setScaledContents(True)
        self.gradientLabel.setScaledContents(True)
        self.colorBarWidget=ColorBarWidget(self)
        self.colorBarWidget.setObjectName("colorBarWidget")
        self.colorBarWidget.setMaximumHeight(20)
        self.colorBarWidget.setMinimumHeight(20)
        self.positionEdit.setValidator(QIntValidator(1,100))
        self.verticalLayout.addWidget(self.colorBarWidget)
        self.verticalLayout.setContentsMargins(1,0,1,0)
        self.verticalLayout.setSpacing(0)
        self.colorLabel.installEventFilter(self)
        self.colorBarWidget.drawGradient()
        self.okBtn.clicked.connect(self.accept)
        self.cancelBtn.clicked.connect(self.reject)
        self.createBtn.clicked.connect(self.createClicked)
        self.delBtn.clicked.connect(self.delClicked)
        self.positionEdit.returnPressed.connect(self.moveBar)
        self.delItemBtn.clicked.connect(self.itemDelClicked)
        self.listWidget.setSpacing(0)
        self.listWidget.setIconSize(QSize(33,33))
        self.listWidget.setStyleSheet("QListWidget::Item{margin:0px;border:1px solid rgb(158,158,158);padding-top:-1px;padding-bottom:-1px;border-left:0px;border-top:0px;}")
        
        self.initColorWidgets()#加载预设文件
        self.listWidget.itemClicked.connect(self.itemClick)#事件关联
        self.okBtn.setFocusPolicy(Qt.NoFocus)
        self.cancelBtn.setFocusPolicy(Qt.NoFocus)
        self.delItemBtn.setFocusPolicy(Qt.NoFocus)
        self.createBtn.setFocusPolicy(Qt.NoFocus)
        self.delBtn.setFocusPolicy(Qt.NoFocus)
        self.listWidget.setMovement(QListView.Static)
    def eventFilter(self, source, event):
        if source == self.colorLabel:  
            if event.type() == QEvent.MouseButtonPress:
                 self.setLabelColor()
                 return True
        return QWidget.eventFilter(self, source, event)#事件过滤器
    def createClicked(self):  
        obj=GradientObject()
        obj.gradientlist=copy.deepcopy(self.resultList)
        obj.iscurrent=False
        obj.name=self.lineEdit.text()
        self.allGradientList.append(obj)
        with open("MainUI/gradient.grd","wb")as f:
            pickle.dump(self.allGradientList,f)
        pixmap=QPixmap(32,32)
        painter=QPainter(pixmap);
        painter.setRenderHint(QPainter.HighQualityAntialiasing,True);
        linearGradient=QLinearGradient(0,0,pixmap.width(),pixmap.height())
        for gradient in self.resultList:
            linearGradient.setColorAt(gradient.position,gradient.color)
        painter.setBrush(linearGradient)
        painter.setPen(Qt.transparent);
        painter.drawRect(0,0,pixmap.width(),pixmap.height())
        painter.end()
        pItem=QListWidgetItem(QIcon(pixmap),"",None,0)
        pItem.setSizeHint(QSize(33,33))
        self.listWidget.addItem(pItem)
        return
    def itemClick(self):
        row=self.listWidget.currentRow()
        self.parent.settings.setValue("gradientindex", row)
        self.colorBarWidget.loadGradientObj(self.allGradientList[row])

    def setLabelColor(self):
         dlg=ColorDialog()
         dlg.showDialog()
         color=dlg.selectedColor
         if color==None:
             return
         self.currentColor=color
         pixmap=QPixmap(10,10)
         pixmap.fill(color)
         self.colorLabel.setPixmap(pixmap)
         self.colorLabel.update()
         self.colorBarWidget.changeBarColor(color)
         self.colorBarWidget.drawGradient()
    def delClicked(self):
        self.colorBarWidget.deleteBar()
    def itemDelClicked(self):
        row=self.listWidget.currentRow()
        self.allGradientList.pop(row)
        self.listWidget.takeItem(row)
        with open("MainUI/gradient.grd","wb")as f:
            pickle.dump(self.allGradientList,f)
        #self.colorBarWidget.loadGradientObj(self.allGradientList[row])
    def initColorWidgets(self):
        try:
            with open("MainUI/gradient.grd","rb")as f:
                list = pickle.load(f)
                self.allGradientList=list
        except:
            return
        self.listWidget.clear()
        for obj in list:
            pixmap=QPixmap(32,32)
            painter=QPainter(pixmap);
            painter.setRenderHint(QPainter.HighQualityAntialiasing,True);
            linearGradient=QLinearGradient(0,0,pixmap.width(),pixmap.height())
            for gradient in obj.gradientlist:
                linearGradient.setColorAt(gradient.position,gradient.color)
            painter.setBrush(linearGradient)
            painter.setPen(Qt.transparent);
            painter.drawRect(0,0,pixmap.width(),pixmap.height())
            painter.end()
            pItem=QListWidgetItem(QIcon(pixmap),"",None,0)
            pItem.setSizeHint(QSize(33,33))
            self.listWidget.addItem(pItem)
    def moveBar(self):
        value=self.positionEdit.text()
        if value=="":
            return
        if self.colorBarWidget.currentSelectedIndex<0:
            return
        x=int(value)
        self.colorBarWidget.barList[self.colorBarWidget.currentSelectedIndex].move(x*self.gradientLabel.width()/100+2,0)