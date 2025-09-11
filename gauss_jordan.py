import re
import unicodedata
from fractions import Fraction


def normalizar_ecuacion(ecuacion: str) -> str:
    ecuacion = unicodedata.normalize("NFKC", ecuacion)
    reemplazos = {"−": "-", "×": "*", "÷": "/", "⁺": "+", "⁻": "-", "∙": "*", "⋅": "*"}
    ecuacion = re.sub(r"[\u200B\u200C\u200D\u2060]", "", ecuacion)
    for viejo, nuevo in reemplazos.items():
        ecuacion = ecuacion.replace(viejo, nuevo)
    return ecuacion.strip()


def convertir_ecuacion(ecuacion, variables):
    ecuacion = ecuacion.replace(" ", "")
    ecuacion = normalizar_ecuacion(ecuacion)
    partes = ecuacion.split("=")
    if len(partes) != 2:
        raise ValueError("La ecuación debe contener un único '='.")

    term_independiente = Fraction(partes[1])
    coeficientes = [Fraction(0)] * len(variables)

    patron = re.compile(r"([+-]?\d*)([a-zA-Z]+)")
    for num in patron.finditer(partes[0]):
        coeficiente, variable = num.groups()
        if coeficiente in ("", "+"):
            coeficiente = Fraction(1)
        elif coeficiente == "-":
            coeficiente = Fraction(-1)
        else:
            coeficiente = Fraction(coeficiente)

        if variable not in variables:
            raise ValueError(f"La variable '{variable}' no está en la lista declarada.")
        coeficientes[variables.index(variable)] = coeficiente

    return coeficientes + [term_independiente]


def crear_matriz():
    while True:
        try:
            n_incog = int(input("Ingrese el número de incógnitas: "))
            if n_incog <= 0:
                print("El número debe ser mayor a 0")
                continue
            break
        except ValueError:
            print("Debe ingresar un numero entero")

    while True:
        variables = input("Ingrese las incógnitas (ej: x y z): ").split()
        if len(variables) != n_incog:
            print(f"Debe ingresar exactamente {n_incog} variables")
            continue
        if len(set(variables)) != n_incog:
            print("Las variables no deben repetirse")
            continue
        break

    matriz = []
    print("Ingrese cada ecuación:")
    for i in range(n_incog):
        while True:
            ecuacion = input(f"Ecuación {i+1}: ")
            try:
                matriz.append(convertir_ecuacion(ecuacion, variables))
                break
            except Exception as e:
                print(f"Error en la ecuación: {e}")
    return matriz, variables


def imprimir_matriz(matriz):
    for fila in matriz:
        print("| " + "  ".join(f"{val!s:>5}" for val in fila[:-1]) + " || " + f"{fila[-1]!s:>5} |")
    print()


def gauss_jordan(matriz, tolerancia=1e-12):
    n, m = len(matriz), len(matriz[0]) - 1
    fila = 0
    pivotes = []

    print("\n--- Proceso Gauss-Jordan ---\nMatriz inicial:")
    imprimir_matriz(matriz)

    for col in range(m):
        # Buscar pivote en esta columna
        pivote = None
        for i in range(fila, n):
            if abs(matriz[i][col]) > tolerancia:
                pivote = i
                break
        if pivote is None:
            continue  # columna libre

        # Intercambiar filas si es necesario
        if pivote != fila:
            print(f"Operacion: F{fila+1} ↔ F{pivote+1}")
            matriz[fila], matriz[pivote] = matriz[pivote], matriz[fila]
            imprimir_matriz(matriz)

        # Normalizar fila pivote
        piv_val = matriz[fila][col]
        if piv_val != 1:
            print(f"Operacion: F{fila+1} → (1/{piv_val})·F{fila+1}")
        matriz[fila] = [x / piv_val for x in matriz[fila]]
        imprimir_matriz(matriz)

        # Eliminar en otras filas
        for i in range(n):
            if i != fila and abs(matriz[i][col]) > tolerancia:
                factor = matriz[i][col]
                if factor != 0:
                    print(f"Operacion: F{i+1} → F{i+1} - ({factor})·F{fila+1}")
                matriz[i] = [a - factor * b for a, b in zip(matriz[i], matriz[fila])]
                imprimir_matriz(matriz)

        pivotes.append(col)
        fila += 1
        if fila == n:
            break

    return matriz, pivotes


def analizar_solucion(matriz, variables, pivotes, tolerancia=1e-12):
    n, m = len(matriz), len(variables)

    # Detectar inconsistencia
    for fila in matriz:
        if all(abs(x) <= tolerancia for x in fila[:-1]) and abs(fila[-1]) > tolerancia:
            return "inconsistente", None, None

    # Ver si hay variables libres
    libres = [variables[j] for j in range(m) if j not in pivotes]
    if len(pivotes) == m:
        # solución única
        sol = [Fraction(0)] * m
        for i, col in enumerate(pivotes):
            sol[col] = matriz[i][-1]
        return "única", sol, libres
    else:
        return "infinitas", None, libres


def imprimir_resultados(tipo, soluciones, variables, libres, pivotes):
    print("\nResultado del sistema de ecuaciones:")
    print("Columnas pivote:", [variables[c] for c in pivotes])

    if tipo == "inconsistente":
        print("➡ El sistema de ecuaciones es inconsistente, no tiene solucion")
    elif tipo == "única":
        print("➡ El sistema tiene solucion unica:")
        for var, val in zip(variables, soluciones):
            print(f"   {var} = {val}")
    else:
        print("➡ El sistema tiene infinitas soluciones:")
        if libres:
            print("Variables libres:", ", ".join(libres))
        else:
            print("no hay variables libres pero faltan restricciones")


if __name__ == "__main__":
    matriz, variables = crear_matriz()
    matriz, pivotes = gauss_jordan(matriz)
    tipo, soluciones, libres = analizar_solucion(matriz, variables, pivotes)
    imprimir_resultados(tipo, soluciones, variables, libres, pivotes)
