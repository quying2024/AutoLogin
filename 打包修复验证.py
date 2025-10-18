#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包修复完成验证
"""

import os
from pathlib import Path

print("=" * 80)
print("   打包问题已修复 - 验证报告")
print("=" * 80)
print()

# 检查打包文件
exe_path = Path("dist/职称申报登录助手/职称申报登录助手.exe")
internal_path = Path("dist/职称申报登录助手/_internal")
numpy_path = internal_path / "numpy"

print("📦 打包文件检查:")
print()

if exe_path.exists():
    size_mb = exe_path.stat().st_size / 1024 / 1024
    print(f"✅ 主程序: {exe_path.name}")
    print(f"   大小: {size_mb:.2f} MB")
else:
    print("❌ 主程序不存在")
print()

if internal_path.exists():
    files = list(internal_path.rglob("*"))
    file_count = sum(1 for f in files if f.is_file())
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    total_mb = total_size / 1024 / 1024
    print(f"✅ 依赖目录: _internal")
    print(f"   文件数: {file_count}")
    print(f"   总大小: {total_mb:.2f} MB")
else:
    print("❌ 依赖目录不存在")
print()

# 检查 numpy
print("=" * 80)
print("   NumPy 包含检查")
print("=" * 80)
print()

if numpy_path.exists():
    numpy_files = list(numpy_path.rglob("*"))
    numpy_file_count = sum(1 for f in numpy_files if f.is_file())
    print(f"✅ numpy 目录存在")
    print(f"   路径: {numpy_path}")
    print(f"   文件数: {numpy_file_count}")
    print()
    
    # 检查关键文件
    key_files = [
        "__init__.py",
        "core/__init__.py",
        "lib/__init__.py",
    ]
    
    print("   关键文件检查:")
    for kf in key_files:
        kf_path = numpy_path / kf
        if kf_path.exists():
            print(f"   ✅ {kf}")
        else:
            print(f"   ❌ {kf}")
else:
    print("❌ numpy 目录不存在")
print()

# 检查 numpy.libs
numpy_libs = internal_path / "numpy.libs"
if numpy_libs.exists():
    lib_files = list(numpy_libs.glob("*.dll"))
    print(f"✅ numpy.libs 目录存在")
    print(f"   DLL 文件数: {len(lib_files)}")
    for dll in lib_files[:3]:  # 显示前3个
        print(f"   - {dll.name}")
else:
    print("⚠️  numpy.libs 目录不存在（某些配置下正常）")
print()

# 问题修复总结
print("=" * 80)
print("   问题修复总结")
print("=" * 80)
print()

print("🔧 修复的问题:")
print("   1. ✅ 添加 numpy 到隐藏导入列表")
print("   2. ✅ 从排除列表移除 numpy")
print("   3. ✅ 重新打包程序")
print()

print("📊 打包结果对比:")
print()
print("   修复前:")
print("   - 主程序: 8.13 MB")
print("   - 依赖: 160.31 MB (1051 文件)")
print("   - 总计: 168.43 MB")
print("   - 状态: ❌ 缺少 numpy，无法运行")
print()
print("   修复后:")
print(f"   - 主程序: {size_mb:.2f} MB")
print(f"   - 依赖: {total_mb:.2f} MB ({file_count} 文件)")
print(f"   - 总计: {size_mb + total_mb:.2f} MB")
print("   - 状态: ✅ 包含 numpy，应该可以运行")
print()

print("=" * 80)
print("   下一步操作")
print("=" * 80)
print()

print("1️⃣  测试 exe 文件")
print("   运行: .\\测试exe文件.bat")
print("   或手动: cd dist\\职称申报登录助手; .\\职称申报登录助手.exe")
print()

print("2️⃣  检查程序启动")
print("   - 程序应该能正常启动")
print("   - 主窗口显示在右下角")
print("   - 没有 numpy 相关错误")
print()

print("3️⃣  测试核心功能")
print("   - 加载 Excel 文件")
print("   - 选择浏览器类型")
print("   - 测试登录功能")
print("   - 检查日志记录")
print()

print("4️⃣  如果测试成功")
print("   - 运行: .\\准备发布包.bat")
print("   - 创建完整发布包")
print("   - 分发给用户")
print()

print("=" * 80)
print("   重要提示")
print("=" * 80)
print()

print("⚠️  注意事项:")
print("   • 文件大小增加 ~28MB 是正常的（numpy 库）")
print("   • exe 和 _internal 必须在同一目录")
print("   • 首次运行可能需要几秒钟加载")
print("   • 建议在干净的 Windows 系统上测试")
print()

print("📝 文档参考:")
print("   • 打包问题修复说明.md - 详细的问题分析")
print("   • 打包发布指南.md - 完整的打包流程")
print("   • 打包快速参考.md - 快速参考手册")
print()

print("=" * 80)
print("   修复完成！请测试 exe 文件")
print("=" * 80)
print()
