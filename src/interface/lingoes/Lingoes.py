# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import struct
import zlib

from Bean import *
from StringIO import StringIO
import array
from enum import Enum

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
        # self.withIndexOffset = -1
        self.limit = -1  # 自己加的字段
        self.compressDataOffset = -1

        self.definitions = -1

        self.offsetCompressDataHeader = -1

        self.inflatWordsIndexLength = -1

        self.inflatWordsLength = -1
        self.inflatXmlLength = -1
        self.offsetIndex = -1  # 单词索引的开始位置


class Charset(Enum):
    UTF_8 = 'UTF-8'
    UTF_16LE = 'UTF-16LE'
    UTF_16BE = 'UTF-16BE'
    EUC_JP = 'EUC-JP'


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

        print '文件：', file_path
        print 'type', self.dataRawBytes[0:4].decode()
        print 'version', self.getShortFromRaw(0x18), '.', self.getShortFromRaw(0x1A)
        print 'ID : 0x%x' % self.getLongFromRaw(0x1C)

        offsetData = self.getIntFromRaw(0x5C) + 0x60
        if len(self.dataRawBytes) > offsetData:
            print 'introduce address : 0x%x' % offsetData

            dict_type = self.getIntFromRaw(offsetData)

            print 'introduce type ；0x%x' % dict_type
            offsetWithInfo = self.getIntFromRaw(offsetData + 4) + offsetData + 12

            if dict_type == 3:
                self._readDictionary(offsetData)
            elif len(self.dataRawBytes) > offsetWithInfo - 0x1C:
                self._readDictionary(offsetWithInfo)
            else:
                print '文件不包含字典数据'

        else:
            print '文件不包含字典数据'

        # self._buildDefinitionsArray()
        self._deflateFile()
        self.rawFile.close()

    def _readDictionary(self, startPosition):
        self.position = startPosition
        self.indexing.offsetIndex = self.position + LENGTH_COMPRESS_HEADER
        # todo
        self.indexing.dictType = self.getIntFromRaw(self.position)  # getint

        self.position += LENGTH_INT

        # 压缩数据的结束位置
        self.indexing.limit = self.getIntFromRaw(self.position) + startPosition + 8

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

        print '索引词组数目：', self.indexing.definitions
        print '索引地址/大小：0x%x' % self.indexing.offsetIndex, '/', self.indexing.offsetCompressDataHeader - self.indexing.offsetIndex, 'B'
        print '压缩数据地址/大小：0x%x' % _pos, '/', self.indexing.limit - _pos, 'B'
        print '词组索引地址/大小（解压后）：0x0 /', self.indexing.inflatWordsIndexLength, 'B'

        print '词组地址/大小（解压后）：0x%x' % (self.indexing.inflatWordsIndexLength), \
            '/', self.indexing.inflatWordsLength, 'B'

        print 'XML地址/大小（解压后）：0x%x' % (self.indexing.inflatWordsIndexLength + \
                                      self.indexing.inflatWordsLength), \
            '/', self.indexing.inflatXmlLength, 'B'

        print '文件大小（解压后）：', (self.indexing.inflatWordsIndexLength + \
                             self.indexing.inflatWordsLength + \
                             self.indexing.inflatXmlLength) / 1024, 'KB'

        self.decompress(_pos)

    def decompress(self, startPos):
        """解压"""
        startOffset = startPos
        offset = -1
        # 上一个数据块偏移地址
        lastOffset = startOffset

        # 以下是读取数据块，我想读入内存中
        self.decompressedBuf = StringIO()
        for offsetRelative in self.deflateStreams:
            offset = startOffset + offsetRelative

            target_bytes = array.array('B', self.dataRawBytes[lastOffset:offset])
            dec_temp_buf = zlib.decompress(target_bytes)
            dec_temp_buf = array.array('c', dec_temp_buf)
            self.decompressedBuf.write(dec_temp_buf)
            lastOffset = offset

        print len(self.decompressedBuf.getvalue())
        out_file = open('./out.txt', 'w')
        out_file.write(self.decompressedBuf.getvalue())

    def extract(self, indexFile, extractedWordsFile, extractedXmlFile, extractedOutputFile,
                idxArray, offsetDefs, offsetXml):

        dataLen = 10;
        defTotal = offsetDefs / dataLen - 1
        words = []  # defTotal
        idxData = []  # 6
        defData = []  # 2

        return

    def getIntFromRaw(self, pos):
        return struct.unpack('i', self.dataRawBytes[pos:pos + LENGTH_INT])[0]

    def getShortFromRaw(self, pos):
        return struct.unpack('h', self.dataRawBytes[pos:pos + LENGTH_SHORT])[0]

    def getLongFromRaw(self, pos):
        return struct.unpack('l', self.dataRawBytes[pos:pos + LENGTH_LONG])[0]

    def getInt(self, bytea, pos):
        return struct.unpack('i', bytea[pos:pos + LENGTH_INT])[0]

    def dectectEncodings(self, byteBuf, offsetWords, offsetXml, defTotal,
                         dataLen, idxData, defData, i):
        if (defTotal < 10):
            test = defTotal
        else:
            test = 10

        for wordDec in Charset:
            for xmlDec in Charset:

                try:
                    self.readDefinitionData(byteBuf, offsetWords, offsetXml, dataLen, wordDec, xmlDec,
                                            idxData, defData, test)
                    print '词组编码：', wordDec
                    print 'xml编码：', xmlDec
                    return (wordDec, xmlDec)
                except:
                    pass
        print 'dectect encoding failed default is UTF-16LE'
        return (Charset.UTF_16LE, Charset.UTF_16LE)

    def readDefinitionData(self, bytebuf, offsetWords, offsetXml, dataLen, wordDecoder, xmlDecoder,
                           idxData, defData, i):
        idxData = self.getIdxData(bytebuf, dataLen * i, idxData)
        lastWordPos = idxData[0]
        lastXmlPos = idxData[1]
        flags = idxData[2]
        refs = idxData[3]
        currentWordOffset = idxData[4]
        currentXmlOffset = idxData[5]

        xml = bytebuf[offsetXml + lastXmlPos, offsetXml + currentXmlOffset].decode(xmlDecoder)
        while refs > 0:
            ref = self.getInt(bytebuf, offsetWords + lastWordPos)
            idxData = self.getIdxData(bytebuf, dataLen * ref, idxData)
            lastXmlPos = idxData[0]
            currentXmlOffset = idxData[5]
            if xml == None or xml == '':
                xml = bytebuf[offsetXml + lastXmlPos, offsetXml + currentXmlOffset].decode(xmlDecoder)
            else:
                xml = bytebuf[offsetXml + lastXmlPos, offsetXml + currentXmlOffset].decode(xmlDecoder) + ',' + xml
            lastWordPos += 4
            refs -= 1

        defData[1] = xml
        word = bytebuf[offsetWords + lastWordPos, offsetWords + currentWordOffset].decode(wordDecoder)
        defData[0] = word
        return defData

    def getIdxData(self, bytebuf, pos, wordIdxData=[]):
        wordIdxData[0] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[1] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[2] = bytebuf[pos] & 0xff
        pos += 1
        wordIdxData[3] = bytebuf[pos] & 0xff
        pos += 1
        wordIdxData[4] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[6] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]

        return wordIdxData


class SensitiveStringDecoder():
    def __int__(self, decoder, name):
        self.name = ''
        self.charsetDecoder = decoder
        self.name = name

    def decode(self, ba, off, len):
        return

    def safeTrim(self, ca, len):
        if len == len(ca):
            return ca;
        else:
            return ca[:len]


if __name__ == '__main__':
    import os

    # LingoesDictReader(os.path.abspath('../../data/localDicts/Vicon English-Chinese(S) Dictionary.ld2'))
    LingoesDictReader(os.path.abspath('../../data/localDicts/dict.ld2'))
