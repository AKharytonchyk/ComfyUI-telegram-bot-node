import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio
import queue
import threading
import time

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock telegram imports before importing our module
sys.modules['telegram'] = Mock()
sys.modules['telegram.ext'] = Mock()

# Mock the telegram components
mock_update = Mock()
mock_context = Mock()
mock_application = Mock()
mock_message_handler = Mock()
mock_filters = Mock()

sys.modules['telegram'].Update = mock_update
sys.modules['telegram.ext'].Application = mock_application
sys.modules['telegram.ext'].MessageHandler = mock_message_handler
sys.modules['telegram.ext'].filters = mock_filters
sys.modules['telegram.ext'].ContextTypes = Mock()

from telegram_nodes import TelegramListener, SaveToTelegram


class TestTelegramListener(unittest.TestCase):
    """Test cases for TelegramListener node"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.listener = TelegramListener()
    
    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.listener, '_stop_bot'):
            self.listener._stop_bot()
    
    def test_input_types_structure(self):
        """Test that INPUT_TYPES returns correct structure"""
        input_types = TelegramListener.INPUT_TYPES()
        
        # Check required keys exist
        self.assertIn('required', input_types)
        self.assertIn('bot_token', input_types['required'])
        self.assertIn('timeout', input_types['required'])
        
        # Check bot_token structure
        bot_token_config = input_types['required']['bot_token']
        self.assertEqual(bot_token_config[0], 'STRING')
        self.assertIn('default', bot_token_config[1])
        self.assertIn('placeholder', bot_token_config[1])
        
        # Check timeout structure
        timeout_config = input_types['required']['timeout']
        self.assertEqual(timeout_config[0], 'INT')
        self.assertIn('min', timeout_config[1])
        self.assertIn('max', timeout_config[1])
    
    def test_class_attributes(self):
        """Test that class attributes are correctly defined"""
        self.assertEqual(TelegramListener.RETURN_TYPES, ("STRING", "STRING"))
        self.assertEqual(TelegramListener.RETURN_NAMES, ("message_text", "chat_id"))
        self.assertEqual(TelegramListener.FUNCTION, "listen_for_message")
        self.assertEqual(TelegramListener.CATEGORY, "telegram")
        self.assertEqual(TelegramListener.OUTPUT_NODE, False)
    
    def test_initialization(self):
        """Test that TelegramListener initializes correctly"""
        self.assertIsNone(self.listener.bot_token)
        self.assertIsNone(self.listener.application)
        self.assertIsInstance(self.listener.message_queue, queue.Queue)
        self.assertEqual(self.listener.chat_ids, {})
        self.assertFalse(self.listener.is_running)
        self.assertIsNone(self.listener.bot_thread)
    
    def test_listen_for_message_empty_token(self):
        """Test listen_for_message with empty bot token"""
        result = self.listener.listen_for_message("", 10)
        self.assertEqual(result, ("Error: Bot token is required", ""))
        
        result = self.listener.listen_for_message("   ", 10)
        self.assertEqual(result, ("Error: Bot token is required", ""))
    
    def test_listen_for_message_invalid_token_format(self):
        """Test listen_for_message with invalid token format"""
        result = self.listener.listen_for_message("invalid_token", 10)
        self.assertEqual(result, ("Error: Invalid bot token format", ""))
        
        result = self.listener.listen_for_message("bot123", 10)
        self.assertEqual(result, ("Error: Invalid bot token format", ""))
    
    def test_listen_for_message_timeout(self):
        """Test listen_for_message timeout behavior"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        
        with patch.object(self.listener, '_start_bot') as mock_start:
            result = self.listener.listen_for_message(valid_token, 1)  # 1 second timeout
            
            # Should timeout and return no message
            self.assertEqual(result, ("No message received within timeout", ""))
            mock_start.assert_called_once_with(valid_token)
    
    def test_listen_for_message_with_queue_message(self):
        """Test listen_for_message with a message in queue"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        
        # Put a test message in the queue
        test_message = {
            'text': 'Hello, bot!',
            'chat_id': 12345,
            'user_id': 67890,
            'username': 'testuser',
            'timestamp': time.time()
        }
        self.listener.message_queue.put(test_message)
        
        with patch.object(self.listener, '_start_bot'):
            result = self.listener.listen_for_message(valid_token, 10)
            
            self.assertEqual(result, ("Hello, bot!", "12345"))
            self.assertIn("12345", self.listener.chat_ids)
    
    @patch('telegram_nodes.asyncio')
    @patch('telegram_nodes.threading.Thread')
    def test_start_bot(self, mock_thread, mock_asyncio):
        """Test _start_bot method"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        
        # Mock the application builder
        mock_app_builder = Mock()
        mock_app = Mock()
        mock_app_builder.token.return_value = mock_app_builder
        mock_app_builder.build.return_value = mock_app
        
        with patch('telegram_nodes.Application.builder', return_value=mock_app_builder):
            self.listener._start_bot(valid_token)
            
            # Verify token was set
            self.assertEqual(self.listener.bot_token, valid_token)
            
            # Verify thread was created and started
            mock_thread.assert_called_once()
            mock_thread.return_value.start.assert_called_once()


class TestSaveToTelegram(unittest.TestCase):
    """Test cases for SaveToTelegram node"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sender = SaveToTelegram()
    
    def test_input_types_structure(self):
        """Test that INPUT_TYPES returns correct structure"""
        input_types = SaveToTelegram.INPUT_TYPES()
        
        # Check required keys exist
        self.assertIn('required', input_types)
        self.assertIn('bot_token', input_types['required'])
        self.assertIn('chat_id', input_types['required'])
        self.assertIn('message', input_types['required'])
        
        # Check all fields are STRING type
        for field in ['bot_token', 'chat_id', 'message']:
            self.assertEqual(input_types['required'][field][0], 'STRING')
            self.assertIn('placeholder', input_types['required'][field][1])
    
    def test_class_attributes(self):
        """Test that class attributes are correctly defined"""
        self.assertEqual(SaveToTelegram.RETURN_TYPES, ("STRING",))
        self.assertEqual(SaveToTelegram.RETURN_NAMES, ("status",))
        self.assertEqual(SaveToTelegram.FUNCTION, "send_message")
        self.assertEqual(SaveToTelegram.CATEGORY, "telegram")
        self.assertEqual(SaveToTelegram.OUTPUT_NODE, True)
    
    def test_initialization(self):
        """Test that SaveToTelegram initializes correctly"""
        self.assertEqual(self.sender.applications, {})
    
    def test_send_message_empty_token(self):
        """Test send_message with empty bot token"""
        result = self.sender.send_message("", "12345", "Hello")
        self.assertEqual(result, ("Error: Bot token is required",))
    
    def test_send_message_empty_chat_id(self):
        """Test send_message with empty chat ID"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        result = self.sender.send_message(valid_token, "", "Hello")
        self.assertEqual(result, ("Error: Chat ID is required",))
    
    def test_send_message_empty_message(self):
        """Test send_message with empty message"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        result = self.sender.send_message(valid_token, "12345", "")
        self.assertEqual(result, ("Error: Message is required",))
    
    def test_send_message_invalid_chat_id(self):
        """Test send_message with invalid chat ID format"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        result = self.sender.send_message(valid_token, "invalid_id", "Hello")
        self.assertEqual(result, ("Error: Invalid chat ID format: invalid_id",))
    
    @patch('telegram_nodes.asyncio')
    @patch('telegram_nodes.threading.Thread')
    def test_send_message_success(self, mock_thread, mock_asyncio):
        """Test successful message sending"""
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        chat_id = "12345"
        message = "Hello, world!"
        
        # Mock the application and bot
        mock_app_builder = Mock()
        mock_app = Mock()
        mock_bot = Mock()
        
        mock_app_builder.token.return_value = mock_app_builder
        mock_app_builder.build.return_value = mock_app
        mock_app.bot = mock_bot
        
        # Mock successful send_message
        async def mock_send_message(*args, **kwargs):
            return True
        
        mock_bot.send_message = AsyncMock(side_effect=mock_send_message)
        
        with patch('telegram_nodes.Application.builder', return_value=mock_app_builder):
            # Mock the thread execution to run immediately
            def mock_thread_init(target):
                target()
                return Mock()
            
            mock_thread.side_effect = mock_thread_init
            
            result = self.sender.send_message(valid_token, chat_id, message)
            
            # Should return success message
            self.assertIn("Message sent successfully", result[0])
            self.assertIn(chat_id, result[0])


class TestTelegramNodesIntegration(unittest.TestCase):
    """Integration tests for both nodes working together"""
    
    def setUp(self):
        """Set up test fixtures for integration tests"""
        self.listener = TelegramListener()
        self.sender = SaveToTelegram()
    
    def tearDown(self):
        """Clean up after integration tests"""
        if hasattr(self.listener, '_stop_bot'):
            self.listener._stop_bot()
    
    def test_chat_id_transfer(self):
        """Test that chat_id can be transferred from listener to sender"""
        # Simulate a message received by listener
        test_message = {
            'text': 'Test message',
            'chat_id': 12345,
            'user_id': 67890,
            'username': 'testuser',
            'timestamp': time.time()
        }
        self.listener.message_queue.put(test_message)
        
        valid_token = "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        
        with patch.object(self.listener, '_start_bot'):
            # Get message from listener
            message_text, chat_id = self.listener.listen_for_message(valid_token, 10)
            
            # Verify message received correctly
            self.assertEqual(message_text, "Test message")
            self.assertEqual(chat_id, "12345")
            
            # Verify chat_id can be used by sender
            self.assertIsInstance(chat_id, str)
            self.assertTrue(chat_id.isdigit())


class TestModuleImports(unittest.TestCase):
    """Test module imports and dependencies"""
    
    def test_imports_structure(self):
        """Test that the module imports are structured correctly"""
        from telegram_nodes import TelegramListener, SaveToTelegram
        
        # Verify classes exist and are callable
        self.assertTrue(callable(TelegramListener))
        self.assertTrue(callable(SaveToTelegram))
        
        # Verify instances can be created
        listener = TelegramListener()
        sender = SaveToTelegram()
        
        self.assertIsInstance(listener, TelegramListener)
        self.assertIsInstance(sender, SaveToTelegram)


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2)
