# coding:utf-8

from res import GenerateImageIndexing
from src.SearchBanner import SearchBanner

import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

GenerateImageIndexing.start()


def main():
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':

    main()
    pass
