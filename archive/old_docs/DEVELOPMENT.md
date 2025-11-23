# 🔧 开发指南

## 🚀 快速开始

### 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd watermarkApp

# 安装依赖
pip install -r requirements.txt
```

### 运行应用
```bash
# 运行优化版本（推荐）
python src/watermark_app_optimized.py

# 运行基础版本
python src/watermark_app.py

# 或使用批处理文件（Windows）
run_optimized.bat  # 优化版本
run_basic.bat      # 基础版本
```

## 📁 项目结构

```
watermarkApp/
├── src/                    # 源代码
├── docs/                   # 文档
├── releases/               # 发布版本
├── assets/                 # 资源文件
├── build/                  # 构建文件
├── dist/                   # 编译输出
├── requirements.txt        # 依赖包
└── README.md              # 项目说明
```

## 🔨 开发流程

### 1. 代码开发
- 在 `src/` 目录中编写代码
- 遵循Python PEP8编码规范
- 添加必要的注释和文档字符串

### 2. 测试
```bash
# 运行应用测试功能
python src/watermark_app_optimized.py

# 测试不同场景
# - 单张图片处理
# - 批量图片处理
# - 不同透明度设置
# - 并行处理开关
```

### 3. 文档更新
- 更新相关文档在 `docs/` 目录
- 更新版本历史 `docs/VERSION_HISTORY.md`
- 更新README.md

### 4. 打包发布
```bash
# 打包优化版本
pyinstaller --onefile --windowed \
  --name "WatermarkApp_v1.1_Optimized" \
  --icon=assets/watermark_app_icon.ico \
  --noconsole src/watermark_app_optimized.py

# 打包基础版本
pyinstaller --onefile --windowed \
  --name "WatermarkApp_v1.0" \
  --icon=assets/watermark_app_icon.ico \
  --noconsole src/watermark_app.py
```

## 🎯 代码规范

### Python代码风格
- 使用4个空格缩进
- 行长度不超过88字符
- 函数和类使用文档字符串
- 变量命名使用snake_case
- 类命名使用PascalCase

### 注释规范
```python
def apply_watermark_optimized(self, image, watermark, opacity, stretch=False):
    """优化的水印应用函数，使用numpy进行快速像素操作
    
    Args:
        image: PIL图像对象
        watermark: 水印图像对象
        opacity: 透明度 (0.0-1.0)
        stretch: 是否拉伸水印
        
    Returns:
        处理后的图像对象
    """
```

## 🧪 测试指南

### 功能测试
1. **基础功能测试**
   - 图片上传
   - 水印上传
   - 透明度调整
   - 保存功能

2. **性能测试**
   - 单张图片处理时间
   - 批量图片处理时间
   - 内存使用情况
   - CPU使用率

3. **兼容性测试**
   - 不同图片格式 (JPG, PNG)
   - 不同图片尺寸
   - 不同水印尺寸

### 性能基准测试
```python
# 创建性能测试脚本
import time
import numpy as np
from PIL import Image

def performance_test():
    # 测试代码
    start_time = time.time()
    # ... 处理逻辑
    end_time = time.time()
    print(f"处理时间: {end_time - start_time:.3f}秒")
```

## 🔄 版本管理

### 版本号规则
- **主版本号**: 重大功能更新或架构变更
- **次版本号**: 新功能添加
- **修订号**: Bug修复和小改进

### 发布流程
1. 更新版本号
2. 更新 `docs/VERSION_HISTORY.md`
3. 创建Git标签
4. 打包应用
5. 创建分发包
6. 更新README.md

## 🐛 调试技巧

### 常见问题
1. **导入错误**
   ```bash
   # 检查依赖安装
   pip list | grep -E "(Pillow|numpy)"
   ```

2. **性能问题**
   ```python
   # 添加性能监控
   import cProfile
   cProfile.run('your_function()')
   ```

3. **内存问题**
   ```python
   # 监控内存使用
   import psutil
   process = psutil.Process()
   print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB")
   ```

## 📦 依赖管理

### 核心依赖
- **Pillow**: 图像处理
- **numpy**: 数值计算优化
- **tkinter**: GUI框架（Python标准库）

### 开发依赖
- **pyinstaller**: 打包工具
- **pytest**: 测试框架（可选）

### 更新依赖
```bash
# 更新requirements.txt
pip freeze > requirements.txt

# 安装特定版本
pip install Pillow==9.0.0
```

## 🎨 UI开发

### tkinter最佳实践
- 使用ttk组件获得现代外观
- 合理使用布局管理器 (pack, grid, place)
- 添加适当的padding和spacing
- 使用一致的颜色方案

### 响应式设计
- 支持窗口大小调整
- 使用相对布局而非绝对位置
- 考虑不同屏幕分辨率

## 🚀 性能优化

### 优化策略
1. **算法优化**: 使用numpy向量化操作
2. **并行处理**: 利用多核CPU
3. **内存优化**: 及时释放大对象
4. **缓存机制**: 避免重复计算

### 性能监控
```python
# 添加性能计时器
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗时: {end - start:.3f}秒")
        return result
    return wrapper
```

---

**遵循开发规范，创造高质量代码！** 🔧✨ 