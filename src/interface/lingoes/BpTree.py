# coding:utf-8

# B* tree
class Node():
    def __init__(self, key='', value=-1, father=None):
        self.key = key
        self.value = value
        self.children = {}
        self.father = father
        self.preBrother = None
        self.nextBrother = None
        self.startChild = None
        self.endChind = None

    def addChild(self, child):
        if len(self.children) == 0:
            self.startChild = child
            self.endChind = self.startChild
            self.children[child.key] = child
        else:
            self.children[child.key] = child
            self.endChind.nextBrother = child
            child.preBrother = self.endChind
            self.endChind = child

    def findChildByKey(self, char):
        if self.children.has_key(char):
            child = self.children[char]
            return child
        else:
            return False


if __name__ == '__main__':
    list = ['q', 'ew']

    print '1'.lower()
