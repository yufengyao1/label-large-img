import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

class MapSaveDlg(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        
        vbox=QVBoxLayout()

        self.labelNameEdit=QComboBox()
        self.labelNameEdit.setEditable(True)
        #self.labelNameEdit.setPlaceholderText("标签名称")
        self.labelDesEdit=QTextEdit()
        self.labelDesEdit.setPlaceholderText("备注")
        vbox.addWidget(self.labelNameEdit)
        vbox.addWidget(self.labelDesEdit)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("确定", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        vbox.addWidget(self.buttonBox)

        self.setLayout(vbox)
        self.setWindowTitle("标记")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(300,280)
  