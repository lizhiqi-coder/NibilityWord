# coding:utf-8

try:
    import pyHook
    import pythoncom
except:

    pass
import threading


class InputDeviceManager():
    _INSTANCE = None

    @staticmethod
    def getInstance():
        return InputDeviceManager()

    def __new__(cls, *args, **kwargs):
        if not InputDeviceManager._INSTANCE:
            try:
                threading.Lock().acquire()
                InputDeviceManager._INSTANCE = super(InputDeviceManager, cls).__init__()
            finally:
                threading.Lock().release()
        return InputDeviceManager._INSTANCE

    def __init__(self):
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self._onKeyEvent
        self.hm.mouse_hook = self._onMouseEvent
        self.hm.HookKeyboard()
        self.hm.HookMouse()
        pythoncom.PumpMessages()

        self.SHOETCUT_MAP = {}
        pass

    # 目前就支持两个组合键
    def setShortcut(self, shortcut_name, runnable):
        self.SHOETCUT_MAP[shortcut_name] = runnable

    def _onKeyEvent(self, event):
        print str(event.KeyID)

    def _onMouseEvent(self, event):
        pass
