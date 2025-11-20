# 🚀 Multi-Layer Watermark App v1.5 - 快速开始

## 📦 新版本亮点

✨ **Multi-Layer Watermark App v1.5** 已发布！基于 v1.4 优化版开发，新增以下功能：

- 🎨 **多图层支持**: 可添加多个水印图层，自由叠加
- 🌈 **4种混合模式**: Normal, Overlay, Screen, Soft Light（完整 Photoshop 算法）
- 🎚️ **独立不透明度**: 每个图层单独控制透明度
- 📊 **图层管理**: 支持添加、编辑、删除、排序
- 🧠 **智能颜色**: 继承 v1.4 的智能反色算法
- 💾 **配置保存**: 图层设置自动保存，下次启动自动加载

## 🏃 快速启动

### Windows 用户
双击运行 `run_multilayer.bat`

或在命令行中：
```bash
python src\watermark_app_multilayer.py
```

### macOS/Linux 用户
在终端中运行：
```bash
./run_multilayer.sh
```

或：
```bash
python3 src/watermark_app_multilayer.py
```

## 📝 基本使用流程

### 1️⃣ 上传图片
- 点击 **"Upload Images"** 按钮
- 选择一张或多张待处理的图片

### 2️⃣ 添加水印图层
- 点击 **"+ Add Layer"** 按钮
- 选择水印图片
- 在弹出窗口中设置：
  - **混合模式**（Normal/Overlay/Screen/Soft Light）
  - **不透明度**（0-100%）
- 点击 **"Save"** 保存

### 3️⃣ 管理图层（可选）
- **编辑图层**: 选中图层 → 点击 "✎ Edit Layer"
- **删除图层**: 选中图层 → 点击 "× Remove"
- **调整顺序**: 选中图层 → 点击 "↑ Up" 或 "↓ Down"

### 4️⃣ 配置参数（可选）
- **Stretch watermark**: 是否拉伸水印适应图片
- **Smart color**: 是否启用智能颜色适应
- **Sensitivity**: 颜色相似度阈值（默认30）
- **Performance**: 性能模式（推荐 Balanced）

### 5️⃣ 选择保存位置
- 点击 **"Select Save Directory"**
- 选择输出文件夹

### 6️⃣ 应用水印
- 点击 **"🚀 Apply Multi-Layer Watermark"**
- 等待处理完成

## 🎨 混合模式使用建议

### Normal（正常）
适合：Logo、文字水印
```
特点：直接覆盖，效果最清晰
建议不透明度：80-100%
```

### Screen（滤色）
适合：光效、高光效果
```
特点：提亮图片，不会变暗
建议不透明度：30-60%
```

### Overlay（叠加）
适合：纹理、图案叠加
```
特点：增强对比度，保留底层细节
建议不透明度：30-70%
```

### Soft Light（柔光）
适合：柔和的艺术效果
```
特点：比 Overlay 更柔和自然
建议不透明度：40-80%
```

## 💡 实用技巧

### 技巧 1: Logo + 文字组合
```
图层1: logo.png (Normal, 100%)
图层2: copyright.png (Normal, 80%)
```

### 技巧 2: 光效叠加
```
图层1: watermark.png (Normal, 70%)
图层2: glow.png (Screen, 50%)
```

### 技巧 3: 复古效果
```
图层1: texture.png (Overlay, 40%)
图层2: vignette.png (Soft Light, 60%)
```

### 技巧 4: 多语言水印
```
图层1: watermark_cn.png (Normal, 100%)
图层2: watermark_en.png (Normal, 80%)
```

## 🔧 配置文件说明

配置自动保存在 `configs/multilayer_watermark_config.json`

包含内容：
- 上次使用的目录
- 智能颜色设置
- 性能模式选择
- **图层配置**（路径、不透明度、混合模式）

下次启动时会自动加载这些设置。

## 📚 详细文档

更多信息请查看：
- 📖 [完整使用指南](docs/MULTILAYER_GUIDE.md)
- 🧠 [智能算法说明](docs/SMART_WATERMARK_ALGORITHM.md)
- 📁 [项目结构说明](PROJECT_STRUCTURE.md)

## 🆚 版本对比

| 功能 | v1.4 Optimized | v1.5 Multi-Layer |
|------|---------------|------------------|
| 水印数量 | 1个 | **多个** ✨ |
| 混合模式 | 无 | **4种** ✨ |
| 图层管理 | 无 | **完整支持** ✨ |
| 智能颜色 | ✅ | ✅ |
| 性能优化 | ✅ | ✅ |

## ⚙️ 系统要求

- Python 3.7+
- 依赖库：
  - tkinter（GUI）
  - Pillow（图像处理）
  - NumPy（数值计算）

安装依赖：
```bash
pip install -r requirements.txt
```

## ❓ 常见问题

**Q: 图层顺序有什么影响？**
A: 从列表底部到顶部依次叠加。底层图层先应用，顶层最后应用。

**Q: 智能颜色对混合模式有影响吗？**
A: 有。智能颜色会在混合前调整水印颜色，可提高可见度。

**Q: 哪个性能模式最好？**
A: 推荐 Balanced。如果处理大量图片，可选 Speed Priority。

**Q: 配置会自动保存吗？**
A: 是的。所有图层设置和参数都会自动保存。

## 📞 获取帮助

如有问题，请查看：
- [详细使用指南](docs/MULTILAYER_GUIDE.md)
- [项目文档](docs/)

---

**Multi-Layer Watermark App v1.5** - 让你的水印更有创意！ 🎨✨
