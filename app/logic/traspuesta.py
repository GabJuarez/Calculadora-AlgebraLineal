from .utils import  matriz_a_str

def traspuesta(matriz):
    """
    Calcula la traspuesta de una matriz y devuelve la traspuesta y los pasos para mostrar en la web.
    matriz: lista de listas (n x m)
    Devuelve: (matriz_traspuesta_str, pasos)
    pasos: lista de tuplas (descripcion, matriz)
    """
    if not matriz or not isinstance(matriz, list) or not all(isinstance(fila, list) for fila in matriz):
        raise ValueError("La matriz debe ser una lista de listas.")
    n = len(matriz)
    m = len(matriz[0])
    for fila in matriz:
        if len(fila) != m:
            raise ValueError("Todas las filas deben tener la misma longitud.")

    pasos = []
    pasos.append(("Matriz original", matriz_a_str(matriz)))

    # Calcular traspuesta
    traspuesta = [[matriz[i][j] for i in range(n)] for j in range(m)]
    pasos.append(("Matriz traspuesta", matriz_a_str(traspuesta)))

    return matriz_a_str(traspuesta), pasos
