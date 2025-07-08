import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QSpinBox, QComboBox,
                            QSystemTrayIcon, QMenu, QAction, QGroupBox, 
                            QRadioButton, QMessageBox, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt5.QtGui import QIcon, QKeySequence, QCursor

from core.auto_clicker import AutoClickerThread
from core.hotkey_manager import HotkeyManager
from core.language_manager import LanguageManager
from utils.constants import DEFAULT_INTERVAL, MIN_INTERVAL, MAX_INTERVAL, LANGUAGES
from utils.path_helper import resource_path

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()

        # 初始化配置管理器
        self.config_manager = config_manager

        # 初始化语言管理器
        self.language_manager = LanguageManager(self.config_manager.get_language())

        # 初始化变量
        self.auto_clicker_thread = None
        self.is_clicking = False
        self.click_interval = self.config_manager.get_click_interval()

        # 初始化热键管理器
        self.hotkey_manager = HotkeyManager(self.config_manager.get_hotkey())
        self.hotkey_manager.hotkey_pressed.connect(self.toggle_clicking)

        # 设置UI
        self.setup_ui()

        # 初始化系统托盘和任务栏图标
        self.setup_system_tray()
        self.setWindowIcon(QIcon(resource_path("resources/icon.png")))

    def setup_ui(self):
        """设置用户界面"""
        # 设置窗口属性
        self.setWindowTitle(self.language_manager.get_text("app_title"))
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon(resource_path("resources/icon.png")))

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 状态指示器
        status_layout = QHBoxLayout()
        self.status_label = QLabel(self.language_manager.get_text("status_inactive"))
        status_layout.addWidget(QLabel(self.language_manager.get_text("status_label")))
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        main_layout.addLayout(status_layout)

        # 点击间隔设置
        interval_group = QGroupBox(self.language_manager.get_text("interval_group"))
        interval_layout = QHBoxLayout()

        interval_layout.addWidget(QLabel(self.language_manager.get_text("interval_label")))

        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(MIN_INTERVAL)
        self.interval_spinbox.setMaximum(MAX_INTERVAL)
        self.interval_spinbox.setValue(self.click_interval)
        self.interval_spinbox.valueChanged.connect(self.update_interval)
        interval_layout.addWidget(self.interval_spinbox)

        interval_layout.addWidget(QLabel(self.language_manager.get_text("ms_label")))
        interval_layout.addStretch()

        interval_group.setLayout(interval_layout)
        main_layout.addWidget(interval_group)

        # 热键设置
        hotkey_group = QGroupBox(self.language_manager.get_text("hotkey_group"))
        hotkey_layout = QVBoxLayout()

        hotkey_info = QLabel(self.language_manager.get_text("hotkey_info"))
        hotkey_info.setWordWrap(True)
        hotkey_layout.addWidget(hotkey_info)

        self.current_hotkey_label = QLabel(f"{self.language_manager.get_text('current_hotkey')}: {self.hotkey_manager.get_current_hotkey_text()}")
        hotkey_layout.addWidget(self.current_hotkey_label)

        change_hotkey_button = QPushButton(self.language_manager.get_text("change_hotkey_button"))
        change_hotkey_button.clicked.connect(self.change_hotkey)
        hotkey_layout.addWidget(change_hotkey_button)

        hotkey_group.setLayout(hotkey_layout)
        main_layout.addWidget(hotkey_group)

        # 语言选择
        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel(self.language_manager.get_text("language_label")))

        self.language_combo = QComboBox()
        for lang_code, lang_name in LANGUAGES.items():
            self.language_combo.addItem(lang_name, lang_code)

        # 设置当前语言
        current_index = list(LANGUAGES.keys()).index(self.config_manager.get_language())
        self.language_combo.setCurrentIndex(current_index)

        self.language_combo.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()
        main_layout.addLayout(language_layout)

        # 控制按钮
        button_layout = QHBoxLayout()

        self.start_stop_button = QPushButton(self.language_manager.get_text("start_button"))
        self.start_stop_button.clicked.connect(self.toggle_clicking)
        button_layout.addWidget(self.start_stop_button)
        
        exit_button = QPushButton(self.language_manager.get_text("exit"))
        exit_button.clicked.connect(self.close_application)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        # 底部信息
        info_label = QLabel(self.language_manager.get_text("tray_info"))
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)

    def setup_system_tray(self):
        """设置系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(resource_path("resources/icon_inactive.png")))

        # 创建托盘菜单
        self.tray_menu = QMenu()

        # 状态信息（不可点击的标签）
        self.tray_info_interval = QAction(f"点击间隔: {self.click_interval}ms")
        self.tray_info_interval.setEnabled(False)
        self.tray_menu.addAction(self.tray_info_interval)
        
        self.tray_info_language = QAction(f"语言模式: {LANGUAGES[self.config_manager.get_language()]}")
        self.tray_info_language.setEnabled(False)
        self.tray_menu.addAction(self.tray_info_language)
        
        self.tray_menu.addSeparator()

        # 功能按钮
        self.tray_action_toggle = QAction(self.language_manager.get_text("start_button"))
        self.tray_action_toggle.triggered.connect(self.toggle_clicking)
        self.tray_menu.addAction(self.tray_action_toggle)

        self.tray_action_show = QAction(self.language_manager.get_text("show_window"))
        self.tray_action_show.triggered.connect(self.show_and_activate)
        self.tray_menu.addAction(self.tray_action_show)
        
        self.tray_action_restart = QAction(self.language_manager.get_text("restart"))
        self.tray_action_restart.triggered.connect(self.restart_application)
        self.tray_menu.addAction(self.tray_action_restart)

        self.tray_menu.addSeparator()

        self.tray_action_exit = QAction(self.language_manager.get_text("exit"))
        self.tray_action_exit.triggered.connect(self.close_application)
        self.tray_menu.addAction(self.tray_action_exit)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """系统托盘图标被激活（如点击）时的响应"""
        if reason == QSystemTrayIcon.Trigger or reason == QSystemTrayIcon.DoubleClick:
            self.show_and_activate()
        elif reason == QSystemTrayIcon.Context:
            # 更新托盘菜单中的状态信息
            self.update_tray_menu_info()
            # 处理右键点击，显示上下文菜单
            self.tray_icon.contextMenu().popup(QCursor.pos())
            
    def show_and_activate(self):
        """显示并激活窗口"""
        # 确保窗口在任务栏中可见
        self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()  # 确保窗口获得焦点
        
    def update_tray_menu_info(self):
        """更新托盘菜单中的状态信息"""
        # 更新点击间隔信息
        self.tray_info_interval.setText(f"点击间隔: {self.click_interval}ms")
        # 更新语言模式信息
        self.tray_info_language.setText(f"语言模式: {LANGUAGES[self.config_manager.get_language()]}")
        # 更新菜单项的文本
        self.tray_action_show.setText(self.language_manager.get_text("show_window"))
        self.tray_action_restart.setText(self.language_manager.get_text("restart"))
        self.tray_action_exit.setText(self.language_manager.get_text("exit"))
    def toggle_clicking(self):
        """切换自动点击状态"""
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        """开始自动点击"""
        if not self.is_clicking:
            # 更新状态
            self.is_clicking = True

            # 更新UI
            self.status_label.setText(self.language_manager.get_text("status_active"))
            self.start_stop_button.setText(self.language_manager.get_text("stop_button"))
            self.tray_action_toggle.setText(self.language_manager.get_text("stop_button"))
            self.tray_icon.setIcon(QIcon(resource_path("resources/icon_active.png")))

            # 创建并启动自动点击线程
            self.auto_clicker_thread = AutoClickerThread(self.click_interval)
            self.auto_clicker_thread.start()

    def stop_clicking(self):
        """停止自动点击"""
        if self.is_clicking:
            # 更新状态
            self.is_clicking = False

            # 更新UI
            self.status_label.setText(self.language_manager.get_text("status_inactive"))
            self.start_stop_button.setText(self.language_manager.get_text("start_button"))
            self.tray_action_toggle.setText(self.language_manager.get_text("start_button"))
            self.tray_icon.setIcon(QIcon(resource_path("resources/icon_inactive.png")))

            # 停止自动点击线程
            if self.auto_clicker_thread:
                self.auto_clicker_thread.stop()
                self.auto_clicker_thread = None

    def update_interval(self, value):
        """更新点击间隔"""
        self.click_interval = value
        self.config_manager.set_click_interval(value)
        # 立即保存配置到磁盘，确保点击间隔设置被记住
        self.config_manager.save_config()

        # 如果正在点击，更新线程的点击间隔
        if self.is_clicking and self.auto_clicker_thread:
            self.auto_clicker_thread.set_interval(value)
            
        # 更新托盘菜单中的间隔信息
        self.update_tray_menu_info()

    def change_language(self, index):
        """更改界面语言"""
        language_code = self.language_combo.itemData(index)
        self.config_manager.set_language(language_code)
        # 立即保存配置到磁盘，确保语言设置被记住
        self.config_manager.save_config()
        
        # 更新托盘菜单中的语言信息
        self.update_tray_menu_info()

        # 显示需要重启应用程序的提示
        QMessageBox.information(
            self,
            self.language_manager.get_text("language_changed_title"),
            self.language_manager.get_text("language_changed_message")
        )

    def change_hotkey(self):
        """更改热键"""
        # 显示热键设置对话框（简化版，实际应用中可能需要更复杂的对话框）
        from ui.hotkey_dialog import HotkeyDialog
        dialog = HotkeyDialog(self.hotkey_manager.get_current_hotkey(), self)
        if dialog.exec_():
            new_hotkey = dialog.get_hotkey()
            if new_hotkey:
                # 更新热键
                self.hotkey_manager.set_hotkey(new_hotkey)
                self.current_hotkey_label.setText(f"{self.language_manager.get_text('current_hotkey')}: {self.hotkey_manager.get_current_hotkey_text()}")
                self.config_manager.set_hotkey(new_hotkey)
                # 立即保存配置到磁盘，确保热键设置被记住
                self.config_manager.save_config()

    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 最小化到系统托盘而不是关闭
        if not self.config_manager.get_exit_on_close():
            event.ignore()
            # 确保任务栏图标仍然可见
            self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
            self.hide()
            # 可选：显示气泡提示
            self.tray_icon.showMessage(
                self.language_manager.get_text("app_title"),
                self.language_manager.get_text("minimized_to_tray"),
                QSystemTrayIcon.Information,
                3000
            )
        else:
            self.close_application()

    def close_application(self):
        """完全关闭应用程序"""
        # 停止自动点击
        if self.is_clicking:
            self.stop_clicking()

        # 移除热键监听器
        self.hotkey_manager.unregister_hotkey()

        # 保存配置
        self.config_manager.save_config()

        # 确保托盘图标被移除
        self.tray_icon.setVisible(False)
        self.tray_icon.deleteLater()

        # 退出应用程序
        QApplication.quit()
        sys.exit()
        sys.exit()
        
    def restart_application(self):
        """重新启动应用程序"""
        # 保存当前的配置
        self.config_manager.save_config()
        
        # 停止点击（如果正在进行）
        if self.is_clicking:
            self.stop_clicking()
            
        # 移除热键监听器
        self.hotkey_manager.unregister_hotkey()
        
        # 移除托盘图标
        self.tray_icon.setVisible(False)
        self.tray_icon.deleteLater()
        
        # 使用 os.execl 重启应用程序
        os.execl(sys.executable, sys.executable, *sys.argv)