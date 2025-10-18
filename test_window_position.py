#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试窗口右下角定位功能
"""

import wx

class TestFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='窗口定位测试', size=(384, 270))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 添加一些文本显示窗口信息
        self.info_text = wx.StaticText(panel, label="正在测试右下角定位...")
        sizer.Add(self.info_text, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        # 添加按钮测试不同定位
        btn_center = wx.Button(panel, label="居中")
        btn_center.Bind(wx.EVT_BUTTON, self.on_center)
        
        btn_bottom_right = wx.Button(panel, label="右下角")
        btn_bottom_right.Bind(wx.EVT_BUTTON, self.on_bottom_right)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_center, 0, wx.ALL, 5)
        btn_sizer.Add(btn_bottom_right, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        
        panel.SetSizer(sizer)
        
        # 默认定位到右下角
        self.position_to_bottom_right()
        
        # 显示当前位置信息
        self.update_position_info()
    
    def position_to_bottom_right(self):
        """将窗口定位到屏幕右下角"""
        try:
            # 获取屏幕尺寸
            screen_size = wx.DisplaySize()
            screen_width = screen_size[0]
            screen_height = screen_size[1]
            
            # 获取窗口尺寸
            window_size = self.GetSize()
            window_width = window_size[0]
            window_height = window_size[1]
            
            # 计算右下角位置（留一些边距）
            margin = 10  # 距离屏幕边缘10像素
            x = screen_width - window_width - margin
            y = screen_height - window_height - margin - 40  # 减去任务栏高度（约40像素）
            
            # 设置窗口位置
            self.SetPosition((x, y))
            print(f"窗口定位到右下角 ({x}, {y})")
            
        except Exception as e:
            print(f"窗口定位失败，使用默认位置: {e}")
            self.Center()
    
    def update_position_info(self):
        """更新位置信息显示"""
        pos = self.GetPosition()
        size = self.GetSize()
        screen_size = wx.DisplaySize()
        
        info = f"窗口位置: ({pos.x}, {pos.y})\n"
        info += f"窗口大小: {size.width} x {size.height}\n"
        info += f"屏幕大小: {screen_size[0]} x {screen_size[1]}"
        
        self.info_text.SetLabel(info)
    
    def on_center(self, event):
        """居中按钮事件"""
        self.Center()
        self.update_position_info()
        print("窗口已居中")
    
    def on_bottom_right(self, event):
        """右下角按钮事件"""
        self.position_to_bottom_right()
        self.update_position_info()

class TestApp(wx.App):
    def OnInit(self):
        frame = TestFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    print("=== 窗口右下角定位测试 ===")
    print("测试窗口将显示在屏幕右下角")
    print("您可以使用按钮测试不同的定位方式")
    
    app = TestApp()
    app.MainLoop()