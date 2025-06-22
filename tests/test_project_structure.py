import unittest
from unittest.mock import patch, Mock
import json
import os
import sys

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests import BaseTestCase


class TestProjectStructure(BaseTestCase):
    """Test the overall project structure and configuration files"""
    
    def test_required_files_exist(self):
        """Test that all required files exist"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        required_files = [
            '__init__.py',
            'telegram_nodes.py',
            'requirements.txt',
            'README.md',
            'LICENSE',
            'setup.py',
            'pyproject.toml',
            'node_list.json',
            'package.json',
            '.gitignore',
            'web/telegram_nodes.js',
            'install.sh',
            'install.bat'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(project_root, file_path)
            self.assertTrue(os.path.exists(full_path), f"Required file missing: {file_path}")
    
    def test_package_json_structure(self):
        """Test package.json structure"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        package_json_path = os.path.join(project_root, 'package.json')
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        # Check required fields
        required_fields = ['name', 'version', 'description', 'keywords', 'license']
        for field in required_fields:
            self.assertIn(field, package_data)
        
        # Check specific values
        self.assertEqual(package_data['name'], 'comfyui-telegram-bot-node')
        self.assertEqual(package_data['version'], '1.0.0')
        self.assertEqual(package_data['license'], 'MIT')
        
        # Check keywords include telegram
        self.assertIn('telegram', package_data['keywords'])
        self.assertIn('comfyui', package_data['keywords'])
    
    def test_node_list_json_structure(self):
        """Test node_list.json structure for ComfyUI Manager compatibility"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        node_list_path = os.path.join(project_root, 'node_list.json')
        
        with open(node_list_path, 'r') as f:
            node_data = json.load(f)
        
        # Check required fields for ComfyUI Manager
        required_fields = ['name', 'description', 'version', 'install_type', 'pip']
        for field in required_fields:
            self.assertIn(field, node_data)
        
        # Check specific values
        self.assertEqual(node_data['install_type'], 'git-clone')
        self.assertIn('python-telegram-bot', node_data['pip'])
        self.assertIn('telegram', node_data['keywords'])
    
    def test_requirements_txt_content(self):
        """Test requirements.txt contains necessary dependencies"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        requirements_path = os.path.join(project_root, 'requirements.txt')
        
        with open(requirements_path, 'r') as f:
            requirements = f.read().strip()
        
        # Should contain python-telegram-bot
        self.assertIn('python-telegram-bot', requirements)
    
    def test_readme_sections(self):
        """Test README.md has required sections"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        readme_path = os.path.join(project_root, 'README.md')
        
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        # Check for important sections
        required_sections = [
            '# ComfyUI Telegram Bot Custom Nodes',
            '## Features',
            '## Installation',
            '## Setup',
            '## Usage',
            '## Example',
            '## License'
        ]
        
        for section in required_sections:
            self.assertIn(section, readme_content, f"README missing section: {section}")
    
    def test_web_directory_structure(self):
        """Test web directory contains required JavaScript files"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        web_dir = os.path.join(project_root, 'web')
        
        self.assertTrue(os.path.exists(web_dir))
        
        js_file = os.path.join(web_dir, 'telegram_nodes.js')
        self.assertTrue(os.path.exists(js_file))
        
        # Check JavaScript file contains ComfyUI integration
        with open(js_file, 'r') as f:
            js_content = f.read()
        
        # Should contain ComfyUI app registration
        self.assertIn('app.registerExtension', js_content)
        self.assertIn('TelegramListener', js_content)
        self.assertIn('SaveToTelegram', js_content)
    
    def test_install_scripts_exist_and_executable(self):
        """Test that install scripts exist"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Check shell script exists
        install_sh = os.path.join(project_root, 'install.sh')
        self.assertTrue(os.path.exists(install_sh))
        
        # Check batch script exists
        install_bat = os.path.join(project_root, 'install.bat')
        self.assertTrue(os.path.exists(install_bat))
        
        # Check shell script has executable permission (on Unix-like systems)
        if os.name != 'nt':  # Not Windows
            import stat
            file_stat = os.stat(install_sh)
            self.assertTrue(file_stat.st_mode & stat.S_IEXEC)
    
    def test_examples_directory(self):
        """Test examples directory structure"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        examples_dir = os.path.join(project_root, 'examples')
        
        self.assertTrue(os.path.exists(examples_dir))
        
        # Check for workflow files
        workflow_json = os.path.join(examples_dir, 'telegram_echo_workflow.json')
        workflow_md = os.path.join(examples_dir, 'echo_bot_workflow.md')
        
        self.assertTrue(os.path.exists(workflow_json))
        self.assertTrue(os.path.exists(workflow_md))
        
        # Validate JSON format
        with open(workflow_json, 'r') as f:
            workflow_data = json.load(f)
        
        # Should contain nodes
        self.assertIn('nodes', workflow_data)
        self.assertGreater(len(workflow_data['nodes']), 0)


class TestGitConfiguration(BaseTestCase):
    """Test git-related configuration"""
    
    def test_gitignore_content(self):
        """Test .gitignore contains appropriate exclusions"""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gitignore_path = os.path.join(project_root, '.gitignore')
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        # Check for important exclusions
        important_exclusions = [
            '__pycache__/',
            '*.pyc',
            '.venv/',
            'venv/',
            '.DS_Store',
            '*.log'
        ]
        
        for exclusion in important_exclusions:
            self.assertIn(exclusion, gitignore_content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
