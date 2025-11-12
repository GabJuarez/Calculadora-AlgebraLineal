import ast
import math
from typing import Any, Tuple
from .utils import transformar_sintaxis, parse_input_number, validar_nodo, evaluar
from tabulate import tabulate

# nombres de math permitidos para que no se pueda acceder a ningun builtin peligroso
_NOMBRES_MATH = {name for name in dir(math) if not name.startswith("_")}
_NOMBRES_PERMITIDOS = _NOMBRES_MATH | {"x"}

def falsa_posicion(funcion: str, intervalo: Tuple[str, str], error : float = 0.0001, max_iter: int = 100):
    """
    Parametros: funcion: str, intervalo: tuple[str, str], error: float
    Devuelve la aproximacion de la raiz usando el metodo de falsa posicion
    con la funcion dada en el intervalo dado hasta el error dado
    0.0001 por defecto
    """
    arbol_funcion = transformar_sintaxis(funcion)
    arbol_funcion = ast.parse(arbol_funcion, mode="eval")
    try:
        validar_nodo(arbol_funcion)
    except ValueError:
        print("Revise la funcion ingresada, tuvo un error al ser validada")

    pasos = [["Iteración", "a", "b", "c", "f(a)", "f(b)", "f(c)"]]
    iteracion = 0
    # Usar parse_input_number para convertir los extremos del intervalo
    a = parse_input_number(intervalo[0])
    b = parse_input_number(intervalo[1])
    evaluacion_a = evaluar(funcion, a)
    evaluacion_b = evaluar(funcion, b)
    if evaluacion_a * evaluacion_b > 0:
        raise ValueError("No es valido usar falsa posicion, ya que al evaluar la funcion en los extremos de los"
                         " intervalos, los resultados deben tener distinto signo")
    c = b - (evaluacion_b * (b- a)) / (evaluacion_b - evaluacion_a)
    evaluacion_c = evaluar(funcion, c)
    while abs(evaluacion_c) > error and iteracion < max_iter:
        if evaluacion_a * evaluacion_c > 0:
            a = c
            evaluacion_a = evaluar(funcion, a)
            c = b - (evaluacion_b * (b - a)) / (evaluacion_b - evaluacion_a)
            evaluacion_c = evaluar(funcion, c)
            iteracion += 1
            paso = [iteracion, a, b, c, evaluacion_a, evaluacion_b, evaluacion_c]
            pasos.append(paso)
        else:
            b = c
            evaluacion_b = evaluar(funcion, b)
            c = b - (evaluacion_b * (b - a)) / (evaluacion_b - evaluacion_a)
            evaluacion_c = evaluar(funcion, c)
            iteracion += 1
            paso = [iteracion, a, b, c, evaluacion_a, evaluacion_b, evaluacion_c]
            pasos.append(paso)
    tabla = tabulate(pasos, headers="firstrow", floatfmt=".6f", tablefmt="html")
    return c, tabla, iteracion

if __name__ == "__main__":
    funcion = "cos(x)-x"
    intervalo = (0, 1)
    raiz, tabla, iteraciones = falsa_posicion(funcion, intervalo)
    print(f"Raíz aproximada: {raiz}")
    print(f"Iteraciones: {iteraciones}")
    print("Tabla de pasos:")
    print(tabla)
