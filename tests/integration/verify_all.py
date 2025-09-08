#!/usr/bin/env python3
"""
Complete verification script for the lexical analyzer.

This script verifies that all functionality mentioned in the README actually works.
"""

import sys
import os
import subprocess
import tempfile
import shutil

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, "src"))


def test_import():
    """Test if the package can be imported."""
    print("1. Testing package import...")
    try:
        import lexical_analyzer
        print("   OK Package imported successfully!")
        return True
    except ImportError as e:
        print(f"   X Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality."""
    print("2. Testing basic functionality...")
    try:
        from lexical_analyzer import LexicalAnalyzer
        
        analyzer = LexicalAnalyzer()
        result = analyzer.process_regex(
            regex_raw="a",
            test_word="a",
            output_dir="./temp_test"
        )
        
        # Clean up
        if os.path.exists("./temp_test"):
            shutil.rmtree("./temp_test")
        
        print("   OK Basic functionality works!")
        return True
    except Exception as e:
        print(f"   X Basic functionality failed: {e}")
        return False


def test_cli_help():
    """Test CLI help command."""
    print("3. Testing CLI help command...")
    try:
        # Try to run the CLI help command
        result = subprocess.run([
            sys.executable, "-m", "lexical_analyzer.cli", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "Lexical Analyzer" in result.stdout:
            print("   OK CLI help command works!")
            return True
        else:
            print(f"   X CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   X CLI test failed: {e}")
        return False


def test_example_script():
    """Test the example script."""
    print("4. Testing example script...")
    try:
        result = subprocess.run([
            sys.executable, "examples/example.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   OK Example script works!")
            return True
        else:
            print(f"   X Example script failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   X Example script test failed: {e}")
        return False


def test_installation():
    """Test package installation."""
    print("5. Testing package installation...")
    try:
        # Try to install the package
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Package installation works!")
            return True
        else:
            print(f"   ❌ Installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Installation test failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("🧪 Lexical Analyzer Complete Verification")
    print("=" * 50)
    
    tests = [
        test_import,
        test_basic_functionality,
        test_cli_help,
        test_example_script,
        test_installation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results:")
    print(f"   Passed: {passed}/{total}")
    print(f"   Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! The project is working correctly.")
        print("\n💡 You can now:")
        print("   1. Run: python examples/example.py")
        print("   2. Use CLI: lexical-analyzer --help")
        print("   3. Install: python install.py")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check the issues above.")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
