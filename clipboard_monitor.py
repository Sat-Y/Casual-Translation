import pyperclip
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal

class ClipboardMonitor(QObject):
    clipboard_updated = pyqtSignal(str)
    
    def __init__(self, translator, main_window):
        super().__init__()
        self.translator = translator
        self.main_window = main_window
        self.last_clipboard_content = ""
        self.running = True
        # 连接信号到主窗口的槽函数
        self.clipboard_updated.connect(self.main_window.on_clipboard_updated)
        self.thread = threading.Thread(target=self.monitor)
        self.thread.daemon = True
        self.thread.start()
    
    def monitor(self):
        while self.running:
            try:
                current_content = pyperclip.paste()
                if current_content != self.last_clipboard_content and current_content.strip():
                    self.last_clipboard_content = current_content
                    # 发送信号而不是直接调用方法
                    self.clipboard_updated.emit(current_content)
                time.sleep(0.5)
            except Exception as e:
                print(f"剪贴板监控错误: {str(e)}")
                time.sleep(1)
    
    def stop(self):
        self.running = False
        self.thread.join(timeout=1)