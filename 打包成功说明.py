#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包成功验证和说明
"""

import os

print("=" * 80)
print("   职称申报登录助手 - 打包成功！")
print("=" * 80)
print()

# 检查文件
dist_path = "dist\\职称申报登录助手"
exe_file = os.path.join(dist_path, "职称申报登录助手.exe")

if os.path.exists(exe_file):
    exe_size = os.path.getsize(exe_file)
    print(f"✅ 主程序: 职称申报登录助手.exe")
    print(f"   文件大小: {exe_size / 1024 / 1024:.2f} MB")
    print()
    
    # 统计依赖文件
    internal_path = os.path.join(dist_path, "_internal")
    if os.path.exists(internal_path):
        file_count = sum([len(files) for r, d, files in os.walk(internal_path)])
        total_size = sum([os.path.getsize(os.path.join(r, f)) 
                         for r, d, files in os.walk(internal_path) 
                         for f in files])
        print(f"✅ 依赖文件: _internal 目录")
        print(f"   文件数量: {file_count} 个")
        print(f"   总大小: {total_size / 1024 / 1024:.2f} MB")
        print()
    
    total_size_all = exe_size + total_size
    print(f"📦 打包总大小: {total_size_all / 1024 / 1024:.2f} MB")
    print()
else:
    print("❌ 错误: 未找到 exe 文件")
    print()

print("=" * 80)
print("   发布准备检查")
print("=" * 80)
print()

checks = [
    ("主程序文件", os.path.exists(exe_file)),
    ("依赖目录", os.path.exists(os.path.join(dist_path, "_internal"))),
    ("配置模板", os.path.exists("settings.json.example")),
    ("打包说明", os.path.exists("打包发布指南.md")),
    ("README文档", os.path.exists("README.md")),
]

for name, status in checks:
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {name}")

print()
print("=" * 80)
print("   下一步操作")
print("=" * 80)
print()

print("1. 测试 exe 文件")
print("   cd dist\\职称申报登录助手")
print("   .\\职称申报登录助手.exe")
print()

print("2. 准备发布文件")
print("   - 复制 dist\\职称申报登录助手\\ 目录")
print("   - 添加 settings.json.example")
print("   - 添加 README.md")
print("   - 添加 Excel 模板文件")
print()

print("3. 首次运行配置")
print("   用户需要:")
print("   - 安装 Playwright 浏览器: playwright install chromium")
print("   - 创建 settings.json 配置文件")
print("   - 准备 Excel 数据文件")
print()

print("4. 打包发布")
print("   - 压缩成 ZIP 文件")
print("   - 或创建安装程序")
print()

print("=" * 80)
print("   重要提示")
print("=" * 80)
print()

print("⚠️  注意事项:")
print("   1. exe 文件和 _internal 目录必须在同一目录")
print("   2. 不要删除 _internal 目录中的任何文件")
print("   3. 首次运行可能需要几秒钟加载")
print("   4. 需要确保系统已安装浏览器（Chrome/Edge/Firefox）")
print()

print("📝 文档清单:")
print("   - 打包发布指南.md - 完整的打包和发布说明")
print("   - README.md - 用户使用说明")
print("   - settings.json.example - 配置文件模板")
print()

print("🔧 开发工具:")
print("   - 打包程序.bat - 完整打包流程")
print("   - 快速打包.bat - 快速开发打包")
print("   - autologin.spec - PyInstaller 配置")
print()

print("=" * 80)
print("   打包完成！祝您使用愉快！")
print("=" * 80)
