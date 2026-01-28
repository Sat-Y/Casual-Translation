#!/usr/bin/env python3
# 创建不含中文路径的虚拟环境并打包项目

import os
import shutil
import subprocess
import tempfile

# 定义源目录
source_dir = os.path.abspath('.')
dist_dir = os.path.join(source_dir, 'dist')

# 创建临时目录，使用不含中文的路径
temp_dir = tempfile.mkdtemp(prefix='casual_', suffix='_translation')
print(f"创建临时目录: {temp_dir}")

# 创建不含中文的虚拟环境路径
venv_dir = os.path.join(temp_dir, 'venv')
print(f"创建虚拟环境目录: {venv_dir}")

try:
    # 创建虚拟环境
    print("创建虚拟环境...")
    subprocess.run(
        ['python', '-m', 'venv', venv_dir],
        check=True,
        shell=True
    )
    
    # 激活虚拟环境并安装依赖
    print("安装项目依赖...")
    pip_exe = os.path.join(venv_dir, 'Scripts', 'pip.exe')
    requirements_txt = os.path.join(source_dir, 'requirements.txt')
    
    subprocess.run(
        [pip_exe, 'install', '-r', requirements_txt],
        check=True,
        shell=True
    )
    
    # 复制项目文件到临时目录
    print("复制项目文件到临时目录...")
    
    # 复制主要Python文件
    files_to_copy = [
        'main.py',
        'translator.py',
        'clipboard_monitor.py',
        '桌宠形象1.ico',
        'requirements.txt'
    ]
    
    for file in files_to_copy:
        src = os.path.join(source_dir, file)
        dst = os.path.join(temp_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"复制文件: {file}")
        else:
            print(f"警告: 文件不存在: {src}")
    
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
        else:
            print(f"警告: 目录不存在: {src}")
    
    # 创建新的spec文件
    print("创建新的spec文件...")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


# 确保包含所有必要的Python文件
added_files = [
    ('translator.py', '.'),
    ('clipboard_monitor.py', '.'),
]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('resources', 'resources')] + added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Casual Translation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=['桌宠形象1.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Casual Translation',
)
"""
    
    spec_file = os.path.join(temp_dir, 'Casual Translation.spec')
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("创建spec文件完成")
    
    # 运行PyInstaller进行打包
    print("运行PyInstaller进行打包...")
    pyinstaller_exe = os.path.join(venv_dir, 'Scripts', 'pyinstaller.exe')
    
    subprocess.run(
        [pyinstaller_exe, 'Casual Translation.spec'],
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
            src_path = os.path.join(temp_dist_dir, item)
            dst_path = os.path.join(dist_dir, item)
            
            # 如果目标路径已存在，先删除
            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            
            # 复制文件或目录
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
                print(f"复制目录: {item}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"复制文件: {item}")
    
    print("打包完成！")
    print(f"打包结果已保存到: {dist_dir}")
    
finally:
    # 清理临时目录
    print(f"清理临时目录: {temp_dir}")
    try:
        shutil.rmtree(temp_dir)
        print("临时目录清理完成")
    except Exception as e:
        print(f"清理临时目录时出错: {str(e)}")
        print("临时目录可能需要手动清理")
