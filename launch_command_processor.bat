@echo off
echo 🎮 GTA5 Command Processor Launcher
echo ===================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 🔍 Checking dependencies...
python -c "import vgamepad" >nul 2>&1
if errorlevel 1 (
    echo ❌ VgamePad not found! Installing...
    pip install vgamepad
    if errorlevel 1 (
        echo ❌ Failed to install vgamepad
        pause
        exit /b 1
    )
)

python -c "import win32gui" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyWin32 not found! Installing...
    pip install pywin32
    if errorlevel 1 (
        echo ❌ Failed to install pywin32
        pause
        exit /b 1
    )
)

echo ✅ All dependencies ready
echo.

REM Check if GTA5 is running
echo 🔍 Checking for GTA5...
python -c "import win32gui; windows = []; win32gui.EnumWindows(lambda hwnd, w: w.append((hwnd, win32gui.GetWindowText(hwnd))) if 'Grand Theft Auto V' in win32gui.GetWindowText(hwnd) else None, windows); print('GTA5 found!' if windows else 'GTA5 not found!')" 2>nul
if errorlevel 1 (
    echo ⚠️  GTA5 window detection failed. Make sure GTA5 is running.
)

echo.
echo 🚀 Starting GTA5 Command Processor...
echo 💡 Make sure GTA5 is running and loaded into a game!
echo 💡 Type 'help' for available commands
echo 💡 Type 'exit' to quit
echo.

REM Run the command processor
python command_processor.py

pause
