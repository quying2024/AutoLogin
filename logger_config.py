#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置模块
为职称申报登录助手提供日志功能
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class LoggerConfig:
    """日志配置类"""
    
    def __init__(self, log_dir="logs", app_name="autologin"):
        """
        初始化日志配置
        
        Args:
            log_dir: 日志文件存放目录
            app_name: 应用名称，用于日志文件命名
        """
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.logger = None
        
        # 确保日志目录存在
        self.log_dir.mkdir(exist_ok=True)
        
        # 初始化日志
        self._setup_logger()
    
    def _setup_logger(self):
        """设置日志记录器"""
        # 创建logger
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # 清除已有的处理器（避免重复）
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 生成日志文件名（按日期）
        log_filename = self._get_log_filename()
        
        # 创建文件处理器
        file_handler = logging.FileHandler(
            log_filename,
            encoding='utf-8',
            mode='a'  # 追加模式
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        
        # 防止日志传播到根logger（避免重复输出）
        self.logger.propagate = False
    
    def _get_log_filename(self):
        """
        获取日志文件名（按日期）
        
        Returns:
            日志文件完整路径
        """
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"{self.app_name}_{today}.log"
        return self.log_dir / filename
    
    def get_logger(self):
        """
        获取logger实例
        
        Returns:
            配置好的logger对象
        """
        return self.logger
    
    def debug(self, message):
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录CRITICAL级别日志"""
        self.logger.critical(message)
    
    def clean_old_logs(self, days=7):
        """
        清理旧日志文件
        
        Args:
            days: 保留最近几天的日志，默认7天
        """
        try:
            import time
            current_time = time.time()
            
            for log_file in self.log_dir.glob(f"{self.app_name}_*.log"):
                # 获取文件修改时间
                file_time = log_file.stat().st_mtime
                # 计算天数差
                days_old = (current_time - file_time) / (24 * 3600)
                
                if days_old > days:
                    log_file.unlink()
                    self.info(f"已删除旧日志文件: {log_file.name}")
        
        except Exception as e:
            self.error(f"清理旧日志失败: {e}")


# 创建全局logger实例
_logger_config = LoggerConfig()
logger = _logger_config.get_logger()


def get_logger():
    """
    获取全局logger实例
    
    Returns:
        配置好的logger对象
    """
    return logger


def clean_old_logs(days=7):
    """
    清理旧日志文件
    
    Args:
        days: 保留最近几天的日志，默认7天
    """
    _logger_config.clean_old_logs(days)


# 在模块加载时清理旧日志
try:
    clean_old_logs()
except:
    pass
