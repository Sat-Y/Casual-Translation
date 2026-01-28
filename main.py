import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow
from utils.hotkey import register_hotkey
from clipboard_monitor import ClipboardMonitor
from translator import Translator

# 设置应用图标
def set_app_icon(app):
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "a.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"已设置应用图标: {icon_path}")
        else:
            print(f"图标文件不存在: {icon_path}")
    except Exception as e:
        print(f"设置图标失败: {str(e)}")

class TranslationApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.translator = Translator()
        self.main_window = MainWindow(self.translator)
        self.clipboard_monitor = ClipboardMonitor(self.translator, self.main_window)
        
    def run(self):
        set_app_icon(self.app)
        # 移除热键注册，用户不需要这个功能
        # register_hotkey(self.main_window.translate_selected_text)
        print("热键功能已移除，程序会自动监控剪贴板")
        self.main_window.show()
        return self.app.exec_()

if __name__ == "__main__":
    app = TranslationApp()
    sys.exit(app.run())