import os
from PyQt5.QtGui import QPixmap

class ResourceManager:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(__file__))
        self.idle_frames = []
        self.translation_frames = []
        self.load_resources()
    
    def load_resources(self):
        """加载所有资源图像"""
        self.load_idle_frames()
        self.load_translation_frames()
    
    def load_idle_frames(self):
        """加载idle状态的动画帧"""
        idle_path = os.path.join(self.base_path, "resources", "idle")
        if os.path.exists(idle_path):
            for i in range(1, 9):
                frame_path = os.path.join(idle_path, f"idle_{i}.png")
                if os.path.exists(frame_path):
                    pixmap = QPixmap(frame_path)
                    if not pixmap.isNull():
                        self.idle_frames.append(pixmap)
                    else:
                        print(f"加载idle帧失败: {frame_path}")
                else:
                    print(f"idle帧文件不存在: {frame_path}")
        else:
            print(f"idle文件夹不存在: {idle_path}")
        print(f"成功加载 {len(self.idle_frames)} 个idle帧")
    
    def load_translation_frames(self):
        """加载translation状态的动画帧"""
        translation_path = os.path.join(self.base_path, "resources", "translation")
        if os.path.exists(translation_path):
            for i in range(1, 5):
                frame_path = os.path.join(translation_path, f"t_{i}.png")
                if os.path.exists(frame_path):
                    pixmap = QPixmap(frame_path)
                    if not pixmap.isNull():
                        self.translation_frames.append(pixmap)
                    else:
                        print(f"加载translation帧失败: {frame_path}")
                else:
                    print(f"translation帧文件不存在: {frame_path}")
        else:
            print(f"translation文件夹不存在: {translation_path}")
        print(f"成功加载 {len(self.translation_frames)} 个translation帧")
    
    def get_idle_frames(self):
        """获取idle状态的动画帧"""
        return self.idle_frames
    
    def get_translation_frames(self):
        """获取translation状态的动画帧"""
        return self.translation_frames
    
    def has_resources(self):
        """检查是否有足够的资源"""
        return len(self.idle_frames) > 0
