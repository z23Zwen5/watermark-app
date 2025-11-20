@echo off
REM Build Multi-Layer Watermark App v1.6 with Icon

echo ========================================
echo   Multi-Layer Watermark App v1.6 Build
echo   Building with custom icon
echo ========================================
echo.

REM Set paths (script is in tools/ directory, need to go up one level)
set "PROJECT_ROOT=%~dp0..\"
set "SRC_FILE=%PROJECT_ROOT%src\watermark_app_multilayer.py"
set "ICON_FILE=%PROJECT_ROOT%assets\watermark_app_icon.ico"
set "OUTPUT_NAME=WatermarkApp_v1.6"

REM Check if icon exists
if not exist "%ICON_FILE%" (
    echo [ERROR] Icon file not found: %ICON_FILE%
    pause
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.7+
    pause
    exit /b 1
)

echo [1/5] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo [2/5] Installing dependencies...
pip install pillow numpy >nul 2>&1

echo [3/5] Cleaning old builds...
if exist "%PROJECT_ROOT%build" rmdir /s /q "%PROJECT_ROOT%build"
if exist "%PROJECT_ROOT%dist" rmdir /s /q "%PROJECT_ROOT%dist"

echo [4/5] Building executable with icon...
cd "%PROJECT_ROOT%"
pyinstaller --onefile ^
            --windowed ^
            --clean ^
            --noconfirm ^
            --icon="%ICON_FILE%" ^
            --name="%OUTPUT_NAME%" ^
            --add-data "configs;configs" ^
            "%SRC_FILE%"

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo [5/5] Build complete!
echo.
echo ========================================
echo   SUCCESS!
echo   Output: dist\%OUTPUT_NAME%.exe
echo   Icon: %ICON_FILE%
echo ========================================
echo.

REM Check if file exists
if exist "%PROJECT_ROOT%dist\%OUTPUT_NAME%.exe" (
    for %%A in ("%PROJECT_ROOT%dist\%OUTPUT_NAME%.exe") do (
        echo File size: %%~zA bytes
    )
    echo.
    echo You can now run: %PROJECT_ROOT%dist\%OUTPUT_NAME%.exe
) else (
    echo [WARNING] Executable not found in dist folder
)

pause