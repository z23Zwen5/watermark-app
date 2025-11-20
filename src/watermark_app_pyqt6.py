#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Layer Watermark App - PyQt6 Genshin Impact Style
Version: 1.6.2 (PyQt6)
"""

import sys
import os
import json
import numpy as np
import threading
import time
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSlider, QComboBox, QListWidget,
    QProgressBar, QCheckBox, QScrollArea, QFrame, QGroupBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QIntValidator
import qtawesome as qta

# Import from existing text_label_module
from text_label_module import TextLabelConfig, draw_text_label, get_system_fonts


class WatermarkLayer:
    """水印图层类"""
    def __init__(self, image_path, opacity=100, blend_mode='normal', visible=True):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGBA")
        self.opacity = int(opacity)
        self.blend_mode = blend_mode
        self.visible = visible
        self.name = os.path.basename(image_path)

    def __str__(self):
        visibility = "👁️" if self.visible else "🚫"
        return f"{visibility} {self.name} ({self.blend_mode}, {self.opacity}%)"


class CustomTitleBar(QWidget):
    """Custom title bar for frameless window"""
    close_requested = pyqtSignal()
    minimize_requested = pyqtSignal()
    maximize_restore_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setObjectName("CustomTitleBar")

        # App Icon (placeholder)
        self.icon_label = QLabel("🎨")
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(10)

        # Title Label
        self.title_label = QLabel("Multi-Layer Watermark App v1.6.2")
        self.title_label.setObjectName("TitleLabel")
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(1)

        # Control Buttons
        self.minimize_btn = self._create_button(qta.icon('fa5s.window-minimize', color='#D3BC8E'), "minimize_button")
        self.maximize_restore_btn = self._create_button(qta.icon('fa5s.window-maximize', color='#D3BC8E'), "maximize_button")
        self.close_btn = self._create_button(qta.icon('fa5s.times', color='#D3BC8E'), "close_button")

        self.minimize_btn.clicked.connect(self.minimize_requested.emit)
        self.maximize_restore_btn.clicked.connect(self.maximize_restore_requested.emit)
        self.close_btn.clicked.connect(self.close_requested.emit)

        self.layout.addWidget(self.minimize_btn)
        self.layout.addWidget(self.maximize_restore_btn)
        self.layout.addWidget(self.close_btn)

        self.start_pos = None

    def _create_button(self, icon, obj_name):
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(16, 16))
        btn.setFixedSize(40, 40)
        btn.setObjectName(obj_name)
        return btn

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.globalPosition().toPoint()
            self.initial_pos = self.parent_window.pos()

    def mouseMoveEvent(self, event):
        if self.start_pos and self.parent_window.windowState() == Qt.WindowState.WindowNoState:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent_window.move(self.initial_pos + delta)

    def mouseReleaseEvent(self, event):
        self.start_pos = None

    def update_maximize_icon(self, is_maximized):
        if is_maximized:
            self.maximize_restore_btn.setIcon(qta.icon('fa5s.window-restore', color='#D3BC8E'))
        else:
            self.maximize_restore_btn.setIcon(qta.icon('fa5s.window-maximize', color='#D3BC8E'))


class MultiLayerWatermarkApp(QMainWindow):
    """主应用类 - Genshin Impact 风格"""

    # Signals for thread communication
    progress_update_signal = pyqtSignal(int)
    status_update_signal = pyqtSignal(str)
    processing_complete_signal = pyqtSignal(str, str)
    processing_error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Layer Watermark App v1.6.2")
        self.setObjectName("MainWindow")
        self.setMinimumSize(700, 850)

        # Frameless window with custom title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Central widget setup
        self.center_widget = QWidget()
        self.center_widget.setObjectName("CenterWidget")
        self.setCentralWidget(self.center_widget)
        self.main_layout = QVBoxLayout(self.center_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Custom Title Bar
        self.title_bar = CustomTitleBar(self)
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_restore_requested.connect(self.toggle_maximize_restore)
        self.main_layout.addWidget(self.title_bar)

        # Main content area
        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        self.main_layout.addWidget(self.content_frame)

        # Scroll area for content
        self.scroll_area = QScrollArea(self.content_frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ScrollArea")

        self.scroll_content = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)

        self.scroll_area.setWidget(self.scroll_content)

        frame_layout = QVBoxLayout(self.content_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.addWidget(self.scroll_area)

        # Initialize variables
        self.config_file = "multilayer_watermark_config.json"
        self.config_dir = "configs"
        os.makedirs(self.config_dir, exist_ok=True)

        self.images = []
        self.image_paths = []
        self.watermark_layers = []
        self.save_directory = None
        self.last_used_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None
        self.last_images_files = []

        self.stretch_var = False
        self.current_layer_index = None
        self._updating_opacity = False
        self.processing_thread = None

        self.text_label_config = TextLabelConfig()

        # Load configuration
        self.load_config()

        # Apply styling
        self.apply_genshin_style()

        # Create UI
        self.create_ui()

        # Auto-load last files
        self.auto_load_last_files()

        # Connect signals
        self.progress_update_signal.connect(self.update_progress_bar)
        self.status_update_signal.connect(self.update_status_label)
        self.processing_complete_signal.connect(self.on_processing_complete)
        self.processing_error_signal.connect(self.on_processing_error)

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_icon(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_icon(True)

    def apply_genshin_style(self):
        """应用原神风格的 QSS 样式"""
        self.setStyleSheet("""
            /* Main Window */
            QMainWindow#MainWindow {
                background: transparent;
            }

            QWidget#CenterWidget {
                background-color: #F0F1F6;
                border-radius: 18px;
                border: 2px solid #D3BC8E;
            }

            QFrame#ContentFrame {
                background-color: transparent;
            }

            /* Custom Title Bar */
            QWidget#CustomTitleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2B3041, stop:1 #3A4158);
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
                padding-left: 10px;
            }

            QLabel#TitleLabel {
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 15px;
                font-weight: bold;
                color: #D3BC8E;
                padding-left: 5px;
            }

            QPushButton#minimize_button, QPushButton#maximize_button, QPushButton#close_button {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }

            QPushButton#minimize_button:hover, QPushButton#maximize_button:hover {
                background-color: rgba(191, 160, 101, 0.3);
            }

            QPushButton#close_button:hover {
                background-color: rgba(224, 102, 102, 0.8);
            }

            QPushButton#minimize_button:pressed, QPushButton#maximize_button:pressed, QPushButton#close_button:pressed {
                background-color: rgba(141, 90, 60, 0.5);
            }

            /* Scroll Area */
            QScrollArea#ScrollArea {
                background-color: transparent;
                border: none;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
            }

            QScrollArea QWidget {
                background-color: #F0F1F6;
            }

            QScrollBar:vertical {
                border: 1px solid #D3BC8E;
                background: #ECE5D8;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D3BC8E, stop:1 #BFA065);
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #BFA065;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            /* Labels */
            QLabel {
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 13px;
                color: #1C2333;
            }

            /* Group Boxes */
            QGroupBox {
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 15px;
                font-weight: bold;
                color: #D3BC8E;
                border: 2px solid #BFA065;
                border-radius: 12px;
                margin-top: 20px;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8F9FA, stop:1 #ECE5D8);
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 15px;
                background-color: #ECE5D8;
                border: 1px solid #BFA065;
                border-radius: 8px;
                margin-left: 15px;
                margin-top: -10px;
            }

            /* Buttons */
            QPushButton {
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 13px;
                font-weight: 500;
                color: #1C2333;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D3BC8E, stop:1 #BFA065);
                border: 1px solid #BFA065;
                border-radius: 8px;
                padding: 8px 16px;
                min-height: 32px;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFE0B3, stop:1 #D3BC8E);
                border: 1px solid #D3BC8E;
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #BFA065, stop:1 #A68D5E);
            }

            QPushButton:disabled {
                background: #CCCCCC;
                color: #666666;
                border: 1px solid #999999;
            }

            /* Primary Action Button */
            QPushButton#applyButton {
                font-size: 15px;
                font-weight: bold;
                padding: 12px 30px;
                min-height: 45px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D3BC8E, stop:0.5 #BFA065, stop:1 #D3BC8E);
                border: 2px solid #BFA065;
            }

            QPushButton#applyButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFE0B3, stop:0.5 #D3BC8E, stop:1 #FFE0B3);
                border: 2px solid #D3BC8E;
            }

            /* List Widget */
            QListWidget {
                background-color: #FFFFFF;
                border: 2px solid #D3BC8E;
                border-radius: 8px;
                padding: 5px;
                outline: none;
            }

            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F1F6;
                color: #2B3041;
                border-radius: 4px;
                margin: 2px;
            }

            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFE0B3, stop:1 #D3BC8E);
                color: #1C2333;
                font-weight: bold;
            }

            QListWidget::item:hover {
                background-color: #FFF8E1;
            }

            /* Combo Box */
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #BFA065;
                border-radius: 8px;
                padding: 6px 12px;
                min-height: 30px;
                color: #1C2333;
            }

            QComboBox:hover {
                border: 2px solid #D3BC8E;
            }

            QComboBox::drop-down {
                border: none;
                width: 25px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #BFA065;
                margin-right: 8px;
            }

            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #BFA065;
                border-radius: 8px;
                selection-background-color: #D3BC8E;
                selection-color: #1C2333;
                outline: none;
            }

            /* Line Edit */
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #BFA065;
                border-radius: 8px;
                padding: 6px 12px;
                min-height: 30px;
                color: #1C2333;
            }

            QLineEdit:focus {
                border: 2px solid #D3BC8E;
            }

            /* Slider */
            QSlider::groove:horizontal {
                border: 1px solid #D3BC8E;
                height: 8px;
                background: #ECE5D8;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D3BC8E, stop:1 #BFA065);
                border: 2px solid #BFA065;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #FFE0B3;
                border: 2px solid #D3BC8E;
            }

            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D3BC8E, stop:1 #BFA065);
                border-radius: 4px;
            }

            /* Checkbox */
            QCheckBox {
                font-family: 'Segoe UI', 'Microsoft YaHei';
                font-size: 13px;
                color: #2B3041;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #BFA065;
                border-radius: 4px;
                background-color: #FFFFFF;
            }

            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #D3BC8E, stop:1 #BFA065);
                border: 2px solid #BFA065;
            }

            QCheckBox::indicator:hover {
                border: 2px solid #D3BC8E;
            }

            /* Progress Bar */
            QProgressBar {
                border: 2px solid #BFA065;
                border-radius: 10px;
                text-align: center;
                color: #1C2333;
                background-color: #ECE5D8;
                height: 25px;
                font-weight: bold;
            }

            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D3BC8E, stop:0.5 #BFA065, stop:1 #D3BC8E);
                border-radius: 8px;
            }
        """)

    def create_ui(self):
        """创建用户界面"""
        # Title section
        title_label = QLabel("Multi-Layer Watermark Tool")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #BFA065; padding: 10px;")
        self.content_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        subtitle_label = QLabel("🎨 Multi-Layer with Blend Modes")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #D3BC8E; padding-bottom: 10px;")
        self.content_layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create sections
        self.create_upload_section()
        self.create_layer_section()
        self.create_settings_section()
        self.create_text_label_section()
        self.create_progress_section()
        self.create_save_section()
        self.create_action_section()

        self.content_layout.addStretch(1)

    def create_upload_section(self):
        """创建文件上传区域"""
        upload_group = QGroupBox("📁 File Upload")
        layout = QVBoxLayout(upload_group)
        layout.setSpacing(10)

        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(10)

        self.upload_image_btn = QPushButton("Upload Images")
        self.upload_image_btn.setIcon(qta.icon('fa5s.images', color='#1C2333'))
        self.upload_image_btn.clicked.connect(self.upload_images)
        btn_layout.addWidget(self.upload_image_btn)
        btn_layout.addStretch(1)

        layout.addWidget(btn_frame)
        self.content_layout.addWidget(upload_group)

    def create_layer_section(self):
        """创建图层管理区域"""
        layer_group = QGroupBox("🎨 Watermark Layers")
        layout = QVBoxLayout(layer_group)
        layout.setSpacing(10)

        tip_label = QLabel("💡 Larger layer numbers appear on top (覆盖下层)")
        tip_label.setStyleSheet("color: #666666; font-size: 11px;")
        layout.addWidget(tip_label)

        self.layer_listbox = QListWidget()
        self.layer_listbox.setMinimumHeight(150)
        self.layer_listbox.itemSelectionChanged.connect(self.on_layer_select)
        layout.addWidget(self.layer_listbox)

        # Layer control buttons
        btn_frame = QFrame()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(8)

        add_btn = QPushButton("Add")
        add_btn.setIcon(qta.icon('fa5s.plus', color='#1C2333'))
        add_btn.clicked.connect(self.add_watermark_layer)
        btn_layout.addWidget(add_btn)

        toggle_btn = QPushButton("Toggle")
        toggle_btn.setIcon(qta.icon('fa5s.eye', color='#1C2333'))
        toggle_btn.clicked.connect(self.toggle_layer_visibility)
        btn_layout.addWidget(toggle_btn)

        remove_btn = QPushButton("Remove")
        remove_btn.setIcon(qta.icon('fa5s.trash', color='#1C2333'))
        remove_btn.clicked.connect(self.remove_selected_layer)
        btn_layout.addWidget(remove_btn)

        up_btn = QPushButton("↑")
        up_btn.clicked.connect(lambda: self.move_layer(-1))
        btn_layout.addWidget(up_btn)

        down_btn = QPushButton("↓")
        down_btn.clicked.connect(lambda: self.move_layer(1))
        btn_layout.addWidget(down_btn)

        btn_layout.addStretch(1)
        layout.addWidget(btn_frame)

        # Layer editor panel
        editor_group = QGroupBox("Layer Properties")
        editor_group.setStyleSheet("""
            QGroupBox {
                border: 1px dashed #BFA065;
                background-color: #F8F9FA;
                padding-top: 25px;
                margin-top: 15px;
                border-radius: 8px;
                font-size: 13px;
            }
            QGroupBox::title {
                background-color: #F8F9FA;
                color: #BFA065;
            }
        """)
        editor_layout = QVBoxLayout(editor_group)
        editor_layout.setSpacing(10)

        # Blend mode
        blend_row = QHBoxLayout()
        blend_row.addWidget(QLabel("Blend Mode:"))
        self.blend_mode_combo = QComboBox()
        self.blend_mode_combo.addItems(['normal', 'overlay', 'screen', 'soft_light'])
        self.blend_mode_combo.currentTextChanged.connect(self.on_blend_mode_change)
        blend_row.addWidget(self.blend_mode_combo)
        blend_row.addStretch(1)
        editor_layout.addLayout(blend_row)

        # Opacity
        opacity_row = QHBoxLayout()
        opacity_row.addWidget(QLabel("Opacity (%):"))

        self.opacity_entry = QLineEdit()
        self.opacity_entry.setValidator(QIntValidator(0, 100))
        self.opacity_entry.setText("100")
        self.opacity_entry.setFixedWidth(60)
        self.opacity_entry.textChanged.connect(self.on_opacity_entry_change)
        opacity_row.addWidget(self.opacity_entry)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.on_opacity_slider_change)
        opacity_row.addWidget(self.opacity_slider)

        editor_layout.addLayout(opacity_row)
        layout.addWidget(editor_group)

        # Initially disable editor
        self.set_editor_enabled(False)

        self.content_layout.addWidget(layer_group)

    def create_settings_section(self):
        """创建基础设置区域"""
        settings_group = QGroupBox("⚙️ Settings")
        layout = QVBoxLayout(settings_group)
        layout.setSpacing(10)

        self.stretch_checkbox = QCheckBox("Stretch watermark to fit image")
        self.stretch_checkbox.setChecked(self.stretch_var)
        self.stretch_checkbox.stateChanged.connect(self.on_stretch_change)
        layout.addWidget(self.stretch_checkbox)

        self.content_layout.addWidget(settings_group)

    def create_text_label_section(self):
        """创建文本标注设置区域"""
        label_group = QGroupBox("🔤 Text Label (文字标注)")
        layout = QVBoxLayout(label_group)
        layout.setSpacing(10)

        # Enable label
        self.label_enabled_checkbox = QCheckBox("Enable text label (add number or filename)")
        self.label_enabled_checkbox.setChecked(self.text_label_config.enabled)
        self.label_enabled_checkbox.stateChanged.connect(self.on_label_enabled_change)
        layout.addWidget(self.label_enabled_checkbox)

        # Label Type
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Label Type:"))
        self.label_type_combo = QComboBox()
        self.label_type_combo.addItems(['number', 'filename'])
        self.label_type_combo.setCurrentText(self.text_label_config.label_type)
        self.label_type_combo.currentTextChanged.connect(self.on_label_type_change)
        type_row.addWidget(self.label_type_combo)
        type_row.addStretch(1)
        layout.addLayout(type_row)

        # Position
        position_row = QHBoxLayout()
        position_row.addWidget(QLabel("Position:"))
        self.label_position_combo = QComboBox()
        self.label_position_combo.addItems(['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'])
        self.label_position_combo.setCurrentText(self.text_label_config.position)
        self.label_position_combo.currentTextChanged.connect(self.on_label_position_change)
        position_row.addWidget(self.label_position_combo)
        position_row.addStretch(1)
        layout.addLayout(position_row)

        # Orientation
        orientation_row = QHBoxLayout()
        orientation_row.addWidget(QLabel("Orientation:"))
        self.label_orientation_combo = QComboBox()
        self.label_orientation_combo.addItems(['horizontal', 'vertical'])
        self.label_orientation_combo.setCurrentText(self.text_label_config.orientation)
        self.label_orientation_combo.currentTextChanged.connect(self.on_label_orientation_change)
        orientation_row.addWidget(self.label_orientation_combo)
        orientation_row.addStretch(1)
        layout.addLayout(orientation_row)

        # Font
        font_row = QHBoxLayout()
        font_row.addWidget(QLabel("Font:"))
        self.label_font_combo = QComboBox()
        system_fonts = get_system_fonts()
        self.label_font_combo.addItems(['(Auto)'] + sorted(system_fonts.keys()))
        self.label_font_combo.setCurrentText(self.text_label_config.font_name or '(Auto)')
        self.label_font_combo.currentTextChanged.connect(self.on_label_font_change)
        font_row.addWidget(self.label_font_combo)
        font_row.addStretch(1)
        layout.addLayout(font_row)

        # Font Size
        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("Font Size:"))
        self.label_font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.label_font_size_slider.setRange(5, 100)
        self.label_font_size_slider.setValue(int(self.text_label_config.font_size * 10))
        self.label_font_size_slider.valueChanged.connect(self.on_label_font_size_change)
        size_row.addWidget(self.label_font_size_slider)

        self.label_font_size_display = QLabel(f"{self.text_label_config.font_size:.1f}%")
        self.label_font_size_display.setStyleSheet("color: #666666; font-size: 11px;")
        size_row.addWidget(self.label_font_size_display)

        layout.addLayout(size_row)

        tip_label = QLabel("💡 Number: 1, 2, 3... | Filename: image_name")
        tip_label.setStyleSheet("color: #666666; font-size: 10px;")
        layout.addWidget(tip_label)

        self.content_layout.addWidget(label_group)

    def create_progress_section(self):
        """创建进度显示区域"""
        progress_frame = QFrame()
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(5)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready to process")
        self.status_label.setStyleSheet("color: #666666; font-size: 12px;")
        progress_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addWidget(progress_frame)

    def create_save_section(self):
        """创建保存目录区域"""
        save_frame = QFrame()
        save_layout = QHBoxLayout(save_frame)
        save_layout.setContentsMargins(0, 0, 0, 0)
        save_layout.setSpacing(10)

        self.save_dir_btn = QPushButton("Select Save Directory")
        self.save_dir_btn.setIcon(qta.icon('fa5s.folder-open', color='#1C2333'))
        self.save_dir_btn.clicked.connect(self.select_save_directory)
        save_layout.addWidget(self.save_dir_btn)

        self.save_dir_label = QLabel("No directory selected")
        self.save_dir_label.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #D3BC8E;
            border-radius: 8px;
            padding: 8px 12px;
            color: #2B3041;
        """)
        self.save_dir_label.setWordWrap(True)
        save_layout.addWidget(self.save_dir_label, 1)

        self.content_layout.addWidget(save_frame)
        self.update_save_dir_label()

    def create_action_section(self):
        """创建操作按钮区域"""
        self.apply_btn = QPushButton("🚀 Apply Multi-Layer Watermark")
        self.apply_btn.setObjectName("applyButton")
        self.apply_btn.clicked.connect(self.apply_watermark_threaded)
        self.content_layout.addWidget(self.apply_btn)

    def set_editor_enabled(self, enabled: bool):
        """启用/禁用编辑器"""
        self.blend_mode_combo.setEnabled(enabled)
        self.opacity_entry.setEnabled(enabled)
        self.opacity_slider.setEnabled(enabled)

    # Layer management methods
    def add_watermark_layer(self):
        """添加水印图层"""
        initial_dir = self.last_watermark_directory or os.path.expanduser("~")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Add Watermark Layer", initial_dir, "Image files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            layer = WatermarkLayer(file_path, opacity=100, blend_mode='normal')
            self.watermark_layers.append(layer)
            self.last_watermark_directory = os.path.dirname(file_path)
            self.update_layer_listbox()
            self.layer_listbox.setCurrentRow(len(self.watermark_layers) - 1)
            self.save_config()

    def on_layer_select(self):
        """当选中图层时"""
        selection = self.layer_listbox.currentRow()
        if selection == -1:
            self.current_layer_index = None
            self.set_editor_enabled(False)
            return

        self.current_layer_index = selection
        layer = self.watermark_layers[selection]

        self.set_editor_enabled(True)
        self._updating_opacity = True
        try:
            self.blend_mode_combo.setCurrentText(layer.blend_mode)
            self.opacity_entry.setText(str(int(layer.opacity)))
            self.opacity_slider.setValue(int(layer.opacity))
        finally:
            self._updating_opacity = False

    def on_blend_mode_change(self, new_mode):
        """混合模式改变"""
        if self.current_layer_index is None:
            return
        layer = self.watermark_layers[self.current_layer_index]
        layer.blend_mode = new_mode
        self.update_layer_listbox_silent(self.current_layer_index)
        self.save_config()

    def on_opacity_entry_change(self, value_str):
        """不透明度输入改变"""
        if self._updating_opacity or self.current_layer_index is None or not value_str:
            return
        try:
            opacity = int(value_str)
            if 0 <= opacity <= 100:
                layer = self.watermark_layers[self.current_layer_index]
                layer.opacity = opacity
                self._updating_opacity = True
                try:
                    self.opacity_slider.setValue(opacity)
                finally:
                    self._updating_opacity = False
                self.update_layer_listbox_silent(self.current_layer_index)
                self.save_config()
        except ValueError:
            pass

    def on_opacity_slider_change(self, value):
        """滑块改变"""
        if self._updating_opacity or self.current_layer_index is None:
            return
        layer = self.watermark_layers[self.current_layer_index]
        layer.opacity = value
        self._updating_opacity = True
        try:
            self.opacity_entry.setText(str(value))
        finally:
            self._updating_opacity = False
        self.update_layer_listbox_silent(self.current_layer_index)
        self.save_config()

    def remove_selected_layer(self):
        """删除选中的图层"""
        selection = self.layer_listbox.currentRow()
        if selection == -1:
            QMessageBox.warning(self, "Warning", "Please select a layer first!")
            return
        del self.watermark_layers[selection]
        self.update_layer_listbox()
        if self.watermark_layers:
            new_index = min(selection, len(self.watermark_layers) - 1)
            self.layer_listbox.setCurrentRow(new_index)
        else:
            self.current_layer_index = None
            self.set_editor_enabled(False)
        self.save_config()

    def move_layer(self, direction):
        """移动图层"""
        selection = self.layer_listbox.currentRow()
        if selection == -1:
            QMessageBox.warning(self, "Warning", "Please select a layer first!")
            return
        new_index = selection + direction
        if 0 <= new_index < len(self.watermark_layers):
            self.watermark_layers[selection], self.watermark_layers[new_index] = \
                self.watermark_layers[new_index], self.watermark_layers[selection]
            self.update_layer_listbox()
            self.layer_listbox.setCurrentRow(new_index)
            self.save_config()

    def toggle_layer_visibility(self):
        """切换图层可见性"""
        selection = self.layer_listbox.currentRow()
        if selection == -1:
            QMessageBox.warning(self, "Warning", "Please select a layer first!")
            return
        layer = self.watermark_layers[selection]
        layer.visible = not layer.visible
        self.update_layer_listbox_silent(selection)
        self.save_config()

    def update_layer_listbox(self):
        """更新图层列表"""
        self.layer_listbox.clear()
        for i, layer in enumerate(self.watermark_layers):
            self.layer_listbox.addItem(f"[{i+1}] {layer}")

    def update_layer_listbox_silent(self, selected_index=None):
        """静默更新图层列表"""
        try:
            self.layer_listbox.itemSelectionChanged.disconnect(self.on_layer_select)
        except TypeError:
            pass
        self.layer_listbox.clear()
        for i, layer in enumerate(self.watermark_layers):
            self.layer_listbox.addItem(f"[{i+1}] {layer}")
        if selected_index is not None and 0 <= selected_index < len(self.watermark_layers):
            self.layer_listbox.setCurrentRow(selected_index)
        self.layer_listbox.itemSelectionChanged.connect(self.on_layer_select)

    # Blend mode algorithms (from original code)
    def apply_blend_mode(self, base_array, layer_array, blend_mode, opacity):
        """应用混合模式"""
        opacity_factor = opacity / 100.0
        blend_alpha = layer_array[:, :, 3]

        if np.max(blend_alpha) < 1:
            return base_array

        if blend_mode == 'normal':
            result = base_array.copy()
            base_rgb = base_array[:, :, :3].astype(np.uint16)
            blend_rgb = layer_array[:, :, :3].astype(np.uint16)
            alpha = blend_alpha.astype(np.uint16)[:, :, np.newaxis]
            alpha = (alpha * opacity) // 100
            result_rgb = (base_rgb * (255 - alpha) + blend_rgb * alpha) // 255
            result[:, :, :3] = result_rgb.astype(np.uint8)
            return result

        blend_alpha_f = blend_alpha.astype(np.float32) / 255.0
        mask = blend_alpha_f * opacity_factor
        has_alpha = mask > 0.001
        if not np.any(has_alpha):
            return base_array

        base_rgb = base_array[:, :, :3].astype(np.float32) / 255.0
        blend_rgb = layer_array[:, :, :3].astype(np.float32) / 255.0

        if blend_mode == 'screen':
            result_rgb = 1.0 - (1.0 - base_rgb) * (1.0 - blend_rgb)
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        elif blend_mode == 'overlay':
            result_rgb = np.where(base_rgb < 0.5,
                                 2 * base_rgb * blend_rgb,
                                 1.0 - 2 * (1.0 - base_rgb) * (1.0 - blend_rgb))
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        elif blend_mode == 'soft_light':
            result_rgb = np.where(blend_rgb < 0.5,
                                 2 * base_rgb * blend_rgb + base_rgb * base_rgb * (1 - 2 * blend_rgb),
                                 2 * base_rgb * (1 - blend_rgb) + np.sqrt(np.maximum(base_rgb, 0)) * (2 * blend_rgb - 1))
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        else:
            result_rgb = base_rgb

        mask_3d = mask[:, :, np.newaxis]
        result_rgb = result_rgb * mask_3d + base_rgb * (1 - mask_3d)

        result = base_array.copy()
        result[:, :, :3] = (np.clip(result_rgb, 0, 1) * 255).astype(np.uint8)
        return result

    def apply_multilayer_watermark(self, image):
        """应用多图层水印"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        result = np.array(image, dtype=np.uint8)
        stretch = self.stretch_var
        img_width, img_height = image.size

        total_visible_layers = sum(1 for layer in self.watermark_layers if layer.visible)
        processed_layers = 0

        for layer in self.watermark_layers:
            if not layer.visible:
                continue

            if stretch:
                new_width, new_height = img_width, img_height
            else:
                watermark_ratio = layer.image.width / layer.image.height
                img_ratio = img_width / img_height
                if img_ratio > watermark_ratio:
                    new_width = img_width
                    new_height = int(new_width / watermark_ratio)
                else:
                    new_height = img_height
                    new_width = int(new_height * watermark_ratio)

            resized_watermark = layer.image.resize((new_width, new_height), Image.Resampling.BILINEAR)
            position = ((img_width - new_width) // 2, (img_height - new_height) // 2)

            layer_array = np.zeros((img_height, img_width, 4), dtype=np.uint8)
            watermark_array = np.array(resized_watermark)

            y1, y2 = position[1], position[1] + new_height
            x1, x2 = position[0], position[0] + new_width
            layer_array[y1:y2, x1:x2] = watermark_array

            result = self.apply_blend_mode(result, layer_array, layer.blend_mode, layer.opacity)

            processed_layers += 1
            if total_visible_layers > 0:
                progress = (processed_layers / total_visible_layers) * 50
                self.progress_update_signal.emit(int(progress))

        return Image.fromarray(result, 'RGBA')

    def apply_watermark_threaded(self):
        """在线程中处理水印"""
        if self.processing_thread and self.processing_thread.is_alive():
            QMessageBox.warning(self, "Processing", "Please wait for current processing!")
            return

        self.apply_btn.setEnabled(False)
        self.apply_btn.setText("Processing...")
        self.processing_thread = threading.Thread(target=self._apply_watermark_task)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _apply_watermark_task(self):
        """水印处理任务"""
        if not self.images:
            self.processing_error_signal.emit("Please upload images first!")
            return
        if not self.watermark_layers:
            self.processing_error_signal.emit("Please add at least one watermark layer!")
            return
        if not any(layer.visible for layer in self.watermark_layers):
            self.processing_error_signal.emit("At least one layer must be visible!")
            return
        if not self.save_directory:
            if self.last_used_directory:
                self.save_directory = self.last_used_directory
            else:
                self.processing_error_signal.emit("Please select a save directory!")
                return

        start_time = time.time()

        try:
            total_images = len(self.images)
            for i, image in enumerate(self.images):
                filename = os.path.basename(self.image_paths[i])
                self.status_update_signal.emit(f"Processing {i+1}/{total_images}: {filename}")

                output = self.apply_multilayer_watermark(image.copy())

                if self.text_label_config.enabled:
                    output = draw_text_label(output, filename, self.text_label_config, index=i+1)

                if output.mode == 'RGBA':
                    rgb_image = Image.new('RGB', output.size, (255, 255, 255))
                    rgb_image.paste(output, mask=output.split()[3])
                    output = rgb_image

                filename_without_ext = os.path.splitext(filename)[0]
                output_filename = f"{filename_without_ext}_multilayer.jpg"
                output_path = os.path.join(self.save_directory, output_filename)
                output.save(output_path, 'JPEG', quality=95, optimize=True)

                progress = 50 + ((i + 1) / total_images) * 50
                self.progress_update_signal.emit(int(progress))

            end_time = time.time()
            processing_time = end_time - start_time
            message = f"Successfully processed {total_images} images!\nTime: {processing_time:.2f}s\nFormat: JPG (Quality 95)"
            self.processing_complete_signal.emit(f"✅ Done! {total_images} images in {processing_time:.2f}s", message)

        except Exception as e:
            self.processing_error_signal.emit(f"Processing failed: {str(e)}")

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_status_label(self, text):
        self.status_label.setText(text)

    def on_processing_complete(self, status_text, message):
        self.status_label.setText(status_text)
        QMessageBox.information(self, "Complete", message)
        self.apply_btn.setEnabled(True)
        self.apply_btn.setText("🚀 Apply Multi-Layer Watermark")
        self.progress_bar.setValue(0)

    def on_processing_error(self, error_message):
        self.status_label.setText(f"❌ Error: {error_message}")
        QMessageBox.critical(self, "Error", error_message)
        self.apply_btn.setEnabled(True)
        self.apply_btn.setText("🚀 Apply Multi-Layer Watermark")
        self.progress_bar.setValue(0)

    # Configuration methods
    def load_config(self):
        """加载配置"""
        try:
            config_path = os.path.join(self.config_dir, self.config_file)
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
                    self.stretch_var = config.get('last_stretch', False)
                    self.last_images_files = config.get('last_images_files', [])

                    layers_info = config.get('layers', [])
                    for layer_info in layers_info:
                        if os.path.exists(layer_info['path']):
                            layer = WatermarkLayer(
                                layer_info['path'],
                                int(layer_info.get('opacity', 100)),
                                str(layer_info.get('blend_mode', 'normal')),
                                bool(layer_info.get('visible', True))
                            )
                            self.watermark_layers.append(layer)

                    text_label_info = config.get('text_label', {})
                    if text_label_info:
                        self.text_label_config.from_dict(text_label_info)
        except Exception as e:
            print(f"❌ Error loading config: {e}")

    def save_config(self):
        """保存配置"""
        try:
            layers_info = []
            for layer in self.watermark_layers:
                layers_info.append({
                    'path': layer.image_path,
                    'opacity': int(layer.opacity),
                    'blend_mode': str(layer.blend_mode),
                    'visible': bool(layer.visible)
                })

            config = {
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory,
                'last_stretch': self.stretch_var,
                'last_images_files': self.last_images_files,
                'layers': layers_info,
                'text_label': self.text_label_config.to_dict()
            }

            os.makedirs(self.config_dir, exist_ok=True)
            config_path = os.path.join(self.config_dir, self.config_file)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error saving config: {e}")

    # Event handlers
    def on_stretch_change(self, state):
        self.stretch_var = bool(state == Qt.CheckState.Checked.value)
        self.save_config()

    def on_label_enabled_change(self, state):
        self.text_label_config.enabled = bool(state == Qt.CheckState.Checked.value)
        self.save_config()

    def on_label_type_change(self, text):
        self.text_label_config.label_type = text
        self.save_config()

    def on_label_position_change(self, text):
        self.text_label_config.position = text
        self.save_config()

    def on_label_orientation_change(self, text):
        self.text_label_config.orientation = text
        self.save_config()

    def on_label_font_change(self, text):
        self.text_label_config.font_name = None if text == '(Auto)' else text
        self.save_config()

    def on_label_font_size_change(self, value):
        self.text_label_config.font_size = value / 10.0
        self.label_font_size_display.setText(f"{self.text_label_config.font_size:.1f}%")
        self.save_config()

    def auto_load_last_files(self):
        """自动加载上次使用的文件"""
        try:
            if self.last_images_files:
                valid_files = [f for f in self.last_images_files if os.path.exists(f)]
                if valid_files:
                    self.image_paths = valid_files
                    self.images = [Image.open(file_path) for file_path in valid_files]
                    print(f"🖼️ Auto-loaded {len(valid_files)} images")

            if self.watermark_layers:
                self.update_layer_listbox()
                if self.watermark_layers:
                    self.layer_listbox.setCurrentRow(0)
                print(f"🎨 Auto-loaded {len(self.watermark_layers)} layers")
        except Exception as e:
            print(f"⚠️ Error during auto-load: {e}")

    def upload_images(self):
        """上传图片"""
        initial_dir = self.last_images_directory or os.path.expanduser("~")
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Upload Images", initial_dir, "Image files (*.jpg *.jpeg *.png)"
        )
        if file_paths:
            self.image_paths = file_paths
            self.images = [Image.open(file_path) for file_path in file_paths]
            self.last_images_directory = os.path.dirname(file_paths[0])
            self.last_used_directory = self.last_images_directory
            self.last_images_files = list(file_paths)
            if not self.save_directory:
                self.save_directory = self.last_used_directory
            self.update_save_dir_label()
            self.save_config()

    def select_save_directory(self):
        """选择保存目录"""
        initial_dir = self.last_used_directory or os.path.expanduser("~")
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory", initial_dir)
        if directory:
            self.save_directory = directory
            self.last_used_directory = directory
            self.update_save_dir_label()
            self.save_config()

    def update_save_dir_label(self):
        """更新保存目录标签"""
        text = self.save_directory if self.save_directory else "No directory selected"
        self.save_dir_label.setText(text)


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    main_window = MultiLayerWatermarkApp()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
