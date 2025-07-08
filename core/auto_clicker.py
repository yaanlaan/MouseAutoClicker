
import time
from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Button, Controller

class AutoClickerThread(QThread):
    """自动点击线程，负责在后台执行连续点击操作"""

    def __init__(self, interval):
        """
        初始化自动点击线程

        参数:
            interval (int): 点击间隔，单位为毫秒
        """
        super().__init__()
        self.mouse = Controller()
        self.interval = interval / 1000.0  # 转换为秒
        self.running = False

    def run(self):
        """线程主函数，执行连续点击"""
        self.running = True

        while self.running:
            # 执行鼠标点击
            self.mouse.click(Button.left)

            # 等待指定的间隔时间
            time.sleep(self.interval)

    def stop(self):
        """停止点击线程"""
        self.running = False
        self.wait()  # 等待线程结束

    def set_interval(self, interval):
        """
        更新点击间隔

        参数:
            interval (int): 新的点击间隔，单位为毫秒
        """
        self.interval = interval / 1000.0
