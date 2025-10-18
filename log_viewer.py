#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志查看工具
用于查看和分析应用日志
"""

import os
from pathlib import Path
from datetime import datetime, timedelta

class LogViewer:
    """日志查看器"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
    
    def list_log_files(self):
        """列出所有日志文件"""
        if not self.log_dir.exists():
            print("日志目录不存在")
            return []
        
        log_files = sorted(self.log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        return log_files
    
    def show_log_files(self):
        """显示所有日志文件列表"""
        log_files = self.list_log_files()
        
        if not log_files:
            print("没有找到日志文件")
            return
        
        print("=" * 70)
        print("日志文件列表".center(70))
        print("=" * 70)
        print(f"{'序号':<6}{'文件名':<30}{'大小':<12}{'修改时间':<22}")
        print("-" * 70)
        
        for idx, log_file in enumerate(log_files, 1):
            size = log_file.stat().st_size
            size_str = self._format_size(size)
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{idx:<6}{log_file.name:<30}{size_str:<12}{mtime_str:<22}")
        
        print("=" * 70)
    
    def view_latest_log(self, lines=50):
        """
        查看最新日志文件的末尾内容
        
        Args:
            lines: 显示行数，默认50行
        """
        log_files = self.list_log_files()
        
        if not log_files:
            print("没有找到日志文件")
            return
        
        latest_log = log_files[0]
        self._view_log_tail(latest_log, lines)
    
    def view_log_by_date(self, date_str=None, lines=None):
        """
        查看指定日期的日志
        
        Args:
            date_str: 日期字符串，格式：YYYY-MM-DD，默认今天
            lines: 显示行数，None表示显示全部
        """
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        log_file = self.log_dir / f"autologin_{date_str}.log"
        
        if not log_file.exists():
            print(f"未找到 {date_str} 的日志文件")
            return
        
        if lines:
            self._view_log_tail(log_file, lines)
        else:
            self._view_full_log(log_file)
    
    def search_logs(self, keyword, days=7):
        """
        搜索包含关键词的日志
        
        Args:
            keyword: 搜索关键词
            days: 搜索最近几天的日志，默认7天
        """
        print(f"搜索关键词: {keyword}")
        print("=" * 70)
        
        found_count = 0
        
        # 获取日期范围内的日志文件
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            log_file = self.log_dir / f"autologin_{date_str}.log"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if keyword.lower() in line.lower():
                            found_count += 1
                            print(f"[{log_file.name}:{line_num}] {line.rstrip()}")
        
        print("=" * 70)
        print(f"共找到 {found_count} 条匹配记录")
    
    def get_log_stats(self):
        """获取日志统计信息"""
        log_files = self.list_log_files()
        
        if not log_files:
            print("没有找到日志文件")
            return
        
        print("=" * 70)
        print("日志统计信息".center(70))
        print("=" * 70)
        
        total_size = 0
        total_lines = 0
        error_count = 0
        warning_count = 0
        
        for log_file in log_files:
            size = log_file.stat().st_size
            total_size += size
            
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines += len(lines)
                
                for line in lines:
                    if 'ERROR' in line:
                        error_count += 1
                    elif 'WARNING' in line:
                        warning_count += 1
        
        print(f"日志文件数量: {len(log_files)}")
        print(f"总大小: {self._format_size(total_size)}")
        print(f"总行数: {total_lines}")
        print(f"错误数量: {error_count}")
        print(f"警告数量: {warning_count}")
        print("=" * 70)
    
    def _view_log_tail(self, log_file, lines):
        """查看日志文件的末尾"""
        print(f"\n{'=' * 70}")
        print(f"查看日志: {log_file.name} (最后 {lines} 行)".center(70))
        print("=" * 70)
        
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            tail_lines = all_lines[-lines:]
            
            for line in tail_lines:
                print(line.rstrip())
        
        print("=" * 70)
    
    def _view_full_log(self, log_file):
        """查看完整日志文件"""
        print(f"\n{'=' * 70}")
        print(f"查看日志: {log_file.name} (完整内容)".center(70))
        print("=" * 70)
        
        with open(log_file, 'r', encoding='utf-8') as f:
            print(f.read())
        
        print("=" * 70)
    
    @staticmethod
    def _format_size(size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"


def main():
    """主函数"""
    viewer = LogViewer()
    
    print("\n职称申报登录助手 - 日志查看工具")
    print("=" * 70)
    print("1. 查看日志文件列表")
    print("2. 查看最新日志（最后50行）")
    print("3. 查看今天的完整日志")
    print("4. 搜索日志")
    print("5. 日志统计")
    print("0. 退出")
    print("=" * 70)
    
    while True:
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == '1':
            viewer.show_log_files()
        
        elif choice == '2':
            viewer.view_latest_log(50)
        
        elif choice == '3':
            viewer.view_log_by_date()
        
        elif choice == '4':
            keyword = input("请输入搜索关键词: ").strip()
            if keyword:
                viewer.search_logs(keyword)
        
        elif choice == '5':
            viewer.get_log_stats()
        
        elif choice == '0':
            print("退出日志查看工具")
            break
        
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()
