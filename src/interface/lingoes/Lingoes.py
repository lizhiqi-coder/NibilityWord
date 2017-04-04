# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import struct
import zlib

from Bean import *

"""
读取二进制文件->读取头->读取索引->读取数据块(blocks)

"""

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
        self.majorVersion = -1
        self.minorVersion = -1

        # string
        self.id = ''
        self.padding = ''

        # int
        self.infoOffset = -1
        self.infoPosition = -1


class Indexing():
    def __init__(self):
        self.dictType = -1  # 3表示本地字典
        self.withIndexOffset = -1
        self.limit = -1  # 自己加的字段
        self.compressDataOffset = -1

        self.definitions = -1

        self.offsetCompressDataHeader = -1

        self.inflatWordsIndexLength = -1

        self.inflatWordsLength = -1
        self.inflatXmlLength = -1
        self.offsetIndex = -1  # 单词索引的开始位置


class LingoesDictReader():
    def __init__(self, file_path):
        # 索引数组
        self.definitionsArray = []
        # 压缩数据块数组
        self.deflateStreams = []

        self.rawFile = open(file_path, 'rb')
        self.dataRawBytes = bytearray(self.rawFile.read())

        self.position = 0

        self.header = Header()
        self.indexing = Indexing()

        self._readHeader()
        self.header.infoPosition = self.position

        assert self.dataRawBytes.__len__() > self.header.infoPosition

        dict_type = self.getIntFromRaw(self.header.infoPosition)

        print dict_type
        if dict_type == 3:
            print 'this is the type i want'
            self._readDictionary(self.header.infoPosition)
        else:
            print 'can not read dict file'

        self._buildDefinitionsArray()
        self._deflateFile()
        self.rawFile.close()

    def _readDictionary(self, startPosition):
        self.position = startPosition
        self.indexing.offsetIndex = self.position + LENGTH_COMPRESS_HEADER
        # todo
        self.indexing.dictType = self.getIntFromRaw(self.position)  # getint

        self.position += LENGTH_INT
        self.indexing.withIndexOffset = self.getIntFromRaw(self.position)  # getint

        # 压缩数据的结束位置
        self.indexing.limit = self.position + self.indexing.withIndexOffset

        self.position += LENGTH_INT

        self.indexing.compressDataOffset = self.getIntFromRaw(self.position)  # getint

        self.indexing.definitions = self.indexing.compressDataOffset / LENGTH_INT

        self.indexing.offsetCompressDataHeader = self.indexing.compressDataOffset + self.indexing.offsetIndex

        self.position += LENGTH_INT

        # 索引单词长度
        self.indexing.inflatWordsIndexLength = self.getIntFromRaw(self.position)  # getint
        self.position += LENGTH_INT

        # 单词数
        self.indexing.inflatWordsLength = self.getIntFromRaw(self.position)  # getint
        self.position += LENGTH_INT

        # xml数
        self.indexing.inflatXmlLength = self.getIntFromRaw(self.position)  # getint

        self.position += LENGTH_INT

    def _readHeader(self):
        self.header.type = struct.unpack('i', self.dataRawBytes[self.position:self.position + LENGTH_TYPE])[
            0]  # getType
        self.position += LENGTH_TYPE

        self.header.checksum = self.dataRawBytes[self.position: self.position + LENGTH_CHECKSUM]  # getChecksum
        self.position += LENGTH_CHECKSUM

        self.header.majorVersion = self.dataRawBytes[self.position: self.position + LENGTH_MINOR_VERSION]  # getshort
        self.position += LENGTH_MAJOR_VERSION

        self.header.minorVersion = self.dataRawBytes[self.position: self.position + LENGTH_MINOR_VERSION]  # getshort
        self.position += LENGTH_MINOR_VERSION

        self.header.id = self.dataRawBytes[self.position:self.position + LENGTH_ID]  # getlong
        self.position += LENGTH_ID

        paddingLength = LENGTH_HEADER - self.position - 4
        self.header.padding = self.dataRawBytes[self.position: self.position + paddingLength]  # paddinglength
        self.position += paddingLength

        self.header.infoOffset = struct.unpack('<i', self.dataRawBytes[self.position: self.position + LENGTH_INT])[
            0]  # getint
        self.position += (LENGTH_OFFSET + self.header.infoOffset)

    def _deflateFile(self):
        self.position = (self.indexing.offsetCompressDataHeader + LENGTH_INT * 2)
        _pos = self.position
        flatOffset = self.getIntFromRaw(_pos)
        _pos += LENGTH_INT
        while (flatOffset + _pos) < self.indexing.limit:
            flatOffset = self.getIntFromRaw(_pos)
            _pos += LENGTH_INT
            self.deflateStreams.append(flatOffset)

    def decompress(self):
        """解压"""
        startOffset = self.position
        offset = -1
        # 上一个数据块偏移地址
        lastOffset = startOffset

        # 以下是读取数据块，我想读入内存中

    def _buildDefinitionsArray(self):
        for i in range(0, self.indexing.definitions):
            val = self.getIntFromRaw(self.indexing.offsetIndex + i * LENGTH_INT)
            self.definitionsArray.append(val)

    def getIntFromRaw(self, pos):
        return struct.unpack('i', self.dataRawBytes[pos:pos + LENGTH_INT])[0]


class LingoesInflateDictReader():
    def __int__(self, inflateBuffer, tableLen, wordsLen, xmlsLen):
        self._offsetTable = DictOffsetTable()
        self._dict = {}
        self._inflateBuffer = inflateBuffer
        self._tableLen = tableLen
        self._wordsLen = wordsLen
        self._xmlsLen = xmlsLen
        self._totalLen = self._tableLen + self._wordsLen + self._xmlsLen

        self._wordsOffset = -1
        self._xmlOffset = -1

        self._readDeflate()

    def getDict(self):
        return self._dict

    def _readDictOffset(self):
        _pos = 0
        wordOffset = self.getIntFromRaw(self._inflateBuffer, _pos)
        _pos += LENGTH_INT
        xmlOffset = self.getIntFromRaw(self._inflateBuffer, _pos)
        _pos += LENGTH_INT
        flag = self._inflateBuffer[_pos]
        _pos += 1
        ref = self._inflateBuffer[_pos]

        return DictOffset(wordOffset, xmlOffset, flag, ref)

    def _readDictWord(self, dictOffset, refs):
        indexPos = self._wordsOffset + dictOffset.wordOffset
        wordPos = indexPos + refs * 4
        wordLen = -1
        if dictOffset._next == None:
            wordLen = self._xmlOffset - dictOffset.wordOffset - refs * 4
        else:
            wordLen = dictOffset.getWordLength() - refs * 4

        return self._inflateBuffer[wordPos, wordLen].decode()

    def _readXml(self):
        return

    def _constructOffsetTable(self):
        tableSize = self._tableLen / DictOffset.bytes()
        for i in range(0, tableSize):
            dictOffset = self._readDictOffset()
            self._offsetTable.add(dictOffset)

    def _readDeflate(self):
        self._constructOffsetTable()
        for i in range(0, self._offsetTable.size() - 1):
            dictOffset = self._offsetTable.get(i)
            refs = dictOffset.ref
            dictWord = self._readDictWord(dictOffset, refs)
            wordPosBase = self._wordsOffset + dictOffset.wordOffset

    def getIntFromRaw(self, byteBuff, pos):

        return struct.unpack('i', byteBuff[pos:pos + LENGTH_INT])[0]


if __name__ == '__main__':
    import os

    # LingoesDictReader(os.path.abspath('../../data/localDicts/Vicon English-Chinese(S) Dictionary.ld2'))
    LingoesDictReader(os.path.abspath('../../data/localDicts/dict.ld2')).decompress()
