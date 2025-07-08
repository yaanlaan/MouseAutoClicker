
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence

class HotkeyDialog(QDialog):
    def __init__(self, current_hotkey=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置热键")
        self.setMinimumWidth(300)
        self.setMinimumHeight(150)

        self.current_hotkey = current_hotkey
        self.new_hotkey = None
        self.is_listening = False

        self.setup_ui()

    def setup_ui(self):
        """设置对话框UI"""
        layout = QVBoxLayout()

        # 指令标签
        instruction = QLabel("请按下您想要设置的热键组合。支持单个按键、组合键和鼠标侧键。")
        instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction)

        # 当前热键显示
        current_layout = QHBoxLayout()
        current_layout.addWidget(QLabel("当前热键:"))

        self.current_label = QLabel(self.current_hotkey_text())
        current_layout.addWidget(self.current_label)

        layout.addLayout(current_layout)

        # 新热键显示
        new_layout = QHBoxLayout()
        new_layout.addWidget(QLabel("新热键:"))

        self.new_label = QLabel("等待输入...")
        new_layout.addWidget(self.new_label)

        layout.addLayout(new_layout)

        # 监听按钮
        self.listen_button = QPushButton("开始监听")
        self.listen_button.clicked.connect(self.toggle_listening)
        layout.addWidget(self.listen_button)

        # 底部按钮
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        self.ok_button = QPushButton("确定")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def toggle_listening(self):
        """切换热键监听状态"""
        self.is_listening = not self.is_listening

        if self.is_listening:
            self.listen_button.setText("停止监听")
            self.new_label.setText("请按下热键...")
            self.grabKeyboard()  # 捕获键盘输入
        else:
            self.listen_button.setText("开始监听")
            self.releaseKeyboard()

    def keyPressEvent(self, event):
        """键盘按下事件处理"""
        if not self.is_listening:
            super().keyPressEvent(event)
            return

        # 忽略单独的修饰键
        if event.key() in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta):
            return

        # 获取修饰键
        modifiers = event.modifiers()

        # 构建热键字符串
        sequence = ""

        if modifiers & Qt.ControlModifier:
            sequence += "Ctrl+"
        if modifiers & Qt.ShiftModifier:
            sequence += "Shift+"
        if modifiers & Qt.AltModifier:
            sequence += "Alt+"
        if modifiers & Qt.MetaModifier:
            sequence += "Meta+"

        # 添加主键
        key_text = QKeySequence(event.key()).toString()
        sequence += key_text

        # 更新UI
        self.new_hotkey = sequence
        self.new_label.setText(sequence)
        self.ok_button.setEnabled(True)

        # 自动停止监听
        self.toggle_listening()

    def current_hotkey_text(self):
        """获取当前热键的显示文本"""
        if not self.current_hotkey:
            return "无"
        return self.current_hotkey

    def get_hotkey(self):
        """获取新设置的热键"""
        return self.new_hotkey
