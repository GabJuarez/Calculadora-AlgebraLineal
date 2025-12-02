from typing import List, Tuple, Dict, Any
from app.logic.utils import transformar_sintaxis
from sympy import symbols, sympify, Poly, factor, N
from sympy import SympifyError

x = symbols('x')


def todas_las_raices(funcion: str, solo_reales: bool = False, max_degree: int = 80) -> Tuple[List[Dict[str, Any]], List[Any], str, int]:
    """
    Dada una cadena que representa un polinomio en x devuelve todas sus raíces y una lista
    de pasos explicativos para mostrarse en la UI.

    Retorna: (raices, pasos, factorizacion_str, grado)
      - raices: lista de dicts con keys: 'exact' (str), 'approx' (str), 'multiplicity' (int), 'is_real' (bool)
      - pasos: lista de pasos (pueden ser strings o tuplas (texto, datos))
      - factorizacion_str: string de la factorización simbólica
      - grado: grado del polinomio (int)
    """
    pasos = []
    if not funcion or not str(funcion).strip():
        raise ValueError("Función vacía")

    expr_str = transformar_sintaxis(funcion)
    pasos.append(("Entrada transformada", expr_str))

    try:
        expr = sympify(expr_str)
    except SympifyError as e:
        raise ValueError(f"Sintaxis inválida: {e}")

    # validar que sólo tiene la variable x
    simb = expr.free_symbols
    if any(s for s in simb if s != x):
        raise ValueError("La expresión contiene símbolos distintos de 'x'. Ingrese un polinomio en x.")

    try:
        poly = Poly(expr, x)
    except Exception:
        raise ValueError("No se pudo interpretar la expresión como un polinomio en x")

    grado = poly.degree()
    pasos.append((f"Polinomio canónico (grado {grado})", str(poly.as_expr())))

    if grado < 1:
        raise ValueError("La expresión no es un polinomio de grado al menos 1")

    if grado > max_degree:
        raise ValueError(f"Polinomio de grado muy alto ({grado}). Límite permitido: {max_degree} para evitar cálculos costosos.")

    # coeficientes
    coef = poly.all_coeffs()
    pasos.append(("Coeficientes (de mayor a menor grado)", [str(c) for c in coef]))

    # factorización simbólica
    try:
        fact = factor(poly.as_expr())
        fact_str = str(fact)
    except Exception:
        fact_str = str(poly.as_expr())
    pasos.append(("Factorización simbólica (si es posible)", fact_str))

    # raíces numéricas
    try:
        numeric_roots = poly.nroots()
    except Exception as e:
        raise ValueError(f"No se pudieron calcular las raíces: {e}")

    # agrupar raíces cercanas para determinar multiplicidad
    clusters = []
    tol = 1e-8
    for r in numeric_roots:
        r_approx = complex(N(r))
        found = False
        for cl in clusters:
            if abs(r_approx - cl['approx']) < tol:
                cl['multiplicity'] += 1
                cl['vals'].append(r)
                found = True
                break
        if not found:
            clusters.append({'approx': r_approx, 'multiplicity': 1, 'vals': [r]})

    raices = []
    reales = 0
    complejas = 0
    for cl in clusters:
        is_real = abs(cl['approx'].imag) < 1e-12
        if is_real:
            reales += 1
        else:
            complejas += 1
        # intentar presentar una forma exacta si es posible tomando la primera representación simbólica
        exact_repr = str(cl['vals'][0])
        # aproximación con 8 decimales para presentación
        approx_repr = f"{cl['approx'].real:.8f}" if is_real else f"{cl['approx'].real:.8f}{'+' if cl['approx'].imag>=0 else ''}{cl['approx'].imag:.8f}i"
        raices.append({
            'exact': exact_repr,
            'approx': approx_repr,
            'multiplicity': cl['multiplicity'],
            'is_real': bool(is_real)
        })

    pasos.append(("Raíces encontradas (aproximación y multiplicidad)", raices))

    resumen = f"Resumen: grado={grado}, raíces reales={reales}, raíces complejas={complejas}"
    pasos.append((resumen, None))

    # filtrar si el usuario pidió solo reales
    if solo_reales:
        raices = [r for r in raices if r['is_real']]

    # ordenar: reales primero, por valor
    def _sort_key(r):
        # convierte la representación en string a partes numéricas para ordenar
        try:
            s = r.get('approx', '0')
            if isinstance(s, str) and 'i' in s:
                comp = complex(s.replace('i', 'j'))
            else:
                comp = complex(float(s))
        except Exception:
            comp = complex(0)
        return (not r.get('is_real', False), comp.real, comp.imag)

    raices.sort(key=_sort_key)

    return raices, pasos, fact_str, grado


if __name__ == '__main__':
    # pequeño test local
    r, p, f, g = todas_las_raices('x^3 - x - 2')
    print('Grado:', g)
    print('Factor:', f)
    for x in r:
        print(x)
