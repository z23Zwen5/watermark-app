# Watermark App 💧

一个简易但实用的图片批量水印工具，支持透明水印覆盖、批量处理、本地运行。

## 🔧 特性 Features
- 支持批量添加透明水印
- 水印透明度可调
- PyInstaller 打包为独立桌面应用
- 自动适配图片尺寸

## 🚀 使用方法

```bash
python watermark_app.py
```

或双击打包好的程序运行。

## 🛠️ 打包命令（PyInstaller）

```bash
pyinstaller --onefile --windowed --name "Watermark App" --icon=watermark_app_icon.ico --noconsole watermark_app.py
```

## 🗃️ 项目结构

```
.
├── watermark_app.py              # 主程序
├── watermark_app_icon.ico        # 程序图标
├── build/                        # PyInstaller 构建中间文件
├── dist/                         # 打包输出目录
├── Watermark App.spec            # 打包配置文件
├── .gitignore                    # 忽略配置
└── README.md                     # 项目说明
```

## 📦 打包说明
- 安装 pyinstaller：`pip install pyinstaller`
- 构建后输出文件在 `dist/` 文件夹下

## 👤 作者
Made with ❤️ by ehcawen
