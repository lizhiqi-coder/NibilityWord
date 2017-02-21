# coding:utf-8
import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


class SearchBanner(QMainWindow):
    def __init__(self):
        super(SearchBanner, self).__init__()
        self.initTransform()
        self.initTitle()
        self.initInputBar()
        self.initShowBar()

    def initTransform(self):
        self.setGeometry(0, 0, 420, 60)
        self.center(self)
        self.moveByCenter(100,100)

    def initTitle(self):
        self.setWindowTitle('NiubilityWord')
        pass

    def initInputBar(self):
        pass

    def initShowBar(self):
        pass

    def center(self, widget):
        rect = widget.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()

        rect.moveCenter(self.center_point)
        widget.move(rect.topLeft())

    def moveByCenter(self, x, y):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()

    sys.exit(app.exec_())
