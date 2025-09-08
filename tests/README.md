# Testing Documentation

This directory contains comprehensive tests for the Lexical Analyzer project.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_basic.py       # Basic functionality tests
│   └── test_core.py        # Core data structure tests
└── integration/            # Integration tests for complete workflows
    ├── test_pipeline.py     # Complete pipeline tests
    └── verify_all.py       # Comprehensive verification script
```

## Running Tests

### Unit Tests
```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Run specific test file
python tests/unit/test_basic.py
python tests/unit/test_core.py
```

### Integration Tests
```bash
# Run all integration tests
python -m pytest tests/integration/ -v

# Run specific test file
python tests/integration/test_pipeline.py
python tests/integration/verify_all.py
```

### Complete Test Suite
```bash
# Run all tests with coverage
python -m pytest tests/ --cov=lexical_analyzer --cov-report=html

# Run comprehensive verification
python tests/integration/verify_all.py
```

## Test Categories

### Unit Tests (`tests/unit/`)

#### `test_basic.py`
- **Purpose**: Basic functionality verification
- **Tests**: Import, initialization, simple regex processing
- **Usage**: Quick verification that the package works
- **Run**: `python tests/unit/test_basic.py`

#### `test_core.py`
- **Purpose**: Core data structure and algorithm tests
- **Tests**: State, Fragment, DFA classes and algorithms
- **Coverage**: All core components individually
- **Run**: `python -m pytest tests/unit/test_core.py -v`

### Integration Tests (`tests/integration/`)

#### `test_pipeline.py`
- **Purpose**: Complete workflow testing
- **Tests**: Full pipeline from regex to visualization
- **Coverage**: End-to-end functionality
- **Run**: `python -m pytest tests/integration/test_pipeline.py -v`

#### `verify_all.py`
- **Purpose**: Comprehensive verification script
- **Tests**: All functionality mentioned in README
- **Coverage**: CLI, examples, installation, everything
- **Run**: `python tests/integration/verify_all.py`

## Test Data

### Example Expressions (`examples/expressions.txt`)
Contains test regular expressions used by integration tests:
- Basic patterns: `a`, `b`, `ab`
- Operators: `a*`, `a+`, `a?`, `a|b`
- Complex patterns: `(a|b)*abb`, `a*b*`
- Epsilon patterns: `ε`, `a*ε`, `ε*`

## Test Output

Tests generate temporary output directories that are automatically cleaned up:
- `temp_test/` - Basic functionality tests
- `test_output/` - Integration test outputs
- `example_output*/` - Example script outputs

## Continuous Integration

Tests are automatically run in CI/CD pipeline:
- **Unit tests**: Fast, isolated component tests
- **Integration tests**: Complete workflow verification
- **Coverage reporting**: HTML and XML coverage reports
- **Linting**: Code quality checks

## Adding New Tests

### Unit Test Template
```python
import pytest
from lexical_analyzer import SomeClass

def test_some_functionality():
    """Test description."""
    # Arrange
    obj = SomeClass()
    
    # Act
    result = obj.some_method()
    
    # Assert
    assert result == expected_value
```

### Integration Test Template
```python
import pytest
import tempfile
import os
from lexical_analyzer import LexicalAnalyzer

@pytest.mark.integration
def test_complete_workflow():
    """Test complete workflow."""
    with tempfile.TemporaryDirectory() as temp_dir:
        analyzer = LexicalAnalyzer()
        result = analyzer.process_regex("a", "a", temp_dir)
        assert result.nfa_accepts == True
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure package is installed with `pip install -e .`
2. **Path Issues**: Run tests from project root directory
3. **Permission Errors**: Ensure write permissions for test output directories

### Debug Mode
```bash
# Run with verbose output
python -m pytest tests/ -v -s

# Run specific test with debugging
python -c "
import sys
sys.path.insert(0, '.')
from tests.unit.test_basic import test_basic_functionality
test_basic_functionality()
"
```
