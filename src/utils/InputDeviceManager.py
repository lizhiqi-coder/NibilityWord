# coding:utf-8


import threading

import NBUtils

try:
    import pyHook
    import pythoncom
except:
    pass
try:
    from evdev import InputDevice, InputEvent
    from select import select
except:
    pass

try:
    from PySide.QtCore import *
except ImportError:
    from PyQt4.QtCore import *

"""
/dev/input
event0:keyboard
event2:mouse
event4:touch pad

"""
try:
    if NBUtils.getPlatform() == NBUtils.PLATFROM_LINUX:
        KEY_CTRL = 29
        KEY_ALT = 56
        KET_SHIFT = 42
        KEY_SPACE = 57
        control_keys = [KEY_ALT, KEY_CTRL, KET_SHIFT, KEY_SPACE]

        KEY_F = 33

    if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
        KEY_ALT = 32
        KEY_F = 70
except:
    pass


class InputDeviceManager(QObject):
    _INSTANCE = None
    if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
        sin = Signal(pyHook.KeyboardEvent)
    else:
        sin = Signal(InputEvent)

    @staticmethod
    def getInstance():
        if InputDeviceManager._INSTANCE == None:
            InputDeviceManager._INSTANCE = InputDeviceManager()
        return InputDeviceManager._INSTANCE

    def __init__(self):
        super(InputDeviceManager, self).__init__()
        self.SHOETCUT_MAPS = {}
        self.first_key_down = False
        self.first_key = -1
        self.sin.connect(self._onKeyEvent)
        if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:

            self.hm = pyHook.HookManager()
            self.hm.KeyDown = self.overrideKeyDown
            self.hm.mouse_hook = self._onMouseEvent
            self.hm.HookKeyboard()
            self.hm.HookMouse()
            work = threading.Thread(target=self._listening_w)
            work.setDaemon(True)
            work.start()

        else:
            # linux 平台
            print("this is linux platform")
            # self.dev = InputDevice('/dev/input/event0')
            # work = threading.Thread(target=self._listening)
            # work.setDaemon(True)
            # work.start()

    def overrideKeyDown(self, event):
        self.sin.emit(event)
        return True

    def _listening_w(self):
        pythoncom.PumpMessages()

    def _listening(self):
        while True:
            select([self.dev], [], [])
            for event in self.dev.read():
                self.sin.emit(event)

    # 目前就支持两个组合键
    def addShortcut(self, shortcut_name, runnable):
        self.SHOETCUT_MAPS[shortcut_name] = runnable

    @Slot()
    def _onKeyEvent(self, event):
        """
        该方法应该放到主线程中执行
        """
        if NBUtils.getPlatform() == NBUtils.PLATFROM_WINDOWS:
            for key_map in self.SHOETCUT_MAPS:
                if key_map[0] == KEY_ALT and event.Alt == KEY_ALT and event.KeyID == key_map[1]:
                    runnable = self.SHOETCUT_MAPS[key_map]
                    runnable()

        else:
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
