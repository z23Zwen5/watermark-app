#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genshin Impact Style Theme for PyQt6
原神风格主题样式定义
"""
import os

# === 颜色常量 ===
class Colors:
    """颜色定义"""
    # Backgrounds
    BG_LIGHT = "#ECE5D8"       # Main Content Beige
    BG_DARK = "#3B4252"        # Sidebar/Header Dark Blue-Grey
    BG_INPUT = "#F7F3EB"       # Input fields background

    # Accents
    ACCENT_GOLD = "#D3BC8E"    # Main Gold
    ACCENT_GOLD_DARK = "#A68D5E"  # Darker Gold (Borders)
    ACCENT_GOLD_LIGHT = "#E3D2B6"  # Lighter Gold (Text)

    # Text Colors
    TEXT_PRIMARY = "#1F2329"   # Dark Ink (Body)
    TEXT_HEADER = "#594D3C"    # Dark Earth Brown (Headers)
    TEXT_TITLE = "#E3D2B6"     # Light Gold (Window Title)
    TEXT_PATH = "#2C3E50"      # Dark Blue-Grey (Path display)

    # Gradients
    BTN_GRAD_1 = "#E0CFA8"
    BTN_GRAD_2 = "#BFA065"


# === 字体设置 ===
FONT_FAMILY = "'HYWenHei-85W', 'Microsoft YaHei UI', 'Microsoft YaHei', 'Segoe UI', sans-serif"


# === 资源路径 ===
def get_asset_path(filename):
    """获取资源文件路径"""
    import sys

    # PyInstaller 打包后的路径处理
    if getattr(sys, 'frozen', False):
        # 运行在打包后的 exe 中
        base_path = sys._MEIPASS
    else:
        # 运行在开发环境中
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

    assets_dir = os.path.join(base_path, "assets", "ui")
    return os.path.join(assets_dir, filename).replace("\\", "/")


ARROW_SVG = get_asset_path("arrow.svg")
ARROW_HOVER_SVG = get_asset_path("arrow_hover.svg")


# === 样式表 ===
class GenshinStyleSheet:
    """集中管理所有 QSS 样式"""

    @staticmethod
    def get_main_style():
        """获取主窗口样式"""
        return f"""
        QMainWindow {{
            background: transparent;
        }}
        QWidget#CenterWidget {{
            background-color: {Colors.BG_LIGHT};
            border-radius: 12px;
            border: 2px solid {Colors.ACCENT_GOLD};
        }}

        /* Generic Labels */
        QLabel {{
            font-family: {FONT_FAMILY};
            color: {Colors.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 500;
        }}

        /* Scroll Area */
        QScrollArea {{ background: transparent; border: none; }}

        /* Group Boxes */
        QGroupBox {{
            font-family: {FONT_FAMILY};
            font-weight: bold;
            font-size: 15px;
            color: {Colors.TEXT_HEADER};
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 12px;
            margin-top: 28px;
            background-color: rgba(255, 255, 255, 0.3);
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 6px 16px;
            background-color: {Colors.BTN_GRAD_1};
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 14px;
            color: #3E3429;
            left: 12px;
        }}

        /* --- Inputs (Text & ComboBox) --- */
        QLineEdit, QComboBox {{
            background-color: {Colors.BG_INPUT};
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 8px;
            padding: 5px 12px;
            color: {Colors.TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            selection-background-color: {Colors.ACCENT_GOLD};
            selection-color: #3E3429;
        }}

       /* ComboBox Optimization */
        QComboBox {{
            padding-right: 40px;
        }}

        /* 下拉按钮区域（容器） */
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;

            border-left-width: 0px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background: transparent;
        }}

        /* 下拉箭头图标 - 基础定义 */
        QComboBox::down-arrow {{
            image: url("{ARROW_SVG}");
            width: 16px;
            height: 16px;

            subcontrol-origin: padding;
            subcontrol-position: center;
        }}

        /* 悬停时状态 */
        QComboBox::down-arrow:hover {{
            image: url("{ARROW_HOVER_SVG}");
        }}
        QComboBox::down-arrow:on {{
            image: url("{ARROW_HOVER_SVG}");
        }}

        /* 下拉列表弹窗样式 */
        QComboBox QAbstractItemView {{
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            background-color: #FFFBF0;
            color: {Colors.TEXT_PRIMARY};
            selection-background-color: {Colors.ACCENT_GOLD};
            selection-color: #3E3429;
            outline: none;
            border-radius: 4px;
        }}

        /* List Widget */
        QListWidget {{
            background-color: #F3F0EA;
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 8px;
            outline: none;
        }}
        QListWidget::item {{
            height: 36px;
            padding-left: 5px;
            border-bottom: 1px solid rgba(166, 141, 94, 0.2);
            color: {Colors.TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
        }}
        QListWidget::item:selected {{
            background-color: rgba(211, 188, 142, 0.6);
            border-left: 4px solid {Colors.ACCENT_GOLD_DARK};
            font-weight: bold;
        }}

        /* --- Circular Checkboxes --- */
        QCheckBox {{
            spacing: 10px;
            font-size: 14px;
            color: {Colors.TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            font-weight: bold;
        }}
        QCheckBox::indicator {{
            width: 20px; height: 20px;
            border: 2px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 12px;
            background: {Colors.BG_INPUT};
        }}
        QCheckBox::indicator:hover {{
            border-color: {Colors.ACCENT_GOLD};
            background: #FFF;
        }}
        QCheckBox::indicator:checked {{
            background-color: {Colors.ACCENT_GOLD};
            border: 2px solid {Colors.ACCENT_GOLD_DARK};
        }}

        /* Sliders */
        QSlider {{
            min-height: 22px;
            background: transparent;
        }}

        QSlider::groove:horizontal {{
            border: 1px solid #BBB;
            height: 6px;
            background: #D0D0D0;
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: {Colors.ACCENT_GOLD_DARK};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: white;
            border: 2px solid {Colors.ACCENT_GOLD_DARK};
            width: 18px; height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{
            background: #FFFBF0;
            border-color: {Colors.ACCENT_GOLD};
        }}

        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            background-color: #D0D0D0;
            border-radius: 6px;
            text-align: center;
            color: #333;
        }}
        QProgressBar::chunk {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                              stop:0 {Colors.ACCENT_GOLD}, stop:1 #F0D8A8);
            border-radius: 5px;
        }}
    """

    @staticmethod
    def get_button_style(style_type='primary'):
        """获取按钮样式

        Args:
            style_type: 按钮类型 ('primary', 'secondary', 'icon')
        """
        if style_type == 'primary':
            return f"""
        QPushButton {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {Colors.BTN_GRAD_1}, stop:1 {Colors.BTN_GRAD_2});
            border: 1px solid #8C7446;
            border-radius: 20px;
            color: #3E3429;
            font-family: {FONT_FAMILY};
            font-weight: bold;
            font-size: 15px;
            padding: 8px 20px;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF4D6, stop:1 {Colors.BTN_GRAD_1});
            border: 1px solid {Colors.ACCENT_GOLD};
        }}
        QPushButton:pressed {{
            background-color: {Colors.BTN_GRAD_2};
            padding-top: 10px;
        }}
        QPushButton:disabled {{
            background-color: #CCC; border: 1px solid #999; color: #666;
        }}
    """
        elif style_type == 'secondary':
            return f"""
        QPushButton {{
            background-color: #FBF9F5;
            border: 1px solid {Colors.ACCENT_GOLD_DARK};
            border-radius: 18px;
            color: {Colors.TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            font-weight: bold;
            font-size: 13px;
            padding: 6px 15px;
        }}
        QPushButton:hover {{
            background-color: #FFF;
            border: 1px solid {Colors.ACCENT_GOLD};
        }}
    """
        elif style_type == 'icon':
            return """
        QPushButton { background: transparent; border: none; border-radius: 15px; }
        QPushButton:hover { background-color: rgba(166, 141, 94, 0.2); }
    """
        else:
            return ""


def apply_global_style(app):
    """应用全局样式到应用程序"""
    app.setStyleSheet(GenshinStyleSheet.get_main_style())
