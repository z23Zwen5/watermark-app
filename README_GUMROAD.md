# Multi-Layer Batch Watermark Tool

## Quick Start

**No installation required!** Simply double-click `Multi-Layer Watermark Tool.exe` to launch the application.

---

## Interface Overview

The application has a clean, intuitive interface with the following sections:

| Section | Description |
|---------|-------------|
| **Source Images** | Select images or folders to process |
| **Watermark Layers** | Manage your watermark layers |
| **General Settings** | Theme and stretch options |
| **Text Label** | Add automatic text labels |
| **Output Folder** | Choose where to save processed images |

---

## Step-by-Step Guide

### 1. Select Source Images

Click **"Select Images / Folder"** to choose:
- Individual image files (PNG, JPG, JPEG, BMP, WEBP)
- An entire folder containing images

The status will show how many images are ready for processing.

### 2. Add Watermark Layers

Use the layer panel to build your watermark stack:

| Button | Function |
|--------|----------|
| **+** | Add a new watermark layer |
| **Eye icon** | Toggle layer visibility (green = visible) |
| **Trash icon** | Delete selected layer |
| **Up/Down arrows** | Reorder layers |

For each layer, you can adjust:
- **Blend Mode**: Normal, Overlay, Screen, or Soft Light
- **Opacity**: 0-100%

> **Tip:** Layers are applied from top to bottom. Use visibility toggles to quickly compare different watermark combinations.

### 3. Configure General Settings

- **UI Theme**: Choose between Genshin Impact or Cyberpunk 2077 themes
- **Stretch watermark to fit image**: When enabled, watermarks will stretch to match the source image dimensions

### 4. Text Labels (Optional)

Enable **"Enable Text Label"** to add automatic text to each image:

| Option | Description |
|--------|-------------|
| **Content** | `number` (1, 2, 3...) or `filename` |
| **Position** | Corner placement (top_left, top_right, bottom_left, bottom_right) |
| **Font** | Select from system fonts or use (Auto) |
| **Size** | Percentage of image height (e.g., 7.5%) |

### 5. Select Output Folder

Click **"Output Folder"** to choose where processed images will be saved.

### 6. Start Processing

Click **"START PROCESSING"** to apply watermarks to all selected images.

Processed images will be saved with `_multilayer` suffix in the output folder.

---

## Blend Modes Explained

| Mode | Effect |
|------|--------|
| **Normal** | Standard overlay with opacity |
| **Overlay** | Enhances contrast, good for logos on varied backgrounds |
| **Screen** | Lightens the image, ideal for light watermarks on dark images |
| **Soft Light** | Subtle contrast enhancement, natural-looking results |

---

## Tips for Best Results

1. **Prepare your watermarks** as PNG files with transparency
2. **Use full-screen watermarks** for best coverage (the tool will scale them automatically)
3. **Experiment with blend modes** - Overlay and Soft Light often give more professional results than Normal
4. **Lower opacity** (30-50%) for subtle, professional watermarks
5. **Stack multiple layers** for complex effects (e.g., logo + pattern + text)


---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| App won't start | Make sure you have Windows 10/11 |
| Watermark not visible | Check layer visibility (eye icon should be green) and opacity |
| Output looks wrong | Try different blend modes |
| Chinese characters not displaying | Use a font that supports Chinese (e.g., Microsoft YaHei) |

---

## System Requirements

- Windows 10 or Windows 11
- No additional software required

---

## Support

If you encounter any issues, please contact me through Gumroad.

Thank you for your purchase!
