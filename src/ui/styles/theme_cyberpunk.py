#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cyberpunk Theme
赛博朋克主题 - 霓虹色调，暗黑未来感
"""
from .theme_base import Theme


class CyberpunkTheme(Theme):
    """赛博朋克风格主题"""

    @property
    def name(self) -> str:
        return "cyberpunk"

    @property
    def display_name(self) -> str:
        return "Cyberpunk 2077"

    # === 颜色定义 ===

    @property
    def bg_light(self) -> str:
        return "#16213e"  # Dark Blue-Grey (Main Content)

    @property
    def bg_dark(self) -> str:
        return "#0a0e27"  # Very Dark Blue-Black (Sidebar/Header)

    @property
    def bg_input(self) -> str:
        return "#1a1a2e"  # Dark Input Background

    @property
    def accent_primary(self) -> str:
        return "#00d4ff"  # Electric Cyan (Primary Accent)

    @property
    def accent_primary_dark(self) -> str:
        return "#00a8cc"  # Deep Cyan (Borders)

    @property
    def accent_primary_light(self) -> str:
        return "#5dfdff"  # Bright Cyan (Highlights)

    @property
    def text_primary(self) -> str:
        return "#e0e0e0"  # Light Grey (Body Text)

    @property
    def text_header(self) -> str:
        return "#00d4ff"  # Electric Cyan (Headers)

    @property
    def text_title(self) -> str:
        return "#5dfdff"  # Bright Cyan (Window Title)

    @property
    def text_path(self) -> str:
        return "#00ffff"  # Neon Cyan (Path Display)

    @property
    def text_secondary(self) -> str:
        return "#7a8ba8"  # Muted Blue-Grey (Hints)

    @property
    def text_highlight(self) -> str:
        return "#ff2a6d"  # Hot Pink (Highlights)

    @property
    def btn_grad_start(self) -> str:
        return "#00d4ff"  # Cyan

    @property
    def btn_grad_end(self) -> str:
        return "#0077ff"  # Electric Blue

    @property
    def icon_color(self) -> str:
        return "#00d4ff"  # Cyan Icons

    @property
    def hover_bg(self) -> str:
        return "rgba(0, 212, 255, 0.15)"  # Glowing Cyan Overlay

    @property
    def close_btn_hover(self) -> str:
        return "#ff006e"  # Hot Pink/Magenta

    @property
    def success_color(self) -> str:
        return "#00ff41"  # Neon Green

    @property
    def error_color(self) -> str:
        return "#ff2a6d"  # Hot Pink

    @property
    def panel_overlay(self) -> str:
        return "rgba(10, 14, 39, 0.7)"  # Dark Semi-Transparent

    @property
    def font_family(self) -> str:
        return "'Consolas', 'Monaco', 'Courier New', 'Microsoft YaHei UI', monospace"

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
            background-color: rgba(10, 14, 39, 0.4);
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 6px 16px;
            background-color: {self.bg_dark};
            border: 1px solid {self.accent_primary};
            border-radius: 14px;
            color: {self.accent_primary_light};
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
            selection-color: {self.bg_dark};
        }}
        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {self.accent_primary};
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
            border: 1px solid {self.accent_primary};
            background-color: {self.bg_dark};
            color: {self.text_primary};
            selection-background-color: {self.accent_primary};
            selection-color: {self.bg_dark};
            outline: none;
            border-radius: 4px;
        }}

        /* List Widget */
        QListWidget {{
            background-color: {self.bg_input};
            border: 1px solid {self.accent_primary_dark};
            border-radius: 8px;
            outline: none;
        }}
        QListWidget::item {{
            height: 36px;
            padding-left: 5px;
            border-bottom: 1px solid rgba(0, 168, 204, 0.2);
            color: {self.text_primary};
            font-family: {self.font_family};
        }}
        QListWidget::item:selected {{
            background-color: rgba(0, 212, 255, 0.3);
            border-left: 4px solid {self.accent_primary};
            font-weight: bold;
            color: {self.accent_primary_light};
        }}
        QListWidget::item:hover {{
            background-color: {self.hover_bg};
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
            border-radius: 4px;
            background: {self.bg_input};
        }}
        QCheckBox::indicator:hover {{
            border-color: {self.accent_primary};
            background: {self.bg_dark};
        }}
        QCheckBox::indicator:checked {{
            background-color: {self.accent_primary};
            border: 2px solid {self.accent_primary_light};
        }}

        /* Sliders */
        QSlider {{
            min-height: 22px;
            background: transparent;
        }}
        QSlider::groove:horizontal {{
            border: 1px solid {self.accent_primary_dark};
            height: 6px;
            background: {self.bg_input};
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 {self.accent_primary}, stop:1 {self.btn_grad_end});
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: {self.accent_primary_light};
            border: 2px solid {self.accent_primary};
            width: 18px; height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{
            background: white;
            border-color: {self.accent_primary_light};
        }}

        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {self.accent_primary_dark};
            background-color: {self.bg_input};
            border-radius: 6px;
            text-align: center;
            color: {self.text_primary};
        }}
        QProgressBar::chunk {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                              stop:0 {self.accent_primary}, stop:1 {self.btn_grad_end});
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
            border: 1px solid {self.accent_primary};
            border-radius: 20px;
            color: {self.bg_dark};
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 15px;
            padding: 8px 20px;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {self.accent_primary_light}, stop:1 {self.accent_primary});
            border: 1px solid {self.accent_primary_light};
        }}
        QPushButton:pressed {{
            background-color: {self.btn_grad_end};
            padding-top: 10px;
        }}
        QPushButton:disabled {{
            background-color: #2a2a3e;
            border: 1px solid #444;
            color: #666;
        }}
    """
        elif style_type == 'secondary':
            return f"""
        QPushButton {{
            background-color: {self.bg_dark};
            border: 1px solid {self.accent_primary_dark};
            border-radius: 18px;
            color: {self.text_primary};
            font-family: {self.font_family};
            font-weight: bold;
            font-size: 13px;
            padding: 6px 15px;
        }}
        QPushButton:hover {{
            background-color: {self.bg_input};
            border: 1px solid {self.accent_primary};
            color: {self.accent_primary_light};
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
            border-bottom: 2px solid {self.accent_primary};
            border-radius: 0px;
            color: {self.bg_dark};
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
            color: {self.accent_primary_light};
        }}
    """
