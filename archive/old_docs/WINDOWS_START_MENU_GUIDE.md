# Windows 11 开始菜单固定指南

**版本**: v1.5
**日期**: 2025-10-23

---

## 🎯 目标

将 `MultiLayerWatermark_v1.5.exe` 固定到 Windows 11 开始菜单（磁贴界面）。

---

## 方法 1：直接右键固定（最快）

### 步骤

1. **找到可执行文件**
   ```
   路径：dist\MultiLayerWatermark_v1.5.exe
   ```

2. **右键菜单**
   - 右键点击 `MultiLayerWatermark_v1.5.exe`
   - 选择 **"固定到'开始'屏幕"** (Pin to Start)

3. **查看结果**
   - 按 `Win` 键
   - 应用会出现在固定的磁贴区域

### 优点
- ✅ 最简单快速
- ✅ 无需额外文件

### 缺点
- ❌ 如果移动 exe 位置，快捷方式会失效
- ❌ 图标名称可能包含版本号（不美观）

---

## 方法 2：使用安装脚本（推荐）

### 步骤

1. **运行构建脚本**（如果还没构建）
   ```cmd
   tools\build_multilayer.bat
   ```

2. **运行安装脚本**
   ```cmd
   tools\install_windows.bat
   ```

   脚本会：
   - ✅ 复制 exe 到 `C:\Program Files\MultiLayerWatermark\` 或 `%LocalAppData%\MultiLayerWatermark\`
   - ✅ 创建开始菜单快捷方式（去掉版本号）
   - ✅ 复制配置文件
   - ✅ 询问是否立即运行

3. **固定到开始屏幕**
   - 按 `Win` 键
   - 搜索 "Multi-Layer Watermark"
   - 右键 → **"固定到开始屏幕"**

### 优点
- ✅ 专业的安装位置
- ✅ 快捷方式名称美观（无版本号）
- ✅ 移动 exe 不影响
- ✅ 易于卸载

### 卸载
```cmd
tools\uninstall_windows.bat
```

---

## 方法 3：手动创建快捷方式

### 步骤

1. **复制 exe 到稳定位置**
   ```
   推荐位置（选一个）:
   - C:\Program Files\MultiLayerWatermark\MultiLayerWatermark.exe
   - %LocalAppData%\MultiLayerWatermark\MultiLayerWatermark.exe
   - D:\Programs\MultiLayerWatermark\MultiLayerWatermark.exe
   ```

2. **创建快捷方式**
   - 右键 exe → "创建快捷方式"
   - 重命名为 "Multi-Layer Watermark"（去掉 .exe 和版本号）

3. **放到开始菜单文件夹**

   **当前用户**（无需管理员）：
   ```
   %AppData%\Microsoft\Windows\Start Menu\Programs
   ```

   或者按 `Win + R` 输入：
   ```
   shell:programs
   ```

   **所有用户**（需要管理员）：
   ```
   C:\ProgramData\Microsoft\Windows\Start Menu\Programs
   ```

4. **固定到开始屏幕**
   - 按 `Win` 键
   - 找到 "Multi-Layer Watermark"
   - 右键 → "固定到开始屏幕"

### 优点
- ✅ 完全控制安装位置
- ✅ 快捷方式名称自定义
- ✅ 移动 exe 不影响

---

## 方法 4：添加到任务栏（额外）

除了开始菜单，你也可以固定到任务栏：

1. **找到 exe 或快捷方式**
2. **右键 → "固定到任务栏"** (Pin to taskbar)

或者：
1. **运行程序**
2. **右键任务栏图标 → "固定到任务栏"**

---

## 🎨 自定义图标（可选）

如果想更改快捷方式的图标：

1. **准备图标文件**
   - 使用 `assets\watermark_app_icon.ico`
   - 或自己准备一个 `.ico` 文件

2. **修改快捷方式图标**
   - 右键快捷方式 → "属性"
   - 点击 "更改图标"
   - 浏览并选择 `.ico` 文件
   - 确定

---

## 📁 目录结构说明

### 开始菜单文件夹位置

| 类型 | 路径 | 环境变量 |
|------|------|----------|
| 当前用户 | `C:\Users\你的用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs` | `%AppData%\Microsoft\Windows\Start Menu\Programs` |
| 所有用户 | `C:\ProgramData\Microsoft\Windows\Start Menu\Programs` | `%ProgramData%\Microsoft\Windows\Start Menu\Programs` |

### 快速打开方法

| 目标 | 命令 (Win + R) |
|------|----------------|
| 当前用户开始菜单 | `shell:programs` |
| 所有用户开始菜单 | `shell:common programs` |
| 当前用户桌面 | `shell:desktop` |

---

## 🔧 常见问题

### Q1: 右键菜单没有"固定到开始屏幕"选项

**原因**: Windows 11 某些情况下不显示此选项

**解决方案**:
1. 按 `Win` 键
2. 在搜索框输入程序名称
3. 右键搜索结果 → "固定到开始屏幕"

### Q2: 固定后图标显示错误

**原因**: 图标缓存问题

**解决方案**:
1. 重启 Windows 资源管理器
2. 或重启电脑
3. 或重新构建 exe 时确保包含图标：
   ```cmd
   --icon=assets/watermark_app_icon.ico
   ```

### Q3: 移动 exe 后快捷方式失效

**原因**: 快捷方式指向的是原始路径

**解决方案**:
- 使用方法 2 或 3，将 exe 安装到固定位置
- 或重新创建快捷方式

### Q4: 删除 exe 后开始菜单仍显示

**原因**: 快捷方式还在

**解决方案**:
1. 右键开始菜单图标 → "取消固定"
2. 或删除快捷方式文件：
   ```
   %AppData%\Microsoft\Windows\Start Menu\Programs
   ```

### Q5: 需要管理员权限

**原因**: 安装到 `C:\Program Files`

**解决方案**:
- 右键 `install_windows.bat` → "以管理员身份运行"
- 或安装到用户目录（不需要管理员权限）

---

## 📋 完整安装流程（推荐）

### 1. 构建程序
```cmd
cd WatermarkApp\watermarkApp
tools\build_multilayer.bat
```

### 2. 安装程序
```cmd
tools\install_windows.bat
```

### 3. 固定到开始屏幕
- 按 `Win` 键
- 搜索 "Multi-Layer Watermark"
- 右键 → "固定到开始屏幕"

### 4. 调整位置（可选）
- 按 `Win` 键
- 拖动磁贴到想要的位置
- 右键 → "调整大小" 选择磁贴大小

---

## 🎨 Windows 11 开始菜单磁贴大小

| 大小 | 说明 |
|------|------|
| 小 | 只显示图标 |
| 中 | 图标 + 名称（推荐） |
| 大 | 大图标 + 名称 |

---

## 🔗 相关脚本

| 脚本 | 功能 |
|------|------|
| [tools/build_multilayer.bat](../tools/build_multilayer.bat) | 构建 exe |
| [tools/install_windows.bat](../tools/install_windows.bat) | 安装程序 |
| [tools/uninstall_windows.bat](../tools/uninstall_windows.bat) | 卸载程序 |

---

## 💡 提示

1. **图标大小**: 确保 `.ico` 文件包含多种尺寸（16x16, 32x32, 48x48, 256x256）
2. **名称**: 建议去掉版本号，使用简洁名称如 "Multi-Layer Watermark"
3. **位置**: 安装到 `C:\Program Files` 更专业，但需要管理员权限
4. **更新**: 更新版本时，重新运行 `install_windows.bat` 即可

---

## 📚 参考资源

- [Windows 11 开始菜单官方文档](https://support.microsoft.com/zh-cn/windows/)
- [快捷方式属性说明](https://docs.microsoft.com/zh-cn/windows/win32/shell/links)

---

**最后更新**: 2025-10-23
**维护者**: WatermarkApp Team
