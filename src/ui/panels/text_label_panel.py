#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Label Panel - Text Annotation Configuration
文本标注面板
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QComboBox, QSlider, QLabel, QGroupBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from text_label_module import get_system_fonts, scan_fonts_async


class TextLabelPanel(QWidget):
    """文本标注面板"""

    # 信号
    config_changed = pyqtSignal(dict)  # 完整的配置字典

    def __init__(self, text_label_config, parent=None):
        super().__init__(parent)
        self.text_label_config = text_label_config
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        group = QGroupBox("Text Label")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)

        # 启用复选框
        self.chk_label = QCheckBox("Enable Text Label")
        self.chk_label.setChecked(self.text_label_config.enabled)
        self.chk_label.stateChanged.connect(self._on_enabled_change)
        vbox.addWidget(self.chk_label)

        # 配置容器
        self.label_container = QWidget()
        l_layout = QVBoxLayout(self.label_container)
        l_layout.setContentsMargins(0, 5, 0, 0)
        l_layout.setSpacing(12)

        # 内容和位置
        grid = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Content:"))
        self.cb_type = QComboBox()
        self.cb_type.addItems(['number', 'filename'])
        self.cb_type.setCurrentText(self.text_label_config.label_type)
        self.cb_type.currentTextChanged.connect(self._on_type_change)
        col1.addWidget(self.cb_type)

        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Position:"))
        self.cb_pos = QComboBox()
        self.cb_pos.addItems(['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'])
        self.cb_pos.setCurrentText(self.text_label_config.position)
        self.cb_pos.currentTextChanged.connect(self._on_position_change)
        col2.addWidget(self.cb_pos)

        grid.addLayout(col1)
        grid.addLayout(col2)
        l_layout.addLayout(grid)

        # 字体选择
        row_font = QHBoxLayout()
        self.cb_font = QComboBox()

        # 获取字体（从缓存或空）
        sys_fonts_dict = get_system_fonts()
        if sys_fonts_dict:
            # 缓存可用，直接加载
            sys_fonts = sorted(sys_fonts_dict.keys())
            self.cb_font.addItems(['(Auto)'] + sys_fonts)
        else:
            # 缓存不可用，显示加载提示并触发后台扫描
            self.cb_font.addItems(['(Auto)', '(Loading fonts...)'])
            # 触发异步扫描
            scan_fonts_async(self._on_fonts_loaded)

        self.cb_font.setCurrentText(self.text_label_config.font_name or '(Auto)')
        self.cb_font.currentTextChanged.connect(self._on_font_change)
        self.cb_font.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_font.addWidget(QLabel("Font:"))
        row_font.addWidget(self.cb_font)
        l_layout.addLayout(row_font)

        # 字体大小
        row_size = QHBoxLayout()
        row_size.addWidget(QLabel("Size:"))
        self.sld_font_size = QSlider(Qt.Orientation.Horizontal)
        self.sld_font_size.setRange(5, 100)
        self.sld_font_size.setValue(int(self.text_label_config.font_size * 10))
        self.sld_font_size.valueChanged.connect(self._on_font_size_change)
        self.lbl_font_size = QLabel(f"{self.text_label_config.font_size:.1f}%")
        self.lbl_font_size.setFixedWidth(45)
        self.lbl_font_size.setStyleSheet("font-weight: bold;")

        row_size.addWidget(self.sld_font_size)
        row_size.addWidget(self.lbl_font_size)
        l_layout.addLayout(row_size)

        vbox.addWidget(self.label_container)
        self.label_container.setVisible(self.text_label_config.enabled)

    def _on_enabled_change(self, state):
        """启用状态改变"""
        is_checked = (state == Qt.CheckState.Checked.value)
        self.text_label_config.enabled = is_checked
        self.label_container.setVisible(is_checked)
        self._emit_config()

    def _on_type_change(self, t):
        """标注类型改变"""
        self.text_label_config.label_type = t
        self._emit_config()

    def _on_position_change(self, p):
        """位置改变"""
        self.text_label_config.position = p
        self._emit_config()

    def _on_font_change(self, f):
        """字体改变"""
        self.text_label_config.font_name = None if f == '(Auto)' else f
        self._emit_config()

    def _on_font_size_change(self, val):
        """字体大小改变"""
        self.text_label_config.font_size = val / 10.0
        self.lbl_font_size.setText(f"{val / 10.0:.1f}%")
        self._emit_config()

    def _emit_config(self):
        """发射配置改变信号"""
        self.config_changed.emit(self.text_label_config.to_dict())

    def _on_fonts_loaded(self, fonts_dict):
        """字体加载完成回调（从后台线程调用）"""
        # 使用 QTimer 在主线程更新 UI
        QTimer.singleShot(0, lambda: self._update_font_list(fonts_dict))

    def _update_font_list(self, fonts_dict):
        """更新字体列表（在主线程）"""
        # 保存当前选择
        current_font = self.cb_font.currentText()

        # 清空并重新填充
        self.cb_font.clear()
        sys_fonts = sorted(fonts_dict.keys())
        self.cb_font.addItems(['(Auto)'] + sys_fonts)

        # 恢复之前的选择
        if current_font and current_font != '(Loading fonts...)':
            index = self.cb_font.findText(current_font)
            if index >= 0:
                self.cb_font.setCurrentIndex(index)

        print(f"✅ UI已更新，加载 {len(sys_fonts)} 个字体")

    def get_config(self):
        """获取配置"""
        return self.text_label_config
