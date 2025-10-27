"""
funciones auxiliares para operaciones de algebra lineal
"""
import re
import unicodedata
from fractions import Fraction

def validar_matriz(matriz):
    """Valida que la matriz sea una lista de listas de numeros y que sea rectangular
       Para: Gauss-Jordan, Eliminacion Gaussiana, Cramer, Inversa, etc."""
    if not isinstance(matriz, list) or not matriz:
        raise ValueError("La matriz debe ser una lista no vacía")
    num_cols = len(matriz[0])
    for fila in matriz:
        if not isinstance(fila, list) or len(fila) != num_cols:
            raise ValueError("Todas las filas deben tener la misma longitud")
        for elem in fila:
            if not isinstance(elem, (int, float, Fraction)):
                raise ValueError("Todos los elementos deben ser números o fracciones")

def normalizar_ecuacion(ecuacion: str) -> str:
    ecuacion = unicodedata.normalize("NFKC", ecuacion)
    reemplazos = {"−": "-", "×": "*", "÷": "/", "⁺": "+", "⁻": "-", "∙": "*", "⋅": "*"}
    ecuacion = re.sub(r"[\u200B\u200C\u200D\u2060]", "", ecuacion)
    for viejo, nuevo in reemplazos.items():
        ecuacion = ecuacion.replace(viejo, nuevo)
    return ecuacion.strip()

def mostrar_matriz(matriz):
    for fila in matriz:
        print("\t".join(str(num) for num in fila))
    print()


def agregar_multiplicacion_implicita(ecuacion, variables):
    for var in variables:
        ecuacion = re.sub(rf'(?<![\w])([\d\.]+)({var})(?![\w])', r'\1*\2', ecuacion)
    return ecuacion


def multiplicar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B")

    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_B):
            for k in range(columnas_A):
                resultado[i][j] += A[i][k] * B[k][j]

    return resultado

def multiplicar_matriz_escalar(matriz, escalar):
    filas = len(matriz)
    columnas = len(matriz[0])
    resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = matriz[i][j] * escalar

    return resultado

def sumar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if filas_A != filas_B or columnas_A != columnas_B:
        raise ValueError("Las matrices deben tener las mismas dimensiones para ser sumadas")

    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_A):
            resultado[i][j] = A[i][j] + B[i][j]

    return resultado

def restar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if filas_A != filas_B or columnas_A != columnas_B:
        raise ValueError("Las matrices deben tener las mismas dimensiones para ser restadas")

    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_A):
            resultado[i][j] = A[i][j] - B[i][j]

    return resultado

def transponer_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    transpuesta = [[0 for _ in range(filas)] for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]

    return transpuesta

def crear_matriz_identidad(tamanio):
    identidad = [[0 for _ in range(tamanio)] for _ in range(tamanio)]
    for i in range(tamanio):
        identidad[i][i] = 1
    return identidad

def matriz_triangular_superior(matriz):
    n = len(matriz)
    import copy
    matriz = copy.deepcopy(matriz)
    for i in range(n):
        pivote = matriz[i][i]
        if pivote == 0:
            for k in range(i + 1, n):
                if matriz[k][i] != 0:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    pivote = matriz[i][i]
                    break
            else:
                raise ValueError("La matriz no es invertible")
        for k in range(i + 1, n):
            factor = matriz[k][i] / pivote
            for j in range(i, n):
                matriz[k][j] -= factor * matriz[i][j]
    return matriz

# fuciones auxiliares para mostrar los pasos con subindices y fracciones
SUBS = {str(i): chr(8320 + i) for i in range(10)}
def subindice(num):
    """Convierte un número en subíndices unicode para notación matemática."""
    return ''.join(SUBS.get(d, d) for d in str(num))

def fraccion_str(frac):
    """Convierte un Fraction en string, mostrando fracción si es necesario."""
    if isinstance(frac, Fraction):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    return str(frac)


if __name__ == '__main__':
    matriz = [[2, 1, -1],
             [-3, -1, 2],
             [-2, 1, 2]]

    print("Matriz original:")
    mostrar_matriz(matriz)
    triangular = matriz_triangular_superior(matriz)
    print("Matriz triangular superior:")
    mostrar_matriz(triangular)