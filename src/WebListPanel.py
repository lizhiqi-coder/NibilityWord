# coding:utf-8

try:
    from PySide.QtGui import *
    from PySide.QtCore import Qt
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import Qt


class WebListPanel(QListWidget):
    def __init__(self):
        super(WebListPanel, self).__init__()
        self._initUI()

    def _initUI(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # web is dict
    def setData(self, web):
        if isinstance(web, dict):
            for key in web:
                value_list = web[key]
                value = ','.join(value_list)
                item_widget = WebListPanel.WebListItem(key, value)
                item = QListWidgetItem()
                self.addItem(item)
                self.setItemWidget(item, item_widget)

    class WebListItem(QWidget):
        def __init__(self, key=None, value=None):
            super(WebListPanel.WebListItem, self).__init__()
            self._key = key
            self._value = value
            self._initUI()

        def _initUI(self):
            label_key = QLabel(self._key)
            label_key.setObjectName('web_lable_key')
            label_value = QLabel(self._value)
            label_value.setObjectName('web_lable_value')
            vlayout = QVBoxLayout()
            self.setLayout(vlayout)
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().addWidget(label_key)
            self.layout().addWidget(label_value)
