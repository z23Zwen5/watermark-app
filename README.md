# 🎨 Multi-Layer Watermark App

> 专业的多图层水印应用 | 支持 Photoshop 混合模式 + 文本标注

[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](docs/VERSION_1.5_RELEASE_NOTES.md)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ 功能亮点

🎨 **多图层系统** - 支持无限制添加水印图层，自由组合
🌈 **混合模式** - 4种专业 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
🎚️ **精细控制** - 每层独立调整不透明度和混合效果
🔤 **文本标注** - 自动添加序号或文件名，智能对比色
⚡ **高性能** - 优化算法，快速处理大图片
💾 **自动保存** - 图层配置自动保存，下次启动恢复

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

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

---

## 📖 使用流程

### 1️⃣ 上传图片
点击 `Upload Images` 选择待处理的图片

### 2️⃣ 添加水印图层
- 点击 `+ Add Layer` 选择水印
- 设置**混合模式**（Normal/Overlay/Screen/Soft Light）
- 调整**不透明度**（0-100%）

### 3️⃣ 文本标注（可选）✨ NEW
- 勾选 `Enable text label`
- 选择标注类型：
  - **Number**: 显示序号（1, 2, 3...）
  - **Filename**: 显示文件名
- 标注自动显示在图片右上角
- 智能对比色：深色背景显示白字，浅色背景显示黑字

### 4️⃣ 管理图层
- **编辑**: 选中图层，调整属性
- **删除**: 选中图层 → `× Remove`
- **排序**: `↑ Up` / `↓ Down`

### 5️⃣ 应用水印
点击 `🚀 Apply Multi-Layer Watermark` 完成处理

---

## 🎨 混合模式说明

| 模式 | 用途 | 推荐不透明度 |
|------|------|-------------|
| **Normal** | Logo、文字水印 | 80-100% |
| **Screen** | 光效、高光效果 | 30-60% |
| **Overlay** | 纹理、图案叠加 | 30-70% |
| **Soft Light** | 柔和艺术效果 | 40-80% |

---

## 💡 实用案例

### 📌 品牌水印 + 序号
```
图层设置:
[1] logo.png (Normal, 100%)
[2] brandname.png (Normal, 80%)

文本标注: 启用，类型=Number
结果: 每张图右上角显示 1, 2, 3...
```

### ✨ 光效水印 + 文件名
```
图层设置:
[1] watermark.png (Normal, 70%)
[2] glow.png (Screen, 50%)

文本标注: 启用，类型=Filename
结果: 每张图右上角显示文件名
```

### 🎭 复古效果
```
[1] texture.png (Overlay, 40%)
[2] vignette.png (Soft Light, 60%)
```

### 🌐 多语言水印
```
[1] watermark_cn.png (Normal, 100%)
[2] watermark_en.png (Normal, 80%)
```

---

## 📚 详细文档

| 文档 | 说明 |
|------|------|
| [快速开始](docs/QUICK_START.md) | 5分钟上手指南 |
| [完整手册](docs/MULTILAYER_GUIDE.md) | 详细功能说明 |
| [发布说明](docs/VERSION_1.5_RELEASE_NOTES.md) | 版本更新内容 |
| [性能分析](performance_analysis.md) | 性能瓶颈详解 ✨ NEW |
| [开发总结](docs/DEVELOPMENT_SUMMARY_V1.5.md) | 技术实现细节 |
| [项目结构](docs/PROJECT_STRUCTURE.md) | 目录组织说明 |

---

## 🆚 版本历史

| 版本 | 主要功能 | 状态 |
|------|---------|------|
| **v1.6** | 多图层 + 文本标注 + 性能优化 | ⭐ 当前版本 |
| v1.5 | 多图层 + 混合模式 | 可用 |
| v1.4 | 智能颜色 + 性能优化 | 已废弃 |
| v1.3 | 基础智能颜色 | 已废弃 |
| v1.2 | 基础水印功能 | 已归档 |

### v1.6 新特性 ✨

- 🔤 **文本标注模块**: 独立的 `text_label_module.py`
- ⚡ **性能优化**: BILINEAR 缩放，提速 1.6-1.9x
- 📊 **性能分析**: 详细的瓶颈分析和优化建议
- 🧹 **代码重构**: 模块化设计，易于扩展

查看完整 [版本历史](docs/VERSION_HISTORY.md)

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

## 📂 项目结构

```
watermarkApp/
├── src/                              # 源代码
│   ├── watermark_app_multilayer.py   # v1.6 主程序
│   └── text_label_module.py          # 文本标注模块 ✨ NEW
├── configs/                          # 配置文件
├── docs/                             # 完整文档
├── tests/                            # 测试文件
├── archive/                          # 归档版本
├── performance_analysis.md           # 性能分析 ✨ NEW
├── test_performance.py               # 性能测试 ✨ NEW
├── run_multilayer.bat                # Windows 启动
├── run_multilayer.sh                 # Linux/Mac 启动
└── README.md                         # 本文档
```

---

## ⚡ 性能指标

### v1.6 处理速度（基于实测）

测试条件: 3个水印图层，BILINEAR 缩放

| 图片尺寸 | v1.5 时间 | v1.6 时间 | 提速 |
|---------|----------|----------|------|
| 1920×1080 (2.1M) | ~0.7秒 | ~0.5秒 | **30%** ⬆️ |
| 2560×1440 (3.7M) | ~1.3秒 | ~1.0秒 | **23%** ⬆️ |
| 3840×2160 (8.3M) | ~3.4秒 | ~2.6秒 | **24%** ⬆️ |

💡 **优化亮点**:
- 使用 BILINEAR 替代 LANCZOS 缩放算法
- 质量几乎无差别，速度提升显著
- 详见 [性能分析文档](performance_analysis.md)

---

## 🎯 核心优势

✅ **专业级混合** - 完整 Photoshop 标准算法
✅ **多层叠加** - 无限创意可能
✅ **文本标注** - 序号/文件名自动添加 ✨ NEW
✅ **简单易用** - 友好的图形界面
✅ **高效处理** - 批量处理支持
✅ **配置记忆** - 自动保存设置

---

## 📞 获取帮助

### 遇到问题？

1. 查看 [快速开始指南](docs/QUICK_START.md)
2. 阅读 [完整使用手册](docs/MULTILAYER_GUIDE.md)
3. 检查 [常见问题](docs/MULTILAYER_GUIDE.md#常见问题)
4. 查看 [性能分析](performance_analysis.md)（新增）

### 技术支持

- 📖 查看文档: [docs/](docs/)
- 🐛 报告问题: 提交 Issue
- 💡 功能建议: 提交 Feature Request

---

## 🔬 性能测试

运行性能测试脚本查看不同分辨率的处理时间：

```bash
python test_performance.py
```

测试内容：
- 内存分配时间
- 混合模式计算时间
- 图片缩放对比（LANCZOS vs BILINEAR）
- 完整流程模拟

---

## 🙏 致谢

感谢以下开源项目:
- [Pillow](https://python-pillow.org/) - 强大的图像处理库
- [NumPy](https://numpy.org/) - 高性能科学计算库

感谢所有用户的支持和反馈！

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

## 🎨 开始创作

**Multi-Layer Watermark App v1.6** - 让每张图片都独一无二！

*现在就开始创作你的专属水印吧！* ✨

---

<p align="center">
  <strong>Made with ❤️ by WatermarkApp Team</strong>
</p>
