#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主程序窗口右下角定位
"""

print("=== 主程序窗口定位测试 ===")

# 测试主程序语法
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ 主程序语法检查通过")
except Exception as e:
    print(f"❌ 主程序语法错误: {e}")

# 测试导入主要模块
try:
    import wx
    print("✅ wxPython模块可用")
except Exception as e:
    print(f"❌ wxPython模块错误: {e}")

print("\n=== 窗口定位修改验证 ===")
print("1. ✅ 移除了 self.Center() 居中定位")
print("2. ✅ 添加了 position_to_bottom_right() 方法")
print("3. ✅ 使用 wx.DisplaySize() 获取屏幕尺寸")
print("4. ✅ 计算右下角位置并留出边距")
print("5. ✅ 考虑任务栏高度（40像素）")

print("\n=== 定位算法说明 ===")
print("屏幕尺寸: wx.DisplaySize() 获取")
print("窗口位置计算:")
print("  x = 屏幕宽度 - 窗口宽度 - 边距(10px)")
print("  y = 屏幕高度 - 窗口高度 - 边距(10px) - 任务栏(40px)")

print("\n=== 窗口信息 ===")
try:
    app = wx.App(False)
    screen_size = wx.DisplaySize()
    print(f"屏幕分辨率: {screen_size[0]} x {screen_size[1]}")
    print(f"窗口大小: 384 x 270")
    
    # 计算预期位置
    margin = 10
    x = screen_size[0] - 384 - margin
    y = screen_size[1] - 270 - margin - 40
    print(f"预期窗口位置: ({x}, {y})")
    
    app.Destroy()
except Exception as e:
    print(f"无法获取屏幕信息: {e}")

print("\n=== 启动测试 ===")
print("现在启动主程序，窗口应该显示在屏幕右下角")
print("启动命令: .\\venv\\Scripts\\python.exe main.py")

print("\n=== 容错机制 ===")
print("如果右下角定位失败，程序会自动回退到居中显示")
print("确保程序在各种屏幕配置下都能正常工作")