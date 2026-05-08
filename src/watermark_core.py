#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watermark Core - Business Logic
核心业务逻辑：图层管理、混合模式、图像处理
"""

import os
import json
import numpy as np
from PIL import Image
from text_label_module import TextLabelConfig, draw_text_label


class WatermarkLayer:
    """水印图层类"""
    def __init__(self, image_path, opacity=100, blend_mode='normal', visible=True):
        self.image_path = image_path
        self._image = None  # 延迟加载：仅在需要时加载
        self.opacity = int(opacity)
        self.blend_mode = blend_mode
        self.visible = visible
        self.name = os.path.basename(image_path)

    @property
    def image(self):
        """延迟加载图片（仅在首次访问时打开）"""
        if self._image is None:
            self._image = Image.open(self.image_path).convert("RGBA")
        return self._image

    def __str__(self):
        visibility = "●" if self.visible else "○"
        return f"{visibility} {self.name} ({self.blend_mode}, {self.opacity}%)"

    def to_dict(self):
        """转换为字典（用于保存配置）"""
        return {
            'path': self.image_path,
            'opacity': int(self.opacity),
            'blend_mode': str(self.blend_mode),
            'visible': bool(self.visible)
        }

    @staticmethod
    def from_dict(data):
        """从字典创建图层"""
        return WatermarkLayer(
            data['path'],
            int(data.get('opacity', 100)),
            str(data.get('blend_mode', 'normal')),
            bool(data.get('visible', True))
        )


class WatermarkEngine:
    """水印处理引擎"""

    @staticmethod
    def apply_blend_mode(base_array, layer_array, blend_mode, opacity):
        """应用混合模式 - 优化版

        Args:
            base_array: 底层图像数组 (numpy array, RGBA)
            layer_array: 混合层图像数组 (numpy array, RGBA)
            blend_mode: 混合模式 (normal/overlay/screen/soft_light)
            opacity: 不透明度 (0-100)

        Returns:
            混合后的图像数组 (numpy array, RGBA)
        """
        opacity_factor = opacity / 100.0
        blend_alpha = layer_array[:, :, 3]

        if np.max(blend_alpha) < 1:
            return base_array

        # Normal 模式优化：使用 uint8 直接计算 (2x faster)
        if blend_mode == 'normal':
            result = base_array.copy()
            base_rgb = base_array[:, :, :3].astype(np.uint16)
            blend_rgb = layer_array[:, :, :3].astype(np.uint16)
            alpha = blend_alpha.astype(np.uint16)[:, :, np.newaxis]
            alpha = (alpha * opacity) // 100
            result_rgb = (base_rgb * (255 - alpha) + blend_rgb * alpha) // 255
            result[:, :, :3] = result_rgb.astype(np.uint8)
            return result

        # 其他混合模式：使用 float32（保证准确性）
        blend_alpha_f = blend_alpha.astype(np.float32) / 255.0
        mask = blend_alpha_f * opacity_factor
        has_alpha = mask > 0.001
        if not np.any(has_alpha):
            return base_array

        base_rgb = base_array[:, :, :3].astype(np.float32) / 255.0
        blend_rgb = layer_array[:, :, :3].astype(np.float32) / 255.0

        if blend_mode == 'screen':
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

        mask_3d = mask[:, :, np.newaxis]
        result_rgb = result_rgb * mask_3d + base_rgb * (1 - mask_3d)

        result = base_array.copy()
        result[:, :, :3] = (np.clip(result_rgb, 0, 1) * 255).astype(np.uint8)
        return result

    @staticmethod
    def apply_multilayer_watermark(image, layers, stretch=False, progress_callback=None):
        """应用多图层水印

        Args:
            image: PIL.Image 对象
            layers: WatermarkLayer 列表
            stretch: 是否拉伸水印以适应图像
            progress_callback: 进度回调函数 func(progress_percentage)

        Returns:
            处理后的 PIL.Image 对象 (RGBA)
        """
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        result = np.array(image, dtype=np.uint8)
        img_width, img_height = image.size

        total_visible_layers = sum(1 for layer in layers if layer.visible)
        processed_layers = 0

        for layer in layers:
            if not layer.visible:
                continue

            # 计算水印尺寸
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

            # 缩放水印（使用 BILINEAR 提速）
            resized_watermark = layer.image.resize((new_width, new_height), Image.Resampling.BILINEAR)
            position = ((img_width - new_width) // 2, (img_height - new_height) // 2)

            # 创建图层数组
            layer_array = np.zeros((img_height, img_width, 4), dtype=np.uint8)
            watermark_array = np.array(resized_watermark)

            # 复制水印到对应位置
            y1, y2 = position[1], position[1] + new_height
            x1, x2 = position[0], position[0] + new_width
            layer_array[y1:y2, x1:x2] = watermark_array

            # 应用混合模式
            result = WatermarkEngine.apply_blend_mode(result, layer_array, layer.blend_mode, layer.opacity)

            # 更新进度
            processed_layers += 1
            if progress_callback and total_visible_layers > 0:
                progress = (processed_layers / total_visible_layers) * 50
                progress_callback(int(progress))

        return Image.fromarray(result, 'RGBA')


class WatermarkConfig:
    """水印配置管理"""

    def __init__(self, config_dir="configs", config_file="multilayer_watermark_config.json"):
        self.config_dir = config_dir
        self.config_file = config_file
        os.makedirs(config_dir, exist_ok=True)

        # 配置数据
        self.last_used_directory = None
        self.save_directory = None
        self.last_watermark_directory = None
        self.last_images_directory = None
        self.last_stretch = False
        self.last_images_files = []
        self.ui_theme = 'genshin'  # UI 主题 (genshin/cyberpunk)
        self.output_resize_enabled = False  # 输出缩放开关
        self.output_resize_height = 1024    # 输出缩放目标高度
        self.layers = []
        self.text_label_config = TextLabelConfig()
        self.gemini_api_key = ""
        self.openai_api_key = ""
        self.claude_api_key = ""
        self.doubao_api_key = ""
        self.qwen_api_key = ""
        self.pan_greeting = ""
        self.custom_prompt = ""  # 自定义 AI 命名 Prompt 模板（空=使用默认）

    def load(self):
        """加载配置"""
        try:
            config_path = os.path.join(self.config_dir, self.config_file)
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.last_used_directory = config.get('last_used_directory')
                    self.save_directory = config.get('save_directory')
                    self.last_watermark_directory = config.get('last_watermark_directory')
                    self.last_images_directory = config.get('last_images_directory')
                    self.last_stretch = config.get('last_stretch', False)
                    self.last_images_files = config.get('last_images_files', [])
                    self.ui_theme = config.get('ui_theme', 'genshin')
                    self.output_resize_enabled = config.get('output_resize_enabled', False)
                    self.output_resize_height = config.get('output_resize_height', 1024)
                    self.gemini_api_key = config.get('gemini_api_key', "")
                    self.openai_api_key = config.get('openai_api_key', "")
                    self.claude_api_key = config.get('claude_api_key', "")
                    self.doubao_api_key = config.get('doubao_api_key', "")
                    self.qwen_api_key = config.get('qwen_api_key', "")
                    self.pan_greeting = config.get('pan_greeting', "")
                    self.custom_prompt = config.get('custom_prompt', "")

                    # 加载图层
                    self.layers = []
                    layers_info = config.get('layers', [])
                    for layer_info in layers_info:
                        if os.path.exists(layer_info['path']):
                            layer = WatermarkLayer.from_dict(layer_info)
                            self.layers.append(layer)

                    # 加载文本标注配置
                    text_label_info = config.get('text_label', {})
                    if text_label_info:
                        self.text_label_config.from_dict(text_label_info)

                return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save(self, layers=None, text_label_config=None, stretch=None, resize_enabled=None, resize_height=None):
        """保存配置

        Args:
            layers: WatermarkLayer 列表 (None 表示使用当前值)
            text_label_config: TextLabelConfig 对象 (None 表示使用当前值)
            stretch: 是否拉伸 (None 表示使用当前值)
            resize_enabled: 是否启用输出缩放 (None 表示使用当前值)
            resize_height: 输出缩放目标高度 (None 表示使用当前值)
        """
        try:
            if layers is None:
                layers = self.layers
            if text_label_config is None:
                text_label_config = self.text_label_config
            if stretch is None:
                stretch = self.last_stretch

            layers_info = [layer.to_dict() for layer in layers]

            # 更新缩放配置（如果提供了新值）
            if resize_enabled is not None:
                self.output_resize_enabled = resize_enabled
            if resize_height is not None:
                self.output_resize_height = resize_height

            config = {
                'last_used_directory': self.last_used_directory,
                'save_directory': self.save_directory,
                'last_watermark_directory': self.last_watermark_directory,
                'last_images_directory': self.last_images_directory,
                'last_stretch': stretch,
                'last_images_files': self.last_images_files,
                'ui_theme': self.ui_theme,
                'output_resize_enabled': self.output_resize_enabled,
                'output_resize_height': self.output_resize_height,
                'gemini_api_key': self.gemini_api_key,
                'openai_api_key': self.openai_api_key,
                'claude_api_key': self.claude_api_key,
                'doubao_api_key': self.doubao_api_key,
                'qwen_api_key': self.qwen_api_key,
                'pan_greeting': self.pan_greeting,
                'custom_prompt': self.custom_prompt,
                'layers': layers_info,
                'text_label': text_label_config.to_dict()
            }

            config_path = os.path.join(self.config_dir, self.config_file)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False


class BatchProcessor:
    """批量处理器"""

    @staticmethod
    def process_images(images, image_paths, layers, text_label_config,
                      save_directory, stretch=False,
                      resize_enabled=False, resize_height=1024,
                      progress_callback=None, status_callback=None):
        """批量处理图片

        Args:
            images: PIL.Image 对象列表
            image_paths: 图片路径列表
            layers: WatermarkLayer 列表
            text_label_config: TextLabelConfig 对象
            save_directory: 保存目录
            stretch: 是否拉伸
            resize_enabled: 是否启用输出缩放
            resize_height: 输出缩放目标高度
            progress_callback: 进度回调 func(percentage)
            status_callback: 状态回调 func(message)

        Returns:
            (success, message) tuple
        """
        try:
            total_images = len(images)

            for i, image in enumerate(images):
                filename = os.path.basename(image_paths[i])

                if status_callback:
                    status_callback(f"Processing {i+1}/{total_images}: {filename}")

                # 应用多图层水印
                output = WatermarkEngine.apply_multilayer_watermark(
                    image.copy(),
                    layers,
                    stretch,
                    lambda p: progress_callback(int(p)) if progress_callback else None
                )

                # 应用文本标注
                if text_label_config.enabled:
                    output = draw_text_label(output, filename, text_label_config, index=i+1)

                # 转换为RGB并保存为JPG
                if output.mode == 'RGBA':
                    rgb_image = Image.new('RGB', output.size, (255, 255, 255))
                    rgb_image.paste(output, mask=output.split()[3])
                    output = rgb_image

                # 输出缩放（等比缩放到目标高度）
                if resize_enabled and resize_height > 0 and output.height != resize_height:
                    ratio = resize_height / output.height
                    new_width = int(output.width * ratio)
                    output = output.resize((new_width, resize_height), Image.Resampling.LANCZOS)

                # 保存文件
                filename_without_ext = os.path.splitext(filename)[0]
                output_filename = f"{filename_without_ext}_multilayer.jpg"
                output_path = os.path.join(save_directory, output_filename)
                output.save(output_path, 'JPEG', quality=95, optimize=True)

                # 更新进度
                if progress_callback:
                    progress = 50 + ((i + 1) / total_images) * 50
                    progress_callback(int(progress))

            return True, f"Successfully processed {total_images} images!"

        except Exception as e:
            return False, f"Processing failed: {str(e)}"
