from gauss_jordan import convertir_ecuacion
from determinantes import calcular_determinante, matriz_triangular, validar_matriz
from sys import exit
from fractions import Fraction

def reemplazar_columnas(matriz, vector_independientes, columna):
    columna = columna - 1
    sustituida = [fila[:] for fila in matriz]
    n = len(sustituida)
    for i in range(n):
        sustituida[i][columna] = vector_independientes[i]
    return sustituida

def crear_matriz():
    n_incog = int(input("Ingrese el número de incógnitas: "))
    variables = input("Ingrese las incógnitas (ej: x y z): ").split()
    matriz = []
    print("Ingrese cada ecuación:" )
    for i in range(n_incog):
        while True:
            ecuacion = input(f"Ecuación {i+1}: ")
            try:
                matriz.append(convertir_ecuacion(ecuacion, variables))
                break
            except Exception as e:
                print(f"Error en la ecuación: {e}")
    return matriz, variables

if __name__ == '__main__':
    aumentada, variables = crear_matriz()
    print("\nVariables detectadas:", variables)
    print("\nMatriz aumentada:")
    for fila in aumentada:
        print(fila)
    A = [list(map(Fraction, fila[:-1])) for fila in aumentada]
    independientes = [Fraction(fila[-1]) for fila in aumentada]
    print("\nMatriz de coeficientes:")
    for fila in A:
        print(fila)
    print("\nVector de independientes:")
    print(independientes)
    validar_matriz(A)
    T, intercambios = matriz_triangular(A)
    determinante_original = calcular_determinante(T, intercambios)
    determinantes_sustituidos = []
    if determinante_original == 0:
        exit("No se puede aplicar cramer debido a que el determinante es cero")

    for i in range(1, len(variables)+1):
        matriz_sustituida = reemplazar_columnas(A, independientes, i)
        validar_matriz(matriz_sustituida)
        T_sust, intercambios_sust = matriz_triangular(matriz_sustituida, mostrar_pasos=True)
        determinante_sustituido = calcular_determinante(T_sust, intercambios_sust)
        determinantes_sustituidos.append(determinante_sustituido)

    soluciones = []
    for i in range(len(variables)):
        solucion = determinantes_sustituidos[i] / determinante_original
        soluciones.append(solucion)

    print("\nSoluciones del sistema usando Regla de Cramer:")
    for var, sol in zip(variables, soluciones):
        print("Soluciones como fracciones:")
        print(f"{var} = {sol.numerator}/{sol.denominator}" if sol.denominator != 1 else f"{var} = {sol.numerator}")
        print("Soluciones como numeros decimales:")
        print(f"{var} = {float(sol):.6f}")
