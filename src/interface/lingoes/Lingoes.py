# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import array
import struct
import sys
import zlib
from io import BytesIO

from Bean import *

"""
读取二进制文件->读取头->读取索引->读取数据块(blocks)

"""

LENGTH_SHORT = 2
LENGTH_INT = 4

"""
java: long->8 int ->4
C: long long ->8 long->4 int ->4
"""
LENGTH_LONG = 8

LENGTH_HEADER = 96
LENGTH_TYPE = LENGTH_INT
LENGTH_CHECKSUM = 20
LENGTH_MAJOR_VERSION = LENGTH_SHORT
LENGTH_MINOR_VERSION = LENGTH_SHORT
LENGTH_ID = LENGTH_LONG
LENGTH_OFFSET = LENGTH_INT
LENGTH_COMPRESS_HEADER = LENGTH_INT * 7

UTF_8 = 'UTF-8'
UTF_16LE = 'UTF-16LE'
UTF_16BE = 'UTF-16BE'
EUC_JP = 'EUC-JP'

CHARSET_LSIT = (UTF_8, UTF_16LE, UTF_16BE, EUC_JP)


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


class LingoesDictReader():
    def __init__(self, file_path):
        # 索引数组
        self.definitionsArray = []
        # 压缩数据块数组
        self.deflateStreams = []

        self.rawFile = open(file_path, 'rb')
        self.dataRawBytes = bytearray(self.rawFile.read())

        self.header = Header()
        self.indexing = Indexing()

        self._readHeader()

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

        self.rawFile.close()

    def _readDictionary(self, startPosition):
        _pos = startPosition
        self.indexing.offsetIndex = _pos + LENGTH_COMPRESS_HEADER

        self.indexing.dictType = self.getIntFromRaw(_pos)  # getint

        _pos += LENGTH_INT

        # 压缩数据的结束位置
        self.indexing.limit = self.getIntFromRaw(_pos) + startPosition + 8

        _pos += LENGTH_INT

        self.indexing.compressDataOffset = self.getIntFromRaw(_pos)  # getint

        self.indexing.definitions = self.indexing.compressDataOffset / LENGTH_INT

        self.indexing.offsetCompressDataHeader = self.indexing.compressDataOffset + self.indexing.offsetIndex

        _pos += LENGTH_INT

        # 索引单词长度
        self.indexing.inflatWordsIndexLength = self.getIntFromRaw(_pos)  # getint
        _pos += LENGTH_INT

        # 单词数
        self.indexing.inflatWordsLength = self.getIntFromRaw(_pos)  # getint
        _pos += LENGTH_INT

        # xml数
        self.indexing.inflatXmlLength = self.getIntFromRaw(_pos)  # getint

        _pos += LENGTH_INT

        self.getInflateBuf()
        self.extract(self.decompressedBuf.getvalue(), self.indexing.inflatWordsIndexLength,
                     self.indexing.inflatWordsIndexLength + self.indexing.inflatWordsLength)

    def _readHeader(self):
        _pos = 0
        self.header.type = struct.unpack('i', self.dataRawBytes[_pos:_pos + LENGTH_TYPE])[
            0]  # getType
        _pos += LENGTH_TYPE

        self.header.checksum = self.dataRawBytes[_pos: _pos + LENGTH_CHECKSUM]  # getChecksum
        _pos += LENGTH_CHECKSUM

        self.header.majorVersion = self.dataRawBytes[_pos: _pos + LENGTH_MINOR_VERSION]  # getshort
        _pos += LENGTH_MAJOR_VERSION

        self.header.minorVersion = self.dataRawBytes[_pos: _pos + LENGTH_MINOR_VERSION]  # getshort
        _pos += LENGTH_MINOR_VERSION

        self.header.id = self.dataRawBytes[_pos:_pos + LENGTH_ID]  # getlong
        _pos += LENGTH_ID

        paddingLength = LENGTH_HEADER - _pos - 4
        self.header.padding = self.dataRawBytes[_pos: _pos + paddingLength]  # paddinglength
        _pos += paddingLength

        self.header.infoOffset = struct.unpack('<i', self.dataRawBytes[_pos: _pos + LENGTH_INT])[
            0]  # getint
        _pos += (LENGTH_OFFSET + self.header.infoOffset)

        self.header.infoPosition = _pos

    def getInflateBuf(self):
        _pos = (self.indexing.offsetCompressDataHeader + LENGTH_INT * 2)
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

        t_pos = self.indexing.offsetIndex
        self.definitionsArray = [-1] * self.indexing.definitions
        for i in range(0, self.indexing.definitions):
            self.definitionsArray[i] = self.getIntFromRaw(t_pos)
            t_pos += LENGTH_INT

    def decompress(self, startPos):
        """解压"""
        startOffset = startPos
        offset = -1
        # 上一个数据块偏移地址
        lastOffset = startOffset

        # 以下是读取数据块，我想读入内存中
        self.decompressedBuf = BytesIO()
        for offsetRelative in self.deflateStreams:
            offset = startOffset + offsetRelative

            target_bytes = array.array('B', self.dataRawBytes[lastOffset:offset])
            dec_temp_buf = zlib.decompress(target_bytes)

            self.decompressedBuf.write(dec_temp_buf)
            lastOffset = offset

    def extract(self, inflatedBytes, offsetDefs, offsetXml):
        DICT_OFFSET_LENGTH = DictOffset.bytes()
        defTotal = offsetDefs / DICT_OFFSET_LENGTH - 1

        print 'def total is -> ', defTotal
        totalWords = [''] * defTotal
        totalXmls = [''] * defTotal
        wordsLen = [0] * defTotal

        indexData = [0] * 6
        wordData = [''] * 2  # word,xml

        encodings = self.dectectEncodings(inflatedBytes, offsetDefs, offsetXml)

        _pos = 8
        counter = 0

        # 两个变量不知道是干嘛的
        fn, pn = 1, 0
        dictOffset = DictOffset()

        for i in range(0, defTotal):
            sys.stdout.write('\rcomplete precent :%.0f %%' % ((i * 100.0) / defTotal))
            sys.stdout.flush()
            # 向indexData和wordData中写入数据
            try:
                indexData, wordData = self.readDefinitionData(inflatedBytes, offsetDefs, offsetXml, encodings[0],
                                                              encodings[1], i)
                totalWords[i] = wordData[0]

                # totalXmls[i] = wordData[1]
                wordsLen[i] = wordData[1].__len__()
                counter += 1
            except Exception, e:
                print '\n', i, 'Exception->', e

        print totalWords
        # print totalXmls
        print '成功读出%d组数据。' % counter

    def getIntFromRaw(self, pos):
        return struct.unpack('i', self.dataRawBytes[pos:pos + LENGTH_INT])[0]

    def getShortFromRaw(self, pos):
        return struct.unpack('h', self.dataRawBytes[pos:pos + LENGTH_SHORT])[0]

    def getLongFromRaw(self, pos):
        return struct.unpack('q', self.dataRawBytes[pos:pos + LENGTH_LONG])[0]

    def getInt(self, bytea, pos):
        return struct.unpack('i', bytea[pos:pos + LENGTH_INT])[0]

    def dectectEncodings(self, byteBuf, offsetWords, offsetXml):
        _indexData = [0] * 6
        _wordData = [''] * 2  # word,xml

        for wordDec in CHARSET_LSIT:
            for xmlDec in CHARSET_LSIT:

                try:
                    self.readDefinitionData(byteBuf, offsetWords, offsetXml, wordDec, xmlDec, 10)
                    print '词组编码：', wordDec
                    print 'xml编码：', xmlDec
                    return (wordDec, xmlDec)
                except:
                    pass
        print 'dectect encoding failed default is UTF-16LE'
        return (UTF_16LE, UTF_16LE)

    def readDefinitionData(self, bytebuf, offsetWords, offsetXml, wordDecoder, xmlDecoder, i):
        idxData = self.getIdxData(bytebuf, DictOffset.bytes() * i)  # size=6
        defData = [''] * 2
        lastWordPos = idxData[0]
        lastXmlPos = idxData[1]
        flags = idxData[2]
        refs = idxData[3]
        currentWordOffset = idxData[4]
        currentXmlOffset = idxData[5]

        xml = bytebuf[offsetXml + lastXmlPos:offsetXml + currentXmlOffset].decode(xmlDecoder)
        while refs > 0:
            ref = self.getInt(bytebuf, offsetWords + lastWordPos)
            idxData = self.getIdxData(bytebuf, DictOffset.bytes() * ref)
            lastXmlPos = idxData[0]
            currentXmlOffset = idxData[5]

            if xml == None or xml == '':
                xml = bytebuf[offsetXml + lastXmlPos:offsetXml + currentXmlOffset].decode(xmlDecoder)
            else:
                xml = bytebuf[offsetXml + lastXmlPos:offsetXml + currentXmlOffset].decode(xmlDecoder) + ',' + xml
            lastWordPos += 4
            refs -= 1

        defData[1] = xml  # 原始xml数据，没有被修剪，包含一些标记语言标签
        word = bytebuf[(offsetWords + lastWordPos):(offsetWords + currentWordOffset)].decode(wordDecoder)
        defData[0] = word

        return idxData, defData

    def getIdxData(self, bytebuf, pos):
        # tepos = pos
        # try:
        wordIdxData = [0] * 6
        wordIdxData[0] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[1] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[2] = struct.unpack('b', bytebuf[pos])[0] & 0xff
        pos += 1
        wordIdxData[3] = struct.unpack('b', bytebuf[pos])[0] & 0xff
        pos += 1
        wordIdxData[4] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        pos += LENGTH_INT
        wordIdxData[5] = struct.unpack('i', bytebuf[pos:pos + LENGTH_INT])[0]
        # except:
        # print bytebuf[pos:pos + LENGTH_INT]

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
