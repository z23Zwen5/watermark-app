#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Layer Watermark App - PyQt6 UI Layer
Style: Genshin Impact (Blue Title Bar / Flat Dialog Panels / Clean Look)
"""

import sys
import os
import threading
import time
from PIL import Image
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSlider, QComboBox, QListWidget,
    QProgressBar, QCheckBox, QScrollArea, QFrame, QGroupBox, QMessageBox, 
    QFileDialog, QSizePolicy, QGraphicsDropShadowEffect, QSplitter, 
    QListWidgetItem, QDialog 
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QIntValidator, QColor, QIcon
import qtawesome as qta

# Import core business logic
from watermark_core import WatermarkLayer, WatermarkConfig, BatchProcessor
from text_label_module import get_system_fonts

# --- GENSHIN STYLE CONSTANTS ---
# Backgrounds
C_BG_LIGHT = "#ECE5D8"       # Main Content Beige
C_BG_DARK = "#3B4252"        # Sidebar/Header Dark Blue-Grey (The "Blue" you like)
C_BG_INPUT = "#F7F3EB"       # Input fields background

# Accents
C_ACCENT_GOLD = "#D3BC8E"    # Main Gold
C_ACCENT_GOLD_DARK = "#A68D5E" # Darker Gold (Borders)
C_ACCENT_GOLD_LIGHT = "#E3D2B6" # Lighter Gold (Text)

# Text Colors
C_TEXT_PRIMARY = "#1F2329"   # Dark Ink (Body)
C_TEXT_HEADER = "#594D3C"    # Dark Earth Brown (Headers)
C_TEXT_TITLE = "#E3D2B6"     # Light Gold (Window Title)
C_TEXT_PATH = "#2C3E50"      # Dark Blue-Grey (Path display)

# Gradients
C_BTN_GRAD_1 = "#E0CFA8"
C_BTN_GRAD_2 = "#BFA065"

# Fonts
FONT_FAMILY = "'HYWenHei-85W', 'Microsoft YaHei UI', 'Microsoft YaHei', 'Segoe UI', sans-serif"

# Resource paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Go up from src/ to project root
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets", "ui")
ARROW_SVG = os.path.join(ASSETS_DIR, "arrow.svg").replace("\\", "/")
ARROW_HOVER_SVG = os.path.join(ASSETS_DIR, "arrow_hover.svg").replace("\\", "/")

class GenshinStyleSheet:
    """Centralized QSS Definition"""
    MAIN = f"""
        QMainWindow {{
            background: transparent;
        }}
        QWidget#CenterWidget {{
            background-color: {C_BG_LIGHT};
            border-radius: 12px;
            border: 2px solid {C_ACCENT_GOLD};
        }}
        
        /* Generic Labels */
        QLabel {{
            font-family: {FONT_FAMILY};
            color: {C_TEXT_PRIMARY};
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
            color: {C_TEXT_HEADER};
            border: 1px solid {C_ACCENT_GOLD_DARK};
            border-radius: 12px;
            margin-top: 28px;
            background-color: rgba(255, 255, 255, 0.3);
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 6px 16px;
            background-color: {C_BTN_GRAD_1};
            border: 1px solid {C_ACCENT_GOLD_DARK};
            border-radius: 14px;
            color: #3E3429;
            left: 12px;
        }}

        /* --- Inputs (Text & ComboBox) --- */
        QLineEdit, QComboBox {{
            background-color: {C_BG_INPUT};
            border: 1px solid {C_ACCENT_GOLD_DARK};
            border-radius: 8px;
            padding: 5px 12px;
            color: {C_TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            selection-background-color: {C_ACCENT_GOLD};
            selection-color: #3E3429;
        }}
        
       /* ComboBox Optimization */
        QComboBox {{
            padding-right: 20px;
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
        
        /* 使用 SVG 图片替换原来的 CSS 三角形 */
        QComboBox::down-arrow {{
            image: url("{ARROW_SVG}");  /* 正常状态图标 - 使用绝对路径 */
            width: 16px;              /* 必须给图标设置尺寸 */
            height: 16px;
            border: none;             /* 清除之前的边框绘制代码 */
            margin-right: 10px;
        }}

        /* 悬停时切换为高亮图标 */
        QComboBox::drop-down:hover QComboBox::down-arrow {{
            image: url("{ARROW_HOVER_SVG}"); /* 悬停状态图标 - 使用绝对路径 */
        }}
        
        /* ComboBox Popup Panel (保持不变) */
        QComboBox QAbstractItemView {{
            border: 1px solid {C_ACCENT_GOLD_DARK};
            background-color: #FFFBF0;
            color: {C_TEXT_PRIMARY}; /* Dark Text */
            selection-background-color: {C_ACCENT_GOLD};
            selection-color: #3E3429;
            outline: none;
            border-radius: 4px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: #F3F0EA;
            border: 1px solid {C_ACCENT_GOLD_DARK};
            border-radius: 8px;
            outline: none;
        }}
        QListWidget::item {{
            height: 36px;
            padding-left: 5px;
            border-bottom: 1px solid rgba(166, 141, 94, 0.2);
            color: {C_TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
        }}
        QListWidget::item:selected {{
            background-color: rgba(211, 188, 142, 0.6);
            border-left: 4px solid {C_ACCENT_GOLD_DARK};
            font-weight: bold;
        }}

        /* --- Circular Checkboxes --- */
        QCheckBox {{
            spacing: 10px;
            font-size: 14px;
            color: {C_TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            font-weight: bold;
        }}
        QCheckBox::indicator {{
            width: 20px; height: 20px;
            border: 2px solid {C_ACCENT_GOLD_DARK};
            border-radius: 12px;
            background: {C_BG_INPUT};
        }}
        QCheckBox::indicator:hover {{
            border-color: {C_ACCENT_GOLD};
            background: #FFF;
        }}
        QCheckBox::indicator:checked {{
            background-color: {C_ACCENT_GOLD};
            border: 2px solid {C_ACCENT_GOLD_DARK};
        }}

        /* Sliders */
        QSlider::groove:horizontal {{
            border: 1px solid #BBB;
            height: 6px;
            background: #D0D0D0;
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: {C_ACCENT_GOLD_DARK};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: white;
            border: 2px solid {C_ACCENT_GOLD_DARK};
            width: 18px; height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {C_ACCENT_GOLD_DARK};
            background-color: #D0D0D0;
            border-radius: 6px;
            text-align: center;
            color: #333;
        }}
        QProgressBar::chunk {{
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                              stop:0 {C_ACCENT_GOLD}, stop:1 #F0D8A8);
            border-radius: 5px;
        }}
    """

    # Button Styles
    BTN_PRIMARY = f"""
        QPushButton {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {C_BTN_GRAD_1}, stop:1 {C_BTN_GRAD_2});
            border: 1px solid #8C7446;
            border-radius: 20px;
            color: #3E3429;
            font-family: {FONT_FAMILY};
            font-weight: bold;
            font-size: 15px;
            padding: 8px 20px;
        }}
        QPushButton:hover {{
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFF4D6, stop:1 {C_BTN_GRAD_1});
            border: 1px solid {C_ACCENT_GOLD};
        }}
        QPushButton:pressed {{
            background-color: {C_BTN_GRAD_2};
            padding-top: 10px;
        }}
        QPushButton:disabled {{
            background-color: #CCC; border: 1px solid #999; color: #666;
        }}
    """

    BTN_SECONDARY = f"""
        QPushButton {{
            background-color: #FBF9F5;
            border: 1px solid {C_ACCENT_GOLD_DARK};
            border-radius: 18px;
            color: {C_TEXT_PRIMARY};
            font-family: {FONT_FAMILY};
            font-weight: bold;
            font-size: 13px;
            padding: 6px 15px;
        }}
        QPushButton:hover {{
            background-color: #FFF;
            border: 1px solid {C_ACCENT_GOLD};
        }}
    """
    
    BTN_ICON = f"""
        QPushButton {{ background: transparent; border: none; border-radius: 15px; }}
        QPushButton:hover {{ background-color: rgba(166, 141, 94, 0.2); }}
    """


class CustomTitleBar(QWidget):
    """Custom Title Bar (Main Window)"""
    close_requested = pyqtSignal()
    minimize_requested = pyqtSignal()
    maximize_restore_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(48) 
        self.setObjectName("CustomTitleBar")
        
        # 1. 开启背景绘制
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # 2. 样式表修改：
        # - 背景改为浅色 (C_BG_LIGHT)
        # - 底部加回一条淡金色的分割线 (border-bottom)，增加层次感
        # - 文字改为深棕色 (C_TEXT_HEADER)
        self.setStyleSheet(f"""
            QWidget#CustomTitleBar {{
                background-color: {C_BG_LIGHT};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid {C_ACCENT_GOLD}; 
            }}
            QLabel {{ 
                color: {C_TEXT_HEADER}; 
                font-family: {FONT_FAMILY};
                font-weight: 900; /* 特粗字体，增强雕刻感 */
                font-size: 16px; 
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)

        # 图标
        self.icon_label = QLabel("✦")
        self.icon_label.setStyleSheet(f"color: {C_ACCENT_GOLD_DARK}; font-size: 22px;")
        layout.addWidget(self.icon_label)
        
        # 标题
        self.title_label = QLabel("Multi-Layer Watermark Tool")
        
        # 3. 【雕刻特效】添加白色投影 (Letterpress Effect)
        # 深色文字 + 右下角白色投影 = 凹陷感
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)      # 边缘清晰，像刻出来的
        shadow.setColor(QColor(255, 255, 255, 180)) # 半透明白色
        shadow.setOffset(1, 1)       # 向右下偏移1像素
        self.title_label.setGraphicsEffect(shadow)
        
        layout.addWidget(self.title_label)
        layout.addStretch(1)

        # 4. 窗口控制按钮
        # 注意：因为背景变浅了，图标颜色(icon_color)需要改为深色 {C_TEXT_HEADER}
        self.minimize_btn = self._create_btn("fa5s.window-minimize", icon_color=C_TEXT_HEADER)
        self.maximize_btn = self._create_btn("fa5s.window-maximize", icon_color=C_TEXT_HEADER)
        self.close_btn = self._create_btn("fa5s.times", hover_color="#FF5C5C", icon_color=C_TEXT_HEADER)

        self.minimize_btn.clicked.connect(self.minimize_requested.emit)
        self.maximize_btn.clicked.connect(self.maximize_restore_requested.emit)
        self.close_btn.clicked.connect(self.close_requested.emit)

        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)

        self.start_pos = None

    # 修改了 _create_btn 方法，增加了 icon_color 参数
    def _create_btn(self, icon_name, hover_color=None, icon_color=C_ACCENT_GOLD):
        btn = QPushButton()
        # 使用传入的颜色 (深色)，而不是默认的金色
        btn.setIcon(qta.icon(icon_name, color=icon_color))
        btn.setFixedSize(36, 36)
        
        # 悬停背景色：深色模式下是半透明白，浅色模式下可以用半透明深色
        bg_hover = f"background-color: {hover_color};" if hover_color else f"background-color: rgba(0,0,0,0.08);"
        
        btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none; border-radius: 18px; }} 
            QPushButton:hover {{ {bg_hover} }}
        """)
        return btn

    def update_maximize_icon(self, is_maximized):
        icon = 'fa5s.window-restore' if is_maximized else 'fa5s.window-maximize'
        # 同样确保图标是深色的
        self.maximize_btn.setIcon(qta.icon(icon, color=C_TEXT_HEADER))

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


class GenshinMessageBox(QDialog):
    """Custom Genshin Style Dialog"""
    def __init__(self, parent, title, message, icon_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 220) 

        # Main Container
        self.widget = QWidget(self)
        self.widget.setGeometry(0, 0, 400, 220)
        self.widget.setStyleSheet(f"""
            QWidget {{
                background-color: {C_BG_LIGHT};
                border: 2px solid {C_ACCENT_GOLD};
                border-radius: 12px;
            }}
            QLabel {{
                border: none;
                font-family: {FONT_FAMILY};
            }}
        """)

        layout = QVBoxLayout(self.widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. Title Bar (Dark Blue)
        # Modified: Removed bottom border (underline) and bottom-radius for flat look
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {C_BG_DARK};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border-bottom: none; /* Removed underline */
            }}
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {C_TEXT_TITLE}; font-weight: bold; font-size: 15px; background: transparent;")
        
        btn_close = QPushButton()
        btn_close.setIcon(qta.icon('fa5s.times', color=C_ACCENT_GOLD))
        btn_close.setFixedSize(30, 30)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("QPushButton { background: transparent; border: none; } QPushButton:hover { background-color: rgba(255,255,255,0.1); border-radius: 15px; }")

        title_layout.addWidget(lbl_title)
        title_layout.addStretch()
        title_layout.addWidget(btn_close)

        layout.addWidget(title_bar)

        # 2. Content Area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 20, 30, 20)
        
        # Icon
        if icon_type == "success":
            lbl_icon = QLabel()
            lbl_icon.setPixmap(qta.icon('fa5s.check-circle', color='#2E7D32').pixmap(40, 40))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_icon.setStyleSheet("background: transparent; border: none;")
            content_layout.addWidget(lbl_icon)
        elif icon_type == "error":
            lbl_icon = QLabel()
            lbl_icon.setPixmap(qta.icon('fa5s.exclamation-circle', color='#C62828').pixmap(40, 40))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_icon.setStyleSheet("background: transparent; border: none;")
            content_layout.addWidget(lbl_icon)

        # Message Text
        lbl_msg = QLabel(message)
        lbl_msg.setWordWrap(True)
        lbl_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_msg.setStyleSheet(f"color: {C_TEXT_PRIMARY}; font-size: 14px; font-weight: 500; background: transparent; border: none;")
        
        content_layout.addWidget(lbl_msg)
        layout.addWidget(content_area)

        # 3. Button Area
        # Modified: Ensure background blends perfectly
        btn_area = QWidget()
        btn_area.setStyleSheet("background-color: transparent;")
        btn_layout = QHBoxLayout(btn_area)
        btn_layout.setContentsMargins(0, 0, 0, 20)
        
        btn_ok = QPushButton("Confirm")
        btn_ok.setFixedSize(120, 36)
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setStyleSheet(GenshinStyleSheet.BTN_PRIMARY)
        btn_ok.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_ok)
        layout.addWidget(btn_area)

        self._start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._start_pos:
            delta = event.globalPosition().toPoint() - self._start_pos
            self.move(self.pos() + delta)
            self._start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._start_pos = None


class MultiLayerWatermarkApp(QMainWindow):
    """Main Application Window"""

    progress_update_signal = pyqtSignal(int)
    status_update_signal = pyqtSignal(str)
    processing_complete_signal = pyqtSignal(str, str)
    processing_error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1100, 750)
        
        self.config = WatermarkConfig()
        self.config.load()
        self.images = []
        self.image_paths = []
        self.watermark_layers = self.config.layers.copy()
        self.text_label_config = self.config.text_label_config
        self.stretch_var = self.config.last_stretch
        self.processing_thread = None
        self.current_layer_index = None
        self._updating_opacity = False

        self.init_ui()
        self.auto_load_last_files()
        
        self.progress_update_signal.connect(self.update_progress_bar)
        self.status_update_signal.connect(self.update_status_label)
        self.processing_complete_signal.connect(self.on_processing_complete)
        self.processing_error_signal.connect(self.on_processing_error)

    def init_ui(self):
        self.setStyleSheet(GenshinStyleSheet.MAIN)
        self.center_widget = QWidget()
        self.center_widget.setObjectName("CenterWidget")
        self.setCentralWidget(self.center_widget)

        main_layout = QVBoxLayout(self.center_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_restore_requested.connect(self.toggle_maximize)
        main_layout.addWidget(self.title_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)

        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        self.create_upload_section(left_column)
        self.create_layer_section(left_column)
        
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        self.create_settings_section(right_column)
        self.create_text_label_section(right_column)
        right_column.addStretch()
        self.create_output_section(right_column)

        content_layout.addLayout(left_column, 55)
        content_layout.addLayout(right_column, 45)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_upload_section(self, layout):
        group = QGroupBox("Source Images")
        vbox = QVBoxLayout(group)
        
        self.upload_btn = QPushButton("  Select Images / Folder")
        self.upload_btn.setIcon(qta.icon('fa5s.images', color='#1F2329'))
        self.upload_btn.setStyleSheet(GenshinStyleSheet.BTN_SECONDARY)
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_images)
        self.upload_btn.setMinimumHeight(45)
        
        self.img_count_label = QLabel("No images selected")
        self.img_count_label.setStyleSheet(f"color: #6F7685; font-style: italic;")
        self.img_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        vbox.addWidget(self.upload_btn)
        vbox.addWidget(self.img_count_label)
        layout.addWidget(group)

    def create_layer_section(self, layout):
        group = QGroupBox("Watermark Layers")
        vbox = QVBoxLayout(group)
        vbox.setSpacing(10)

        self.layer_list = QListWidget()
        self.layer_list.setMinimumHeight(150)
        self.layer_list.itemSelectionChanged.connect(self.on_layer_select)
        vbox.addWidget(self.layer_list)

        hbox_tools = QHBoxLayout()
        cmds = [
            ('fa5s.plus', self.add_watermark_layer, "Add Layer"),
            ('fa5s.eye', self.toggle_layer_visibility, "Toggle Visibility"),
            ('fa5s.trash', self.remove_selected_layer, "Remove"),
            ('fa5s.arrow-up', lambda: self.move_layer(-1), "Move Up"),
            ('fa5s.arrow-down', lambda: self.move_layer(1), "Move Down")
        ]

        for icon, func, tip in cmds:
            btn = QPushButton()
            btn.setIcon(qta.icon(icon, color='#3E3429'))
            btn.setFixedSize(34, 34)
            btn.setToolTip(tip)
            btn.clicked.connect(func)
            btn.setStyleSheet(GenshinStyleSheet.BTN_ICON)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            hbox_tools.addWidget(btn)
        
        hbox_tools.addStretch()
        vbox.addLayout(hbox_tools)

        self.prop_frame = QFrame()
        self.prop_frame.setStyleSheet(f"background: rgba(255,255,255,0.4); border-radius: 8px; padding: 8px; border: 1px solid #CCC;")
        prop_layout = QVBoxLayout(self.prop_frame)
        
        row1 = QHBoxLayout()
        lbl_blend = QLabel("Blend Mode:")
        lbl_blend.setStyleSheet("font-weight: bold;")
        row1.addWidget(lbl_blend)
        self.blend_combo = QComboBox()
        self.blend_combo.addItems(['normal', 'overlay', 'screen', 'soft_light'])
        self.blend_combo.currentTextChanged.connect(self.on_blend_mode_change)
        row1.addWidget(self.blend_combo, 1)
        prop_layout.addLayout(row1)

        row2 = QHBoxLayout()
        lbl_op = QLabel("Opacity:")
        lbl_op.setStyleSheet("font-weight: bold;")
        row2.addWidget(lbl_op)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.valueChanged.connect(self.on_opacity_slider_change)
        
        self.opacity_val = QLabel("100%")
        self.opacity_val.setStyleSheet(f"color: {C_TEXT_PRIMARY}; font-weight: bold; font-size: 11px;") 
        self.opacity_val.setFixedWidth(60) 
        self.opacity_val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        row2.addWidget(self.opacity_slider)
        row2.addWidget(self.opacity_val)
        prop_layout.addLayout(row2)

        self.prop_frame.setEnabled(False)
        vbox.addWidget(self.prop_frame)
        layout.addWidget(group)

    def create_settings_section(self, layout):
        group = QGroupBox("General Settings")
        vbox = QVBoxLayout(group)
        
        self.chk_stretch = QCheckBox("Stretch watermark to fit image")
        self.chk_stretch.setChecked(self.stretch_var)
        self.chk_stretch.stateChanged.connect(self.on_stretch_change)
        
        vbox.addWidget(self.chk_stretch)
        layout.addWidget(group)

    def create_text_label_section(self, layout):
        group = QGroupBox("Text Label")
        vbox = QVBoxLayout(group)
        
        self.chk_label = QCheckBox("Enable Text Label")
        self.chk_label.setChecked(self.text_label_config.enabled)
        self.chk_label.stateChanged.connect(self.on_label_enabled_change)
        vbox.addWidget(self.chk_label)

        self.label_container = QWidget()
        l_layout = QVBoxLayout(self.label_container)
        l_layout.setContentsMargins(0, 5, 0, 0)
        l_layout.setSpacing(12)

        grid = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("Content:"))
        self.cb_type = QComboBox()
        self.cb_type.addItems(['number', 'filename'])
        self.cb_type.setCurrentText(self.text_label_config.label_type)
        self.cb_type.currentTextChanged.connect(self.on_label_type_change)
        col1.addWidget(self.cb_type)
        
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("Position:"))
        self.cb_pos = QComboBox()
        self.cb_pos.addItems(['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'])
        self.cb_pos.setCurrentText(self.text_label_config.position)
        self.cb_pos.currentTextChanged.connect(self.on_label_position_change)
        col2.addWidget(self.cb_pos)
        
        grid.addLayout(col1)
        grid.addLayout(col2)
        l_layout.addLayout(grid)

        row_font = QHBoxLayout()
        self.cb_font = QComboBox()
        sys_fonts = sorted(get_system_fonts().keys())
        self.cb_font.addItems(['(Auto)'] + sys_fonts)
        self.cb_font.setCurrentText(self.text_label_config.font_name or '(Auto)')
        self.cb_font.currentTextChanged.connect(self.on_label_font_change)
        self.cb_font.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_font.addWidget(QLabel("Font:"))
        row_font.addWidget(self.cb_font)
        l_layout.addLayout(row_font)

        row_size = QHBoxLayout()
        row_size.addWidget(QLabel("Size:"))
        self.sld_font_size = QSlider(Qt.Orientation.Horizontal)
        self.sld_font_size.setRange(5, 100)
        self.sld_font_size.setValue(int(self.text_label_config.font_size * 10))
        self.sld_font_size.valueChanged.connect(self.on_label_font_size_change)
        self.lbl_font_size = QLabel(f"{self.text_label_config.font_size:.1f}%")
        self.lbl_font_size.setFixedWidth(45)
        self.lbl_font_size.setStyleSheet("font-weight: bold;")
        
        row_size.addWidget(self.sld_font_size)
        row_size.addWidget(self.lbl_font_size)
        l_layout.addLayout(row_size)

        vbox.addWidget(self.label_container)
        self.label_container.setVisible(self.text_label_config.enabled)
        layout.addWidget(group)

    def create_output_section(self, layout):
        frame = QFrame()
        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(15)

        hbox_path = QHBoxLayout()
        self.btn_path = QPushButton(" Output Folder")
        self.btn_path.setIcon(qta.icon('fa5s.folder', color='#1F2329'))
        self.btn_path.setStyleSheet(GenshinStyleSheet.BTN_SECONDARY)
        self.btn_path.clicked.connect(self.select_save_directory)
        
        self.lbl_path = QLabel("Auto (Same as source)")
        self.lbl_path.setStyleSheet(f"color: {C_TEXT_PATH}; font-weight: bold; font-size: 13px;")
        self.lbl_path.setWordWrap(True)
        
        hbox_path.addWidget(self.btn_path)
        hbox_path.addWidget(self.lbl_path, 1)
        vbox.addLayout(hbox_path)

        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        self.pbar.setFixedHeight(12)
        vbox.addWidget(self.pbar)

        self.lbl_status = QLabel("Ready")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet(f"color: #6F7685; font-weight: bold;")
        vbox.addWidget(self.lbl_status)

        self.btn_apply = QPushButton("START PROCESSING")
        self.btn_apply.setStyleSheet(GenshinStyleSheet.BTN_PRIMARY)
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.setMinimumHeight(55)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(166, 141, 94, 120))
        shadow.setOffset(0, 5)
        self.btn_apply.setGraphicsEffect(shadow)
        self.btn_apply.clicked.connect(self.apply_watermark_threaded)
        
        vbox.addWidget(self.btn_apply)
        layout.addWidget(frame)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_icon(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_icon(True)

    def auto_load_last_files(self):
        if self.config.last_images_files:
            valid = [f for f in self.config.last_images_files if os.path.exists(f)]
            if valid:
                self.image_paths = valid
                self.img_count_label.setText(f"{len(valid)} images loaded")
                self.img_count_label.setStyleSheet(f"color: #E3D2B6; font-weight: bold;") 
                self.images = [Image.open(p) for p in valid] 
        self.update_layer_listbox()
        self.update_save_dir_label()

    def upload_images(self):
        init_dir = self.config.last_images_directory or os.path.expanduser("~")
        paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", init_dir, "Images (*.png *.jpg *.jpeg *.webp)")
        if paths:
            self.image_paths = paths
            self.images = [Image.open(p) for p in paths]
            self.config.last_images_directory = os.path.dirname(paths[0])
            self.config.last_images_files = list(paths)
            
            self.img_count_label.setText(f"{len(paths)} images selected")
            self.img_count_label.setStyleSheet(f"color: #E3D2B6; font-weight: bold;")
            
            if not self.config.save_directory:
                self.config.save_directory = self.config.last_images_directory
            self.update_save_dir_label()
            self.save_config()

    def add_watermark_layer(self):
        init_dir = self.config.last_watermark_directory or os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(self, "Select Watermark", init_dir, "Images (*.png *.jpg *.jpeg)")
        if path:
            layer = WatermarkLayer(path)
            self.watermark_layers.append(layer)
            self.config.last_watermark_directory = os.path.dirname(path)
            self.update_layer_listbox()
            self.save_config()

    def update_layer_listbox(self):
        self.layer_list.clear()
        for i, layer in enumerate(self.watermark_layers):
            item = QListWidgetItem(f"  Layer {i+1}: {layer.name}")
            
            # Use fa5s icons for compatibility
            icon_name = 'fa5s.check-circle' if layer.visible else 'fa5s.circle'
            icon_color = C_ACCENT_GOLD if layer.visible else '#999'
            
            item.setIcon(qta.icon(icon_name, color=icon_color))
            self.layer_list.addItem(item)

    def on_layer_select(self):
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

    def on_blend_mode_change(self, text):
        if self.current_layer_index is not None:
            self.watermark_layers[self.current_layer_index].blend_mode = text
            self.save_config()

    def on_opacity_slider_change(self, val):
        if self._updating_opacity or self.current_layer_index is None: return
        self.watermark_layers[self.current_layer_index].opacity = val
        self.opacity_val.setText(f"{val}%")
        self.save_config()

    def toggle_layer_visibility(self):
        row = self.layer_list.currentRow()
        if row != -1:
            self.watermark_layers[row].visible = not self.watermark_layers[row].visible
            self.update_layer_listbox()
            self.layer_list.setCurrentRow(row)
            self.save_config()

    def remove_selected_layer(self):
        row = self.layer_list.currentRow()
        if row != -1:
            del self.watermark_layers[row]
            self.update_layer_listbox()
            self.prop_frame.setEnabled(False)
            self.save_config()

    def move_layer(self, direction):
        row = self.layer_list.currentRow()
        if row == -1: return
        new_row = row + direction
        if 0 <= new_row < len(self.watermark_layers):
            self.watermark_layers[row], self.watermark_layers[new_row] = self.watermark_layers[new_row], self.watermark_layers[row]
            self.update_layer_listbox()
            self.layer_list.setCurrentRow(new_row)
            self.save_config()

    def on_stretch_change(self, state):
        self.stretch_var = (state == Qt.CheckState.Checked.value)
        self.save_config()

    def on_label_enabled_change(self, state):
        is_checked = (state == Qt.CheckState.Checked.value)
        self.text_label_config.enabled = is_checked
        self.label_container.setVisible(is_checked)
        self.save_config()

    def on_label_type_change(self, t): self.text_label_config.label_type = t; self.save_config()
    def on_label_position_change(self, p): self.text_label_config.position = p; self.save_config()
    def on_label_font_change(self, f): self.text_label_config.font_name = None if f=='(Auto)' else f; self.save_config()
    def on_label_font_size_change(self, val): 
        self.text_label_config.font_size = val/10.0
        self.lbl_font_size.setText(f"{val/10.0:.1f}%")
        self.save_config()

    def select_save_directory(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.config.save_directory or "")
        if d:
            self.config.save_directory = d
            self.config.last_used_directory = d
            self.update_save_dir_label()
            self.save_config()

    def update_save_dir_label(self):
        d = self.config.save_directory
        if d:
            self.lbl_path.setText(f"📂 {os.path.basename(d)} ({d})")
        else:
            self.lbl_path.setText("Auto (Save to source folder)")

    def save_config(self):
        self.config.save(self.watermark_layers, self.text_label_config, self.stretch_var)

    def apply_watermark_threaded(self):
        if not self.images:
            dlg = GenshinMessageBox(self, "Oops", "Please select images first!", "error")
            dlg.exec()
            return
        if not self.watermark_layers:
            dlg = GenshinMessageBox(self, "Oops", "Add at least one watermark layer!", "error")
            dlg.exec()
            return

        self.btn_apply.setEnabled(False)
        self.btn_apply.setText("Processing...")
        self.processing_thread = threading.Thread(target=self._run_process)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _run_process(self):
        save_dir = self.config.save_directory or self.config.last_images_directory
        success, msg = BatchProcessor.process_images(
            self.images, self.image_paths, self.watermark_layers,
            self.text_label_config, save_dir, self.stretch_var,
            lambda p: self.progress_update_signal.emit(p),
            lambda s: self.status_update_signal.emit(s)
        )
        if success:
            self.processing_complete_signal.emit("Done!", msg)
        else:
            self.processing_error_signal.emit(msg)

    def on_processing_complete(self, status, msg):
        self.lbl_status.setText(status)
        self.pbar.setValue(100)
        self.btn_apply.setEnabled(True)
        self.btn_apply.setText("START PROCESSING")
        dlg = GenshinMessageBox(self, "Mission Accomplished", msg, "success")
        dlg.exec()

    def on_processing_error(self, err):
        self.lbl_status.setText("Error")
        self.btn_apply.setEnabled(True)
        self.btn_apply.setText("START PROCESSING")
        dlg = GenshinMessageBox(self, "Processing Failed", err, "error")
        dlg.exec()
    
    def update_progress_bar(self, val): self.pbar.setValue(val)
    def update_status_label(self, txt): self.lbl_status.setText(txt)


def main():
    app = QApplication(sys.argv)
    window = MultiLayerWatermarkApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()