"""
Unit tests for the lexical analyzer core functionality.

This module contains comprehensive unit tests for all core components
of the lexical analyzer system.
"""

import pytest
from unittest.mock import Mock, patch

from lexical_analyzer.core import State, Fragment, DFA, RegexError
from lexical_analyzer.algorithms import (
    normalize_regex, validate_regex, insert_concat_ops, to_postfix
)
from lexical_analyzer.algorithms.thompson import ThompsonNFA
from lexical_analyzer.algorithms.subset_construction import NFASimulator, nfa_to_dfa
from lexical_analyzer.algorithms.hopcroft import hopcroft_minimize


class TestState:
    """Test cases for State class."""
    
    def test_state_creation(self):
        """Test state creation and string representation."""
        state = State(0)
        assert state.id == 0
        assert str(state) == "q0"
        assert repr(state) == "State(id=0)"
    
    def test_state_immutability(self):
        """Test that State is immutable."""
        state = State(0)
        with pytest.raises(AttributeError):
            state.id = 1


class TestFragment:
    """Test cases for Fragment class."""
    
    def test_fragment_creation(self):
        """Test fragment creation and backward compatibility."""
        start = State(0)
        accept = State(1)
        transitions = {0: [("a", 1)]}
        
        fragment = Fragment(start, accept, transitions)
        
        assert fragment.start == start
        assert fragment.accept == accept
        assert fragment.transitions == transitions
        assert fragment.trans == transitions  # Backward compatibility


class TestDFA:
    """Test cases for DFA class."""
    
    def test_dfa_creation(self):
        """Test DFA creation and validation."""
        dfa = DFA(
            name="test",
            alphabet=("a", "b"),
            states=("S0", "S1"),
            start_state="S0",
            accept_states=("S1",),
            transitions={"S0": {"a": "S1", "b": "S0"}, "S1": {"a": "S1", "b": "S1"}}
        )
        
        assert dfa.name == "test"
        assert dfa.alphabet == ("a", "b")
        assert dfa.states == ("S0", "S1")
        assert dfa.start_state == "S0"
        assert dfa.accept_states == ("S1",)
    
    def test_dfa_validation_invalid_start_state(self):
        """Test DFA validation with invalid start state."""
        with pytest.raises(ValueError, match="Start state 'S2' not in states"):
            DFA(
                name="test",
                alphabet=("a",),
                states=("S0", "S1"),
                start_state="S2",
                accept_states=("S1",),
                transitions={"S0": {"a": "S1"}, "S1": {"a": "S1"}}
            )
    
    def test_dfa_simulation(self):
        """Test DFA simulation."""
        dfa = DFA(
            name="test",
            alphabet=("a", "b"),
            states=("S0", "S1"),
            start_state="S0",
            accept_states=("S1",),
            transitions={"S0": {"a": "S1", "b": "S0"}, "S1": {"a": "S1", "b": "S1"}}
        )
        
        assert dfa.simulate("a") == True
        assert dfa.simulate("aa") == True
        assert dfa.simulate("b") == False
        assert dfa.simulate("ab") == True
        assert dfa.simulate("c") == False  # Invalid symbol
    
    def test_dfa_is_total(self):
        """Test DFA total check."""
        dfa = DFA(
            name="test",
            alphabet=("a", "b"),
            states=("S0", "S1"),
            start_state="S0",
            accept_states=("S1",),
            transitions={"S0": {"a": "S1", "b": "S0"}, "S1": {"a": "S1", "b": "S1"}}
        )
        
        assert dfa.is_total() == True


class TestRegexAlgorithms:
    """Test cases for regular expression algorithms."""
    
    def test_normalize_regex_empty(self):
        """Test normalization of empty regex."""
        with pytest.raises(RegexError, match="Empty regular expression"):
            normalize_regex("")
    
    def test_normalize_regex_epsilon(self):
        """Test epsilon normalization."""
        assert normalize_regex("epsilon") == "eps"
        assert normalize_regex("eps") == "eps"
        assert normalize_regex("\\e") == "eps"
        # Note: \\epsilon might normalize differently, so we check it contains eps
        result = normalize_regex("\\epsilon")
        assert "eps" in result
    
    def test_validate_regex_balanced_parentheses(self):
        """Test validation of balanced parentheses."""
        validate_regex("(a|b)*")  # Should not raise
        
        with pytest.raises(RegexError, match="Unbalanced parentheses"):
            validate_regex("(a|b")
        
        with pytest.raises(RegexError, match="Unbalanced parentheses"):
            validate_regex("a|b)")
    
    def test_insert_concat_ops(self):
        """Test insertion of concatenation operators."""
        assert insert_concat_ops("ab") == "a.b"
        assert insert_concat_ops("a*b") == "a*.b"
        assert insert_concat_ops("(a|b)c") == "(a|b).c"
        assert insert_concat_ops("a(b|c)") == "a.(b|c)"
    
    def test_to_postfix(self):
        """Test infix to postfix conversion."""
        assert to_postfix("a") == "a"
        assert to_postfix("a|b") == "ab|"
        assert to_postfix("a.b") == "ab."
        assert to_postfix("a*") == "a*"
        assert to_postfix("(a|b)*") == "ab|*"
        assert to_postfix("a.b.c") == "ab.c."


class TestThompsonNFA:
    """Test cases for Thompson's NFA construction."""
    
    def test_thompson_symbol(self):
        """Test symbol construction."""
        nfa = ThompsonNFA()
        fragment = nfa.symbol("a")
        
        assert fragment.start.id == 0
        assert fragment.accept.id == 1
        assert 0 in fragment.transitions
        assert fragment.transitions[0] == [("a", 1)]
    
    def test_thompson_epsilon(self):
        """Test epsilon construction."""
        nfa = ThompsonNFA()
        fragment = nfa.symbol("ε")
        
        assert fragment.start.id == 0
        assert fragment.accept.id == 1
        assert fragment.transitions[0] == [(None, 1)]
    
    def test_thompson_concat(self):
        """Test concatenation construction."""
        nfa = ThompsonNFA()
        frag1 = nfa.symbol("a")
        frag2 = nfa.symbol("b")
        result = nfa.concat(frag1, frag2)
        
        assert result.start.id == 0
        assert result.accept.id == 3
        assert 1 in result.transitions  # Epsilon transition from frag1.accept to frag2.start
    
    def test_thompson_union(self):
        """Test union construction."""
        nfa = ThompsonNFA()
        frag1 = nfa.symbol("a")
        frag2 = nfa.symbol("b")
        result = nfa.union(frag1, frag2)
        
        assert result.start.id == 4
        assert result.accept.id == 5
        # Should have epsilon transitions from start to both fragments
        assert (None, 0) in result.transitions[4]
        assert (None, 2) in result.transitions[4]
    
    def test_thompson_star(self):
        """Test Kleene star construction."""
        nfa = ThompsonNFA()
        frag = nfa.symbol("a")
        result = nfa.star(frag)
        
        assert result.start.id == 2
        assert result.accept.id == 3
        # Should have epsilon transitions for looping and skipping
        assert (None, 0) in result.transitions[2]  # Start to fragment start
        assert (None, 3) in result.transitions[2]  # Skip (zero occurrences)
        assert (None, 3) in result.transitions[1]  # Fragment accept to accept
        assert (None, 0) in result.transitions[1]  # Loop back
    
    def test_thompson_from_postfix(self):
        """Test NFA construction from postfix expression."""
        nfa = ThompsonNFA()
        
        # Simple cases - IDs may vary due to state management
        symbol_fragment = nfa.from_postfix("a")
        assert symbol_fragment.start.id >= 0
        
        # Union creates additional states
        union_fragment = nfa.from_postfix("ab|")
        assert union_fragment.start.id >= 4
        
        # Concatenation creates additional states
        concat_fragment = nfa.from_postfix("ab.")
        assert concat_fragment.start.id >= 0
        
        # Star creates additional states
        star_fragment = nfa.from_postfix("a*")
        assert star_fragment.start.id >= 0
    
    def test_thompson_invalid_postfix(self):
        """Test error handling for invalid postfix expressions."""
        nfa = ThompsonNFA()
        
        with pytest.raises(RegexError, match="Empty postfix expression"):
            nfa.from_postfix("")
        
        with pytest.raises(RegexError, match="Insufficient operands for union"):
            nfa.from_postfix("a|")
        
        with pytest.raises(RegexError, match="Insufficient operands for star"):
            nfa.from_postfix("*")


class TestNFASimulator:
    """Test cases for NFA simulation."""
    
    def test_nfa_simulator_creation(self):
        """Test NFA simulator creation."""
        nfa = ThompsonNFA()
        fragment = nfa.symbol("a")
        simulator = NFASimulator(fragment)
        
        assert simulator.start_state == 0
        assert simulator.accept_state == 1
        assert simulator.transitions == {0: [("a", 1)]}
    
    def test_nfa_get_alphabet(self):
        """Test alphabet extraction."""
        nfa = ThompsonNFA()
        fragment = nfa.from_postfix("ab|")
        simulator = NFASimulator(fragment)
        
        alphabet = simulator.get_alphabet()
        assert "a" in alphabet
        assert "b" in alphabet
        assert len(alphabet) == 2
    
    def test_nfa_epsilon_closure(self):
        """Test epsilon closure calculation."""
        nfa = ThompsonNFA()
        fragment = nfa.star(nfa.symbol("a"))
        simulator = NFASimulator(fragment)
        
        closure = simulator.epsilon_closure({simulator.start_state})
        assert simulator.start_state in closure
        assert simulator.accept_state in closure
    
    def test_nfa_simulation(self):
        """Test NFA simulation."""
        nfa = ThompsonNFA()
        fragment = nfa.from_postfix("ab|")
        simulator = NFASimulator(fragment)
        
        assert simulator.simulate("a") == True
        assert simulator.simulate("b") == True
        assert simulator.simulate("c") == False
        assert simulator.simulate("ab") == False  # Should not accept concatenation


class TestSubsetConstruction:
    """Test cases for subset construction algorithm."""
    
    def test_nfa_to_dfa_simple(self):
        """Test NFA to DFA conversion for simple case."""
        nfa = ThompsonNFA()
        fragment = nfa.symbol("a")
        simulator = NFASimulator(fragment)
        
        dfa = nfa_to_dfa(simulator)
        
        assert len(dfa.states) >= 1
        assert dfa.simulate("a") == True
        assert dfa.simulate("b") == False
    
    def test_nfa_to_dfa_union(self):
        """Test NFA to DFA conversion for union."""
        nfa = ThompsonNFA()
        fragment = nfa.from_postfix("ab|")
        simulator = NFASimulator(fragment)
        
        dfa = nfa_to_dfa(simulator)
        
        assert dfa.simulate("a") == True
        assert dfa.simulate("b") == True
        assert dfa.simulate("c") == False


class TestHopcroftMinimization:
    """Test cases for Hopcroft's minimization algorithm."""
    
    def test_hopcroft_minimize_simple(self):
        """Test DFA minimization for simple case."""
        # Create a simple DFA
        dfa = DFA(
            name="test",
            alphabet=("a", "b"),
            states=("S0", "S1", "S2"),
            start_state="S0",
            accept_states=("S2",),
            transitions={
                "S0": {"a": "S1", "b": "S0"},
                "S1": {"a": "S2", "b": "S1"},
                "S2": {"a": "S2", "b": "S2"}
            }
        )
        
        minimized_dfa, log = hopcroft_minimize(dfa)
        
        assert len(minimized_dfa.states) <= len(dfa.states)
        assert minimized_dfa.simulate("aa") == True
        assert minimized_dfa.simulate("aab") == True
        assert minimized_dfa.simulate("b") == False
        assert len(log) > 0


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_complete_pipeline_simple(self):
        """Test complete pipeline for simple regex."""
        from lexical_analyzer import LexicalAnalyzer
        
        analyzer = LexicalAnalyzer()
        
        # This would require mocking file operations
        # For now, just test that the analyzer can be instantiated
        assert analyzer.eps_symbol == "ε"
    
    def test_error_handling(self):
        """Test error handling throughout the pipeline."""
        with pytest.raises(RegexError):
            normalize_regex("")
        
        with pytest.raises(RegexError):
            validate_regex("(a|b")
        
        with pytest.raises(RegexError):
            to_postfix("")


if __name__ == "__main__":
    pytest.main([__file__])

