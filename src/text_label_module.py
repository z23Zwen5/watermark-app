"""
Text Label Module for Watermark App
文本标注模块 - 在图片上添加序号或文件名标注

功能：
- 支持序号（1, 2, 3...）或文件名标注
- 智能字体选择（中英文自适应）
- 自动对比色（基于背景颜色）
- 半透明背景（提高可读性）
- 可配置位置/大小/颜色
"""

from PIL import Image, ImageDraw, ImageFont
import os
import colorsys


class TextLabelConfig:
    """文本标注配置类"""

    # 位置常量
    POSITION_TOP_RIGHT = 'top_right'
    POSITION_TOP_LEFT = 'top_left'
    POSITION_BOTTOM_RIGHT = 'bottom_right'
    POSITION_BOTTOM_LEFT = 'bottom_left'

    # 标注类型
    LABEL_TYPE_NUMBER = 'number'      # 序号 (1, 2, 3...)
    LABEL_TYPE_FILENAME = 'filename'  # 文件名

    def __init__(self):
        # 基础设置
        self.enabled = False
        self.label_type = self.LABEL_TYPE_NUMBER
        self.position = self.POSITION_TOP_RIGHT

        # 文本样式
        self.font_size = 36
        self.text_color = (255, 255, 255)  # 白色
        self.auto_contrast = True  # 自动对比色

        # 背景样式
        self.background_enabled = True
        self.background_color = (0, 0, 0)  # 黑色
        self.background_opacity = 128  # 半透明 (0-255)

        # 边距
        self.margin_x = 20
        self.margin_y = 20
        self.padding_x = 15
        self.padding_y = 10

    def to_dict(self):
        """转换为字典（用于保存配置）"""
        return {
            'enabled': self.enabled,
            'label_type': self.label_type,
            'position': self.position,
            'font_size': self.font_size,
            'text_color': list(self.text_color),
            'auto_contrast': self.auto_contrast,
            'background_enabled': self.background_enabled,
            'background_color': list(self.background_color),
            'background_opacity': self.background_opacity,
            'margin_x': self.margin_x,
            'margin_y': self.margin_y,
            'padding_x': self.padding_x,
            'padding_y': self.padding_y,
        }

    def from_dict(self, config_dict):
        """从字典加载配置"""
        self.enabled = config_dict.get('enabled', False)
        self.label_type = config_dict.get('label_type', self.LABEL_TYPE_NUMBER)
        self.position = config_dict.get('position', self.POSITION_TOP_RIGHT)
        self.font_size = config_dict.get('font_size', 36)
        self.text_color = tuple(config_dict.get('text_color', [255, 255, 255]))
        self.auto_contrast = config_dict.get('auto_contrast', True)
        self.background_enabled = config_dict.get('background_enabled', True)
        self.background_color = tuple(config_dict.get('background_color', [0, 0, 0]))
        self.background_opacity = config_dict.get('background_opacity', 128)
        self.margin_x = config_dict.get('margin_x', 20)
        self.margin_y = config_dict.get('margin_y', 20)
        self.padding_x = config_dict.get('padding_x', 15)
        self.padding_y = config_dict.get('padding_y', 10)


class TextLabelDrawer:
    """文本标注绘制器"""

    def __init__(self, config: TextLabelConfig):
        self.config = config
        self._font_cache = {}

    def get_font(self, size):
        """获取字体（带缓存）

        尝试加载系统字体，优先使用支持中文的字体
        """
        if size in self._font_cache:
            return self._font_cache[size]

        # 常见的中文字体路径（按优先级）
        font_paths = [
            # Windows
            "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",    # 宋体
            "C:/Windows/Fonts/simhei.ttf",    # 黑体
            "C:/Windows/Fonts/arial.ttf",     # Arial
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",  # Noto CJK
            # macOS
            "/System/Library/Fonts/PingFang.ttc",  # 苹方
            "/Library/Fonts/Arial.ttf",
        ]

        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, size)
                    print(f"✅ 加载字体: {font_path}")
                    break
                except Exception as e:
                    print(f"⚠️ 字体加载失败 {font_path}: {e}")
                    continue

        # 如果没有找到字体，使用默认字体
        if font is None:
            print("⚠️ 未找到系统字体，使用默认字体")
            font = ImageFont.load_default()

        self._font_cache[size] = font
        return font

    def get_contrasting_color(self, image, position):
        """获取对比色

        Args:
            image: PIL Image对象
            position: 标注位置 (top_right, top_left, bottom_right, bottom_left)

        Returns:
            (text_color, bg_color) 元组
        """
        # 采样区域大小
        sample_size = 100
        width, height = image.size

        # 根据位置确定采样区域
        if position == TextLabelConfig.POSITION_TOP_RIGHT:
            box = (max(0, width - sample_size), 0, width, min(height, sample_size))
        elif position == TextLabelConfig.POSITION_TOP_LEFT:
            box = (0, 0, min(width, sample_size), min(height, sample_size))
        elif position == TextLabelConfig.POSITION_BOTTOM_RIGHT:
            box = (max(0, width - sample_size), max(0, height - sample_size), width, height)
        else:  # BOTTOM_LEFT
            box = (0, max(0, height - sample_size), min(width, sample_size), height)

        # 裁剪并转换为RGB
        region = image.crop(box)
        if region.mode != 'RGB':
            region = region.convert('RGB')

        # 计算平均颜色
        pixels = list(region.getdata())
        avg_r = sum(p[0] for p in pixels) / len(pixels)
        avg_g = sum(p[1] for p in pixels) / len(pixels)
        avg_b = sum(p[2] for p in pixels) / len(pixels)

        # 计算亮度
        brightness = (avg_r * 299 + avg_g * 587 + avg_b * 114) / 1000

        # 根据亮度选择对比色
        if brightness > 128:
            # 背景较亮，使用深色文字
            text_color = (0, 0, 0)  # 黑色
            bg_color = (255, 255, 255)  # 白色背景
        else:
            # 背景较暗，使用浅色文字
            text_color = (255, 255, 255)  # 白色
            bg_color = (0, 0, 0)  # 黑色背景

        return text_color, bg_color

    def draw_text_label(self, image, text, index=None):
        """在图片上绘制文本标注

        Args:
            image: PIL Image对象
            text: 要显示的文本（文件名）
            index: 序号（如果 label_type 为 number）

        Returns:
            处理后的 PIL Image对象
        """
        if not self.config.enabled:
            return image

        # 确保图片是RGBA模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 创建绘图对象
        # 使用透明图层来绘制，这样可以控制背景透明度
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # 准备文本
        if self.config.label_type == TextLabelConfig.LABEL_TYPE_NUMBER:
            if index is not None:
                label_text = str(index)
            else:
                label_text = "?"
        else:  # FILENAME
            # 移除扩展名
            label_text = os.path.splitext(text)[0]

        # 获取字体
        font = self.get_font(self.config.font_size)

        # 获取文本边界框（使用 textbbox）
        try:
            bbox = draw.textbbox((0, 0), label_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 旧版本 Pillow 的兼容方案
            text_width, text_height = draw.textsize(label_text, font=font)

        # 计算背景框尺寸
        box_width = text_width + 2 * self.config.padding_x
        box_height = text_height + 2 * self.config.padding_y

        # 计算位置
        width, height = image.size
        if self.config.position == TextLabelConfig.POSITION_TOP_RIGHT:
            x = width - self.config.margin_x - box_width
            y = self.config.margin_y
        elif self.config.position == TextLabelConfig.POSITION_TOP_LEFT:
            x = self.config.margin_x
            y = self.config.margin_y
        elif self.config.position == TextLabelConfig.POSITION_BOTTOM_RIGHT:
            x = width - self.config.margin_x - box_width
            y = height - self.config.margin_y - box_height
        else:  # BOTTOM_LEFT
            x = self.config.margin_x
            y = height - self.config.margin_y - box_height

        # 获取颜色
        if self.config.auto_contrast:
            text_color, bg_color = self.get_contrasting_color(image, self.config.position)
        else:
            text_color = self.config.text_color
            bg_color = self.config.background_color

        # 绘制背景框
        if self.config.background_enabled:
            bg_color_with_alpha = bg_color + (self.config.background_opacity,)
            draw.rectangle(
                [x, y, x + box_width, y + box_height],
                fill=bg_color_with_alpha
            )

        # 绘制文本
        text_x = x + self.config.padding_x
        text_y = y + self.config.padding_y
        text_color_with_alpha = text_color + (255,)  # 文字不透明
        draw.text((text_x, text_y), label_text, fill=text_color_with_alpha, font=font)

        # 合并图层
        result = Image.alpha_composite(image, overlay)

        return result


def draw_text_label(image, text, config: TextLabelConfig, index=None):
    """便捷函数：在图片上绘制文本标注

    Args:
        image: PIL Image对象
        text: 要显示的文本（文件名）
        config: TextLabelConfig配置对象
        index: 序号（如果 label_type 为 number）

    Returns:
        处理后的 PIL Image对象
    """
    drawer = TextLabelDrawer(config)
    return drawer.draw_text_label(image, text, index)


# 测试代码
if __name__ == "__main__":
    print("🧪 Text Label Module 测试")

    # 创建测试配置
    config = TextLabelConfig()
    config.enabled = True
    config.label_type = TextLabelConfig.LABEL_TYPE_NUMBER
    config.position = TextLabelConfig.POSITION_TOP_RIGHT
    config.font_size = 48
    config.auto_contrast = True

    # 打印配置
    print("\n配置信息:")
    print(f"  启用: {config.enabled}")
    print(f"  标注类型: {config.label_type}")
    print(f"  位置: {config.position}")
    print(f"  字体大小: {config.font_size}")
    print(f"  自动对比色: {config.auto_contrast}")

    # 测试字体加载
    drawer = TextLabelDrawer(config)
    font = drawer.get_font(36)
    print(f"\n字体加载测试: {'成功' if font else '失败'}")

    print("\n✅ 模块测试完成")
