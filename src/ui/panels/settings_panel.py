#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Panel - General Application Settings
设置面板
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox, QLabel, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal
from ..styles.theme_base import ThemeManager


class SettingsPanel(QWidget):
    """设置面板"""

    # 信号
    stretch_changed = pyqtSignal(bool)
    theme_changed = pyqtSignal(str)  # 主题名称

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stretch_var = False
        self.current_theme = 'genshin'  # 默认主题
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        group = QGroupBox("General Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)
        vbox.setSpacing(15)

        # 主题选择
        theme_row = QHBoxLayout()
        theme_label = QLabel("UI Theme:")
        theme_label.setStyleSheet("font-weight: bold; min-width: 80px;")

        self.theme_combo = QComboBox()
        # 获取所有可用主题
        available_themes = ThemeManager.get_available_themes()

        # 添加主题选项（带显示名称）
        theme_display_names = {
            'genshin': '🎨 Genshin Impact',
            'cyberpunk': '🌆 Cyberpunk 2077'
        }

        for theme_name in available_themes:
            display_name = theme_display_names.get(theme_name, theme_name.capitalize())
            self.theme_combo.addItem(display_name, theme_name)

        # 设置当前主题
        current_theme = ThemeManager.get_theme()
        index = self.theme_combo.findData(current_theme.name)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            self.current_theme = current_theme.name

        self.theme_combo.currentIndexChanged.connect(self._on_theme_change)

        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        vbox.addLayout(theme_row)

        # 拉伸选项
        self.chk_stretch = QCheckBox("Stretch watermark to fit image")
        self.chk_stretch.setChecked(self.stretch_var)
        self.chk_stretch.stateChanged.connect(self._on_stretch_change)

        vbox.addWidget(self.chk_stretch)

    def _on_stretch_change(self, state):
        """拉伸选项改变"""
        self.stretch_var = (state == Qt.CheckState.Checked.value)
        self.stretch_changed.emit(self.stretch_var)

    def _on_theme_change(self, index):
        """主题改变"""
        if index >= 0:
            theme_name = self.theme_combo.itemData(index)
            if theme_name and theme_name != self.current_theme:
                self.current_theme = theme_name
                self.theme_changed.emit(theme_name)

    def set_stretch(self, value):
        """设置拉伸选项"""
        self.stretch_var = value
        self.chk_stretch.setChecked(value)

    def get_stretch(self):
        """获取拉伸选项"""
        return self.stretch_var

    def set_theme(self, theme_name):
        """设置主题"""
        index = self.theme_combo.findData(theme_name)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            self.current_theme = theme_name

    def get_theme(self):
        """获取当前主题"""
        return self.current_theme
