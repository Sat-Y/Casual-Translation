from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint
import pyperclip
import os

class TranslationBubble(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_timer()
    
    def init_ui(self):
        """初始化气泡UI"""
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置固定大小
        self.setFixedSize(300, 150)
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 翻译结果标签
        self.result_label = QLabel()
        self.result_label.setFont(QFont("Arial", 14))  # 增大字体大小
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.result_label)
        
        # 底部布局（包含复制按钮）
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        # 复制按钮
        self.copy_button = QPushButton()
        self.copy_button.setFixedSize(28, 28)
        # 使用更加美观的图标
        self.copy_button.setText("📋")
        self.copy_button.setToolTip("复制翻译结果")
        self.copy_button.clicked.connect(self.copy_result)
        bottom_layout.addWidget(self.copy_button)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                line-height: 1.4;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 4px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.2);
            }
        """)
        
        # 添加阴影效果（使用PyQt5支持的方式）
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    
    def init_timer(self):
        """初始化自动消失定时器"""
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
    
    def show_translation(self, text, position):
        """显示翻译结果"""
        self.result_label.setText(text)
        # 设置位置（在宠物旁边）
        self.move(position)
        self.show()
        # 启动自动消失定时器（8秒）
        self.hide_timer.start(8000)
    
    def copy_result(self):
        """复制翻译结果到剪贴板"""
        text = self.result_label.text()
        if text:
            pyperclip.copy(text)
            # 复制后加快消失速度
            self.hide_timer.start(2000)
            # 通知主窗口，暂时禁用剪贴板监控
            if hasattr(self, 'parent') and self.parent():
                self.parent().disable_clipboard_monitor_temp()
    
    def hide(self):
        """隐藏气泡"""
        super().hide()
        self.hide_timer.stop()
    
    def set_position_relative_to(self, widget):
        """相对于指定控件设置位置"""
        if widget:
            # 获取控件的位置和大小
            widget_rect = widget.frameGeometry()
            widget_pos = widget.mapToGlobal(QPoint(0, 0))
            
            # 计算气泡位置（在控件右侧）
            bubble_pos = QPoint(
                widget_pos.x() + widget_rect.width() + 10,
                widget_pos.y() + (widget_rect.height() - self.height()) // 2
            )
            
            self.move(bubble_pos)
