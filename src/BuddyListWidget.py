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
        self.setFocusPolicy(Qt.NoFocus)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pass

    def setData(self, explains):
        self.clear()
        if isinstance(explains, dict):
            for key in explains:
                if isinstance(explains[key], list):
                    for value in explains[key]:
                        m_item = BuddyListWidget.BuddyListItem(key, value)
                        item = QListWidgetItem()
                        self.addItem(item)
                        self.setItemWidget(item, m_item)
                else:
                    value = explains[key]
                    m_item = BuddyListWidget.BuddyListItem(key, value)
                    item = QListWidgetItem()
                    self.addItem(item)
                    self.setItemWidget(item, m_item)

        elif isinstance(explains, list):
            for i in range(len(explains)):
                m_item = BuddyListWidget.BuddyListItem(str(i + 1) + '.', explains[i])
                item = QListWidgetItem()
                self.addItem(item)
                self.setItemWidget(item, m_item)

    class BuddyListItem(QWidget):
        def __init__(self, key=None, value=None):
            super(BuddyListWidget.BuddyListItem, self).__init__()
            self._key = key
            self._value = value
            self._initUI()

        def getKey(self):
            return self._key

        def _initUI(self):
            key_lb = QLabel(self._key)
            key_lb.setMinimumWidth(20)
            key_lb.setObjectName('key_label')
            value_lb = QLabel(self._value)
            value_lb.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            value_lb.setObjectName('value_label')
            root_layout = QHBoxLayout()
            self.setLayout(root_layout)
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().setAlignment(Qt.AlignLeft)
            self.layout().addWidget(key_lb)
            self.layout().addWidget(value_lb)
            key_lb.adjustSize()
            key_lb.setFixedWidth(key_lb.width() + 3)
