
from fractions import Fraction

def parse_fraction(value):
    value = value.strip()
    if '/' in value:
        num, denom = value.split('/')
        return Fraction(int(num), int(denom))
    else:
        return Fraction(value)

def validar_matriz(matriz):
    n = len(matriz)
    if n == 0:
        raise ValueError("La matriz no puede estar vacía")
    for fila in matriz:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada")
        for elemento in fila:
            if not isinstance(elemento, Fraction):
                raise ValueError("Todos los elementos deben ser numéricos y tipo Fraction")
    return True

def matriz_triangular(matriz, tolerancia=1e-12, mostrar_pasos=False):
    n = len(matriz)
    import copy
    matriz = copy.deepcopy(matriz)
    intercambios = 0
    for i in range(n):
        pivote = matriz[i][i]
        if abs(float(pivote)) <= tolerancia:
            for k in range(i + 1, n):
                if abs(float(matriz[k][i])) > tolerancia:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    intercambios += 1
                    pivote = matriz[i][i]
                    if mostrar_pasos:
                        print(f"Intercambio de fila {i+1} con fila {k+1} por pivote cero:")
                        for fila in matriz:
                            print('\t'.join(str(num) for num in fila))
                        print()
                    break
            else:
                raise ValueError("no se encontro pivote")
        for k in range(i + 1, n):
            numerador = matriz[k][i]
            factor = numerador / pivote
            for j in range(i, n):
                matriz[k][j] -= factor * matriz[i][j]
            if mostrar_pasos:
                print(f"Eliminando elemento en fila {k+1}, columna {i+1} (factor = {factor}):")
                for fila in matriz:
                    print('\t'.join(str(num) for num in fila))
                print()
    return matriz, intercambios

def calcular_determinante(matriz, intercambios):
    n = len(matriz)
    determinante = Fraction(1)
    for i in range(n):
        determinante *= matriz[i][i]
    if intercambios % 2 == 1:
        determinante *= -1
    return determinante

if __name__ == '__main__':
    pass
