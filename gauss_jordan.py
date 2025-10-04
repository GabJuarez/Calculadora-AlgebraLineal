import re
import unicodedata
from fractions import Fraction
import ast


def normalizar_ecuacion(ecuacion: str) -> str:
    ecuacion = unicodedata.normalize("NFKC", ecuacion)
    reemplazos = {"−": "-", "×": "*", "÷": "/", "⁺": "+", "⁻": "-", "∙": "*", "⋅": "*"}
    ecuacion = re.sub(r"[\u200B\u200C\u200D\u2060]", "", ecuacion)
    for viejo, nuevo in reemplazos.items():
        ecuacion = ecuacion.replace(viejo, nuevo)
    return ecuacion.strip()


def agregar_multiplicacion_implicita(ecuacion, variables):
    # Inserta * entre número y variable (ej: 0.8x -> 0.8*x)
    for var in variables:
        ecuacion = re.sub(rf'(?<![\w])([\d\.]+)({var})(?![\w])', r'\1*\2', ecuacion)
    return ecuacion


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


def crear_matriz():
    n_incog = int(input("Ingrese el número de incógnitas: "))
    variables = input("Ingrese las incógnitas (ej: x y z): ").split()
    matriz = []
    print("Ingrese cada ecuación:")
    for i in range(n_incog):
        while True:
            ecuacion = input(f"Ecuación {i+1}: ")
            try:
                matriz.append(convertir_ecuacion(ecuacion, variables))
                break
            except Exception as e:
                print(f"Error en la ecuación: {e}")
    return matriz, variables


def imprimir_matriz(matriz):
    for fila in matriz:
        print("| " + "  ".join(f"{val!s:>5}" for val in fila[:-1]) + " || " + f"{fila[-1]!s:>5} |")
    print()


def gauss_jordan(matriz, tolerancia=1e-12):
    n, m = len(matriz), len(matriz[0]) - 1
    fila = 0
    pivotes = []

    print("\n--- Proceso Gauss-Jordan ---\nMatriz inicial:")
    imprimir_matriz(matriz)

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
            print(f"Operacion: F{fila+1} ↔ F{pivote+1}")
            matriz[fila], matriz[pivote] = matriz[pivote], matriz[fila]
            imprimir_matriz(matriz)

        # Normalizar fila pivote
        piv_val = matriz[fila][col]
        if piv_val != 1:
            print(f"Operacion: F{fila+1} → (1/{piv_val})·F{fila+1}")
        matriz[fila] = [x / piv_val for x in matriz[fila]]
        imprimir_matriz(matriz)

        # Eliminar en otras filas
        for i in range(n):
            if i != fila and abs(matriz[i][col]) > tolerancia:
                factor = matriz[i][col]
                if factor != 0:
                    print(f"Operacion: F{i+1} → F{i+1} - ({factor})·F{fila+1}")
                matriz[i] = [a - factor * b for a, b in zip(matriz[i], matriz[fila])]
                imprimir_matriz(matriz)

        pivotes.append(col)
        fila += 1
        if fila == n:
            break

    return matriz, pivotes


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
    print("\nResultado del sistema de ecuaciones:")
    print("Columnas pivote:", [variables[c] for c in pivotes])

    if tipo == "inconsistente":
        print("➡ El sistema de ecuaciones es inconsistente, no tiene solucion")
    elif tipo == "única":
        print("➡ El sistema tiene solucion unica:")
        for var, val in zip(variables, soluciones):
            print(f"   {var} = {val}")
    else:
        print("➡ El sistema tiene infinitas soluciones:")
        if libres:
            print("Variables libres:", ", ".join(libres))
        else:
            print("no hay variables libres pero faltan restricciones")


if __name__ == "__main__":
    matriz, variables = crear_matriz()
    matriz, pivotes = gauss_jordan(matriz)
    tipo, soluciones, libres = analizar_solucion(matriz, variables, pivotes)
    imprimir_resultados(tipo, soluciones, variables, libres, pivotes)
