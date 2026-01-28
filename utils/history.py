import json
import os

class HistoryManager:
    def __init__(self, history_file="translation_history.json"):
        self.history_file = history_file
        self.history = self.load_history()
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载历史记录错误: {str(e)}")
        return []
    
    def save_history(self):
        """保存历史记录"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录错误: {str(e)}")
    
    def add_record(self, original, translated):
        """添加翻译记录"""
        record = {
            "original": original,
            "translated": translated,
            "timestamp": self.get_timestamp()
        }
        self.history.insert(0, record)  # 添加到开头
        # 限制历史记录数量
        if len(self.history) > 100:
            self.history = self.history[:100]
        self.save_history()
    
    def get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_history(self):
        """获取历史记录"""
        return self.history
    
    def clear_history(self):
        """清空历史记录"""
        self.history = []
        self.save_history()