#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文本标注的所有位置和方向组合
"""

from PIL import Image, ImageDraw
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from text_label_module import TextLabelConfig, TextLabelDrawer


def create_test_image(width=800, height=600):
    """创建测试图片（渐变背景）"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # 创建渐变背景
    for y in range(height):
        # 从深蓝到浅蓝的渐变
        brightness = int(255 * y / height)
        color = (0, brightness // 2, brightness)
        draw.line([(0, y), (width, y)], fill=color)

    return image


def test_all_positions_and_orientations():
    """测试所有位置和方向组合"""
    print("🧪 测试文本标注的所有位置和方向组合\n")

    # 创建测试图片
    test_image = create_test_image()

    # 所有位置
    positions = [
        ('top_left', '左上'),
        ('top_right', '右上'),
        ('bottom_left', '左下'),
        ('bottom_right', '右下'),
        ('center', '中间')
    ]

    # 所有方向
    orientations = [
        ('horizontal', '横向'),
        ('vertical', '竖向')
    ]

    # 创建输出目录
    output_dir = 'test_output'
    os.makedirs(output_dir, exist_ok=True)

    # 测试每个组合
    for pos_key, pos_name in positions:
        for orient_key, orient_name in orientations:
            print(f"📝 测试: {pos_name} + {orient_name}")

            # 创建配置
            config = TextLabelConfig()
            config.enabled = True
            config.label_type = TextLabelConfig.LABEL_TYPE_FILENAME
            config.position = pos_key
            config.orientation = orient_key
            config.font_size = 5.0  # 5% of image height
            config.auto_contrast = True

            # 绘制标注
            drawer = TextLabelDrawer(config)
            result = drawer.draw_text_label(test_image.copy(), "测试Test123", index=None)

            # 保存测试图片
            output_filename = f"test_{pos_key}_{orient_key}.png"
            output_path = os.path.join(output_dir, output_filename)
            result.save(output_path)

            print(f"   ✅ 保存: {output_path}")

    print(f"\n✨ 所有测试完成！结果保存在 '{output_dir}/' 目录")
    print(f"📊 共生成 {len(positions) * len(orientations)} 张测试图片")


def test_config_serialization():
    """测试配置序列化"""
    print("\n🧪 测试配置序列化\n")

    # 创建配置
    config = TextLabelConfig()
    config.enabled = True
    config.position = 'center'
    config.orientation = 'vertical'
    config.font_size = 3.5

    # 序列化
    config_dict = config.to_dict()
    print("📤 序列化配置:")
    print(f"   position: {config_dict['position']}")
    print(f"   orientation: {config_dict['orientation']}")
    print(f"   font_size: {config_dict['font_size']}")

    # 反序列化
    new_config = TextLabelConfig()
    new_config.from_dict(config_dict)
    print("\n📥 反序列化配置:")
    print(f"   position: {new_config.position}")
    print(f"   orientation: {new_config.orientation}")
    print(f"   font_size: {new_config.font_size}")

    # 验证
    assert new_config.position == config.position, "位置配置不匹配"
    assert new_config.orientation == config.orientation, "方向配置不匹配"
    assert new_config.font_size == config.font_size, "字体大小配置不匹配"

    print("\n✅ 配置序列化测试通过！")


if __name__ == "__main__":
    print("="*60)
    print("🎯 Text Label Module - 位置和方向测试")
    print("="*60 + "\n")

    try:
        # 测试配置序列化
        test_config_serialization()

        # 测试所有位置和方向组合
        test_all_positions_and_orientations()

        print("\n" + "="*60)
        print("✅ 所有测试通过！")
        print("="*60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
