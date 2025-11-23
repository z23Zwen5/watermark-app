#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window - Modular Architecture
主窗口 - 模块化架构
"""
import time
import threading
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from watermark_core import WatermarkConfig, BatchProcessor
from .styles.theme_base import ThemeManager
from .components import CustomTitleBar, GenshinMessageBox
from .panels import (
    UploadPanel, LayerPanel, SettingsPanel,
    TextLabelPanel, OutputPanel
)


class MainWindow(QMainWindow):
    """主窗口 - 协调所有UI组件"""

    # 处理信号
    progress_update_signal = pyqtSignal(int)
    status_update_signal = pyqtSignal(str)
    processing_complete_signal = pyqtSignal(str, str)
    processing_error_signal = pyqtSignal(str)

    def __init__(self):
        t0 = time.time()
        super().__init__()
        print(f"  ⏱️  super().__init__: {(time.time() - t0)*1000:.0f}ms")

        # 无边框窗口
        t0 = time.time()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1100, 750)
        print(f"  ⏱️  窗口设置: {(time.time() - t0)*1000:.0f}ms")

        # 业务逻辑
        t0 = time.time()
        self.config = WatermarkConfig()
        self.config.load()
        print(f"  ⏱️  加载配置: {(time.time() - t0)*1000:.0f}ms")

        # 应用保存的主题设置
        t0 = time.time()
        if hasattr(self.config, 'ui_theme'):
            ThemeManager.set_theme(self.config.ui_theme)
            # 重新应用样式
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            theme = ThemeManager.get_theme()
            app.setStyleSheet(theme.get_main_stylesheet())
        print(f"  ⏱️  应用主题: {(time.time() - t0)*1000:.0f}ms")

        # 数据
        self.images = []
        self.image_paths = []

        # 处理线程
        self.processing_thread = None

        # 创建UI
        t0 = time.time()
        self._create_ui()
        print(f"  ⏱️  创建UI: {(time.time() - t0)*1000:.0f}ms")

        # 连接信号
        t0 = time.time()
        self._connect_signals()
        print(f"  ⏱️  连接信号: {(time.time() - t0)*1000:.0f}ms")

        # 加载初始数据
        t0 = time.time()
        self._load_initial_data()
        print(f"  ⏱️  加载初始数据: {(time.time() - t0)*1000:.0f}ms")

    def _create_ui(self):
        """创建UI"""
        # 获取当前主题
        theme = ThemeManager.get_theme()

        # 应用样式 (主样式已在 apply_global_style 中应用，这里不需要重复)
        # self.setStyleSheet(theme.get_main_stylesheet())

        # 中心部件
        t0 = time.time()
        self.center_widget = QWidget()
        self.center_widget.setObjectName("CenterWidget")
        self.setCentralWidget(self.center_widget)

        main_layout = QVBoxLayout(self.center_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        print(f"    ⏱️  中心部件: {(time.time() - t0)*1000:.0f}ms")

        # 标题栏
        t0 = time.time()
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        print(f"    ⏱️  标题栏: {(time.time() - t0)*1000:.0f}ms")

        # 创建滚动区域
        t0 = time.time()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(25)
        print(f"    ⏱️  滚动区域: {(time.time() - t0)*1000:.0f}ms")

        # 左列：上传 + 图层
        left_column = QVBoxLayout()
        left_column.setSpacing(20)

        t0 = time.time()
        self.upload_panel = UploadPanel(self.config)
        print(f"    ⏱️  上传面板: {(time.time() - t0)*1000:.0f}ms")

        t0 = time.time()
        self.layer_panel = LayerPanel(self.config)
        print(f"    ⏱️  图层面板: {(time.time() - t0)*1000:.0f}ms")

        left_column.addWidget(self.upload_panel)
        left_column.addWidget(self.layer_panel)

        # 右列：设置 + 文本标注 + 输出
        right_column = QVBoxLayout()
        right_column.setSpacing(20)

        t0 = time.time()
        self.settings_panel = SettingsPanel()
        print(f"    ⏱️  设置面板: {(time.time() - t0)*1000:.0f}ms")

        t0 = time.time()
        self.text_label_panel = TextLabelPanel(self.config.text_label_config)
        print(f"    ⏱️  文本标注面板: {(time.time() - t0)*1000:.0f}ms")

        t0 = time.time()
        self.output_panel = OutputPanel(self.config)
        print(f"    ⏱️  输出面板: {(time.time() - t0)*1000:.0f}ms")

        right_column.addWidget(self.settings_panel)
        right_column.addWidget(self.text_label_panel)
        right_column.addStretch()
        right_column.addWidget(self.output_panel)

        # 添加到内容布局
        content_layout.addLayout(left_column, 55)
        content_layout.addLayout(right_column, 45)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _connect_signals(self):
        """连接信号槽"""
        # 标题栏
        self.title_bar.close_requested.connect(self.close)
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_restore_requested.connect(self._toggle_maximize)

        # 上传面板
        self.upload_panel.images_selected.connect(self._on_images_selected)

        # 图层面板
        self.layer_panel.layers_changed.connect(self._save_config)

        # 设置面板
        self.settings_panel.stretch_changed.connect(self._on_stretch_changed)
        self.settings_panel.theme_changed.connect(self._on_theme_changed)

        # 文本标注面板
        self.text_label_panel.config_changed.connect(self._on_text_label_changed)

        # 输出面板
        self.output_panel.process_requested.connect(self._start_processing)
        self.output_panel.directory_changed.connect(self._save_config)

        # 处理信号
        self.progress_update_signal.connect(self.output_panel.update_progress)
        self.status_update_signal.connect(self.output_panel.update_status)
        self.processing_complete_signal.connect(self._on_processing_complete)
        self.processing_error_signal.connect(self._on_processing_error)

    def _load_initial_data(self):
        """加载初始数据"""
        # 设置图层
        t0 = time.time()
        self.layer_panel.set_layers(self.config.layers)
        print(f"    ⏱️  加载图层 ({len(self.config.layers)}个): {(time.time() - t0)*1000:.0f}ms")

        # 设置其他配置
        self.settings_panel.set_stretch(self.config.last_stretch)

        # 设置主题选择器
        if hasattr(self.config, 'ui_theme'):
            self.settings_panel.set_theme(self.config.ui_theme)

        # 更新输出目录显示
        self.output_panel.update_path_label()

        # 自动加载上次的文件
        t0 = time.time()
        self.upload_panel.load_last_files()
        print(f"    ⏱️  加载上次文件: {(time.time() - t0)*1000:.0f}ms")

    def _toggle_maximize(self):
        """切换最大化状态"""
        if self.isMaximized():
            self.showNormal()
            self.title_bar.update_maximize_icon(False)
        else:
            self.showMaximized()
            self.title_bar.update_maximize_icon(True)

    # === 槽函数 ===

    def _on_images_selected(self, paths, images):
        """图片选择事件"""
        self.image_paths = paths
        self.images = images
        self._save_config()

    def _on_stretch_changed(self, value):
        """拉伸设置改变"""
        self.config.last_stretch = value
        self._save_config()

    def _on_theme_changed(self, theme_name):
        """主题改变"""
        # 切换主题
        ThemeManager.set_theme(theme_name)

        # 获取应用实例
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()

        # 获取新主题
        new_theme = ThemeManager.get_theme()

        # 应用新样式
        app.setStyleSheet(new_theme.get_main_stylesheet())

        # 保存主题设置到配置
        self.config.ui_theme = theme_name
        self._save_config()

        # 显示提示消息
        dlg = GenshinMessageBox(
            self,
            "Theme Switched",
            f"Successfully switched to {new_theme.display_name} theme!",
            "success"
        )
        dlg.exec()

    def _on_text_label_changed(self, config_dict):
        """文本标注配置改变"""
        self.config.text_label_config.from_dict(config_dict)
        self._save_config()

    def _save_config(self):
        """保存配置"""
        self.config.save(
            self.layer_panel.get_layers(),
            self.config.text_label_config,
            self.settings_panel.get_stretch()
        )

    def _start_processing(self):
        """开始处理"""
        if not self.images:
            dlg = GenshinMessageBox(
                self,
                "Oops",
                "Please select images first!",
                "error"
            )
            dlg.exec()
            return

        layers = self.layer_panel.get_layers()
        if not layers:
            dlg = GenshinMessageBox(
                self,
                "Oops",
                "Add at least one watermark layer!",
                "error"
            )
            dlg.exec()
            return

        # 检查是否有可见图层
        visible_layers = [l for l in layers if l.visible]
        if not visible_layers:
            dlg = GenshinMessageBox(
                self,
                "Oops",
                "At least one layer must be visible!",
                "error"
            )
            dlg.exec()
            return

        # 设置处理状态
        self.output_panel.set_processing_state(True)
        self.output_panel.reset_progress()

        # 在线程中处理
        self.processing_thread = threading.Thread(target=self._run_process)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def _run_process(self):
        """运行处理（在线程中）"""
        save_dir = self.config.save_directory or self.config.last_images_directory

        success, msg = BatchProcessor.process_images(
            self.images,
            self.image_paths,
            self.layer_panel.get_layers(),
            self.config.text_label_config,
            save_dir,
            self.settings_panel.get_stretch(),
            lambda p: self.progress_update_signal.emit(p),
            lambda s: self.status_update_signal.emit(s)
        )

        if success:
            self.processing_complete_signal.emit("Done!", msg)
        else:
            self.processing_error_signal.emit(msg)

    def _on_processing_complete(self, status, msg):
        """处理完成"""
        self.output_panel.set_processing_state(False)
        dlg = GenshinMessageBox(self, "Mission Accomplished", msg, "success")
        dlg.exec()

    def _on_processing_error(self, err):
        """处理错误"""
        self.output_panel.set_processing_state(False)
        dlg = GenshinMessageBox(self, "Processing Failed", err, "error")
        dlg.exec()

    def closeEvent(self, event):
        """关闭事件 - 保存配置"""
        self._save_config()
        event.accept()
