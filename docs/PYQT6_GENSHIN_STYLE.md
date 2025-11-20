# 🎨 PyQt6 Genshin Impact Style - Multi-Layer Watermark App

> **原神风格的精美水印应用 - PyQt6 版本**

---

## 📌 版本信息

- **应用版本**: v1.6.2 (PyQt6)
- **UI 框架**: PyQt6
- **设计风格**: Genshin Impact (原神)
- **创建日期**: 2025-11-20

---

## ✨ 新特性

### 🎨 原神美学设计

1. **颜色主题**
   - 金色主色调 (#D3BC8E, #BFA065) - 经典原神金色
   - 深色标题栏 (#2B3041) - 优雅深蓝
   - 柔和背景 (#F0F1F6, #ECE5D8) - 暖米色调

2. **视觉效果**
   - ✨ 渐变金色按钮 - 悬停发光效果
   - 🎯 圆角边框 (18px / 12px / 8px) - 柔和曲线
   - 💫 平滑过渡动画 (200-300ms ease-out)
   - 🌟 金色进度条 - 双向渐变
   - 📦 卡片式分组 - 阴影与层次感

3. **交互设计**
   - 按钮悬停金光效果
   - 选中项金色高亮
   - 自定义标题栏（可拖动）
   - 平滑滚动条

---

## 🚀 快速开始

### 方法 1: 使用启动脚本 (推荐)

#### Windows:
```bash
run_pyqt6.bat
```

#### Linux/macOS:
```bash
./run_pyqt6.sh
```

### 方法 2: 直接运行

```bash
python3 src/watermark_app_pyqt6.py
```

---

## 📦 安装依赖

### 完整安装

```bash
pip install -r requirements_pyqt6.txt
```

### 手动安装

```bash
pip install PyQt6>=6.4.0
pip install qtawesome>=1.2.0
pip install Pillow>=9.0.0
pip install numpy>=1.20.0
```

---

## 🎯 功能对比

| 功能 | Tkinter 版本 | PyQt6 版本 | 说明 |
|------|-------------|-----------|------|
| 多图层水印 | ✅ | ✅ | 完全兼容 |
| 混合模式 | ✅ | ✅ | Normal/Overlay/Screen/Soft Light |
| 图层可见性 | ✅ | ✅ | 眼睛图标切换 |
| 文本标注 | ✅ | ✅ | 序号/文件名 |
| 系统字体 | ✅ | ✅ | 自动扫描 |
| 百分比字体 | ✅ | ✅ | 相对图片高度 |
| 自定义标题栏 | ❌ | ✅ | 无边框窗口 |
| 拖动窗口 | ✅ (系统) | ✅ (自定义) | 标题栏拖动 |
| 图标支持 | ❌ | ✅ | Font Awesome |
| 渐变效果 | ❌ | ✅ | QSS 渐变 |
| 平滑动画 | ❌ | ✅ | CSS transitions |
| 高 DPI | ⚠️ | ✅ | 完美支持 |

---

## 🎨 UI 设计参数

### 颜色方案

#### 主色调
```css
/* 金色系列 */
#D3BC8E  /* 亮金色 - 主要元素 */
#BFA065  /* 深金色 - 边框、强调 */
#FFE0B3  /* 浅金色 - 悬停效果 */
#FFF8E1  /* 极浅金 - 按压效果 */

/* 背景色 */
#F0F1F6  /* 主背景 - 浅灰 */
#ECE5D8  /* 卡片背景 - 暖米色 */
#FFFFFF  /* 输入框背景 - 纯白 */

/* 文字色 */
#1C2333  /* 主文字 - 深蓝 */
#2B3041  /* 次要文字 - 灰蓝 */
#666666  /* 提示文字 - 灰色 */
```

#### 特殊颜色
```css
/* 标题栏渐变 */
qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop:0 #2B3041, stop:1 #3A4158)

/* 按钮渐变 */
qlineargradient(x1:0, y1:0, x2:0, y2:1,
    stop:0 #D3BC8E, stop:1 #BFA065)
```

### 圆角半径
```css
18px  /* 主窗口、大卡片 */
12px  /* 分组框、中等元素 */
8px   /* 按钮、输入框、小元素 */
4px   /* 复选框、滑块手柄 */
```

### 间距规范
```css
/* 边距 */
20px  /* 主容器内边距 */
15px  /* 分组框内边距 */
10px  /* 元素间距 */
8px   /* 按钮组间距 */
5px   /* 紧密元素间距 */

/* 元素高度 */
40px  /* 标题栏 */
36px  /* 标准按钮 */
45px  /* 主操作按钮 */
30px  /* 输入框/下拉框 */
25px  /* 进度条 */
```

---

## 🖼️ UI 布局结构

```
┌─────────────────────────────────────────┐
│  🎨 [标题栏] Multi-Layer Watermark  [-][□][×]│ ← 自定义标题栏
├─────────────────────────────────────────┤
│                                         │
│  Multi-Layer Watermark Tool             │ ← 应用标题
│  🎨 Multi-Layer with Blend Modes        │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 📁 File Upload                    │ │
│  │  [Upload Images] 🖼️               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 🎨 Watermark Layers               │ │
│  │  💡 Larger layer numbers on top   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │ [1] 👁️ logo.png (normal, 100%) │ │ ← 图层列表
│  │  │ [2] 👁️ mark.png (overlay, 80%) │ │
│  │  └─────────────────────────────┘ │ │
│  │  [Add] [Toggle] [Remove] [↑] [↓]  │ │
│  │  ┌─ Layer Properties ────────┐   │ │
│  │  │ Blend Mode: [normal ▼]     │   │ │
│  │  │ Opacity (%): [100] ━━━━●─  │   │ │
│  │  └───────────────────────────┘   │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ ⚙️ Settings                       │ │
│  │  ☑ Stretch watermark to fit      │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ 🔤 Text Label (文字标注)          │ │
│  │  ☑ Enable text label              │ │
│  │  Label Type: [number ▼]           │ │
│  │  Position: [bottom_right ▼]       │ │
│  │  Orientation: [horizontal ▼]      │ │
│  │  Font: [(Auto) ▼]                 │ │
│  │  Font Size: ━━━●───── 3.0%        │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45%      │ ← 进度条
│  Ready to process                      │
│                                         │
│  [Select Save Directory] /path/to/dir  │
│                                         │
│  [🚀 Apply Multi-Layer Watermark]      │ ← 主按钮
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔧 技术实现

### 核心技术栈

```python
# UI 框架
PyQt6           # 现代化 GUI 框架
qtawesome       # Font Awesome 图标库

# 图像处理
Pillow (PIL)    # 图像处理
NumPy           # 数值计算

# 系统集成
json            # 配置管理
threading       # 多线程处理
```

### 关键特性实现

#### 1. 自定义标题栏

```python
class CustomTitleBar(QWidget):
    """无边框窗口的自定义标题栏"""
    - 拖动功能 (mousePressEvent/mouseMoveEvent)
    - 最小化/最大化/关闭按钮
    - 标题显示与图标
    - 原神风格样式
```

#### 2. QSS 样式系统

```python
def apply_genshin_style(self):
    """应用原神风格的 QSS"""
    - 渐变背景 (qlineargradient)
    - 圆角边框 (border-radius)
    - 悬停效果 (:hover)
    - 按压效果 (:pressed)
    - 禁用状态 (:disabled)
```

#### 3. 信号与槽机制

```python
# 线程安全的 UI 更新
progress_update_signal = pyqtSignal(int)
status_update_signal = pyqtSignal(str)
processing_complete_signal = pyqtSignal(str, str)

# 连接到 UI 更新方法
self.progress_update_signal.connect(self.update_progress_bar)
```

#### 4. 混合模式算法 (保留原版)

```python
def apply_blend_mode(self, base, layer, mode, opacity):
    """
    Photoshop 标准混合模式
    - Normal: uint8 优化 (2x faster)
    - Overlay/Screen/Soft Light: float32 精确计算
    """
```

---

## 🎯 使用指南

### 基本工作流程

1. **上传图片** 📁
   - 点击 "Upload Images" 按钮
   - 选择一张或多张图片 (JPG/PNG)

2. **添加水印图层** 🎨
   - 点击 "Add" 按钮添加水印
   - 支持多个图层（按序号叠加）

3. **调整图层属性** ⚙️
   - 选中图层查看属性
   - 调整混合模式（normal/overlay/screen/soft_light）
   - 调整不透明度（0-100%）
   - 切换可见性（👁️ 图标）

4. **配置文本标注** 🔤 (可选)
   - 启用文本标注复选框
   - 选择类型（序号/文件名）
   - 设置位置、方向、字体、大小

5. **选择保存目录** 💾
   - 点击 "Select Save Directory"
   - 选择输出文件夹

6. **应用水印** 🚀
   - 点击主按钮 "Apply Multi-Layer Watermark"
   - 等待进度条完成
   - 查看输出文件（*_multilayer.jpg）

---

## 🌟 高级功能

### 图层管理

#### 图层顺序
- 数字大的图层在上方（覆盖下层）
- 使用 ↑↓ 按钮调整顺序

#### 图层可见性
- 👁️ = 可见，🚫 = 隐藏
- 点击 "Toggle" 切换当前图层
- 隐藏的图层不参与渲染（性能优化）

#### 混合模式详解

```
Normal      - 标准叠加（最快，uint8 优化）
Overlay     - 叠加模式（增强对比度）
Screen      - 滤色模式（提亮效果）
Soft Light  - 柔光模式（柔和混合）
```

### 文本标注

#### 字体大小（百分比）
```
1080p (1920×1080): 3% = 32px
4K (3840×2160):    3% = 64px
8K (7680×4320):    3% = 128px
```

#### 方向选项
- **Horizontal**: 横向文字（默认）
- **Vertical**: 纵向文字（每字一行）

---

## 🔍 与 Tkinter 版本对比

### 优势 ✅

1. **更美观的界面**
   - 原神风格设计
   - 专业渐变与阴影
   - 自定义标题栏

2. **更好的用户体验**
   - Font Awesome 图标
   - 平滑动画过渡
   - 高 DPI 完美支持

3. **更强大的样式系统**
   - QSS (类似 CSS)
   - 灵活的主题定制
   - 状态管理 (hover/pressed)

4. **更现代的架构**
   - 信号与槽机制
   - 更好的线程安全
   - 更清晰的代码结构

### 劣势 ⚠️

1. **依赖更重**
   - PyQt6 包体积大（~120MB）
   - Tkinter 是 Python 内置

2. **学习曲线**
   - QSS 语法需要学习
   - 信号槽机制更复杂

3. **启动略慢**
   - PyQt6 初始化时间更长
   - Tkinter 启动更快

---

## 🐛 常见问题

### Q1: 窗口无法拖动？
**A**: 确保在标题栏区域拖动，不是内容区域。

### Q2: 图标不显示？
**A**: 检查 `qtawesome` 是否正确安装：
```bash
pip install qtawesome --upgrade
```

### Q3: 高 DPI 模糊？
**A**: 代码已自动启用高 DPI 支持：
```python
app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
```

### Q4: 无法最大化/最小化？
**A**: 检查标题栏按钮是否响应，尝试重启应用。

### Q5: 样式加载失败？
**A**: 检查 QSS 语法，确保没有特殊字符冲突。

---

## 📝 配置文件

与 Tkinter 版本**完全兼容**，使用相同的配置文件：

```json
configs/multilayer_watermark_config.json
```

配置包含：
- 上次使用的目录
- 图层信息（路径、不透明度、混合模式、可见性）
- 文本标注设置
- 拉伸选项

---

## 🎨 自定义主题

### 修改颜色主题

编辑 `apply_genshin_style()` 方法中的 QSS：

```python
def apply_genshin_style(self):
    self.setStyleSheet("""
        /* 修改金色为蓝色 */
        QGroupBox {
            color: #88E0E6;  /* 风元素蓝 */
            border: 2px solid #98D1EC;
        }

        QPushButton {
            background: qlineargradient(
                stop:0 #88E0E6, stop:1 #98D1EC);
        }
    """)
```

### 元素颜色对照表

```
原神元素色：
风 (Anemo):  #88E0E6
岩 (Geo):    #D3BC8E (当前使用)
雷 (Electro): #D390EA
水 (Hydro):  #98D1EC
火 (Pyro):   #FF9999
冰 (Cryo):   #99CCFF
草 (Dendro): #99FF99
```

---

## 📚 开发文档

### 添加新功能

1. **UI 组件**
```python
def create_custom_section(self):
    group = QGroupBox("⭐ Custom Section")
    layout = QVBoxLayout(group)
    # 添加组件...
    self.content_layout.addWidget(group)
```

2. **样式定制**
```python
# 在 apply_genshin_style() 中添加
"""
QWidget#CustomWidget {
    background-color: #F0F1F6;
    border: 2px solid #D3BC8E;
    border-radius: 12px;
}
"""
```

3. **事件处理**
```python
def on_custom_button_click(self):
    # 处理逻辑
    self.save_config()  # 保存配置
```

---

## 🚀 性能优化

### 已实现的优化

1. **混合模式**
   - Normal 模式使用 uint8 直接计算 (2x faster)
   - 其他模式使用 float32 保证精度

2. **图层渲染**
   - 跳过不可见图层
   - NumPy 向量化计算
   - BILINEAR 缩放（速度 vs 质量平衡）

3. **UI 响应**
   - 多线程处理（避免冻结）
   - 信号槽异步更新
   - 进度条实时反馈

---

## 📄 许可证

与主项目相同，遵循 MIT License。

---

## 🤝 贡献

欢迎提交问题和改进建议！

- **报告 Bug**: 在 GitHub Issues 中提交
- **功能建议**: 描述您的想法和用例
- **代码贡献**: Fork 项目并提交 Pull Request

---

## 📮 联系方式

- **项目**: Multi-Layer Watermark App
- **版本**: v1.6.2 (PyQt6 Genshin Style)
- **更新**: 2025-11-20

---

**享受原神风格的水印体验！** ✨🎮

