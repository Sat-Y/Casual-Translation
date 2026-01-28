import keyboard

def register_hotkey(callback):
    """注册热键鼠标侧键1来触发翻译功能"""
    try:
        # 鼠标侧键1通常对应mouse4
        keyboard.add_hotkey('mouse4', callback)
        print("热键已注册: 鼠标侧键1 (mouse4)")
    except Exception as e:
        print(f"热键注册错误: {str(e)}")