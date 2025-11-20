#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload Panel - Image Selection
图片上传面板
"""
import os
from PIL import Image
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta
from ..styles import GenshinStyleSheet


class UploadPanel(QWidget):
    """图片上传面板"""

    # 信号
    images_selected = pyqtSignal(list, list)  # (image_paths, images)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.image_paths = []
        self.images = []
        self._create_ui()

    def _create_ui(self):
        """创建UI"""
        group = QGroupBox("Source Images")
        layout = QVBoxLayout(self)
        layout.addWidget(group)

        vbox = QVBoxLayout(group)

        # 上传按钮
        self.upload_btn = QPushButton("  Select Images / Folder")
        self.upload_btn.setIcon(qta.icon('fa5s.images', color='#1F2329'))
        self.upload_btn.setStyleSheet(GenshinStyleSheet.get_button_style('secondary'))
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self._upload_images)
        self.upload_btn.setMinimumHeight(45)

        # 图片计数标签
        self.img_count_label = QLabel("No images selected")
        self.img_count_label.setStyleSheet("color: #6F7685; font-style: italic;")
        self.img_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox.addWidget(self.upload_btn)
        vbox.addWidget(self.img_count_label)

    def _upload_images(self):
        """选择图片"""
        init_dir = self.config.last_images_directory or os.path.expanduser("~")
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            init_dir,
            "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if paths:
            self.image_paths = paths
            self.images = [Image.open(p) for p in paths]
            self.config.last_images_directory = os.path.dirname(paths[0])
            self.config.last_images_files = list(paths)

            self.img_count_label.setText(f"{len(paths)} images selected")
            self.img_count_label.setStyleSheet("color: #E3D2B6; font-weight: bold;")

            # 发射信号
            self.images_selected.emit(self.image_paths, self.images)

    def load_last_files(self):
        """自动加载上次的文件"""
        if self.config.last_images_files:
            valid = [f for f in self.config.last_images_files if os.path.exists(f)]
            if valid:
                self.image_paths = valid
                self.images = [Image.open(p) for p in valid]
                self.img_count_label.setText(f"{len(valid)} images loaded")
                self.img_count_label.setStyleSheet("color: #E3D2B6; font-weight: bold;")
                # 发射信号
                self.images_selected.emit(self.image_paths, self.images)

    def get_images(self):
        """获取已选择的图片"""
        return self.image_paths, self.images
