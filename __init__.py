"""
ComfyUI Telegram Bot Custom Nodes

A collection of custom nodes for ComfyUI that enable Telegram bot integration.
"""

try:
    from .telegram_nodes import TelegramListener, SaveToTelegram
except ImportError:
    # Handle case where running tests or importing without package structure
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from telegram_nodes import TelegramListener, SaveToTelegram

# Version info
__version__ = "1.0.0"

# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "TelegramListener": TelegramListener,
    "SaveToTelegram": SaveToTelegram,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TelegramListener": "Telegram Listener",
    "SaveToTelegram": "Save to Telegram",
}

# Web directory for UI components
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
