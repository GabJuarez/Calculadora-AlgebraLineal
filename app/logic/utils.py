"""
funciones auxiliares para operaciones de algebra lineal
"""
import re
import unicodedata
from fractions import Fraction

def validar_matriz(matriz):
    """Valida que la matriz sea una lista de listas de numeros y que sea rectangular
       Para: Gauss-Jordan, Eliminacion Gaussiana, Cramer, Inversa, etc."""
    if not isinstance(matriz, list) or not matriz:
        raise ValueError("La matriz debe ser una lista no vacía")
    num_cols = len(matriz[0])
    for fila in matriz:
        if not isinstance(fila, list) or len(fila) != num_cols:
            raise ValueError("Todas las filas deben tener la misma longitud")
        for elem in fila:
            if not isinstance(elem, (int, float, Fraction)):
                raise ValueError("Todos los elementos deben ser números o fracciones")

def mostrar_matriz(matriz):
    for fila in matriz:
        print("\t".join(str(num) for num in fila))
    print()


def agregar_multiplicacion_implicita(ecuacion, variables):
    for var in variables:
        ecuacion = re.sub(rf'(?<![\w])([\d\.]+)({var})(?![\w])', r'\1*\2', ecuacion)
    return ecuacion


def multiplicar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if columnas_A != filas_B:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B")

    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_B):
            for k in range(columnas_A):
                resultado[i][j] += A[i][k] * B[k][j]

    return resultado

def multiplicar_matriz_escalar(matriz, escalar):
    filas = len(matriz)
    columnas = len(matriz[0])
    resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = matriz[i][j] * escalar

    return resultado

def sumar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if filas_A != filas_B or columnas_A != columnas_B:
        raise ValueError("Las matrices deben tener las mismas dimensiones para ser sumadas")

    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_A):
            resultado[i][j] = A[i][j] + B[i][j]

    return resultado

def restar_matrices(A, B):
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])

    if filas_A != filas_B or columnas_A != columnas_B:
        raise ValueError("Las matrices deben tener las mismas dimensiones para ser restadas")

    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_A):
            resultado[i][j] = A[i][j] - B[i][j]

    return resultado

def transponer_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    transpuesta = [[0 for _ in range(filas)] for _ in range(columnas)]

    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]

    return transpuesta

def crear_matriz_identidad(tamanio):
    identidad = [[0 for _ in range(tamanio)] for _ in range(tamanio)]
    for i in range(tamanio):
        identidad[i][i] = 1
    return identidad


# fuciones auxiliares para mostrar los pasos con subindices y fracciones
SUBS = {str(i): chr(8320 + i) for i in range(10)}
def subindice(num):
    """Convierte un número en subíndices unicode para notación matemática."""
    return ''.join(SUBS.get(d, d) for d in str(num))

def fraccion_str(frac):
    """Convierte un Fraction en string, mostrando fracción si es necesario."""
    if isinstance(frac, Fraction):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"
    return str(frac)

def matriz_a_str(matriz):
    """
    Convierte una matriz (lista de listas) a formato string/fracción para mostrar en la web.
    """
    return [[fraccion_str(val) for val in fila] for fila in matriz]

def sumar_matrices_pasos(A, B):
    """
    Suma dos matrices mostrando el paso a paso y la matriz en cada paso con notación matemática unicode.
    """
    filas_A = len(A)
    columnas_A = len(A[0])
    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]
    pasos = []
    from fractions import Fraction
    for i in range(filas_A):
        fila_paso = []
        for j in range(columnas_A):
            suma = A[i][j] + B[i][j]
            resultado[i][j] = suma
            a_str = fraccion_str(A[i][j])
            b_str = fraccion_str(B[i][j])
            suma_str = fraccion_str(suma)
            fila_paso.append(f"F{subindice(i+1)}[{subindice(j+1)}] = {a_str} + {b_str} = {suma_str}")
        pasos.append(f"<strong>Operación en fila {subindice(i+1)}</strong><br>" + '<br>'.join(fila_paso))
        pasos.append(f"<span class='matriz-label-final'>Matriz parcial tras sumar fila {subindice(i+1)}</span>:{matriz_a_str(resultado)}")
    return resultado, pasos

def restar_matrices_pasos(A, B):
    """
    Resta dos matrices mostrando el paso a paso y la matriz en cada paso con notación matemática unicode.
    """
    filas_A = len(A)
    columnas_A = len(A[0])
    resultado = [[0 for _ in range(columnas_A)] for _ in range(filas_A)]
    pasos = []
    from fractions import Fraction
    for i in range(filas_A):
        fila_paso = []
        for j in range(columnas_A):
            resta = A[i][j] - B[i][j]
            resultado[i][j] = resta
            a_str = fraccion_str(A[i][j])
            b_str = fraccion_str(B[i][j])
            resta_str = fraccion_str(resta)
            fila_paso.append(f"F{subindice(i+1)}[{subindice(j+1)}] = {a_str} - {b_str} = {resta_str}")
        pasos.append(f"<strong>Operación en fila {subindice(i+1)}</strong><br>" + '<br>'.join(fila_paso))
        pasos.append(f"<span class='matriz-label-final'>Matriz parcial tras restar fila {subindice(i+1)}</span>:{matriz_a_str(resultado)}")
    return resultado, pasos

def multiplicar_matrices_pasos(A, B):
    """
    Multiplica dos matrices mostrando el paso a paso y la matriz en cada paso con notación matemática unicode.
    """
    filas_A = len(A)
    columnas_A = len(A[0])
    filas_B = len(B)
    columnas_B = len(B[0])
    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]
    pasos = []
    from fractions import Fraction
    for i in range(filas_A):
        fila_paso = []
        for j in range(columnas_B):
            suma = 0
            detalle = []
            for k in range(columnas_A):
                a_str = fraccion_str(A[i][k])
                b_str = fraccion_str(B[k][j])
                detalle.append(f"{a_str}·{b_str}")
                suma += A[i][k] * B[k][j]
            suma_str = fraccion_str(suma)
            resultado[i][j] = suma
            fila_paso.append(f"F{subindice(i+1)}[{subindice(j+1)}] = " + ' + '.join(detalle) + f" = {suma_str}")
        pasos.append(f"<strong>Operación en fila {subindice(i+1)}</strong><br>" + '<br>'.join(fila_paso))
        pasos.append(f"<span class='matriz-label-final'>Matriz parcial tras multiplicar fila {subindice(i+1)}</span>:{matriz_a_str(resultado)}")
    return resultado, pasos


def transformar_sintaxis(expr: str) -> str:
    """
    Transforma una expresión de entrada del usuario a sintaxis válida de Python.
    - '^' -> '**'
    - 'sen' -> 'sin', 'ln' -> 'log'
    - inserta multiplicación implícita: '2x' -> '2*x', ')x' -> ')*x'

    Se intenta reutilizar `app.logic.utils.transformar_sintaxis` si está disponible.
    """
    s = expr.strip()
    # reemplazos simples
    s = s.replace("^", "**")
    # reemplazos de funciones/abreviaturas en forma sensible a mayúsculas
    replacements = {
        r"\bsen(?=\s*\()": "sin",
        r"\bsenh(?=\s*\()": "sinh",
        r"\bln(?=\s*\()": "log",
        # cos, tan, exp, sqrt, etc. se dejan como están (se asume que el usuario usa cos/tan)
    }
    for pat, repl in replacements.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    # insertar multiplicación entre número/u paréntesis cerrado y variable/función abierta
    s = re.sub(r"(\d|\))\s*(?=[A-Za-z\(])", r"\1*", s)
    return s

if __name__ == '__main__':
    matriz = [[2, 1, -1],
             [-3, -1, 2],
             [-2, 1, 2]]
