#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Title Bar Component
自定义标题栏组件
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
import qtawesome as qta
from ..styles.theme_base import ThemeManager


class CustomTitleBar(QWidget):
    """Custom Title Bar (Main Window)
    自定义标题栏（主窗口）
    """
    close_requested = pyqtSignal()
    minimize_requested = pyqtSignal()
    maximize_restore_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.theme = ThemeManager.get_theme()
        self.setFixedHeight(48)
        self.setObjectName("CustomTitleBar")

        # 开启背景绘制
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # 设置样式
        self.setStyleSheet(f"""
            QWidget#CustomTitleBar {{
                background-color: {self.theme.bg_light};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid {self.theme.accent_primary};
            }}
            QLabel {{
                color: {self.theme.text_header};
                font-family: {self.theme.font_family};
                font-weight: 900;
                font-size: 16px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)

        # 标题
        self.title_label = QLabel("Multi-Layer Watermark Tool")

        # 雕刻特效 - 添加白色投影 (Letterpress Effect)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setColor(QColor(255, 255, 255, 180))
        shadow.setOffset(1, 1)
        self.title_label.setGraphicsEffect(shadow)

        layout.addWidget(self.title_label)
        layout.addStretch(1)

        # 窗口控制按钮
        self.minimize_btn = self._create_btn("fa5s.window-minimize", icon_color=self.theme.text_header)
        self.maximize_btn = self._create_btn("fa5s.window-maximize", icon_color=self.theme.text_header)
        self.close_btn = self._create_btn("fa5s.times", hover_color=self.theme.close_btn_hover, icon_color=self.theme.text_header)

        self.minimize_btn.clicked.connect(self.minimize_requested.emit)
        self.maximize_btn.clicked.connect(self.maximize_restore_requested.emit)
        self.close_btn.clicked.connect(self.close_requested.emit)

        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)

        self.start_pos = None

    def _create_btn(self, icon_name, hover_color=None, icon_color=None):
        """创建控制按钮"""
        if icon_color is None:
            icon_color = self.theme.accent_primary

        btn = QPushButton()
        btn.setIcon(qta.icon(icon_name, color=icon_color))
        btn.setFixedSize(36, 36)

        bg_hover = f"background-color: {hover_color};" if hover_color else f"background-color: {self.theme.hover_bg};"

        btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: none; border-radius: 18px; }}
            QPushButton:hover {{ {bg_hover} }}
        """)
        return btn

    def update_maximize_icon(self, is_maximized):
        """更新最大化图标"""
        icon = 'fa5s.window-restore' if is_maximized else 'fa5s.window-maximize'
        self.maximize_btn.setIcon(qta.icon(icon, color=self.theme.text_header))

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
