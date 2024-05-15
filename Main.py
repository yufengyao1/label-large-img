import sys
sys.path.append('ConcentrationAna')  #专注度分析模块加入环境变量
sys.path.append('MainUI')  #label模块
sys.path.append('yolov5')
import gc
import time
import os
import multiprocessing
import configparser
from MainUI.Main_form import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from MainUI.Helper import Helper
from multiprocessing import Process
from MainUI.DefinedUI import *
import numpy as np
from MainUI.Loading import LoadingDlg
from MainUI.ThreadTools import *
from DeepLearning.DeepMain import *
from DeepLearning.AttentionAna import AttentionAnaWindow
from DeepLearning.ObjectDec import *
from DeepLearning.BehaviorDec import *
from LingoAce.ClassAna import ClassAnaWindow
from LingoAce.VisualEffect import VisualEffectWindow
from LingoAce.VisualEffect2000 import VisualEffectWindow2000
from LingoAce.VisualEffectCam2000 import VisualEffectCamWindow2000
from LingoAce.VisualEffectCam import VisualEffectCamWindow
from LingoAce.GestureRecWindow import GestureRecWindow
from LingoAce.FaceDetect import FaceDetectWindow
from LingoAce.YawnDecWindow import BehaviorDecWindow

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initVariables()
        self.initSetting()
        self.initUI()
        self.initLink()
        self.thumbQueue = multiprocessing.Queue()

    def initSetting(self):
        self.watermarkImg = QImage("img/watermark.png")
        self.settings = QSettings("MainUI/config.ini", QSettings.IniFormat)
        tmpstr = self.settings.value("gridwidth")
        if tmpstr:
            self.gridwidth = int(tmpstr)
        else:
            self.gridwidth = 320
            self.settings.setValue("gridwidth", 320)
        tmpstr = self.settings.value("gridheight")
        if tmpstr:
            self.gridheight = int(tmpstr)
        else:
            self.gridheight = 320
            self.settings.setValue("gridheight", 320)
        tmpstr = self.settings.value("colormode")
        if tmpstr:
            self.colormode = int(tmpstr)
        else:
            self.colormode = 0
            self.settings.setValue("colormode", 0)
        thumbmode = self.settings.value("thumbmode")  # 缩略图模式
        if thumbmode:
            self.thumbmode = int(thumbmode)
        else:
            self.thumbmode = 1
            self.settings.setValue("thumbmode", 1)

        linewidth = self.settings.value("labellinewidth")
        if linewidth == None:
            linewidth = 5
        self.labelLineWidth = float(linewidth)
        pointwidth = self.settings.value("labelpointwidth")
        if pointwidth == None:
            pointwidth = 5
        self.labelPointWidth = float(pointwidth)

        labelgridwidth = self.settings.value("labelgridwidth")
        if labelgridwidth == None:
            labelgridwidth = 320
        self.labelGridWidth = int(labelgridwidth)

        labelgridheight = self.settings.value("labelgridheight")
        if labelgridheight == None:
            labelgridheight = 320
        self.labelGridHeight = int(labelgridheight)

    def initLink(self):
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.initThumbnailLabel)
        self.scrollArea.horizontalScrollBar().valueChanged.connect(self.initThumbnailLabel)

        self.gradientLab.installEventFilter(self)
        self.thumbnailLabel.installEventFilter(self)
        self.sizeEdit.installEventFilter(self)
        self.widgetPics.itemDoubleClicked.connect(
            lambda: Helper.itemDoubleclick(self))  # 事件关联
        self.heatlistWidget.clicked.connect(self.heatlistClick)
        self.labellistWidget.clicked.connect(self.labellistClick)

    def initMenu(self):
        # 菜单栏
        menuBar = self.menuBar()
        # menuBar.setNativeMenuBar(True)
        menuFile = menuBar.addMenu("文件(F)")
        menuFile.addAction("打开图像(O)                ",
                           lambda: self.openImage(""), "Ctrl+O")
        menuFile.addAction("打开文件夹(F)...                 ",
                           lambda: self.openFolder(0), "Ctrl+F")
        menuFile.addAction("添加文件夹(F)...                 ",
                           lambda: self.openFolder(1), "Ctrl+A")
        
        menuFile.addSeparator()
        menuFile.addAction("打开标记文件(J)                 ",
                           lambda: Helper.loadJsonData(self))
        menuFile.addAction("保存标记文件...             ", lambda: Helper.saveLabelData(self))
        menuFile.addAction("保存标记图像...             ",
                           lambda: Helper.exportLabeledImage(self, 1))
        menuFile.addSeparator()
        menuFile.addAction("保存叠加图                  ",
                           lambda: Helper.saveHeatMap(self, 1))
        menuFile.addAction("保存热图...                  ",
                           lambda: Helper.saveHeatMap(self, 2))
        menuFile.addSeparator()
        menuFile.addAction("加载热图数据                  ",
                           lambda: Helper.loadHeatData(self), "Ctrl+H")
        menuFile.addSeparator()
        menuFile.addAction("退出(X)                ",
                           lambda: Helper.exit(self), "Alt+E")
        
        menuHeat = menuBar.addMenu("热图(H)")
        menuHeat.addAction("渐变编辑器                  ",
                           lambda: Helper.showGradientDlg(self))

        menuLabel = menuBar.addMenu("标注(L)")
        self.mMoveAction = QAction("移动             ")
        self.mMoveAction.triggered.connect(lambda: Helper.drawLabel(self, 0))
        # self.mMoveAction.setShortcut("Ctrl+M")
        self.mMoveAction.setCheckable(True)
        self.mMoveAction.setChecked(True)
        menuLabel.addAction(self.mMoveAction)
        self.mPolygonAction = QAction("多边形             ")
        self.mPolygonAction.triggered.connect(
            lambda: Helper.drawLabel(self, 1))
        self.mPolygonAction.setCheckable(True)
        self.mPolygonAction.setChecked(False)
        menuLabel.addAction(self.mPolygonAction)
        self.mRectAction = QAction("矩形             ")
        self.mRectAction.triggered.connect(lambda: Helper.drawLabel(self, 2))
        self.mRectAction.setCheckable(True)
        self.mRectAction.setChecked(False)
        menuLabel.addAction(self.mRectAction)
        self.mCircleAction = QAction("圆形             ")
        self.mCircleAction.triggered.connect(lambda: Helper.drawLabel(self, 3))
        self.mCircleAction.setCheckable(True)
        self.mCircleAction.setChecked(False)
        menuLabel.addAction(self.mCircleAction)
        self.mLineAction = QAction("直线             ")
        self.mLineAction.triggered.connect(lambda: Helper.drawLabel(self, 4))
        self.mLineAction.setCheckable(True)
        self.mLineAction.setChecked(False)
        menuLabel.addAction(self.mLineAction)
        self.mPointAction = QAction("点             ")
        self.mPointAction.triggered.connect(lambda: Helper.drawLabel(self, 5))
        self.mPointAction.setCheckable(True)
        self.mPointAction.setChecked(False)
        menuLabel.addAction(self.mPointAction)
        self.mPolylineAction = QAction("折线            ")
        self.mPolylineAction.triggered.connect(
            lambda: Helper.drawLabel(self, 6))
        self.mPolylineAction.setCheckable(True)
        self.mPolylineAction.setChecked(False)
        menuLabel.addAction(self.mPolylineAction)
        self.mPenAction = QAction("画笔            ")
        self.mPenAction.triggered.connect(lambda: Helper.drawLabel(self, 7))
        self.mPenAction.setCheckable(True)
        self.mPenAction.setChecked(False)
        menuLabel.addAction(self.mPenAction)
        self.mGridPolygonAction = QAction("多网格             ")
        self.mGridPolygonAction.triggered.connect(
            lambda: Helper.drawLabel(self, 6.5))
        self.mGridPolygonAction.setCheckable(True)
        self.mGridPolygonAction.setChecked(False)
        menuLabel.addAction(self.mGridPolygonAction)
        self.mGridPolygonAction.setVisible(False)
        self.mSingleGridAction = QAction("网格             ")
        self.mSingleGridAction.triggered.connect(
            lambda: Helper.drawLabel(self, 6.6))
        self.mSingleGridAction.setCheckable(True)
        self.mSingleGridAction.setChecked(False)
        menuLabel.addAction(self.mSingleGridAction)
        menuLabel.addSeparator()
        menuLabel.addAction("颜色编辑器(C)    ", lambda: Helper.setLabelColor(self))
        menuLabel.addAction("标注线条编辑器(L)    ", lambda: Helper.showSizeDlg(self))

        menuView = menuBar.addMenu("视图(V)")
        self.mV1Action = QAction("原图视图              ")
        self.mV1Action.triggered.connect(lambda: Helper.setViewMode(self, 0))
        self.mV1Action.setCheckable(True)
        self.mV1Action.setChecked(False)
        # self.mV1Action.setShortcut("Ctrl+1")
        menuView.addAction(self.mV1Action)
        self.mV2Action = QAction("叠加视图              ")
        self.mV2Action.triggered.connect(lambda: Helper.setViewMode(self, 1))
        self.mV2Action.setCheckable(True)
        self.mV2Action.setChecked(True)
        # self.mV2Action.setShortcut("Ctrl+2")
        menuView.addAction(self.mV2Action)
        self.mV3Action = QAction("热力视图              ")
        self.mV3Action.triggered.connect(lambda: Helper.setViewMode(self, 3))
        self.mV3Action.setCheckable(True)
        self.mV3Action.setChecked(False)
        # self.mV3Action.setShortcut("Ctrl+3")
        menuView.addAction(self.mV3Action)
        self.mV4Action = QAction("原图热力双视图              ")
        self.mV4Action.triggered.connect(lambda: Helper.setViewMode(self, 2))
        self.mV4Action.setCheckable(True)
        self.mV4Action.setChecked(False)
        # self.mV4Action.setShortcut("Ctrl+4")
        menuView.addAction(self.mV4Action)
        menuView.addSeparator()
        menuView.addAction("放大...                  ", self.zoomIn, "Ctrl+=")
        menuView.addAction("缩小...                  ", self.zoomOut, "Ctrl+-")
        menuView.addAction("区域放大             ",
                           lambda: Helper.drawLabel(self, 8), "Ctrl+E")
        menuView.addAction("自动调整             ",
                           lambda: Helper.autoSize(self), "Ctrl+J")
        menuZoom = menuView.addMenu("倍数缩放")
        menuZoom.addAction("x1倍             ",
                           lambda: Helper.zoomOther(self, "1", True))
        menuZoom.addAction("x2倍             ",
                           lambda: Helper.zoomOther(self, "2", True))
        menuZoom.addAction("x4倍             ",
                           lambda: Helper.zoomOther(self, "4", True))
        menuZoom.addAction("x10倍             ",
                           lambda: Helper.zoomOther(self, "10", True))
        menuZoom.addAction("x20倍             ",
                           lambda: Helper.zoomOther(self, "20", True))
        menuZoom.addAction("x40倍             ",
                           lambda: Helper.zoomOther(self, "40", True))
        menuView.addSeparator()
        self.ruleAction = QAction("标尺(R)              ")
        self.ruleAction.triggered.connect(lambda: Helper.setRulerView(self))
        # self.ruleAction.setShortcut("Ctrl+R")
        self.ruleAction.setCheckable(True)
        self.ruleAction.setChecked(True)
        menuView.addAction(self.ruleAction)
        self.gridAction = QAction("网格(G)              ")
        self.gridAction.triggered.connect(lambda: Helper.setGridView(self))
        # self.gridAction.setShortcut("Ctrl+G")
        self.gridAction.setCheckable(True)
        self.gridAction.setChecked(False)
        menuView.addAction(self.gridAction)

        menuParameterSet = menuBar.addMenu("选项(O)")
        menuParameterSet.addAction(
            "系统参数(P)                    ", lambda: Helper.openParameterSetDlg(self))

        menuDeepL=menuBar.addMenu("视觉分析(D)")
        # menuDeepL.addAction("batch转图片(B)                    ", lambda: BatchHelper.batchToJpg(self))
        # menuDeepL.addAction("测试               ", lambda: BatchHelper.loadDataset(self))
        menuDeepL.addAction("Yolov5目标检测           ", self.openObjectDecWindow)
        menuDeepL.addAction("专注度分析               ", self.openDeepLWindow)
        # menuDeepL.addAction("吸烟检测               ", lambda: self.openBehaviorDeccWindow("smokeana"))
        menuDeepL.addAction("背景检测               ", lambda: self.openBehaviorDeccWindow("backana"))
        menuDeepL.addAction("分辨率检测               ", lambda: self.openBehaviorDeccWindow("resolutionana"))
        menuDeepL.addAction("抖动检测               ", lambda: self.openBehaviorDeccWindow("shakingana"))
        menuDeepL.addAction("打哈欠检测               ", lambda: self.openBehaviorDeccWindow("yawnana"))
        menuDeepL.addAction("低头_侧看_仰躺检测               ", self.openAttentionDecWindow)
        menuDeepL.addAction("黑屏检测               ", lambda: self.openBehaviorDeccWindow("nopersonana"))
        menuDeepL.addAction("画面卡顿检测               ", lambda: self.openBehaviorDeccWindow("stuckana"))
        menuDeepL.addAction("抽烟_喝水_吃东西_户外检测               ", lambda: self.openBehaviorDeccWindow("smoke_drink_eat"))
        menuDeepL.addAction("综合检测               ", lambda: self.openBehaviorDeccWindow("allana"))
        # menuDeepL.addAction("切出系统检测               ", lambda: self.openBehaviorDeccWindow("blackana"))
        menuAIClass=menuBar.addMenu("LingoAce(L)")
        menuAIClass.addAction("AI监课               ", self.openClassAnaWindow)
        menuAIClass.addAction("人脸检测               ", self.openFaceDetectWindow)
        menuAIClass.addAction("虚拟特效(mp4)98点               ", self.openVisualEffectWindow)
        menuAIClass.addAction("虚拟特效(cam)98点               ", self.openVisualEffectCamWindow)
        menuAIClass.addAction("虚拟特效(mp4)2000点               ", self.openVisualEffectWindow2000)
        menuAIClass.addAction("虚拟特效(cam)2000点               ", self.openVisualEffectCamWindow2000)
        menuAIClass.addAction("手势识别(cam)               ", self.openGestureRecWindow)
        menuAIClass.addAction("哈欠识别               ", self.openYawnRecWindow)
        
        menuHelp = menuBar.addMenu("帮助(H)")
        menuHelp.addAction("联机帮助..                         ")
        menuHelp.addAction("支持中心..                         ")
        menuHelp.addAction("法律声明..                         ")
        menuHelp.addSeparator()
        menuHelp.addAction("产品注册..                         ")
        menuHelp.addAction("更新...                         ")

    def initTopToolBar(self):
        # 顶部工具栏
        self.topToolBar = QToolBar()
        self.topToolBar.setObjectName("topToolBar")
        self.addToolBar(Qt.TopToolBarArea, self.topToolBar)
        openFolderTool = QAction(QIcon("img/folderopen.png"), "打开文件夹", self)
        openFolderTool.triggered.connect(lambda: self.openFolder(0))
        self.topToolBar.addAction(openFolderTool)
        addFolderTool = QAction(QIcon("img/addfolder.png"), "添加文件夹", self)
        addFolderTool.triggered.connect(lambda: self.openFolder(1))
        self.topToolBar.addAction(addFolderTool)
        openTool = QAction(QIcon("img/image.png"), "打开文件", self)
        openTool.triggered.connect(lambda: self.openImage(""))
        self.topToolBar.addAction(openTool)
        openHeatTool = QAction(QIcon("img/txt.png"), "加载热图数据", self)
        openHeatTool.triggered.connect(lambda: Helper.loadHeatData(self))
        self.topToolBar.addAction(openHeatTool)
        openJsonTool = QAction(QIcon("img/json.png"), "打开标记文件", self)
        openJsonTool.triggered.connect(lambda: Helper.loadJsonData(self))
        self.topToolBar.addAction(openJsonTool)
        self.topToolBar.addSeparator()

        self.columnLabel = QLabel(" 热图类型: ")
        self.columnLabel.setObjectName("columnLabel")
        self.topToolBar.addWidget(self.columnLabel)

        columnstr = self.settings.value("columnnum")
        if not columnstr:
            columnstr = "3"
        self.heatTypeCombo = QComboBox()
        self.heatTypeCombo.setEditable(True)
        self.heatTypeCombo.addItems(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.heatTypeCombo.setCurrentText(columnstr)
        self.heatTypeCombo.currentTextChanged.connect(
            lambda: Helper.setColumnNum(self))
        self.heatTypeCombo.setFixedWidth(80)
        self.heatTypeCombo.setFixedHeight(20)
        # self.columnEdit=QLineEdit(columnstr)
        # self.columnEdit.setValidator(QIntValidator(1,100))
        # self.columnEdit.returnPressed.connect(lambda:Helper.setColumnNum(self))
        # self.columnEdit.setFixedWidth(45)
        # self.columnEdit.setEnabled(False)
        # self.columnEdit.clearFocus()
        # self.columnEdit.setEnabled(True)
        self.topToolBar.addWidget(self.heatTypeCombo)
        self.topToolBar.addSeparator()

        tmplabel = QLabel(" 缩放: ")
        tmplabel.setObjectName("tmplabel")
        self.topToolBar.addWidget(tmplabel)
        self.scaleCombox = QComboBox()
        self.scaleCombox.setEditable(True)
        self.scaleCombox.addItems(["1", "2", "4", "10", "20", "40"])
        self.scaleCombox.currentTextChanged.connect(
            lambda: Helper.zoomOther(self, self.scaleCombox.currentText(), False))
        self.scaleCombox.setFixedWidth(80)
        self.scaleCombox.setFixedHeight(20)
        self.topToolBar.addWidget(self.scaleCombox)
        self.topToolBar.addSeparator()

        self.viewOriginTool = QAction(QIcon("img/v1.png"), "原图视图", self)
        self.viewOriginTool.triggered.connect(
            lambda: Helper.setViewMode(self, 0))
        self.topToolBar.addAction(self.viewOriginTool)
        self.viewOriginTool.setCheckable(True)

        self.viewStackTool = QAction(QIcon("img/v2.png"), "叠加视图", self)
        self.viewStackTool.triggered.connect(
            lambda: Helper.setViewMode(self, 1))
        self.topToolBar.addAction(self.viewStackTool)
        self.viewStackTool.setCheckable(True)

        self.viewHeatTool = QAction(QIcon("img/v3.png"), "热力视图", self)
        self.viewHeatTool.triggered.connect(
            lambda: Helper.setViewMode(self, 3))
        self.topToolBar.addAction(self.viewHeatTool)
        self.viewHeatTool.setCheckable(True)

        self.viewDoubleTool = QAction(QIcon("img/v4.png"), "双视图", self)
        self.viewDoubleTool.triggered.connect(
            lambda: Helper.setViewMode(self, 2))
        self.topToolBar.addAction(self.viewDoubleTool)
        self.viewDoubleTool.setCheckable(True)
        self.topToolBar.addSeparator()

        self.viewHeatTool.setEnabled(False)
        self.viewDoubleTool.setEnabled(False)
        self.viewStackTool.setEnabled(False)

        self.gridTool = QAction(QIcon("img/grid.png"), "网格", self)
        self.gridTool.triggered.connect(lambda: Helper.setGridView(self))
        self.gridTool.setCheckable(True)
        self.topToolBar.addAction(self.gridTool)

        self.rulerTool = QAction(QIcon("img/ruler.png"), "标尺", self)
        self.rulerTool.triggered.connect(lambda: Helper.setRulerView(self))
        self.rulerTool.setCheckable(True)
        self.rulerTool.setChecked(True)
        self.topToolBar.addAction(self.rulerTool)
        self.topToolBar.addSeparator()

        self.gradientLab = QLabel()
        self.gradientLab.setObjectName("gradientLab")
        self.gradientLab.resize(70, 18)
        self.gradientLab.setScaledContents(True)
        pixmap = QPixmap(70, 18)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        linearGradient = QLinearGradient(0, 10, pixmap.width(), 10)
        linearGradient.setColorAt(0, Qt.yellow)
        linearGradient.setColorAt(1, Qt.red)
        painter.setBrush(linearGradient)
        painter.setPen(Qt.transparent)
        painter.drawRect(0, 0, pixmap.width(), pixmap.height())
        painter.end()
        self.gradientLab.setPixmap(pixmap)
        self.topToolBar.addWidget(self.gradientLab)

        self.sizeEdit = QLineEdit(str(int(self.labelLineWidth)))
        self.sizeEdit.setObjectName("sizeEdit")
        self.sizeEdit.setValidator(QDoubleValidator(0.5, 100, 1))
        self.sizeEdit.returnPressed.connect(lambda: Helper.setColumnNum(self))
        self.sizeEdit.setFixedWidth(54)
        self.sizeEdit.setFixedHeight(24)
        self.sizeEdit.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.sizeEdit.setEnabled(False)
        self.topToolBar.addWidget(self.sizeEdit)

    def initLeftToolBar(self):
        # 左侧工具条
        self.toolBar = QToolBar()
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        self.moveTool = QAction(QIcon("img/hand.png"), "移动", self)
        self.moveTool.triggered.connect(lambda: Helper.drawLabel(self, 0))
        self.toolBar.addAction(self.moveTool)

        self.pointTool = QAction(QIcon("img/point.png"), "点", self)
        self.pointTool.triggered.connect(lambda: Helper.drawLabel(self, 5))
        self.toolBar.addAction(self.pointTool)

        self.lineTool = QAction(QIcon("img/line.png"), "直线", self)
        self.lineTool.triggered.connect(lambda: Helper.drawLabel(self, 4))
        self.toolBar.addAction(self.lineTool)

        self.rectTool = QAction(QIcon("img/rect.png"), "矩形", self)
        self.rectTool.triggered.connect(lambda: Helper.drawLabel(self, 2))
        self.toolBar.addAction(self.rectTool)

        self.circleTool = QAction(QIcon("img/circle.png"), "圆形", self)
        self.circleTool.triggered.connect(lambda: Helper.drawLabel(self, 3))
        self.toolBar.addAction(self.circleTool)

        self.multiLineTool = QAction(QIcon("img/polyline.png"), "折线", self)
        self.multiLineTool.triggered.connect(lambda: Helper.drawLabel(self, 6))
        self.toolBar.addAction(self.multiLineTool)

        self.polygonTool = QAction(QIcon("img/polygon.png"), "多边形", self)
        self.polygonTool.triggered.connect(lambda: Helper.drawLabel(self, 1))
        self.toolBar.addAction(self.polygonTool)

        self.brushTool = QAction(QIcon("img/brush.png"), "画笔", self)
        self.brushTool.triggered.connect(lambda: Helper.drawLabel(self, 7))
        self.toolBar.addAction(self.brushTool)

        self.gridPolygonTool = QAction(QIcon("img/gridlabel.png"), "多网格", self)
        self.gridPolygonTool.triggered.connect(
            lambda: Helper.drawLabel(self, 6.5))
        self.toolBar.addAction(self.gridPolygonTool)
        self.gridPolygonTool.setVisible(False)

        self.singleGridTool = QAction(QIcon("img/gridlabel.png"), "网格", self)
        self.singleGridTool.triggered.connect(
            lambda: Helper.drawLabel(self, 6.6))
        self.toolBar.addAction(self.singleGridTool)

        self.moveTool.setCheckable(True)
        self.polygonTool.setCheckable(True)
        self.rectTool.setCheckable(True)
        self.circleTool.setCheckable(True)
        self.lineTool.setCheckable(True)
        self.pointTool.setCheckable(True)
        self.multiLineTool.setCheckable(True)
        self.brushTool.setCheckable(True)
        self.gridPolygonTool.setCheckable(True)
        self.singleGridTool.setCheckable(True)
        # self.toolBar.addSeparator()
        # self.toolBar.addSeparator()
        self.measureTool = QAction(QIcon("img/measure2.png"), "测量", self)
        self.measureTool.triggered.connect(lambda: Helper.beginMeasure(self))
        self.measureTool.setCheckable(True)
        self.measureTool.setChecked(False)
        self.toolBar.addAction(self.measureTool)
        self.toolBar.addSeparator()

        zoomInTool = QAction(QIcon("img/in.png"), "放大", self)
        zoomInTool.triggered.connect(self.zoomIn)
        self.toolBar.addAction(zoomInTool)
        zoomOutTool = QAction(QIcon("img/out.png"), "缩小", self)
        zoomOutTool.triggered.connect(self.zoomOut)
        self.toolBar.addAction(zoomOutTool)
        self.zoomInRectTool = QAction(QIcon("img/zoom.png"), "区域放大", self)
        self.zoomInRectTool.triggered.connect(
            lambda: Helper.drawLabel(self, 8))
        self.zoomInRectTool.setCheckable(True)
        self.toolBar.addAction(self.zoomInRectTool)
        # zoomOutTool=QAction(QIcon("img/out.png"),"范围缩小",self)
        # zoomOutTool.triggered.connect(self.zoomOut)
        # self.toolBar.addAction(zoomOutTool)
        autoAdjustTool = QAction(QIcon("img/expand.png"), "自动调整图像", self)
        autoAdjustTool.triggered.connect(lambda: Helper.autoSize(self))
        self.toolBar.addAction(autoAdjustTool)
        self.toolBar.addSeparator()

        # gradientTool=QAction(QIcon("img/gradient.png"),"渐变工具(G)",self)
        # gradientTool.triggered.connect(lambda:Helper.autoSize(self))
        # self.toolBar.addAction(gradientTool)

        # 设置标记颜色
        self.currentLabelColor = QColor(85, 0, 0)
        icopixmap = QPixmap(18, 18)
        icopixmap.fill(self.currentLabelColor)
        painter = QPainter(icopixmap)
        painter.setPen(QColor(220, 220, 220))
        painter.drawRect(0, 0, 17, 17)
        painter.end()
        self.colorTool = QAction(QIcon(icopixmap), "标记颜色", self)
        self.colorTool.triggered.connect(lambda: Helper.setLabelColor(self))
        self.toolBar.addAction(self.colorTool)

    def initUI(self):
        self.initMenu()
        self.initTopToolBar()
        self.initLeftToolBar()
        self.setWindowTitle("Label Large Image")
        self.setWindowIcon(QIcon('img/logo.png'))
        # 第一个tab页面板
        self.scrollWidgets = QWidget()
        self.scrollWidgets.setObjectName("scrollWidgets")
        self.scrollArea = MyScrollArea(self)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setCursor(Qt.PointingHandCursor)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        #self.scrollAreaWidgetContents.setStyleSheet("background: rgb(40,40,40)");
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidgetResizable(True)
        self.imgLabel = MyLabel(self)
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setParent(self.scrollAreaWidgetContents)
        self.scrollAreaR = MyScrollArea(self)
        self.scrollAreaR.setObjectName("scrollAreaR")
        self.scrollAreaR.setCursor(Qt.OpenHandCursor)
        self.scrollAreaWidgetRight = QWidget()
        self.scrollAreaWidgetRight.setObjectName("scrollAreaWidgetRight")
        self.scrollAreaR.setWidget(self.scrollAreaWidgetRight)
        self.scrollAreaR.setWidgetResizable(True)
        self.imgLabelR = HeatLabel(self)
        self.imgLabelR.setObjectName("imgLabelR")
        self.imgLabelR.setParent(self.scrollAreaWidgetRight)
        self.leftXLabel = XLabel(self)
        self.leftXLabel.setObjectName("leftXLabel")
        self.leftXLabel.setParent(self.scrollArea)
        self.leftXLabel.resize(2000, 18)
        self.leftXLabel.move(0, 0)
        self.leftXLabel.setVisible(False)
        self.leftYLabel = YLabel(self)
        self.leftYLabel.setObjectName("leftYLabel")
        self.leftYLabel.setParent(self.scrollArea)
        self.leftYLabel.setMinimumWidth(18)
        self.leftYLabel.resize(18, 2000)
        self.leftYLabel.move(0, 0)
        self.leftYLabel.setVisible(False)
        self.rightXLabel = XLabel(self)
        self.rightXLabel.setObjectName("rightXLabel")
        self.rightXLabel.setParent(self.scrollAreaR)
        self.rightXLabel.resize(2000, 18)
        self.rightXLabel.move(0, 0)
        self.rightXLabel.setVisible(False)
        self.rightYLabel = YLabel(self)
        self.rightYLabel.setObjectName("rightYLabel")
        self.rightYLabel.setParent(self.scrollAreaR)
        self.rightYLabel.resize(18, 2000)
        self.rightYLabel.move(0, 0)
        self.rightYLabel.setVisible(False)
        hscrollbox = QHBoxLayout()
        hscrollbox.setContentsMargins(0, 0, 0, 0)
        hscrollbox.setSpacing(1)
        hscrollbox.addWidget(self.scrollArea)
        hscrollbox.addWidget(self.scrollAreaR)
        self.scrollWidgets.setLayout(hscrollbox)

        self.centerWidget = QWidget()  # 中心面板
        self.centerWidget.setObjectName("centerWidget")
        self.stackedWidget = QTabWidget()  # tab面板
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.addTab(
            self.scrollWidgets, "    jpg@ 8.33%(RGB/8#)    ")
        # self.stackedWidget.addTab(self.scrollWidgets,"example_893212-1_10.jpg@ 8.33%(RGB/8#)")
        self.stackedWidget.setCurrentIndex(0)  # 默认显示imgLabel尺寸会自动调整到正确值
        self.stackedWidget.setTabEnabled(0, False)
        # self.stackedWidget.setVisible(False)
        tmplayout = QHBoxLayout()
        tmplayout.setContentsMargins(0, 0, 0, 0)
        tmplayout.setSpacing(1)
        tmplayout.addWidget(self.stackedWidget)
        self.centerWidget.setLayout(tmplayout)
        # self.stackedWidget.setVisible(False)

        # 概率和标记splitter
        vsplitter = QSplitter(Qt.Vertical)
        heatlistW = QWidget()  # 概率列表面板
        labelheatlist = QLabel("概率列表")
        labelheatlist.setObjectName("heatlistLabel")
        labelheatlist.setAlignment(Qt.AlignCenter)
        labelheatlist.setMaximumHeight(20)
        self.heatlistWidget = QListView()
        self.heatlistWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.heatlistWidget.setObjectName("heatlistWidget")
        self.labellistWidget = QListView()
        self.labellistWidget.setContextMenuPolicy(3)
        self.labellistWidget.customContextMenuRequested[QPoint].connect(
            lambda: Helper.listWidgetContext(self, QPoint(0, 0)))
        heatvbox = QVBoxLayout()
        heatvbox.setContentsMargins(0, 0, 0, 0)
        heatvbox.setSpacing(0)
        heatvbox.addWidget(labelheatlist)
        heatvbox.addWidget(self.heatlistWidget)
        heatlistW.setLayout(heatvbox)

        labellistW = QWidget()  # 标记列表面板
        label = QLabel("标记列表")
        label.setObjectName("labellistLabel")
        label.setAlignment(Qt.AlignCenter)
        label.setMaximumHeight(20)
        self.labellistWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.labellistWidget.setObjectName("labellistWidget")
        labelvbox = QVBoxLayout()
        labelvbox.setContentsMargins(0, 0, 0, 0)
        labelvbox.setSpacing(0)
        labelvbox.addWidget(label)
        labelvbox.addWidget(self.labellistWidget)
        labellistW.setLayout(labelvbox)
        vsplitter.addWidget(heatlistW)  # 最右侧分割布局控件
        vsplitter.addWidget(labellistW)
        vsplitter.setHandleWidth(1)

       # 初始化缩略图

        self.thumbnailLabel = QLabel(self.scrollArea)
        self.thumbnailLabel.setObjectName("thumbnailLabel")
        self.thumbnailLabel.setParent(self.scrollArea)
        self.thumbnailLabel.resize(self.thumbsize, self.thumbsize)
        self.thumbnailLabel.move(self.thumbposition)
        self.thumbnailLabel.installEventFilter(self)
        self.thumbnailLabel.raise_()  # 初始化窗口控件
        self.thumbnailLabel.setVisible(False)

        # 初始化度量条

        self.measureLabel = QLabel(self.scrollArea)
        self.measureLabel.setObjectName("measureLabel")
        self.measureLabel.setParent(self.scrollArea)
        self.measureLabel.resize(100, 30)
        self.measureLabel.move(self.measureposition)
        self.measureLabel.raise_()  # 初始化窗口控件
        self.measureLabel.setVisible(True)
        self.measureLabel.setStyleSheet("background-color:transparent")

        self.initMeasureLabel()
        # pixmap=QPixmap(150,20)
        # pixmap.fill(Qt.transparent)
        # painter=QPainter(pixmap)
        #pen=QPen(QColor(255, 0, 0), 2)
        # painter.setPen(pen)
        # painter.drawLine(0,10,150,10)
        # painter.end()
        # self.measureLabel.setPixmap(pixmap)
        # 左侧文件列表
        self.FileListW = QWidget()
        self.widgetPics = QListWidget()  # 图片缩略图面板
        self.widgetPics.setObjectName("widgetPics")
        self.widgetPics.setIconSize(QSize(150, 70))  # 设置显示图片大小
        self.widgetPics.setResizeMode(QListView.Adjust)
        self.widgetPics.setViewMode(QListView.IconMode)  # 设置显示图片模式
        self.widgetPics.setMovement(QListView.Static)  # 设置图片不可移动
        self.widgetPics.setWordWrap(True)
        self.widgetPics.setSpacing(0)
        self.folderlabel = QLabel("文件列表")
        self.folderlabel.setAlignment(Qt.AlignCenter)
        self.folderlabel.setObjectName("folderlabel")
        self.folderlabel.setMaximumHeight(20)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.folderlabel)
        vbox.addWidget(self.widgetPics)
        self.FileListW.setLayout(vbox)
        # self.FileListW.setMaximumWidth(150)
        # self.FileListW.setVisible(False)

        hsplitter = QSplitter(Qt.Horizontal)  # splitter总布局
        hsplitter.setObjectName("hsplitter")
        hsplitter.addWidget(self.FileListW)
        hsplitter.addWidget(self.centerWidget)
        hsplitter.addWidget(vsplitter)
        hsplitter.setStretchFactor(0, 1)
        hsplitter.setStretchFactor(1, 15)
        hsplitter.setStretchFactor(2, 1)
        hsplitter.setHandleWidth(1)

        self.setCentralWidget(hsplitter)

        self.scrollbarX = self.scrollArea.horizontalScrollBar()
        self.scrollbarY = self.scrollArea.verticalScrollBar()
        self.scrollbarXR = self.scrollAreaR.horizontalScrollBar()
        self.scrollbarYR = self.scrollAreaR.verticalScrollBar()
        self.scrollArea.disconnect()
        self.scrollAreaR.setVisible(False)
        self.moveTool.setChecked(True)
        Helper.setDefaultGradient(self)
        Helper.setMouseMoveTrack(self)
        Helper.setViewMode(self, self.viewMode)
        self.setStyleSheet(Helper.readQss("style/MainWindow.qss"))
        self.showMaximized()  # 最大化显示，需要在菜单栏初始化之后使用
    
    def openDeepLWindow(self):#打开专注度分析窗口
        self.deepmain=DeepMainWindow(self)
        self.deepmain.show()
        return  
    def openAttentionDecWindow(self):#打开头部姿势检测窗口
        self.attentionDecWindow=AttentionAnaWindow(self)
        self.attentionDecWindow.show()
        return  
    def openObjectDecWindow(self):#打开目标检测窗体
        self.objdec=ObjectDecWindow(self)
        self.objdec.show()
        return  
    def openBehaviorDeccWindow(self,anatype):
        self.decwindow=BehaviorDecWindow(self,anatype)
        self.decwindow.show()
    def openClassAnaWindow(self):
        self.decwindow=ClassAnaWindow(self)
        self.decwindow.show()
    def openVisualEffectWindow(self): #虚拟特效
        self.visualeffectwindow=VisualEffectWindow(self)
        self.visualeffectwindow.show()
    def openVisualEffectWindow2000(self): #虚拟特效
        self.visualeffectwindow2000=VisualEffectWindow2000(self)
        self.visualeffectwindow2000.show()
    def openVisualEffectCamWindow2000(self):
        self.visualeffectcamwindow2000=VisualEffectCamWindow2000(self)
        self.visualeffectcamwindow2000.show()
    def openVisualEffectCamWindow(self): #虚拟特效-cam
        self.visualeffectcamwindow=VisualEffectCamWindow(self)
        self.visualeffectcamwindow.show()
    def openGestureRecWindow(self): #手势识别
        self.gesturerecwindow=GestureRecWindow(self)
        self.gesturerecwindow.show()
    def openYawnRecWindow(self): #手势识别
        self.yawnrecwindow=BehaviorDecWindow(self,"yawnana")
        self.yawnrecwindow.show()
    def openFaceDetectWindow(self): #虚拟特效
        self.facedetectwindow=FaceDetectWindow(self)
        self.facedetectwindow.show()
    def listWidgetContext(self, point):
        popMenu = QMenu()
        popMenu.addAction("添加")
        popMenu.addAction("修改")
        popMenu.addAction("删除")
        popMenu.exec_(QCursor.pos())

    def initVariables(self):
        self.lastX = 0
        self.lastY = 0
        self.lastXR = 0
        self.lastYR = 0
        self.edgesize = 100  # 定值
        self.edgesizex = self.edgesize  # 当前值
        self.edgesizey = self.edgesize  # 当前值
        self.edgesizexR = self.edgesize  # 当前值
        self.edgesizeyR = self.edgesize  # 当前值
        self.thumbsize = 250
        self.thumbposition = QPoint(21, 21)
        self.measureposition = QPoint(21, 521)  # 单位测量标尺位置
        self.paddingsize = 20
        self.listsize = 200
        self.currentzoomscale = 0
        self.cachePixmap = None
        self.ifcache = False  # 是否缓存当前场景
        self.usecache = False
        self.usecacheR = False
        self.loadimageThread = None
        self.foldericon = QIcon("img/folder.ico")
        self.openfolderlock = False
        self.openimagelock = False
        self.currentImageFile = ""
        self.currentFolder = ""
        self.lock = False
        self.viewMode = 1  # 只显示一张图  0-单张原图 1-单张叠加图 2- 两张图 3-单张热图
        self.rulesize = 18
        self.showruler = True
        self.showgrid = False
        self.listPoint = QPoint(0, 0)
        self.labelList = []
        self.eventType = 0  # 0-平移  1-polygon 2-rect 3-圆形 4-直线 5-点 6-折线
        self.drawLabel = 0  # 0-未在编辑
        self.currentLabel = None  # 当前正在绘制的label
        # self.currentLabelType=0
        self.currentLabelViewPointList = []
        self.currentLabelColor = QColor(0, 0, 255)
        self.tmpMovePoint = QPointF(0, 0)  # 鼠标当前位置点
        self.startMovePoint = QPointF(-1000, -1000)  # 鼠标开始点击位置
        self.endMovePoint = QPointF(-1000, -1000)  # 鼠标开始点击位置
        self.ifDrawRect = False
        self.heatDataColumn = 3
        self.allowScroll = True  # 是否响应鼠标滚动
        self.gradientList = []
        self.isLargeImage = False  # 是否是超大图像
        self.largeScale = 1
        self.sizeDlgShowed = False

        # self.labelLineWidth=5#标记线宽
        # self.labelPointWidth=25#标记点大小
        self.changeFolder = False
        self.isRunning = False
        self.isadddefaultthumb = False  # 正在加载默认图标
        self.gridwidth = 320
        self.gridheight = 320
        self.actualGridwidth = 320
        self.actualGridheight = 320
        self.labelGridWidth = 320
        self.labelGridHeight = 320
        self.colormode = 0
        self.thumbmode = 1  # 缩略图显示模式 0-原图 1-叠加图
        self.currentShapeType = ""
        self.drawTmpPoint = True
        self.heatDataList = []  # 保存热图坐标
        self.heatDataColorList = []  # 保存热图坐标对应的颜色
        self.addedFolders = []  # 控制避免重复添加文件夹
        self.filelist = []  # 文件列表
        self.highlightLabelIndex = -1  # 当前高亮显示的标记
        self.thumImageOrigin = None
        self.thumbImageColor = None
        self.measureList = []  # 测量功能数组
        self.physicalbili = 1
        self.physicalwidth = -1
        self.watermarkImg = None
        self.isdrawing = False  # 正在绘制图形
        self.lastImgSize = None
        self.scaleSize = 20  # 图像默认像素尺寸的放大倍数
        self.lastH = 0

    def openFolder(self, type):
        # type=0 打开文件夹   type=1 追加文件夹
        historyfolder = self.settings.value("folder")
        if historyfolder == None:
            historyfolder = ""
        folder = QFileDialog.getExistingDirectory(self, "打开文件夹", historyfolder)
        if folder == "":
            return
        if self.currentFolder == folder and len(self.addedFolders) == 1:
            return
        if type == 0:
            del self.addedFolders[:]
            self.addedFolders.append(folder)
        else:
            if folder in self.addedFolders:
                return
            else:
                self.addedFolders.append(folder)

        self.currentFolder = folder
        self.settings.setValue("folder", folder)
        try:
            self.addDeaulThumb(folder, type)
            # self.createThumb(folder)
            if hasattr(self, 'createThumbThread'):
                self.createThumbThread.stop()
                while self.isRunning == True:
                    time.sleep(0.001)
                    QApplication.processEvents()
            self.createThumbThread = createThumbThread(self)
            self.createThumbThread.refresh_signal.connect(self.updatePicWidget)
            self.createThumbThread.start()
        except Exception as e:
            print(e)
            return

    def addDeaulThumb(self, folder, type):
      # try:
        self.isadddefaultthumb = True
        self.FileListW.setVisible(True)
        self.FileListW.setMinimumWidth(50)
        self.stackedWidget.setVisible(True)
        if type == 0:
            del self.filelist[:]
            self.filelist = Helper.getFiles(folder)
        else:
            self.filelist.extend(Helper.getFiles(folder))

        self.widgetPics.clear()
        for i in range(len(self.filelist)):  # 设置默认图标
            filestr = self.filelist[i]
            #filename= os.path.basename(os.path.splitext(filestr)[0])
            filename = os.path.basename(filestr)
            if len(filename) > 14:
                filename = filename[:14] + "\n" + filename[14:]
            pItem = QListWidgetItem(self.foldericon, filename, None, 0)
            # pItem.setSizeHint(QSize(140,175))
            pItem.setSizeHint(QSize(110, 110))
            pItem.setTextAlignment(Qt.AlignHCenter)
            self.widgetPics.addItem(pItem)
        tmpfolder = folder
        tmpfolder = tmpfolder[-50:]
        self.folderlabel.setText(tmpfolder)

    def createThumb(self, folder):
      # try:
        QApplication.processEvents()
        self.isRunning = True
        cachelist = Helper.getDatFiles("cache")
        for i in range(len(self.filelist)):
            havecache = False
            tmpfile = self.filelist[i]
            for cache in cachelist:
                if(os.path.basename(os.path.splitext(tmpfile)[0]) == os.path.basename(os.path.splitext(cache)[0])):
                    havecache = True
                    tmppix = QPixmap()
                    file = QFile(cache)
                    file.open(QIODevice.ReadOnly)
                    inn = QDataStream(file)
                    inn >> tmppix
                    file.close()
                    self.widgetPics.item(i).setIcon(QIcon(tmppix))
                    del tmppix
                    gc.collect()
                    break
            if havecache:
                continue
            self.p1 = multiprocessing.Process(
                target=Helper.createThumbnail, args=(self.thumbQueue, self.filelist[i]))
            self.p1.start()
            imgbytes = []
            while True:
                imgbytes = self.thumbQueue.get()
                if imgbytes:
                    break
                time.sleep(0.001)
                QApplication.processEvents()
            buffer = QBuffer()
            buffer.setData(imgbytes)
            buffer.open(QBuffer.ReadOnly)
            inn = QDataStream(buffer)
            image = QPixmap()
            inn >> image

            if(image.width() > 0):
                self.widgetPics.item(i).setIcon(QIcon(image))
            del inn
            del buffer
            del image
            gc.collect()
            QApplication.processEvents()

    def openImage(self, file):
        try:
            historyfile = self.settings.value("openfilefolder")
            if historyfile == None:
                historyfile = ""
            if(file == ""):
                file, filetype = QFileDialog.getOpenFileName(
                    self, "打开文件", historyfile, "JPEG Files (*.jpg);;BMP Files (*.bmp);;PNG Files (*.png)")  # 设置文件扩展名过滤,注意用双分号间隔
                if file == "" or self.currentImageFile == file:
                    return
            self.settings.setValue("openfilefolder", file)
            self.loadProcess = Process(target=Helper.showLoadingDlg)
            self.loadProcess.start()
            if hasattr(self, 'mainImage'):
                self.imgLabel.createcache()
                del self.mainImage
            if hasattr(self, 'heatImage'):
                del self.heatImage
            gc.collect()
            self.widgetPics.blockSignals(True)  # 暂时取消事件绑定 防止多次点击
            Helper.drawLabel(self, 0)
            self.loadImage(file)
        except:
            return

    async def testasync(self):
        self.dlg = LoadingDlg()
        self.dlg.exec()

    def adjustState(self):  # 调整位置
        if self.imgLabel.width() < self.scrollArea.width()-self.rulesize:
            hsize = self.scrollArea.width()-2*self.paddingsize-self.rulesize
            movex = int((self.scrollArea.width() -
                         self.imgLabel.width()+self.rulesize)/2)
            self.edgesizex = movex
        else:
            hsize = self.imgLabel.width()+2*self.edgesize
            movex = self.edgesize
            self.edgesizex = self.edgesize
        if self.imgLabel.height() < self.scrollArea.height()-self.rulesize:
            vsize = self.scrollArea.height()-2*self.paddingsize-self.rulesize
            movey = int((self.scrollArea.height() -
                         self.imgLabel.height()+self.rulesize)/2)
            self.edgesizey = movey
        else:
            vsize = self.imgLabel.height()+2*self.edgesize
            movey = self.edgesize
            self.edgesizey = self.edgesize
        self.scrollAreaWidgetContents.setMinimumSize(hsize, vsize)
        self.imgLabel.move(movex, movey)

    def adjustStateR(self):
        if self.imgLabelR.width() < self.scrollAreaR.width()-self.rulesize:
            hsize = self.scrollAreaR.width()-2*self.paddingsize-self.rulesize
            movex = int((self.scrollAreaR.width() -
                         self.imgLabelR.width()+self.rulesize)/2)
            self.edgesizexR = movex
        else:
            hsize = self.imgLabelR.width()+2*self.edgesize
            movex = self.edgesize
            self.edgesizexR = self.edgesize
        if self.imgLabelR.height() < self.scrollAreaR.height()-self.rulesize:
            vsize = self.scrollAreaR.height()-2*self.paddingsize-self.rulesize
            movey = int((self.scrollAreaR.height() -
                         self.imgLabelR.height()+self.rulesize)/2)
            self.edgesizeyR = movey
        else:
            vsize = self.imgLabelR.height()+2*self.edgesize
            movey = self.edgesize
            self.edgesizeyR = self.edgesize
        self.scrollAreaWidgetRight.setMinimumSize(hsize, vsize)
        self.imgLabelR.move(movex, movey)

    def initThumbnailLabel(self):
        try:
            if hasattr(self, 'mainImage') == False:
                return
            self.tempPix = self.thumbImage.copy()
            self.thumbnailLabel.setAlignment(QtCore.Qt.AlignCenter)

            x = (self.scrollArea.width()/2 -
                 self.scrollAreaWidgetContents.x()-self.edgesizex)
            y = (self.scrollArea.height()/2 -
                 self.scrollAreaWidgetContents.y()-self.edgesizey)
            xdouble = self.tempPix.width()*x/self.imgLabel.width()
            ydouble = self.tempPix.height()*y/self.imgLabel.height()
            x = int(self.tempPix.width()*x/self.imgLabel.width())
            y = int(self.tempPix.height()*y/self.imgLabel.height())
            self.thumbpoint = QPointF(xdouble, ydouble)
            painter = QPainter(self.tempPix)
            pen = QPen(QColor(255, 0, 0), 1)
            painter.setPen(pen)
            painter.drawLine(QPoint(x, 0), QPoint(x, self.tempPix.height()))
            painter.drawLine(QPoint(0, y), QPoint(self.tempPix.width(), y))
            rect = Helper.getViewRect(self)
            painter.fillRect(rect, QColor(255, 255, 255, 100))
            painter.drawRect(rect)
            painter.end()
            self.thumbnailLabel.setPixmap(self.tempPix)
            self.thumbnailLabel.resize(
                self.tempPix.width(), self.tempPix.height())  # 缩略图
            if self.viewMode == 2:
                self.movetoPositionR(self.thumbpoint)  # 右边图像跟随左边滚动条移动
        except Exception as e:
            print(e)

    def initMeasureLabel(self):
        if self.physicalwidth == -1:
            self.measureLabel.setVisible(False)
        else:
            self.measureLabel.setVisible(True)
        if hasattr(self, 'mainImage') == False:
            return
        width = self.physicalwidth
        pixmap = QPixmap(150, 30)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setFont(QFont("微软雅黑", 8.5))
        pen = QPen(QColor(0, 0, 0), 2)
        painter.setPen(pen)
        basex = 5
        basey = 28
        baseh = 5
        rulelength = 70
        reallength = rulelength*width/self.imgLabel.width()  # 当前50像素对应的真实像素尺寸
        painter.drawLine(basex, basey, basex+rulelength, basey)
        painter.drawLine(basex, basey, basex, basey-baseh)
        painter.drawLine(basex+rulelength, basey,
                         basex+rulelength, basey-baseh)
        fm = painter.fontMetrics()
        txtw = fm.width(str(round(reallength, 2))+"μm")
        tmpx = (rulelength-txtw)/2
        painter.drawText(basex+tmpx+1, basey-8, str(round(reallength, 2))+"μm")
        painter.end()
        self.measureLabel.setPixmap(pixmap)

    def zoomIn(self):
        try:
            tmpw = self.imgLabel.width()+self.imgLabel.width() / 3
            if tmpw/self.mainImage.width() > 100:
                return
            self.imgLabel.resize(int(self.imgLabel.width(
            )+self.imgLabel.width() / 3), int(self.imgLabel.height()+self.imgLabel.height() / 3))
            self.imgLabelR.resize(self.imgLabel.width(),
                                  self.imgLabel.height())
            self.adjustState()
            self.movetoPosition(self.thumbpoint)
            Helper.setTabName(self, self.currentImageFile, True)
            if self.viewMode == 2:
                self.adjustStateR()
                self.movetoPositionR(self.thumbpoint)
            self.initMeasureLabel()
        except:
            return

    def zoomOut(self):
        try:
            if(self.imgLabel.width() < 50):
                return
            self.imgLabel.resize(int(self.imgLabel.width(
            )-self.imgLabel.width() / 4), int(self.imgLabel.height()-self.imgLabel.height() / 4))
            self.imgLabelR.resize(self.imgLabel.width(),
                                  self.imgLabel.height())
            self.adjustState()
            self.movetoPosition(self.thumbpoint)
            Helper.setTabName(self, self.currentImageFile, True)
            if self.viewMode == 2:
                self.adjustStateR()
                self.movetoPositionR(self.thumbpoint)
            self.initMeasureLabel()
        except:
            return

    def zoomOther(self, valuestr, settab):
        try:
            if not hasattr(self, 'mainImage'):
                return
            if valuestr == "":
                return
            value = float(valuestr)
            if value <= 0:
                return
            self.imgLabel.resize(
                int(self.mainImage.width()*value), int(self.mainImage.height()*value))
            self.adjustState()
            self.imgLabelR.resize(self.imgLabel.width(),
                                  self.imgLabel.height())
            self.adjustStateR()
            self.movetoPosition(self.thumbpoint)
            Helper.setTabName(self, self.currentImageFile, settab)
        except:
            return

    def heatlistClick(self, qModelIndex):
        list_num = qModelIndex.row()  # 这个值就是所选的列表值
        x = self.heatList[list_num, 0]
        y = self.heatList[list_num, 1]
        realx = x*320+160
        realy = y*320+160
        bilix = float(self.imgLabel.width())*realx/self.mainImage.width()
        biliy = float(self.imgLabel.height())*realy/self.mainImage.height()
        # self.movetoPosition(QPoint(x,y))

        realx = int(bilix+self.edgesizex -
                    (self.scrollArea.width()-16)/2)+18-self.rulesize
        realy = int(biliy+self.edgesizey -
                    (self.scrollArea.height()-16)/2)+18-self.rulesize

        self.scrollArea.horizontalScrollBar().setValue(realx)
        self.scrollArea.verticalScrollBar().setValue(realy)
    # 标记列表点击事件

    def labellistClick(self, qModelIndex):
        list_num = qModelIndex.row()  # 这个值就是所选的列表值
        self.highlightLabelIndex = list_num
        lab = self.labelList[list_num]
        points = lab.pointList
        maxx = 0
        minx = 100000000
        maxy = 0
        miny = 10000000
        for p in points:
            tmpx = QPointF(p).x()
            tmpy = QPointF(p).y()
            if tmpx < minx:
                minx = tmpx
            if tmpx > maxx:
                maxx = tmpx
            if tmpy < miny:
                miny = tmpy
            if tmpy > maxy:
                maxy = tmpy
        realx = (minx+maxx)/2
        realy = (miny+maxy)/2
        bilix = float(self.imgLabel.width())*realx/self.mainImage.width()
        biliy = float(self.imgLabel.height())*realy/self.mainImage.height()
        realx = int(bilix+self.edgesizex -
                    (self.scrollArea.width()-16)/2)+18-self.rulesize
        realy = int(biliy+self.edgesizey -
                    (self.scrollArea.height()-16)/2)+18-self.rulesize
        self.scrollArea.horizontalScrollBar().setValue(realx)
        self.scrollArea.verticalScrollBar().setValue(realy)
        self.imgLabel.repaint()
        self.imgLabelR.repaint()

    def cv_imread(self, file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
        return cv_img

    def test(self):
        return

    def followScroll(self):
        self.scrollbarX.setValue(self.scrollbarXR.value())
        self.scrollbarY.setValue(self.scrollbarYR.value())

    def movetoPosition(self, pos):
        x = pos.x()
        y = pos.y()
        realx = int(x*self.imgLabel.width()/self.thumbnailLabel.width() +
                    self.edgesizex-self.scrollArea.width()/2)
        realy = int(y*self.imgLabel.height()/self.thumbnailLabel.height() +
                    self.edgesizey-self.scrollArea.height()/2)
        self.scrollArea.horizontalScrollBar().setValue(realx)
        self.scrollArea.verticalScrollBar().setValue(realy)
        return  # 缩略图点击定位

    def movetoPositionR(self, pos):
        x = pos.x()
        y = pos.y()
        realx = int(x*self.imgLabelR.width()/self.thumbnailLabel.width() +
                    self.edgesizexR-self.scrollAreaR.width()/2)
        realy = int(y*self.imgLabelR.height()/self.thumbnailLabel.height() +
                    self.edgesizeyR-self.scrollAreaR.height()/2)
        self.scrollAreaR.horizontalScrollBar().setValue(realx)
        self.scrollAreaR.verticalScrollBar().setValue(realy)
        return  # 缩略图点击定位

    def eventFilter(self, source, event):
        if source == self.gradientLab:  # 渐变编辑
            if event.type() == QEvent.MouseButtonPress:
                Helper.showGradientDlg(self)
                return QWidget.eventFilter(self, source, event)
            else:
                # return true无法显示背景图片
                return QWidget.eventFilter(self, source, event)
        elif source == self.sizeEdit:
            if event.type() == QEvent.MouseButtonPress:
                Helper.showSizeDlg(self)
                return QWidget.eventFilter(self, source, event)
            else:
                # return true无法显示背景图片
                return QWidget.eventFilter(self, source, event)
        if hasattr(self, 'mainImage') == False:
            return QWidget.eventFilter(self, source, event)  # 事件过滤器
        if source == self.thumbnailLabel:  # 缩略图点击
            if event.type() == QEvent.MouseButtonPress:
                pos = event.pos()
                self.movetoPosition(pos)
                self.movetoPositionR(pos)
                return QWidget.eventFilter(self, source, event)  # 事件过滤器
        return QWidget.eventFilter(self, source, event)  # 事件过滤器

    def resizeEvent(self, a0):
        if hasattr(self, 'thumbpoint') == False:
            return
        # if self.lastH==0:
        #    self.lastH=self.height()
        #    return
        # bili=self.height()/self.lastH
        # self.imgLabel.resize(int(self.imgLabel.width()*bili),int(self.imgLabel.height()*bili))
        # self.imgLabelR.resize(self.imgLabel.width(),self.imgLabel.height())
        self.adjustState()
        self.adjustStateR()
        self.movetoPosition(self.thumbpoint)
        # self.lastH=self.height()
        return super().resizeEvent(a0)

    def slot_appendPix(self, pixmap, i, lastone, filename):
        self.pics.append(pixmap)
        self.picspath.append(filename)
        if lastone == True:
            # self.loadDlg.close()
            self.widgetPics.clear()
            for pic in self.pics:
                pItem = QListWidgetItem(QIcon(pic), os.path.basename(
                    os.path.splitext(self.picspath[i])[0]), None, 0)
                self.widgetPics.addItem(pItem)
            self.stackedWidget.setCurrentIndex(1)

    def updatePicWidget(self, image, index):
        self.widgetPics.item(index).setIcon(QIcon(image))
        self.widgetPics.update()

    def loadImage(self, file):  # 加载图像
        self.isLargeImage = False
        self.largeScale = 1
        self.physicalwidth = -1  # 物理宽度um
        pixmap = QPixmap(file)
        if pixmap.width() == 0:
            reader = QImageReader(file)
            size = reader.size()
            for i in range(1, 100):
                if size.width()/i < 20000 and size.height()/i < 20000:
                    self.largeScale = i
                    break
            reader.setScaledSize(
                QSize(int(size.width()/self.largeScale), int(size.height()/self.largeScale)))
            image = QImage()
            reader.read(image)
            pixmap = QPixmap(image)
            self.isLargeImage = True
            self.largeScale = 2

        self.stackedWidget.setVisible(True)
        self.widgetPics.blockSignals(False)  # 恢复点击事件绑定
        if pixmap == None or pixmap.width() == 0:
            self.loadProcess.terminate()
            return
        Helper.clearLabelWidget(self)  # 清空标记列表
        self.mainImage = pixmap
        self.lastImgSize = self.mainImage.size()
        self.usecache = False
        #self.thumbImage = self.mainImage.scaled(QSize(self.thumbsize, self.thumbsize), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation);
        self.thumbImageOrigin = self.mainImage.scaled(QSize(
            self.thumbsize, self.thumbsize), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.thumbImage = self.thumbImageOrigin
        self.locked = False  # 解锁内存
        self.currentImageFile = file
        file = self.currentImageFile
        self.scaleSize = 20  # 重置缩放倍数
        scanfile = os.path.dirname(
            file)+"/"+"Scan_" + os.path.basename(os.path.splitext(file)[0])+".txt"
        if os.path.exists(scanfile):
            config = configparser.ConfigParser(allow_no_value=True)  # 类实例化
            config.read(scanfile)
            value = config.get("General", "Size")
            value = value.replace("mm", "")
            value = value.split('x')
            width = float(value[0])*1000
            self.physicalwidth = width
            hasquality = config.has_option("General", "Quantity")
            if hasquality:
                self.scaleSize = int(config.get("General", "Quantity"))
        Helper.setTabName(self, file, True)
        Helper.autoSize(self)
        if self.showruler:
            self.leftXLabel.setVisible(True)
            self.leftYLabel.setVisible(True)
            self.rightXLabel.setVisible(True)
            self.rightYLabel.setVisible(True)
        if hasattr(self, 'cachePixmap'):
            del self.cachePixmap
        # 加载热图
        heatfile = os.path.dirname(
            file)+"/" + os.path.basename(os.path.splitext(file)[0])+".txt"
        if not os.path.exists(heatfile):
            slm = QStringListModel()
            self.heatlistWidget.setModel(slm)
            self.loadProcess.terminate()
            Helper.setViewMode(self, 0)
            self.viewHeatTool.setEnabled(False)
            self.viewDoubleTool.setEnabled(False)
            self.viewStackTool.setEnabled(False)
            self.mV2Action.setEnabled(False)
            self.mV3Action.setEnabled(False)
            self.mV4Action.setEnabled(False)
        else:
            self.viewHeatTool.setEnabled(True)
            self.viewDoubleTool.setEnabled(True)
            self.viewStackTool.setEnabled(True)
            self.mV2Action.setEnabled(True)
            self.mV3Action.setEnabled(True)
            self.mV4Action.setEnabled(True)
            Helper.loadHeatMap(self, file, heatfile)
            self.loadProcess.terminate()
            self.imgLabelR.resize(self.imgLabel.width(),
                                  self.imgLabel.height())
            self.adjustStateR()
        self.stackedWidget.setVisible(True)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.setTabEnabled(0, True)
        self.scrollAreaWidgetContents.setStyleSheet(
            "background: rgb(247,247,247)")
        self.scrollAreaWidgetRight.setStyleSheet(
            "background: rgb(247,247,247)")
        # QApplication.processEvents()
        Helper.autoSize(self)
        self.initMeasureLabel()


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())
