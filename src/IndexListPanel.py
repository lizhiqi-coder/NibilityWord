# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
from BuddyListWidget import BuddyListWidget
from res import R
from utils import NBUtils

import sys


class IndexListPanel(QListWidget):
    """实时模糊搜索列表:本地快速查找"""

    def __init__(self):
        super(IndexListPanel, self).__init__()
        self._initUI()

    def initTransfrom(self, w, h):
        self.setGeometry(0, 0, w, h)
        self.setFixedSize(w, h)

    def _initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.global_style)
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.index_list_widget = BuddyListWidget()
        self.layout().addWidget(self.index_list_widget)

    def refresh(self, dict):
        self.index_list_widget.setData(dict=dict)
        self.index_list_widget.setCurrentRow(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = IndexListPanel()
    panel.show()

    dict = {'1': 'value1', '2': 'value2'}
    panel.refresh(dict)
    sys.exit(app.exec_())
