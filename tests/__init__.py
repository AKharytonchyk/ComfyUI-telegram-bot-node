# Test configuration and utilities

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Mock telegram dependencies for all tests
def mock_telegram_imports():
    """Mock telegram imports to avoid dependency issues during testing"""
    telegram_mock = Mock()
    telegram_ext_mock = Mock()
    
    # Mock main telegram module
    sys.modules['telegram'] = telegram_mock
    sys.modules['telegram.ext'] = telegram_ext_mock
    
    # Mock specific classes and functions
    telegram_mock.Update = Mock()
    telegram_ext_mock.Application = Mock()
    telegram_ext_mock.MessageHandler = Mock()
    telegram_ext_mock.filters = Mock()
    telegram_ext_mock.ContextTypes = Mock()
    
    # Mock Application.builder() chain
    mock_builder = Mock()
    mock_app = Mock()
    mock_builder.token.return_value = mock_builder
    mock_builder.build.return_value = mock_app
    telegram_ext_mock.Application.builder.return_value = mock_builder
    
    return telegram_mock, telegram_ext_mock

# Apply mocks globally for all test modules
mock_telegram_imports()


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and utilities"""
    
    def setUp(self):
        """Common setup for all test cases"""
        # Ensure mocks are in place
        mock_telegram_imports()
    
    def create_valid_bot_token(self):
        """Create a valid-looking bot token for testing"""
        return "bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    
    def create_test_message(self, text="Test message", chat_id=12345, user_id=67890, username="testuser"):
        """Create a test message dictionary"""
        import time
        return {
            'text': text,
            'chat_id': chat_id,
            'user_id': user_id,
            'username': username,
            'timestamp': time.time()
        }
    
    def assertValidComfyUINodeStructure(self, node_class):
        """Assert that a class follows ComfyUI node structure"""
        # Check required class methods exist
        self.assertTrue(hasattr(node_class, 'INPUT_TYPES'))
        self.assertTrue(callable(getattr(node_class, 'INPUT_TYPES')))
        
        # Check required class attributes
        self.assertTrue(hasattr(node_class, 'RETURN_TYPES'))
        self.assertTrue(hasattr(node_class, 'FUNCTION'))
        self.assertTrue(hasattr(node_class, 'CATEGORY'))
        
        # Check INPUT_TYPES structure
        input_types = node_class.INPUT_TYPES()
        self.assertIsInstance(input_types, dict)
        self.assertIn('required', input_types)
        
        # Check that RETURN_TYPES is a tuple
        self.assertIsInstance(node_class.RETURN_TYPES, tuple)
        
        # Check that FUNCTION is a string
        self.assertIsInstance(node_class.FUNCTION, str)
        
        # Check that CATEGORY is a string
        self.assertIsInstance(node_class.CATEGORY, str)


def run_all_tests():
    """Run all tests in the tests directory"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run all tests when this module is executed directly
    success = run_all_tests()
    sys.exit(0 if success else 1)
