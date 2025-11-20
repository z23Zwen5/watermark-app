#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window - Modular Architecture
主窗口 - 模块化架构

注意：这是一个框架版本，展示模块化架构
完整的面板拆分需要进一步实现
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
import threading

from watermark_core import WatermarkConfig
from .styles import GenshinStyleSheet
from .components import CustomTitleBar, GenshinMessageBox


class MainWindow(QMainWindow):
    """主窗口 - 协调所有UI组件

    TODO: 拆分成独立的面板：
    - UploadPanel: 图片上传
    - LayerPanel: 图层管理
    - SettingsPanel: 设置面板
    - TextLabelPanel: 文本标注
    - OutputPanel: 输出处理
    """

    # 处理信号
    progress_update_signal = pyqtSignal(int)
    status_update_signal = pyqtSignal(str)
    processing_complete_signal = pyqtSignal(str, str)
    processing_error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # 无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1100, 750)

        # 业务逻辑
        self.config = WatermarkConfig()
        self.config.load()

        # 数据
        self.images = []
        self.image_paths = []

        # 创建UI
        self._create_ui()

        # 连接信号
        self._connect_signals()

    def _create_ui(self):
        """创建UI"""
        # 应用样式
        self.setStyleSheet(GenshinStyleSheet.get_main_style())

        # 中心部件
        self.center_widget = QWidget()
        self.center_widget.setObjectName("CenterWidget")
        self.setCentralWidget(self.center_widget)

        main_layout = QVBoxLayout(self.center_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 标题栏
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)

        # TODO: 替换为独立的面板组件
        # 临时占位符
        placeholder = QLabel("🚧 UI 模块化架构已创建\n\n待完成:\n• 上传面板\n• 图层面板\n• 设置面板\n• 文本标注面板\n• 输出面板")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 16px; padding: 50px;")
        content_layout.addWidget(placeholder)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _connect_signals(self):
        """连接信号槽"""
        # 标题栏
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_restore_requested.connect(self._toggle_maximize)

        # TODO: 连接面板信号

    def _toggle_maximize(self):
        """切换最大化状态"""
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_icon(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_icon(True)

    def closeEvent(self, event):
        """关闭事件 - 保存配置"""
        # TODO: 保存配置
        event.accept()
