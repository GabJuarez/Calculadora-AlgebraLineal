from .utils import normalizar_ecuacion, agregar_multiplicacion_implicita
from fractions import Fraction
import ast


def convertir_ecuacion(ecuacion, variables):
    ecuacion = ecuacion.replace(" ", "")
    ecuacion = normalizar_ecuacion(ecuacion)
    ecuacion = agregar_multiplicacion_implicita(ecuacion, variables)
    partes = ecuacion.split("=")
    if len(partes) != 2:
        raise ValueError("La ecuación debe contener un único '='.")

    # Parse left side (variables and coefficients)
    expr_izq = partes[0]
    tree = ast.parse(expr_izq, mode='eval')
    def recolectar(node):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                left = recolectar(node.left)
                right = recolectar(node.right)
                return [l + r for l, r in zip(left[0], right[0])], left[1] + right[1]
            elif isinstance(node.op, ast.Sub):
                left = recolectar(node.left)
                right = recolectar(node.right)
                return [l - r for l, r in zip(left[0], right[0])], left[1] - right[1]
            elif isinstance(node.op, ast.Mult):
                left = recolectar(node.left)
                right = recolectar(node.right)
                if all(x == 0 for x in left[0]):
                    # left is constant
                    return [right[0][i] * left[1] for i in range(len(variables))], right[1] * left[1]
                elif all(x == 0 for x in right[0]):
                    # right is constant
                    return [left[0][i] * right[1] for i in range(len(variables))], left[1] * right[1]
                else:
                    raise ValueError("Multiplicación de variables no soportada")
            elif isinstance(node.op, ast.Div):
                left = recolectar(node.left)
                right = recolectar(node.right)
                if all(x == 0 for x in right[0]):
                    # right is constant
                    return [left[0][i] / right[1] for i in range(len(variables))], left[1] / right[1]
                else:
                    raise ValueError("División de variables entre variables no soportada")
            else:
                raise ValueError("Operación no soportada")
        elif isinstance(node, ast.Num):
            return [Fraction(0)] * len(variables), Fraction(str(node.n))
        elif isinstance(node, ast.Constant):
            return [Fraction(0)] * len(variables), Fraction(str(node.value))
        elif isinstance(node, ast.Name):
            if node.id in variables:
                idx = variables.index(node.id)
                return [Fraction(1) if i == idx else Fraction(0) for i in range(len(variables))], Fraction(0)
            else:
                raise ValueError(f"Variable '{node.id}' no reconocida")
        elif isinstance(node, ast.UnaryOp):
            coef, const = recolectar(node.operand)
            if isinstance(node.op, ast.USub):
                return [-c for c in coef], -const
            elif isinstance(node.op, ast.UAdd):
                return coef, const
            else:
                raise ValueError("Operador unario no soportado")
        else:
            raise ValueError("Expresión no soportada")
    coeficientes, term_indep_izq = recolectar(tree.body)

    # Parse right side (término independiente, puede ser expresión)
    expr_der = partes[1]
    tree_der = ast.parse(expr_der, mode='eval')
    def recolectar_right(node):
        if isinstance(node, ast.BinOp):
            left = recolectar_right(node.left)
            right = recolectar_right(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                return left / right
            else:
                raise ValueError("Operación no soportada")
        elif isinstance(node, ast.Num):
            return Fraction(str(node.n))
        elif isinstance(node, ast.Constant):
            return Fraction(str(node.value))
        elif isinstance(node, ast.UnaryOp):
            val = recolectar_right(node.operand)
            if isinstance(node.op, ast.USub):
                return -val
            elif isinstance(node.op, ast.UAdd):
                return val
            else:
                raise ValueError("Operador unario no soportado")
        elif isinstance(node, ast.Name):
            if node.id in variables:
                idx = variables.index(node.id)
                return Fraction(1) if idx == 0 else Fraction(0)
            else:
                raise ValueError(f"Variable '{node.id}' no reconocida en el lado derecho")
        else:
            raise ValueError("Expresión no soportada")

    def recolectar_right(node):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add):
                left = recolectar_right(node.left)
                right = recolectar_right(node.right)
                return [l + r for l, r in zip(left[0], right[0])], left[1] + right[1]
            elif isinstance(node.op, ast.Sub):
                left = recolectar_right(node.left)
                right = recolectar_right(node.right)
                return [l - r for l, r in zip(left[0], right[0])], left[1] - right[1]
            elif isinstance(node.op, ast.Mult):
                left = recolectar_right(node.left)
                right = recolectar_right(node.right)
                if all(x == 0 for x in left[0]):
                    return [right[0][i] * left[1] for i in range(len(variables))], right[1] * left[1]
                elif all(x == 0 for x in right[0]):
                    return [left[0][i] * right[1] for i in range(len(variables))], left[1] * right[1]
                else:
                    raise ValueError("Multiplicación de variables no soportada")
            elif isinstance(node.op, ast.Div):
                left = recolectar_right(node.left)
                right = recolectar_right(node.right)
                if all(x == 0 for x in right[0]):
                    return [left[0][i] / right[1] for i in range(len(variables))], left[1] / right[1]
                else:
                    raise ValueError("División de variables entre variables no soportada")
            else:
                raise ValueError("Operación no soportada")
        elif isinstance(node, ast.Num):
            return [Fraction(0)] * len(variables), Fraction(str(node.n))
        elif isinstance(node, ast.Constant):
            return [Fraction(0)] * len(variables), Fraction(str(node.value))
        elif isinstance(node, ast.Name):
            if node.id in variables:
                idx = variables.index(node.id)
                return [Fraction(1) if i == idx else Fraction(0) for i in range(len(variables))], Fraction(0)
            else:
                raise ValueError(f"Variable '{node.id}' no reconocida en el lado derecho")
        elif isinstance(node, ast.UnaryOp):
            coef, const = recolectar_right(node.operand)
            if isinstance(node.op, ast.USub):
                return [-c for c in coef], -const
            elif isinstance(node.op, ast.UAdd):
                return coef, const
            else:
                raise ValueError("Operador unario no soportado")
        else:
            raise ValueError("Expresión no soportada")
    coef_der, term_indep_der = recolectar_right(tree_der.body)

    # Mueve todos los términos al lado izquierdo
    coef_final = [a - b for a, b in zip(coeficientes, coef_der)]
    term_indep = term_indep_der - term_indep_izq
    return coef_final + [term_indep]


def crear_matriz(n_incog, variables, ecuaciones):
    matriz = []
    for ecuacion in ecuaciones:
        matriz.append(convertir_ecuacion(ecuacion, variables))
    return matriz, variables


def imprimir_matriz(matriz):
    from fractions import Fraction
    lines = []
    for fila in matriz:
        line = "| " + "  ".join(f"{Fraction(val).limit_denominator()!s:>8}" for val in fila[:-1]) + " || " + f"{Fraction(fila[-1]).limit_denominator()!s:>8} |"
        lines.append(line)
    return "\n".join(lines)


def gauss_jordan(matriz, tolerancia=1e-12):
    n, m = len(matriz), len(matriz[0]) - 1
    fila = 0
    pivotes = []
    procedimiento = []
    from .gauss_jordan import imprimir_matriz
    procedimiento.append("\n--- Proceso Gauss-Jordan ---\nMatriz inicial:")
    procedimiento.append(imprimir_matriz(matriz))

    for col in range(m):
        # Buscar pivote en esta columna
        pivote = None
        for i in range(fila, n):
            if abs(matriz[i][col]) > tolerancia:
                pivote = i
                break
        if pivote is None:
            continue  # columna libre

        # Intercambiar filas si es necesario
        if pivote != fila:
            procedimiento.append(f"Operacion: F{fila+1} ↔ F{pivote+1}")
            matriz[fila], matriz[pivote] = matriz[pivote], matriz[fila]
            procedimiento.append(imprimir_matriz(matriz))

        # Normalizar fila pivote
        piv_val = matriz[fila][col]
        if piv_val != 1:
            procedimiento.append(f"Operacion: F{fila+1} → (1/{piv_val})·F{fila+1}")
        matriz[fila] = [x / piv_val for x in matriz[fila]]
        procedimiento.append(imprimir_matriz(matriz))

        # Eliminar en otras filas
        for i in range(n):
            if i != fila and abs(matriz[i][col]) > tolerancia:
                factor = matriz[i][col]
                if factor != 0:
                    procedimiento.append(f"Operacion: F{i+1} → F{i+1} - ({factor})·F{fila+1}")
                matriz[i] = [a - factor * b for a, b in zip(matriz[i], matriz[fila])]
                procedimiento.append(imprimir_matriz(matriz))

        pivotes.append(col)
        fila += 1
        if fila == n:
            break

    procedimiento.append("\nMatriz final tras Gauss-Jordan:")
    procedimiento.append(imprimir_matriz(matriz))
    return matriz, pivotes, procedimiento


def analizar_solucion(matriz, variables, pivotes, tolerancia=1e-12):
    n, m = len(matriz), len(variables)

    # Detectar inconsistencia
    for fila in matriz:
        if all(abs(x) <= tolerancia for x in fila[:-1]) and abs(fila[-1]) > tolerancia:
            return "inconsistente", None, None

    # Ver si hay variables libres
    libres = [variables[j] for j in range(m) if j not in pivotes]
    if len(pivotes) == m:
        # solución única
        sol = [Fraction(0)] * m
        for i, col in enumerate(pivotes):
            sol[col] = matriz[i][-1]
        return "única", sol, libres
    else:
        return "infinitas", None, libres


def imprimir_resultados(tipo, soluciones, variables, libres, pivotes):
    from fractions import Fraction
    result = []
    result.append("Columnas pivote: " + ", ".join([variables[c] for c in pivotes]))

    if tipo == "inconsistente":
        result.append("➡ El sistema de ecuaciones es inconsistente, no tiene solucion")
    elif tipo == "única":
        result.append("➡ El sistema tiene solucion unica:")
        for var, val in zip(variables, soluciones):
            result.append(f"   {var} = {Fraction(val).limit_denominator()}")
    else:
        result.append("➡ El sistema tiene infinitas soluciones:")
        if libres:
            result.append("Variables libres: " + ", ".join(libres))
        else:
            result.append("no hay variables libres pero faltan restricciones")
    return "\n".join(result)
