import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class SaveFileDlg(QFileDialog):
    def __init__(self,parent=None):
        super().__init__(parent)

        #layout=QHBoxLayout()
        #edit=QLineEdit()
        #layout.addWidget(edit)
        #self.setLayout(layout)
        