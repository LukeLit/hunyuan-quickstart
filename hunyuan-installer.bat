@echo off
REM Hunyuan Quickstart Installer - Windows Launcher
echo ========================================
echo Hunyuan Quickstart Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check for required packages
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing tkinter...
    echo Note: tkinter usually comes with Python, but may need to be installed separately
    pause
)

echo.
echo Launching installer GUI...
echo.

python installer_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to launch installer
    pause
    exit /b 1
)

pause

