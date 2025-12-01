from app.logic.utils import validar_matriz, subindice, fraccion_str
from fractions import Fraction
import math


def _simplify_row(row):
    if not row:
        return row
    dens = [f.denominator for f in row]
    L = 1
    for d in dens:
        if d:
            L = math.lcm(L, d)
    Ns = [f.numerator * (L // f.denominator) for f in row]
    g = abs(L)
    for n in Ns:
        g = math.gcd(g, n)
    if g == 0:
        return [Fraction(0, 1) for _ in row]
    new_den = L // g
    new_row = [Fraction(n // g, new_den) for n in Ns]
    return new_row


def _to_fraction(x, max_den=10**6):
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x, 1)
    if isinstance(x, float):
        return Fraction(x).limit_denominator(max_den)
    try:
        return Fraction(str(x))
    except Exception:
        try:
            return Fraction(float(x)).limit_denominator(max_den)
        except Exception:
            return Fraction(0, 1)


def rref(matriz):
    """
    Calcula la forma reducida por filas (RREF) de una matriz cualquiera.
    Devuelve: (matriz_reducida_str, pasos)
    pasos: lista de tuplas (descripcion, matriz_en_strings)
    """
    validar_matriz(matriz)
    n = len(matriz)
    if n == 0:
        return [], []
    m = len(matriz[0])
    if any(len(fila) != m for fila in matriz):
        raise ValueError("Todas las filas deben tener la misma longitud")

    A = [[_to_fraction(elem) for elem in fila] for fila in matriz]
    pasos = [("Matriz inicial", [fila.copy() for fila in A])]

    row = 0
    for col in range(m):
        if row >= n:
            break
        # buscar pivot
        pivot_row = None
        for r in range(row, n):
            if A[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        # swap
        if pivot_row != row:
            A[row], A[pivot_row] = A[pivot_row], A[row]
            A[row] = _simplify_row(A[row])
            A[pivot_row] = _simplify_row(A[pivot_row])
            pasos.append((f"F{subindice(row+1)} ↔ F{subindice(pivot_row+1)}", [fila.copy() for fila in A]))
        # normalize pivot row
        pivote = A[row][col]
        A[row] = [elem / pivote for elem in A[row]]
        A[row] = _simplify_row(A[row])
        pasos.append((f"F{subindice(row+1)} → F{subindice(row+1)} ÷ {fraccion_str(pivote)}", [fila.copy() for fila in A]))
        # eliminate other rows
        for r in range(n):
            if r != row:
                factor = A[r][col]
                if factor != 0:
                    A[r] = [A[r][k] - factor * A[row][k] for k in range(m)]
                    A[r] = _simplify_row(A[r])
                    pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(row+1)}", [fila.copy() for fila in A]))
        row += 1

    pasos.append(("Matriz reducida (RREF)", [fila.copy() for fila in A]))

    # convertir a strings
    matriz_reducida = [[fraccion_str(A[i][j]) for j in range(m)] for i in range(n)]
    pasos_str = []
    for descripcion, matriz_paso in pasos:
        matriz_paso_str = [[fraccion_str(elem) for elem in fila] for fila in matriz_paso]
        pasos_str.append((descripcion, matriz_paso_str))

    return matriz_reducida, pasos_str

