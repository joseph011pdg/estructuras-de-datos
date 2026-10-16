// ============================================================
// Registro de notas de estudiantes
// Estructura de datos: vector (arreglo dinámico) de registros
// Lenguaje: C++
// ============================================================
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
using namespace std;

// 1. Registro (struct) que agrupa los datos de un estudiante
struct Estudiante {
    string nombre;
    double nota;
};

// 2. Lee una nota y valida que esté entre 0 y 10
double leerNota() {
    double nota;
    while (true) {
        cout << "  Nota (0 - 10): ";
        if (cin >> nota && nota >= 0 && nota <= 10) {
            cin.ignore(1000, '\n');            // limpia el salto de línea
            return nota;
        }
        cout << "  Valor invalido. Intente de nuevo.\n";
        cin.clear();                           // restablece el estado de cin
        cin.ignore(1000, '\n');                // descarta la entrada errónea
    }
}

// 3. Operación AGREGAR: inserta un registro al final del vector
void agregarEstudiante(vector<Estudiante>& registro) {
    Estudiante e;
    cout << "  Nombre: ";
    getline(cin, e.nombre);
    e.nota = leerNota();
    registro.push_back(e);
}

// 4. Operación MOSTRAR: recorre el vector con un índice
void mostrarRegistro(const vector<Estudiante>& registro) {
    if (registro.empty()) {
        cout << "  El registro esta vacio.\n";
        return;
    }
    cout << "\n  #   Nombre              Nota\n";
    cout << "  ---------------------------------\n";
    for (size_t i = 0; i < registro.size(); i++) {
        cout << "  " << left << setw(4) << i + 1
             << setw(20) << registro[i].nombre
             << fixed << setprecision(2) << registro[i].nota << "\n";
    }
}

// 5. Operación ELIMINAR: busca por nombre y borra el elemento
void eliminarEstudiante(vector<Estudiante>& registro) {
    string nombre;
    cout << "  Nombre a eliminar: ";
    getline(cin, nombre);
    for (size_t i = 0; i < registro.size(); i++) {
        if (registro[i].nombre == nombre) {
            registro.erase(registro.begin() + i);
            cout << "  '" << nombre << "' fue eliminado.\n";
            return;
        }
    }
    cout << "  No se encontro a '" << nombre << "'.\n";
}

// 6. Operación ORDENAR: muestra una copia ordenada de mayor a menor nota
void mostrarOrdenado(const vector<Estudiante>& registro) {
    vector<Estudiante> copia = registro;       // no altera el original
    sort(copia.begin(), copia.end(),
         [](const Estudiante& a, const Estudiante& b) { return a.nota > b.nota; });
    cout << "\n  Ranking (mayor a menor):";
    mostrarRegistro(copia);
}

// 7. Valor agregado: estadísticas descriptivas del curso
void mostrarEstadisticas(const vector<Estudiante>& registro) {
    if (registro.empty()) {
        cout << "  No hay datos para calcular.\n";
        return;
    }
    double suma = 0, maxima = registro[0].nota, minima = registro[0].nota;
    int aprobados = 0;
    for (const Estudiante& e : registro) {
        suma += e.nota;
        maxima = max(maxima, e.nota);
        minima = min(minima, e.nota);
        if (e.nota >= 7) aprobados++;
    }
    cout << fixed << setprecision(2);
    cout << "  Promedio: " << suma / registro.size() << "\n";
    cout << "  Nota maxima: " << maxima << " | Nota minima: " << minima << "\n";
    cout << "  Aprobados (>= 7): " << aprobados << " de " << registro.size() << "\n";
}

// 8. Programa principal: carga inicial y menú de opciones
int main() {
    vector<Estudiante> registro;               // estructura dinámica vacía

    cout << "=== REGISTRO DE NOTAS (C++) ===\n";
    cout << "Ingrese los datos de 3 estudiantes:\n";
    for (int i = 1; i <= 3; i++) {
        cout << "Estudiante " << i << ":\n";
        agregarEstudiante(registro);
    }

    int opcion;
    do {
        cout << "\n1. Agregar  2. Mostrar  3. Eliminar  4. Ordenar  5. Estadisticas  0. Salir\n";
        cout << "Opcion: ";
        if (!(cin >> opcion)) {                // entrada no numérica
            cin.clear();
            opcion = -1;
        }
        cin.ignore(1000, '\n');
        switch (opcion) {
            case 1: agregarEstudiante(registro); break;
            case 2: mostrarRegistro(registro); break;
            case 3: eliminarEstudiante(registro); break;
            case 4: mostrarOrdenado(registro); break;
            case 5: mostrarEstadisticas(registro); break;
            case 0: cout << "Programa finalizado.\n"; break;
            default: cout << "Opcion no valida.\n";
        }
    } while (opcion != 0);

    return 0;
}
