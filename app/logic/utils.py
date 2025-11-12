"""
funciones auxiliares para operaciones de algebra lineal
"""
import re
import unicodedata
from fractions import Fraction
import ast
import math
from typing import Any

# nombres de math permitidos para evaluaciones seguras
_NOMBRES_MATH = {name for name in dir(math) if not name.startswith("_")}
_NOMBRES_PERMITIDOS = _NOMBRES_MATH | {"x"}

# operadores permitidos para binarios y unarios
_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

def validar_nodo(node: ast.AST) -> None:
    """
    Valida recursivamente un nodo AST para asegurar que sólo contiene elementos permitidos
    (operadores, llamadas a funciones de math y la variable `x`). Lanza ValueError en caso
    contrario.
    """
    if isinstance(node, ast.Expression):
        validar_nodo(node.body)
    elif isinstance(node, ast.BinOp):
        if not isinstance(node.op, _ALLOWED_BINOPS):
            raise ValueError("Operador binario no permitido")
        validar_nodo(node.left)
        validar_nodo(node.right)
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, _ALLOWED_UNARYOPS):
            raise ValueError("Operador unario no permitido")
        validar_nodo(node.operand)
    elif isinstance(node, ast.Call):
        # solo llamadas directas a nombres (sin atributos)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Solo se puede llamar directamente a funciones permitidas")
        nombre = node.func.id
        if nombre not in _NOMBRES_PERMITIDOS:
            raise ValueError(f"Función '{nombre}' no permitida")
        for arg in node.args:
            validar_nodo(arg)
        if node.keywords:
            raise ValueError("Argumentos por palabra clave no permitidos")
    elif isinstance(node, ast.Name):
        if node.id not in _NOMBRES_PERMITIDOS:
            raise ValueError(f"Nombre '{node.id}' no permitido")
    elif isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Sólo constantes numéricas permitidas")
    elif isinstance(node, ast.Num):  # compatibilidad con versiones antiguas
        return
    else:
        raise ValueError(f"Elemento de expresión {type(node).__name__} no permitido. No se permiten conjuntos (llaves) ni expresiones con llaves en la función. Por favor, ingrese una expresión matemática válida.")


def evaluar(funcion: str, x: Any) -> float:
    """
    Evalúa la función (string) con un valor dado x de forma segura.
    Convierte la sintaxis mediante `transformar_sintaxis`, parsea a AST, valida y evalúa
    usando únicamente el módulo math y la variable x en el entorno.
    """
    expr = transformar_sintaxis(funcion)
    tree = ast.parse(expr, mode="eval")
    validar_nodo(tree)
    env = {name: getattr(math, name) for name in _NOMBRES_MATH}
    env["x"] = x
    return float(eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": None}, env))


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
        # Create a clean text (no HTML) and attach the current matrix as strings so templates render pills + table
        texto = f"Operación en fila {subindice(i+1)}: " + ' ; '.join(fila_paso)
        pasos.append((texto, matriz_a_str(resultado)))
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
        texto = f"Operación en fila {subindice(i+1)}: " + ' ; '.join(fila_paso)
        pasos.append((texto, matriz_a_str(resultado)))
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
        texto = f"Operación en fila {subindice(i+1)}: " + ' ; '.join(fila_paso)
        pasos.append((texto, matriz_a_str(resultado)))
    return resultado, pasos


def transformar_sintaxis(expr: str) -> str:
    """
    Transforma una expresión de entrada del usuario a sintaxis válida de Python.
    - '^' -> '**'
    - 'sen' -> 'sin', 'ln' -> 'log'
    - inserta multiplicación implícita: '2x' -> '2*x', ')x' -> ')*x', '2(' -> '2*('

    Hace transformaciones seguras y no asume que la entrada ya es string.
    """
    if expr is None:
        return ''
    # Asegurar que trabajamos con string
    s = str(expr).strip()
    # reemplazos simples
    s = s.replace('^', '**')
    # Normalizar algunos nombres en español a funciones de math
    replacements = {
        r"\bsen\b": "sin",
        r"\bsinh\b": "sinh",
        r"\bln\b": "log",
        r"\bexp\b": "exp",
        r"\bsqrt\b": "sqrt",
        # dejar cos/tan/log si vienen en inglés
    }
    for pat, repl in replacements.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    # insertar multiplicación implícita entre: número o paréntesis cerrado y paréntesis abierto/función/variable
    # ejemplos: 2x -> 2*x, 2(x+1) -> 2*(x+1), )( -> )*(
    # solamente entre número/parentesis cerrado y letra o '('
    s = re.sub(r"(?<=[0-9\)])\s*(?=[A-Za-z\(])", "*", s)
    # eliminar caracteres unicode invisibles y normalizar espacios
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r"\s+", " ", s)
    return s


def parse_input_number(value) -> float:
    """
    Convierte un string o número en un float, aceptando fracciones, decimales y expresiones matemáticas.
    Acepta: "1/2", "2.5", "ln(2)", "sqrt(2)", "3/4 + 1/2", "pi", "e"
    Si recibe un float/int, lo retorna directamente.
    """
    import math
    import ast

    # Si ya es número, devolver float
    if isinstance(value, (float, int)):
        return float(value)
    if value is None:
        raise ValueError("Valor vacío")

    s = str(value).strip()
    if s == '':
        raise ValueError("Valor vacío")

    # usar transformar_sintaxis para reemplazos comunes
    s = transformar_sintaxis(s)

    # Construir entorno seguro con funciones de math y constantes
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
    # añadir alias comunes y Fraction si se quiere
    from fractions import Fraction
    allowed_names['Fraction'] = Fraction
    allowed_names['pi'] = math.pi
    allowed_names['e'] = math.e

    # Intentar caso simple de fracción entero/entero (ej: 3/4) -> usar Fraction para precisión
    simple_frac = re.fullmatch(r"([+-]?\d+)\s*/\s*([+-]?\d+)", s)
    if simple_frac:
        num, den = simple_frac.groups()
        return float(Fraction(int(num), int(den)))

    # Intentar conversión directa a float
    try:
        return float(s)
    except Exception:
        pass

    # Evaluar expresión segura usando AST
    try:
        tree = ast.parse(s, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Sintaxis inválida en número/expresión: {e}")

    # Validar nodos permitidos
    ALLOWED_NODES = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
        ast.Call, ast.Name, ast.Load, ast.Subscript, ast.Index,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
        ast.UAdd, ast.USub, ast.Tuple, ast.List
    )

    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Expresión no permitida: {type(node).__name__}")
        # nombres solo de math y 'Fraction'
        if isinstance(node, ast.Name):
            if node.id not in allowed_names:
                raise ValueError(f"Nombre o función '{node.id}' no permitido en expresiones numéricas")

    try:
        value_eval = eval(compile(tree, filename='<ast>', mode='eval'), {'__builtins__': None}, allowed_names)
        return float(value_eval)
    except Exception as e:
        raise ValueError(f"No se pudo convertir '{value}' a número: {e}")

if __name__ == '__main__':
    matriz = [[2, 1, -1],
             [-3, -1, 2],
             [-2, 1, 2]]
