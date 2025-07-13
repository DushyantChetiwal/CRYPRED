@echo off
REM Quick start script for CRYPRED Hyperfrequent Arbitrage

echo 🚀 Starting CRYPRED Hyperfrequent Arbitrage System
echo ================================================

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

REM Check if script exists
if not exist "scripts\hyperfrequent_arbitrage.py" (
    echo ❌ Arbitrage script not found!
    echo    Make sure you're running this from the CRYPRED directory
    pause
    exit /b 1
)

echo ✅ Python found: %PYTHON_CMD%
echo ✅ Arbitrage script found
echo.

REM Get interval from user or use default
set /p interval="⏰ Enter check interval in seconds (default: 10): " || set interval=10

REM Validate interval
if "%interval%"=="" set interval=10
echo|set /p dummy="🔄 Using interval: %interval% seconds"
echo.

echo 💡 Tips:
echo    • Press Ctrl+C to stop the arbitrage monitor
echo    • Logs are saved to arbitrage_runner.log
echo    • Opportunities are saved to data/arbitrage/
echo    • For automatic startup, run: setup_windows_task.ps1
echo.

echo 🚀 Starting arbitrage monitor...
echo ================================
echo.

REM Start the arbitrage system
%PYTHON_CMD% scripts\hyperfrequent_arbitrage.py %interval%

echo.
echo 🛑 Arbitrage monitor stopped
pause 