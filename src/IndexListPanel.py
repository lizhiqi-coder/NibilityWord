# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
import sys

from BuddyListWidget import BuddyListWidget
from res import R
from utils import NBUtils


class IndexListPanel(QWidget):
    """实时模糊搜索列表:本地快速查找"""

    def __init__(self):
        super(IndexListPanel, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._initUI()

    def _initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.global_style)
        root_layout = QVBoxLayout()
        self.setLayout(root_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.index_list_widget = BuddyListWidget()
        self.index_list_widget.setObjectName('index_list_frame')
        self.layout().addWidget(self.index_list_widget)

    def display(self, dict_result_list):
        self.clear()
        display_data = {}
        self.dict_result_list = dict_result_list
        for dict in self.dict_result_list:
            display_data[dict.query] = ''.join(dict.explains)

        self.index_list_widget.setData(display_data)

    def getCurrentKey(self):
        item = self.index_list_widget.currentItem()
        item_widget = self.index_list_widget.itemWidget(item)
        key = item_widget.getKey()

        return key

    def clear(self):
        self.dict_result_list = []
        self.index_list_widget.setData({})


if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = IndexListPanel()
    panel.show()

    dict = {'1': 'value1', '2': 'value2'}
    panel.display()
    sys.exit(app.exec_())
