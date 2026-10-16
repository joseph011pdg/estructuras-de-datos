# Unidad 1 · Tema 1 — Registro de notas en C++ y Python

**Actividad:** Introducción a las estructuras de datos: C++ vs. Python
**Estructura usada:** vector (arreglo dinámico) de registros. En C++ es `vector<Estudiante>` con un `struct`; en Python, una lista de diccionarios `{"nombre", "nota"}`.

Ambos programas hacen lo mismo:

1. Registrar al menos 3 estudiantes con su nombre y nota (0 a 10, validada).
2. Agregar más estudiantes en cualquier momento.
3. Mostrar todos los datos en forma de tabla.
4. Eliminar a un estudiante buscándolo por su nombre.
5. Mostrar a los estudiantes ordenados de la nota más alta a la más baja.
6. Calcular estadísticas: promedio, nota máxima, nota mínima y número de aprobados (nota ≥ 7).

## Archivos

| Archivo | Descripción |
|---|---|
| `registro_notas.cpp` | Versión en C++ |
| `registro_notas.py` | Versión en Python |
| `salida_cpp.txt` | Salida de una ejecución de prueba en C++ |
| `salida_py.txt` | Salida de la misma prueba en Python |

## Cómo ejecutar

**C++** (requiere g++ con C++11 o superior):

```bash
g++ -std=c++17 registro_notas.cpp -o registro_notas
./registro_notas
```

**Python** (3.8 o superior):

```bash
python registro_notas.py
```
