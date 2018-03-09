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
from utils.MediaUtils import MediaLoader
from WebListPanel import WebListPanel


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
        self.head_name = QLineEdit()
        self.head_name.setReadOnly(True)
        self.head_name.setObjectName('detail_head')
        self.head_name.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.head_bar.layout().addWidget(self.head_name)

    def __initPhoneBar(self):
        self.phone_bar = QFrame()

        bar_layout = QHBoxLayout()
        self.phone_bar.setLayout(bar_layout)
        self.phone_bar.layout().setAlignment(Qt.AlignLeft)

        self.ph_item = PhItem()
        self.ph_item2 = PhItem()

        self.phone_bar.layout().addWidget(self.ph_item)
        self.phone_bar.layout().addWidget(self.ph_item2)

        pass

    def _initMeaningListBar(self):
        self.meaning_list_bar = BuddyListWidget()
        self.meaning_list_bar.setObjectName('air_frame')
        self.meaning_list_bar.setViewportMargins(10, 10, 10, 0)

        pass

    def __initOtherBar(self):
        self.other_bar = QFrame()
        pass

    # 网络释义
    def _initWebBar(self):
        self.btn_web = QPushButton()
        self.btn_web.setIcon(QIcon(R.png.down))
        self.btn_web.setObjectName('btn_web')
        self.web_bar = WebListPanel()
        self.btn_web.clicked.connect(self._onShowWeb)

    def _onShowWeb(self):
        if self.web_bar.isHidden():
            self.web_bar.show()
        else:
            self.web_bar.hide()

    def _initAdvBar(self):
        self.adv_var = QFrame()

    def __initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.global_style)
        self._initHead()
        self.__initPhoneBar()
        self._initMeaningListBar()
        self._initWebBar()
        self._initAdvBar()
        self.__initOtherBar()

        self.root_layout = QVBoxLayout()
        self.setLayout(self.root_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.layout().addWidget(self.head_bar)
        self.layout().addWidget(self.phone_bar)

        self.root_layout.addWidget(self.meaning_list_bar)
        self.root_layout.addWidget(self.btn_web)
        self.root_layout.addWidget(self.web_bar)
        # self.root_layout.addWidget(self.other_bar)

    def display(self, result):
        self.clear()
        cn_to_en = NBUtils.containsChinese(result.query)
        if cn_to_en:
            self.head_name.setText(''.join(result.translation))
        else:
            self.head_name.setText(result.query)

        if result.phones != None and len(result.phones) > 0:

            if len(result.phones) == 1:
                self.ph_item.setData(title=u'发音',
                                     ph_symbol=result.phones['phonetic'][0],
                                     sound=result.phones['phonetic'][1])
            else:
                self.ph_item.setData(title=u'英',
                                     ph_symbol=result.phones['uk'][0],
                                     sound=result.phones['uk'][1])
                self.ph_item2.setData(title=u'美',
                                      ph_symbol=result.phones['us'][0],
                                      sound=result.phones['us'][1])

        if cn_to_en:
            explains = []
        else:
            explains = {}
            if result.explains == None or len(result.explains) == 0:
                explains[u'解释:'] = ''.join(result.translation)

        for item in result.explains:

            split = item.split('.')
            if len(split) > 1 and not cn_to_en:
                first = split[0] + '.'
                if explains.has_key(first) and isinstance(explains[first], list):
                    explains[first].append(split[1])
                else:
                    second = []
                    second.append(split[1])
                    explains[first] = second

            elif not cn_to_en:
                explains[u'解释:'] = item
            elif cn_to_en:
                explains.append(item)

        self.meaning_list_bar.setData(explains)

        if result.web != None:
            self.btn_web.show()
            self.web_bar.setData(result.web)

    def clear(self):
        self.head_name.setText('')
        self.ph_item.hide()
        self.ph_item2.hide()
        self.meaning_list_bar.setData({})
        self.btn_web.hide()
        self.web_bar.hide()


# -------------------------------------------------------------------#

class PhItem(QFrame):
    def __init__(self):
        super(PhItem, self).__init__()
        self._initUI()

    def _initUI(self):
        ph_item_layout = QHBoxLayout()

        self.setLayout(ph_item_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.lb_title = QLabel(u'英/美')
        self.lb_ph_symbol = QLabel(u'[音标]')
        self.lb_title.setObjectName('PhItem')
        self.lb_ph_symbol.setObjectName('PhItem')

        self.btn_sound = QPushButton()
        self.btn_sound.setIcon(QIcon(R.png.sound))
        ph_item_layout.addWidget(self.lb_title)
        ph_item_layout.addWidget(self.lb_ph_symbol)
        ph_item_layout.addWidget(self.btn_sound)
        self.btn_sound.clicked.connect(self._onDisplaySound)

    def setData(self, title=None, ph_symbol=None, sound=None):
        self.title = title
        self.ph_symbol = '[' + ph_symbol + ']'
        if sound == None or sound == "":
            self.btn_sound.hide()
        else:
            self.sound = sound
            self.btn_sound.show()
        self.lb_title.setText(self.title)
        self.lb_ph_symbol.setText(self.ph_symbol)
        self.show()

    def _onDisplaySound(self):
        print 'display sound'
        print self.sound
        MediaLoader.getInstance().loadMedia(self.sound).playAudio()


# -------------------------------------------------------------------#



if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = DetailPanel(300, 100)
    panel.show()
    sys.exit(app.exec_())
