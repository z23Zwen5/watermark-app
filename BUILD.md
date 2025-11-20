# 🔨 快速构建指南

## 一键构建

### Windows
```cmd
tools\build_multilayer.bat
```

### Linux/Mac
```bash
./tools/build_multilayer.sh
```

---

## 手动构建（带图标）

### Windows
```cmd
python -m PyInstaller --name=MultiLayerWatermark_v1.5 --onefile --windowed --icon=assets/watermark_app_icon.ico --hidden-import=numpy --hidden-import=PIL --hidden-import=PIL._tkinter_finder src/watermark_app_multilayer.py
```

### Linux/Mac
```bash
python3 -m PyInstaller --name=MultiLayerWatermark_v1.5 --onefile --windowed --icon=assets/watermark_app_icon.ico --hidden-import=numpy --hidden-import=PIL --hidden-import=PIL._tkinter_finder src/watermark_app_multilayer.py
```

**注意**: 配置文件会在程序首次运行时自动创建，不需要打包。

---

## 关键参数

- `--icon=assets/watermark_app_icon.ico` - **添加图标** ⭐
- `--onefile` - 单文件打包
- `--windowed` - 无控制台窗口
- `--hidden-import` - 包含隐藏的依赖模块

---

## 输出位置

```
dist/MultiLayerWatermark_v1.5.exe  # Windows
dist/MultiLayerWatermark_v1.5      # Linux/Mac
```

---

📖 **详细文档**: [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md)
