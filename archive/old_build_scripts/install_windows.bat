@echo off
REM Multi-Layer Watermark 安装脚本 (Windows 11)
REM 将程序复制到 Program Files 并创建开始菜单快捷方式

setlocal enabledelayedexpansion

echo ========================================
echo   Multi-Layer Watermark 安装程序
echo   Version: v1.5
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo [WARN] 未以管理员身份运行
    echo 将安装到用户目录: %LocalAppData%
    set "INSTALL_DIR=%LocalAppData%\MultiLayerWatermark"
    set "START_MENU=%AppData%\Microsoft\Windows\Start Menu\Programs"
) else (
    echo [OK] 以管理员身份运行
    echo 将安装到系统目录: C:\Program Files
    set "INSTALL_DIR=C:\Program Files\MultiLayerWatermark"
    set "START_MENU=C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
)

echo.
echo [1/4] 创建安装目录...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo [OK] 已创建: %INSTALL_DIR%
) else (
    echo [OK] 目录已存在: %INSTALL_DIR%
)
echo.

echo [2/4] 复制程序文件...
set "EXE_PATH=%~dp0..\dist\MultiLayerWatermark_v1.5.exe"
if not exist "%EXE_PATH%" (
    echo [ERROR] 找不到可执行文件: %EXE_PATH%
    echo 请先运行 build_multilayer.bat 构建程序
    pause
    exit /b 1
)

copy /Y "%EXE_PATH%" "%INSTALL_DIR%\MultiLayerWatermark.exe"
if errorlevel 1 (
    echo [ERROR] 复制失败！
    pause
    exit /b 1
)
echo [OK] 已复制程序文件
echo.

echo [3/4] 创建开始菜单快捷方式...
set "SHORTCUT=%START_MENU%\Multi-Layer Watermark.lnk"

REM 使用 PowerShell 创建快捷方式
powershell -Command ^
    "$WScriptShell = New-Object -ComObject WScript.Shell; ^
     $Shortcut = $WScriptShell.CreateShortcut('%SHORTCUT%'); ^
     $Shortcut.TargetPath = '%INSTALL_DIR%\MultiLayerWatermark.exe'; ^
     $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
     $Shortcut.Description = 'Multi-Layer Watermark Application'; ^
     $Shortcut.Save()"

if errorlevel 1 (
    echo [ERROR] 创建快捷方式失败！
    pause
    exit /b 1
)
echo [OK] 已创建开始菜单快捷方式
echo.

echo [4/4] 复制配置文件（可选）...
set "CONFIG_SRC=%~dp0..\configs"
if exist "%CONFIG_SRC%" (
    if not exist "%INSTALL_DIR%\configs" (
        mkdir "%INSTALL_DIR%\configs"
    )
    xcopy /Y /I "%CONFIG_SRC%\*.json" "%INSTALL_DIR%\configs\" >nul 2>&1
    echo [OK] 已复制配置文件
) else (
    echo [SKIP] 配置文件不存在，将在首次运行时创建
)
echo.

echo ========================================
echo   安装成功！
echo ========================================
echo.
echo 安装位置: %INSTALL_DIR%
echo 快捷方式: %SHORTCUT%
echo.
echo 下一步:
echo 1. 按 Win 键打开开始菜单
echo 2. 搜索 "Multi-Layer Watermark"
echo 3. 右键选择 "固定到开始屏幕"
echo 4. 或直接点击运行
echo.
echo 要卸载程序，请删除以下文件夹:
echo - %INSTALL_DIR%
echo - %SHORTCUT%
echo.

REM 询问是否立即运行
set /p RUN="是否立即运行程序？(Y/N): "
if /i "%RUN%"=="Y" (
    start "" "%INSTALL_DIR%\MultiLayerWatermark.exe"
)

pause
