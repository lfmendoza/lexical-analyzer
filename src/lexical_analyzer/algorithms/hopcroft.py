"""
Hopcroft's algorithm for DFA minimization.

This module implements Hopcroft's algorithm for minimizing deterministic
finite automata by partitioning states into equivalence classes.
"""

from typing import List, Set, Tuple, Dict
from dataclasses import dataclass

from ..core import DFA, RegexError
from .subset_construction import ensure_total_dfa


def hopcroft_minimize(dfa: DFA) -> Tuple[DFA, List[str]]:
    """
    Minimize a DFA using Hopcroft's algorithm.
    
    Args:
        dfa: DFA to minimize
        
    Returns:
        Tuple of (minimized DFA, minimization log)
        
    Raises:
        RegexError: If the DFA is invalid
    """
    if not dfa.is_total():
        dfa = ensure_total_dfa(dfa)
    
    alphabet = set(dfa.alphabet)
    accept_states = set(dfa.accept_states)
    all_states = set(dfa.states)
    
    # Initialize partition
    if accept_states == all_states:
        # All states are accepting
        partition = [accept_states]
    else:
        non_accept_states = all_states - accept_states
        partition = [accept_states, non_accept_states] if non_accept_states else [accept_states]
    
    # Work queue
    work_queue = [block for block in partition if block]
    log = [f"Initialization: {[sorted(block) for block in partition]}"]
    
    # Precalculate predecessors for optimization
    predecessors = {symbol: {state: set() for state in all_states} for symbol in alphabet}
    
    for state in all_states:
        for symbol in alphabet:
            next_state = dfa.transitions[state][symbol]
            predecessors[symbol][next_state].add(state)
    
    # Main Hopcroft algorithm
    while work_queue:
        current_block = work_queue.pop(0)
        
        for symbol in alphabet:
            # States that reach current_block with symbol
            predecessors_with_symbol = set()
            for state in current_block:
                predecessors_with_symbol.update(predecessors[symbol][state])
            
            if not predecessors_with_symbol:
                continue
            
            # Split each block in the partition
            new_partition = []
            
            for block in partition:
                intersection = block & predecessors_with_symbol
                difference = block - predecessors_with_symbol
                
                if intersection and difference:
                    # Block can be split
                    new_partition.extend([intersection, difference])
                    
                    log.append(f"Split by '{symbol}': {sorted(block)} -> "
                              f"{sorted(intersection)} | {sorted(difference)}")
                    
                    # Update work queue
                    if block in work_queue:
                        work_queue.remove(block)
                        work_queue.extend([intersection, difference])
                    else:
                        # Add smaller block for optimization
                        smaller_block = intersection if len(intersection) <= len(difference) else difference
                        work_queue.append(smaller_block)
                else:
                    # Block cannot be split
                    new_partition.append(block)
            
            partition = new_partition
    
    # Create minimized DFA
    if not partition:
        raise RegexError("Error in minimization: empty partition")
    
    # Create mapping from original states to new states
    state_to_block = {}
    for block in partition:
        for state in block:
            state_to_block[state] = block
    
    # Create names for blocks
    block_names = {}
    for i, block in enumerate(partition):
        representative = min(block)  # Use lexicographically smallest state
        block_names[frozenset(block)] = f"B{i}"
    
    # Build transitions for minimized DFA
    new_transitions = {}
    new_states = tuple(block_names[frozenset(block)] for block in partition)
    new_start_state = block_names[frozenset(state_to_block[dfa.start_state])]
    new_accept_states = tuple(sorted(
        block_names[frozenset(state_to_block[state])] 
        for state in accept_states 
        if state in state_to_block
    ))
    
    # Create transitions
    for block in partition:
        block_name = block_names[frozenset(block)]
        representative = min(block)
        new_transitions[block_name] = {}
        
        for symbol in alphabet:
            next_state = dfa.transitions[representative][symbol]
            next_block = state_to_block[next_state]
            new_transitions[block_name][symbol] = block_names[frozenset(next_block)]
    
    # Create minimized DFA
    minimized_dfa = DFA(
        name=dfa.name + "_min",
        alphabet=dfa.alphabet,
        states=new_states,
        start_state=new_start_state,
        accept_states=new_accept_states,
        transitions=new_transitions
    )
    
    log.append(f"Minimization completed: {len(dfa.states)} -> {len(minimized_dfa.states)} states")
    
    return minimized_dfa, log

