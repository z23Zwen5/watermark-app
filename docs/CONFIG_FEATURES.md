# 🔧 配置记忆功能说明

## 📋 功能概述

水印应用现在具备完整的配置记忆功能，能够自动保存和恢复用户的所有设置和文件路径，让您的使用体验更加便捷。

## 🎯 记忆功能详解

### 📁 路径记忆
- **水印文件夹路径** - 记住上次选择水印文件的文件夹位置
- **图片文件夹路径** - 记住上次选择图片的文件夹位置  
- **保存目录路径** - 记住上次选择的输出目录
- **通用目录路径** - 记住最后使用的目录作为备选

### 📄 文件记忆
- **具体水印文件** - 记住上次使用的水印文件完整路径
- **具体图片文件** - 记住上次选择的所有图片文件路径
- **自动加载** - 启动时自动加载上次使用的文件（如果文件仍存在）

### ⚙️ 设置记忆
- **透明度设置** - 记住上次设置的透明度值 (0-100%)
- **拉伸选项** - 记住是否启用水印拉伸
- **并行处理** - 记住是否启用并行处理（仅v1.1优化版）

## 🔄 工作流程

### 首次使用
1. 启动应用，使用默认设置
2. 选择文件和调整设置
3. 应用自动保存所有配置

### 再次使用
1. 启动应用，自动加载上次配置
2. 自动恢复透明度、拉伸等设置
3. 自动加载上次使用的文件（如果存在）
4. 文件选择对话框自动定位到上次使用的文件夹

## 📊 配置文件结构

配置保存在 `watermark_app_config.json` 文件中：

```json
{
  "last_used_directory": "最后使用的目录",
  "save_directory": "保存目录",
  "last_watermark_directory": "水印文件夹",
  "last_images_directory": "图片文件夹",
  "last_opacity": 75,
  "last_stretch": false,
  "last_parallel": true,
  "last_watermark_file": "具体水印文件路径",
  "last_images_files": ["图片文件1", "图片文件2", "..."]
}
```

## ✨ 智能特性

### 🔍 自动检测
- **文件存在性检查** - 启动时检查上次文件是否仍存在
- **路径有效性验证** - 确保记住的路径仍然可访问
- **错误处理** - 文件不存在时优雅降级，不影响正常使用

### 💾 实时保存
- **即时保存** - 每次更改设置时立即保存配置
- **透明度滑块** - 拖动时实时保存
- **选项切换** - 勾选/取消时立即保存
- **文件选择** - 选择文件后立即保存路径

### 🎨 用户体验
- **无感知操作** - 配置保存和加载在后台进行
- **控制台反馈** - 在控制台显示配置加载状态
- **错误容错** - 配置文件损坏时使用默认设置

## 🚀 使用示例

### 典型工作流程
```
第一次使用:
1. 启动应用 → 使用默认设置
2. 选择水印文件 → 自动记住文件夹和文件路径
3. 选择图片文件 → 自动记住文件夹和文件路径
4. 调整透明度到75% → 自动保存设置
5. 启用拉伸选项 → 自动保存设置
6. 处理图片 → 完成

第二次使用:
1. 启动应用 → 自动加载上次的水印和图片
2. 透明度自动设置为75%
3. 拉伸选项自动启用
4. 文件选择对话框自动定位到上次文件夹
5. 直接处理或微调设置 → 享受便捷体验
```

## 🔧 高级功能

### 配置重置
如需重置所有配置，删除 `watermark_app_config.json` 文件即可：
```bash
# Windows
del watermark_app_config.json

# 或手动删除该文件
```

### 配置备份
可以备份配置文件以在不同设备间同步设置：
```bash
# 备份配置
copy watermark_app_config.json watermark_config_backup.json

# 恢复配置
copy watermark_config_backup.json watermark_app_config.json
```

### 配置迁移
两个版本（v1.0和v1.1）共享同一配置文件，设置可以无缝迁移。

## 🎯 版本差异

| 功能 | v1.0 基础版 | v1.1 优化版 |
|------|------------|------------|
| 路径记忆 | ✅ 完整支持 | ✅ 完整支持 |
| 文件记忆 | ✅ 完整支持 | ✅ 完整支持 |
| 透明度记忆 | ✅ 支持 | ✅ 支持 |
| 拉伸选项记忆 | ✅ 支持 | ✅ 支持 |
| 并行处理记忆 | ❌ 不适用 | ✅ 支持 |
| 自动加载文件 | ✅ 支持 | ✅ 支持 + 进度显示 |

## 🛡️ 隐私说明

- **本地存储** - 所有配置仅保存在本地，不会上传到任何服务器
- **文件路径** - 仅记录文件路径，不复制或移动文件内容
- **安全性** - 配置文件为纯文本JSON格式，可随时查看和编辑

## 💡 使用建议

### 最佳实践
1. **保持文件位置稳定** - 避免频繁移动常用的水印和图片文件
2. **使用固定工作目录** - 建议为水印项目创建专门的文件夹
3. **定期备份配置** - 重要项目可备份配置文件
4. **合理组织文件** - 按项目或类型组织水印和图片文件

### 故障排除
1. **配置不生效** - 检查配置文件是否存在且格式正确
2. **文件无法加载** - 确认文件路径仍然有效
3. **设置丢失** - 检查是否有权限写入配置文件

---

**智能配置记忆，让每次使用都像回到家一样熟悉！** 🏠✨ 