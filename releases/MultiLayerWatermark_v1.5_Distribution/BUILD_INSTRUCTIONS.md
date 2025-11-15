# 🔨 构建说明 - Build Instructions

## 打包成 Windows exe

### 前置要求
1. Python 3.7+
2. 已安装依赖包

### 步骤

#### 1. 安装 PyInstaller
```bash
pip install pyinstaller
```

#### 2. 执行打包
```bash
pyinstaller build/MultiLayerWatermark_v1.5.spec --clean --noconfirm
```

#### 3. 查找输出
打包完成后，exe 文件位于：
```
dist/MultiLayerWatermark_v1.5.exe
```

### 打包选项说明

- `--clean`: 清理临时文件
- `--noconfirm`: 自动覆盖输出
- `--onefile`: 打包成单文件（已在 spec 中配置）
- `--windowed`: 不显示控制台（已在 spec 中配置）

---

## 自定义打包

### 修改图标
编辑 `build/MultiLayerWatermark_v1.5.spec` 文件：
```python
icon='../assets/your_icon.ico'
```

### 修改程序名称
编辑 spec 文件中的 `name` 参数：
```python
name='YourAppName'
```

### 添加数据文件
如需打包额外文件（如配置、图片），修改 `datas` 参数：
```python
datas=[
    ('../configs/*.json', 'configs'),
    ('../assets/*.png', 'assets'),
]
```

---

## 测试打包结果

### 在本机测试
```bash
dist/MultiLayerWatermark_v1.5.exe
```

### 在其他机器测试
1. 复制 exe 到其他 Windows 机器
2. 无需安装 Python
3. 双击运行

---

## 常见问题

### Q: 打包后 exe 很大？
A: 正常现象，包含了 Python 解释器和所有依赖库
- 预期大小: 30-50 MB

### Q: 打包失败找不到模块？
A: 添加到 spec 文件的 `hiddenimports`:
```python
hiddenimports=['missing_module']
```

### Q: exe 无法运行？
A: 检查：
1. 是否有杀毒软件拦截
2. 使用 `--debug` 选项重新打包查看日志
3. 尝试在控制台模式运行查看错误

---

## 打包优化

### 减小文件大小
```bash
# 使用 UPX 压缩
pyinstaller build/MultiLayerWatermark_v1.5.spec --clean --upx-dir=/path/to/upx
```

### 加快启动速度
- 使用 `--noupx` 禁用压缩
- 调整 `excludes` 排除不需要的模块

---

## 分发建议

### 创建安装包
推荐使用：
- Inno Setup (Windows)
- NSIS
- MSI

### 数字签名
使用代码签名证书为 exe 签名，避免 Windows SmartScreen 警告

---

*Happy Building!* 🎉
