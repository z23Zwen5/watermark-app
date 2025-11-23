#!/bin/bash
# Multi-Layer Watermark App v1.6.2 优化构建脚本 (Linux/macOS)
# PyQt6 版本 - Genshin Impact 风格界面
# 优化重点: 使用 onedir 模式，大幅提升启动速度（5-7秒 -> 0.5-1秒）
# 详细分析见: docs/STARTUP_PERFORMANCE_ANALYSIS.md

set -e  # 遇到错误立即退出

echo "========================================"
echo "  Multi-Layer Watermark Build Script"
echo "  Version: v1.6.2 PyQt6 (Optimized)"
echo "  Mode: onedir (Fast Startup)"
echo "========================================"
echo ""

# 设置路径
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
DIST_DIR="$PROJECT_ROOT/dist"
SRC_FILE="$PROJECT_ROOT/src/watermark_app_pyqt6_ui.py"
ICON_FILE="$PROJECT_ROOT/assets/watermark_app_icon.ico"

echo "[1/8] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 未安装！"
    echo "请安装 Python 3.7+"
    exit 1
fi
python3 --version
echo "[OK] Python 环境正常"
echo ""

echo "[2/8] 检查 PyInstaller..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[WARN] PyInstaller 未安装，正在安装..."
    pip3 install pyinstaller
fi
echo "[OK] PyInstaller 已安装"
echo ""

echo "[3/8] 检查项目依赖..."
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "正在安装依赖..."
    pip3 install -r "$PROJECT_ROOT/requirements.txt" -q
    echo "[OK] 依赖已安装"
else
    echo "[WARN] 未找到 requirements.txt"
fi
echo ""

echo "[4/8] 检查源文件..."
if [ ! -f "$SRC_FILE" ]; then
    echo "[ERROR] 源文件不存在: $SRC_FILE"
    exit 1
fi
echo "[OK] 源文件: watermark_app_pyqt6_ui.py"
echo ""

echo "[4.5/8] 检查 PyQt6 依赖..."
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "[WARN] PyQt6 未安装，正在安装..."
    pip3 install PyQt6 qtawesome
fi
if ! python3 -c "import qtawesome" 2>/dev/null; then
    echo "[WARN] qtawesome 未安装，正在安装..."
    pip3 install qtawesome
fi
echo "[OK] PyQt6 和 qtawesome 已安装"
echo ""

echo "[5/8] 检查图标文件..."
ICON_ARG=""
if [ -f "$ICON_FILE" ]; then
    echo "[OK] 图标文件: watermark_app_icon.ico"
    ICON_ARG="--icon=$ICON_FILE"
else
    echo "[WARN] 图标文件不存在: $ICON_FILE"
fi
echo ""

echo "[6/8] 清理旧的构建文件..."
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
    echo "[OK] 已清理 build 目录"
fi
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
    echo "[OK] 已清理 dist 目录"
fi
mkdir -p "$BUILD_DIR"
echo ""

echo "[7/8] 开始构建（优化模式）..."
echo "========================================"
echo "优化说明:"
echo "  [✓] PyQt6 版本 - 现代化界面"
echo "  [✓] onedir 模式 - 启动速度提升 2-4 秒"
echo "  [✓] 自动检测依赖"
echo "  [✓] 优化 DLL 加载"
echo "========================================"
echo ""
cd "$PROJECT_ROOT"

# 使用 PyInstaller 构建（优化版 PyQt6）
# 关键变化：
#   1. --onedir (替代 --onefile) - 大幅提升启动速度
#   2. 添加 PyQt6 必要的隐藏导入
#   3. 添加 --noupx（避免 UPX 压缩带来的启动延迟）
#   4. 收集 qtawesome 数据文件

python3 -m PyInstaller \
    --name=WatermarkApp_PyQt6_v1.6.2_Optimized \
    --onedir \
    --windowed \
    --clean \
    --noupx \
    $ICON_ARG \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=qtawesome \
    --collect-data qtawesome \
    --hidden-import=numpy \
    --hidden-import=PIL \
    --distpath="$DIST_DIR" \
    --workpath="$BUILD_DIR/temp" \
    --specpath="$BUILD_DIR" \
    "$SRC_FILE"

echo ""
echo "========================================"
echo "  构建成功！"
echo "========================================"
echo ""

# 检查输出目录
OUTPUT_DIR="$DIST_DIR/WatermarkApp_PyQt6_v1.6.2_Optimized"
EXE_FILE="$OUTPUT_DIR/WatermarkApp_PyQt6_v1.6.2_Optimized"

if [ -f "$EXE_FILE" ]; then
    echo "[OK] 输出目录: $OUTPUT_DIR"
    echo "[OK] 主程序: WatermarkApp_PyQt6_v1.6.2_Optimized"
    echo ""

    # 显示目录大小
    SIZE=$(du -sh "$OUTPUT_DIR" | cut -f1)
    echo "[INFO] 程序大小: $SIZE"

    echo ""
    echo "========================================"
    echo "  性能优化说明"
    echo "========================================"
    echo ""
    echo "界面版本:"
    echo "  PyQt6 版本 - Genshin Impact 风格 ✓"
    echo ""
    echo "启动速度对比:"
    echo "  onefile 模式:  5-7 秒   (旧版)"
    echo "  onedir 模式:   0.5-1 秒 (当前) ✓"
    echo ""
    echo "分发方式:"
    echo "  1. 压缩整个文件夹: $OUTPUT_DIR"
    echo "  2. 分发给用户后解压使用"
    echo "  3. 运行: ./WatermarkApp_PyQt6_v1.6.2_Optimized"
    echo ""
    echo "下一步优化（可选）:"
    echo "  - 实施代码层面优化（延迟加载、异步字体扫描）"
    echo "  - 详见: docs/STARTUP_PERFORMANCE_ANALYSIS.md"
    echo ""
else
    echo "[WARN] 未找到可执行文件"
    echo "请检查: $OUTPUT_DIR"
fi

echo "[8/8] 创建快速启动说明文件..."
README_FILE="$OUTPUT_DIR/README_快速开始.txt"
if [ -f "$EXE_FILE" ]; then
    cat > "$README_FILE" << 'EOF'
Multi-Layer Watermark App v1.6.2 PyQt6 - 快速开始
========================================

界面版本:
  PyQt6 版本 - Genshin Impact 原神风格界面

运行方法:
  ./WatermarkApp_PyQt6_v1.6.2_Optimized

优化说明:
  - 使用 onedir 模式，启动速度提升 5-10 倍
  - 从 5-7 秒降至 0.5-1 秒
  - PyQt6 现代化界面，更流畅的用户体验

分发说明:
  - 需要分发整个文件夹（而非单个可执行文件）
  - 请保持所有库文件在同一目录
  - 包含 PyQt6 运行时库

故障排除:
  - 如果启动失败，检查执行权限: chmod +x WatermarkApp_PyQt6_v1.6.2_Optimized
  - 确保所有文件解压到同一目录
  - 需要较新的操作系统（Linux: glibc 2.28+, macOS: 10.14+）

文档资源:
  - GitHub: https://github.com/z23Zwen5/watermark-app
  - 性能分析: docs/STARTUP_PERFORMANCE_ANALYSIS.md

========================================
EOF
    echo "[OK] 已创建快速启动说明: README_快速开始.txt"

    # 设置可执行权限
    chmod +x "$EXE_FILE"
    echo "[OK] 已设置可执行权限"
fi

echo ""
echo "========================================"
echo "  构建完成！"
echo "========================================"
