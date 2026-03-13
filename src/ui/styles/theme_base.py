#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme System - Abstract Base and Theme Manager
主题系统 - 抽象基类和主题管理器
"""
import os
from abc import ABC, abstractmethod


class Theme(ABC):
    """主题抽象基类

    所有主题必须实现这个接口
    """

    # === 基础信息 ===
    @property
    @abstractmethod
    def name(self) -> str:
        """主题名称"""
        pass

    @property
    @abstractmethod
    def display_name(self) -> str:
        """显示名称"""
        pass

    # === 颜色定义 ===

    # 背景色
    @property
    @abstractmethod
    def bg_light(self) -> str:
        """浅色背景"""
        pass

    @property
    @abstractmethod
    def bg_dark(self) -> str:
        """深色背景"""
        pass

    @property
    @abstractmethod
    def bg_input(self) -> str:
        """输入框背景"""
        pass

    # 主题色
    @property
    @abstractmethod
    def accent_primary(self) -> str:
        """主要强调色"""
        pass

    @property
    @abstractmethod
    def accent_primary_dark(self) -> str:
        """深色强调色（边框等）"""
        pass

    @property
    @abstractmethod
    def accent_primary_light(self) -> str:
        """浅色强调色（文本等）"""
        pass

    # 文本色
    @property
    @abstractmethod
    def text_primary(self) -> str:
        """主要文本"""
        pass

    @property
    @abstractmethod
    def text_header(self) -> str:
        """标题文本"""
        pass

    @property
    @abstractmethod
    def text_title(self) -> str:
        """窗口标题文本"""
        pass

    @property
    @abstractmethod
    def text_path(self) -> str:
        """路径显示文本"""
        pass

    @property
    @abstractmethod
    def text_secondary(self) -> str:
        """次要文本（灰色提示）"""
        pass

    @property
    @abstractmethod
    def text_highlight(self) -> str:
        """高亮文本"""
        pass

    # 按钮渐变色
    @property
    @abstractmethod
    def btn_grad_start(self) -> str:
        """按钮渐变起始色"""
        pass

    @property
    @abstractmethod
    def btn_grad_end(self) -> str:
        """按钮渐变结束色"""
        pass

    # 特殊颜色
    @property
    @abstractmethod
    def icon_color(self) -> str:
        """图标颜色"""
        pass

    @property
    @abstractmethod
    def hover_bg(self) -> str:
        """悬停背景（半透明）"""
        pass

    @property
    @abstractmethod
    def close_btn_hover(self) -> str:
        """关闭按钮悬停色"""
        pass

    @property
    @abstractmethod
    def success_color(self) -> str:
        """成功图标颜色"""
        pass

    @property
    @abstractmethod
    def error_color(self) -> str:
        """错误图标颜色"""
        pass

    @property
    @abstractmethod
    def panel_overlay(self) -> str:
        """面板半透明覆盖层"""
        pass

    # === 字体 ===
    @property
    @abstractmethod
    def font_family(self) -> str:
        """字体族"""
        pass

    # === 资源路径 ===
    def get_asset_path(self, filename: str) -> str:
        """获取主题资源文件路径"""
        import sys

        # PyInstaller 打包后的路径处理
        if getattr(sys, 'frozen', False):
            # 运行在打包后的 exe 中
            base_path = sys._MEIPASS
        else:
            # 运行在开发环境中
            script_dir = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

        assets_dir = os.path.join(base_path, "assets", "ui", self.name)
        return os.path.join(assets_dir, filename).replace("\\", "/")

    @property
    def arrow_svg(self) -> str:
        """下拉箭头图标"""
        return self.get_asset_path("arrow.svg")

    @property
    def arrow_hover_svg(self) -> str:
        """悬停状态下拉箭头图标"""
        return self.get_asset_path("arrow_hover.svg")

    # === 样式表生成 ===

    @abstractmethod
    def get_main_stylesheet(self) -> str:
        """获取主窗口样式表"""
        pass

    @abstractmethod
    def get_button_stylesheet(self, style_type: str = 'primary') -> str:
        """获取按钮样式表

        Args:
            style_type: 'primary', 'secondary', 'icon'
        """
        pass

    @abstractmethod
    def get_mode_switcher_stylesheet(self) -> str:
        """获取模式切换 Tab 按钮样式表（使用 objectName 区分激活/非激活状态）"""
        pass


class ThemeManager:
    """主题管理器 - 单例模式"""

    _instance = None
    _current_theme: Theme = None
    _themes: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register_theme(cls, theme: Theme):
        """注册主题"""
        cls._themes[theme.name] = theme

    @classmethod
    def set_theme(cls, theme_name: str):
        """设置当前主题"""
        if theme_name in cls._themes:
            cls._current_theme = cls._themes[theme_name]
        else:
            raise ValueError(f"Theme '{theme_name}' not registered")

    @classmethod
    def get_theme(cls) -> Theme:
        """获取当前主题"""
        if cls._current_theme is None:
            raise RuntimeError("No theme set. Call set_theme() first.")
        return cls._current_theme

    @classmethod
    def get_available_themes(cls) -> list:
        """获取所有可用主题"""
        return list(cls._themes.keys())
