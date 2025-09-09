#!/usr/bin/env python3
"""
Script para Probar Expresiones Regulares Complejas
=================================================

Este script está diseñado para probar expresiones regulares más complejas
que incluyen caracteres especiales como ?, !, etc.

Uso:
1. Modifica las variables REGEX y TEST_WORDS al inicio del archivo
2. Ejecuta: python test_complex_regex.py
3. Revisa los resultados y archivos generados
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer import LexicalAnalyzer

# =============================================================================
# CONFIGURACIÓN - MODIFICA AQUÍ TUS PRUEBAS
# =============================================================================

# Expresión regular a probar (usar caracteres simples para evitar problemas)
REGEX = r"(a|b)*abb"

# Lista de palabras a probar (usar caracteres ASCII simples)
TEST_WORDS = [
    "aaaaaaaaaaaaaaaaaaaaaaaaabb",    # Debe ser aceptada
    "aaaaaaaaaaaaaaaaaaaaaaaaabab",   # No debe ser aceptada
    "abb",                            # Debe ser aceptada
    "aabb",                           # Debe ser aceptada
    "babb",                           # Debe ser aceptada
    "abab",                           # No debe ser aceptada
    "ab",                             # No debe ser aceptada
    "a",                              # No debe ser aceptada
    "b",                              # No debe ser aceptada
    "",                               # No debe ser aceptada
]

# Directorio base para los resultados
OUTPUT_BASE_DIR = "./complex_test_results"

# =============================================================================
# NO MODIFIQUES NADA DESDE AQUÍ HACIA ABAJO
# =============================================================================

def run_tests():
    """Ejecutar todas las pruebas configuradas"""
    
    print("=" * 80)
    print("LEXICAL ANALYZER - PRUEBAS DE EXPRESIONES COMPLEJAS")
    print("=" * 80)
    print(f"Expresión regular: {REGEX}")
    print(f"Palabras a probar: {len(TEST_WORDS)}")
    print(f"Directorio de salida: {OUTPUT_BASE_DIR}")
    print()
    
    # Crear el analizador
    analyzer = LexicalAnalyzer(eps_symbol="eps")
    
    # Contadores para estadísticas
    total_tests = len(TEST_WORDS)
    accepted_count = 0
    rejected_count = 0
    error_count = 0
    
    # Crear directorio base si no existe
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    
    # Ejecutar cada prueba
    for i, word in enumerate(TEST_WORDS, 1):
        print(f"Prueba {i:2d}/{total_tests}: '{word}'")
        print(f"  Longitud: {len(word)} caracteres")
        
        try:
            # Procesar la expresión
            result = analyzer.process_regex(
                regex_raw=REGEX,
                test_word=word,
                output_dir=os.path.join(OUTPUT_BASE_DIR, f"test_{i:02d}")
            )
            
            # Mostrar resultados
            accepts = result.dfa_min_accepts
            status = "ACEPTADA" if accepts else "RECHAZADA"
            emoji = "OK" if accepts else "X"
            
            print(f"  Resultado: {emoji} {status}")
            print(f"    - Postfix: {result.postfix}")
            print(f"    - Estados: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
            print(f"    - Acepta: NFA={result.nfa_accepts}, DFA={result.dfa_accepts}, Min={result.dfa_min_accepts}")
            print(f"    - Archivos: {os.path.join(OUTPUT_BASE_DIR, f'test_{i:02d}')}/")
            
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
    
    # Análisis de la expresión regular
    print("ANÁLISIS DE LA EXPRESIÓN REGULAR:")
    print(f"'{REGEX}' significa:")
    
    if "*" in REGEX:
        print("- El símbolo '*' indica cero o más repeticiones")
    if "|" in REGEX:
        print("- El símbolo '|' indica alternancia (OR)")
    if "(" in REGEX and ")" in REGEX:
        print("- Los paréntesis agrupan operaciones")
    if "+" in REGEX:
        print("- El símbolo '+' indica una o más repeticiones")
    if "?" in REGEX:
        print("- El símbolo '?' indica cero o una repetición")
    
    print()
    print("ARCHIVOS GENERADOS:")
    print(f"- Directorio base: {OUTPUT_BASE_DIR}/")
    print("- Cada prueba tiene su propio subdirectorio con:")
    print("  * nfa.svg: Autómata finito no determinístico")
    print("  * dfa.svg: Autómata finito determinístico")
    print("  * dfa_min.svg: AFD minimizado")
    print("  * regex.txt: Información detallada del procesamiento")
    
    print()
    print("=" * 80)
    print("PRUEBAS COMPLETADAS")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
