# Assets Directory Structure

This directory contains all resource files used by the Watermark App.

## Directory Structure

```
assets/
├── ui/                          # UI-specific resources (PyQt6)
│   ├── arrow.svg               # Dropdown arrow icon (normal)
│   └── arrow_hover.svg         # Dropdown arrow icon (hover)
│
└── watermark_app_icon.ico      # Application icon (used for .exe)
```

## Usage Guidelines

### Application Icon
- **watermark_app_icon.ico** - Used when building the .exe file with PyInstaller
- Referenced in: `tools/build_exe_with_icon.bat`

### UI Resources
- **ui/** - Contains all PyQt6 UI assets (icons, images, etc.)
- Referenced in: `src/watermark_app_pyqt6_ui.py`
- Color scheme follows Genshin Impact theme (gold/beige)

## Adding New Assets

1. **For UI elements**: Place in `assets/ui/`
2. **For app icons**: Place in `assets/` root
3. **For watermark samples**: Consider creating `assets/samples/`
4. **For documentation images**: Consider creating `assets/docs/`

## Path Usage in Code

```python
# Example from watermark_app_pyqt6_ui.py
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "ui")
ICON_PATH = os.path.join(ASSETS_DIR, "icon.svg").replace("\\", "/")
```

## Notes
- Always use forward slashes in QSS/CSS paths
- Use `os.path.join()` for cross-platform compatibility
- Convert backslashes with `.replace("\\", "/")` for QSS usage