# coding:utf-8
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
import sys

from res import R
from utils import NBUtils

"""

我的词典
快捷按键
关于我们
检查更新
"""


class SettingPage(QWidget):
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 430

    def __init__(self):
        super(SettingPage, self).__init__()
        self._initUI()
        self.initContent()

    def _initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.setting_page_style)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setFixedWidth(self.SCREEN_WIDTH)
        self.setFixedHeight(self.SCREEN_HEIGHT)

        self.setWindowTitle(R.string.setting)
        self.setWindowIcon(QIcon(R.png.setting))

        self.root_layout = QHBoxLayout()
        self.setLayout(self.root_layout)
        self.layout().setAlignment(Qt.AlignLeft)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        catalogue_frame = QFrame()
        # catalogue_frame.setFixedWidth(self.SCREEN_WIDTH / 6+30)
        catalogue_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.content_frame = QFrame()
        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout().addWidget(catalogue_frame)
        self.layout().addWidget(self.content_frame)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        catalogue_frame.setLayout(left_layout)
        self.content_frame.setLayout(right_layout)

        catalogue_frame.layout().setContentsMargins(20, 20, 20, 20)
        catalogue_frame.layout().setSpacing(10)
        catalogue_frame.layout().setAlignment(Qt.AlignTop)

        self.btn_my_dict = CatalogButton(R.string.my_dict)
        self.btn_shortcut = CatalogButton(R.string.shortcut)
        self.btn_about_me = CatalogButton(R.string.about_me)
        self.btn_check_update = CatalogButton(R.string.check_update)

        self.btn_my_dict.toggled.connect(lambda: self.onBtnChecked(self.btn_my_dict, 1))
        self.btn_shortcut.toggled.connect(lambda: self.onBtnChecked(self.btn_shortcut, 2))
        self.btn_about_me.toggled.connect(lambda: self.onBtnChecked(self.btn_about_me, 3))
        self.btn_check_update.toggled.connect(lambda: self.onBtnChecked(self.btn_check_update, 4))

        catalogue_frame.layout().addWidget(self.btn_my_dict)
        catalogue_frame.layout().addWidget(self.btn_shortcut)
        catalogue_frame.layout().addWidget(self.btn_about_me)
        catalogue_frame.layout().addWidget(self.btn_check_update)

    def initContent(self):
        self.pannel_about_me = QLabel("about me")
        self.content_frame.layout().addWidget(self.pannel_about_me)

    def moveByCenter(self, x, y):
        rect = self.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(self.center_point + QPoint(x, y))
        self.move(rect.topLeft())

    def onBtnChecked(self, btn, btn_id):
        if btn.isChecked():

            if btn_id == 1:
                print 1
            elif btn_id == 2:
                print 2
            elif btn_id == 3:
                self.pannel_about_me.show()
            elif btn_id == 4:
                print 4


class CatalogButton(QRadioButton):
    def __init__(self, text):
        super(CatalogButton, self).__init__(text)
        self.setObjectName('CatalogButton')
        self.setFocusPolicy(Qt.NoFocus)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setting = SettingPage()
    setting.show()
    setting.moveByCenter(0, 0)
    sys.exit(app.exec_())
