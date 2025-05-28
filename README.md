# 🚀 水印应用 WatermarkApp

一个高性能的批量图片水印添加工具，支持透明水印、批量处理和**智能配置记忆**。

## ⚡ 性能亮点

- **30倍性能提升** - v1.1优化版相比v1.0提升30倍以上
- **96.7%时间节省** - 从分钟级处理降至秒级
- **智能配置记忆** - v1.2自动记住所有设置和文件路径
- **自动文件加载** - 启动即恢复上次工作状态
- **并行处理** - 充分利用多核CPU
- **智能缓存** - 避免重复计算

## 📁 项目结构

```
watermarkApp/
├── src/                          # 源代码
│   ├── watermark_app.py         # v1.0 基础版本
│   └── watermark_app_optimized.py # v1.1/v1.2 优化版本
├── docs/                         # 文档
│   ├── VERSION_HISTORY.md       # 版本历史
│   ├── CONFIG_FEATURES.md       # 配置功能说明
│   ├── OPTIMIZATION_GUIDE.md    # 优化指南
│   ├── PERFORMANCE_SUMMARY.md   # 性能报告
│   └── USAGE_EXAMPLE.md         # 使用示例
├── releases/                     # 发布版本
│   ├── WatermarkApp_v1.1_优化版_分发包.zip
│   ├── WatermarkApp_v1.1_Distribution/
│   └── 分发包说明.txt
├── assets/                       # 资源文件
│   └── watermark_app_icon.ico   # 应用图标
├── build/                        # 构建文件
│   ├── *.spec                   # PyInstaller配置
│   └── ...
├── dist/                         # 编译输出
│   └── *.exe                    # 可执行文件
├── requirements.txt              # 依赖包
├── .gitignore                   # Git忽略文件
└── README.md                    # 项目说明
```

## 🚀 快速开始

### 方式一：使用预编译版本（推荐）
1. 下载 `releases/WatermarkApp_v1.1_优化版_分发包.zip`
2. 解压并运行 `WatermarkApp_v1.1_Optimized.exe`

### 方式二：从源代码运行
```bash
# 安装依赖
pip install -r requirements.txt

# 运行v1.2配置增强版（推荐）
python src/watermark_app_optimized.py

# 或运行基础版本
python src/watermark_app.py

# 或使用批处理文件（Windows）
run_optimized.bat  # 优化版本
run_basic.bat      # 基础版本
```

## 🆕 v1.2 配置增强功能

### 🧠 智能记忆系统
- **完整设置记忆** - 透明度、拉伸选项、并行处理等
- **文件路径记忆** - 分别记住水印、图片、保存目录
- **自动文件加载** - 启动时自动加载上次使用的文件
- **实时保存** - 每次更改立即保存配置

### 🎯 用户体验提升
```
第一次使用:
选择文件 → 调整设置 → 处理图片 → 自动保存配置

第二次使用:
启动应用 → 自动恢复所有设置 → 直接处理 ✨
```

### 📊 配置功能对比

| 功能 | v1.0/v1.1 | v1.2 配置增强版 |
|------|-----------|----------------|
| 路径记忆 | 基础支持 | **完整支持** |
| 设置记忆 | ❌ | **✅ 全部记忆** |
| 文件自动加载 | ❌ | **✅ 智能加载** |
| 实时保存 | ❌ | **✅ 即时保存** |

## 📊 版本对比

| 特性 | v1.0 基础版 | v1.1 优化版 | v1.2 配置增强版 |
|------|------------|------------|----------------|
| 性能 | 逐像素处理 | numpy向量化 | numpy向量化 |
| 并发 | 单线程 | 多线程并行 | 多线程并行 |
| 缓存 | 无缓存 | 智能缓存 | 智能缓存 |
| UI | 处理时冻结 | 异步响应 | 异步响应 |
| 进度 | 无反馈 | 实时进度条 | 实时进度条 |
| **配置记忆** | **基础** | **基础** | **🆕 完整智能** |
| **文件记忆** | **❌** | **❌** | **🆕 自动加载** |

## 🎯 主要功能

- ✅ 批量添加透明水印
- ✅ 水印透明度可调 (0-100%)
- ✅ 水印拉伸选项
- ✅ **智能配置记忆** 🆕
- ✅ **自动文件加载** 🆕
- ✅ 并行处理支持
- ✅ 实时进度显示
- ✅ 现代化UI设计

## 📚 文档

- [配置功能说明](docs/CONFIG_FEATURES.md) - **🆕 详细的配置记忆功能介绍**
- [版本历史](docs/VERSION_HISTORY.md) - 完整版本更新记录
- [优化指南](docs/OPTIMIZATION_GUIDE.md) - 性能优化使用指南
- [性能报告](docs/PERFORMANCE_SUMMARY.md) - 详细性能测试结果
- [使用示例](docs/USAGE_EXAMPLE.md) - 详细使用教程

## 🔧 开发

### 打包为exe
```bash
# v1.2配置增强版
pyinstaller --onefile --windowed --icon=assets/watermark_app_icon.ico src/watermark_app_optimized.py

# 基础版本
pyinstaller --onefile --windowed --icon=assets/watermark_app_icon.ico src/watermark_app.py
```

## 📈 性能数据

| 测试场景 | v1.0 耗时 | v1.1/v1.2 耗时 | 性能提升 |
|---------|----------|----------------|----------|
| 3张高清图片 | 8.871秒 | 0.289秒 | **30.67倍** |
| 5张标清图片 | 6.405秒 | 0.226秒 | **28.34倍** |
| 2张4K图片 | 24.876秒 | 0.808秒 | **30.79倍** |

## 🎉 技术栈

- **Python 3.7+** - 主要开发语言
- **tkinter** - GUI框架
- **Pillow (PIL)** - 图像处理
- **numpy** - 数值计算优化
- **PyInstaller** - 打包工具

## 🎯 推荐使用

- **🏆 日常使用**: v1.2 配置增强版 - 最佳用户体验
- **⚡ 高性能需求**: v1.1/v1.2 优化版 - 30倍性能提升  
- **💧 简单需求**: v1.0 基础版 - 轻量级选择

---

**享受30倍性能提升 + 智能配置记忆的水印处理体验！** ⚡🧠
