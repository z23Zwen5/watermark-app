# 构建指南 - Build Guide

**版本**: v1.5
**日期**: 2025-10-23

---

## 📦 快速构建

### Windows 用户

```cmd
cd tools
build_multilayer.bat
```

### Linux/Mac 用户

```bash
cd tools
./build_multilayer.sh
```

---

## 🔨 手动构建（带图标）

### 前置要求

1. **Python 3.7+** - 已安装并在 PATH 中
2. **PyInstaller** - 自动安装或手动安装：
   ```bash
   pip install pyinstaller
   ```
3. **项目依赖** - 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 构建命令

#### Windows

```cmd
cd WatermarkApp/watermarkApp

python -m PyInstaller ^
    --name=MultiLayerWatermark_v1.5 ^
    --onefile ^
    --windowed ^
    --clean ^
    --icon=assets/watermark_app_icon.ico ^
    --hidden-import=numpy ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=tkinter ^
    --hidden-import=json ^
    src/watermark_app_multilayer.py
```

**注意**:
- 不需要打包 `configs` 目录，配置文件会在程序首次运行时自动创建
- 如果需要预设配置，可以手动复制 `configs` 目录到可执行文件所在目录

#### Linux/Mac (Bash)

```bash
cd WatermarkApp/watermarkApp

python3 -m PyInstaller \
    --name=MultiLayerWatermark_v1.5 \
    --onefile \
    --windowed \
    --clean \
    --icon=assets/watermark_app_icon.ico \
    --hidden-import=numpy \
    --hidden-import=PIL \
    --hidden-import=PIL._tkinter_finder \
    --hidden-import=tkinter \
    --hidden-import=json \
    src/watermark_app_multilayer.py
```

**注意**:
- 不需要打包 `configs` 目录，配置文件会在程序首次运行时自动创建
- 如果需要预设配置，可以手动复制 `configs` 目录到可执行文件所在目录

---

## 🎯 PyInstaller 参数详解

### 基本参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--name` | 可执行文件名称 | `--name=MultiLayerWatermark_v1.5` |
| `--onefile` | 打包为单个文件 | （无值） |
| `--windowed` | 不显示控制台窗口（GUI 应用） | （无值） |
| `--clean` | 清理临时文件 | （无值） |

### 图标参数 ⭐

| 参数 | 说明 | 示例 |
|------|------|------|
| `--icon` | 设置可执行文件图标 | `--icon=assets/watermark_app_icon.ico` |

**重要提示**：
- ✅ Windows: 使用 `.ico` 格式（支持多尺寸）
- ⚠️ Mac: 使用 `.icns` 格式
- ⚠️ Linux: 图标参数在 Linux 上无效（需要桌面文件配置）

### 数据和依赖参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--add-data` | 添加数据文件/目录 | `--add-data="configs;configs"` (Windows)<br>`--add-data="configs:configs"` (Linux/Mac) |
| `--hidden-import` | 强制导入隐藏模块 | `--hidden-import=numpy` |

**数据文件格式**：
- Windows: `源路径;目标路径` （分号）
- Linux/Mac: `源路径:目标路径` （冒号）

---

## 🖼️ 图标文件要求

### Windows (.ico)

- **格式**: ICO
- **推荐尺寸**: 包含多个尺寸（16x16, 32x32, 48x48, 64x64, 128x128, 256x256）
- **位置**: `assets/watermark_app_icon.ico`

### 创建 ICO 文件

#### 方法 1: 在线工具
- 访问 [ICO Convert](https://icoconvert.com/)
- 上传 PNG/JPG 图片
- 选择多尺寸输出
- 下载 ICO 文件

#### 方法 2: Python 脚本

```python
from PIL import Image

# 打开原图
img = Image.open('watermark_icon.png')

# 创建多尺寸 ICO
img.save('watermark_app_icon.ico', format='ICO',
         sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
```

#### 方法 3: ImageMagick

```bash
convert watermark_icon.png -define icon:auto-resize=256,128,64,48,32,16 watermark_app_icon.ico
```

---

## 🐛 常见问题

### 问题 1: 图标不显示

**原因**: 图标文件路径错误或格式不正确

**解决方案**:
1. 检查图标文件是否存在：
   ```bash
   ls -la assets/watermark_app_icon.ico
   ```
2. 确保使用相对路径或绝对路径：
   ```bash
   --icon=assets/watermark_app_icon.ico  # 相对路径
   --icon=/full/path/to/assets/watermark_app_icon.ico  # 绝对路径
   ```
3. 确保 ICO 文件包含多种尺寸：
   ```bash
   file assets/watermark_app_icon.ico
   ```

### 问题 2: 找不到模块

**错误信息**:
```
ModuleNotFoundError: No module named 'numpy'
```

**解决方案**:
```bash
# 添加隐藏导入
--hidden-import=numpy
--hidden-import=PIL
--hidden-import=tkinter
```

### 问题 3: tkinter 找不到

**错误信息**:
```
ModuleNotFoundError: No module named '_tkinter'
```

**解决方案**:
```bash
# 添加特殊导入
--hidden-import=PIL._tkinter_finder
```

### 问题 4: 配置文件找不到

**错误信息**:
```
FileNotFoundError: configs/multilayer_watermark_config.json
```

**解决方案**:
```bash
# 添加数据文件
--add-data="configs;configs"  # Windows
--add-data="configs:configs"  # Linux/Mac
```

---

## 📊 构建输出

### 目录结构

```
watermarkApp/
├── build/                          # 构建临时文件
│   ├── temp/                       # 临时工作目录
│   └── MultiLayerWatermark_v1.5.spec  # PyInstaller 配置
│
├── dist/                           # 输出目录
│   └── MultiLayerWatermark_v1.5.exe   # 可执行文件 (Windows)
│   └── MultiLayerWatermark_v1.5       # 可执行文件 (Linux/Mac)
│
└── ...
```

### 文件大小

- **Windows**: 约 20-40 MB（包含所有依赖）
- **Linux**: 约 20-35 MB
- **Mac**: 约 25-45 MB

---

## 🎯 高级选项

### 1. 添加版本信息（Windows）

创建 `version.txt`:

```ini
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 5, 0, 0),
    prodvers=(1, 5, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'WatermarkApp Team'),
            StringStruct(u'FileDescription', u'Multi-Layer Watermark Application'),
            StringStruct(u'FileVersion', u'1.5.0.0'),
            StringStruct(u'InternalName', u'MultiLayerWatermark'),
            StringStruct(u'LegalCopyright', u'Copyright 2025'),
            StringStruct(u'OriginalFilename', u'MultiLayerWatermark_v1.5.exe'),
            StringStruct(u'ProductName', u'Multi-Layer Watermark App'),
            StringStruct(u'ProductVersion', u'1.5.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

构建时添加：
```bash
--version-file=version.txt
```

### 2. 优化文件大小

```bash
# 使用 UPX 压缩
--upx-dir=/path/to/upx

# 排除不需要的模块
--exclude-module=matplotlib
--exclude-module=scipy
```

### 3. 调试模式

```bash
# 显示控制台输出（调试用）
--console

# 启用调试日志
--debug=all
```

---

## ✅ 验证构建

### 1. 检查文件

```bash
# Windows
dir dist\MultiLayerWatermark_v1.5.exe

# Linux/Mac
ls -lh dist/MultiLayerWatermark_v1.5
```

### 2. 测试运行

```bash
# Windows
dist\MultiLayerWatermark_v1.5.exe

# Linux/Mac
./dist/MultiLayerWatermark_v1.5
```

### 3. 检查图标

- **Windows**: 右键点击可执行文件 → 属性 → 查看图标
- **Mac**: 在 Finder 中查看文件图标
- **Linux**: 需要配置桌面文件

---

## 🚀 发布清单

构建完成后，创建发布包：

1. ✅ 复制可执行文件
2. ✅ 复制 `configs/` 目录（示例配置）
3. ✅ 复制 `README.md`
4. ✅ 复制 `docs/` 目录（可选）
5. ✅ 创建发布说明

```bash
# 创建发布包
mkdir -p releases/MultiLayerWatermark_v1.5_Distribution
cp dist/MultiLayerWatermark_v1.5.exe releases/MultiLayerWatermark_v1.5_Distribution/
cp -r configs releases/MultiLayerWatermark_v1.5_Distribution/
cp README.md releases/MultiLayerWatermark_v1.5_Distribution/

# 打包
cd releases
tar -czvf MultiLayerWatermark_v1.5_Distribution.tar.gz MultiLayerWatermark_v1.5_Distribution/
```

---

## 📚 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/en/stable/)
- [PyInstaller 命令选项](https://pyinstaller.org/en/stable/usage.html)
- [Windows ICO 格式](https://en.wikipedia.org/wiki/ICO_(file_format))

---

**最后更新**: 2025-10-23
**维护者**: WatermarkApp Team
