import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import json
import numpy as np
import threading
import time
from text_label_module import TextLabelConfig, draw_text_label

# 导入核心业务逻辑
from watermark_core import (
    WatermarkLayer,
    WatermarkEngine,
    WatermarkConfig,
    BatchProcessor
)

class MultiLayerWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Layer Watermark App v1.5")
        self.root.configure(bg='#FAFAFA')

        # Set minimum window size
        self.root.minsize(550, 650)

        # 使用 watermark_core 的配置管理
        self.config = WatermarkConfig()
        self.config.load()

        # Initialize variables
        self.images = []
        self.image_paths = []
        self.watermark_layers = []  # 现在使用导入的 WatermarkLayer 类

        # 从 config 对象获取路径
        self.save_directory = self.config.save_directory
        self.last_used_directory = self.config.last_used_directory
        self.last_watermark_directory = self.config.last_watermark_directory
        self.last_images_directory = self.config.last_images_directory
        self.last_images_files = self.config.last_images_files
        self.last_stretch = self.config.last_stretch

        # Initialize UI variables
        self.stretch_var = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.layer_listbox = None
        self.blend_mode_var = None
        self.blend_mode_combo = None
        self.opacity_entry = None
        self.opacity_var = None
        self.opacity_slider = None

        # 记住当前选中的图层索引
        self.current_layer_index = None

        # 标志位：防止循环更新
        self._updating_opacity = False

        # 处理线程
        self.processing_thread = None

        # 文本标注配置（从 config 获取）
        self.text_label_config = self.config.text_label_config

        # 加载上次的图层
        self.watermark_layers = self.config.layers.copy()

        # Create UI
        self.create_ui()

        # Auto-load last used files
        self.auto_load_last_files()

    def create_ui(self):
        """创建用户界面"""
        # Main container
        main_container = tk.Frame(self.root, bg='#FAFAFA')
        main_container.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title section
        title_frame = tk.Frame(main_container, bg='#FAFAFA')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(
            title_frame,
            text="Multi-Layer Watermark App v1.5",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="🎨 Multi-Layer with Blend Modes",
            font=('Helvetica', 12),
            fg='#0095F6',
            bg='#FAFAFA'
        )
        subtitle_label.pack()

        # File upload section
        self.create_upload_section(main_container)

        # Layer management section
        self.create_layer_section(main_container)

        # Settings section
        self.create_settings_section(main_container)

        # Text label section
        self.create_text_label_section(main_container)

        # Progress section
        self.create_progress_section(main_container)

        # Save directory section
        self.create_save_section(main_container)

        # Action buttons
        self.create_action_section(main_container)

    def create_upload_section(self, parent):
        """创建文件上传区域"""
        upload_frame = tk.LabelFrame(parent, text="📁 File Upload", font=('Helvetica', 11, 'bold'),
                                   fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        upload_frame.pack(fill=tk.X, pady=(0, 15))

        button_style = {
            'font': ('Helvetica', 10),
            'bg': '#0095F6',
            'fg': 'white',
            'activebackground': '#0081D6',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }

        btn_frame = tk.Frame(upload_frame, bg='#FAFAFA')
        btn_frame.pack(fill=tk.X)

        self.upload_image_btn = tk.Button(btn_frame, text="Upload Images",
                                        command=self.upload_images, **button_style)
        self.upload_image_btn.pack(side=tk.LEFT, padx=(0, 10))

    def create_layer_section(self, parent):
        """创建图层管理区域"""
        layer_frame = tk.LabelFrame(parent, text="🎨 Watermark Layers", font=('Helvetica', 11, 'bold'),
                                   fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        layer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 提示信息
        tip_label = tk.Label(layer_frame, text="💡 Larger layer numbers appear on top (覆盖下层)",
                           font=('Helvetica', 9), fg='#666666', bg='#FAFAFA', anchor='w')
        tip_label.pack(fill=tk.X, pady=(0, 5))

        # Layer list
        list_frame = tk.Frame(layer_frame, bg='#FAFAFA')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.layer_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       font=('Courier', 9), height=6, bg='#FFFFFF',
                                       selectmode=tk.SINGLE)
        self.layer_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.layer_listbox.bind('<<ListboxSelect>>', self.on_layer_select)
        scrollbar.config(command=self.layer_listbox.yview)

        # Layer control buttons
        btn_frame = tk.Frame(layer_frame, bg='#FAFAFA')
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        button_style = {
            'font': ('Helvetica', 9),
            'bg': '#0095F6',
            'fg': 'white',
            'activebackground': '#0081D6',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'padx': 10,
            'pady': 5,
            'cursor': 'hand2'
        }

        tk.Button(btn_frame, text="+ Add Layer", command=self.add_watermark_layer,
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="👁️ Toggle", command=self.toggle_layer_visibility,
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="× Remove", command=self.remove_selected_layer,
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="↑ Up", command=lambda: self.move_layer(-1),
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="↓ Down", command=lambda: self.move_layer(1),
                 **button_style).pack(side=tk.LEFT)

        # Layer editor panel (inline)
        editor_frame = tk.LabelFrame(layer_frame, text="Layer Properties", font=('Helvetica', 10, 'bold'),
                                    fg='#262626', bg='#FAFAFA', padx=10, pady=8)
        editor_frame.pack(fill=tk.X)

        # Blend mode
        blend_row = tk.Frame(editor_frame, bg='#FAFAFA')
        blend_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(blend_row, text="Blend Mode:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=12, anchor='w').pack(side=tk.LEFT)

        self.blend_mode_var = tk.StringVar(value='normal')
        self.blend_mode_combo = ttk.Combobox(blend_row, textvariable=self.blend_mode_var,
                                            values=['normal', 'overlay', 'screen', 'soft_light'],
                                            state='readonly', width=15)
        self.blend_mode_combo.pack(side=tk.LEFT)
        self.blend_mode_combo.bind('<<ComboboxSelected>>', self.on_blend_mode_change)

        # Opacity
        opacity_row = tk.Frame(editor_frame, bg='#FAFAFA')
        opacity_row.pack(fill=tk.X, pady=(0, 5))

        tk.Label(opacity_row, text="Opacity (%):", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=12, anchor='w').pack(side=tk.LEFT)

        # Opacity entry with validation
        vcmd = (self.root.register(self.validate_opacity), '%P')
        self.opacity_entry = tk.Entry(opacity_row, width=8, validate='key', validatecommand=vcmd)
        self.opacity_entry.insert(0, '100')
        self.opacity_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.opacity_entry.bind('<KeyRelease>', self.on_opacity_entry_change)
        self.opacity_entry.bind('<FocusOut>', self.on_opacity_entry_change)

        # Opacity slider
        self.opacity_var = tk.IntVar(value=100)
        self.opacity_slider = tk.Scale(opacity_row, from_=0, to=100, orient=tk.HORIZONTAL,
                                      variable=self.opacity_var, showvalue=False,
                                      length=150, command=self.on_opacity_slider_change)
        self.opacity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 默认禁用编辑器
        self.blend_mode_combo.config(state='disabled')
        self.opacity_entry.config(state='disabled')
        self.opacity_slider.config(state='disabled')

    def create_settings_section(self, parent):
        """创建基础设置区域"""
        settings_frame = tk.LabelFrame(parent, text="⚙️ Settings", font=('Helvetica', 11, 'bold'),
                                     fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        # Stretch option
        self.stretch_var = tk.BooleanVar(value=getattr(self, 'last_stretch', False))
        stretch_cb = ttk.Checkbutton(settings_frame, text="Stretch watermark to fit image",
                                   variable=self.stretch_var, command=self.on_stretch_change)
        stretch_cb.pack(pady=5)

    def create_text_label_section(self, parent):
        """创建文本标注设置区域"""
        label_frame = tk.LabelFrame(parent, text="🔤 Text Label (文字标注)", font=('Helvetica', 11, 'bold'),
                                   fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        label_frame.pack(fill=tk.X, pady=(0, 15))

        # 启用标注
        self.label_enabled_var = tk.BooleanVar(value=self.text_label_config.enabled)
        enabled_cb = ttk.Checkbutton(label_frame, text="Enable text label (add number or filename)",
                                    variable=self.label_enabled_var,
                                    command=self.on_label_enabled_change)
        enabled_cb.pack(anchor='w', pady=(0, 8))

        # 标注类型
        type_row = tk.Frame(label_frame, bg='#FAFAFA')
        type_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(type_row, text="Label Type:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=10, anchor='w').pack(side=tk.LEFT, padx=(0, 10))

        self.label_type_var = tk.StringVar(value=self.text_label_config.label_type)
        label_type_combo = ttk.Combobox(type_row, textvariable=self.label_type_var,
                                       values=['number', 'filename'],
                                       state='readonly', width=12)
        label_type_combo.pack(side=tk.LEFT)
        label_type_combo.bind('<<ComboboxSelected>>', self.on_label_type_change)

        # 位置选择
        position_row = tk.Frame(label_frame, bg='#FAFAFA')
        position_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(position_row, text="Position:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=10, anchor='w').pack(side=tk.LEFT, padx=(0, 10))

        self.label_position_var = tk.StringVar(value=self.text_label_config.position)
        position_combo = ttk.Combobox(position_row, textvariable=self.label_position_var,
                                     values=['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'],
                                     state='readonly', width=12)
        position_combo.pack(side=tk.LEFT)
        position_combo.bind('<<ComboboxSelected>>', self.on_label_position_change)

        # 文字方向选择
        orientation_row = tk.Frame(label_frame, bg='#FAFAFA')
        orientation_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(orientation_row, text="Orientation:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=10, anchor='w').pack(side=tk.LEFT, padx=(0, 10))

        self.label_orientation_var = tk.StringVar(value=self.text_label_config.orientation)
        orientation_combo = ttk.Combobox(orientation_row, textvariable=self.label_orientation_var,
                                        values=['horizontal', 'vertical'],
                                        state='readonly', width=12)
        orientation_combo.pack(side=tk.LEFT)
        orientation_combo.bind('<<ComboboxSelected>>', self.on_label_orientation_change)

        # 字体选择（类似 Photoshop）
        font_row = tk.Frame(label_frame, bg='#FAFAFA')
        font_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(font_row, text="Font:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=10, anchor='w').pack(side=tk.LEFT, padx=(0, 10))

        # 获取系统字体并导入函数
        from text_label_module import get_system_fonts
        system_fonts = get_system_fonts()
        font_names = sorted(system_fonts.keys())

        self.label_font_var = tk.StringVar(value=self.text_label_config.font_name or '(Auto)')
        font_combo = ttk.Combobox(font_row, textvariable=self.label_font_var,
                                  values=['(Auto)'] + font_names,
                                  state='readonly', width=20)
        font_combo.pack(side=tk.LEFT)
        font_combo.bind('<<ComboboxSelected>>', self.on_label_font_change)

        # 字体大小（百分比，相对于图片高度）
        size_row = tk.Frame(label_frame, bg='#FAFAFA')
        size_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(size_row, text="Font Size:", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=10, anchor='w').pack(side=tk.LEFT, padx=(0, 10))

        self.label_font_size_var = tk.DoubleVar(value=self.text_label_config.font_size)
        self.label_font_size_slider = tk.Scale(size_row, from_=0.5, to=10.0, resolution=0.1,
                                               orient=tk.HORIZONTAL,
                                               variable=self.label_font_size_var,
                                               showvalue=True, length=180,
                                               command=self.on_label_font_size_change)
        self.label_font_size_slider.pack(side=tk.LEFT)

        tk.Label(size_row, text="% (of image height)", font=('Helvetica', 9),
                fg='#666666', bg='#FAFAFA').pack(side=tk.LEFT, padx=(5, 0))

        # 提示信息
        tip_label = tk.Label(label_frame,
                           text="💡 Number: 1, 2, 3...  |  Filename: image_name  |  Font: Auto-detect",
                           font=('Helvetica', 8), fg='#666666', bg='#FAFAFA')
        tip_label.pack(anchor='w', pady=(5, 0))

    def create_progress_section(self, parent):
        """创建进度显示区域"""
        progress_frame = tk.Frame(parent, bg='#FAFAFA')
        progress_frame.pack(fill=tk.X, pady=(0, 15))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = tk.Label(progress_frame, text="Ready to process",
                                   font=('Helvetica', 9), fg='#666666', bg='#FAFAFA')
        self.status_label.pack()

    def create_save_section(self, parent):
        """创建保存目录区域"""
        save_frame = tk.Frame(parent, bg='#FAFAFA')
        save_frame.pack(fill=tk.X, pady=(0, 15))

        button_style = {
            'font': ('Helvetica', 10),
            'bg': '#0095F6',
            'fg': 'white',
            'activebackground': '#0081D6',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }

        self.save_dir_btn = tk.Button(save_frame, text="Select Save Directory",
                                    command=self.select_save_directory, **button_style)
        self.save_dir_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.save_dir_label = tk.Label(save_frame, text="No directory selected",
                                     wraplength=300, justify=tk.LEFT, bg='#FFFFFF',
                                     fg='#262626', relief=tk.SOLID, borderwidth=1,
                                     padx=10, pady=5)
        self.save_dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.update_save_dir_label()

    def create_action_section(self, parent):
        """创建操作按钮区域"""
        action_frame = tk.Frame(parent, bg='#FAFAFA')
        action_frame.pack(fill=tk.X, pady=(15, 0))

        button_style = {
            'font': ('Helvetica', 14, 'bold'),
            'bg': '#0095F6',
            'fg': 'white',
            'activebackground': '#0081D6',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'padx': 30,
            'pady': 15,
            'cursor': 'hand2'
        }

        self.apply_btn = tk.Button(action_frame, text="🚀 Apply Multi-Layer Watermark",
                                 command=self.apply_watermark_threaded, **button_style)
        self.apply_btn.pack(fill=tk.X)

    # 图层管理方法
    def add_watermark_layer(self):
        """添加水印图层"""
        self.root.lift()
        initial_dir = self.last_watermark_directory if self.last_watermark_directory else "/"
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")],
            initialdir=initial_dir,
            parent=self.root
        )
        if file_path:
            # 创建新图层（默认 normal 模式，100% 不透明度）
            layer = WatermarkLayer(file_path, opacity=100, blend_mode='normal')
            self.watermark_layers.append(layer)
            self.last_watermark_directory = os.path.dirname(file_path)

            # 更新列表显示
            self.update_layer_listbox()

            # 自动选中新添加的图层
            self.layer_listbox.selection_clear(0, tk.END)
            self.layer_listbox.selection_set(len(self.watermark_layers) - 1)
            self.layer_listbox.see(len(self.watermark_layers) - 1)
            self.on_layer_select(None)

            self.save_config()

    def on_layer_select(self, event):
        """当选中图层时，更新编辑面板"""
        selection = self.layer_listbox.curselection()
        if not selection:
            # 没有选中，禁用编辑器
            self.current_layer_index = None
            self.blend_mode_combo.config(state='disabled')
            self.opacity_entry.config(state='disabled')
            self.opacity_slider.config(state='disabled')
            return

        # 有选中，启用编辑器并显示当前图层属性
        index = selection[0]
        self.current_layer_index = index  # 记住当前选中的图层
        layer = self.watermark_layers[index]

        print(f"🎯 Layer selected: [{index}] {layer.name} (blend_mode={layer.blend_mode}, opacity={layer.opacity})")

        self.blend_mode_combo.config(state='readonly')
        self.opacity_entry.config(state='normal')
        self.opacity_slider.config(state='normal')

        # 更新显示值（使用标志位防止循环更新）
        self._updating_opacity = True
        try:
            self.blend_mode_var.set(layer.blend_mode)
            self.opacity_entry.delete(0, tk.END)
            self.opacity_entry.insert(0, str(int(layer.opacity)))
            self.opacity_var.set(int(layer.opacity))  # 更新滑块
            print(f"  - UI updated: blend_mode_var={self.blend_mode_var.get()}, opacity={self.opacity_entry.get()}")
        finally:
            self._updating_opacity = False

    def validate_opacity(self, value):
        """验证不透明度输入"""
        if value == "":
            return True
        try:
            num = int(value)
            return 0 <= num <= 100
        except ValueError:
            return False

    def on_blend_mode_change(self, event):
        """混合模式改变时"""
        # 使用记住的索引，而不是依赖 listbox 选中状态
        if self.current_layer_index is None:
            print("⚠️ No layer selected (current_layer_index is None)")
            return

        index = self.current_layer_index
        if index >= len(self.watermark_layers):
            print(f"⚠️ Invalid layer index: {index} >= {len(self.watermark_layers)}")
            return

        layer = self.watermark_layers[index]
        new_mode = self.blend_mode_var.get()

        print(f"🎨 Blend mode changed: {layer.blend_mode} -> {new_mode} (layer index: {index})")
        layer.blend_mode = new_mode

        # 更新列表显示（不触发选中事件）
        self.update_layer_listbox_silent(index)
        print(f"✅ Layer blend_mode saved: {self.watermark_layers[index].blend_mode}")
        self.save_config()

    def on_opacity_entry_change(self, event):
        """不透明度输入改变时"""
        # 防止循环更新
        if self._updating_opacity:
            return

        # 使用记住的索引，而不是依赖 listbox 选中状态
        if self.current_layer_index is None:
            return

        value = self.opacity_entry.get()
        if value == "":
            return

        try:
            opacity = int(value)
            if 0 <= opacity <= 100:
                index = self.current_layer_index
                if index >= len(self.watermark_layers):
                    return

                layer = self.watermark_layers[index]
                layer.opacity = int(opacity)  # 确保是整数

                # 同步更新滑块
                self._updating_opacity = True
                try:
                    self.opacity_var.set(opacity)
                finally:
                    self._updating_opacity = False

                # 更新列表显示（不触发选中事件）
                self.update_layer_listbox_silent(index)
                self.save_config()
        except ValueError:
            pass

    def on_opacity_slider_change(self, value):
        """滑块改变时"""
        # 防止循环更新
        if self._updating_opacity:
            return

        # 使用记住的索引
        if self.current_layer_index is None:
            return

        try:
            opacity = int(float(value))  # Scale 返回的可能是字符串
            if 0 <= opacity <= 100:
                index = self.current_layer_index
                if index >= len(self.watermark_layers):
                    return

                layer = self.watermark_layers[index]
                layer.opacity = opacity

                # 同步更新输入框
                self._updating_opacity = True
                try:
                    self.opacity_entry.delete(0, tk.END)
                    self.opacity_entry.insert(0, str(opacity))
                finally:
                    self._updating_opacity = False

                # 更新列表显示（不触发选中事件）
                self.update_layer_listbox_silent(index)
                self.save_config()
        except (ValueError, TypeError):
            pass

    def remove_selected_layer(self):
        """删除选中的图层"""
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "请先选择一个图层！")
            return

        index = selection[0]
        del self.watermark_layers[index]
        self.update_layer_listbox()

        # 如果还有图层，选中前一个
        if self.watermark_layers:
            new_index = min(index, len(self.watermark_layers) - 1)
            self.layer_listbox.selection_set(new_index)
            self.current_layer_index = new_index  # 更新记住的索引
            self.on_layer_select(None)
        else:
            # 没有图层了，禁用编辑器
            self.current_layer_index = None
            self.blend_mode_combo.config(state='disabled')
            self.opacity_entry.config(state='disabled')
            self.opacity_slider.config(state='disabled')

        self.save_config()

    def move_layer(self, direction):
        """移动图层位置 (-1向上, 1向下)"""
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "请先选择一个图层！")
            return

        index = selection[0]
        new_index = index + direction

        if 0 <= new_index < len(self.watermark_layers):
            self.watermark_layers[index], self.watermark_layers[new_index] = \
                self.watermark_layers[new_index], self.watermark_layers[index]
            self.update_layer_listbox()
            self.layer_listbox.selection_set(new_index)
            self.current_layer_index = new_index  # 更新记住的索引
            # 触发选中事件更新编辑面板
            self.on_layer_select(None)
            self.save_config()

    def toggle_layer_visibility(self):
        """切换图层可见性（类似 Photoshop 的眼睛图标）"""
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "请先选择一个图层！")
            return

        index = selection[0]
        layer = self.watermark_layers[index]

        # 切换可见性
        layer.visible = not layer.visible

        # 更新列表显示（保持选中状态）
        self.update_layer_listbox_silent(selected_index=index)

        # 保存配置
        self.save_config()

        # 提示用户
        status = "可见" if layer.visible else "隐藏"
        print(f"图层 [{index+1}] {layer.name} 已设置为{status}")

    def update_layer_listbox(self):
        """更新图层列表显示"""
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.watermark_layers):
            # 自定义显示格式，保持 emoji
            visibility = "👁️" if layer.visible else "🚫"
            display_text = f"[{i+1}] {visibility} {layer.name} ({layer.blend_mode}, {layer.opacity}%)"
            self.layer_listbox.insert(tk.END, display_text)

    def update_layer_listbox_silent(self, selected_index=None):
        """更新图层列表显示（不触发选中事件）

        Args:
            selected_index: 需要保持选中的图层索引，如果为 None 则不保持选中
        """
        # 暂时解绑选中事件
        self.layer_listbox.unbind('<<ListboxSelect>>')

        # 更新列表
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.watermark_layers):
            # 自定义显示格式，保持 emoji
            visibility = "👁️" if layer.visible else "🚫"
            display_text = f"[{i+1}] {visibility} {layer.name} ({layer.blend_mode}, {layer.opacity}%)"
            self.layer_listbox.insert(tk.END, display_text)

        # 恢复选中状态
        if selected_index is not None and 0 <= selected_index < len(self.watermark_layers):
            self.layer_listbox.selection_set(selected_index)
            self.layer_listbox.see(selected_index)

        # 重新绑定选中事件
        self.layer_listbox.bind('<<ListboxSelect>>', self.on_layer_select)

    def apply_multilayer_watermark(self, image):
        """应用多图层水印 - 使用 WatermarkEngine"""
        # 创建进度回调函数（适配 Tkinter）
        def update_progress(progress):
            self.root.after(0, lambda: self.progress_var.set(progress))

        # 使用 WatermarkEngine 处理
        return WatermarkEngine.apply_multilayer_watermark(
            image,
            self.watermark_layers,
            self.stretch_var.get(),
            update_progress
        )

    def apply_watermark_threaded(self):
        """在线程中处理水印"""
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showwarning("Processing", "请等待当前处理完成！")
            return

        self.processing_thread = threading.Thread(target=self.apply_watermark)
        self.processing_thread.daemon = True
        self.processing_thread.start()

    def apply_watermark(self):
        """应用水印主方法"""
        if not self.images:
            messagebox.showerror("Error", "请先上传图片！")
            return

        if not self.watermark_layers:
            messagebox.showerror("Error", "请先添加至少一个水印图层！")
            return

        if not self.save_directory:
            if self.last_used_directory:
                self.save_directory = self.last_used_directory
                self.update_save_dir_label()
            else:
                messagebox.showerror("Error", "请选择保存目录！")
                return

        # 更新UI
        self.apply_btn.config(state='disabled', text='Processing...')
        self.progress_var.set(0)

        start_time = time.time()

        try:
            total_images = len(self.images)
            for i, image in enumerate(self.images):
                # 更新状态
                self.root.after(0, lambda i=i: self.status_label.config(
                    text=f"Processing image {i+1}/{total_images}: {os.path.basename(self.image_paths[i])}"))

                # 处理图片
                output = self.apply_multilayer_watermark(image)

                # 应用文本标注
                if self.text_label_config.enabled:
                    filename = os.path.basename(self.image_paths[i])
                    output = draw_text_label(output, filename, self.text_label_config, index=i+1)

                # 转换为RGB并保存为JPG（保持画质）
                if output.mode == 'RGBA':
                    # 创建白色背景
                    rgb_image = Image.new('RGB', output.size, (255, 255, 255))
                    rgb_image.paste(output, mask=output.split()[3])  # 使用alpha通道作为mask
                    output = rgb_image

                original_filename = os.path.basename(self.image_paths[i])
                filename_without_ext = os.path.splitext(original_filename)[0]
                output_filename = f"{filename_without_ext}_multilayer.jpg"
                output_path = os.path.join(self.save_directory, output_filename)

                # 保存为高质量JPG
                output.save(output_path, 'JPEG', quality=95, optimize=True)

                # 更新进度
                progress = 50 + ((i + 1) / total_images) * 50
                self.root.after(0, lambda p=progress: self.progress_var.set(p))

            # 完成
            end_time = time.time()
            processing_time = end_time - start_time

            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ 完成! 处理{total_images}张图片，耗时{processing_time:.2f}秒"))

            messagebox.showinfo("完成", f"成功处理{total_images}张图片！\n耗时: {processing_time:.2f}秒\n输出格式: JPG (质量95)")

        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"❌ 错误: {str(e)}"))
            messagebox.showerror("错误", f"处理失败: {str(e)}")

        finally:
            # 恢复UI
            self.root.after(0, lambda: self.apply_btn.config(state='normal', text='🚀 Apply Multi-Layer Watermark'))

    # 配置和事件处理方法
    def save_config(self):
        """使用 WatermarkConfig 保存配置"""
        # 更新 config 对象的属性
        self.config.last_used_directory = self.last_used_directory
        self.config.save_directory = self.save_directory
        self.config.last_watermark_directory = self.last_watermark_directory
        self.config.last_images_directory = self.last_images_directory
        self.config.last_images_files = getattr(self, 'last_images_files', [])

        # 保存配置
        stretch = self.stretch_var.get() if self.stretch_var else False
        self.config.save(
            self.watermark_layers,
            self.text_label_config,
            stretch
        )

    # 事件处理方法
    def on_stretch_change(self):
        self.save_config()

    def on_label_enabled_change(self):
        """标注启用状态改变"""
        self.text_label_config.enabled = self.label_enabled_var.get()
        self.save_config()

    def on_label_type_change(self, event):
        """标注类型改变"""
        self.text_label_config.label_type = self.label_type_var.get()
        self.save_config()

    def on_label_position_change(self, event):
        """标注位置改变"""
        self.text_label_config.position = self.label_position_var.get()
        self.save_config()
        print(f"📍 位置已更改: {self.text_label_config.position}")

    def on_label_orientation_change(self, event):
        """标注方向改变"""
        self.text_label_config.orientation = self.label_orientation_var.get()
        self.save_config()
        print(f"↔️ 方向已更改: {self.text_label_config.orientation}")

    def on_label_font_change(self, event):
        """标注字体改变"""
        font_name = self.label_font_var.get()
        if font_name == '(Auto)':
            self.text_label_config.font_name = None
        else:
            self.text_label_config.font_name = font_name
        self.save_config()
        print(f"🎨 字体已更改: {self.text_label_config.font_name or 'Auto'}")

    def on_label_font_size_change(self, value):
        """标注字体大小改变（百分比）"""
        self.text_label_config.font_size = round(float(value), 1)
        self.save_config()

    def auto_load_last_files(self):
        """自动加载文件"""
        try:
            if self.last_images_files:
                valid_files = [f for f in self.last_images_files if os.path.exists(f)]
                if valid_files:
                    self.image_paths = valid_files
                    self.images = [Image.open(file_path) for file_path in valid_files]
                    print(f"🖼️ 自动加载图片: {len(valid_files)}张")

            # 更新图层列表显示
            if self.watermark_layers:
                self.update_layer_listbox()
                print(f"🎨 自动加载图层: {len(self.watermark_layers)}个")
        except Exception as e:
            print(f"⚠️ 自动加载出错: {e}")

    def upload_images(self):
        """上传图片"""
        self.root.lift()
        initial_dir = self.last_images_directory if self.last_images_directory else "/"
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            initialdir=initial_dir,
            parent=self.root
        )
        if file_paths:
            self.image_paths = file_paths
            self.images = [Image.open(file_path) for file_path in file_paths]
            self.last_images_directory = os.path.dirname(file_paths[0])
            self.last_used_directory = self.last_images_directory
            self.last_images_files = list(file_paths)
            if not self.save_directory:
                self.save_directory = self.last_used_directory
            self.update_save_dir_label()
            self.save_config()

    def select_save_directory(self):
        """选择保存目录"""
        self.root.lift()
        initial_dir = self.last_used_directory if self.last_used_directory else "/"
        directory = filedialog.askdirectory(initialdir=initial_dir, parent=self.root)
        if directory:
            self.save_directory = directory
            self.last_used_directory = directory
            self.update_save_dir_label()
            self.save_config()

    def update_save_dir_label(self):
        """更新保存目录标签"""
        if self.save_dir_label:
            text = self.save_directory if self.save_directory else "No directory selected"
            self.save_dir_label.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiLayerWatermarkApp(root)
    root.mainloop()
