# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


class DetailPanel(QWidget):
    def __init__(self):
        super(DetailPanel, self).__init__()

    def initTransfrom(self, w, h):
        self.setGeometry(0, 0, w, h)
        self.setFixedSize(w, h)
