#!/bin/bash

# ComfyUI Telegram Bot Nodes Installation Script

echo "Installing ComfyUI Telegram Bot Nodes..."

# Check if we're in a ComfyUI custom_nodes directory
if [[ ! -d "../ComfyUI" && ! -f "../main.py" ]]; then
    echo "Warning: This doesn't appear to be a ComfyUI custom_nodes directory"
    echo "Make sure to place this in ComfyUI/custom_nodes/"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    echo "Error: pip not found. Please install the requirements manually:"
    echo "pip install python-telegram-bot==20.7"
    exit 1
fi

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart ComfyUI"
echo "2. Get a bot token from @BotFather on Telegram"
echo "3. Look for 'Telegram Listener' and 'Save to Telegram' nodes in the node menu"
echo ""
echo "For help, check the README.md file"
