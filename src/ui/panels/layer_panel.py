#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layer Panel - Watermark Layer Management
图层管理面板
"""
import os
import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QSlider, QComboBox, QLabel, QFrame,
    QGroupBox, QListWidgetItem, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta
from watermark_core import WatermarkLayer
from ..styles.theme_base import ThemeManager


class LayerPanel(QWidget):
    """图层管理面板"""

    # 信号
    layer_added = pyqtSignal(object)  # WatermarkLayer
    layer_removed = pyqtSignal(int)   # index
    layer_modified = pyqtSignal(int, dict)  # index, changes
    visibility_toggled = pyqtSignal(int)
    layer_moved = pyqtSignal(int, int)  # from_index, to_index
    layers_changed = pyqtSignal()  # 图层发生任何变化

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.theme = ThemeManager.get_theme()
        self.watermark_layers = []
        self.current_layer_index = None
        self._updating_opacity = False
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        t0 = time.time()
        group = QGroupBox("Watermark Layers")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)
        vbox.setSpacing(10)
        print(f"      ⏱️  图层面板-基础布局: {(time.time() - t0)*1000:.0f}ms")

        # 图层列表
        t0 = time.time()
        self.layer_list = QListWidget()
        self.layer_list.setMinimumHeight(150)
        self.layer_list.itemSelectionChanged.connect(self._on_layer_select)
        vbox.addWidget(self.layer_list)
        print(f"      ⏱️  图层面板-列表控件: {(time.time() - t0)*1000:.0f}ms")

        # 工具栏
        t0 = time.time()
        hbox_tools = QHBoxLayout()
        cmds = [
            ('fa5s.plus', self._add_layer, "Add Layer"),
            ('fa5s.eye', self._toggle_visibility, "Toggle Visibility"),
            ('fa5s.trash', self._remove_layer, "Remove"),
            ('fa5s.arrow-up', lambda: self._move_layer(-1), "Move Up"),
            ('fa5s.arrow-down', lambda: self._move_layer(1), "Move Down")
        ]

        for icon, func, tip in cmds:
            t1 = time.time()
            btn = QPushButton()
            btn.setIcon(qta.icon(icon, color=self.theme.icon_color))
            btn.setFixedSize(34, 34)
            btn.setToolTip(tip)
            btn.clicked.connect(func)
            btn.setStyleSheet(self.theme.get_button_stylesheet('icon'))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            hbox_tools.addWidget(btn)
            print(f"        ⏱️  图标按钮 {icon}: {(time.time() - t1)*1000:.0f}ms")

        hbox_tools.addStretch()
        vbox.addLayout(hbox_tools)
        print(f"      ⏱️  图层面板-工具栏: {(time.time() - t0)*1000:.0f}ms")

        # 属性面板
        t0 = time.time()
        self.prop_frame = QFrame()
        self.prop_frame.setStyleSheet(
            f"background: {self.theme.panel_overlay}; border-radius: 8px; "
            f"padding: 8px; border: 1px solid {self.theme.accent_primary_dark};"
        )
        prop_layout = QVBoxLayout(self.prop_frame)

        # 混合模式
        row1 = QHBoxLayout()
        lbl_blend = QLabel("Blend Mode:")
        lbl_blend.setStyleSheet("font-weight: bold;")
        row1.addWidget(lbl_blend)
        self.blend_combo = QComboBox()
        self.blend_combo.addItems(['normal', 'overlay', 'screen', 'soft_light'])
        self.blend_combo.currentTextChanged.connect(self._on_blend_mode_change)
        row1.addWidget(self.blend_combo, 1)
        prop_layout.addLayout(row1)

        # 透明度
        row2 = QHBoxLayout()
        lbl_op = QLabel("Opacity:")
        lbl_op.setStyleSheet("font-weight: bold;")
        row2.addWidget(lbl_op)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.valueChanged.connect(self._on_opacity_change)

        self.opacity_val = QLabel("100%")
        self.opacity_val.setStyleSheet(
            f"color: {self.theme.text_primary}; font-weight: bold; font-size: 11px;"
        )
        self.opacity_val.setFixedWidth(60)
        self.opacity_val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        row2.addWidget(self.opacity_slider)
        row2.addWidget(self.opacity_val)
        prop_layout.addLayout(row2)

        self.prop_frame.setEnabled(False)
        vbox.addWidget(self.prop_frame)
        print(f"      ⏱️  图层面板-属性面板: {(time.time() - t0)*1000:.0f}ms")

    def set_layers(self, layers):
        """设置图层列表"""
        self.watermark_layers = layers
        self._update_list()

    def get_layers(self):
        """获取图层列表"""
        return self.watermark_layers

    def _add_layer(self):
        """添加图层"""
        init_dir = self.config.last_watermark_directory or os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Watermark",
            init_dir,
            "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            layer = WatermarkLayer(path)
            self.watermark_layers.append(layer)
            self.config.last_watermark_directory = os.path.dirname(path)
            self._update_list()
            self.layer_added.emit(layer)
            self.layers_changed.emit()

    def _remove_layer(self):
        """删除选中的图层"""
        row = self.layer_list.currentRow()
        if row != -1:
            del self.watermark_layers[row]
            self._update_list()
            self.prop_frame.setEnabled(False)
            self.layer_removed.emit(row)
            self.layers_changed.emit()

    def _toggle_visibility(self):
        """切换图层可见性"""
        row = self.layer_list.currentRow()
        if row != -1:
            self.watermark_layers[row].visible = not self.watermark_layers[row].visible
            self._update_list()
            self.layer_list.setCurrentRow(row)
            self.visibility_toggled.emit(row)
            self.layers_changed.emit()

    def _move_layer(self, direction):
        """移动图层"""
        row = self.layer_list.currentRow()
        if row == -1:
            return

        new_row = row + direction
        if 0 <= new_row < len(self.watermark_layers):
            # 交换图层
            self.watermark_layers[row], self.watermark_layers[new_row] = \
                self.watermark_layers[new_row], self.watermark_layers[row]
            self._update_list()
            self.layer_list.setCurrentRow(new_row)
            self.layer_moved.emit(row, new_row)
            self.layers_changed.emit()

    def _update_list(self):
        """更新图层列表显示"""
        self.layer_list.clear()
        for i, layer in enumerate(self.watermark_layers):
            item = QListWidgetItem(f"  Layer {i+1}: {layer.name}")

            # 使用 fa5s 图标
            icon_name = 'fa5s.check-circle' if layer.visible else 'fa5s.circle'
            icon_color = self.theme.accent_primary if layer.visible else self.theme.text_secondary

            item.setIcon(qta.icon(icon_name, color=icon_color))
            self.layer_list.addItem(item)

    def _on_layer_select(self):
        """图层选中事件"""
        idx = self.layer_list.currentRow()
        if idx == -1:
            self.prop_frame.setEnabled(False)
            self.current_layer_index = None
            return

        self.prop_frame.setEnabled(True)
        self.current_layer_index = idx
        layer = self.watermark_layers[idx]

        self._updating_opacity = True
        self.blend_combo.setCurrentText(layer.blend_mode)
        self.opacity_slider.setValue(int(layer.opacity))
        self.opacity_val.setText(f"{int(layer.opacity)}%")
        self._updating_opacity = False

    def _on_blend_mode_change(self, text):
        """混合模式改变"""
        if self.current_layer_index is not None:
            self.watermark_layers[self.current_layer_index].blend_mode = text
            self.layer_modified.emit(self.current_layer_index, {'blend_mode': text})
            self.layers_changed.emit()

    def _on_opacity_change(self, val):
        """透明度改变"""
        if self._updating_opacity or self.current_layer_index is None:
            return

        self.watermark_layers[self.current_layer_index].opacity = val
        self.opacity_val.setText(f"{val}%")
        self.layer_modified.emit(self.current_layer_index, {'opacity': val})
        self.layers_changed.emit()
