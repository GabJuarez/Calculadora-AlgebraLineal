import ast
import math
from typing import Any, Tuple
from .utils import transformar_sintaxis
from tabulate import tabulate

# nombres de math permitidos para que no se pueda acceder a ningun buildin peligroso
_NOMBRES_MATH = {name for name in dir(math) if not name.startswith("_")}
_NOMBRES_PERMITIDOS = _NOMBRES_MATH | {"x"}

# operadores permitidos para binarios y unarios
_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

def _validar_nodo(node: ast.AST) -> None:
    """
    Parametros: nodo del arbol ast para poderse llamar recursivamente
    Valida recursivamente el arbol ast para asegurar
    que solo hay elementos permitidos
    Lanza ValueError si hay elementos no permitidos
    para la expresion"""

    if isinstance(node, ast.Expression):
        _validar_nodo(node.body)
    elif isinstance(node, ast.BinOp):
        if not isinstance(node.op, _ALLOWED_BINOPS):
            raise ValueError("Operador binario no permitido")
        _validar_nodo(node.left)
        _validar_nodo(node.right)
    elif isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, _ALLOWED_UNARYOPS):
            raise ValueError("Operador unario no permitido")
        _validar_nodo(node.operand)
    elif isinstance(node, ast.Call):
        # solo llamadas directas a nombres (sin atributos)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Solo se puede llamar directamente a funciones permitidas")
        nombre = node.func.id
        if nombre not in _NOMBRES_PERMITIDOS:
            raise ValueError(f"Función '{nombre}' no permitida")
        for arg in node.args:
            _validar_nodo(arg)
        if node.keywords:
            raise ValueError("Argumentos por palabra clave no permitidos")
    elif isinstance(node, ast.Name):
        if node.id not in _NOMBRES_PERMITIDOS:
            raise ValueError(f"Nombre '{node.id}' no permitido")
    elif isinstance(node, ast.Constant):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Sólo constantes numéricas permitidas")
    elif isinstance(node, ast.Num):  # compatibilidad
        return
    else:
        raise ValueError(f"Elemento de expresión {type(node).__name__} no permitido")


def evaluar(funcion: str, x: Any) -> float:
    """
    Evalúa la función (string) con un valor dado x.
    Transforma la sintaxis que usa el usuario a sintaxis de Python antes de validar y evaluar.
    """
    expr = transformar_sintaxis(funcion)

    # Parsear a AST tree, validar y evaluar la expresión con solo math y la variable x en el entorno
    tree = ast.parse(expr, mode="eval")
    _validar_nodo(tree)
    env = {name: getattr(math, name) for name in _NOMBRES_MATH}
    env["x"] = x

    # Evaluar en un entorno controlado sin builtins
    return float(eval(compile(tree, filename="<ast>", mode="eval"), {"__builtins__": None}, env))


def biseccion(funcion: str, intervalo: Tuple[float, float], error : float = 0.0001, max_iter: int = 100):
    """
    Parametros: funcion: str, intervalo: tuple[float, float], error: float
    Devuelve la aproximacion de la raiz usando el metodo de biseccion
    con la funcion dada en el intervalo dado hasta el error dado
    0.0001 por defecto
    """

    arbol_funcion = transformar_sintaxis(funcion)
    arbol_funcion = ast.parse(arbol_funcion, mode="eval")
    try:
        _validar_nodo(arbol_funcion)
    except ValueError:
        print("Revise la funcion ingresada, tuvo un error al ser validada")

    pasos = [["Iteración", "a", "b", "c", "f(a)", "f(b)", "f(c)"]]
    iteracion = 0
    a, b = intervalo
    evaluacion_a = evaluar(funcion, a)
    evaluacion_b = evaluar(funcion, b)
    if evaluacion_a * evaluacion_b > 0:
        raise ValueError("No es valido usar biseccion, ya que al evaluar la funcion en los extremos de los"
                         " intervalos, los resultados deben tener distinto signo")
    c = (a + b) / 2.0
    evaluacion_c = evaluar(funcion, c)
    while abs(evaluacion_c) > error or iteracion == max_iter:
        if evaluacion_a * evaluacion_c > 0:
            a = c
            evaluacion_a = evaluar(funcion, a)
            c = (a + b) / 2.0
            evaluacion_c = evaluar(funcion, c)
            iteracion += 1
            paso = [iteracion, a, b, c, evaluacion_a, evaluacion_b, evaluacion_c]
            pasos.append(paso)
        else:
            b = c
            evaluacion_b = evaluar(funcion, b)
            c = (a + b) / 2.0
            evaluacion_c = evaluar(funcion, c)
            iteracion += 1
            paso = [iteracion, a, b, c, evaluacion_a, evaluacion_b, evaluacion_c]
            pasos.append(paso)
    tabla = tabulate(pasos, headers="firstrow", floatfmt=".6f", tablefmt="html")
    return c, tabla, iteracion

if __name__ == "__main__":
    funcion = "x^3 - x - 2"
    intervalo = (1, 2)
    raiz, tabla, iteraciones = biseccion(funcion, intervalo)
    print(f"Raíz aproximada: {raiz}")
    print(f"Iteraciones: {iteraciones}")
    print("Tabla de pasos:")
    print(tabla)


