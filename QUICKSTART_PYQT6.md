# 🚀 PyQt6 Genshin Impact Style - Quick Start

## Installation

```bash
# Install dependencies
pip install -r requirements_pyqt6.txt
```

## Launch

### Windows
```bash
run_pyqt6.bat
```

### Linux/macOS
```bash
./run_pyqt6.sh
```

### Direct Python
```bash
python3 src/watermark_app_pyqt6.py
```

## First Time Usage

1. **Upload Images** 📁
   - Click "Upload Images" button
   - Select one or more images

2. **Add Watermark Layers** 🎨
   - Click "Add" button
   - Select watermark image(s)
   - Adjust blend mode and opacity

3. **Configure Text Label** 🔤 (Optional)
   - Check "Enable text label"
   - Choose type: number or filename
   - Adjust font and size

4. **Select Output Directory** 💾
   - Click "Select Save Directory"

5. **Apply Watermark** 🚀
   - Click "Apply Multi-Layer Watermark"
   - Wait for completion

## Key Features

### Genshin Impact Aesthetic
- ✨ Gold theme colors (#D3BC8E)
- 🎯 Custom title bar (draggable)
- 💫 Smooth animations
- 🌟 Beautiful gradients

### Layer Management
- 👁️ Toggle visibility (eye icon)
- ↑↓ Reorder layers
- 🎚️ Adjust opacity (0-100%)
- 🌈 4 blend modes

### Blend Modes
- **Normal**: Standard overlay
- **Overlay**: Enhanced contrast
- **Screen**: Brightening effect
- **Soft Light**: Gentle blend

## Tips

💡 **Layer Order**: Higher numbers = top layer
💡 **Hidden Layers**: 🚫 icon means hidden
💡 **Font Size**: Use 3-5% for best results
💡 **Performance**: Hide unused layers

## Troubleshooting

**Can't drag window?**
- Drag from the title bar at the top

**Icons not showing?**
```bash
pip install qtawesome --upgrade
```

**Blurry on high DPI?**
- Already enabled automatically!

**Config not loading?**
- Check `configs/multilayer_watermark_config.json`

## Documentation

Full documentation: [PYQT6_GENSHIN_STYLE.md](docs/PYQT6_GENSHIN_STYLE.md)

---

**Enjoy the Genshin Impact aesthetic!** ✨🎮
