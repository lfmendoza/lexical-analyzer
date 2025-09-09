#!/usr/bin/env python3
"""
Script para Probar el Algoritmo de Thompson Paso a Paso
======================================================

Este script prueba el algoritmo de Thompson con la expresión problemática
para identificar exactamente dónde falla.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer.algorithms import normalize_regex, validate_regex, insert_concat_ops, to_postfix
from lexical_analyzer.algorithms.thompson import ThompsonNFA

def test_thompson_step_by_step(regex: str):
    """Probar el algoritmo de Thompson paso a paso"""
    
    print("=" * 80)
    print("PRUEBA DEL ALGORITMO DE THOMPSON")
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
        
        # Paso 5: Algoritmo de Thompson
        print("PASO 5: Algoritmo de Thompson")
        print("Creando ThompsonNFA...")
        thompson_nfa = ThompsonNFA()
        
        print("Procesando postfix...")
        print(f"Postfix a procesar: {postfix}")
        
        # Procesar cada carácter del postfix
        for i, char in enumerate(postfix):
            print(f"  Carácter {i+1}: '{char}'")
        
        print("Construyendo NFA...")
        nfa_fragment = thompson_nfa.from_postfix(postfix)
        
        print("OK - NFA construido exitosamente")
        print(f"Estados creados: {thompson_nfa.next_id}")
        print()
        
        print("=" * 80)
        print("ALGORITMO DE THOMPSON COMPLETADO - ÉXITO")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERROR en Thompson: {e}")
        print()
        print("=" * 80)
        print("ALGORITMO DE THOMPSON FALLÓ")
        print("=" * 80)
        
        return False

if __name__ == "__main__":
    # Expresión problemática
    regex = r"\?(((.|eps)?!?)\*)+"
    
    print("PROBANDO ALGORITMO DE THOMPSON:")
    print(f"'{regex}'")
    print()
    
    # Probar el algoritmo
    success = test_thompson_step_by_step(regex)
    
    if not success:
        print()
        print("ANÁLISIS DEL ERROR:")
        print("-" * 40)
        print("El error 'Insufficient operands for concatenation' indica que")
        print("hay operadores de concatenación (.) en el postfix que no tienen")
        print("suficientes operandos en la pila del algoritmo de Thompson.")
        print()
        print("POSIBLES CAUSAS:")
        print("1. La expresión postfix tiene operadores mal posicionados")
        print("2. Hay operadores de concatenación implícitos mal insertados")
        print("3. La precedencia de operadores no está bien calculada")
        print()
        print("SOLUCIONES SUGERIDAS:")
        print("1. Revisar la inserción de concatenación implícita")
        print("2. Verificar la conversión a postfix")
        print("3. Simplificar la expresión regular")
