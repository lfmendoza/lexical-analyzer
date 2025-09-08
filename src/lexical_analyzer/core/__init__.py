"""
Core data structures and types for the lexical analyzer.

This module contains the fundamental data structures used throughout
the lexical analysis system, including states, fragments, and automata.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set, Mapping
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class State:
    """
    Represents a state in a finite automaton.
    
    Attributes:
        id: Unique identifier for the state
    """
    id: int
    
    def __str__(self) -> str:
        return f"q{self.id}"
    
    def __repr__(self) -> str:
        return f"State(id={self.id})"


@dataclass
class Fragment:
    """
    Represents a fragment of an NFA used in Thompson's construction.
    
    Attributes:
        start: Starting state of the fragment
        accept: Accepting state of the fragment
        transitions: Dictionary mapping states to their transitions
    """
    start: State
    accept: State
    transitions: Dict[int, List[Tuple[Optional[str], int]]]
    
    def __post_init__(self) -> None:
        """Maintain backward compatibility with 'trans' attribute."""
        if not hasattr(self, 'trans'):
            self.trans = self.transitions


@dataclass(frozen=True)
class DFA:
    """
    Represents a Deterministic Finite Automaton (DFA).
    
    Immutable data structure to ensure consistency and thread safety.
    """
    name: str
    alphabet: Tuple[str, ...]
    states: Tuple[str, ...]
    start_state: str
    accept_states: Tuple[str, ...]
    transitions: Mapping[str, Mapping[str, str]]
    
    def __post_init__(self) -> None:
        """Validate DFA structure after initialization."""
        if self.start_state not in self.states:
            raise ValueError(f"Start state '{self.start_state}' not in states")
        
        for accept_state in self.accept_states:
            if accept_state not in self.states:
                raise ValueError(f"Accept state '{accept_state}' not in states")
        
        for state in self.states:
            if state not in self.transitions:
                raise ValueError(f"State '{state}' missing transitions")
            
            for symbol in self.alphabet:
                if symbol not in self.transitions[state]:
                    raise ValueError(f"Missing transition for state '{state}' and symbol '{symbol}'")
                
                next_state = self.transitions[state][symbol]
                if next_state not in self.states:
                    raise ValueError(f"Invalid destination state '{next_state}' from '{state}' with '{symbol}'")
    
    def simulate(self, input_string: str) -> bool:
        """
        Simulate the DFA with an input string.
        
        Args:
            input_string: String to process
            
        Returns:
            True if the string is accepted, False otherwise
        """
        current_state = self.start_state
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            
            current_state = self.transitions[current_state][symbol]
        
        return current_state in self.accept_states
    
    def is_total(self) -> bool:
        """
        Check if the DFA is total (has transitions for all states and symbols).
        
        Returns:
            True if the DFA is total, False otherwise
        """
        for state in self.states:
            if state not in self.transitions:
                return False
            
            for symbol in self.alphabet:
                if symbol not in self.transitions[state]:
                    return False
        
        return True


class Automaton(ABC):
    """Abstract base class for finite automata."""
    
    @abstractmethod
    def simulate(self, input_string: str) -> bool:
        """Simulate the automaton with an input string."""
        pass
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if the automaton is valid."""
        pass


class RegexError(Exception):
    """Custom exception for regular expression processing errors."""
    pass

