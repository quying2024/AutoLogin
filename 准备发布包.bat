@echo off
chcp 65001 >nul
REM ========================================================================
REM 准备完整发布包
REM ========================================================================

echo.
echo ========================================================================
echo   准备发布包
echo ========================================================================
echo.

set RELEASE_DIR=发布包_职称申报登录助手_v1.0.0
set DIST_SOURCE=dist\职称申报登录助手

REM 检查 dist 目录是否存在
if not exist "%DIST_SOURCE%" (
    echo [错误] 未找到打包输出目录
    echo 请先运行"打包程序.bat"完成打包
    pause
    exit /b 1
)

REM 创建发布目录
echo [1/5] 创建发布目录...
if exist "%RELEASE_DIR%" (
    rmdir /s /q "%RELEASE_DIR%"
)
mkdir "%RELEASE_DIR%"
echo 完成
echo.

REM 复制主程序和依赖
echo [2/5] 复制程序文件...
xcopy "%DIST_SOURCE%\*" "%RELEASE_DIR%\" /E /I /H /Y >nul
echo 完成
echo.

REM 复制配置模板
echo [3/5] 复制配置文件...
if exist "settings.json.example" (
    copy "settings.json.example" "%RELEASE_DIR%\settings.json.example" >nul
    echo   settings.json.example - 配置文件模板
)
echo 完成
echo.

REM 复制文档
echo [4/5] 复制文档...
if exist "README.md" (
    copy "README.md" "%RELEASE_DIR%\README.md" >nul
    echo   README.md - 使用说明
)
if exist "打包发布指南.md" (
    copy "打包发布指南.md" "%RELEASE_DIR%\打包发布指南.md" >nul
    echo   打包发布指南.md - 发布指南
)
echo 完成
echo.

REM 创建快速启动说明
echo [5/5] 创建启动说明...
(
echo 职称申报登录助手 - 快速启动指南
echo ================================================================================
echo.
echo 首次使用:
echo   1. 安装 Playwright 浏览器
echo      打开 PowerShell，运行: playwright install chromium
echo.
echo   2. 配置程序
echo      - 复制 settings.json.example 为 settings.json
echo      - 填写您的超级鹰账号信息
echo.
echo   3. 准备数据文件
echo      - 创建 Excel 文件包含用户信息
echo      - 在 settings.json 中指定文件路径
echo.
echo 运行程序:
echo   双击 "职称申报登录助手.exe" 即可启动
echo.
echo 日志文件:
echo   程序会自动在 logs 目录下创建日志文件
echo   格式: autologin_YYYY-MM-DD.log
echo.
echo 常见问题:
echo   1. 程序无法启动
echo      - 检查是否有杀毒软件拦截
echo      - 确保 _internal 目录完整
echo.
echo   2. 浏览器无法启动
echo      - 确认已安装 Playwright 浏览器
echo      - 或使用系统已安装的 Chrome/Edge
echo.
echo   3. 验证码识别失败
echo      - 检查超级鹰账号配置
echo      - 确认账号有足够的题分
echo.
echo 技术支持:
echo   如有问题请查看 README.md 或联系技术支持
echo.
echo ================================================================================
) > "%RELEASE_DIR%\快速启动指南.txt"
echo 完成
echo.

echo ========================================================================
echo   发布包准备完成！
echo ========================================================================
echo.
echo 发布目录: %RELEASE_DIR%
echo.
echo 包含文件:
dir /B "%RELEASE_DIR%"
echo.

echo 下一步操作:
echo   1. 测试发布包中的 exe 是否正常运行
echo   2. 压缩为 ZIP 文件便于分发
echo   3. 或使用安装程序制作工具打包
echo.

REM 询问是否创建 ZIP 压缩包
set /p CREATE_ZIP=是否创建 ZIP 压缩包? (Y/N): 
if /i "%CREATE_ZIP%"=="Y" (
    echo.
    echo 正在创建 ZIP 压缩包...
    powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%RELEASE_DIR%.zip' -Force"
    if %errorlevel% equ 0 (
        echo 完成! ZIP 文件: %RELEASE_DIR%.zip
        for %%F in ("%RELEASE_DIR%.zip") do echo 文件大小: %%~zF bytes
    ) else (
        echo 创建 ZIP 失败
    )
)

echo.
echo ========================================================================
pause
