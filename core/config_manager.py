
import os
import yaml
from pathlib import Path

from utils.constants import DEFAULT_INTERVAL, DEFAULT_LANGUAGE, DEFAULT_HOTKEY

class ConfigManager:
    """配置管理器，负责保存和加载用户设置"""

    def __init__(self):
        """初始化配置管理器"""
        # 获取用户文档目录下的配置文件路径
        self.config_dir = os.path.join(Path.home(), ".mouse_auto_clicker")
        self.config_file = os.path.join(self.config_dir, "config.yaml")

        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # 加载配置
        self.load_config()

    def load_config(self):
        """加载配置"""
        # 默认配置
        self.config = {
            "click_interval": DEFAULT_INTERVAL,
            "hotkey": DEFAULT_HOTKEY,
            "hotkey_enabled": True,
            "language": DEFAULT_LANGUAGE,
            "exit_on_close": False
        }

        # 如果配置文件存在，则从文件加载
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = yaml.safe_load(f)
                    if loaded_config and isinstance(loaded_config, dict):
                        self.config.update(loaded_config)
            except Exception as e:
                print(f"加载配置文件时出错: {e}")

    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"保存配置文件时出错: {e}")

    def get_click_interval(self):
        """获取点击间隔"""
        return self.config["click_interval"]

    def set_click_interval(self, interval):
        """设置点击间隔"""
        self.config["click_interval"] = interval

    def get_hotkey(self):
        """获取热键"""
        return self.config["hotkey"]

    def set_hotkey(self, hotkey):
        """设置热键"""
        self.config["hotkey"] = hotkey

    def get_hotkey_enabled(self):
        """获取热键启用状态"""
        return self.config["hotkey_enabled"]

    def set_hotkey_enabled(self, enabled):
        """设置热键启用状态"""
        self.config["hotkey_enabled"] = enabled

    def get_language(self):
        """获取语言"""
        return self.config["language"]

    def set_language(self, language):
        """设置语言"""
        self.config["language"] = language

    def get_exit_on_close(self):
        """获取关闭行为设置"""
        return self.config["exit_on_close"]

    def set_exit_on_close(self, value):
        """设置关闭行为"""
        self.config["exit_on_close"] = value

