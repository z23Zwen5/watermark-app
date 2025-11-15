import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import json
import numpy as np
import threading
import time

class WatermarkLayer:
    """水印图层类"""
    def __init__(self, image_path, opacity=100, blend_mode='normal'):
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGBA")
        self.opacity = opacity  # 0-100
        self.blend_mode = blend_mode  # normal, overlay, screen, soft_light
        self.name = os.path.basename(image_path)

    def __str__(self):
        return f"{self.name} ({self.blend_mode}, {self.opacity}%)"

class MultiLayerWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Layer Watermark App v1.5")
        self.root.configure(bg='#FAFAFA')

        # Set minimum window size
        self.root.minsize(550, 650)

        # Initialize path memory
        self.config_file = "multilayer_watermark_config.json"

        # Initialize variables
        self.images = []
        self.image_paths = []
        self.watermark_layers = []  # 多个水印图层
        self.save_directory = None
        self.last_used_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None

        # Initialize UI variables
        self.stretch_var = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.layer_listbox = None
        self.blend_mode_var = None
        self.blend_mode_combo = None
        self.opacity_entry = None

        # 处理线程
        self.processing_thread = None

        # Load configuration
        self.load_config()

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
        opacity_row.pack(fill=tk.X)

        tk.Label(opacity_row, text="Opacity (%):", font=('Helvetica', 9),
                fg='#262626', bg='#FAFAFA', width=12, anchor='w').pack(side=tk.LEFT)

        # Opacity entry with validation
        vcmd = (self.root.register(self.validate_opacity), '%P')
        self.opacity_entry = tk.Entry(opacity_row, width=8, validate='key', validatecommand=vcmd)
        self.opacity_entry.insert(0, '100')
        self.opacity_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.opacity_entry.bind('<KeyRelease>', self.on_opacity_entry_change)
        self.opacity_entry.bind('<FocusOut>', self.on_opacity_entry_change)

        tk.Label(opacity_row, text="(0-100)", font=('Helvetica', 8),
                fg='#999999', bg='#FAFAFA').pack(side=tk.LEFT)

        # 默认禁用编辑器
        self.blend_mode_combo.config(state='disabled')
        self.opacity_entry.config(state='disabled')

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
            self.blend_mode_combo.config(state='disabled')
            self.opacity_entry.config(state='disabled')
            return

        # 有选中，启用编辑器并显示当前图层属性
        index = selection[0]
        layer = self.watermark_layers[index]

        self.blend_mode_combo.config(state='readonly')
        self.opacity_entry.config(state='normal')

        # 更新显示值
        self.blend_mode_var.set(layer.blend_mode)
        self.opacity_entry.delete(0, tk.END)
        self.opacity_entry.insert(0, str(int(layer.opacity)))

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
        selection = self.layer_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        layer = self.watermark_layers[index]
        layer.blend_mode = self.blend_mode_var.get()

        # 更新列表显示
        self.update_layer_listbox()
        # 保持选中状态
        self.layer_listbox.selection_set(index)
        self.save_config()

    def on_opacity_entry_change(self, event):
        """不透明度输入改变时"""
        selection = self.layer_listbox.curselection()
        if not selection:
            return

        value = self.opacity_entry.get()
        if value == "":
            return

        try:
            opacity = int(value)
            if 0 <= opacity <= 100:
                index = selection[0]
                layer = self.watermark_layers[index]
                layer.opacity = opacity

                # 更新列表显示
                self.update_layer_listbox()
                # 保持选中状态
                self.layer_listbox.selection_set(index)
                self.save_config()
        except ValueError:
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
            self.on_layer_select(None)
        else:
            # 没有图层了，禁用编辑器
            self.blend_mode_combo.config(state='disabled')
            self.opacity_entry.config(state='disabled')

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
            # 触发选中事件更新编辑面板
            self.on_layer_select(None)
            self.save_config()

    def update_layer_listbox(self):
        """更新图层列表显示"""
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.watermark_layers):
            self.layer_listbox.insert(tk.END, f"[{i+1}] {layer}")

    # 混合模式算法（优化版 - 所有逻辑整合在 apply_blend_mode 中）
    def apply_blend_mode(self, base_array, layer_array, blend_mode, opacity):
        """应用混合模式 - 优化版"""
        opacity_factor = opacity / 100.0

        # 只处理有alpha的区域，跳过完全透明的区域
        blend_alpha = layer_array[:, :, 3].astype(np.float32) / 255.0
        mask = blend_alpha * opacity_factor

        # 如果整个图层都是透明的，直接返回
        if np.max(mask) < 0.001:
            return base_array

        # 只在有alpha的地方进行混合计算（优化性能）
        has_alpha = mask > 0.001
        if not np.any(has_alpha):
            return base_array

        # 归一化到 0-1（只转换需要的通道）
        base_rgb = base_array[:, :, :3].astype(np.float32) / 255.0
        blend_rgb = layer_array[:, :, :3].astype(np.float32) / 255.0

        # 应用混合模式
        if blend_mode == 'normal':
            result_rgb = blend_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        elif blend_mode == 'screen':
            result_rgb = 1.0 - (1.0 - base_rgb) * (1.0 - blend_rgb)
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        elif blend_mode == 'overlay':
            result_rgb = np.where(base_rgb < 0.5,
                                 2 * base_rgb * blend_rgb,
                                 1.0 - 2 * (1.0 - base_rgb) * (1.0 - blend_rgb))
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        elif blend_mode == 'soft_light':
            result_rgb = np.where(blend_rgb < 0.5,
                                 2 * base_rgb * blend_rgb + base_rgb * base_rgb * (1 - 2 * blend_rgb),
                                 2 * base_rgb * (1 - blend_rgb) + np.sqrt(np.maximum(base_rgb, 0)) * (2 * blend_rgb - 1))
            result_rgb = result_rgb * opacity_factor + base_rgb * (1 - opacity_factor)
        else:
            result_rgb = base_rgb

        # 应用 alpha mask（只在有alpha的地方混合）
        mask_3d = mask[:, :, np.newaxis]
        result_rgb = result_rgb * mask_3d + base_rgb * (1 - mask_3d)

        # 合并RGB（直接在原数组上操作，避免重新分配内存）
        result = base_array.copy()
        result[:, :, :3] = (np.clip(result_rgb, 0, 1) * 255).astype(np.uint8)

        return result

    def apply_multilayer_watermark(self, image):
        """应用多图层水印 - 优化版"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        result = np.array(image, dtype=np.uint8)
        stretch = self.stretch_var.get()
        img_width, img_height = image.size

        # 逐层应用水印
        for layer_idx, layer in enumerate(self.watermark_layers):
            # 计算水印尺寸（缓存计算结果）
            if stretch:
                new_width, new_height = img_width, img_height
            else:
                watermark_ratio = layer.image.width / layer.image.height
                img_ratio = img_width / img_height
                if img_ratio > watermark_ratio:
                    new_width = img_width
                    new_height = int(new_width / watermark_ratio)
                else:
                    new_height = img_height
                    new_width = int(new_height * watermark_ratio)

            # 缩放水印（使用更快的 BILINEAR 如果图层不透明度低）
            if layer.opacity < 50:
                resized_watermark = layer.image.resize((new_width, new_height), Image.BILINEAR)
            else:
                resized_watermark = layer.image.resize((new_width, new_height), Image.LANCZOS)

            # 优化：直接创建 numpy 数组而不是 PIL Image
            position = ((img_width - new_width) // 2, (img_height - new_height) // 2)

            # 创建图层数组（只在需要的区域）
            layer_array = np.zeros((img_height, img_width, 4), dtype=np.uint8)
            watermark_array = np.array(resized_watermark)

            # 只复制水印到对应位置（避免创建完整画布）
            y1, y2 = position[1], position[1] + new_height
            x1, x2 = position[0], position[0] + new_width
            layer_array[y1:y2, x1:x2] = watermark_array

            # 应用混合模式
            result = self.apply_blend_mode(result, layer_array, layer.blend_mode, layer.opacity)

            # 更新进度
            progress = ((layer_idx + 1) / len(self.watermark_layers)) * 50
            self.root.after(0, lambda p=progress: self.progress_var.set(p))

        return Image.fromarray(result, 'RGBA')

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
    def load_config(self):
        """加载配置"""
        try:
            config_path = os.path.join("configs", self.config_file)
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
                    self.last_stretch = config.get('last_stretch', False)
                    self.last_images_files = config.get('last_images_files', [])

                    # 加载图层信息
                    layers_info = config.get('layers', [])
                    for layer_info in layers_info:
                        if os.path.exists(layer_info['path']):
                            layer = WatermarkLayer(
                                layer_info['path'],
                                layer_info.get('opacity', 100),
                                layer_info.get('blend_mode', 'normal')
                            )
                            self.watermark_layers.append(layer)
            else:
                self.set_default_config()
        except Exception as e:
            print(f"❌ 加载配置出错: {e}")
            self.set_default_config()

    def set_default_config(self):
        """设置默认配置"""
        self.last_used_directory = None
        self.save_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None
        self.last_stretch = False
        self.last_images_files = []

    def save_config(self):
        """保存配置"""
        try:
            # 保存图层信息
            layers_info = []
            for layer in self.watermark_layers:
                layers_info.append({
                    'path': layer.image_path,
                    'opacity': layer.opacity,
                    'blend_mode': layer.blend_mode
                })

            config = {
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory,
                'last_stretch': self.stretch_var.get() if self.stretch_var else self.last_stretch,
                'last_images_files': self.last_images_files,
                'layers': layers_info
            }

            # 确保configs目录存在
            os.makedirs("configs", exist_ok=True)
            config_path = os.path.join("configs", self.config_file)

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存配置出错: {e}")

    # 事件处理方法
    def on_stretch_change(self):
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
