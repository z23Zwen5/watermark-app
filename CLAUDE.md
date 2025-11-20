# 🤖 CLAUDE.md - AI Context Document

> **此文档专门为 AI 助手（如 Claude）提供项目上下文信息**
> 人类用户请查看 [README.md](README.md)

---

## 📌 项目概述

**Multi-Layer Watermark App v1.6** 是一个基于 Python + Tkinter 的多图层水印应用，支持 Photoshop 混合模式和文本标注功能。

### 核心特性
- 🎨 多图层水印系统
- 🌈 4种 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
- 🔤 文本标注功能（序号或文件名）
- ⚡ 高性能处理（NumPy 向量化 + BILINEAR 缩放）
- 💾 配置自动保存/加载

### 最近更新 (v1.6)
- ✨ 新增文本标注模块（右上角显示序号或文件名）
- ⚡ 性能优化：改用 BILINEAR 缩放提速 1.6-1.9x
- 📊 新增性能分析文档和测试工具
- 🧹 代码模块化：独立 text_label_module.py

---

## 📂 项目结构

```
watermarkApp/
├── src/                              # 源代码
│   ├── watermark_app_multilayer.py   # v1.6 多图层版（926行，当前最新）
│   ├── text_label_module.py          # v1.6 文本标注模块（320行，NEW！）
│   ├── watermark_app_smart_optimized.py  # v1.4 优化版（已过时）
│   └── watermark_app_smart.py        # v1.3 基础版（已过时）
│
├── configs/                          # 配置文件
│   └── multilayer_watermark_config.json
│
├── docs/                             # 文档（已整理）
│   ├── MULTILAYER_GUIDE.md           # v1.5 完整使用指南
│   ├── QUICK_START.md                # 快速开始
│   ├── VERSION_1.5_RELEASE_NOTES.md  # v1.5 发布说明
│   ├── DEVELOPMENT_SUMMARY_V1.5.md   # v1.5 开发总结
│   ├── PROJECT_STRUCTURE.md          # 项目结构
│   └── ... (其他文档)
│
├── tests/                            # 测试文件
│   ├── images/                       # 测试用图片
│   ├── performance/                  # 性能测试
│   └── ...
│
├── archive/                          # 归档版本
│   └── watermark_app_alpha_protected.py  # Alpha保护版（已归档）
│
├── versions/                         # 历史版本
├── releases/                         # 发布包
├── tools/                            # 工具脚本
│
├── performance_analysis.md           # 性能分析文档（NEW！）
├── test_performance.py               # 性能测试脚本（NEW！）
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

#### 2. 文本标注（新功能）
- **智能字体选择**：自动检测系统字体（支持中英文）
- **自动对比色**：根据背景亮度自动选择黑/白文字
- **半透明背景**：提高文字可读性
- **两种模式**：序号（1,2,3...）或文件名

#### 3. 性能优化
- **NumPy 向量化**：避免逐像素循环
- **BILINEAR 缩放**：比 LANCZOS 快 1.6-1.9x，质量肉眼难辨
- **类型转换优化**：减少 uint8 ↔ float32 转换次数

---

## 🎯 版本演进

| 版本 | 文件 | 主要功能 | 状态 | 行数 |
|------|------|---------|------|------|
| **v1.6** | `watermark_app_multilayer.py` + `text_label_module.py` | 多图层 + 文本标注 + 性能优化 | ⭐ 当前最新 | 926 + 320 |
| v1.5 | `watermark_app_multilayer.py` | 多图层 + 混合模式 | 已过时 | ~870 |
| v1.4 | `watermark_app_smart_optimized.py` | 智能颜色 + 优化 | 已废弃 | ~700 |
| v1.3 | `watermark_app_smart.py` | 基础智能颜色 | 已废弃 | ~500 |
| v1.2 | `versions/watermark_app_v1.2.py` | 基础水印 | 已归档 | ~400 |

**重要变更：**
- ❌ **智能颜色适应功能已废弃**（v1.4/v1.3 特性不再维护）
- ✅ v1.6 专注于多图层 + 文本标注 + 性能优化

---

## 💡 代码架构

### v1.6 主要类结构

#### 1. 主应用类 (`watermark_app_multilayer.py`)

```python
class WatermarkLayer:
    """水印图层类"""
    - image_path: str
    - image: PIL.Image
    - opacity: int (0-100)
    - blend_mode: str ('normal'|'overlay'|'screen'|'soft_light')
    - name: str

class MultiLayerWatermarkApp:
    """主应用类"""

    # 核心属性
    - watermark_layers: List[WatermarkLayer]
    - text_label_config: TextLabelConfig  # 新增

    # 图层管理
    - add_watermark_layer()
    - edit_layer_dialog()
    - remove_selected_layer()
    - move_layer(direction)

    # 混合模式
    - apply_blend_mode(base, layer, mode, opacity)

    # 核心处理
    - apply_multilayer_watermark(image)

    # UI 组件
    - create_layer_section()
    - create_text_label_section()  # 新增
    - create_settings_section()

    # 配置管理
    - load_config()
    - save_config()
```

#### 2. 文本标注模块 (`text_label_module.py`) ✨ NEW

```python
class TextLabelConfig:
    """文本标注配置类"""
    - enabled: bool
    - label_type: str ('number'|'filename')
    - position: str ('top_right'|'top_left'|...)
    - font_size: int
    - auto_contrast: bool
    - background_enabled: bool
    - background_opacity: int

    # 配置持久化
    - to_dict() -> dict
    - from_dict(config_dict)

class TextLabelDrawer:
    """文本标注绘制器"""
    - get_font(size) -> ImageFont
    - get_contrasting_color(image, position) -> (text_color, bg_color)
    - draw_text_label(image, text, index) -> Image

# 便捷函数
def draw_text_label(image, text, config, index=None) -> Image
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
  "last_images_files": ["路径1", "路径2"],
  "layers": [
    {
      "path": "水印文件路径",
      "opacity": 100,
      "blend_mode": "normal"
    }
  ],
  "text_label": {
    "enabled": false,
    "label_type": "number",
    "position": "top_right",
    "font_size": 36,
    "auto_contrast": true,
    "background_enabled": true,
    "background_color": [0, 0, 0],
    "background_opacity": 128
  }
}
```

---

## 🔍 关键文件说明

### 主程序
- **[src/watermark_app_multilayer.py](src/watermark_app_multilayer.py)** (926行)
  - v1.6 的主程序
  - 包含完整的多图层系统、混合模式、文本标注集成

- **[src/text_label_module.py](src/text_label_module.py)** (320行) ✨ NEW
  - v1.6 新增的文本标注模块
  - 独立的配置类和绘制器
  - 支持序号和文件名两种模式

### 性能分析 ✨ NEW
- **[performance_analysis.md](performance_analysis.md)**
  - 详细的性能瓶颈分析
  - 识别了 4 个主要性能问题
  - 提供优化建议和理论分析

- **[test_performance.py](test_performance.py)**
  - 性能测试脚本
  - 测试不同分辨率的处理时间
  - 对比 LANCZOS vs BILINEAR 性能

### 用户文档
- **[README.md](README.md)** - 用户主文档
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - 快速开始指南
- **[docs/MULTILAYER_GUIDE.md](docs/MULTILAYER_GUIDE.md)** - 完整使用手册

### 技术文档
- **[docs/DEVELOPMENT_SUMMARY_V1.5.md](docs/DEVELOPMENT_SUMMARY_V1.5.md)** - v1.5 开发总结
- **[docs/VERSION_1.5_RELEASE_NOTES.md](docs/VERSION_1.5_RELEASE_NOTES.md)** - v1.5 发布说明
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - 项目结构

---

## 🚨 重要注意事项

### 1. 智能颜色适应功能已废弃 ❌

**废弃的功能：**
- ✗ `watermark_app_smart.py` - v1.3 智能颜色版本
- ✗ `watermark_app_smart_optimized.py` - v1.4 优化版本
- ✗ 智能颜色适应算法（Enhanced/Classic/Gentle）
- ✗ 颜色相似度检测
- ✗ HSV 色彩空间对比色生成

**原因：**
- 与多图层系统架构不兼容
- 维护成本高
- 用户反馈使用率低
- v1.6 专注于多图层 + 文本标注

**替代方案：**
- 使用混合模式（Overlay/Screen）实现类似效果
- 文本标注功能的自动对比色仍然保留

### 2. 文件结构已整理
- ✅ 所有测试文件已移至 `tests/` 目录
- ✅ 所有文档已移至 `docs/` 目录
- ✅ 根目录只保留 README.md 和 CLAUDE.md

### 3. .gitignore 配置
已配置忽略：
- 测试目录：`tests/alpha_protection/`, `tests/performance/` 等
- 配置文件：`*_config.json`（除了示例配置）
- 输出目录：`results/`, `output/`, `processed/`
- 临时文件：`*.tmp`, `*.temp`, `*.log`

### 4. 中文编码
- 项目中使用 UTF-8 编码
- 文件名可能包含中文（如测试图片）
- 代码中有中文注释和UI文本

### 5. 配置文件路径
- 配置文件使用相对路径查找
- 支持 `configs/` 目录下的配置文件
- 向下兼容旧版配置格式（自动迁移）

---

## 📊 性能特性

### 性能数据（基于实测）

#### 不同分辨率的处理时间（单张图，3 个图层）

| 图片尺寸 | 像素数 | 内存使用 | 处理时间 (v1.5) | 处理时间 (v1.6) | 提速 |
|---------|--------|---------|----------------|----------------|------|
| 1920x1080 | 2.1M | ~120 MB | ~0.7秒 | ~0.5秒 | **30%** |
| 2560x1440 | 3.7M | ~210 MB | ~1.3秒 | ~1.0秒 | **23%** |
| 3840x2160 | 8.3M | ~720 MB | ~3.4秒 | ~2.6秒 | **24%** |

### 性能瓶颈（按耗时排序）

从性能测试结果（4K 图片）：

1. 🔴 **类型转换** (uint8 ↔ float32): 392ms (35%)
2. 🟡 **uint8 转换回来**: 227ms (20%)
3. 🟡 **混合计算**: 192ms (17%)
4. 🟢 **图片缩放** (BILINEAR): 120ms (11%) ⬇️ 已优化

### v1.6 性能优化

#### ✅ 已完成的优化

1. **BILINEAR 缩放**
   ```python
   # v1.5: LANCZOS (慢但高质量)
   resized = layer.image.resize(size, Image.LANCZOS)  # ~190ms

   # v1.6: BILINEAR (快且质量够用)
   resized = layer.image.resize(size, Image.BILINEAR)  # ~120ms
   ```
   **提升：1.6-1.9x**

2. **NumPy 向量化**
   - 避免逐像素循环
   - 使用 NumPy 数组操作
   - 批量处理 RGB 通道

#### 💡 未来优化方向

1. **只处理水印覆盖区域**（最大收益 50-90%）
2. **复用临时数组**（减少内存分配）
3. **减少类型转换**（最大瓶颈）
4. **多进程处理**（批量处理多张图片）

详见 [performance_analysis.md](performance_analysis.md)

---

## 🎓 开发指南

### 添加新功能

#### 添加新混合模式
1. 在 `apply_blend_mode()` 中添加算法
2. 在 UI 的 `blend_mode_combo` 中添加选项
3. 更新文档说明

#### 扩展文本标注功能
1. 修改 `text_label_module.py` 中的 `TextLabelConfig`
2. 在主程序中添加对应的 UI 控件
3. 更新配置文件的保存/加载逻辑

示例（添加字体颜色选择）：
```python
# text_label_module.py
class TextLabelConfig:
    def __init__(self):
        self.custom_color = (255, 0, 0)  # 新增

# watermark_app_multilayer.py
def create_text_label_section(self, parent):
    # 添加颜色选择器
    color_button = tk.Button(...)
```

### 性能优化建议
- 优先使用 NumPy 向量化操作
- 避免逐像素循环（除非必要）
- 使用缓存减少重复计算
- 考虑使用多线程处理多张图片
- 参考 `performance_analysis.md` 中的建议

---

## 🤝 与 AI 协作建议

### 当需要修改代码时
1. 先查看 `src/watermark_app_multilayer.py` 了解当前实现
2. 参考 `docs/DEVELOPMENT_SUMMARY_V1.5.md` 了解设计决策
3. 查看 `performance_analysis.md` 了解性能考虑
4. 保持代码风格一致（使用中文注释，遵循现有结构）

### 当需要添加功能时
1. 优先考虑创建独立模块（参考 `text_label_module.py`）
2. 更新相关文档（至少更新 README.md 和 CLAUDE.md）
3. 考虑配置文件兼容性
4. 添加适当的错误处理

### 当需要调试问题时
1. 检查 `configs/` 目录下的配置文件
2. 查看 `tests/` 目录下是否有相关测试
3. 注意中文编码问题
4. 检查 PIL/NumPy 版本兼容性

### 当需要优化性能时
1. 先运行 `test_performance.py` 获取基准数据
2. 使用 `cProfile` 或 `line_profiler` 找到瓶颈
3. 参考 `performance_analysis.md` 中的建议
4. 确保优化不影响功能正确性

---

## 🎯 快速参考

### 启动应用
```bash
python src/watermark_app_multilayer.py
```

### 运行性能测试
```bash
python test_performance.py
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
- [快速开始](docs/QUICK_START.md)
- [多图层指南](docs/MULTILAYER_GUIDE.md)
- [性能分析](performance_analysis.md)

---

## ✅ 总结

**Multi-Layer Watermark App v1.6** 是一个功能完整、文档齐全、性能优异的专业水印应用。

### 核心价值
- 🎨 多图层系统 - 创意无限
- 🌈 专业混合模式 - Photoshop 标准
- 🔤 文本标注 - 序号/文件名自动添加
- ⚡ 高性能处理 - NumPy + BILINEAR 优化
- 📚 完善文档 - 易于理解和扩展

### 代码质量
- 清晰的类结构
- 完整的中文注释
- 模块化设计（独立的 text_label_module）
- 良好的错误处理
- 性能监控和分析

### 适合 AI 协作
- 结构清晰，易于理解
- 文档完善，上下文充足
- 代码规范，易于扩展
- 模块化设计，职责明确

### v1.6 新特性
- ✨ 文本标注功能（序号/文件名）
- ⚡ 性能优化（BILINEAR 缩放提速 1.6-1.9x）
- 📊 性能分析文档和测试工具
- 🧹 代码模块化（独立 text_label_module.py）

---

*最后更新: 2025-11-20*
*版本: v1.6.0*
*维护者: WatermarkApp Team*
