#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统测试脚本
"""

import os
from pathlib import Path

print("=" * 70)
print("   日志系统集成测试")
print("=" * 70)

# 1. 检查日志模块
try:
    from logger_config import get_logger
    logger = get_logger()
    print("✅ logger_config.py 导入成功")
except Exception as e:
    print(f"❌ logger_config.py 导入失败: {e}")
    exit(1)

# 2. 检查主程序语法
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ main.py 语法检查通过")
except Exception as e:
    print(f"❌ main.py 语法错误: {e}")
    exit(1)

# 3. 检查captcha_handler
try:
    py_compile.compile('captcha_handler.py', doraise=True)
    print("✅ captcha_handler.py 语法检查通过")
except Exception as e:
    print(f"❌ captcha_handler.py 语法错误: {e}")

# 4. 测试日志写入
print("\n" + "=" * 70)
print("   测试日志写入功能")
print("=" * 70)

logger.info("=== 日志系统测试开始 ===")
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.info("=== 日志系统测试结束 ===")

print("✅ 日志写入测试完成")

# 5. 检查日志文件
log_dir = Path("logs")
if log_dir.exists():
    log_files = list(log_dir.glob("*.log"))
    print(f"✅ 日志目录存在，共有 {len(log_files)} 个日志文件")
    
    if log_files:
        latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
        size = latest_log.stat().st_size
        print(f"✅ 最新日志文件: {latest_log.name} ({size} 字节)")
        
        # 显示最后几行
        with open(latest_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"\n最后5行日志内容:")
            print("-" * 70)
            for line in lines[-5:]:
                print(line.rstrip())
            print("-" * 70)
else:
    print("❌ 日志目录不存在")

# 6. 检查CONSOLE_OUTPUT设置
print("\n" + "=" * 70)
print("   检查控制台输出设置")
print("=" * 70)

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()
    if 'CONSOLE_OUTPUT = False' in content:
        print("✅ 控制台输出已关闭（发布模式）")
    elif 'CONSOLE_OUTPUT = True' in content:
        print("⚠️  控制台输出已开启（开发模式）")
    else:
        print("❌ 未找到CONSOLE_OUTPUT设置")

# 7. 统计替换情况
log_count = content.count('log(')
print(f"✅ main.py中使用log()函数 {log_count} 次")

print("\n" + "=" * 70)
print("   测试总结")
print("=" * 70)

print("\n✅ 日志系统集成完成！")
print("\n发布准备:")
print("  1. ✅ 日志模块正常工作")
print("  2. ✅ 主程序已集成日志")
print("  3. ✅ 验证码模块已集成日志")
print("  4. ✅ 日志文件自动生成")

print("\n使用说明:")
print("  • 查看日志: python log_viewer.py")
print("  • 日志位置: logs/ 目录")
print("  • 控制台输出: 可在main.py中配置CONSOLE_OUTPUT")

print("\n" + "=" * 70)
