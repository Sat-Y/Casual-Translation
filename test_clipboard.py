#!/usr/bin/env python3
# 测试剪贴板操作的脚本
import pyperclip
import time

def test_clipboard_translation():
    print("开始测试剪贴板翻译功能...")
    
    # 测试中文转英文
    print("\n测试1: 中文转英文")
    chinese_text = "你好，世界！"
    pyperclip.copy(chinese_text)
    print(f"已复制中文文本: {chinese_text}")
    print("请查看程序是否显示英文翻译结果...")
    time.sleep(3)
    
    # 测试英文转中文
    print("\n测试2: 英文转中文")
    english_text = "Hello, world!"
    pyperclip.copy(english_text)
    print(f"已复制英文文本: {english_text}")
    print("请查看程序是否显示中文翻译结果...")
    time.sleep(3)
    
    # 测试更长的中文文本
    print("\n测试3: 更长的中文文本")
    long_chinese_text = "这是一个更长的中文文本，用于测试翻译功能是否正常工作。"
    pyperclip.copy(long_chinese_text)
    print(f"已复制中文文本: {long_chinese_text}")
    print("请查看程序是否显示英文翻译结果...")
    time.sleep(3)
    
    # 测试更长的英文文本
    print("\n测试4: 更长的英文文本")
    long_english_text = "This is a longer English text used to test whether the translation function works properly."
    pyperclip.copy(long_english_text)
    print(f"已复制英文文本: {long_english_text}")
    print("请查看程序是否显示中文翻译结果...")
    time.sleep(3)
    
    print("\n剪贴板翻译功能测试完成！")

if __name__ == "__main__":
    test_clipboard_translation()
