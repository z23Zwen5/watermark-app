import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os
import json
import numpy as np
from math import sqrt
import threading
import time
import colorsys
from scipy import ndimage

class AlphaProtectedWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Watermark App v1.6 (Vectorized)")
        self.root.configure(bg='#FAFAFA')
        
        # Set minimum window size
        self.root.minsize(500, 750)
        
        # Initialize path memory
        self.config_file = "alpha_protected_watermark_config.json"
        
        # Initialize variables
        self.images = []
        self.watermark = None
        self.image_paths = []
        self.save_directory = None
        self.last_used_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None
        
        # Initialize UI variables
        self.opacity_slider = None
        self.stretch_var = None
        self.smart_color_var = None
        self.sensitivity_slider = None
        self.algorithm_var = None
        self.performance_var = None
        self.smoothing_var = None
        self.smoothing_radius_slider = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        
        # 性能优化相关
        self.color_cache = {}
        self.processing_thread = None
        
        # Debounce timer
        self.opacity_save_timer = None
        
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
            text="Smart Watermark App v1.6",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="⚡ Vectorized Processing & Alpha Protection",
            font=('Helvetica', 12),
            fg='#0095F6',
            bg='#FAFAFA'
        )
        subtitle_label.pack()

        # File upload section
        self.create_upload_section(main_container)
        
        # Settings section
        self.create_settings_section(main_container)
        
        # Smart algorithm section
        self.create_smart_section(main_container)
        
        # Alpha protection section
        self.create_alpha_section(main_container)
        
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
        
        self.upload_watermark_btn = tk.Button(btn_frame, text="Upload Watermark", 
                                            command=self.upload_watermark, **button_style)
        self.upload_watermark_btn.pack(side=tk.LEFT)

    def create_settings_section(self, parent):
        """创建基础设置区域"""
        settings_frame = tk.LabelFrame(parent, text="⚙️ Basic Settings", font=('Helvetica', 11, 'bold'),
                                     fg='#0095F6', bg='#FAFAFA', padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Opacity
        opacity_frame = tk.Frame(settings_frame, bg='#FAFAFA')
        opacity_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(opacity_frame, text="Opacity", font=('Helvetica', 10), 
                fg='#262626', bg='#FAFAFA').pack(anchor='w')
        
        self.opacity_slider = ttk.Scale(opacity_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.on_opacity_change)
        self.opacity_slider.set(getattr(self, 'last_opacity', 50))
        self.opacity_slider.pack(fill=tk.X, pady=(5, 0))
        
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

    def create_alpha_section(self, parent):
        """创建Alpha通道保护区域"""
        alpha_frame = tk.LabelFrame(parent, text="🛡️ Alpha Channel Protection", 
                                  font=('Helvetica', 11, 'bold'), fg='#0095F6',
                                  bg='#FAFAFA', padx=10, pady=10)
        alpha_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Description
        desc_text = ("Alpha Channel Protection automatically protects opaque elements (Alpha=255) "
                    "like logos and icons while applying smart color adaptation to semi-transparent "
                    "patterns and backgrounds.")
        desc_label = tk.Label(alpha_frame, text=desc_text, wraplength=450, justify=tk.LEFT,
                            font=('Helvetica', 9), fg='#666666', bg='#FAFAFA')
        desc_label.pack(pady=(0, 10))
        
        # Enable smoothing
        self.smoothing_var = tk.BooleanVar(value=getattr(self, 'last_smoothing', True))
        smoothing_cb = ttk.Checkbutton(alpha_frame, text="🌊 Enable edge smoothing (reduces pixelation)",
                                     variable=self.smoothing_var, command=self.on_smoothing_change)
        smoothing_cb.pack(pady=(0, 10))
        
        # Smoothing radius
        smooth_frame = tk.Frame(alpha_frame, bg='#FAFAFA')
        smooth_frame.pack(fill=tk.X)
        
        tk.Label(smooth_frame, text="Smoothing Radius (Higher = Smoother)",
                font=('Helvetica', 10), fg='#262626', bg='#FAFAFA').pack(anchor='w')
        
        self.smoothing_radius_slider = ttk.Scale(smooth_frame, from_=0.5, to=5.0, orient=tk.HORIZONTAL,
                                               command=self.on_smoothing_radius_change)
        self.smoothing_radius_slider.set(getattr(self, 'last_smoothing_radius', 1.5))
        self.smoothing_radius_slider.pack(fill=tk.X, pady=(5, 0))

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
        
        self.apply_btn = tk.Button(action_frame, text="🛡️ Apply Alpha Protected Watermark",
                                 command=self.apply_watermark_threaded, **button_style)
        self.apply_btn.pack(fill=tk.X)

    # Alpha protection core methods - 使用向量化版本



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
                    self.last_opacity = config.get('last_opacity', 50)
                    self.last_stretch = config.get('last_stretch', False)
                    self.last_smart_color = config.get('last_smart_color', True)
                    self.last_sensitivity = config.get('last_sensitivity', 30)
                    self.last_algorithm = config.get('last_algorithm', 'enhanced')
                    self.last_performance = config.get('last_performance', 'balanced')
                    self.last_smoothing = config.get('last_smoothing', True)
                    self.last_smoothing_radius = config.get('last_smoothing_radius', 1.5)
                    self.last_watermark_file = config.get('last_watermark_file')
                    self.last_images_files = config.get('last_images_files', [])
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
        self.last_opacity = 50
        self.last_stretch = False
        self.last_smart_color = True
        self.last_sensitivity = 30
        self.last_algorithm = 'enhanced'
        self.last_performance = 'balanced'
        self.last_smoothing = True
        self.last_smoothing_radius = 1.5
        self.last_watermark_file = None
        self.last_images_files = []

    def save_config(self):
        """保存配置"""
        try:
            config = {
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory,
                'last_opacity': self.opacity_slider.get() if self.opacity_slider else self.last_opacity,
                'last_stretch': self.stretch_var.get() if self.stretch_var else self.last_stretch,
                'last_smart_color': self.smart_color_var.get() if self.smart_color_var else self.last_smart_color,
                'last_sensitivity': self.sensitivity_slider.get() if self.sensitivity_slider else self.last_sensitivity,
                'last_algorithm': self.algorithm_var.get() if self.algorithm_var else self.last_algorithm,
                'last_performance': self.performance_var.get() if self.performance_var else self.last_performance,
                'last_smoothing': self.smoothing_var.get() if self.smoothing_var else self.last_smoothing,
                'last_smoothing_radius': self.smoothing_radius_slider.get() if self.smoothing_radius_slider else self.last_smoothing_radius,
                'last_watermark_file': self.last_watermark_file,
                'last_images_files': self.last_images_files
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存配置出错: {e}")

    # 事件处理方法
    def on_opacity_change(self, value):
        if self.opacity_save_timer:
            self.root.after_cancel(self.opacity_save_timer)
        self.opacity_save_timer = self.root.after(1000, self.save_config)

    def on_stretch_change(self):
        self.save_config()

    def on_smart_color_change(self):
        self.save_config()

    def on_sensitivity_change(self, value):
        if self.opacity_save_timer:
            self.root.after_cancel(self.opacity_save_timer)
        self.opacity_save_timer = self.root.after(1000, self.save_config)

    def on_algorithm_change(self):
        self.save_config()

    def on_performance_change(self):
        self.save_config()

    def on_smoothing_change(self):
        self.save_config()

    def on_smoothing_radius_change(self, value):
        if self.opacity_save_timer:
            self.root.after_cancel(self.opacity_save_timer)
        self.opacity_save_timer = self.root.after(1000, self.save_config)

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
        if not self.images or not self.watermark:
            messagebox.showerror("Error", "请先上传图片和水印！")
            return

        if not self.save_directory:
            if self.last_used_directory:
                self.save_directory = self.last_used_directory
                self.update_save_dir_label()
            else:
                messagebox.showerror("Error", "请选择保存目录！")
                return

        # 获取设置
        opacity = self.opacity_slider.get() / 100.0
        stretch = self.stretch_var.get()
        smart_color = self.smart_color_var.get()
        sensitivity = self.sensitivity_slider.get()
        algorithm = self.algorithm_var.get()
        performance_mode = self.performance_var.get()
        enable_smoothing = self.smoothing_var.get()
        smoothing_radius = self.smoothing_radius_slider.get()
        
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
                output = self.apply_alpha_protected_watermark(
                    image, self.watermark, opacity, stretch, smart_color, 
                    sensitivity, algorithm, performance_mode, enable_smoothing, smoothing_radius
                )
                
                # 保存
                if output.mode == 'RGBA':
                    output = output.convert('RGB')
                
                original_filename = os.path.basename(self.image_paths[i])
                filename_without_ext = os.path.splitext(original_filename)[0]
                output_filename = f"{filename_without_ext}_alpha_protected_v15.png"
                output_path = os.path.join(self.save_directory, output_filename)
                
                output.save(output_path)
                
                # 更新进度
                progress = ((i + 1) / total_images) * 100
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
            self.root.after(0, lambda: self.apply_btn.config(state='normal', text='🛡️ Apply Alpha Protected Watermark'))

    def auto_load_last_files(self):
        """自动加载文件"""
        try:
            if self.last_watermark_file and os.path.exists(self.last_watermark_file):
                self.watermark = Image.open(self.last_watermark_file).convert("RGBA")
                print(f"🎨 自动加载水印: {self.last_watermark_file}")
            
            if self.last_images_files:
                valid_files = [f for f in self.last_images_files if os.path.exists(f)]
                if valid_files:
                    self.image_paths = valid_files
                    self.images = [Image.open(file_path) for file_path in valid_files]
                    print(f"🖼️ 自动加载图片: {len(valid_files)}张")
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

    def upload_watermark(self):
        """上传水印"""
        self.root.lift()
        initial_dir = self.last_watermark_directory if self.last_watermark_directory else "/"
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png")],
            initialdir=initial_dir,
            parent=self.root
        )
        if file_path:
            self.watermark = Image.open(file_path).convert("RGBA")
            self.last_watermark_directory = os.path.dirname(file_path)
            self.last_watermark_file = file_path
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

    def calculate_color_distance_vectorized(self, colors1, colors2):
        """向量化计算颜色距离"""
        if len(colors1.shape) == 1:
            colors1 = colors1.reshape(1, -1)
        if len(colors2.shape) == 1:
            colors2 = colors2.reshape(1, -1)
        
        # 确保颜色数组只有RGB通道
        colors1_rgb = colors1[:, :3]
        colors2_rgb = colors2[:, :3]
        
        # 计算欧几里得距离
        diff = colors1_rgb - colors2_rgb
        distances = np.sqrt(np.sum(diff ** 2, axis=1))
        return distances

    def rgb_to_hsv_vectorized(self, rgb):
        """向量化RGB到HSV转换"""
        rgb = rgb.astype(np.float32)
        max_val = np.max(rgb, axis=1)
        min_val = np.min(rgb, axis=1)
        diff = max_val - min_val
        
        # Value
        v = max_val
        
        # Saturation
        s = np.where(max_val != 0, diff / max_val, 0)
        
        # Hue
        h = np.zeros_like(max_val)
        
        # Red is max
        idx = (rgb[:, 0] == max_val) & (diff != 0)
        h[idx] = (60 * ((rgb[idx, 1] - rgb[idx, 2]) / diff[idx]) + 360) % 360
        
        # Green is max
        idx = (rgb[:, 1] == max_val) & (diff != 0)
        h[idx] = (60 * ((rgb[idx, 2] - rgb[idx, 0]) / diff[idx]) + 120) % 360
        
        # Blue is max
        idx = (rgb[:, 2] == max_val) & (diff != 0)
        h[idx] = (60 * ((rgb[idx, 0] - rgb[idx, 1]) / diff[idx]) + 240) % 360
        
        h = h / 360.0  # 归一化到0-1
        
        return np.stack([h, s, v], axis=1)

    def hsv_to_rgb_vectorized(self, hsv):
        """向量化HSV到RGB转换"""
        h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]
        
        c = v * s
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = v - c
        
        rgb = np.zeros((len(h), 3), dtype=np.float32)
        
        # 根据色相区间设置RGB值
        idx = (h >= 0) & (h < 1/6)
        if np.any(idx):
            rgb[idx, 0] = c[idx]
            rgb[idx, 1] = x[idx]
            rgb[idx, 2] = 0
        
        idx = (h >= 1/6) & (h < 2/6)
        if np.any(idx):
            rgb[idx, 0] = x[idx]
            rgb[idx, 1] = c[idx]
            rgb[idx, 2] = 0
        
        idx = (h >= 2/6) & (h < 3/6)
        if np.any(idx):
            rgb[idx, 0] = 0
            rgb[idx, 1] = c[idx]
            rgb[idx, 2] = x[idx]
        
        idx = (h >= 3/6) & (h < 4/6)
        if np.any(idx):
            rgb[idx, 0] = 0
            rgb[idx, 1] = x[idx]
            rgb[idx, 2] = c[idx]
        
        idx = (h >= 4/6) & (h < 5/6)
        if np.any(idx):
            rgb[idx, 0] = x[idx]
            rgb[idx, 1] = 0
            rgb[idx, 2] = c[idx]
        
        idx = (h >= 5/6) & (h <= 1)
        if np.any(idx):
            rgb[idx, 0] = c[idx]
            rgb[idx, 1] = 0
            rgb[idx, 2] = x[idx]
        
        # 添加基础亮度
        rgb += m.reshape(-1, 1)
        
        return rgb

    def get_contrasting_colors_vectorized(self, colors, algorithm='enhanced'):
        """完全向量化生成对比色"""
        if len(colors.shape) == 1:
            colors = colors.reshape(1, -1)
        
        colors_rgb = colors[:, :3] / 255.0  # 归一化到0-1
        
        if algorithm == 'enhanced':
            # 向量化HSV处理
            hsv = self.rgb_to_hsv_vectorized(colors_rgb)
            h, s, v = hsv[:, 0], hsv[:, 1], hsv[:, 2]
            
            # 调整色相以获得对比色
            h = np.where(h < 0.5, h + 0.5, h - 0.5)
            
            # 调整饱和度和明度
            v_mask = v > 0.5
            v = np.where(v_mask, np.maximum(0.2, v - 0.4), np.minimum(1.0, v + 0.4))
            s = np.where(v_mask, np.minimum(1.0, s + 0.3), np.minimum(1.0, s + 0.2))
            
            # 转换回RGB
            hsv_new = np.stack([h, s, v], axis=1)
            contrasting_colors = self.hsv_to_rgb_vectorized(hsv_new)
        
        elif algorithm == 'classic':
            # 简单的RGB反转
            contrasting_colors = 1.0 - colors_rgb
        
        else:  # gentle
            # 温和调整
            contrasting_colors = np.clip(colors_rgb + 0.3, 0, 1)
            mask = contrasting_colors > 0.8
            contrasting_colors[mask] = colors_rgb[mask] - 0.4
        
        return (contrasting_colors * 255).astype(np.uint8)

    def apply_alpha_protected_watermark_vectorized(self, image, watermark, opacity, stretch, 
                                                 smart_color, sensitivity, algorithm, 
                                                 performance_mode, enable_smoothing, smoothing_radius):
        """向量化的Alpha通道保护水印应用"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 计算水印尺寸
        if stretch:
            new_width, new_height = image.width, image.height
        else:
            watermark_ratio = watermark.width / watermark.height
            if image.width / image.height > watermark_ratio:
                new_width = image.width
                new_height = int(new_width / watermark_ratio)
            else:
                new_height = image.height
                new_width = int(new_height * watermark_ratio)

        # 缩放水印
        resized_watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
        position = ((image.width - new_width) // 2, (image.height - new_height) // 2)

        # 转换为NumPy数组
        image_array = np.array(image, dtype=np.uint8)
        watermark_array = np.array(resized_watermark, dtype=np.uint8)
        
        # 创建保护蒙版
        protection_mask = self.create_protection_mask_vectorized(watermark_array)
        
        # 应用边缘平滑
        if enable_smoothing:
            smooth_mask = self.apply_edge_smoothing_vectorized(protection_mask, smoothing_radius)
        else:
            smooth_mask = protection_mask.astype(np.float32)

        # 向量化处理
        return self._process_with_alpha_protection_vectorized(
            image_array, watermark_array, position, opacity, smart_color, 
            sensitivity, algorithm, performance_mode, protection_mask, smooth_mask
        )

    def create_protection_mask_vectorized(self, watermark_array):
        """向量化创建保护蒙版"""
        alpha_channel = watermark_array[:, :, 3]
        # Alpha值为255的区域为完全保护区域
        protection_mask = (alpha_channel == 255).astype(np.uint8)
        return protection_mask

    def apply_edge_smoothing_vectorized(self, mask, smoothing_radius):
        """向量化边缘平滑"""
        if smoothing_radius <= 0:
            return mask.astype(np.float32)
        
        # 使用高斯滤波进行边缘平滑
        smooth_mask = ndimage.gaussian_filter(mask.astype(np.float32), sigma=smoothing_radius)
        return smooth_mask

    def _process_with_alpha_protection_vectorized(self, image_array, watermark_array, position, 
                                                opacity, smart_color, sensitivity, algorithm, 
                                                performance_mode, protection_mask, smooth_mask):
        """向量化的Alpha保护处理"""
        h, w = watermark_array.shape[:2]
        img_h, img_w = image_array.shape[:2]
        
        # 计算有效区域
        start_x, start_y = position
        end_x = min(start_x + w, img_w)
        end_y = min(start_y + h, img_h)
        
        # 调整水印区域以匹配有效区域
        wm_end_x = end_x - start_x
        wm_end_y = end_y - start_y
        
        if wm_end_x <= 0 or wm_end_y <= 0:
            return Image.fromarray(image_array, 'RGBA')
        
        # 确保索引不越界
        safe_wm_end_y = min(wm_end_y, watermark_array.shape[0])
        safe_wm_end_x = min(wm_end_x, watermark_array.shape[1])
        safe_end_y = min(end_y, image_array.shape[0])
        safe_end_x = min(end_x, image_array.shape[1])
        
        # 提取相关区域
        bg_region = image_array[start_y:safe_end_y, start_x:safe_end_x]
        wm_region = watermark_array[:safe_wm_end_y, :safe_wm_end_x]
        mask_region = protection_mask[:safe_wm_end_y, :safe_wm_end_x]
        smooth_region = smooth_mask[:safe_wm_end_y, :safe_wm_end_x]
        
        # 确保所有区域尺寸一致
        min_h = min(bg_region.shape[0], wm_region.shape[0])
        min_w = min(bg_region.shape[1], wm_region.shape[1])
        
        bg_region = bg_region[:min_h, :min_w]
        wm_region = wm_region[:min_h, :min_w]
        mask_region = mask_region[:min_h, :min_w]
        smooth_region = smooth_region[:min_h, :min_w]
        
        # 只处理有Alpha值的像素
        alpha_mask = wm_region[:, :, 3] > 0
        
        if not np.any(alpha_mask):
            return Image.fromarray(image_array, 'RGBA')
        
        # 更新进度
        self.root.after(0, lambda: self.progress_var.set(20))
        
        # 提取有效像素
        valid_pixels = np.where(alpha_mask)
        wm_colors = wm_region[valid_pixels]  # [N, 4] RGBA
        bg_colors = bg_region[valid_pixels]  # [N, 4] RGBA
        protection_values = mask_region[valid_pixels]  # [N]
        smooth_values = smooth_region[valid_pixels]  # [N]
        
        # 更新进度
        self.root.after(0, lambda: self.progress_var.set(40))
        
        # 智能颜色调整
        if smart_color:
            # 计算颜色距离
            distances = self.calculate_color_distance_vectorized(wm_colors, bg_colors)
            
            # 找出需要调整的像素
            need_adjustment = (distances < sensitivity) & (smooth_values < 0.9)
            
            if np.any(need_adjustment):
                # 生成对比色
                contrasting_colors = self.get_contrasting_colors_vectorized(
                    bg_colors[need_adjustment], algorithm
                )
                
                # 应用保护因子混合
                protection_factors = smooth_values[need_adjustment].reshape(-1, 1)
                mix_factors = 1.0 - protection_factors
                
                # 混合原色和对比色
                original_colors = wm_colors[need_adjustment, :3].astype(np.float32)
                mixed_colors = (original_colors * protection_factors + 
                              contrasting_colors.astype(np.float32) * mix_factors)
                
                # 更新颜色
                wm_colors[need_adjustment, :3] = np.clip(mixed_colors, 0, 255).astype(np.uint8)
        
        # 更新进度
        self.root.after(0, lambda: self.progress_var.set(70))
        
        # 应用透明度
        wm_colors[:, 3] = (wm_colors[:, 3].astype(np.float32) * opacity / 100).astype(np.uint8)
        
        # 创建结果图像
        result_array = image_array.copy()
        
        # Alpha混合
        alpha_ratio = wm_colors[:, 3:4].astype(np.float32) / 255.0
        inv_alpha = 1.0 - alpha_ratio
        
        # 向量化混合
        for c in range(3):  # RGB通道
            result_array[start_y:end_y, start_x:end_x][valid_pixels[0], valid_pixels[1], c] = (
                bg_colors[:, c].astype(np.float32) * inv_alpha.flatten() +
                wm_colors[:, c].astype(np.float32) * alpha_ratio.flatten()
            ).astype(np.uint8)
        
        # 更新进度
        self.root.after(0, lambda: self.progress_var.set(100))
        
        return Image.fromarray(result_array, 'RGBA')

    def apply_alpha_protected_watermark(self, image, watermark, opacity, stretch, 
                                      smart_color, sensitivity, algorithm, 
                                      performance_mode, enable_smoothing, smoothing_radius):
        """应用Alpha通道保护的智能水印 - 使用向量化版本"""
        return self.apply_alpha_protected_watermark_vectorized(
            image, watermark, opacity, stretch, smart_color, sensitivity, 
            algorithm, performance_mode, enable_smoothing, smoothing_radius
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AlphaProtectedWatermarkApp(root)
    root.mainloop() 