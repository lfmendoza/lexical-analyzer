"""
NFA simulation and subset construction algorithms.

This module implements NFA simulation with epsilon-closure and the subset
construction algorithm for converting NFAs to DFAs.
"""

from typing import Dict, List, Set, Tuple, Optional, Mapping
from dataclasses import dataclass

from ..core import Fragment, DFA, RegexError


@dataclass
class NFASimulator:
    """
    NFA simulator with epsilon-closure and state transition capabilities.
    
    Implements efficient algorithms for NFA simulation and analysis.
    """
    
    def __init__(self, fragment: Fragment):
        """
        Initialize simulator with an NFA fragment.
        
        Args:
            fragment: NFA fragment to simulate
        """
        self.start_state = fragment.start.id
        self.accept_state = fragment.accept.id
        self.transitions = fragment.transitions
        
        # Cache for optimization
        self._alphabet_cache: Optional[List[str]] = None
        self._epsilon_closure_cache: Dict[int, Set[int]] = {}
    
    def get_alphabet(self) -> List[str]:
        """
        Get the alphabet of the NFA (symbols other than epsilon).
        
        Returns:
            Sorted list of symbols in the alphabet
        """
        if self._alphabet_cache is not None:
            return self._alphabet_cache
        
        symbols = set()
        for state_transitions in self.transitions.values():
            for symbol, _ in state_transitions:
                if symbol is not None:
                    symbols.add(symbol)
        
        self._alphabet_cache = sorted(symbols)
        return self._alphabet_cache
    
    def epsilon_closure(self, states: Set[int]) -> Set[int]:
        """
        Calculate epsilon-closure of a set of states.
        
        Args:
            states: Set of initial states
            
        Returns:
            Set of states reachable via epsilon transitions
        """
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            
            # Check cache first
            if state in self._epsilon_closure_cache:
                cached_closure = self._epsilon_closure_cache[state]
                closure.update(cached_closure)
                continue
            
            # Calculate epsilon closure for this state
            state_closure = {state}
            state_stack = [state]
            
            while state_stack:
                current_state = state_stack.pop()
                for trans_symbol, next_state in self.transitions.get(current_state, []):
                    if trans_symbol is None and next_state not in state_closure:
                        state_closure.add(next_state)
                        state_stack.append(next_state)
            
            # Cache the result
            self._epsilon_closure_cache[state] = state_closure
            closure.update(state_closure)
        
        return closure
    
    def move(self, states: Set[int], symbol: str) -> Set[int]:
        """
        Calculate the set of states reachable from a given set with a symbol.
        
        Args:
            states: Set of initial states
            symbol: Input symbol
            
        Returns:
            Set of states reachable with the given symbol
        """
        result = set()
        
        for state in states:
            for trans_symbol, next_state in self.transitions.get(state, []):
                if trans_symbol == symbol:
                    result.add(next_state)
        
        return result
    
    def simulate(self, input_string: str) -> bool:
        """
        Simulate the NFA with an input string.
        
        Args:
            input_string: String to process
            
        Returns:
            True if the string is accepted, False otherwise
        """
        # Initial state: epsilon closure of start state
        current_states = self.epsilon_closure({self.start_state})
        
        # Process each symbol in the input
        for symbol in input_string:
            # Move with current symbol
            next_states = self.move(current_states, symbol)
            
            # If no states are reachable, reject
            if not next_states:
                return False
            
            # Calculate epsilon closure of reached states
            current_states = self.epsilon_closure(next_states)
        
        # Check if any current state is accepting
        return self.accept_state in current_states
    
    def get_reachable_states(self) -> Set[int]:
        """
        Get all states reachable from the start state.
        
        Returns:
            Set of reachable states
        """
        return self.epsilon_closure({self.start_state})
    
    def is_valid(self) -> bool:
        """
        Check if the NFA is valid.
        
        Returns:
            True if the NFA is valid, False otherwise
        """
        return (self.start_state is not None and 
                self.accept_state is not None and
                self.transitions is not None)


def nfa_to_dfa(nfa: NFASimulator) -> DFA:
    """
    Convert NFA to DFA using subset construction algorithm.
    
    Args:
        nfa: NFA simulator to convert
        
    Returns:
        Equivalent DFA
        
    Raises:
        RegexError: If the NFA is invalid
    """
    if not nfa.is_valid():
        raise RegexError("Invalid NFA for conversion")
    
    alphabet = tuple(nfa.get_alphabet())
    
    # Initial state: epsilon closure of NFA start state
    initial_states = frozenset(nfa.epsilon_closure({nfa.start_state}))
    
    # Work with sets of NFA states
    work_queue = [initial_states]
    processed_states = {initial_states}
    state_mapping = {initial_states: 'S0'}
    transitions = {}
    accept_states = set()
    
    def get_state_name(state_set: frozenset) -> str:
        """Get or create a name for a state set."""
        if state_set not in state_mapping:
            state_name = f'S{len(state_mapping)}'
            state_mapping[state_set] = state_name
            work_queue.append(state_set)
            processed_states.add(state_set)
        return state_mapping[state_set]
    
    # Process all states
    while work_queue:
        current_states = work_queue.pop(0)
        current_name = state_mapping[current_states]
        
        # Check if it's an accepting state
        if nfa.accept_state in current_states:
            accept_states.add(current_name)
        
        # Initialize transitions for this state
        transitions[current_name] = {}
        
        # Calculate transitions for each alphabet symbol
        for symbol in alphabet:
            # Move with symbol and calculate epsilon closure
            next_states = frozenset(nfa.epsilon_closure(nfa.move(current_states, symbol)))
            next_name = get_state_name(next_states)
            transitions[current_name][symbol] = next_name
    
    # Create DFA
    all_states = tuple(state_mapping[state_set] for state_set in processed_states)
    start_state = state_mapping[initial_states]
    accept_states_tuple = tuple(sorted(accept_states))
    
    return DFA(
        name="subset_dfa",
        alphabet=alphabet,
        states=all_states,
        start_state=start_state,
        accept_states=accept_states_tuple,
        transitions=transitions
    )


def ensure_total_dfa(dfa: DFA) -> DFA:
    """
    Ensure DFA is total by adding sink state for undefined transitions.
    
    Args:
        dfa: DFA to make total
        
    Returns:
        Total DFA equivalent
    """
    if dfa.is_total():
        return dfa
    
    sink_state = "__sink__"
    new_transitions = {state: dict(dfa.transitions[state]) for state in dfa.states}
    
    # Add missing transitions to sink state
    for state in dfa.states:
        for symbol in dfa.alphabet:
            if symbol not in new_transitions[state]:
                new_transitions[state][symbol] = sink_state
    
    # Add sink state transitions
    new_transitions[sink_state] = {symbol: sink_state for symbol in dfa.alphabet}
    
    # Create new states tuple
    new_states = dfa.states + (sink_state,)
    
    return DFA(
        name=dfa.name + "_total",
        alphabet=dfa.alphabet,
        states=new_states,
        start_state=dfa.start_state,
        accept_states=dfa.accept_states,
        transitions=new_transitions
    )

