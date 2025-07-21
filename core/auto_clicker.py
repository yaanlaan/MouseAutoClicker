
import time
import random
from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Button, Controller

class AutoClickerThread(QThread):
    """自动点击线程，负责在后台执行连续点击操作"""

    
    def __init__(self, interval, jitter_enabled=False, jitter_percent=20):
        """
        初始化自动点击线程

        参数:
            interval (int): 点击间隔，单位为毫秒
            jitter_enabled (bool): 是否启用随机抖动
            jitter_percent (int): 随机抖动幅度百分比
        """
        super().__init__()
        self.mouse = Controller()
        self.interval = interval / 1000.0  # 转换为秒
        self.jitter_enabled = jitter_enabled
        self.jitter_percent = jitter_percent
        self.running = False

    def run(self):
        """线程主函数，执行连续点击"""
        self.running = True
        click_count = 0

        while self.running:
            # 执行鼠标点击
            self.mouse.click(Button.left)
            click_count += 1
            
            # 计算等待时间（考虑随机抖动）
            wait_time = self.calculate_wait_time()
            
            
            # 等待指定的间隔时间
            time.sleep(wait_time)
            
    def calculate_wait_time(self):
        """计算实际等待时间，考虑随机抖动"""
        if not self.jitter_enabled:
            return self.interval
            
        # 计算抖动范围
        jitter_range = self.interval * (self.jitter_percent / 100.0)
        
        # 在基础间隔的基础上添加随机抖动（可正可负）
        jitter = random.uniform(-jitter_range, jitter_range)
        
        # 确保最终间隔不小于0.01秒
        return max(0.01, self.interval + jitter)

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
        
    def set_jitter_enabled(self, enabled):
        """
        启用或禁用随机抖动
        
        参数:
            enabled (bool): 是否启用随机抖动
        """
        self.jitter_enabled = enabled
        
    def set_jitter_percent(self, percent):
        """
        设置随机抖动幅度
        
        参数:
            percent (int): 随机抖动幅度百分比
        """
        self.jitter_percent = percent
