import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button

class HotkeyManager(QObject):
    """热键管理器，处理全局热键监听和触发"""

    # 定义信号
    hotkey_pressed = pyqtSignal()

    def __init__(self, hotkey=None):
        """
        初始化热键管理器

        参数:
            hotkey (str): 热键字符串，如"F6"或"Ctrl+Shift+C"
        """
        super().__init__()

        # 默认热键为F6
        self.default_hotkey = "F6"
        self.current_hotkey = hotkey if hotkey else self.default_hotkey

        # 热键监听器
        self.keyboard_listener = None
        self.mouse_listener = None
        self.start_listener()

    def start_listener(self):
        """启动热键监听器"""
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

        # 解析热键字符串
        keys = self.parse_hotkey(self.current_hotkey)
        # 创建一个集合来跟踪当前按下的键
        self.pressed_keys = set()

        # 定义键盘回调函数
        def on_press(key):
            key_str = self.normalize_key(key)
            self.pressed_keys.add(key_str)
            if all(k in self.pressed_keys for k in keys):
                self.pressed_keys.remove(key_str)
                self.hotkey_pressed.emit()

        def on_release(key):
            key_str = self.normalize_key(key)
            if key_str in self.pressed_keys:
                self.pressed_keys.remove(key_str)
            return True

        # 定义鼠标回调函数
        def on_click(x, y, button, pressed):
            key_str = self.normalize_key(button)
            
            if pressed:
                self.pressed_keys.add(key_str)
                if all(k in self.pressed_keys for k in keys):
                    self.pressed_keys.remove(key_str)
                    self.hotkey_pressed.emit()
            else:
                if key_str in self.pressed_keys:
                    self.pressed_keys.remove(key_str)

        # 启动键盘监听器
        self.keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.keyboard_listener.daemon = True
        self.keyboard_listener.start()

        # 启动鼠标监听器
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

    def normalize_key(self, key):
        if isinstance(key, Key):
            return key.name
        if isinstance(key, KeyCode):
            return key.char if key.char else f"KeyCode({key.vk})"
        if isinstance(key, Button):
            return f"mouse_{key.name}"
        return str(key)

    def parse_hotkey(self, hotkey_str):
        parts = hotkey_str.split('+')
        result = []

        for part in parts:
            part = part.strip().lower()

            if part == 'ctrl':
                result.append('ctrl_l')
            elif part == 'alt':
                result.append('alt_l')
            elif part == 'shift':
                result.append('shift_l')
            elif part.startswith('f') and part[1:].isdigit() and 1 <= int(part[1:]) <= 12:
                result.append(f'f{part[1:]}')
            elif part in ['mouse_left', 'mouse_right', 'mouse_middle', 'mouse_x1', 'mouse_x2']:
                result.append(part)
            else:
                result.append(part)

        return result

    def set_hotkey(self, hotkey):
        self.current_hotkey = hotkey
        self.start_listener()

    def get_current_hotkey(self):
        return self.current_hotkey

    def get_current_hotkey_text(self):
        return self.current_hotkey

    def unregister_hotkey(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
