from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class LoadingDlg(QDialog):
 def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)
     #self.setWindowModality(Qt.ApplicationModal)
     self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint |  Qt.Drawer)
     self.label=QLabel("解析图像")
     vbox=QVBoxLayout()
     vbox.addWidget(self.label)

     hbox=QHBoxLayout()
     progressbar=QProgressBar()
     progressbar.setMinimumSize(300,20)
     progressbar.setMinimum(0)
     progressbar.setMaximum(0)
     button=QPushButton("取消")
     button.setMinimumSize(90,20)
     hbox.addWidget(progressbar)
     #hbox.addWidget(button)
     hbox.setContentsMargins(0,0,0,0)

     vbox.addLayout(hbox)
     self.setLayout(vbox)


     self.setStyleSheet("QProgressBar{margin:0px;}")

     self.resize(400,65)
     self.setWindowTitle("进程")
     
     