
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

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
        self.listener = None
        self.start_listener()

    def start_listener(self):
        """启动热键监听器"""
        if self.listener:
            self.listener.stop()

        # 解析热键字符串
        keys = self.parse_hotkey(self.current_hotkey)

        # 创建一个集合来跟踪当前按下的键
        self.pressed_keys = set()

        # 定义回调函数
        def on_press(key):
            # 转换键对象以便于比较
            key_str = self.normalize_key(key)

            # 将按下的键添加到集合
            self.pressed_keys.add(key_str)

            # 检查是否匹配热键组合
            if all(k in self.pressed_keys for k in keys):
                # 触发信号
                self.hotkey_pressed.emit()

        def on_release(key):
            # 转换键对象以便于比较
            key_str = self.normalize_key(key)

            # 将释放的键从集合中移除
            if key_str in self.pressed_keys:
                self.pressed_keys.remove(key_str)

            return True  # 继续监听

        # 启动监听器
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.daemon = True
        self.listener.start()

    def normalize_key(self, key):
        """将pynput键对象转换为字符串表示"""
        if isinstance(key, Key):
            # 特殊键，如F1-F12, Ctrl, Shift等
            return key.name
        if isinstance(key, KeyCode):
            # 常规按键
            return key.char if key.char else f"KeyCode({key.vk})"
        # 其他情况，直接返回字符串表示
        return str(key)

    def parse_hotkey(self, hotkey_str):
        """
        解析热键字符串为键列表

        参数:
            hotkey_str (str): 热键字符串，如"F6"或"Ctrl+Shift+C"

        返回:
            list: 键字符串列表
        """
        parts = hotkey_str.split('+')
        result = []

        for part in parts:
            part = part.strip().lower()

            # 处理特殊键
            if part == 'ctrl':
                result.append('ctrl_l')  # 左Ctrl键
            elif part == 'alt':
                result.append('alt_l')  # 左Alt键
            elif part == 'shift':
                result.append('shift_l')  # 左Shift键
            elif part.startswith('f') and part[1:].isdigit() and 1 <= int(part[1:]) <= 12:
                # F1-F12键
                result.append(f'f{part[1:]}')
            else:
                # 普通键
                result.append(part)

        return result

    def set_hotkey(self, hotkey):
        """
        设置新的热键

        参数:
            hotkey (str): 新的热键字符串
        """
        self.current_hotkey = hotkey

        # 重启监听器以应用新热键
        self.start_listener()

    def get_current_hotkey(self):
        """
        获取当前设置的热键

        返回:
            str: 当前热键字符串
        """
        return self.current_hotkey

    def get_current_hotkey_text(self):
        """
        获取当前热键的显示文本

        返回:
            str: 格式化的热键文本
        """
        return self.current_hotkey

    def unregister_hotkey(self):
        """注销热键监听器"""
        if self.listener:
            self.listener.stop()
            self.listener = None
