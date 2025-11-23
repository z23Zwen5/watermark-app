# 📦 构建脚本对比说明

## 脚本列表

### 🚀 优化版（推荐）
- `build_multilayer_optimized.bat` (Windows)
- `build_multilayer_optimized.sh` (Linux/macOS)

**特点**:
- ✅ **onedir** 模式 - 启动速度提升 2-4 秒
- ✅ 移除不必要的隐藏导入
- ✅ 添加 `--noupx` 避免压缩延迟
- ✅ 自动生成快速启动说明

**适用场景**:
- 🎯 **优先推荐** - 适合大多数场景
- 个人使用
- 团队内部分发
- 追求最快启动速度

### 📦 原版（向后兼容）
- `build_multilayer.bat` (Windows)
- `build_multilayer.sh` (Linux/macOS)
- `build_with_icon.py` (跨平台)

**特点**:
- 📄 **onefile** 模式 - 单文件分发
- 包含更多隐藏导入
- 完整的依赖检查

**适用场景**:
- 需要单文件分发
- 网络下载分享
- 便携使用（U盘）

---

## 性能对比

| 指标 | 原版 (onefile) | 优化版 (onedir) |
|------|---------------|----------------|
| **启动时间** | 5-7 秒 | 0.5-1 秒 ⚡ |
| **首次解压** | 每次启动 | 无需解压 ✓ |
| **文件大小** | ~50-100 MB (单文件) | ~100-150 MB (文件夹) |
| **分发方式** | 单个 .exe | 整个文件夹 |
| **便携性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **性能** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 使用方法

### Windows 用户

**优化版（推荐）**:
```cmd
cd tools
build_multilayer_optimized.bat
```

**原版**:
```cmd
cd tools
build_multilayer.bat
```

### Linux/macOS 用户

**优化版（推荐）**:
```bash
cd tools
./build_multilayer_optimized.sh
```

**原版**:
```bash
cd tools
./build_multilayer.sh
```

---

## 构建输出

### 优化版输出结构

```
dist/
└── WatermarkApp_v1.6.2_Optimized/
    ├── WatermarkApp_v1.6.2_Optimized.exe  # 主程序
    ├── _internal/                          # 依赖库
    │   ├── PIL/
    │   ├── numpy/
    │   ├── tkinter/
    │   └── ...
    └── README_快速开始.txt                 # 使用说明
```

**分发方式**:
1. 压缩整个 `WatermarkApp_v1.6.2_Optimized` 文件夹为 .zip
2. 分发给用户
3. 用户解压后双击 `.exe` 运行

### 原版输出结构

```
dist/
└── MultiLayerWatermark_v1.5.exe  # 单个文件
```

**分发方式**:
1. 直接分发单个 `.exe` 文件
2. 用户双击运行（首次启动会较慢）

---

## 何时使用哪个版本？

### 使用优化版（推荐大多数情况）

✅ **推荐场景**:
- 频繁使用，注重启动速度
- 本地安装使用
- 团队内部分发
- 不介意文件夹分发

### 使用原版

✅ **推荐场景**:
- 需要通过网络分享（单文件更方便）
- 便携使用（U盘、云盘）
- 不经常启动（偶尔使用）
- 分发给非技术用户（单文件更简单）

---

## 性能优化说明

详细的性能分析和优化方案请查看:
📄 [STARTUP_PERFORMANCE_ANALYSIS.md](../docs/STARTUP_PERFORMANCE_ANALYSIS.md)

### 关键优化点

1. **onedir vs onefile**
   - onefile: 每次启动解压到临时目录（2-4秒）
   - onedir: 直接运行，无需解压（0.1秒）

2. **移除冗余隐藏导入**
   - 原版: 手动指定 `--hidden-import numpy/PIL/tkinter/json`
   - 优化版: 让 PyInstaller 自动检测（避免过度导入）

3. **添加 --noupx**
   - 避免 UPX 压缩带来的额外解压时间
   - 稍微增加文件大小，但大幅提升启动速度

---

## 进一步优化

构建脚本只能优化到这里（2-4秒提升）。

要进一步提升到 **0.5-1秒**，需要代码层面优化：
- 延迟加载水印图层
- 异步字体扫描
- 可选的自动加载图片

详见: [STARTUP_PERFORMANCE_ANALYSIS.md](../docs/STARTUP_PERFORMANCE_ANALYSIS.md)

---

## 常见问题

### Q: 为什么优化版启动这么快？
A: onedir 模式不需要每次启动时解压，DLL 直接加载，节省 2-4 秒。

### Q: 优化版文件更大了？
A: 是的，但这是用空间换时间。实际增加不到 50MB，对现代硬盘可忽略。

### Q: 能否同时拥有单文件和快速启动？
A: 不能，这是 PyInstaller 的限制。单文件必须先解压才能运行。

### Q: 杀毒软件会拦截吗？
A: 两个版本都可能被拦截（PyInstaller 通病）。解决方法：
   - 添加到白名单
   - 使用代码签名证书

---

*创建时间: 2025-11-23*
*版本: v1.6.2*
