@echo off
chcp 65001 >nul
echo.
echo ========================================================================
echo   测试打包后的 exe 文件
echo ========================================================================
echo.

set EXE_PATH=dist\职称申报登录助手\职称申报登录助手.exe

if not exist "%EXE_PATH%" (
    echo [错误] 未找到 exe 文件！
    echo 请先运行打包: .\打包程序.bat
    pause
    exit /b 1
)

echo [1/3] 检查文件...
echo ✓ exe 文件存在
echo   路径: %EXE_PATH%
for %%F in ("%EXE_PATH%") do echo   大小: %%~zF bytes
echo.

echo [2/3] 检查依赖目录...
if exist "dist\职称申报登录助手\_internal" (
    echo ✓ _internal 目录存在
) else (
    echo ✗ _internal 目录缺失！
    pause
    exit /b 1
)
echo.

echo [3/3] 准备启动测试...
echo.
echo 即将启动程序，请检查：
echo   1. 程序是否能正常启动
echo   2. 主窗口是否显示在右下角
echo   3. 是否有错误提示
echo   4. 各功能按钮是否可用
echo.
echo 按任意键启动程序...
pause >nul

echo.
echo 正在启动 exe 文件...
cd dist\职称申报登录助手
start "" "职称申报登录助手.exe"

echo.
echo ========================================================================
echo   程序已启动！
echo ========================================================================
echo.
echo 测试清单：
echo   □ 程序窗口是否正常显示
echo   □ 位置是否在右下角
echo   □ 按钮是否可以点击
echo   □ 能否加载 Excel 文件
echo   □ 浏览器选择是否正常
echo   □ 是否有 numpy 相关错误
echo.
echo 如果一切正常，说明打包成功！
echo 如果有错误，请查看 logs 目录中的日志文件。
echo.
echo ========================================================================

cd ..\..
pause
