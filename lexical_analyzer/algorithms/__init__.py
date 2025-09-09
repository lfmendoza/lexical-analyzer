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
EPS = "eps"
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
    
    # First, tokenize the regex to handle escape sequences and multi-character symbols
    tokens = []
    i = 0
    
    while i < len(regex):
        char = regex[i]
        
        # Handle escape sequences
        if char == '\\' and i + 1 < len(regex):
            # It's an escape sequence - treat the next character as literal
            next_char = regex[i + 1]
            tokens.append(f'\\{next_char}')
            i += 2
        # Handle character classes [abc]
        elif char == '[':
            # Find the closing bracket
            j = i + 1
            while j < len(regex) and regex[j] != ']':
                j += 1
            if j < len(regex):
                # Extract characters inside brackets
                chars_inside = regex[i+1:j]
                tokens.append(f'[{chars_inside}]')
                i = j + 1
            else:
                # No closing bracket found, treat as normal character
                tokens.append(char)
                i += 1
        # Handle multi-character symbols (like 'eps')
        elif char == 'e' and i + 2 < len(regex) and regex[i:i+3] == 'eps':
            # It's the 'eps' symbol - treat as single symbol
            tokens.append('eps')
            i += 3
        else:
            # Normal character
            tokens.append(char)
            i += 1
    
    # Now insert concatenation between tokens
    result = []
    
    for i, token in enumerate(tokens):
        result.append(token)
        
        # Don't add concatenation after the last token
        if i == len(tokens) - 1:
            continue
        
        next_token = tokens[i + 1]
        
        # Add concatenation between:
        # - Symbol and symbol
        # - Symbol and opening parenthesis
        # - Symbol and epsilon
        # - Closing parenthesis and symbol
        # - Closing parenthesis and opening parenthesis
        # - Closing parenthesis and epsilon
        # - Unary operator and symbol
        # - Unary operator and opening parenthesis
        # - Unary operator and epsilon
        # - Epsilon and symbol
        # - Epsilon and opening parenthesis
        # - Epsilon and epsilon
        
        # Check if token is an escaped character or character class
        is_token_escaped = token.startswith('\\')
        is_token_char_class = token.startswith('[') and token.endswith(']')
        is_next_token_escaped = next_token.startswith('\\')
        is_next_token_char_class = next_token.startswith('[') and next_token.endswith(']')
        
        # Extract the actual character for escaped tokens
        token_char = token[1:] if is_token_escaped else token
        next_token_char = next_token[1:] if is_next_token_escaped else next_token
        
        should_concat = (
            # Symbol and symbol (including escaped characters and character classes)
            ((token_char not in OPERATORS and token_char != EPS and not is_token_escaped and not is_token_char_class) and 
             (next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class)) or
            # Escaped character and symbol/character class
            (is_token_escaped and (next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class)) or
            # Symbol and escaped character/character class
            ((token_char not in OPERATORS and token_char != EPS and not is_token_escaped and not is_token_char_class) and (is_next_token_escaped or is_next_token_char_class)) or
            # Escaped character and escaped character/character class
            (is_token_escaped and (is_next_token_escaped or is_next_token_char_class)) or
            # Character class and symbol/escaped/character class
            (is_token_char_class and ((next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class) or is_next_token_escaped or is_next_token_char_class)) or
            # Symbol/escaped/character class and opening parenthesis
            (((token_char not in OPERATORS and token_char != EPS and not is_token_escaped and not is_token_char_class) or is_token_escaped or is_token_char_class) and next_token == "(") or
            # Symbol/escaped/character class and epsilon
            (((token_char not in OPERATORS and token_char != EPS and not is_token_escaped and not is_token_char_class) or is_token_escaped or is_token_char_class) and next_token == EPS) or
            # Closing parenthesis and symbol/escaped/character class
            (token == ")" and ((next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class) or is_next_token_escaped or is_next_token_char_class)) or
            # Closing parenthesis and opening parenthesis
            (token == ")" and next_token == "(") or
            # Closing parenthesis and epsilon
            (token == ")" and next_token == EPS) or
            # Unary operator and symbol/escaped/character class
            (token in UNARY_OPERATORS and ((next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class) or is_next_token_escaped or is_next_token_char_class)) or
            # Unary operator and opening parenthesis
            (token in UNARY_OPERATORS and next_token == "(") or
            # Unary operator and epsilon
            (token in UNARY_OPERATORS and next_token == EPS) or
            # Epsilon and symbol/escaped/character class
            (token == EPS and ((next_token_char not in OPERATORS and next_token_char != EPS and not is_next_token_escaped and not is_next_token_char_class) or is_next_token_escaped or is_next_token_char_class)) or
            # Epsilon and opening parenthesis
            (token == EPS and next_token == "(") or
            # Epsilon and epsilon
            (token == EPS and next_token == EPS)
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
    
    # First, tokenize the regex to handle escape sequences, character classes, and multi-character symbols
    tokens = []
    i = 0
    
    while i < len(regex):
        char = regex[i]
        
        # Handle escape sequences
        if char == '\\' and i + 1 < len(regex):
            # It's an escape sequence - treat the next character as literal
            next_char = regex[i + 1]
            tokens.append(f'\\{next_char}')
            i += 2
        # Handle character classes [abc]
        elif char == '[':
            # Find the closing bracket
            j = i + 1
            while j < len(regex) and regex[j] != ']':
                j += 1
            if j < len(regex):
                # Extract characters inside brackets
                chars_inside = regex[i+1:j]
                tokens.append(f'[{chars_inside}]')
                i = j + 1
            else:
                # No closing bracket found, treat as normal character
                tokens.append(char)
                i += 1
        # Handle multi-character symbols (like 'eps')
        elif char == 'e' and i + 2 < len(regex) and regex[i:i+3] == 'eps':
            # It's the 'eps' symbol - treat as single symbol
            tokens.append('eps')
            i += 3
        else:
            # Normal character
            tokens.append(char)
            i += 1
    
    # Now apply Shunting Yard algorithm to tokens
    output: List[str] = []
    operator_stack: List[str] = []
    
    for i, token in enumerate(tokens):
        # Check if token is an escaped character or character class
        is_token_escaped = token.startswith('\\')
        is_token_char_class = token.startswith('[') and token.endswith(']')
        
        if token == "(":
            operator_stack.append(token)
        elif token == ")":
            # Pop operators until we find the matching opening parenthesis
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            
            if not operator_stack:
                raise RegexError(f"Unbalanced parentheses at position {i}")
            
            operator_stack.pop()  # Remove the opening parenthesis
        elif token in OPERATORS:
            # Handle operator precedence and associativity
            while (operator_stack and 
                   operator_stack[-1] != "(" and
                   operator_stack[-1] in PRECEDENCE):
                
                top_op = operator_stack[-1]
                top_prec = PRECEDENCE[top_op]
                curr_prec = PRECEDENCE[token]
                
                # Check precedence and associativity
                if (top_prec > curr_prec or 
                    (top_prec == curr_prec and ASSOCIATIVITY[token] == "left")):
                    output.append(operator_stack.pop())
                else:
                    break
            
            operator_stack.append(token)
        elif is_token_escaped or is_token_char_class or token == EPS:
            # Escaped character, character class, or epsilon
            output.append(token)
        elif is_symbol(token):
            # Regular symbol
            output.append(token)
        else:
            raise RegexError(f"Unrecognized token at position {i}: {repr(token)}")
    
    # Empty the operator stack
    while operator_stack:
        op = operator_stack.pop()
        if op in ("(", ")"):
            raise RegexError("Unbalanced parentheses")
        output.append(op)
    
    return "".join(output)

