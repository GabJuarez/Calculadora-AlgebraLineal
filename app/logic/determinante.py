from app.logic.utils import matriz_a_str, subindice, validar_matriz, fraccion_str
from fractions import Fraction


def _eliminacion_con_pivoteo(matriz):
    """
    Realiza eliminación gaussiana con pivoteo parcial sobre una matriz cuadrada.
    Devuelve una tupla: (matriz_trabajo, pasos, swap_count, es_singular)
    - matriz_trabajo: matriz triangular en Fraction
    - pasos: lista de tuplas (descripcion, matriz_en_string)
    - swap_count: número de intercambios de filas realizados
    - es_singular: True si se detectó singularidad (pivote 0 en columna)
    """
    validar_matriz(matriz)
    n = len(matriz)
    if any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz debe ser cuadrada.")

    trabajo = [[Fraction(str(elem)) for elem in fila] for fila in matriz]
    pasos = [("Matriz original", matriz_a_str(trabajo))]
    swap_count = 0

    for i in range(n):
        # pivoteo parcial: seleccionar fila con mayor valor absoluto en columna i
        max_row = max(range(i, n), key=lambda r: abs(trabajo[r][i]))
        if trabajo[max_row][i] == 0:
            # columna completa de ceros => singular
            return trabajo, pasos, swap_count, True
        if max_row != i:
            trabajo[i], trabajo[max_row] = trabajo[max_row], trabajo[i]
            swap_count += 1
            pasos.append((f"F{subindice(i+1)} ↔ F{subindice(max_row+1)} (pivoteo parcial)", matriz_a_str(trabajo)))

        pivote = trabajo[i][i]
        # eliminar debajo del pivote
        for j in range(i+1, n):
            factor = trabajo[j][i] / pivote
            if factor != 0:
                descripcion = f"F{subindice(j+1)} → F{subindice(j+1)} − {fraccion_str(factor)} × F{subindice(i+1)}"
                trabajo[j] = [trabajo[j][k] - factor * trabajo[i][k] for k in range(n)]
                pasos.append((descripcion, matriz_a_str(trabajo)))

    pasos.append(("Matriz triangular superior", matriz_a_str(trabajo)))
    return trabajo, pasos, swap_count, False


def matriz_triangular(matriz):
    """
    Convierte una matriz cuadrada en su forma triangular superior mostrando todos los pasos.
    Devuelve: (matriz_triangular_str, pasos)
    pasos: lista de tuplas (descripcion, matriz_en_strings)

    Nota: ahora devuelve la triangular parcial y los pasos incluso si la matriz es singular
    (no lanza excepción) para permitir mostrar el proceso en la interfaz.
    """
    trabajo, pasos, swap_count, es_singular = _eliminacion_con_pivoteo(matriz)
    if es_singular:
        # Añadir un paso informativo pero devolver la matriz tal como quedó
        pasos.append(("No se pudo triangularizar completamente: la matriz es singular.", matriz_a_str(trabajo)))
    return matriz_a_str(trabajo), pasos


def calcular_determinante(matriz):
    """
    Calcula el determinante usando eliminación gaussiana con pivoteo parcial.
    Devuelve: (determinante (Fraction), pasos)
    """
    trabajo, pasos_elim, swap_count, es_singular = _eliminacion_con_pivoteo(matriz)
    if es_singular:
        descripcion = "La matriz es singular, determinante = 0"
        # Devolver también los pasos realizados hasta detectar la singularidad
        pasos = pasos_elim + [(descripcion, matriz_a_str(trabajo))]
        return Fraction(0, 1), pasos

    n = len(trabajo)
    diagonal = [trabajo[i][i] for i in range(n)]
    det = Fraction(1, 1)
    for val in diagonal:
        det *= val
    # cada intercambio de filas cambia el signo del determinante
    if swap_count % 2 == 1:
        det *= -1

    multiplicacion = " × ".join([fraccion_str(val) for val in diagonal])
    signo_swaps = f" (se aplicó {swap_count} intercambio(s) de filas → cambio de signo)" if swap_count else ""
    descripcion = f"Determinante = {multiplicacion}{signo_swaps} = {fraccion_str(det)}"
    pasos_determinante = [(descripcion, None)]
    pasos = pasos_elim + pasos_determinante
    return det, pasos


if __name__ == "__main__":
    matriz_ejemplo = [
        [5, -3, 2],
        [-7, 3, -7],
        [9, -5, 5]
    ]
    det, pasos = calcular_determinante(matriz_ejemplo)
    for desc, mat_str in pasos:
        print(desc)
        if mat_str:
            print(mat_str)
    print(f"Determinante final: {det}")