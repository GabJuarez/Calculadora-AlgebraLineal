from utils import validar_matriz
from fractions import Fraction


def gauss_jordan(matriz):
    """
    Resuelve un sistema de ecuaciones lineales usando el metodo de Gauss-Jordan
    La matriz debe ser aumentada (coeficientes + terminos independientes)
    Devuelve la matriz reducida, la solución y el paso a paso
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
            pasos.append((f"Intercambio fila {i+1} con fila {max_row+1}", [fila.copy() for fila in A]))
        # normalizar la fila i
        pivote = A[i][i]
        A[i] = [elem / pivote for elem in A[i]]
        pasos.append((f"Normalizar fila {i+1} (dividir por pivote {pivote})", [fila.copy() for fila in A]))
        # eliminar todos los demas elementos en la columna i
        for j in range(n):
            if j != i:
                factor = A[j][i]
                if factor != 0:
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(m)]
                    pasos.append((f"Eliminar elemento en fila {j+1}, columna {i+1} (restar {factor} * fila {i+1})", [fila.copy() for fila in A]))
    soluciones = [A[i][-1] for i in range(n)]
    pasos.append(("Matriz reducida final", [fila.copy() for fila in A]))
    pasos.append(("Soluciones", [soluciones]))

    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j].denominator == 1:
                A[i][j] = A[i][j].numerator
            else:
                numerador = str(A[i][j].numerator)
                denominador = str(A[i][j].denominator)
                A[i][j] = f"{numerador}/{denominador}"

    for i in range(len(pasos)):
        for j in range(len(pasos[i][1])):
            for k in range(len(pasos[i][1][j])):
                if pasos[i][1][j][k].denominator == 1:
                    pasos[i][1][j][k] = pasos[i][1][j][k].numerator
                else:
                    numerador = str(pasos[i][1][j][k].numerator)
                    denominador = str(pasos[i][1][j][k].denominator)
                    pasos[i][1][j][k] = f"{numerador}/{denominador}"

    for i in range(len(soluciones)):
        if soluciones[i].denominator == 1:
            soluciones[i] = soluciones[i].numerator
        else:
            numerador = str(soluciones[i].numerator)
            denominador = str(soluciones[i].denominator)
            soluciones[i] = f"{numerador}/{denominador}"

    return A, soluciones, pasos

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
