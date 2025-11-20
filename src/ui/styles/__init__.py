"""UI Styles Package - Multi-Theme System"""
from .theme_base import Theme, ThemeManager
from .theme_genshin import GenshinTheme
from .theme_cyberpunk import CyberpunkTheme


def initialize_themes():
    """初始化主题系统"""
    # 注册所有主题
    ThemeManager.register_theme(GenshinTheme())
    ThemeManager.register_theme(CyberpunkTheme())

    # 设置默认主题
    ThemeManager.set_theme('genshin')


def apply_global_style(app):
    """应用全局样式

    Args:
        app: QApplication 实例
    """
    # 初始化主题
    initialize_themes()

    # 获取当前主题
    theme = ThemeManager.get_theme()

    # 应用主样式表
    app.setStyleSheet(theme.get_main_stylesheet())


__all__ = [
    'Theme',
    'ThemeManager',
    'GenshinTheme',
    'CyberpunkTheme',
    'initialize_themes',
    'apply_global_style'
]
