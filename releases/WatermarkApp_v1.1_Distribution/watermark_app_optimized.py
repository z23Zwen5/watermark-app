import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import os
import json
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App v1.1 (Optimized)")
        self.root.configure(bg='#FAFAFA')  # Instagram-style background
        
        # Set minimum window size
        self.root.minsize(400, 550)
        
        # Initialize path memory
        self.config_file = "watermark_app_config.json"
        self.load_config()
        
        # Main container with padding
        main_container = tk.Frame(root, bg='#FAFAFA')
        main_container.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_container,
            text="Watermark App v1.1",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_container,
            text="⚡ Optimized Performance Edition",
            font=('Helvetica', 10),
            fg='#0095F6',
            bg='#FAFAFA'
        )
        subtitle_label.pack(pady=(0, 20))

        # Create buttons frame
        buttons_frame = tk.Frame(main_container, bg='#FAFAFA')
        buttons_frame.pack(fill=tk.X, pady=(0, 15))

        # Style for buttons
        button_style = {
            'font': ('Helvetica', 10),
            'bg': '#0095F6',  # Instagram blue
            'fg': 'white',
            'activebackground': '#0081D6',
            'activeforeground': 'white',
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'  # Hand cursor on hover
        }

        # Style for the apply button (with larger font)
        apply_button_style = button_style.copy()
        apply_button_style['font'] = ('Helvetica', 12, 'bold')
        apply_button_style['pady'] = 12

        # Upload buttons frame
        upload_frame = tk.Frame(buttons_frame, bg='#FAFAFA')
        upload_frame.pack(fill=tk.X, pady=(0, 15))

        # Upload image button
        self.upload_image_btn = tk.Button(
            upload_frame,
            text="Upload Images",
            command=self.upload_images,
            **button_style
        )
        self.upload_image_btn.pack(side=tk.LEFT, padx=5)

        # Upload watermark button
        self.upload_watermark_btn = tk.Button(
            upload_frame,
            text="Upload Watermark",
            command=self.upload_watermark,
            **button_style
        )
        self.upload_watermark_btn.pack(side=tk.LEFT, padx=5)

        # Settings frame
        settings_frame = tk.Frame(main_container, bg='#FAFAFA')
        settings_frame.pack(fill=tk.X, pady=15)

        # Opacity control frame
        opacity_frame = tk.Frame(settings_frame, bg='#FAFAFA')
        opacity_frame.pack(fill=tk.X, pady=(0, 10))

        # Opacity label
        opacity_label = tk.Label(
            opacity_frame,
            text="Opacity",
            font=('Helvetica', 12),
            fg='#262626',
            bg='#FAFAFA'
        )
        opacity_label.pack(anchor='w')

        # Custom style for slider
        self.opacity_slider = ttk.Scale(
            opacity_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL
        )
        self.opacity_slider.set(50)
        self.opacity_slider.pack(fill=tk.X, pady=(5, 0))

        # Stretch option
        self.stretch_var = tk.BooleanVar()
        self.stretch_var.set(False)
        self.stretch_checkbox = ttk.Checkbutton(
            settings_frame,
            text="Stretch watermark to fit image",
            variable=self.stretch_var,
            style='Switch.TCheckbutton'
        )
        self.stretch_checkbox.pack(pady=10)

        # Performance options frame
        perf_frame = tk.Frame(settings_frame, bg='#FAFAFA')
        perf_frame.pack(fill=tk.X, pady=10)

        # Parallel processing option
        self.parallel_var = tk.BooleanVar()
        self.parallel_var.set(True)
        self.parallel_checkbox = ttk.Checkbutton(
            perf_frame,
            text="Enable parallel processing (faster)",
            variable=self.parallel_var,
            style='Switch.TCheckbutton'
        )
        self.parallel_checkbox.pack(pady=5)

        # Save directory frame with modern styling
        save_dir_frame = tk.Frame(main_container, bg='#FAFAFA')
        save_dir_frame.pack(fill=tk.X, pady=15)

        # Save directory button
        self.save_dir_btn = tk.Button(
            save_dir_frame,
            text="Select Save Directory",
            command=self.select_save_directory,
            **button_style
        )
        self.save_dir_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Save directory label with border
        self.save_dir_label = tk.Label(
            save_dir_frame,
            text="No directory selected",
            wraplength=300,
            justify=tk.LEFT,
            bg='#FFFFFF',
            fg='#262626',
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=5
        )
        self.save_dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Progress frame
        progress_frame = tk.Frame(main_container, bg='#FAFAFA')
        progress_frame.pack(fill=tk.X, pady=15)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        # Progress label
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to process",
            font=('Helvetica', 9),
            fg='#666666',
            bg='#FAFAFA'
        )
        self.progress_label.pack()

        # Apply watermark button (prominent)
        self.apply_watermark_btn = tk.Button(
            main_container,
            text="Apply Watermark",
            command=self.apply_watermark_threaded,
            **apply_button_style
        )
        self.apply_watermark_btn.pack(fill=tk.X, pady=(20, 0))

        # Initialize variables
        self.images = []
        self.watermark = None
        self.image_paths = []
        self.save_directory = None
        self.last_used_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None
        self.watermark_cache = {}  # Cache for preprocessed watermarks

        # Configure style for the switch
        style = ttk.Style()
        style.configure('Switch.TCheckbutton', 
                       background='#FAFAFA',
                       font=('Helvetica', 10))

    def load_config(self):
        """加载配置文件，记住上次使用的路径"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
            else:
                self.last_used_directory = None
                self.save_directory = None
                self.last_watermark_directory = None
                self.last_images_directory = None
        except Exception as e:
            print(f"加载配置文件时出错: {e}")
            self.last_used_directory = None
            self.save_directory = None
            self.last_watermark_directory = None
            self.last_images_directory = None

    def save_config(self):
        """保存配置文件，记住当前使用的路径"""
        try:
            config = {
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件时出错: {e}")

    def upload_images(self):
        self.root.lift()  # Bring window to top
        # 使用记住的图片文件夹路径作为初始目录
        initial_dir = self.last_images_directory if self.last_images_directory else "/"
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")],
            initialdir=initial_dir,
            parent=self.root
        )
        if file_paths:
            self.image_paths = file_paths
            self.images = [Image.open(file_path) for file_path in file_paths]
            # 记住图片文件夹路径
            self.last_images_directory = os.path.dirname(file_paths[0])
            self.last_used_directory = self.last_images_directory
            if not self.save_directory:
                self.save_directory = self.last_used_directory
            self.update_save_dir_label()
            # 保存配置
            self.save_config()
            # 更新进度标签
            self.progress_label.config(text=f"Loaded {len(file_paths)} images")

    def upload_watermark(self):
        self.root.lift()  # Bring window to top
        # 使用记住的水印文件夹路径作为初始目录
        initial_dir = self.last_watermark_directory if self.last_watermark_directory else "/"
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png")],
            initialdir=initial_dir,
            parent=self.root
        )
        if file_path:
            self.watermark = Image.open(file_path).convert("RGBA")
            # 记住水印文件夹路径
            self.last_watermark_directory = os.path.dirname(file_path)
            # 保存配置
            self.save_config()
            # 清空缓存
            self.watermark_cache.clear()
            # 更新进度标签
            self.progress_label.config(text="Watermark loaded")

    def select_save_directory(self):
        self.root.lift()  # Bring window to top
        initial_dir = self.last_used_directory if self.last_used_directory else "/"
        directory = filedialog.askdirectory(
            initialdir=initial_dir,
            parent=self.root
        )
        if directory:
            self.save_directory = directory
            self.last_used_directory = directory
            self.update_save_dir_label()
            # 保存配置
            self.save_config()

    def update_save_dir_label(self):
        if self.save_directory:
            self.save_dir_label.config(text=self.save_directory)
        else:
            self.save_dir_label.config(text="No directory selected")

    def apply_watermark_optimized(self, image, watermark, opacity, stretch=False):
        """优化的水印应用函数，使用numpy进行快速像素操作"""
        # 确保图像是RGBA模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # 计算水印尺寸
        if stretch:
            new_width = image.width
            new_height = image.height
        else:
            watermark_ratio = watermark.width / watermark.height
            if image.width / image.height > watermark_ratio:
                new_width = image.width
                new_height = int(new_width / watermark_ratio)
            else:
                new_height = image.height
                new_width = int(new_height * watermark_ratio)
        
        # 检查缓存
        cache_key = (new_width, new_height, opacity)
        if cache_key in self.watermark_cache:
            processed_watermark = self.watermark_cache[cache_key]
        else:
            # 调整水印大小
            resized_watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
            
            # 使用numpy进行快速透明度处理
            watermark_array = np.array(resized_watermark)
            # 只修改alpha通道
            watermark_array[:, :, 3] = (watermark_array[:, :, 3] * opacity).astype(np.uint8)
            processed_watermark = Image.fromarray(watermark_array, 'RGBA')
            
            # 缓存处理后的水印
            self.watermark_cache[cache_key] = processed_watermark
        
        # 计算居中位置
        position = ((image.width - new_width) // 2, (image.height - new_height) // 2)
        
        # 创建临时图像用于合成
        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
        temp.paste(processed_watermark, position)
        
        # 使用alpha合成
        output = Image.alpha_composite(image, temp)
        
        # 转换为RGB（如果需要）
        if output.mode == 'RGBA':
            output = output.convert('RGB')
        
        return output

    def process_single_image(self, args):
        """处理单张图片的函数，用于并行处理"""
        i, image, image_path, opacity, stretch = args
        
        try:
            # 应用水印
            output = self.apply_watermark_optimized(image, self.watermark, opacity, stretch)
            
            # 生成输出文件名
            original_filename = os.path.basename(image_path)
            filename_without_ext = os.path.splitext(original_filename)[0]
            output_filename = f"{filename_without_ext}_watermarked.png"
            output_path = os.path.join(self.save_directory, output_filename)
            
            # 保存图片
            output.save(output_path)
            
            return f"Saved: {output_path}"
        except Exception as e:
            return f"Error processing {image_path}: {str(e)}"

    def apply_watermark_threaded(self):
        """在单独线程中运行水印应用，避免UI冻结"""
        thread = threading.Thread(target=self.apply_watermark)
        thread.daemon = True
        thread.start()

    def apply_watermark(self):
        if not self.images or not self.watermark:
            self.progress_label.config(text="Please upload images and a watermark first.")
            return

        if not self.save_directory:
            if self.last_used_directory:
                self.save_directory = self.last_used_directory
                self.update_save_dir_label()
            else:
                self.progress_label.config(text="Please select a save directory first.")
                return

        # 禁用按钮
        self.apply_watermark_btn.config(state='disabled', text='Processing...')
        
        start_time = time.time()
        opacity = self.opacity_slider.get() / 100.0
        stretch = self.stretch_var.get()
        use_parallel = self.parallel_var.get()
        
        try:
            if use_parallel and len(self.images) > 1:
                # 并行处理
                self.progress_label.config(text="Processing images in parallel...")
                
                # 准备参数
                args_list = [(i, image, self.image_paths[i], opacity, stretch) 
                           for i, image in enumerate(self.images)]
                
                # 使用线程池并行处理
                with ThreadPoolExecutor(max_workers=min(4, len(self.images))) as executor:
                    results = []
                    for i, result in enumerate(executor.map(self.process_single_image, args_list)):
                        progress = (i + 1) / len(self.images) * 100
                        self.progress_var.set(progress)
                        self.progress_label.config(text=f"Processing: {i+1}/{len(self.images)}")
                        self.root.update_idletasks()
                        results.append(result)
                        print(result)
            else:
                # 串行处理
                self.progress_label.config(text="Processing images...")
                for i, image in enumerate(self.images):
                    args = (i, image, self.image_paths[i], opacity, stretch)
                    result = self.process_single_image(args)
                    print(result)
                    
                    # 更新进度
                    progress = (i + 1) / len(self.images) * 100
                    self.progress_var.set(progress)
                    self.progress_label.config(text=f"Processing: {i+1}/{len(self.images)}")
                    self.root.update_idletasks()
            
            # 完成处理
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.progress_var.set(100)
            self.progress_label.config(
                text=f"✅ Completed! Processed {len(self.images)} images in {processing_time:.2f}s"
            )
            
        except Exception as e:
            self.progress_label.config(text=f"Error: {str(e)}")
            print(f"Error during processing: {e}")
        
        finally:
            # 重新启用按钮
            self.apply_watermark_btn.config(state='normal', text='Apply Watermark')

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop() 