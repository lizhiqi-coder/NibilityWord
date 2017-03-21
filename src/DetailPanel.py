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


class DetailPanel(QWidget):
    def __init__(self, w, h):
        super(DetailPanel, self).__init__()
        self.initTransfrom(w, h)
        self.__initUI()

    def initTransfrom(self, w, h):
        self.setGeometry(200, 200, w, h)

    def _initHead(self):
        self.head_bar = QFrame()
        self.head_bar.setLayout(QHBoxLayout())
        self.head_bar.layout().setAlignment(Qt.AlignLeft)
        self.head_name = QLabel('head')
        self.head_name.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        font = QFont()
        font.setBold(True)
        font.setPixelSize(R.dimen.text_size_big)
        self.head_name.setFont(font)
        self.head_bar.layout().addWidget(self.head_name)

    def __initPhoneBar(self):
        self.phone_bar = QFrame()

        bar_layout = QHBoxLayout()
        self.phone_bar.setLayout(bar_layout)
        self.phone_bar.layout().setAlignment(Qt.AlignLeft)

        item = PhItem(title=u'英/美', ph_symbol=u'[音标]')

        self.phone_bar.layout().addWidget(item)

        pass

    def _initMeaningListBar(self):
        dict = {'1': '2'}
        self.meaning_list_bar = BuddyListWidget()
        self.meaning_list_bar.setData(dict)
        pass

    def __initOtherBar(self):
        self.other_bar = QFrame()
        pass

    def __initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.global_style)
        self._initHead()
        self.__initPhoneBar()
        self._initMeaningListBar()
        self.__initOtherBar()

        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)
        self.layout().setSpacing(0)
        self.layout().addWidget(self.head_bar)
        self.layout().addWidget(self.phone_bar)

        self.root_layout.addWidget(self.meaning_list_bar)
        # self.root_layout.addWidget(self.other_bar)

    def display(self, result):
        pass


# -------------------------------------------------------------------#
class PhItem(QFrame):
    def __init__(self, title=None, ph_symbol=None, sound=None):
        super(PhItem, self).__init__()
        self.title = title
        self.ph_symbol = ph_symbol
        self.sound = sound
        self._initUI()

    def _initUI(self):
        ph_item_layout = QHBoxLayout()

        self.setLayout(ph_item_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        lb_title = QLabel(u'英/美')
        lb_ph_symbol = QLabel(u'[音标]')
        btn_sound = QPushButton()
        btn_sound.setIcon(QIcon(R.png.sound))
        ph_item_layout.addWidget(lb_title)
        ph_item_layout.addWidget(lb_ph_symbol)
        ph_item_layout.addWidget(btn_sound)

        lb_title.setText(self.title)
        lb_ph_symbol.setText(self.ph_symbol)
        btn_sound.clicked.connect(self._onDisplaySound)

    def _onDisplaySound(self):
        print 'display sound'


# -------------------------------------------------------------------#



if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = DetailPanel(300, 100)
    panel.show()
    sys.exit(app.exec_())
