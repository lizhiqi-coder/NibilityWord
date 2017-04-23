# coding:utf-8

try:
    from PySide.QtCore import *
except:
    from PyQt4.QtCore import *

import array
import struct
import zlib
from io import BytesIO

from Bean import *
import xml.etree.ElementTree as ET
from src.model.DetailModel import DictResult
import linecache
import re
from src.utils import NBUtils
import os
from BpTree import Node

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
        self.raw_file_path = file_path
        self.cooked_file_path = os.path.splitext(self.raw_file_path)[0] + '.cooked'
        if os.path.exists(self.cooked_file_path) and os.path.getsize(self.cooked_file_path):
            return

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

        self.header.infoOffset = struct.unpack('i', self.dataRawBytes[_pos: _pos + LENGTH_INT])[
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

        cooked_file = open(self.cooked_file_path, 'w')
        cooked_file.truncate()

        DICT_OFFSET_LENGTH = DictOffset.bytes()
        defTotal = offsetDefs / DICT_OFFSET_LENGTH - 1

        totalWords = [''] * defTotal
        totalXmls = [''] * defTotal
        wordsLen = [0] * defTotal

        indexData = [0] * 6
        wordData = [''] * 2  # word,xml

        encodings = self.dectectEncodings(inflatedBytes, offsetDefs, offsetXml)

        _pos = 8
        counter = 0

        for i in range(0, defTotal):
            # sys.stdout.write('\rcomplete precent :%.0f %%' % ((i * 100.0) / defTotal))
            # sys.stdout.flush()
            # 向indexData和wordData中写入数据
            try:
                indexData, wordData = self.readDefinitionData(inflatedBytes, offsetDefs, offsetXml, encodings[0],
                                                              encodings[1], i)
                totalWords[i] = wordData[0]

                totalXmls[i] = wordData[1]
                wordsLen[i] = wordData[1].__len__()

                # 写入缓存文件
                line = wordData[0] + '=' + wordData[1] + '\n'
                cooked_file.write(line.encode(encodings[0]))
                counter += 1
            except Exception, e:
                print i, 'Exception->', e

        cooked_file.close()
        print '\n'
        # print totalWords
        # print totalXmls
        print '成功读取 %d 组数据' % counter

    def getIntFromRaw(self, pos):
        return struct.unpack('i', self.dataRawBytes[pos:pos + LENGTH_INT])[0]

    def getShortFromRaw(self, pos):
        return struct.unpack('h', self.dataRawBytes[pos:pos + LENGTH_SHORT])[0]

    def getLongFromRaw(self, pos):
        return struct.unpack('q', self.dataRawBytes[pos:pos + LENGTH_LONG])[0]

    def getInt(self, bytea, pos):
        return struct.unpack('i', bytea[pos:pos + LENGTH_INT])[0]

    def dectectEncodings(self, byteBuf, offsetWords, offsetXml):

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
            lastXmlPos = idxData[1]
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

        return wordIdxData

    def getCookedFile(self):
        if os.path.exists(self.cooked_file_path):
            return self.cooked_file_path
        else:
            return None


class Lingoes():
    TAG_EXPLEIN = 'N'
    TAG_POS = 'U'
    TAG_EOW = 'E'
    TAG_PHONE = 'M'
    TAG_ROOT = 'C'

    MAX_FAST_ENTRY = 10

    DICT_SPLIT = '='
    INDEX_LEVEL = 3

    def __init__(self, dict_file_name):
        self.dict_file_name = dict_file_name
        # find file path
        raw_file_path = os.path.join(NBUtils.getRootDir(), 'data/localDicts/', self.dict_file_name)
        self.cooked_file_path = LingoesDictReader(raw_file_path).getCookedFile()
        if self.cooked_file_path == None:
            return
        self.indexing = self.buildIndex()
        linecache.checkcache(self.cooked_file_path)

    def buildIndexTree(self):
        cooked_file = open(self.cooked_file_path, 'r')
        line = cooked_file.readline()
        line_index = 1
        root = Node()
        while line:
            input_node = root
            head_word = line.split(self.DICT_SPLIT)[0]
            for i in range(len(head_word)):
                if i >= self.INDEX_LEVEL:
                    break
                char = head_word[i].lower()
                child_node = input_node.findChildByKey(char)

                if child_node:
                    child_node.value = line_index
                else:
                    child_node = Node(key=char, value=line_index, father=input_node)
                    input_node.addChild(child_node)

                input_node = child_node
        return root
        cooked_file.close()

    def buildIndex(self):
        """建立二级索引"""
        cooked_file = open(self.cooked_file_path, 'r')

        line = cooked_file.readline()
        line_index = 1
        # indexing = [[-1] * 27] * 26  # 第二个为空的情况 创建列表，会导致重复
        indexing = [[-1] * 27 for i in range(26)]
        indexing[0][0] = line_index

        while line:
            idx = [-1] * 2
            for char in line.split('=')[0]:
                if idx[0] == -1 and char.isalpha() and 'a' <= char.lower() <= 'z':

                    idx[0] = ord(char.lower()) - ord('a')

                elif idx[0] != -1 and idx[1] == -1 and char.isalpha() and 'a' <= char.lower() <= 'z':
                    idx[1] = ord(char.lower()) - ord('a') + 1

                    break
            if idx[1] == -1:
                idx[1] = 0

            indexing[idx[0]][idx[1]] = line_index

            line = cooked_file.readline()
            line_index += 1

        cooked_file.close()

        return indexing

    def searchTree(self, str):
        root = self.buildIndexTree()

        node = root
        str_i = 0
        while node.findChildByKey(str[str_i]) and str_i < len(str):
            node = node.findChildByKey(str[str_i])
            str_i += 1
        end = node.value

        if node.preBrother:
            start = node.preBrother.value + 1
        else:
            father = node.father
            while father.preBrother == None:
                if father == root:
                    break
                father = father.father
            if father == root:
                start = 1
            else:
                last_end_node = father
                while last_end_node.endChind:
                    last_end_node = last_end_node.endChind
                start = last_end_node.value + 1

        return start, end

    def __del__(self):
        linecache.clearcache()
        pass

    def getFastEntry(self, key):
        row = ord(key[0]) - ord('a')
        if len(key) == 1:
            start = self.indexing[row][0]
            end = self.indexing[row][ord('z') - ord('a') + 1]
        if len(key) >= 2 and key[1].isalpha():
            col = ord(key[1]) - ord('a') + 1
            if self.indexing[col] == -1:
                return  # 不存在第二字母为key[1]的单词索引
            else:
                end = self.indexing[row][col]
                pre_offset = 1
                while self.indexing[row][col - pre_offset] == -1 and col - pre_offset > 0:
                    pre_offset += 1
                start = self.indexing[row][col - pre_offset] + 1

        matched_entry_list = []
        for i in range(start, end + 1):
            line = linecache.getline(self.cooked_file_path, i)
            word = line.split('=')[0].strip()
            pattern = r'^\s*' + key + r'\S*\s*'
            if re.match(pattern, word):
                xml = line.split('=')[1].strip()

                EOW, phones, explains = self._parseXml(xml)

                dictResult = DictResult(query=word,
                                        translation=None,
                                        phones=phones,
                                        explains=explains)
                matched_entry_list.append(dictResult)
                if len(matched_entry_list) >= self.MAX_FAST_ENTRY:
                    break

        return matched_entry_list

    def _parseXml(self, str):
        root_head = '<' + self.TAG_ROOT + '>'
        root_end = '</' + self.TAG_ROOT + '>'
        xmls = str.split(root_end + ',' + root_head)
        EOW = []
        phones = []
        explains = []

        for xml in xmls:
            if not xml.startswith(root_head):
                xml = root_head + xml
            if not xml.endswith(root_end):
                xml = xml + root_end

            a, b, c = self._parseXmlInter(xml)
            EOW.extend(a)
            phones.extend(b)
            explains.extend(c)

        return EOW, phones, explains

    def _parseXmlInter(self, xml_str):
        """
        parts of speech POS
        exchange of word EOW
        explains
        phones
        """
        EOW = []
        phones = []
        explains = []

        root = ET.fromstring(xml_str)

        for explain_xml in root.iter(self.TAG_EXPLEIN):

            if len(explain_xml) > 0 and explain_xml[0].tag == self.TAG_POS:  # 存在词性
                explain = explain_xml[0].text + explain_xml[0].tail

            else:
                if explain_xml.text == None:
                    continue
                else:
                    explain = explain_xml.text

            explains.append(explain)

        for phone_xml in root.iter(self.TAG_PHONE):
            if phone_xml.text == None:
                continue
            phones.append(phone_xml.text)

        EOW_xml = root.find(self.TAG_EOW)
        if EOW_xml != None:
            EOW = EOW_xml.text.split('|')

        return EOW, phones, explains


if __name__ == '__main__':
    pass
