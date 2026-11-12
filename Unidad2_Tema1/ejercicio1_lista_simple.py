"""Ejercicio 1: Historial de despachos finalizados (lista enlazada simple).
Todos los datos se ingresan manualmente por teclado."""
from datetime import datetime
from decimal import Decimal, InvalidOperation


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


def leer_fecha(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            datetime.strptime(texto, "%d/%m/%Y")
            return texto
        except ValueError:
            print("  [!] Use el formato DD/MM/AAAA con una fecha real.")


def leer_decimal(mensaje, permitir_cero=False):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = Decimal(texto)
            if valor.is_finite() and (valor > 0 or (permitir_cero and valor == 0)):
                return valor.quantize(Decimal("0.01"))
            print("  [!] El monto debe ser positivo.")
        except InvalidOperation:
            print("  [!] Ingrese un valor numérico (ej. 350.50).")


# ---------- Modelo de datos y nodo ----------
class RegistroDespacho:
    def __init__(self, id_registro, nombre_transportista, fecha, monto_flete):
        self.id_registro = id_registro
        self.nombre_transportista = nombre_transportista
        self.fecha = fecha
        self.monto_flete = monto_flete

    def __str__(self):
        return (f"ID {self.id_registro:<4}| {self.nombre_transportista:<18}| "
                f"{self.fecha} | $ {self.monto_flete:>9.2f}")


class NodoSimple:
    def __init__(self, dato):
        self.dato = dato      # objeto RegistroDespacho
        self.sig = None       # puntero al siguiente nodo


# ---------- TAD: lista enlazada simple ----------
class HistorialDespachos:
    def __init__(self):
        self.inicio = None
        self.fin = None       # permite insertar al final en O(1)
        self.cantidad = 0

    def existe_id(self, id_registro):
        actual = self.inicio
        while actual is not None:
            if actual.dato.id_registro == id_registro:
                return True
            actual = actual.sig
        return False

    def insertar_final(self, registro):
        nuevo = NodoSimple(registro)
        if self.inicio is None:          # lista vacía
            self.inicio = nuevo
        else:                            # se enlaza detrás del último
            self.fin.sig = nuevo
        self.fin = nuevo
        self.cantidad += 1

    def mostrar_historial(self):
        print("\n=== HISTORIAL DE DESPACHOS FINALIZADOS ===")
        if self.inicio is None:
            print("Sin despachos registrados.")
            return
        actual = self.inicio
        while actual is not None:        # recorrido simple hasta None
            print(actual.dato)
            actual = actual.sig
        print(f"Total de despachos: {self.cantidad}")

    def filtrar_por_monto(self, valor_minimo):
        print(f"\n=== DESPACHOS CON FLETE MAYOR A $ {valor_minimo:.2f} ===")
        actual = self.inicio
        encontrados = 0
        while actual is not None:
            if actual.dato.monto_flete > valor_minimo:
                print(actual.dato)
                encontrados += 1
            actual = actual.sig
        if encontrados == 0:
            print("Ningún despacho supera ese monto.")
        else:
            print(f"Coincidencias: {encontrados} de {self.cantidad}")


# ---------- Programa principal (menú interactivo) ----------
def registrar_despacho(historial):
    print("\n--- Nuevo despacho ---")
    while True:
        id_registro = leer_entero("ID del registro: ")
        if not historial.existe_id(id_registro):
            break
        print("  [!] Ese ID ya existe en el historial.")
    nombre = leer_texto("Nombre del transportista: ")
    fecha = leer_fecha("Fecha (DD/MM/AAAA): ")
    monto = leer_decimal("Monto del flete ($): ")
    historial.insertar_final(RegistroDespacho(id_registro, nombre, fecha, monto))
    print(f"  [OK] Despacho {id_registro} insertado al final de la lista.")


def menu():
    historial = HistorialDespachos()
    while True:
        print("\n===== EJERCICIO 1 · LISTA SIMPLE =====")
        print("[1] Registrar despacho  [2] Mostrar historial")
        print("[3] Filtrar por monto   [4] Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_despacho(historial)
        elif opcion == "2":
            historial.mostrar_historial()
        elif opcion == "3":
            minimo = leer_decimal("Monto mínimo para la auditoría ($): ",
                                  permitir_cero=True)
            historial.filtrar_por_monto(minimo)
        elif opcion == "4":
            print("Fin del módulo de despachos.")
            break
        else:
            print("  [!] Opción no válida.")


if __name__ == "__main__":
    menu()
