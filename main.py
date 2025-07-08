import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from utils.path_helper import resource_path
from utils.singleton import SingleInstanceManager

from ui.main_window import MainWindow
from core.config_manager import ConfigManager

def main():
    # 检查程序是否已在运行
    instance_manager = SingleInstanceManager()
    if not instance_manager.try_acquire_lock():
        # 如果已经有一个实例在运行，显示消息并退出
        app = QApplication(sys.argv)
        instance_manager.show_already_running_message()
        sys.exit(0)
        
    # 初始化配置
    config_manager = ConfigManager()

    # 创建应用程序
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("resources/icon.png")))

    # 创建并显示主窗口
    window = MainWindow(config_manager)
    window.show()

    # 程序退出时释放锁
    result = app.exec_()
    instance_manager.release_lock()
    sys.exit(result)

if __name__ == "__main__":
    main()