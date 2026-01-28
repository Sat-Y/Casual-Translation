import requests
import time

class Translator:
    def __init__(self):
        pass
    
    def translate(self, text, src='zh-CN', dest='en'):
        # 只使用deepseek API（国内AI翻译）
        try:
            result = self.deepseek_translate(text, src, dest)
            if result:
                return result
        except Exception as e:
            print(f"DeepSeek翻译失败: {str(e)}")
        
        # 如果失败，返回错误信息
        return "翻译服务暂时不可用，请检查网络连接后再试"
    

    
    def deepseek_translate(self, text, src, dest):
        """使用DeepSeek API进行翻译（国内AI翻译服务）"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            # 根据翻译方向生成更明确的提示词，确保短词也能正确翻译
            if src == 'zh-CN' and dest == 'en':
                system_prompt = "You are a professional translator. Your only task is to translate the following Chinese text to English accurately. Do not add any explanations, just provide the translation. Maintain the original meaning and context. For short words or phrases, simply translate them directly without any additional content."
            elif src == 'en' and dest == 'zh-CN':
                system_prompt = "You are a professional translator. Your only task is to translate the following English text to Chinese accurately. Do not add any explanations, just provide the translation. Maintain the original meaning and context. For short words or phrases, simply translate them directly without any additional content."
            else:
                # 默认提示词
                system_prompt = "You are a professional translator. Your only task is to translate the text accurately. Do not add any explanations, just provide the translation. Maintain the original meaning and context. For short words or phrases, simply translate them directly without any additional content."
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 1000
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_DEEPSEEK_API_KEY"  # 请替换为您自己的DeepSeek API密钥
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
            else:
                print(f"DeepSeek API错误: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"DeepSeek翻译异常: {str(e)}")
        return None
    
    def load_system_prompt(self):
        """加载系统提示词"""
        try:
            with open("translation_prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            # 默认提示词
            return "You are a professional translator. Translate the following Chinese text to English accurately. Maintain the original meaning and context."
    
    def save_system_prompt(self, prompt):
        """保存系统提示词"""
        try:
            with open("translation_prompt.txt", "w", encoding="utf-8") as f:
                f.write(prompt)
            return True
        except Exception as e:
            print(f"保存提示词失败: {str(e)}")
            return False
    
    def load_rest_prompt(self):
        """加载休息模式提示词"""
        try:
            with open("rest_prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except:
            # 默认提示词
            return "You are a cute and friendly desktop pet. Chat with the user in a warm and lively manner. Be playful and engaging, and respond to their questions and comments with enthusiasm."
    
    def save_rest_prompt(self, prompt):
        """保存休息模式提示词"""
        try:
            with open("rest_prompt.txt", "w", encoding="utf-8") as f:
                f.write(prompt)
            return True
        except Exception as e:
            print(f"保存休息提示词失败: {str(e)}")
            return False
    
    def chat(self, text):
        """休息模式的AI聊天功能"""
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            # 加载休息模式提示词
            system_prompt = self.load_rest_prompt()
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_DEEPSEEK_API_KEY"  # 请替换为您自己的DeepSeek API密钥
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
            else:
                print(f"DeepSeek API错误: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"聊天异常: {str(e)}")
        return "抱歉，我现在无法聊天，请稍后再试。"
    

