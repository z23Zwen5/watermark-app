"""
性能测试：展示图片大小对处理速度的影响
"""
import numpy as np
import time
from PIL import Image

def test_memory_allocation():
    """测试内存分配时间"""
    print("📊 测试1：内存分配时间\n")

    sizes = [
        (1920, 1080, "1080p"),
        (2560, 1440, "1440p"),
        (3840, 2160, "4K"),
        (7680, 4320, "8K"),
    ]

    for width, height, name in sizes:
        # 测试创建空数组
        start = time.time()
        arr = np.zeros((height, width, 4), dtype=np.uint8)
        alloc_time = time.time() - start

        # 测试类型转换
        start = time.time()
        arr_float = arr[:, :, :3].astype(np.float32) / 255.0
        convert_time = time.time() - start

        size_mb = (width * height * 4) / (1024 * 1024)
        pixels = width * height / 1_000_000

        print(f"{name:6s} ({width}x{height}): {pixels:.1f}M像素, {size_mb:.1f}MB")
        print(f"  └─ 分配时间: {alloc_time*1000:.2f}ms, 转换时间: {convert_time*1000:.2f}ms\n")


def test_blend_operations():
    """测试混合操作时间"""
    print("\n📊 测试2：混合模式计算时间\n")

    sizes = [
        (1920, 1080, "1080p"),
        (3840, 2160, "4K"),
    ]

    for width, height, name in sizes:
        # 创建测试数组
        base = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        blend = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)

        # 转换为 float32
        start = time.time()
        base_f = base.astype(np.float32) / 255.0
        blend_f = blend.astype(np.float32) / 255.0
        convert_time = time.time() - start

        # Normal 混合
        start = time.time()
        result = blend_f * 0.5 + base_f * 0.5
        normal_time = time.time() - start

        # Overlay 混合
        start = time.time()
        result = np.where(base_f < 0.5,
                         2 * base_f * blend_f,
                         1.0 - 2 * (1.0 - base_f) * (1.0 - blend_f))
        overlay_time = time.time() - start

        # 转换回 uint8
        start = time.time()
        result_uint8 = (np.clip(result, 0, 1) * 255).astype(np.uint8)
        back_convert_time = time.time() - start

        total = convert_time + normal_time + back_convert_time

        print(f"{name} ({width}x{height}):")
        print(f"  ├─ float32转换:  {convert_time*1000:.1f}ms")
        print(f"  ├─ Normal混合:   {normal_time*1000:.1f}ms")
        print(f"  ├─ Overlay混合:  {overlay_time*1000:.1f}ms")
        print(f"  ├─ uint8转换:    {back_convert_time*1000:.1f}ms")
        print(f"  └─ 总计:        {total*1000:.1f}ms\n")


def test_image_resize():
    """测试图片缩放时间"""
    print("\n📊 测试3：图片缩放时间 (LANCZOS vs BILINEAR)\n")

    # 创建小水印
    watermark = Image.new('RGBA', (500, 500), (255, 0, 0, 128))

    target_sizes = [
        (1920, 1080, "1080p"),
        (3840, 2160, "4K"),
    ]

    for width, height, name in target_sizes:
        # LANCZOS
        start = time.time()
        resized_lanczos = watermark.resize((width, height), Image.LANCZOS)
        lanczos_time = time.time() - start

        # BILINEAR
        start = time.time()
        resized_bilinear = watermark.resize((width, height), Image.BILINEAR)
        bilinear_time = time.time() - start

        speedup = lanczos_time / bilinear_time

        print(f"{name} (500x500 → {width}x{height}):")
        print(f"  ├─ LANCZOS:   {lanczos_time*1000:.1f}ms")
        print(f"  ├─ BILINEAR:  {bilinear_time*1000:.1f}ms")
        print(f"  └─ 提速:      {speedup:.1f}x\n")


def simulate_full_pipeline():
    """模拟完整水印处理流程"""
    print("\n📊 测试4：完整流程模拟 (单层水印)\n")

    sizes = [
        (1920, 1080, "1080p"),
        (2560, 1440, "1440p"),
        (3840, 2160, "4K"),
    ]

    watermark = Image.new('RGBA', (500, 500), (255, 0, 0, 128))

    for width, height, name in sizes:
        total_start = time.time()

        # 1. 创建原图
        step_start = time.time()
        image = np.random.randint(0, 255, (height, width, 4), dtype=np.uint8)
        create_time = time.time() - step_start

        # 2. 缩放水印
        step_start = time.time()
        resized_watermark = watermark.resize((width, height), Image.LANCZOS)
        resize_time = time.time() - step_start

        # 3. 创建图层数组
        step_start = time.time()
        layer_array = np.zeros((height, width, 4), dtype=np.uint8)
        layer_array[:, :, :] = np.array(resized_watermark)
        layer_time = time.time() - step_start

        # 4. 类型转换
        step_start = time.time()
        base_rgb = image[:, :, :3].astype(np.float32) / 255.0
        blend_rgb = layer_array[:, :, :3].astype(np.float32) / 255.0
        convert_time = time.time() - step_start

        # 5. 混合计算
        step_start = time.time()
        result_rgb = blend_rgb * 0.5 + base_rgb * 0.5
        blend_time = time.time() - step_start

        # 6. 转换回来
        step_start = time.time()
        result = image.copy()
        result[:, :, :3] = (np.clip(result_rgb, 0, 1) * 255).astype(np.uint8)
        back_time = time.time() - step_start

        total_time = time.time() - total_start
        pixels = width * height / 1_000_000

        print(f"{name} ({width}x{height}, {pixels:.1f}M像素):")
        print(f"  ├─ 创建原图:     {create_time*1000:.1f}ms")
        print(f"  ├─ 缩放水印:     {resize_time*1000:.1f}ms")
        print(f"  ├─ 创建图层:     {layer_time*1000:.1f}ms")
        print(f"  ├─ float转换:    {convert_time*1000:.1f}ms")
        print(f"  ├─ 混合计算:     {blend_time*1000:.1f}ms")
        print(f"  ├─ uint8转换:    {back_time*1000:.1f}ms")
        print(f"  └─ 总计:         {total_time*1000:.1f}ms ({total_time:.2f}秒)\n")


if __name__ == "__main__":
    print("=" * 60)
    print("🔬 Watermark App 性能分析测试")
    print("=" * 60)

    test_memory_allocation()
    test_blend_operations()
    test_image_resize()
    simulate_full_pipeline()

    print("=" * 60)
    print("✅ 测试完成！")
    print("\n结论：图片像素数每翻4倍，处理时间约翻4倍")
    print("      这是线性复杂度 O(width × height) 的典型表现")
    print("=" * 60)
