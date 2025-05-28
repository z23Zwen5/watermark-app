import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import os
import json

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.configure(bg='#FAFAFA')  # Instagram-style background
        
        # Set minimum window size
        self.root.minsize(400, 500)
        
        # Initialize path memory
        self.config_file = "watermark_app_config.json"
        self.load_config()
        
        # Main container with padding
        main_container = tk.Frame(root, bg='#FAFAFA')
        main_container.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_container,
            text="Watermark App",
            font=('Helvetica', 24, 'bold'),
            fg='#262626',
            bg='#FAFAFA'
        )
        title_label.pack(pady=(0, 20))

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
            text="Apply Watermark",
            command=self.apply_watermark,
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

        # Configure style for the switch
        style = ttk.Style()
        style.configure('Switch.TCheckbutton', 
                       background='#FAFAFA',
                       font=('Helvetica', 10))

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
        for i, image in enumerate(self.images):
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            if self.stretch_var.get():
                # Stretch watermark to fit image exactly
                new_width = image.width
                new_height = image.height
            else:
                # Maintain aspect ratio
                watermark_ratio = self.watermark.width / self.watermark.height
                if image.width / image.height > watermark_ratio:
                    new_width = image.width
                    new_height = int(new_width / watermark_ratio)
                else:
                    new_height = image.height
                    new_width = int(new_height * watermark_ratio)

            # Resize the watermark
            resized_watermark = self.watermark.resize((new_width, new_height), Image.LANCZOS)

            # Create a new watermark image with the desired opacity
            watermark = Image.new('RGBA', resized_watermark.size, (0, 0, 0, 0))
            for x in range(resized_watermark.width):
                for y in range(resized_watermark.height):
                    r, g, b, a = resized_watermark.getpixel((x, y))
                    watermark.putpixel((x, y), (r, g, b, int(a * opacity)))

            # Calculate position to center the watermark
            position = ((image.width - new_width) // 2, (image.height - new_height) // 2)

            # Create a new blank image with alpha channel
            temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
            temp.paste(watermark, position)
            output = Image.alpha_composite(image, temp)

            if output.mode == 'RGBA':
                output = output.convert('RGB')
            
            original_filename = os.path.basename(self.image_paths[i])
            filename_without_ext = os.path.splitext(original_filename)[0]
            output_filename = f"{filename_without_ext}_watermarked.png"
            output_path = os.path.join(self.save_directory, output_filename)
            
            output.save(output_path)
            print(f"Saved: {output_path}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()