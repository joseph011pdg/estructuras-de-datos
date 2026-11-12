"""Ejercicio 3: Monitoreo cíclico de rutas (lista doble circular).
Todos los datos se ingresan manualmente por teclado."""


# ---------- Entrada de datos validada (sin asserts) ----------
def leer_entero(mensaje, minimo=0):
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
            if valor >= minimo:
                return valor
            print(f"  [!] Debe ser un entero mayor o igual a {minimo}.")
        except ValueError:
            print("  [!] Ingrese un número entero válido.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  [!] El campo no puede quedar vacío.")


def leer_estado():
    while True:
        print("Estado: 1) En Ruta  2) Detenido  3) Alerta de Desvío")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            return "En Ruta"
        if opcion == "2":
            return "Detenido"
        if opcion == "3":
            return "Alerta de Desvío"
        print("  [!] Elija 1, 2 o 3.")


# ---------- Modelo de datos y nodo ----------
class MonitoreoRuta:
    def __init__(self, id_unidad, nombre_chofer, velocidad_actual, estado_ruta):
        self.id_unidad = id_unidad
        self.nombre_chofer = nombre_chofer
        self.velocidad_actual = velocidad_actual
        self.estado_ruta = estado_ruta

    def __str__(self):
        return (f"Unidad {self.id_unidad} | {self.nombre_chofer:<10}| "
                f"{self.velocidad_actual:>3} km/h | {self.estado_ruta}")


class NodoCircular:
    def __init__(self, dato):
        self.dato = dato
        self.sig = None
        self.ant = None


# ---------- TAD: lista doble circular ----------
class MonitorCircular:
    def __init__(self):
        self.inicio = None    # no existe 'fin': el último es inicio.ant
        self.cantidad = 0

    def buscar_nodo(self, id_unidad):
        if self.inicio is None:
            return None
        actual = self.inicio
        while True:                      # se detiene al volver al inicio
            if actual.dato.id_unidad == id_unidad:
                return actual
            actual = actual.sig
            if actual is self.inicio:
                return None

    def conectar_unidad(self, unidad):
        nuevo = NodoCircular(unidad)
        if self.inicio is None:          # una sola unidad: se apunta a sí misma
            nuevo.sig = nuevo
            nuevo.ant = nuevo
            self.inicio = nuevo
        else:                            # se inserta entre el último y el inicio
            ultimo = self.inicio.ant
            nuevo.ant = ultimo
            nuevo.sig = self.inicio
            ultimo.sig = nuevo
            self.inicio.ant = nuevo
        self.cantidad += 1

    def desconectar_unidad(self, id_unidad):
        nodo = self.buscar_nodo(id_unidad)
        if nodo is None:
            print(f"  [!] La unidad {id_unidad} no está en monitoreo.")
            return
        if nodo.sig is nodo:             # era la única unidad
            self.inicio = None
        else:                            # se cierra el ciclo sin el nodo
            nodo.ant.sig = nodo.sig
            nodo.sig.ant = nodo.ant
            if nodo is self.inicio:
                self.inicio = nodo.sig
        nodo.sig = None                  # se aísla el nodo retirado
        nodo.ant = None
        self.cantidad -= 1
        print(f"  [OK] Unidad {id_unidad} llegó a destino y salió del ciclo.")

    def carrusel(self, vueltas, adelante=True):
        if self.inicio is None:
            print("No hay unidades en carretera.")
            return
        sentido = "horario (sig)" if adelante else "antihorario (ant)"
        print(f"\n=== PANEL CÍCLICO · {vueltas} vuelta(s) · sentido {sentido} ===")
        actual = self.inicio if adelante else self.inicio.ant
        for paso in range(1, self.cantidad * vueltas + 1):
            print(f"[{paso:02d}] {actual.dato}")
            actual = actual.sig if adelante else actual.ant
            if actual is self.inicio and adelante and paso < self.cantidad * vueltas:
                print("     ---- regreso automático a la primera unidad ----")

    def actualizar_telemetria(self, id_unidad, velocidad, estado):
        nodo = self.buscar_nodo(id_unidad)
        if nodo is None:
            print(f"  [!] La unidad {id_unidad} no está en monitoreo.")
            return
        nodo.dato.velocidad_actual = velocidad
        nodo.dato.estado_ruta = estado
        print(f"  [OK] Telemetría de la unidad {id_unidad} actualizada.")

    # ----- PARTE PERSONALIZADA: semáforo de riesgo en el carrusel -----
    def panel_alertas(self, limite):
        if self.inicio is None:
            print("No hay unidades en carretera.")
            return
        print(f"\n=== SEMÁFORO DE RIESGO (límite {limite} km/h) ===")
        criticas = altas = medias = 0
        actual = self.inicio
        for _ in range(self.cantidad):   # exactamente una vuelta
            dato = actual.dato
            exceso = dato.velocidad_actual > limite
            desvio = dato.estado_ruta == "Alerta de Desvío"
            if exceso and desvio:
                nivel, accion = "ROJO", "llamar al chofer y bloquear ruta"
                criticas += 1
            elif exceso:
                extra = dato.velocidad_actual - limite
                nivel, accion = "NARANJA", f"reducir {extra} km/h de inmediato"
                altas += 1
            elif desvio:
                nivel, accion = "NARANJA", "verificar ruta autorizada por GPS"
                altas += 1
            elif dato.estado_ruta == "Detenido":
                nivel, accion = "AMARILLO", "confirmar motivo de la parada"
                medias += 1
            else:
                nivel, accion = "VERDE", "supervisión normal"
            print(f"{nivel:<8} | Unidad {dato.id_unidad} | {accion}")
            actual = actual.sig
        print(f"Resumen -> rojo: {criticas} | naranja: {altas} | amarillo: {medias}")

    def verificar_circularidad(self):
        """Comprueba con if (no assert) que no exista ningún None."""
        if self.inicio is None:
            print("  [i] Ciclo vacío: inicio = None, cantidad = 0.")
            return
        errores = 0
        actual = self.inicio
        for _ in range(self.cantidad):
            if actual.sig is None or actual.ant is None or actual.sig.ant is not actual:
                errores += 1
            actual = actual.sig
        if actual is not self.inicio:    # tras n pasos debe volver al inicio
            errores += 1
        if errores == 0:
            print(f"  [OK] {self.cantidad} nodo(s): ciclo cerrado en ambos sentidos.")
        else:
            print(f"  [X] Se detectaron {errores} inconsistencias.")


# ---------- Programa principal (menú interactivo) ----------
def conectar(monitor):
    print("\n--- Unidad que sale de la central ---")
    while True:
        id_unidad = leer_entero("ID de la unidad: ", minimo=1)
        if monitor.buscar_nodo(id_unidad) is None:
            break
        print("  [!] Esa unidad ya está en monitoreo.")
    chofer = leer_texto("Nombre del chofer: ")
    velocidad = leer_entero("Velocidad actual (km/h): ")
    estado = leer_estado()
    monitor.conectar_unidad(MonitoreoRuta(id_unidad, chofer, velocidad, estado))
    print(f"  [OK] Unidad {id_unidad} conectada al ciclo de monitoreo.")


def menu():
    monitor = MonitorCircular()
    while True:
        print("\n===== EJERCICIO 3 · LISTA DOBLE CIRCULAR =====")
        print("[1] Conectar unidad      [2] Desconectar unidad  [3] Ver carrusel")
        print("[4] Actualizar telemetría [5] Semáforo de riesgo [6] Verificar ciclo")
        print("[7] Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            conectar(monitor)
        elif opcion == "2":
            monitor.desconectar_unidad(leer_entero("ID a desconectar: ", 1))
        elif opcion == "3":
            vueltas = leer_entero("Número de vueltas: ", minimo=1)
            sentido = input("Sentido [A]delante / [R]etroceso: ").strip().upper()
            monitor.carrusel(vueltas, adelante=(sentido != "R"))
        elif opcion == "4":
            id_unidad = leer_entero("ID de la unidad: ", 1)
            velocidad = leer_entero("Nueva velocidad (km/h): ")
            monitor.actualizar_telemetria(id_unidad, velocidad, leer_estado())
        elif opcion == "5":
            monitor.panel_alertas(leer_entero("Límite de velocidad (km/h): ", 1))
        elif opcion == "6":
            monitor.verificar_circularidad()
        elif opcion == "7":
            print("Fin del módulo de monitoreo.")
            break
        else:
            print("  [!] Opción no válida.")


if __name__ == "__main__":
    menu()
