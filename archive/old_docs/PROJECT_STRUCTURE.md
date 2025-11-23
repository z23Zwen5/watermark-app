# 📁 WatermarkApp 项目结构说明

## 🎯 整理后的项目结构

```
watermarkApp/
├── 🚀 watermark_app.py              # 主启动文件（V1.5 Alpha保护版）
├── 📋 requirements.txt              # 主要依赖包
├── 📖 README.md                     # 项目说明文档
├── 📄 PROJECT_STRUCTURE.md          # 项目结构说明（本文件）
│
├── 📂 src/                          # 源代码目录
│   ├── watermark_app_multilayer.py         # V1.5 多图层混合模式水印（当前最新版本）
│   ├── watermark_app_smart_optimized.py    # V1.4 优化版智能水印
│   └── watermark_app_smart.py              # V1.3 基础智能水印
│
├── 📂 configs/                      # 配置文件目录
│   ├── multilayer_watermark_config.json          # 多图层版配置（最新）
│   ├── smart_watermark_optimized_config.json     # 优化版配置
│   ├── smart_watermark_config.json               # 基础智能版配置
│   ├── watermark_app_config.json                 # 基础版配置
│   └── requirements_smart.txt                    # 智能版依赖
│
├── 📂 tests/                        # 测试文件目录
│   ├── images/                      # 测试图片
│   │   ├── dark_test_*.png          # 暗色背景测试图片
│   │   ├── debug_test_*.png         # 调试测试图片
│   │   ├── test_black_watermark.png # 黑色水印测试
│   │   └── test_dark_image.png      # 暗色图片测试
│   ├── test_smart_watermark.py      # 智能水印算法测试
│   ├── performance_test.py          # 性能测试脚本
│   ├── test_2k_performance.py       # 2K分辨率性能测试
│   ├── simple_vectorized_test.py    # 简单向量化测试
│   └── performance_test_vectorized.py  # 向量化性能测试
│
├── 📂 versions/                     # 版本管理目录
│   └── watermark_app_v1.2.py       # V1.2基础版（已归档）
│
├── 📂 docs/                         # 文档目录
│   ├── MULTILAYER_GUIDE.md         # 多图层水印使用指南（最新）
│   ├── SMART_WATERMARK_ALGORITHM.md # 智能水印算法说明
│   ├── PERFORMANCE_SUMMARY.md      # 性能测试总结
│   ├── VERSION_HISTORY.md          # 版本历史
│   └── ... (其他文档)
│
├── 📂 releases/                     # 发布版本目录
│   ├── WatermarkApp_v1.1_优化版_分发包.zip
│   ├── WatermarkApp_v1.2_配置增强版_分发包.zip
│   └── WatermarkApp_v1.1_Distribution/
│
├── 📂 build/                        # 构建文件目录
│   ├── *.spec                       # PyInstaller规格文件
│   └── ... (构建缓存文件)
│
├── 📂 dist/                         # 编译输出目录
│   └── *.exe                        # 可执行文件
│
├── 📂 temp/                         # 临时文件目录
│   ├── create_test.py               # 临时测试脚本
│   └── test_alpha_protection.py     # 临时Alpha保护测试
│
├── 📂 tools/                        # 工具脚本目录
├── 📂 results/                      # 输出结果目录
├── 📂 assets/                       # 资源文件目录
├── 📂 test_images/                  # 额外测试图片目录
├── 📂 performance_test/             # 性能测试结果目录
├── 📂 alpha_protection_test/        # Alpha保护测试目录
└── 📂 archive/                      # 归档文件目录
    ├── watermark_app_alpha_protected.py       # V1.5 Alpha保护版（已归档）
    ├── alpha_protected_watermark_config.json  # Alpha保护版配置
    └── requirements_alpha_protected.txt       # Alpha保护版依赖
```

## 🎯 主要改进

### ✅ **已完成的整理**
1. **源代码集中**: 所有源代码移至 `src/` 目录
2. **配置统一管理**: 配置文件集中在 `configs/` 目录
3. **测试文件分类**: 测试脚本和测试图片分别组织
4. **版本管理**: 旧版本移至 `versions/` 目录
5. **清理重复文件**: 删除根目录中的重复文件
6. **主启动文件**: 创建统一的 `watermark_app.py` 启动入口

### 🔧 **配置文件路径更新**
- 配置文件已移动到 `configs/` 目录
- 主启动文件自动处理路径解析
- 保持向下兼容性

## 🚀 使用方法

### **启动应用**
```bash
# 启动最新版本（V1.5 多图层版）
python src/watermark_app_multilayer.py

# 或使用 Python 3
python3 src/watermark_app_multilayer.py
```

### **运行特定版本**
```bash
# V1.5 多图层混合模式版（推荐）⭐
python src/watermark_app_multilayer.py

# V1.4 优化版智能水印
python src/watermark_app_smart_optimized.py

# V1.3 基础智能版
python src/watermark_app_smart.py
```

### **运行测试**
```bash
# 性能测试
python tests/performance_test.py

# 智能算法测试
python tests/test_smart_watermark.py
```

## 📊 版本对比

| 版本 | 文件名 | 主要功能 | 推荐使用 |
|------|--------|----------|----------|
| **V1.5** | `watermark_app_multilayer.py` | 多图层 + 混合模式 + 智能颜色 | ⭐ **当前最新** |
| V1.4 | `watermark_app_smart_optimized.py` | 智能颜色 + 性能优化 | 高性能需求 |
| V1.3 | `watermark_app_smart.py` | 基础智能颜色调整 | 简单需求 |
| V1.2 | `versions/watermark_app_v1.2.py` | 基础水印功能 | 已归档 |
| ~V1.5 Alpha~ | `archive/watermark_app_alpha_protected.py` | Alpha保护版本 | 已归档 |

## 🛠️ 开发说明

### **添加新功能**
1. 在 `src/` 目录中创建新版本
2. 更新主启动文件 `watermark_app.py`
3. 添加相应的配置文件到 `configs/`
4. 创建测试文件到 `tests/`

### **创建发布版本**
1. 使用 `build/` 目录中的 `.spec` 文件
2. 输出到 `dist/` 目录
3. 打包到 `releases/` 目录

## 📝 注意事项

1. **配置文件**: 现在位于 `configs/` 目录，程序会自动寻找
2. **测试图片**: 统一存放在 `tests/images/` 目录
3. **主启动**: 始终使用 `watermark_app.py` 启动最新版本
4. **向下兼容**: 旧版本文件仍可独立运行

---

*整理完成时间: 2024年6月*  
*整理目标: 提高项目可维护性和开发效率* 