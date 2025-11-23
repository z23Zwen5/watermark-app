# 主题切换功能使用指南

## 功能概述

应用现在支持两种 UI 主题：
- **🎨 Genshin Impact** - 米黄色调，温暖优雅
- **🌆 Cyberpunk 2077** - 霓虹色调，暗黑未来感

## 如何切换主题

### 方法 1：通过 UI 切换（推荐）

1. 启动应用
2. 在右侧面板找到 **"General Settings"** 部分
3. 找到 **"UI Theme"** 下拉框
4. 选择你喜欢的主题：
   - 🎨 Genshin Impact
   - 🌆 Cyberpunk 2077
5. 主题会立即切换，并显示确认消息

### 方法 2：通过配置文件

编辑 `configs/multilayer_watermark_config.json`：

```json
{
  "ui_theme": "cyberpunk",
  ...
}
```

可选值：
- `"genshin"` - Genshin Impact 主题
- `"cyberpunk"` - Cyberpunk 2077 主题

## 主题特色

### Genshin Impact 主题
- **主色调**：米黄色 (#ECE5D8)
- **强调色**：金色 (#D3BC8E)
- **风格**：温暖、优雅、柔和
- **字体**：'HYWenHei', 'Microsoft YaHei UI', sans-serif

### Cyberpunk 2077 主题
- **主色调**：暗蓝色 (#16213e)
- **强调色**：电光蓝 (#00d4ff)
- **风格**：科技感、未来感、霓虹发光
- **字体**：'Consolas', 'Monaco', 'Courier New', monospace
- **特效**：按钮和元素有发光效果（box-shadow）

## 技术细节

### 主题持久化
- 主题选择会自动保存到配置文件
- 下次启动应用时，会自动加载上次使用的主题
- 无需重启应用，主题切换即时生效

### 实现原理
- 基于抽象主题类（Theme ABC）
- 使用单例模式的 ThemeManager 管理主题
- 所有 UI 组件动态引用主题属性
- 支持运行时热切换

### 扩展主题

如需添加新主题，可参考 `src/ui/styles/theme_cyberpunk.py`：

1. 创建新的主题类，继承 `Theme`
2. 实现所有抽象属性和方法
3. 在 `src/ui/styles/__init__.py` 中注册主题
4. 在 `settings_panel.py` 中添加显示名称

## 注意事项

1. **部分元素需重启**：某些 UI 元素（如已创建的对话框）可能需要重启应用才能完全更新
2. **主题兼容性**：所有功能在两种主题下都完全可用
3. **性能影响**：主题切换不会影响图片处理性能

## 故障排除

### 主题未切换
- 检查配置文件是否可写
- 检查 `ui_theme` 值是否为 `genshin` 或 `cyberpunk`
- 尝试重启应用

### 样式显示异常
- 确保使用的是 PyQt6 版本应用
- 检查控制台是否有错误信息
- 尝试切换到另一个主题再切回

## 反馈

如有问题或建议，请提交 Issue。
