# 使用示例：路径记忆功能

## 功能演示

### 第一次使用
1. 启动应用：`python watermark_app.py`
2. 点击 "Upload Images" 按钮
3. 选择图片文件（例如从 `C:\Users\用户名\Pictures\Photos` 文件夹）
4. 点击 "Upload Watermark" 按钮  
5. 选择水印文件（例如从 `C:\Users\用户名\Documents\Watermarks` 文件夹）

### 第二次使用（体验路径记忆）
1. 重新启动应用
2. 点击 "Upload Images" 按钮
   - **自动定位**：文件对话框会直接打开到上次的图片文件夹 `C:\Users\用户名\Pictures\Photos`
3. 点击 "Upload Watermark" 按钮
   - **自动定位**：文件对话框会直接打开到上次的水印文件夹 `C:\Users\用户名\Documents\Watermarks`

## 配置文件示例

应用会在程序目录下自动创建 `watermark_app_config.json` 文件：

```json
{
  "last_used_directory": "C:/Users/用户名/Pictures/Photos",
  "save_directory": "C:/Users/用户名/Pictures/Photos", 
  "last_watermark_directory": "C:/Users/用户名/Documents/Watermarks",
  "last_images_directory": "C:/Users/用户名/Pictures/Photos"
}
```

## 优势

- **提高效率**：无需每次都重新导航到文件夹
- **用户友好**：记住用户的使用习惯
- **自动化**：无需手动配置，自动学习用户行为
- **跨会话**：重启应用后仍然记住路径

## 注意事项

- 配置文件会在首次选择文件夹后自动创建
- 如果移动了文件夹或路径不存在，会回退到系统默认位置
- 可以手动删除配置文件来重置所有路径记忆 