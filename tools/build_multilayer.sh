#!/bin/bash
# Multi-Layer Watermark App v1.5 构建脚本
# 用于将 Python 程序打包成独立可执行文件

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
DIST_DIR="$PROJECT_ROOT/dist"
SRC_FILE="$PROJECT_ROOT/src/watermark_app_multilayer.py"
ICON_FILE="$PROJECT_ROOT/assets/watermark_app_icon.ico"
SPEC_FILE="$BUILD_DIR/MultiLayerWatermark_v1.5.spec"

echo -e "${BLUE}🔨 Multi-Layer Watermark App v1.5 构建脚本${NC}"
echo "================================================"

# 检查 Python
echo -e "${YELLOW}📦 检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装！${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3: $(python3 --version)${NC}"

# 检查 PyInstaller
echo -e "${YELLOW}📦 检查 PyInstaller...${NC}"
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PyInstaller 未安装，正在安装...${NC}"
    pip3 install pyinstaller
fi
echo -e "${GREEN}✅ PyInstaller 已安装${NC}"

# 检查依赖
echo -e "${YELLOW}📦 检查项目依赖...${NC}"
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip3 install -r "$PROJECT_ROOT/requirements.txt" -q
    echo -e "${GREEN}✅ 依赖已安装${NC}"
else
    echo -e "${YELLOW}⚠️  未找到 requirements.txt${NC}"
fi

# 检查源文件
echo -e "${YELLOW}📄 检查源文件...${NC}"
if [ ! -f "$SRC_FILE" ]; then
    echo -e "${RED}❌ 源文件不存在: $SRC_FILE${NC}"
    exit 1
fi
echo -e "${GREEN}✅ 源文件: $(basename $SRC_FILE)${NC}"

# 检查图标文件
echo -e "${YELLOW}🎨 检查图标文件...${NC}"
if [ ! -f "$ICON_FILE" ]; then
    echo -e "${YELLOW}⚠️  图标文件不存在: $ICON_FILE${NC}"
    ICON_ARG=""
else
    echo -e "${GREEN}✅ 图标文件: $(basename $ICON_FILE)${NC}"
    ICON_ARG="--icon=$ICON_FILE"
fi

# 清理旧的构建
echo -e "${YELLOW}🧹 清理旧的构建文件...${NC}"
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
    echo -e "${GREEN}✅ 已清理 build 目录${NC}"
fi
if [ -d "$DIST_DIR" ]; then
    rm -rf "$DIST_DIR"
    echo -e "${GREEN}✅ 已清理 dist 目录${NC}"
fi

# 创建构建目录
mkdir -p "$BUILD_DIR"

# 开始构建
echo ""
echo -e "${BLUE}🚀 开始构建...${NC}"
echo "================================================"

cd "$PROJECT_ROOT"

# 使用 PyInstaller 构建
# 注意：不打包 configs 目录，因为配置文件应该在运行时创建
# 用户可以手动复制 configs 目录到可执行文件目录
python3 -m PyInstaller \
    --name="MultiLayerWatermark_v1.5" \
    --onefile \
    --windowed \
    --clean \
    $ICON_ARG \
    --hidden-import=numpy \
    --hidden-import=PIL \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=tkinter \
    --hidden-import=json \
    --distpath="$DIST_DIR" \
    --workpath="$BUILD_DIR/temp" \
    --specpath="$BUILD_DIR" \
    "$SRC_FILE"

# 检查构建结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 构建成功！${NC}"
    echo "================================================"
    echo -e "${BLUE}📦 输出文件:${NC}"

    # Windows 可执行文件
    if [ -f "$DIST_DIR/MultiLayerWatermark_v1.5.exe" ]; then
        ls -lh "$DIST_DIR/MultiLayerWatermark_v1.5.exe"
        echo ""
        echo -e "${GREEN}✅ Windows 可执行文件: $DIST_DIR/MultiLayerWatermark_v1.5.exe${NC}"
    # Linux/Mac 可执行文件
    elif [ -f "$DIST_DIR/MultiLayerWatermark_v1.5" ]; then
        ls -lh "$DIST_DIR/MultiLayerWatermark_v1.5"
        echo ""
        echo -e "${GREEN}✅ 可执行文件: $DIST_DIR/MultiLayerWatermark_v1.5${NC}"
    else
        echo -e "${YELLOW}⚠️  未找到可执行文件${NC}"
    fi

    echo ""
    echo -e "${BLUE}💡 下一步:${NC}"
    echo "1. 测试可执行文件: cd $DIST_DIR && ./MultiLayerWatermark_v1.5"
    echo "2. 如果需要，复制 configs/ 目录到可执行文件目录"
else
    echo ""
    echo -e "${RED}❌ 构建失败！${NC}"
    exit 1
fi
