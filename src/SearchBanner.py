# coding:utf-8
import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from interface.IBaiduDictionary import translate
from res import R


class SearchBanner(QWidget):
    def __init__(self):
        super(SearchBanner, self).__init__()
        self.__initTransform()
        self.__initTitle()
        self.__initInputBar()
        self.__initShowBar()

    def __initTransform(self):
        self.setGeometry(0, 0, 420, 60)
        self.__center(self)
        self.moveByCenter(100, 100)

    def __initTitle(self):
        self.setWindowTitle('NiubilityWord')
        self.setWindowIcon(QIcon(R.png.dict))

        pass

    def __initInputBar(self):
        self.text_edit = QLineEdit()
        self.text_edit.setFixedHeight(35)
        self.btn_search = QPushButton()
        self.btn_search.setIcon(QIcon(R.png.search))

        self.btn_clear = QPushButton()
        self.btn_clear.setIcon(QIcon(R.png.clear))
        self.btn_history = QComboBox()
        self.btn_history.resize(20,20)

        root_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(self.btn_clear)
        input_layout.addWidget(self.btn_history)
        root_layout.addLayout(input_layout)
        # root_layout.addStretch(1)
        root_layout.addWidget(self.btn_search)
        self.setLayout(root_layout)

        pass

    def __initShowBar(self):
        pass

    def __center(self, widget):
        rect = widget.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().__center()

        rect.moveCenter(self.center_point)
        widget.move(rect.topLeft())

    def moveByCenter(self, x, y):

        pass

    def __onSearch(self):
        result = translate("ad", 'sd', 'sd')
        self.__displayResult(result)

    def __displayResult(self, result):
        pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'tip',
                                     'are you sure to quit?',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()
    sys.exit(app.exec_())
