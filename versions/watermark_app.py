#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WatermarkApp 主启动文件
自动启动最新版本: V1.5 Alpha保护智能水印应用

作者: AI Assistant
版本: V1.5 (Alpha Protection)
日期: 2024
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # 导入并启动最新版本的应用
    from watermark_app_alpha_protected import AlphaProtectedWatermarkApp
    import tkinter as tk
    
    def main():
        """主函数"""
        print("🚀 启动 WatermarkApp V1.5 (Alpha Protection)")
        print("📍 当前版本: Alpha通道保护智能水印应用")
        print("✨ 新功能: 智能保护公司logo/图标，自动调整背景图案颜色")
        print("-" * 50)
        
        root = tk.Tk()
        app = AlphaProtectedWatermarkApp(root)
        root.mainloop()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保所有依赖已正确安装:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动错误: {e}")
    sys.exit(1) 