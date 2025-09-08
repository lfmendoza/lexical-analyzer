#!/usr/bin/env python3
"""
Professional CLI for the Lexical Analyzer.

This module provides a command-line interface following industry standards
with comprehensive error handling, logging, and user experience.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import List, Tuple

from lexical_analyzer import LexicalAnalyzer, RegexError


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments with comprehensive help."""
    parser = argparse.ArgumentParser(
        prog="lexical-analyzer",
        description="""
Lexical Analyzer - Professional Regular Expression Processing

Implements industry-standard algorithms for regular expression processing:
• Shunting Yard algorithm for infix -> postfix conversion
• Thompson's construction for NFA generation
• Subset construction for NFA -> DFA conversion
• Hopcroft's algorithm for DFA minimization
• Comprehensive simulation and SVG visualization

This tool processes regular expressions through the complete pipeline and
generates professional visualizations suitable for academic and industrial use.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single regex
  lexical-analyzer --regex "(a|b)*abb" --word "aabb" --outdir results

  # Process multiple regexes from file
  lexical-analyzer --input expressions.txt --word "test" --outdir results

  # Use ASCII epsilon symbol
  lexical-analyzer --regex "a*" --word "aaa" --ascii-eps --outdir results

  # Verbose output with detailed logging
  lexical-analyzer --regex "a*b*" --word "ab" --verbose --outdir results
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--regex", 
        help="Single regular expression in infix notation"
    )
    input_group.add_argument(
        "--input", 
        help="File containing regular expressions (one per line)"
    )
    
    # Required arguments
    parser.add_argument(
        "--word", 
        required=True,
        help="Test word to verify against generated automata"
    )
    parser.add_argument(
        "--outdir", 
        default="./outputs",
        help="Output directory for generated files (default: ./outputs)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--ascii-eps", 
        action="store_true",
        help="Use 'eps' instead of 'ε' in SVG visualizations"
    )
    parser.add_argument(
        "--eps", 
        default="ε",
        help="Symbol to use for epsilon (default: ε)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose logging output"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="Lexical Analyzer 1.0.0"
    )
    
    return parser.parse_args()


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate command line arguments."""
    # Check if input file exists
    if args.input and not Path(args.input).exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")
    
    # Check if output directory is writable
    output_path = Path(args.outdir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Cannot create output directory: {args.outdir}")


def process_single_regex(analyzer: LexicalAnalyzer, args: argparse.Namespace) -> None:
    """Process a single regular expression."""
    print(f"Processing single regular expression...")
    print(f"Regex: {args.regex}")
    print(f"Test word: '{args.word}'")
    print(f"Output directory: {args.outdir}")
    print("-" * 60)
    
    try:
        result = analyzer.process_regex(
            args.regex, 
            args.word, 
            args.outdir, 
            ascii_eps=args.ascii_eps
        )
        
        print("✓ Processing completed successfully")
        print(f"  Postfix: {result.postfix}")
        print(f"  States: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
        print(f"  Accepts '{args.word}': NFA={'Yes' if result.nfa_accepts else 'No'}, "
              f"DFA={'Yes' if result.dfa_accepts else 'No'}, "
              f"Min={'Yes' if result.dfa_min_accepts else 'No'}")
        print(f"  Files generated in: {args.outdir}")
        
    except RegexError as e:
        print(f"✗ Error processing regular expression: {e}")
        sys.exit(1)


def process_file_regexes(analyzer: LexicalAnalyzer, args: argparse.Namespace) -> None:
    """Process multiple regular expressions from a file."""
    print(f"Processing regular expressions from file...")
    print(f"Input file: {args.input}")
    print(f"Test word: '{args.word}'")
    print(f"Output directory: {args.outdir}")
    print("-" * 60)
    
    try:
        results = analyzer.process_file(
            args.input,
            args.word,
            args.outdir,
            ascii_eps=args.ascii_eps
        )
        
        print(f"✓ Successfully processed {len(results)} regular expressions")
        
        for i, result in enumerate(results, 1):
            print(f"[{i}] Postfix: {result.postfix}")
            print(f"     States: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
            print(f"     Accepts '{args.word}': NFA={'Yes' if result.nfa_accepts else 'No'}, "
                  f"DFA={'Yes' if result.dfa_accepts else 'No'}, "
                  f"Min={'Yes' if result.dfa_min_accepts else 'No'}")
        
        print(f"Files generated in: {args.outdir}")
        
    except RegexError as e:
        print(f"✗ Error processing file: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        # Parse and validate arguments
        args = parse_arguments()
        validate_arguments(args)
        
        # Setup logging
        setup_logging(args.verbose)
        logger = logging.getLogger(__name__)
        logger.info("Starting Lexical Analyzer")
        
        # Initialize analyzer
        analyzer = LexicalAnalyzer(eps_symbol=args.eps)
        
        # Process based on input type
        if args.regex:
            process_single_regex(analyzer, args)
        else:
            process_file_regexes(analyzer, args)
        
        logger.info("Lexical Analyzer completed successfully")
        
    except KeyboardInterrupt:
        print("\nX Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"X Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

