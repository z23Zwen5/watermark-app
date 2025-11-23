# 🚀 启动性能分析报告

## 📊 问题总结

Build 后的应用启动过慢，主要有 **4 个性能瓶颈**：

### 🔴 关键问题（启动时间 +2-5 秒）

1. **PyInstaller onefile 解压开销** ⚠️ 最严重
2. **启动时加载水印图层图片**
3. **系统字体扫描**
4. **自动加载上次打开的图片**

---

## 🔍 详细分析

### 1️⃣ PyInstaller onefile 解压开销 ⚠️

**位置**: `tools/build_with_icon.py:45` & `tools/build_multilayer.bat:98`

```python
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",  # ← 问题根源
    "--windowed",
    ...
]
```

**问题**:
- `--onefile` 将所有依赖打包到单个 .exe 中（~50-100 MB）
- **每次启动**时，PyInstaller 会：
  1. 解压整个程序到临时目录（`%TEMP%/_MEIxxxxxx`）
  2. 加载所有 DLL（Pillow, NumPy, tkinter）
  3. 初始化 Python 运行时
- 典型延迟：**2-4 秒**（取决于磁盘速度）

**证据**:
- Windows: 查看 `C:\Users\<用户>\AppData\Local\Temp\_MEI*` 目录
- 每次启动都会创建新的临时目录

---

### 2️⃣ 启动时加载水印图层图片

**位置**: `src/watermark_core.py:16-18` & `watermark_core.py:216`

```python
# WatermarkLayer.__init__
def __init__(self, image_path, opacity=100, blend_mode='normal', visible=True):
    self.image_path = image_path
    self.image = Image.open(image_path).convert("RGBA")  # ← 立即加载
    ...

# WatermarkConfig.load()
for layer_info in layers_info:
    if os.path.exists(layer_info['path']):
        layer = WatermarkLayer.from_dict(layer_info)  # ← 触发 Image.open
        self.layers.append(layer)
```

**问题**:
- 配置中有 3 个图层 → 启动时立即打开 3 张高清图片
- 每张图片解码耗时：50-200ms（取决于分辨率和格式）
- 总延迟：**150-600ms**

**为什么这是问题**:
- 用户可能根本不需要处理图片（只是打开应用查看配置）
- 水印图片在真正处理时才需要加载

---

### 3️⃣ 系统字体扫描

**位置**: `src/text_label_module.py:19-91`

```python
def scan_system_fonts():
    """扫描系统已安装字体"""
    # Windows: C:/Windows/Fonts (通常有 200-500 个字体文件)
    # macOS: /Library/Fonts, /System/Library/Fonts
    # Linux: /usr/share/fonts

    for font_dir in font_dirs:
        for root, dirs, files in os.walk(font_dir):  # ← 递归扫描
            for file in files:
                if file.lower().endswith(('.ttf', '.ttc', '.otf')):
                    ...
```

**触发位置**: `src/watermark_app_multilayer.py:326`

```python
def create_text_label_section(self, parent):
    ...
    from text_label_module import get_system_fonts
    system_fonts = get_system_fonts()  # ← UI 创建时立即扫描
    font_names = sorted(system_fonts.keys())
```

**问题**:
- 典型系统有 200-500 个字体文件
- 需要递归扫描多个目录（Windows 至少 2 个）
- 典型延迟：**300-800ms**（取决于字体数量和磁盘速度）

**虽然有缓存，但首次扫描仍在启动时发生**

---

### 4️⃣ 自动加载上次打开的图片

**位置**: `src/watermark_app_multilayer.py:849-864`

```python
def auto_load_last_files(self):
    """自动加载文件"""
    if self.last_images_files:
        valid_files = [f for f in self.last_images_files if os.path.exists(f)]
        if valid_files:
            self.images = [Image.open(file_path) for file_path in valid_files]  # ← 立即加载
            ...
```

**调用位置**: `src/watermark_app_multilayer.py:75`

```python
class MultiLayerWatermarkApp:
    def __init__(self, root):
        ...
        self.create_ui()
        self.auto_load_last_files()  # ← 初始化时立即调用
```

**问题**:
- 用户上次打开了 10 张 4K 图片 → 启动时全部解码
- 每张 4K 图片解码：100-300ms
- 总延迟：**1-3 秒**（取决于图片数量和大小）

---

## 💡 优化方案

### ✅ 方案 1：改用 onedir 模式 **（推荐，立竿见影）**

**修改 Build 脚本**:

```python
# tools/build_with_icon.py
cmd = [
    sys.executable, "-m", "PyInstaller",
    # "--onefile",  # ← 移除
    "--onedir",     # ← 改用目录模式
    "--windowed",
    ...
]
```

**优势**:
- ✅ 启动速度提升 **2-4 秒**
- ✅ 不需要每次解压
- ✅ DLL 加载更快

**劣势**:
- ❌ 分发时是一个文件夹（而非单个 exe）
- ❌ 需要打包整个文件夹分发

**适用场景**:
- 个人使用 / 团队内部使用
- 不需要单文件便携性

---

### ✅ 方案 2：延迟加载图层图片 **（推荐）**

**修改 WatermarkLayer**:

```python
# src/watermark_core.py
class WatermarkLayer:
    def __init__(self, image_path, opacity=100, blend_mode='normal', visible=True):
        self.image_path = image_path
        self._image = None  # ← 延迟加载
        self.opacity = int(opacity)
        self.blend_mode = blend_mode
        self.visible = visible
        self.name = os.path.basename(image_path)

    @property
    def image(self):
        """懒加载图片（第一次访问时才打开）"""
        if self._image is None:
            self._image = Image.open(self.image_path).convert("RGBA")
        return self._image
```

**优势**:
- ✅ 启动时不加载图片
- ✅ 仅在真正处理时才加载
- ✅ 代码改动极小（使用 property）

**节省时间**: **150-600ms**

---

### ✅ 方案 3：异步字体扫描 **（推荐）**

**修改字体加载逻辑**:

```python
# src/text_label_module.py
import threading

_SYSTEM_FONTS_CACHE = None
_FONTS_LOADING = False

def get_system_fonts():
    """获取系统字体（异步加载）"""
    global _SYSTEM_FONTS_CACHE, _FONTS_LOADING

    if _SYSTEM_FONTS_CACHE is None and not _FONTS_LOADING:
        _FONTS_LOADING = True
        # 启动后台线程扫描
        threading.Thread(target=_scan_fonts_background, daemon=True).start()
        # 返回默认字体列表
        return {'Arial': None, 'Default': None}

    return _SYSTEM_FONTS_CACHE or {'Arial': None}

def _scan_fonts_background():
    global _SYSTEM_FONTS_CACHE, _FONTS_LOADING
    print("🔍 后台扫描系统字体...")
    _SYSTEM_FONTS_CACHE = scan_system_fonts()
    _FONTS_LOADING = False
    print(f"✅ 找到 {len(_SYSTEM_FONTS_CACHE)} 个字体")
```

**UI 部分**:

```python
# src/watermark_app_multilayer.py
def create_text_label_section(self, parent):
    ...
    # 先显示默认字体，后台扫描完成后刷新
    system_fonts = get_system_fonts()
    font_names = sorted(system_fonts.keys())

    font_combo = ttk.Combobox(..., values=['(Auto)'] + font_names, ...)

    # 注册刷新回调（扫描完成后更新下拉框）
    self.root.after(500, self._refresh_font_list)

def _refresh_font_list(self):
    """刷新字体列表（字体扫描完成后调用）"""
    from text_label_module import get_system_fonts
    system_fonts = get_system_fonts()
    if len(system_fonts) > 2:  # 扫描完成
        font_names = sorted(system_fonts.keys())
        self.label_font_combo['values'] = ['(Auto)'] + font_names
    else:
        self.root.after(500, self._refresh_font_list)  # 继续等待
```

**优势**:
- ✅ 启动时不阻塞
- ✅ 用户仍可使用默认字体
- ✅ 字体列表后台填充

**节省时间**: **300-800ms**

---

### ✅ 方案 4：移除自动加载图片（或改为可选）**（推荐）**

**方案 A：完全移除**

```python
# src/watermark_app_multilayer.py
def __init__(self, root):
    ...
    self.create_ui()
    # self.auto_load_last_files()  # ← 移除
```

**方案 B：改为手动触发**

```python
def create_ui(self):
    ...
    # 添加"加载上次文件"按钮
    reload_btn = tk.Button(..., text="Load Last Session",
                          command=self.auto_load_last_files)
```

**方案 C：延迟 500ms 后台加载**

```python
def __init__(self, root):
    ...
    self.create_ui()
    # 延迟加载，不阻塞启动
    self.root.after(500, self.auto_load_last_files)
```

**优势**:
- ✅ 启动速度大幅提升
- ✅ 用户可按需加载

**节省时间**: **1-3 秒**（取决于图片数量）

---

## 📈 预期效果

### 当前启动时间（onefile）
```
PyInstaller 解压:     2-4 秒  ⚠️
加载水印图层:          0.5 秒
扫描系统字体:          0.6 秒
自动加载图片:          2 秒
───────────────────────────────
总计:                 5-7 秒  ❌
```

### 优化后启动时间（应用所有方案）
```
PyInstaller onedir:   0.5 秒  ✅ (改用 onedir)
延迟加载图层:          0 秒    ✅ (懒加载)
异步扫描字体:          0 秒    ✅ (后台线程)
移除自动加载:          0 秒    ✅ (按需加载)
───────────────────────────────
总计:                 0.5 秒  ✅ (提速 10-14x)
```

**如果保留 onefile 模式**（仅应用方案 2-4）:
```
总计:                 2.5 秒  ✅ (提速 2-3x)
```

---

## 🎯 推荐实施顺序

### 阶段 1: 快速优化（30 分钟）
1. ✅ **方案 4C**: 延迟 500ms 加载上次文件（改 1 行代码）
2. ✅ **方案 2**: 延迟加载图层图片（改 WatermarkLayer 类）

**预期效果**: 启动时间减少 **2-3 秒**

---

### 阶段 2: 深度优化（1-2 小时）
3. ✅ **方案 3**: 异步字体扫描（改 text_label_module + UI）
4. ✅ **方案 1**: 改用 onedir 模式（修改 build 脚本）

**预期效果**: 启动时间减少到 **0.5-1 秒**

---

## 🛠️ 测试建议

### 测试脚本

```python
# test_startup_time.py
import time
import subprocess

def test_startup():
    times = []
    for i in range(5):
        start = time.time()
        # 启动应用，等待窗口出现后立即关闭
        subprocess.run(['dist/WatermarkApp_v1.6.exe'], timeout=10)
        end = time.time()
        times.append(end - start)

    print(f"平均启动时间: {sum(times)/len(times):.2f} 秒")
    print(f"最快启动: {min(times):.2f} 秒")
    print(f"最慢启动: {max(times):.2f} 秒")
```

### 手动测试
1. 清理临时目录 `%TEMP%\_MEI*`
2. 用秒表测量从双击到窗口完全显示的时间
3. 重复 5 次取平均值

---

## 📝 其他建议

### 1. 添加启动性能监控

```python
# src/watermark_app_multilayer.py
import time

class MultiLayerWatermarkApp:
    def __init__(self, root):
        start_time = time.time()

        self.root = root
        print(f"[{time.time()-start_time:.3f}s] Root initialized")

        self.config = WatermarkConfig()
        self.config.load()
        print(f"[{time.time()-start_time:.3f}s] Config loaded")

        self.create_ui()
        print(f"[{time.time()-start_time:.3f}s] UI created")

        # self.auto_load_last_files()
        print(f"[{time.time()-start_time:.3f}s] Startup complete")
```

### 2. 考虑使用 Nuitka（替代 PyInstaller）

- Nuitka 将 Python 编译为 C，启动更快
- 但构建时间更长，配置更复杂

### 3. 添加启动画面（如果无法优化）

```python
# 启动时显示 splash screen，隐藏加载延迟
import tkinter as tk

class SplashScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # 无边框
        tk.Label(self.root, text="Loading...", font=('Arial', 20)).pack()
        self.root.update()

    def destroy(self):
        self.root.destroy()
```

---

## ✅ 总结

### 核心问题
- **PyInstaller onefile** 是最大瓶颈（2-4 秒）
- **启动时加载所有资源** 是次要问题（2-3 秒）

### 最佳方案
1. **改用 onedir** → 立即提速 2-4 秒
2. **延迟加载图层/图片** → 再提速 2-3 秒
3. **异步字体扫描** → 再提速 0.5-1 秒

**最终效果**: 从 **5-7 秒** 降至 **0.5-1 秒** 🚀

---

*分析完成时间: 2025-11-23*
*分析工具: Claude Code*
