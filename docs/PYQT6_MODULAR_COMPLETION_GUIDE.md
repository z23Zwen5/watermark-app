# PyQt6 UI 模块化拆分完成指南

## 📊 当前进度

### ✅ 已完成部分

1. **目录结构** (100%)
```
src/ui/
├── __init__.py
├── styles/
│   ├── __init__.py
│   └── genshin_style.py       (326行)
├── components/
│   ├── __init__.py
│   ├── title_bar.py            (120行)
│   └── message_box.py          (174行)
└── main_window.py              (117行，框架版本）
```

2. **样式模块** - `ui/styles/genshin_style.py`
   - ✅ 颜色常量 (`Colors` 类)
   - ✅ 字体设置
   - ✅ 资源路径函数
   - ✅ 样式表类 (`GenshinStyleSheet`)
   - ✅ 全局样式应用函数

3. **组件模块** - `ui/components/`
   - ✅ `CustomTitleBar` - 自定义标题栏
   - ✅ `GenshinMessageBox` - 消息对话框

4. **入口文件** - `watermark_app_pyqt6_modular.py`
   - ✅ 主函数
   - ✅ 样式应用
   - ✅ 窗口创建和显示

### 🚧 待完成部分

#### Phase 1: 提取面板组件（预计 3-4小时）

需要从 `watermark_app_pyqt6_ui.py` 的 `MultiLayerWatermarkApp` 类中提取以下5个面板：

1. **UploadPanel** (`ui/panels/upload_panel.py`) - 约80行
2. **LayerPanel** (`ui/panels/layer_panel.py`) - 约200行
3. **SettingsPanel** (`ui/panels/settings_panel.py`) - 约60行
4. **TextLabelPanel** (`ui/panels/text_label_panel.py`) - 约150行
5. **OutputPanel** (`ui/panels/output_panel.py`) - 约100行

#### Phase 2: 完善主窗口（预计 1-2小时）

更新 `ui/main_window.py`，集成所有面板。

#### Phase 3: 测试与验证（预计 1小时）

- 功能完整性测试
- 与原版本对比测试

---

## 📝 详细拆分步骤

### Step 1: 创建 UploadPanel

**目标**: 处理图片上传功能

**位置**: `src/ui/panels/upload_panel.py`

**需要提取的代码段**（从 `watermark_app_pyqt6_ui.py`）:
- 图片选择按钮
- 图片路径显示
- 图片列表显示

**模板代码**:
```python
# ui/panels/upload_panel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QGroupBox
from PyQt6.QtCore import pyqtSignal
import qtawesome as qta
from ..styles import GenshinStyleSheet

class UploadPanel(QWidget):
    """图片上传面板"""
    images_selected = pyqtSignal(list)  # 发出选中的图片路径列表

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._create_ui()

    def _create_ui(self):
        group = QGroupBox("Upload Images")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)

        # 选择按钮
        btn_select = QPushButton()
        btn_select.setIcon(qta.icon('fa5s.file-upload', color='#3E3429'))
        btn_select.setText(" Select Images")
        btn_select.setStyleSheet(GenshinStyleSheet.get_button_style('primary'))
        btn_select.clicked.connect(self._select_images)
        vbox.addWidget(btn_select)

        # 路径显示
        self.lbl_path = QLabel("No images selected")
        vbox.addWidget(self.lbl_path)

    def _select_images(self):
        """选择图片"""
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            self.config.last_images_directory or "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if paths:
            self.lbl_path.setText(f"{len(paths)} images selected")
            self.images_selected.emit(paths)

    def load_files(self, paths):
        """加载文件（自动加载上次的文件）"""
        if paths:
            self.lbl_path.setText(f"{len(paths)} images loaded")
```

**提取来源**:
- 查找 `watermark_app_pyqt6_ui.py` 中第 527 行后的 `create_upload_section` 方法
- 复制 UI 创建代码
- 修改为使用相对导入和信号发射

---

### Step 2: 创建 LayerPanel

**目标**: 管理水印图层

**位置**: `src/ui/panels/layer_panel.py`

**核心功能**:
- 图层列表显示
- 添加/删除/移动图层
- 图层可见性切换
- 混合模式和透明度控制

**信号定义**:
```python
class LayerPanel(QWidget):
    layer_added = pyqtSignal(object)  # WatermarkLayer
    layer_removed = pyqtSignal(int)   # index
    layer_modified = pyqtSignal(int, dict)  # index, changes
    visibility_toggled = pyqtSignal(int)
    layer_moved = pyqtSignal(int, int)  # from_index, to_index
```

**提取来源**:
- `create_watermark_section` 方法
- 图层列表相关的所有事件处理方法

---

### Step 3: 创建 SettingsPanel

**目标**: 应用设置

**位置**: `src/ui/panels/settings_panel.py`

**核心功能**:
- 水印拉伸选项
- 其他全局设置

**信号定义**:
```python
class SettingsPanel(QWidget):
    stretch_changed = pyqtSignal(bool)
```

**提取来源**:
- 查找 stretch checkbox 相关代码

---

### Step 4: 创建 TextLabelPanel

**目标**: 文本标注配置

**位置**: `src/ui/panels/text_label_panel.py`

**核心功能**:
- 启用/禁用标注
- 标注类型选择（序号/文件名）
- 位置选择
- 字体大小和字体选择
- 自动对比色选项

**信号定义**:
```python
class TextLabelPanel(QWidget):
    config_changed = pyqtSignal(dict)  # 完整的 text_label 配置字典
```

**提取来源**:
- `create_text_label_section` 方法

---

### Step 5: 创建 OutputPanel

**目标**: 输出和处理控制

**位置**: `src/ui/panels/output_panel.py`

**核心功能**:
- 选择输出目录
- 进度条
- 状态显示
- 处理按钮

**信号定义**:
```python
class OutputPanel(QWidget):
    process_requested = pyqtSignal()
    directory_changed = pyqtSignal(str)
```

**提取来源**:
- `create_output_section` 方法
- 进度和状态更新方法

---

### Step 6: 创建 panels/__init__.py

```python
# ui/panels/__init__.py
"""UI Panels Package"""
from .upload_panel import UploadPanel
from .layer_panel import LayerPanel
from .settings_panel import SettingsPanel
from .text_label_panel import TextLabelPanel
from .output_panel import OutputPanel

__all__ = [
    'UploadPanel',
    'LayerPanel',
    'SettingsPanel',
    'TextLabelPanel',
    'OutputPanel'
]
```

---

### Step 7: 完善 main_window.py

将占位符替换为真实的面板：

```python
# ui/main_window.py
from .panels import (
    UploadPanel, LayerPanel, SettingsPanel,
    TextLabelPanel, OutputPanel
)

class MainWindow(QMainWindow):
    def _create_ui(self):
        # ... 前面代码保持不变 ...

        # 左列：上传 + 图层
        left_column = QVBoxLayout()
        left_column.setSpacing(20)

        self.upload_panel = UploadPanel(self.config)
        self.layer_panel = LayerPanel()

        left_column.addWidget(self.upload_panel)
        left_column.addWidget(self.layer_panel)

        # 右列：设置 + 文本标注 + 输出
        right_column = QVBoxLayout()
        right_column.setSpacing(20)

        self.settings_panel = SettingsPanel()
        self.text_label_panel = TextLabelPanel(self.config.text_label_config)
        self.output_panel = OutputPanel(self.config)

        right_column.addWidget(self.settings_panel)
        right_column.addWidget(self.text_label_panel)
        right_column.addStretch()
        right_column.addWidget(self.output_panel)

        # 添加到内容布局
        content_layout.addLayout(left_column, 55)
        content_layout.addLayout(right_column, 45)

    def _connect_signals(self):
        """连接所有信号"""
        # 标题栏
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_restore_requested.connect(self._toggle_maximize)

        # 上传面板
        self.upload_panel.images_selected.connect(self._on_images_selected)

        # 图层面板
        self.layer_panel.layer_added.connect(self._on_layer_added)
        self.layer_panel.layer_removed.connect(self._on_layer_removed)
        self.layer_panel.layer_modified.connect(self._on_layer_modified)

        # 设置面板
        self.settings_panel.stretch_changed.connect(self._on_stretch_changed)

        # 文本标注面板
        self.text_label_panel.config_changed.connect(self._on_text_label_changed)

        # 输出面板
        self.output_panel.process_requested.connect(self._start_processing)
        self.output_panel.directory_changed.connect(self._on_output_dir_changed)

        # 处理信号
        self.progress_update_signal.connect(self.output_panel.update_progress)
        self.status_update_signal.connect(self.output_panel.update_status)
```

---

## 🧪 测试清单

### 单元测试
- [ ] 每个面板可以独立创建和显示
- [ ] 样式正确应用
- [ ] 信号正确发射

### 集成测试
- [ ] 主窗口正常启动
- [ ] 所有面板正常显示
- [ ] 面板间信号通信正常

### 功能测试
- [ ] 图片选择功能
- [ ] 图层管理功能
- [ ] 文本标注配置
- [ ] 水印处理功能
- [ ] 配置保存和加载

### 对比测试
- [ ] 与 `watermark_app_pyqt6_ui.py` 功能一致
- [ ] 性能无明显降低
- [ ] 配置文件兼容

---

## 📦 最终结构

完成后的目录结构：

```
src/
├── ui/
│   ├── __init__.py           (5行)
│   ├── styles/
│   │   ├── __init__.py       (19行)
│   │   └── genshin_style.py  (326行)
│   ├── components/
│   │   ├── __init__.py       (8行)
│   │   ├── title_bar.py      (120行)
│   │   └── message_box.py    (174行)
│   ├── panels/
│   │   ├── __init__.py       (14行)
│   │   ├── upload_panel.py   (~80行)
│   │   ├── layer_panel.py    (~200行)
│   │   ├── settings_panel.py (~60行)
│   │   ├── text_label_panel.py (~150行)
│   │   └── output_panel.py   (~100行)
│   └── main_window.py        (~250行)
├── watermark_app_pyqt6_modular.py  (~30行)
├── watermark_core.py         (现有文件)
├── text_label_module.py      (现有文件)
└── watermark_app_pyqt6_ui.py (保留作为参考)
```

**代码量统计**:
- 原始文件: 1006行
- 拆分后总计: ~1500行 (增加约50%，因为增加了接口和文档)
- 但每个文件平均: ~100行（更易维护）

---

## 🚀 优势总结

### 1. 可维护性
- 每个文件职责单一，易于定位问题
- 修改一个功能不影响其他模块

### 2. 可测试性
- 每个面板可以独立测试
- 降低测试复杂度

### 3. 团队协作
- 多人可以并行开发不同面板
- 减少代码冲突

### 4. 可扩展性
- 添加新面板只需新增文件
- 不需要修改现有代码

### 5. 代码复用
- 样式统一管理
- 组件可以在不同项目中复用

---

## 📚 参考资料

1. **原始文件**: `src/watermark_app_pyqt6_ui.py`
2. **核心逻辑**: `src/watermark_core.py`
3. **文本模块**: `src/text_label_module.py`
4. **指南**: `docs/PYQT6_MODULAR_IMPLEMENTATION_GUIDE.md`

---

## ✅ 完成后的下一步

1. 删除或归档 `watermark_app_pyqt6_ui.py`
2. 更新 README.md
3. 添加单元测试
4. 优化性能
5. 编写API文档

---

**作者**: Claude Code
**日期**: 2025-11-20
**版本**: 1.0
