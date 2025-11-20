#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复配置文件中的数据类型
确保 opacity 是整数，blend_mode 是字符串
"""

import json
import os

def fix_config_types(config_path):
    """修复配置文件中的数据类型"""
    print(f"🔧 修复配置文件: {config_path}")

    if not os.path.exists(config_path):
        print(f"⚠️ 配置文件不存在: {config_path}")
        return False

    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 修复图层配置
    layers = config.get('layers', [])
    fixed = False

    for i, layer in enumerate(layers):
        # 修复 opacity
        if 'opacity' in layer:
            old_opacity = layer['opacity']
            new_opacity = int(old_opacity)
            if type(old_opacity) != int:  # 检查类型而不是值
                print(f"  图层 {i+1}: opacity {old_opacity} (type: {type(old_opacity).__name__}) -> {new_opacity} (type: int)")
                layer['opacity'] = new_opacity
                fixed = True

        # 确保 blend_mode 是字符串
        if 'blend_mode' in layer:
            old_mode = layer['blend_mode']
            new_mode = str(old_mode)
            if type(old_mode) != str:
                print(f"  图层 {i+1}: blend_mode 类型转换为字符串")
                layer['blend_mode'] = new_mode
                fixed = True

    if fixed:
        # 保存修复后的配置
        backup_path = config_path + '.backup'
        print(f"  💾 创建备份: {backup_path}")
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print(f"  💾 保存修复后的配置")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print("  ✅ 修复完成")
        return True
    else:
        print("  ℹ️ 配置文件已经是正确的类型")
        return False

if __name__ == "__main__":
    config_path = os.path.join("configs", "multilayer_watermark_config.json")
    fix_config_types(config_path)
