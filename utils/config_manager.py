import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载配置文件错误: {str(e)}")
        # 返回默认配置
        return {
            "current_mode": "translate",
            "rest_prompt": "You are a cute and friendly desktop pet. Chat with the user in a warm and lively manner. Be playful and engaging, and respond to their questions and comments with enthusiasm."
        }
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件错误: {str(e)}")
            return False
    
    def get_current_mode(self):
        """获取当前模式"""
        return self.config.get("current_mode", "rest")
    
    def set_current_mode(self, mode):
        """设置当前模式"""
        self.config["current_mode"] = mode
        return self.save_config()
    
    def get_rest_prompt(self):
        """获取休息模式提示词"""
        return self.config.get("rest_prompt", "You are a cute and friendly desktop pet. Chat with the user in a warm and lively manner. Be playful and engaging, and respond to their questions and comments with enthusiasm.")
    
    def set_rest_prompt(self, prompt):
        """设置休息模式提示词"""
        self.config["rest_prompt"] = prompt
        return self.save_config()
    
    def get_config(self):
        """获取完整配置"""
        return self.config
    
    def set_config(self, config):
        """设置完整配置"""
        self.config = config
        return self.save_config()