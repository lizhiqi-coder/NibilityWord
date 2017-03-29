# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import struct


class Lingoes():
    def __init__(self):
        self.ld2_file = ""
        self.ld2_byte_array = QByteArray()
        self.inflate_pos = 0
        self.availableEncodings = ()

        pass

    def _readDictionary(self, offsetWithIndex, outputfile=""):
        pass

    def _inflateData(self):
        """填充数据"""
        pass

    def _decompress(self):
        """解压"""
        pass

    def _extract(self):
        """提取"""
        pass

    def _detectEncodings(self):
        pass

    def _readDefinitionData(self):
        pass

    def _getIdxData(self):
        pass

    def _strip(self):
        pass

    def extractToFile(self):
        pass

    def getInt(self,index):
        self.ld2_byte_array.number()

if __name__ == '__main__':
    pass
