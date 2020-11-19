# coding:utf-8

import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from res import RCreater

try:
    if RCreater.start():
        from res import R
        # from src.SearchBanner import SearchBanner
except Exception, e:
    print e
from src.SearchBanner import SearchBanner


def main():
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    trayIcon = QSystemTrayIcon()
    trayIcon.setIcon(QIcon(R.png.tray_icon))

    mainBanner.show()
    trayIcon.show()
    trayIcon.activated.connect(mainBanner.onTrayActivated)

    quitAction = QAction(R.string.quit, mainBanner, triggered=qApp.quit)
    trayMenu = QMenu(mainBanner)
    trayMenu.addAction(quitAction)
    trayIcon.setContextMenu(trayMenu)

    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()
    pass
