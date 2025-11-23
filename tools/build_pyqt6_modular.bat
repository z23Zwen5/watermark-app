@echo off
REM Multi-Layer Watermark App - PyQt6 模块化版本构建脚本
REM 版本: v2.0 (Modular Architecture)
REM 优化模式: onedir (快速启动 <1秒)

setlocal enabledelayedexpansion

echo ========================================
echo   WatermarkApp PyQt6 Build Script
echo   Version: v2.0 (Modular)
echo   Mode: onedir (Fast Startup)
echo ========================================
echo.

REM 设置路径
set "PROJECT_ROOT=%~dp0.."
set "BUILD_DIR=%PROJECT_ROOT%\build"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "SRC_FILE=%PROJECT_ROOT%\src\watermark_app_pyqt6_modular.py"
set "ICON_FILE=%PROJECT_ROOT%\assets\watermark_app_icon.ico"
set "APP_NAME=WatermarkApp_PyQt6_v2.0"

echo [1/7] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装或不在 PATH 中！
    pause
    exit /b 1
)
python --version
echo [OK] Python 环境正常
echo.

echo [2/7] 检查 PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PyInstaller 未安装，正在安装...
    pip install pyinstaller
)
echo [OK] PyInstaller 已安装
echo.

echo [3/7] 检查依赖...
python -c "from PyQt6 import QtWidgets" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PyQt6 未安装，正在安装...
    pip install -r "%PROJECT_ROOT%\requirements_pyqt6.txt"
)
echo [OK] 所有依赖已安装
echo.

echo [4/7] 清理旧文件...
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo [OK] 清理 build 目录
)
if exist "%DIST_DIR%\%APP_NAME%" (
    rmdir /s /q "%DIST_DIR%\%APP_NAME%"
    echo [OK] 清理旧的 dist 目录
)
echo.

echo [5/7] 开始构建...
echo 源文件: %SRC_FILE%
echo 图标: %ICON_FILE%
echo 输出目录: %DIST_DIR%\%APP_NAME%
echo.

cd /d "%PROJECT_ROOT%"

python -m PyInstaller ^
    --name=%APP_NAME% ^
    --onedir ^
    --windowed ^
    --icon="%ICON_FILE%" ^
    --add-data "assets;assets" ^
    --paths="src" ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PyQt6.QtSvg ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=numpy ^
    --hidden-import=watermark_core ^
    --hidden-import=text_label_module ^
    --hidden-import=ui.main_window ^
    --hidden-import=ui.components.title_bar ^
    --hidden-import=ui.components.message_box ^
    --hidden-import=ui.panels.upload_panel ^
    --hidden-import=ui.panels.layer_panel ^
    --hidden-import=ui.panels.output_panel ^
    --hidden-import=ui.panels.settings_panel ^
    --hidden-import=ui.styles ^
    --hidden-import=ui.styles.theme_base ^
    --hidden-import=ui.styles.theme_genshin ^
    --hidden-import=ui.styles.theme_cyberpunk ^
    --hidden-import=ui.styles.genshin_style ^
    --noconfirm ^
    --clean ^
    "src\watermark_app_pyqt6_modular.py"

if errorlevel 1 (
    echo.
    echo [ERROR] 构建失败！
    pause
    exit /b 1
)

echo.
echo [6/7] 验证输出...
if exist "%DIST_DIR%\%APP_NAME%\%APP_NAME%.exe" (
    echo [OK] 构建成功！
    echo.
    echo 输出位置: %DIST_DIR%\%APP_NAME%\
    echo 主程序: %APP_NAME%.exe
) else (
    echo [ERROR] 未找到生成的 exe 文件
    pause
    exit /b 1
)

echo.
echo [7/7] 清理临时文件...
if exist "%PROJECT_ROOT%\*.spec" (
    del /q "%PROJECT_ROOT%\*.spec"
    echo [OK] 清理 spec 文件
)

echo.
echo ========================================
echo   构建完成！
echo ========================================
echo.
echo 📁 输出位置: %DIST_DIR%\%APP_NAME%\
echo 🚀 启动程序: %APP_NAME%.exe
echo.
echo 💡 提示: onedir 模式启动速度快 (<1秒)
echo    可以将整个文件夹复制到其他电脑使用
echo.
pause
