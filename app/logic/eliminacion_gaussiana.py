from .utils import validar_matriz, subindice, fraccion_str, matriz_a_str
from fractions import Fraction


def eliminacion_gaussiana(matriz):
    """
    Eliminación de Gauss (metodo de eliminacion hacia atras) para la matriz aumentada.
    Devuelve: (matriz_triangular_str, soluciones_str, pasos_str)
    pasos_str es lista de tuplas: (descripcion_str, matriz_en_strings)
    Las descripciones usan notacion matemática (subindices, flechas, operaciones con filas)
    """
    # Validar entrada si existe esa función en utils
    try:
        validar_matriz(matriz)
    except Exception:
        pass

    # Conversión a Fraction para cálculos internos
    matriz_trabajo = [[Fraction(str(elemento)) for elemento in fila] for fila in matriz]

    n = len(matriz_trabajo)
    if n == 0:
        raise ValueError("La matriz debe tener al menos una fila")
    m = len(matriz_trabajo[0])
    if m != n + 1:
        raise ValueError("La matriz debe ser aumentada con n+1 columnas.")

    pasos = []
    # Usar matriz_a_str para mostrar la matriz aumentada inicial
    pasos.append(("Matriz aumentada inicial", matriz_a_str(matriz_trabajo)))

    # Eliminación hacia adelante con pivoteo parcial
    for i in range(n):
        fila_max = max(range(i, n), key=lambda r: abs(matriz_trabajo[r][i]))
        if matriz_trabajo[fila_max][i] == 0:
            raise ValueError("El sistema no tiene solución única (columna nula o pivote cero).")
        if fila_max != i:
            matriz_trabajo[i], matriz_trabajo[fila_max] = matriz_trabajo[fila_max], matriz_trabajo[i]
            pasos.append((f"F{subindice(i+1)} ↔ F{subindice(fila_max+1)}", matriz_a_str(matriz_trabajo)))

        pivote = matriz_trabajo[i][i]
        matriz_trabajo[i] = [elemento / pivote for elemento in matriz_trabajo[i]]
        pasos.append((f"F{subindice(i+1)} → F{subindice(i+1)} ÷ {fraccion_str(pivote)}", matriz_a_str(matriz_trabajo)))

        for r in range(i+1, n):
            factor = matriz_trabajo[r][i]
            if factor != 0:
                matriz_trabajo[r] = [matriz_trabajo[r][k] - factor * matriz_trabajo[i][k] for k in range(m)]
                pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(i+1)}", matriz_a_str(matriz_trabajo)))

    # Usar matriz_a_str para mostrar la matriz triangular superior
    pasos.append(("Matriz triangular superior", matriz_a_str(matriz_trabajo)))

    soluciones = [Fraction(0) for _ in range(n)]

    # Sustitución regresiva: solo mostrar una ecuación por variable
    for i in range(n - 1, -1, -1):
        if matriz_trabajo[i][i] == 0:
            if matriz_trabajo[i][-1] != 0:
                raise ValueError("Sistema incompatible detectado.")
            raise ValueError("Infinitas soluciones detectadas.")

        suma_ecuacion = []
        suma_valor = Fraction(0)
        for j in range(i + 1, n):
            coef = matriz_trabajo[i][j]
            if coef != 0:
                suma_ecuacion.append(f"{fraccion_str(coef)}×{fraccion_str(soluciones[j])}")
                suma_valor += coef * soluciones[j]

        if suma_ecuacion:
            ecuacion = f"x{subindice(i+1)} = ({fraccion_str(matriz_trabajo[i][-1])} − ({' + '.join(suma_ecuacion)})) ÷ {fraccion_str(matriz_trabajo[i][i])}"
        else:
            ecuacion = f"x{subindice(i+1)} = {fraccion_str(matriz_trabajo[i][-1])} ÷ {fraccion_str(matriz_trabajo[i][i])}"

        numerador = matriz_trabajo[i][-1] - suma_valor
        solucion_i = numerador / matriz_trabajo[i][i]
        soluciones[i] = solucion_i
        # Mostrar la ecuación final sin división si el pivote es 1
        if matriz_trabajo[i][i] == 1:
            ecuacion_final = f"x{subindice(i+1)} = {fraccion_str(solucion_i)}"
        else:
            ecuacion_final = f"x{subindice(i+1)} = {fraccion_str(numerador)} ÷ {fraccion_str(matriz_trabajo[i][i])} = {fraccion_str(solucion_i)}"

        pasos.append((f"Sustitución hacia atrás: {ecuacion}", None))
        pasos.append((f"Resultado: {ecuacion_final}", None))

    matriz_triangular_str = matriz_a_str(matriz_trabajo)
    soluciones_str = [fraccion_str(valor) for valor in soluciones]
    pasos_str = pasos

    return matriz_triangular_str, soluciones_str, pasos_str


if __name__ == "__main__":
    # Prueba básica de consola
    sistemas = {
        "Sistema 1 (única solución)": [
            [1, 1, 12],
            [1, 3, 26]
        ],
    }
    for nombre, matriz in sistemas.items():
        print("\n" + "=" * 60)
        print(nombre)
        mt, soluciones, pasos = eliminacion_gaussiana(matriz)
        print("Matriz triangular:")
        for fila in mt:
            print(fila)
        print("Soluciones:", soluciones)
        print("Pasos:")
        for desc, mat in pasos:
            print(desc)
            if mat:
                for f in mat:
                    print(f)
            print()
        print("=" * 60 + "\n")
