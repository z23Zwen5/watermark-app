@echo off
REM Multi-Layer Watermark App v1.6.2 优化构建脚本 (Windows)
REM 优化重点: 使用 onedir 模式，大幅提升启动速度（5-7秒 -> 0.5-1秒）
REM 详细分析见: docs/STARTUP_PERFORMANCE_ANALYSIS.md

setlocal enabledelayedexpansion

echo ========================================
echo   Multi-Layer Watermark Build Script
echo   Version: v1.6.2 (Optimized)
echo   Mode: onedir (Fast Startup)
echo ========================================
echo.

REM 设置路径
set "PROJECT_ROOT=%~dp0.."
set "BUILD_DIR=%PROJECT_ROOT%\build"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "SRC_FILE=%PROJECT_ROOT%\src\watermark_app_multilayer.py"
set "ICON_FILE=%PROJECT_ROOT%\assets\watermark_app_icon.ico"

echo [1/8] 检查 Python 环境...
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

echo [2/8] 检查 PyInstaller...
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

echo [3/8] 检查项目依赖...
if exist "%PROJECT_ROOT%\requirements.txt" (
    echo 正在安装依赖...
    pip install -r "%PROJECT_ROOT%\requirements.txt" -q
    echo [OK] 依赖已安装
) else (
    echo [WARN] 未找到 requirements.txt
)
echo.

echo [4/8] 检查源文件...
if not exist "%SRC_FILE%" (
    echo [ERROR] 源文件不存在: %SRC_FILE%
    pause
    exit /b 1
)
echo [OK] 源文件: watermark_app_multilayer.py
echo.

echo [5/8] 检查图标文件...
if not exist "%ICON_FILE%" (
    echo [WARN] 图标文件不存在: %ICON_FILE%
    set "ICON_ARG="
) else (
    echo [OK] 图标文件: watermark_app_icon.ico
    set "ICON_ARG=--icon=%ICON_FILE%"
)
echo.

echo [6/8] 清理旧的构建文件...
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

echo [7/8] 开始构建（优化模式）...
echo ========================================
echo 优化说明:
echo   [✓] onedir 模式 - 启动速度提升 2-4 秒
echo   [✓] 移除不必要的隐藏导入
echo   [✓] 优化 DLL 加载
echo ========================================
echo.
cd /d "%PROJECT_ROOT%"

REM 使用 PyInstaller 构建（优化版）
REM 关键变化：
REM   1. --onedir (替代 --onefile) - 大幅提升启动速度
REM   2. 移除过多的 --hidden-import（让 PyInstaller 自动检测）
REM   3. 添加 --noupx（避免 UPX 压缩带来的启动延迟）

python -m PyInstaller ^
    --name=WatermarkApp_v1.6.2_Optimized ^
    --onedir ^
    --windowed ^
    --clean ^
    --noupx ^
    %ICON_ARG% ^
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

REM 检查输出目录
set "OUTPUT_DIR=%DIST_DIR%\WatermarkApp_v1.6.2_Optimized"
set "EXE_FILE=%OUTPUT_DIR%\WatermarkApp_v1.6.2_Optimized.exe"

if exist "%EXE_FILE%" (
    echo [OK] 输出目录: %OUTPUT_DIR%
    echo [OK] 主程序: WatermarkApp_v1.6.2_Optimized.exe
    echo.

    REM 显示目录大小
    for /f "tokens=3" %%a in ('dir "%OUTPUT_DIR%" ^| find "File(s)"') do set SIZE=%%a
    echo [INFO] 程序大小: !SIZE! bytes

    echo.
    echo ========================================
    echo   性能优化说明
    echo ========================================
    echo.
    echo 启动速度对比:
    echo   onefile 模式:  5-7 秒   (旧版)
    echo   onedir 模式:   0.5-1 秒 (当前) ✓
    echo.
    echo 分发方式:
    echo   1. 压缩整个文件夹: %OUTPUT_DIR%
    echo   2. 分发给用户后解压使用
    echo   3. 双击运行: WatermarkApp_v1.6.2_Optimized.exe
    echo.
    echo 下一步优化（可选）:
    echo   - 实施代码层面优化（延迟加载、异步字体扫描）
    echo   - 详见: docs/STARTUP_PERFORMANCE_ANALYSIS.md
    echo.
) else (
    echo [WARN] 未找到可执行文件
    echo 请检查: %OUTPUT_DIR%
)

echo [8/8] 创建快速启动说明文件...
set "README_FILE=%OUTPUT_DIR%\README_快速开始.txt"
if exist "%EXE_FILE%" (
    (
        echo Multi-Layer Watermark App v1.6.2 - 快速开始
        echo ========================================
        echo.
        echo 运行方法:
        echo   双击: WatermarkApp_v1.6.2_Optimized.exe
        echo.
        echo 优化说明:
        echo   - 使用 onedir 模式，启动速度提升 5-10 倍
        echo   - 从 5-7 秒降至 0.5-1 秒
        echo.
        echo 分发说明:
        echo   - 需要分发整个文件夹（而非单个 exe）
        echo   - 请保持所有 DLL 和文件在同一目录
        echo.
        echo 故障排除:
        echo   - 如果启动失败，检查 Windows Defender 是否拦截
        echo   - 确保所有文件解压到同一目录
        echo.
        echo 文档资源:
        echo   - GitHub: https://github.com/z23Zwen5/watermark-app
        echo   - 性能分析: docs/STARTUP_PERFORMANCE_ANALYSIS.md
        echo.
        echo ========================================
    ) > "%README_FILE%"
    echo [OK] 已创建快速启动说明: README_快速开始.txt
)

echo.
echo ========================================
echo   构建完成！
echo ========================================
pause
