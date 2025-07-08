
import sys
import os

def resource_path(relative_path):
    """获取资源的绝对路径，用于处理PyInstaller打包后的路径问题"""
    try:
        # PyInstaller创建临时文件夹，存储路径存储在_MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
