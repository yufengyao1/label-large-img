import sys,gc,time,threading,os,multiprocessing
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from Helper import Helper
from multiprocessing import Process
import ctypes
class openfolderThread(QThread):
    created_signal=pyqtSignal(QPixmap,int,bool,str) 
    def __init__(self, folder):
        super(openfolderThread, self).__init__()
        self.folder = folder
        self.listsize=200  
    def __del__(self):
        self.wait()
    def run(self):
        try:
            files=Helper.getFiles(self.folder);
            i=0
            lastone=False
            for file in files:
                QApplication.processEvents()
                if i==len(files)-1:
                    lastone=True
                tmpImage = QPixmap(file)
                tmpPix = tmpImage.scaled(QSize(self.listsize, self.listsize),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)  
                self.created_signal.emit(tmpPix,int(i),lastone,file)        #发送信号
                i = i + 1
                del tmpPix
                del tmpImage
                gc.collect()
                time.sleep(0.002)
            self.exit(0)            #关闭线程
        finally:
            return

class loadimageThread(QThread):
    created_signal=pyqtSignal(QPixmap,str) 
    def __init__(self,filename):
        super(loadimageThread, self).__init__()
        self.filename = filename
    def __del__(self):#缺少时函数中创建的线程会跟随函数结束而关闭，导致线程报错
        self.wait()
    def run(self):
        #try:
            pixmap = QPixmap(self.filename)
            self.created_signal.emit(pixmap,self.filename)        #发送信号
            del pixmap
            self.exit(0)            #关闭线程
        #except:
        #    self.created_signal.emit(None)        #发送信号
        #finally:
        #    return
class createThumbThread(QThread):
    refresh_signal=pyqtSignal(QPixmap,int) 
    def __init__(self,parent):
        super(createThumbThread, self).__init__()
        #self.folder = folder
        self.parent=parent
        self.letrun=True
    def __del__(self):#缺少时函数中创建的线程会跟随函数结束而关闭，导致线程报错
        self.wait()
    def run(self):
     try:
         self.parent.isRunning=True
         cachelist = Helper.getDatFiles("cache")
         for i in range(len(self.parent.filelist)):
             havecache = False
             tmpfile = self.parent.filelist[i]
             for cache in cachelist: 
                 if(os.path.basename(os.path.splitext(tmpfile)[0]) == os.path.basename(os.path.splitext(cache)[0])):
                     havecache = True
                     tmppix = QPixmap()
                     file = QFile(cache)
                     file.open(QIODevice.ReadOnly)
                     inn = QDataStream(file)
                     inn >> tmppix
                     file.close()
                     self.refresh_signal.emit(tmppix,i)        #发送信号-线程里不能直接操作UI
                     #self.parent.widgetPics.item(i).setIcon(QIcon(tmppix))
                     del tmppix
                     gc.collect()
                     break
             if havecache:
                 continue
             p1 = multiprocessing.Process(target=Helper.createThumbnail,args=(self.parent.thumbQueue,self.parent.filelist[i]))
             p1.start()
             imgbytes=[];
             while True:
                 if not self.letrun:
                     return
                 imgbytes = self.parent.thumbQueue.get()
                 if imgbytes:
                     break
                 time.sleep(0.001)
                 QApplication.processEvents()
             p1.terminate()
             buffer=QBuffer()
             buffer.setData(imgbytes)
             buffer.open(QBuffer.ReadOnly)
             inn = QDataStream(buffer)
             image = QPixmap()
             inn >> image
         
             if(image.width() > 0 and self.letrun):
                 self.refresh_signal.emit(image,i)        #发送信号
                 #self.parent.widgetPics.item(i).setIcon(QIcon(image))
                 #self.parent.widgetPics.repaint()
             del inn
             del buffer
             del image
             gc.collect() 
             if self.letrun==False:
                 self.parent.isRunning=False
                 return
         self.parent.isRunning=False
     except:
         self.parent.isRunning=False
         return
    def stop(self):
         self.letrun=False