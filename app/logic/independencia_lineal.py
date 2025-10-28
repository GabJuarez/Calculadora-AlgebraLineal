from .utils import validar_matriz, subindice, fraccion_str
from fractions import Fraction


def comprobar_independencia_lineal(matriz):
    """
    Comprueba la independencia lineal de los vectores dados como *columnas* de la matriz.
    Devuelve:
      - matriz_reducida_str: matriz en RREF con elementos como cadenas (fracciones)
      - resultado_str: lista de cadenas con resumen (independiente/ dependiente, rango, vectores independientes)
      - pasos_str: lista de tuplas (descripción, matriz_en_cadenas) con los pasos intermedios
    """
    validar_matriz(matriz)
    filas = len(matriz)
    columnas = len(matriz[0])

    # Verificar si el número de vectores (columnas) es mayor que el número de entradas (filas)
    if columnas > filas:
        return None, [
            "Dependientes",
            f"Rango: {filas}",
            "El número de vectores es mayor que el número de entradas, por lo que son linealmente dependientes."
        ], []

    # trabajar con Fracciones
    matriz_fracciones = [[Fraction(elem) for elem in fila] for fila in matriz]
    pasos = [("Matriz inicial", [fila.copy() for fila in matriz_fracciones])]

    # algoritmo RREF recorriendo columnas (permite más columnas que filas)
    fila_actual = 0
    pivotes = []
    matriz_trabajo = [fila.copy() for fila in matriz_fracciones]

    for columna in range(columnas):
        if fila_actual >= filas:
            break
        # encontrar fila con máximo en valor absoluto en esta columna desde 'fila_actual'
        fila_maxima = max(range(fila_actual, filas), key=lambda r: abs(matriz_trabajo[r][columna]))
        if matriz_trabajo[fila_maxima][columna] == 0:
            continue  # no pivote en esta columna
        if fila_maxima != fila_actual:
            matriz_trabajo[fila_actual], matriz_trabajo[fila_maxima] = matriz_trabajo[fila_maxima], matriz_trabajo[fila_actual]
            pasos.append((f"F{subindice(fila_actual+1)} ↔ F{subindice(fila_maxima+1)}", [[fraccion_str(el) for el in f] for f in matriz_trabajo]))
        pivote = matriz_trabajo[fila_actual][columna]

        # normalizar fila pivote
        matriz_trabajo[fila_actual] = [elem / pivote for elem in matriz_trabajo[fila_actual]]
        pasos.append((f"F{subindice(fila_actual+1)} → F{subindice(fila_actual+1)} ÷ {fraccion_str(pivote)}", [[fraccion_str(el) for el in f] for f in matriz_trabajo]))
        # eliminar en todas las demás filas
        for r in range(filas):
            if r != fila_actual and matriz_trabajo[r][columna] != 0:
                factor = matriz_trabajo[r][columna]
                matriz_trabajo[r] = [matriz_trabajo[r][k] - factor * matriz_trabajo[fila_actual][k] for k in range(columnas)]
                pasos.append((f"F{subindice(r+1)} → F{subindice(r+1)} − {fraccion_str(factor)} × F{subindice(fila_actual+1)}", [[fraccion_str(el) for el in f] for f in matriz_trabajo]))
        pivotes.append((fila_actual, columna))
        fila_actual += 1

    # preparar resultados
    rango = len(pivotes)
    independientes = [col for (_, col) in pivotes]
    es_independiente = (rango == columnas)
    estado = "Independientes" if es_independiente else "Dependientes"
    vectores_independientes = [subindice(c+1) for c in independientes]  # 1-based con subíndices

    matriz_reducida_str = [[fraccion_str(matriz_trabajo[i][j]) for j in range(columnas)] for i in range(filas)]
    resultado_str = [
        estado,
        f"Rango: {rango}",
        "Vectores independientes (columnas): [" + ", ".join(vectores_independientes) + "]"
    ]
    pasos_str = pasos + [("Matriz en forma reducida (RREF)", [[fraccion_str(el) for el in f] for f in matriz_trabajo])]

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
        mt, res, pasos = comprobar_independencia_lineal(matriz)
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
