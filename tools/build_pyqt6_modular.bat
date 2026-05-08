@echo off
REM Multi-Layer Watermark App - PyQt6 模块化版本构建脚本
REM 版本: v2.2 (Modular Architecture + AI Rename)
REM 优化模式: onedir (快速启动 <1秒)

setlocal enabledelayedexpansion

echo ========================================
echo   WatermarkApp PyQt6 Build Script
echo   Version: v2.2 (AI Rename)
echo   Mode: onedir (Fast Startup)
echo ========================================
echo.

REM 设置路径
set "PROJECT_ROOT=%~dp0.."
set "BUILD_DIR=%PROJECT_ROOT%\build"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "SRC_FILE=%PROJECT_ROOT%\src\watermark_app_pyqt6_modular.py"
set "ICON_FILE=%PROJECT_ROOT%\assets\watermark_app_icon.ico"
set "APP_NAME=WatermarkApp_PyQt6_v2.2"

echo [1/8] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装或不在 PATH 中！
    pause
    exit /b 1
)
python --version
echo [OK] Python 环境正常
echo.

echo [2/8] 检查 PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PyInstaller 未安装，正在安装...
    pip install pyinstaller
)
echo [OK] PyInstaller 已安装
echo.

echo [3/8] 检查依赖...
python -c "from PyQt6 import QtWidgets" >nul 2>&1
if errorlevel 1 (
    echo [WARN] PyQt6 未安装，正在安装...
    pip install -r "%PROJECT_ROOT%\requirements_pyqt6.txt"
)
echo [OK] 所有依赖已安装
echo.

echo [4/8] 生成资源文件 (SVG + ICO)...
python "%~dp0generate_assets.py"
if errorlevel 1 (
    echo [WARN] 资源生成失败，使用现有资源继续...
)
echo.

echo [5/8] 清理旧文件...
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo [OK] 清理 build 目录
)

REM 先备份 dist 目录中的用户 config（避免清理时丢失）
set "CONFIG_BACKUP="
if exist "%DIST_DIR%\%APP_NAME%\_internal\configs\multilayer_watermark_config.json" (
    set "CONFIG_BACKUP=%TEMP%\watermark_config_backup_%RANDOM%.json"
    copy /y "%DIST_DIR%\%APP_NAME%\_internal\configs\multilayer_watermark_config.json" "!CONFIG_BACKUP!" >nul
    echo [OK] 已备份用户 config 到 !CONFIG_BACKUP!
) else if exist "%DIST_DIR%\%APP_NAME%\configs\multilayer_watermark_config.json" (
    set "CONFIG_BACKUP=%TEMP%\watermark_config_backup_%RANDOM%.json"
    copy /y "%DIST_DIR%\%APP_NAME%\configs\multilayer_watermark_config.json" "!CONFIG_BACKUP!" >nul
    echo [OK] 已备份用户 config 到 !CONFIG_BACKUP!
)

if exist "%DIST_DIR%\%APP_NAME%" (
    rmdir /s /q "%DIST_DIR%\%APP_NAME%"
    echo [OK] 清理旧的 dist 目录
)
echo.

echo [6/8] 开始构建...
echo 源文件: %SRC_FILE%
echo 图标: %ICON_FILE%
echo 输出目录: %DIST_DIR%\%APP_NAME%
echo.

cd /d "%PROJECT_ROOT%"

REM 获取 qtawesome 字体目录
for /f "delims=" %%i in ('python -c "import qtawesome, os; print(os.path.join(os.path.dirname(qtawesome.__file__), 'fonts'))"') do set "QTA_FONTS_DIR=%%i"
echo qtawesome fonts: %QTA_FONTS_DIR%

python -m PyInstaller ^
    --name=%APP_NAME% ^
    --onedir ^
    --windowed ^
    --icon="%ICON_FILE%" ^
    --add-data "assets;assets" ^
    --add-data "%QTA_FONTS_DIR%;qtawesome/fonts" ^
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
    --hidden-import=rename_module ^
    --hidden-import=ui.main_window ^
    --hidden-import=ui.components.title_bar ^
    --hidden-import=ui.components.message_box ^
    --hidden-import=ui.panels.upload_panel ^
    --hidden-import=ui.panels.layer_panel ^
    --hidden-import=ui.panels.output_panel ^
    --hidden-import=ui.panels.settings_panel ^
    --hidden-import=ui.panels.text_label_panel ^
    --hidden-import=ui.panels.rename_panel ^
    --hidden-import=ui.styles ^
    --hidden-import=ui.styles.theme_base ^
    --hidden-import=ui.styles.theme_genshin ^
    --hidden-import=ui.styles.theme_cyberpunk ^
    --hidden-import=ui.styles.genshin_style ^
    --hidden-import=qtawesome ^
    --collect-all=qtawesome ^
    --collect-all=numpy ^
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
echo [7/8] 验证输出...
if exist "%DIST_DIR%\%APP_NAME%\%APP_NAME%.exe" (
    echo [OK] 构建成功！
    echo.
    echo 输出位置: %DIST_DIR%\%APP_NAME%\
    echo 主程序: %APP_NAME%.exe
    echo 版本: v2.2 - AI Rename
) else (
    echo [ERROR] 未找到生成的 exe 文件
    pause
    exit /b 1
)

REM 还原用户 config（如果有备份）
if defined CONFIG_BACKUP (
    if exist "!CONFIG_BACKUP!" (
        if exist "%DIST_DIR%\%APP_NAME%\_internal\configs" (
            copy /y "!CONFIG_BACKUP!" "%DIST_DIR%\%APP_NAME%\_internal\configs\multilayer_watermark_config.json" >nul
            echo [OK] 已还原用户 config 到 _internal\configs\
        ) else if exist "%DIST_DIR%\%APP_NAME%\configs" (
            copy /y "!CONFIG_BACKUP!" "%DIST_DIR%\%APP_NAME%\configs\multilayer_watermark_config.json" >nul
            echo [OK] 已还原用户 config 到 configs\
        ) else (
            mkdir "%DIST_DIR%\%APP_NAME%\configs" >nul 2>&1
            copy /y "!CONFIG_BACKUP!" "%DIST_DIR%\%APP_NAME%\configs\multilayer_watermark_config.json" >nul
            echo [OK] 已创建并还原 config 到 configs\
        )
        del /q "!CONFIG_BACKUP!" >nul 2>&1
    )
)

echo.
echo [8/8] 清理临时文件...
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
echo    包含: 水印功能 + AI 命名 + 网盘发货
echo.
pause
