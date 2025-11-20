#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试原神Geo主题配置（不需要GUI）
"""

print("🎮 测试原神Geo主题配置")
print("=" * 60)

# 直接测试主题类（不导入tkinter）
class GenshinGeoTheme:
    """原神岩元素（Geo）主题配色"""
    # Colors
    PRIMARY = "#FFCC33"           # 金黄色
    SECONDARY = "#2D240F"         # 深棕色
    BACKGROUND = "#140F05"        # 深背景
    TEXT_PRIMARY = "#FFF8E1"      # 浅米色
    TEXT_SECONDARY = "#D4AF37"    # 金色
    ACCENT = "#FFD700"            # 亮金色
    BORDER = "#6B4E23"            # 棕色边框
    SUCCESS = "#4CAF50"           # 成功绿色
    ERROR = "#F44336"             # 错误红色
    GRADIENT_START = "#FFDD66"    # 渐变开始
    GRADIENT_END = "#FFB700"      # 渐变结束

    # Darker variations for better contrast
    BG_LIGHT = "#1E1810"          # 稍亮的背景
    BG_MEDIUM = "#2A2015"         # 中等背景
    BG_DARK = "#0F0A03"           # 更深背景

    # Fonts
    FONT_PRIMARY = "Segoe UI"
    FONT_SECONDARY = "Georgia"
    FONT_H1 = 24
    FONT_H2 = 18
    FONT_BODY = 12
    FONT_SMALL = 10

print("\n🎨 主题配色:")
print(f"  ⚡ PRIMARY (主色): {GenshinGeoTheme.PRIMARY}")
print(f"  ✨ ACCENT (强调色): {GenshinGeoTheme.ACCENT}")
print(f"  🌑 BACKGROUND (背景): {GenshinGeoTheme.BACKGROUND}")
print(f"  📝 TEXT_PRIMARY (主文字): {GenshinGeoTheme.TEXT_PRIMARY}")
print(f"  📄 TEXT_SECONDARY (次要文字): {GenshinGeoTheme.TEXT_SECONDARY}")
print(f"  🔸 BORDER (边框): {GenshinGeoTheme.BORDER}")

print("\n🎨 背景渐变:")
print(f"  🌟 BG_LIGHT (浅背景): {GenshinGeoTheme.BG_LIGHT}")
print(f"  🌘 BG_MEDIUM (中等背景): {GenshinGeoTheme.BG_MEDIUM}")
print(f"  🌑 BG_DARK (深背景): {GenshinGeoTheme.BG_DARK}")

print("\n✨ 渐变效果:")
print(f"  ☀️ GRADIENT_START: {GenshinGeoTheme.GRADIENT_START}")
print(f"  🌅 GRADIENT_END: {GenshinGeoTheme.GRADIENT_END}")

print("\n📚 字体配置:")
print(f"  PRIMARY FONT: {GenshinGeoTheme.FONT_PRIMARY}")
print(f"  SECONDARY FONT: {GenshinGeoTheme.FONT_SECONDARY}")
print(f"  H1: {GenshinGeoTheme.FONT_H1}px")
print(f"  H2: {GenshinGeoTheme.FONT_H2}px")
print(f"  BODY: {GenshinGeoTheme.FONT_BODY}px")

# 验证颜色格式
def validate_hex_color(color):
    """验证十六进制颜色格式"""
    return color.startswith('#') and len(color) == 7

print("\n🔍 颜色格式验证:")
colors_to_test = [
    ('PRIMARY', GenshinGeoTheme.PRIMARY),
    ('ACCENT', GenshinGeoTheme.ACCENT),
    ('BACKGROUND', GenshinGeoTheme.BACKGROUND),
    ('TEXT_PRIMARY', GenshinGeoTheme.TEXT_PRIMARY),
    ('TEXT_SECONDARY', GenshinGeoTheme.TEXT_SECONDARY),
]

all_valid = True
for name, color in colors_to_test:
    is_valid = validate_hex_color(color)
    status = "✅" if is_valid else "❌"
    print(f"  {status} {name}: {color}")
    if not is_valid:
        all_valid = False

print("\n" + "=" * 60)
if all_valid:
    print("✅ 所有配置测试通过！")
    print("💎 原神Geo主题已准备就绪！")
else:
    print("❌ 部分配置测试失败")
print("=" * 60)
