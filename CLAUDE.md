# 🤖 CLAUDE.md - AI Context Document

> **此文档专门为 AI 助手（如 Claude）提供项目上下文信息**
> 人类用户请查看 [README.md](README.md)

---

## 📌 项目概述

**Multi-Layer Watermark App v1.5** 是一个基于 Python + Tkinter 的多图层水印应用，支持 Photoshop 混合模式和智能颜色适应。

### 核心特性
- 🎨 多图层水印系统
- 🌈 4种 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
- 🧠 智能颜色适应（自动检测背景并调整水印颜色）
- ⚡ 高性能处理（NumPy 向量化计算）
- 💾 配置自动保存/加载

---

## 📂 项目结构

```
watermarkApp/
├── src/                              # 源代码
│   ├── watermark_app_multilayer.py   # v1.5 多图层版（当前最新）
│   ├── watermark_app_smart_optimized.py  # v1.4 优化版
│   └── watermark_app_smart.py        # v1.3 基础智能版
│
├── configs/                          # 配置文件
│   ├── multilayer_watermark_config.json
│   ├── smart_watermark_optimized_config.json
│   └── smart_watermark_config.json
│
├── docs/                             # 文档（已整理）
│   ├── MULTILAYER_GUIDE.md           # v1.5 完整使用指南
│   ├── QUICK_START.md                # 快速开始
│   ├── VERSION_1.5_RELEASE_NOTES.md  # 发布说明
│   ├── DEVELOPMENT_SUMMARY_V1.5.md   # 开发总结
│   ├── PROJECT_STRUCTURE.md          # 项目结构
│   ├── SMART_WATERMARK_ALGORITHM.md  # 智能算法说明
│   └── ... (其他文档)
│
├── tests/                            # 测试文件（已整理）
│   ├── images/                       # 测试用图片
│   ├── alpha_protection/             # Alpha保护测试
│   ├── performance/                  # 性能测试
│   ├── images_samples/               # 图片样本
│   └── temp/                         # 临时文件
│
├── archive/                          # 归档版本
│   └── watermark_app_alpha_protected.py  # v1.5 Alpha保护版（已归档）
│
├── versions/                         # 历史版本
├── releases/                         # 发布包
├── tools/                            # 工具脚本
├── assets/                           # 资源文件
│
├── run_multilayer.bat                # Windows 启动脚本
├── run_multilayer.sh                 # Linux/Mac 启动脚本
├── requirements.txt                  # Python 依赖
├── .gitignore                        # Git 忽略配置
├── README.md                         # 用户文档
└── CLAUDE.md                         # 本文档（AI上下文）
```

---

## 🔧 技术栈

### 核心库
- **Python 3.7+**
- **tkinter** - GUI 界面
- **Pillow (PIL)** - 图像处理
- **NumPy** - 数值计算和向量化
- **colorsys** - 色彩空间转换

### 关键算法

#### 1. Photoshop 混合模式
基于 Wikipedia 和 Photoshop 官方算法实现：

```python
# Normal
result = blend * opacity + base * (1 - opacity)

# Screen
result = 1.0 - (1.0 - base) * (1.0 - blend)

# Overlay
if base < 0.5:
    result = 2 * base * blend
else:
    result = 1.0 - 2 * (1.0 - base) * (1.0 - blend)

# Soft Light
if blend < 0.5:
    result = 2*base*blend + base²*(1-2*blend)
else:
    result = 2*base*(1-blend) + √base*(2*blend-1)
```

#### 2. 智能颜色适应
- 使用 RGB 欧几里得距离检测颜色相似度
- 基于 HSV 色彩空间生成对比色
- 支持三种算法：Enhanced（推荐）、Classic、Gentle

#### 3. 性能优化
- NumPy 向量化计算（避免逐像素循环）
- 颜色距离缓存
- 可选采样模式（Speed/Balanced/Quality）

---

## 🎯 版本演进

| 版本 | 文件 | 主要功能 | 状态 |
|------|------|---------|------|
| **v1.5** | `watermark_app_multilayer.py` | 多图层 + 混合模式 | ⭐ 当前最新 |
| v1.4 | `watermark_app_smart_optimized.py` | 智能颜色 + 优化 | 可用 |
| v1.3 | `watermark_app_smart.py` | 基础智能颜色 | 可用 |
| v1.2 | `versions/watermark_app_v1.2.py` | 基础水印 | 已归档 |
| ~v1.5α~ | `archive/watermark_app_alpha_protected.py` | Alpha保护 | 已归档 |

**重要决策**：Alpha 保护版本已归档，因其设计理念与多图层系统不兼容。

---

## 💡 代码架构

### v1.5 主要类结构

```python
class WatermarkLayer:
    """水印图层类"""
    - image_path: str
    - image: PIL.Image
    - opacity: float (0-100)
    - blend_mode: str ('normal'|'overlay'|'screen'|'soft_light')
    - name: str

class MultiLayerWatermarkApp:
    """主应用类"""

    # 图层管理
    - watermark_layers: List[WatermarkLayer]
    - add_watermark_layer()
    - edit_layer_dialog()
    - remove_selected_layer()
    - move_layer(direction)

    # 混合模式
    - blend_normal()
    - blend_screen()
    - blend_overlay()
    - blend_soft_light()
    - apply_blend_mode()

    # 智能颜色（继承自 v1.4）
    - calculate_color_distance_optimized()
    - get_contrasting_color_enhanced()

    # 核心处理
    - apply_multilayer_watermark()

    # UI 组件
    - create_layer_section()
    - create_upload_section()
    - create_settings_section()
    - create_smart_section()

    # 配置管理
    - load_config()
    - save_config()
```

---

## 📝 配置文件格式

### multilayer_watermark_config.json
```json
{
  "last_used_directory": "路径",
  "save_directory": "路径",
  "last_watermark_directory": "路径",
  "last_images_directory": "路径",
  "last_stretch": false,
  "last_smart_color": true,
  "last_sensitivity": 30,
  "last_algorithm": "enhanced",
  "last_performance": "balanced",
  "last_images_files": ["路径1", "路径2"],
  "layers": [
    {
      "path": "水印文件路径",
      "opacity": 100,
      "blend_mode": "normal"
    }
  ]
}
```

---

## 🔍 关键文件说明

### 主程序
- **[src/watermark_app_multilayer.py](src/watermark_app_multilayer.py)** (870行)
  - v1.5 的核心实现
  - 包含完整的多图层系统和混合模式

### 文档（给人看）
- **[README.md](README.md)** - 用户主文档
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - 快速开始指南
- **[docs/MULTILAYER_GUIDE.md](docs/MULTILAYER_GUIDE.md)** - 完整使用手册

### 文档（给开发者看）
- **[docs/DEVELOPMENT_SUMMARY_V1.5.md](docs/DEVELOPMENT_SUMMARY_V1.5.md)** - 开发总结
- **[docs/VERSION_1.5_RELEASE_NOTES.md](docs/VERSION_1.5_RELEASE_NOTES.md)** - 发布说明
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - 项目结构

### 技术文档
- **[docs/SMART_WATERMARK_ALGORITHM.md](docs/SMART_WATERMARK_ALGORITHM.md)** - 智能算法详解

---

## 🚨 重要注意事项

### 1. 文件结构已整理
- ✅ 所有测试文件已移至 `tests/` 目录
- ✅ 所有文档已移至 `docs/` 目录
- ✅ 根目录只保留 README.md 和 CLAUDE.md

### 2. .gitignore 配置
已配置忽略：
- 测试目录：`tests/alpha_protection/`, `tests/performance/` 等
- 配置文件：`*_config.json`（除了示例配置）
- 输出目录：`results/`, `output/`, `processed/`
- 临时文件：`*.tmp`, `*.temp`, `*.log`

### 3. 中文编码
- 项目中使用 UTF-8 编码
- 文件名可能包含中文（如测试图片）
- 代码中有中文注释和UI文本

### 4. 配置文件路径
- 配置文件使用相对路径查找
- 支持 `configs/` 目录下的配置文件
- 向下兼容旧版配置格式

---

## 🎓 开发指南

### 添加新混合模式
1. 在 `MultiLayerWatermarkApp` 类中添加 `blend_xxx()` 方法
2. 在 `apply_blend_mode()` 中添加条件分支
3. 在 `edit_layer_dialog()` UI 中添加选项
4. 更新文档说明

### 添加新智能算法
1. 在 `get_contrasting_color_enhanced()` 中添加新算法分支
2. 在 UI 的 `algorithm_var` 选项中添加新选项
3. 更新文档说明

### 性能优化建议
- 优先使用 NumPy 向量化操作
- 避免逐像素循环（除非必要）
- 使用缓存减少重复计算
- 考虑使用多线程处理多张图片

---

## 🤝 与 AI 协作建议

### 当需要修改代码时
1. 先查看 `src/watermark_app_multilayer.py` 了解当前实现
2. 参考 `docs/DEVELOPMENT_SUMMARY_V1.5.md` 了解设计决策
3. 查看 `docs/SMART_WATERMARK_ALGORITHM.md` 了解算法细节
4. 保持代码风格一致（使用中文注释，遵循现有结构）

### 当需要添加功能时
1. 优先考虑扩展现有类，而非创建新文件
2. 更新相关文档（至少更新 README.md 和 CLAUDE.md）
3. 考虑配置文件兼容性
4. 添加适当的错误处理

### 当需要调试问题时
1. 检查 `configs/` 目录下的配置文件
2. 查看 `tests/` 目录下是否有相关测试
3. 注意中文编码问题
4. 检查 PIL/NumPy 版本兼容性

---

## 📊 性能基准

### 测试环境
- 图片尺寸: 1920x1080
- 图层数量: 2个
- 测试平台: 现代多核CPU

### 性能数据
| 模式 | 单张耗时 | 质量评分 |
|------|---------|---------|
| Quality | 3.5秒 | ⭐⭐⭐⭐⭐ |
| Balanced | 2.0秒 | ⭐⭐⭐⭐ |
| Speed | 1.2秒 | ⭐⭐⭐ |

---

## 🔮 未来计划

### v1.6 可能的功能
- [ ] 更多混合模式（Multiply, Color Dodge, Color Burn）
- [ ] 图层位置独立控制
- [ ] 预设模板系统
- [ ] 图层缩放比例调整

### 长期计划
- [ ] GPU 加速（CUDA/OpenCL）
- [ ] 实时预览功能
- [ ] 图层效果（模糊、阴影、描边）
- [ ] 批量配置应用

---

## 🎯 快速参考

### 启动应用
```bash
python src/watermark_app_multilayer.py
```

### 运行测试
```bash
python tests/performance_test.py
python tests/test_smart_watermark.py
```

### 查看配置
```bash
cat configs/multilayer_watermark_config.json
```

### 检查依赖
```bash
pip list | grep -E "Pillow|numpy"
```

---

## 📚 相关资源

### 外部参考
- [Pillow 文档](https://pillow.readthedocs.io/)
- [NumPy 文档](https://numpy.org/doc/)
- [Photoshop Blend Modes - Wikipedia](https://en.wikipedia.org/wiki/Blend_modes)
- [Deep Sky Colors - Blend Mode Formulas](https://www.deepskycolors.com/tools-tutorials/formulas-for-photoshop-blending-modes/)

### 内部文档
- [完整文档列表](docs/)
- [版本历史](docs/VERSION_HISTORY.md)
- [智能算法详解](docs/SMART_WATERMARK_ALGORITHM.md)

---

## ✅ 总结

**Multi-Layer Watermark App v1.5** 是一个功能完整、文档齐全的专业水印应用。

**核心价值**:
- 🎨 多图层系统 - 创意无限
- 🌈 专业混合模式 - Photoshop 标准
- 🧠 智能颜色适应 - 自动优化
- ⚡ 高性能处理 - NumPy 加速
- 📚 完善文档 - 易于理解和扩展

**代码质量**:
- 清晰的类结构
- 完整的中文注释
- 模块化设计
- 良好的错误处理

**适合 AI 协作**:
- 结构清晰，易于理解
- 文档完善，上下文充足
- 代码规范，易于扩展

---

*最后更新: 2025-10-23*
*版本: v1.5.0*
*维护者: WatermarkApp Team*
