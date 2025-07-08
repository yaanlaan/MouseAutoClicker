
# 点击间隔设置
DEFAULT_INTERVAL = 1000  # 默认间隔：1000毫秒（1秒）
MIN_INTERVAL = 50       # 最小间隔：50毫秒
MAX_INTERVAL = 60000    # 最大间隔：60000毫秒（60秒）

# 热键设置
DEFAULT_HOTKEY = "F6"   # 默认热键

# 语言设置
DEFAULT_LANGUAGE = "zh_CN"  # 默认语言：中文

# 支持的语言
LANGUAGES = {
    "zh_CN": "中文",
    "en_US": "English"
}

# 翻译字典
TRANSLATIONS = {
    "zh_CN": {
        # 应用程序相关
        "app_title": "鼠标自动点击器",

        # 状态相关
        "status_label": "状态:",
        "status_active": "活跃 - 正在点击",
        "status_inactive": "非活跃 - 已停止",

        # 间隔设置相关
        "interval_group": "点击间隔设置",
        "interval_label": "间隔:",
        "ms_label": "毫秒",

        # 热键相关
        "hotkey_group": "热键设置",
        "hotkey_info": "您可以使用热键来切换自动点击的开启/关闭状态，即使在应用程序最小化时也能生效。",
        "current_hotkey": "当前热键",
        "change_hotkey_button": "更改热键",

        # 语言相关
        "language_label": "界面语言:",
        "language_changed_title": "语言已更改",
        "language_changed_message": "语言设置已更改，重启应用程序后生效。",

        # 按钮相关
        "start_button": "开始点击",
        "stop_button": "停止点击",

        # 系统托盘相关
        "tray_info": "应用程序将在最小化时继续在系统托盘运行",
        "show_window": "显示主窗口",
        "minimized_to_tray": "自动点击器已最小化到系统托盘",
        "restart": "重新启动",
        "exit": "退出"
    },
    "en_US": {
        # 应用程序相关
        "app_title": "Mouse Auto Clicker",

        # 状态相关
        "status_label": "Status:",
        "status_active": "Active - Clicking",
        "status_inactive": "Inactive - Stopped",

        # 间隔设置相关
        "interval_group": "Click Interval Settings",
        "interval_label": "Interval:",
        "ms_label": "ms",

        # 热键相关
        "hotkey_group": "Hotkey Settings",
        "hotkey_info": "You can use a hotkey to toggle auto-clicking on/off, even when the application is minimized.",
        "current_hotkey": "Current Hotkey",
        "change_hotkey_button": "Change Hotkey",

        # 语言相关
        "language_label": "Interface Language:",
        "language_changed_title": "Language Changed",
        "language_changed_message": "Language setting has been changed. It will take effect after restarting the application.",

        # 按钮相关
        "start_button": "Start Clicking",
        "stop_button": "Stop Clicking",

        # 系统托盘相关
        "tray_info": "The application will continue running in the system tray when minimized",
        "show_window": "Show Main Window",
        "minimized_to_tray": "Auto Clicker has been minimized to the system tray",
        "restart": "Restart",
        "exit": "Exit"
    }
}