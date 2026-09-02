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
    ATMOSPHERE_MODE_OPTIONS, ATMOSPHERE_MODE_KEY, can_build_offline,
    TONE_OPTIONS, TONE_KEY, IMAGE_EXTS,
    PROVIDERS, PROVIDER_ORDER,
    PAN_GREETING, DEFAULT_PROMPT_TEMPLATE,
    DEFAULT_POST_TEMPLATE, DEFAULT_POST_TAGS, parse_tag_list,
    sort_paths, is_named_file,
    generate_and_build, save_rename_outputs,
    build_pan_message, build_spec_from_named_files,
)


class PromptEditDialog(QDialog):
    """AI 命名 Prompt 编辑对话框（支持保存 / 取消 / 还原默认）"""

    PLACEHOLDER_HELP = (
        "可用占位符（调用时会自动替换）：\n"
        "  {date} - 日期(MMDD)   {series_block} - 系列名块\n"
        "  {lang_desc} - 副题语言说明   {theme_block} - 主题背景块\n"
        "  {count_line} - 图片数量提示   {series_name_field} - AI取名时的JSON字段\n"
        "  {names_block} - 「沿用文件名作角色名」开启时的角色名块（模板缺省时自动追加到末尾）\n"
        "  {atmosphere_rules} - 文案模式对应的规则块   {atmosphere_field} - 对应的JSON字段行"
    )

    def __init__(self, current_template: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑 AI 命名 Prompt")
        self.resize(760, 620)
        self.setMinimumSize(520, 400)
        self._result_template: str | None = None  # 保存后返回的模板

        theme = ThemeManager.get_theme()
        self.setStyleSheet(theme.get_main_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        help_lbl = QLabel(self.PLACEHOLDER_HELP)
        help_lbl.setStyleSheet(
            f"color: {theme.text_secondary}; font-size: 11px; "
            f"background: {theme.bg_input}; padding: 8px; border-radius: 4px;"
        )
        help_lbl.setWordWrap(True)
        layout.addWidget(help_lbl)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 10))
        self.text_edit.setPlainText(current_template or DEFAULT_PROMPT_TEMPLATE)
        layout.addWidget(self.text_edit, 1)

        btn_row = QHBoxLayout()
        self.btn_restore = QPushButton("还原默认")
        self.btn_restore.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.btn_restore.clicked.connect(self._on_restore)
        btn_row.addWidget(self.btn_restore)

        btn_row.addStretch()

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("保存")
        self.btn_save.setStyleSheet(theme.get_button_stylesheet('primary'))
        self.btn_save.clicked.connect(self._on_save)
        btn_row.addWidget(self.btn_save)

        layout.addLayout(btn_row)

    def _on_restore(self):
        confirm = GenshinMessageBox(
            self, "还原默认",
            "确定将当前 Prompt 还原为初始默认模板？\n未保存的修改会丢失。",
            "success",
        )
        if confirm.exec():
            self.text_edit.setPlainText(DEFAULT_PROMPT_TEMPLATE)

    def _on_save(self):
        txt = self.text_edit.toPlainText().strip()
        # 保存原样文本（空串 = 使用默认）；与默认相同也存为空，避免冗余
        if not txt or txt == DEFAULT_PROMPT_TEMPLATE.strip():
            self._result_template = ""
        else:
            self._result_template = self.text_edit.toPlainText()
        self.accept()

    def get_template(self) -> str | None:
        """返回保存后的模板字符串（空串 = 使用默认）；取消时返回 None。"""
        return self._result_template


class PostTemplateEditDialog(QDialog):
    """小红书文案模板 + 默认标签编辑对话框。"""

    PLACEHOLDER_HELP = (
        "可用占位符（生成时自动替换）：\n"
        "  {date} - 日期(MMDD)   {series} - 系列名   {emoji} - 表情\n"
        "  {atmosphere} - 氛围文案 / 本期元素（随「Copy」下拉切换，留空时自动折叠空行）\n"
        "  {tags} - 标签字符串（含 # 前缀）"
    )

    def __init__(self, current_template: str, current_tags: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("编辑小红书文案模板")
        self.resize(720, 600)
        self.setMinimumSize(520, 400)
        self._result_template: str | None = None
        self._result_tags: str | None = None

        theme = ThemeManager.get_theme()
        self.setStyleSheet(theme.get_main_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        help_lbl = QLabel(self.PLACEHOLDER_HELP)
        help_lbl.setStyleSheet(
            f"color: {theme.text_secondary}; font-size: 11px; "
            f"background: {theme.bg_input}; padding: 8px; border-radius: 4px;"
        )
        help_lbl.setWordWrap(True)
        layout.addWidget(help_lbl)

        tpl_lbl = QLabel("文案模板：")
        tpl_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
        layout.addWidget(tpl_lbl)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 10))
        self.text_edit.setPlainText(current_template or DEFAULT_POST_TEMPLATE)
        layout.addWidget(self.text_edit, 1)

        tags_lbl = QLabel("默认标签（空格 / 逗号 分隔，无需 #）：")
        tags_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
        layout.addWidget(tags_lbl)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText(" ".join(DEFAULT_POST_TAGS))
        self.tags_edit.setText(current_tags or " ".join(DEFAULT_POST_TAGS))
        layout.addWidget(self.tags_edit)

        btn_row = QHBoxLayout()
        self.btn_restore = QPushButton("还原默认")
        self.btn_restore.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.btn_restore.clicked.connect(self._on_restore)
        btn_row.addWidget(self.btn_restore)

        btn_row.addStretch()

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setStyleSheet(theme.get_button_stylesheet('secondary'))
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("保存")
        self.btn_save.setStyleSheet(theme.get_button_stylesheet('primary'))
        self.btn_save.clicked.connect(self._on_save)
        btn_row.addWidget(self.btn_save)

        layout.addLayout(btn_row)

    def _on_restore(self):
        confirm = GenshinMessageBox(
            self, "还原默认",
            "确定将文案模板和默认标签都还原为初始值？\n未保存的修改会丢失。",
            "success",
        )
        if confirm.exec():
            self.text_edit.setPlainText(DEFAULT_POST_TEMPLATE)
            self.tags_edit.setText(" ".join(DEFAULT_POST_TAGS))

    def _on_save(self):
        tpl_raw = self.text_edit.toPlainText()
        tags_raw = self.tags_edit.text().strip()
        # 与默认相同则存空串，避免冗余
        if not tpl_raw.strip() or tpl_raw.strip() == DEFAULT_POST_TEMPLATE.strip():
            self._result_template = ""
        else:
            self._result_template = tpl_raw

        default_tags_str = " ".join(DEFAULT_POST_TAGS)
        if not tags_raw or parse_tag_list(tags_raw) == DEFAULT_POST_TAGS:
            self._result_tags = ""
        else:
            self._result_tags = tags_raw
        self.accept()

    def get_result(self) -> tuple:
        """返回 (template, tags)；空串表示使用默认；取消时两个都是 None。"""
        return self._result_template, self._result_tags


class PanDeliveryDialog(QDialog):
    """网盘发货信息生成对话框"""

    def __init__(self, file_names: list, image_paths: list, save_folder: str, config=None, parent=None):
        super().__init__(parent)
        self.file_names = file_names          # 已生成命名的文件名列表
        self.image_paths = image_paths        # 原始图片路径（用于 is_named_file 模式）
        self.save_folder = save_folder        # 规格清单.txt 所在目录
        self.config = config

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

        # 问候语编辑
        greeting_lbl = QLabel("发货问候语（每次发货信息开头）：")
        greeting_lbl.setStyleSheet(f"color: {theme.text_secondary}; font-size: 12px;")
        layout.addWidget(greeting_lbl)

        self.greeting_edit = QTextEdit()
        self.greeting_edit.setFixedHeight(60)
        self.greeting_edit.setPlaceholderText(PAN_GREETING)
        saved = self.config.pan_greeting if self.config else ""
        self.greeting_edit.setPlainText(saved if saved else PAN_GREETING)
        self.greeting_edit.textChanged.connect(self._on_greeting_changed)
        layout.addWidget(self.greeting_edit)

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

        self.copy_btn = QPushButton("复制")
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
            self.status_lbl.setText("请先粘贴网盘分享文本")
            return

        file_names, warnings = self._get_effective_file_names()
        if not file_names:
            self.status_lbl.setText("无可用文件名（请先生成命名或选择已命名图片）")
            return

        greeting = self.greeting_edit.toPlainText().strip()
        msg, unmatched = build_pan_message(file_names, pan_raw, greeting=greeting)
        self.result_text.setPlainText(msg)

        if warnings:
            skipped = warnings[0]
            prefix = f"已跳过 {skipped} 张未命名图片。"
        else:
            prefix = ""

        if unmatched:
            names_str = ", ".join(unmatched[:5])
            if len(unmatched) > 5:
                names_str += f" …等{len(unmatched)}个"
            matched_n = len(file_names) - len(unmatched)
            self.status_lbl.setText(
                f"{prefix}{matched_n}/{len(file_names)} 已匹配，未匹配: {names_str}"
            )
            self.status_lbl.setStyleSheet("color: orange; font-size: 11px;")
        else:
            self.status_lbl.setText(f"{prefix}全部 {len(file_names)} 个文件已匹配")
            self.status_lbl.setStyleSheet("color: #4CAF50; font-size: 11px;")

    def _on_copy(self):
        content = self.result_text.toPlainText().strip()
        if not content:
            return
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(content)
        self.status_lbl.setText("已复制到剪贴板")

    def _on_append(self):
        content = self.result_text.toPlainText().strip()
        if not content:
            self.status_lbl.setText("请先生成发货信息")
            return
        if not self.save_folder:
            self.status_lbl.setText("未知保存目录")
            return
        target = os.path.join(self.save_folder, "规格清单.txt")
        if not os.path.exists(target):
            self.status_lbl.setText("未找到 规格清单.txt，请先保存文件")
            return
        try:
            with open(target, "a", encoding="utf-8") as f:
                f.write("\n\n=== 发货信息 ===\n")
                f.write(content)
            self.status_lbl.setText("已追加到 规格清单.txt")
        except Exception as e:
            self.status_lbl.setText(f"写入失败: {e}")


    def _on_greeting_changed(self):
        if self.config:
            self.config.pan_greeting = self.greeting_edit.toPlainText().strip()
            self.config.save()


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
        grp = QGroupBox("Source Images")
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
        grp = QGroupBox("Naming Config")
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

        # 沿用文件名作角色名：开启后副题直接取图片文件名，AI 只负责系列名/文案/标签
        self.use_filename_chk = QCheckBox("沿用文件名作角色名")
        self.use_filename_chk.setToolTip(
            "开启后，每张图的角色名（副题）直接使用图片文件名（去扩展名），\n"
            "AI 不再另取副题，只负责系列名、氛围文案和标签。\n"
            "已按 MMDD-系列・副题 命名的文件会自动取其中的副题。"
        )
        self.use_filename_chk.setChecked(bool(getattr(self.config, "rename_use_filename_as_name", False)))
        self.use_filename_chk.stateChanged.connect(self._on_use_filename_changed)
        row1.addWidget(self.use_filename_chk)
        grid_lay.addLayout(row1)

        # 行2：副题语言 + Provider + Model + API Key 折叠按钮
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Tone:"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(TONE_OPTIONS)
        self.tone_combo.setMinimumWidth(180)
        row2.addWidget(self.tone_combo)

        # 文案模式：{atmosphere} 位置输出 氛围文案 / 本期元素 / 留空
        row2.addSpacing(12)
        row2.addWidget(QLabel("Copy:"))
        self.atmosphere_combo = QComboBox()
        self.atmosphere_combo.addItems(ATMOSPHERE_MODE_OPTIONS)
        self.atmosphere_combo.setToolTip(
            "小红书文案中 {atmosphere} 位置的内容：\n"
            "氛围文案 - AI 写 2-4 句诗意文案（默认）\n"
            "本期元素 - AI 概括「本期元素：xxx、xxx」关键词行\n"
            "留空 - 不生成，该段自动省略"
        )
        saved_mode = getattr(self.config, "rename_atmosphere_mode", "atmosphere")
        for label, key in ATMOSPHERE_MODE_KEY.items():
            if key == saved_mode:
                self.atmosphere_combo.setCurrentText(label)
                break
        self.atmosphere_combo.currentTextChanged.connect(self._on_atmosphere_mode_changed)
        row2.addWidget(self.atmosphere_combo)

        row2.addSpacing(12)
        row2.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([PROVIDERS[k]["display_name"] for k in PROVIDER_ORDER])
        self.provider_combo.setMinimumWidth(130)
        row2.addWidget(self.provider_combo)

        row2.addSpacing(8)
        row2.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(PROVIDERS["gemini"]["models"])
        self.model_combo.setMinimumWidth(220)
        self.model_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        # 弹出列表额外加宽，让长 model ID / ep-xxx 完整显示
        self.model_combo.view().setMinimumWidth(320)
        row2.addWidget(self.model_combo)

        # 在 model_combo 创建后再连接信号，避免 addItems 触发时 model_combo 尚未存在
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)

        row2.addStretch()

        # API Key 折叠指示按钮（右侧，状态指示）
        self.btn_apikey_toggle = QPushButton()
        self.btn_apikey_toggle.setFixedHeight(28)
        self.btn_apikey_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apikey_toggle.clicked.connect(self._on_toggle_api_key_section)
        row2.addWidget(self.btn_apikey_toggle)
        grid_lay.addLayout(row2)

        # 行3：主题提示词（选填）
        row3 = QHBoxLayout()
        hint_lbl = QLabel("Theme:")
        hint_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px;")
        row3.addWidget(hint_lbl)
        self.theme_hint_edit = QLineEdit()
        self.theme_hint_edit.setPlaceholderText("可选：描述主题风格/角色背景，帮助 AI 更精准输出（如：暗黑风鬼怪，主角是狐妖）")
        row3.addWidget(self.theme_hint_edit, 1)

        self.btn_edit_prompt = QPushButton("Edit Prompt")
        self.btn_edit_prompt.setFixedHeight(28)
        self.btn_edit_prompt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_prompt.setToolTip("编辑内置的 AI 命名 Prompt 模板")
        self.btn_edit_prompt.clicked.connect(self._on_edit_prompt)
        self._update_edit_prompt_btn_style()
        row3.addWidget(self.btn_edit_prompt)

        self.btn_edit_post = QPushButton("Edit Post")
        self.btn_edit_post.setFixedHeight(28)
        self.btn_edit_post.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_post.clicked.connect(self._on_edit_post)
        self._update_edit_post_btn_style()
        row3.addWidget(self.btn_edit_post)
        grid_lay.addLayout(row3)

        # 行4：API Key 展开区（初始折叠）
        self._api_key_widget = QWidget()
        key_lay = QHBoxLayout(self._api_key_widget)
        key_lay.setContentsMargins(0, 4, 0, 0)
        key_lay.setSpacing(6)

        self._key_lbl = QLabel("Gemini Key:")
        self._key_lbl.setStyleSheet(f"color: {self.theme.text_secondary}; font-size: 12px;")
        key_lay.addWidget(self._key_lbl)

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

        # 初始：已有 Gemini Key 则折叠，没有则展开
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

        self.btn_generate = QPushButton("Generate Names")
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

        self.btn_spec = QPushButton("Generate Specs")
        self.btn_spec.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_spec.clicked.connect(self._on_generate_spec)
        tool_row.addWidget(self.btn_spec)

        self.btn_pan = QPushButton("Pan Delivery")
        self.btn_pan.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_pan.clicked.connect(self._on_pan_delivery)
        tool_row.addWidget(self.btn_pan)
        lay.addLayout(tool_row)

        return container

    def _make_results_group(self) -> QGroupBox:
        grp = QGroupBox("Results")
        lay = QVBoxLayout(grp)
        lay.setSpacing(10)

        # 3-tab 结果区
        self.result_tabs = QTabWidget()
        self._tab_filenames = self._make_result_tab()
        self._tab_display = self._make_result_tab()
        self._tab_post = self._make_result_tab()
        self.result_tabs.addTab(self._tab_filenames[0], "File Names")
        self.result_tabs.addTab(self._tab_display[0], "Display Names")
        self.result_tabs.addTab(self._tab_post[0], "Post Copy")
        self.result_tabs.setMinimumHeight(200)
        lay.addWidget(self.result_tabs)

        # 操作按钮行
        btn_row = QHBoxLayout()

        self.btn_save_txt = QPushButton("Save TXT Files")
        self.btn_save_txt.setStyleSheet(self.theme.get_button_stylesheet('secondary'))
        self.btn_save_txt.clicked.connect(self._on_save_txt)
        btn_row.addWidget(self.btn_save_txt)

        self.btn_save_rename = QPushButton("Save & Rename")
        self.btn_save_rename.setStyleSheet(self.theme.get_button_stylesheet('primary'))
        self.btn_save_rename.clicked.connect(self._on_save_and_rename)
        btn_row.addWidget(self.btn_save_rename)

        self.btn_rename = QPushButton("Rename Files")
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

        copy_btn = QPushButton("Copy")
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
        init_dir = self.config.last_images_directory or os.path.expanduser("~")
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", init_dir, ext_filter)
        if not files:
            return
        self.image_paths = sort_paths(files)
        self.config.last_images_directory = os.path.dirname(self.image_paths[0])
        # 新一批图片 → 清掉上一批的命名结果，避免误用到新批次
        self._last_outputs = {}
        self._results_group.setVisible(False)
        self.config_changed.emit()
        n = len(self.image_paths)
        self.lbl_count.setText(f"{n} image{'s' if n != 1 else ''} selected")
        self.list_files.clear()
        for p in self.image_paths:
            self.list_files.addItem(os.path.basename(p))

    def _on_toggle_api_key_section(self):
        self._api_key_expanded = not self._api_key_expanded
        self._api_key_widget.setVisible(self._api_key_expanded)
        self._update_apikey_btn_label()

    def _current_provider_key(self) -> str:
        """根据 combo 的 display_name 反查 PROVIDERS 的内部 key。"""
        txt = self.provider_combo.currentText() if hasattr(self, 'provider_combo') else ""
        for k in PROVIDER_ORDER:
            if PROVIDERS[k]["display_name"] == txt:
                return k
        return "gemini"

    def _update_apikey_btn_label(self):
        """根据当前 provider 的 Key 状态和展开状态更新按钮文字和颜色"""
        spec = PROVIDERS[self._current_provider_key()]
        has_key = bool(getattr(self.config, spec["key_attr"], ""))
        arrow = "▲" if self._api_key_expanded else "▼"
        if has_key:
            self.btn_apikey_toggle.setText(f"Key set {arrow}")
            self.btn_apikey_toggle.setStyleSheet(
                self.theme.get_button_stylesheet('secondary') +
                "QPushButton { color: #4CAF50; border-color: #4CAF50; }"
            )
        else:
            self.btn_apikey_toggle.setText(f"Set API Key {arrow}")
            self.btn_apikey_toggle.setStyleSheet(
                self.theme.get_button_stylesheet('secondary') +
                "QPushButton { color: #FF9800; border-color: #FF9800; }"
            )

    def _on_provider_changed(self, provider_text: str):
        """切换 provider 时：更新模型列表、Key 输入框内容和标签。"""
        spec = PROVIDERS[self._current_provider_key()]
        self.model_combo.clear()
        self.model_combo.setEditable(spec.get("model_editable", False))
        self.model_combo.addItems(spec["models"])
        self.model_combo.view().setMinimumWidth(320)
        self._key_lbl.setText(spec["key_label"])
        self.key_edit.setPlaceholderText(spec["key_placeholder"])
        self.key_edit.setText(getattr(self.config, spec["key_attr"], ""))
        # 切换后重置显示状态
        self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_toggle_key.setText("Show")
        self._update_apikey_btn_label()

    def _update_edit_prompt_btn_style(self):
        """自定义 Prompt 时按钮高亮，否则普通样式。"""
        is_custom = bool(self.config.custom_prompt)
        base = self.theme.get_button_stylesheet('secondary')
        if is_custom:
            self.btn_edit_prompt.setText("Edit Prompt *")
            self.btn_edit_prompt.setStyleSheet(
                base + "QPushButton { color: #4CAF50; border-color: #4CAF50; }"
            )
            self.btn_edit_prompt.setToolTip("当前使用自定义 Prompt（点击编辑）")
        else:
            self.btn_edit_prompt.setText("Edit Prompt")
            self.btn_edit_prompt.setStyleSheet(base)
            self.btn_edit_prompt.setToolTip("编辑内置的 AI 命名 Prompt 模板")

    def _on_edit_prompt(self):
        dlg = PromptEditDialog(self.config.custom_prompt, parent=self)
        if dlg.exec():
            tpl = dlg.get_template()
            if tpl is not None:
                self.config.custom_prompt = tpl
                self.config_changed.emit()
                self._update_edit_prompt_btn_style()
                self.lbl_status.setText(
                    "Prompt saved (custom)" if tpl else "Prompt reset to default"
                )

    def _update_edit_post_btn_style(self):
        """自定义文案模板或标签时按钮高亮。"""
        is_custom = bool(self.config.custom_post_template) or bool(self.config.custom_post_tags)
        base = self.theme.get_button_stylesheet('secondary')
        if is_custom:
            self.btn_edit_post.setText("Edit Post *")
            self.btn_edit_post.setStyleSheet(
                base + "QPushButton { color: #4CAF50; border-color: #4CAF50; }"
            )
            self.btn_edit_post.setToolTip("当前使用自定义文案模板（点击编辑）")
        else:
            self.btn_edit_post.setText("Edit Post")
            self.btn_edit_post.setStyleSheet(base)
            self.btn_edit_post.setToolTip("编辑小红书文案模板和默认标签")

    def _on_edit_post(self):
        dlg = PostTemplateEditDialog(
            self.config.custom_post_template,
            self.config.custom_post_tags,
            parent=self,
        )
        if dlg.exec():
            tpl, tags = dlg.get_result()
            if tpl is not None:
                self.config.custom_post_template = tpl
                self.config.custom_post_tags = tags or ""
                self.config_changed.emit()
                self._update_edit_post_btn_style()
                self.lbl_status.setText(
                    "Post template saved (custom)" if (tpl or tags) else "Post template reset to default"
                )

    def _on_auto_series_changed(self, state):
        if state:
            self.series_edit.setPlaceholderText("（可选：给 AI 一个参考方向）")
        else:
            self.series_edit.setPlaceholderText("系列名")

    def _current_atmosphere_mode(self) -> str:
        return ATMOSPHERE_MODE_KEY.get(self.atmosphere_combo.currentText(), "atmosphere")

    def _on_atmosphere_mode_changed(self, _text):
        self.config.rename_atmosphere_mode = self._current_atmosphere_mode()
        self.config_changed.emit()

    def _on_use_filename_changed(self, state):
        self.config.rename_use_filename_as_name = bool(state)
        self.config_changed.emit()
        self.lbl_status.setText("角色名将沿用图片文件名" if state else "角色名由 AI 生成")

    def _on_toggle_key_visibility(self):
        if self.key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle_key.setText("Hide")
        else:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle_key.setText("Show")

    def _on_save_key(self):
        key = self.key_edit.text().strip()
        spec = PROVIDERS[self._current_provider_key()]
        setattr(self.config, spec["key_attr"], key)
        self.config_changed.emit()
        self.lbl_status.setText("API Key saved")
        self._update_apikey_btn_label()
        # 保存后自动折叠
        if key and self._api_key_expanded:
            self._api_key_expanded = False
            self._api_key_widget.setVisible(False)
            self._update_apikey_btn_label()

    def _on_generate(self):
        if not self.image_paths:
            dlg = GenshinMessageBox(self, "Oops", "Please select images first!", "error")
            dlg.exec()
            return
        api_key = self.key_edit.text().strip()
        provider = self.provider_combo.currentText()
        use_filename_as_name = self.use_filename_chk.isChecked()
        atmosphere_mode = self._current_atmosphere_mode()
        auto_series = self.auto_series_chk.isChecked()
        # 角色名沿用文件名 + 文案留空 + 手动系列名 → 本地生成，不需要 API Key
        offline = can_build_offline(use_filename_as_name, atmosphere_mode, auto_series)
        if not api_key and not offline:
            dlg = GenshinMessageBox(self, "Oops", f"Please enter your {provider} API Key!", "error")
            dlg.exec()
            return
        date = self.date_edit.text().strip()
        if not date:
            dlg = GenshinMessageBox(self, "Oops", "Please enter the date (MMDD)!", "error")
            dlg.exec()
            return
        series = self.series_edit.text().strip()
        if not auto_series and not series:
            dlg = GenshinMessageBox(self, "Oops", "Please enter a series name or enable AI naming!", "error")
            dlg.exec()
            return

        self.btn_generate.setEnabled(False)
        self.lbl_status.setText("Building locally (no API call)…" if offline else f"Calling {provider} API…")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)   # indeterminate

        tone = TONE_KEY.get(self.tone_combo.currentText(), "中文")
        model = self.model_combo.currentText()
        theme_hint = self.theme_hint_edit.text().strip()
        image_paths_copy = self.image_paths.copy()
        provider_key = self._current_provider_key()
        custom_prompt = self.config.custom_prompt
        custom_post_template = self.config.custom_post_template
        custom_post_tags_list = parse_tag_list(self.config.custom_post_tags) or None

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
                    provider=provider_key,
                    theme_hint=theme_hint,
                    prompt_template=custom_prompt,
                    post_template=custom_post_template or None,
                    default_tags=custom_post_tags_list,
                    use_filename_as_name=use_filename_as_name,
                    atmosphere_mode=atmosphere_mode,
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

        # 填充 3 个 tab
        self._tab_filenames[1].setPlainText("\n".join(outputs["file_names"]))
        self._tab_display[1].setPlainText("\n".join(outputs["display_names"]))
        self._tab_post[1].setPlainText(outputs["post"])

        self._results_group.setVisible(True)
        if result.get("offline"):
            suffix = " (本地生成，未调用 API)"
        elif self.use_filename_chk.isChecked():
            suffix = " (角色名沿用文件名)"
        else:
            suffix = ""
        self.lbl_status.setText(f"Done. Generated {len(outputs['file_names'])} names.{suffix}")

    def _on_generation_error(self, err: str):
        self.btn_generate.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.lbl_status.setText("Generation failed")
        dlg = GenshinMessageBox(self, "API Error", f"Call failed:\n\n{err[:600]}", "error")
        dlg.exec()

    def _default_target_dir(self) -> str:
        """Save TXT / Rename / Generate Specs 共用的默认目录 —— 始终跟着当前选中的图片走。"""
        if self.image_paths:
            return os.path.dirname(self.image_paths[0])
        return self.config.rename_save_directory or self.config.last_images_directory or ""

    def _build_rename_confirm_msg(self, target_folder: str, action: str) -> str:
        """Confirm Rename / Save & Rename 弹窗的正文。
        显式列出目标目录，并在源/目标目录不同时提示「文件会被移动」，避免误把上一批的目录用上。
        """
        source_dirs = {os.path.dirname(p) for p in self.image_paths if p}
        cross_folder = bool(source_dirs) and any(d != target_folder for d in source_dirs)

        header = "Will save TXT files and rename:" if action == "save_rename" else "Will rename the following files:"
        lines = [header, "", f"Target folder:  {target_folder}"]
        if cross_folder:
            # 跨目录 = os.rename 会把文件物理移动过去
            src_summary = next(iter(source_dirs)) if len(source_dirs) == 1 else f"{len(source_dirs)} folders"
            lines.append(f"Source folder:  {src_summary}")
            lines.append("[!] Files will be MOVED to the target folder (cross-folder rename).")
        lines.append("")

        for i, p in enumerate(self.image_paths):
            if i < len(self._last_outputs["file_names"]):
                lines.append(f"{os.path.basename(p)}  ->  {self._last_outputs['file_names'][i]}")
        return "\n".join(lines)

    def _on_save_txt(self):
        if not self._last_outputs:
            dlg = GenshinMessageBox(self, "Oops", "Please generate names first!", "error")
            dlg.exec()
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder", self._default_target_dir())
        if not folder:
            return
        try:
            result = save_rename_outputs(
                folder=folder,
                image_paths=self.image_paths,
                outputs=self._last_outputs,
                save_txts=True,
                rename_images=False,
            )
            self.config.rename_save_directory = folder
            self.config_changed.emit()
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
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder", self._default_target_dir())
        if not folder:
            return

        confirm_msg = self._build_rename_confirm_msg(folder, "rename")
        dlg_confirm = GenshinMessageBox(self, "Confirm Rename", confirm_msg, "success")
        if not dlg_confirm.exec():
            return

        try:
            result = save_rename_outputs(
                folder=folder,
                image_paths=self.image_paths,
                outputs=self._last_outputs,
                save_txts=False,
                rename_images=True,
            )
            self.config.rename_save_directory = folder
            self.config_changed.emit()
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

    def _on_save_and_rename(self):
        """一键：写 文案.txt + 规格清单.txt，然后按命名重命名图片。"""
        if not self._last_outputs:
            dlg = GenshinMessageBox(self, "Oops", "Please generate names first!", "error")
            dlg.exec()
            return
        folder = QFileDialog.getExistingDirectory(self, "Select Target Folder", self._default_target_dir())
        if not folder:
            return

        confirm_msg = self._build_rename_confirm_msg(folder, "save_rename")
        dlg_confirm = GenshinMessageBox(self, "Confirm Save & Rename", confirm_msg, "success")
        if not dlg_confirm.exec():
            return

        try:
            result = save_rename_outputs(
                folder=folder,
                image_paths=self.image_paths,
                outputs=self._last_outputs,
                save_txts=True,
                rename_images=True,
            )
            self.config.rename_save_directory = folder
            self.config_changed.emit()
            self.image_paths = [
                os.path.join(folder, new) for _, new in result["renamed"]
            ]
            self.list_files.clear()
            for p in self.image_paths:
                self.list_files.addItem(os.path.basename(p))

            saved = ", ".join(result["txt_files"])
            count = len(result["renamed"])
            msg = f"Saved {saved}\nRenamed {count} file(s)\n\n{folder}"
            dlg = GenshinMessageBox(self, "Done", msg, "success")
            dlg.exec()
        except Exception as e:
            dlg = GenshinMessageBox(self, "Error", f"Save & Rename failed:\n{e}", "error")
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
        folder = QFileDialog.getExistingDirectory(self, "Select Save Folder", self._default_target_dir())
        if not folder:
            return

        try:
            spec_path = os.path.join(folder, "规格清单.txt")
            with open(spec_path, "w", encoding="utf-8") as f:
                f.write("\n".join(result["display_names"]))
            self.config.rename_save_directory = folder
            self.config_changed.emit()

            named_count = len(result["display_names"])
            total_count = len(self.image_paths)
            if named_count < total_count:
                skipped = total_count - named_count
                msg = f"Saved 规格清单.txt ({named_count} entries, skipped {skipped} unnamed files)\n\n{folder}"
            else:
                msg = f"Saved 规格清单.txt ({named_count} entries)\n\n{folder}"
            dlg = GenshinMessageBox(self, "Saved", msg, "success")
            dlg.exec()
            self.lbl_status.setText(f"Specs saved ({named_count} entries)")
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
            save_folder=self._default_target_dir(),
            config=self.config,
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
