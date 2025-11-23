"""
Text Label Module for Watermark App
文本标注模块 - 在图片上添加序号或文件名标注

功能：
- 支持序号（1, 2, 3...）或文件名标注
- 自动扫描系统字体（类似 Photoshop）
- 字体下拉选择
- 自动对比色（基于背景颜色）
- 半透明背景（提高可读性）
- 可配置位置/大小/颜色
"""

from PIL import Image, ImageDraw, ImageFont
import os
import colorsys
import platform


def scan_system_fonts():
    """扫描系统已安装字体（类似 Photoshop）

    Returns:
        dict: {字体显示名称: 字体文件路径}
    """
    fonts = {}
    system = platform.system()

    # 定义字体目录
    font_dirs = []
    if system == 'Windows':
        font_dirs = [
            'C:/Windows/Fonts',
            os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Fonts')
        ]
    elif system == 'Darwin':  # macOS
        font_dirs = [
            '/Library/Fonts',
            '/System/Library/Fonts',
            os.path.expanduser('~/Library/Fonts')
        ]
    else:  # Linux
        font_dirs = [
            '/usr/share/fonts',
            '/usr/local/share/fonts',
            os.path.expanduser('~/.fonts'),
            os.path.expanduser('~/.local/share/fonts')
        ]

    # 支持的字体扩展名
    font_extensions = ('.ttf', '.ttc', '.otf')

    # 扫描字体目录
    for font_dir in font_dirs:
        if not os.path.exists(font_dir):
            continue

        try:
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith(font_extensions):
                        font_path = os.path.join(root, file)
                        # 使用文件名（去掉扩展名）作为显示名称
                        font_name = os.path.splitext(file)[0]
                        # 清理字体名称
                        font_name = font_name.replace('_', ' ').replace('-', ' ')
                        fonts[font_name] = font_path
        except Exception as e:
            print(f"⚠️ 扫描字体目录出错 {font_dir}: {e}")

    # 添加常用字体的友好名称映射
    friendly_names = {
        'Arial': 'Arial',
        'msyh': '微软雅黑',
        'simsun': '宋体',
        'simhei': '黑体',
        'PingFang': '苹方',
        'DejaVuSans': 'DejaVu Sans',
        'NotoSans': 'Noto Sans',
    }

    # 应用友好名称
    renamed_fonts = {}
    for font_name, font_path in fonts.items():
        display_name = font_name
        for key, friendly in friendly_names.items():
            if key.lower() in font_name.lower():
                display_name = friendly
                break
        renamed_fonts[display_name] = font_path

    return renamed_fonts


# 全局字体缓存（应用启动时扫描一次）
_SYSTEM_FONTS_CACHE = None

def get_system_fonts():
    """获取系统字体（带缓存）"""
    global _SYSTEM_FONTS_CACHE
    if _SYSTEM_FONTS_CACHE is None:
        print("🔍 正在扫描系统字体...")
        _SYSTEM_FONTS_CACHE = scan_system_fonts()
        print(f"✅ 找到 {len(_SYSTEM_FONTS_CACHE)} 个字体")
    return _SYSTEM_FONTS_CACHE


class TextLabelConfig:
    """文本标注配置类"""

    # 位置常量
    POSITION_TOP_RIGHT = 'top_right'
    POSITION_TOP_LEFT = 'top_left'
    POSITION_BOTTOM_RIGHT = 'bottom_right'
    POSITION_BOTTOM_LEFT = 'bottom_left'
    POSITION_CENTER = 'center'

    # 标注类型
    LABEL_TYPE_NUMBER = 'number'      # 序号 (1, 2, 3...)
    LABEL_TYPE_FILENAME = 'filename'  # 文件名

    # 文字方向常量
    ORIENTATION_HORIZONTAL = 'horizontal'  # 横向排布（左到右）
    ORIENTATION_VERTICAL = 'vertical'      # 竖向排布（上到下）

    def __init__(self):
        # 基础设置
        self.enabled = False
        self.label_type = self.LABEL_TYPE_NUMBER
        self.position = self.POSITION_TOP_RIGHT
        self.orientation = self.ORIENTATION_HORIZONTAL  # 文字方向（横向/竖向）

        # 文本样式
        self.font_size = 3.0  # 字体大小百分比（相对于图片高度）
        self.font_name = None  # 字体名称（从系统字体中选择）
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
            'orientation': self.orientation,
            'font_size': self.font_size,
            'font_name': self.font_name,
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
        self.orientation = config_dict.get('orientation', self.ORIENTATION_HORIZONTAL)

        # 字体大小：兼容旧配置（像素值 > 15 视为旧格式）
        font_size = config_dict.get('font_size', 3.0)
        if font_size > 15:  # 旧配置使用像素值
            # 转换为百分比（基于 1080p 高度）
            self.font_size = round((font_size / 1080) * 100, 1)
            print(f"🔄 转换旧字体大小: {font_size}px → {self.font_size}%")
        else:
            self.font_size = float(font_size)

        self.font_name = config_dict.get('font_name', None)
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

        优先使用用户选择的字体，否则使用默认字体
        """
        cache_key = (self.config.font_name, size)
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        font = None

        # 如果用户选择了字体，尝试加载
        if self.config.font_name:
            system_fonts = get_system_fonts()
            if self.config.font_name in system_fonts:
                font_path = system_fonts[self.config.font_name]
                try:
                    font = ImageFont.truetype(font_path, size)
                    print(f"✅ 加载字体: {self.config.font_name} ({font_path})")
                except Exception as e:
                    print(f"⚠️ 字体加载失败 {self.config.font_name}: {e}")

        # 如果没有选择字体或加载失败，使用默认字体列表
        if font is None:
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

            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, size)
                        print(f"✅ 加载默认字体: {font_path}")
                        break
                    except Exception as e:
                        continue

        # 如果还是没有找到字体，使用 PIL 默认字体
        if font is None:
            print("⚠️ 未找到系统字体，使用默认字体")
            font = ImageFont.load_default()

        self._font_cache[cache_key] = font
        return font

    def get_contrasting_color(self, image, position):
        """获取对比色

        Args:
            image: PIL Image对象
            position: 标注位置 (top_right, top_left, bottom_right, bottom_left, center)

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
        elif position == TextLabelConfig.POSITION_BOTTOM_LEFT:
            box = (0, max(0, height - sample_size), min(width, sample_size), height)
        else:  # CENTER
            # 中心区域采样
            center_x = width // 2
            center_y = height // 2
            half_sample = sample_size // 2
            box = (max(0, center_x - half_sample), max(0, center_y - half_sample),
                   min(width, center_x + half_sample), min(height, center_y + half_sample))

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

        # 根据图片高度计算实际字体像素大小（百分比转像素）
        actual_font_size = int(image.height * (self.config.font_size / 100))
        # 确保字体大小在合理范围内
        actual_font_size = max(12, min(actual_font_size, 500))
        font = self.get_font(actual_font_size)

        # 计算文本尺寸（根据文字方向）
        # 用于存储文本边界框的偏移量
        text_bbox_offset_x = 0
        text_bbox_offset_y = 0

        if self.config.orientation == TextLabelConfig.ORIENTATION_VERTICAL:
            # 竖向排布：逐字符测量，垂直堆叠
            char_heights = []
            max_char_width = 0
            char_bboxes = []

            for char in label_text:
                try:
                    bbox = draw.textbbox((0, 0), char, font=font)
                    char_width = bbox[2] - bbox[0]
                    char_height = bbox[3] - bbox[1]
                    char_bboxes.append(bbox)
                except AttributeError:
                    char_width, char_height = draw.textsize(char, font=font)
                    char_bboxes.append(None)

                char_heights.append(char_height)
                max_char_width = max(max_char_width, char_width)

            # 竖向排布的总尺寸
            text_width = max_char_width
            text_height = sum(char_heights)

            # 获取第一个字符的偏移量（用于对齐）
            if char_bboxes and char_bboxes[0] is not None:
                text_bbox_offset_x = char_bboxes[0][0]
                text_bbox_offset_y = char_bboxes[0][1]
        else:
            # 横向排布（默认）
            try:
                bbox = draw.textbbox((0, 0), label_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                # 保存偏移量，用于对齐背景框和文字
                text_bbox_offset_x = bbox[0]
                text_bbox_offset_y = bbox[1]
            except AttributeError:
                # 旧版本 Pillow 的兼容方案
                text_width, text_height = draw.textsize(label_text, font=font)
                # textsize 没有偏移量

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
        elif self.config.position == TextLabelConfig.POSITION_BOTTOM_LEFT:
            x = self.config.margin_x
            y = height - self.config.margin_y - box_height
        else:  # CENTER
            x = (width - box_width) // 2
            y = (height - box_height) // 2

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

        # 绘制文本（减去偏移量以对齐背景框）
        text_color_with_alpha = text_color + (255,)  # 文字不透明

        if self.config.orientation == TextLabelConfig.ORIENTATION_VERTICAL:
            # 竖向排布：逐字符绘制
            text_x = x + self.config.padding_x - text_bbox_offset_x
            text_y = y + self.config.padding_y - text_bbox_offset_y

            for i, char in enumerate(label_text):
                draw.text((text_x, text_y), char, fill=text_color_with_alpha, font=font)

                # 计算下一个字符的Y位置
                try:
                    char_bbox = draw.textbbox((0, 0), char, font=font)
                    char_height = char_bbox[3] - char_bbox[1]
                except AttributeError:
                    _, char_height = draw.textsize(char, font=font)

                text_y += char_height
        else:
            # 横向排布（默认）
            # 减去偏移量，使文字和背景框完美对齐
            text_x = x + self.config.padding_x - text_bbox_offset_x
            text_y = y + self.config.padding_y - text_bbox_offset_y
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
