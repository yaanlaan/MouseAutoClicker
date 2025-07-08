
import os
import json
from PyQt5.QtCore import QSettings

from utils.constants import DEFAULT_INTERVAL, DEFAULT_LANGUAGE, DEFAULT_HOTKEY

class ConfigManager:
    """配置管理器，负责保存和加载用户设置"""

    def __init__(self):
        """初始化配置管理器"""
        self.settings = QSettings("AutoClicker", "MouseAutoClicker")
        self.load_config()

    def load_config(self):
        """加载配置"""
        # 点击间隔
        self.click_interval = self.settings.value("click_interval", DEFAULT_INTERVAL, type=int)

        # 热键
        self.hotkey = self.settings.value("hotkey", DEFAULT_HOTKEY, type=str)

        # 语言
        self.language = self.settings.value("language", DEFAULT_LANGUAGE, type=str)

        # 退出时行为（是否完全退出）
        self.exit_on_close = self.settings.value("exit_on_close", False, type=bool)

    def save_config(self):
        """保存配置"""
        # 点击间隔
        self.settings.setValue("click_interval", self.click_interval)

        # 热键
        self.settings.setValue("hotkey", self.hotkey)

        # 语言
        self.settings.setValue("language", self.language)

        # 退出时行为
        self.settings.setValue("exit_on_close", self.exit_on_close)

        # 确保设置被写入
        self.settings.sync()

    def get_click_interval(self):
        """获取点击间隔"""
        return self.click_interval

    def set_click_interval(self, interval):
        """设置点击间隔"""
        self.click_interval = interval

    def get_hotkey(self):
        """获取热键"""
        return self.hotkey

    def set_hotkey(self, hotkey):
        """设置热键"""
        self.hotkey = hotkey

    def get_language(self):
        """获取语言"""
        return self.language

    def set_language(self, language):
        """设置语言"""
        self.language = language

    def get_exit_on_close(self):
        """获取关闭行为设置"""
        return self.exit_on_close

    def set_exit_on_close(self, value):
        """设置关闭行为"""
        self.exit_on_close = value
