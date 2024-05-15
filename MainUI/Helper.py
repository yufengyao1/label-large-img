import sys,gc,time,os,json,pickle,base64,io,configparser,re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import urllib
from PIL import Image
import numpy as np
from Label import Label
from Label_form import LabelDlg
from ColorDialog import ColorDialog
from Loading import LoadingDlg
from Gradient import GradientDlg
from SizeSet import SizeSetDlg
from multiprocessing import Process
from operator import itemgetter
from ParameterSet import ParameterSetDlg
import math
from io import BytesIO
class Helper(object):
    finished = False  
    @staticmethod
    def getFiles2(f):
        list = []
        fs = os.listdir(f)
        for f1 in fs:
            houzhui = os.path.splitext(f1)[1].upper()
            if houzhui != ".JPG" and houzhui != ".TIFF":
                continue
            tmp_path = os.path.join(f, f1)
            if not os.path.isdir(tmp_path):
                list.append(tmp_path)
        return list
    def getFiles(dir):
        files_ = []
        list = os.listdir(dir)
        for i in range(0, len(list)):
            path = os.path.join(dir, list[i])
            if os.path.isdir(path):
                files_.extend(Helper.getFiles(path))
            if os.path.isfile(path):
                houzhui = os.path.splitext(path)[1].upper()
                if houzhui != ".PNG" and houzhui != ".JPG" and houzhui != ".TIFF" and houzhui!=".JSON":
                    continue
                files_.append(path)
        files_.sort()
        return files_
    def getVideoFiles(dir):
        files_ = []
        list = os.listdir(dir)
        for i in range(0, len(list)):
            path = os.path.join(dir, list[i])
            if os.path.isdir(path):
                files_.extend(Helper.getFiles(path))
            if os.path.isfile(path):
                houzhui = os.path.splitext(path)[1].upper()
                if houzhui != ".MP4":
                    continue
                files_.append(path)
        files_.sort()
        return files_
    def getDatFiles(f):
        list = []
        fs = os.listdir(f)
        for f1 in fs:
            houzhui = os.path.splitext(f1)[1].upper()
            if houzhui != ".DAT" :
                continue
            tmp_path = os.path.join(f, f1)
            if not os.path.isdir(tmp_path):
                list.append(tmp_path)
        return list
    def openFolder(folder): 
         app = QApplication(sys.argv)
         files = Helper.getFiles(folder)
         qsharedmemory = QSharedMemory("test")
         pp = qsharedmemory.attach()

         buffer = QBuffer()
         buffer.open(QBuffer.ReadWrite)
         out = QDataStream(buffer)
         sizestr = ""
         for file in files:
             tmpImage = QPixmap(file)
             tmpPix = tmpImage.scaled(QSize(200, 200),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)  
             out << tmpPix
             #filename =os.path.basename(os.path.splitext(file)[0])
             filename = file
             out << QByteArray(bytes(filename,encoding="utf-8"))
             #sizestr=sizestr+str(buffer.size())+","
             del tmpImage
             del tmpPix
             gc.collect()
         #print(str(buffer.size()))
         #qsharedmemory.create(buffer.size(),QSharedMemory.ReadWrite)
         qsharedmemory.data()[:buffer.size()] = buffer.data()[:buffer.size()]

         Helper.setMemoryState(str(len(files)))
    def createThumbnail2(file):
         app = QApplication(sys.argv)
         qsharedmemory = QSharedMemory("test")
         qsharedmemory.attach()
         buffer = QBuffer()
         buffer.open(QBuffer.ReadWrite)
         out = QDataStream(buffer)
         tmpImage = QPixmap(file)
         if tmpImage.width() == 0:   
             Helper.setMemoryState("1")
             app.exit()
             return
         
         tmpPix = tmpImage.scaled(QSize(104, 105),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)  
         bottommap = QPixmap(128,128)
         bottommap.fill(Qt.transparent)
         painter = QPainter(bottommap)
         painter.setRenderHint(QPainter.Antialiasing)
         painter.setRenderHint(QPainter.SmoothPixmapTransform)
         painter.drawPixmap(12,13,tmpPix)
         painter.end()
         out << bottommap

         filename = os.path.basename(os.path.splitext(file)[0])
         #url= urllib.parse(filename)
         #保存到缓存文件夹中
         file = QFile("cache/" + filename + ".dat")
         file.open(QIODevice.WriteOnly)
         out = QDataStream(file)
         out << bottommap


         del tmpImage
         del tmpPix
         del bottommap
         gc.collect()  
         qsharedmemory.data()[:buffer.size()] = buffer.data()[:buffer.size()]
         Helper.setMemoryState("1")
         app.exit()
    def createThumbnail(q,file):
       try:
         app = QApplication(sys.argv)
         image=QPixmap()
         if file[-4:].upper()=="JSON":
           with open(file) as f:
             jsonlab = json.load(f)
             obj=Helper.obj_dic(jsonlab)#将dict字符串转换成对象
             base64str=obj.imageData
             image.loadFromData(base64.b64decode(base64str))
             image = image.scaled(QSize(104,105),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
             #Helper.loadJsonPixmap(self,image,file)
         else:
             reader = QImageReader(file)
             reader.setScaledSize(QSize(104,105))
             image = QImage()
             reader.read(image)
         tmpPix = QPixmap(image)
         if tmpPix.width() == 0: 
             list = []
             q.put(list)
             app.exit()
             return
         #tmpPix = tmpImage.scaled(QSize(104,
         #105),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
         bottommap = QPixmap(128,128)
         bottommap.fill(Qt.transparent)
         painter = QPainter(bottommap)
         painter.setRenderHint(QPainter.Antialiasing)
         painter.setRenderHint(QPainter.SmoothPixmapTransform)
         painter.drawPixmap(12,13,tmpPix)
         painter.end()

         #保存到缓存文件夹中
         filename = os.path.basename(os.path.splitext(file)[0])
         file = QFile("cache/" + filename + ".dat")
         file.open(QIODevice.WriteOnly)
         out = QDataStream(file)
         out << bottommap
         file.close()  

         buffer = QBuffer()
         buffer.open(QBuffer.WriteOnly)
         out2 = QDataStream(buffer)
         out2 << bottommap
         q.put(buffer.data())
         buffer.close() 
        
         del tmpPix
         del bottommap
         gc.collect()  
         app.exit()
       except Exception as e:
           print(e)
    def openImage(file): 
         app = QApplication(sys.argv)
         qsharedmemory = QSharedMemory("test")
         pp = qsharedmemory.attach()
         buffer = QBuffer()
         buffer.open(QBuffer.ReadWrite)
         out = QDataStream(buffer)
         tmpImage = QPixmap(file)
         buffer.write(tmpImage)
         out << tmpImage
         qsharedmemory.data()[:buffer.size()] = buffer.data()[:buffer.size()]
         Helper.setMemoryState("1")
    def setMemoryState(valuestr):
         memory_state = QSharedMemory("state")
         p = memory_state.attach()
         b = QBuffer()
         b.open(QBuffer.ReadWrite)
         out = QDataStream(b)
         out << QByteArray(bytes(valuestr,encoding="utf-8"))
         memory_state.data()[0:b.size()] = b.data()[0:b.size()] 
    def readMemoryState(self):
        b = QBuffer()
        b.setData(self.memory_state.data())
        b.open(QBuffer.ReadWrite)
        tmpinn = QDataStream(b)
        statearray = QByteArray()
        tmpinn >> statearray
        return str(bytes(statearray.data()),encoding="utf-8")
    def setMemoryState_Main(self,valuestr):
         self.memory_state = QSharedMemory("state")
         self.memory_state.create(1000,QSharedMemory.ReadWrite)
         b = QBuffer()
         b.open(QBuffer.ReadWrite)
         out = QDataStream(b)
         out << QByteArray(bytes("-1",encoding="utf-8"))
         self.memory_state.create(b.size())
         aaa = b.data()[0:b.size()] 
         bbb = self.memory_state.data()
         if not bbb:
            return
         self.memory_state.data()[0:b.size()] = b.data()[0:b.size()] 
         b.close()
    def itemDoubleclick(self):
         a = self.widgetPics.currentRow()
         filename=self.filelist[a]
         if(self.currentImageFile == filename):
             return
         if filename[-4:].upper()!="JSON":
             self.openImage(self.filelist[a])
         else:
             Helper.loadJsonDataWithFile(self,filename) 
    def setPage(self,page):
         self.stackedWidget.setCurrentIndex(page)
         return
    def exit(self):
         self.close()
         return
    def waitForState(self):
        while(True):
             #if self.isadddefaultthumb==True:
             #    return 0
             value = Helper.readMemoryState(self)
             if value == "":
                 return 0
             state = int(Helper.readMemoryState(self))
             if state == 1:
                 return 1
             elif state == 0:
                 return 0
             time.sleep(0.001)
             QApplication.processEvents()
        return 1
    def waitForOpenimgLock(self):
        while(self.openimagelock):
             #time.sleep(0.05)
             QApplication.processEvents()
    def waitForOpendlgLock(self):
        while(self.openfolderlock):
             #print("folserlock: "+str(self.openfolderlock))
             #time.sleep(0.05)
             QApplication.processEvents()
    def setTabName(self,file,settab):
         w = self.imgLabel.width()
         scale = w *self.scaleSize/ self.mainImage.width()
         self.scaleCombox.currentTextChanged.disconnect()
         if settab:
            self.scaleCombox.setCurrentText(str(round(scale,2)))
         self.scaleCombox.currentTextChanged.connect(lambda:Helper.zoomOther(self,self.scaleCombox.currentText(),False))
         scalestr = str(round(scale,2))
         self.currentzoomscale = w / self.mainImage.width()
         #self.stackedWidget.setTabText(0,os.path.basename(file) + "@ " + scalestr + "%(RGB/8#)")
         self.stackedWidget.setTabText(0,os.path.basename(file) + "@ " + self.scaleCombox.currentText() + "X(RGB/8#)")
    def getHeatPoints(self,file,column):
         Image.MAX_IMAGE_PIXELS = None
         im = Image.open(file)
         width,height = im.size
         count = 0
         patchsize = 320
         for left in range(0,int(width * 1.0 / patchsize) - 1):
             for top in range(0,int(height * 1.0 / patchsize) - 1):
                 img = im.crop((left * patchsize,top * patchsize,(left + 1) * patchsize,(top + 1) * patchsize))
                 okimg = np.array(img)
                 okimg = okimg[:,:,0]
                 okimg[okimg < 220] = 1
                 okimg[okimg >= 220] = 0
                 if np.sum(okimg) * 1.0 / patchsize / patchsize > 0.3:

                     count = count + 1         
         return
    def loadHeatMap1(self,file,heatfile):#渐变热图
     try:
         ############################################读取txt
         txtfile = QFile(heatfile)
         txtfile.open(QIODevice.ReadOnly or QIODevice.Text)
         inn = QTextStream(txtfile)
         valuelist = []
         xlist = []
         ylist = []
         column = self.heatDataColumn
         while (not inn.atEnd()):
             line = inn.readLine()
             valuelist.append(float(line.split(" ")[column]))

         Image.MAX_IMAGE_PIXELS = None
         im = Image.open(file)
         width,height = im.size
         count = 0
         patchwidth = self.gridwidth
         patchheight = self.gridheight
         #patchsize=320
         validsize = 0.3 * patchwidth * patchheight
         for left in range(0,int(width * 1.0 / patchwidth) - 1):
             for top in range(0,int(height * 1.0 / patchheight) - 1):
                 img = im.crop((left * patchwidth,top * patchheight,(left + 1) * patchwidth,(top + 1) * patchheight))
                 okimg = np.array(img)
                 okimg = okimg[:,:,0]
                 okimg[okimg < 220] = 1
                 okimg[okimg >= 220] = 0
                 if np.sum(okimg) > validsize:
                     count = count + 1       
                     xlist.append(left)
                     ylist.append(top)
         del im
         gc.collect()

         if len(xlist) != len(valuelist):#热力数据不相符
             self.loadProcess.terminate()
             QMessageBox.information(self,"提示","热图数据不符")
             return
         if self.isLargeImage == True:
            patchwidth = int(patchwidth / 2)
            patchheight = int(patchheight / 2)

         self.heatImage = QPixmap(int(width / patchwidth) + 1,int(height / patchheight) + 1)
         self.heatImage.fill(QColor(239,241,238))
         painter = QPainter(self.heatImage)  
         for i in range(len(xlist)):
             value = float(valuelist[i])
             color = Helper.getGradientColor(self,value)
             pen = QPen(color, 1)
             painter.setPen(pen)
             painter.drawPoint(int(xlist[i]),int(ylist[i]))
         painter.end()
         self.heatImage = self.heatImage.scaled(width - width % patchwidth + patchwidth,height - height % patchheight + patchheight, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)

     
         self.heatList = np.c_[xlist,ylist,valuelist]
         self.heatList = self.heatList[np.argsort(self.heatList[:,2])]
         self.heatList = self.heatList[::-1]

         ItemModel = QStandardItemModel()
         pixmap = QPixmap(2000,2)
         pixmap.fill(QColor(40,40,40))
         painter = QPainter(pixmap)
         for i in range(len(xlist)):
            item = QStandardItem("    " + str(i + 1).rjust(3,'0') + " - " + str(self.heatList[i,2])[0:7].ljust(7,'0'))
            color = Helper.getGradientColor(self,float(self.heatList[i,2]))
            painter.fillRect(QRect(0,0,3,2),color)   
            item.setBackground(QBrush(pixmap))
            ItemModel.appendRow(item)
         painter.end()
         self.heatlistWidget.setModel(ItemModel)
         self.viewHeatTool.setEnabled(True)
         self.viewDoubleTool.setEnabled(True)
         self.viewStackTool.setEnabled(True)
         self.mV2Action.setEnabled(True)
         self.mV3Action.setEnabled(True)
         self.mV4Action.setEnabled(True)

         self.loadProcess.terminate()
     except:
         self.loadProcess.terminate()
         QMessageBox.information(self,"提示","热图数据不符")
         return
     return
    def loadHeatMap(self,file,heatfile):#非渐变热图
     try:
         ############################################读取txt
         txtfile = QFile(heatfile)
         txtfile.open(QIODevice.ReadOnly or QIODevice.Text)
         inn = QTextStream(txtfile)
         valuelist = []
         xlist = []
         ylist = []
         column = self.heatDataColumn
         while (not inn.atEnd()):
             line = inn.readLine()
             valuelist.append(float(line.split(" ")[column]))
         Image.MAX_IMAGE_PIXELS = None
         im = Image.open(file)
         width,height = im.size
         count = 0
         patchwidth = self.gridwidth
         patchheight = self.gridheight
         validsize = 0.3 * patchwidth * patchheight
         self.heatDataList.clear()
         for left in range(0,int(width * 1.0 / patchwidth) - 1):
             for top in range(0,int(height * 1.0 / patchheight) - 1):
                 img = im.crop((left * patchwidth,top * patchheight,(left + 1) * patchwidth,(top + 1) * patchheight))
                 okimg = np.array(img)
                 okimg = okimg[:,:,0]
                 okimg[okimg < 220] = 1
                 okimg[okimg >= 220] = 0
                 if np.sum(okimg) > validsize:
                     count = count + 1       
                     xlist.append(left)
                     ylist.append(top)
                     self.heatDataList.append(QPoint(left,top))#热图坐标添加到全局数组
         del im
         if len(xlist) != len(valuelist):#热力数据不相符
             self.loadProcess.terminate()
             QMessageBox.information(self,"提示","热图数据不符")
             return
         if self.isLargeImage == True:
            patchwidth = int(patchwidth / self.largeScale)
            patchheight = int(patchheight / self.largeScale)
            self.actualGridwidth=self.gridwidth/self.largeScale
            self.actualGridheight=self.gridheight/self.largeScale

         self.heatImage = QPixmap(1,1)
         self.heatDataColorList=[]
         gc.collect()
         for i in range(len(xlist)):
             value = float(valuelist[i])
             color = Helper.getGradientColor(self,value)
             self.heatDataColorList.append(color)
         self.heatList = np.c_[xlist,ylist,valuelist]
         self.heatList = self.heatList[np.argsort(self.heatList[:,2])]
         self.heatList = self.heatList[::-1]

         ItemModel = QStandardItemModel()
         pixmap = QPixmap(2000,2)
         pixmap.fill(QColor(40,40,40))
         painter = QPainter(pixmap)
         for i in range(len(xlist)):
            item = QStandardItem("    " + str(i + 1).rjust(3,'0') + " - " + str(self.heatList[i,2])[0:7].ljust(7,'0'))
            color = Helper.getGradientColor(self,float(self.heatList[i,2]))
            painter.fillRect(QRect(0,0,3,2),color)   
            item.setBackground(QBrush(pixmap))
            ItemModel.appendRow(item)
         painter.end()
         self.heatlistWidget.setModel(ItemModel)
         self.viewHeatTool.setEnabled(True)
         self.viewDoubleTool.setEnabled(True)
         self.viewStackTool.setEnabled(True)
         self.mV2Action.setEnabled(True)
         self.mV3Action.setEnabled(True)
         self.mV4Action.setEnabled(True)
         if self.thumbmode==1:#显示叠加缩略图
             tmpImage=QPixmap(self.mainImage)
             painter=QPainter(tmpImage)
             Helper.drawHeatMap(self,painter)
             painter.end()
             self.thumbImageColor=tmpImage.scaled(QSize(self.thumbsize, self.thumbsize), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation);
             self.thumbImage = self.thumbImageColor;
             
             del tmpImage
         gc.collect()
         self.loadProcess.terminate()
     except Exception as e:
         print(e)
         self.loadProcess.terminate()
         QMessageBox.information(self,"提示","热图数据不符")
         return
     return
    def loadJsonHeatMap(self,file,heatfile):#非渐变热图
     try:
         ############################################读取txt
         txtfile = QFile(heatfile)
         txtfile.open(QIODevice.ReadOnly or QIODevice.Text)
         inn = QTextStream(txtfile)
         valuelist = []
         xlist = []
         ylist = []
         column = self.heatDataColumn
         while (not inn.atEnd()):
             line = inn.readLine()
             valuelist.append(float(line.split(" ")[column]))
         
         Image.MAX_IMAGE_PIXELS = None
         im=None
         with open(file) as f:
             jsonstr = json.load(f)
             obj=Helper.obj_dic(jsonstr)#将dict字符串转换成对象
             base64str=obj.imageData
             img_b64decode = base64.b64decode(base64str)  # base64解码
             fp = io.BytesIO(img_b64decode)
             im = Image.open(fp)
         width,height = im.size
         count = 0
         patchwidth = self.gridwidth
         patchheight = self.gridheight
         validsize = 0.3 * patchwidth * patchheight
         self.heatDataList.clear()
         for left in range(0,int(width * 1.0 / patchwidth) - 1):
             for top in range(0,int(height * 1.0 / patchheight) - 1):
                 img = im.crop((left * patchwidth,top * patchheight,(left + 1) * patchwidth,(top + 1) * patchheight))
                 okimg = np.array(img)
                 okimg = okimg[:,:,0]
                 okimg[okimg < 220] = 1
                 okimg[okimg >= 220] = 0
                 if np.sum(okimg) > validsize:
                     count = count + 1       
                     xlist.append(left)
                     ylist.append(top)
                     self.heatDataList.append(QPoint(left,top))#热图坐标添加到全局数组
         del im
         gc.collect()

         if len(xlist) != len(valuelist):#热力数据不相符
             self.loadProcess.terminate()
             QMessageBox.information(self,"提示","热图数据不符")
             return
         if self.isLargeImage == True:
            patchwidth = int(patchwidth / self.largeScale)
            patchheight = int(patchheight / self.largeScale)
            self.actualGridwidth=self.gridwidth/self.largeScale
            self.actualGridheight=self.gridheight/self.largeScale

         self.heatImage = QPixmap(1,1)
         self.heatDataColorList.clear()
         for i in range(len(xlist)):
             value = float(valuelist[i])
             color = Helper.getGradientColor(self,value)
             self.heatDataColorList.append(color)

         self.heatList = np.c_[xlist,ylist,valuelist]
         self.heatList = self.heatList[np.argsort(self.heatList[:,2])]
         self.heatList = self.heatList[::-1]

         ItemModel = QStandardItemModel()
         pixmap = QPixmap(2000,2)
         pixmap.fill(QColor(40,40,40))
         painter = QPainter(pixmap)
         for i in range(len(xlist)):
            item = QStandardItem("    " + str(i + 1).rjust(3,'0') + " - " + str(self.heatList[i,2])[0:7].ljust(7,'0'))
            color = Helper.getGradientColor(self,float(self.heatList[i,2]))
            painter.fillRect(QRect(0,0,3,2),color)   
            item.setBackground(QBrush(pixmap))
            ItemModel.appendRow(item)
         painter.end()
         self.heatlistWidget.setModel(ItemModel)
         self.viewHeatTool.setEnabled(True)
         self.viewDoubleTool.setEnabled(True)
         self.viewStackTool.setEnabled(True)
         self.mV2Action.setEnabled(True)
         self.mV3Action.setEnabled(True)
         self.mV4Action.setEnabled(True)
         if self.thumbmode==1:#显示叠加缩略图
             tmpImage=QPixmap(self.mainImage)
             painter=QPainter(tmpImage)
             Helper.drawHeatMap(self,painter)
             painter.end()
             self.thumbImage = tmpImage.scaled(QSize(self.thumbsize, self.thumbsize), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation);
             del tmpImage
         gc.collect()
         self.loadProcess.terminate()
     except Exception as e:
         print(e)
         self.loadProcess.terminate()
         QMessageBox.information(self,"提示","热图数据不符")
         return
     return
    def drawHeatMap(self,painter):
        painter.setCompositionMode(QPainter.CompositionMode_Overlay)
        for i,point in enumerate(self.heatDataList):
            realx=point.x()*self.gridwidth
            realy=point.y()*self.gridheight
            endx=realx+self.actualGridwidth
            endy=realy+self.actualGridheight
            painter.fillRect(realx,realy,endx-realx,endy-realy,self.heatDataColorList[i])
        return;
    def loadHeatData(self):
        heatfile, filetype = QFileDialog.getOpenFileName(self,"打开热图数据","","All Files (*);;TXT Files (*.txt)")  #设置文件扩展名过滤,注意用双分号间隔
        if heatfile == "":
            return
        self.loadProcess = Process(target=Helper.showReloadingHeatMapDlg)
        self.loadProcess.start()
        Helper.loadHeatMap(self,self.currentImageFile,heatfile)     
    def setViewMode(self,mode):
        self.viewMode = mode
        if mode == 0:
            self.viewOriginTool.setChecked(True)
            self.viewStackTool.setChecked(False)
            self.viewHeatTool.setChecked(False)
            self.viewDoubleTool.setChecked(False)

            self.mV1Action.setChecked(True)
            self.mV2Action.setChecked(False)
            self.mV3Action.setChecked(False)
            self.mV4Action.setChecked(False)
        elif mode == 1:
            self.viewOriginTool.setChecked(False)
            self.viewStackTool.setChecked(True)
            self.viewHeatTool.setChecked(False)
            self.viewDoubleTool.setChecked(False)

            self.mV1Action.setChecked(False)
            self.mV2Action.setChecked(True)
            self.mV3Action.setChecked(False)
            self.mV4Action.setChecked(False)
        elif mode == 2:
            self.viewOriginTool.setChecked(False)
            self.viewStackTool.setChecked(False)
            self.viewHeatTool.setChecked(False)
            self.viewDoubleTool.setChecked(True)

            self.mV1Action.setChecked(False)
            self.mV2Action.setChecked(False)
            self.mV3Action.setChecked(False)
            self.mV4Action.setChecked(True)
        elif mode == 3:
            self.viewOriginTool.setChecked(False)
            self.viewStackTool.setChecked(False)
            self.viewHeatTool.setChecked(True)
            self.viewDoubleTool.setChecked(False)

            self.mV1Action.setChecked(False)
            self.mV2Action.setChecked(False)
            self.mV3Action.setChecked(True)
            self.mV4Action.setChecked(False)
        if not hasattr(self, 'mainImage'):
            return
        if(mode == 0 or mode == 1 or mode == 3):
             try:
                 self.scrollAreaR.verticalScrollBar().valueChanged.disconnect(self.followScroll)
                 self.scrollAreaR.horizontalScrollBar().valueChanged.disconnect(self.followScroll)
             except:
                 self.imgLabel.repaint()
                 self.imgLabelR.repaint()
             finally:
                 self.scrollAreaR.setVisible(False)
                 self.imgLabel.repaint()
                 self.imgLabelR.repaint()
        else:
             self.scrollAreaR.verticalScrollBar().valueChanged.connect(self.followScroll)
             self.scrollAreaR.horizontalScrollBar().valueChanged.connect(self.followScroll)
             self.scrollAreaR.setVisible(True)
             self.imgLabelR.resize(self.imgLabel.width(),self.imgLabel.height())
             self.adjustStateR()
             self.movetoPositionR(self.thumbpoint)
             self.adjustState()#scroll尺寸改变之后需要重新计算图像位置
             self.imgLabel.repaint()
             self.imgLabelR.repaint()
        
        self.imgLabel.repaint()
        self.imgLabelR.repaint()
             
    def followScroll(self):
        self.scrollbarX.setValue(self.scrollbarXR.value())
        self.scrollbarY.setValue(self.scrollbarYR.value())

    def setRulerView(self):
        if self.showruler:
            self.showruler = False
            self.rulesize = 0
            self.leftXLabel.setVisible(False)
            self.leftYLabel.setVisible(False)
            self.rightXLabel.setVisible(False)
            self.rightYLabel.setVisible(False)
            self.rulerTool.setChecked(False)
            self.ruleAction.setChecked(False)
        else:
            self.showruler = True
            self.rulesize = 18
            self.leftXLabel.setVisible(True)
            self.leftYLabel.setVisible(True)
            self.rightXLabel.setVisible(True)
            self.rightYLabel.setVisible(True)
            self.rulerTool.setChecked(True)
            self.ruleAction.setChecked(True)

    def setGridView(self):
        if self.showgrid:
            self.showgrid = False
            self.gridTool.setChecked(False)
            self.gridAction.setChecked(False)
            self.imgLabel.repaint()
            self.imgLabelR.repaint()
        else:
            self.showgrid = True
            self.gridTool.setChecked(True)
            self.gridAction.setChecked(True)
            self.imgLabel.repaint()
            self.imgLabelR.repaint()
    def getViewRect(self):
        piw = self.imgLabel.width()
        pih = self.imgLabel.height()
        psw = self.scrollArea.width()
        psh = self.scrollArea.height()
        viewx = self.scrollbarX.value() - self.imgLabel.x()
        if viewx < 0:
            vieww = psw + viewx
            viewx = 0              
        else:
            vieww = psw

        viewy = self.scrollbarY.value() - self.imgLabel.y()
        if viewy < 0:
            viewh = psh + viewy
            viewy = 0
        else:
            viewh = psh

        if psw - (piw - viewx) > 0:
            vieww = piw - viewx
        if psh - (pih - viewy) > 0:
            viewh = pih - viewy

        if(pih < psh):
            viewh = pih
        if(piw < psw):
            vieww = piw
        thumbRectX = int(self.thumbnailLabel.width() * viewx / self.imgLabel.width())
        thumbRectY = int(self.thumbnailLabel.height() * viewy / self.imgLabel.height())
        thumbRectW = int(self.thumbnailLabel.width() * vieww / self.imgLabel.width())
        thumbRectH = int(self.thumbnailLabel.height() * viewh / self.imgLabel.height())
        return QRect(thumbRectX,thumbRectY,thumbRectW,thumbRectH)
    def zoomOther(self,valuestr,settab):
     if not hasattr(self, 'mainImage'):
         return
     if valuestr == "":
         return
     value = float(valuestr)
     if value <= 0:
         return
     self.imgLabel.resize(int(self.mainImage.width() * value/self.scaleSize),int(self.mainImage.height() * value/self.scaleSize))
     self.adjustState() 
     self.imgLabelR.resize(self.imgLabel.width(),self.imgLabel.height())
     self.adjustStateR()
     self.movetoPosition(self.thumbpoint)
     Helper.setTabName(self,self.currentImageFile,settab)
    def drawLabel(self,type):
        if self.isdrawing==True:
            if type==0:
                self.moveTool.setChecked(self.eventType==0)
            elif type==1:
                self.polygonTool.setChecked(self.eventType==1)
            elif type==2:
                self.rectTool.setChecked(self.eventType==2)
            elif type==3:
                self.circleTool.setChecked(self.eventType==3)
            elif type==4:
                self.lineTool.setChecked(self.eventType==4)
            elif type==5:
                self.pointTool.setChecked(self.eventType==5)
            elif type==6:
                self.multiLineTool.setChecked(self.eventType==6)
            elif type==7:
                self.brushTool.setChecked(self.eventType==7)
            elif type==8:
                self.zoomInRectTool.setChecked(self.eventType==8)
            elif type==6.5:
                self.gridPolygonTool.setChecked(self.eventType==6.5)
            elif type==6.6:
                self.singleGridTool.setChecked(self.eventType==6.5)
            elif type==9:
                self.measureTool.setChecked(self.eventType==9)
            return
        self.eventType = type
        if type == 0:
            self.scrollArea.setCursor(Qt.PointingHandCursor)
            self.scrollAreaR.setCursor(Qt.PointingHandCursor)
        else:
            self.scrollArea.setCursor(Qt.ArrowCursor)
            self.scrollAreaR.setCursor(Qt.ArrowCursor)
        self.imgLabel.repaint()
        self.imgLabelR.repaint()

        if type == 0:
            self.moveTool.setChecked(True)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.singleGridTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(True)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)
            self.mGridPolygonAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
            return
        elif type == 1:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(True)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(True)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 2:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(True)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(True)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 3:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(True)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(True)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 4:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(True)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(True)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 5:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(True)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(True)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 6:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(True)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(True)
            self.mPenAction.setChecked(False)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 7:
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(True)
            self.gridPolygonTool.setChecked(False)
            self.measureTool.setChecked(False)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(True)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 8: #矩形放大
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.zoomInRectTool.setChecked(True)
            self.singleGridTool.setChecked(False)
            self.measureTool.setChecked(False)
        elif type == 6.5: #网格
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.gridPolygonTool.setChecked(True)
            self.measureTool.setChecked(False)

            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)
            self.mGridPolygonAction.setChecked(True)

            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
        elif type == 6.6: #单网格
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.singleGridTool.setChecked(True)
            self.measureTool.setChecked(False)

            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)
            self.mGridPolygonAction.setChecked(False)
            self.mSingleGridAction.setChecked(True)
        elif type==9:#测量
            self.moveTool.setChecked(False)
            self.polygonTool.setChecked(False)
            self.rectTool.setChecked(False)
            self.circleTool.setChecked(False)
            self.lineTool.setChecked(False)
            self.pointTool.setChecked(False)
            self.multiLineTool.setChecked(False)
            self.zoomInRectTool.setChecked(False)
            self.brushTool.setChecked(False)
            self.gridPolygonTool.setChecked(False)
            self.singleGridTool.setChecked(False)
            self.measureTool.setChecked(True)

            self.mGridPolygonAction.setChecked(False)
            self.mMoveAction.setChecked(False)
            self.mPolygonAction.setChecked(False)
            self.mRectAction.setChecked(False)
            self.mCircleAction.setChecked(False)
            self.mLineAction.setChecked(False)
            self.mPointAction.setChecked(False)
            self.mPolylineAction.setChecked(False)
            self.mPenAction.setChecked(False)
            self.mGridPolygonAction.setChecked(False)
            self.singleGridTool.setChecked(False)
            self.mSingleGridAction.setChecked(False)
            
        if type > 0 and type < 8:
            if len(self.labelList) > 0:
                self.labelList.pop()
            lab = Label()
            lab.labelColor = self.currentLabelColor
            lab.shapeType = Helper.getShapeType(type)
            self.currentShapeType = Helper.getShapeType(type)
            lab.pointList = []
            lab.labelType = type
            self.labelList.append(lab)
        return
    def getShapeType(type):
        if type == 1:
            shapetype = "polygon"
        elif type == 2:
            shapetype = "rectangle"
        elif type == 3:
            shapetype = "circle"
        elif type == 4:
            shapetype = "line"
        elif type == 5:
            shapetype = "point"
        elif type == 6:
            shapetype = "linestrip"
        elif type==6.5:#grid
            shapetype="polygon"
        elif type==6.6:#grid
            shapetype="polygon"
        elif type == 7:
            shapetype = "polygon"
        return shapetype
    def handlerMove(self,source,event):
               if event.type() == QEvent.MouseMove and event.buttons() == QtCore.Qt.LeftButton:
                 if self.lastY == 0:
                    self.lastY = event.pos().y()
                 if self.lastX == 0:
                    self.lastX = event.pos().x()     
                 distanceX = self.lastX - event.pos().x()
                 distanceY = self.lastY - event.pos().y()
                 self.lastX = event.pos().x()
                 self.lastY = event.pos().y()  
                 if(self.viewMode == 2):   
                    self.scrollbarXR.setValue(self.scrollbarXR.value() + distanceX)
                    self.scrollbarYR.setValue(self.scrollbarYR.value() + distanceY)
                 else:
                    self.scrollbarX.setValue(self.scrollbarX.value() + distanceX)
                    self.scrollbarY.setValue(self.scrollbarY.value() + distanceY)
                 self.thumbnailLabel.move(self.thumbposition)
                 return True
               elif event.type() == QEvent.MouseButtonRelease:
                  self.lastY = 0
                  self.lastX = 0          
                  return True
               elif event.type() == QEvent.Resize:
                   self.adjustState()
                   if hasattr(self, 'thumbpoint'):
                     self.movetoPosition(self.thumbpoint)
                   self.imgLabelR.resize(self.imgLabel.width(),self.imgLabel.height())
    def handlerDraw(self,source,event):
        x = event.pos().x() - self.imgLabel.x() 
        y = event.pos().y() - self.imgLabel.y()
        x = event.pos().x() - self.imgLabel.x() + self.scrollbarX.value()
        y = event.pos().y() - self.imgLabel.y() + self.scrollbarY.value()
        realx = self.mainImage.width() * x / self.imgLabel.width()
        realy = self.mainImage.height() * y / self.imgLabel.height()
        self.labelList[-1].pointList.append(QPointF(realx,realy))
        self.labelList[-1].labelColor = self.currentLabelColor
        self.imgLabel.repaint()
        self.imgLabelR.repaint()
        if (self.eventType == 2 or self.eventType == 3 or self.eventType == 4) and len(self.labelList[-1].pointList) == 2:#矩形、圆限定两个点
            Helper.showLabelDlg(self)
            return True
        if self.eventType == 5 and len(self.labelList[-1].pointList) == 1:#点
            Helper.showLabelDlg(self)
            return True
        return True
    def handlerMouseHover(self,source,event):
        x = event.pos().x() - self.imgLabel.x() 
        y = event.pos().y() - self.imgLabel.y()
        x = event.pos().x() - self.imgLabel.x() + self.scrollbarX.value()
        y = event.pos().y() - self.imgLabel.y() + self.scrollbarY.value()
        realx = self.mainImage.width() * x / self.imgLabel.width()
        realy = self.mainImage.height() * y / self.imgLabel.height()
        self.tmpMovePoint = QPointF(realx,realy)
        if self.eventType != 0:
            self.imgLabel.repaint()
            self.imgLabelR.repaint()
    def showLabelDlg(self):
        dlg = LabelDlg()
        labelnames = []
        for label in self.labelList:
            if not label.labelName in labelnames:
                dlg.labelNameEdit.addItem(label.labelName)
                labelnames.append(label.labelName)
        dlg.labelNameEdit.setCurrentText("")
        result = dlg.exec_()
        if result == 1:
            labelname = dlg.labelNameEdit.currentText()
            labeldes = dlg.labelDesEdit.toPlainText()
            self.labelList[-1].labelName = labelname
            self.labelList[-1].labelDes = labeldes

            lab = Label()
            lab.pointList = []
            lab.labelColor = self.currentLabelColor
            lab.labelType = self.eventType
            lab.shapeType = self.currentShapeType

            self.labelList.append(lab)

            ItemModel = QStandardItemModel()
            for label in self.labelList[0:-1]:
                labelname = label.labelName
                item = QStandardItem(labelname)
                item.setCheckable(True)
                item.setBackground(QBrush(QColor(label.labelColor)))
                ItemModel.appendRow(item)
            self.labellistWidget.setModel(ItemModel)
        else:
            self.labelList.pop()
            lab = Label()
            lab.pointList = []
            lab.labelColor = self.currentLabelColor
            lab.labelType = self.eventType
            self.labelList.append(lab)
        return True
    def clearLabelWidget(self):#清空标记列表
        self.labelList.clear()
        ItemModel = QStandardItemModel()
        self.labellistWidget.setModel(ItemModel)

    def showLoadingDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.show()
        app.exec_()
    def showLoadingJsonDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.label.setText("加载标记文件")
        dlg.show()
        app.exec_()

    def showGradientDlg(self):
        dlg = GradientDlg(self)
        result = dlg.exec_()
        #print(result)
        if result == 1:
            self.gradientList = dlg.resultList
            pixmap = QPixmap(70,18)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing,True)
            linearGradient = QLinearGradient(0,10,pixmap.width(),10)
            for gradient in self.gradientList:
                linearGradient.setColorAt(gradient.position,gradient.color)
            painter.setBrush(linearGradient)
            painter.setPen(Qt.transparent)
            painter.drawRect(0,0,pixmap.width(),pixmap.height())
            painter.end()
            self.gradientLab.setPixmap(pixmap)
            self.gradientList = sorted(self.gradientList, key=lambda k: k.position) 
            #QApplication.processEvents()

            if not hasattr(self, 'mainImage'):
                return
            loadProcess = Process(target=Helper.showReloadingHeatMapDlg)
            loadProcess.start()
            try:
                file = self.currentImageFile
                heatfile = os.path.dirname(file) + "/" + os.path.basename(os.path.splitext(file)[0]) + ".txt"
                Helper.loadHeatMap(self,file,heatfile)
                self.imgLabel.repaint()
                self.imgLabelR.repaint()
                
            finally:
                loadProcess.terminate()

            return
    def showSizeDlg(self):
        if not hasattr(self, 'dlg') :
            self.sizeEdit.setStyleSheet("background-image: url(img/sizeeditback.png);")
            self.dlg = SizeSetDlg(self)
            self.dlg.show()   
        else:
            if self.dlg.isVisible() == True:
                self.sizeEdit.setStyleSheet("background-image: url(img/sizeeditback2.png);")
                self.dlg.hide()
            else:
                self.sizeEdit.setStyleSheet("background-image: url(img/sizeeditback.png);")
                self.dlg.show()    
        
    def showReloadingHeatMapDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.label.setText("加载热图数据")
        dlg.show()
        app.exec_()
    def showExportImageDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.label.setText("保存标记图像")
        dlg.show()
        app.exec_()
    def showExportLabelDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.label.setText("保存标记文件")
        dlg.show()
        app.exec_()
    def showExportBothImageDlg():
        app = QApplication(sys.argv)
        dlg = LoadingDlg()
        dlg.label.setText("保存图像")
        dlg.show()
        app.exec_()
    def setLabelColor(self):
         dlg = ColorDialog()
         dlg.showDialog()
         color = dlg.selectedColor
         if color == None:
             return
         self.currentLabelColor = color
         if self.eventType != 0:
             self.labelList[-1].labelColor = color
         icopixmap = QPixmap(18,18)
         icopixmap.fill(color)
         painter = QPainter(icopixmap)
         painter.setPen(QColor(220,220,220))
         painter.drawRect(0,0,17,17)
         painter.end()
         self.colorTool.setIcon(QIcon(icopixmap))
    def readQss(style):
        f = open(style,'r')
        filecontent = f.read()
        f.close()
        return filecontent
    def autoSize(self):#自动计算尺寸
       try:
         if not hasattr(self, 'mainImage'):
             return
         if self.mainImage.width() > self.mainImage.height():
             w = int(self.scrollArea.width() - 2 * self.paddingsize - self.rulesize)
             h = int(w * self.mainImage.height() / self.mainImage.width())
         else:
             h = int(self.scrollArea.height() - 2 * self.paddingsize - self.rulesize)
             w = int(h * self.mainImage.width() / self.mainImage.height())
         if h > self.scrollArea.height() - 2 * self.paddingsize - self.rulesize:
              h = int(self.scrollArea.height() - 2 * self.paddingsize) - self.rulesize
              w = int(h * self.mainImage.width() / self.mainImage.height())
         if w > self.scrollArea.width() - 2 * self.paddingsize - self.rulesize:
              w = int(self.scrollArea.width() - 2 * self.paddingsize) - self.rulesize
              h = int(w * self.mainImage.height() / self.mainImage.width())

         self.imgLabel.resize(w,h)
         self.originsize = self.imgLabel.size()
         self.adjustState()
         self.initThumbnailLabel()
         self.thumbnailLabel.setVisible(True)

         self.imgLabelR.resize(w,h)
         self.adjustStateR()
         Helper.setTabName(self,self.currentImageFile,True)
       except:
           return
    def setMouseMoveTrack(self):
        self.scrollArea.setMouseTracking(True)
        self.scrollAreaWidgetContents.setMouseTracking(True)
        self.imgLabel.setMouseTracking(True)
        self.scrollWidgets.setMouseTracking(True)

        self.scrollAreaR.setMouseTracking(True)
        self.scrollAreaWidgetRight.setMouseTracking(True)
        self.imgLabelR.setMouseTracking(True)
    def saveHeatMap(self,savetype):
        if not hasattr(self, 'heatImage'):
                QMessageBox.information(self, "提示", "请加载热图数据       ",QMessageBox.Ok)
                return
        defaultfile = self.settings.value("saveheatmapfile")
        if not defaultfile:
            defaultfile = ""
        else:
            dirname=os.path.dirname(defaultfile)
            filename= os.path.basename(os.path.splitext(self.currentImageFile)[0])
            defaultfile=dirname+"/"+filename+".jpg"
        fileName,type = QFileDialog.getSaveFileName(self,"Open Config",defaultfile,"Jpeg Files (*.jpg)")
        if fileName == "":
            return
        loadProcess = Process(target=Helper.showExportBothImageDlg)
        loadProcess.start()
        try:
            self.settings.setValue("saveheatmapfile",fileName)
            if savetype == 1:#保存叠加图
                pixmap = QImage(self.mainImage.copy())
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode_Overlay)
                for i,point in enumerate(self.heatDataList):
                    realx=point.x()*self.actualGridwidth
                    realy=point.y()*self.actualGridheight
                    painter.fillRect(realx,realy,self.actualGridwidth,self.actualGridheight,self.heatDataColorList[i])
                painter.setCompositionMode(QPainter.CompositionMode_Multiply)
                painter.drawImage(QRect(pixmap.width()-self.watermarkImg.width(),pixmap.height()-self.watermarkImg.height(),self.watermarkImg.width(),self.watermarkImg.height()),self.watermarkImg,QRect(0,0,self.watermarkImg.width(),self.watermarkImg.height()))
                painter.end()
                image = QImage(pixmap)
                image.setDotsPerMeterX(3779)
                image.setDotsPerMeterY(3779)
                image.save(fileName,"JPG")
                del pixmap
                del image
                gc.collect()
            elif savetype == 2:
                pixmap = QPixmap(self.mainImage.width(),self.mainImage.height())
                pixmap.fill(QColor(255,255,255))
                painter = QPainter(pixmap)
                for i,point in enumerate(self.heatDataList):
                    realx=point.x()*self.actualGridwidth
                    realy=point.y()*self.actualGridheight
                    painter.fillRect(realx,realy,self.actualGridwidth,self.actualGridheight,self.heatDataColorList[i])
                painter.setCompositionMode(QPainter.CompositionMode_Multiply)
                painter.drawImage(QRect(pixmap.width()-self.watermarkImg.width(),pixmap.height()-self.watermarkImg.height(),self.watermarkImg.width(),self.watermarkImg.height()),self.watermarkImg,QRect(0,0,self.watermarkImg.width(),self.watermarkImg.height()))
                painter.end()
                image = QImage(pixmap)
                image.setDotsPerMeterX(3779)
                image.setDotsPerMeterY(3779)
                image.save(fileName,"JPG")
                del pixmap
                del image
                gc.collect()
        except Exception as ex:
            print(ex)
            return
        finally:
            loadProcess.terminate()
        return
    #保存标记文件
    def saveLabelData(self):
        if not hasattr(self, 'mainImage'):
                QMessageBox.information(self, "提示", "请加载图像数据       ",QMessageBox.Ok)
                return
        #print(self.currentImageFile)
        defaultfile = self.settings.value("savelabelfile")
        if not defaultfile:
            defaultfile = ""
        else:
            dirname=os.path.dirname(defaultfile)
            filename= os.path.basename(os.path.splitext(self.currentImageFile)[0])
            defaultfile=dirname+"/"+filename+".json"
        fileName,type = QFileDialog.getSaveFileName(self,"Open Config",defaultfile,"JSON Files (*.json)")
        if fileName == "":
            return
        loadProcess = Process(target=Helper.showExportLabelDlg)
        loadProcess.start()
        self.settings.setValue("savelabelfile",fileName)
        try:
            largescale=self.largeScale
            if self.currentImageFile[-4:].upper()!="JSON":
                imagepath = "imagepath"
                imagedata = "imagedata"
                imageheight = self.mainImage.height()
                imagewidth = self.mainImage.width()
                list = []
                for label in self.labelList:
                    if len(label.pointList) == 0:
                            continue
                    list.append(label)
                with open(fileName,"w+",encoding="utf-8") as  f:
                    f.write("{\"version\": \"4.1.2\",\"flags\": {},\"shapes\": [")
                    for labindex,label in enumerate(list):
                        if len(label.pointList) == 0:
                            continue
                        f.write("{")
                        f.write("\"label\":\"" + label.labelName + "\",")
                        f.write("\"points\":" + "[")

                        length = len(label.pointList)
                        for i,point in enumerate(label.pointList):
                            if i != length - 1:
                                f.write("[" + str(point.x()*largescale) + "," + str(point.y()*largescale) + "],")
                            else:
                                f.write("[" + str(point.x()*largescale) + "," + str(point.y()*largescale) + "]")
                        f.write("]" + ",")
                        #f.write("\"group_id\":\""+label.labelGroup+"\",")
                        f.write("\"group_id\":" + "null" + ",")
                        f.write("\"shape_type\":\"" + label.shapeType + "\",")
                        f.write("\"label_type\":\"" + str(label.labelType) + "\",")
                        f.write("\"flags\":" + "{},")
                        f.write("\"description\":\"" + label.labelDes + "\",")
                        f.write("\"color\":\"" + label.labelColor.name() + "\"")
                        f.write("}")
                        if labindex != (len(list) - 1):
                            f.write(",")
                    f.write("],")
                    f.write("\"imagePath\": \"" + "\",")#找不到文件会报错，所以赋值为空，使用base64图片
                    #f.write("\"imageData\": \"" + Helper.changeToBase64(self) + "\",")
                    f.write("\"imageData\": \"" + Helper.getBase64(self) + "\",")
                    f.write("\"imageHeight\": " + str(imageheight) + ",")
                    f.write("\"imageWidth\": " + str(imagewidth))
                    f.write("}")
            else:#本就是json文件
                jsonObj=None
                with open(self.currentImageFile) as f:
                     jsonstr = json.load(f)
                     jsonObj=Helper.obj_dic(jsonstr)#将dict字符串转换成对象
                imagepath = jsonObj.imagePath
                #imagedata = jsonObj.imageData
                imageheight = jsonObj.imageHeight
                imagewidth = jsonObj.imageWidth
                list = []
                for label in self.labelList:
                    if len(label.pointList) == 0:
                            continue
                    list.append(label)
                with open(fileName,"w+",encoding="utf-8") as  f:
                    f.write("{\"version\": \"4.1.2\",\"flags\": {},\"shapes\": [")
                    for labindex,label in enumerate(list):
                        if len(label.pointList) == 0:
                            continue
                        f.write("{")
                        f.write("\"label\":\"" + label.labelName + "\",")
                        f.write("\"points\":" + "[")

                        length = len(label.pointList)
                        for i,point in enumerate(label.pointList):
                            if i != length - 1:
                                f.write("[" + str(point.x()*largescale) + "," + str(point.y()*largescale) + "],")
                            else:
                                f.write("[" + str(point.x()*largescale) + "," + str(point.y()*largescale) + "]")
                        f.write("]" + ",")
                        #f.write("\"group_id\":\""+label.labelGroup+"\",")
                        f.write("\"group_id\":" + "null" + ",")
                        f.write("\"shape_type\":\"" + label.shapeType + "\",")
                        f.write("\"label_type\":\"" + str(label.labelType) + "\",")
                        f.write("\"flags\":" + "{},")
                        f.write("\"description\":\"" + label.labelDes + "\",")
                        f.write("\"color\":\"" + label.labelColor.name() + "\"")
                        f.write("}")
                        if labindex != (len(list) - 1):
                            f.write(",")
                    f.write("],")
                    f.write("\"imagePath\": \"" + "\",")#找不到文件会报错，所以赋值为空，使用base64图片
                    #f.write("\"imageData\": \"" + Helper.changeToBase64(self) + "\",")
                    f.write("\"imageData\": \"" + jsonObj.imageData + "\",")
                    f.write("\"imageHeight\": " + str(imageheight) + ",")
                    f.write("\"imageWidth\": " + str(imagewidth))
                    f.write("}")
        finally:
            loadProcess.terminate()
        return
    def changeToBase64(self):  
        ba = QByteArray()
        buf = QBuffer(ba)
        self.mainImage.save(buf, "jpg")
        hexed = ba.toBase64()
        buf.close()
        return str(hexed)[2:-1]
    def getBase64(self):
        with open(self.currentImageFile, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
            return image_base64
 
    def exportLabeledImage(self,savetype):
        if not hasattr(self, 'mainImage'):
                QMessageBox.information(self, "提示", "请加载图像数据       ",QMessageBox.Ok)
                return
        if len(self.labelList) == 0:
                QMessageBox.information(self, "提示", "请执行图像标记       ",QMessageBox.Ok)
                return
        defaultfile = self.settings.value("savelabeledimagefile")
        if not defaultfile:
            defaultfile = ""
        else:
            dirname=os.path.dirname(defaultfile)
            filename= os.path.basename(os.path.splitext(self.currentImageFile)[0])
            defaultfile=dirname+"/"+filename+".jpg"
        fileName,type = QFileDialog.getSaveFileName(self,"Open Config",defaultfile,"Jpeg Files (*.jpg)")
        if fileName == "":
            return

        loadProcess = Process(target=Helper.showExportImageDlg)
        loadProcess.start()
        self.settings.setValue("savelabeledimagefile",fileName)
        try:
            if savetype == 1:#保存叠加图
                pixmap = QPixmap(self.mainImage.copy())
                painter = QPainter(pixmap)
                painter.setCompositionMode(QPainter.CompositionMode_Overlay)
                if hasattr(self, 'heatImage') and self.viewMode != 0 :
                     #painter.drawPixmap(0,0,self.heatImage)
                     for i,point in enumerate(self.heatDataList):
                        realx=point.x()*self.actualGridwidth
                        realy=point.y()*self.actualGridheight
                        painter.fillRect(realx,realy,self.actualGridwidth,self.actualGridheight,self.heatDataColorList[i])

                #绘制label
                linewidth = self.labelLineWidth
                pointsize = self.labelPointWidth
                if len(self.labelList) > 0:            
                    painter.setCompositionMode(QPainter.CompositionMode_Source)            
                
                    viewPointList = []
                    for lab in self.labelList:  
                        labeltype = lab.labelType
                        labelcolor = QColor(lab.labelColor)
                        points = lab.pointList
                        painter.setPen(labelcolor)
                        if len(points) == 0:
                            continue
                        if labeltype == 1:#polygon
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points))
                            painter.setPen(QPen(labelcolor,linewidth))
                            painter.drawPolygon(QPolygonF(points))
                        elif labeltype == 2:#rect
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points))
                            painter.setPen(QPen(labelcolor,linewidth))
                            if len(points) >= 2:
                                points = points[:2]
                            painter.drawRect(QRectF(QPointF(points[0]),QPointF(points[1])))
                        elif labeltype == 3:#circle
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points[:1]))
                            painter.setPen(QPen(labelcolor,linewidth))
                            if len(points) >= 2:
                                points = points[:2]
                            r = math.sqrt(math.pow(QPointF(points[0]).x() - QPointF(points[1]).x(),2) + math.pow(QPointF(points[0]).y() - QPointF(points[1]).y(),2))
                            painter.drawEllipse(QPointF(points[0]),r,r)
                        elif labeltype == 4:#line
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points))
                            painter.setPen(QPen(labelcolor,linewidth))
                            if len(points) >= 2:
                                points = points[:2]
                            painter.drawLine(QPointF(points[0]),QPointF(points[1]))
                        elif labeltype == 5:#point
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            if len(points) > 0:
                                painter.drawPoint(QPointF(points[0]))
                        if labeltype == 6:#polyline
                            pen = QPen(labelcolor,pointsize)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points))
                            painter.setPen(QPen(labelcolor,linewidth))
                            painter.drawPolyline(QPolygonF(points))   
                        elif labeltype == 7:#画笔
                            pen = QPen(labelcolor,2)
                            pen.setCapStyle(Qt.RoundCap)
                            painter.setPen(pen)
                            painter.drawPoints(QPolygonF(points))
                            painter.setPen(QPen(labelcolor,linewidth))
                            painter.drawPolygon(QPolygonF(points))
                painter.setCompositionMode(QPainter.CompositionMode_Multiply)
                painter.drawImage(QRect(pixmap.width()-self.watermarkImg.width(),pixmap.height()-self.watermarkImg.height(),self.watermarkImg.width(),self.watermarkImg.height()),self.watermarkImg,QRect(0,0,self.watermarkImg.width(),self.watermarkImg.height()))
                painter.end()
                image = QImage(pixmap)
                image.setDotsPerMeterX(3779)
                image.setDotsPerMeterY(3779)
                image.save(fileName,"JPG")
                del pixmap
                del image
                gc.collect()
            elif savetype == 2:
                pixmap = QPixmap(self.mainImage.width(),self.mainImage.height())
                pixmap.fill(QColor(255,255,255))
                painter = QPainter(pixmap)
                #painter.drawPixmap(0,0,self.heatImage)
                for i,point in enumerate(self.heatDataList):
                    realx=point.x()*self.actualGridwidth
                    realy=point.y()*self.actualGridheight
                    painter.fillRect(realx,realy,self.actualGridwidth,self.actualGridheight,self.heatDataColorList[i])
                painter.setCompositionMode(QPainter.CompositionMode_Multiply)
                painter.drawImage(QRect(pixmap.width()-self.watermarkImg.width(),pixmap.height()-self.watermarkImg.height(),self.watermarkImg.width(),self.watermarkImg.height()),self.watermarkImg,QRect(0,0,self.watermarkImg.width(),self.watermarkImg.height()))
                painter.end()
                image = QImage(pixmap)
                image.setDotsPerMeterX(3779)
                image.setDotsPerMeterY(3779)
                image.save(fileName,"JPG")
                del pixmap
                del image
                gc.collect()
        except:
            return
        finally:
            loadProcess.terminate()
        return

    def setColumnNum(self):
        columnstr = self.heatTypeCombo.currentText()  
        if columnstr == "":
            self.heatDataColumn = 3
        else:
            self.heatDataColumn = int(columnstr)
            #####################################重新获取heatlist
        self.settings.setValue("columnnum", self.heatDataColumn)
        if not hasattr(self, 'mainImage'):
            return
        if not hasattr(self, 'lastcolumn'):
            self.lastcolumn = self.heatDataColumn
        else:
            if self.lastcolumn == self.heatDataColumn:
                return
            else:
                self.lastcolumn = self.heatDataColumn

        QApplication.processEvents()
        loadProcess = Process(target=Helper.showReloadingHeatMapDlg)
        loadProcess.start()
        try:
            file = self.currentImageFile
            heatfile = os.path.dirname(file) + "/" + os.path.basename(os.path.splitext(file)[0]) + ".txt"
            Helper.loadHeatMap(self,file,heatfile)
            self.imgLabel.repaint()
            self.imgLabelR.repaint()
                
        finally:
            loadProcess.terminate()
    def getGradientColor(self,value):
        for i in range(len(self.gradientList) - 1):
            p1 = self.gradientList[i].position
            p2 = self.gradientList[i + 1].position
            if value >= p1 and value <= p2:
                c1 = self.gradientList[i].color
                c2 = self.gradientList[i + 1].color
                bili = (value - p1) / (p2 - p1)
                r = c1.red() + (c2.red() - c1.red()) * bili
                g = c1.green() + (c2.green() - c1.green()) * bili
                b = c1.blue() + (c2.blue() - c1.blue()) * bili
                return QColor(r,g,b)
        return QColor(255,0,0)
    def setDefaultGradient(self):
        with open("MainUI/gradient.grd","rb")as f:
            list = pickle.load(f)
            str = self.settings.value("gradientindex")
            index = -1
            if str:
                index = int(str)
            if(index > len(list) - 1):
                index = len(list) - 1
            self.gradientList = list[index].gradientlist
            self.gradientList = sorted(self.gradientList, key=lambda k: k.position) 
            pixmap = QPixmap(70,18)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing,True)
            linearGradient = QLinearGradient(0,10,pixmap.width(),10)
            for gradient in self.gradientList:
                linearGradient.setColorAt(gradient.position,gradient.color)
            painter.setBrush(linearGradient)
            painter.setPen(Qt.transparent)
            painter.drawRect(0,0,pixmap.width(),pixmap.height())
            painter.end()
            self.gradientLab.setPixmap(pixmap)
    def listWidgetContext(self,point):
        popMenu = QMenu()

        modifyAction = QAction("修改")
        modifyAction.triggered.connect(lambda:Helper.modifyListItem(self))
        popMenu.addAction(modifyAction)

        delAction = QAction("删除")
        delAction.triggered.connect(lambda:Helper.deleteListItem(self))
        popMenu.addAction(delAction)
        #delselectedAction=QAction("删除所选")
        #delselectedAction.triggered.connect(lambda:Helper.deleteSelectedListItem(self))
        #popMenu.addAction(delselectedAction)
        popMenu.exec_(QCursor.pos())
    def deleteListItem(self):
        index = self.labellistWidget.currentIndex().row()
        self.labelList.pop(index)
        self.highlightLabelIndex=-1
        self.imgLabel.repaint()
        self.imgLabelR.repaint()

        ItemModel = QStandardItemModel()
        pixmap = QPixmap(2000,2)
        pixmap.fill(QColor(40,40,40))
        painter = QPainter(pixmap)
        for label in self.labelList:
            if len(label.pointList)==0:
                continue;
            labelname = label.labelName
            item = QStandardItem("    " + labelname)
            painter.fillRect(QRect(0,0,10,2),QColor(label.labelColor))
            item.setBackground(QBrush(pixmap))
            ItemModel.appendRow(item)
        painter.end()
        self.labellistWidget.setModel(ItemModel)
    def modifyListItem(self):
        index = self.labellistWidget.currentIndex().row()
        name = self.labelList[index].labelName
        des = self.labelList[index].labelDes
        dlg = LabelDlg()
        
        labelnames = []
        for label in self.labelList:
            if not label.labelName in labelnames:
                dlg.labelNameEdit.addItem(label.labelName)
                labelnames.append(label.labelName)
        #dlg.labelNameEdit.setCurrentText("")
        dlg.labelNameEdit.setCurrentText(name)
        dlg.labelDesEdit.setText(des)
        result = dlg.exec_()
        if result == 1:
            labelname = dlg.labelNameEdit.currentText()
            labeldes = dlg.labelDesEdit.toPlainText()
            self.labelList[index].labelName = labelname
            self.labelList[index].labelDes = labeldes


            ItemModel = QStandardItemModel()
            pixmap = QPixmap(2000,2)
            pixmap.fill(QColor(40,40,40))
            painter = QPainter(pixmap)
            for label in self.labelList:
                if len(label.pointList)==0:
                    continue;
                labelname = label.labelName
                item = QStandardItem("    " + labelname)
                painter.fillRect(QRect(0,0,10,2),QColor(label.labelColor))
                item.setBackground(QBrush(pixmap))
                #item.setBackground(QBrush(QColor(label.labelColor)))
                ItemModel.appendRow(item)
            painter.end()



            #ItemModel =QStandardItemModel();
            #for label in self.labelList[0:-1]:
            #    labelname=label.labelName
            #    item=QStandardItem(labelname)
            #    item.setBackground(QBrush(QColor(label.labelColor)))
            #    ItemModel.appendRow(item)
            self.labellistWidget.setModel(ItemModel)




    def deleteSelectedListItem(self):
        index = self.labellistWidget.currentIndex()
        self.labelList.pop(index)
    def obj_dic(d):
        top = type('new', (object,), d)
        seqs = tuple, list, set, frozenset
        for i, j in d.items():
            if isinstance(j, dict):
                setattr(top, i, Helper.obj_dic(j))
            elif isinstance(j, seqs):
                setattr(top, i,type(j)(Helper.obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
            else:
                setattr(top, i, j)
        return top

    def loadJsonData(self):
        try:
         historyfile = self.settings.value("openjsonfile")
         if historyfile == None:
             historyfile = ""
         file,filetype = QFileDialog.getOpenFileName(self,"加载标记文件",historyfile,"Json Files (*.json);;Txt Files (*.txt)")  #设置文件扩展名过滤,注意用双分号间隔
         if file == "":
             return

         self.settings.setValue("openjsonfile", file)
         self.loadProcess = Process(target=Helper.showLoadingJsonDlg)
         self.loadProcess.start()
         self.labelList.clear()
         image=QPixmap()
         with open(file) as f:
             jsonlab = json.load(f)
             obj=Helper.obj_dic(jsonlab)#将dict字符串转换成对象
             base64str=obj.imageData
             decodearray=base64.b64decode(base64str)
             image.loadFromData(base64.b64decode(base64str))
             if image.width()==0:
                 self.isLargeImage=True
                 with open('tmp.jpg','wb') as ff:
                    ff.write(base64.b64decode(base64str))
                 reader=QImageReader("tmp.jpg")
                 size=reader.size()
                 for i in range(1,100):
                    if size.width()/i<20000 and size.height()/i<20000:
                        self.largeScale=i
                        break
                 reader.setScaledSize(QSize(int(size.width()/self.largeScale),int(size.height()/self.largeScale)))
                 img=QImage()
                 reader.read(img);
                 image=QPixmap(img)
             else:
                 self.isLargeImage=False
                 self.largeScale=1

             Helper.loadJsonPixmap(self,image,file)
             labellist=obj.shapes
             for lab in labellist:
                 tmplab=Label()
                 tmplab.labelName=lab.label
                 tmplab.labelDes=lab.description
                 pointlist=[]
                 gc.collect()
                 for p in lab.points:
                     pointlist.append(QPointF(float(p[0]/self.largeScale),float(p[1])/self.largeScale))
                 tmplab.pointList=pointlist
                 tmplab.labelColor=QColor(lab.color)
                 tmplab.labelType=int(lab.label_type)
                 tmplab.shapeType=lab.shape_type
                 self.labelList.append(tmplab)
             lab=Label()
             lab.pointList=[]
             lab.labelColor=self.currentLabelColor
             lab.labelType=self.eventType
             lab.shapeType=self.currentShapeType
             self.labelList.append(lab)

             ItemModel =QStandardItemModel();
             pixmap=QPixmap(2000,2)
             pixmap.fill(QColor(40,40,40))
             painter=QPainter(pixmap)
             for label in self.labelList:
                if len(label.pointList)==0:
                    continue
                labelname=label.labelName
                item=QStandardItem("    "+labelname)
                painter.fillRect(QRect(0,0,10,2),QColor(label.labelColor))
                item.setBackground(QBrush(pixmap))
                ItemModel.appendRow(item)
             painter.end()
             self.labellistWidget.setModel(ItemModel)
        except Exception as e:
           print(e)
    def loadJsonDataWithFile(self,file):
        #try:
         if file == "":
             return
         self.loadProcess = Process(target=Helper.showLoadingJsonDlg)
         self.loadProcess.start()
         self.labelList.clear()
         self.heatDataList.clear()#热图坐标
         with open(file) as f:
             jsonlab = json.load(f)
             obj=Helper.obj_dic(jsonlab)#将dict字符串转换成对象
             base64str=obj.imageData
             image=QPixmap()
             decodearray=base64.b64decode(base64str)
             image.loadFromData(decodearray)

             if image.width()==0:
                 self.isLargeImage=True
                 with open('tmp.jpg','wb') as ff:
                    ff.write(decodearray)
                 reader=QImageReader("tmp.jpg")
                 size=reader.size()
                 for i in range(1,100):
                    if size.width()/i<20000 and size.height()/i<20000:
                        self.largeScale=i
                        break
                 reader.setScaledSize(QSize(int(size.width()/self.largeScale),int(size.height()/self.largeScale)))
                 img=QImage()
                 reader.read(img);
                 image=QPixmap(img)
             else:
                 self.isLargeImage=False
                 self.largeScale=1

             Helper.loadJsonPixmap(self,image,file)

             labellist=obj.shapes
             for lab in labellist:
                 tmplab=Label()
                 tmplab.labelName=lab.label
                 tmplab.labelDes=lab.description
                 pointlist=[]
                 gc.collect()
                 for p in lab.points:
                     pointlist.append(QPointF(float(p[0]),float(p[1])))
                 tmplab.pointList=pointlist
                 tmplab.labelColor=QColor(lab.color)
                 tmplab.labelType=int(lab.label_type)
                 tmplab.shapeType=lab.shape_type
                 self.labelList.append(tmplab)
             lab=Label()
             lab.pointList=[]
             lab.labelColor=self.currentLabelColor
             lab.labelType=self.eventType
             lab.shapeType=self.currentShapeType
             self.labelList.append(lab)

             ItemModel =QStandardItemModel();
             pixmap=QPixmap(2000,2)
             pixmap.fill(QColor(40,40,40))
             painter=QPainter(pixmap)
             for label in self.labelList:
                if len(label.pointList)==0:
                    continue
                labelname=label.labelName
                item=QStandardItem("    "+labelname)
                painter.fillRect(QRect(0,0,10,2),QColor(label.labelColor))
                item.setBackground(QBrush(pixmap))
                #item.setBackground(QBrush(QColor(label.labelColor)))
                ItemModel.appendRow(item)
             painter.end()
             self.labellistWidget.setModel(ItemModel)
        #except:
    def loadJsonPixmap(self,pixmap,file):
        self.widgetPics.blockSignals(False)#恢复点击事件绑定     
        if pixmap==None or pixmap.width()==0:
            self.loadProcess.terminate()
            return    
        Helper.clearLabelWidget(self)
        self.mainImage=pixmap
        self.usecache=False 
        self.thumbImage = self.mainImage.scaled(QSize(self.thumbsize, self.thumbsize), QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation);
        self.locked=False#解锁内存

        self.currentImageFile=file
        Helper.setTabName(self,os.path.basename(file),True)

        Helper.autoSize(self)
        if self.showruler:
            self.leftXLabel.setVisible(True)
            self.leftYLabel.setVisible(True)
            self.rightXLabel.setVisible(True)
            self.rightYLabel.setVisible(True)

        #QApplication.processEvents()
        if hasattr(self, 'cachePixmap'):
            del self.cachePixmap
        #################################加载热图
        heatfile=os.path.dirname(file)+"/"+ os.path.basename(os.path.splitext(file)[0])+".txt"
        if not os.path.exists(heatfile):
            slm=QStringListModel()
            self.heatlistWidget.setModel(slm)
            self.loadProcess.terminate()
            Helper.setViewMode(self,0)
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
            Helper.loadJsonHeatMap(self,file,heatfile)#加载json热图
            self.loadProcess.terminate()
            self.imgLabelR.resize(self.imgLabel.width(),self.imgLabel.height())
            self.adjustStateR()
        self.stackedWidget.setVisible(True)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.setTabEnabled(0,True)
        #self.stackedWidget.setStyleSheet("QTabBar::tab:disabled {width: 0; color: transparent;} QTabWidget::tab-bar {left: 1px;}")
        #self.mainWidget.setStyleSheet("background: rgb(57,57,57);")

        self.scrollAreaWidgetContents.setStyleSheet("background: rgb(247,247,247)")
        self.scrollAreaWidgetRight.setStyleSheet("background: rgb(247,247,247)")

        QApplication.processEvents()
        Helper.autoSize(self)  
    def openParameterSetDlg(self):
        dlg=ParameterSetDlg(self)
        dlg.show()
    def beginMeasure(self):
        if(self.eventType==9):
            self.eventType=0
            self.measureTool.setChecked(False)
            self.imgLabel.repaint()
            self.imgLabelR.repaint()
            return
        if not hasattr(self, 'heatImage'):
            QMessageBox.information(self, "提示", "请加载热图数据       ",QMessageBox.Ok)
            self.measureTool.setChecked(False)
            return
        file=self.currentImageFile
        scanfile=os.path.dirname(file)+"/"+"Scan_"+ os.path.basename(os.path.splitext(file)[0])+".txt"
        if not os.path.exists(scanfile):
            QMessageBox.information(self,"提示","缺少Scan文件，无法执行操作")
            self.measureTool.setChecked(False)
            return
        config = configparser.ConfigParser() # 类实例化
        config.read(scanfile)
        value = config.get("General","Size")
        value=value.replace("mm","")
        value=value.split('x')
        width=float(value[0])*1000
        self.physicalbili=width/self.mainImage.width()
        self.measureList.clear();
        self.tmpMovePoint=QPointF(0,0)#鼠标当前位置点
        Helper.drawLabel(self,9);
   