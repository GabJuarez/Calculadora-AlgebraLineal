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


def crear_matriz_directa(n):
    matriz = []
    for i in range(n):
        while True:
            fila = input(f"Ingrese la fila {i + 1} (separe los números con espacios): ")
            numeros = fila.strip().split()
            if len(numeros) != n:
                print(f"Debe ingresar exactamente {n} números.")
                continue
            try:
                fila_numeros = [float(x) for x in numeros]
                matriz.append(fila_numeros)
                break
            except ValueError:
                print("Ingrese solo números válidos.")
    return matriz


def mostrar_matriz(m):
    for fila in m:
        print("\t".join(f"{num:.2f}" for num in fila))
    print()


def matriz_identidad(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def gauss_jordan_pasos(A):
    n = len(A)
    I = matriz_identidad(n)
    aumentada = [A[i] + I[i] for i in range(n)]

    print("Matriz aumentada inicial [A | I]:")
    mostrar_matriz(aumentada)

    for i in range(n):
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

        aumentada[i] = [x / pivote for x in aumentada[i]]
        print(f"Dividimos la fila {i + 1} por el pivote {pivote}")
        mostrar_matriz(aumentada)

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
    A = crear_matriz_directa(n)

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
