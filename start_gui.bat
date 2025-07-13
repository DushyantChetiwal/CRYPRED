@echo off
REM Quick start script for CRYPRED Arbitrage GUI

echo 🖥️  Starting CRYPRED Arbitrage GUI
echo =====================================

REM Check if Python is available
python3 --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found! Please install Python 3.x
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python
    )
) else (
    set PYTHON_CMD=python3
)

REM Check if GUI script exists
if not exist "scripts\arbitrage_gui.py" (
    echo ❌ GUI script not found!
    echo    Make sure you're running this from the CRYPRED directory
    pause
    exit /b 1
)

echo ✅ Python found: %PYTHON_CMD%
echo ✅ GUI script found
echo.

echo 📦 Checking dependencies...
%PYTHON_CMD% -c "import matplotlib, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Missing dependencies detected!
    echo 📦 Installing required packages...
    %PYTHON_CMD% -m pip install matplotlib pandas
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        echo 💡 Please run: pip install matplotlib pandas
        pause
        exit /b 1
    )
)

echo ✅ Dependencies verified
echo.

echo 🚀 Features:
echo    • Real-time price charts for INR vs USD
echo    • Interactive navigation with scroll controls
echo    • Live arbitrage opportunity detection
echo    • Historical data viewing from session start
echo    • Multi-cryptocurrency pair monitoring
echo.

echo 🎯 Starting GUI application...
echo ===============================
echo.

REM Start the GUI
%PYTHON_CMD% scripts\arbitrage_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ GUI failed to start
    echo 💡 Check error messages above
    pause
)

echo.
echo 🖥️  GUI application closed
pause 