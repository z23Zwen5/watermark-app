@echo off
chcp 65001 >nul
echo ========================================
echo   Multi-Layer Watermark App v1.5
echo   多图层水印应用 v1.5
echo ========================================
echo.

REM 尝试使用 python 命令
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [启动中] 使用 python 命令...
    python src\watermark_app_multilayer.py
    goto end
)

REM 尝试使用 python3 命令
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo [启动中] 使用 python3 命令...
    python3 src\watermark_app_multilayer.py
    goto end
)

REM 如果都没有找到，提示用户
echo [错误] 未找到 Python！
echo.
echo 请安装 Python 3.7 或更高版本：
echo https://www.python.org/downloads/
echo.
pause
goto end

:end
if %errorlevel% neq 0 (
    echo.
    echo [错误] 程序运行出错！
    pause
)
