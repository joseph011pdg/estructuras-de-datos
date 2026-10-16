# ============================================================
# Registro de notas de estudiantes
# Estructura de datos: lista (arreglo dinámico) de registros
# Lenguaje: Python
# ============================================================


# 1. Registro: cada estudiante es un diccionario {"nombre", "nota"}
def crear_estudiante(nombre, nota):
    return {"nombre": nombre, "nota": nota}


# 2. Lee una nota y valida que esté entre 0 y 10
def leer_nota():
    while True:
        try:
            nota = float(input("  Nota (0 - 10): "))
            if 0 <= nota <= 10:
                return nota
        except ValueError:
            pass                                  # texto no numérico
        print("  Valor invalido. Intente de nuevo.")


# 3. Operación AGREGAR: inserta un registro al final de la lista
def agregar_estudiante(registro):
    nombre = input("  Nombre: ")
    nota = leer_nota()
    registro.append(crear_estudiante(nombre, nota))


# 4. Operación MOSTRAR: recorre la lista con su índice
def mostrar_registro(registro):
    if not registro:
        print("  El registro esta vacio.")
        return
    print("\n  #   Nombre              Nota")
    print("  ---------------------------------")
    for i, e in enumerate(registro, start=1):
        print(f"  {i:<4}{e['nombre']:<20}{e['nota']:.2f}")


# 5. Operación ELIMINAR: busca por nombre y borra el elemento
def eliminar_estudiante(registro):
    nombre = input("  Nombre a eliminar: ")
    for i, e in enumerate(registro):
        if e["nombre"] == nombre:
            registro.pop(i)
            print(f"  '{nombre}' fue eliminado.")
            return
    print(f"  No se encontro a '{nombre}'.")


# 6. Operación ORDENAR: muestra una copia ordenada de mayor a menor nota
def mostrar_ordenado(registro):
    copia = sorted(registro, key=lambda e: e["nota"], reverse=True)
    print("\n  Ranking (mayor a menor):", end="")
    mostrar_registro(copia)


# 7. Valor agregado: estadísticas descriptivas del curso
def mostrar_estadisticas(registro):
    if not registro:
        print("  No hay datos para calcular.")
        return
    notas = [e["nota"] for e in registro]
    aprobados = sum(1 for n in notas if n >= 7)
    print(f"  Promedio: {sum(notas) / len(notas):.2f}")
    print(f"  Nota maxima: {max(notas):.2f} | Nota minima: {min(notas):.2f}")
    print(f"  Aprobados (>= 7): {aprobados} de {len(notas)}")


# 8. Programa principal: carga inicial y menú de opciones
def main():
    registro = []                                 # estructura dinámica vacía

    print("=== REGISTRO DE NOTAS (Python) ===")
    print("Ingrese los datos de 3 estudiantes:")
    for i in range(1, 4):
        print(f"Estudiante {i}:")
        agregar_estudiante(registro)

    opcion = -1
    while opcion != 0:
        print("\n1. Agregar  2. Mostrar  3. Eliminar  4. Ordenar  5. Estadisticas  0. Salir")
        try:
            opcion = int(input("Opcion: "))
        except ValueError:
            opcion = -1                           # entrada no numérica
        if opcion == 1:
            agregar_estudiante(registro)
        elif opcion == 2:
            mostrar_registro(registro)
        elif opcion == 3:
            eliminar_estudiante(registro)
        elif opcion == 4:
            mostrar_ordenado(registro)
        elif opcion == 5:
            mostrar_estadisticas(registro)
        elif opcion == 0:
            print("Programa finalizado.")
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
