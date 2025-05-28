# Watermark App 💧

一个简易但实用的图片批量水印工具，支持透明水印覆盖、批量处理、本地运行。

## 🔧 特性 Features
- 支持批量添加透明水印
- 水印透明度可调
- **🆕 智能路径记忆：自动记住水印文件夹和图片文件夹路径**
- PyInstaller 打包为独立桌面应用
- 自动适配图片尺寸

## ✨ 新功能：路径记忆
- **水印文件夹记忆**：应用会记住上次选择水印文件的文件夹位置
- **图片文件夹记忆**：应用会记住上次选择图片的文件夹位置
- **自动定位**：下次打开文件选择对话框时，会自动定位到上次使用的位置
- **配置持久化**：路径信息保存在 `watermark_app_config.json` 文件中

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
├── watermark_app_config.json     # 配置文件（自动生成）
├── build/                        # PyInstaller 构建中间文件
├── dist/                         # 打包输出目录
├── Watermark App.spec            # 打包配置文件
├── .gitignore                    # 忽略配置
└── README.md                     # 项目说明
```

## 📝 配置文件说明
应用会自动创建 `watermark_app_config.json` 配置文件来保存路径信息：
```json
{
  "last_used_directory": "最后使用的目录",
  "save_directory": "保存目录", 
  "last_watermark_directory": "最后使用的水印文件夹",
  "last_images_directory": "最后使用的图片文件夹"
}
```

## 📦 打包说明
- 安装 pyinstaller：`pip install pyinstaller`
- 构建后输出文件在 `dist/` 文件夹下

## 👤 作者
Made with ❤️ by ehcawen
