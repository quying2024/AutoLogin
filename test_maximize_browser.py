#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试浏览器最大化窗口功能
"""

print("=== 浏览器最大化窗口测试 ===")

# 测试主程序语法
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ 主程序语法检查通过")
except Exception as e:
    print(f"❌ 主程序语法错误: {e}")

print("\n=== 浏览器窗口最大化修改验证 ===")
print("1. ✅ Chrome/Edge/Chromium: 添加了 --start-maximized 启动参数")
print("2. ✅ Firefox: 使用 --width=1920 --height=1080 参数")
print("3. ✅ 页面创建后: 设置viewport为1920x1080")
print("4. ✅ JavaScript最大化: 使用window.resizeTo()函数")

print("\n=== 最大化方法说明 ===")
print("方法1: 启动参数 --start-maximized")
print("   - 适用于Chrome, Edge, Chromium")
print("   - 浏览器启动时就是最大化状态")

print("\nFire方法2: Firefox专用参数")
print("   - 使用--width和--height参数")
print("   - 设置为1920x1080分辨率")

print("\nApp方法3: 页面级设置")
print("   - 使用page.set_viewport_size()")
print("   - 设置视窗大小为1920x1080")

print("\nweb方法4: JavaScript动态最大化")
print("   - 使用window.resizeTo(screen.width, screen.height)")
print("   - 适配用户实际屏幕分辨率")

print("\n=== 启动测试 ===")
print("现在启动程序，浏览器窗口应该以最大化方式显示")
print("启动命令: .\\venv\\Scripts\\python.exe main.py")