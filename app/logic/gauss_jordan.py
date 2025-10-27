from .utils import validar_matriz, subindice, fraccion_str
from fractions import Fraction

def gauss_jordan(matriz):
    """
    Resuelve un sistema de ecuaciones lineales usando el metodo de Gauss-Jordan
    La matriz debe ser aumentada (coeficientes + terminos independientes)
    Devuelve la matriz reducida, la solucion y el paso a paso
    """
    validar_matriz(matriz)
    n = len(matriz)
    m = len(matriz[0])
    A = [[Fraction(elem) for elem in fila] for fila in matriz]
    pasos = [("Matriz inicial", [fila.copy() for fila in A])]

    for i in range(n):
        # buscar el maximo de la columna para evitar dividir por cero
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            raise ValueError("El sistema no tiene solución única (columna nula).")
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            pasos.append((f"F{subindice(i+1)} ↔ F{subindice(max_row+1)}", [fila.copy() for fila in A]))
        # normalizar la fila i
        pivote = A[i][i]
        A[i] = [elem / pivote for elem in A[i]]
        pasos.append((f"F{subindice(i+1)} → F{subindice(i+1)} ÷ {fraccion_str(pivote)}", [fila.copy() for fila in A]))
        # eliminar todos los demas elementos en la columna i
        for j in range(n):
            if j != i:
                factor = A[j][i]
                if factor != 0:
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(m)]
                    pasos.append((f"F{subindice(j+1)} → F{subindice(j+1)} − {fraccion_str(factor)} × F{subindice(i+1)}", [fila.copy() for fila in A]))
    soluciones = [A[i][-1] for i in range(n)]
    pasos.append(("Matriz reducida final", [fila.copy() for fila in A]))

    matriz_reducida = [[fraccion_str(A[i][j]) for j in range(m)] for i in range(n)]
    soluciones_str = [fraccion_str(sol) for sol in soluciones]
    pasos_str = []
    for descripcion, matriz_paso in pasos:
        matriz_paso_str = [[fraccion_str(elem) for elem in fila] for fila in matriz_paso]
        pasos_str.append((descripcion, matriz_paso_str))

    return matriz_reducida, soluciones_str, pasos_str

# prueba del modulo en consola
if __name__ == "__main__":
    matriz = [[1, 2, 3],
              [4, 5, 6]]

    matriz_reducida, soluciones, pasos = gauss_jordan(matriz)

    print("Matriz reducida:")
    for fila in matriz_reducida:
        print(fila)

    for paso in pasos:
        print(paso[0])
        for fila in paso[1]:
            print(fila)
        print()

    print("Soluciones:", soluciones)
