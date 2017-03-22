# coding:utf-8

try:
    from PySide.QtGui import *
    from PySide.QtCore import Qt
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import Qt


class BuddyListWidget(QListWidget):
    def __init__(self):
        super(BuddyListWidget, self).__init__()
        self._initUI()

    def _initUI(self):
        pass

    def setData(self, dict={}):
        self.clear()
        for key in dict:
            m_item = BuddyListWidget.BuddyListItem(key, dict[key])
            item = QListWidgetItem()
            self.addItem(item)
            self.setItemWidget(item, m_item)

    class BuddyListItem(QWidget):
        def __init__(self, key=None, value=None):
            super(BuddyListWidget.BuddyListItem, self).__init__()
            self._key = key
            self._value = value
            self._initUI()

        def _initUI(self):
            key_lb = QLabel(self._key)
            key_lb.setFixedWidth(40)
            value_lb = QLabel(self._value)
            value_lb.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            root_layout = QHBoxLayout()
            self.setLayout(root_layout)
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().setAlignment(Qt.AlignLeft)
            self.layout().addWidget(key_lb)
            self.layout().addWidget(value_lb)
