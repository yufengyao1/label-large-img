from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
 
class ColorDialog (QtWidgets.QWidget):
    def __init__(self, parent= None):
        QtWidgets.QWidget.__init__(self)
  
        color = QColor(0, 0, 0)
        self.selectedColor=None
        self.setGeometry(300, 300, 350, 80)
        self.setWindowTitle('ColorDialog')
        self.button = QPushButton('Dialog', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(20, 20)
        self.button.clicked.connect(self.showDialog)
        self.setFocus()
        
        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet('QWidget{background-color:%s}'%color.name())
        self.widget.setGeometry(130, 22, 100, 100)
        
    def showDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            #self.patent.setStyleSheet('QWidget {background-color:%s}'%col.name())
            self.selectedColor=col