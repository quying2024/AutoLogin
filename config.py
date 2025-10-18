#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
管理超级鹰API等设置
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_file = Path("config.json")
        self.default_config = {
            "chaojiying": {
                "username": "",
                "password": "",
                "soft_id": ""
            },
            "login": {
                "url": "http://222.143.33.99:8083/zcsb/login.do",
                "timeout": 30,
                "retry_count": 3
            },
            "ui": {
                "window_width": 384,
                "window_height": 270
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return self.default_config.copy()
        else:
            # 创建默认配置文件
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config=None):
        """保存配置文件"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        # 遍历到最后一个键
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        self.save_config()
    
    def get_chaojiying_config(self):
        """获取超级鹰配置"""
        return {
            "username": self.get("chaojiying.username", ""),
            "password": self.get("chaojiying.password", ""),
            "soft_id": self.get("chaojiying.soft_id", "")
        }
    
    def set_chaojiying_config(self, username, password, soft_id):
        """设置超级鹰配置"""
        self.set("chaojiying.username", username)
        self.set("chaojiying.password", password)
        self.set("chaojiying.soft_id", soft_id)
    
    def is_chaojiying_configured(self):
        """检查超级鹰是否已配置"""
        config = self.get_chaojiying_config()
        return all([config["username"], config["password"], config["soft_id"]])

# 全局配置实例
config = Config()
