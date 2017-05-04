# coding:utf-8


import threading

import NBUtils

"""
/dev/input
event0:keyboard
event2:mouse
event4:touch pad

"""
KEY_CTRL = 29
KEY_ALT = 56
KET_SHIFT = 42
KEY_SPACE = 57
control_keys = [KEY_ALT, KEY_CTRL, KET_SHIFT, KEY_SPACE]

KEY_F = 33


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
        self.SHOETCUT_MAPS = {}
        self.first_key_down = False
        self.first_key = -1
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
                import threading
            except:
                pass
            self.dev = InputDevice('/dev/input/event0')
            work = threading.Thread(target=self._listening)
            work.setDaemon(True)
            work.start()

    def _listening(self):
        from select import select
        while True:
            select([self.dev], [], [])
            for event in self.dev.read():
                self._onKeyEvent(event)

    # 目前就支持两个组合键
    def addShortcut(self, shortcut_name, runnable):
        self.SHOETCUT_MAPS[shortcut_name] = runnable

    def _onKeyEvent(self, event):
        if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
            print str(event.KeyID)
        else:
            print 'key  %s, value %s' % (event.code, event.value)
            if self.first_key_down and event.value == 1:
                for key_map in self.SHOETCUT_MAPS:
                    if self.first_key == key_map[0]:  # 命中第一个按键
                        if event.code == key_map[1]:
                            runnable = self.SHOETCUT_MAPS[key_map]
                            runnable()

            if event.code in control_keys and event.value == 1:
                self.first_key_down = True
                self.first_key = event.code
            if event.code in control_keys and event.value == 0:
                self.first_key_down = False
                self.first_key = -1

    def _onMouseEvent(self, event):
        pass


def run():
    print 'run'


if __name__ == "__main__":
    InputDeviceManager.getInstance().addShortcut((KEY_ALT, KEY_F), runnable=run)
    pass
