import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import os
import json
import numpy as np
from math import sqrt

class SmartWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Watermark App v1.3 (Intelligent Color Adaptation)")
        self.root.configure(bg='#FAFAFA')  # Instagram-style background
        
        # Set minimum window size
        self.root.minsize(450, 650)
        
        # Initialize path memory
        self.config_file = "smart_watermark_config.json"
        
        # Initialize variables first
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
        
        # Debounce timer for opacity changes
        self.opacity_save_timer = None
        
        # Load configuration before creating UI
        self.load_config()
        
        # Main container with padding
        main_container = tk.Frame(root, bg='#FAFAFA')
        main_container.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_container,
            text="Smart Watermark App v1.3",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_container,
            text="🧠 Intelligent Color Adaptation",
            font=('Helvetica', 12),
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
            orient=tk.HORIZONTAL,
            command=self.on_opacity_change
        )
        # Set default value from config
        default_opacity = getattr(self, 'last_opacity', 50)
        self.opacity_slider.set(default_opacity)
        self.opacity_slider.pack(fill=tk.X, pady=(5, 0))

        # Stretch option
        self.stretch_var = tk.BooleanVar()
        # Set default value from config
        default_stretch = getattr(self, 'last_stretch', False)
        self.stretch_var.set(default_stretch)
        self.stretch_checkbox = ttk.Checkbutton(
            settings_frame,
            text="Stretch watermark to fit image",
            variable=self.stretch_var,
            style='Switch.TCheckbutton',
            command=self.on_stretch_change
        )
        self.stretch_checkbox.pack(pady=5)

        # 🆕 Smart Color Adaptation Frame
        smart_frame = tk.LabelFrame(
            main_container,
            text="🧠 Smart Color Adaptation",
            font=('Helvetica', 11, 'bold'),
            fg='#0095F6',
            bg='#FAFAFA',
            padx=10,
            pady=10
        )
        smart_frame.pack(fill=tk.X, pady=15)

        # Smart color option
        self.smart_color_var = tk.BooleanVar()
        default_smart_color = getattr(self, 'last_smart_color', True)
        self.smart_color_var.set(default_smart_color)
        self.smart_color_checkbox = ttk.Checkbutton(
            smart_frame,
            text="🎯 Enable intelligent color adaptation",
            variable=self.smart_color_var,
            style='Switch.TCheckbutton',
            command=self.on_smart_color_change
        )
        self.smart_color_checkbox.pack(pady=(0, 10))

        # Color sensitivity frame
        sensitivity_frame = tk.Frame(smart_frame, bg='#FAFAFA')
        sensitivity_frame.pack(fill=tk.X, pady=(0, 5))

        # Sensitivity label
        sensitivity_label = tk.Label(
            sensitivity_frame,
            text="Color Similarity Sensitivity (Lower = More Sensitive)",
            font=('Helvetica', 10),
            fg='#262626',
            bg='#FAFAFA'
        )
        sensitivity_label.pack(anchor='w')

        # Sensitivity slider
        self.sensitivity_slider = ttk.Scale(
            sensitivity_frame,
            from_=10,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.on_sensitivity_change
        )
        default_sensitivity = getattr(self, 'last_sensitivity', 30)
        self.sensitivity_slider.set(default_sensitivity)
        self.sensitivity_slider.pack(fill=tk.X, pady=(5, 0))

        # Algorithm description
        desc_label = tk.Label(
            smart_frame,
            text="💡 When watermark color is too similar to background,\nautomatically adjusts to contrasting color for maximum visibility",
            font=('Helvetica', 9),
            fg='#666666',
            bg='#FAFAFA',
            justify=tk.LEFT
        )
        desc_label.pack(pady=(5, 0))

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

        # Apply watermark button (prominent)
        self.apply_watermark_btn = tk.Button(
            main_container,
            text="🚀 Apply Smart Watermark",
            command=self.apply_watermark,
            **apply_button_style
        )
        self.apply_watermark_btn.pack(fill=tk.X, pady=(20, 0))

        # Configure style for the switch
        style = ttk.Style()
        style.configure('Switch.TCheckbutton', 
                       background='#FAFAFA',
                       font=('Helvetica', 10))

        # Update UI with loaded configuration
        self.update_save_dir_label()
        
        # Auto-load last used files if they exist
        self.auto_load_last_files()

    def calculate_color_distance(self, color1, color2):
        """计算两个颜色之间的欧几里得距离"""
        return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

    def get_contrasting_color(self, color):
        """获取对比色"""
        r, g, b = color[:3]
        
        # 计算亮度 (使用相对亮度公式)
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        
        # 如果原色较暗，返回亮色；如果原色较亮，返回暗色
        if luminance < 128:
            # 原色较暗，返回更亮的对比色
            contrast_r = min(255, r + (255 - r) * 0.8)
            contrast_g = min(255, g + (255 - g) * 0.8)
            contrast_b = min(255, b + (255 - b) * 0.8)
        else:
            # 原色较亮，返回更暗的对比色
            contrast_r = max(0, r * 0.2)
            contrast_g = max(0, g * 0.2)
            contrast_b = max(0, b * 0.2)
        
        return (int(contrast_r), int(contrast_g), int(contrast_b))

    def get_adaptive_color(self, watermark_color, background_color, sensitivity):
        """根据背景色智能调整水印颜色"""
        # 计算颜色距离
        distance = self.calculate_color_distance(watermark_color[:3], background_color[:3])
        
        # 如果颜色距离小于敏感度阈值，则使用对比色
        if distance < sensitivity:
            contrasting_color = self.get_contrasting_color(background_color)
            print(f"🎨 颜色自适应: 背景{background_color[:3]} → 水印{watermark_color[:3]} → 对比色{contrasting_color}")
            return contrasting_color + (watermark_color[-1],)  # 保持原始alpha值
        
        return watermark_color

    def apply_smart_watermark_to_image(self, image, watermark, opacity, stretch, smart_color, sensitivity):
        """对单张图片应用智能水印"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        if stretch:
            # Stretch watermark to fit image exactly
            new_width = image.width
            new_height = image.height
        else:
            # Maintain aspect ratio
            watermark_ratio = watermark.width / watermark.height
            if image.width / image.height > watermark_ratio:
                new_width = image.width
                new_height = int(new_width / watermark_ratio)
            else:
                new_height = image.height
                new_width = int(new_height * watermark_ratio)

        # Resize the watermark
        resized_watermark = watermark.resize((new_width, new_height), Image.LANCZOS)

        # Calculate position to center the watermark
        position = ((image.width - new_width) // 2, (image.height - new_height) // 2)

        # 创建智能适应的水印
        smart_watermark = Image.new('RGBA', resized_watermark.size, (0, 0, 0, 0))
        
        # 转换为numpy数组进行快速处理
        image_array = np.array(image)
        
        for x in range(resized_watermark.width):
            for y in range(resized_watermark.height):
                watermark_pixel = resized_watermark.getpixel((x, y))
                r, g, b, a = watermark_pixel
                
                if a > 0:  # 只处理非透明像素
                    # 获取对应背景位置的颜色
                    bg_x = position[0] + x
                    bg_y = position[1] + y
                    
                    if 0 <= bg_x < image.width and 0 <= bg_y < image.height:
                        bg_color = tuple(image_array[bg_y, bg_x])
                        
                        if smart_color:
                            # 应用智能颜色适应
                            adapted_color = self.get_adaptive_color(
                                watermark_pixel, bg_color, sensitivity
                            )
                            r, g, b = adapted_color[:3]
                    
                    # 应用透明度
                    smart_watermark.putpixel((x, y), (r, g, b, int(a * opacity)))

        # 应用水印到图片
        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
        temp.paste(smart_watermark, position)
        output = Image.alpha_composite(image, temp)

        return output

    def load_config(self):
        """加载配置文件，记住上次使用的路径和设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 路径配置
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
                    
                    # 用户设置配置
                    self.last_opacity = config.get('last_opacity', 50)
                    self.last_stretch = config.get('last_stretch', False)
                    self.last_smart_color = config.get('last_smart_color', True)
                    self.last_sensitivity = config.get('last_sensitivity', 30)
                    
                    # 文件路径记忆
                    self.last_watermark_file = config.get('last_watermark_file')
                    self.last_images_files = config.get('last_images_files', [])
                    print("📝 配置加载成功")
            else:
                # 默认配置
                self.last_used_directory = None
                self.save_directory = None
                self.last_watermark_directory = None
                self.last_images_directory = None
                self.last_opacity = 50
                self.last_stretch = False
                self.last_smart_color = True
                self.last_sensitivity = 30
                self.last_watermark_file = None
                self.last_images_files = []
                print("📝 使用默认配置")
        except Exception as e:
            print(f"❌ 加载配置文件时出错: {e}")
            # 使用默认配置
            self.last_used_directory = None
            self.save_directory = None
            self.last_watermark_directory = None
            self.last_images_directory = None
            self.last_opacity = 50
            self.last_stretch = False
            self.last_smart_color = True
            self.last_sensitivity = 30
            self.last_watermark_file = None
            self.last_images_files = []

    def save_config(self):
        """保存配置文件，记住当前使用的路径和设置"""
        try:
            config = {
                # 路径配置
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory,
                
                # 用户设置配置
                'last_opacity': self.opacity_slider.get() if self.opacity_slider else self.last_opacity,
                'last_stretch': self.stretch_var.get() if self.stretch_var else self.last_stretch,
                'last_smart_color': self.smart_color_var.get() if self.smart_color_var else self.last_smart_color,
                'last_sensitivity': self.sensitivity_slider.get() if self.sensitivity_slider else self.last_sensitivity,
                
                # 文件路径记忆
                'last_watermark_file': self.last_watermark_file,
                'last_images_files': self.last_images_files
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"💾 配置保存成功")
        except Exception as e:
            print(f"❌ 保存配置文件时出错: {e}")

    def on_opacity_change(self, value):
        """透明度滑块变化时保存配置"""
        if self.opacity_save_timer:
            self.root.after_cancel(self.opacity_save_timer)
        self.opacity_save_timer = self.root.after(1000, self.save_config)

    def on_stretch_change(self):
        """拉伸选项变化时保存配置"""
        self.save_config()

    def on_smart_color_change(self):
        """智能颜色选项变化时保存配置"""
        self.save_config()

    def on_sensitivity_change(self, value):
        """敏感度滑块变化时保存配置"""
        if self.opacity_save_timer:
            self.root.after_cancel(self.opacity_save_timer)
        self.opacity_save_timer = self.root.after(1000, self.save_config)

    def auto_load_last_files(self):
        """自动加载上次使用的文件"""
        try:
            # 自动加载上次的水印文件
            if self.last_watermark_file and os.path.exists(self.last_watermark_file):
                self.watermark = Image.open(self.last_watermark_file).convert("RGBA")
                print(f"🎨 自动加载水印: {self.last_watermark_file}")
            
            # 自动加载上次的图片文件
            if self.last_images_files:
                valid_files = [f for f in self.last_images_files if os.path.exists(f)]
                if valid_files:
                    self.image_paths = valid_files
                    self.images = [Image.open(file_path) for file_path in valid_files]
                    print(f"🖼️ 自动加载图片: {len(valid_files)}张")
                else:
                    print("⚠️ 上次的图片文件不存在，跳过自动加载")
        except Exception as e:
            print(f"⚠️ 自动加载文件时出错: {e}")

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
            # 记住图片文件夹路径和文件路径
            self.last_images_directory = os.path.dirname(file_paths[0])
            self.last_used_directory = self.last_images_directory
            self.last_images_files = list(file_paths)  # 记住具体文件路径
            if not self.save_directory:
                self.save_directory = self.last_used_directory
            self.update_save_dir_label()
            # 保存配置
            self.save_config()

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
            # 记住水印文件夹路径和文件路径
            self.last_watermark_directory = os.path.dirname(file_path)
            self.last_watermark_file = file_path  # 记住具体文件路径
            # 保存配置
            self.save_config()

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

    def apply_watermark(self):
        if not self.images or not self.watermark:
            print("Please upload images and a watermark first.")
            return

        if not self.save_directory:
            if self.last_used_directory:
                self.save_directory = self.last_used_directory
                self.update_save_dir_label()
            else:
                print("Please select a save directory first.")
                return

        opacity = self.opacity_slider.get() / 100.0
        stretch = self.stretch_var.get()
        smart_color = self.smart_color_var.get()
        sensitivity = self.sensitivity_slider.get()
        
        print(f"🚀 开始智能水印处理...")
        print(f"🎛️ 设置: 透明度={opacity:.0%}, 拉伸={stretch}, 智能颜色={smart_color}, 敏感度={sensitivity}")
        
        for i, image in enumerate(self.images):
            print(f"🖼️ 处理图片 {i+1}/{len(self.images)}: {os.path.basename(self.image_paths[i])}")
            
            # 应用智能水印
            output = self.apply_smart_watermark_to_image(
                image, self.watermark, opacity, stretch, smart_color, sensitivity
            )

            if output.mode == 'RGBA':
                output = output.convert('RGB')
            
            original_filename = os.path.basename(self.image_paths[i])
            filename_without_ext = os.path.splitext(original_filename)[0]
            output_filename = f"{filename_without_ext}_smart_watermarked.png"
            output_path = os.path.join(self.save_directory, output_filename)
            
            output.save(output_path)
            print(f"✅ 保存完成: {output_path}")
        
        print(f"🎉 所有图片处理完成！")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartWatermarkApp(root)
    root.mainloop() 