# coding:utf-8
import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from interface.IBaiduDictionary import translate
from DetailPanel import DetailPanel
from ListPanel import ListPanel
from res import R


class SearchBanner(QWidget):
    def __init__(self):
        super(SearchBanner, self).__init__()
        self.__initTransform()
        self.__initTitle()
        self.__initInputBar()
        self.__initDetailPanel()
        self.__initListPanel()

    def __initTransform(self):
        self.setGeometry(0, 0, 420, 60)
        self.setFixedWidth(self.width())
        self.__center(self)
        self.moveByCenter(100, 100)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

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
        self.btn_history.resize(20, 20)

        bar_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(self.btn_clear)
        input_layout.addWidget(self.btn_history)
        bar_layout.addLayout(input_layout)
        bar_layout.addWidget(self.btn_search)

        self.root_layout = QVBoxLayout()
        self.root_layout.addLayout(bar_layout)
        self.setLayout(self.root_layout)

        pass

    def __center(self, widget):
        rect = widget.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()

        rect.moveCenter(self.center_point)
        widget.move(rect.topLeft())

    def moveByCenter(self, x, y):
        pass

    def __onSearch(self):
        result = translate("ad", 'sd', 'sd')
        self.__displayResult(result)

    def __displayResult(self, result):
        pass

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'tip',
    #                                  'are you sure to quit?',
    #                                  QMessageBox.Yes, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def __initDetailPanel(self):
        self.detail_panel = DetailPanel()
        self.detail_panel.initTransfrom(self.width(), 200)
        self.detail_panel.hide()
        self.root_layout.addWidget(self.detail_panel)

    def __initListPanel(self):
        self.list_panel = ListPanel()
        self.list_panel.initTransfrom(self.width() - 30, 200)
        # self.list_panel.hide()
        self.root_layout.addWidget(self.list_panel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()
    sys.exit(app.exec_())
