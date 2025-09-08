# Analizador Léxico - Procesamiento de Expresiones Regulares

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-dependency%20management-orange.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/lfmendoza/lexical-analyzer/actions)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Última Actualización](https://img.shields.io/github/last-commit/lfmendoza/lexical-analyzer)](https://github.com/lfmendoza/lexical-analyzer/commits/main)
[![Tamaño del Código](https://img.shields.io/github/languages/code-size/lfmendoza/lexical-analyzer)](https://github.com/lfmendoza/lexical-analyzer)

> **Repositorio**: [https://github.com/lfmendoza/lexical-analyzer](https://github.com/lfmendoza/lexical-analyzer)

Este proyecto implementa los algoritmos fundamentales para el procesamiento de expresiones regulares, desarrollado como parte del curso de Teoría de la Computación. El objetivo es construir autómatas finitos a partir de expresiones regulares y verificar si cadenas pertenecen al lenguaje que estas definen.

## ¿Qué hace este proyecto?

El analizador toma una expresión regular (como `(a|b)*abb`) y una cadena de prueba (como `"aabb"`), y te dice si la cadena pertenece al lenguaje definido por la expresión regular. Para hacer esto, implementa varios algoritmos clásicos:

- **Shunting Yard**: Convierte expresiones de notación infija a postfija
- **Construcción de Thompson**: Genera un AFN (Autómata Finito No-determinista) 
- **Construcción por Subconjuntos**: Convierte el AFN a un AFD (Autómata Finito Determinista)
- **Algoritmo de Hopcroft**: Minimiza el AFD para reducir el número de estados

Además, genera visualizaciones en SVG de todos los autómatas para que puedas ver cómo funcionan.

## Instalación

### Opción 1: Con Poetry (Recomendado)

Si tienes Poetry instalado:

```bash
# Instalar dependencias
poetry install

# Activar el entorno virtual
poetry shell
```

### Opción 2: Con pip

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar el paquete
pip install -e .
```

## Uso

### Desde la línea de comandos

```bash
# Procesar una expresión regular
lexical-analyzer --regex "(a|b)*abb" --word "aabb" --outdir resultados

# Procesar múltiples expresiones desde un archivo
lexical-analyzer --input examples/expressions.txt --word "test" --outdir resultados

# Usar símbolo epsilon en ASCII (útil para algunos terminales)
lexical-analyzer --regex "a*" --word "aaa" --ascii-eps --outdir resultados
```

### Desde Python

```python
from lexical_analyzer import LexicalAnalyzer

# Crear el analizador
analyzer = LexicalAnalyzer()

# Procesar una expresión
resultado = analyzer.process_regex(
    regex_raw="(a|b)*abb",
    test_word="aabb", 
    output_dir="./resultados"
)

print(f"¿Acepta 'aabb'? {resultado.nfa_accepts}")
print(f"Estados: NFA={resultado.nfa_states}, DFA={resultado.dfa_states}")
```

## Estructura del Proyecto

```
lexical-analyzer/
├── algorithms/              # Implementación de los algoritmos
│   ├── thompson.py         # Construcción de Thompson
│   ├── subset_construction.py  # Construcción por subconjuntos  
│   └── hopcroft.py         # Minimización de Hopcroft
├── core/                   # Estructuras de datos básicas
├── visualization/          # Generación de gráficos SVG
├── examples/               # Ejemplos de uso
├── tests/                  # Pruebas unitarias e integración
├── cli.py                  # Interfaz de línea de comandos
└── __init__.py             # Módulo principal
```

## Ejemplos Incluidos

En la carpeta `examples/` encontrarás:

- `example.py`: Script que muestra cómo usar el analizador programáticamente
- `expressions.txt`: Archivo con expresiones regulares de ejemplo para probar

Para ejecutar el ejemplo:

```bash
python examples/example.py
```

## Desarrollo

### Configurar el entorno de desarrollo

```bash
# Instalar dependencias de desarrollo
poetry install --with dev

# Instalar hooks de pre-commit
poetry run pre-commit install
```

### Ejecutar pruebas

```bash
# Todas las pruebas
poetry run pytest

# Solo pruebas unitarias
poetry run pytest tests/unit/

# Con cobertura
poetry run pytest --cov=lexical_analyzer --cov-report=html
```

### Formatear código

```bash
# Formatear con Black
poetry run black .

# Ordenar imports
poetry run isort .

# Verificar estilo
poetry run flake8 .
```

## Archivos de Salida

Para cada expresión regular procesada, el analizador genera:

- **`nfa.svg`**: Visualización del AFN generado
- **`dfa.svg`**: Visualización del AFD por construcción de subconjuntos
- **`dfa_min.svg`**: Visualización del AFD minimizado
- **`regex.txt`**: Reporte detallado del procesamiento

## Algoritmos Implementados

### Shunting Yard
Convierte expresiones regulares de notación infija a postfija, manejando correctamente la precedencia de operadores y paréntesis.

### Construcción de Thompson
Genera un AFN a partir de una expresión regular en notación postfija. Cada símbolo, operador de unión, concatenación y estrella de Kleene se traduce a fragmentos de AFN que se combinan apropiadamente.

### Construcción por Subconjuntos
Convierte un AFN a un AFD usando el algoritmo de construcción por subconjuntos, calculando cierres epsilon y transiciones deterministas.

### Minimización de Hopcroft
Minimiza un AFD usando el algoritmo de Hopcroft, particionando estados en clases de equivalencia para reducir el número de estados necesarios.

## Casos de Prueba

El proyecto incluye varios casos de prueba que cubren:

- Expresiones básicas (`a`, `ab`, `a|b`)
- Operadores unarios (`a*`, `a+`, `a?`)
- Expresiones complejas (`(a|b)*abb(a|b)*`)
- Casos con epsilon
- Validación de entrada

## Requisitos

- Python 3.8 o superior
- Poetry (para gestión de dependencias)

## Estado del Proyecto

[![GitHub stars](https://img.shields.io/github/stars/lfmendoza/lexical-analyzer?style=social)](https://github.com/lfmendoza/lexical-analyzer)
[![GitHub forks](https://img.shields.io/github/forks/lfmendoza/lexical-analyzer?style=social)](https://github.com/lfmendoza/lexical-analyzer/fork)
[![GitHub issues](https://img.shields.io/github/issues/lfmendoza/lexical-analyzer)](https://github.com/lfmendoza/lexical-analyzer/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/lfmendoza/lexical-analyzer)](https://github.com/lfmendoza/lexical-analyzer/pulls)

## Contribuir

¡Las contribuciones son bienvenidas! Si quieres contribuir al proyecto:

1. **Fork** el repositorio: [https://github.com/lfmendoza/lexical-analyzer](https://github.com/lfmendoza/lexical-analyzer)
2. **Clona** tu fork localmente: `git clone https://github.com/tu-usuario/lexical-analyzer.git`
3. **Crea** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
4. **Haz commit** de tus cambios: `git commit -am 'Agregar nueva funcionalidad'`
5. **Push** a tu rama: `git push origin feature/nueva-funcionalidad`
6. **Abre** un Pull Request en [GitHub](https://github.com/lfmendoza/lexical-analyzer/pulls)

### Guías de Contribución

- Asegúrate de que todos los tests pasen: `poetry run pytest`
- Sigue el estilo de código: `poetry run black . && poetry run isort .`
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Enlaces Útiles

- **Repositorio**: [https://github.com/lfmendoza/lexical-analyzer](https://github.com/lfmendoza/lexical-analyzer)
- **Issues**: [Reportar problemas](https://github.com/lfmendoza/lexical-analyzer/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/lfmendoza/lexical-analyzer/discussions)
- **Wiki**: [Documentación adicional](https://github.com/lfmendoza/lexical-analyzer/wiki)

## Referencias Académicas

- Thompson, K. (1968). "Programming techniques: Regular expression search algorithm"
- Hopcroft, J. E. (1971). "An n log n algorithm for minimizing states in a finite automaton"
- Aho, A. V., Sethi, R., & Ullman, J. D. (1986). "Compilers: Principles, Techniques, and Tools"