@echo off
echo ========================================
echo   职称申报登录助手 - 开发模式
echo ========================================
echo.
echo 开发模式特性:
echo - 所有功能: 与正常模式相同
echo - 控制台输出: 已启用（显示调试信息）
echo - 日志记录: 已启用（同时记录到文件）
echo.
echo 注意: 此模式用于开发和调试
echo       请在main.py中设置 CONSOLE_OUTPUT = True
echo.
echo 正在启动程序...
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat

REM 临时设置环境变量以启用控制台输出
set DEV_MODE=1
.\venv\Scripts\python.exe main.py

echo.
echo 程序已退出
pause