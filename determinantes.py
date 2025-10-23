from matriz_inversa import leer_tamanio, crear_matriz_directa, mostrar_matriz
from fractions import Fraction
import copy

def validar_matriz(matriz):
    n = len(matriz)
    if n == 0:
        raise ValueError("La matriz no puede estar vacía")
    for fila in matriz:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada")
        for elemento in fila:
            if not (isinstance(elemento, (int, float, Fraction))):
                raise ValueError("Todos los elementos deben ser numéricos")
    return True

def matriz_triangular(matriz, tolerancia=1e-12):
    n = len(matriz)
    matriz = copy.deepcopy(matriz)
    intercambios = 0
    for i in range(n):
        pivote = matriz[i][i]
        # Convertir a Fraction de forma robusta
        if not isinstance(pivote, Fraction):
            if isinstance(pivote, float):
                pivote = Fraction(str(pivote))
            else:
                pivote = Fraction(pivote)
        if abs(pivote) <= tolerancia:
            for k in range(i + 1, n):
                if abs(matriz[k][i]) > tolerancia:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    intercambios += 1
                    pivote = matriz[i][i]
                    if not isinstance(pivote, Fraction):
                        if isinstance(pivote, float):
                            pivote = Fraction(str(pivote))
                        else:
                            pivote = Fraction(pivote)
                    break
            else:
                raise ValueError("no se encontro pivote")
        for k in range(i + 1, n):
            numerador = matriz[k][i]
            # Convertir a Fraction de forma robusta
            if not isinstance(numerador, Fraction):
                if isinstance(numerador, float):
                    numerador = Fraction(str(numerador))
                else:
                    numerador = Fraction(numerador)
            factor = numerador / pivote
            for j in range(i, n):
                matriz[k][j] -= factor * matriz[i][j]
    return matriz, intercambios

def calcular_determinante(matriz, intercambios):
    n = len(matriz)
    determinante = Fraction(1)
    for i in range(n):
        determinante *= matriz[i][i]
    if intercambios % 2 == 1:
        determinante *= -1
    return determinante

if __name__ == '__main__':
    n = leer_tamanio()
    A = crear_matriz_directa(n)
    validar_matriz(A)
    T, intercambios = matriz_triangular(A)
    D = calcular_determinante(T, intercambios)
    print("\nMatriz A:")
    mostrar_matriz(A)
    print("\nMatriz triangular T:")
    mostrar_matriz(T)
    print(f"\nPara la matriz dada 'A' el determinante calculado es: {D}")
