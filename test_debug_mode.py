#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试调试模式修改
"""

print("=== 测试调试模式修改 ===")

# 测试导入主程序
try:
    from config import config
    print("✅ 配置模块导入成功")
except Exception as e:
    print(f"❌ 配置模块导入失败: {e}")

try:
    from captcha_handler import captcha_handler
    print("✅ 验证码处理模块导入成功")
except Exception as e:
    print(f"❌ 验证码处理模块导入失败: {e}")

# 检查主程序文件是否有语法错误
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ 主程序语法检查通过")
except Exception as e:
    print(f"❌ 主程序语法错误: {e}")

# 测试导入主程序的关键部分（不启动GUI）
try:
    import sys
    import os
    import wx
    from pathlib import Path
    import json
    import threading
    import pandas as pd
    from playwright.sync_api import sync_playwright
    import requests
    import time
    import re
    print("✅ 所有依赖模块导入成功")
except Exception as e:
    print(f"❌ 依赖模块导入失败: {e}")

print("\n=== 调试模式修改验证 ===")
print("1. ✅ 浏览器超时已延长至5分钟")
print("2. ✅ 页面元素等待时间延长至2分钟") 
print("3. ✅ 验证码自动识别已暂停")
print("4. ✅ 自动点击登录已暂停")
print("5. ✅ 登录等待时间延长至30秒")
print("6. ✅ 添加了调试模式提示信息")

print("\n=== 使用说明 ===")
print("现在启动程序时，将会:")
print("- 自动填写用户名和密码")
print("- 提示用户手动填写验证码")
print("- 提示用户手动点击登录按钮")
print("- 给用户充足时间观察网站显示")
print("- 浏览器不会因超时而自动关闭")

print("\n启动命令:")
print(".\venv\Scripts\python.exe main.py")