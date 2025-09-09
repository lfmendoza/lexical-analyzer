# 🧪 Scripts de Pruebas para Lexical Analyzer

Este directorio contiene scripts de prueba que te permiten probar fácilmente diferentes expresiones regulares sin usar el CLI (que puede fallar en Windows).

## 📁 Scripts Disponibles

### 1. `test_simple.py` - Prueba Individual
**Para:** Probar una expresión regular con una palabra específica.

**Uso:**
1. Abre `test_simple.py`
2. Modifica estas líneas:
   ```python
   REGEX = "(a|b)*abb"                    # Tu expresión regular
   WORD = "aaaaaaaaaaaaaaaaaaaaaaaaabb"  # Tu palabra a probar
   ```
3. Ejecuta: `python test_simple.py`

**Ejemplo de salida:**
```
============================================================
PRUEBA SIMPLE - LEXICAL ANALYZER
============================================================
Expresión: (a|b)*abb
Palabra:   'aaaaaaaaaaaaaaaaaaaaaaaaabb'
Longitud:  27 caracteres

RESULTADOS:
  Postfix: ab|*a.b.b.
  Estados: NFA=14, DFA=5, Min=4

SIMULACIÓN:
  NFA acepta:     ✅ SÍ
  DFA acepta:     ✅ SÍ
  DFA Min acepta: ✅ SÍ

🎉 RESULTADO: LA PALABRA ES ACEPTADA
```

### 2. `test_lexical.py` - Pruebas Múltiples
**Para:** Probar una expresión regular con múltiples palabras.

**Uso:**
1. Abre `test_lexical.py`
2. Modifica estas secciones:
   ```python
   # Expresión regular a probar
   REGEX = "(a|b)*abb"
   
   # Lista de palabras a probar
   TEST_WORDS = [
       "aaaaaaaaaaaaaaaaaaaaaaaaabb",    # Debe ser aceptada
       "aaaaaaaaaaaaaaaaaaaaaaaaabab",   # No debe ser aceptada
       "abb",                            # Debe ser aceptada
       "aabb",                           # Debe ser aceptada
       # ... más palabras
   ]
   ```
3. Ejecuta: `python test_lexical.py`

**Características:**
- Prueba múltiples palabras automáticamente
- Genera estadísticas completas
- Crea directorios organizados para cada prueba
- Muestra análisis de la expresión regular

### 3. `test_from_files.py` - Pruebas desde Archivos
**Para:** Probar múltiples expresiones regulares con múltiples palabras desde archivos de texto.

**Uso:**
1. Ejecuta: `python test_from_files.py` (crea archivos de ejemplo)
2. Modifica los archivos generados:
   - `expresiones.txt`: Lista de expresiones regulares
   - `palabras.txt`: Lista de palabras a probar
3. Ejecuta nuevamente: `python test_from_files.py`

**Ejemplo de `expresiones.txt`:**
```
# Archivo de expresiones regulares
# Una expresión por línea
# Las líneas que empiezan con # son comentarios

(a|b)*abb
a*b*
(ab)*
a+
a?
```

**Ejemplo de `palabras.txt`:**
```
# Archivo de palabras de prueba
# Una palabra por línea

aaaaaaaaaaaaaaaaaaaaaaaaabb
aaaaaaaaaaaaaaaaaaaaaaaaabab
abb
aabb
babb
abab
ab
a
b

```

## 🎯 Casos de Uso Recomendados

### Para Pruebas Rápidas
```bash
python test_simple.py
```
- Cambia `REGEX` y `WORD` en el archivo
- Ejecuta y ve el resultado inmediatamente

### Para Pruebas Exhaustivas
```bash
python test_lexical.py
```
- Modifica `TEST_WORDS` con todas las palabras que quieres probar
- Obtén un reporte completo con estadísticas

### Para Pruebas Masivas
```bash
python test_from_files.py
```
- Modifica `expresiones.txt` y `palabras.txt`
- Prueba todas las combinaciones automáticamente

## 📊 Interpretación de Resultados

### Estados del Autómata
- **NFA:** Autómata finito no determinístico (Thompson)
- **DFA:** Autómata finito determinístico (Subconjuntos)
- **Min:** AFD minimizado (Hopcroft)

### Archivos Generados
Cada prueba genera:
- `nfa.svg`: Visualización del AFN
- `dfa.svg`: Visualización del AFD
- `dfa_min.svg`: Visualización del AFD minimizado
- `regex.txt`: Información detallada del procesamiento

### Códigos de Resultado
- ✅ **ACEPTADA**: La palabra pertenece al lenguaje
- ❌ **RECHAZADA**: La palabra no pertenece al lenguaje
- ⚠️ **ERROR**: Error en el procesamiento

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd C:\Users\tu_usuario\Desktop\Development\Collage\lexical-analyzer
python test_simple.py
```

### Error: "UnicodeEncodeError"
Los scripts están diseñados para Windows y no deberían tener problemas de Unicode.

### Error: "Permission denied"
```bash
# Cierra cualquier archivo SVG que esté abierto
# Luego ejecuta el script nuevamente
```

## 📝 Ejemplos de Expresiones Regulares

### Básicas
- `a`: Solo la letra 'a'
- `a*`: Cero o más 'a'
- `a+`: Una o más 'a'
- `a?`: Cero o una 'a'

### Con Alternancia
- `a|b`: 'a' o 'b'
- `(a|b)*`: Cualquier secuencia de 'a' y 'b'

### Con Concatenación
- `ab`: 'a' seguido de 'b'
- `a*b*`: Cero o más 'a' seguido de cero o más 'b'

### Complejas
- `(a|b)*abb`: Cualquier secuencia que termine en 'abb'
- `a*b*a*`: Secuencias de 'a', luego 'b', luego 'a'
- `(ab)*`: Repeticiones de 'ab'

## 🚀 Próximos Pasos

1. **Prueba básica**: Usa `test_simple.py` para familiarizarte
2. **Pruebas múltiples**: Usa `test_lexical.py` para casos complejos
3. **Pruebas masivas**: Usa `test_from_files.py` para análisis exhaustivos
4. **Visualización**: Abre los archivos `.svg` generados para ver los autómatas
5. **Análisis**: Revisa los archivos `regex.txt` para información detallada

¡Los scripts están listos para usar! 🎉
