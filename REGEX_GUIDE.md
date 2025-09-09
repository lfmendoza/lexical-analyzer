# 📝 GUÍA DE EXPRESIONES REGULARES VÁLIDAS

## ⚠️ **Problemas Comunes en Windows**

### 1. **Caracteres Unicode Problemáticos**
- ❌ `ε` (epsilon griego) → ✅ `eps`
- ❌ `?` (interrogación) → ✅ `\?` (escapado)
- ❌ `!` (exclamación) → ✅ `\!` (escapado)

### 2. **Secuencias de Escape**
- ❌ `"\?"` → ✅ `r"\?"` (raw string)
- ❌ `"\\?"` → ✅ `r"\?"` (raw string)

## ✅ **Expresiones Regulares Válidas**

### **Básicas**
```python
REGEX = r"a"           # Solo 'a'
REGEX = r"a*"           # Cero o más 'a'
REGEX = r"a+"           # Una o más 'a'
REGEX = r"a?"           # Cero o una 'a'
```

### **Con Alternancia**
```python
REGEX = r"a|b"          # 'a' o 'b'
REGEX = r"(a|b)*"       # Cualquier secuencia de 'a' y 'b'
```

### **Con Concatenación**
```python
REGEX = r"ab"           # 'a' seguido de 'b'
REGEX = r"a*b*"         # Cero o más 'a' seguido de cero o más 'b'
```

### **Complejas**
```python
REGEX = r"(a|b)*abb"    # Cualquier secuencia que termine en 'abb'
REGEX = r"a*b*a*"       # Secuencias de 'a', luego 'b', luego 'a'
REGEX = r"(ab)*"        # Repeticiones de 'ab'
```

### **Con Epsilon**
```python
REGEX = r"a*eps"        # Cero o más 'a' seguido de epsilon
REGEX = r"(a|eps)*"     # Cualquier secuencia de 'a' y epsilon
```

## ❌ **Expresiones Regulares Inválidas**

### **Sintaxis Incorrecta**
```python
# ❌ Operadores sin operandos suficientes
REGEX = r"\?(((.|eps)?!?)\*)+"  # Error: "Insufficient operands for concatenation"

# ❌ Paréntesis desbalanceados
REGEX = r"((a|b)*abb"           # Error: "Unbalanced parentheses"

# ❌ Operadores mal posicionados
REGEX = r"*a"                   # Error: "*" al inicio
REGEX = r"a|"                   # Error: "|" al final
```

### **Caracteres Problemáticos**
```python
# ❌ Caracteres Unicode
REGEX = r"(a|b)*ε"              # Error: UnicodeEncodeError
REGEX = r"a?b!"                 # Error: UnicodeEncodeError

# ❌ Secuencias de escape incorrectas
REGEX = "\?(((.|eps)?!?)\*)+"   # Error: SyntaxWarning
```

## 🎯 **Ejemplos de Uso Correcto**

### **Para el Script `test_lexical.py`**
```python
# Expresión regular a probar
REGEX = r"(a|b)*abb"

# Lista de palabras a probar
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
```

### **Para el Script `test_simple.py`**
```python
REGEX = r"(a|b)*abb"                    # Tu expresión regular aquí
WORD = "aaaaaaaaaaaaaaaaaaaaaaaaabb"  # Tu palabra a probar aquí
```

## 🔧 **Consejos para Windows**

### **1. Usar Raw Strings**
```python
# ✅ Correcto
REGEX = r"\?(((.|eps)?!?)\*)+"

# ❌ Incorrecto
REGEX = "\?(((.|eps)?!?)\*)+"
```

### **2. Evitar Caracteres Unicode**
```python
# ✅ Correcto
REGEX = r"(a|b)*eps"

# ❌ Incorrecto
REGEX = r"(a|b)*ε"
```

### **3. Escapar Caracteres Especiales**
```python
# ✅ Correcto
REGEX = r"\?a\*b"

# ❌ Incorrecto
REGEX = r"?a*b"
```

## 📚 **Referencia de Operadores**

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `*` | Cero o más | `a*` |
| `+` | Una o más | `a+` |
| `?` | Cero o una | `a?` |
| `\|` | Alternancia | `a\|b` |
| `()` | Agrupación | `(ab)*` |
| `.` | Concatenación | `ab` |
| `eps` | Epsilon | `a*eps` |

## 🚀 **Próximos Pasos**

1. **Usa expresiones regulares válidas** con la sintaxis correcta
2. **Evita caracteres Unicode** que causen problemas en Windows
3. **Usa raw strings** (`r"..."`) para secuencias de escape
4. **Prueba con palabras simples** antes de usar casos complejos
5. **Revisa los errores** del analizador para corregir la sintaxis

**¡Con estas reglas, tus scripts funcionarán perfectamente en Windows!** 🎉
