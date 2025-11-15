# 🎨 Multi-Layer Watermark App

> 专业的多图层水印应用 | 支持 Photoshop 混合模式 + 智能颜色适应

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](docs/VERSION_1.5_RELEASE_NOTES.md)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ 功能亮点

🎨 **多图层系统** - 支持无限制添加水印图层，自由组合
🌈 **混合模式** - 4种专业 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
🎚️ **精细控制** - 每层独立调整不透明度和混合效果
🧠 **智能适应** - 自动检测背景颜色并调整水印颜色
⚡ **高性能** - 三种性能模式，支持批量处理
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

### 3️⃣ 管理图层
- **编辑**: 选中图层 → `✎ Edit Layer`
- **删除**: 选中图层 → `× Remove`
- **排序**: `↑ Up` / `↓ Down`

### 4️⃣ 应用水印
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

### 📌 品牌水印
```
[1] logo.png (Normal, 100%)
[2] brandname.png (Normal, 80%)
```

### ✨ 光效水印
```
[1] watermark.png (Normal, 70%)
[2] glow.png (Screen, 50%)
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
| [开发总结](docs/DEVELOPMENT_SUMMARY_V1.5.md) | 技术实现细节 |
| [项目结构](docs/PROJECT_STRUCTURE.md) | 目录组织说明 |

---

## 🆚 版本历史

| 版本 | 主要功能 | 状态 |
|------|---------|------|
| **v1.5** | 多图层 + 混合模式 + 智能颜色 | ⭐ 当前版本 |
| v1.4 | 智能颜色 + 性能优化 | 可用 |
| v1.3 | 基础智能颜色 | 可用 |
| v1.2 | 基础水印功能 | 已归档 |

查看完整 [版本历史](docs/VERSION_HISTORY.md)

---

## 💻 系统要求

- **Python**: 3.7 或更高版本
- **内存**: 最低 2GB，推荐 4GB+
- **系统**: Windows 7+, macOS 10.12+, Linux

### 依赖库
```
Pillow >= 8.0.0
numpy >= 1.19.0
```

---

## 📂 项目结构

```
watermarkApp/
├── src/                    # 源代码
│   └── watermark_app_multilayer.py  # v1.5 主程序
├── configs/                # 配置文件
├── docs/                   # 完整文档
├── tests/                  # 测试文件
├── archive/                # 归档版本
├── run_multilayer.bat      # Windows 启动
├── run_multilayer.sh       # Linux/Mac 启动
└── README.md               # 本文档
```

---

## ⚡ 性能指标

测试环境: 1920x1080 图片, 2个图层

| 性能模式 | 处理时间 | 质量 | 适用场景 |
|---------|---------|------|---------|
| Quality | 3.5秒 | ⭐⭐⭐⭐⭐ | 精品输出 |
| Balanced | 2.0秒 | ⭐⭐⭐⭐ | 日常使用（推荐）|
| Speed | 1.2秒 | ⭐⭐⭐ | 批量处理 |

---

## 🎯 核心优势

✅ **专业级混合** - 完整 Photoshop 标准算法
✅ **多层叠加** - 无限创意可能
✅ **智能适应** - 自动颜色调整
✅ **简单易用** - 友好的图形界面
✅ **高效处理** - 批量处理支持
✅ **配置记忆** - 自动保存设置

---

## 📞 获取帮助

### 遇到问题？

1. 查看 [快速开始指南](docs/QUICK_START.md)
2. 阅读 [完整使用手册](docs/MULTILAYER_GUIDE.md)
3. 检查 [常见问题](docs/MULTILAYER_GUIDE.md#常见问题)

### 技术支持

- 📖 查看文档: [docs/](docs/)
- 🐛 报告问题: 提交 Issue
- 💡 功能建议: 提交 Feature Request

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

**Multi-Layer Watermark App v1.5** - 让每张图片都独一无二！

*现在就开始创作你的专属水印吧！* ✨

---

<p align="center">
  <strong>Made with ❤️ by WatermarkApp Team</strong>
</p>
