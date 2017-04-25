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


class TitleBar(QWidget):
    TITLE_HEIGHT = 30

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self._initUI()
        self.is_pressed = False
        self.startPos = None

    def _initUI(self):
        NBUtils.bindStyleSheet(self, R.qss.title_bar_style)
        self.titleIcon = QPushButton()
        self.titleText = QLabel()
        self.btn_close = QPushButton()
        self.btn_close.setIcon(QIcon(R.png.close))
        self.btn_close.setObjectName('btn_function')
        self.btn_setting = QPushButton()
        self.btn_setting.setIcon(QIcon(R.png.setting))
        self.btn_setting.setObjectName('btn_function')

        self.root_layout = QHBoxLayout()
        self.setLayout(self.root_layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(10)

        self.layout().addWidget(self.titleIcon)
        self.layout().addWidget(self.titleText)
        self.layout().addWidget(self.btn_setting)
        self.layout().addWidget(self.btn_close)
        self.titleText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.setFixedHeight(self.TITLE_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.btn_close.clicked.connect(self._onClose)
        self.btn_setting.clicked.connect(self._onSetting)

    def setTitleIcon(self, icon_path):
        self.titleIcon.setIcon(QIcon(icon_path))

    def setTitleText(self, text):
        self.titleText.setText(text)

    def mousePressEvent(self, event):
        self.is_pressed = True
        self.startPos = event.globalPos()

        return QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.is_pressed:
            movePos = event.globalPos() - self.startPos
            widgetPos = self.parentWidget().pos()
            self.parentWidget().move(widgetPos.x() + movePos.x(),
                                     widgetPos.y() + movePos.y())
            self.startPos = event.globalPos()
        return QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.is_pressed = False
        return QWidget.mouseReleaseEvent(self, event)

    def _onClose(self):
        self.parent().close()

    def _onSetting(self):
        pass


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
        self.setGeometry(0, 0, 350, 60)
        self.setFixedWidth(self.width())
        self.setMaximumHeight(self.height())
        self.moveByCenter(350, -300)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        NBUtils.bindStyleSheet(self, R.qss.global_style)

        self.root_layout = QVBoxLayout()
        self.root_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.root_layout)
        self.layout().setContentsMargins(10, 0, 10, 10)

    def __initTitle(self):
        self.title_bar = TitleBar(self)
        self.layout().addWidget(self.title_bar)
        self.title_bar.setTitleIcon(R.png.dict)
        self.title_bar.setTitleText(R.string.app_name_cn)

    def __initInputBar(self):

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
        input_frame.setObjectName('input_frame')
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
        self.text_edit.keyPressEvent = self._onEditKeyPress

        self.btn_search.clicked.connect(self.__onSearch)
        self.btn_clear.clicked.connect(self._onClear)

        self.locked_input_bar = False

    def _onEditKeyPress(self, event):
        if not self.index_list_panel.isHidden():
            end_row = self.index_list_panel.index_list_widget.count() - 1
            if event.key() == Qt.Key_Up and self.index_list_panel.index_list_widget.currentRow() <= 0:
                self.index_list_panel.index_list_widget.setCurrentRow(end_row)

            elif event.key() == Qt.Key_Down and self.index_list_panel.index_list_widget.currentRow() >= end_row:
                self.index_list_panel.index_list_widget.setCurrentRow(0)
            else:
                self.index_list_panel.index_list_widget.keyPressEvent(event)
        QLineEdit.keyPressEvent(self.text_edit, event)

    def _onClear(self):
        self.text_edit.clear()

    def __center(self, widget):
        rect = widget.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()

        rect.moveCenter(self.center_point)
        widget.move(rect.topLeft())

    def moveByCenter(self, x, y):
        rect = self.frameGeometry()
        self.center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(self.center_point + QPoint(x, y))
        self.move(rect.topLeft())
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
        self.index_list_panel = IndexListPanel(self.width() - 30, 200)
        self.index_list_panel.hide()
        self.root_layout.addWidget(self.index_list_panel)
        self.index_list_panel.index_list_widget.itemSelectionChanged.connect(self.onListPanelSelectChanged)
        self.local_dict = Lingoes('Vicon English-Chinese(S) Dictionary.ld2')

    def onListPanelSelectChanged(self):

        key_word = self.index_list_panel.getCurrentKey()
        self.locked_input_bar = True
        self.text_edit.setText(key_word)
        self.locked_input_bar = False

    def __onInputChanged(self):
        if self.locked_input_bar:
            return
        self.detail_panel.hide()
        if self.text_edit.text() != '' and not NBUtils.containsChinese(self.text_edit.text()):
            self.index_list_panel.show()
            self.btn_clear.show()

            fast_entrys = self.local_dict.getFastEntry(self.text_edit.text())
            self.index_list_panel.display(fast_entrys)

        else:
            self.index_list_panel.hide()
            self.btn_clear.hide()
            self.adjustSize()

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
