# python
try:
    from .utils import validar_matriz, subindice, fraccion_str
except Exception:
    try:
        from app.logic.utils import validar_matriz, subindice, fraccion_str
    except Exception:
        from fractions import Fraction
        def validar_matriz(matriz):
            return True
        def subindice(num):
            return str(num)
        def fraccion_str(f):
            if isinstance(f, Fraction):
                return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"
            return str(f)

from fractions import Fraction
import copy

def independencia_lineal(matriz):
    """
    Comprueba independencia lineal de los vectores dados como *columnas* de la matriz.
    Devuelve:
      - matriz_reducida_str: matriz en RREF con elementos como strings (fracciones)
      - resultado_str: lista de strings con resumen (independiente/ dependiente, rango, vectores independientes)
      - pasos_str: lista de tuplas (descripcion, matriz_en_strings) con los pasos intermedios
    """
    validar_matriz(matriz)
    n = len(matriz)
    m = len(matriz[0])
    # trabajar con Fracciones
    A = [[Fraction(elem) for elem in fila] for fila in matriz]
    pasos = [("Matriz inicial", [fila.copy() for fila in A])]

    # algoritmo RREF recorriendo columnas (permite más columnas que filas)
    row = 0
    pivots = []
    A_work = [fila.copy() for fila in A]

    for col in range(m):
        if row >= n:
            break
        # encontrar fila con máximo en valor absoluto en esta columna desde 'row'
        max_row = max(range(row, n), key=lambda r: abs(A_work[r][col]))
        if A_work[max_row][col] == 0:
            continue  # no pivote en esta columna
        if max_row != row:
            A_work[row], A_work[max_row] = A_work[max_row], A_work[row]
            pasos.append((f"F{subindice(row+1)} ↔ F{subindice(max_row+1)}", [[fraccion_str(el) for el in f] for f in A_work]))
        piv = A_work[row][col]
        # normalizar fila pivot
        A_work[row] = [elem / piv for elem in A_work[row]]
        pasos.append((f"F{subindice(row+1)} → F{subindice(row+1)} ÷ {fraccion_str(piv)}", [[fraccion_str(el) for el in f] for f in A_work]))
        # eliminar en todas las demás filas
        for r in range(n):
            if r != row and A_work[r][col] != 0:
                factor = A_work[r][col]
                A_work[r] = [A_work[r][k] - factor * A_work[row][k] for k in range(m)]
                pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(row+1)}", [[fraccion_str(el) for el in f] for f in A_work]))
        pivots.append((row, col))
        row += 1

    # preparar resultados
    rango = len(pivots)
    independientes = [col for (_, col) in pivots]
    es_independiente = (rango == m)
    estado = "Independientes" if es_independiente else "Dependientes"
    vectores_ind = [subindice(c+1) for c in independientes]  # 1-based con subíndices

    matriz_reducida_str = [[fraccion_str(A_work[i][j]) for j in range(m)] for i in range(n)]
    resultado_str = [
        estado,
        f"Rango: {rango}",
        "Vectores independientes (columnas): [" + ", ".join(vectores_ind) + "]"
    ]
    pasos_str = pasos + [("Matriz en forma reducida (RREF)", [[fraccion_str(el) for el in f] for f in A_work])]

    return matriz_reducida_str, resultado_str, pasos_str

if __name__ == "__main__":
    # prueba básica
    sistemas = {
        "Ejemplo 1 (independientes)": [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ],
        "Ejemplo 2 (dependientes)": [
            [1, 2, 3],
            [2, 4, 6],
            [3, 6, 9],
        ],
        "Ejemplo 3 (más vectores que dimensión)": [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
        ],
    }

    for nombre, matriz in sistemas.items():
        print("\n" + "=" * 60)
        print(nombre)
        mt, res, pasos = independencia_lineal(matriz)
        print("Matriz reducida:")
        for fila in mt:
            print(fila)
        print("Resumen:", res)
        print("Pasos:")
        for desc, mat in pasos:
            print(desc)
            for f in mat:
                print(f)
            print()
        print("=" * 60 + "\n")

