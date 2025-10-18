@echo off
echo ========================================
echo   职称申报登录助手 - 调试模式
echo ========================================
echo.
echo 调试模式特性:
echo - 验证码自动识别: 已暂停
echo - 自动点击登录: 已暂停  
echo - 浏览器超时: 延长至5分钟
echo - 用户操作时间: 延长至30秒
echo - 浏览器窗口: 最大化启动
echo - 主窗口位置: 屏幕右下角
echo.
echo 正在启动程序...
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat
.\venv\Scripts\python.exe main.py

echo.
echo 程序已退出，按任意键关闭...
pause > nul