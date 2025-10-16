import re

def leer_tamanio():
    while True:
        entrada = input("Ingrese el tamaño de la matriz (ej. 3x3): ")
        if re.match(r"^\d+x\d+$", entrada): # Aqui hay una validacion que indica que si la entrada es igual al patron que le indicamos abajo entonces se ejecutara lo siguiente
            # Los terminos ^ y $ aseguran que no hayan terminos repetidos y /d representan digitos
            n, m = map(int, entrada.lower().split('x')) # Aqui indicamos que n y m van a valer los valores partidos a partir de x
            # El metodo map(int) indica que se van a convertir dos pares a enteros
            if n == m: # Validacion que indica que la matriz debe ser cuadrada de lo contrario pues mandamos un mensaje
                return n
            else:
                print("La matriz debe ser cuadrada. Intente nuevamente.")
        else:
            print("Formato incorrecto. Ejemplo válido: 3x3")


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

def mostrar_matriz(m):
    for fila in m:
        print("\t".join(f"{num:.2f}" for num in fila))
    print()


def matriz_identidad(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    ## Aqui para cada fila i crea una lista con 1 en la posicion j y cuando i es igual a j pone 0

def gauss_jordan_pasos(A):
    n = len(A)
    I = matriz_identidad(n)
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



def main():
    print("=== Inversa de matriz paso a paso usando [A|I] ===")
    n = leer_tamanio()
    A = crear_matriz_directa(n)

    print("\nMatriz A:")
    mostrar_matriz(A)

    try:
        inversa = gauss_jordan_pasos(A)
        print("Matriz inversa A^-1:")
        mostrar_matriz(inversa)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
