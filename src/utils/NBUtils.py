# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


def bindStyleSheet(ref, style_sheet):
    style_file = QFile(style_sheet)
    style_file.open(QFile.ReadOnly)
    static_style_sheet = str(style_file.readAll())
    ref.setStyleSheet(static_style_sheet)
