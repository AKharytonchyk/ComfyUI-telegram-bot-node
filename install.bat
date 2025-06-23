@echo off
REM ComfyUI Telegram Bot Nodes Installation Script for Windows

echo Installing ComfyUI Telegram Bot Nodes...

REM Check if we're in the correct ComfyUI directory structure
REM The correct structure should be: ComfyUI\custom_nodes\ComfyUI-telegram-bot-node\
if not exist "..\..\main.py" if not exist "..\..\comfyui_main.py" (
    echo Warning: This doesn't appear to be in ComfyUI\custom_nodes\ directory
    echo Expected structure: ComfyUI\custom_nodes\ComfyUI-telegram-bot-node\
    echo Current location: %CD%
    echo.
    echo To install correctly:
    echo 1. Place this folder in ComfyUI\custom_nodes\
    echo 2. Run this script from within the folder
    echo.
    set /p continue="Continue anyway? (y/N): "
    if /i not "%continue%"=="y" (
        echo Installation cancelled.
        pause
        exit /b 1
    )
)

REM Check if we're in the right directory
if not exist "requirements.txt" (
    echo Error: requirements.txt not found in current directory
    echo Please run this script from the ComfyUI-telegram-bot-node directory
    pause
    exit /b 1
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    echo Please run: pip install python-telegram-bot==20.7
    pause
    exit /b 1
)

echo Installation complete!
echo.
echo Next steps:
echo 1. Restart ComfyUI
echo 2. Get a bot token from @BotFather on Telegram
echo 3. Look for 'Telegram Listener' and 'Save to Telegram' nodes in the node menu
echo.
echo For help, check the README.md file
pause
