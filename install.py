#!/usr/bin/env python3
"""
Simple installation script for the lexical analyzer.

This script installs the package in development mode using pip.
"""

import subprocess
import sys
import os


def install_package():
    """Install the package in development mode."""
    print("Installing Lexical Analyzer in development mode...")
    
    try:
        # Change to the project root directory
        project_root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_root)
        
        # Install the package
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)
        
        print("OK Package installed successfully!")
        print("You can now run:")
        print("   - python examples/example.py")
        print("   - lexical-analyzer --help")
        
    except subprocess.CalledProcessError as e:
        print(f"X Installation failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"X Unexpected error: {e}")
        return False
    
    return True


def test_import():
    """Test if the package can be imported."""
    print("Testing package import...")
    
    try:
        import lexical_analyzer
        print("OK Package imported successfully!")
        return True
    except ImportError as e:
        print(f"X Import failed: {e}")
        return False


if __name__ == "__main__":
    print("Lexical Analyzer Installation Script")
    print("=" * 50)
    
    if install_package():
        test_import()
    
    print("\nNext steps:")
    print("1. Run: python examples/example.py")
    print("2. Or use CLI: lexical-analyzer --help")
