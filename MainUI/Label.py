from PyQt5.QtGui import QColor
class Label(object):
    """description of class"""
    labelType=1
    shapeType="polygon"
    labelName=""
    labelDes=""
    pointList=[]
    labelGroup="defaultgroup"
    labelColor=QColor(255,0,0)
class GradientPart(object):
        position=0
        color=QColor(255,0,0)

class GradientObject(object):
        name="未定义"
        gradientlist=[]#存储多个滑块-gradientpart
        iscurrent=False