#!/bin/bash
# Hunyuan Quickstart Installer - Linux/WSL2 Launcher

echo "========================================"
echo "Hunyuan Quickstart Installer"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using your package manager"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"

# Check for tkinter
echo "Checking dependencies..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "tkinter not found. Installing..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3-tk
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-tkinter
    else
        echo "WARNING: Could not auto-install tkinter"
        echo "Please install python3-tk manually"
    fi
fi

echo ""
echo "Launching installer GUI..."
echo ""

python3 installer_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to launch installer"
    exit 1
fi

