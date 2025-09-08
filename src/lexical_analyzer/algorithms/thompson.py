"""
Thompson's construction algorithm for building NFAs from regular expressions.

This module implements Thompson's algorithm for constructing non-deterministic
finite automata (NFA) from regular expressions in postfix notation.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from ..core import State, Fragment, RegexError


@dataclass
class ThompsonNFA:
    """
    Thompson's NFA constructor.
    
    Implements Thompson's construction algorithm for building NFAs from
    regular expressions in postfix notation.
    """
    
    def __init__(self):
        self.next_id = 0
        self._states: List[State] = []
    
    def new_state(self) -> State:
        """Create a new state with unique ID."""
        state = State(self.next_id)
        self.next_id += 1
        self._states.append(state)
        return state
    
    def add_transition(self, transitions: Dict[int, List[Tuple[Optional[str], int]]], 
                      from_state: int, symbol: Optional[str], to_state: int) -> None:
        """Add a transition to the transitions dictionary."""
        if from_state not in transitions:
            transitions[from_state] = []
        transitions[from_state].append((symbol, to_state))
    
    def merge_transitions(self, *transition_dicts) -> Dict[int, List[Tuple[Optional[str], int]]]:
        """Combine multiple transition dictionaries."""
        merged = {}
        for trans_dict in transition_dicts:
            for state, transitions in trans_dict.items():
                if state not in merged:
                    merged[state] = []
                merged[state].extend(transitions)
        return merged
    
    def symbol(self, char: str) -> Fragment:
        """
        Build an NFA fragment for a single symbol.
        
        Args:
            char: Input symbol (can be EPS for epsilon)
            
        Returns:
            NFA fragment that accepts the given symbol
        """
        start = self.new_state()
        accept = self.new_state()
        transitions = {}
        
        # Create transition with the given symbol
        symbol = None if char == "ε" else char
        self.add_transition(transitions, start.id, symbol, accept.id)
        
        return Fragment(start, accept, transitions)
    
    def concat(self, frag1: Fragment, frag2: Fragment) -> Fragment:
        """
        Concatenate two NFA fragments.
        
        Args:
            frag1: First fragment
            frag2: Second fragment
            
        Returns:
            Concatenated NFA fragment
        """
        # Connect frag1's accept state to frag2's start state with epsilon
        merged_transitions = self.merge_transitions(frag1.transitions, frag2.transitions)
        self.add_transition(merged_transitions, frag1.accept.id, None, frag2.start.id)
        
        return Fragment(frag1.start, frag2.accept, merged_transitions)
    
    def union(self, frag1: Fragment, frag2: Fragment) -> Fragment:
        """
        Create union of two NFA fragments.
        
        Args:
            frag1: First fragment
            frag2: Second fragment
            
        Returns:
            Union NFA fragment
        """
        start = self.new_state()
        accept = self.new_state()
        
        # Merge transitions from both fragments
        merged_transitions = self.merge_transitions(frag1.transitions, frag2.transitions)
        
        # Add epsilon transitions from new start to both fragment starts
        self.add_transition(merged_transitions, start.id, None, frag1.start.id)
        self.add_transition(merged_transitions, start.id, None, frag2.start.id)
        
        # Add epsilon transitions from both fragment accepts to new accept
        self.add_transition(merged_transitions, frag1.accept.id, None, accept.id)
        self.add_transition(merged_transitions, frag2.accept.id, None, accept.id)
        
        return Fragment(start, accept, merged_transitions)
    
    def star(self, frag: Fragment) -> Fragment:
        """
        Apply Kleene star to an NFA fragment.
        
        Args:
            frag: Fragment to apply star to
            
        Returns:
            NFA fragment with Kleene star applied
        """
        start = self.new_state()
        accept = self.new_state()
        
        # Add all original transitions
        transitions = dict(frag.transitions)
        
        # Add epsilon transitions
        self.add_transition(transitions, start.id, None, frag.start.id)  # Start to fragment start
        self.add_transition(transitions, frag.accept.id, None, accept.id)  # Fragment accept to accept
        self.add_transition(transitions, frag.accept.id, None, frag.start.id)  # Loop back
        self.add_transition(transitions, start.id, None, accept.id)  # Skip (zero occurrences)
        
        return Fragment(start, accept, transitions)
    
    def plus(self, frag: Fragment) -> Fragment:
        """
        Apply plus operator to an NFA fragment.
        
        Args:
            frag: Fragment to apply plus to
            
        Returns:
            NFA fragment with plus applied
        """
        # Plus is equivalent to concatenation with star
        return self.concat(frag, self.star(frag))
    
    def optional(self, frag: Fragment) -> Fragment:
        """
        Apply optional operator to an NFA fragment.
        
        Args:
            frag: Fragment to apply optional to
            
        Returns:
            NFA fragment with optional applied
        """
        start = self.new_state()
        accept = self.new_state()
        
        # Add all original transitions
        transitions = dict(frag.transitions)
        
        # Add epsilon transitions
        self.add_transition(transitions, start.id, None, frag.start.id)  # Start to fragment start
        self.add_transition(transitions, frag.accept.id, None, accept.id)  # Fragment accept to accept
        self.add_transition(transitions, start.id, None, accept.id)  # Skip (zero occurrences)
        
        return Fragment(start, accept, transitions)
    
    def from_postfix(self, postfix_regex: str) -> Fragment:
        """
        Build NFA from postfix regular expression.
        
        Args:
            postfix_regex: Regular expression in postfix notation
            
        Returns:
            Complete NFA fragment
            
        Raises:
            RegexError: If the postfix expression is invalid
        """
        if not postfix_regex:
            raise RegexError("Empty postfix expression")
        
        stack: List[Fragment] = []
        
        for char in postfix_regex:
            if char == "ε" or (char not in {"*", "+", "?", "|", "."} and char.isprintable()):
                # Symbol or epsilon
                stack.append(self.symbol(char))
            elif char == ".":
                # Concatenation
                if len(stack) < 2:
                    raise RegexError("Insufficient operands for concatenation")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(self.concat(frag1, frag2))
            elif char == "|":
                # Union
                if len(stack) < 2:
                    raise RegexError("Insufficient operands for union")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(self.union(frag1, frag2))
            elif char == "*":
                # Kleene star
                if not stack:
                    raise RegexError("Insufficient operands for star")
                frag = stack.pop()
                stack.append(self.star(frag))
            elif char == "+":
                # Plus
                if not stack:
                    raise RegexError("Insufficient operands for plus")
                frag = stack.pop()
                stack.append(self.plus(frag))
            elif char == "?":
                # Optional
                if not stack:
                    raise RegexError("Insufficient operands for optional")
                frag = stack.pop()
                stack.append(self.optional(frag))
            else:
                raise RegexError(f"Invalid character in postfix expression: {repr(char)}")
        
        if len(stack) != 1:
            raise RegexError(f"Invalid expression: {len(stack)} fragments remaining")
        
        return stack[0]

