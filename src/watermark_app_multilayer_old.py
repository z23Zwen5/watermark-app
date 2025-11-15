import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import os
import json
import numpy as np
from math import sqrt
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import colorsys

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
        self.root.minsize(600, 800)

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
        self.smart_color_var = None
        self.sensitivity_slider = None
        self.algorithm_var = None
        self.performance_var = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.layer_listbox = None

        # 性能优化相关
        self.color_cache = {}
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

        # Smart algorithm section
        self.create_smart_section(main_container)

        # Performance section
        self.create_performance_section(main_container)

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

        # Layer list
        list_frame = tk.Frame(layer_frame, bg='#FAFAFA')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.layer_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       font=('Courier', 9), height=8, bg='#FFFFFF',
                                       selectmode=tk.SINGLE)
        self.layer_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.layer_listbox.yview)

        # Layer control buttons
        btn_frame = tk.Frame(layer_frame, bg='#FAFAFA')
        btn_frame.pack(fill=tk.X)

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
        tk.Button(btn_frame, text="✎ Edit Layer", command=self.edit_selected_layer,
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="× Remove", command=self.remove_selected_layer,
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="↑ Up", command=lambda: self.move_layer(-1),
                 **button_style).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="↓ Down", command=lambda: self.move_layer(1),
                 **button_style).pack(side=tk.LEFT)

    def create_settings_section(self, parent):
        """创建基础设置区域"""
        settings_frame = tk.LabelFrame(parent, text="⚙️ Basic Settings", font=('Helvetica', 11, 'bold'),
                                     fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        # Stretch option
        self.stretch_var = tk.BooleanVar(value=getattr(self, 'last_stretch', False))
        stretch_cb = ttk.Checkbutton(settings_frame, text="Stretch watermark to fit image",
                                   variable=self.stretch_var, command=self.on_stretch_change)
        stretch_cb.pack(pady=5)

    def create_smart_section(self, parent):
        """创建智能算法区域"""
        smart_frame = tk.LabelFrame(parent, text="🧠 Smart Color Adaptation",
                                  font=('Helvetica', 11, 'bold'), fg='#0095F6',
                                  bg='#FAFAFA', padx=10, pady=10)
        smart_frame.pack(fill=tk.X, pady=(0, 15))

        # Enable smart color
        self.smart_color_var = tk.BooleanVar(value=getattr(self, 'last_smart_color', True))
        smart_cb = ttk.Checkbutton(smart_frame, text="🎯 Enable intelligent color adaptation",
                                 variable=self.smart_color_var, command=self.on_smart_color_change)
        smart_cb.pack(pady=(0, 10))

        # Sensitivity
        sens_frame = tk.Frame(smart_frame, bg='#FAFAFA')
        sens_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(sens_frame, text="Color Similarity Sensitivity (Lower = More Sensitive)",
                font=('Helvetica', 10), fg='#262626', bg='#FAFAFA').pack(anchor='w')

        self.sensitivity_slider = ttk.Scale(sens_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                          command=self.on_sensitivity_change)
        self.sensitivity_slider.set(getattr(self, 'last_sensitivity', 30))
        self.sensitivity_slider.pack(fill=tk.X, pady=(5, 0))

        # Algorithm selection
        alg_frame = tk.Frame(smart_frame, bg='#FAFAFA')
        alg_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(alg_frame, text="Color Adaptation Algorithm:", font=('Helvetica', 10),
                fg='#262626', bg='#FAFAFA').pack(anchor='w')

        self.algorithm_var = tk.StringVar(value=getattr(self, 'last_algorithm', 'enhanced'))
        alg_options = [
            ('Enhanced (Recommended)', 'enhanced'),
            ('Classic', 'classic'),
            ('Gentle', 'gentle')
        ]

        for text, value in alg_options:
            ttk.Radiobutton(alg_frame, text=text, variable=self.algorithm_var,
                          value=value, command=self.on_algorithm_change).pack(anchor='w')

    def create_performance_section(self, parent):
        """创建性能优化区域"""
        perf_frame = tk.LabelFrame(parent, text="⚡ Performance Optimization",
                                 font=('Helvetica', 11, 'bold'), fg='#0095F6',
                                 bg='#FAFAFA', padx=10, pady=10)
        perf_frame.pack(fill=tk.X, pady=(0, 15))

        self.performance_var = tk.StringVar(value=getattr(self, 'last_performance', 'balanced'))
        perf_options = [
            ('🏃‍♂️ Speed Priority - Faster processing, good quality', 'speed'),
            ('⚖️ Balanced - Good speed and quality (Recommended)', 'balanced'),
            ('🎨 Quality Priority - Best quality, slower processing', 'quality')
        ]

        for text, value in perf_options:
            ttk.Radiobutton(perf_frame, text=text, variable=self.performance_var,
                          value=value, command=self.on_performance_change).pack(anchor='w', pady=2)

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
            # 创建新图层
            layer = WatermarkLayer(file_path)
            self.watermark_layers.append(layer)
            self.last_watermark_directory = os.path.dirname(file_path)

            # 弹出编辑窗口设置混合模式和不透明度
            self.edit_layer_dialog(layer)

            # 更新列表显示
            self.update_layer_listbox()
            self.save_config()

    def edit_selected_layer(self):
        """编辑选中的图层"""
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "请先选择一个图层！")
            return

        index = selection[0]
        layer = self.watermark_layers[index]
        self.edit_layer_dialog(layer)
        self.update_layer_listbox()
        self.save_config()

    def edit_layer_dialog(self, layer):
        """图层编辑对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Layer: {layer.name}")
        dialog.configure(bg='#FAFAFA')
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # 图层名称
        tk.Label(dialog, text=f"Layer: {layer.name}", font=('Helvetica', 12, 'bold'),
                bg='#FAFAFA', fg='#262626').pack(pady=(20, 10))

        # 混合模式
        tk.Label(dialog, text="Blend Mode:", font=('Helvetica', 10),
                bg='#FAFAFA', fg='#262626').pack(anchor='w', padx=20, pady=(10, 5))

        blend_var = tk.StringVar(value=layer.blend_mode)
        blend_frame = tk.Frame(dialog, bg='#FAFAFA')
        blend_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        blend_modes = [
            ('Normal', 'normal'),
            ('Overlay', 'overlay'),
            ('Screen', 'screen'),
            ('Soft Light', 'soft_light')
        ]

        for text, value in blend_modes:
            ttk.Radiobutton(blend_frame, text=text, variable=blend_var,
                          value=value).pack(anchor='w')

        # 不透明度
        tk.Label(dialog, text="Opacity:", font=('Helvetica', 10),
                bg='#FAFAFA', fg='#262626').pack(anchor='w', padx=20, pady=(10, 5))

        opacity_frame = tk.Frame(dialog, bg='#FAFAFA')
        opacity_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        opacity_var = tk.DoubleVar(value=layer.opacity)
        opacity_label = tk.Label(opacity_frame, text=f"{int(layer.opacity)}%",
                                font=('Helvetica', 10), bg='#FAFAFA', fg='#262626')
        opacity_label.pack(anchor='e')

        def on_opacity_change(val):
            opacity_label.config(text=f"{int(float(val))}%")

        opacity_slider = ttk.Scale(opacity_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                  variable=opacity_var, command=on_opacity_change)
        opacity_slider.pack(fill=tk.X)

        # 确认按钮
        def save_changes():
            layer.blend_mode = blend_var.get()
            layer.opacity = opacity_var.get()
            dialog.destroy()

        tk.Button(dialog, text="Save", font=('Helvetica', 12, 'bold'),
                 bg='#0095F6', fg='white', command=save_changes,
                 padx=30, pady=10).pack(pady=20)

    def remove_selected_layer(self):
        """删除选中的图层"""
        selection = self.layer_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "请先选择一个图层！")
            return

        index = selection[0]
        del self.watermark_layers[index]
        self.update_layer_listbox()
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
            self.save_config()

    def update_layer_listbox(self):
        """更新图层列表显示"""
        self.layer_listbox.delete(0, tk.END)
        for i, layer in enumerate(self.watermark_layers):
            self.layer_listbox.insert(tk.END, f"[{i+1}] {layer}")

    # 混合模式算法
    def blend_normal(self, base, blend, opacity):
        """Normal混合模式"""
        return blend * opacity + base * (1 - opacity)

    def blend_screen(self, base, blend, opacity):
        """Screen混合模式: 1 - (1-base)*(1-blend)"""
        result = 1.0 - (1.0 - base) * (1.0 - blend)
        return result * opacity + base * (1 - opacity)

    def blend_overlay(self, base, blend, opacity):
        """Overlay混合模式"""
        result = np.where(base < 0.5,
                         2 * base * blend,
                         1.0 - 2 * (1.0 - base) * (1.0 - blend))
        return result * opacity + base * (1 - opacity)

    def blend_soft_light(self, base, blend, opacity):
        """Soft Light混合模式"""
        result = np.where(blend < 0.5,
                         2 * base * blend + base * base * (1 - 2 * blend),
                         2 * base * (1 - blend) + np.sqrt(base) * (2 * blend - 1))
        return result * opacity + base * (1 - opacity)

    def apply_blend_mode(self, base_array, layer_array, blend_mode, opacity):
        """应用混合模式"""
        # 归一化到 0-1
        base = base_array.astype(np.float32) / 255.0
        blend = layer_array.astype(np.float32) / 255.0
        opacity_factor = opacity / 100.0

        # 分离RGB和Alpha
        base_rgb = base[:, :, :3]
        base_alpha = base[:, :, 3:4]
        blend_rgb = blend[:, :, :3]
        blend_alpha = blend[:, :, 3:4]

        # 应用混合模式
        if blend_mode == 'normal':
            result_rgb = self.blend_normal(base_rgb, blend_rgb, opacity_factor)
        elif blend_mode == 'screen':
            result_rgb = self.blend_screen(base_rgb, blend_rgb, opacity_factor)
        elif blend_mode == 'overlay':
            result_rgb = self.blend_overlay(base_rgb, blend_rgb, opacity_factor)
        elif blend_mode == 'soft_light':
            result_rgb = self.blend_soft_light(base_rgb, blend_rgb, opacity_factor)
        else:
            result_rgb = base_rgb

        # 考虑图层alpha通道
        mask = blend_alpha * opacity_factor
        result_rgb = result_rgb * mask + base_rgb * (1 - mask)
        result_alpha = np.maximum(base_alpha, blend_alpha * opacity_factor)

        # 合并RGBA
        result = np.concatenate([result_rgb, result_alpha], axis=2)
        return (result * 255).astype(np.uint8)

    # 颜色计算优化方法
    def calculate_color_distance_optimized(self, color1, color2):
        """优化的颜色距离计算"""
        cache_key = (tuple(color1[:3]), tuple(color2[:3]))
        if cache_key in self.color_cache:
            return self.color_cache[cache_key]

        distance = sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1[:3], color2[:3])))
        self.color_cache[cache_key] = distance
        return distance

    def get_contrasting_color_enhanced(self, color, algorithm='enhanced'):
        """增强的对比色算法"""
        r, g, b = color[:3]

        if algorithm == 'enhanced':
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

            if v < 0.5:
                new_v = min(1.0, v + 0.6)
                new_s = max(0.1, s * 0.8)
            else:
                new_v = max(0.0, v - 0.6)
                new_s = min(1.0, s * 1.2)

            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, new_s, new_v)
            return (int(new_r * 255), int(new_g * 255), int(new_b * 255))

        elif algorithm == 'gentle':
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < 128:
                factor = 0.5
                return (min(255, int(r + (255 - r) * factor)),
                       min(255, int(g + (255 - g) * factor)),
                       min(255, int(b + (255 - b) * factor)))
            else:
                factor = 0.5
                return (max(0, int(r * factor)),
                       max(0, int(g * factor)),
                       max(0, int(b * factor)))

        else:  # classic
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < 128:
                return (min(255, r + int((255 - r) * 0.8)),
                       min(255, g + int((255 - g) * 0.8)),
                       min(255, b + int((255 - b) * 0.8)))
            else:
                return (max(0, int(r * 0.2)),
                       max(0, int(g * 0.2)),
                       max(0, int(b * 0.2)))

    def apply_multilayer_watermark(self, image):
        """应用多图层水印"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        result = np.array(image)
        stretch = self.stretch_var.get()
        smart_color = self.smart_color_var.get()
        sensitivity = self.sensitivity_slider.get()
        algorithm = self.algorithm_var.get()

        # 逐层应用水印
        for layer_idx, layer in enumerate(self.watermark_layers):
            # 计算水印尺寸
            if stretch:
                new_width, new_height = image.width, image.height
            else:
                watermark_ratio = layer.image.width / layer.image.height
                if image.width / image.height > watermark_ratio:
                    new_width = image.width
                    new_height = int(new_width / watermark_ratio)
                else:
                    new_height = image.height
                    new_width = int(new_height * watermark_ratio)

            # 缩放水印
            resized_watermark = layer.image.resize((new_width, new_height), Image.LANCZOS)

            # 创建与图片同尺寸的画布
            layer_canvas = Image.new('RGBA', image.size, (0, 0, 0, 0))
            position = ((image.width - new_width) // 2, (image.height - new_height) // 2)

            # 智能颜色适应
            if smart_color:
                smart_watermark = Image.new('RGBA', resized_watermark.size, (0, 0, 0, 0))

                for x in range(resized_watermark.width):
                    for y in range(resized_watermark.height):
                        watermark_pixel = resized_watermark.getpixel((x, y))
                        r, g, b, a = watermark_pixel

                        if a > 0:
                            bg_x = position[0] + x
                            bg_y = position[1] + y

                            if 0 <= bg_x < image.width and 0 <= bg_y < image.height:
                                bg_color = tuple(result[bg_y, bg_x])

                                distance = self.calculate_color_distance_optimized(watermark_pixel, bg_color)
                                if distance < sensitivity:
                                    contrasting_color = self.get_contrasting_color_enhanced(bg_color, algorithm)
                                    r, g, b = contrasting_color

                        smart_watermark.putpixel((x, y), (r, g, b, a))

                layer_canvas.paste(smart_watermark, position)
            else:
                layer_canvas.paste(resized_watermark, position)

            # 应用混合模式
            layer_array = np.array(layer_canvas)
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

        # 清空缓存
        self.color_cache.clear()

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

                # 保存
                if output.mode == 'RGBA':
                    output = output.convert('RGB')

                original_filename = os.path.basename(self.image_paths[i])
                filename_without_ext = os.path.splitext(original_filename)[0]
                output_filename = f"{filename_without_ext}_multilayer.png"
                output_path = os.path.join(self.save_directory, output_filename)

                output.save(output_path)

                # 更新进度
                progress = 50 + ((i + 1) / total_images) * 50
                self.root.after(0, lambda p=progress: self.progress_var.set(p))

            # 完成
            end_time = time.time()
            processing_time = end_time - start_time

            self.root.after(0, lambda: self.status_label.config(
                text=f"✅ 完成! 处理{total_images}张图片，耗时{processing_time:.2f}秒"))

            messagebox.showinfo("完成", f"成功处理{total_images}张图片！\n耗时: {processing_time:.2f}秒")

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
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
                    self.last_stretch = config.get('last_stretch', False)
                    self.last_smart_color = config.get('last_smart_color', True)
                    self.last_sensitivity = config.get('last_sensitivity', 30)
                    self.last_algorithm = config.get('last_algorithm', 'enhanced')
                    self.last_performance = config.get('last_performance', 'balanced')
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
        self.last_smart_color = True
        self.last_sensitivity = 30
        self.last_algorithm = 'enhanced'
        self.last_performance = 'balanced'
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
                'last_smart_color': self.smart_color_var.get() if self.smart_color_var else self.last_smart_color,
                'last_sensitivity': self.sensitivity_slider.get() if self.sensitivity_slider else self.last_sensitivity,
                'last_algorithm': self.algorithm_var.get() if self.algorithm_var else self.last_algorithm,
                'last_performance': self.performance_var.get() if self.performance_var else self.last_performance,
                'last_images_files': self.last_images_files,
                'layers': layers_info
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存配置出错: {e}")

    # 事件处理方法
    def on_stretch_change(self):
        self.save_config()

    def on_smart_color_change(self):
        self.save_config()

    def on_sensitivity_change(self, value):
        pass

    def on_algorithm_change(self):
        self.save_config()

    def on_performance_change(self):
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
