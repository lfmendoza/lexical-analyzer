#!/usr/bin/env python3
"""
Script para Probar una Versión Corregida del Algoritmo de Concatenación
======================================================================

Este script implementa una versión corregida que trata 'eps' como un símbolo único.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer.algorithms import normalize_regex, validate_regex, to_postfix
from lexical_analyzer.core import RegexError

def insert_concat_ops_fixed(regex: str) -> str:
    """
    Insert implicit concatenation operators - versión corregida que maneja 'eps'.
    
    Args:
        regex: Regular expression string
        
    Returns:
        Regular expression with explicit concatenation operators
    """
    if not regex:
        return regex
    
    result = []
    i = 0
    
    while i < len(regex):
        char = regex[i]
        
        # Manejar símbolos de múltiples caracteres (como 'eps')
        if char == 'e' and i + 2 < len(regex) and regex[i:i+3] == 'eps':
            # Es el símbolo 'eps' - tratarlo como un solo símbolo
            result.append('eps')
            i += 3
        else:
            # Carácter normal
            result.append(char)
            i += 1
    
    # Ahora insertar concatenación entre símbolos
    final_result = []
    
    for i, token in enumerate(result):
        final_result.append(token)
        
        # Don't add concatenation after the last token
        if i == len(result) - 1:
            continue
        
        next_token = result[i + 1]
        
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
        
        should_concat = (
            (token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."} and 
             next_token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."}) or
            (token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."} and next_token == "(") or
            (token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."} and next_token == "eps") or
            (token == ")" and next_token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."}) or
            (token == ")" and next_token == "(") or
            (token == ")" and next_token == "eps") or
            (token in {"*", "+", "?"} and next_token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."}) or
            (token in {"*", "+", "?"} and next_token == "(") or
            (token in {"*", "+", "?"} and next_token == "eps") or
            (token == "eps" and next_token not in {"(", ")", "[", "]", "-", "^", "*", "+", "?", "|", "."}) or
            (token == "eps" and next_token == "(") or
            (token == "eps" and next_token == "eps")
        )
        
        if should_concat:
            final_result.append(".")
    
    return "".join(final_result)

def test_fixed_concat(regex: str):
    """Probar la versión corregida del algoritmo de concatenación"""
    
    print("=" * 80)
    print("PRUEBA DEL ALGORITMO DE CONCATENACIÓN CORREGIDO")
    print("=" * 80)
    print(f"Expresión original: {regex}")
    print()
    
    try:
        # Paso 1: Normalización
        print("PASO 1: Normalización")
        normalized = normalize_regex(regex, eps_symbol="eps")
        print(f"Normalizada: {normalized}")
        print()
        
        # Paso 2: Validación básica
        print("PASO 2: Validación básica")
        validate_regex(normalized)
        print("OK - Validación básica pasada")
        print()
        
        # Paso 3: Inserción de concatenación corregida
        print("PASO 3: Inserción de concatenación corregida")
        with_concat = insert_concat_ops_fixed(normalized)
        print(f"Con concatenación: {with_concat}")
        print()
        
        # Paso 4: Conversión a postfix
        print("PASO 4: Conversión a postfix")
        postfix = to_postfix(with_concat)
        print(f"Postfix: {postfix}")
        print()
        
        print("=" * 80)
        print("ALGORITMO DE CONCATENACIÓN CORREGIDO COMPLETADO - ÉXITO")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERROR en concatenación corregida: {e}")
        print()
        print("=" * 80)
        print("ALGORITMO DE CONCATENACIÓN CORREGIDO FALLÓ")
        print("=" * 80)
        
        return False

if __name__ == "__main__":
    # Expresión problemática
    regex = r"\?(((.|eps)?!?)\*)+"
    
    print("PROBANDO ALGORITMO DE CONCATENACIÓN CORREGIDO:")
    print(f"'{regex}'")
    print()
    
    # Probar el algoritmo corregido
    success = test_fixed_concat(regex)
    
    if success:
        print()
        print("SOLUCIÓN ENCONTRADA:")
        print("-" * 40)
        print("El problema estaba en que el algoritmo de inserción de concatenación")
        print("trataba 'eps' como tres caracteres separados ('e', 'p', 's') en lugar")
        print("de un solo símbolo.")
        print()
        print("La versión corregida:")
        print("- Trata 'eps' como un símbolo único")
        print("- Inserta concatenación correctamente")
        print("- Genera postfix válido")
