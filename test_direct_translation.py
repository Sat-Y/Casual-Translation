#!/usr/bin/env python3
# 直接测试翻译功能的脚本
from translator import Translator

def test_direct_translation():
    translator = Translator()
    
    # 测试中文转英文
    print("测试中文转英文：")
    chinese_text = "你好，世界！"
    english_translation = translator.translate(chinese_text, src='zh-CN', dest='en')
    print(f"中文：{chinese_text}")
    print(f"英文：{english_translation}")
    print()
    
    # 测试英文转中文
    print("测试英文转中文：")
    english_text = "Hello, world!"
    chinese_translation = translator.translate(english_text, src='en', dest='zh-CN')
    print(f"英文：{english_text}")
    print(f"中文：{chinese_translation}")
    print()
    
    print("直接翻译测试完成！")

if __name__ == "__main__":
    test_direct_translation()
