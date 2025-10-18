#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职称申报登录助手
基于 Python + WxPython + Playwright 的自动化登录工具
"""

import wx
import os
import json
import threading
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright
import requests
import time
import re
from config import config
from captcha_handler import captcha_handler
from logger_config import get_logger

# 获取日志记录器
logger = get_logger()

# 控制台输出开关（发布版本设置为False）
CONSOLE_OUTPUT = False  # True: 显示控制台输出, False: 仅记录到日志文件

def log(message, level='info'):
    """
    统一的日志记录函数
    
    Args:
        message: 日志消息
        level: 日志级别 (debug, info, warning, error, critical)
    """
    # 记录到日志文件
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    elif level == 'critical':
        logger.critical(message)
    else:
        logger.info(message)
    
    # 如果启用控制台输出，则打印到终端
    if CONSOLE_OUTPUT:
        log(message)


class AutoLoginFrame(wx.Frame):
    def __init__(self):
        # 设置窗口不可调整大小
        super().__init__(parent=None, title='职称申报登录助手', size=(384, 270), 
                         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.file_path = ""
        self.is_running = False
        self.browser = None
        self.page = None
        self.accounts_data = None
        self.current_account = None
        self.playwright = None  # 添加 Playwright 实例
        
        # 加载配置文件
        self.load_config()
        
        # 初始化UI
        self.init_ui()
        
        # 设置窗口位置到右下角
        self.position_to_bottom_right()
    
    def position_to_bottom_right(self):
        """将窗口定位到屏幕右下角"""
        try:
            # 获取主显示器的工作区域（排除任务栏等）
            display = wx.Display()
            client_area = display.GetClientArea()
            
            # 如果无法获取工作区域，使用传统方法
            if client_area.width == 0 or client_area.height == 0:
                screen_size = wx.DisplaySize()
                screen_width = screen_size[0]
                screen_height = screen_size[1] - 40  # 减去任务栏高度
                client_x, client_y = 0, 0
            else:
                screen_width = client_area.width
                screen_height = client_area.height
                client_x = client_area.x
                client_y = client_area.y
            
            # 获取窗口尺寸
            window_size = self.GetSize()
            window_width = window_size[0]
            window_height = window_size[1]
            
            # 计算右下角位置（留一些边距）
            margin = 15  # 距离屏幕边缘15像素
            x = client_x + screen_width - window_width - margin
            y = client_y + screen_height - window_height - margin
            
            # 确保窗口不会超出屏幕范围
            if x < client_x:
                x = client_x + margin
            if y < client_y:
                y = client_y + margin
            
            # 设置窗口位置
            self.SetPosition((x, y))
            log(f"调试: 窗口定位到右下角 ({x}, {y})")
            log(f"调试: 工作区域 {screen_width}x{screen_height} at ({client_x}, {client_y})")
            
        except Exception as e:
            log(f"调试: 窗口定位失败，使用默认位置: {e}")
            # 如果定位失败，使用默认居中
            self.Center()
        
    def load_config(self):
        """加载配置文件"""
        config_file = Path("app_config.txt")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.file_path = f.read().strip()
            except:
                self.file_path = ""
        else:
            self.file_path = ""
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open("app_config.txt", 'w', encoding='utf-8') as f:
                f.write(self.file_path)
        except Exception as e:
            wx.MessageBox(f"保存配置文件失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
    
    def init_ui(self):
        """初始化用户界面"""
        panel = wx.Panel(self)
        
        # 主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 标题
        title = wx.StaticText(panel, label="职称申报登录助手", style=wx.ALIGN_CENTER)
        title_font = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="微软雅黑")
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        
        # 姓名输入框和登录按钮在同一行
        name_login_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_label = wx.StaticText(panel, label="姓名:")
        self.name_input = wx.TextCtrl(panel, size=(150, -1), style=wx.TE_PROCESS_ENTER)  # 缩短输入框，支持回车键
        self.name_input.Bind(wx.EVT_TEXT_ENTER, self.on_login)  # 绑定回车键事件
        self.login_btn = wx.Button(panel, label="登录", size=(80, 30))  # 调整按钮大小
        self.login_btn.Bind(wx.EVT_BUTTON, self.on_login)
        
        name_login_sizer.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        name_login_sizer.Add(self.name_input, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        name_login_sizer.Add(self.login_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        main_sizer.Add(name_login_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        
        # 浏览器选择按钮区域
        browser_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # 创建浏览器选择按钮
        self.browser_buttons = {}
        self.selected_browser = "chrome"  # 默认选择Chrome
        
        browsers = [
            ("edge", "Edge"),
            ("chrome", "Chrome"), 
            ("chromium", "Chromium"),
            ("firefox", "Firefox")
        ]
        
        # 在按钮前添加弹性空间，实现居中分散布局
        browser_sizer.Add(wx.StaticText(panel, label=""), 1, wx.EXPAND)
        
        for i, (browser_key, browser_name) in enumerate(browsers):
            btn = wx.ToggleButton(panel, label=browser_name, size=(55, 22))  # 缩小按钮尺寸
            
            # 设置较小的字体
            btn_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            btn.SetFont(btn_font)
            
            # 设置淡色背景和文字颜色
            btn.SetBackgroundColour(wx.Colour(245, 245, 245))  # 浅灰色背景
            btn.SetForegroundColour(wx.Colour(120, 120, 120))  # 深灰色文字
            
            btn.Bind(wx.EVT_TOGGLEBUTTON, lambda event, key=browser_key: self.on_browser_select(event, key))
            self.browser_buttons[browser_key] = btn
            
            # 添加按钮，按钮之间用弹性空间分散
            browser_sizer.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL)
            if i < len(browsers) - 1:  # 不是最后一个按钮时添加弹性空间
                browser_sizer.Add(wx.StaticText(panel, label=""), 1, wx.EXPAND)
        
        # 在按钮后添加弹性空间
        browser_sizer.Add(wx.StaticText(panel, label=""), 1, wx.EXPAND)
        
        # 默认选择Chrome按钮并设置选中样式
        chrome_btn = self.browser_buttons["chrome"]
        chrome_btn.SetValue(True)
        # 使用加深边框的方式显示选中状态（通过重新设置按钮样式实现）
        self.set_button_selected_style(chrome_btn)
        
        main_sizer.Add(browser_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # 添加一些空白空间，将文件路径推到底部
        main_sizer.Add(wx.StaticText(panel, label=""), 1, wx.EXPAND)
        
        # 文件路径区域（保持在底部）
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_btn = wx.Button(panel, label="文件路径", size=(55, 22))  # 与浏览器按钮相同大小
        
        # 设置更小的字体以适应按钮尺寸
        file_btn_font = wx.Font(6, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.file_btn.SetFont(file_btn_font)
        
        self.file_btn.Bind(wx.EVT_BUTTON, self.on_select_file)
        self.file_path_text = wx.StaticText(panel, label="未选择文件")
        
        # 设置文件路径显示文字的字体和颜色
        path_text_font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.file_path_text.SetFont(path_text_font)
        self.file_path_text.SetForegroundColour(wx.Colour(130, 130, 130))  # 淡灰色
        
        file_sizer.Add(self.file_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        file_sizer.Add(self.file_path_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        main_sizer.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)
        
        # 更新文件路径显示
        self.update_file_path_display()
        
        # 自动加载上次使用的文件
        self.auto_load_last_file()
        
        panel.SetSizer(main_sizer)
    
    def on_browser_select(self, event, browser_key):
        """浏览器选择事件处理"""
        # 取消其他按钮的选择状态（实现互锁效果）
        for key, btn in self.browser_buttons.items():
            if key != browser_key:
                btn.SetValue(False)
                # 恢复未选中按钮的普通样式
                self.set_button_normal_style(btn)
        
        # 确保当前按钮保持选中状态，并设置选中样式
        selected_btn = self.browser_buttons[browser_key]
        selected_btn.SetValue(True)
        self.set_button_selected_style(selected_btn)
        
        self.selected_browser = browser_key
        log(f"调试: 选择了浏览器: {browser_key}")
    
    def set_button_normal_style(self, btn):
        """设置按钮普通样式"""
        btn.SetBackgroundColour(wx.Colour(245, 245, 245))  # 浅灰色背景
        btn.SetForegroundColour(wx.Colour(120, 120, 120))  # 深灰色文字
        btn.Refresh()  # 刷新按钮显示
    
    def set_button_selected_style(self, btn):
        """设置按钮选中样式（加深边框）"""
        # 保持背景色不变，只改变文字颜色来突出显示
        btn.SetBackgroundColour(wx.Colour(245, 245, 245))  # 保持浅灰色背景
        btn.SetForegroundColour(wx.Colour(30, 30, 30))     # 深黑色文字
        btn.Refresh()  # 刷新按钮显示
    
    def launch_selected_browser(self):
        """根据选择的浏览器类型启动浏览器"""
        try:
            browser_args = [
                '--no-first-run', 
                '--no-default-browser-check',
                '--start-maximized'  # 启动时最大化窗口
            ]
            log(f"调试: 启动浏览器类型: {self.selected_browser}")
            log("调试: 浏览器将以最大化窗口启动")
            
            if self.selected_browser == "chrome":
                return self.playwright.chromium.launch(
                    headless=False,
                    args=browser_args,
                    channel="chrome"  # 使用系统安装的Chrome
                )
            elif self.selected_browser == "chromium":
                return self.playwright.chromium.launch(
                    headless=False,
                    args=browser_args
                )
            elif self.selected_browser == "edge":
                return self.playwright.chromium.launch(
                    headless=False,
                    args=browser_args,
                    channel="msedge"  # 使用系统安装的Edge
                )
            elif self.selected_browser == "firefox":
                # Firefox使用不同的最大化参数
                firefox_args = [
                    '--width=1920',
                    '--height=1080'
                ]
                return self.playwright.firefox.launch(
                    headless=False,
                    args=firefox_args
                )
            else:
                # 默认使用Chrome
                log("调试: 未知浏览器类型，使用Chrome作为默认")
                return self.playwright.chromium.launch(
                    headless=False,
                    args=browser_args,
                    channel="chrome"
                )
                
        except Exception as e:
            log(f"调试: 启动{self.selected_browser}失败: {e}")
            log("调试: 尝试使用默认Chromium")
            # 如果指定浏览器启动失败，回退到默认Chromium
            return self.playwright.chromium.launch(
                headless=False,
                args=browser_args
            )

    def update_file_path_display(self):
        """更新文件路径显示"""
        if self.file_path:
            # 只显示文件名
            filename = os.path.basename(self.file_path)
            self.file_path_text.SetLabel(filename)
        else:
            self.file_path_text.SetLabel("未选择文件")
    
    def auto_load_last_file(self):
        """自动加载上次使用的文件"""
        # 如果没有保存的文件路径，尝试使用默认文件
        if not self.file_path:
            default_file = "docs/2025职称申报账号信息.xlsx"
            if os.path.exists(default_file):
                self.file_path = default_file
                self.save_config()
                log(f"调试: 使用默认文件: {self.file_path}")
        
        if self.file_path and os.path.exists(self.file_path):
            try:
                log(f"调试: 自动加载文件: {self.file_path}")
                self.load_accounts_data()
                log("调试: 文件自动加载成功")
            except Exception as e:
                log(f"调试: 自动加载文件失败: {e}")
                # 如果自动加载失败，清空文件路径
                self.file_path = ""
                self.save_config()
                self.update_file_path_display()
        else:
            log("调试: 没有可用的文件路径")
    
    def on_select_file(self, event):
        """选择文件按钮事件"""
        with wx.FileDialog(self, "选择账号信息文件", wildcard="Excel files (*.xlsx;*.xls)|*.xlsx;*.xls",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            
            self.file_path = fileDialog.GetPath()
            self.save_config()
            self.update_file_path_display()
            
            # 尝试加载文件
            try:
                self.load_accounts_data()
                wx.MessageBox("文件加载成功！", "提示", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"文件加载失败: {e}", "错误", wx.OK | wx.ICON_ERROR)
    
    def load_accounts_data(self):
        """加载账号数据"""
        if not self.file_path or not os.path.exists(self.file_path):
            raise Exception("文件不存在")
        
        try:
            log(f"调试: 正在读取文件 {self.file_path}")
            self.accounts_data = pd.read_excel(self.file_path)
            log(f"调试: 读取成功，数据形状: {self.accounts_data.shape}")
            log(f"调试: 列名: {list(self.accounts_data.columns)}")
            
            required_columns = ['姓名', '单位', '身份证号码', '密码']
            
            # 检查必需的列
            missing_columns = [col for col in required_columns if col not in self.accounts_data.columns]
            if missing_columns:
                raise Exception(f"缺少必需的列: {', '.join(missing_columns)}")
            
            # 显示前几行数据
            log("调试: 前5行数据:")
            log(self.accounts_data.head())
            
            # 清理数据
            original_count = len(self.accounts_data)
            self.accounts_data = self.accounts_data.dropna(subset=['姓名', '身份证号码', '密码'])
            log(f"调试: 清理前 {original_count} 行，清理后 {len(self.accounts_data)} 行")
            
            # 显示姓名列的数据类型和内容
            log(f"调试: 姓名列数据类型: {self.accounts_data['姓名'].dtype}")
            log(f"调试: 姓名列内容: {self.accounts_data['姓名'].tolist()}")
            
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {e}")
    
    def find_account_by_name(self, name):
        """根据姓名查找账号信息"""
        if self.accounts_data is None:
            log("调试: accounts_data 为 None")
            return None
        
        log(f"调试: 查找姓名 '{name}'")
        log(f"调试: 数据类型 {type(name)}")
        log(f"调试: 所有姓名: {self.accounts_data['姓名'].tolist()}")
        
        # 尝试精确匹配
        account = self.accounts_data[self.accounts_data['姓名'] == name]
        if len(account) > 0:
            log(f"调试: 找到精确匹配")
            return account.iloc[0]
        
        # 尝试去除空格后匹配
        name_trimmed = name.strip()
        account = self.accounts_data[self.accounts_data['姓名'].str.strip() == name_trimmed]
        if len(account) > 0:
            log(f"调试: 找到去除空格后的匹配")
            return account.iloc[0]
        
        # 尝试包含匹配
        account = self.accounts_data[self.accounts_data['姓名'].str.contains(name, na=False)]
        if len(account) > 0:
            log(f"调试: 找到包含匹配")
            return account.iloc[0]
        
        log(f"调试: 未找到匹配")
        return None
    
    def on_login(self, event):
        """登录按钮事件"""
        if self.is_running:
            wx.MessageBox("登录程序正在运行中，请稍候...", "提示", wx.OK | wx.ICON_INFORMATION)
            return
        
        name = self.name_input.GetValue().strip()
        if not name:
            wx.MessageBox("请输入姓名", "提示", wx.OK | wx.ICON_WARNING)
            return
        
        if not self.file_path or not os.path.exists(self.file_path):
            wx.MessageBox("请先选择账号信息文件", "提示", wx.OK | wx.ICON_WARNING)
            return
        
        # 查找账号信息
        account = self.find_account_by_name(name)
        if account is None:
            wx.MessageBox(f"未找到姓名为 '{name}' 的账号信息", "错误", wx.OK | wx.ICON_ERROR)
            return
        
        self.current_account = account
        
        # 在新线程中执行登录
        self.is_running = True
        self.login_btn.SetLabel("登录中...")
        self.login_btn.Disable()
        
        # 保存线程引用，防止被垃圾回收
        self.login_thread = threading.Thread(target=self.perform_login)
        self.login_thread.daemon = False  # 改为非守护线程
        self.login_thread.start()
    
    def perform_login(self):
        """执行登录操作"""
        browser = None
        page = None
        
        try:
            log("="*50)
            log("� 职称申报登录助手")
            log("- 验证码自动识别: 已启用")
            log("- 自动点击登录: 已启用")  
            log("- 浏览器超时: 60秒")
            log("- 浏览器窗口: 最大化启动")
            log("- 主窗口位置: 屏幕右下角")
            log("="*50)
            
            # 启动 Playwright（不使用上下文管理器）
            self.playwright = sync_playwright().start()
            
            # 根据选择的浏览器类型启动浏览器
            browser = self.launch_selected_browser()
            page = browser.new_page()
            
            # 最大化浏览器窗口
            try:
                log("调试: 正在最大化浏览器窗口...")
                # 方法1: 使用viewport设置大窗口
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                # 方法2: 使用JavaScript最大化窗口（适用于支持的浏览器）
                page.evaluate("() => { if (window.screen) { window.moveTo(0, 0); window.resizeTo(screen.width, screen.height); } }")
                log("调试: 浏览器窗口已最大化")
            except Exception as e:
                log(f"调试: 窗口最大化失败: {e}")
            
            # 设置超时时间
            page.set_default_timeout(60000)  # 60秒超时
            
            # 访问登录页面
            login_url = config.get("login.url", "http://222.143.33.99:8083/zcsb/login.do")
            log(f"调试: 正在访问登录页面: {login_url}")
            page.goto(login_url)
            
            # 等待页面加载
            log("调试: 等待页面加载...")
            page.wait_for_load_state("networkidle")
            
            # 等待页面元素出现
            log("调试: 等待页面元素...")
            page.wait_for_selector('#account', timeout=30000)
            page.wait_for_selector('#password', timeout=30000)
            
            # 填写用户名（身份证号码）
            username = str(self.current_account['身份证号码'])
            log(f"调试: 填写用户名: {username}")
            page.fill('#account', username)
            
            # 填写密码
            password = str(self.current_account['密码'])
            log(f"调试: 填写密码: {password[:3]}***")
            page.fill('#password', password)
            
            # 检查是否有验证码
            log("调试: 检查验证码...")
            captcha_input = page.query_selector('#code')
            if captcha_input:
                log("调试: 发现验证码输入框")
                
                # 先点击验证码图片刷新（如果可以点击的话）
                captcha_img = page.query_selector('#imgVcode')
                if captcha_img:
                    log("调试: 点击验证码图片刷新")
                    try:
                        captcha_img.click()
                        # 等待验证码图片刷新
                        page.wait_for_timeout(1000)  # 等待1秒
                    except:
                        log("调试: 验证码图片无法点击，继续使用当前图片")
                
                # 处理验证码
                captcha_text = self.handle_captcha(page)
                if captcha_text:
                    log(f"调试: 验证码识别结果: {captcha_text}")
                    page.fill('#code', captcha_text)
                else:
                    wx.CallAfter(wx.MessageBox, "验证码识别失败，请检查超级鹰配置", "错误", wx.OK | wx.ICON_ERROR)
                    return
            else:
                log("调试: 未发现验证码输入框")
            
            # 点击登录按钮
            log("调试: 查找登录按钮...")
            login_button = page.query_selector('#submitImg')
            if login_button:
                log("调试: 点击登录按钮")
                login_button.click()
            else:
                log("调试: 未找到登录按钮，尝试按回车键")
                page.keyboard.press("Enter")
            
            # 等待登录结果
            log("调试: 等待登录结果...")
            page.wait_for_timeout(5000)
            
            # 处理可能的弹窗
            self.handle_popups(page)
            
            # 检查登录是否成功
            if self.check_login_success(page):
                # 登录成功，静默保持浏览器打开，不显示提示
                user_name = self.current_account['姓名']
                log(f"调试: 用户 {user_name} 登录成功，浏览器保持打开状态")
                
                # 登录成功后，让浏览器完全独立运行
                # 不保存浏览器引用，让它自由运行
                log("调试: 浏览器已独立运行，不再受程序控制")
                
                # 异步更新UI（不传递浏览器引用）
                wx.CallAfter(self.setup_success_ui, user_name)
                
                # 清理本地引用，让浏览器独立
                browser = None
                page = None
                return  # 浏览器独立运行
            else:
                wx.CallAfter(wx.MessageBox, "登录失败，请检查账号信息", "错误", wx.OK | wx.ICON_ERROR)
                
        except Exception as e:
            log(f"调试: 登录过程中出现错误: {e}")
            wx.CallAfter(wx.MessageBox, f"登录过程中出现错误: {e}", "错误", wx.OK | wx.ICON_ERROR)
        
        finally:
            # 只在登录失败或出错时清理资源
            # 如果 browser 和 page 被设置为 None，说明登录成功，浏览器已独立
            if browser is not None or page is not None:
                try:
                    if page:
                        page.close()
                    if browser:
                        browser.close()
                    log("调试: 登录失败，已清理浏览器资源")
                except Exception as e:
                    log(f"调试: 清理浏览器资源时出错: {e}")
                
                # 恢复UI状态（仅在登录失败时）
                wx.CallAfter(self.reset_ui_state)
            else:
                log("调试: 登录成功，浏览器已独立运行")
    
    def handle_captcha(self, page):
        """处理验证码"""
        try:
            # 查找验证码图片 - 使用正确的选择器
            captcha_selectors = [
                '#imgVcode',  # 正确的验证码图片选择器
                'img[src*="captcha"]',
                'img[alt*="验证码"]',
                'img[id*="captcha"]',
                'img[id*="code"]',
                'img[class*="captcha"]',
                'img[class*="code"]',
                '#captchaImg',
                '#codeImg',
                'img[onclick*="captcha"]'
            ]
            
            captcha_img = None
            for selector in captcha_selectors:
                captcha_img = page.query_selector(selector)
                if captcha_img:
                    log(f"调试: 使用选择器找到验证码图片: {selector}")
                    break
            
            if not captcha_img:
                log("调试: 未找到验证码图片")
                # 尝试获取所有img元素进行调试
                all_imgs = page.query_selector_all('img')
                log(f"调试: 页面共有 {len(all_imgs)} 个图片元素")
                for i, img in enumerate(all_imgs[:5]):  # 只显示前5个
                    src = img.get_attribute('src') or ''
                    alt = img.get_attribute('alt') or ''
                    id_attr = img.get_attribute('id') or ''
                    class_attr = img.get_attribute('class') or ''
                    log(f"调试: 图片{i}: src={src[:50]}..., alt={alt}, id={id_attr}, class={class_attr}")
                return None
            
            # 等待一下确保验证码图片已更新
            page.wait_for_timeout(500)
            
            # 使用Playwright直接截图验证码元素，确保获取的是当前显示的图片
            log("调试: 使用Playwright截图获取验证码图片")
            try:
                img_bytes = captcha_img.screenshot()
                log(f"调试: 截图获取的图片大小: {len(img_bytes)} 字节")
            except Exception as e:
                log(f"调试: 截图失败，尝试下载方式: {e}")
                # 备用方案：下载验证码图片
                captcha_src = captcha_img.get_attribute('src')
                log(f"调试: 验证码图片源: {captcha_src[:100]}...")
                
                if captcha_src.startswith('data:'):
                    # 内联图片，直接使用
                    log("调试: 处理内联验证码图片")
                    import base64
                    img_data = captcha_src.split(',')[1]
                    img_bytes = base64.b64decode(img_data)
                else:
                    # 外部图片，下载
                    log("调试: 下载外部验证码图片")
                    # 如果是相对路径，需要补全URL
                    if captcha_src.startswith('/'):
                        captcha_src = f"http://222.143.33.99:8083{captcha_src}"
                    elif not captcha_src.startswith('http'):
                        captcha_src = f"http://222.143.33.99:8083/zcsb/{captcha_src}"
                    
                    # 添加随机参数避免缓存
                    import time
                    if '?' in captcha_src:
                        captcha_src += f"&_t={int(time.time() * 1000)}"
                    else:
                        captcha_src += f"?_t={int(time.time() * 1000)}"
                    
                    log(f"调试: 完整验证码URL: {captcha_src}")
                    
                    # 使用页面的cookies下载验证码
                    cookies = page.context.cookies()
                    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
                    
                    response = requests.get(captcha_src, cookies=cookie_dict)
                    img_bytes = response.content
                    log(f"调试: 下载的图片大小: {len(img_bytes)} 字节")
            
            # 保存验证码图片
            captcha_path = captcha_handler.save_captcha_image(img_bytes)
            if not captcha_path:
                return None
            
            # 使用超级鹰识别验证码
            captcha_text = captcha_handler.recognize_captcha(captcha_path)
            
            # 删除临时文件
            captcha_handler.cleanup_captcha_file(captcha_path)
            
            return captcha_text
            
        except Exception as e:
            log(f"验证码处理失败: {e}")
            return None
    

    
    def handle_popups(self, page):
        """处理弹窗"""
        try:
            # 等待一段时间让弹窗出现
            page.wait_for_timeout(3000)  # 增加等待时间
            
            # 首先专门检查通知弹窗
            log("调试: 检查通知弹窗...")
            notification_close_btn = page.query_selector('#newModalGongGao > div > div > div.modal-footer > button')
            if notification_close_btn:
                log("调试: 发现通知弹窗，正在关闭...")
                try:
                    # 检查弹窗标题确认是"通知"
                    modal_title = page.query_selector('#newModalGongGao .modal-title')
                    if modal_title:
                        title_text = modal_title.inner_text().strip()
                        log(f"调试: 弹窗标题: {title_text}")
                        if title_text == "通知":
                            notification_close_btn.click()
                            page.wait_for_timeout(1000)
                            log("调试: 通知弹窗已关闭")
                            # 关闭弹窗后，点击"基本信息"菜单
                            self.click_basic_info(page)
                            return
                    else:
                        # 如果找不到标题，但找到了关闭按钮，也尝试关闭
                        log("调试: 未找到弹窗标题，但发现关闭按钮，尝试关闭...")
                        notification_close_btn.click()
                        page.wait_for_timeout(1000)
                        log("调试: 弹窗已关闭")
                        # 关闭弹窗后，点击"基本信息"菜单
                        self.click_basic_info(page)
                        return
                except Exception as e:
                    log(f"调试: 关闭通知弹窗时出错: {e}")
            
            # 处理其他类型的弹窗
            log("调试: 检查其他弹窗...")
            dialogs = page.query_selector_all('div[class*="dialog"], div[class*="modal"], div[class*="popup"]')
            
            for dialog in dialogs:
                try:
                    # 检查是否是修改密码弹窗
                    dialog_text = dialog.inner_text().lower()
                    log(f"调试: 发现弹窗，内容: {dialog_text[:100]}...")
                    
                    if '修改密码' in dialog_text or 'change password' in dialog_text:
                        # 这是修改密码弹窗，无法自动处理
                        log("调试: 检测到修改密码弹窗，需要用户手动处理")
                        wx.CallAfter(wx.MessageBox, 
                                    "检测到修改密码弹窗，请手动修改密码后继续", 
                                    "提示", wx.OK | wx.ICON_WARNING)
                        return
                    
                    # 检查是否是注意事项弹窗（但不是通知弹窗）
                    if '注意事项' in dialog_text and '通知' not in dialog_text:
                        log("调试: 检测到注意事项弹窗，尝试关闭...")
                        # 尝试关闭弹窗
                        close_btn = dialog.query_selector('button[class*="close"], .close, [aria-label="Close"]')
                        if close_btn:
                            close_btn.click()
                            page.wait_for_timeout(1000)
                            log("调试: 注意事项弹窗已关闭")
                    else:
                        log("调试: 发现其他类型弹窗，保持不变等待用户处理")
                
                except Exception as e:
                    log(f"调试: 处理单个弹窗时出错: {e}")
            
            # 处理浏览器原生弹窗
            page.on("dialog", lambda dialog: dialog.dismiss())
            
        except Exception as e:
            log(f"调试: 处理弹窗时出错: {e}")
    
    def click_basic_info(self, page):
        """点击基本信息菜单"""
        try:
            log("调试: 准备点击基本信息菜单...")
            
            # 等待页面加载完毕
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)  # 额外等待2秒确保页面完全加载
            
            # 查找基本信息菜单链接
            basic_info_selector = "#nav-accordion > li:nth-child(3) > a"
            log(f"调试: 查找基本信息菜单: {basic_info_selector}")
            
            # 等待基本信息菜单出现
            basic_info_link = page.wait_for_selector(basic_info_selector, timeout=10000)
            
            if basic_info_link:
                log("调试: 找到基本信息菜单，准备点击...")
                
                # 确保元素可见并可点击
                basic_info_link.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                
                # 点击基本信息菜单
                basic_info_link.click()
                log("调试: 已点击基本信息菜单")
                
                # 等待页面响应
                page.wait_for_timeout(2000)
                log("调试: 基本信息页面加载完成，可以开始录入工作")
                
            else:
                log("调试: 未找到基本信息菜单")
                
        except Exception as e:
            log(f"调试: 点击基本信息菜单时出错: {e}")
            # 即使点击失败也不影响主流程，用户可以手动点击
    
    def check_login_success(self, page):
        """检查登录是否成功"""
        try:
            # 检查URL是否改变（登录后通常会跳转）
            current_url = page.url
            log(f"调试: 当前URL: {current_url}")
            if "login" not in current_url.lower():
                log("调试: URL已改变，可能登录成功")
                return True
            
            # 检查是否有登录成功的元素
            success_indicators = [
                'text=欢迎',
                'text=登录成功',
                'text=个人中心',
                '[class*="user-info"]',
                '[class*="logout"]'
            ]
            
            for indicator in success_indicators:
                try:
                    element = page.query_selector(indicator)
                    if element:
                        log(f"调试: 找到成功指示器: {indicator}")
                        return True
                except:
                    continue
            
            # 检查是否有错误信息
            error_indicators = [
                'text=用户名或密码错误',
                'text=验证码错误',
                'text=登录失败',
                '[class*="error"]'
            ]
            
            for indicator in error_indicators:
                try:
                    element = page.query_selector(indicator)
                    if element:
                        log(f"调试: 找到错误指示器: {indicator}")
                        return False
                except:
                    continue
            
            # 默认认为登录成功（如果没有明显的错误信息）
            log("调试: 未找到明确的成功或失败指示器，默认认为成功")
            return True
            
        except Exception as e:
            log(f"检查登录状态时出错: {e}")
            return False
    
    def reset_ui_state(self):
        """重置UI状态"""
        self.is_running = False
        self.login_btn.SetLabel("登录")
        self.login_btn.Enable()
    
    def setup_success_ui(self, user_name):
        """设置登录成功的UI状态，不显示提示窗口"""
        try:
            log(f"调试: 开始设置成功UI状态，用户: {user_name}")
            
            # 更新UI状态，显示当前登录用户
            self.update_ui_for_success(user_name)
            
            log("调试: 成功UI状态设置完成，浏览器已独立运行")
            
        except Exception as e:
            log(f"调试: 设置成功UI状态时出错: {e}")
            import traceback
            traceback.print_exc()
    
    def update_ui_for_success(self, user_name):
        """更新UI显示登录成功状态"""
        # 重置UI状态
        self.reset_ui_state()
        
        # 更新登录按钮文本显示当前用户
        self.login_btn.SetLabel(f"已登录: {user_name}")
        
        # 可选：改变按钮颜色表示成功状态
        self.login_btn.SetBackgroundColour(wx.Colour(144, 238, 144))  # 浅绿色
    
    def start_browser_monitor(self):
        """启动浏览器监控线程"""
        try:
            log("调试: 启动浏览器监控线程")
            monitor_thread = threading.Thread(target=self.monitor_browser)
            monitor_thread.daemon = True
            monitor_thread.start()
        except Exception as e:
            log(f"调试: 启动浏览器监控失败: {e}")
    
    def monitor_browser(self):
        """监控浏览器状态"""
        try:
            log("调试: 浏览器监控线程已启动")
            import time
            
            while True:
                if hasattr(self, 'active_browser') and self.active_browser:
                    try:
                        # 检查浏览器是否还存在
                        contexts = self.active_browser.contexts
                        if not contexts:
                            log("调试: 浏览器上下文已丢失")
                            break
                        
                        # 检查页面是否还存在
                        if hasattr(self, 'active_page') and self.active_page:
                            try:
                                # 尝试获取页面标题来测试连接
                                title = self.active_page.title()
                                log(f"调试: 浏览器监控正常，页面标题: {title[:50]}...")
                            except Exception as e:
                                log(f"调试: 页面连接已断开: {e}")
                                break
                        
                        time.sleep(5)  # 每5秒检查一次
                        
                    except Exception as e:
                        log(f"调试: 浏览器监控检查失败: {e}")
                        break
                else:
                    log("调试: 没有活动的浏览器需要监控")
                    break
            
            log("调试: 浏览器监控线程结束")
            
        except Exception as e:
            log(f"调试: 浏览器监控线程异常: {e}")
            import traceback
            traceback.print_exc()
    
    def add_close_browser_button(self):
        """添加关闭浏览器按钮"""
        if hasattr(self, 'close_browser_btn'):
            return  # 按钮已存在
        
        # 获取主面板
        panel = self.GetChildren()[0]
        main_sizer = panel.GetSizer()
        
        # 创建关闭浏览器按钮
        self.close_browser_btn = wx.Button(panel, label="关闭浏览器", size=(100, 30))
        self.close_browser_btn.Bind(wx.EVT_BUTTON, self.on_close_browser)
        
        # 添加到布局中（在设置按钮下方）
        main_sizer.Add(self.close_browser_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        # 刷新布局
        panel.Layout()
        self.Layout()
    
    def on_close_browser(self, event):
        """关闭浏览器按钮事件"""
        if hasattr(self, 'active_browser') and self.active_browser:
            try:
                if hasattr(self, 'active_page') and self.active_page:
                    self.active_page.close()
                self.active_browser.close()
                
                # 停止 Playwright 实例
                if hasattr(self, 'playwright') and self.playwright:
                    self.playwright.stop()
                    self.playwright = None
                
                log("调试: 浏览器已手动关闭")
                wx.MessageBox("浏览器已关闭", "提示", wx.OK | wx.ICON_INFORMATION)
                
                # 移除关闭按钮
                self.remove_close_browser_button()
                
            except Exception as e:
                log(f"调试: 关闭浏览器时出错: {e}")
                wx.MessageBox(f"关闭浏览器时出错: {e}", "错误", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("没有活动的浏览器需要关闭", "提示", wx.OK | wx.ICON_INFORMATION)
    
    def remove_close_browser_button(self):
        """移除关闭浏览器按钮"""
        if hasattr(self, 'close_browser_btn'):
            self.close_browser_btn.Destroy()
            delattr(self, 'close_browser_btn')
            # 清理浏览器引用
            if hasattr(self, 'active_browser'):
                delattr(self, 'active_browser')
            if hasattr(self, 'active_page'):
                delattr(self, 'active_page')
            # 刷新布局
            panel = self.GetChildren()[0]
            panel.Layout()
            self.Layout()

def main():
    """主函数"""
    try:
        log("调试: 启动主程序")
        app = wx.App()
        frame = AutoLoginFrame()
        frame.Show()
        
        # 添加退出处理
        def on_exit():
            log("调试: 程序正在退出")
            # 完全不清理Playwright，避免EPIPE错误和浏览器关闭
            # 让操作系统在进程结束时自动清理资源
            # 重定向stderr以抑制Node.js的EPIPE错误输出
            import sys
            try:
                if sys.platform == 'win32':
                    sys.stderr = open('nul', 'w', encoding='utf-8')
                else:
                    sys.stderr = open('/dev/null', 'w')
            except:
                pass
            log("调试: 程序退出完成（浏览器保持运行）")
        
        import atexit
        atexit.register(on_exit)
        
        log("调试: 开始主循环")
        app.MainLoop()
        log("调试: 主循环结束")
        
    except Exception as e:
        log(f"调试: 主函数异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
