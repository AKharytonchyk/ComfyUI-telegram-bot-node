#!/bin/bash

# ComfyUI Telegram Bot Nodes Installation Script

echo "Installing ComfyUI Telegram Bot Nodes..."

# Check if we're in a ComfyUI custom_nodes directory
# The correct structure should be: ComfyUI/custom_nodes/ComfyUI-telegram-bot-node/
if [[ ! -f "../../main.py" && ! -f "../../comfyui_main.py" ]]; then
    echo "Warning: This doesn't appear to be in ComfyUI/custom_nodes/ directory"
    echo "Expected structure: ComfyUI/custom_nodes/ComfyUI-telegram-bot-node/"
    echo "Current location: $(pwd)"
    echo ""
    echo "To install correctly:"
    echo "1. Place this folder in ComfyUI/custom_nodes/"
    echo "2. Run this script from within the folder"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
fi

# Check if we're already inside the custom node directory
if [[ ! -f "requirements.txt" ]]; then
    echo "Error: requirements.txt not found in current directory"
    echo "Please run this script from the ComfyUI-telegram-bot-node directory"
    exit 1
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
