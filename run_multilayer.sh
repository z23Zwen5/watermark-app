#!/bin/bash

echo "========================================"
echo "  Multi-Layer Watermark App v1.5"
echo "  多图层水印应用 v1.5"
echo "========================================"
echo ""

# 检查 Python 是否安装
if command -v python3 &> /dev/null; then
    echo "[启动中] 使用 python3 命令..."
    python3 src/watermark_app_multilayer.py
elif command -v python &> /dev/null; then
    echo "[启动中] 使用 python 命令..."
    python src/watermark_app_multilayer.py
else
    echo "[错误] 未找到 Python！"
    echo ""
    echo "请安装 Python 3.7 或更高版本："
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi
