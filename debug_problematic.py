#!/usr/bin/env python3
"""
Script de Debug para la Expresión Problemática
==============================================

Este script hace debug paso a paso para identificar exactamente dónde falla.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer.algorithms import normalize_regex, validate_regex, insert_concat_ops, to_postfix
from lexical_analyzer.algorithms.thompson import ThompsonNFA

def debug_regex_processing(regex: str):
    """Debug paso a paso del procesamiento de regex"""
    
    print("=" * 80)
    print("DEBUG PASO A PASO")
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
        
        # Paso 3: Inserción de concatenación
        print("PASO 3: Inserción de concatenación")
        with_concat = insert_concat_ops(normalized)
        print(f"Con concatenación: {with_concat}")
        print()
        
        # Paso 4: Conversión a postfix
        print("PASO 4: Conversión a postfix")
        postfix = to_postfix(with_concat)
        print(f"Postfix: {postfix}")
        print()
        
        # Paso 5: Debug del algoritmo de Thompson
        print("PASO 5: Debug del algoritmo de Thompson")
        print("Creando ThompsonNFA...")
        thompson_nfa = ThompsonNFA()
        
        print("Procesando postfix carácter por carácter...")
        print(f"Postfix: {postfix}")
        
        # Simular el procesamiento paso a paso
        stack = []
        i = 0
        
        while i < len(postfix):
            char = postfix[i]
            print(f"  Posición {i}: '{char}'")
            
            # Handle multi-character symbols (like 'eps')
            if char == 'e' and i + 2 < len(postfix) and postfix[i:i+3] == 'eps':
                print(f"    -> Detectado símbolo 'eps' completo")
                stack.append("eps_fragment")
                i += 3
            elif char == "ε" or (char not in {"*", "+", "?", "|", "."} and char.isprintable()):
                print(f"    -> Símbolo normal: '{char}'")
                stack.append(f"symbol_{char}")
                i += 1
            elif char == ".":
                print(f"    -> Operador concatenación")
                if len(stack) < 2:
                    print(f"    -> ERROR: Solo {len(stack)} operandos en la pila")
                    print(f"    -> Pila actual: {stack}")
                    raise Exception("Insufficient operands for concatenation")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(f"concat({frag1}, {frag2})")
                i += 1
            elif char == "|":
                print(f"    -> Operador unión")
                if len(stack) < 2:
                    print(f"    -> ERROR: Solo {len(stack)} operandos en la pila")
                    raise Exception("Insufficient operands for union")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(f"union({frag1}, {frag2})")
                i += 1
            elif char == "*":
                print(f"    -> Operador estrella")
                if not stack:
                    print(f"    -> ERROR: Pila vacía")
                    raise Exception("Insufficient operands for star")
                frag = stack.pop()
                stack.append(f"star({frag})")
                i += 1
            elif char == "+":
                print(f"    -> Operador plus")
                if not stack:
                    print(f"    -> ERROR: Pila vacía")
                    raise Exception("Insufficient operands for plus")
                frag = stack.pop()
                stack.append(f"plus({frag})")
                i += 1
            elif char == "?":
                print(f"    -> Operador opcional")
                if not stack:
                    print(f"    -> ERROR: Pila vacía")
                    raise Exception("Insufficient operands for optional")
                frag = stack.pop()
                stack.append(f"optional({frag})")
                i += 1
            else:
                print(f"    -> ERROR: Carácter no reconocido: '{char}'")
                raise Exception(f"Unrecognized symbol at position {i}: {repr(char)}")
            
            print(f"    -> Pila después: {stack}")
            print()
        
        print("=" * 80)
        print("DEBUG COMPLETADO - ÉXITO")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        print()
        print("=" * 80)
        print("DEBUG COMPLETADO - FALLO")
        print("=" * 80)
        
        return False

if __name__ == "__main__":
    # Expresión problemática
    regex = r"\?(((.|eps)?!?)\*)+"
    
    print("DEBUG DE EXPRESIÓN PROBLEMÁTICA:")
    print(f"'{regex}'")
    print()
    
    # Debug paso a paso
    success = debug_regex_processing(regex)
    
    if not success:
        print()
        print("ANÁLISIS DEL PROBLEMA:")
        print("-" * 40)
        print("El debug muestra exactamente dónde y por qué falla el procesamiento.")
        print("Revisa los pasos anteriores para identificar el problema específico.")
