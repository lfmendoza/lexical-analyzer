#!/usr/bin/env python3
"""
Setup script for the Lexical Analyzer project.

This script handles the complete setup of the development environment
including virtual environment creation, dependency installation, and
pre-commit hook configuration.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_requirements() -> bool:
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    requirements = {
        "python": "Python 3.8+",
        "poetry": "Poetry package manager",
        "git": "Git version control"
    }
    
    all_good = True
    for tool, description in requirements.items():
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True)
            print(f"✅ {description} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {description} is not installed")
            all_good = False
    
    return all_good


def setup_poetry() -> bool:
    """Setup Poetry and install dependencies."""
    print("📦 Setting up Poetry...")
    
    commands = [
        ("poetry install", "Installing dependencies"),
        ("poetry install --with dev", "Installing development dependencies"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def setup_pre_commit() -> bool:
    """Setup pre-commit hooks."""
    print("🪝 Setting up pre-commit hooks...")
    
    commands = [
        ("poetry run pre-commit install", "Installing pre-commit hooks"),
        ("poetry run pre-commit install --hook-type commit-msg", "Installing commit-msg hook"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def run_tests() -> bool:
    """Run the test suite to verify setup."""
    print("🧪 Running tests...")
    
    commands = [
        ("poetry run pytest tests/unit/ -v", "Running unit tests"),
        ("poetry run pytest tests/integration/ -v", "Running integration tests"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def run_linting() -> bool:
    """Run code quality checks."""
    print("🔍 Running code quality checks...")
    
    commands = [
        ("poetry run black --check src/ tests/", "Checking code formatting"),
        ("poetry run isort --check-only src/ tests/", "Checking import sorting"),
        ("poetry run flake8 src/ tests/", "Running linting"),
        ("poetry run mypy src/", "Running type checking"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def create_example_files() -> bool:
    """Create example files for testing."""
    print("📝 Creating example files...")
    
    try:
        # Create example expressions file
        examples_dir = Path("examples")
        examples_dir.mkdir(exist_ok=True)
        
        with open(examples_dir / "expressions.txt", "w") as f:
            f.write("# Example regular expressions\n")
            f.write("(a|b)*abb\n")
            f.write("a*b*\n")
            f.write("(a|b)*\n")
            f.write("a+\n")
            f.write("(ab)*\n")
        
        # Create example script
        with open(examples_dir / "example.py", "w") as f:
            f.write('''#!/usr/bin/env python3
"""
Example usage of the Lexical Analyzer.
"""

from lexical_analyzer import LexicalAnalyzer

def main():
    # Initialize analyzer
    analyzer = LexicalAnalyzer()
    
    # Process a simple regular expression
    result = analyzer.process_regex(
        regex_raw="(a|b)*abb",
        test_word="aabb",
        output_dir="./example_output"
    )
    
    print(f"Processing completed!")
    print(f"Postfix: {result.postfix}")
    print(f"NFA accepts 'aabb': {result.nfa_accepts}")
    print(f"DFA accepts 'aabb': {result.dfa_accepts}")
    print(f"Minimized DFA accepts 'aabb': {result.dfa_min_accepts}")
    print(f"States: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")

if __name__ == "__main__":
    main()
''')
        
        print("✅ Example files created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create example files: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Lexical Analyzer Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing tools.")
        sys.exit(1)
    
    # Setup Poetry
    if not setup_poetry():
        print("\n❌ Poetry setup failed.")
        sys.exit(1)
    
    # Setup pre-commit hooks
    if not setup_pre_commit():
        print("\n❌ Pre-commit setup failed.")
        sys.exit(1)
    
    # Create example files
    if not create_example_files():
        print("\n❌ Example file creation failed.")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed.")
        sys.exit(1)
    
    # Run linting
    if not run_linting():
        print("\n❌ Linting failed.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment: poetry shell")
    print("2. Run the analyzer: poetry run lexical-analyzer --help")
    print("3. Try the example: python examples/example.py")
    print("4. Run tests: poetry run pytest")
    print("5. Check code quality: poetry run pre-commit run --all-files")


if __name__ == "__main__":
    main()

