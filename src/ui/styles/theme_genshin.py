#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genshin Impact Theme
原神主题 - 米黄色调，温暖优雅
"""
from .theme_base import Theme


class GenshinTheme(Theme):
    """原神风格主题"""

    @property
    def name(self) -> str:
        return "genshin"

    @property
    def display_name(self) -> str:
        return "Genshin Impact"

    # === 颜色定义 ===

    @property
    def bg_light(self) -> str:
        return "#ECE5D8"  # Main Content Beige

    @property
    def bg_dark(self) -> str:
        return "#3B4252"  # Sidebar/Header Dark Blue-Grey

    @property
    def bg_input(self) -> str:
        return "#F7F3EB"  # Input fields background

    @property
    def accent_primary(self) -> str:
        return "#D3BC8E"  # Main Gold

    @property
    def accent_primary_dark(self) -> str:
        return "#A68D5E"  # Darker Gold (Borders)

    @property
    def accent_primary_light(self) -> str:
        return "#E3D2B6"  # Lighter Gold (Text)

    @property
    def text_primary(self) -> str:
        return "#1F2329"  # Dark Ink (Body)

    @property
    def text_header(self) -> str:
        return "#594D3C"  # Dark Earth Brown (Headers)

    @property
    def text_title(self) -> str:
        return "#E3D2B6"  # Light Gold (Window Title)

    @property
    def text_path(self) -> str:
        return "#2C3E50"  # Dark Blue-Grey (Path display)

    @property
    def text_secondary(self) -> str:
        return "#6F7685"  # 灰色提示文本

    @property
    def text_highlight(self) -> str:
        return "#E3D2B6"  # 高亮文本（金色）

    @property
    def btn_grad_start(self) -> str:
        return "#E0CFA8"

    @property
    def btn_grad_end(self) -> str:
        return "#BFA065"

    @property
    def icon_color(self) -> str:
        return "#3E3429"  # 深棕色图标

    @property
    def hover_bg(self) -> str:
        return "rgba(0, 0, 0, 0.08)"  # 浅色背景下的悬停

    @property
    def close_btn_hover(self) -> str:
        return "#FF5C5C"  # 关闭按钮红色

    @property
    def success_color(self) -> str:
        return "#2E7D32"  # 绿色

    @property
    def error_color(self) -> str:
        return "#C62828"  # 红色

    @property
    def panel_overlay(self) -> str:
        return "rgba(255, 255, 255, 0.4)"  # 半透明白色覆盖层

    @property
    def font_family(self) -> str:
        return "'HYWenHei-85W', 'Microsoft YaHei UI', 'Microsoft YaHei', 'Segoe UI', sans-serif"

    # === 样式表生成 ===

    def get_main_stylesheet(self) -> str:
        """获取主窗口样式表"""
        return f"""
        QMainWindow {{
            background: transparent;
        }}
        QWidget#CenterWidget {{
            background-color: {self.bg_light};
            border-radius: 12px;
            border: 2px solid {self.accent_primary};
        }}

        /* Generic Labels */
        QLabel {{
            font-family: {self.font_family};
            color: {self.text_primary};
            font-size: 14px;
            font-weight: 500;
        }}

        /* Scroll Area */
        QScrollArea {{ background: transparent; border: none; }}

        /* Group Boxes */
        QGroupBox {{
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 15px;
            color: {self.text_header};
            border: 1px solid {self.accent_primary_dark};
            border-radius: 12px;
            margin-top: 28px;
            background-color: rgba(255, 255, 255, 0.3);
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 6px 16px;
            background-color: {self.btn_grad_start};
            border: 1px solid {self.accent_primary_dark};
            border-radius: 14px;
            color: #3E3429;
            left: 12px;
        }}

        /* Inputs */
        QLineEdit, QComboBox {{
            background-color: {self.bg_input};
            border: 1px solid {self.accent_primary_dark};
            border-radius: 8px;
            padding: 5px 12px;
            color: {self.text_primary};
            font-family: {self.font_family};
            selection-background-color: {self.accent_primary};
            selection-color: #3E3429;
        }}

        /* ComboBox */
        QComboBox {{
            padding-right: 40px;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 0px;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background: transparent;
        }}
        QComboBox::down-arrow {{
            image: url("{self.arrow_svg}");
            width: 16px;
            height: 16px;
            subcontrol-origin: padding;
            subcontrol-position: center;
        }}
        QComboBox::down-arrow:hover {{
            image: url("{self.arrow_hover_svg}");
        }}
        QComboBox::down-arrow:on {{
            image: url("{self.arrow_hover_svg}");
        }}
        QComboBox QAbstractItemView {{
            border: 1px solid {self.accent_primary_dark};
            background-color: #FFFBF0;
            color: {self.text_primary};
            selection-background-color: {self.accent_primary};
            selection-color: #3E3429;
            outline: none;
            border-radius: 4px;
        }}

        /* List Widget */
        QListWidget {{
            background-color: #F3F0EA;
            border: 1px solid {self.accent_primary_dark};
            border-radius: 8px;
            outline: none;
        }}
        QListWidget::item {{
            height: 36px;
            padding-left: 5px;
            border-bottom: 1px solid rgba(166, 141, 94, 0.2);
            color: {self.text_primary};
            font-family: {self.font_family};
        }}
        QListWidget::item:selected {{
            background-color: rgba(211, 188, 142, 0.6);
            border-left: 4px solid {self.accent_primary_dark};
            font-weight: bold;
        }}

        /* Checkboxes */
        QCheckBox {{
            spacing: 10px;
            font-size: 14px;
            color: {self.text_primary};
            font-family: {self.font_family};
            font-weight: bold;
        }}
        QCheckBox::indicator {{
            width: 20px; height: 20px;
            border: 2px solid {self.accent_primary_dark};
            border-radius: 12px;
            background: {self.bg_input};
        }}
        QCheckBox::indicator:hover {{
            border-color: {self.accent_primary};
            background: #FFF;
        }}
        QCheckBox::indicator:checked {{
            background-color: {self.accent_primary};
            border: 2px solid {self.accent_primary_dark};
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
            background: {self.accent_primary_dark};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: white;
            border: 2px solid {self.accent_primary_dark};
            width: 18px; height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{
            background: #FFFBF0;
            border-color: {self.accent_primary};
        }}

        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {self.accent_primary_dark};
            background-color: #D0D0D0;
            border-radius: 6px;
            text-align: center;
            color: #333;
        }}
        QProgressBar::chunk {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                              stop:0 {self.accent_primary}, stop:1 #F0D8A8);
            border-radius: 5px;
        }}
    """

    def get_button_stylesheet(self, style_type: str = 'primary') -> str:
        """获取按钮样式表"""
        if style_type == 'primary':
            return f"""
        QPushButton {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.btn_grad_start}, stop:1 {self.btn_grad_end});
            border: 1px solid #8C7446;
            border-radius: 20px;
            color: #3E3429;
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 15px;
            padding: 8px 20px;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFF4D6, stop:1 {self.btn_grad_start});
            border: 1px solid {self.accent_primary};
        }}
        QPushButton:pressed {{
            background-color: {self.btn_grad_end};
            padding-top: 10px;
        }}
        QPushButton:disabled {{
            background-color: #CCC;
            border: 1px solid #999;
            color: #666;
        }}
    """
        elif style_type == 'secondary':
            return f"""
        QPushButton {{
            background-color: #FBF9F5;
            border: 1px solid {self.accent_primary_dark};
            border-radius: 18px;
            color: {self.text_primary};
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 13px;
            padding: 6px 15px;
        }}
        QPushButton:hover {{
            background-color: #FFF;
            border: 1px solid {self.accent_primary};
        }}
    """
        elif style_type == 'icon':
            return f"""
        QPushButton {{
            background: transparent;
            border: none;
            border-radius: 15px;
        }}
        QPushButton:hover {{
            background-color: {self.hover_bg};
        }}
    """
        else:
            return ""

    def get_mode_switcher_stylesheet(self) -> str:
        """获取模式切换 Tab 按钮样式表"""
        return f"""
        QWidget#ModeSwitcherBar {{
            background-color: {self.bg_dark};
            border-bottom: 1px solid {self.accent_primary_dark};
        }}
        QPushButton#ModeBtnActive {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.btn_grad_start}, stop:1 {self.btn_grad_end});
            border: none;
            border-bottom: 2px solid {self.accent_primary_dark};
            border-radius: 0px;
            color: #3E3429;
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 13px;
            padding: 6px 28px;
            min-height: 36px;
            max-height: 36px;
        }}
        QPushButton#ModeBtnInactive {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            border-radius: 0px;
            color: {self.accent_primary_light};
            font-family: {self.font_family};
            font-size: 13px;
            padding: 6px 28px;
            min-height: 36px;
            max-height: 36px;
        }}
        QPushButton#ModeBtnInactive:hover {{
            background-color: {self.hover_bg};
            border-bottom: 2px solid {self.accent_primary};
            color: {self.text_primary};
        }}
    """
