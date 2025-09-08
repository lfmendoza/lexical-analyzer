#!/usr/bin/env python3
"""
Simple test script to verify the lexical analyzer works.

This script tests the basic functionality without requiring package installation.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_basic_functionality():
    """Test basic functionality of the lexical analyzer."""
    print("Testing Lexical Analyzer Basic Functionality")
    print("=" * 50)
    
    # Test import
    print("1. Testing import...")
    from lexical_analyzer import LexicalAnalyzer
    print("   OK Import successful!")
    
    # Test initialization
    print("2. Testing initialization...")
    analyzer = LexicalAnalyzer()
    print("   OK Analyzer created successfully!")
    
    # Test simple regex processing
    print("3. Testing simple regex processing...")
    result = analyzer.process_regex(
        regex_raw="a",
        test_word="a",
        output_dir="./test_output"
    )
    print("   OK Simple regex processing successful!")
    print(f"   Result: {result.postfix}")
    print(f"   Accepts 'a': {result.nfa_accepts}")
    
    # Clean up test output
    import shutil
    if os.path.exists("./test_output"):
        shutil.rmtree("./test_output")
    
    print("\nAll tests passed!")
    # Test passed - no return value needed for pytest


if __name__ == "__main__":
    try:
        test_basic_functionality()
        print("\nNext steps:")
        print("1. Install: python install.py")
        print("2. Run: python examples/example.py")
        print("3. Or use CLI: lexical-analyzer --help")
    except Exception as e:
        print(f"\nX Tests failed: {e}")
        sys.exit(1)
