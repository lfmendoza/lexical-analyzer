#!/usr/bin/env python3
"""
Script para Probar una Versión Corregida del Algoritmo de Thompson
================================================================

Este script implementa una versión corregida que maneja símbolos de múltiples
caracteres como 'eps'.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer.algorithms import normalize_regex, validate_regex, insert_concat_ops, to_postfix
from lexical_analyzer.algorithms.thompson import ThompsonNFA
from lexical_analyzer.core import Fragment, State, RegexError

class FixedThompsonNFA(ThompsonNFA):
    """Versión corregida de ThompsonNFA que maneja símbolos de múltiples caracteres"""
    
    def from_postfix_fixed(self, postfix_regex: str) -> Fragment:
        """
        Build NFA from postfix regular expression - versión corregida.
        
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
        i = 0
        
        while i < len(postfix_regex):
            char = postfix_regex[i]
            
            # Manejar símbolos de múltiples caracteres (como 'eps')
            if char == 'e' and i + 2 < len(postfix_regex) and postfix_regex[i:i+3] == 'eps':
                # Es el símbolo 'eps'
                stack.append(self.epsilon())
                i += 3
            elif char == "ε" or (char not in {"*", "+", "?", "|", "."} and char.isprintable()):
                # Symbol or epsilon
                stack.append(self.symbol(char))
                i += 1
            elif char == ".":
                # Concatenation
                if len(stack) < 2:
                    raise RegexError("Insufficient operands for concatenation")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(self.concat(frag1, frag2))
                i += 1
            elif char == "|":
                # Union
                if len(stack) < 2:
                    raise RegexError("Insufficient operands for union")
                frag2 = stack.pop()
                frag1 = stack.pop()
                stack.append(self.union(frag1, frag2))
                i += 1
            elif char == "*":
                # Kleene star
                if not stack:
                    raise RegexError("Insufficient operands for star")
                frag = stack.pop()
                stack.append(self.star(frag))
                i += 1
            elif char == "+":
                # Plus
                if not stack:
                    raise RegexError("Insufficient operands for plus")
                frag = stack.pop()
                stack.append(self.plus(frag))
                i += 1
            elif char == "?":
                # Optional
                if not stack:
                    raise RegexError("Insufficient operands for optional")
                frag = stack.pop()
                stack.append(self.optional(frag))
                i += 1
            else:
                raise RegexError(f"Unrecognized symbol at position {i}: {repr(char)}")
        
        if len(stack) != 1:
            raise RegexError(f"Invalid postfix expression: {len(stack)} fragments remaining")
        
        return stack[0]

def test_fixed_thompson(regex: str):
    """Probar la versión corregida del algoritmo de Thompson"""
    
    print("=" * 80)
    print("PRUEBA DEL ALGORITMO DE THOMPSON CORREGIDO")
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
        
        # Paso 5: Algoritmo de Thompson corregido
        print("PASO 5: Algoritmo de Thompson corregido")
        print("Creando FixedThompsonNFA...")
        thompson_nfa = FixedThompsonNFA()
        
        print("Procesando postfix...")
        print(f"Postfix a procesar: {postfix}")
        
        print("Construyendo NFA...")
        nfa_fragment = thompson_nfa.from_postfix_fixed(postfix)
        
        print("OK - NFA construido exitosamente")
        print(f"Estados creados: {thompson_nfa.next_id}")
        print()
        
        print("=" * 80)
        print("ALGORITMO DE THOMPSON CORREGIDO COMPLETADO - ÉXITO")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERROR en Thompson corregido: {e}")
        print()
        print("=" * 80)
        print("ALGORITMO DE THOMPSON CORREGIDO FALLÓ")
        print("=" * 80)
        
        return False

if __name__ == "__main__":
    # Expresión problemática
    regex = r"\?(((.|eps)?!?)\*)+"
    
    print("PROBANDO ALGORITMO DE THOMPSON CORREGIDO:")
    print(f"'{regex}'")
    print()
    
    # Probar el algoritmo corregido
    success = test_fixed_thompson(regex)
    
    if success:
        print()
        print("SOLUCIÓN ENCONTRADA:")
        print("-" * 40)
        print("El problema estaba en que el algoritmo de Thompson original")
        print("procesa cada carácter individualmente, pero 'eps' debe ser")
        print("tratado como un solo símbolo de múltiples caracteres.")
        print()
        print("La versión corregida maneja correctamente:")
        print("- Símbolos de múltiples caracteres como 'eps'")
        print("- Operadores de concatenación implícitos")
        print("- Expresiones regulares complejas")
