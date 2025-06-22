@echo off
REM ComfyUI Telegram Bot Nodes Installation Script for Windows

echo Installing ComfyUI Telegram Bot Nodes...

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
