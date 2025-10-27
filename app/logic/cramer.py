from .determinantes import calcular_determinante, matriz_triangular, validar_matriz
from fractions import Fraction
from .utils import subindice, fraccion_str

def reemplazar_columnas(matriz, vector_independientes, columna):
    columna = columna - 1
    sustituida = [fila[:] for fila in matriz]
    n = len(sustituida)
    for i in range(n):
        sustituida[i][columna] = vector_independientes[i]
    return sustituida

def resolver_cramer(A, B):
    A_fraccion = [[Fraction(str(x)) for x in fila] for fila in A]
    B_fraccion = [Fraction(str(x)) for x in B]
    validar_matriz(A_fraccion)
    n = len(A_fraccion)
    T, intercambios = matriz_triangular(A_fraccion)
    determinante_A = calcular_determinante(T, intercambios)
    if determinante_A == 0:
        raise ValueError('El sistema no tiene solución única (determinante cero)')
    determinantes_sustituidos = []
    soluciones = []
    pasos = []
    pasos.append((f"Determinante principal: Det(A) = {fraccion_str(determinante_A)}", None))
    for i in range(1, n + 1):
        matriz_sustituida = reemplazar_columnas(A_fraccion, B_fraccion, i)
        validar_matriz(matriz_sustituida)
        T_sustituida, intercambiada_sustituida = matriz_triangular(matriz_sustituida)
        determinante_sustituida = calcular_determinante(T_sustituida, intercambiada_sustituida)
        determinantes_sustituidos.append(determinante_sustituida)
        solucion = determinante_sustituida / determinante_A
        matriz_sustituida_str = [[fraccion_str(x) for x in fila] for fila in matriz_sustituida]
        pasos.append((f"Reemplazamos la columna {i} de A por el vector de independientes B para calcular A{subindice(i)}:", matriz_sustituida_str))
        pasos.append((f"Calculamos el determinante: Det(A{subindice(i)}) = {fraccion_str(determinante_sustituida)}", None))
        pasos.append((f"Calculamos la solución: x{subindice(i)} = Det(A{subindice(i)}) / Det(A) = {fraccion_str(determinante_sustituida)} / {fraccion_str(determinante_A)} = {fraccion_str(solucion)}", None))
    soluciones_str = [fraccion_str(sol) for sol in soluciones]
    determinantes_str = [fraccion_str(det) for det in determinantes_sustituidos]
    return soluciones_str, fraccion_str(determinante_A), determinantes_str, pasos

if __name__ == "__main__":
    A = [[2, -1, 3],
         [1, 0, 2],
         [4, 1, 8]]
    B = [5, 3, 11]
    soluciones, det_A, dets_sustituidos, pasos = resolver_cramer(A, B)
    print("Soluciones:", soluciones)
    print("Determinante de A:", det_A)
    print("Determinantes de matrices sustituidas:", dets_sustituidos)
    for descripcion, matriz in pasos:
        print(descripcion)
        if matriz:
            for fila in matriz:
                print("\t".join(fila))
            print()
