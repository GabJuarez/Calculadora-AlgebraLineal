import re
import unicodedata
from fractions import Fraction
import ast


def normalizar_ecuacion(ecuacion: str) -> str:
    # Normaliza los caracteres de acuerdo a la normalizacion NFKC de unicode
    ecuacion = unicodedata.normalize("NFKC", ecuacion)

    # Caracteres especiales a normalizar
    reemplazos = {"−": "-", "×": "*", "÷": "/", "⁺": "+", "⁻": "-", "∙": "*", "⋅": "*"}
    ecuacion = re.sub(r"[\u200B\u200C\u200D\u2060]", "", ecuacion)

    for old, new in reemplazos.items():
        # se reemplazan caracteres especiales (si los hay) por caracteres normalizados
        ecuacion = ecuacion.replace(old, new)

    return ecuacion.strip()


def evaluar_lado(expr, variables):
    tree = ast.parse(expr, mode='eval')
    coef = {v: Fraction(0) for v in variables}
    const = Fraction(0)

    class Visitor(ast.NodeVisitor):
        def visit_BinOp(self, node):
            left_coef, left_const = self.visit(node.left)
            right_coef, right_const = self.visit(node.right)
            if isinstance(node.op, ast.Add):
                return (
                    {v: left_coef[v] + right_coef[v] for v in variables},
                    left_const + right_const
                )
            elif isinstance(node.op, ast.Sub):
                return (
                    {v: left_coef[v] - right_coef[v] for v in variables},
                    left_const - right_const
                )
            elif isinstance(node.op, ast.Mult):
                if all(v == 0 for v in right_coef.values()):
                    # right is constant
                    return (
                        {v: left_coef[v] * right_const for v in variables},
                        left_const * right_const
                    )
                elif all(v == 0 for v in left_coef.values()):
                    # left is constant
                    return (
                        {v: right_coef[v] * left_const for v in variables},
                        right_const * left_const
                    )
                else:
                    raise ValueError("Multiplicación de variables no soportada")
            elif isinstance(node.op, ast.Div):
                if all(v == 0 for v in right_coef.values()):
                    # right is constant
                    return (
                        {v: left_coef[v] / right_const for v in variables},
                        left_const / right_const
                    )
                else:
                    raise ValueError("División de variables entre variables no soportada")
            else:
                raise ValueError("Operación no soportada")

        def visit_Num(self, node):
            return ({v: Fraction(0) for v in variables}, Fraction(node.n))

        def visit_Constant(self, node):
            return ({v: Fraction(0) for v in variables}, Fraction(node.value))

        def visit_Name(self, node):
            if node.id in variables:
                return ({v: Fraction(1) if v == node.id else Fraction(0) for v in variables}, Fraction(0))
            else:
                raise ValueError(f"Variable '{node.id}' no reconocida")

        def visit_UnaryOp(self, node):
            coef, const = self.visit(node.operand)
            if isinstance(node.op, ast.USub):
                return ({v: -coef[v] for v in variables}, -const)
            elif isinstance(node.op, ast.UAdd):
                return (coef, const)
            else:
                raise ValueError("Operador unario no soportado")

        def generic_visit(self, node):
            raise ValueError("Expresión no soportada")

    visitor = Visitor()
    coef, const = visitor.visit(tree.body)
    return coef, const


def agregar_multiplicacion_implicita(ecuacion, variables):
    # Inserta * entre número y variable (ej: 30x -> 30*x)
    for var in variables:
        # Busca patrones como 30x, -5y, 2.5z, etc.
        ecuacion = re.sub(rf'(?<![\w])([\d\.]+)({var})(?![\w])', r'\1*\2', ecuacion)
    return ecuacion


def convertir_ecuacion(ecuacion, variables):
    ecuacion = ecuacion.replace(" ", "")
    ecuacion = normalizar_ecuacion(ecuacion)
    ecuacion = agregar_multiplicacion_implicita(ecuacion, variables)
    partes = ecuacion.split("=")
    if len(partes) != 2:
        raise ValueError("La ecuación debe contener un único signo '='.")

    coef_izq, const_izq = evaluar_lado(partes[0], variables)
    coef_der, const_der = evaluar_lado(partes[1], variables)

    # Mueve todos los términos al lado izquierdo
    coef_final = [coef_izq[v] - coef_der[v] for v in variables]
    term_indep = const_der - const_izq

    return coef_final + [term_indep]


def crear_matriz():
    while True:
        try:
            n_incog = int(input("Ingrese el numero de incognitas: "))
            if n_incog <= 0:
                print("El numero de incógnitas debe ser mayor a cero.")
                continue
            break
        except ValueError:
            print("Debe ingresar un número entero.")

    while True:
        variables = input(
            "Ingrese las incognitas (separadas por espacios, ej: x y z): "
        ).split()
        if len(variables) != n_incog:
            print(f"Debe ingresar exactamente {n_incog} variables.")
            continue
        if len(set(variables)) != n_incog:
            print("Las variables no deben repetirse.")
            continue
        break

    matriz = []
    print("Ingrese cada ecuacion")
    for i in range(n_incog):
        while True:
            ecuacion = input(f"Ecuacion {i + 1}: ")
            if not ecuacion.strip():
                print("La ecuacion no puede estar vacia.")
                continue
            try:
                fila = convertir_ecuacion(ecuacion, variables)
                matriz.append(fila)
                break
            except Exception as e:
                print(f"Error en la ecuacion: {e}")
    return matriz, variables


def eliminacion_filas(matriz, tolerancia=1e-12):
    n = len(matriz)

    # Eliminacion hacia adelante
    for i in range(n):
        pivote = matriz[i][i]
        if abs(pivote) <= tolerancia:
            for k in range(i + 1, n):
                if abs(matriz[k][i]) > tolerancia:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    pivote = matriz[i][i]
                    break
            else:
                raise ValueError("Sistema sin solucion unica")

        for j in range(i, n + 1):
            matriz[i][j] /= pivote

        print(f"\nOperacion: F{i + 1} -> 1/{pivote} * F{i + 1}")
        for fila in matriz:
            print(
                " | ".join(
                    f"{f.numerator}/{f.denominator}"
                    if f.denominator != 1
                    else f"{f.numerator}"
                    for f in fila
                )
            )

        for k in range(i + 1, n):
            factor = matriz[k][i]
            for j in range(i, n + 1):
                matriz[k][j] -= factor * matriz[i][j]

            if abs(factor) > tolerancia:
                print(f"\nOperacion: F{k + 1} -> F{k + 1} - ({factor}) * F{i + 1}")
                for fila in matriz:
                    print(
                        " | ".join(
                            f"{f.numerator}/{f.denominator}"
                            if f.denominator != 1
                            else f"{f.numerator}"
                            for f in fila
                        )
                    )

    # Sustitución hacia atras
    soluciones = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        soluciones[i] = matriz[i][n]  # termino independiente
        operaciones = []
        for j in range(i + 1, n):
            operaciones.append(f"{matriz[i][j]}*{soluciones[j]}")
            soluciones[i] -= matriz[i][j] * soluciones[j]

        # impresion de los pasos de sustitucion al tener la matriz triangular
        if operaciones:
            print(
                f"\nSustitucion para variable {i + 1}: {matriz[i][n]} - ({' + '.join(operaciones)}) = {soluciones[i]}"
            )
        else:
            print(
                f"\nSustitucion para variable {i + 1}: {soluciones[i]} (sin otras variables)"
            )

    return soluciones


def imprimir_soluciones(soluciones, variables):
    print("\nSolucion del sistema:")
    for i, j in zip(variables, soluciones):
        print(f"{i} = {j}")


if __name__ == "__main__":
    matriz, variables = crear_matriz()
    soluciones = eliminacion_filas(matriz)
    imprimir_soluciones(soluciones, variables)
