try:
    from .utils import validar_matriz, normalizar_ecuacion, subindice, fraccion_str
except Exception:
    try:
        from app.logic.utils import validar_matriz, normalizar_ecuacion, subindice, fraccion_str
    except Exception:
        from fractions import Fraction
        def validar_matriz(matriz):
            return True
        def normalizar_ecuacion(s):
            return s
        def subindice(num):
            return str(num)
        def fraccion_str(f):
            if isinstance(f, Fraction):
                return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
            return str(f)

from fractions import Fraction
import copy
import ast

def _to_frac(v):
    if isinstance(v, Fraction):
        return v
    if isinstance(v, (int, float)):
        return Fraction(v)
    if isinstance(v, str):
        # intentar conversión directa, luego normalizar, luego literal_eval
        try:
            return Fraction(v)
        except Exception:
            try:
                s = normalizar_ecuacion(v)
                return Fraction(s)
            except Exception:
                try:
                    val = ast.literal_eval(v)
                    return Fraction(val)
                except Exception:
                    raise ValueError(f"No se pudo convertir '{v}' a Fraction.")
    raise ValueError(f"Tipo no soportado para conversión a Fraction: {type(v)}")

def eliminacion_gaussiana(matriz):
    """
    Eliminación Gauss (forward elimination) para matriz aumentada.
    Devuelve: (matriz_triangular_str, soluciones_str, pasos_str)
    pasos_str es lista de tuplas: (descripcion, matriz_en_strings)
    """
    # intentar validar; si falla por strings, convertimos y validamos de nuevo
    try:
        validar_matriz(matriz)
        A = [[Fraction(elem) for elem in fila] for fila in matriz]
    except Exception:
        A = [[_to_frac(elem) for elem in fila] for fila in matriz]
        validar_matriz(A)

    n = len(A)
    if n == 0:
        raise ValueError("La matriz debe tener al menos una fila")
    m = len(A[0])
    if m != n + 1:
        raise ValueError("La matriz debe ser aumentada con n+1 columnas.")

    pasos = []
    pasos.append(("Matriz inicial", [[fraccion_str(elem) for elem in fila] for fila in A]))

    # copia interna para operar con Fracciones
    A = [fila.copy() for fila in A]

    # Eliminación hacia adelante con pivoteo parcial
    for i in range(n):
        # buscar fila con mayor valor absoluto en columna i
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            raise ValueError("El sistema no tiene solución única (columna nula o pivote cero).")
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            pasos.append((f"F{subindice(i+1)} ↔ F{subindice(max_row+1)}", [[fraccion_str(elem) for elem in fila] for fila in A]))

        pivote = A[i][i]
        # normalizar fila i
        A[i] = [elem / pivote for elem in A[i]]
        pasos.append((f"F{subindice(i+1)} → F{subindice(i+1)} ÷ {fraccion_str(pivote)}", [[fraccion_str(elem) for elem in fila] for fila in A]))

        # eliminar debajo
        for r in range(i+1, n):
            factor = A[r][i]
            if factor != 0:
                A[r] = [A[r][k] - factor * A[i][k] for k in range(m)]
                pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(i+1)}", [[fraccion_str(elem) for elem in fila] for fila in A]))

    pasos.append(("Matriz triangular superior", [[fraccion_str(elem) for elem in fila] for fila in A]))

    # Sustitución regresiva
    x = [Fraction(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        if A[i][i] == 0:
            if A[i][-1] != 0:
                raise ValueError("Sistema incompatible detectado.")
            raise ValueError("Infinitas soluciones detectadas.")
        suma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (A[i][-1] - suma) / A[i][i]
        pasos.append((f"Sustitución para x{subindice(i+1)}", [[fraccion_str(elem) for elem in fila] for fila in A]))

    matriz_triangular_str = [[fraccion_str(A[i][j]) for j in range(m)] for i in range(n)]
    soluciones_str = [fraccion_str(val) for val in x]
    pasos_str = pasos

    return matriz_triangular_str, soluciones_str, pasos_str

if __name__ == "__main__":
    # prueba básica
    sistemas = {
        "Sistema 1 (única solución)": [
            [2, 3, -1, 5],
            [4, 4, -3, 3],
            [-2, 3, 2, 7],
        ],
    }
    for nombre, matriz in sistemas.items():
        print("\n" + "=" * 60)
        print(nombre)
        mt, soluciones, pasos = eliminacion_gaussiana(matriz)
        print("Matriz triangular:")
        for fila in mt:
            print(fila)
        print("Soluciones:", soluciones)
        print("Pasos:")
        for desc, mat in pasos:
            print(desc)
            for f in mat:
                print(f)
            print()
        print("=" * 60 + "\n")
