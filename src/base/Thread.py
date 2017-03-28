# coding:utf-8
try:
    from PySide.QtCore import QThread, QMutex
except ImportError:
    from PyQt4.QtCore import QThread, QMutex


class WorkThread(QThread):
    def __init__(self, runnable):
        super(WorkThread, self).__init__()
        self.runnable = runnable
        self.stopped = False
        self.mutex = QMutex()

    def run(self, *args, **kwargs):
        self.runnable()
        self.stop()
        self.finished.connect(self.deleteLater)

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = False
        finally:
            self.mutex.unlock()

    def isStopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()
