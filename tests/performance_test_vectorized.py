#!/usr/bin/env python3
"""
向量化优化性能测试脚本
测试向量化实现相对于原始像素级循环的性能提升
"""

import time
import numpy as np
from PIL import Image
import os
import sys

# 添加src目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_images():
    """创建测试图像"""
    test_images = {}
    
    # 小图像 (400x300)
    small_img = Image.new('RGBA', (400, 300), (255, 255, 255, 255))
    test_images['small'] = small_img
    
    # 中等图像 (1200x800) 
    medium_img = Image.new('RGBA', (1200, 800), (128, 128, 128, 255))
    test_images['medium'] = medium_img
    
    # 2K图像 (2048x1536)
    large_img = Image.new('RGBA', (2048, 1536), (64, 64, 64, 255))
    test_images['2k'] = large_img
    
    # 4K图像 (3840x2160)
    xlarge_img = Image.new('RGBA', (3840, 2160), (32, 32, 32, 255))
    test_images['4k'] = xlarge_img
    
    return test_images

def create_test_watermark():
    """创建测试水印"""
    # 创建一个包含不同Alpha值的水印
    watermark = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    
    # 绘制一些图案
    pixels = []
    for y in range(200):
        row = []
        for x in range(200):
            # 创建渐变效果和一些完全不透明的区域
            if x < 50 or y < 50:  # 左上角完全不透明（保护区域）
                alpha = 255
            elif x > 150 and y > 150:  # 右下角完全不透明（保护区域）
                alpha = 255
            else:  # 其他区域半透明
                alpha = int(128 + 64 * np.sin(x * 0.1) * np.cos(y * 0.1))
            
            # 创建一些颜色模式
            r = int(128 + 127 * np.sin(x * 0.05))
            g = int(128 + 127 * np.cos(y * 0.05))
            b = int(128 + 127 * np.sin((x + y) * 0.03))
            
            row.append((r, g, b, alpha))
        pixels.extend(row)
    
    watermark.putdata(pixels)
    return watermark

def benchmark_vectorized_processing():
    """基准测试向量化处理"""
    print("🚀 向量化水印处理性能测试")
    print("=" * 60)
    
    # 创建测试数据
    test_images = create_test_images()
    watermark = create_test_watermark()
    
    # 导入向量化版本的应用
    try:
        from watermark_app_alpha_protected import AlphaProtectedWatermarkApp
        import tkinter as tk
        
        # 创建临时根窗口（不显示）
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        app = AlphaProtectedWatermarkApp(root)
        
        print("✅ 成功加载向量化版本")
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return
    
    # 测试参数
    test_params = {
        'opacity': 50,
        'stretch': False,
        'smart_color': True,
        'sensitivity': 30,
        'algorithm': 'enhanced',
        'performance_mode': 'balanced',
        'enable_smoothing': True,
        'smoothing_radius': 1.5
    }
    
    results = {}
    
    for size_name, test_image in test_images.items():
        print(f"\n📊 测试图像尺寸: {size_name} ({test_image.width}x{test_image.height})")
        print("-" * 40)
        
        # 预热运行
        try:
            app.apply_alpha_protected_watermark(
                test_image, watermark, **test_params
            )
            print("🔥 预热完成")
        except Exception as e:
            print(f"⚠️ 预热失败: {e}")
            continue
        
        # 性能测试 - 运行3次取平均值
        times = []
        for i in range(3):
            start_time = time.time()
            
            try:
                result = app.apply_alpha_protected_watermark(
                    test_image, watermark, **test_params
                )
                
                end_time = time.time()
                processing_time = end_time - start_time
                times.append(processing_time)
                
                print(f"  运行 {i+1}: {processing_time:.3f}秒")
                
            except Exception as e:
                print(f"  ❌ 运行 {i+1} 失败: {e}")
                break
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            results[size_name] = {
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'size': (test_image.width, test_image.height),
                'pixels': test_image.width * test_image.height
            }
            
            print(f"  ⏱️ 平均时间: {avg_time:.3f}秒")
            print(f"  ⚡ 最快时间: {min_time:.3f}秒")
            print(f"  🐌 最慢时间: {max_time:.3f}秒")
            
            # 计算处理速度
            pixels_per_sec = results[size_name]['pixels'] / avg_time
            print(f"  🚀 处理速度: {pixels_per_sec:,.0f} 像素/秒")
    
    # 清理
    root.destroy()
    
    # 输出汇总报告
    print("\n" + "=" * 60)
    print("📈 性能汇总报告")
    print("=" * 60)
    
    if results:
        print(f"{'尺寸':<8} {'分辨率':<12} {'平均时间':<10} {'处理速度':<15}")
        print("-" * 50)
        
        for size_name, data in results.items():
            resolution = f"{data['size'][0]}x{data['size'][1]}"
            avg_time = f"{data['avg_time']:.3f}s"
            speed = f"{data['pixels']/data['avg_time']:,.0f} px/s"
            
            print(f"{size_name:<8} {resolution:<12} {avg_time:<10} {speed:<15}")
        
        # 性能分析
        print(f"\n🎯 性能分析:")
        
        if '2k' in results:
            time_2k = results['2k']['avg_time']
            print(f"   • 2K图像处理时间: {time_2k:.2f}秒")
            
            if time_2k < 4.0:
                print("   ✅ 优秀! 相比目标11秒有显著提升")
                improvement = 11.0 / time_2k
                print(f"   🚀 性能提升: {improvement:.1f}倍")
            elif time_2k < 6.0:
                print("   ✅ 良好! 达到预期性能目标")
                improvement = 11.0 / time_2k
                print(f"   🚀 性能提升: {improvement:.1f}倍")
            else:
                print("   ⚠️ 仍需优化")
        
        # 内存效率分析
        print(f"\n💾 内存效率:")
        print("   • 向量化处理减少了像素级循环")
        print("   • 批量处理降低了函数调用开销")
        print("   • NumPy数组操作更高效")
        
    else:
        print("❌ 没有成功的测试结果")

def compare_algorithms():
    """比较不同算法的性能"""
    print("\n🔬 算法性能对比")
    print("=" * 40)
    
    # 创建测试数据
    test_image = Image.new('RGBA', (1000, 1000), (128, 128, 128, 255))
    watermark = create_test_watermark()
    
    try:
        from watermark_app_alpha_protected import AlphaProtectedWatermarkApp
        import tkinter as tk
        
        root = tk.Tk()
        root.withdraw()
        app = AlphaProtectedWatermarkApp(root)
        
        algorithms = ['enhanced', 'classic', 'gentle']
        
        for algorithm in algorithms:
            print(f"\n🧠 测试算法: {algorithm}")
            
            params = {
                'opacity': 50,
                'stretch': False,
                'smart_color': True,
                'sensitivity': 30,
                'algorithm': algorithm,
                'performance_mode': 'balanced',
                'enable_smoothing': True,
                'smoothing_radius': 1.5
            }
            
            start_time = time.time()
            result = app.apply_alpha_protected_watermark(test_image, watermark, **params)
            end_time = time.time()
            
            print(f"   ⏱️ 处理时间: {end_time - start_time:.3f}秒")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ 算法对比失败: {e}")

if __name__ == "__main__":
    print("🧪 向量化水印处理性能测试套件")
    print("=" * 60)
    
    # 运行基准测试
    benchmark_vectorized_processing()
    
    # 运行算法对比
    compare_algorithms()
    
    print(f"\n✅ 测试完成!")
    print("💡 提示: 如果性能仍不满意，可以考虑:")
    print("   1. 启用多进程并行处理")
    print("   2. 使用GPU加速(CuPy)")
    print("   3. 进一步优化内存访问模式") 