#!/usr/bin/env python3
"""
Build script for Multi-Layer Watermark App with icon
"""

import os
import sys
import subprocess
import shutil

def main():
    # 设置路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_file = os.path.join(project_root, "src", "watermark_app_multilayer.py")
    icon_file = os.path.join(project_root, "assets", "watermark_app_icon.ico")
    dist_dir = os.path.join(project_root, "dist")
    build_dir = os.path.join(project_root, "build")

    # 检查源文件
    if not os.path.exists(src_file):
        print(f"Error: Source file not found: {src_file}")
        return 1

    # 检查图标文件
    if not os.path.exists(icon_file):
        print(f"Error: Icon file not found: {icon_file}")
        return 1

    print("========================================")
    print("  Multi-Layer Watermark App v1.6 Build")
    print("========================================")
    print()

    # 清理旧的构建文件
    print("[1/4] Cleaning old build files...")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    # 构建命令
    print("[2/4] Building executable with icon...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--icon={icon_file}",
        f"--name=WatermarkApp_v1.6",
        "--add-data", f"{os.path.join(project_root, 'configs')}:configs",
        src_file
    ]

    print(f"Command: {' '.join(cmd)}")
    print()

    # 执行构建
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Build failed!")
            print("STDERR:", result.stderr)
            return 1
    except Exception as e:
        print(f"Error running PyInstaller: {e}")
        return 1

    print("[3/4] Build complete!")

    # 检查输出
    exe_file = os.path.join(dist_dir, "WatermarkApp_v1.6.exe")
    if os.path.exists(exe_file):
        size_mb = os.path.getsize(exe_file) / (1024 * 1024)
        print(f"[4/4] Success! Executable created:")
        print(f"  File: {exe_file}")
        print(f"  Size: {size_mb:.2f} MB")
    else:
        print("[4/4] Warning: Executable not found in expected location")

    print()
    print("Build completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())