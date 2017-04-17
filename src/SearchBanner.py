# coding:utf-8
import sys

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

from interface import IYoudao
from DetailPanel import DetailPanel
from IndexListPanel import IndexListPanel
from res import R
from utils import NBUtils
from src.interface.lingoes.Lingoes import Lingoes


class SearchBanner(QWidget):
    def __init__(self):
        super(SearchBanner, self).__init__()
        self.__initTransform()
        self.__initTitle()
        self.__initInputBar()
        self.__initDetailPanel()
        self.__initListPanel()

        self._initShortcut()

    def __initTransform(self):
        self.setGeometry(0, 0, 420, 60)
        self.setFixedWidth(self.width())
        self.__center(self)
        self.moveByCenter(100, 100)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        NBUtils.bindStyleSheet(self, R.qss.global_style)

    def __initTitle(self):
        self.setWindowTitle(u'牛霸词典')
        self.setWindowIcon(QIcon(R.png.dict))

    def __initInputBar(self):
        self.root_layout = QVBoxLayout()
        self.root_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(self.root_layout)

        self.text_edit = QLineEdit()
        self.text_edit.setFont(QFont(R.string.Helvetica, R.dimen.text_size_small))
        self.text_edit.setFixedHeight(35)
        self.text_edit.setFocus()
        self.btn_search = QPushButton()
        self.btn_search.setIcon(QIcon(R.png.search))

        self.btn_clear = QPushButton()
        self.btn_clear.setIcon(QIcon(R.png.clear))
        self.btn_clear.hide()
        self.btn_history = QPushButton()
        self.btn_history.setIcon(QIcon(R.png.show_list))

        input_frame = QFrame()

        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)
        input_frame.layout().setContentsMargins(5, 0, 5, 0)
        input_frame.layout().setSpacing(0)
        input_frame.layout().addWidget(self.text_edit)
        input_frame.layout().addWidget(self.btn_clear)
        input_frame.layout().addWidget(self.btn_history)

        bar_layout = QHBoxLayout()
        bar_layout.addWidget(input_frame)
        bar_layout.addWidget(self.btn_search)
        self.btn_search.setObjectName("btn_search")
        self.layout().addLayout(bar_layout)

        # 绑定信号量
        self.text_edit.textChanged.connect(self.__onInputChanged)
        self.text_edit.returnPressed.connect(self.__onSearch)

        self.btn_search.clicked.connect(self.__onSearch)
        self.btn_clear.clicked.connect(self._onClear)

    def _onClear(self):
        self.text_edit.clear()

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
        result = None
        try:
            key_word = self.text_edit.text()
            result = IYoudao.translate(key_word)
            self.index_list_panel.hide()
        except Exception, e:
            print 'onSearch except', e
        if result != None:
            self.detail_panel.show()
            self.detail_panel.display(result=result)
        else:
            self.detail_panel.hide()

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'tip',
    #                                  'are you sure to quit?',
    #                                  QMessageBox.Yes, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def __initDetailPanel(self):
        self.detail_panel = DetailPanel(self.width(), 200)
        self.detail_panel.hide()
        self.root_layout.addWidget(self.detail_panel)

    def __initListPanel(self):
        self.index_list_panel = IndexListPanel()
        self.index_list_panel.initTransfrom(self.width() - 30, 200)
        self.index_list_panel.hide()
        self.root_layout.addWidget(self.index_list_panel)
        self.local_dict = Lingoes('Vicon English-Chinese(S) Dictionary.ld2')

    def __onInputChanged(self):
        self.detail_panel.hide()
        if self.text_edit.text() != '':
            self.index_list_panel.show()
            self.btn_clear.show()
            fast_entrys = self.local_dict.getFastEntry(self.text_edit.text())
            for fast in fast_entrys:
                print fast.query, '---->', fast.explains
                # self.index_list_panel.setData(entry)


        else:
            self.index_list_panel.hide()
            self.btn_clear.hide()

    def _initShortcut(self):

        show_win_action = QAction(self)
        show_win_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_F))
        show_win_action.triggered.connect(self._onShowWinAction)
        self.insertAction(show_win_action, show_win_action)

    def _onShowWinAction(self):
        print '_onShowWinAction'
        if self.isHidden():
            self.show()
        else:
            self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainBanner = SearchBanner()
    mainBanner.show()
    sys.exit(app.exec_())
