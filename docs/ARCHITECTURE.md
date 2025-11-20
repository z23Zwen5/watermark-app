# 🏗️ PyQt6 架构说明

> 代码结构：业务逻辑与 UI 分离

---

## 📂 文件结构

```
src/
├── watermark_core.py           # 核心业务逻辑（400+ 行）
├── watermark_app_pyqt6_ui.py   # UI 界面层（1000+ 行）
├── watermark_app_pyqt6.py      # 旧版本（保留作为备份）
└── text_label_module.py        # 文本标注模块
```

---

## 🎯 架构设计

### 分层架构

```
┌─────────────────────────────────────┐
│   watermark_app_pyqt6_ui.py        │  ← UI 层
│   (用户界面、事件处理)               │
└─────────────────┬───────────────────┘
                  │
                  │ 调用
                  ▼
┌─────────────────────────────────────┐
│   watermark_core.py                 │  ← 业务逻辑层
│   (数据模型、图像处理、配置管理)      │
└─────────────────┬───────────────────┘
                  │
                  │ 使用
                  ▼
┌─────────────────────────────────────┐
│   text_label_module.py              │  ← 功能模块
│   PIL/NumPy                         │
└─────────────────────────────────────┘
```

---

## 📦 核心模块 (watermark_core.py)

### 1. WatermarkLayer
**图层数据模型**

```python
class WatermarkLayer:
    """水印图层类"""
    - image_path: str         # 图片路径
    - image: PIL.Image        # 图片对象
    - opacity: int            # 不透明度 (0-100)
    - blend_mode: str         # 混合模式
    - visible: bool           # 可见性

    方法:
    - to_dict()              # 转换为字典（保存配置）
    - from_dict(data)        # 从字典创建图层
    - __str__()              # 字符串表示
```

### 2. WatermarkEngine
**图像处理引擎**

```python
class WatermarkEngine:
    """静态方法集合 - 图像处理"""

    @staticmethod
    apply_blend_mode(base, layer, mode, opacity)
    # 应用混合模式（Normal/Overlay/Screen/Soft Light）
    # 性能优化：Normal 模式使用 uint8，其他用 float32

    @staticmethod
    apply_multilayer_watermark(image, layers, stretch, callback)
    # 应用多图层水印
    # 支持进度回调
```

### 3. WatermarkConfig
**配置管理器**

```python
class WatermarkConfig:
    """配置文件的读写和管理"""

    属性:
    - last_used_directory
    - save_directory
    - last_watermark_directory
    - last_images_directory
    - last_stretch
    - last_images_files
    - layers
    - text_label_config

    方法:
    - load()                 # 从 JSON 加载配置
    - save(layers, config, stretch)  # 保存配置到 JSON
```

### 4. BatchProcessor
**批量处理器**

```python
class BatchProcessor:
    """静态方法 - 批量图像处理"""

    @staticmethod
    process_images(images, paths, layers, text_config,
                   save_dir, stretch, progress_cb, status_cb)
    # 批量处理图片
    # 应用水印和文本标注
    # 保存为 JPG
    # 返回 (success, message)
```

---

## 🎨 UI 模块 (watermark_app_pyqt6_ui.py)

### 1. CustomTitleBar
**自定义标题栏**

```python
class CustomTitleBar(QWidget):
    """无边框窗口的自定义标题栏"""

    信号:
    - close_requested
    - minimize_requested
    - maximize_restore_requested

    功能:
    - 拖动窗口
    - 最小化/最大化/关闭
    - 原神风格样式
```

### 2. MultiLayerWatermarkApp
**主应用窗口**

```python
class MultiLayerWatermarkApp(QMainWindow):
    """UI 界面层 - 负责显示和交互"""

    信号:
    - progress_update_signal(int)
    - status_update_signal(str)
    - processing_complete_signal(str, str)
    - processing_error_signal(str)

    主要方法:
    - create_ui()                    # 创建界面
    - create_*_section()             # 创建各个区域
    - add_watermark_layer()          # 添加图层
    - on_*_change()                  # 事件处理
    - apply_watermark_threaded()     # 线程处理
    - save_config()                  # 委托给 WatermarkConfig
```

---

## 🔄 数据流

### 启动流程

```
1. main()
   ↓
2. MultiLayerWatermarkApp.__init__()
   ↓
3. WatermarkConfig.load()          # 加载配置
   ↓
4. create_ui()                     # 创建界面
   ↓
5. auto_load_last_files()          # 自动加载文件
```

### 处理流程

```
1. 用户点击 "Apply Watermark"
   ↓
2. apply_watermark_threaded()       # UI 层
   ↓
3. _apply_watermark_task()          # 线程中
   ↓
4. BatchProcessor.process_images()  # 核心层
   ↓
5. WatermarkEngine.apply_multilayer_watermark()
   ↓
6. WatermarkEngine.apply_blend_mode()
   ↓
7. draw_text_label()                # 文本模块
   ↓
8. 保存 JPG 文件
   ↓
9. processing_complete_signal       # 回到 UI 层
```

---

## ✅ 优势

### 1. **可维护性**
- 业务逻辑和 UI 完全分离
- 每个类职责单一
- 易于定位和修复 bug

### 2. **可测试性**
```python
# 可以独立测试核心逻辑
from watermark_core import WatermarkEngine, WatermarkLayer

layer1 = WatermarkLayer("logo.png", 80, "overlay")
layer2 = WatermarkLayer("mark.png", 50, "screen")
result = WatermarkEngine.apply_multilayer_watermark(
    image, [layer1, layer2], stretch=False
)
```

### 3. **可扩展性**
- 添加新混合模式：只需修改 `WatermarkEngine`
- 更换 UI 框架：只需重写 UI 层，核心不变
- 添加新功能：清晰知道在哪个模块添加

### 4. **代码复用**
- 核心逻辑可被其他项目引用
- CLI 工具可以直接使用 `watermark_core`
- Web API 可以使用相同的核心

---

## 📝 使用示例

### 纯业务逻辑使用

```python
from watermark_core import WatermarkLayer, WatermarkEngine, BatchProcessor
from PIL import Image

# 创建图层
layer1 = WatermarkLayer("watermark1.png", 100, "normal")
layer2 = WatermarkLayer("watermark2.png", 50, "overlay")

# 加载图片
image = Image.open("photo.jpg")

# 应用水印
result = WatermarkEngine.apply_multilayer_watermark(
    image,
    [layer1, layer2],
    stretch=False
)

# 保存结果
result.save("output.jpg")
```

### UI 使用

```bash
# 用户直接运行 UI
python src/watermark_app_pyqt6_ui.py

# 或使用启动脚本
./run_pyqt6.sh
```

---

## 🔧 开发指南

### 添加新的混合模式

**修改文件**: `watermark_core.py`

```python
# 在 WatermarkEngine.apply_blend_mode() 中添加
elif blend_mode == 'multiply':
    result_rgb = base_rgb * blend_rgb
    result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
```

**修改文件**: `watermark_app_pyqt6_ui.py`

```python
# 在 create_layer_section() 中添加选项
self.blend_mode_combo.addItems([
    'normal', 'overlay', 'screen', 'soft_light', 'multiply'
])
```

### 添加新的 UI 区域

**修改文件**: `watermark_app_pyqt6_ui.py`

```python
def create_ui(self):
    # ...
    self.create_custom_section(right_column)  # 添加新区域

def create_custom_section(self, parent_layout):
    """创建自定义区域"""
    custom_group = QGroupBox("✦ Custom Settings")
    layout = QVBoxLayout(custom_group)
    # 添加组件...
    parent_layout.addWidget(custom_group)
```

### 添加新的配置项

**修改文件**: `watermark_core.py`

```python
class WatermarkConfig:
    def __init__(self):
        # ...
        self.custom_setting = "default_value"

    def load(self):
        # ...
        self.custom_setting = config.get('custom_setting', 'default')

    def save(self):
        config = {
            # ...
            'custom_setting': self.custom_setting
        }
```

---

## 🧪 测试

### 单元测试示例

```python
import unittest
from watermark_core import WatermarkLayer, WatermarkEngine
from PIL import Image
import numpy as np

class TestWatermarkEngine(unittest.TestCase):
    def test_blend_mode_normal(self):
        # 创建测试图像
        base = np.ones((100, 100, 4), dtype=np.uint8) * 128
        layer = np.ones((100, 100, 4), dtype=np.uint8) * 200

        # 应用混合模式
        result = WatermarkEngine.apply_blend_mode(
            base, layer, 'normal', 100
        )

        # 验证结果
        self.assertEqual(result.shape, (100, 100, 4))
        self.assertTrue(np.all(result[:,:,:3] > 128))
```

---

## 📊 代码统计

| 文件 | 行数 | 职责 |
|------|------|------|
| `watermark_core.py` | ~400 | 业务逻辑 |
| `watermark_app_pyqt6_ui.py` | ~1000 | UI 界面 |
| `text_label_module.py` | ~320 | 文本标注 |

**总计**: ~1720 行（原来单文件 1300+ 行）

---

## 🚀 未来扩展

### 可能的改进

1. **命令行工具**
```python
# cli.py
from watermark_core import *

def main():
    parser = argparse.ArgumentParser()
    # 添加命令行参数...
    # 使用 WatermarkEngine 处理
```

2. **Web API**
```python
# api.py
from flask import Flask
from watermark_core import WatermarkEngine

@app.route('/apply', methods=['POST'])
def apply_watermark():
    # 使用核心逻辑处理
    return result
```

3. **插件系统**
```python
# plugins/custom_blend.py
def register_blend_mode():
    WatermarkEngine.register_mode('custom', custom_blend_func)
```

---

## 📚 相关文档

- [PyQt6 Genshin Style Guide](PYQT6_GENSHIN_STYLE.md)
- [Quick Start Guide](../QUICKSTART_PYQT6.md)
- [Main README](../README.md)

---

*最后更新: 2025-11-20*
*架构版本: 2.0 (分层架构)*
