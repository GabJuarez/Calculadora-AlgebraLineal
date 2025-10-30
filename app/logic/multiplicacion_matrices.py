from fractions import Fraction
from .utils import validar_matriz, multiplicar_matrices, matriz_a_str


def texto_a_matriz(texto):
    lineas = texto.strip().splitlines()
    matriz = []

    for linea in lineas:
        fila = [Fraction(celda) for celda in linea.split()]
        matriz.append(fila)

    validar_matriz(matriz)
    return matriz


def multiplicar_textos(a_texto, b_texto):
    A = texto_a_matriz(a_texto)
    B = texto_a_matriz(b_texto)
    return multiplicar_matrices(A, B)


def multiplicar_y_formatear(a_texto, b_texto):
    resultado = multiplicar_textos(a_texto, b_texto)
    return matriz_a_str(resultado)


if __name__ == "__main__":
    a = "1 2\n3 4"
    b = "5 6\n7 8"

    print("Matriz A:\n", a)
    print("Matriz B:\n", b)
    print("Resultado:\n", multiplicar_y_formatear(a, b))
