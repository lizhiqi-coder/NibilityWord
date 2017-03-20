# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from model.DetailModel import DetailModel
from res import R
import sys


class DetailPanel(QWidget):
    def __init__(self, w, h):
        super(DetailPanel, self).__init__()
        self.initTransfrom(w, h)
        self.__initUI()

    def initTransfrom(self, w, h):
        self.setGeometry(0, 0, w, h)
        # self.setFixedSize(w, h)

    def __initPhoneBar(self):
        self.phone_bar = QLabel()

        bar_layout = QHBoxLayout()
        ph_item_layout = QHBoxLayout()
        title = QLabel(u'英/美')
        ph_symbol = QLabel(u'[音标]')
        sound_btn = QPushButton()
        sound_btn.setIcon(QIcon(R.png.sound))
        ph_item_layout.addWidget(title)
        ph_item_layout.addWidget(ph_symbol)
        ph_item_layout.addWidget(sound_btn)

        ph_item = QFrame()
        ph_item.setLayout(ph_item_layout)

        bar_layout.addWidget(ph_item)

        self.phone_bar.setLayout(bar_layout)

        pass

    def __initExchangeListBar(self):
        self.exchange_list_bar = QListWidget()
        pass

    def __initOtherBar(self):
        self.other_bar = QFrame()
        pass

    def __initUI(self):
        self.__initPhoneBar()
        self.__initExchangeListBar()
        self.__initOtherBar()

        self.root_layout = QVBoxLayout()
        self.root_layout.addWidget(self.phone_bar)
        # self.root_layout.addWidget(self.exchange_list_bar)
        # self.root_layout.addWidget(self.other_bar)

        self.setLayout(self.root_layout)


    def display(self, result):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = DetailPanel(300,100)
    panel.show()
    sys.exit(app.exec_())
