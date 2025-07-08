import socket
import sys
import os
import tempfile
from PyQt5.QtWidgets import QMessageBox

class SingleInstanceManager:
    """
    确保应用程序只能运行一个实例
    使用套接字绑定和锁文件双重机制来确保唯一性
    """

    def __init__(self, unique_id="MouseAutoClicker"):
        """
        初始化单例管理器

        Args:
            unique_id (str): 用于区分不同应用的唯一标识符
        """
        self.unique_id = unique_id
        self.socket = None
        self.port = 38643  # 使用一个不太常用的端口
        self.lock_file_path = os.path.join(tempfile.gettempdir(), f"{unique_id}.lock")
        self.lock_file = None

    def try_acquire_lock(self):
        """
        尝试获取锁，如果另一个实例已在运行，则返回False

        Returns:
            bool: 如果成功获取锁（即没有其他实例运行）则返回True，否则返回False
        """
        try:
            # 方法1: 套接字绑定
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 尝试绑定套接字
            try:
                self.socket.bind(('127.0.0.1', self.port))
                self.socket.listen(1)  # 开始监听，使绑定更加稳定
            except socket.error:
                # 如果绑定失败，说明端口已被占用
                self.socket.close()
                self.socket = None
                return False
            
            # 方法2: 文件锁定
            try:
                # 尝试创建或打开锁文件
                if not os.path.exists(self.lock_file_path):
                    # 如果文件不存在，则创建新文件
                    self.lock_file = open(self.lock_file_path, 'w')
                    self.lock_file.write(f"PID: {os.getpid()}\nStarted: {self.get_current_time()}")
                    self.lock_file.flush()
                else:
                    # 如果文件已存在，尝试打开它
                    self.lock_file = open(self.lock_file_path, 'w')
                
                # 尝试锁定文件
                try:
                    import msvcrt
                    msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                except (ImportError, IOError):
                    # 如果锁定失败，关闭文件并返回False
                    if self.lock_file:
                        self.lock_file.close()
                        self.lock_file = None
                    # 关闭之前创建的套接字
                    if self.socket:
                        self.socket.close()
                        self.socket = None
                    return False
            except IOError:
                # 无法操作文件，可能是权限问题
                if self.socket:
                    self.socket.close()
                    self.socket = None
                return False
                    
            # 成功获取锁
            return True
            
        except Exception as e:
            print(f"单例检查出错: {e}")
            # 确保资源被释放
            self.release_lock()
            return False
            
    def get_current_time(self):
        """获取当前时间的字符串表示，用于记录到锁文件
        
        Returns:
            str: 当前时间的字符串表示
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_already_running_message(self):
        """显示程序已在运行的消息框"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("MouseAutoClicker 已在运行")
        msg.setText("MouseAutoClicker 的另一个实例已经在运行中。")
        msg.setInformativeText("请使用已运行的实例，或关闭它后再启动新的实例。")
        msg.exec_()

    def release_lock(self):
        """释放所有锁资源"""
        # 关闭套接字
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        # 释放文件锁并删除锁文件
        if self.lock_file:
            try:
                # 在Windows上解锁文件
                try:
                    import msvcrt
                    msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                except (ImportError, IOError):
                    pass
                
                self.lock_file.close()
                if os.path.exists(self.lock_file_path):
                    os.remove(self.lock_file_path)
            except:
                pass
