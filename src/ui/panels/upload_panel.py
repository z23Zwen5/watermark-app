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
from ..styles.theme_base import ThemeManager


class UploadPanel(QWidget):
    """图片上传面板"""

    # 信号
    images_selected = pyqtSignal(list, list)  # (image_paths, images)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.theme = ThemeManager.get_theme()
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
        self.upload_btn.setIcon(qta.icon('fa5s.images', color=self.theme.text_primary))
        self.upload_btn.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.upload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_btn.clicked.connect(self._upload_images)
        self.upload_btn.setMinimumHeight(45)

        # 图片计数标签
        self.img_count_label = QLabel("No images selected")
        self.img_count_label.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic;")
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
            self.img_count_label.setStyleSheet(f"color: {self.theme.text_highlight}; font-weight: bold;")

            # 发射信号
            self.images_selected.emit(self.image_paths, self.images)

    def load_last_files(self):
        """自动加载上次的文件（仅记录路径，不加载图片以加快启动）"""
        if self.config.last_images_files:
            valid = [f for f in self.config.last_images_files if os.path.exists(f)]
            if valid:
                self.image_paths = valid
                # 延迟加载：仅记录路径，不立即打开图片（加快启动速度）
                # self.images = [Image.open(p) for p in valid]  # 旧版本：启动时加载所有图片
                self.images = []  # 暂时为空，在处理时再加载

                # 显示提示信息
                self.img_count_label.setText(f"{len(valid)} images ready (click to reload)")
                self.img_count_label.setStyleSheet(f"color: {self.theme.text_secondary}; font-style: italic;")
                # 不发射信号，让用户手动重新选择图片

    def get_images(self):
        """获取已选择的图片"""
        return self.image_paths, self.images
