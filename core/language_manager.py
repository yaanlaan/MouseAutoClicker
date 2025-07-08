
from utils.constants import TRANSLATIONS

class LanguageManager:
    """语言管理器，负责处理多语言文本"""

    def __init__(self, language_code):
        """
        初始化语言管理器

        参数:
            language_code (str): 语言代码，如"zh_CN"或"en_US"
        """
        self.set_language(language_code)

    def set_language(self, language_code):
        """
        设置当前语言

        参数:
            language_code (str): 语言代码
        """
        self.language_code = language_code

        # 确保语言代码有效
        if language_code not in TRANSLATIONS:
            self.language_code = "zh_CN"  # 默认使用中文

    def get_text(self, key):
        """
        获取特定键的翻译文本

        参数:
            key (str): 文本键

        返回:
            str: 翻译后的文本，如果没有找到翻译则返回键本身
        """
        if key in TRANSLATIONS[self.language_code]:
            return TRANSLATIONS[self.language_code][key]

        # 如果在当前语言中找不到，尝试使用中文
        if key in TRANSLATIONS["zh_CN"]:
            return TRANSLATIONS["zh_CN"][key]

        # 如果仍然找不到，返回键本身
        return key
