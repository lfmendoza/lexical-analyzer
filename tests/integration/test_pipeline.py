"""
Integration tests for the complete lexical analyzer pipeline.

This module contains tests that verify the complete workflow
from regular expression input to final output.
"""

import pytest
import tempfile
import os
from pathlib import Path

from lexical_analyzer import LexicalAnalyzer, RegexError


@pytest.mark.integration
class TestCompletePipeline:
    """Test the complete processing pipeline."""
    
    def test_single_regex_processing(self):
        """Test processing a single regular expression."""
        analyzer = LexicalAnalyzer()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyzer.process_regex(
                regex_raw="(a|b)*abb",
                test_word="aabb",
                output_dir=temp_dir
            )
            
            # Verify result structure
            assert result.postfix is not None
            assert result.nfa_svg_path is not None
            assert result.dfa_svg_path is not None
            assert result.dfa_min_svg_path is not None
            assert result.regex_info_path is not None
            
            # Verify files were created
            assert os.path.exists(result.nfa_svg_path)
            assert os.path.exists(result.dfa_svg_path)
            assert os.path.exists(result.dfa_min_svg_path)
            assert os.path.exists(result.regex_info_path)
            
            # Verify simulation results
            assert result.nfa_accepts == True
            assert result.dfa_accepts == True
            assert result.dfa_min_accepts == True
    
    def test_file_processing(self):
        """Test processing multiple regexes from a file."""
        analyzer = LexicalAnalyzer()
        
        # Create temporary expressions file
        expressions_content = """# Test expressions
(a|b)*abb
a*b*
(ab)*
a+
a?
"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            expressions_file = os.path.join(temp_dir, "expressions.txt")
            with open(expressions_file, "w") as f:
                f.write(expressions_content)
            
            results = analyzer.process_file(
                input_file=expressions_file,
                test_word="aabb",
                output_base_dir=temp_dir
            )
            
            # Verify we got results for all expressions
            assert len(results) == 5
            
            # Verify each result
            for i, result in enumerate(results):
                assert result.postfix is not None
                assert result.nfa_states > 0
                assert result.dfa_states > 0
                assert result.dfa_min_states > 0
    
    def test_error_handling(self):
        """Test error handling in the pipeline."""
        analyzer = LexicalAnalyzer()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test invalid regex
            with pytest.raises(RegexError):
                analyzer.process_regex(
                    regex_raw="(a|b",  # Unbalanced parentheses
                    test_word="test",
                    output_dir=temp_dir
                )
            
            # Test empty regex
            with pytest.raises(RegexError):
                analyzer.process_regex(
                    regex_raw="",
                    test_word="test",
                    output_dir=temp_dir
                )
    
    def test_different_epsilon_symbols(self):
        """Test different epsilon symbol representations."""
        analyzer = LexicalAnalyzer(eps_symbol="ε")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyzer.process_regex(
                regex_raw="a*ε",
                test_word="a",
                output_dir=temp_dir,
                ascii_eps=True
            )
            
            assert result.postfix is not None
            assert result.nfa_accepts == True
    
    def test_complex_regex_patterns(self):
        """Test complex regular expression patterns."""
        analyzer = LexicalAnalyzer()
        
        test_cases = [
            ("(a|b)*abb(a|b)*", "babbaaaa"),
            ("a*b*", "aabbb"),
            ("(ab)*", "ababab"),
            ("a+", "aaa"),
            ("a?", "a"),
            ("a?", ""),
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for regex, test_word in test_cases:
                result = analyzer.process_regex(
                    regex_raw=regex,
                    test_word=test_word,
                    output_dir=os.path.join(temp_dir, f"test_{regex.replace('|', '_').replace('*', 'star').replace('(', '').replace(')', '')}")
                )
                
                # Basic verification
                assert result.postfix is not None
                assert result.nfa_states > 0
                assert result.dfa_states > 0
                assert result.dfa_min_states > 0
                
                # Verify consistency between automata
                assert result.nfa_accepts == result.dfa_accepts
                assert result.dfa_accepts == result.dfa_min_accepts
    
    def test_output_file_contents(self):
        """Test that output files contain expected content."""
        analyzer = LexicalAnalyzer()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyzer.process_regex(
                regex_raw="(a|b)*abb",
                test_word="aabb",
                output_dir=temp_dir
            )
            
            # Check regex.txt content
            with open(result.regex_info_path, "r") as f:
                content = f.read()
                assert "Regular Expression Processing Report" in content
                assert "(a|b)*abb" in content
                assert "aabb" in content
                assert "NFA accepts" in content
                assert "DFA accepts" in content
            
            # Check SVG files are valid XML
            for svg_path in [result.nfa_svg_path, result.dfa_svg_path, result.dfa_min_svg_path]:
                with open(svg_path, "r") as f:
                    svg_content = f.read()
                    assert svg_content.startswith("<?xml")
                    assert "<svg" in svg_content
                    assert "</svg>" in svg_content


@pytest.mark.integration
class TestCLIIntegration:
    """Test CLI integration."""
    
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        from lexical_analyzer.cli import main, parse_arguments
        assert callable(main)
        assert callable(parse_arguments)
    
    def test_cli_help(self):
        """Test CLI help functionality."""
        import subprocess
        import sys
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "lexical_analyzer.cli", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            assert result.returncode == 0
            assert "Lexical Analyzer" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI test skipped - module not properly installed")


if __name__ == "__main__":
    pytest.main([__file__])
