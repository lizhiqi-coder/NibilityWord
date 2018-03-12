# coding:utf-8

try:
    from PySide.QtGui import *
    from PySide.QtCore import Qt
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import Qt

from res import R
from utils import NBUtils


class WebListPannel(QWidget):
    def __init__(self):
        super(WebListPannel, self).__init__()
        self._initUI()

    def _initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.web_panel_style)
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.setLayout(self.root_layout)

        self.btn_web = QPushButton()
        self.btn_web.setIcon(QIcon(R.png.down))
        self.btn_web.setObjectName('btn_web')
        self.web_widget = WebListWidget()
        self.web_widget.setObjectName('web_list_widget')
        self.btn_web.clicked.connect(self._onShowWeb)

        self.root_layout.addWidget(self.btn_web)
        self.root_layout.addWidget(self.web_widget)
        self.btn_web.hide()
        self.web_widget.hide()

    def _onShowWeb(self):
        if self.web_widget.isHidden():
            self.web_widget.show()
        else:
            self.web_widget.hide()

    def display(self, web):
        self.btn_web.show()
        self.web_widget.hide()
        self.web_widget.setData(web)


class WebListWidget(QListWidget):
    def __init__(self):
        super(WebListWidget, self).__init__()
        self._initUI()

    def _initUI(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # web is dict
    def setData(self, web):
        self.clear()
        if isinstance(web, dict):
            for key in web:
                value_list = web[key]
                value = ','.join(value_list)
                item_widget = WebListWidget.WebListItem(key, value)
                item = QListWidgetItem()
                self.addItem(item)
                self.setItemWidget(item, item_widget)

    class WebListItem(QWidget):
        def __init__(self, key=None, value=None):
            super(WebListWidget.WebListItem, self).__init__()
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
            self.layout().setAlignment(Qt.AlignLeft)
            self.layout().setSpacing(0)
            self.layout().addWidget(label_key)
            self.layout().addWidget(label_value)
