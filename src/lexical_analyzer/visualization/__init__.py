"""
SVG visualization for finite automata.

This module provides professional SVG generation for NFAs and DFAs
with clear, readable visualizations suitable for academic and industrial use.
"""

import os
import math
from typing import Dict, List, Tuple, Optional

from ..core import Fragment, DFA


def svg_escape(text: str) -> str:
    """
    Escape special characters for SVG output.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text safe for SVG
    """
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))


def draw_nfa_svg(fragment: Fragment, path: str, ascii_eps: bool = False) -> None:
    """
    Generate SVG visualization of an NFA fragment.
    
    Args:
        fragment: NFA fragment to visualize
        path: Output file path
        ascii_eps: Use 'eps' instead of 'ε' in SVG
    """
    # Calculate layout
    n_states = len(set().union(*[
        {fragment.start.id, fragment.accept.id},
        *[set(trans.keys()) for trans in fragment.transitions.values()],
        *[set(next_state for _, next_state in trans) 
          for trans in fragment.transitions.values()]
    ]))
    
    num_cols = math.ceil(math.sqrt(n_states))
    cell_width = 120
    cell_height = 100
    radius = 20
    
    # Calculate positions
    positions = {}
    for i in range(n_states):
        row = i // num_cols
        col = i % num_cols
        x = 50 + col * cell_width
        y = 50 + row * cell_height
        positions[i] = (x, y)
    
    # Build SVG
    svg_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">',
        '<defs>',
        '  <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '    <polygon points="0 0, 10 3.5, 0 7" fill="black" />',
        '  </marker>',
        '</defs>',
        '<style>',
        '  .state { fill: white; stroke: black; stroke-width: 2; }',
        '  .accept { fill: lightgreen; stroke: black; stroke-width: 2; }',
        '  .start { fill: lightblue; stroke: black; stroke-width: 2; }',
        '  .text { font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; }',
        '  .transition { font-family: Arial, sans-serif; font-size: 10px; }',
        '</style>'
    ]
    
    # Add transitions
    for from_state, transitions in fragment.transitions.items():
        for symbol, to_state in transitions:
            x1, y1 = positions[from_state]
            x2, y2 = positions[to_state]
            
            # Calculate arrow position
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Normalize
                dx /= length
                dy /= length
                
                # Start and end points (on circle edges)
                start_x = x1 + dx * radius
                start_y = y1 + dy * radius
                end_x = x2 - dx * radius
                end_y = y2 - dy * radius
                
                # Label position
                label_x = (start_x + end_x) / 2
                label_y = (start_y + end_y) / 2 - 5
                
                # Draw arrow
                svg_parts.append(f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" '
                               f'stroke="black" stroke-width="2" marker-end="url(#arrowhead)" />')
                
                # Add label
                symbol_text = "eps" if ascii_eps and symbol is None else (symbol or "ε")
                svg_parts.append(f'<text x="{label_x}" y="{label_y}" class="transition" '
                               f'text-anchor="middle">{svg_escape(symbol_text)}</text>')
    
    # Add states
    for state_id, (x, y) in positions.items():
        if state_id == fragment.start.id:
            css_class = "start"
        elif state_id == fragment.accept.id:
            css_class = "accept"
        else:
            css_class = "state"
        
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" class="{css_class}" />')
        svg_parts.append(f'<text x="{x}" y="{y+4}" class="text">{state_id}</text>')
    
    # Add start arrow
    start_x, start_y = positions[fragment.start.id]
    svg_parts.append(f'<line x1="{start_x-radius-20}" y1="{start_y}" '
                    f'x2="{start_x-radius}" y2="{start_y}" stroke="black" stroke-width="2" '
                    f'marker-end="url(#arrowhead)" />')
    
    svg_parts.append('</svg>')
    
    # Write to file
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))


def draw_dfa_svg(dfa: DFA, path: str) -> None:
    """
    Generate SVG visualization of a DFA.
    
    Args:
        dfa: DFA to visualize
        path: Output file path
    """
    n_states = len(dfa.states)
    num_cols = math.ceil(math.sqrt(n_states))
    cell_width = 120
    cell_height = 100
    radius = 20
    
    # Calculate positions
    positions = {}
    for i, state in enumerate(dfa.states):
        row = i // num_cols
        col = i % num_cols
        x = 50 + col * cell_width
        y = 50 + row * cell_height
        positions[state] = (x, y)
    
    # Build SVG
    svg_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">',
        '<defs>',
        '  <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '    <polygon points="0 0, 10 3.5, 0 7" fill="black" />',
        '  </marker>',
        '</defs>',
        '<style>',
        '  .state { fill: white; stroke: black; stroke-width: 2; }',
        '  .accept { fill: lightgreen; stroke: black; stroke-width: 2; }',
        '  .start { fill: lightblue; stroke: black; stroke-width: 2; }',
        '  .text { font-family: Arial, sans-serif; font-size: 12px; text-anchor: middle; font-weight: bold; }',
        '  .transition { font-family: Arial, sans-serif; font-size: 10px; }',
        '</style>'
    ]
    
    # Add transitions
    for from_state, transitions in dfa.transitions.items():
        for symbol, to_state in transitions.items():
            x1, y1 = positions[from_state]
            x2, y2 = positions[to_state]
            
            # Calculate arrow position
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Normalize
                dx /= length
                dy /= length
                
                # Start and end points (on circle edges)
                start_x = x1 + dx * radius
                start_y = y1 + dy * radius
                end_x = x2 - dx * radius
                end_y = y2 - dy * radius
                
                # Label position
                label_x = (start_x + end_x) / 2
                label_y = (start_y + end_y) / 2 - 5
                
                # Draw arrow
                svg_parts.append(f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" '
                               f'stroke="black" stroke-width="2" marker-end="url(#arrowhead)" />')
                
                # Add label
                svg_parts.append(f'<text x="{label_x}" y="{label_y}" class="transition" '
                               f'text-anchor="middle">{svg_escape(symbol)}</text>')
    
    # Add states
    for state, (x, y) in positions.items():
        if state == dfa.start_state:
            css_class = "start"
        elif state in dfa.accept_states:
            css_class = "accept"
        else:
            css_class = "state"
        
        svg_parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" class="{css_class}" />')
        svg_parts.append(f'<text x="{x}" y="{y+4}" class="text">{svg_escape(state)}</text>')
    
    # Add start arrow
    start_x, start_y = positions[dfa.start_state]
    svg_parts.append(f'<line x1="{start_x-radius-20}" y1="{start_y}" '
                    f'x2="{start_x-radius}" y2="{start_y}" stroke="black" stroke-width="2" '
                    f'marker-end="url(#arrowhead)" />')
    
    svg_parts.append('</svg>')
    
    # Write to file
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

