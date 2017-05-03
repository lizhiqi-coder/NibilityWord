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
        catalogue_frame.setObjectName('catalogue_frame')
        # catalogue_frame.setFixedWidth(self.SCREEN_WIDTH / 6+30)
        catalogue_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.content_frame = QFrame()
        self.content_frame.setObjectName('content_frame')
        self.content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout().addWidget(catalogue_frame)
        self.layout().addWidget(self.content_frame)

        left_layout = QVBoxLayout()
        right_layout = QStackedLayout()
        catalogue_frame.setLayout(left_layout)
        self.content_frame.setLayout(right_layout)

        catalogue_frame.layout().setContentsMargins(20, 20, 20, 20)
        catalogue_frame.layout().setSpacing(10)
        catalogue_frame.layout().setAlignment(Qt.AlignTop)

        self.btn_my_dict = CatalogButton(R.string.my_dict)
        self.btn_shortcut = CatalogButton(R.string.shortcut)
        self.btn_check_update = CatalogButton(R.string.check_update)
        self.btn_about_me = CatalogButton(R.string.about_me)

        self.btn_my_dict.toggled.connect(lambda: self.onBtnChecked(self.btn_my_dict, 0))
        self.btn_shortcut.toggled.connect(lambda: self.onBtnChecked(self.btn_shortcut, 1))
        self.btn_check_update.toggled.connect(lambda: self.onBtnChecked(self.btn_check_update, 2))
        self.btn_about_me.toggled.connect(lambda: self.onBtnChecked(self.btn_about_me, 3))

        catalogue_frame.layout().addWidget(self.btn_my_dict)
        catalogue_frame.layout().addWidget(self.btn_shortcut)
        catalogue_frame.layout().addWidget(self.btn_check_update)
        catalogue_frame.layout().addWidget(self.btn_about_me)

    def initContent(self):
        pannel_about_me = QTextEdit(NBUtils.parseHtml(R.html.about_me_content))
        pannel_about_me.setReadOnly(True)

        to_do01 = QLabel(NBUtils.parseHtml(R.html.to_do))
        to_do01.setAlignment(Qt.AlignCenter)
        shortcut_content = QLabel(NBUtils.parseHtml(R.html.shortcut_content))
        shortcut_content.setAlignment(Qt.AlignCenter)
        pannel_check_update = QLabel(NBUtils.parseHtml(R.html.check_update))
        pannel_check_update.setAlignment(Qt.AlignCenter)

        self.content_frame.layout().addWidget(to_do01)
        self.content_frame.layout().addWidget(shortcut_content)
        self.content_frame.layout().addWidget(pannel_check_update)
        self.content_frame.layout().addWidget(pannel_about_me)
        self.btn_about_me.setChecked(True)

    def moveByCenter(self, x, y):
        rect = self.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(self.center_point + QPoint(x, y))
        self.move(rect.topLeft())

    def onBtnChecked(self, btn, btn_id):
        if btn.isChecked():
            self.content_frame.layout().setCurrentIndex(btn_id)


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
