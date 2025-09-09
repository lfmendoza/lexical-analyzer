#!/usr/bin/env python3
"""
Script Simple para Probar una Expresión Regular
==============================================

Script súper simple para probar una expresión regular específica.
Solo modifica las variables REGEX y WORD al inicio.

Uso:
1. Cambia REGEX y WORD
2. Ejecuta: python test_simple.py
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer import LexicalAnalyzer

# =============================================================================
# CAMBIA ESTAS VARIABLES PARA TUS PRUEBAS
# =============================================================================

REGEX = "(a|b)*abb"                    # Tu expresión regular aquí
WORD = "aaaaaaaaaaaaaaaaaaaaaaaaabb"  # Tu palabra a probar aquí

# =============================================================================

def main():
    print("=" * 60)
    print("PRUEBA SIMPLE - LEXICAL ANALYZER")
    print("=" * 60)
    print(f"Expresión: {REGEX}")
    print(f"Palabra:   '{WORD}'")
    print(f"Longitud:  {len(WORD)} caracteres")
    print()
    
    try:
        # Crear analizador y procesar
        analyzer = LexicalAnalyzer(eps_symbol="eps")
        result = analyzer.process_regex(
            regex_raw=REGEX,
            test_word=WORD,
            output_dir="./simple_test_result"
        )
        
        # Mostrar resultados
        print("RESULTADOS:")
        print(f"  Postfix: {result.postfix}")
        print(f"  Estados: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
        print()
        
        print("SIMULACIÓN:")
        print(f"  NFA acepta:     {'OK SÍ' if result.nfa_accepts else 'X NO'}")
        print(f"  DFA acepta:     {'OK SÍ' if result.dfa_accepts else 'X NO'}")
        print(f"  DFA Min acepta: {'OK SÍ' if result.dfa_min_accepts else 'X NO'}")
        print()
        
        print("ARCHIVOS GENERADOS:")
        print("  - ./simple_test_result/nfa.svg")
        print("  - ./simple_test_result/dfa.svg") 
        print("  - ./simple_test_result/dfa_min.svg")
        print("  - ./simple_test_result/regex.txt")
        
        # Resultado final
        final_result = result.dfa_min_accepts
        print()
        print("=" * 60)
        if final_result:
            print("RESULTADO: LA PALABRA ES ACEPTADA")
        else:
            print("RESULTADO: LA PALABRA ES RECHAZADA")
        print("=" * 60)
        
    except Exception as e:
        print(f"X ERROR: {e}")
        print("=" * 60)

if __name__ == "__main__":
    main()
