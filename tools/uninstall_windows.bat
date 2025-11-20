@echo off
REM Multi-Layer Watermark 卸载脚本 (Windows 11)

setlocal enabledelayedexpansion

echo ========================================
echo   Multi-Layer Watermark 卸载程序
echo   Version: v1.5
echo ========================================
echo.

REM 检查可能的安装位置
set "USER_INSTALL=%LocalAppData%\MultiLayerWatermark"
set "SYSTEM_INSTALL=C:\Program Files\MultiLayerWatermark"
set "USER_SHORTCUT=%AppData%\Microsoft\Windows\Start Menu\Programs\Multi-Layer Watermark.lnk"
set "SYSTEM_SHORTCUT=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Multi-Layer Watermark.lnk"

echo 正在查找安装位置...
echo.

set "FOUND=0"

REM 检查用户安装
if exist "%USER_INSTALL%" (
    echo [找到] 用户安装: %USER_INSTALL%
    set "FOUND=1"
    set "INSTALL_DIR=%USER_INSTALL%"
    set "SHORTCUT=%USER_SHORTCUT%"
)

REM 检查系统安装
if exist "%SYSTEM_INSTALL%" (
    echo [找到] 系统安装: %SYSTEM_INSTALL%
    set "FOUND=1"
    set "INSTALL_DIR=%SYSTEM_INSTALL%"
    set "SHORTCUT=%SYSTEM_SHORTCUT%"
)

if "%FOUND%"=="0" (
    echo [警告] 未找到安装文件
    echo.
    echo 可能的位置:
    echo - %USER_INSTALL%
    echo - %SYSTEM_INSTALL%
    echo.
    pause
    exit /b 1
)

echo.
echo 将删除以下内容:
echo - 程序文件: %INSTALL_DIR%
echo - 快捷方式: %SHORTCUT%
echo.

set /p CONFIRM="确认卸载？(Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo 已取消卸载
    pause
    exit /b 0
)

echo.
echo [1/2] 删除程序文件...
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    if errorlevel 1 (
        echo [ERROR] 删除失败，可能需要管理员权限
        echo 请手动删除: %INSTALL_DIR%
    ) else (
        echo [OK] 已删除程序文件
    )
) else (
    echo [SKIP] 程序文件不存在
)

echo.
echo [2/2] 删除快捷方式...
if exist "%SHORTCUT%" (
    del /f /q "%SHORTCUT%"
    if errorlevel 1 (
        echo [ERROR] 删除失败
        echo 请手动删除: %SHORTCUT%
    ) else (
        echo [OK] 已删除快捷方式
    )
) else (
    echo [SKIP] 快捷方式不存在
)

REM 检查其他可能的快捷方式位置
if exist "%USER_SHORTCUT%" (
    del /f /q "%USER_SHORTCUT%" >nul 2>&1
)
if exist "%SYSTEM_SHORTCUT%" (
    del /f /q "%SYSTEM_SHORTCUT%" >nul 2>&1
)

echo.
echo ========================================
echo   卸载完成！
echo ========================================
echo.
echo 注意:
echo - 配置文件已删除
echo - 如果图标仍显示在开始菜单，请右键取消固定
echo.
pause
