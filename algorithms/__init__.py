"""
Regular expression processing algorithms.

This module contains implementations of core algorithms for regular expression
processing, including Shunting Yard, Thompson's construction, subset construction,
and Hopcroft's minimization algorithm.
"""

import re
from typing import List, Set, Dict, Tuple, Optional, Union
from dataclasses import dataclass

from ..core import State, Fragment, DFA, RegexError


# Constants
EPS = "ε"
OPERATORS = {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."}
UNARY_OPERATORS = {"*", "+", "?"}
BINARY_OPERATORS = {"|", "."}

PRECEDENCE = {
    "(": 0,
    ")": 0,
    "|": 1,
    ".": 2,
    "*": 3,
    "+": 3,
    "?": 3,
}

ASSOCIATIVITY = {
    "|": "left",
    ".": "left",
    "*": "right",
    "+": "right",
    "?": "right",
}


def normalize_regex(regex: str, eps_symbol: str = EPS) -> str:
    """
    Normalize a regular expression string.
    
    Args:
        regex: Raw regular expression string
        eps_symbol: Symbol to use for epsilon
        
    Returns:
        Normalized regular expression string
        
    Raises:
        RegexError: If the regex is empty or contains invalid characters
    """
    if not regex or not regex.strip():
        raise RegexError("Empty regular expression")
    
    # Remove control characters and normalize whitespace
    normalized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', regex.strip())
    
    # Standardize epsilon representations
    epsilon_patterns = [r'\bepsilon\b', r'\beps\b', r'\\e', r'\\epsilon']
    for pattern in epsilon_patterns:
        normalized = re.sub(pattern, eps_symbol, normalized, flags=re.IGNORECASE)
    
    return normalized


def is_symbol(char: str) -> bool:
    """
    Check if a character is a valid symbol (not an operator or epsilon).
    
    Args:
        char: Character to check
        
    Returns:
        True if the character is a valid symbol, False otherwise
    """
    return char not in OPERATORS and char != EPS


def validate_regex(regex: str) -> None:
    """
    Validate basic structure of a regular expression.
    
    Args:
        regex: Regular expression to validate
        
    Raises:
        RegexError: If the regex has structural issues
    """
    # Check balanced parentheses
    paren_count = 0
    bracket_count = 0
    
    for char in regex:
        if char == "(":
            paren_count += 1
        elif char == ")":
            paren_count -= 1
            if paren_count < 0:
                raise RegexError("Unbalanced parentheses")
        elif char == "[":
            bracket_count += 1
        elif char == "]":
            bracket_count -= 1
            if bracket_count < 0:
                raise RegexError("Unbalanced square brackets")
    
    if paren_count != 0:
        raise RegexError("Unbalanced parentheses")
    if bracket_count != 0:
        raise RegexError("Unbalanced square brackets")
    
    # Check unary operators
    for i, char in enumerate(regex):
        if char in UNARY_OPERATORS:
            if i == 0:
                raise RegexError(f"Unary operator '{char}' at beginning of expression")
            prev_char = regex[i-1]
            if prev_char in BINARY_OPERATORS or prev_char == "(":
                raise RegexError(f"Unary operator '{char}' after '{prev_char}'")


def insert_concat_ops(regex: str) -> str:
    """
    Insert implicit concatenation operators into a regular expression.
    
    Args:
        regex: Regular expression string
        
    Returns:
        Regular expression with explicit concatenation operators
    """
    if not regex:
        return regex
    
    result = []
    
    for i, char in enumerate(regex):
        result.append(char)
        
        # Don't add concatenation after the last character
        if i == len(regex) - 1:
            continue
        
        next_char = regex[i + 1]
        
        # Add concatenation between:
        # - Symbol and symbol
        # - Symbol and opening parenthesis
        # - Closing parenthesis and symbol
        # - Closing parenthesis and opening parenthesis
        # - Unary operator and symbol
        # - Unary operator and opening parenthesis
        # - Epsilon and symbol
        # - Epsilon and opening parenthesis
        
        should_concat = (
            (is_symbol(char) and (is_symbol(next_char) or next_char == "(")) or
            (char == ")" and (is_symbol(next_char) or next_char == "(")) or
            (char in UNARY_OPERATORS and (is_symbol(next_char) or next_char == "(")) or
            (char == EPS and (is_symbol(next_char) or next_char == "("))
        )
        
        if should_concat:
            result.append(".")
    
    return "".join(result)


def to_postfix(regex: str) -> str:
    """
    Convert infix regular expression to postfix notation using Shunting Yard algorithm.
    
    Args:
        regex: Infix regular expression
        
    Returns:
        Postfix regular expression
        
    Raises:
        RegexError: If the regex contains invalid characters or unbalanced parentheses
    """
    if not regex:
        raise RegexError("Empty regular expression")
    
    output: List[str] = []
    operator_stack: List[str] = []
    
    for i, char in enumerate(regex):
        if char == "(":
            operator_stack.append(char)
        elif char == ")":
            # Pop operators until we find the matching opening parenthesis
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            
            if not operator_stack:
                raise RegexError(f"Unbalanced parentheses at position {i}")
            
            operator_stack.pop()  # Remove the opening parenthesis
        elif char in OPERATORS:
            # Handle operator precedence and associativity
            while (operator_stack and 
                   operator_stack[-1] != "(" and
                   operator_stack[-1] in PRECEDENCE):
                
                top_op = operator_stack[-1]
                top_prec = PRECEDENCE[top_op]
                curr_prec = PRECEDENCE[char]
                
                # Check precedence and associativity
                if (top_prec > curr_prec or 
                    (top_prec == curr_prec and ASSOCIATIVITY[char] == "left")):
                    output.append(operator_stack.pop())
                else:
                    break
            
            operator_stack.append(char)
        elif is_symbol(char) or char == EPS:
            output.append(char)
        else:
            raise RegexError(f"Unrecognized symbol at position {i}: {repr(char)}")
    
    # Empty the operator stack
    while operator_stack:
        op = operator_stack.pop()
        if op in ("(", ")"):
            raise RegexError("Unbalanced parentheses")
        output.append(op)
    
    return "".join(output)

