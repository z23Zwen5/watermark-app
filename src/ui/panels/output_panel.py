#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Output Panel - Processing and Output Control
输出面板
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QProgressBar, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta
from ..styles.theme_base import ThemeManager


class OutputPanel(QWidget):
    """输出面板"""

    # 信号
    process_requested = pyqtSignal()
    directory_changed = pyqtSignal(str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.theme = ThemeManager.get_theme()
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        frame = QFrame()
        layout = QVBoxLayout(self)
        layout.addWidget(frame)

        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(15)

        # 输出文件夹选择
        hbox_path = QHBoxLayout()
        self.btn_path = QPushButton(" Output Folder")
        self.btn_path.setIcon(qta.icon('fa5s.folder', color=self.theme.text_primary))
        self.btn_path.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_path.clicked.connect(self._select_directory)

        self.lbl_path = QLabel("Auto (Same as source)")
        self.lbl_path.setStyleSheet(
            f"color: {self.theme.text_path}; font-weight: bold; font-size: 13px;"
        )
        self.lbl_path.setWordWrap(True)

        hbox_path.addWidget(self.btn_path)
        hbox_path.addWidget(self.lbl_path, 1)
        vbox.addLayout(hbox_path)

        # 进度条
        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        self.pbar.setFixedHeight(12)
        vbox.addWidget(self.pbar)

        # 状态标签
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet(f"color: {self.theme.text_secondary}; font-weight: bold;")
        vbox.addWidget(self.lbl_status)

        # 处理按钮
        self.btn_apply = QPushButton("START PROCESSING")
        self.btn_apply.setStyleSheet(self.theme.get_button_stylesheet('primary'))
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.setMinimumHeight(55)
        self.btn_apply.clicked.connect(self._on_process_clicked)

        vbox.addWidget(self.btn_apply)

    def _select_directory(self):
        """选择输出目录"""
        d = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.config.save_directory or ""
        )
        if d:
            self.config.save_directory = d
            self.config.last_used_directory = d
            self.update_path_label()
            self.directory_changed.emit(d)

    def update_path_label(self):
        """更新路径标签"""
        d = self.config.save_directory
        if d:
            self.lbl_path.setText(f"📂 {os.path.basename(d)} ({d})")
        else:
            self.lbl_path.setText("Auto (Save to source folder)")

    def _on_process_clicked(self):
        """处理按钮点击"""
        self.process_requested.emit()

    def update_progress(self, value):
        """更新进度条"""
        self.pbar.setValue(int(value))

    def update_status(self, text):
        """更新状态文本"""
        self.lbl_status.setText(text)

    def set_processing_state(self, processing):
        """设置处理状态"""
        if processing:
            self.btn_apply.setEnabled(False)
            self.btn_apply.setText("PROCESSING...")
        else:
            self.btn_apply.setEnabled(True)
            self.btn_apply.setText("START PROCESSING")

    def reset_progress(self):
        """重置进度"""
        self.pbar.setValue(0)
        self.lbl_status.setText("Ready")
