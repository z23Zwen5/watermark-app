#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asset Generator - 生成应用所需的 SVG 和 ICO 资源
用于 build 前自动生成/更新 assets 目录下的所有 UI 资源。

生成内容：
  - assets/watermark_app_icon.ico  (从 600x600 PNG 生成多尺寸 ICO)
  - assets/ui/<theme>/arrow.svg          (各主题下拉箭头)
  - assets/ui/<theme>/arrow_hover.svg    (各主题下拉箭头悬停态)
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
UI_DIR = os.path.join(ASSETS_DIR, "ui")

# ── 主题配色 ──────────────────────────────────────────────
# (arrow_normal_color, arrow_hover_color)
THEMES = {
    "genshin":   ("#A68D5E", "#D3BC8E"),   # 暗金 / 亮金
    "cyberpunk": ("#00a8cc", "#00d4ff"),    # 深青 / 亮青
}

# 同时在 assets/ui/ 根目录放一份默认（genshin）
DEFAULT_THEME = "genshin"

# ── SVG 模板 ─────────────────────────────────────────────
ARROW_SVG_TEMPLATE = """\
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M6 9L12 15L18 9" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def generate_svgs():
    """为每个主题生成 arrow SVG 文件。"""
    created = []
    for theme_name, (normal_color, hover_color) in THEMES.items():
        theme_dir = os.path.join(UI_DIR, theme_name)
        os.makedirs(theme_dir, exist_ok=True)

        arrow_path = os.path.join(theme_dir, "arrow.svg")
        arrow_hover_path = os.path.join(theme_dir, "arrow_hover.svg")

        with open(arrow_path, "w", encoding="utf-8") as f:
            f.write(ARROW_SVG_TEMPLATE.format(color=normal_color))
        with open(arrow_hover_path, "w", encoding="utf-8") as f:
            f.write(ARROW_SVG_TEMPLATE.format(color=hover_color))

        created.extend([arrow_path, arrow_hover_path])

    # 根目录放默认主题副本
    default_normal, default_hover = THEMES[DEFAULT_THEME]
    for filename, color in [("arrow.svg", default_normal), ("arrow_hover.svg", default_hover)]:
        path = os.path.join(UI_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(ARROW_SVG_TEMPLATE.format(color=color))
        created.append(path)

    return created


def generate_ico():
    """从 600x600 PNG 生成多尺寸 ICO 文件。"""
    try:
        from PIL import Image
    except ImportError:
        print("[WARN] Pillow not installed, skipping ICO generation")
        return None

    png_path = os.path.join(ASSETS_DIR, "watermark_app_icon_600x600.png")
    ico_path = os.path.join(ASSETS_DIR, "watermark_app_icon.ico")

    if not os.path.exists(png_path):
        print(f"[WARN] Source PNG not found: {png_path}")
        print("       Skipping ICO generation")
        return None

    img = Image.open(png_path).convert("RGBA")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format="ICO", sizes=sizes)
    return ico_path


def main():
    print("=" * 50)
    print("  Asset Generator")
    print("=" * 50)
    print()

    # 1) SVG
    print("[1/2] Generating SVG assets...")
    svgs = generate_svgs()
    for p in svgs:
        rel = os.path.relpath(p, PROJECT_ROOT)
        print(f"  ✓ {rel}")
    print(f"  → {len(svgs)} SVG files generated")
    print()

    # 2) ICO
    print("[2/2] Generating ICO from PNG...")
    ico = generate_ico()
    if ico:
        rel = os.path.relpath(ico, PROJECT_ROOT)
        print(f"  ✓ {rel}")
    print()

    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
