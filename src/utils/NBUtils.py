# coding:utf-8

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

import platform


def bindStyleSheet(ref, style_sheet):
    style_file = QFile(style_sheet)
    style_file.open(QFile.ReadOnly)
    static_style_sheet = str(style_file.readAll())
    ref.setStyleSheet(static_style_sheet)


PLATFROM_WINDOWS = 'windows'
PLATFROM_LINUX = 'linux'


def getPlatform():
    if platform.system() == PLATFROM_WINDOWS:
        return PLATFROM_WINDOWS
    else:
        PLATFROM_LINUX


def containsChinese(str):
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False
