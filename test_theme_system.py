#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Theme System
测试主题系统
"""
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.styles.theme_base import ThemeManager
from ui.styles.theme_genshin import GenshinTheme
from ui.styles.theme_cyberpunk import CyberpunkTheme


def test_theme_registration():
    """测试主题注册"""
    print("=" * 50)
    print("测试主题注册...")

    # 手动注册主题
    ThemeManager.register_theme(GenshinTheme())
    ThemeManager.register_theme(CyberpunkTheme())
    ThemeManager.set_theme('genshin')

    available = ThemeManager.get_available_themes()
    print(f"✓ 可用主题: {available}")
    assert 'genshin' in available, "Genshin 主题未注册"
    assert 'cyberpunk' in available, "Cyberpunk 主题未注册"
    print("✓ 主题注册成功\n")


def test_theme_switching():
    """测试主题切换"""
    print("=" * 50)
    print("测试主题切换...")

    # 切换到 Genshin 主题
    ThemeManager.set_theme('genshin')
    theme = ThemeManager.get_theme()
    print(f"✓ 当前主题: {theme.display_name}")
    assert theme.name == 'genshin'
    assert theme.bg_light == "#ECE5D8"
    print(f"  背景色: {theme.bg_light}")
    print(f"  主题色: {theme.accent_primary}")

    # 切换到 Cyberpunk 主题
    ThemeManager.set_theme('cyberpunk')
    theme = ThemeManager.get_theme()
    print(f"✓ 当前主题: {theme.display_name}")
    assert theme.name == 'cyberpunk'
    assert theme.bg_light == "#16213e"
    print(f"  背景色: {theme.bg_light}")
    print(f"  主题色: {theme.accent_primary}")
    print("✓ 主题切换成功\n")


def test_theme_properties():
    """测试主题属性"""
    print("=" * 50)
    print("测试主题属性...")

    ThemeManager.set_theme('genshin')
    theme = ThemeManager.get_theme()

    # 测试所有必需的颜色属性
    required_colors = [
        'bg_light', 'bg_dark', 'bg_input',
        'accent_primary', 'accent_primary_dark', 'accent_primary_light',
        'text_primary', 'text_header', 'text_title', 'text_path',
        'text_secondary', 'text_highlight',
        'btn_grad_start', 'btn_grad_end',
        'icon_color', 'hover_bg', 'close_btn_hover',
        'success_color', 'error_color', 'panel_overlay',
        'font_family'
    ]

    for prop in required_colors:
        value = getattr(theme, prop)
        assert value is not None, f"属性 {prop} 未定义"
        print(f"  ✓ {prop}: {value}")

    print("✓ 所有主题属性完整\n")


def test_stylesheet_generation():
    """测试样式表生成"""
    print("=" * 50)
    print("测试样式表生成...")

    ThemeManager.set_theme('cyberpunk')
    theme = ThemeManager.get_theme()

    # 测试主样式表
    main_style = theme.get_main_stylesheet()
    assert 'QMainWindow' in main_style
    assert theme.bg_light in main_style
    print("✓ 主样式表生成成功")

    # 测试按钮样式表
    for style_type in ['primary', 'secondary', 'icon']:
        btn_style = theme.get_button_stylesheet(style_type)
        assert 'QPushButton' in btn_style
        print(f"✓ {style_type} 按钮样式表生成成功")

    print("✓ 样式表生成成功\n")


def main():
    """主测试函数"""
    print("\n🧪 主题系统测试开始\n")

    try:
        test_theme_registration()
        test_theme_switching()
        test_theme_properties()
        test_stylesheet_generation()

        print("=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        return 0

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
