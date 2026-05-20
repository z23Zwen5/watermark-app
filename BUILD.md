# 🔨 构建指南

## 快速开始

### 一键构建（推荐）

```cmd
tools\build_pyqt6_modular.bat
```

**输出位置**: `dist/WatermarkApp_PyQt6_v2.0/`

---

## 构建模式说明

### ✅ onedir 模式（默认，推荐）

**特点**:
- ⚡ **启动速度快** - 0.5-1秒
- 📦 输出为文件夹（包含 .exe 和依赖 DLL）
- 💾 体积较大（~200MB）但启动无需解压

**构建命令**:
```cmd
tools\build_pyqt6_modular.bat
```

### ⚠️ onefile 模式（不推荐）

**特点**:
- 🐌 **启动慢** - 5-7秒（需解压到临时目录）
- 📦 单个 .exe 文件
- 💾 体积较小（~50MB）

**问题**:
- 每次启动都需要解压所有依赖到 `%TEMP%\_MEI*`
- 详见: [docs/STARTUP_PERFORMANCE_ANALYSIS.md](docs/STARTUP_PERFORMANCE_ANALYSIS.md)

---

## 手动构建

```cmd
python -m PyInstaller ^
    --name=WatermarkApp_PyQt6_v2.0 ^
    --onedir ^
    --windowed ^
    --icon=assets/watermark_app_icon.ico ^
    --add-data "assets;assets" ^
    --hidden-import=PyQt6 ^
    --hidden-import=PIL ^
    --hidden-import=numpy ^
    src/watermark_app_pyqt6_modular.py
```

---

## 关键参数

- `--onedir` - 📁 文件夹模式（快速启动）
- `--windowed` - 🪟 无控制台窗口
- `--icon` - 🎨 应用图标
- `--add-data` - 📦 打包资源文件（主题 SVG 等）
- `--hidden-import` - 🔍 包含隐藏依赖

---

## 输出结构

```
dist/
└── WatermarkApp_PyQt6_v2.0/
    ├── WatermarkApp_PyQt6_v2.0.exe  # 主程序
    ├── assets/                       # 主题资源
    │   └── ui/
    │       ├── genshin/             # 原神主题
    │       └── cyberpunk/           # 赛博朋克主题
    ├── PyQt6/                        # PyQt6 依赖
    ├── PIL/                          # Pillow 依赖
    ├── numpy/                        # NumPy 依赖
    └── ... (其他 DLL)
```

---

## 性能优化

### 启动速度对比

| 模式 | 启动时间 | 体积 | 推荐 |
|------|---------|------|------|
| onedir | **0.5-1秒** | ~200MB | ✅ |
| onefile | 5-7秒 | ~50MB | ❌ |

### 优化建议

1. **使用 onedir 模式** - 避免每次启动解压
2. **延迟加载** - 图层图片在使用时加载（已实现）
3. **字体缓存** - 系统字体扫描结果缓存（已实现）

详见: [docs/STARTUP_PERFORMANCE_ANALYSIS.md](docs/STARTUP_PERFORMANCE_ANALYSIS.md)

---

## 故障排除

### 构建失败

1. **检查 Python 版本**: `python --version` (需要 3.7+)
2. **安装依赖**: `pip install -r requirements_pyqt6.txt`
3. **清理缓存**: 删除 `build/` 和 `dist/` 目录

### 运行时错误

1. **缺少资源文件** - 检查 `assets/` 目录是否完整
2. **DLL 缺失** - 重新构建或安装 Visual C++ Redistributable

### ⚠️ Python DLL 加载失败（Unicode 路径问题）

**错误信息**:
```
Failed to load Python DLL 'E:\下载\_internal\python310.dll'.
LoadLibrary: 找不到指定的模块。
```

**原因**: 这是 PyInstaller 的已知问题。当应用程序路径包含非 ASCII 字符（如中文、日文、韩文）时，Windows 的 `LoadLibrary` 无法正确加载 Python DLL。

**解决方案**:

| 方案 | 操作 | 推荐度 |
|------|------|--------|
| **移动到 ASCII 路径** | 将整个程序文件夹移动到只包含英文的路径，如 `C:\WatermarkApp\` 或 `D:\Apps\` | ✅ 推荐 |
| **避免中文路径** | 不要放在「下载」「桌面」「文档」等中文名文件夹中 | ✅ 推荐 |
| **更新 PyInstaller** | `pip install --upgrade pyinstaller` (6.0+ 版本可能有改善) | 🔄 可选 |

**正确的路径示例**:
```
✅ C:\WatermarkApp\WatermarkApp_PyQt6_v2.1.exe
✅ D:\Tools\WatermarkApp\WatermarkApp_PyQt6_v2.1.exe
❌ E:\下载\WatermarkApp\WatermarkApp_PyQt6_v2.1.exe
❌ C:\Users\用户\Desktop\WatermarkApp\...
```

**参考**: [PyInstaller Issue #1224](https://github.com/pyinstaller/pyinstaller/issues/1224), [Issue #1295](https://github.com/pyinstaller/pyinstaller/issues/1295)

---

## 分发

将整个 `dist/WatermarkApp_PyQt6_v2.0/` 文件夹复制到目标电脑即可运行。

**无需安装 Python 或任何依赖！**

---

📖 **详细文档**:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构说明
- [docs/PYQT6_MODULAR_COMPLETION_GUIDE.md](docs/PYQT6_MODULAR_COMPLETION_GUIDE.md) - 模块化指南
