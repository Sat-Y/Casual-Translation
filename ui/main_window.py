from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QApplication
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint
import pyperclip
import os
from utils.history import HistoryManager
from utils.resource_manager import ResourceManager
from utils.config_manager import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.history_manager = HistoryManager()
        self.resource_manager = ResourceManager()
        self.config_manager = ConfigManager()
        # 添加缩放因子
        self.scale_factor = 1.0
        self.min_scale = 0.2  # 更小的最小缩放比例
        self.max_scale = 2.0
        # 剪贴板监控控制
        self.clipboard_monitor_enabled = True
        self.last_translated_content = ""
        # 模式控制
        self.current_mode = self.config_manager.get_current_mode()  # 从配置加载当前模式
        # 初始化UI和其他组件
        self.init_ui()
        self.init_animation()
        self.init_drag()
        self.init_bubble()
        self.init_status_sign()
        # 无论当前模式是什么，都保持剪贴板监控开启
        # 这样在休息模式下也能读取剪贴板进行聊天
        self.clipboard_monitor_enabled = True
        print(f"初始化完成，当前模式: {self.current_mode}，剪贴板监控: {self.clipboard_monitor_enabled}")
    
    def init_animation(self):
        """初始化动画相关变量和定时器"""
        self.current_frame = 0
        self.current_state = "idle"  # idle 或 translation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(400)  # 300ms per frame，动画速度变慢
    
    def init_drag(self):
        """初始化拖动相关变量"""
        self.dragging = False
        self.drag_start_position = QPoint()
    
    def init_bubble(self):
        """初始化气泡组件"""
        from ui.bubble import TranslationBubble
        self.bubble = TranslationBubble(self)
        self.bubble.hide()



    def init_status_sign(self):
        """初始化状态牌子"""
        # 创建状态牌子
        self.status_sign = QLabel()
        self.status_sign.setFixedSize(100, 50)
        self.status_sign.setAlignment(Qt.AlignCenter)
        self.status_sign.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid black;
                border-radius: 8px;
                color: black;
                font-family: 'Comic Sans MS', cursive;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        # 初始化位置平滑过渡（必须在update_status_sign之前调用）
        self.init_smooth_positioning()
        # 加载状态图片
        self.load_status_images()
        # 设置初始图片
        self.update_status_sign()
        # 添加点击事件
        self.status_sign.mousePressEvent = self.on_sign_clicked
        # 将牌子添加到窗口中
        self.status_sign.setParent(self)
        # 初始化牌子动画
        self.init_sign_animation()
    
    def load_status_images(self):
        """加载状态图片"""
        # 从 resources/brand 目录加载图片
        self.rest_image = None
        self.translate_image = None
        # 尝试加载图片
        import sys
        # 获取资源文件的正确路径（支持开发环境和打包环境）
        if hasattr(sys, '_MEIPASS'):
            # 打包环境
            base_path = sys._MEIPASS
        else:
            # 开发环境
            base_path = os.path.abspath('.')
        
        rest_image_path = os.path.join(base_path, "resources", "brand", "rest.png")
        translate_image_path = os.path.join(base_path, "resources", "brand", "work.png")
        
        if os.path.exists(rest_image_path):
            self.rest_image = QPixmap(rest_image_path)
        if os.path.exists(translate_image_path):
            self.translate_image = QPixmap(translate_image_path)
        print(f"加载状态图片: rest={os.path.exists(rest_image_path)}, translate={os.path.exists(translate_image_path)}")
        print(f"资源基础路径: {base_path}")

    def init_sign_animation(self):
        """初始化牌子动画"""
        # 轻微摇晃动画，减弱晃动效果
        self.sign_animation_timer = QTimer(self)
        self.sign_animation_timer.timeout.connect(self.update_sign_animation)
        self.sign_animation_timer.start(150)  # 减慢动画速度
        self.sign_offset = 0
        self.sign_offset_direction = 1
    
    def init_smooth_positioning(self):
        """初始化平滑定位相关变量"""
        # 目标位置
        self.target_sign_pos = None
        # 当前位置
        self.current_sign_pos = None
        # 平滑过渡定时器
        self.smooth_move_timer = QTimer(self)
        self.smooth_move_timer.timeout.connect(self.update_smooth_position)
        self.smooth_move_timer.setInterval(16)  # 约60fps
        # 平滑过渡速度（0-1，值越大速度越快）
        self.smooth_move_speed = 0.15
    
    def init_ui(self):
        """初始化无边框半透明窗口和宠物图像显示"""
        # 设置窗口属性
        self.setWindowTitle("Casual Translation")
        
        # 无边框窗口，设置为最顶层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # 半透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 宠物图像显示
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pet_label)
        
        central_widget.setLayout(layout)
        
        # 添加设置按钮
        self.settings_button = QPushButton()
        self.settings_button.setFixedSize(32, 32)
        self.settings_button.setText("⚙️")
        self.settings_button.setToolTip("设置")
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 24px;
                border: 1px solid #E0E0E0;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 1.0);
                border: 1px solid #CCCCCC;
            }
        """)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        # 将设置按钮添加到窗口中
        self.settings_button.setParent(self)
        

        
        # 确保状态牌子已初始化
        if not hasattr(self, 'status_sign'):
            self.init_status_sign()
        
        # 获取屏幕尺寸
        screen = QApplication.desktop().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # 检查是否有动画帧，如果有，设置初始大小
        idle_frames = self.resource_manager.get_idle_frames()
        if idle_frames:
            # 使用第一个idle帧作为初始图像
            initial_pixmap = idle_frames[0]
            
            # 以最小的样子启动，使用最小缩放因子
            scale_factor = self.min_scale  # 使用最小缩放因子
            # 确保使用最小缩放因子
            self.scale_factor = scale_factor
            
            # 应用缩放因子
            scaled_width = int(initial_pixmap.width() * scale_factor)
            scaled_height = int(initial_pixmap.height() * scale_factor)
            scaled_pixmap = initial_pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.pet_label.setPixmap(scaled_pixmap)
            # 设置窗口大小
            self.resize(scaled_pixmap.width(), scaled_pixmap.height())
        else:
            # 如果没有动画帧，设置默认大小
            self.resize(200, 200)
        
        # 设置窗口位置在屏幕中央偏上，确保在屏幕可见区域内
        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 3
        # 确保y坐标不为负数
        y = max(y, 20)  # 至少在屏幕上方20像素
        self.move(x, y)
        
        # 调整设置按钮的位置（在桌宠右上角）
        self.update_settings_button_position()
        # 调整状态牌子的位置（在桌宠正右边）
        self.update_status_sign_position()
        
        # 确保窗口显示
        self.show()
        self.raise_()
        self.activateWindow()
        # 再次更新状态牌子位置，确保在窗口显示后位置正确
        self.update_status_sign_position()
        # 确保状态牌子显示在最顶层
        if hasattr(self, 'status_sign'):
            self.status_sign.show()
            self.status_sign.raise_()
        print(f"桌宠窗口已显示，位置: ({self.x()}, {self.y()})，大小: {self.size()}")
        if hasattr(self, 'status_sign'):
            print(f"状态牌子位置: ({self.status_sign.x()}, {self.status_sign.y()})，大小: {self.status_sign.size()}")
    
    def update_settings_button_position(self):
        """更新设置按钮的位置，使其位于桌宠右上角"""
        if hasattr(self, 'settings_button'):
            # 设置按钮位于桌宠右上角，稍微向外偏移一点
            button_x = self.width() - self.settings_button.width() - 5
            button_y = -5
            self.settings_button.move(button_x, button_y)
            # 确保按钮显示在最顶层
            self.settings_button.raise_()



    def update_status_sign_position(self):
        """更新状态牌子的位置，使其固定在桌宠脚旁边"""
        if hasattr(self, 'status_sign'):
            # 状态牌子应该作为独立的窗口显示，而不是作为桌宠窗口的子控件
            # 这样即使桌宠缩小，牌子也能正常显示
            if self.status_sign.parent() == self:
                # 移除父控件关系，使牌子成为独立窗口
                self.status_sign.setParent(None)
                # 设置牌子为顶层窗口
                self.status_sign.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
                # 设置半透明背景
                self.status_sign.setAttribute(Qt.WA_TranslucentBackground)
            
            # 使用窗口的全局位置来计算牌子位置
            window_global_pos = self.mapToGlobal(QPoint(0, 0))
            # 计算牌子的全局位置（固定在桌宠脚旁边，右下角位置）
            # 桌宠是坐着的，脚在下方，所以将牌子放在右下角，靠近脚的位置
            sign_global_x = window_global_pos.x() + self.width() + 10  # 右侧
            sign_global_y = window_global_pos.y() + self.height() - self.status_sign.height()  # 底部对齐
            
            # 确保牌子在屏幕可见范围内
            screen = QApplication.desktop().screenGeometry()
            max_x = screen.width() - self.status_sign.width() - 10
            max_y = screen.height() - self.status_sign.height() - 10
            sign_global_x = max(min(sign_global_x, max_x), 10)
            sign_global_y = max(min(sign_global_y, max_y), 10)
            
            # 设置目标位置，启动平滑过渡
            self.target_sign_pos = QPoint(sign_global_x, sign_global_y)
            # 如果当前位置未初始化，直接设置
            if self.current_sign_pos is None:
                self.current_sign_pos = self.target_sign_pos
                self.status_sign.move(self.current_sign_pos)
            # 启动平滑移动定时器
            if not self.smooth_move_timer.isActive():
                self.smooth_move_timer.start()
            
            # 确保牌子显示在最顶层
            self.status_sign.show()
            self.status_sign.raise_()
            # 只在位置实际变化时打印，减少日志输出
            if not hasattr(self, 'last_sign_pos') or self.last_sign_pos != self.target_sign_pos:
                print(f"更新牌子目标位置: 全局({sign_global_x}, {sign_global_y})")
                self.last_sign_pos = self.target_sign_pos

    def update_sign_animation(self):
        """更新牌子动画，实现轻微摇晃效果"""
        if hasattr(self, 'status_sign'):
            # 轻微摇晃动画（位置动画），减弱晃动幅度
            self.sign_offset += self.sign_offset_direction * 0.5
            if self.sign_offset >= 1.5 or self.sign_offset <= -1.5:
                self.sign_offset_direction *= -1
            # 应用位置偏移
            original_x = self.status_sign.x()
            original_y = self.status_sign.y()
            # 将浮点数转换为整数
            self.status_sign.move(int(original_x + self.sign_offset), int(original_y))
    
    def update_smooth_position(self):
        """更新平滑位置过渡"""
        if hasattr(self, 'status_sign') and self.current_sign_pos is not None and self.target_sign_pos is not None:
            # 计算当前位置和目标位置的差值
            dx = self.target_sign_pos.x() - self.current_sign_pos.x()
            dy = self.target_sign_pos.y() - self.current_sign_pos.y()
            
            # 计算距离
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            # 如果距离很小，直接设置到目标位置并停止定时器
            if distance < 1:
                self.current_sign_pos = self.target_sign_pos
                self.status_sign.move(self.current_sign_pos)
                self.smooth_move_timer.stop()
                return
            
            # 使用平滑过渡算法（缓动）
            new_x = self.current_sign_pos.x() + dx * self.smooth_move_speed
            new_y = self.current_sign_pos.y() + dy * self.smooth_move_speed
            
            # 更新当前位置
            self.current_sign_pos = QPoint(int(new_x), int(new_y))
            
            # 应用新位置
            self.status_sign.move(self.current_sign_pos)

    def on_sign_clicked(self, event):
        """牌子点击事件，实现翻转动画"""
        if hasattr(self, 'status_sign'):
            # 翻转动画
            self.toggle_mode()

    def open_settings_dialog(self):
        """打开设置对话框"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QGroupBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout()
        
        # 休息模式提示词设置
        rest_prompt_group = QGroupBox("休息模式提示词")
        rest_prompt_layout = QVBoxLayout()
        
        rest_label = QLabel("AI提示词:")
        rest_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.rest_prompt_text = QTextEdit()
        # 加载当前休息模式提示词
        current_rest_prompt = self.translator.load_rest_prompt()
        self.rest_prompt_text.setText(current_rest_prompt)
        self.rest_prompt_text.setPlaceholderText("请输入休息模式AI提示词，例如：You are a cute and friendly desktop pet...")
        
        save_rest_button = QPushButton("保存休息提示词")
        save_rest_button.clicked.connect(lambda: self.save_rest_prompt(dialog))
        
        rest_prompt_layout.addWidget(rest_label)
        rest_prompt_layout.addWidget(self.rest_prompt_text)
        rest_prompt_layout.addWidget(save_rest_button)
        rest_prompt_group.setLayout(rest_prompt_layout)
        
        # 程序控制
        control_group = QGroupBox("程序控制")
        control_layout = QVBoxLayout()
        
        exit_button = QPushButton("结束程序")
        exit_button.clicked.connect(self.exit_program)
        
        control_layout.addWidget(exit_button)
        control_group.setLayout(control_layout)
        
        # 添加所有组到主布局
        layout.addWidget(rest_prompt_group)
        layout.addWidget(control_group)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(dialog.reject)
        layout.addWidget(cancel_button)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def toggle_mode(self):
        """切换模式"""
        if self.current_mode == "rest":
            self.current_mode = "translate"
            # 开启剪贴板监控
            self.clipboard_monitor_enabled = True
            print("切换到翻译模式，开启剪贴板监控")
        else:
            self.current_mode = "rest"
            # 保持剪贴板监控开启，以便能够读取剪贴板进行聊天
            self.clipboard_monitor_enabled = True
            print("切换到休息模式，保持剪贴板监控开启")
        # 保存当前模式到配置
        self.config_manager.set_current_mode(self.current_mode)
        # 更新状态牌子
        self.update_status_sign()
        # 播放翻转动画
        self.play_sign_flip_animation()

    def update_status_sign(self):
        """更新状态牌子的显示"""
        if hasattr(self, 'status_sign'):
            # 计算牌子大小为桌宠的1/2（放大一倍）
            sign_width = max(int(self.width() * 0.5), 120)  # 最小120像素
            sign_height = max(int(self.height() * 0.5), 80)  # 最小80像素
            self.status_sign.setFixedSize(sign_width, sign_height)
            
            if self.current_mode == "rest":
                if self.rest_image:
                    # 使用休息中图片，缩放到牌子大小
                    scaled_image = self.rest_image.scaled(sign_width, sign_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.status_sign.setPixmap(scaled_image)
                    self.status_sign.setText("")
                else:
                    # 没有图片时使用文字
                    self.status_sign.setText("休息中")
            else:
                if self.translate_image:
                    # 使用翻译中图片，缩放到牌子大小
                    scaled_image = self.translate_image.scaled(sign_width, sign_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.status_sign.setPixmap(scaled_image)
                    self.status_sign.setText("")
                else:
                    # 没有图片时使用文字
                    self.status_sign.setText("翻译中")
            # 确保牌子显示
            self.status_sign.show()
            self.status_sign.raise_()
            # 更新牌子位置
            self.update_status_sign_position()

    def play_sign_flip_animation(self):
        """播放牌子翻转动画"""
        if hasattr(self, 'status_sign'):
            # 简单的位置动画作为翻转动画的替代
            original_x = self.status_sign.x()
            original_y = self.status_sign.y()
            # 左右移动模拟翻转动画
            for offset in range(0, 20, 2):
                self.status_sign.move(original_x + offset, original_y)
                QApplication.processEvents()
                QTimer.singleShot(10, lambda: None)
            for offset in range(20, -20, -2):
                self.status_sign.move(original_x + offset, original_y)
                QApplication.processEvents()
                QTimer.singleShot(10, lambda: None)
            for offset in range(-20, 0, 2):
                self.status_sign.move(original_x + offset, original_y)
                QApplication.processEvents()
                QTimer.singleShot(10, lambda: None)
            # 恢复原始位置
            self.status_sign.move(original_x, original_y)
            # 动画完成后再次更新状态文字，确保显示正确
            self.update_status_sign()
            # 确保牌子显示在最顶层
            self.status_sign.show()
            self.status_sign.raise_()

    def open_settings(self):
        """打开设置提示词的对话框"""
        # 这个方法现在被 open_settings_dialog 方法替代
        self.open_settings_dialog()
    
    def save_prompt(self, dialog):
        """保存翻译提示词"""
        prompt = self.translate_prompt_text.toPlainText().strip()
        if prompt:
            success = self.translator.save_system_prompt(prompt)
            if success:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "成功", "提示词保存成功！")
                dialog.accept()
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "错误", "提示词保存失败，请检查权限。")
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "提示词不能为空！")

    def save_rest_prompt(self, dialog):
        """保存休息模式提示词"""
        prompt = self.rest_prompt_text.toPlainText().strip()
        if prompt:
            # 保存到翻译器
            success1 = self.translator.save_rest_prompt(prompt)
            # 保存到配置
            success2 = self.config_manager.set_rest_prompt(prompt)
            if success1 and success2:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "成功", "休息模式提示词保存成功！")
                dialog.accept()
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "错误", "提示词保存失败，请检查权限。")
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "提示词不能为空！")
    
    def init_tray(self):
        """移除系统托盘功能，用户希望关闭窗口时直接退出程序"""
        # 不再创建系统托盘图标
        print("系统托盘功能已移除，关闭窗口时程序会直接退出")
        # 不显示托盘图标
        # self.tray_icon = QSystemTrayIcon(self)
        # self.tray_icon.hide()
    
    def translate(self, text):
        """翻译文本并在气泡中显示结果"""
        print(f"开始翻译: {text}")
        if text:
            # 设置为翻译状态，切换动画
            self.set_state("translation")
            # 检测文本类型并确定翻译方向
            if self.is_chinese_text(text):
                # 中文转英文
                print("检测到中文文本，翻译成英文")
                translation = self.translator.translate(text, src='zh-CN', dest='en')
            else:
                # 英文转中文
                print("检测到英文文本，翻译成中文")
                translation = self.translator.translate(text, src='en', dest='zh-CN')
            print(f"翻译结果: {translation}")
            # 记录翻译结果，用于防止循环翻译
            self.last_translated_content = translation
            # 添加到历史记录
            self.history_manager.add_record(text, translation)
            # 显示翻译结果在气泡中
            if hasattr(self, 'bubble'):
                print("显示翻译结果在气泡中")
                # 计算气泡位置（在宠物右侧）
                bubble_pos = self.mapToGlobal(QPoint(self.width() + 10, (self.height() - 150) // 2))
                print(f"气泡位置: {bubble_pos}")
                self.bubble.show_translation(translation, bubble_pos)
            else:
                print("气泡不存在")
            # 翻译完成后恢复idle状态
            # 延迟恢复，让用户看到翻译动画
            QTimer.singleShot(2000, lambda: self.set_state("idle"))
        print("翻译完成")

    def chat(self, text):
        """聊天功能，在休息模式下使用"""
        if text:
            # 执行聊天
            response = self.translator.chat(text)
            # 显示聊天结果在气泡中
            if hasattr(self, 'bubble'):
                # 计算气泡位置（在宠物右侧）
                bubble_pos = self.mapToGlobal(QPoint(self.width() + 10, (self.height() - 150) // 2))
                self.bubble.show_translation(response, bubble_pos)
    
    def translate_selected_text(self):
        try:
            # 先尝试模拟Ctrl+C复制选中的文本
            import keyboard
            keyboard.press_and_release('ctrl+c')
            # 等待一小段时间确保复制完成
            import time
            time.sleep(0.1)
            # 然后从剪贴板获取文本
            text = pyperclip.paste().strip()
            if text:
                print(f"获取到选中的文本: {text}")
                self.translate(text)
                self.show()
                self.activateWindow()
            else:
                print("未获取到选中的文本")
        except Exception as e:
            print(f"翻译选中文本错误: {str(e)}")
    

    
    def on_clipboard_updated(self, content):
        """剪贴板更新时根据当前模式执行不同操作"""
        print(f"接收到剪贴板更新: {content}")
        print(f"当前模式: {self.current_mode}")
        print(f"剪贴板监控启用: {self.clipboard_monitor_enabled}")
        # 检查是否启用了剪贴板监控
        if not self.clipboard_monitor_enabled:
            print("剪贴板监控已禁用")
            return
        
        # 检查内容是否与上次翻译的结果相同，避免循环翻译
        if content.strip() == self.last_translated_content.strip():
            print("内容与上次翻译结果相同，跳过")
            return
        
        # 根据当前模式执行不同操作
        if self.current_mode == "translate":
            # 翻译模式：执行翻译
            print("执行翻译")
            self.translate(content)
        else:
            # 休息模式：只有当复制了"你好"时才执行聊天
            if content.strip() == "你好":
                print("检测到'你好'，执行聊天")
                self.chat(content)
            else:
                print("休息模式下只响应'你好'，跳过其他内容")

    def is_chinese_text(self, text):
        """检测文本是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def disable_clipboard_monitor_temp(self):
        """暂时禁用剪贴板监控，防止循环翻译"""
        self.clipboard_monitor_enabled = False
        # 1秒后重新启用
        QTimer.singleShot(1000, self.enable_clipboard_monitor)

    def enable_clipboard_monitor(self):
        """启用剪贴板监控"""
        self.clipboard_monitor_enabled = True
    
    def mousePressEvent(self, event):
        """鼠标按下事件，开始拖动"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件，拖动窗口"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件，结束拖动"""
        self.dragging = False
        # 拖动结束后更新状态牌子的位置
        self.update_status_sign_position()
        event.accept()
    
    def update_animation(self):
        """更新宠物动画帧"""
        if self.current_state == "idle":
            frames = self.resource_manager.get_idle_frames()
        else:  # translation
            frames = self.resource_manager.get_translation_frames()
        
        if frames:
            self.current_frame = (self.current_frame + 1) % len(frames)
            original_pixmap = frames[self.current_frame]
            # 应用缩放因子
            scaled_width = int(original_pixmap.width() * self.scale_factor)
            scaled_height = int(original_pixmap.height() * self.scale_factor)
            scaled_pixmap = original_pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.pet_label.setPixmap(scaled_pixmap)
            # 调整窗口大小以适应缩放后的图像
            self.resize(scaled_pixmap.width(), scaled_pixmap.height())
            # 更新设置按钮的位置
            self.update_settings_button_position()
            # 只在窗口大小变化时更新状态牌子的位置
            if not hasattr(self, 'last_window_size') or self.last_window_size != self.size():
                self.update_status_sign_position()
                self.last_window_size = self.size()

    def wheelEvent(self, event):
        """鼠标滚轮事件，实现等比例缩放"""
        # 获取滚轮方向
        delta = event.angleDelta().y()
        if delta > 0:
            # 放大
            self.scale_factor = min(self.scale_factor * 1.1, self.max_scale)
        else:
            # 缩小
            self.scale_factor = max(self.scale_factor * 0.9, self.min_scale)
        # 更新动画显示
        self.update_animation()

    def exit_program(self):
        """结束程序"""
        # 停止动画定时器
        self.animation_timer.stop()
        # 停止剪贴板监控
        try:
            # 直接退出应用
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()
        except Exception as e:
            print(f"关闭程序时错误: {str(e)}")
    
    def set_state(self, state):
        """设置宠物状态"""
        if state != self.current_state:
            self.current_state = state
            self.current_frame = 0
    
    def closeEvent(self, event):
        """关闭窗口时直接退出程序，而不是最小化到托盘"""
        # 停止动画定时器
        self.animation_timer.stop()
        # 停止剪贴板监控
        try:
            # 假设主程序中有对clipboard_monitor的引用
            # 这里我们直接退出应用
            from PyQt5.QtWidgets import QApplication
            QApplication.quit()
        except Exception as e:
            print(f"关闭程序时错误: {str(e)}")
        # 接受关闭事件
        event.accept()