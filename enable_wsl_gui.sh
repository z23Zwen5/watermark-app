#!/bin/bash
echo "配置 WSL GUI 支持..."

# 1. 检查是否为 WSL2
if grep -q microsoft /proc/version; then
    echo "✓ 检测到 WSL 环境"
    
    # 2. 设置 DISPLAY 变量
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0
    echo "✓ DISPLAY 设置为: $DISPLAY"
    
    # 3. 安装必要的包
    echo "需要安装 python3-tk 包，请运行："
    echo "sudo apt-get update && sudo apt-get install -y python3-tk"
    
    # 4. 提醒用户安装 X Server
    echo ""
    echo "=== 重要提示 ==="
    echo "1. 请在 Windows 上安装 X Server (如 VcXsrv 或 Xming)"
    echo "2. 启动 X Server 时，勾选 'Disable access control'"
    echo "3. 然后运行: python3 src/watermark_app_multilayer.py"
else
    echo "非 WSL 环境，直接运行即可"
fi
