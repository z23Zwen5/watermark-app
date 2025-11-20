# 🤖 CLAUDE.md - AI Context Document

> **此文档专门为 AI 助手提供项目上下文**
> 人类用户请查看 [README.md](README.md)

---

## 📌 项目概述

**Multi-Layer Watermark App v1.6.2** - 基于 Python + Tkinter 的专业多图层水印应用

### 核心特性
- 🎨 多图层水印系统
- 🌈 4种 Photoshop 混合模式（Normal/Overlay/Screen/Soft Light）
- 👁️ 图层可见性切换（类似 Photoshop）
- 🔤 文本标注（序号/文件名，智能对比色）
- 🎨 系统字体选择（自动扫描已安装字体）
- 📏 百分比字体大小（多分辨率一致）
- ⚡ 高性能处理（NumPy 向量化 + uint8 优化）
- 💾 配置自动保存/加载

### v1.6.2 更新
- 👁️ **图层可见性**: 类似 Photoshop 眼睛图标，隐藏/显示图层
- 🎨 **系统字体**: 自动扫描 Windows/macOS/Linux 字体，下拉选择
- 📏 **百分比字体**: 字体大小基于图片高度（3% = 1080p:32px, 4K:64px）
- 🔄 **向后兼容**: 自动转换旧配置像素值为百分比

### v1.6.0 核心功能
- ✨ 新增文本标注模块（独立 `text_label_module.py`）
- ⚡ uint8 优化：Normal 模式提速 2x
- ⚡ BILINEAR 缩放：比 LANCZOS 快 1.6-1.9x
- 📊 性能提升：**4K图片处理快 1.95x**（3.2s → 1.64s）
- 📄 新增 `performance_analysis.md` 和 `test_performance.py`

---

## 📂 核心文件

```
watermarkApp/
├── src/
│   ├── watermark_app_multilayer.py    # 主程序 (948行)
│   └── text_label_module.py           # 文本标注模块 (320行)
├── configs/
│   └── multilayer_watermark_config.json
├── performance_analysis.md            # 性能分析文档
├── test_performance.py                # 性能测试脚本
├── requirements.txt                   # Pillow, numpy
└── run_multilayer.{bat,sh}            # 启动脚本
```

---

## 🔧 技术栈

- **Python 3.7+** + tkinter + Pillow + NumPy
- **混合模式算法**：Photoshop 标准（Normal/Screen/Overlay/Soft Light）
- **性能优化**：
  - NumPy 向量化（避免逐像素循环）
  - uint8 直接计算（Normal 模式，避免 float32 转换）
  - BILINEAR 缩放（替代 LANCZOS）

---

## 💡 代码架构

### 主应用 (`watermark_app_multilayer.py`)

```python
class WatermarkLayer:
    """水印图层"""
    image_path: str
    image: PIL.Image
    opacity: int (0-100)
    blend_mode: str
    visible: bool  # 图层可见性（类似 Photoshop 眼睛图标）

class MultiLayerWatermarkApp:
    """主应用类"""

    # 核心属性
    watermark_layers: List[WatermarkLayer]
    text_label_config: TextLabelConfig

    # 核心方法
    apply_blend_mode(base, layer, mode, opacity)  # 混合模式计算
    apply_multilayer_watermark(image)             # 多图层叠加（跳过不可见图层）
    toggle_layer_visibility()                      # 切换图层可见性
    load_config() / save_config()                 # 配置持久化
```

**关键优化**（`apply_blend_mode` 第 594-665 行）：
```python
# Normal 模式：uint8 直接计算（2x 快）
if blend_mode == 'normal':
    base_rgb = base_array[:, :, :3].astype(np.uint16)
    blend_rgb = layer_array[:, :, :3].astype(np.uint16)
    alpha = blend_alpha.astype(np.uint16)[:, :, np.newaxis]
    alpha = (alpha * opacity) // 100
    result_rgb = (base_rgb * (255 - alpha) + blend_rgb * alpha) // 255
    result[:, :, :3] = result_rgb.astype(np.uint8)
    return result

# 其他模式：float32（保证准确性）
# screen, overlay, soft_light...
```

### 文本标注模块 (`text_label_module.py`)

```python
class TextLabelConfig:
    """配置类"""
    enabled: bool
    label_type: str   # 'number' | 'filename'
    position: str     # 'top_right' | ...
    font_size: float  # 百分比（相对图片高度，3.0 = 3%）
    font_name: str    # 字体名称（从系统字体中选择）
    auto_contrast: bool

    to_dict() / from_dict()  # 配置序列化（自动转换旧像素值）

class TextLabelDrawer:
    """绘制器"""
    get_font(size)                           # 智能字体选择（系统字体 + 中英文）
    get_contrasting_color(image, position)   # 自动对比色
    draw_text_label(image, text, index)      # 绘制标注（动态计算像素大小）

# 系统字体扫描
scan_system_fonts()    # 扫描 Windows/macOS/Linux 字体目录
get_system_fonts()     # 获取缓存的字体映射 {name: path}
```

---

## 📝 配置文件格式

`configs/multilayer_watermark_config.json`:
```json
{
  "layers": [
    {"path": "水印路径", "opacity": 100, "blend_mode": "normal", "visible": true}
  ],
  "text_label": {
    "enabled": false,
    "label_type": "number",
    "position": "top_right",
    "font_size": 3.0,
    "font_name": "Arial",
    "auto_contrast": true,
    "background_enabled": true,
    "background_opacity": 128
  }
}
```

---

## 📊 性能数据

### 实测结果（4K 图片 3840×2160，3 图层）

| 版本 | 算法 | 时间 | 提速 |
|------|------|------|------|
| v1.5 | LANCZOS + float32 | 3.2s | baseline |
| v1.6 | BILINEAR + float32 | 2.8s | 1.14x |
| **v1.6** | **BILINEAR + uint8** | **1.64s** | **1.95x** ⬆️ |

**性能瓶颈**（已优化）：
1. ~~类型转换 (uint8 ↔ float32): 35%~~ → uint8 优化解决
2. ~~图片缩放 (LANCZOS): 15%~~ → BILINEAR 优化解决
3. 混合计算: 17%（已最优）

---

## 🚨 重要注意事项

### 1. 智能颜色适应已废弃 ❌

**废弃的版本**：
- `src/watermark_app_smart.py` (v1.3)
- `src/watermark_app_smart_optimized.py` (v1.4)

**原因**：与多图层架构不兼容，维护成本高

**替代方案**：
- 使用混合模式（Overlay/Screen）
- 文本标注的自动对比色功能保留

### 2. 文件编码
- UTF-8 编码，支持中文文件名和注释
- 配置文件路径：优先 `configs/`，兼容旧版

### 3. 使用场景
- **全屏半透明水印**（主要场景）
- **多图层叠加效果**
- **批量处理图片**

---

## 🎯 快速参考

### 启动应用
```bash
python src/watermark_app_multilayer.py
```

### 性能测试
```bash
python test_performance.py
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 检查版本
```bash
grep "version" README.md
git log --oneline -5
```

---

## 🤝 AI 协作建议

### 修改代码前必读
1. **查看主程序**：`src/watermark_app_multilayer.py` (948行)
2. **性能考虑**：参考 `performance_analysis.md`
3. **代码风格**：中文注释，遵循现有结构
4. **测试场景**：全屏半透明水印（非小 logo）

### 添加功能流程
1. 创建独立模块（参考 `text_label_module.py`）
2. 在主程序中集成
3. 更新配置文件格式（`to_dict`/`from_dict`）
4. 更新 README.md 和 CLAUDE.md
5. 添加错误处理

### 性能优化原则
1. 优先 NumPy 向量化
2. 避免 uint8 ↔ float32 转换
3. 使用 uint16 中间类型防止溢出
4. 测试前后性能（`test_performance.py`）
5. 确保功能正确性

### 调试问题
- 检查配置：`configs/multilayer_watermark_config.json`
- 查看测试：`tests/` 目录
- 注意编码：UTF-8
- 版本兼容：Pillow >= 8.0, NumPy >= 1.20

---

## 📚 文档资源

### 用户文档
- [README.md](README.md) - 主文档
- [docs/QUICK_START.md](docs/QUICK_START.md) - 快速开始
- [docs/MULTILAYER_GUIDE.md](docs/MULTILAYER_GUIDE.md) - 完整指南

### 技术文档
- [performance_analysis.md](performance_analysis.md) - 性能分析
- [docs/DEVELOPMENT_SUMMARY_V1.5.md](docs/DEVELOPMENT_SUMMARY_V1.5.md) - 开发总结
- [docs/VERSION_1.5_RELEASE_NOTES.md](docs/VERSION_1.5_RELEASE_NOTES.md) - 发布说明

### 外部参考
- [Pillow 文档](https://pillow.readthedocs.io/)
- [NumPy 文档](https://numpy.org/doc/)
- [Photoshop Blend Modes](https://en.wikipedia.org/wiki/Blend_modes)

---

## 🎓 开发示例

### 添加新混合模式
```python
# src/watermark_app_multilayer.py - apply_blend_mode()
if blend_mode == 'multiply':
    result_rgb = base_rgb * blend_rgb  # 添加算法

# UI 部分 - create_layer_section()
blend_mode_combo = ttk.Combobox(...,
    values=['normal', 'overlay', 'screen', 'soft_light', 'multiply'])
```

### 扩展文本标注
```python
# text_label_module.py
class TextLabelConfig:
    def __init__(self):
        self.custom_color = (255, 0, 0)  # 新增自定义颜色

# watermark_app_multilayer.py
def create_text_label_section(self, parent):
    color_button = tk.Button(text="Choose Color",
                            command=self.choose_label_color)
```

---

## ✅ 版本总结

**v1.6.2** 是功能完整、性能优异的稳定版本：

### 核心价值
- 🎨 多图层创意组合 + 图层可见性切换
- 🌈 专业混合模式
- 🔤 智能文本标注 + 系统字体选择 + 百分比字体
- ⚡ 高性能处理（1.95x 提速）
- 📚 完善文档

### 代码质量
- 模块化设计（独立 text_label_module）
- 清晰的类结构
- 完整的中文注释
- 性能监控和优化
- 向后兼容设计

### 适合场景
- 摄影师批量加水印
- 内容创作者添加版权信息
- 设计师多图层效果制作
- 自动添加图片序号/文件名

---

*最后更新: 2025-11-20*
*版本: v1.6.2*
*总行数: 320 行*
