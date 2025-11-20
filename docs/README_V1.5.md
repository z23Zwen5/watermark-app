# 🎨 Multi-Layer Watermark App v1.5

> 基于 v1.4 优化版开发的专业多图层水印应用
> 支持 Photoshop 混合模式 + 智能颜色适应

---

## 📸 功能概览

```
┌─────────────────────────────────────────────┐
│  🖼️  原始图片                               │
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  🎨 图层1: Logo (Normal, 100%)      │  │
│  │  🌈 图层2: Text (Overlay, 80%)      │  │
│  │  ✨ 图层3: Glow (Screen, 50%)       │  │
│  └──────────────────────────────────────┘  │
│           ↓                                  │
│  🧠 智能颜色适应 (可选)                     │
│           ↓                                  │
│  💾 输出: 多层叠加水印图片                  │
└─────────────────────────────────────────────┘
```

## ✨ 核心特性

### 🎨 多图层系统
- ✅ 无限制添加水印图层
- ✅ 每层独立配置
- ✅ 自由调整图层顺序
- ✅ 实时列表管理

### 🌈 Photoshop 混合模式
- **Normal**: 正常覆盖（Logo、文字）
- **Screen**: 滤色提亮（光效、高光）
- **Overlay**: 叠加对比（纹理、图案）
- **Soft Light**: 柔光效果（艺术效果）

### 🎚️ 精细控制
- 每层独立不透明度（0-100%）
- 智能颜色自适应
- 三种颜色算法（Enhanced/Classic/Gentle）
- 三种性能模式（Speed/Balanced/Quality）

### 💾 智能配置
- 自动保存所有设置
- 图层信息持久化
- 路径智能记忆
- 下次启动自动加载

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动应用

**Windows:**
```bash
run_multilayer.bat
```

**Linux/Mac:**
```bash
chmod +x run_multilayer.sh
./run_multilayer.sh
```

**或直接运行:**
```bash
python src/watermark_app_multilayer.py
```

## 📖 基本使用

### 1. 上传图片
点击 `Upload Images` → 选择待处理图片

### 2. 添加水印图层
点击 `+ Add Layer` → 选择水印 → 配置混合模式和不透明度

### 3. 管理图层
- **编辑**: 选中图层 → `✎ Edit Layer`
- **删除**: 选中图层 → `× Remove`
- **排序**: `↑ Up` / `↓ Down`

### 4. 应用水印
点击 `🚀 Apply Multi-Layer Watermark` → 等待完成

## 💡 实用案例

### 案例 1️⃣: 品牌水印
```
[1] logo.png (Normal, 100%)
[2] brandname.png (Normal, 80%)
```
**效果**: 清晰的Logo + 稍透明的品牌名

### 案例 2️⃣: 光效水印
```
[1] watermark.png (Normal, 70%)
[2] glow.png (Screen, 50%)
```
**效果**: 带光晕的发光水印

### 案例 3️⃣: 复古效果
```
[1] texture.png (Overlay, 40%)
[2] vignette.png (Soft Light, 60%)
```
**效果**: 复古艺术质感

### 案例 4️⃣: 多语言
```
[1] watermark_cn.png (Normal, 100%)
[2] watermark_en.png (Normal, 80%)
```
**效果**: 中英文双语水印

## 🎨 混合模式详解

### Normal（正常）
```python
result = blend * opacity + base * (1 - opacity)
```
- **用途**: Logo、文字、标准水印
- **特点**: 直接覆盖，最清晰
- **推荐不透明度**: 80-100%

### Screen（滤色）
```python
result = 1 - (1 - base) * (1 - blend)
```
- **用途**: 光效、高光、光晕
- **特点**: 只会变亮，不会变暗
- **推荐不透明度**: 30-60%

### Overlay（叠加）
```python
if base < 0.5:
    result = 2 * base * blend
else:
    result = 1 - 2 * (1 - base) * (1 - blend)
```
- **用途**: 纹理、图案、增强对比
- **特点**: 保留底层细节
- **推荐不透明度**: 30-70%

### Soft Light（柔光）
```python
if blend < 0.5:
    result = 2*base*blend + base²*(1-2*blend)
else:
    result = 2*base*(1-blend) + √base*(2*blend-1)
```
- **用途**: 柔和艺术效果
- **特点**: 比 Overlay 更自然
- **推荐不透明度**: 40-80%

## 🧠 智能颜色适应

### 工作原理
1. 检测水印颜色与背景颜色相似度
2. 如果相似度超过阈值，生成对比色
3. 在应用混合模式前调整颜色

### 三种算法
- **Enhanced**: HSV 色彩空间，自然对比（推荐）
- **Classic**: RGB 空间，强烈对比
- **Gentle**: 柔和对比

### 敏感度设置
- **10-30**: 高敏感，轻微相似即调整
- **30-50**: 中敏感（推荐）
- **50-100**: 低敏感，只调整极相似

## ⚡ 性能模式

### Quality Priority（质量优先）
- 逐像素精确处理
- 最佳效果
- 适合：少量图片、追求完美

### Balanced（平衡）
- 适中采样率
- 速度与质量兼顾
- 适合：日常使用（推荐）

### Speed Priority（速度优先）
- 采样处理
- 最快速度
- 适合：批量处理、预览

## 📊 性能指标

测试环境: 1920x1080 图片, 2个水印图层

| 模式 | 单张耗时 | 质量 | 适用场景 |
|------|---------|------|---------|
| Quality | 3.5秒 | ⭐⭐⭐⭐⭐ | 精品输出 |
| Balanced | 2.0秒 | ⭐⭐⭐⭐ | 日常使用 |
| Speed | 1.2秒 | ⭐⭐⭐ | 批量处理 |

## 📂 项目结构

```
watermarkApp/
├── src/
│   └── watermark_app_multilayer.py    # v1.5 主程序
├── configs/
│   └── multilayer_watermark_config.json  # 配置文件
├── docs/
│   └── MULTILAYER_GUIDE.md             # 详细指南
├── run_multilayer.bat                   # Windows启动
├── run_multilayer.sh                    # Linux/Mac启动
├── QUICK_START.md                       # 快速开始
└── VERSION_1.5_RELEASE_NOTES.md        # 发布说明
```

## 📚 文档导航

- 📘 [快速开始指南](QUICK_START.md) - 5分钟上手
- 📗 [完整使用手册](docs/MULTILAYER_GUIDE.md) - 详细功能说明
- 📙 [发布说明](VERSION_1.5_RELEASE_NOTES.md) - 更新内容
- 📕 [智能算法](docs/SMART_WATERMARK_ALGORITHM.md) - 技术细节
- 📓 [项目结构](PROJECT_STRUCTURE.md) - 目录说明

## 🔧 配置文件示例

```json
{
  "last_stretch": false,
  "last_smart_color": true,
  "last_sensitivity": 30,
  "last_algorithm": "enhanced",
  "last_performance": "balanced",
  "layers": [
    {
      "path": "D:/watermarks/logo.png",
      "opacity": 100,
      "blend_mode": "normal"
    },
    {
      "path": "D:/watermarks/text.png",
      "opacity": 80,
      "blend_mode": "overlay"
    }
  ]
}
```

## 🆚 版本对比

| 特性 | v1.4 | v1.5 |
|------|------|------|
| 水印图层 | 1个 | **多个** ✨ |
| 混合模式 | ❌ | **4种** ✨ |
| 图层管理 | ❌ | **完整** ✨ |
| 独立不透明度 | ❌ | **✅** ✨ |
| 智能颜色 | ✅ | ✅ |
| 性能优化 | ✅ | ✅ |
| 配置保存 | ✅ | **增强** ✨ |

## 💻 系统要求

### 最低配置
- Python 3.7+
- 2GB RAM
- Windows 7+ / macOS 10.12+ / Linux

### 推荐配置
- Python 3.9+
- 4GB+ RAM
- 多核处理器

### 依赖库
```txt
Pillow >= 8.0.0
numpy >= 1.19.0
```

## 🐛 问题反馈

如遇到问题，请检查：
1. Python 版本是否 3.7+
2. 依赖库是否正确安装
3. 配置文件是否完整

## 📝 更新计划

### 近期计划 (v1.6)
- [ ] 更多混合模式（Multiply, Color Dodge）
- [ ] 图层位置独立控制
- [ ] 预设模板系统

### 长远规划
- [ ] GPU 加速
- [ ] 实时预览
- [ ] 图层效果（模糊、阴影）

## 🙏 致谢

感谢：
- Pillow 图像处理库
- NumPy 科学计算库
- 所有用户的支持和反馈

## 📄 许可证

本项目基于现有 WatermarkApp 项目开发

---

## 🎯 核心优势总结

✅ **专业级混合** - 完整 Photoshop 算法
✅ **多层叠加** - 无限创意可能
✅ **智能适应** - 自动颜色调整
✅ **简单易用** - 友好的图形界面
✅ **高效处理** - 三种性能模式
✅ **配置记忆** - 自动保存设置

---

**Multi-Layer Watermark App v1.5** - 让每张图片都独一无二！ 🎨✨

*开始创作你的专属水印吧！*
