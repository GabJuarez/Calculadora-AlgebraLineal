from .utils import crear_matriz_identidad

def crear_matriz_directa(n): # Esta funcion se encarga de construir la matriz que el usuario ingreso.
    matriz = []
    for i in range(n): # Ciclo for para recorrer el tamanio de la matriz
        while True:
            fila = input(f"Ingrese la fila {i + 1} (separe los números con espacios): ")
            numeros = fila.strip().split() # Eliminamos espacios al inicio
            if len(numeros) != n:
                print(f"Debe ingresar exactamente {n} números.") # Esto valida que la cantidad de valores sea n
                continue
            try:
                fila_numeros = [float(x) for x in numeros] # Aqui convertirmos la entrada a flotantes para tener mayor precision
                matriz.append(fila_numeros)
                break
            except ValueError:
                print("Ingrese solo números válidos.")
    return matriz

def mostrar_matriz(matriz):
    for fila in matriz:
        print("\t".join(str(num) for num in fila))
    print()

def gauss_jordan_pasos(A):
    n = len(A)
    I = crear_matriz_identidad(n)
    aumentada = [A[i] + I[i] for i in range(n)]
    # Para cada fila i concatenamos la fila A[i] con la fila I[i] formando la matriz aumentada

    print("Matriz aumentada inicial [A | I]:")
    mostrar_matriz(aumentada)

    # Bucle principal por columna/fila pivote:
    for i in range(n):
        pivote = aumentada[i][i]
        if pivote == 0:
            for k in range(i + 1, n): # Se busca una fila tal que aumentada[k][i] != 0 y si se encuentra se intercambian filas
                if aumentada[k][i] != 0:
                    aumentada[i], aumentada[k] = aumentada[k], aumentada[i]
                    pivote = aumentada[i][i]
                    print(f"Intercambiamos fila {i + 1} con fila {k + 1} por pivote cero")
                    mostrar_matriz(aumentada)
                    break
            else: # Si no se encuentra la fila k entonces la matriz no es invertible
                raise ValueError("La matriz no tiene inversa.")

        aumentada[i] = [x / pivote for x in aumentada[i]]
        print(f"Dividimos la fila {i + 1} por el pivote {pivote}")
        mostrar_matriz(aumentada)
        # Aqui se divide la fila [i] entre el pivote dejando 1 en la posicion diagonal

        for j in range(n):
            if j != i: # Para cada fila que sea distinta que i
                factor = aumentada[j][i] # Esta es la entrada que buscamos eliminar
                aumentada[j] = [a - factor * b for a, b in zip(aumentada[j], aumentada[i])] # Aqui tenemos una operacion entre fila j, fila pivote y esto hace cero la entrada en la columna i
                print(f"Hacemos cero en la columna {i + 1}, fila {j + 1}")
                mostrar_matriz(aumentada)

    inversa = [fila[n:] for fila in aumentada] # Cuando la parte izquierda de la matriz aumentada se ha convertido en la identidad, entonces la parte derechha contiene la inversa
    return inversa




if __name__ == "__main__":
    pass