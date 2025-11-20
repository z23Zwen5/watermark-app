#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Layer Watermark App - PyQt6 Modular Version
主程序 - 模块化 PyQt6 版本

这是新的模块化架构入口
使用 ui/ 包中的模块化组件
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import apply_global_style


def main():
    """主函数"""
    # 创建应用
    app = QApplication(sys.argv)

    # 应用全局样式
    apply_global_style(app)

    # 创建并显示主窗口
    window = MainWindow()
    window.show()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
