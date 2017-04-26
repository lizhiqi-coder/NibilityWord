# coding:utf-8

import sys

from src.SearchBanner import SearchBanner

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from res import R


def main():
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    trayIcon = QSystemTrayIcon()
    trayIcon.setIcon(QIcon(R.png.dict))

    mainBanner.show()
    trayIcon.show()
    trayIcon.activated.connect(mainBanner.show)
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()
    pass
