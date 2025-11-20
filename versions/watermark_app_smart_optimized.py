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

class SmartWatermarkAppOptimized:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Watermark App v1.4 (Optimized)")
        self.root.configure(bg='#FAFAFA')
        
        # Set minimum window size
        self.root.minsize(500, 700)
        
        # Initialize path memory
        self.config_file = "smart_watermark_optimized_config.json"
        
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
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        
        # 性能优化相关
        self.color_cache = {}  # 颜色缓存
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
            text="Smart Watermark App v1.4",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="🚀 Optimized Intelligent Color Adaptation",
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
        
        self.apply_btn = tk.Button(action_frame, text="🚀 Apply Smart Watermark",
                                 command=self.apply_watermark_threaded, **button_style)
        self.apply_btn.pack(fill=tk.X)

    # 颜色计算优化方法
    def calculate_color_distance_optimized(self, color1, color2):
        """优化的颜色距离计算"""
        # 使用缓存避免重复计算
        cache_key = (tuple(color1[:3]), tuple(color2[:3]))
        if cache_key in self.color_cache:
            return self.color_cache[cache_key]
        
        # 计算欧几里得距离
        distance = sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1[:3], color2[:3])))
        self.color_cache[cache_key] = distance
        return distance

    def get_contrasting_color_enhanced(self, color, algorithm='enhanced'):
        """增强的对比色算法"""
        r, g, b = color[:3]
        
        if algorithm == 'enhanced':
            # 使用HSV色彩空间进行更自然的对比
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            
            # 调整明度和饱和度
            if v < 0.5:
                # 暗色 -> 亮色
                new_v = min(1.0, v + 0.6)
                new_s = max(0.1, s * 0.8)
            else:
                # 亮色 -> 暗色
                new_v = max(0.0, v - 0.6)
                new_s = min(1.0, s * 1.2)
            
            # 转换回RGB
            new_r, new_g, new_b = colorsys.hsv_to_rgb(h, new_s, new_v)
            return (int(new_r * 255), int(new_g * 255), int(new_b * 255))
            
        elif algorithm == 'gentle':
            # 温和对比算法
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < 128:
                factor = 0.5  # 更温和的调整
                return (min(255, int(r + (255 - r) * factor)),
                       min(255, int(g + (255 - g) * factor)),
                       min(255, int(b + (255 - b) * factor)))
            else:
                factor = 0.5
                return (max(0, int(r * factor)),
                       max(0, int(g * factor)),
                       max(0, int(b * factor)))
        
        else:  # classic
            # 经典算法
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            if luminance < 128:
                return (min(255, r + int((255 - r) * 0.8)),
                       min(255, g + int((255 - g) * 0.8)),
                       min(255, b + int((255 - b) * 0.8)))
            else:
                return (max(0, int(r * 0.2)),
                       max(0, int(g * 0.2)),
                       max(0, int(b * 0.2)))

    def apply_smart_watermark_optimized(self, image, watermark, opacity, stretch, 
                                      smart_color, sensitivity, algorithm, performance_mode):
        """优化的智能水印处理"""
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

        # 根据性能模式选择处理策略
        if performance_mode == 'speed':
            return self._process_speed_mode(image, resized_watermark, position, opacity, 
                                          smart_color, sensitivity, algorithm)
        elif performance_mode == 'quality':
            return self._process_quality_mode(image, resized_watermark, position, opacity,
                                            smart_color, sensitivity, algorithm)
        else:  # balanced
            return self._process_balanced_mode(image, resized_watermark, position, opacity,
                                             smart_color, sensitivity, algorithm)

    def _process_speed_mode(self, image, watermark, position, opacity, smart_color, sensitivity, algorithm):
        """速度优先模式 - 采样处理"""
        smart_watermark = Image.new('RGBA', watermark.size, (0, 0, 0, 0))
        image_array = np.array(image)
        
        # 采样步长，减少计算量
        step = 3
        
        for x in range(0, watermark.width, step):
            for y in range(0, watermark.height, step):
                # 处理采样点
                self._process_pixel_block(image_array, watermark, smart_watermark, 
                                        x, y, min(step, watermark.width - x), 
                                        min(step, watermark.height - y),
                                        position, opacity, smart_color, sensitivity, algorithm)
        
        return self._apply_watermark_to_image(image, smart_watermark, position)

    def _process_balanced_mode(self, image, watermark, position, opacity, smart_color, sensitivity, algorithm):
        """平衡模式 - 适中的采样率"""
        smart_watermark = Image.new('RGBA', watermark.size, (0, 0, 0, 0))
        image_array = np.array(image)
        
        step = 2
        
        for x in range(0, watermark.width, step):
            for y in range(0, watermark.height, step):
                self._process_pixel_block(image_array, watermark, smart_watermark, 
                                        x, y, min(step, watermark.width - x), 
                                        min(step, watermark.height - y),
                                        position, opacity, smart_color, sensitivity, algorithm)
        
        return self._apply_watermark_to_image(image, smart_watermark, position)

    def _process_quality_mode(self, image, watermark, position, opacity, smart_color, sensitivity, algorithm):
        """质量优先模式 - 逐像素处理"""
        smart_watermark = Image.new('RGBA', watermark.size, (0, 0, 0, 0))
        image_array = np.array(image)
        
        total_pixels = watermark.width * watermark.height
        processed = 0
        
        for x in range(watermark.width):
            for y in range(watermark.height):
                watermark_pixel = watermark.getpixel((x, y))
                r, g, b, a = watermark_pixel
                
                if a > 0:
                    bg_x = position[0] + x
                    bg_y = position[1] + y
                    
                    if 0 <= bg_x < image.width and 0 <= bg_y < image.height:
                        bg_color = tuple(image_array[bg_y, bg_x])
                        
                        if smart_color:
                            distance = self.calculate_color_distance_optimized(watermark_pixel, bg_color)
                            if distance < sensitivity:
                                contrasting_color = self.get_contrasting_color_enhanced(bg_color, algorithm)
                                r, g, b = contrasting_color
                    
                    smart_watermark.putpixel((x, y), (r, g, b, int(a * opacity)))
                
                # 更新进度
                processed += 1
                if processed % 1000 == 0:
                    progress = (processed / total_pixels) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
        
        return self._apply_watermark_to_image(image, smart_watermark, position)

    def _process_pixel_block(self, image_array, watermark, smart_watermark, x, y, w, h, 
                           position, opacity, smart_color, sensitivity, algorithm):
        """处理像素块"""
        for dx in range(w):
            for dy in range(h):
                px, py = x + dx, y + dy
                if px >= watermark.width or py >= watermark.height:
                    continue
                    
                watermark_pixel = watermark.getpixel((px, py))
                r, g, b, a = watermark_pixel
                
                if a > 0:
                    bg_x = position[0] + px
                    bg_y = position[1] + py
                    
                    if 0 <= bg_x < image_array.shape[1] and 0 <= bg_y < image_array.shape[0]:
                        bg_color = tuple(image_array[bg_y, bg_x])
                        
                        if smart_color:
                            distance = self.calculate_color_distance_optimized(watermark_pixel, bg_color)
                            if distance < sensitivity:
                                contrasting_color = self.get_contrasting_color_enhanced(bg_color, algorithm)
                                r, g, b = contrasting_color
                    
                    smart_watermark.putpixel((px, py), (r, g, b, int(a * opacity)))

    def _apply_watermark_to_image(self, image, watermark, position):
        """将水印应用到图片"""
        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
        temp.paste(watermark, position)
        return Image.alpha_composite(image, temp)

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
                output = self.apply_smart_watermark_optimized(
                    image, self.watermark, opacity, stretch, smart_color, 
                    sensitivity, algorithm, performance_mode
                )
                
                # 保存
                if output.mode == 'RGBA':
                    output = output.convert('RGB')
                
                original_filename = os.path.basename(self.image_paths[i])
                filename_without_ext = os.path.splitext(original_filename)[0]
                output_filename = f"{filename_without_ext}_smart_v14.png"
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
            self.root.after(0, lambda: self.apply_btn.config(state='normal', text='🚀 Apply Smart Watermark'))

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

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartWatermarkAppOptimized(root)
    root.mainloop() 