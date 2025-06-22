import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock telegram imports before importing our module
from unittest.mock import Mock
sys.modules['telegram'] = Mock()
sys.modules['telegram.ext'] = Mock()

# Test the __init__.py module
class TestInit(unittest.TestCase):
    """Test cases for __init__.py module"""
    
    def test_node_mappings_exist(self):
        """Test that NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS exist"""
        import __init__ as init_module
        
        # Check that the mappings exist
        self.assertTrue(hasattr(init_module, 'NODE_CLASS_MAPPINGS'))
        self.assertTrue(hasattr(init_module, 'NODE_DISPLAY_NAME_MAPPINGS'))
        self.assertTrue(hasattr(init_module, 'WEB_DIRECTORY'))
    
    def test_node_class_mappings_structure(self):
        """Test NODE_CLASS_MAPPINGS structure"""
        import __init__ as init_module
        
        mappings = init_module.NODE_CLASS_MAPPINGS
        
        # Check that required nodes exist
        self.assertIn('TelegramListener', mappings)
        self.assertIn('SaveToTelegram', mappings)
        
        # Check that they are callable (classes)
        self.assertTrue(callable(mappings['TelegramListener']))
        self.assertTrue(callable(mappings['SaveToTelegram']))
    
    def test_node_display_name_mappings_structure(self):
        """Test NODE_DISPLAY_NAME_MAPPINGS structure"""
        import __init__ as init_module
        
        display_mappings = init_module.NODE_DISPLAY_NAME_MAPPINGS
        
        # Check that display names exist for all nodes
        self.assertIn('TelegramListener', display_mappings)
        self.assertIn('SaveToTelegram', display_mappings)
        
        # Check that display names are strings
        self.assertIsInstance(display_mappings['TelegramListener'], str)
        self.assertIsInstance(display_mappings['SaveToTelegram'], str)
        
        # Check specific display names
        self.assertEqual(display_mappings['TelegramListener'], 'Telegram Listener')
        self.assertEqual(display_mappings['SaveToTelegram'], 'Save to Telegram')
    
    def test_web_directory_setting(self):
        """Test WEB_DIRECTORY setting"""
        import __init__ as init_module
        
        self.assertEqual(init_module.WEB_DIRECTORY, "./web")
    
    def test_version_exists(self):
        """Test that version is defined"""
        import __init__ as init_module
        
        self.assertTrue(hasattr(init_module, '__version__'))
        self.assertIsInstance(init_module.__version__, str)
        self.assertEqual(init_module.__version__, "1.0.0")
    
    def test_all_exports(self):
        """Test __all__ exports"""
        import __init__ as init_module
        
        self.assertTrue(hasattr(init_module, '__all__'))
        expected_exports = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
        
        for export in expected_exports:
            self.assertIn(export, init_module.__all__)


if __name__ == '__main__':
    unittest.main(verbosity=2)
