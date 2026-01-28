# Casual Translation

一个简洁易用的桌面翻译工具，支持中英文互译，具有剪贴板监控和桌面宠物模式。

## 功能特点

### 📝 翻译功能
- 支持中英文互译
- 自动监控剪贴板，复制文本后自动翻译
- 使用DeepSeek API提供高质量翻译
- 简洁的用户界面，操作直观

### 🐱 桌面宠物模式
- 休息时可作为桌面宠物互动
- 可爱的动画效果
- 支持简单的聊天功能

### 🎨 界面设计
- 美观简洁的界面
- 支持拖拽移动
- 响应式设计，适配不同屏幕尺寸

## 快速开始

### 环境要求
- Python 3.7+
- Windows 10/11

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python main.py
```

或者双击运行 `run.bat` 文件。

### 打包成可执行文件

```bash
python package.py
```

## 配置说明

### API密钥配置

1. 打开 `translator.py` 文件
2. 在 `deepseek_translate` 和 `chat` 方法中，将 `Authorization` 头中的 API 密钥替换为您自己的 DeepSeek API 密钥

### 提示词配置

- `translation_prompt.txt` - 翻译模式的系统提示词
- `rest_prompt.txt` - 休息模式的系统提示词

您可以根据需要修改这些文件来自定义翻译和聊天行为。

## 使用方法

1. **翻译模式**：
   - 复制任何文本，系统会自动检测并翻译
   - 翻译结果会显示在主界面上
   - 支持手动输入文本进行翻译

2. **休息模式**：
   - 点击界面上的切换按钮进入休息模式
   - 可以与桌面宠物进行简单的聊天
   - 再次点击按钮返回翻译模式

## 项目结构

```
Casual Translation/
├── main.py              # 主入口文件
├── translator.py        # 翻译功能实现
├── clipboard_monitor.py # 剪贴板监控
├── ui/                  # UI相关文件
├── utils/               # 工具函数
├── requirements.txt     # 依赖包
├── run.bat              # 运行脚本
├── package.py           # 打包脚本
├── translation_prompt.txt # 翻译提示词
└── rest_prompt.txt      # 休息模式提示词
```

## 技术栈

- **前端**：PyQt5
- **后端**：Python 3.13
- **翻译服务**：DeepSeek API
- **剪贴板监控**：pyperclip
- **打包工具**：PyInstaller

## 注意事项

1. 使用前请确保您已配置有效的 DeepSeek API 密钥
2. 翻译服务依赖网络连接
3. 首次运行可能需要安装依赖包

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

本项目采用 MIT 许可证。

## 联系方式

- GitHub: [https://github.com/Sat-Y/Casual-Translation](https://github.com/Sat-Y/Casual-Translation)
