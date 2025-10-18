#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置对话框
用于配置超级鹰API等设置
"""

import wx
from config import config
from captcha_handler import captcha_handler

class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="设置", size=(400, 300))
        
        self.init_ui()
        self.load_settings()
        
        # 设置窗口居中
        self.Center()
    
    def init_ui(self):
        """初始化用户界面"""
        panel = wx.Panel(self)
        
        # 主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 超级鹰设置
        chaojiying_box = wx.StaticBox(panel, label="超级鹰验证码识别设置")
        chaojiying_sizer = wx.StaticBoxSizer(chaojiying_box, wx.VERTICAL)
        
        # 用户名
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(panel, label="用户名:")
        self.username_input = wx.TextCtrl(panel, size=(200, -1))
        username_sizer.Add(username_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        username_sizer.Add(self.username_input, 1, wx.EXPAND)
        chaojiying_sizer.Add(username_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 密码
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(panel, label="密码:")
        self.password_input = wx.TextCtrl(panel, size=(200, -1), style=wx.TE_PASSWORD)
        password_sizer.Add(password_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        password_sizer.Add(self.password_input, 1, wx.EXPAND)
        chaojiying_sizer.Add(password_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 软件ID
        softid_sizer = wx.BoxSizer(wx.HORIZONTAL)
        softid_label = wx.StaticText(panel, label="软件ID:")
        self.softid_input = wx.TextCtrl(panel, size=(200, -1))
        softid_sizer.Add(softid_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        softid_sizer.Add(self.softid_input, 1, wx.EXPAND)
        chaojiying_sizer.Add(softid_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 测试按钮
        test_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.test_btn = wx.Button(panel, label="测试连接")
        self.test_btn.Bind(wx.EVT_BUTTON, self.on_test_connection)
        self.balance_label = wx.StaticText(panel, label="余额: 未查询")
        test_sizer.Add(self.test_btn, 0, wx.RIGHT, 10)
        test_sizer.Add(self.balance_label, 1, wx.ALIGN_CENTER_VERTICAL)
        chaojiying_sizer.Add(test_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(chaojiying_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 登录设置
        login_box = wx.StaticBox(panel, label="登录设置")
        login_sizer = wx.StaticBoxSizer(login_box, wx.VERTICAL)
        
        # 超时时间
        timeout_sizer = wx.BoxSizer(wx.HORIZONTAL)
        timeout_label = wx.StaticText(panel, label="超时时间(秒):")
        self.timeout_input = wx.SpinCtrl(panel, value="30", min=10, max=120)
        timeout_sizer.Add(timeout_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        timeout_sizer.Add(self.timeout_input, 0)
        login_sizer.Add(timeout_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        # 重试次数
        retry_sizer = wx.BoxSizer(wx.HORIZONTAL)
        retry_label = wx.StaticText(panel, label="重试次数:")
        self.retry_input = wx.SpinCtrl(panel, value="3", min=1, max=10)
        retry_sizer.Add(retry_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        retry_sizer.Add(self.retry_input, 0)
        login_sizer.Add(retry_sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        main_sizer.Add(login_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 按钮区域
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(panel, label="保存")
        cancel_btn = wx.Button(panel, label="取消")
        
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        button_sizer.Add(save_btn, 0, wx.RIGHT, 10)
        button_sizer.Add(cancel_btn, 0)
        
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        panel.SetSizer(main_sizer)
    
    def load_settings(self):
        """加载设置"""
        # 超级鹰设置
        chaojiying_config = config.get_chaojiying_config()
        self.username_input.SetValue(chaojiying_config["username"])
        self.password_input.SetValue(chaojiying_config["password"])
        self.softid_input.SetValue(chaojiying_config["soft_id"])
        
        # 登录设置
        self.timeout_input.SetValue(config.get("login.timeout", 30))
        self.retry_input.SetValue(config.get("login.retry_count", 3))
    
    def on_test_connection(self, event):
        """测试超级鹰连接"""
        # 临时保存设置
        username = self.username_input.GetValue().strip()
        password = self.password_input.GetValue().strip()
        soft_id = self.softid_input.GetValue().strip()
        
        if not all([username, password, soft_id]):
            wx.MessageBox("请填写完整的超级鹰配置信息", "提示", wx.OK | wx.ICON_WARNING)
            return
        
        # 临时设置配置
        config.set_chaojiying_config(username, password, soft_id)
        
        # 测试连接
        self.test_btn.Disable()
        self.test_btn.SetLabel("测试中...")
        
        # 在新线程中测试
        import threading
        thread = threading.Thread(target=self.test_connection_thread)
        thread.daemon = True
        thread.start()
    
    def test_connection_thread(self):
        """测试连接线程"""
        try:
            balance = captcha_handler.get_balance()
            
            if balance is not None:
                wx.CallAfter(self.balance_label.SetLabel, f"余额: {balance}")
                wx.CallAfter(wx.MessageBox, f"连接成功！账户余额: {balance}", "提示", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.CallAfter(self.balance_label.SetLabel, "余额: 查询失败")
                wx.CallAfter(wx.MessageBox, "连接失败，请检查配置信息", "错误", wx.OK | wx.ICON_ERROR)
                
        except Exception as e:
            wx.CallAfter(self.balance_label.SetLabel, "余额: 查询失败")
            wx.CallAfter(wx.MessageBox, f"连接测试失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
        
        finally:
            wx.CallAfter(self.test_btn.Enable)
            wx.CallAfter(self.test_btn.SetLabel, "测试连接")
    
    def on_save(self, event):
        """保存设置"""
        try:
            # 保存超级鹰设置
            username = self.username_input.GetValue().strip()
            password = self.password_input.GetValue().strip()
            soft_id = self.softid_input.GetValue().strip()
            
            config.set_chaojiying_config(username, password, soft_id)
            
            # 保存登录设置
            config.set("login.timeout", self.timeout_input.GetValue())
            config.set("login.retry_count", self.retry_input.GetValue())
            
            wx.MessageBox("设置保存成功！", "提示", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            
        except Exception as e:
            wx.MessageBox(f"保存设置失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
    
    def on_cancel(self, event):
        """取消设置"""
        self.EndModal(wx.ID_CANCEL)
