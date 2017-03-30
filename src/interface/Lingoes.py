# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import struct

LENGTH_SHORT = 2
LENGTH_INT = 4
LENGTH_LONG = 8
LENGTH_HEADER = 96
LENGTH_TYPE = LENGTH_INT
LENGTH_CHECKSUM = 20
LENGTH_MAJOR_VERSION = LENGTH_SHORT
LENGTH_MINOR_VERSION = LENGTH_SHORT
LENGTH_ID = LENGTH_LONG
LENGTH_OFFSET = LENGTH_INT
LENGTH_COMPRESS_HEADER = LENGTH_INT * 7


class Header():
    def __init__(self):
        # string
        self.type = ''
        self.checksum = ''

        # short
        self.majorVersion
        self.minorVersion

        # string
        self.id = ''
        self.padding = ''

        # int
        self.infoOffset
        self.infoPosition
        self.dictType  # 3表示本地字典
        self.withIndexOffset
        self.limit  # 自己加的字段
        self.compressDataOffset

        self.definitions

        self.offsetCompressDataHeader

        self.inflatWordsIndexLength

        self.inflatXmlLength

        self.offsetIndex  # 单词索引的开始位置


class LingoesDictReader():
    def __init__(self):
        # 索引数组
        self.definitionsArrays = []
        # 压缩数据块数组
        self.deflateStreams = []

        self.dataRawBytes = bytearray()
        self.header = Header()

        pass

    def _readDictionary(self, offsetWithIndex, file_path=""):
        btye_file = open(file_path, 'rb')

        pass

    def _readHeader(self, pos):
        self.header.type =

    def _inflateData(self):
        """填充数据"""
        pass

    def _decompress(self, inflateData, offset, length):
        """解压"""
        data = self.ld2_byte_array[offset, length]
        header = QByteArray(4, '\0')
        pass

    def _extract(self):
        """提取"""
        pass

    def _detectEncodings(self, inflateBytes, offsetWords, offXml, defTotal, dataLen, idxData=[]):
        pass

    def _readDefinitionData(self):
        pass

    def _getIdxData(self, inflateBytes, pos):
        wordIdxData = []
        wordIdxData.append(inflateBytes[pos, SIZE_INT])
        pos += SIZE_INT
        wordIdxData.append(inflateBytes[pos, SIZE_INT])
        pos += SIZE_INT
        wordIdxData.append(inflateBytes[pos] & 0xff)
        pos += 1
        wordIdxData.append(inflateBytes[pos] & 0xff)
        pos += 1
        wordIdxData.append(inflateBytes[pos, SIZE_INT])
        pos += SIZE_INT
        wordIdxData.append(inflateBytes[pos, SIZE_INT])
        pos += SIZE_INT

        return wordIdxData

    def _strip(self):
        pass

    def extractToFile(self):
        pass


if __name__ == '__main__':
    pass
