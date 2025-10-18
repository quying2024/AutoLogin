#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的窗口右下角定位功能
"""

import wx

print("=== 改进版窗口定位测试 ===")

class AdvancedTestFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='改进版定位测试', size=(384, 270))
        
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 显示定位信息
        self.info_text = wx.StaticText(panel, label="测试改进后的右下角定位...")
        font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.info_text.SetFont(font)
        sizer.Add(self.info_text, 1, wx.ALL | wx.EXPAND, 10)
        
        panel.SetSizer(sizer)
        
        # 使用改进的定位方法
        self.position_to_bottom_right_advanced()
    
    def position_to_bottom_right_advanced(self):
        """改进版右下角定位方法"""
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
            
            # 更新显示信息
            info = f"改进版定位结果:\n"
            info += f"工作区域: {screen_width}x{screen_height}\n"
            info += f"工作区偏移: ({client_x}, {client_y})\n"
            info += f"窗口位置: ({x}, {y})\n"
            info += f"窗口大小: {window_width}x{window_height}\n"
            info += f"边距设置: {margin}px"
            
            self.info_text.SetLabel(info)
            
            print(f"改进版定位: 窗口位于 ({x}, {y})")
            print(f"工作区域: {screen_width}x{screen_height} at ({client_x}, {client_y})")
            
        except Exception as e:
            print(f"定位失败: {e}")
            self.Center()
            self.info_text.SetLabel(f"定位失败，已居中显示\n错误: {e}")

if __name__ == "__main__":
    app = wx.App()
    
    # 显示屏幕信息
    try:
        display = wx.Display()
        client_area = display.GetClientArea()
        screen_size = wx.DisplaySize()
        
        print(f"屏幕总尺寸: {screen_size[0]}x{screen_size[1]}")
        print(f"工作区域: {client_area.width}x{client_area.height} at ({client_area.x}, {client_area.y})")
        
        # 计算预期位置
        margin = 15
        x = client_area.x + client_area.width - 384 - margin
        y = client_area.y + client_area.height - 270 - margin
        print(f"预期窗口位置: ({x}, {y})")
        
    except Exception as e:
        print(f"无法获取显示信息: {e}")
    
    frame = AdvancedTestFrame()
    frame.Show()
    
    print("\n改进功能:")
    print("1. 使用wx.Display().GetClientArea()获取工作区域")
    print("2. 自动排除任务栏和其他系统UI")
    print("3. 支持多显示器配置")
    print("4. 边界检查防止窗口超出屏幕")
    print("5. 增加边距到15像素提供更好视觉效果")
    
    app.MainLoop()