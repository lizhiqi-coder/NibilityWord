# coding:utf-8


import threading

import NBUtils


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
        if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
            try:
                import pyHook
                import pythoncom
            except:
                pass
            self.hm = pyHook.HookManager()
            self.hm.KeyDown = self._onKeyEvent
            self.hm.mouse_hook = self._onMouseEvent
            self.hm.HookKeyboard()
            self.hm.HookMouse()
            pythoncom.PumpMessages()

        else:
            # linux 平台
            try:
                from evdev import InputDevice
                from select import select
            except:
                pass
            dev = InputDevice('/dev/input/event4')
            mice=InputDevice
            while True:
                select([dev], [], [])
                for event in dev.read():
                    if (event.value == 1) and event.code != 0:
                        # print "key %s: " % (event.code)
                        self._onKeyEvent(event)

        self.SHOETCUT_MAP = {}
        pass

    # 目前就支持两个组合键
    def setShortcut(self, shortcut_name, runnable):
        self.SHOETCUT_MAP[shortcut_name] = runnable

    def _onKeyEvent(self, event):
        if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
            print str(event.KeyID)
        else:
            print 'key  %s, value %s' % (event.code, event.value)

    def _onMouseEvent(self, event):
        pass
