#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genshin Style Message Box Component
原神风格消息框组件
"""
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
import qtawesome as qta
from ..styles import Colors, FONT_FAMILY, GenshinStyleSheet


class GenshinMessageBox(QDialog):
    """Custom Genshin Style Dialog
    自定义原神风格对话框
    """

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
                background-color: {Colors.BG_LIGHT};
                border: 2px solid {Colors.ACCENT_GOLD};
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
        self._create_title_bar(layout, title)

        # 2. Content Area
        self._create_content_area(layout, message, icon_type)

        # 3. Button Area
        self._create_button_area(layout)

        self._start_pos = None

    def _create_title_bar(self, parent_layout, title):
        """创建标题栏"""
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_DARK};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                border-bottom: none;
            }}
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"""
            color: {Colors.TEXT_TITLE};
            font-weight: bold;
            font-size: 15px;
            background: transparent;
        """)

        btn_close = QPushButton()
        btn_close.setIcon(qta.icon('fa5s.times', color=Colors.ACCENT_GOLD))
        btn_close.setFixedSize(30, 30)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                border-radius: 15px;
            }
        """)

        title_layout.addWidget(lbl_title)
        title_layout.addStretch()
        title_layout.addWidget(btn_close)

        parent_layout.addWidget(title_bar)

    def _create_content_area(self, parent_layout, message, icon_type):
        """创建内容区域"""
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
        lbl_msg.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)

        content_layout.addWidget(lbl_msg)
        parent_layout.addWidget(content_area)

    def _create_button_area(self, parent_layout):
        """创建按钮区域"""
        btn_area = QWidget()
        btn_area.setStyleSheet("background-color: transparent;")
        btn_layout = QHBoxLayout(btn_area)
        btn_layout.setContentsMargins(0, 0, 0, 20)

        btn_ok = QPushButton("Confirm")
        btn_ok.setFixedSize(120, 36)
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setStyleSheet(GenshinStyleSheet.get_button_style('primary'))
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_ok)
        parent_layout.addWidget(btn_area)

    # 拖拽支持
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
