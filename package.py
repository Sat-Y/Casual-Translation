#!/usr/bin/env python3
# 打包脚本，解决PyInstaller无法处理含有中文路径的问题

import os
import shutil
import subprocess
import tempfile

# 定义源目录和目标目录
source_dir = os.path.abspath('.')
dist_dir = os.path.join(source_dir, 'dist')

# 创建临时目录，使用不含中文的路径
temp_dir = tempfile.mkdtemp(prefix='casual_', suffix='_translation')
print(f"创建临时目录: {temp_dir}")

try:
    # 复制项目文件到临时目录
    print("复制项目文件到临时目录...")
    
    # 复制主要Python文件
    files_to_copy = [
        'main.py',
        'translator.py',
        'clipboard_monitor.py',
        'main.spec',
        '桌宠形象1.ico',
        'requirements.txt'
    ]
    
    for file in files_to_copy:
        src = os.path.join(source_dir, file)
        dst = os.path.join(temp_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"复制文件: {file}")
    
    # 复制目录
    dirs_to_copy = [
        'ui',
        'utils',
        'resources'
    ]
    
    for dir_name in dirs_to_copy:
        src = os.path.join(source_dir, dir_name)
        dst = os.path.join(temp_dir, dir_name)
        if os.path.exists(src):
            shutil.copytree(src, dst)
            print(f"复制目录: {dir_name}")
    
    # 复制虚拟环境中的PyQt5插件
    print("复制PyQt5插件...")
    pyqt5_plugins_src = os.path.join(source_dir, '.venv', 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')
    pyqt5_plugins_dst = os.path.join(temp_dir, 'plugins')
    if os.path.exists(pyqt5_plugins_src):
        shutil.copytree(pyqt5_plugins_src, pyqt5_plugins_dst)
        print(f"复制PyQt5插件目录")
    
    # 修改spec文件
    print("修改spec文件...")
    spec_file = os.path.join(temp_dir, 'main.spec')
    if os.path.exists(spec_file):
        with open(spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
        
        # 修改输出文件名
        spec_content = spec_content.replace("name='main'", "name='Casual Translation'")
        
        # 添加插件目录到datas
        plugins_dst = os.path.join('plugins')
        if "datas=[('resources', 'resources')]" in spec_content:
            spec_content = spec_content.replace(
                "datas=[('resources', 'resources')]",
                f"datas=[('resources', 'resources'), ('{plugins_dst}', 'PyQt5\\Qt5\\plugins')]"
            )
        
        # 写入修改后的spec文件
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print("修改spec文件完成")
    
    # 运行PyInstaller进行打包
    print("运行PyInstaller进行打包...")
    subprocess.run(
        ['pyinstaller', 'main.spec'],
        cwd=temp_dir,
        check=True,
        shell=True
    )
    
    # 复制打包结果到原目录
    print("复制打包结果到原目录...")
    temp_dist_dir = os.path.join(temp_dir, 'dist')
    if os.path.exists(temp_dist_dir):
        # 确保目标dist目录存在
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)
        
        # 复制所有文件
        for item in os.listdir(temp_dist_dir):
            src = os.path.join(temp_dist_dir, item)
            dst = os.path.join(dist_dir, item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"复制文件: {item}")
            elif os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"复制目录: {item}")
    
    print("\n打包完成！")
    print(f"打包结果位于: {dist_dir}")
    
finally:
    # 清理临时目录
    print(f"清理临时目录: {temp_dir}")
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("临时目录清理完成")
