# Lexical Analyzer

A professional implementation of regular expression processing algorithms for lexical analysis, following industry standards and best practices.

## Features

- **Shunting Yard Algorithm**: Robust infix to postfix conversion
- **Thompson's Construction**: Efficient NFA generation from regular expressions
- **Subset Construction**: NFA to DFA conversion with epsilon-closure
- **Hopcroft's Algorithm**: DFA minimization with state partitioning
- **Professional Visualization**: High-quality SVG generation
- **Comprehensive Testing**: Unit and integration tests
- **Industry Standards**: Type hints, logging, error handling, and documentation

## Installation

### Using Poetry (Recommended)

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone <repository-url>
cd lexical-analyzer

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Process single regular expression
lexical-analyzer --regex "(a|b)*abb" --word "aabb" --outdir results

# Process multiple expressions from file
lexical-analyzer --input expressions.txt --word "test" --outdir results

# Use ASCII epsilon symbol
lexical-analyzer --regex "a*" --word "aaa" --ascii-eps --outdir results

# Verbose output
lexical-analyzer --regex "a*b*" --word "ab" --verbose --outdir results
```

### Programmatic Usage

```python
from lexical_analyzer import LexicalAnalyzer

# Initialize analyzer
analyzer = LexicalAnalyzer(eps_symbol="ε")

# Process single regex
result = analyzer.process_regex(
    regex_raw="(a|b)*abb",
    test_word="aabb",
    output_dir="./results"
)

print(f"Postfix: {result.postfix}")
print(f"NFA accepts: {result.nfa_accepts}")
print(f"DFA accepts: {result.dfa_accepts}")
print(f"Minimized DFA accepts: {result.dfa_min_accepts}")

# Process multiple regexes from file
results = analyzer.process_file(
    input_file="expressions.txt",
    test_word="test",
    output_base_dir="./results"
)
```

## Project Structure

```
lexical-analyzer/
├── src/
│   └── lexical_analyzer/
│       ├── algorithms/          # Core algorithms
│       │   ├── __init__.py
│       │   ├── thompson.py      # Thompson's construction
│       │   ├── subset_construction.py  # NFA to DFA
│       │   └── hopcroft.py      # DFA minimization
│       ├── core/                # Core data structures
│       │   └── __init__.py
│       ├── visualization/       # SVG generation
│       │   └── __init__.py
│       ├── __init__.py
│       └── cli.py              # Command line interface
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── docs/                       # Documentation
├── examples/                   # Usage examples
├── scripts/                    # Utility scripts
├── config/                     # Configuration files
├── pyproject.toml             # Project configuration
├── .pre-commit-config.yaml    # Pre-commit hooks
└── README.md                  # This file
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
poetry install --with dev

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/lexical_analyzer --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Code Quality

The project follows strict code quality standards:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks

## API Reference

### Core Classes

#### `LexicalAnalyzer`

Main class for processing regular expressions.

```python
class LexicalAnalyzer:
    def __init__(self, eps_symbol: str = "ε"):
        """Initialize the lexical analyzer."""
    
    def process_regex(self, regex_raw: str, test_word: str, 
                     output_dir: str, ascii_eps: bool = False) -> ProcessingResult:
        """Process a single regular expression."""
    
    def process_file(self, input_file: str, test_word: str,
                    output_base_dir: str, ascii_eps: bool = False) -> List[ProcessingResult]:
        """Process multiple regular expressions from a file."""
```

#### `ProcessingResult`

Result of regular expression processing.

```python
@dataclass
class ProcessingResult:
    postfix: str
    nfa_svg_path: str
    dfa_svg_path: str
    dfa_min_svg_path: str
    regex_info_path: str
    nfa_accepts: bool
    dfa_accepts: bool
    dfa_min_accepts: bool
    nfa_states: int
    dfa_states: int
    dfa_min_states: int
    minimization_log: List[str]
```

### Algorithms

#### Thompson's Construction

```python
class ThompsonNFA:
    def symbol(self, char: str) -> Fragment:
        """Build NFA fragment for a single symbol."""
    
    def concat(self, frag1: Fragment, frag2: Fragment) -> Fragment:
        """Concatenate two NFA fragments."""
    
    def union(self, frag1: Fragment, frag2: Fragment) -> Fragment:
        """Create union of two NFA fragments."""
    
    def star(self, frag: Fragment) -> Fragment:
        """Apply Kleene star to an NFA fragment."""
    
    def from_postfix(self, postfix_regex: str) -> Fragment:
        """Build NFA from postfix regular expression."""
```

#### Subset Construction

```python
def nfa_to_dfa(nfa: NFASimulator) -> DFA:
    """Convert NFA to DFA using subset construction algorithm."""

class NFASimulator:
    def epsilon_closure(self, states: Set[int]) -> Set[int]:
        """Calculate epsilon-closure of a set of states."""
    
    def move(self, states: Set[int], symbol: str) -> Set[int]:
        """Calculate states reachable with a symbol."""
    
    def simulate(self, input_string: str) -> bool:
        """Simulate the NFA with an input string."""
```

#### Hopcroft's Minimization

```python
def hopcroft_minimize(dfa: DFA) -> Tuple[DFA, List[str]]:
    """Minimize a DFA using Hopcroft's algorithm."""
```

## Output Files

For each processed regular expression, the following files are generated:

- **`nfa.svg`**: NFA visualization
- **`dfa.svg`**: DFA visualization  
- **`dfa_min.svg`**: Minimized DFA visualization
- **`regex.txt`**: Detailed processing information

## Error Handling

The system provides comprehensive error handling with custom exceptions:

```python
class RegexError(Exception):
    """Custom exception for regular expression processing errors."""
```

Common error scenarios:
- Invalid regular expression syntax
- Unbalanced parentheses or brackets
- Insufficient operands for operators
- File I/O errors
- Invalid automaton states

## Performance

The implementation is optimized for performance:

- **Caching**: Epsilon-closure and alphabet calculations are cached
- **Efficient Data Structures**: Uses appropriate data structures for each algorithm
- **Memory Management**: Proper cleanup and resource management
- **Algorithmic Complexity**: Follows optimal complexity bounds

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Run code quality checks
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thompson's construction algorithm
- Hopcroft's minimization algorithm
- Shunting Yard algorithm
- Subset construction algorithm