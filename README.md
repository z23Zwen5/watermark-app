# 🎨 Multi-Layer Watermark App

> 专业多图层水印应用 | PyQt6 模块化架构 | 多主题支持

[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](CLAUDE.md)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 v2.1 新特性

### 📐 输出缩放功能 (NEW!)
- **等比缩放** - 输出图片自动缩放到指定高度
- **可调节** - 高度范围 256-4096 px，默认 1024 px
- **可开关** - 不需要时可关闭，保持原始尺寸
- **高质量** - 使用 LANCZOS 算法保证缩放质量

### 🎨 多主题支持
- **Genshin Impact** - 温暖金色调，优雅原神风格
- **Cyberpunk 2077** - 霓虹赛博朋克，未来科技感
- 运行时一键切换主题

### 🏗️ 模块化架构
- 完全重构的 UI 组件系统
- 清晰的代码结构，易于维护和扩展
- 核心功能与 UI 完全解耦

### ⚡ 性能优化
- **快速启动**: onedir 模式，<1秒启动
- 延迟加载图层图片
- 系统字体扫描缓存

---

## ✨ 核心功能

🎨 **多图层系统** - 支持无限制添加水印图层，自由组合
🌈 **混合模式** - 4种专业 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
👁️ **图层可见性** - 一键隐藏/显示图层（类似 Photoshop）
🎚️ **精细控制** - 每层独立调整不透明度和混合效果
📐 **输出缩放** - 等比缩放输出图片到指定高度（可选）
🎭 **多主题** - Genshin Impact / Cyberpunk 2077 主题
💾 **自动保存** - 图层配置自动保存，下次启动恢复
⚡ **高性能** - 优化算法，快速处理大图片

---

## 🚀 快速开始

### 方式一：运行源码

```bash
# 安装依赖
pip install -r requirements_pyqt6.txt

# 启动应用
python src/watermark_app_pyqt6_modular.py
```

或使用快捷脚本：
```cmd
run_pyqt6.bat        # Windows
```

### 方式二：构建可执行文件

```cmd
# 一键构建
tools\build_pyqt6_modular.bat

# 运行生成的 exe
dist\WatermarkApp_PyQt6_v2.0\WatermarkApp_PyQt6_v2.0.exe
```

详见: [BUILD.md](BUILD.md)

---

## 📖 使用指南

### 1️⃣ 上传图片
点击 `📂 Upload Images` 选择待处理的图片

### 2️⃣ 添加水印图层
- 点击 `➕ Add Layer` 选择水印
- 设置**混合模式**（Normal/Overlay/Screen/Soft Light）
- 调整**不透明度**（0-100%）
- 切换图层可见性 👁️

### 3️⃣ 应用水印
点击 `🎨 Apply Watermark` 批量处理图片

### 4️⃣ 切换主题 🎨
在设置面板选择主题：
- Genshin Impact（默认）
- Cyberpunk 2077

---

## 📂 项目结构

```
watermarkApp/
├── src/
│   ├── watermark_app_pyqt6_modular.py  # 主入口
│   ├── watermark_core.py               # 核心水印引擎
│   └── ui/                              # UI 模块化组件
│       ├── main_window.py               # 主窗口
│       ├── components/                  # UI 组件
│       │   ├── title_bar.py            # 自定义标题栏
│       │   └── message_box.py          # 消息框
│       ├── panels/                      # 功能面板
│       │   ├── upload_panel.py         # 上传面板
│       │   ├── layer_panel.py          # 图层面板
│       │   ├── output_panel.py         # 输出面板
│       │   └── settings_panel.py       # 设置面板
│       └── styles/                      # 主题系统
│           ├── theme_base.py           # 主题基类
│           ├── theme_genshin.py        # 原神主题
│           └── theme_cyberpunk.py      # 赛博朋克主题
├── assets/
│   └── ui/
│       ├── genshin/                     # 原神主题资源
│       └── cyberpunk/                   # 赛博朋克主题资源
├── configs/
│   └── multilayer_watermark_config.json # 配置文件
├── tools/
│   └── build_pyqt6_modular.bat         # 构建脚本
└── docs/
    ├── ARCHITECTURE.md                  # 架构文档
    ├── PYQT6_MODULAR_COMPLETION_GUIDE.md
    ├── STARTUP_PERFORMANCE_ANALYSIS.md
    └── THEME_SWITCHING_GUIDE.md
```

---

## 🎨 主题预览

### Genshin Impact 主题
- 🌟 温暖金色调 (#D3BC8E)
- 📜 米黄色背景 (#ECE5D8)
- 🎯 优雅按钮渐变

### Cyberpunk 2077 主题
- ⚡ 霓虹青色 (#00F0FF)
- 🔮 洋红色点缀 (#FF2A6D)
- 🌃 深色未来感背景

---

## 🛠️ 技术栈

- **Python 3.7+**
- **PyQt6** - 现代化 GUI 框架
- **Pillow** - 图像处理
- **NumPy** - 高性能数值计算
- **PyInstaller** - 打包为可执行文件

---

## 📊 性能对比

### 启动速度

| 构建模式 | 启动时间 | 体积 |
|----------|---------|------|
| **onedir** ✅ | **0.5-1秒** | ~200MB |
| onefile | 5-7秒 | ~50MB |

推荐使用 onedir 模式获得最佳启动体验！

---

## 📚 文档

- [BUILD.md](BUILD.md) - 构建指南
- [CLAUDE.md](CLAUDE.md) - AI 上下文文档
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构说明
- [docs/PYQT6_MODULAR_COMPLETION_GUIDE.md](docs/PYQT6_MODULAR_COMPLETION_GUIDE.md) - 模块化完整指南
- [docs/STARTUP_PERFORMANCE_ANALYSIS.md](docs/STARTUP_PERFORMANCE_ANALYSIS.md) - 性能分析
- [docs/THEME_SWITCHING_GUIDE.md](docs/THEME_SWITCHING_GUIDE.md) - 主题切换指南

---

## 📜 历史版本

### v2.1 (2025-01) - 输出缩放功能
- 📐 新增输出缩放功能（等比缩放到指定高度）
- 🔧 修复图层面板索引越界 bug
- 🎨 UI 细节优化

### v2.0 (2025-11) - PyQt6 模块化重构
- 🏗️ 完全模块化架构
- 🎨 多主题支持（Genshin/Cyberpunk）
- ⚡ 性能优化（<1秒启动）
- 🎯 UI/核心分离

### v1.6.2 (2025-06) - Tkinter 版本
- 👁️ 图层可见性切换
- 🎨 系统字体选择
- 📏 百分比字体大小
- 🔤 文本标注模块

详见: [versions/](versions/) 目录

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 自由使用、修改和分发

---

## 🎓 开发指南

### 添加新主题

1. 在 `src/ui/styles/` 创建新主题类（继承 `Theme`）
2. 在 `assets/ui/` 创建主题资源目录
3. 在 `ThemeManager` 中注册主题

详见: [docs/THEME_SWITCHING_GUIDE.md](docs/THEME_SWITCHING_GUIDE.md)

### 添加新功能面板

1. 在 `src/ui/panels/` 创建面板类
2. 在 `main_window.py` 中添加到布局
3. 使用 `ThemeManager.current_theme()` 获取主题样式

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
