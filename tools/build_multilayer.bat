@echo off
REM Multi-Layer Watermark App v1.5 构建脚本 (Windows)
REM 用于将 Python 程序打包成独立可执行文件

setlocal enabledelayedexpansion

echo ========================================
echo   Multi-Layer Watermark Build Script
echo   Version: v1.5
echo ========================================
echo.

REM 设置路径
set "PROJECT_ROOT=%~dp0.."
set "BUILD_DIR=%PROJECT_ROOT%\build"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "SRC_FILE=%PROJECT_ROOT%\src\watermark_app_multilayer.py"
set "ICON_FILE=%PROJECT_ROOT%\assets\watermark_app_icon.ico"
set "SPEC_FILE=%BUILD_DIR%\MultiLayerWatermark_v1.5.spec"

echo [1/7] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装或不在 PATH 中！
    echo 请安装 Python 3.7+ 并添加到 PATH
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
    if errorlevel 1 (
        echo [ERROR] PyInstaller 安装失败！
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller 已安装
echo.

echo [3/7] 检查项目依赖...
if exist "%PROJECT_ROOT%\requirements.txt" (
    echo 正在安装依赖...
    pip install -r "%PROJECT_ROOT%\requirements.txt" -q
    echo [OK] 依赖已安装
) else (
    echo [WARN] 未找到 requirements.txt
)
echo.

echo [4/7] 检查源文件...
if not exist "%SRC_FILE%" (
    echo [ERROR] 源文件不存在: %SRC_FILE%
    pause
    exit /b 1
)
echo [OK] 源文件: watermark_app_multilayer.py
echo.

echo [5/7] 检查图标文件...
if not exist "%ICON_FILE%" (
    echo [WARN] 图标文件不存在: %ICON_FILE%
    set "ICON_ARG="
) else (
    echo [OK] 图标文件: watermark_app_icon.ico
    set "ICON_ARG=--icon=%ICON_FILE%"
)
echo.

echo [6/7] 清理旧的构建文件...
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo [OK] 已清理 build 目录
)
if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
    echo [OK] 已清理 dist 目录
)
mkdir "%BUILD_DIR%" >nul 2>&1
echo.

echo [7/7] 开始构建...
echo ========================================
cd /d "%PROJECT_ROOT%"

REM 使用 PyInstaller 构建
REM 注意：不打包 configs 目录，因为配置文件应该在运行时创建
REM 用户可以手动复制 configs 目录到可执行文件目录

python -m PyInstaller ^
    --name=MultiLayerWatermark_v1.5 ^
    --onefile ^
    --windowed ^
    --clean ^
    %ICON_ARG% ^
    --hidden-import=numpy ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=tkinter ^
    --hidden-import=json ^
    --distpath="%DIST_DIR%" ^
    --workpath="%BUILD_DIR%\temp" ^
    --specpath="%BUILD_DIR%" ^
    "%SRC_FILE%"

if errorlevel 1 (
    echo.
    echo [ERROR] 构建失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   构建成功！
echo ========================================
echo.

if exist "%DIST_DIR%\MultiLayerWatermark_v1.5.exe" (
    echo [OK] 输出文件: %DIST_DIR%\MultiLayerWatermark_v1.5.exe
    dir "%DIST_DIR%\MultiLayerWatermark_v1.5.exe"
    echo.
    echo 下一步:
    echo 1. 双击运行: %DIST_DIR%\MultiLayerWatermark_v1.5.exe
    echo 2. 如果需要，复制 configs 目录到可执行文件目录
) else (
    echo [WARN] 未找到可执行文件
)

echo.
pause
