from fractions import Fraction
from .utils import (
    validar_matriz,
    multiplicar_matrices_pasos,
    multiplicar_matriz_escalar,
    sumar_matrices_pasos,
    restar_matrices_pasos,
    matriz_a_str
)

def operar_matrices(A, B, escalar_a=None, escalar_b=None, operacion='suma'):
    """
    Realiza la operación entre dos matrices (suma, resta, multiplicación),
    considerando escalares opcionales para cada matriz.
    Devuelve la matriz resultado y los pasos realizados.
    """
    pasos = []
    validar_matriz(A)
    validar_matriz(B)
    if escalar_a is not None and escalar_a != '':
        try:
            escalar_a = Fraction(escalar_a)
        except Exception:
            raise ValueError("Escalar A inválido")
        A = multiplicar_matriz_escalar(A, escalar_a)
        pasos.append(f"Se multiplica Matriz A por escalar {matriz_a_str([[escalar_a]])[0][0]}")
        pasos.append(f"Matriz A tras multiplicar por escalar: {matriz_a_str(A)}")
    if escalar_b is not None and escalar_b != '':
        try:
            escalar_b = Fraction(escalar_b)
        except Exception:
            raise ValueError("Escalar B inválido")
        B = multiplicar_matriz_escalar(B, escalar_b)
        pasos.append(f"Se multiplica Matriz B por escalar {matriz_a_str([[escalar_b]])[0][0]}")
        pasos.append(f"Matriz B tras multiplicar por escalar: {matriz_a_str(B)}")
    # Realizar operación con pasos
    if operacion == 'suma':
        resultado, pasos_op = sumar_matrices_pasos(A, B)
        pasos.append("Se suman las matrices A y B")
        pasos.extend(pasos_op)
    elif operacion == 'resta':
        resultado, pasos_op = restar_matrices_pasos(A, B)
        pasos.append("Se resta la matriz B de la matriz A")
        pasos.extend(pasos_op)
    elif operacion == 'multiplicacion':
        resultado, pasos_op = multiplicar_matrices_pasos(A, B)
        pasos.append("Se multiplica la matriz A por la matriz B")
        pasos.extend(pasos_op)
    else:
        raise ValueError("Operación no soportada")
    return {
        'resultado': matriz_a_str(resultado),
        'pasos': pasos
    }
