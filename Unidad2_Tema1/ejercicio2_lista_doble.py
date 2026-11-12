"""Ejercicio 2: Zona de triaje y espera de carga (lista doblemente enlazada).
Todos los datos se ingresan manualmente por teclado."""
from datetime import datetime


# ---------- Entrada de datos validada (sin asserts) ----------
def leer_entero(mensaje, minimo=1):
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


def leer_hora(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            datetime.strptime(texto, "%H:%M")
            return texto
        except ValueError:
            print("  [!] Use el formato HH:MM de 24 horas (ej. 07:45).")


def leer_tipo_carga():
    while True:
        print("Tipo de carga: 1) Perecederos  2) Frágil  3) General")
        opcion = input("Seleccione: ").strip()
        if opcion == "1":
            return "Perecederos"
        if opcion == "2":
            return "Frágil"
        if opcion == "3":
            return "General"
        print("  [!] Elija 1, 2 o 3.")


# ---------- Modelo de datos y nodo ----------
class VehiculoEspera:
    def __init__(self, numero_ticket, placa_vehiculo, hora_llegada, tipo_carga):
        self.numero_ticket = numero_ticket
        self.placa_vehiculo = placa_vehiculo.upper()
        self.hora_llegada = hora_llegada
        self.tipo_carga = tipo_carga

    def __str__(self):
        return (f"Ticket {self.numero_ticket} | {self.placa_vehiculo:<9}| "
                f"{self.hora_llegada} | {self.tipo_carga}")


class NodoDoble:
    def __init__(self, dato):
        self.dato = dato
        self.ant = None       # puntero al nodo anterior
        self.sig = None       # puntero al nodo siguiente


# ---------- TAD: lista doblemente enlazada ----------
class FilaEspera:
    def __init__(self):
        self.inicio = None
        self.fin = None
        self.cantidad = 0

    def buscar_nodo(self, numero_ticket):
        actual = self.inicio
        while actual is not None:
            if actual.dato.numero_ticket == numero_ticket:
                return actual
            actual = actual.sig
        return None

    def registrar_llegada(self, vehiculo):
        nuevo = NodoDoble(vehiculo)
        if self.inicio is None:          # primer camión de la bahía
            self.inicio = nuevo
        else:                            # enlace doble con el antiguo fin
            nuevo.ant = self.fin
            self.fin.sig = nuevo
        self.fin = nuevo
        self.cantidad += 1

    def mostrar_fila(self, adelante=True):
        titulo = "INICIO -> FIN" if adelante else "FIN -> INICIO"
        print(f"\n=== FILA DE ESPERA ({titulo}) ===")
        if self.inicio is None:
            print("Sin vehículos en espera.")
            return
        actual = self.inicio if adelante else self.fin
        posicion = 1
        while actual is not None:
            print(f"{posicion}. {actual.dato}")
            actual = actual.sig if adelante else actual.ant
            posicion += 1

    def navegar_fila(self, numero_ticket):
        actual = self.buscar_nodo(numero_ticket)
        if actual is None:
            print(f"  [!] No existe el ticket {numero_ticket}.")
            return
        while True:
            anterior = actual.ant.dato if actual.ant else "Ninguno (inicio de fila)"
            siguiente = actual.sig.dato if actual.sig else "Ninguno (fin de fila)"
            print(f"\n  ANTERIOR    : {anterior}")
            print(f"> SELECCIONADO: {actual.dato}")
            print(f"  SIGUIENTE   : {siguiente}")
            paso = input("[S] siguiente  [A] anterior  [X] salir: ").strip().upper()
            if paso == "S" and actual.sig is not None:
                actual = actual.sig
            elif paso == "A" and actual.ant is not None:
                actual = actual.ant
            elif paso == "X":
                break
            else:
                print("  [!] Movimiento no disponible en ese sentido.")

    def mover_a_inicio(self, numero_ticket):
        nodo = self.buscar_nodo(numero_ticket)
        if nodo is None:
            print(f"  [!] No existe el ticket {numero_ticket}.")
            return
        if nodo is self.inicio:
            print("  [i] Ese vehículo ya está en la cabeza de la fila.")
            return
        # 1) Desenlazar: el anterior y el siguiente se conectan entre sí
        nodo.ant.sig = nodo.sig
        if nodo.sig is not None:
            nodo.sig.ant = nodo.ant
        else:                            # era el último: fin retrocede
            self.fin = nodo.ant
        # 2) Reenlazar el MISMO nodo delante del inicio actual
        nodo.ant = None
        nodo.sig = self.inicio
        self.inicio.ant = nodo
        self.inicio = nodo
        print(f"  [OK] Pase directo: ticket {numero_ticket} movido a la cabeza.")

    def verificar_enlaces(self):
        """Comprueba con if (no assert) que ant y sig sean coherentes."""
        errores = 0
        contador = 0
        actual = self.inicio
        if actual is not None and actual.ant is not None:
            errores += 1
        while actual is not None:
            contador += 1
            if actual.sig is not None and actual.sig.ant is not actual:
                errores += 1
            if actual.sig is None and actual is not self.fin:
                errores += 1
            actual = actual.sig
        if contador != self.cantidad:
            errores += 1
        if errores == 0:
            print(f"  [OK] {contador} nodo(s): punteros ant/sig coherentes.")
        else:
            print(f"  [X] Se detectaron {errores} inconsistencias.")


# ---------- Programa principal (menú interactivo) ----------
def registrar(fila):
    print("\n--- Llegada de vehículo ---")
    while True:
        ticket = leer_entero("Número de ticket (ej. 101): ")
        if fila.buscar_nodo(ticket) is None:
            break
        print("  [!] Ese ticket ya está en la fila.")
    placa = leer_texto("Placa del vehículo: ")
    hora = leer_hora("Hora de llegada (HH:MM): ")
    carga = leer_tipo_carga()
    fila.registrar_llegada(VehiculoEspera(ticket, placa, hora, carga))
    print(f"  [OK] Ticket {ticket} registrado al final de la fila.")


def menu():
    fila = FilaEspera()
    while True:
        print("\n===== EJERCICIO 2 · LISTA DOBLE =====")
        print("[1] Registrar llegada   [2] Fila inicio->fin  [3] Fila fin->inicio")
        print("[4] Navegar fila        [5] Pase directo      [6] Verificar punteros")
        print("[7] Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar(fila)
        elif opcion == "2":
            fila.mostrar_fila(adelante=True)
        elif opcion == "3":
            fila.mostrar_fila(adelante=False)
        elif opcion == "4":
            fila.navegar_fila(leer_entero("Ticket a seleccionar: "))
        elif opcion == "5":
            fila.mover_a_inicio(leer_entero("Ticket con carga urgente: "))
        elif opcion == "6":
            fila.verificar_enlaces()
        elif opcion == "7":
            print("Fin del módulo de espera de carga.")
            break
        else:
            print("  [!] Opción no válida.")


if __name__ == "__main__":
    menu()
