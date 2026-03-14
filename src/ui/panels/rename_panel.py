#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename Panel - AI 命名面板（完整功能）
使用 Gemini API 分析原图，生成规范命名、文案、规格清单，并批量重命名文件。
"""
import os
import threading
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QCheckBox, QComboBox, QGroupBox, QListWidget,
    QProgressBar, QFileDialog, QTabWidget, QTextEdit, QDialog,
    QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import qtawesome as qta

from ..styles.theme_base import ThemeManager
from ..components.message_box import GenshinMessageBox
from rename_module import (
    TONE_OPTIONS, TONE_KEY, IMAGE_EXTS,
    sort_paths, is_named_file,
    generate_and_build, save_rename_outputs,
    build_pan_message, build_spec_from_named_files,
)


class PanDeliveryDialog(QDialog):
    """网盘发货信息生成对话框"""

    def __init__(self, file_names: list, image_paths: list, save_folder: str, parent=None):
        super().__init__(parent)
        self.file_names = file_names          # 已生成命名的文件名列表
        self.image_paths = image_paths        # 原始图片路径（用于 is_named_file 模式）
        self.save_folder = save_folder        # 规格清单.txt 所在目录

        self.setWindowTitle("网盘发货信息")
        self.resize(680, 560)
        self.setMinimumSize(500, 400)

        theme = ThemeManager.get_theme()
        self.setStyleSheet(theme.get_main_stylesheet())
        self._create_ui(theme)

    def _create_ui(self, theme):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # 说明
        info_lbl = QLabel("粘贴百度网盘分享文本（每条分享之间换行分隔）：")
        info_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
        layout.addWidget(info_lbl)

        # 输入区
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("粘贴网盘分享内容…")
        self.input_text.setFixedHeight(150)
        layout.addWidget(self.input_text)

        # 按钮行
        btn_row = QHBoxLayout()
        self.gen_btn = QPushButton("生成发货信息")
        self.gen_btn.setStyleSheet(theme.get_button_stylesheet('primary'))
        self.gen_btn.clicked.connect(self._on_generate)
        btn_row.addWidget(self.gen_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # 预览标签
        preview_lbl = QLabel("发货信息预览：")
        preview_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
        layout.addWidget(preview_lbl)

        # 预览区
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("生成后显示…")
        layout.addWidget(self.result_text)

        # 状态 + 操作行
        bottom_row = QHBoxLayout()
        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 11px;")
        bottom_row.addWidget(self.status_lbl, 1)

        self.copy_btn = QPushButton("📋 复制")
        self.copy_btn.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.copy_btn.clicked.connect(self._on_copy)
        bottom_row.addWidget(self.copy_btn)

        self.append_btn = QPushButton("追加到 规格清单.txt")
        self.append_btn.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.append_btn.clicked.connect(self._on_append)
        bottom_row.addWidget(self.append_btn)

        layout.addLayout(bottom_row)

    def _get_effective_file_names(self):
        """获取有效文件名列表（优先使用已生成命名，其次识别已命名图片）。"""
        if self.file_names:
            return self.file_names, []

        # 未生成命名 → 尝试识别已命名图片
        named = [p for p in self.image_paths if is_named_file(p)]
        skipped = len(self.image_paths) - len(named)
        names = [os.path.basename(p) for p in named]
        return names, [skipped] if skipped > 0 else []

    def _on_generate(self):
        pan_raw = self.input_text.toPlainText().strip()
        if not pan_raw:
            self.status_lbl.setText("⚠ 请先粘贴网盘分享文本")
            return

        file_names, warnings = self._get_effective_file_names()
        if not file_names:
            self.status_lbl.setText("⚠ 无可用文件名（请先生成命名或选择已命名图片）")
            return

        msg, unmatched = build_pan_message(file_names, pan_raw)
        self.result_text.setPlainText(msg)

        if warnings:
            skipped = warnings[0]
            prefix = f"⚠ 已跳过 {skipped} 张未命名图片。"
        else:
            prefix = ""

        if unmatched:
            names_str = ", ".join(unmatched[:5])
            if len(unmatched) > 5:
                names_str += f" …等{len(unmatched)}个"
            matched_n = len(file_names) - len(unmatched)
            self.status_lbl.setText(
                f"{prefix}⚠ {matched_n}/{len(file_names)} 已匹配，未匹配: {names_str}"
            )
            self.status_lbl.setStyleSheet("color: orange; font-size: 11px;")
        else:
            self.status_lbl.setText(f"{prefix}✅ 全部 {len(file_names)} 个文件已匹配")
            self.status_lbl.setStyleSheet("color: #4CAF50; font-size: 11px;")

    def _on_copy(self):
        content = self.result_text.toPlainText().strip()
        if not content:
            return
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(content)
        self.status_lbl.setText("已复制到剪贴板 ✓")

    def _on_append(self):
        content = self.result_text.toPlainText().strip()
        if not content:
            self.status_lbl.setText("⚠ 请先生成发货信息")
            return
        if not self.save_folder:
            self.status_lbl.setText("⚠ 未知保存目录")
            return
        target = os.path.join(self.save_folder, "规格清单.txt")
        if not os.path.exists(target):
            self.status_lbl.setText("⚠ 未找到 规格清单.txt，请先保存文件")
            return
        try:
            with open(target, "a", encoding="utf-8") as f:
                f.write("\n\n=== 发货信息 ===\n")
                f.write(content)
            self.status_lbl.setText("已追加到 规格清单.txt ✓")
        except Exception as e:
            self.status_lbl.setText(f"写入失败: {e}")


class RenamePanel(QWidget):
    """AI 命名面板 - 全功能"""

    # 对外信号
    config_changed = pyqtSignal()   # API Key 保存时通知 MainWindow 持久化配置

    # 内部线程信号
    _generation_complete = pyqtSignal(dict)
    _generation_error = pyqtSignal(str)

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config                 # WatermarkConfig 实例
        self.image_paths: list = []          # 当前选中的原图路径
        self._last_outputs: dict = {}        # 最近一次生成的 outputs dict
        self._last_save_folder: str = ""     # 最近一次保存的目录

        self.theme = ThemeManager.get_theme()
        self._create_ui()
        self._connect_signals()

    # ----------------------------------------------------------------
    # UI 构建
    # ----------------------------------------------------------------

    def _create_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self._vbox = QVBoxLayout(content)
        self._vbox.setContentsMargins(25, 20, 25, 25)
        self._vbox.setSpacing(15)

        self._vbox.addWidget(self._make_source_group(), 1)    # 文件列表拉伸
        self._vbox.addWidget(self._make_config_group(), 0)   # 配置区固定
        self._vbox.addWidget(self._make_action_strip(), 0)   # 操作区固定
        self._results_group = self._make_results_group()
        self._results_group.setVisible(False)
        self._vbox.addWidget(self._results_group, 1)          # 结果区拉伸

        scroll.setWidget(content)
        outer.addWidget(scroll)

    def _make_source_group(self) -> QGroupBox:
        grp = QGroupBox("📁 Source Images")
        lay = QVBoxLayout(grp)
        lay.setSpacing(8)

        btn_row = QHBoxLayout()
        self.btn_select = QPushButton(" Select Images")
        self.btn_select.setIcon(qta.icon('fa5s.images', color=self.theme.text_primary))
        self.btn_select.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_select.clicked.connect(self._on_select_images)
        btn_row.addWidget(self.btn_select)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        self.lbl_count = QLabel("No images selected")
        self.lbl_count.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px;")
        lay.addWidget(self.lbl_count)

        self.list_files = QListWidget()
        self.list_files.setMinimumHeight(60)
        self.list_files.setStyleSheet(
            f"QListWidget {{ border: 1px solid {self.theme.accent_primary_dark}; "
            f"border-radius: 6px; background: {self.theme.bg_input}; "
            f"color: {self.theme.text_primary}; font-size: 12px; }}"
        )
        lay.addWidget(self.list_files)
        return grp

    def _make_config_group(self) -> QGroupBox:
        grp = QGroupBox("⚙️ Naming Config")
        grid_lay = QVBoxLayout(grp)
        grid_lay.setSpacing(8)

        # 行1：日期 + 系列名 + AI取系列名
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Date (MMDD):"))
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText(datetime.now().strftime("%m%d"))
        self.date_edit.setText(datetime.now().strftime("%m%d"))
        self.date_edit.setFixedWidth(70)
        row1.addWidget(self.date_edit)

        row1.addSpacing(12)
        row1.addWidget(QLabel("Series:"))
        self.series_edit = QLineEdit()
        self.series_edit.setPlaceholderText("系列名")
        row1.addWidget(self.series_edit, 1)

        self.auto_series_chk = QCheckBox("AI取系列名")
        self.auto_series_chk.stateChanged.connect(self._on_auto_series_changed)
        row1.addWidget(self.auto_series_chk)
        grid_lay.addLayout(row1)

        # 行2：副题语言 + 模型 + API Key 折叠按钮
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Tone:"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(TONE_OPTIONS)
        self.tone_combo.setMinimumWidth(200)
        row2.addWidget(self.tone_combo)

        row2.addSpacing(12)
        row2.addWidget(QLabel("Model:"))
        self.model_edit = QLineEdit("gemini-2.5-flash")
        self.model_edit.setFixedWidth(160)
        row2.addWidget(self.model_edit)

        row2.addStretch()

        # API Key 折叠指示按钮（右侧，状态指示）
        self.btn_apikey_toggle = QPushButton()
        self.btn_apikey_toggle.setFixedHeight(28)
        self.btn_apikey_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apikey_toggle.clicked.connect(self._on_toggle_api_key_section)
        row2.addWidget(self.btn_apikey_toggle)
        grid_lay.addLayout(row2)

        # 行3：API Key 展开区（初始折叠）
        self._api_key_widget = QWidget()
        key_lay = QHBoxLayout(self._api_key_widget)
        key_lay.setContentsMargins(0, 4, 0, 0)
        key_lay.setSpacing(6)

        key_lbl = QLabel("API Key:")
        key_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px;")
        key_lay.addWidget(key_lbl)

        self.key_edit = QLineEdit()
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.key_edit.setPlaceholderText("AIza…")
        self.key_edit.setText(self.config.gemini_api_key)
        key_lay.addWidget(self.key_edit, 1)

        self.btn_toggle_key = QPushButton("Show")
        self.btn_toggle_key.setFixedHeight(28)
        self.btn_toggle_key.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_toggle_key.clicked.connect(self._on_toggle_key_visibility)
        key_lay.addWidget(self.btn_toggle_key)

        self.btn_save_key = QPushButton("Save")
        self.btn_save_key.setFixedHeight(28)
        self.btn_save_key.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_save_key.clicked.connect(self._on_save_key)
        key_lay.addWidget(self.btn_save_key)

        # 初始：已有 Key 则折叠，没有 Key 则展开
        self._api_key_expanded = not bool(self.config.gemini_api_key)
        self._api_key_widget.setVisible(self._api_key_expanded)
        self._update_apikey_btn_label()
        grid_lay.addWidget(self._api_key_widget)

        return grp

    def _make_action_strip(self) -> QWidget:
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self.btn_generate = QPushButton("🚀  Generate Names")
        self.btn_generate.setStyleSheet(self.theme.get_button_stylesheet('primary'))
        self.btn_generate.setMinimumHeight(50)
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate.clicked.connect(self._on_generate)
        lay.addWidget(self.btn_generate)

        self.lbl_status = QLabel("Ready")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px;")
        lay.addWidget(self.lbl_status)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setVisible(False)
        lay.addWidget(self.progress_bar)

        # 工具按钮行（支持已命名图片直接使用，无需先生成）
        tool_row = QHBoxLayout()
        tool_row.addStretch()

        self.btn_spec = QPushButton("📋 Generate Specs")
        self.btn_spec.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_spec.clicked.connect(self._on_generate_spec)
        tool_row.addWidget(self.btn_spec)

        self.btn_pan = QPushButton("📎 Pan Delivery")
        self.btn_pan.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_pan.clicked.connect(self._on_pan_delivery)
        tool_row.addWidget(self.btn_pan)
        lay.addLayout(tool_row)

        return container

    def _make_results_group(self) -> QGroupBox:
        grp = QGroupBox("✅ Results")
        lay = QVBoxLayout(grp)
        lay.setSpacing(10)

        # 4-tab 结果区
        self.result_tabs = QTabWidget()
        self._tab_filenames = self._make_result_tab()
        self._tab_display = self._make_result_tab()
        self._tab_explanations = self._make_result_tab()
        self._tab_post = self._make_result_tab()
        self.result_tabs.addTab(self._tab_filenames[0], "File Names")
        self.result_tabs.addTab(self._tab_display[0], "Display Names")
        self.result_tabs.addTab(self._tab_explanations[0], "Explanations")
        self.result_tabs.addTab(self._tab_post[0], "Post Copy")
        self.result_tabs.setMinimumHeight(200)
        lay.addWidget(self.result_tabs)

        # 操作按钮行
        btn_row = QHBoxLayout()

        self.btn_save_txt = QPushButton("💾 Save TXT Files")
        self.btn_save_txt.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_save_txt.clicked.connect(self._on_save_txt)
        btn_row.addWidget(self.btn_save_txt)

        self.btn_rename = QPushButton("✏️ Rename Files")
        self.btn_rename.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_rename.clicked.connect(self._on_rename_files)
        btn_row.addWidget(self.btn_rename)

        lay.addLayout(btn_row)
        return grp

    def _make_result_tab(self):
        """创建一个结果 Tab（文本区 + Copy 按钮）。返回 (widget, text_edit)。"""
        widget = QWidget()
        lay = QVBoxLayout(widget)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(4)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Consolas", 10))
        lay.addWidget(text_edit)

        copy_btn = QPushButton("📋 Copy")
        copy_btn.setFixedHeight(28)
        copy_btn.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        copy_btn.clicked.connect(lambda: self._copy_text(text_edit))
        lay.addWidget(copy_btn)

        return widget, text_edit

    # ----------------------------------------------------------------
    # 信号连接
    # ----------------------------------------------------------------

    def _connect_signals(self):
        self._generation_complete.connect(self._on_generation_complete)
        self._generation_error.connect(self._on_generation_error)

    # ----------------------------------------------------------------
    # 事件处理
    # ----------------------------------------------------------------

    def _on_select_images(self):
        ext_filter = "Images (" + " ".join(f"*{e}" for e in IMAGE_EXTS) + ")"
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", ext_filter)
        if not files:
            return
        self.image_paths = sort_paths(files)
        n = len(self.image_paths)
        self.lbl_count.setText(f"{n} image{'s' if n != 1 else ''} selected")
        self.list_files.clear()
        for p in self.image_paths:
            self.list_files.addItem(os.path.basename(p))

    def _on_toggle_api_key_section(self):
        self._api_key_expanded = not self._api_key_expanded
        self._api_key_widget.setVisible(self._api_key_expanded)
        self._update_apikey_btn_label()

    def _update_apikey_btn_label(self):
        """根据 Key 状态和展开状态更新按钮文字和颜色"""
        has_key = bool(self.config.gemini_api_key)
        arrow = "▲" if self._api_key_expanded else "▼"
        if has_key:
            self.btn_apikey_toggle.setText(f"🔑 Key set {arrow}")
            self.btn_apikey_toggle.setStyleSheet(
                self.theme.get_button_stylesheet('secondary') +
                "QPushButton { color: #4CAF50; border-color: #4CAF50; }"
            )
        else:
            self.btn_apikey_toggle.setText(f"🔑 Set API Key {arrow}")
            self.btn_apikey_toggle.setStyleSheet(
                self.theme.get_button_stylesheet('secondary') +
                "QPushButton { color: #FF9800; border-color: #FF9800; }"
            )

    def _on_auto_series_changed(self, state):
        if state:
            self.series_edit.setPlaceholderText("（可选：给 AI 一个参考方向）")
        else:
            self.series_edit.setPlaceholderText("系列名")

    def _on_toggle_key_visibility(self):
        if self.key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle_key.setText("Hide")
        else:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle_key.setText("Show")

    def _on_save_key(self):
        self.config.gemini_api_key = self.key_edit.text().strip()
        self.config_changed.emit()
        self.lbl_status.setText("API Key saved ✓")
        self._update_apikey_btn_label()
        # 保存后自动折叠
        if self.config.gemini_api_key and self._api_key_expanded:
            self._api_key_expanded = False
            self._api_key_widget.setVisible(False)
            self._update_apikey_btn_label()

    def _on_generate(self):
        if not self.image_paths:
            dlg = GenshinMessageBox(self, "Oops", "Please select images first!", "error")
            dlg.exec()
            return
        api_key = self.key_edit.text().strip()
        if not api_key:
            dlg = GenshinMessageBox(self, "Oops", "Please enter your Gemini API Key!", "error")
            dlg.exec()
            return
        date = self.date_edit.text().strip()
        if not date:
            dlg = GenshinMessageBox(self, "Oops", "Please enter the date (MMDD)!", "error")
            dlg.exec()
            return
        series = self.series_edit.text().strip()
        auto_series = self.auto_series_chk.isChecked()
        if not auto_series and not series:
            dlg = GenshinMessageBox(self, "Oops", "Please enter a series name or enable AI naming!", "error")
            dlg.exec()
            return

        self.btn_generate.setEnabled(False)
        self.lbl_status.setText("⏳ Calling Gemini API…")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)   # indeterminate

        tone = TONE_KEY.get(self.tone_combo.currentText(), "中文")
        model = self.model_edit.text().strip() or "gemini-2.5-flash"
        image_paths_copy = self.image_paths.copy()

        def _worker():
            try:
                result = generate_and_build(
                    api_key=api_key,
                    image_paths=image_paths_copy,
                    date=date,
                    series=series,
                    tone=tone,
                    auto_series=auto_series,
                    model=model,
                )
                self._generation_complete.emit(result)
            except Exception as e:
                err_msg = str(e)
                self._generation_error.emit(err_msg)

        threading.Thread(target=_worker, daemon=True).start()

    def _on_generation_complete(self, result: dict):
        self.btn_generate.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)

        # 如果 AI 返回了系列名，更新输入框
        if result.get("series_name") and self.auto_series_chk.isChecked():
            self.series_edit.setText(result["series_name"])

        outputs = result["outputs"]
        self._last_outputs = outputs

        # 填充 4 个 tab
        self._tab_filenames[1].setPlainText("\n".join(outputs["file_names"]))
        self._tab_display[1].setPlainText("\n".join(outputs["display_names"]))
        self._tab_explanations[1].setPlainText("\n".join(outputs["explanations"]))
        self._tab_post[1].setPlainText(outputs["post"])

        self._results_group.setVisible(True)
        self.lbl_status.setText(f"✅ Done! Generated {len(outputs['file_names'])} names.")

    def _on_generation_error(self, err: str):
        self.btn_generate.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.lbl_status.setText("❌ Generation failed")
        dlg = GenshinMessageBox(self, "API Error", f"Call failed:\n\n{err[:600]}", "error")
        dlg.exec()

    def _on_save_txt(self):
        if not self._last_outputs:
            dlg = GenshinMessageBox(self, "Oops", "Please generate names first!", "error")
            dlg.exec()
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if not folder:
            return
        try:
            result = save_rename_outputs(
                folder=folder,
                image_paths=self.image_paths,
                outputs=self._last_outputs,
                rename_images=False,
                save_explanation=True,
            )
            self._last_save_folder = folder
            saved = ", ".join(result["txt_files"])
            dlg = GenshinMessageBox(self, "Saved", f"Files saved to {folder}:\n\n{saved}", "success")
            dlg.exec()
        except Exception as e:
            dlg = GenshinMessageBox(self, "Error", f"Save failed:\n{e}", "error")
            dlg.exec()

    def _on_rename_files(self):
        if not self._last_outputs:
            dlg = GenshinMessageBox(self, "Oops", "Please generate names first!", "error")
            dlg.exec()
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder")
        if not folder:
            return

        # 构建确认提示
        lines = ["Will rename the following files:\n"]
        for i, p in enumerate(self.image_paths):
            if i < len(self._last_outputs["file_names"]):
                lines.append(f"{os.path.basename(p)}  →  {self._last_outputs['file_names'][i]}")
        confirm_msg = "\n".join(lines)
        dlg_confirm = GenshinMessageBox(self, "Confirm Rename", confirm_msg, "success")
        if not dlg_confirm.exec():
            return

        try:
            result = save_rename_outputs(
                folder=folder,
                image_paths=self.image_paths,
                outputs=self._last_outputs,
                rename_images=True,
                save_explanation=False,
            )
            self._last_save_folder = folder
            # 更新 image_paths 为重命名后的路径
            self.image_paths = [
                os.path.join(folder, new) for _, new in result["renamed"]
            ]
            self.list_files.clear()
            for p in self.image_paths:
                self.list_files.addItem(os.path.basename(p))

            count = len(result["renamed"])
            dlg = GenshinMessageBox(self, "Done", f"Renamed {count} file(s) to {folder}", "success")
            dlg.exec()
        except Exception as e:
            dlg = GenshinMessageBox(self, "Error", f"Rename failed:\n{e}", "error")
            dlg.exec()

    def _on_generate_spec(self):
        """从已命名图片的文件名解析并生成规格清单.txt"""
        if not self.image_paths:
            dlg = GenshinMessageBox(self, "Oops", "Please select images first!", "error")
            dlg.exec()
            return

        result = build_spec_from_named_files(self.image_paths)
        if not result:
            dlg = GenshinMessageBox(
                self, "Oops",
                "No files match the naming format (MMDD-Series・Subtitle).\n"
                "Please select already-named images.",
                "error"
            )
            dlg.exec()
            return

        # 选择保存目录
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if not folder:
            return

        try:
            spec_path = os.path.join(folder, "规格清单.txt")
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("\n".join(result["display_names"]))
            self._last_save_folder = folder

            named_count = len(result["display_names"])
            total_count = len(self.image_paths)
            if named_count < total_count:
                skipped = total_count - named_count
                msg = f"Saved 规格清单.txt ({named_count} entries, skipped {skipped} unnamed files)\n\n{folder}"
            else:
                msg = f"Saved 规格清单.txt ({named_count} entries)\n\n{folder}"
            dlg = GenshinMessageBox(self, "Saved", msg, "success")
            dlg.exec()
            self.lbl_status.setText(f"✅ Specs saved ({named_count} entries)")
        except Exception as e:
            dlg = GenshinMessageBox(self, "Error", f"Save failed:\n{e}", "error")
            dlg.exec()

    def _on_pan_delivery(self):
        # Pan Delivery 支持两种模式：已生成命名 or 已命名图片
        file_names = self._last_outputs.get("file_names", []) if self._last_outputs else []

        if not file_names and not self.image_paths:
            dlg = GenshinMessageBox(
                self, "Oops",
                "Please generate names first, or select images that are already named in MMDD-系列名・副题 format.",
                "error"
            )
            dlg.exec()
            return

        # 检查 image_paths 中有没有已命名的（如果 file_names 为空）
        if not file_names:
            named = [p for p in self.image_paths if is_named_file(p)]
            if not named:
                dlg = GenshinMessageBox(
                    self, "Oops",
                    "No valid file names available. Please generate names first.",
                    "error"
                )
                dlg.exec()
                return

        dlg = PanDeliveryDialog(
            file_names=file_names,
            image_paths=self.image_paths,
            save_folder=self._last_save_folder,
            parent=self,
        )
        dlg.exec()

    # ----------------------------------------------------------------
    # 工具方法
    # ----------------------------------------------------------------

    @staticmethod
    def _copy_text(text_edit: QTextEdit):
        content = text_edit.toPlainText().strip()
        if content:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(content)
