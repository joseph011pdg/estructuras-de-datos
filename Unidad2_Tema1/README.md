# Unidad 2 · Tema 1: TAD y listas enlazadas

**Asignatura:** Estructuras de Datos · **Estudiante:** Joseph Damian Pardo Gualan  
**Carrera:** Ciencia de Datos e Inteligencia Artificial · UNACH

Aplicativo de control operativo para una empresa de logística, dividido en tres módulos.
Ningún módulo usa listas nativas de Python para guardar los datos: todo se almacena en nodos
enlazados con punteros `sig` / `ant`. Todos los datos se ingresan manualmente por teclado
mediante un menú interactivo, sin `assert`; las entradas inválidas se vuelven a solicitar.

| Archivo | Estructura | Contenido |
|---|---|---|
| `ejercicio1_lista_simple.py` | Lista enlazada simple | Historial de despachos: insertar al final, mostrar, filtrar por monto de flete |
| `ejercicio2_lista_doble.py` | Lista doblemente enlazada | Fila de espera de carga: registrar, recorrer en ambos sentidos, navegar, pase directo a la cabeza |
| `ejercicio3_lista_circular.py` | Lista doble circular | Monitoreo de rutas: conectar, desconectar, carrusel cíclico, semáforo de riesgo |
| `Pardo_Joseph_Unidad2_Tema1.ipynb` | — | Los tres ejercicios en un notebook (una celda por ejercicio) |

## Ejecución

```bash
python ejercicio1_lista_simple.py
python ejercicio2_lista_doble.py
python ejercicio3_lista_circular.py
```

Requiere Python 3.8 o superior; solo usa la biblioteca estándar (`datetime`, `decimal`).
