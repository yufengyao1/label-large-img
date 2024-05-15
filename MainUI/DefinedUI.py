from PyQt5.QtGui import QPainter,QPixmap,QFont,QPolygonF
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import gc,math,sip
from Label import GradientPart,Label
from Label_form import LabelDlg
class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel,self).__init__(parent)
        self.parent=parent
        self.lastviewx=0
        self.lastviewy=0
        self.realx=0
        self.realy=0
        self.realw=0
        self.realh=0
        self.vieww=0
        self.viewh=0
        self.linewidth=parent.labelLineWidth
        self.pointSize=parent.labelPointWidth
        self.alpha=0.3       
    def createcache(self):
        try:
            self.parent.cachePixmap=QPixmap(QSize(self.vieww,self.viewh))
            p=QPainter(self.parent.cachePixmap)
            p.setRenderHint(QPainter.SmoothPixmapTransform)
            p.drawPixmap(QRectF(0,0,self.vieww,self.viewh),self.parent.mainImage,QRectF(self.realx,self.realy,self.realw,self.realh))
            p.end()
            self.parent.usecache=True
            return
        except Exception as e:
            print(e)
    def mouseMoveEvent(self, event):
        DrawHelper.measureLineMove(self,event)
        return super().mouseMoveEvent(event)
    def mousePressEvent(self, event):
        DrawHelper.measureLineMousePress(self,event)
        return super().mousePressEvent(event)
    def paintEvent(self, evt):
          super().paintEvent(evt)
        #try:
          if(self.parent.usecache==True):
              tmp=QPainter(self)
              tmp.setRenderHint(QPainter.HighQualityAntialiasing)
              tmp.setRenderHint(QPainter.SmoothPixmapTransform)
              if self.parent.viewMode!=3:
                  tmp.setCompositionMode(QPainter.CompositionMode_Source)
                  tmp.drawPixmap(QPoint(self.lastviewx,self.lastviewy),self.parent.cachePixmap)
              if self.parent.viewMode==1:
                   tmp.setCompositionMode(QPainter.CompositionMode_Overlay)
                   DrawHelper.drawHeatMap(self,tmp)#绘制热图
              elif self.parent.viewMode==3:    
                   DrawHelper.drawHeatMap(self,tmp)#绘制热图

              tmp.end()
              return
          if hasattr(self.parent, 'mainImage')==False:
              return
          piw=self.parent.imgLabel.width()
          pih=self.parent.imgLabel.height()
          psw=self.parent.scrollArea.width()
          psh=self.parent.scrollArea.height()
          viewx=self.parent.scrollbarX.value()-self.parent.imgLabel.x()
          if viewx<0:
              self.vieww=psw+viewx
              viewx=0              
          else:
              self.vieww=psw
          viewy=self.parent.scrollbarY.value()-self.parent.imgLabel.y()
          if viewy<0:
              self.viewh=psh+viewy
              viewy=0
          else:
              self.viewh=psh
          if psw-(piw-viewx)>0:
              self.vieww=piw-viewx
          if psh-(pih-viewy)>0:
              self.viewh=pih-viewy

          if(pih<psh):
              self.viewh=pih
          if(piw<psw):
              self.vieww=piw
          self.realx= int(self.parent.mainImage.width() *viewx/self.parent.imgLabel.width())
          self.realy= int(self.parent.mainImage.height() *viewy/self.parent.imgLabel.height())
          self.realh=int(self.parent.mainImage.height() *self.viewh/self.parent.imgLabel.height())
          self.realw=int(self.parent.mainImage.width() *self.vieww/self.parent.imgLabel.width())
          self.lastviewx=viewx
          self.lastviewy=viewy      
          painter2=QPainter(self)
          painter2.setPen(QPen(QColor(140,140,140),0.5))
          painter2.setRenderHint(QPainter.SmoothPixmapTransform)
          if self.parent.viewMode!=3:
            painter2.setCompositionMode(QPainter.CompositionMode_Source)
            painter2.drawPixmap(QRectF(viewx,viewy,self.vieww,self.viewh),self.parent.mainImage,QRectF(self.realx,self.realy,self.realw,self.realh))
          if self.parent.viewMode==1:
             if hasattr(self.parent, 'heatImage'):
                 painter2.setCompositionMode(QPainter.CompositionMode_Overlay)
                 DrawHelper.drawHeatMap(self,painter2)#绘制热图
          if self.parent.viewMode==3:    
             if hasattr(self.parent, 'heatImage'):  
                 DrawHelper.drawHeatMap(self,painter2)#绘制热图
          if self.parent.showgrid:
              painter2.setPen(QPen(QColor(140,140,140),0.5))
              painter2.setRenderHint(QPainter.Antialiasing, False)
              painter2.setCompositionMode(QPainter.CompositionMode_Source)
              bilix = self.parent.mainImage.width() / piw #一个视觉像素相当于N个图片像素
              partlength = math.ceil(4 * bilix * 10)
              for m in range(partlength,partlength + 99):
                 if m % 10 == 0:
                     partlength = m
                     break
              startnum=int(self.realx/partlength)
              shownum=int(self.realw/partlength)+5
              for i in range(startnum,startnum+shownum):
                  if i%2==0:
                      continue
                  realx=i*partlength
                  x=float(round(1.0*realx/bilix))
                  if x<-20:
                      continue
                  painter2.drawLine(x, viewy,  x, viewy+self.viewh)  
                  
              biliy = self.parent.mainImage.height() / pih #一个视觉像素相当于N个图片像素
              partlength = math.ceil(4 * biliy * 10)
              for m in range(partlength,partlength + 99):
                 if m % 10 == 0:
                     partlength = m
                     break
              startnum=int(self.realy/partlength)
              shownum=int(self.realh/partlength)+5
              for i in range(startnum,startnum+shownum):
                  if i%2==0:
                      continue
                  realy=i*partlength
                  y=float(round(1.0*realy/biliy))
                  if y<-20:
                      continue
                  painter2.drawLine(viewx,y, viewx+self.vieww,y)
          
          DrawHelper.drawLabelGrid(self,painter2,piw,pih)
          DrawHelper.drawDragRect(self,painter2)
          DrawHelper.drawLabels(self,painter2)
          DrawHelper.drawMeasureLine(self,painter2)#绘制测线
          #DrawHelper.drawMeasureRule(self,painter2)#绘制标尺
          painter2.end()
class HeatLabel(QLabel):
    def __init__(self, parent=None):
        super(HeatLabel,self).__init__(parent)
        self.parent=parent
        self.lastviewx=0
        self.lastviewy=0
        self.realx=0
        self.realy=0
        self.realw=0
        self.realh=0
        self.vieww=0
        self.viewh=0
        self.linewidth=0.5
        self.pointSize=5
        self.alpha=0.5
    def createcache(self):
        try:
            self.parent.cacheHeatPixmap=QPixmap(QSize(self.vieww,self.viewh))
            p=QPainter(self.parent.cacheHeatPixmap)
            p.setRenderHint(QPainter.SmoothPixmapTransform)
            p.drawPixmap(QRectF(0,0,self.vieww,self.viewh),self.parent.heatImage,QRectF(self.realx,self.realy,self.realw,self.realh))
            p.end()
            self.parent.usecache=True
            return
        except Exception as e:
            print(e)
    def mousePressEvent(self, event):
        DrawHelper.measureLineMousePress(self,event)
        return super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        DrawHelper.measureLineMove(self,event)
        return super().mouseMoveEvent(event)
    def paintEvent(self, evt):
          super().paintEvent(evt)
        #try:
          if(self.parent.usecacheR==True):
              tmp=QPainter(self)
              tmp.setRenderHint(QPainter.HighQualityAntialiasing)
              tmp.setRenderHint(QPainter.SmoothPixmapTransform)
              tmp.drawPixmap(QPoint(self.lastviewx,self.lastviewy),self.parent.cacheHeatPixmap)
              tmp.end()
              return
          if hasattr(self.parent, 'heatImage')==False or hasattr(self.parent, 'mainImage')==False:
              return
          piw=self.parent.imgLabelR.width()
          pih=self.parent.imgLabelR.height()
          psw=self.parent.scrollAreaR.width()
          psh=self.parent.scrollAreaR.height()
          viewx=self.parent.scrollbarXR.value()-self.parent.imgLabelR.x()
          if viewx<0:
              self.vieww=psw+viewx
              viewx=0              
          else:
              self.vieww=psw
          viewy=self.parent.scrollbarYR.value()-self.parent.imgLabelR.y()
          if viewy<0:
              self.viewh=psh+viewy
              viewy=0
          else:
              self.viewh=psh
          if psw-(piw-viewx)>0:
              self.vieww=piw-viewx
          if psh-(pih-viewy)>0:
              self.viewh=pih-viewy
          if(pih<psh):
              self.viewh=pih
          if(piw<psw):
              self.vieww=piw
          self.realx= int(self.parent.mainImage.width() *viewx/self.parent.imgLabelR.width())
          self.realy= int(self.parent.mainImage.height() *viewy/self.parent.imgLabelR.height())
          self.realh=int(self.parent.mainImage.height() *self.viewh/self.parent.imgLabelR.height())
          self.realw=int(self.parent.mainImage.width() *self.vieww/self.parent.imgLabelR.width())
          self.lastviewx=viewx
          self.lastviewy=viewy

          painter2=QPainter(self)
          DrawHelper.drawHeatMap(self,painter2)
          if self.parent.showgrid:
              painter2.setPen(QPen(QColor(140,140,140),0.5))
              painter2.setRenderHint(QPainter.Antialiasing, False)
              painter2.setCompositionMode(QPainter.CompositionMode_Source)
              bilix = self.parent.mainImage.width() / piw #一个视觉像素相当于N个图片像素
              partlength = math.ceil(4 * bilix * 10)
              for m in range(partlength,partlength + 99):
                 if m % 10 == 0:
                     partlength = m
                     break
              startnum=int(self.realx/partlength)
              shownum=int(self.realw/partlength)+5
              for i in range(startnum,startnum+shownum):
                  if i%2==0:
                      continue
                  realx=i*partlength
                  x=float(round(1.0*realx/bilix))
                  if x<-20:
                      continue
                  painter2.drawLine(x, viewy,  x, viewy+self.viewh)  
                  
              biliy = self.parent.mainImage.height() / pih #一个视觉像素相当于N个图片像素
              partlength = math.ceil(4 * biliy * 10)
              for m in range(partlength,partlength + 99):
                 if m % 10 == 0:
                     partlength = m
                     break
              startnum=int(self.realy/partlength)
              shownum=int(self.realh/partlength)+5
              for i in range(startnum,startnum+shownum):
                  if i%2==0:
                      continue
                  realy=i*partlength
                  y=float(round(1.0*realy/biliy))
                  if y<-20:
                      continue
                  painter2.drawLine(viewx,y, viewx+self.vieww,y)
          DrawHelper.drawLabelGrid(self,painter2,piw,pih)
          DrawHelper.drawDragRect(self,painter2)
          DrawHelper.drawLabels(self,painter2)
          DrawHelper.drawMeasureLine(self,painter2)#绘制测线
          painter2.end()
class DrawHelper(object): 
    @staticmethod
    def drawLabelGrid(self,painter2,piw,pih):
        if self.parent.eventType==6.6:#开启网格标记
              painter2.setPen(QPen(QColor(140,140,140),0.5))
              painter2.setRenderHint(QPainter.Antialiasing, False)
              painter2.setCompositionMode(QPainter.CompositionMode_Source)
              bilix = self.parent.mainImage.width() / piw #一个视觉像素相当于N个图片像素
              viewgridwidth=self.parent.labelGridWidth*piw/self.parent.mainImage.width()
              viewgridheight=self.parent.labelGridHeight*pih/self.parent.mainImage.height()
              xstart=int(self.realx/self.parent.labelGridWidth)-1
              xend=int((self.realx+self.realw)/self.parent.labelGridWidth)+1
              ystart=int(self.realy/self.parent.labelGridHeight)-1
              yend=int((self.realy+self.realh)/self.parent.labelGridHeight)+1
              vxstart=xstart*viewgridwidth
              vxend=xend*viewgridwidth
              vystart=ystart*viewgridheight
              vyend=yend*viewgridheight
              for xx in range(xstart,xend):#垂线
                  painter2.drawLine(xx*viewgridwidth, vystart,  xx*viewgridwidth, vyend)  
              for yy in range(ystart,yend):#水平线
                  painter2.drawLine(vxstart, yy*viewgridheight,  vxend, yy*viewgridheight)  
    def drawMeasureLine(self,painter2):
        if self.parent.eventType==9:#绘制测线
              painter2.setRenderHint(QPainter.Antialiasing)
              painter2.setCompositionMode(QPainter.CompositionMode_Source)   
              font=QFont("Microsoft YaHei",9.5)
              painter2.setFont(font)
              if len(self.parent.measureList)==1:
                  realx_1=self.parent.measureList[0].x()
                  realy_1=self.parent.measureList[0].y()
                  viewx_1=self.width()* realx_1/self.parent.mainImage.width()
                  viewy_1=self.height()* realy_1/self.parent.mainImage.height()
                  painter2.setPen(QPen(QColor(0,0,0),5,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                  painter2.drawPoint(viewx_1,viewy_1)
              if len(self.parent.measureList)==2:
                  painter2.setPen(QPen(QColor(0,0,0),1,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                  realx_1=self.parent.measureList[0].x()
                  realy_1=self.parent.measureList[0].y()
                  viewx_1=self.width()* realx_1/self.parent.mainImage.width()
                  viewy_1=self.height()* realy_1/self.parent.mainImage.height()
                  realx_2=self.parent.measureList[-1].x()
                  realy_2=self.parent.measureList[-1].y()
                  viewx_2=self.width()* realx_2/self.parent.mainImage.width()
                  viewy_2=self.height()* realy_2/self.parent.mainImage.height()
                  painter2.drawLine(viewx_1,viewy_1,viewx_2,viewy_2)
                  pixlength=math.sqrt((realx_2-realx_1)*(realx_2-realx_1)+(realy_2-realy_1)*(realy_2-realy_1))
                  reallength=self.parent.physicalbili*pixlength
                  offsetx=0
                  offsety=0
                  if viewx_2+100>self.width():
                      offsetx=-100
                  if viewy_2-20<0:
                      offsety=30
                  painter2.drawText(viewx_2+10+offsetx,viewy_2-5+offsety,str(round(reallength,2))+"μm")
                  painter2.setPen(QPen(QColor(0,0,0),5,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                  painter2.drawPoint(viewx_1,viewy_1)
                  painter2.drawPoint(viewx_2,viewy_2)
              elif len(self.parent.measureList)==1 and self.parent.tmpMovePoint.x()!=0:
                  painter2.setPen(QPen(QColor(0,0,0),1,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                  realx_1=self.parent.measureList[0].x()
                  realy_1=self.parent.measureList[0].y()
                  viewx_1=self.width()* realx_1/self.parent.mainImage.width()
                  viewy_1=self.height()* realy_1/self.parent.mainImage.height()
                  realx_2=self.parent.tmpMovePoint.x()
                  realy_2=self.parent.tmpMovePoint.y()
                  viewx_2=self.width()* realx_2/self.parent.mainImage.width()
                  viewy_2=self.height()* realy_2/self.parent.mainImage.height()
                  painter2.drawLine(viewx_1,viewy_1,viewx_2,viewy_2)
                  pixlength=math.sqrt((realx_2-realx_1)*(realx_2-realx_1)+(realy_2-realy_1)*(realy_2-realy_1))
                  reallength=self.parent.physicalbili*pixlength
                  offsetx=0
                  offsety=0
                  if viewx_2+100>self.width():
                      offsetx=-100
                  if viewy_2-20<0:
                      offsety=30
                  painter2.drawText(viewx_2+10+offsetx,viewy_2-5+offsety,str(round(reallength,2))+"μm")
                  painter2.setPen(QPen(QColor(0,0,0),5,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                  painter2.drawPoint(viewx_1,viewy_1)
                  painter2.drawPoint(viewx_2,viewy_2)
              else:
                   return
    def drawMeasureRule(self,painter2):
        #绘制测量标尺
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setCompositionMode(QPainter.CompositionMode_Source)   
        font=QFont("Microsoft YaHei",9.5)
        painter2.setFont(font)
        painter2.setPen(QPen(QColor(0,0,0),2,Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
        basex=21+self.parent.scrollArea.horizontalScrollBar().value()
        basey=self.parent.scrollArea.height()-200+self.parent.scrollArea.verticalScrollBar().value()
        print(basey)
        painter2.drawLine(basex,basey,basex+50,basey)
        painter2.drawLine(basex,basey,basex,basey-5)
        painter2.drawLine(basex+50,basey,basex+50,basey-5)


    def drawLabels(self,painter2):
        if len(self.parent.labelList)>0:     
              self.linewidth=self.parent.labelLineWidth*self.parent.currentzoomscale
              self.pointSize=self.parent.labelPointWidth*self.parent.currentzoomscale
              if self.linewidth>5:
                  self.linewidth=5
              if self.pointSize>10:
                  self.pointSize=10
              painter2.setPen(QPen(QColor(140,140,140),0.5))
              painter2.setRenderHint(QPainter.Antialiasing)
              painter2.setCompositionMode(QPainter.CompositionMode_Source)            
              painter2.setPen(QPen(self.parent.currentLabelColor,self.linewidth))
              viewPointList=[]
              for lab in self.parent.labelList: 
                  p=[]
                  for point in lab.pointList:
                     realx=QPointF(point).x()
                     realy=QPointF(point).y()
                     viewx=self.width()* realx/self.parent.mainImage.width()
                     viewy=self.height()* realy/self.parent.mainImage.height()
                     p.append(QPointF(viewx,viewy))
                  viewPointList.append(p)
              #添加临时点
              realx=QPointF(self.parent.tmpMovePoint).x()
              realy=QPointF(self.parent.tmpMovePoint).y()
              viewx=self.width()* realx/self.parent.mainImage.width()
              viewy=self.height()* realy/self.parent.mainImage.height()
              if self.parent.eventType>0 and self.parent.eventType!=6.6:
                viewPointList[-1].append(QPointF(viewx,viewy))
              for i,points in enumerate(viewPointList):
                      labelcolor=self.parent.labelList[i].labelColor
                      labeltype=self.parent.labelList[i].labelType
                      if labeltype==1:#polygon
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap);
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         polygon=QPolygonF(points)
                         if self.parent.eventType<8:
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                 color=QColor(labelcolor)
                                 color.setAlphaF(self.alpha)
                                 brush=QBrush(color)
                                 painter2.setBrush(brush); 
                                 painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                 painter2.drawPolygon(QPolygonF(points))
                         painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                         painter2.setBrush(Qt.NoBrush)
                         painter2.drawPolygon(QPolygonF(points))
                      elif labeltype==7:#polygon
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,2)
                         pen.setCapStyle(Qt.RoundCap)
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         polygon=QPolygonF(points)

                         if self.parent.eventType<8:
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                 color=QColor(labelcolor)
                                 color.setAlphaF(self.alpha)
                                 brush=QBrush(color)
                                 painter2.setBrush(brush); 
                                 painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                 painter2.drawPolygon(QPolygonF(points))
                         painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                         painter2.setBrush(Qt.NoBrush)
                         painter2.drawPolygon(QPolygonF(points))
                      elif labeltype==6.6:#singlegrid
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,2)
                         pen.setCapStyle(Qt.RoundCap)
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         polygon=QPolygonF(points)

                         if self.parent.eventType<8:
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                 color=QColor(labelcolor)
                                 color.setAlphaF(self.alpha)
                                 brush=QBrush(color)
                                 painter2.setBrush(brush); 
                                 painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                 painter2.drawPolygon(QPolygonF(points))

                         painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                         painter2.setBrush(Qt.NoBrush)
                         painter2.drawPolygon(QPolygonF(points))
                      elif labeltype==6.5 :#grid
                         if not self.parent.drawTmpPoint:
                             points=points[0:-1]
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,2)
                         pen.setCapStyle(Qt.RoundCap)
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         polygon=QPolygonF(points)

                         if self.parent.eventType<8:
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                 color=QColor(labelcolor)
                                 color.setAlphaF(self.alpha)
                                 brush=QBrush(color)
                                 painter2.setBrush(brush); 
                                 painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                 painter2.drawPolygon(QPolygonF(points))
                         painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                         painter2.setBrush(Qt.NoBrush)
                         painter2.drawPolygon(QPolygonF(points))
                      elif labeltype==2:#rect
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap)
                         painter2.setPen(pen)
                         painter2.setRenderHint(QPainter.Antialiasing)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         painter2.setRenderHint(QPainter.Antialiasing, False)
                         if len(points)>=2:
                            points=points[:2]

                            if self.parent.eventType<8:
                                polygon=QRectF(QPointF(points[0]),QPointF(points[1]))
                                if polygon.contains(QPointF(viewx,viewy)) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                    painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                    color=QColor(labelcolor)
                                    color.setAlphaF(self.alpha)
                                    brush=QBrush(color)
                                    painter2.setBrush(brush); 
                                    painter2.drawRect(QRectF(QPointF(points[0]),QPointF(points[1])))

                            painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                            painter2.setBrush(Qt.NoBrush)
                            painter2.drawRect(QRectF(QPointF(points[0]),QPointF(points[1])))


                      elif labeltype==3:#circle
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap);
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points[:1]))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         if len(points)>=2:
                            points=points[:2]
                            r=math.sqrt(math.pow(QPointF(points[0]).x()-QPointF(points[1]).x(),2)+math.pow(QPointF(points[0]).y()-QPointF(points[1]).y(),2))
                            if self.parent.eventType<8:
                                distance=math.sqrt(math.pow(QPointF(points[0]).x()-viewx,2)+math.pow(QPointF(points[0]).y()-viewy,2))
                                if distance<r or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                    color=QColor(labelcolor)
                                    color.setAlphaF(self.alpha)
                                    brush=QBrush(color)
                                    painter2.setBrush(brush); 
                                    painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                    painter2.drawEllipse(QPointF(points[0]),r,r)
                            painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                            painter2.setBrush(Qt.NoBrush)
                            painter2.drawEllipse(QPointF(points[0]),r,r)
                      elif labeltype==4:#line
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap);
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))
                         if len(points)>=2:
                            points=points[:2]
                            painter2.drawLine(QPointF(points[0]),QPointF(points[1]))
                      elif labeltype==5:#point
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap);
                         painter2.setPen(pen)
                         if len(points)>0:
                            painter2.drawPoint(QPointF(points[0]))
                      if labeltype==6:#polyline
                         painter2.setRenderHint(QPainter.Antialiasing)
                         pen=QPen(labelcolor,self.pointSize)
                         pen.setCapStyle(Qt.RoundCap);
                         painter2.setPen(pen)
                         painter2.drawPoints(QPolygonF(points))
                         painter2.setPen(QPen(labelcolor,self.linewidth))

                         if self.parent.eventType<8:
                             polygon=QPolygonF(points)
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill) or i==len(viewPointList)-1 or i==self.parent.highlightLabelIndex:
                                 color=QColor(labelcolor)
                                 color.setAlphaF(self.alpha)
                                 brush=QBrush(color)
                                 painter2.setBrush(brush); 
                                 painter2.setCompositionMode(QPainter.CompositionMode_Multiply)
                                 painter2.drawPolygon(QPolygonF(points))
                         painter2.setCompositionMode(QPainter.CompositionMode_Source) 
                         painter2.setBrush(Qt.NoBrush)
                         painter2.drawPolyline(QPolygonF(points))   
    def drawHeatMap(self,painter):
        w=self.parent.lastImgSize.width()
        h=self.parent.lastImgSize.height()
        for i,point in enumerate(self.parent.heatDataList):
            realx=point.x()*self.parent.actualGridwidth
            realy=point.y()*self.parent.actualGridheight
            endx=realx+self.parent.actualGridwidth
            endy=realy+self.parent.actualGridheight
            viewx=round(self.width()* realx/w)
            viewy=round(self.height()* realy/h)
            viewx2=round(self.width()* endx/w)
            viewy2=round(self.height()* endy/h)
            painter.fillRect(viewx,viewy,viewx2-viewx,viewy2-viewy,self.parent.heatDataColorList[i])
    def drawDragRect(self,painter2):
        if self.parent.eventType==8 and self.parent.ifDrawRect==True:#绘制拖拽矩形
              painter2.setCompositionMode(QPainter.CompositionMode_Clear)
              painter2.setPen(QPen(QColor(0,0,0),1,Qt.DashLine,Qt.RoundCap, Qt.RoundJoin))
              realx=self.parent.startMovePoint.x()
              realy=self.parent.startMovePoint.y()
              viewxstart=realx
              viewystart=realy
              realx=self.parent.endMovePoint.x()
              realy=self.parent.endMovePoint.y()
              viewxend=realx
              viewyend=realy
              painter2.drawRect(QRect(QPoint(viewxstart,viewystart),QPoint(viewxend,viewyend)))
    def measureLineMove(self,event):
        if self.parent.eventType==9:#测量功能记录两个点
            if(len(self.parent.measureList)!=1):
                return
            x=event.pos().x()
            y=event.pos().y()
            if x>0 and y>0:
                realx=self.parent.mainImage.width()* x/self.parent.imgLabel.width()
                realy=self.parent.mainImage.height()* y/self.parent.imgLabel.height()
                self.parent.tmpMovePoint=QPointF(realx,realy)
                self.parent.imgLabel.repaint()
                self.parent.imgLabelR.repaint()
    def measureLineMousePress(self, event):
        if self.parent.eventType==9:#测量功能记录两个点
            x=event.pos().x()
            y=event.pos().y()
            realx=self.parent.mainImage.width()* x/self.parent.imgLabel.width()
            realy=self.parent.mainImage.height()* y/self.parent.imgLabel.height()
            if(len(self.parent.measureList)<2):
               self.parent.tmpMovePoint=QPoint(0,0)
               self.parent.measureList.append(QPoint(realx,realy))
            else:
               self.parent.measureList.clear()
               self.parent.measureList.append(QPoint(realx,realy))
            self.parent.imgLabel.repaint()
            self.parent.imgLabelR.repaint()
class XLabel(QLabel):
    def __init__(self, parent=None):
        super(XLabel,self).__init__(parent)
        self.parent = parent
        self.txtPen=QPen(QColor(165,165,165))
        self.linePen=QPen(QColor(97,97,97))
    def paintEvent(self, evt):
          super().paintEvent(evt)
          if not hasattr(self.parent, 'mainImage'):
              return
          painter = QPainter(self)
          painter.setPen(self.linePen)
          painter.setFont(QFont("Microsoft YaHei",6));
          painter.drawLine(0, 17, self.width(), 17)

          piw = self.parent.imgLabel.width()
          pih = self.parent.imgLabel.height()
          psw = self.parent.scrollArea.width()
          psh = self.parent.scrollArea.height()

          viewx=self.parent.scrollbarX.value()-self.parent.imgLabel.x()
          if viewx<0:
              self.vieww=psw+viewx
              viewx=0              
          else:
              self.vieww=psw
          viewy=self.parent.scrollbarY.value()-self.parent.imgLabel.y()
          if viewy<0:
              self.viewh=psh+viewy
              viewy=0
          else:
              self.viewh=psh
          self.realx= int(self.parent.mainImage.width() *viewx/self.parent.imgLabel.width())
          self.realy= int(self.parent.mainImage.height() *viewy/self.parent.imgLabel.height())
          self.realw=int(self.parent.mainImage.width() *self.vieww/self.parent.imgLabel.width())

          startx = self.parent.imgLabel.x()-self.parent.scrollbarX.value()
          bilix = self.parent.mainImage.width() / piw #一个视觉像素相当于N个图片像素
          partlength = math.ceil(4 * bilix * 10)
          for m in range(partlength,partlength + 99):
             if m % 10 == 0:
                 partlength = m
                 break
          startnum=int(self.realx/partlength)
          shownum=int(self.realw/partlength)+5
          for i in range(startnum,startnum+shownum):
              realx=i*partlength
              x=float(round(1.0*realx/bilix))

              if startx+x<-20:
                  continue

              s=str(int(i*partlength*self.parent.largeScale))
              painter.setPen(self.txtPen)
              painter.drawText(startx+x+2,11,s)
              painter.setPen(self.linePen)
              painter.drawLine(startx + x, 0, startx + x, 17)
              if(startx+1>self.width()+50):
                  break

              for m in range(0,9):
                  realx=realx+partlength/10
                  x=round(1.0*realx/bilix)+startx
                  if not m%2==0:
                      painter.drawLine(x,11,x,17)
                  else:
                      painter.drawLine(x,13,x,17)

          mainLineNum =math.ceil(float(startx) * bilix / partlength)+5;
          for i in range(0,mainLineNum):
              realx=i*partlength
              x=startx- float(round(1.0*realx/bilix))
              s=str(int(i*partlength*self.parent.largeScale))
              painter.setPen(self.txtPen)
              painter.drawText(x+2,11,s)
              painter.setPen(self.linePen)
              painter.drawLine(x, 0, x, 17)

              for m in range(0,9):
                  realx=realx+partlength/10
                  x=startx-round(1.0*realx/bilix)
                  if not m%2==0:
                      painter.drawLine(x,11,x,17)
                  else:
                      painter.drawLine(x,13,x,17)

          painter.end()          
class YLabel(QLabel):
    def __init__(self, parent=None):
        super(YLabel,self).__init__(parent)
        self.parent = parent
        self.txtPen=QPen(QColor(165,165,165))
        self.linePen=QPen(QColor(97,97,97))
    def paintEvent(self, evt):
          super().paintEvent(evt)
          if not hasattr(self.parent, 'mainImage'):
              return
          painter = QPainter(self)
          painter.setPen(self.linePen)
          font=QFont("Microsoft YaHei",6)
          painter.setFont(font);
          painter.drawLine(17, 17,  17,self.height())


          piw = self.parent.imgLabel.width()
          pih = self.parent.imgLabel.height()
          psw = self.parent.scrollArea.width()
          psh = self.parent.scrollArea.height()
          viewx=self.parent.scrollbarX.value()-self.parent.imgLabel.x()
          if viewx<0:
              self.vieww=psw+viewx
              viewx=0              
          else:
              self.vieww=psw
          viewy=self.parent.scrollbarY.value()-self.parent.imgLabel.y()
          if viewy<0:
              self.viewh=psh+viewy
              viewy=0
          else:
              self.viewh=psh
          self.realy= int(self.parent.mainImage.height() *viewy/self.parent.imgLabel.height())
          self.realw=int(self.parent.mainImage.width() *self.vieww/self.parent.imgLabel.width())
          self.realh=int(self.parent.mainImage.height() *self.viewh/self.parent.imgLabel.height())


          #realh=self.parent.mainImage.height()
          starty = self.parent.imgLabel.y()-self.parent.scrollbarY.value()
          biliy = self.parent.mainImage.height() / pih #一个视觉像素相当于N个图片像素
          partlength = math.ceil(4 * biliy * 10)
          for m in range(partlength,partlength + 99):
             if m % 10 == 0:
                 partlength = m
                 break
          #mainLineNum = (int)(math.ceil(float(realh)/ partlength)) + math.ceil(float(pih) * biliy / partlength)+50;
          startnum=int(self.realy/partlength)
          shownum=int(self.realh/partlength)+5
          for i in range(startnum,startnum+shownum):
              realy=i*partlength
              y=float(round(1.0*realy/biliy))
              if starty+y<-20:
                  continue
              s=str(int(i*partlength*self.parent.largeScale))
           
              painter.rotate(90)
              painter.setPen(self.txtPen)
              painter.drawText(starty+y+4,-2,s)
              painter.resetTransform()
              painter.setPen(self.linePen)
              painter.drawLine(0,starty + y, 17,starty + y)
              

              for m in range(0,9):
                  realy=realy+partlength/10
                  y=round(1.0*realy/biliy)+starty
                  if not m%2==0:
                      painter.drawLine(11,y,17,y)
                  else:
                      painter.drawLine(13,y,17,y)

          mainLineNum =math.ceil(float(starty) * biliy / partlength)+5;
          for i in range(0,mainLineNum):
              realy=i*partlength
              y=starty- float(round(1.0*realy/biliy))
              s=str(int(i*partlength*self.parent.largeScale))
              painter.rotate(90)
              painter.setPen(self.txtPen)
              painter.drawText(y+4,-2,s)
              painter.resetTransform()
              painter.setPen(self.linePen)
              painter.drawLine( 0, y, 17,y)

              for m in range(0,9):
                  realy=realy+partlength/10
                  y=starty-round(1.0*realy/biliy)
                  if not m%2==0:
                      painter.drawLine(11,y,17,y)
                  else:
                      painter.drawLine(13,y,17,y)
          painter.fillRect(0,0,18,18,QColor(83,83,83))
          painter.end()
class MyScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super(MyScrollArea,self).__init__(parent)
        self.parent=parent
        self.lastX=0;
        self.lastY=0;
        self.startPoint=None
        self.candraw=False
        self.ifspacekey=False
    def resizeEvent(self, a0):
        left=80
        bottom=80
        if self.parent.imgLabel.width()<self.width():
            self.parent.measureLabel.move(left,self.height()-bottom)
        else:
            self.parent.measureLabel.move(left,self.height()-bottom-20)
        return super().resizeEvent(a0)
    def wheelEvent(self, evt):
        if self.parent.allowScroll==True:
            super().wheelEvent(evt)
        else:
            scroll=evt.angleDelta();
            if scroll.y() > 0:
                self.parent.zoomIn()
            else:
                self.parent.zoomOut()
            return
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z and self.parent.eventType!=0:
            if len(self.parent.labelList[-1].pointList)>0:
                self.parent.labelList[-1].pointList.pop()
                self.parent.imgLabel.repaint()
                self.parent.imgLabelR.repaint()
                return
        if event.key() == Qt.Key_Control:
            self.parent.allowScroll=False
        elif event.key() == Qt.Key_Space:
            self.ifspacekey=True
    def keyReleaseEvent(self,event):
        if(event.key() == Qt.Key_Control):
            self.parent.allowScroll=True
        elif event.key() == Qt.Key_Space:
            self.ifspacekey=False
    def mouseMoveEvent(self, event):
        if self.parent.eventType==9:#测量功能记录两个点
            return super().mouseMoveEvent(event)
        if event.buttons() == QtCore.Qt.LeftButton and (self.parent.eventType==0 or self.parent.eventType==6.6):
            if self.lastY == 0:
                self.lastY = event.pos().y()
            if self.lastX == 0:
                self.lastX = event.pos().x()     
            distanceX = self.lastX - event.pos().x()
            distanceY = self.lastY - event.pos().y()
            self.lastX = event.pos().x()
            self.lastY = event.pos().y()  
            if(self.parent.viewMode==2):   
                self.parent.scrollbarXR.setValue(self.parent.scrollbarXR.value() + distanceX)
                self.parent.scrollbarYR.setValue(self.parent.scrollbarYR.value() + distanceY)
            else:
                self.parent.scrollbarX.setValue(self.parent.scrollbarX.value() + distanceX)
                self.parent.scrollbarY.setValue(self.parent.scrollbarY.value() + distanceY)
            self.parent.thumbnailLabel.move(self.parent.thumbposition)
            return 
        elif self.parent.eventType!=0 and self.ifspacekey==True and event.buttons() == QtCore.Qt.LeftButton:
            if self.lastY == 0:
                self.lastY = event.pos().y()
            if self.lastX == 0:
                self.lastX = event.pos().x()     
            distanceX = self.lastX - event.pos().x()
            distanceY = self.lastY - event.pos().y()
            self.lastX = event.pos().x()
            self.lastY = event.pos().y()  
            if(self.parent.viewMode==2):   
                self.parent.scrollbarXR.setValue(self.parent.scrollbarXR.value() + distanceX)
                self.parent.scrollbarYR.setValue(self.parent.scrollbarYR.value() + distanceY)
            else:
                self.parent.scrollbarX.setValue(self.parent.scrollbarX.value() + distanceX)
                self.parent.scrollbarY.setValue(self.parent.scrollbarY.value() + distanceY)
            self.parent.thumbnailLabel.move(self.parent.thumbposition)
            return 
        elif self.parent.eventType==6.6:
            viewx=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
            viewy=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
            realx= int(self.parent.mainImage.width() *viewx/self.parent.imgLabel.width())
            realy= int(self.parent.mainImage.height() *viewy/self.parent.imgLabel.height())
            x=math.floor(realx/self.parent.labelGridWidth)*self.parent.labelGridWidth
            y=math.floor(realy/self.parent.labelGridHeight)*self.parent.labelGridHeight
            self.parent.labelList[-1].pointList=[]
            gc.collect()
            self.parent.labelList[-1].pointList.append(QPointF(x,y))
            self.parent.labelList[-1].pointList.append(QPointF(x+self.parent.labelGridWidth,y))
            self.parent.labelList[-1].pointList.append(QPointF(x+self.parent.labelGridWidth,y+self.parent.labelGridHeight))
            self.parent.labelList[-1].pointList.append(QPointF(x,y+self.parent.labelGridHeight))
            self.parent.labelList[-1].labelColor=self.parent.currentLabelColor
            #print(self.parent.labelList[-1].pointList)
            self.parent.imgLabel.repaint()
        else:
            x=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
            y=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
            realx=self.parent.mainImage.width()* x/self.parent.imgLabel.width()
            realy=self.parent.mainImage.height()* y/self.parent.imgLabel.height()
            if self.candraw==True and self.parent.eventType==7 and self.ifspacekey==False:
                self.parent.labelList[-1].pointList.append(QPointF(realx,realy))
                self.parent.labelList[-1].labelColor=self.parent.currentLabelColor
            self.parent.tmpMovePoint=QPointF(realx,realy)
            self.parent.endMovePoint=QPointF(x,y)
            self.parent.imgLabel.repaint()
            self.parent.imgLabelR.repaint()
        return super().mouseMoveEvent(event)
    def mouseReleaseEvent(self, event):
        self.lastY = 0
        self.lastX = 0     
        if self.parent.eventType==8:
             self.parent.ifDrawRect=False
             width=abs(self.parent.startMovePoint.x()-self.parent.endMovePoint.x())
             height=abs(self.parent.startMovePoint.y()-self.parent.endMovePoint.y())
             if height<5 or width<5:
                 return
             biliold=1.0*self.parent.imgLabel.width()/self.parent.mainImage.width()
             bili=biliold*1.0* (self.parent.scrollArea.height()-10)/height
  
             bilix=int((self.parent.startMovePoint.x()+self.parent.endMovePoint.x())/2)/self.parent.imgLabel.width()
             biliy=int((self.parent.startMovePoint.y()+self.parent.endMovePoint.y())/2)/self.parent.imgLabel.height()

             self.parent.zoomOther(str(bili),True)
             realx=int(bilix*self.parent.imgLabel.width()+self.parent.edgesizex-self.parent.scrollArea.width()/2)
             realy=int(biliy*self.parent.imgLabel.height()+self.parent.edgesizey-self.parent.scrollArea.height()/2)

             self.parent.scrollArea.horizontalScrollBar().setValue(realx)
             self.parent.scrollArea.verticalScrollBar().setValue(realy)
             self.drawLabel(0)
             

        return super().mouseReleaseEvent(event)
    def mousePressEvent(self, event):
        viewx=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
        viewy=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
        self.highlightItem(viewx,viewy)#高亮选中标记列表
        #if self.parent.eventType==9:#测量功能记录两个点
        #    x=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
        #    y=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
        #    realx=self.parent.mainImage.width()* x/self.parent.imgLabel.width()
        #    realy=self.parent.mainImage.height()* y/self.parent.imgLabel.height()
        #    if(len(self.parent.measureList)<2):
        #       self.parent.tmpMovePoint=QPoint(0,0)
        #       self.parent.measureList.append(QPoint(realx,realy))
        #    else:
        #       self.parent.measureList.clear()
        #       self.parent.measureList.append(QPoint(realx,realy))
        #    self.parent.imgLabel.repaint()
        #    self.parent.imgLabelR.repaint()
        #    return super().mousePressEvent(event)
        if self.parent.eventType==8 and event.buttons() == QtCore.Qt.LeftButton:
            self.parent.ifDrawRect=True
            x=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
            y=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
            self.parent.startMovePoint=QPoint(x,y)
            return super().mousePressEvent(event)
        elif self.parent.eventType==6.6:
            return super().mousePressEvent(event)
        elif self.parent.eventType>0 and self.parent.eventType<8 and event.buttons() == QtCore.Qt.LeftButton:#绘制图形
            self.parent.isdrawing=True#正在绘制
            if self.parent.eventType==7:
                self.candraw=True #允许画笔拾取点
            else:
                self.candraw=False
            x=event.pos().x()-self.parent.imgLabel.x() +self.parent.scrollbarX.value()
            y=event.pos().y()-self.parent.imgLabel.y() +self.parent.scrollbarY.value()
            realx=self.parent.mainImage.width()* x/self.parent.imgLabel.width()
            realy=self.parent.mainImage.height()* y/self.parent.imgLabel.height()
            if self.ifspacekey==False:
                self.parent.labelList[-1].pointList.append(QPointF(realx,realy))
                self.parent.labelList[-1].labelColor=self.parent.currentLabelColor
            self.parent.imgLabel.repaint()
            self.parent.imgLabelR.repaint()
            eventType=self.parent.eventType
            if (eventType==2 or eventType==3  or eventType==4) and len(self.parent.labelList[-1].pointList)==2 and self.ifspacekey==False:#矩形、圆限定两个点
                self.showLabelDlg(self.parent)
                return
            elif eventType==5  and len(self.parent.labelList[-1].pointList)==1 and self.ifspacekey==False:#点
                self.showLabelDlg(self.parent)
                return
            return 
        return super().mousePressEvent(event)
    def mouseDoubleClickEvent(self, event):
      try:
        if self.parent.eventType==6.5:
            gridwidth=self.parent.gridwidth
            gridheight=self.parent.gridheight
            realpoints=self.parent.labelList[-1].pointList
            realpolygon=QPolygonF(realpoints)
            minx=1000000
            maxx=0
            miny=1000000
            maxy=0
            for smallp in realpoints:
                realx=QPointF(smallp).x()
                realy=QPointF(smallp).y()
                maxx= realx if realx>maxx else maxx
                minx= realx if realx<minx else minx
                maxy=realy if realy>maxy else maxy
                miny=realy if realy<miny else miny
            minx=int(minx/gridwidth)-1
            maxx=int(maxx/gridwidth)+1
            miny=int(miny/gridheight)-1
            maxy=int(maxy/gridheight)+1
            tmppoints=[]
            for xx in range(minx,maxx):
                for yy in range(miny,maxy):
                    for ii in range(0,gridwidth,5):
                        iscontain=False
                        for jj in range(0,gridheight,5):
                            if realpolygon.containsPoint(QPointF(gridwidth*xx+ii,gridheight*yy+jj),Qt.OddEvenFill):
                                iscontain=True
                                #realx=xx*320
                                #realy=yy*320
                                #viewx=self.parent.imgLabel.width()* realx/self.parent.mainImage.width()
                                #viewy=self.parent.imgLabel.height()* realy/self.parent.mainImage.height()
                                #viewwidth=self.parent.imgLabel.width()* 320/self.parent.mainImage.width()
                                #viewheight=self.parent.imgLabel.height()* 320/self.parent.mainImage.height()       
                                #self.parent.tmpPath.addRect(QRectF(viewx,viewy,viewwidth,viewheight))
                                tmppoints.append(QPoint(xx,yy))
                                break;
                        if iscontain:
                            break
            minx=100000
            maxx=0
            miny=100000
            maxy=0
            for p in tmppoints:
                x=QPoint(p).x()
                y=QPoint(p).y()
                maxx= x if x>maxx else maxx
                minx= x if x<minx else minx
                maxy=y if y>maxy else maxy
                miny=y if y<miny else miny
            maxx=maxx+1
            maxy=maxy+1
            existpoint=[]
            #计算顶部线条
            toppoints=[]
            for xx in range(minx,maxx):
                tmpy=100000
                for p in tmppoints:
                    if p.x()==xx:
                        if p.y()<tmpy:  
                            tmpy=p.y()
                isexist=False
                for ep in existpoint:
                    if ep.x()==xx and ep.y()==tmpy:
                        isexist=True
                        break
                #isexist=False

                toppoints.append(QPoint(xx*gridwidth,tmpy*gridheight))
                toppoints.append(QPoint(xx*gridwidth+gridwidth,tmpy*gridheight))
                existpoint.append(QPoint(xx,tmpy))
            #计算底部线条  
            bottompoints=[]
            for xx in range(minx,maxx):
                tmpy=0
                for p in tmppoints:
                    if p.x()==xx:
                        if p.y()>tmpy:
                            tmpy=p.y()
                isexist=False
                for ep in existpoint:
                    if ep.x()==xx and ep.y()==tmpy:
                        isexist=True
                        break

                bottompoints.append(QPoint(xx*gridwidth,tmpy*gridheight+gridheight))
                bottompoints.append(QPoint(xx*gridwidth+gridwidth,tmpy*gridheight+gridheight))
                existpoint.append(QPoint(xx,tmpy))
            bottompoints.reverse()
            #计算左侧线条
            leftpoints=[]
            for yy in range(miny,maxy):
                tmpx=100000
                for p in tmppoints:
                    if p.y()==yy:
                        if p.x()<tmpx:
                            tmpx=p.x()
                isexist=False
                for ep in existpoint:
                    if ep.x()==tmpx and ep.y()==yy:
                        isexist=True
                        break
                #isexist=False
                
                leftpoints.append(QPoint(tmpx*gridwidth,yy*gridheight))
                leftpoints.append(QPoint(tmpx*gridwidth,yy*gridheight+gridheight))
                existpoint.append(QPoint(tmpx,yy))
            leftpoints.reverse()
            #计算右侧线条
            rightpoints=[]
            for yy in range(miny,maxy):
                tmpx=0
                for p in tmppoints:
                    if p.y()==yy:
                        if p.x()>tmpx:
                            tmpx=p.x()
                isexist=False
                for ep in existpoint:
                    if ep.x()==tmpx and ep.y()==yy:
                        isexist=True
                        break
                rightpoints.append(QPoint(tmpx*gridwidth+gridwidth,yy*gridheight))
                rightpoints.append(QPoint(tmpx*gridwidth+gridwidth,yy*gridheight+gridheight))
                existpoint.append(QPoint(tmpx,yy))
            for i,point in enumerate(rightpoints):
                if point==toppoints[-1]:
                    rightpoints=rightpoints[i:]
                    break;
            for i,point in enumerate(rightpoints):
                if point==bottompoints[0]:
                    rightpoints=rightpoints[:i]
                    break;
            #for i,point in enumerate(bottompoints):
            #    if point==rightpoints[-1]:
            #        bottompoints=bottompoints[i:]
            #        break;
            for i,point in enumerate(leftpoints):
                if point==bottompoints[-1]:
                    leftpoints=leftpoints[i:]
                    break;
            for i,point in enumerate(toppoints):
                if point==leftpoints[-1]:
                    toppoints=toppoints[i:]
                    break;

            toppoints.extend(rightpoints)
            toppoints.extend(bottompoints)
            toppoints.extend(leftpoints)
            #resultpoints=toppoints[0:-1]
            self.parent.labelList[-1].pointList.clear()
            #gc.collect()
            self.parent.labelList[-1].pointList=toppoints
            self.parent.drawTmpPoint=False
            self.parent.imgLabel.repaint()
            self.parent.imgLabelR.repaint()
        if self.parent.eventType!=0 and self.parent.eventType!=8:
            self.candraw=False
            self.showLabelDlg(self.parent)
        return super().mouseDoubleClickEvent(event)
      except:
        return
        #return super().mousedoubleclickevent(event)
    def showLabelDlg(self,parent):
        self.parent.isdrawing=False
        if len(parent.labelList[-1].pointList)<2 and parent.eventType!=5:
            return
        self.parent.imgLabel.repaint()
        self.parent.imgLabelR.repaint()
        dlg=LabelDlg()
        labelnames=[]
        for label in parent.labelList:
            if not label.labelName in labelnames:
                dlg.labelNameEdit.addItem(label.labelName)
                labelnames.append(label.labelName)
        dlg.labelNameEdit.setCurrentText("")
        result=dlg.exec_()
        if result==1:
            labelname=dlg.labelNameEdit.currentText()
            labeldes=dlg.labelDesEdit.toPlainText()
            parent.labelList[-1].labelName=labelname
            parent.labelList[-1].labelDes=labeldes

            lab=Label()
            lab.pointList=[]
            lab.labelColor=parent.currentLabelColor
            lab.labelType=parent.eventType
            lab.shapeType=parent.currentShapeType
            parent.labelList.append(lab)

            ItemModel =QStandardItemModel();
            pixmap=QPixmap(2000,2)
            pixmap.fill(QColor(40,40,40))
            painter=QPainter(pixmap)
            for label in parent.labelList[0:-1]:
                labelname=label.labelName
                item=QStandardItem("    "+labelname)
                painter.fillRect(QRect(0,0,10,2),QColor(label.labelColor))
                item.setBackground(QBrush(pixmap))
                #item.setBackground(QBrush(QColor(label.labelColor)))
                ItemModel.appendRow(item)
            painter.end()
            parent.labellistWidget.setModel(ItemModel)
        else:
            parent.labelList.pop()
            lab=Label()
            lab.pointList=[]
            lab.labelColor=parent.currentLabelColor
            lab.labelType=parent.eventType
            parent.labelList.append(lab)
        self.parent.tmpMovePoint=QPoint(0,0)
        self.parent.imgLabel.repaint()
        self.parent.imgLabelR.repaint()
        self.parent.drawTmpPoint=True
        return True
    def drawLabel(self,type):
        self.parent.eventType=type
        self.parent.scrollArea.setCursor(Qt.PointingHandCursor)
        self.parent.scrollAreaR.setCursor(Qt.PointingHandCursor)
        self.parent.moveTool.setChecked(True)
        self.parent.polygonTool.setChecked(False)
        self.parent.rectTool.setChecked(False)
        self.parent.circleTool.setChecked(False)
        self.parent.lineTool.setChecked(False)
        self.parent.pointTool.setChecked(False)
        self.parent.multiLineTool.setChecked(False)
        self.parent.zoomInRectTool.setChecked(False)
        self.parent.brushTool.setChecked(False)
        return
    def highlightItem(self,viewx,viewy):
        if self.parent.eventType!=0:
            return
        viewPointList=[]
        for lab in self.parent.labelList: 
            p=[]
            for point in lab.pointList:
                realx=QPointF(point).x()
                realy=QPointF(point).y()
                vx=self.parent.imgLabel.width()* realx/self.parent.mainImage.width()
                vy=self.parent.imgLabel.height()* realy/self.parent.mainImage.height()
                p.append(QPointF(vx,vy))
            viewPointList.append(p)
        self.parent.highlightLabelIndex=-1
        for i,points in enumerate(viewPointList):
                      if len(points)<2:
                          continue
                      labeltype=self.parent.labelList[i].labelType
                      if labeltype==6 or labeltype==6.5 or labeltype==6.6 or labeltype==7 or labeltype==1:#grid
                         polygon=QPolygonF(points)
                         if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill):
                               self.parent.highlightLabelIndex=i;
                               idx=self.parent.labellistWidget.model().index(i,0)
                               self.parent.labellistWidget.setCurrentIndex(idx)
                      elif labeltype==2:#rect
                            polygon=QRectF(QPointF(points[0]),QPointF(points[1]))
                            if polygon.contains(QPointF(viewx,viewy)):
                               self.parent.highlightLabelIndex=i;
                               idx=self.parent.labellistWidget.model().index(i,0)
                               self.parent.labellistWidget.setCurrentIndex(idx)
                      elif labeltype==3:#circle
                            r=math.sqrt(math.pow(QPointF(points[0]).x()-QPointF(points[1]).x(),2)+math.pow(QPointF(points[0]).y()-QPointF(points[1]).y(),2))
                            distance=math.sqrt(math.pow(QPointF(points[0]).x()-viewx,2)+math.pow(QPointF(points[0]).y()-viewy,2))
                            if distance<r:
                               self.parent.highlightLabelIndex=i;
                               idx=self.parent.labellistWidget.model().index(i,0)
                               self.parent.labellistWidget.setCurrentIndex(idx)
                      if labeltype==6:#polyline
                             polygon=QPolygonF(points)
                             if polygon.containsPoint(QPointF(viewx,viewy),Qt.OddEvenFill):
                               self.parent.highlightLabelIndex=i;
                               idx=self.parent.labellistWidget.model().index(i,0)
                               self.parent.labellistWidget.setCurrentIndex(idx)
        
        self.parent.imgLabel.repaint()
        self.parent.imgLabelR.repaint()
class ColorBarWidget(QLabel):
    def __init__(self, parent=None):
        super(ColorBarWidget,self).__init__(parent)
        self.parent = parent
        self.barList=[]#滑块实体
        self.colorList=[]
        self.offset=8-6+1
        self.offsetR=8-6-1
        self.barLength=self.parent.gradientLabel.width()
        self.initEdgeBars()
        self.selectedBar=None
        self.minx=0
        self.maxx=0
        self.currentSelectedIndex=-1
        self.gradientPixmap=None

    def mousePressEvent(self, event):###########bar点击事件
        needcreate=True
        for i,b in enumerate(self.barList):
            x=b.x()
            if event.pos().x()>=x and event.pos().x()<=x+11:
                self.selectedBar=b
                self.setSelectedColor(b)
                self.currentSelectedIndex=i
                x=b.x()+2
                po=int(100*x/self.parent.gradientLabel.width())
                self.parent.positionEdit.setText(str(po))
                needcreate=False
            else:
                self.cancelSelectedColor(b)

        if needcreate:
            self.bar=QLabel(self)
            self.barList.append(self.bar)
            self.colorList.append(self.parent.currentColor)
            self.currentSelectedIndex=len(self.colorList)-1
            self.bar.resize(11,17)
            self.setBarColor(self.bar,self.parent.currentColor)
            self.bar.move(event.pos().x()-6,0)
            po=int(100*event.pos().x()/self.parent.gradientLabel.width())
            self.parent.positionEdit.setText(str(po))
            self.bar.show()#不show看不到
            self.selectedBar=self.bar
            self.setSelectedColor(self.bar)
            self.drawGradient()
        return super().mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        self.selectedBar=None
        return super().mouseReleaseEvent(event)
    def mouseMoveEvent(self, event):
        if self.currentSelectedIndex==-1:
            return
        if event.buttons() == QtCore.Qt.LeftButton :
            if(self.selectedBar!=None):
                if self.currentSelectedIndex<2:#边上两个滑块不可动
                    return
                if (event.pos().x()+6>406) or (event.pos().x()-16<2):
                    self.selectedBar.deleteLater()
                    self.barList.pop(self.currentSelectedIndex)
                    self.colorList.pop(self.currentSelectedIndex)
                    self.currentSelectedIndex=-1
                self.selectedBar.move(event.pos().x()-6,0)
                po=int(100*event.pos().x()/self.parent.gradientLabel.width())
                self.parent.positionEdit.setText(str(po))
                self.update()
                self.drawGradient()
    def initEdgeBars(self):
        self.barLeft=QLabel(self)
        self.barLeft.resize(11,17)
        self.setBarColor(self.barLeft,QColor(255,255,0))
        self.barLeft.move(2,0)
        self.barList.append(self.barLeft)
        self.colorList.append(QColor(255,255,0))
        self.minx=self.offset
        self.barRight=QLabel(self)
        self.barRight.resize(11,17)
        self.barRight.move(410,0)
        self.setBarColor(self.barRight,QColor(255,0,0))
        self.colorList.append(QColor(255,0,0))
        self.barList.append(self.barRight)
        self.maxx=self.offsetR+self.barLength
    def setBarColor(self,bar,color):
        pixmap=QPixmap("img/colorbar.bmp")
        #pixmap=bar.pixmap()
        painter=QPainter(pixmap)
        painter.fillRect(2,8,7,7,QBrush(color))
        painter.end()
        bar.setPixmap(pixmap)
    def changeBarColor(self,color):
        if self.currentSelectedIndex==-1:
            return
        bar=self.barList[self.currentSelectedIndex]
        #pixmap=QPixmap("img/colorbar.bmp")
        pixmap=bar.pixmap()
        painter=QPainter(pixmap)
        painter.fillRect(2,8,7,7,QBrush(color))
        painter.end()
        bar.setPixmap(pixmap)
        self.colorList[self.currentSelectedIndex]=color
    def setSelectedColor(self,bar):
        color=QColor(102,102,102)
        pixmap=bar.pixmap()
        #pixmap=QPixmap("img/colorbar.bmp")
        painter=QPainter(pixmap)
        painter.fillRect(5,1,1,1,QBrush(color))
        painter.fillRect(4,2,3,1,QBrush(color))
        painter.fillRect(3,2,5,1,QBrush(color))
        painter.fillRect(2,3,7,1,QBrush(color))
        painter.fillRect(1,4,9,1,QBrush(color))

        color=QColor(0,0,0)
        painter.fillRect(0,5,11,1,QBrush(color))
        painter.drawPoint(1,4)
        painter.drawPoint(2,3)
        painter.drawPoint(3,2)
        painter.drawPoint(4,1)
        painter.drawPoint(5,0)
        painter.drawPoint(9,4)
        painter.drawPoint(8,3)
        painter.drawPoint(7,2)
        painter.drawPoint(6,1)
        painter.end()
        bar.setPixmap(pixmap)
    def cancelSelectedColor(self,bar):
        color=QColor(237,237,237)
        pixmap=bar.pixmap()
        #pixmap=QPixmap("img/colorbar.bmp")
        painter=QPainter(pixmap)
        painter.fillRect(5,1,1,1,QBrush(color))
        painter.fillRect(3,2,3,1,QBrush(color))
        painter.fillRect(2,3,5,1,QBrush(color))
        painter.fillRect(1,4,7,1,QBrush(color))
        painter.fillRect(1,5,9,1,QBrush(color))

        color=QColor(158,158,158)
        painter.fillRect(1,6,9,1,QBrush(color))
        color=QColor(102,102,102)
        painter.drawPoint(1,4)
        painter.drawPoint(2,3)
        painter.drawPoint(3,2)
        painter.drawPoint(4,1)
        painter.drawPoint(5,0)
        painter.drawPoint(9,4)
        painter.drawPoint(8,3)
        painter.drawPoint(7,2)
        painter.drawPoint(6,1)
        painter.drawPoint(0,6)
        painter.drawPoint(10,6)
        painter.end()
        bar.setPixmap(pixmap)
    def drawGradient(self):
        pixmap=QPixmap(self.parent.gradientLabel.width()-2,self.parent.gradientLabel.height()-2)
        painter=QPainter(pixmap);
        painter.setRenderHint(QPainter.Antialiasing,True);
        linearGradient=QLinearGradient(0,10,pixmap.width(),10)
        self.parent.resultList.clear()
        for i,bar in enumerate(self.barList):
            position=1.0*(bar.x()-2)/self.parent.gradientLabel.width() 
            if position<0 or id==0:
                position=0
            if position>1 or i==1:
                position=1
            linearGradient.setColorAt(position,self.colorList[i])
            gra=GradientPart()#添加到结果集
            gra.position=position
            gra.color=self.colorList[i]
            self.parent.resultList.append(gra)
        painter.setBrush(linearGradient)
        painter.setPen(Qt.transparent);
        painter.drawRect(0,0,pixmap.width(),pixmap.height())
        painter.end()
        
        self.parent.gradientLabel.setPixmap(pixmap)#渐变条颜色设置
    def deleteBar(self):
        #print(self.selectedBar)
        if self.currentSelectedIndex==-1:
            return
        ##if self.selectedBar!=None:
        #self.selectedBar.deleteLater()
        self.barList[self.currentSelectedIndex].deleteLater()
        self.barList.pop(self.currentSelectedIndex)
        self.colorList.pop(self.currentSelectedIndex)
        self.currentSelectedIndex=-1
    def loadGradientObj(self,obj):
        for bar in self.barList:
            bar.deleteLater()
        self.barList.clear()
        self.colorList.clear()
        gc.collect()
        for i,gra in enumerate(obj.gradientlist):
            bar=QLabel(self)
            bar.resize(11,17)
            self.barList.append(bar)
            self.colorList.append(gra.color)
            self.setBarColor(bar,gra.color)
            if i==0:
                x=2
            elif i==1:
                x=self.parent.gradientLabel.width()-13
            else:
                x=gra.position
                x=int(x*self.parent.gradientLabel.width()+2)
            bar.move(x,0)
            bar.show()#不show看不到
        self.parent.lineEdit.setText(obj.name)
        self.drawGradient()