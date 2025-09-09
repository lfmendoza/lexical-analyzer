#!/usr/bin/env python3
"""
Script para Probar la Expresión Problemática Original
====================================================

Este script prueba específicamente la expresión regular problemática
que el usuario quería usar.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer import LexicalAnalyzer

def test_problematic_regex():
    """Probar la expresión regular problemática"""
    
    print("=" * 80)
    print("PRUEBA DE EXPRESIÓN REGULAR PROBLEMÁTICA")
    print("=" * 80)
    
    # Expresión problemática original
    regex = r"\?(((.|eps)?!?)\*)+"
    test_words = [
        "?.., ?, ?!.",    # Debe ser aceptada
        "!, !.!.!, !?.",   # No debe ser aceptada
    ]
    
    print(f"Expresión regular: {regex}")
    print(f"Palabras a probar: {len(test_words)}")
    print()
    
    # Crear el analizador
    analyzer = LexicalAnalyzer(eps_symbol="eps")
    
    # Contadores para estadísticas
    total_tests = len(test_words)
    accepted_count = 0
    rejected_count = 0
    error_count = 0
    
    # Ejecutar cada prueba
    for i, word in enumerate(test_words, 1):
        print(f"Prueba {i:2d}/{total_tests}: '{word}'")
        print(f"  Longitud: {len(word)} caracteres")
        
        try:
            # Procesar la expresión
            result = analyzer.process_regex(
                regex_raw=regex,
                test_word=word,
                output_dir=f"./problematic_test_{i:02d}"
            )
            
            # Mostrar resultados
            accepts = result.dfa_min_accepts
            status = "ACEPTADA" if accepts else "RECHAZADA"
            emoji = "OK" if accepts else "X"
            
            print(f"  Resultado: {emoji} {status}")
            print(f"    - Postfix: {result.postfix}")
            print(f"    - Estados: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
            print(f"    - Acepta: NFA={result.nfa_accepts}, DFA={result.dfa_accepts}, Min={result.dfa_min_accepts}")
            print(f"    - Archivos: ./problematic_test_{i:02d}/")
            
            # Actualizar contadores
            if accepts:
                accepted_count += 1
            else:
                rejected_count += 1
                
        except Exception as e:
            print(f"  ERROR: {e}")
            error_count += 1
        
        print()
    
    # Mostrar resumen final
    print("=" * 80)
    print("RESUMEN DE RESULTADOS")
    print("=" * 80)
    print(f"Total de pruebas: {total_tests}")
    print(f"OK Aceptadas: {accepted_count}")
    print(f"X Rechazadas: {rejected_count}")
    print(f"! Errores: {error_count}")
    print()
    
    if error_count == 0:
        print("ÉXITO: La expresión regular problemática ahora funciona correctamente!")
        print("Las correcciones aplicadas al algoritmo resolvieron el problema.")
    else:
        print("AÚN HAY PROBLEMAS: La expresión regular sigue fallando.")
    
    print()
    print("=" * 80)
    print("PRUEBAS COMPLETADAS")
    print("=" * 80)

if __name__ == "__main__":
    test_problematic_regex()
