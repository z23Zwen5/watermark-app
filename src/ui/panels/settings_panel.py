#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Panel - General Application Settings
设置面板
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal


class SettingsPanel(QWidget):
    """设置面板"""

    # 信号
    stretch_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stretch_var = False
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        group = QGroupBox("General Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)

        # 拉伸选项
        self.chk_stretch = QCheckBox("Stretch watermark to fit image")
        self.chk_stretch.setChecked(self.stretch_var)
        self.chk_stretch.stateChanged.connect(self._on_stretch_change)

        vbox.addWidget(self.chk_stretch)

    def _on_stretch_change(self, state):
        """拉伸选项改变"""
        self.stretch_var = (state == Qt.CheckState.Checked.value)
        self.stretch_changed.emit(self.stretch_var)

    def set_stretch(self, value):
        """设置拉伸选项"""
        self.stretch_var = value
        self.chk_stretch.setChecked(value)

    def get_stretch(self):
        """获取拉伸选项"""
        return self.stretch_var
