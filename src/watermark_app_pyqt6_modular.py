#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Layer Watermark App - PyQt6 Modular Version
主程序 - 模块化 PyQt6 版本

这是新的模块化架构入口
使用 ui/ 包中的模块化组件
"""
import sys
import time
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import apply_global_style


def main():
    """主函数"""
    start_time = time.time()
    print("🚀 应用启动...")

    # 创建应用
    t0 = time.time()
    app = QApplication(sys.argv)
    print(f"⏱️  创建 QApplication: {(time.time() - t0)*1000:.0f}ms")

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
