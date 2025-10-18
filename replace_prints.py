#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将main.py中的print语句替换为log函数调用的脚本
"""

import re

def replace_prints_with_logs(file_path):
    """
    将文件中的print()替换为log()
    
    Args:
        file_path: 要处理的文件路径
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计替换次数
    print_count = len(re.findall(r'print\(', content))
    
    # 替换 print("调试: xxx") 为 log("调试: xxx")
    # 替换 print(f"调试: xxx") 为 log(f"调试: xxx")
    content = re.sub(r'\bprint\(', 'log(', content)
    
    # 保存修改后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已替换 {print_count} 个 print() 调用")
    print(f"✅ 文件已更新: {file_path}")

if __name__ == "__main__":
    replace_prints_with_logs('main.py')
    print("\n提示: 如果需要启用控制台输出，请将 CONSOLE_OUTPUT 设置为 True")
