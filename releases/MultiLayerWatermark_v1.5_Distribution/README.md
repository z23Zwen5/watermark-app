# 🎨 Multi-Layer Watermark App v1.5 - 分发包

> 专业的多图层水印应用 | 支持 Photoshop 混合模式

---

## 📦 包内容

```
MultiLayerWatermark_v1.5_Distribution/
├── src/
│   └── watermark_app_multilayer.py    # 主程序源码
├── configs/
│   └── multilayer_watermark_config.json # 配置文件示例
├── docs/
│   ├── MULTILAYER_GUIDE.md            # 完整使用指南
│   ├── QUICK_START.md                  # 快速开始
│   ├── VERSION_1.5_RELEASE_NOTES.md   # 版本说明
│   ├── OPTIMIZATION_MULTILAYER.md     # 性能优化说明
│   └── PROJECT_STRUCTURE.md           # 项目结构
├── build/
│   └── MultiLayerWatermark_v1.5.spec  # PyInstaller 打包配置
├── assets/
│   └── watermark_app_icon.ico         # 应用图标
├── requirements.txt                    # Python 依赖
├── run_multilayer.bat                  # Windows 启动脚本
├── run_multilayer.sh                   # Linux/Mac 启动脚本
└── README.md                           # 本文档
```

---

## 🚀 快速开始

### 方式一：直接运行源码（推荐）

#### 1. 安装 Python
- 下载 Python 3.7 或更高版本: https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 运行程序

**Windows 用户**
```bash
run_multilayer.bat
```

**macOS/Linux 用户**
```bash
chmod +x run_multilayer.sh
./run_multilayer.sh
```

**或直接运行**
```bash
python src/watermark_app_multilayer.py
```

### 方式二：打包成 exe（Windows）

#### 1. 安装 PyInstaller
```bash
pip install pyinstaller
```

#### 2. 打包
```bash
pyinstaller build/MultiLayerWatermark_v1.5.spec --clean
```

#### 3. 运行
生成的 exe 文件在 `dist/` 目录下：
```
dist/MultiLayerWatermark_v1.5.exe
```

---

## ✨ 核心功能

### 🎨 多图层系统
- 支持添加多个水印图层
- 每层独立配置混合模式和不透明度
- 图层顺序可调整（数字越大越上层）

### 🌈 Photoshop 混合模式
- **Normal**: Logo、文字水印
- **Screen**: 光效、高光效果
- **Overlay**: 纹理叠加
- **Soft Light**: 柔和艺术效果

### 🎚️ 精细控制
- Blend Mode 下拉选择
- Opacity 数字输入（0-100）
- 实时生效，无需确认

### ⚡ 性能优化
- Alpha 通道预检查
- 自适应缩放质量
- 内存优化
- **速度提升 40-60%**

---

## 📖 使用流程

1. **Upload Images** - 上传待处理图片
2. **+ Add Layer** - 添加水印图层
3. 选中图层 → 设置 **Blend Mode** 和 **Opacity**
4. 可选：调整图层顺序（↑ Up / ↓ Down）
5. **Select Save Directory** - 选择输出目录
6. **🚀 Apply Multi-Layer Watermark** - 应用水印

---

## 💡 使用案例

### 案例 1: 品牌水印
```
[1] logo.png (normal, 100%)
[2] text.png (normal, 80%)
```

### 案例 2: 光效水印
```
[1] watermark.png (normal, 70%)
[2] glow.png (screen, 50%)
```

### 案例 3: 艺术效果
```
[1] texture.png (overlay, 40%)
[2] pattern.png (soft_light, 60%)
```

---

## 📚 详细文档

- [完整使用指南](docs/MULTILAYER_GUIDE.md)
- [快速开始](docs/QUICK_START.md)
- [版本说明](docs/VERSION_1.5_RELEASE_NOTES.md)
- [性能优化说明](docs/OPTIMIZATION_MULTILAYER.md)

---

## 💻 系统要求

- **Python**: 3.7 或更高版本
- **内存**: 最低 2GB，推荐 4GB+
- **系统**: Windows 7+, macOS 10.12+, Linux

### 依赖库
```
Pillow >= 8.0.0
numpy >= 1.20.0
```

---

## ⚡ 性能指标

| 场景 | 处理时间 |
|------|---------|
| 1920x1080 + 2层 | ~160ms |
| 2K + 2层 | ~290ms |
| 批量100张 | ~16秒 |

---

## 🔧 常见问题

### Q: 如何打包成独立 exe？
A: 运行 `pyinstaller build/MultiLayerWatermark_v1.5.spec --clean`

### Q: 图层顺序如何理解？
A: 数字越大的图层越在上面，会覆盖下层

### Q: 输出格式是什么？
A: JPG 格式，质量 95%，保持高画质

### Q: 支持哪些图片格式？
A: 输入支持 JPG, PNG；输出为 JPG

---

## 📝 更新日志

### v1.5.0 (2025-10-23)
- ✨ 新增多图层水印系统
- 🌈 新增 4 种 Photoshop 混合模式
- 🎚️ 内联编辑界面（类似 Photoshop）
- ⚡ 性能优化，速度提升 40-60%
- 💾 图层配置自动保存

---

## 🙏 致谢

- [Pillow](https://python-pillow.org/) - 图像处理
- [NumPy](https://numpy.org/) - 数值计算
- [PyInstaller](https://pyinstaller.org/) - 打包工具

---

## 📞 获取帮助

如有问题，请查看：
- [docs/MULTILAYER_GUIDE.md](docs/MULTILAYER_GUIDE.md)
- [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 🎨 开始使用

**Multi-Layer Watermark App v1.5** - 让每张图片都独一无二！

*现在就开始创作你的专属水印吧！* ✨

---

<p align="center">
  <strong>Version: 1.5.0 | Release Date: 2025-10-23</strong>
</p>
