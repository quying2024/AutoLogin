@echo off
echo ========================================
echo   职称申报登录助手 - 日志查看
echo ========================================
echo.
echo 正在启动日志查看工具...
echo.

cd /d "%~dp0"
call .\venv\Scripts\activate.bat
.\venv\Scripts\python.exe log_viewer.py

echo.
pause