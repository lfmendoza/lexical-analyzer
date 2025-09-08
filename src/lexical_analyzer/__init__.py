"""
Main lexical analyzer module.

This module provides the main interface for processing regular expressions
through the complete pipeline: normalization → postfix → NFA → DFA → minimized DFA.
"""

import os
import logging
from typing import Dict, Union, List, Tuple
from dataclasses import dataclass

from .core import RegexError
from .algorithms import (
    normalize_regex, validate_regex, insert_concat_ops, to_postfix
)
from .algorithms.thompson import ThompsonNFA
from .algorithms.subset_construction import NFASimulator, nfa_to_dfa, ensure_total_dfa
from .algorithms.hopcroft import hopcroft_minimize
from .visualization import draw_nfa_svg, draw_dfa_svg


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """Result of regular expression processing."""
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


class LexicalAnalyzer:
    """
    Professional lexical analyzer for regular expression processing.
    
    Implements the complete pipeline from regular expressions to minimized DFAs
    with comprehensive error handling and logging.
    """
    
    def __init__(self, eps_symbol: str = "ε"):
        """
        Initialize the lexical analyzer.
        
        Args:
            eps_symbol: Symbol to use for epsilon
        """
        self.eps_symbol = eps_symbol
        logger.info(f"Initialized LexicalAnalyzer with epsilon symbol: {eps_symbol}")
    
    def process_regex(self, regex_raw: str, test_word: str, output_dir: str, 
                     ascii_eps: bool = False) -> ProcessingResult:
        """
        Process a regular expression through the complete pipeline.
        
        Args:
            regex_raw: Raw regular expression in infix notation
            test_word: Word to test against the automata
            output_dir: Directory for output files
            ascii_eps: Use 'eps' instead of 'ε' in SVG files
            
        Returns:
            ProcessingResult with all generated data
            
        Raises:
            RegexError: If there are errors in processing
        """
        logger.info(f"Processing regex: {regex_raw}")
        logger.info(f"Test word: {test_word}")
        logger.info(f"Output directory: {output_dir}")
        
        try:
            # Step 1: Normalization
            logger.debug("Step 1: Normalizing regex")
            regex_normalized = normalize_regex(regex_raw, eps_symbol=self.eps_symbol)
            
            # Step 2: Basic validation
            logger.debug("Step 2: Validating regex structure")
            validate_regex(regex_normalized)
            
            # Step 3: Insert implicit concatenation
            logger.debug("Step 3: Inserting concatenation operators")
            regex_with_concat = insert_concat_ops(regex_normalized)
            
            # Step 4: Convert to postfix (Shunting Yard)
            logger.debug("Step 4: Converting to postfix notation")
            regex_postfix = to_postfix(regex_with_concat)
            
            # Step 5: Build NFA (Thompson)
            logger.debug("Step 5: Building NFA with Thompson's algorithm")
            thompson_nfa = ThompsonNFA()
            nfa_fragment = thompson_nfa.from_postfix(regex_postfix)
            nfa_simulator = NFASimulator(nfa_fragment)
            
            # Step 6: Convert NFA → DFA (Subset construction)
            logger.debug("Step 6: Converting NFA to DFA")
            dfa = nfa_to_dfa(nfa_simulator)
            
            # Step 7: Minimize DFA (Hopcroft)
            logger.debug("Step 7: Minimizing DFA with Hopcroft's algorithm")
            dfa_minimized, minimization_log = hopcroft_minimize(dfa)
            
            # Step 8: Create output directory
            logger.debug("Step 8: Creating output directory")
            os.makedirs(output_dir, exist_ok=True)
            
            # Step 9: Generate SVG visualizations
            logger.debug("Step 9: Generating SVG visualizations")
            nfa_svg_path = os.path.join(output_dir, "nfa.svg")
            draw_nfa_svg(nfa_fragment, nfa_svg_path, ascii_eps=ascii_eps)
            
            dfa_svg_path = os.path.join(output_dir, "dfa.svg")
            draw_dfa_svg(dfa, dfa_svg_path)
            
            dfa_min_svg_path = os.path.join(output_dir, "dfa_min.svg")
            draw_dfa_svg(dfa_minimized, dfa_min_svg_path)
            
            # Step 10: Run simulations
            logger.debug("Step 10: Running simulations")
            nfa_result = nfa_simulator.simulate(test_word)
            dfa_result = dfa.simulate(test_word)
            dfa_min_result = dfa_minimized.simulate(test_word)
            
            # Step 11: Save detailed information
            logger.debug("Step 11: Saving detailed information")
            regex_info_path = os.path.join(output_dir, "regex.txt")
            self._save_processing_info(
                regex_info_path, regex_raw, regex_normalized, regex_with_concat,
                regex_postfix, thompson_nfa, dfa, dfa_minimized, test_word,
                nfa_result, dfa_result, dfa_min_result, minimization_log
            )
            
            logger.info("Processing completed successfully")
            
            return ProcessingResult(
                postfix=regex_postfix,
                nfa_svg_path=nfa_svg_path,
                dfa_svg_path=dfa_svg_path,
                dfa_min_svg_path=dfa_min_svg_path,
                regex_info_path=regex_info_path,
                nfa_accepts=nfa_result,
                dfa_accepts=dfa_result,
                dfa_min_accepts=dfa_min_result,
                nfa_states=thompson_nfa.next_id,
                dfa_states=len(dfa.states),
                dfa_min_states=len(dfa_minimized.states),
                minimization_log=minimization_log
            )
            
        except Exception as e:
            logger.error(f"Error processing regex '{regex_raw}': {str(e)}")
            raise RegexError(f"Error processing expression regular '{regex_raw}': {str(e)}") from e
    
    def _save_processing_info(self, path: str, regex_raw: str, regex_normalized: str,
                             regex_with_concat: str, regex_postfix: str,
                             thompson_nfa: ThompsonNFA, dfa, dfa_minimized,
                             test_word: str, nfa_result: bool, dfa_result: bool,
                             dfa_min_result: bool, minimization_log: List[str]) -> None:
        """Save detailed processing information to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Regular Expression Processing Report\n")
            f.write(f"===================================\n\n")
            f.write(f"Original regex:     {regex_raw}\n")
            f.write(f"Normalized regex:   {regex_normalized}\n")
            f.write(f"With concatenation: {regex_with_concat}\n")
            f.write(f"Postfix notation:    {regex_postfix}\n\n")
            
            f.write(f"Automaton Statistics:\n")
            f.write(f"  NFA states:        {thompson_nfa.next_id}\n")
            f.write(f"  DFA states:        {len(dfa.states)}\n")
            f.write(f"  DFA min states:    {len(dfa_minimized.states)}\n\n")
            
            f.write(f"Simulation Results for '{test_word}':\n")
            f.write(f"  NFA accepts:       {'Yes' if nfa_result else 'No'}\n")
            f.write(f"  DFA accepts:       {'Yes' if dfa_result else 'No'}\n")
            f.write(f"  DFA min accepts:   {'Yes' if dfa_min_result else 'No'}\n\n")
            
            f.write(f"Minimization Log:\n")
            for log_entry in minimization_log:
                f.write(f"  {log_entry}\n")
    
    def process_file(self, input_file: str, test_word: str, output_base_dir: str,
                    ascii_eps: bool = False) -> List[ProcessingResult]:
        """
        Process multiple regular expressions from a file.
        
        Args:
            input_file: Path to file containing regular expressions
            test_word: Word to test against all automata
            output_base_dir: Base directory for output files
            ascii_eps: Use 'eps' instead of 'ε' in SVG files
            
        Returns:
            List of ProcessingResult objects
            
        Raises:
            RegexError: If there are errors in processing
        """
        logger.info(f"Processing file: {input_file}")
        
        regex_list = []
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        regex_list.append((line, line_num))
        except FileNotFoundError:
            raise RegexError(f"Input file not found: {input_file}")
        except Exception as e:
            raise RegexError(f"Error reading input file '{input_file}': {str(e)}")
        
        if not regex_list:
            raise RegexError("No valid regular expressions found in input file")
        
        results = []
        for i, (regex_raw, line_num) in enumerate(regex_list, 1):
            try:
                output_subdir = os.path.join(output_base_dir, f"case_{i:02d}")
                result = self.process_regex(regex_raw, test_word, output_subdir, ascii_eps)
                results.append(result)
                logger.info(f"Successfully processed case {i}: {regex_raw}")
            except RegexError as e:
                logger.error(f"Error in case {i} (line {line_num}): {e}")
                raise
        
        return results

