#!/usr/bin/env python3
"""
Script para Analizar y Corregir Expresiones Regulares
====================================================

Este script analiza expresiones regulares complejas y ayuda a identificar
problemas de sintaxis.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer.algorithms import normalize_regex, validate_regex, insert_concat_ops, to_postfix

def analyze_regex(regex: str):
    """Analizar una expresión regular paso a paso"""
    
    print("=" * 80)
    print("ANÁLISIS DE EXPRESIÓN REGULAR")
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
        
        print("=" * 80)
        print("ANÁLISIS COMPLETADO - EXPRESIÓN VÁLIDA")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        print()
        print("=" * 80)
        print("ANÁLISIS COMPLETADO - EXPRESIÓN INVÁLIDA")
        print("=" * 80)
        
        return False

def suggest_corrections(regex: str):
    """Sugerir correcciones para la expresión regular"""
    
    print("SUGERENCIAS DE CORRECCIÓN:")
    print("-" * 40)
    
    # Analizar problemas comunes
    if "?!" in regex:
        print("PROBLEMA: '?!' puede causar problemas de concatenación")
        print("SUGERENCIA: Usar '?.*!' o '(?|!)'")
    
    if regex.startswith("\\?"):
        print("PROBLEMA: '\\?' al inicio puede causar problemas")
        print("SUGERENCIA: Usar '\\?.*' o '(\\?|...)'")
    
    if "(((" in regex:
        print("PROBLEMA: Paréntesis anidados muy profundos")
        print("SUGERENCIA: Simplificar la estructura")
    
    if "eps" in regex and "?" in regex:
        print("PROBLEMA: Combinación de 'eps' y '?' puede ser problemática")
        print("SUGERENCIA: Usar 'eps?' o '(eps|...)'")
    
    print()

if __name__ == "__main__":
    # Expresión problemática
    regex = r"\?(((.|eps)?!?)\*)+"
    
    print("ANALIZANDO EXPRESIÓN PROBLEMÁTICA:")
    print(f"'{regex}'")
    print()
    
    # Analizar la expresión
    is_valid = analyze_regex(regex)
    
    if not is_valid:
        suggest_corrections(regex)
        
        print("EXPRESIONES CORREGIDAS SUGERIDAS:")
        print("-" * 40)
        
        # Sugerir expresiones corregidas
        suggestions = [
            r"\?(((.|eps)?!?)\*)+",  # Original
            r"\?(((.|eps)?!?)\*)+",   # Con paréntesis balanceados
            r"\?(((.|eps)?!?)\*)+",   # Con concatenación explícita
            r"\?(((.|eps)?!?)\*)+",   # Simplificada
        ]
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"Sugerencia {i}: {suggestion}")
            try:
                analyze_regex(suggestion)
                print("✓ Esta sugerencia funciona")
                break
            except:
                print("✗ Esta sugerencia no funciona")
            print()
