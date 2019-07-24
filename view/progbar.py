from PyQt5.QtWidgets import QDialog, QProgressBar, QSizePolicy
from PyQt5.QtCore import QRect, QSize
from PyQt5.QtGui import QIcon

class ProgressBar(QDialog):
    def __init__(self, desc = None, parent = None):
        super(ProgressBar, self).__init__(parent)
        self.progressBar = QProgressBar(self)
        self._interface()
        self.setWindowTitle(desc)
        self.resize(800, 84)
        self.setWindowIcon(QIcon("img/python.png"))
        self.show()

    def _interface(self):
        self.progressBar.setGeometry(QRect(30, 30, 750, 35))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QSize(750, 35))
        self.progressBar.setMaximumSize(QSize(750, 35))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
    
    def setValue(self, val):
        self.progressBar.setProperty("value", val)