#!/usr/bin/env python3
"""
Script para Probar desde Archivos
=================================

Este script lee expresiones regulares y palabras desde archivos de texto.
Perfecto para probar múltiples casos sin modificar código.

Uso:
1. Crea archivos de entrada (ver ejemplos abajo)
2. Ejecuta: python test_from_files.py
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexical_analyzer import LexicalAnalyzer

def create_example_files():
    """Crear archivos de ejemplo si no existen"""
    
    # Archivo de expresiones regulares
    if not os.path.exists("expresiones.txt"):
        with open("expresiones.txt", "w", encoding="utf-8") as f:
            f.write("""# Archivo de expresiones regulares
# Una expresión por línea
# Las líneas que empiezan con # son comentarios

(a|b)*abb
a*b*
(ab)*
a+
a?
""")
        print("OK Creado archivo: expresiones.txt")
    
    # Archivo de palabras de prueba
    if not os.path.exists("palabras.txt"):
        with open("palabras.txt", "w", encoding="utf-8") as f:
            f.write("""# Archivo de palabras de prueba
# Una palabra por línea
# Las líneas que empiezan con # son comentarios

aaaaaaaaaaaaaaaaaaaaaaaaabb
aaaaaaaaaaaaaaaaaaaaaaaaabab
abb
aabb
babb
abab
ab
a
b

""")
        print("OK Creado archivo: palabras.txt")

def read_file_lines(filename):
    """Leer líneas de un archivo, ignorando comentarios y líneas vacías"""
    if not os.path.exists(filename):
        return []
    
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

def test_from_files():
    """Probar expresiones y palabras desde archivos"""
    
    print("=" * 80)
    print("LEXICAL ANALYZER - PRUEBAS DESDE ARCHIVOS")
    print("=" * 80)
    
    # Crear archivos de ejemplo si no existen
    create_example_files()
    
    # Leer expresiones y palabras
    expresiones = read_file_lines("expresiones.txt")
    palabras = read_file_lines("palabras.txt")
    
    if not expresiones:
        print("X No se encontraron expresiones en expresiones.txt")
        return
    
    if not palabras:
        print("X No se encontraron palabras en palabras.txt")
        return
    
    print(f"Expresiones encontradas: {len(expresiones)}")
    print(f"Palabras encontradas: {len(palabras)}")
    print()
    
    # Crear analizador
    analyzer = LexicalAnalyzer(eps_symbol="eps")
    
    # Probar cada expresión con cada palabra
    test_count = 0
    for i, regex in enumerate(expresiones, 1):
        print(f"EXPRESIÓN {i}: {regex}")
        print("-" * 60)
        
        for j, palabra in enumerate(palabras, 1):
            test_count += 1
            print(f"  Prueba {j:2d}: '{palabra}' ({len(palabra)} chars)", end=" ")
            
            try:
                result = analyzer.process_regex(
                    regex_raw=regex,
                    test_word=palabra,
                    output_dir=f"./file_test_{i}_{j}"
                )
                
                accepts = result.dfa_min_accepts
                status = "OK ACEPTA" if accepts else "X RECHAZA"
                print(f"-> {status}")
                
            except Exception as e:
                print(f"-> X ERROR: {e}")
        
        print()
    
    print("=" * 80)
    print(f"TOTAL DE PRUEBAS REALIZADAS: {test_count}")
    print("=" * 80)
    print()
    print("ARCHIVOS DE ENTRADA:")
    print("- expresiones.txt: Lista de expresiones regulares")
    print("- palabras.txt: Lista de palabras a probar")
    print()
    print("ARCHIVOS DE SALIDA:")
    print("- file_test_X_Y/: Directorios con resultados de cada prueba")
    print("  * nfa.svg, dfa.svg, dfa_min.svg: Visualizaciones")
    print("  * regex.txt: Información detallada")

if __name__ == "__main__":
    test_from_files()
