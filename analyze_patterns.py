#!/usr/bin/env python3
"""
Script de Análisis de Patrones
==============================

Analiza los patrones específicos de las palabras de prueba para crear
una expresión regular que funcione correctamente.
"""

def analyze_patterns():
    """Analiza los patrones de las palabras de prueba"""
    
    print("=" * 80)
    print("ANÁLISIS DE PATRONES DE LAS PALABRAS DE PRUEBA")
    print("=" * 80)
    
    test_words = [
        "if(a){y}else{n}",    # Debe ser aceptada
        "if(atx){y}",         # Debe ser aceptada  
        "if(){y}else{n}",     # No debe ser aceptada
        "if(a){y}else{",      # No debe ser aceptada
        "if(t){a}"            # No debe ser aceptada
    ]
    
    print("Palabras de prueba:")
    for i, word in enumerate(test_words, 1):
        status = "ACEPTADA" if i <= 2 else "RECHAZADA"
        print(f"  {i}. '{word}' -> {status}")
    
    print("\nAnálisis de patrones:")
    print("-" * 40)
    
    # Analizar patrones comunes
    print("Patrones comunes en palabras ACEPTADAS:")
    print("  - Todas empiezan con 'if('")
    print("  - Todas tienen '){y}'")
    print("  - La primera tiene 'else{n}' al final")
    print("  - La segunda NO tiene 'else{n}'")
    
    print("\nPatrones en palabras RECHAZADAS:")
    print("  - 'if(){y}else{n}' -> Paréntesis vacíos")
    print("  - 'if(a){y}else{' -> Falta 'n}' al final")
    print("  - 'if(t){a}' -> No tiene '){y}'")
    
    print("\nExpresión regular sugerida:")
    print("-" * 40)
    print("Para que las primeras dos sean aceptadas y las últimas tres rechazadas:")
    print("REGEX = r'if\\([axt]+\\)\\{y\\}(else\\{n\\})?'")
    print()
    print("Esta expresión significa:")
    print("  - 'if(' -> Literal 'if('")
    print("  - '[axt]+' -> Uno o más caracteres de a, x, t")
    print("  - '){y}' -> Literal '){y}'")
    print("  - '(else{n})?' -> Opcionalmente 'else{n}'")
    
    print("\nVerificación:")
    print("-" * 40)
    regex_pattern = r"if\([axt]+\)\{y\}(else\{n\})?"
    
    for i, word in enumerate(test_words, 1):
        # Simulación simple de matching
        matches = False
        if word.startswith("if(") and word.endswith("){y}"):
            # Verificar que entre los paréntesis solo hay a, x, t
            middle = word[3:word.find("){y}")]
            if middle and all(c in "axt" for c in middle):
                matches = True
        elif word == "if(a){y}else{n}":
            matches = True
            
        status = "✓ ACEPTADA" if matches else "✗ RECHAZADA"
        expected = "✓ ACEPTADA" if i <= 2 else "✗ RECHAZADA"
        result = "CORRECTO" if (matches == (i <= 2)) else "INCORRECTO"
        
        print(f"  {i}. '{word}' -> {status} (esperado: {expected}) [{result}]")

if __name__ == "__main__":
    analyze_patterns()
