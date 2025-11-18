import ast
from typing import Any
from app.logic.utils import transformar_sintaxis, parse_input_number, validar_nodo
from tabulate import tabulate
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


def metodo_tangente(funcion: str, a_input: Any, b_input: Any, tolerancia: float = 0.0001, max_iteraciones: int = 100):
    """
    Implementación del método de la tangente/secante usando:
        c = b - f(b)*(b-a)/(f(b)-f(a))

    Retorna: (raiz_encontrada, tabla_html, iteraciones_usadas, f_en_raiz)
    Tabla columnas: Iteración | a | b | f(a) | f(b) | c | f(c)
    """
    if funcion is None or str(funcion).strip() == "":
        raise ValueError("Función vacía")

    expresion_transformada = transformar_sintaxis(funcion)
    arbol = ast.parse(expresion_transformada, mode="eval")
    validar_nodo(arbol)

    try:
        a = float(parse_input_number(a_input))
        b = float(parse_input_number(b_input))
    except Exception as e:
        raise ValueError(f"Intervalo inválido: {e}")

    x_sym = sp.symbols('x')
    try:
        local_dict = {'e': sp.E, 'pi': sp.pi, 'ln': sp.log}
        sympy_expr = parse_expr(expresion_transformada, local_dict=local_dict)
        sympy_deriv = sp.diff(sympy_expr, x_sym)  # no usado pero útil si se necesita
        f_num = sp.lambdify(x_sym, sympy_expr, modules=["math"])
    except Exception as e:
        raise ValueError("No se pudo procesar la expresión con SymPy. Revise la sintaxis de la función. Detalle: " + str(e))

    # Cabecera: Iteración | a | b | f(a) | f(b) | c | f(c)
    tabla_pasos = [["Iteración", "a", "b", "f(a)", "f(b)", "c", "f(c)"]]

    def formatear_num(v, decimales=6):
        try:
            n = float(v)
        except Exception:
            return str(v)
        if n != n:
            return 'NaN'
        return f"{n:.{decimales}f}"

    iteracion = 0

    # evaluar f(a) y f(b) inicialmente
    try:
        fa = float(f_num(a))
    except Exception:
        fa = float('nan')
    try:
        fb = float(f_num(b))
    except Exception:
        fb = float('nan')

    # ciclo principal: secante (se actualizan a <- b, b <- c)
    raiz = None
    f_en_raiz = float('nan')

    while iteracion < max_iteraciones:
        denom = (fb - fa)
        if abs(denom) < 1e-15:
            raise ValueError(f"Denominador cercano a cero en iteración {iteracion}. f(b)-f(a) ≈ 0")

        # formula: c = b - f(b)*(b-a)/(f(b)-f(a))
        c = b - fb * (b - a) / denom

        try:
            fc = float(f_num(c))
        except Exception:
            fc = float('nan')

        # registrar paso
        fila = [str(iteracion + 1), formatear_num(a), formatear_num(b), formatear_num(fa), formatear_num(fb), formatear_num(c), formatear_num(fc)]
        tabla_pasos.append(fila)

        iteracion += 1

        # condición de paro: |f(c)| pequeño o cambio en c respecto a b pequeño
        if (isinstance(fc, float) and abs(fc) <= float(tolerancia)) or abs(c - b) <= float(tolerancia):
            raiz = c
            try:
                f_en_raiz = format(float(fc) if isinstance(fc, (int, float)) else float('nan'), '.3f')
            except Exception:
                f_en_raiz = str(float('nan'))
            break

        # actualizar para siguiente iteración: secante actualiza (a,b) -> (b,c)
        a, fa = b, fb
        b, fb = c, fc

    if raiz is None:
        # si no convergió, tomar última aproximación b
        raiz = b
        try:
            f_en_raiz = format(float(fb) if isinstance(fb, (int, float)) else float('nan'), '.3f')
        except Exception:
            f_en_raiz = str(float('nan'))

    tabla_html = tabulate(tabla_pasos, headers="firstrow", tablefmt="html")

    return raiz, tabla_html, iteracion, f_en_raiz


if __name__ == "__main__":
    raiz, tabla, it, fc = metodo_tangente("x**3 - x - 2", 1.0, 2.0)
    print(raiz, it, fc)
