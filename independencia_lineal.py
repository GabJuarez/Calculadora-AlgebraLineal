from gauss_jordan import gauss_jordan, analizar_solucion
from fractions import Fraction
from sys import exit

def pedir_vectores():
    n = int(input("Ingrese el número de vectores: "))
    m = int(input("Ingrese la dimensión de los vectores: "))
    if n <= 0 or m <= 0:
        print("El número de vectores y la dimensión deben ser positivos")
        return None, n, m
    if n == 1:
        contador = 0
        while True:
            entrada = input(f"Vector (separado por espacios): ")
            partes = entrada.strip().split()
            break
        for parte in partes:
            if parte == 0 or parte == "0":
                contador += 1
        if contador == len(partes):
            print("El vector es el vector 0, por lo tanto, los vectores es linealmente dependiente")
            exit(0)
        else:
            print("El vector no es el vector 0, por lo tanto, el vector es linealmente independiente")
            exit(0)

    if n > m:
        print("\nEl numero de vectores es mayor que la dimension, por lo tanto, los vectores son linealmente dependientes")
        return None, n, m
    vectores = []
    for i in range(n):
        while True:
            entrada = input(f"Vector {i+1} (separado por espacios): ")
            partes = entrada.strip().split()
            if len(partes) != m:
                print(f"Debe ingresar {m} componentes")
                continue
            try:
                vector = [Fraction(x) for x in partes]
                vectores.append(vector)
                break
            except Exception:
                print("Componentes invalidas, intente de nuevo")
    return vectores, n, m

def construir_matriz(vectores, n, m):
    matriz = []
    for i in range(m):
        fila = [vectores[j][i] for j in range(n)]
        matriz.append(fila)
    for fila in matriz:
        fila.append(Fraction(0))
    return matriz

def es_trivial(soluciones):
    for solucion in soluciones:
        if solucion.numerator != 0:
            return False
    return True

def main():
    print("Verificador de independencia lineal de vectores")
    vectores, n, m = pedir_vectores()
    if vectores is None:
        print("Los vectores son linealmente dependientes (por definicion)")
        return
    matriz = construir_matriz(vectores, n, m)
    print("\nMatriz del sistema homogéneo (cada columna es un vector):")
    for fila in matriz:
        for frac in fila:
            print("|", end="")
            print(frac.numerator, end=" ")
        print("|")


    matriz_gj, pivotes = gauss_jordan(matriz)
    tipo, soluciones, libres = analizar_solucion(matriz_gj, [f"c{i+1}" for i in range(n)], pivotes)
    print("\nResultado:")
    print(soluciones)
    if tipo == "única" and es_trivial(soluciones):
        print("Los vectores son linealmente independientes (solo la solucion trivial)")
    else:
        print("Los vectores son linealmente dependientes (existen soluciones no triviales)")

if __name__ == "__main__":
    main()
