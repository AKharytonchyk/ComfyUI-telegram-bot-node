import asyncio
import threading
import queue
import time
from typing import Dict, Any, Optional, Tuple
import logging

try:
    from telegram import Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
except ImportError:
    print("Please install python-telegram-bot: pip install python-telegram-bot")
    raise


class TelegramListener:
    """
    A ComfyUI node that listens to Telegram messages and outputs the text content.
    """
    
    def __init__(self):
        self.bot_token = None
        self.application = None
        self.message_queue = queue.Queue()
        self.chat_ids = {}  # Store chat IDs for responses
        self.is_running = False
        self.bot_thread = None
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot_token": ("STRING", {"default": "", "multiline": False}),
                "timeout": ("INT", {"default": 10, "min": 1, "max": 300}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("message_text", "chat_id")
    FUNCTION = "listen_for_message"
    CATEGORY = "telegram"
    
    def listen_for_message(self, bot_token: str, timeout: int) -> Tuple[str, str]:
        """
        Listen for Telegram messages and return the message text and chat ID.
        """
        if not bot_token:
            return ("Error: Bot token is required", "")
            
        # If bot token changed or not running, restart the bot
        if self.bot_token != bot_token or not self.is_running:
            self._stop_bot()
            self._start_bot(bot_token)
        
        # Wait for a message with timeout
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                message_data = self.message_queue.get(timeout=1)
                chat_id = str(message_data['chat_id'])
                message_text = message_data['text']
                
                # Store chat ID for potential response
                self.chat_ids[chat_id] = message_data['chat_id']
                
                return (message_text, chat_id)
            except queue.Empty:
                continue
        
        return ("No message received within timeout", "")
    
    def _start_bot(self, bot_token: str):
        """Start the Telegram bot in a separate thread."""
        self.bot_token = bot_token
        
        def run_bot():
            try:
                # Create application
                self.application = Application.builder().token(bot_token).build()
                
                # Add message handler
                message_handler = MessageHandler(
                    filters.TEXT & ~filters.COMMAND, 
                    self._handle_message
                )
                self.application.add_handler(message_handler)
                
                # Run the bot
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                self.is_running = True
                loop.run_until_complete(self.application.run_polling(stop_signals=None))
                
            except Exception as e:
                logging.error(f"Bot error: {e}")
                self.is_running = False
        
        self.bot_thread = threading.Thread(target=run_bot, daemon=True)
        self.bot_thread.start()
    
    def _stop_bot(self):
        """Stop the running bot."""
        if self.application and self.is_running:
            try:
                # Stop the application
                asyncio.run(self.application.stop())
                self.is_running = False
            except Exception as e:
                logging.error(f"Error stopping bot: {e}")
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming Telegram messages."""
        if update.message and update.message.text:
            message_data = {
                'text': update.message.text,
                'chat_id': update.message.chat_id,
                'user_id': update.message.from_user.id,
                'username': update.message.from_user.username or "",
                'timestamp': time.time()
            }
            self.message_queue.put(message_data)


class SaveToTelegram:
    """
    A ComfyUI node that sends messages back to Telegram chats.
    """
    
    def __init__(self):
        self.applications = {}  # Store applications by bot token
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bot_token": ("STRING", {"default": "", "multiline": False}),
                "chat_id": ("STRING", {"default": "", "multiline": False}),
                "message": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "send_message"
    CATEGORY = "telegram"
    
    def send_message(self, bot_token: str, chat_id: str, message: str) -> Tuple[str]:
        """
        Send a message to a Telegram chat.
        """
        if not bot_token:
            return ("Error: Bot token is required",)
        
        if not chat_id:
            return ("Error: Chat ID is required",)
        
        if not message:
            return ("Error: Message is required",)
        
        try:
            # Convert chat_id to int if it's numeric
            try:
                chat_id_int = int(chat_id)
            except ValueError:
                return (f"Error: Invalid chat ID format: {chat_id}",)
            
            # Get or create application for this bot token
            if bot_token not in self.applications:
                self.applications[bot_token] = Application.builder().token(bot_token).build()
            
            application = self.applications[bot_token]
            
            # Send message synchronously
            async def send_async():
                await application.bot.send_message(chat_id=chat_id_int, text=message)
            
            # Run in event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is already running, create a new one in a thread
                    def run_in_thread():
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        new_loop.run_until_complete(send_async())
                        new_loop.close()
                    
                    thread = threading.Thread(target=run_in_thread)
                    thread.start()
                    thread.join()
                else:
                    loop.run_until_complete(send_async())
            except RuntimeError:
                # No event loop, create one
                asyncio.run(send_async())
            
            return (f"Message sent successfully to chat {chat_id}",)
            
        except Exception as e:
            return (f"Error sending message: {str(e)}",)
