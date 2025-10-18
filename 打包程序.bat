@echo off
chcp 65001 >nul
REM ========================================================================
REM 职称申报登录助手 - 打包脚本
REM 将 Python 程序打包成 Windows exe 可执行文件
REM ========================================================================

echo.
echo ========================================================================
echo   职称申报登录助手 - 打包工具
echo ========================================================================
echo.

REM 检查虚拟环境是否存在
if not exist "venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境！
    echo 请先创建虚拟环境: python -m venv venv
    pause
    exit /b 1
)

REM 激活虚拟环境
echo [1/6] 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [错误] 虚拟环境激活失败！
    pause
    exit /b 1
)
echo ✓ 虚拟环境已激活
echo.

REM 检查 PyInstaller 是否已安装
echo [2/6] 检查 PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [提示] PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo [错误] PyInstaller 安装失败！
        pause
        exit /b 1
    )
)
echo ✓ PyInstaller 已就绪
echo.

REM 清理旧的打包文件
echo [3/6] 清理旧的打包文件...
if exist "build" (
    echo 删除 build 目录...
    rmdir /s /q build
)
if exist "dist" (
    echo 删除 dist 目录...
    rmdir /s /q dist
)
echo ✓ 清理完成
echo.

REM 安装 Playwright 浏览器（如果需要）
echo [4/6] 检查 Playwright 浏览器...
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.launch(); p.stop()" 2>nul
if %errorlevel% neq 0 (
    echo [提示] Playwright 浏览器未安装，正在安装...
    playwright install chromium
)
echo ✓ Playwright 浏览器已就绪
echo.

REM 执行打包
echo [5/6] 开始打包程序...
echo 这可能需要几分钟时间，请耐心等待...
echo.
pyinstaller --clean autologin.spec
if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败！
    echo 请检查错误信息并修复后重试。
    pause
    exit /b 1
)
echo.
echo ✓ 打包成功
echo.

REM 检查输出文件
echo [6/6] 验证打包结果...
if exist "dist\职称申报登录助手\职称申报登录助手.exe" (
    echo ✓ exe 文件已生成
    echo.
    echo ========================================================================
    echo   打包完成！
    echo ========================================================================
    echo.
    echo 输出目录: dist\职称申报登录助手\
    echo.
    echo 主程序: 职称申报登录助手.exe
    echo.
    echo 注意事项:
    echo   1. 首次运行需要安装 Playwright 浏览器
    echo   2. 需要准备 settings.json 配置文件
    echo   3. 需要准备 Excel 数据文件
    echo   4. dist 目录中的所有文件都需要一起分发
    echo.
    echo 测试建议:
    echo   1. 先在本机测试 exe 文件是否正常运行
    echo   2. 检查日志文件是否正常生成（logs 目录）
    echo   3. 测试验证码识别功能
    echo   4. 测试自动登录功能
    echo.
    echo ========================================================================
    echo.
    
    REM 打开输出目录
    explorer "dist\职称申报登录助手\"
) else (
    echo [错误] 未找到生成的 exe 文件！
    echo 请检查打包过程是否有错误。
    pause
    exit /b 1
)

pause
