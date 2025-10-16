import re


def leer_tamanio():
    while True:
        entrada = input("Ingrese el tamaño de la matriz (ej. 3x3): ")
        if re.match(r"^\d+x\d+$", entrada):
            n, m = map(int, entrada.lower().split('x'))
            if n == m:
                return n
            else:
                print("La matriz debe ser cuadrada. Intente nuevamente.")
        else:
            print("Formato incorrecto. Ejemplo válido: 3x3")


def ecuacion_a_lista(ecuacion, variables):
    ecuacion = ecuacion.replace(" ", "")
    izquierda, derecha = ecuacion.split("=")
    coeficientes = []
    for var in variables:
        match = re.search(r"([+-]?\d*\.?\d*)" + var, izquierda)
        if match:
            coef = match.group(1)
            if coef == "" or coef == "+":
                coef = 1
            elif coef == "-":
                coef = -1
            else:
                coef = float(coef)
        else:
            coef = 0
        coeficientes.append(coef)
    termino = float(derecha)
    return coeficientes, termino


def crear_matriz_por_ecuaciones(n):
    variables = [chr(ord('x') + i) for i in range(n)]
    A = []
    b = []
    for i in range(n):
        ecuacion = input(f"Ingrese la ecuación {i + 1} (ej. 3x + 2y - z = 4): ")
        fila, termino = ecuacion_a_lista(ecuacion, variables)
        A.append(fila)
        b.append([termino])
    return A, b


def mostrar_matriz(m):
    for fila in m:
        print("\t".join(f"{num:.2f}" for num in fila))
    print()


def matriz_identidad(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def gauss_jordan_pasos(A):
    """
    Calcula la inversa mostrando paso a paso usando [A | I]
    """
    n = len(A)
    I = matriz_identidad(n)
    aumentada = [A[i] + I[i] for i in range(n)]

    print("Matriz aumentada inicial [A | I]:")
    mostrar_matriz(aumentada)

    for i in range(n):
        # Pivote
        pivote = aumentada[i][i]
        if pivote == 0:
            for k in range(i + 1, n):
                if aumentada[k][i] != 0:
                    aumentada[i], aumentada[k] = aumentada[k], aumentada[i]
                    pivote = aumentada[i][i]
                    print(f"Intercambiamos fila {i + 1} con fila {k + 1} por pivote cero")
                    mostrar_matriz(aumentada)
                    break
            else:
                raise ValueError("La matriz no tiene inversa.")

        # Dividir fila por pivote
        aumentada[i] = [x / pivote for x in aumentada[i]]
        print(f"Dividimos la fila {i + 1} por el pivote {pivote}")
        mostrar_matriz(aumentada)

        # Hacer ceros en otras filas
        for j in range(n):
            if j != i:
                factor = aumentada[j][i]
                aumentada[j] = [a - factor * b for a, b in zip(aumentada[j], aumentada[i])]
                print(f"Hacemos cero en la columna {i + 1}, fila {j + 1}")
                mostrar_matriz(aumentada)

    inversa = [fila[n:] for fila in aumentada]
    return inversa


def main():
    print("=== Inversa de matriz paso a paso usando [A|I] ===")
    n = leer_tamanio()
    A, b = crear_matriz_por_ecuaciones(n)

    print("\nMatriz A:")
    mostrar_matriz(A)

    try:
        inversa = gauss_jordan_pasos(A)
        print("Matriz inversa A^-1:")
        mostrar_matriz(inversa)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
