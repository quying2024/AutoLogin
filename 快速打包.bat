@echo off
chcp 65001 >nul
REM ========================================================================
REM 快速打包脚本（适用于开发测试）
REM ========================================================================

echo.
echo [快速打包] 开始打包...
echo.

REM 清理
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM 打包
call venv\Scripts\activate
pyinstaller --clean autologin.spec

if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo [成功] 打包完成！
echo 输出目录: dist\职称申报登录助手\
echo.

pause
