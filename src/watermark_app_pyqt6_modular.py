#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Layer Watermark App - PyQt6 Modular Version
主程序 - 模块化 PyQt6 版本

这是新的模块化架构入口
使用 ui/ 包中的模块化组件
"""
import os
import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow
from ui.styles import apply_global_style


def _get_icon_path() -> str:
    """获取应用图标路径（兼容开发环境和 PyInstaller 打包）"""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", "watermark_app_icon.ico")


def main():
    """主函数"""
    start_time = time.time()
    print("🚀 应用启动...")

    # Windows 任务栏图标：设置 AppUserModelID 使任务栏显示自定义图标
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "starcore.watermarkapp.v2"
        )
    except Exception:
        pass

    # 创建应用
    t0 = time.time()
    app = QApplication(sys.argv)

    # 设置应用图标（任务栏 + 窗口）
    icon_path = _get_icon_path()
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    print(f"⏱️  创建 QApplication: {(time.time() - t0)*1000:.0f}ms")

    # 预加载 qtawesome 图标字体（避免首次使用时延迟）
    t0 = time.time()
    try:
        import qtawesome as qta
        # 创建一个临时图标来触发字体加载
        _ = qta.icon('fa5s.circle')
        print(f"⏱️  预加载图标字体: {(time.time() - t0)*1000:.0f}ms")
    except:
        print(f"⏱️  预加载图标字体: 失败")

    # 应用全局样式
    t0 = time.time()
    apply_global_style(app)
    print(f"⏱️  应用全局样式: {(time.time() - t0)*1000:.0f}ms")

    # 创建并显示主窗口
    t0 = time.time()
    window = MainWindow()
    print(f"⏱️  创建主窗口: {(time.time() - t0)*1000:.0f}ms")

    t0 = time.time()
    window.show()
    print(f"⏱️  显示窗口: {(time.time() - t0)*1000:.0f}ms")

    print(f"✅ 总启动时间: {(time.time() - start_time)*1000:.0f}ms\n")

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
