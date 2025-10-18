@echo off
echo ========================================
echo   职称申报登录助手 - 正常模式
echo ========================================
echo.
echo 正常模式特性:
echo - 验证码自动识别: 已启用
echo - 自动点击登录: 已启用  
echo - 浏览器超时: 60秒
echo - 浏览器窗口: 最大化启动
echo - 主窗口位置: 屏幕右下角
echo - 日志记录: 已启用（logs目录）
echo - 控制台输出: 已关闭（专业模式）
echo.
echo 提示: 如需查看运行日志，请使用 log_viewer.py
echo.
echo 正在启动程序...
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat
.\venv\Scripts\python.exe main.py

echo.
echo 程序已退出
echo 日志位置: logs\autologin_%date:~0,10%.log
echo.
pause