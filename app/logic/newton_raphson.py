import ast
from typing import Any
from app.logic.utils import transformar_sintaxis, parse_input_number, validar_nodo
from tabulate import tabulate
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


def newton_raphson(funcion: str, valor_inicial_input: Any, tolerancia: float = 0.0001, max_iteraciones: int = 100):
    """
    Implementación del método de Newton-Raphson usando SymPy para la derivada simbólica.

    Retorna: (raiz_encontrada, tabla_html, iteraciones_usadas, f_en_raiz)
    La tabla está en el orden: Iteración | xi | f(xi) | f'(xi) | xi+1
    """
    if funcion is None or str(funcion).strip() == "":
        raise ValueError("Función vacía")

    expresion_transformada = transformar_sintaxis(funcion)
    arbol = ast.parse(expresion_transformada, mode="eval")
    validar_nodo(arbol)

    # convertir valor inicial
    try:
        valor_inicial = parse_input_number(valor_inicial_input)
    except Exception as e:
        raise ValueError(f"Valor inicial inválido: {e}")

    # Preparar SymPy para derivada simbólica y funciones numéricas rápidas
    x_sym = sp.symbols('x')
    try:
        # permitir que el usuario use 'e', 'pi' y 'ln' en la entrada (ej: e^x, ln(x))
        local_dict = {'e': sp.E, 'pi': sp.pi, 'ln': sp.log}
        # parse_expr permite pasar local_dict de forma segura
        sympy_expr = parse_expr(expresion_transformada, local_dict=local_dict)
        sympy_deriv = sp.diff(sympy_expr, x_sym)
        # Usar módulos compatibles con funciones matemáticas; math está bien para escala escalar
        f_num = sp.lambdify(x_sym, sympy_expr, modules=["math"])
        fprime_num = sp.lambdify(x_sym, sympy_deriv, modules=["math"])
    except Exception as e:
        # devolver detalle del error para facilitar el debug en el frontend
        raise ValueError("No se pudo procesar la expresión con SymPy. Revise la sintaxis de la función. Detalle: " + str(e))

    # Cabecera solicitada: Iteración | xi | f(xi) | f'(xi) | xi+1
    tabla_pasos = [["Iteración", "xi", "f(xi)", "f'(xi)", "xi+1"]]

    # helper: formatea número con signo y n decimales; maneja NaN
    def formato_numero(valor, decimales=4):
        try:
            v = float(valor)
        except Exception:
            return str(valor)
        if v != v:  # NaN
            return 'NaN'
        fmt = f"{{:+.{decimales}f}}"
        return fmt.format(v)

    iteracion = 0
    x_actual = float(valor_inicial)

    # evaluar f en el punto inicial
    try:
        f_actual = float(f_num(x_actual))
    except Exception:
        raise ValueError("Error al evaluar la función en el valor inicial.")

    tolerancia_val = float(tolerancia)

    while iteracion < max_iteraciones:
        try:
            derivada = float(fprime_num(x_actual))
        except Exception:
            raise ValueError("Error al evaluar la derivada simbólica en el punto actual.")

        if abs(derivada) < 1e-12:
            raise ValueError(f"Derivada cercana a cero en iteración {iteracion}. El método puede fallar o diverger.")

        x_siguiente = x_actual - f_actual / derivada

        # Añadir fila: iteración, xi, f(xi), f'(xi), xi+1
        fila = [f"+{iteracion + 1}", formato_numero(x_actual), formato_numero(f_actual), formato_numero(derivada), formato_numero(x_siguiente)]
        tabla_pasos.append(fila)

        # evaluar f en el nuevo punto
        try:
            f_siguiente = float(f_num(x_siguiente))
        except Exception:
            f_siguiente = float('nan')

        iteracion += 1

        diferencia = abs(x_siguiente - x_actual)
        # condición de paro: f(x_siguiente) pequeño o cambio pequeño en x
        if (isinstance(f_siguiente, float) and abs(f_siguiente) <= tolerancia_val) or diferencia <= tolerancia_val:
            x_actual = x_siguiente
            f_actual = f_siguiente
            break

        # preparar siguiente iteración
        x_actual = x_siguiente
        f_actual = f_siguiente

    # Generar tabla HTML (las celdas ya están formateadas como strings)
    tabla_html = tabulate(tabla_pasos, headers="firstrow", tablefmt="html")
    raiz_encontrada = x_actual
    f_en_raiz = round(float(f_actual) if isinstance(f_actual, (int, float)) else float('nan'), 5)

    return raiz_encontrada, tabla_html, iteracion, f_en_raiz


if __name__ == "__main__":
    raiz, tabla, iteraciones, f_en_raiz = newton_raphson("x^3 - x - 2", 1.5)
    print(f_en_raiz)
