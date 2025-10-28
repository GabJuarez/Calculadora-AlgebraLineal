from .utils import matriz_a_str, subindice, validar_matriz, fraccion_str
from fractions import Fraction


def matriz_triangular(matriz):
    """
    Convierte una matriz cuadrada en su forma triangular superior mostrando todos los pasos.
    Devuelve: (matriz_triangular_str, pasos)
    pasos: lista de tuplas (descripcion, matriz_en_strings)
    """
    try:
        validar_matriz(matriz)
        n = len(matriz)
        if any(len(fila) != n for fila in matriz):
            raise ValueError("La matriz debe ser cuadrada.")
    except ValueError as e:
        raise ValueError(f"Matriz inválida: {e}")

    matriz_trabajo = [[Fraction(str(elem)) for elem in fila] for fila in matriz]
    pasos_triangular = [("Matriz original", matriz_a_str(matriz_trabajo))]

    for i in range(n):
        # pivoteo parcial si es cero
        if matriz_trabajo[i][i] == 0:
            for k in range(i+1, n):
                if matriz_trabajo[k][i] != 0:
                    matriz_trabajo[i], matriz_trabajo[k] = matriz_trabajo[k], matriz_trabajo[i]
                    pasos_triangular.append((f"F{subindice(i+1)} ↔ F{subindice(k+1)} (intercambio por pivote cero)", matriz_a_str(matriz_trabajo)))
                    break
            else:
                raise ValueError("La matriz es singular, no se puede triangularizar completamente.")
        pivote = matriz_trabajo[i][i]
        # eliminando los elementos debajo del pivote
        for j in range(i+1, n):
            factor = matriz_trabajo[j][i] / pivote
            if factor != 0:
                pasos_triangular.append( (
                    f"F{subindice(j+1)} → F{subindice(j+1)} − {fraccion_str(factor)} × F{subindice(i+1)}",
                    matriz_a_str(matriz_trabajo)
                ))
                matriz_trabajo[j] = [matriz_trabajo[j][k] - factor * matriz_trabajo[i][k] for k in range(n)]
    pasos_triangular.append(("Matriz triangular superior", matriz_a_str(matriz_trabajo)))
    return matriz_a_str(matriz_trabajo), pasos_triangular


def calcular_determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada multiplicando los elementos
    de la diagonal principal calculada mediante eliminacion gaussiana en la funcion
    matriz_triangular.
    Devuelve: (determinante, pasos)
    pasos: lista de tuplas (descripcion, matriz_en_strings)
    """
    n = len(matriz)
    matriz_trabajo = [[Fraction(str(elem)) for elem in fila] for fila in matriz]
    for i in range(n):
        pivote = matriz_trabajo[i][i]
        for j in range(i+1, n):
            factor = matriz_trabajo[j][i] / pivote
            if factor != 0:
                matriz_trabajo[j] = [matriz_trabajo[j][k] - factor * matriz_trabajo[i][k] for k in range(n)]
    diagonal = [matriz_trabajo[i][i] for i in range(n)]
    det = Fraction(1, 1)
    for val in diagonal:
        det *= val
    multiplicacion = " × ".join([fraccion_str(val) for val in diagonal])
    descripcion = f"Determinante = " + multiplicacion + f" = {fraccion_str(det)}"
    pasos_determinante = [(descripcion, None)]
    return det, pasos_determinante
