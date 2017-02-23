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
        self.setWindowTitle(u'牛霸词典')
        self.setWindowIcon(QIcon(R.png.dict))

    def __initInputBar(self):
        self.text_edit = QLineEdit()
        self.text_edit.setFixedHeight(35)
        self.text_edit.setFocus()
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

        # 绑定信号量
        self.text_edit.textChanged.connect(self.__onInputChanged)
        self.text_edit.returnPressed.connect(self.__onSearch)

        self.btn_search.clicked.connect(self.__onSearch)

    def __center(self, widget):
        rect = widget.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()

        rect.moveCenter(self.center_point)
        widget.move(rect.topLeft())

    def moveByCenter(self, x, y):
        pass

    def __onSearch(self):
        print '__onSearch'
        key_word = ''
        try:
            key_word = self.text_edit.text()
            result = translate(key_word, 'en', 'cn')
            self.list_panel.hide()
            if result != None:
                self.detail_panel.show()
                self.__displayResult(result)
            else:
                self.detail_panel.hide()
        except:
            print 'onSearch except'

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
        self.list_panel.hide()
        self.root_layout.addWidget(self.list_panel)

    def __onInputChanged(self):
        self.detail_panel.hide()
        if self.text_edit.text() != '':
            self.list_panel.show()
        else:
            self.list_panel.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()
    sys.exit(app.exec_())
