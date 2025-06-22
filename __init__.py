"""
ComfyUI Telegram Bot Custom Nodes

A collection of custom nodes for ComfyUI that enable Telegram bot integration.
"""

from .telegram_nodes import TelegramListener, SaveToTelegram

NODE_CLASS_MAPPINGS = {
    "TelegramListener": TelegramListener,
    "SaveToTelegram": SaveToTelegram,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TelegramListener": "Telegram Listener",
    "SaveToTelegram": "Save to Telegram",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
