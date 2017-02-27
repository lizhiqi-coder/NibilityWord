# coding:utf-8
try:
    from PySide.QtCore import QThread
except:
    from PyQt4.QtCore import QThread


class TranslateThread(QThread):
    def __init__(self):
        super(TranslateThread, self).__init__()

    def run(self, *args, **kwargs):


        pass
    def finished(self, *args, **kwargs):
        pass

    def postResult(self):
        pass

    
