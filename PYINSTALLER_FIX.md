# PyInstaller 资源路径修复说明

## 🐛 问题

PyInstaller 打包后，SVG 图标无法加载。

## 🔍 原因

PyInstaller 的 `onedir` 模式会将资源文件放在 `_internal` 子目录下，具体路径为：
```
dist/WatermarkApp_PyQt6_v2.0/
├── WatermarkApp_PyQt6_v2.0.exe
└── _internal/
    ├── assets/
    │   └── ui/
    │       ├── genshin/
    │       │   ├── arrow.svg
    │       │   └── arrow_hover.svg
    │       └── cyberpunk/
    │           ├── arrow.svg
    │           └── arrow_hover.svg
    └── ... (其他依赖)
```

但代码中使用的路径计算方式无法正确定位到 `_internal` 目录。

## ✅ 解决方案

### 1. 修复 `theme_base.py` 中的 `get_asset_path` 方法

```python
def get_asset_path(self, filename: str) -> str:
    """获取主题资源文件路径"""
    import sys

    # PyInstaller 打包后的路径处理
    if getattr(sys, 'frozen', False):
        # 运行在打包后的 exe 中
        base_path = sys._MEIPASS
    else:
        # 运行在开发环境中
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

    assets_dir = os.path.join(base_path, "assets", "ui", self.name)
    return os.path.join(assets_dir, filename).replace("\\", "/")
```

### 2. 修复 `genshin_style.py` 中的 `get_asset_path` 函数

```python
def get_asset_path(filename):
    """获取资源文件路径"""
    import sys

    # PyInstaller 打包后的路径处理
    if getattr(sys, 'frozen', False):
        # 运行在打包后的 exe 中
        base_path = sys._MEIPASS
    else:
        # 运行在开发环境中
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

    assets_dir = os.path.join(base_path, "assets", "ui")
    return os.path.join(assets_dir, filename).replace("\\", "/")
```

## 🔑 关键概念

### `sys.frozen`
- PyInstaller 打包后，`sys.frozen` 属性为 `True`
- 开发环境中，这个属性不存在（或为 `False`）

### `sys._MEIPASS`
- PyInstaller 打包后的临时解压目录
- 在 `onedir` 模式下，指向 `_internal` 目录
- 所有通过 `--add-data` 添加的资源都在这个目录下

## 📝 修改的文件

1. `src/ui/styles/theme_base.py` - 第 165-179 行
2. `src/ui/styles/genshin_style.py` - 第 38-52 行

## ✅ 验证

### 开发环境
```bash
python src/watermark_app_pyqt6_modular.py
```
应该正常加载 SVG 图标

### 打包后
```bash
# 重新构建
tools\build_pyqt6_modular.bat

# 运行
dist\WatermarkApp_PyQt6_v2.0\WatermarkApp_PyQt6_v2.0.exe
```
应该正常加载 SVG 图标

## 📚 参考

- [PyInstaller 文档 - Runtime Information](https://pyinstaller.org/en/stable/runtime-information.html)
- [PyInstaller 文档 - Adding Data Files](https://pyinstaller.org/en/stable/spec-files.html#adding-data-files)
