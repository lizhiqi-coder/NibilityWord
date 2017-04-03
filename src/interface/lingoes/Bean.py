# coding:utf-8

class DictOffset():
    def __int__(self, wordOffset, xmlOffset, flag, ref):
        self.wordOffset = wordOffset  # int
        self.xmlOffset = xmlOffset  # int
        self.flag = flag  # byte
        self.ref = ref  # byte

        self._prev = DictOffset(None, None, None, None)
        self._next = DictOffset(None, None, None, None)

    def setPrev(self, prev):
        self._prev = prev

    def setNext(self, _next):
        self._next = _next

    def getWordLength(self):
        return self._next.wordOffset - self._prev.wordOffset

    def getXmlLength(self):
        return self._next.xmlOffset - self._prev.xmlOffset

    def toString(self):
        return "DictOffset{" + \
               "wordOffset=" + self.wordOffset + \
               ", xmlOffset=" + self.xmlOffset + \
               ", flag=" + self.flag + \
               ", ref=" + self.ref + \
               '}'

    @staticmethod
    def bytes():
        return 10


class DictOffsetTable():
    def __int__(self):
        self.data = []
        self.last = None

    def add(self, dictOffset):
        if self.last != None:
            self.last.setNext(dictOffset)
            dictOffset.setPrev(self.last)

        self.last = dictOffset
        self.data.append(dictOffset)

    def get(self, i):
        return self.data[i]

    def size(self):
        return len(self.data)
