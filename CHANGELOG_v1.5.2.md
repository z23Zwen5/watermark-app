# 🔧 Changelog - v1.5.2

**发布日期**: 2025-10-23
**版本**: v1.5.2 (Bug Fix Release)

---

## 🐛 Bug 修复

### 1. 配置文件类型不一致问题

**问题**: `opacity` 在配置文件中保存为 `float` 类型（100.0），导致类型不一致。

**修复**:
- ✅ `WatermarkLayer` 初始化时强制转换 `opacity` 为整数
- ✅ 保存配置时强制转换为整数和字符串
- ✅ 加载配置时强制类型转换
- ✅ 修复现有配置文件（使用 `tools/fix_config_types.py`）

**文件修改**:
- [src/watermark_app_multilayer.py](src/watermark_app_multilayer.py)
  - 第 15 行: `WatermarkLayer.__init__()`
  - 第 392 行: `on_opacity_entry_change()`
  - 第 653-654 行: `load_config()`
  - 第 680-681 行: `save_config()`

**详细文档**: [docs/BUGFIX_BLEND_MODE_CONFIG.md](docs/BUGFIX_BLEND_MODE_CONFIG.md)

---

### 2. Blend Mode 下拉菜单切换问题

**问题**: 使用下拉菜单切换 blend mode 时，显示可能不正确或被重置。

**原因**: `update_layer_listbox()` 后重新选中图层触发了 `<<ListboxSelect>>` 事件，导致 UI 控件值被意外更新。

**修复**:
- ✅ 创建 `update_layer_listbox_silent()` 方法，暂时解绑事件
- ✅ 在 `on_blend_mode_change()` 中使用新方法
- ✅ 在 `on_opacity_entry_change()` 中使用新方法
- ✅ 添加调试输出，方便追踪问题

**文件修改**:
- [src/watermark_app_multilayer.py](src/watermark_app_multilayer.py)
  - 第 343-352 行: `on_layer_select()` - 添加调试输出
  - 第 364-380 行: `on_blend_mode_change()` - 使用 silent 更新
  - 第 382-403 行: `on_opacity_entry_change()` - 使用 silent 更新
  - 第 453-473 行: `update_layer_listbox_silent()` - 新增方法

**详细文档**: [docs/BUGFIX_BLEND_MODE_UI.md](docs/BUGFIX_BLEND_MODE_UI.md)

---

## 🛠️ 新增工具

### 1. 配置文件类型修复工具

**文件**: [tools/fix_config_types.py](tools/fix_config_types.py)

**功能**:
- 自动检测并修复配置文件中的类型问题
- 将 `opacity` 从 `float` 转换为 `int`
- 自动创建备份文件

**使用方法**:
```bash
python tools/fix_config_types.py
```

---

### 2. 配置类型测试脚本

**文件**: [tests/test_config_save_load.py](tests/test_config_save_load.py)

**功能**:
- 检查配置文件中的数据类型
- 测试 `WatermarkLayer` 类的类型处理
- 验证类型转换逻辑

**使用方法**:
```bash
python tests/test_config_save_load.py
```

---

### 3. Blend Mode 切换测试

**文件**: [tests/test_blend_mode_change.py](tests/test_blend_mode_change.py)

**功能**:
- 简化的测试应用，用于调试 blend mode 切换
- 包含详细的调试输出
- 可独立运行，不需要实际图片文件

**使用方法**:
```bash
python tests/test_blend_mode_change.py
```

---

## 📚 新增文档

### 1. 构建指南

**文件**:
- [BUILD.md](BUILD.md) - 快速参考
- [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md) - 完整指南

**内容**:
- ✅ 一键构建脚本使用说明
- ✅ 手动构建命令（带图标）
- ✅ PyInstaller 参数详解
- ✅ 图标文件创建方法
- ✅ 常见问题解答
- ✅ 构建验证步骤

---

### 2. Bug 修复文档

**文件**:
- [docs/BUGFIX_BLEND_MODE_CONFIG.md](docs/BUGFIX_BLEND_MODE_CONFIG.md)
- [docs/BUGFIX_BLEND_MODE_UI.md](docs/BUGFIX_BLEND_MODE_UI.md)

**内容**:
- ✅ 问题描述和根本原因分析
- ✅ 解决方案详细说明
- ✅ 代码修改对比
- ✅ 测试验证步骤
- ✅ 后续优化建议

---

## 🔨 构建脚本

### Windows 构建脚本

**文件**: [tools/build_multilayer.bat](tools/build_multilayer.bat)

**功能**:
- ✅ 自动检查 Python 和依赖
- ✅ 自动安装 PyInstaller
- ✅ 清理旧的构建文件
- ✅ 使用正确的图标和参数构建
- ✅ 显示构建进度和结果

**使用方法**:
```cmd
cd tools
build_multilayer.bat
```

---

### Linux/Mac 构建脚本

**文件**: [tools/build_multilayer.sh](tools/build_multilayer.sh)

**功能**:
- ✅ 彩色输出，易于阅读
- ✅ 完整的错误检查
- ✅ 自动处理依赖
- ✅ 支持图标配置

**使用方法**:
```bash
cd tools
./build_multilayer.sh
```

---

## 🎯 影响范围

### 修改的文件

1. **核心程序**
   - [src/watermark_app_multilayer.py](src/watermark_app_multilayer.py)

2. **配置文件**
   - [configs/multilayer_watermark_config.json](configs/multilayer_watermark_config.json) - 已修复

3. **新增工具**
   - [tools/fix_config_types.py](tools/fix_config_types.py)
   - [tools/build_multilayer.sh](tools/build_multilayer.sh)
   - [tools/build_multilayer.bat](tools/build_multilayer.bat)

4. **新增测试**
   - [tests/test_config_save_load.py](tests/test_config_save_load.py)
   - [tests/test_blend_mode_change.py](tests/test_blend_mode_change.py)

5. **新增文档**
   - [BUILD.md](BUILD.md)
   - [docs/BUILD_GUIDE.md](docs/BUILD_GUIDE.md)
   - [docs/BUGFIX_BLEND_MODE_CONFIG.md](docs/BUGFIX_BLEND_MODE_CONFIG.md)
   - [docs/BUGFIX_BLEND_MODE_UI.md](docs/BUGFIX_BLEND_MODE_UI.md)
   - [CHANGELOG_v1.5.2.md](CHANGELOG_v1.5.2.md)

---

## ✅ 向后兼容性

### 配置文件

- ✅ **完全兼容旧配置文件**
- ✅ 自动处理 `float` 类型的 `opacity`
- ✅ 自动处理缺失的字段（使用默认值）
- ✅ 提供修复工具升级旧配置

### 代码接口

- ✅ 所有公共方法保持不变
- ✅ 新增方法不影响现有功能
- ✅ 调试输出可以移除（不影响功能）

---

## 🧪 测试覆盖

### 手动测试

- ✅ Blend mode 切换（4种模式）
- ✅ Opacity 修改（0-100）
- ✅ 多图层操作
- ✅ 配置保存和加载
- ✅ 图层添加/删除/移动
- ✅ 应用水印处理

### 自动化测试

- ✅ 配置文件类型检查
- ✅ WatermarkLayer 类型转换
- ✅ Blend mode UI 交互（测试应用）

---

## 📊 性能影响

### 修复前

- **问题**: 不必要的事件触发，可能导致 UI 闪烁
- **用户体验**: 下拉菜单显示不稳定

### 修复后

- **改进**: 减少不必要的事件触发
- **用户体验**: 下拉菜单切换流畅，显示准确
- **性能**: 无显著影响（事件解绑/绑定开销极小）

---

## 🔮 下一步计划

### v1.6 可能的功能

- [ ] 更多混合模式（Multiply, Color Dodge, Color Burn）
- [ ] 图层位置独立控制
- [ ] 预设模板系统
- [ ] 实时预览功能

### 代码质量改进

- [ ] 添加单元测试框架
- [ ] 使用 MVC 模式重构
- [ ] 添加类型提示（Type Hints）
- [ ] 使用 dataclass 管理配置

---

## 💡 用户指南

### 如何更新到 v1.5.2

1. **拉取最新代码**:
   ```bash
   git pull origin main
   ```

2. **修复现有配置文件**（可选）:
   ```bash
   python tools/fix_config_types.py
   ```

3. **运行程序**:
   ```bash
   python src/watermark_app_multilayer.py
   ```

4. **构建可执行文件**（可选）:
   ```bash
   # Windows
   tools\build_multilayer.bat

   # Linux/Mac
   ./tools/build_multilayer.sh
   ```

---

### 验证修复是否生效

1. 启动程序
2. 添加一个水印图层
3. 在下拉菜单中切换 blend mode
4. 观察下拉菜单和列表显示是否一致
5. 检查配置文件 `configs/multilayer_watermark_config.json`
6. 确认 `opacity` 是整数类型（如 `100` 而不是 `100.0`）

---

## 🎓 开发者笔记

### 关键经验

1. **类型一致性很重要**: JSON 的 `100.0` 会被解析为 `float`，需要显式转换
2. **事件绑定要谨慎**: tkinter 的事件会在意外的时候触发
3. **调试输出是好朋友**: 添加 print 语句帮助追踪问题
4. **向后兼容优先**: 确保旧配置文件能正常工作

### 代码风格

```python
# ✅ 好的做法
def update_something_silent(self, param):
    """明确的方法名，说明不触发事件"""
    pass

# ❌ 不好的做法
def update_something2(self, param, silent=False):
    """用参数控制行为，容易忘记传递"""
    pass
```

---

## 📞 反馈和支持

如果遇到问题或有建议，请：

1. 查看相关文档（[docs/](docs/)）
2. 运行测试工具验证
3. 提交 Issue（包含调试输出）

---

**版本**: v1.5.2
**维护者**: WatermarkApp Team
**最后更新**: 2025-10-23
