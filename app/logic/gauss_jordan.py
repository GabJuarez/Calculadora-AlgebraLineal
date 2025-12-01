from app.logic.utils import validar_matriz, subindice, fraccion_str
from fractions import Fraction
import math

def _simplify_row(row):
    """Reduce a una representación equivalente con enteros más pequeños.
    Convierte la fila de Fraction a numeradores enteros sobre un denominador común L,
    calcula d = gcd(N1,N2,...,L) y devuelve la fila como [Fraction(Ni//d, L//d)].
    Esto evita que los numeradores/denominadores crezcan innecesariamente.
    """
    if not row:
        return row
    # obtener denominadores
    dens = [f.denominator for f in row]
    # lcm de denominadores
    L = 1
    for d in dens:
        if d:
            L = math.lcm(L, d)
    # convertir a numeradores sobre L
    Ns = [f.numerator * (L // f.denominator) for f in row]
    # gcd de todos los numeradores y L
    g = abs(L)
    for n in Ns:
        g = math.gcd(g, n)
    if g == 0:
        # todo ceros -> devolver ceros
        return [Fraction(0, 1) for _ in row]
    # crear nueva fila simplificada
    new_den = L // g
    new_row = [Fraction(n // g, new_den) for n in Ns]
    return new_row

def _to_fraction(x, max_den=10**6):
    """Convertir un valor a Fraction de forma segura.
    - Si ya es Fraction, devolver tal cual.
    - Si es int, convertir directamente.
    - Si es float, limitar denominador para evitar fracciones enormes derivadas de la representación binaria.
    - Intentar crear Fraction(str(x)) para cadenas numéricas cuando sea posible.
    """
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x, 1)
    if isinstance(x, float):
        return Fraction(x).limit_denominator(max_den)
    try:
        # intentar construir desde string (maneja '3/4') o desde int-like
        return Fraction(str(x))
    except Exception:
        try:
            return Fraction(float(x)).limit_denominator(max_den)
        except Exception:
            # fallback
            return Fraction(0, 1)

def gauss_jordan(matriz):
    """
    Resuelve un sistema de ecuaciones lineales usando el metodo de Gauss-Jordan
    La matriz debe ser aumentada (coeficientes + terminos independientes)
    Devuelve la matriz reducida (como strings), la solucion (lista de strings, con parámetros si corresponde)
    y el paso a paso.
    """
    try:
        validar_matriz(matriz)
    except Exception:
        pass

    n = len(matriz)
    m = len(matriz[0])  # columnas totales (variables + 1)
    A = [[_to_fraction(elem) for elem in fila] for fila in matriz]
    pasos = [("Matriz inicial", [fila.copy() for fila in A])]

    row = 0
    pivot_cols = []

    # RREF sobre las columnas de coeficientes (sin la última columna de términos independientes)
    for col in range(m - 1):
        if row >= n:
            break
        # buscar un pivot (elemento no nulo) en la columna desde 'row' hacia abajo
        pivot_row = None
        for r in range(row, n):
            if A[r][col] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            # columna de coeficientes completamente nula -> variable potencialmente libre
            continue

        # intercambiar filas si es necesario
        if pivot_row != row:
            A[row], A[pivot_row] = A[pivot_row], A[row]
            # simplificar filas afectadas
            A[row] = _simplify_row(A[row])
            A[pivot_row] = _simplify_row(A[pivot_row])
            pasos.append((f"F{subindice(row+1)} ↔ F{subindice(pivot_row+1)}", [fila.copy() for fila in A]))

        # normalizar la fila pivot
        pivote = A[row][col]
        A[row] = [elem / pivote for elem in A[row]]
        # simplificar fila
        A[row] = _simplify_row(A[row])
        pasos.append((f"F{subindice(row+1)} → F{subindice(row+1)} ÷ {fraccion_str(pivote)}", [fila.copy() for fila in A]))

        # eliminar la columna en todas las otras filas
        for r in range(n):
            if r != row:
                factor = A[r][col]
                if factor != 0:
                    A[r] = [A[r][k] - factor * A[row][k] for k in range(m)]
                    # simplificar fila resultante
                    A[r] = _simplify_row(A[r])
                    pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(row+1)}", [fila.copy() for fila in A]))

        pivot_cols.append(col)
        row += 1

    pasos.append(("Matriz reducida final", [fila.copy() for fila in A]))

    # Verificar inconsistencia: fila de ceros en coeficientes y término independiente distinto de cero
    for r in range(n):
        if all(A[r][c] == 0 for c in range(m - 1)) and A[r][-1] != 0:
            raise ValueError("Sistema incompatible (sin solución).")

    # Construir la solución: variables libres como parámetros t1, t2, ...
    num_vars = m - 1
    free_cols = [c for c in range(num_vars) if c not in pivot_cols]
    param_names = [f"t{i+1}" for i in range(len(free_cols))]

    soluciones_expr = [None] * num_vars
    # Asignar parámetros a variables libres
    for idx, col in enumerate(free_cols):
        soluciones_expr[col] = param_names[idx]

    # Para cada variable con pivot, encontrar la fila correspondiente y escribir la expresión
    for pc in pivot_cols:
        # encontrar fila con 1 en la columna pc (en RREF)
        pivot_row = next((r for r in range(n) if A[r][pc] == 1), None)
        if pivot_row is None:
            continue
        rhs = A[pivot_row][-1]
        # empezar con el término independiente
        expr = fraccion_str(rhs) if rhs != 0 else "0"
        # sumar los términos de variables libres (x_pc = rhs - sum(A[row][free]*free))
        for idx, fc in enumerate(free_cols):
            coeff = -A[pivot_row][fc]
            if coeff != 0:
                coeff_abs = abs(coeff)
                coeff_str = fraccion_str(coeff_abs)
                param = param_names[idx]
                # construir término (omitir 1)
                term = f"{param}" if coeff_abs == 1 else f"{coeff_str}×{param}"
                # signo
                sign = "+" if coeff > 0 else "-"
                if expr != "0":
                    expr = f"{expr} {sign} {term}"
                else:
                    expr = f"{term}" if coeff > 0 else f"-{term}"
        soluciones_expr[pc] = expr

    # Variables que no tienen pivot ni son libres explícitas (p. ej. columnas extra) -> 0
    for i in range(num_vars):
        if soluciones_expr[i] is None:
            soluciones_expr[i] = "0"

    # Convertir matriz reducida a strings y pasos a strings
    matriz_reducida = [[fraccion_str(A[i][j]) for j in range(m)] for i in range(n)]
    soluciones_str = [sol for sol in soluciones_expr]
    pasos_str = []
    for descripcion, matriz_paso in pasos:
        matriz_paso_str = [[fraccion_str(elem) for elem in fila] for fila in matriz_paso]
        pasos_str.append((descripcion, matriz_paso_str))

    return matriz_reducida, soluciones_str, pasos_str


# prueba del modulo en consola
if __name__ == "__main__":
    # sistema de ecuaciones que de como resultados fracciones simplifiables
    matriz = [
        [1, 1, 1, 10/5],  # x + y + z = 3
        [2, -1, 1, 2],  # 2x - y + z = 2
        [-1, 3, 2, 5]  # -x + 3y + 2z = 5
    ]

    matriz_reducida, soluciones, pasos = gauss_jordan(matriz)

    print("Matriz reducida:")
    for fila in matriz_reducida:
        print(fila)

    for paso in pasos:
        print(paso[0])
        for fila in paso[1]:
            print(fila)
        print()

    print("Soluciones:")
    for i, sol in enumerate(soluciones):
        print(f"x{i+1} = {sol}")
