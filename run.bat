@echo off

:: 进入项目目录
cd /d "%~dp0"

:: 激活虚拟环境
call ".venv\Scripts\activate.bat"

:: 运行项目
python main.py

:: 暂停以便查看错误信息（如果有）
pause
