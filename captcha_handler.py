#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证码处理模块
集成超级鹰验证码识别服务
"""

import requests
import base64
import os
import time
from config import config
from logger_config import get_logger

# 获取日志记录器
logger = get_logger()

class CaptchaHandler:
    def __init__(self):
        self.chaojiying_config = config.get_chaojiying_config()
    
    def recognize_captcha(self, image_path, captcha_type="1004"):
        """
        使用超级鹰识别验证码
        
        Args:
            image_path: 验证码图片路径
            captcha_type: 验证码类型，默认1004（4位数字字母混合）
        
        Returns:
            str: 识别结果，失败返回None
        """
        if not config.is_chaojiying_configured():
            logger.info("超级鹰未配置，无法识别验证码")
            return None
        
        try:
            # 读取图片文件
            with open(image_path, 'rb') as f:
                img_data = f.read()
            
            # 调用超级鹰API
            url = "http://upload.chaojiying.net/Upload/Processing.php"
            data = {
                'user': self.chaojiying_config["username"],
                'pass': self.chaojiying_config["password"],
                'softid': self.chaojiying_config["soft_id"],
                'codetype': captcha_type,
            }
            files = {'userfile': ('captcha.png', img_data, 'image/png')}
            
            response = requests.post(url, data=data, files=files, timeout=30)
            result = response.text
            
            # 解析结果 - 支持JSON格式和老格式
            try:
                import json
                result_json = json.loads(result)
                if result_json.get("err_no") == 0:
                    # JSON格式成功识别
                    captcha_text = result_json.get("pic_str", "")
                    logger.info(f"验证码识别成功: {captcha_text}")
                    return captcha_text
                else:
                    logger.info(f"验证码识别失败: {result}")
                    return None
            except json.JSONDecodeError:
                # 尝试老格式解析
                if result.startswith('OK'):
                    # 老格式成功识别
                    captcha_text = result.split('|')[1]
                    logger.info(f"验证码识别成功: {captcha_text}")
                    return captcha_text
                else:
                    logger.info(f"验证码识别失败: {result}")
                    return None
                
        except Exception as e:
            logger.info(f"验证码识别出错: {e}")
            return None
    
    def report_error(self, captcha_id):
        """
        报告验证码识别错误
        
        Args:
            captcha_id: 验证码ID
        """
        if not config.is_chaojiying_configured():
            return
        
        try:
            url = "http://upload.chaojiying.net/Upload/ReportError.php"
            data = {
                'user': self.chaojiying_config["username"],
                'pass': self.chaojiying_config["password"],
                'softid': self.chaojiying_config["soft_id"],
                'id': captcha_id,
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.text
            
            if result.startswith('OK'):
                logger.info(f"验证码错误报告成功: {captcha_id}")
            else:
                logger.info(f"验证码错误报告失败: {result}")
                
        except Exception as e:
            logger.info(f"报告验证码错误时出错: {e}")
    
    def get_balance(self):
        """
        获取超级鹰账户余额
        
        Returns:
            float: 账户余额，失败返回None
        """
        if not config.is_chaojiying_configured():
            return None
        
        try:
            url = "http://upload.chaojiying.net/Upload/GetScore.php"
            data = {
                'user': self.chaojiying_config["username"],
                'pass': self.chaojiying_config["password"],
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.text
            
            if result.isdigit():
                balance = float(result)
                logger.info(f"超级鹰账户余额: {balance}")
                return balance
            else:
                logger.info(f"获取余额失败: {result}")
                return None
                
        except Exception as e:
            logger.info(f"获取余额时出错: {e}")
            return None
    
    def save_captcha_image(self, image_data, filename="captcha.png"):
        """
        保存验证码图片
        
        Args:
            image_data: 图片数据（bytes或base64字符串）
            filename: 文件名
        
        Returns:
            str: 保存的文件路径，失败返回None
        """
        try:
            # 如果是base64字符串，解码为bytes
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    # 处理data URL格式
                    img_data = image_data.split(',')[1]
                    image_data = base64.b64decode(img_data)
                else:
                    # 直接base64解码
                    image_data = base64.b64decode(image_data)
            
            # 保存文件
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            return os.path.abspath(filename)
            
        except Exception as e:
            logger.info(f"保存验证码图片失败: {e}")
            return None
    
    def cleanup_captcha_file(self, filepath):
        """
        清理验证码临时文件
        
        Args:
            filepath: 文件路径
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"已清理验证码文件: {filepath}")
        except Exception as e:
            logger.info(f"清理验证码文件失败: {e}")

# 全局验证码处理器实例
captcha_handler = CaptchaHandler()
