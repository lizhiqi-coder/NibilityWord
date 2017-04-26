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


class SettingPage(QWidget):
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 430

    def __init__(self):
        super(SettingPage, self).__init__()
        self._initUI()

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

        calalogue_frame = QFrame()
        calalogue_frame.setFixedWidth(self.SCREEN_WIDTH / 6)
        calalogue_frame.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        content_frame = QFrame()
        content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout().addWidget(calalogue_frame)
        self.layout().addWidget(content_frame)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        calalogue_frame.setLayout(left_layout)
        content_frame.setLayout(right_layout)

        calalogue_frame.layout().setContentsMargins(20, 20, 20, 20)
        calalogue_frame.layout().setSpacing(10)
        calalogue_frame.layout().setAlignment(Qt.AlignTop)
        calalogue_frame.layout().addWidget(QPushButton('button'))
        calalogue_frame.layout().addWidget(QPushButton('button'))
        calalogue_frame.layout().addWidget(QPushButton('button'))
        calalogue_frame.layout().addWidget(QPushButton('button'))

    def moveByCenter(self, x, y):
        rect = self.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(self.center_point + QPoint(x, y))
        self.move(rect.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setting = SettingPage()
    setting.show()
    sys.exit(app.exec_())
