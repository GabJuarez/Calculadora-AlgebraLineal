from .utils import normalizar_ecuacion, agregar_multiplicacion_implicita
from fractions import Fraction
import ast


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


def crear_matriz(n_incog, variables, ecuaciones):
    matriz = []
    for ecuacion in ecuaciones:
        fila = convertir_ecuacion(ecuacion, variables)
        matriz.append(fila)
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

        # Eliminacion en otras filas
        for k in range(i + 1, n):
            factor = matriz[k][i]
            for j in range(i, n + 1):
                matriz[k][j] -= factor * matriz[i][j]

    # Sustitución hacia atras
    soluciones = [Fraction(0)] * n
    for i in range(n - 1, -1, -1):
        soluciones[i] = matriz[i][n]
        for j in range(i + 1, n):
            soluciones[i] -= matriz[i][j] * soluciones[j]

    return soluciones


def imprimir_soluciones(soluciones, variables):
    lines = []
    lines.append("Solucion del sistema:")
    for i, j in zip(variables, soluciones):
        lines.append(f"{i} = {j}")
    return "\n".join(lines)
