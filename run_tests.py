#!/usr/bin/env python3
"""
Test runner script for ComfyUI Telegram Bot Nodes

This script runs all unit tests and generates a coverage report.
"""

import sys
import os
import unittest
import argparse
from io import StringIO

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_tests(verbosity=2, pattern='test_*.py', coverage=False):
    """Run all tests with optional coverage reporting"""
    
    if coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
        except ImportError:
            print("Coverage.py not installed. Install with: pip install coverage")
            coverage = False
    
    # Discover and run tests
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern=pattern)
    
    # Create test runner
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream, 
        verbosity=verbosity,
        buffer=True
    )
    
    # Run tests
    print(f"Running tests from {test_dir}")
    print("=" * 70)
    
    result = runner.run(suite)
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    # Print summary
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    # Print detailed failure/error info
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Generate coverage report
    if coverage:
        cov.stop()
        cov.save()
        
        print("\n" + "=" * 70)
        print("COVERAGE REPORT:")
        print("=" * 70)
        cov.report(show_missing=True)
        
        # Generate HTML coverage report
        html_dir = os.path.join(project_root, 'htmlcov')
        cov.html_report(directory=html_dir)
        print(f"\nHTML coverage report generated in: {html_dir}")
    
    return result.wasSuccessful()


def main():
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(description='Run ComfyUI Telegram Bot Nodes tests')
    parser.add_argument('-v', '--verbosity', type=int, default=2, 
                       help='Test output verbosity (0-2)')
    parser.add_argument('-p', '--pattern', default='test_*.py',
                       help='Test file pattern')
    parser.add_argument('-c', '--coverage', action='store_true',
                       help='Generate coverage report')
    parser.add_argument('--specific', type=str,
                       help='Run specific test module (e.g., test_telegram_nodes)')
    
    args = parser.parse_args()
    
    if args.specific:
        # Run specific test module
        test_module = args.specific
        if not test_module.startswith('test_'):
            test_module = f'test_{test_module}'
        if not test_module.endswith('.py'):
            test_module = f'{test_module}.py'
        
        args.pattern = test_module
    
    success = run_tests(
        verbosity=args.verbosity,
        pattern=args.pattern,
        coverage=args.coverage
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
