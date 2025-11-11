from flask import Blueprint, render_template, request, jsonify
from app import (gauss_jordan, resolver_cramer, gauss_jordan_pasos,
                 eliminacion_gaussiana, matriz_desde_formulario, traspuesta,
                 matriz_triangular,calcular_determinante, biseccion)
from app.logic.operaciones_matrices import operar_matrices
import re

routes_bp = Blueprint('routes_bp', __name__)

def validar_matriz(matriz):
    """
    Valida que todos los elementos de la matriz sean enteros, decimales o fracciones tipo a/b
    Devuelve True si es valida, de lo contrario lanza una excepcion
    """
    regex = re.compile(r'^-?\d+$|^-?\d+\.\d+$|^-?\d+/\d+$')
    for fila in matriz:
        for val in fila:
            # Si es int o float, es valido
            if isinstance(val, (int, float)):
                continue
            val_str = str(val).strip().replace(' ', '')
            if not val_str or not regex.fullmatch(val_str):
                raise ValueError(f"Todos los elementos deben ser números o fracciones. Valor inválido: '{val}'")
    return True

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/cramer', methods=['GET', 'POST'])
def cramer_view():
    resultado = None
    error = None
    pasos = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            soluciones, det_A, determinantes, pasos = resolver_cramer([fila[:-1] for fila in matriz], [fila[-1] for fila in matriz])
            resultado = {
                'soluciones': soluciones,
                'det_A': det_A,
                'determinantes': determinantes
            }
        except Exception as e:
            error = str(e)
    return render_template('cramer.html', resultado=resultado, error=error, pasos=pasos)

@routes_bp.route('/gauss_jordan', methods=['GET', 'POST'])
def gauss_jordan_view():
    resultado = None
    error = None
    pasos = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            matriz_reducida, soluciones, pasos = gauss_jordan(matriz)
            resultado = {'matriz_reducida': matriz_reducida, 'soluciones': soluciones}
        except Exception as e:
            error = str(e)
    return render_template('gauss_jordan.html', resultado=resultado, error=error, pasos=pasos)

@routes_bp.route('/matriz_inversa', methods=['GET', 'POST'])
def matriz_inversa_view():
    resultado = None
    error = None
    pasos = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            inversa, pasos = gauss_jordan_pasos(matriz)
            resultado = {'inversa': inversa}
        except Exception as e:
            error = str(e)
    return render_template('matriz_inversa.html', resultado=resultado, error=error, pasos=pasos)

@routes_bp.route('/eliminacion_gaussiana', methods=['GET', 'POST'])
def eliminacion_gaussiana_view():
    matriz_triangular = None
    soluciones = None
    pasos = None
    error = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            matriz_triangular, soluciones, pasos = eliminacion_gaussiana(matriz)

        except Exception as e:
            error  = str(e)
    return render_template('eliminacion_gaussiana.html', matriz_triangular=matriz_triangular, soluciones=soluciones, pasos=pasos, error=error)

@routes_bp.route('/traspuesta', methods=['GET', 'POST'])
def traspuesta_view():
    matriz_traspuesta = None
    pasos = None
    error = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            matriz_traspuesta, pasos = traspuesta(matriz)
        except Exception as e:
            error = str(e)
    return render_template('traspuesta.html', matriz_traspuesta=matriz_traspuesta, pasos=pasos, error=error)

@routes_bp.route('/determinante', methods=['GET', 'POST'])
def determinante_view():
    triangular = None
    pasos_triangular = None
    determinante = None
    pasos_determinante = None
    error = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            triangular, pasos_triangular = matriz_triangular(matriz)
            determinante, pasos_determinante = calcular_determinante(matriz)
        except Exception as e:
            error = str(e)
    return render_template('determinante.html', triangular=triangular,
                           pasos_triangular=pasos_triangular, determinante=determinante,
                           pasos_determinante=pasos_determinante, error=error)

@routes_bp.route('/informacion')
def informacion_view():
    return render_template('informacion.html')

@routes_bp.route('/sistemas')
def sistemas_view():
    return render_template('sistemas.html')

@routes_bp.route('/independencia_lineal', methods=['GET', 'POST'])
def independencia_lineal():
    resultado = None
    pasos = []
    error = None
    if request.method == 'POST':
        try:
            matriz = matriz_desde_formulario(request)
            validar_matriz(matriz)
            from app.logic.independencia_lineal import comprobar_independencia_lineal
            matriz_reducida_str, resultado_str, pasos_str = comprobar_independencia_lineal(matriz)
            resultado = {
                'matriz_reducida': matriz_reducida_str,
                'resultado': resultado_str
            }
            pasos = pasos_str
        except Exception as e:
            error = str(e)
        pass
    return render_template('independencia_lineal.html', resultado=resultado, pasos=pasos, error=error)

@routes_bp.route('/operaciones_matrices', methods=['GET', 'POST'])
def operaciones_matrices_view():
    resultado = None
    pasos = []
    error = None
    if request.method == 'POST':
        try:
            # Leer datos del formulario
            filas_a = int(request.form['filas_a'])
            columnas_a = int(request.form['columnas_a'])
            filas_b = int(request.form['filas_b'])
            columnas_b = int(request.form['columnas_b'])
            escalar_a = request.form.get('escalar_a', None)
            escalar_b = request.form.get('escalar_b', None)
            operacion = request.form.get('operacion', 'suma')
            # Leer matrices
            def leer_matriz(prefix, filas, columnas):
                matriz = []
                for i in range(filas):
                    fila = []
                    for j in range(columnas):
                        val = request.form.get(f"{prefix}_{i}_{j}", '0')
                        try:
                            fila.append(float(val))
                        except Exception:
                            fila.append(0)
                    matriz.append(fila)
                return matriz
            matriz_a = leer_matriz('matriz_a', filas_a, columnas_a)
            matriz_b = leer_matriz('matriz_b', filas_b, columnas_b)
            # Ejecutar operación
            res = operar_matrices(matriz_a, matriz_b, escalar_a, escalar_b, operacion)
            resultado = res['resultado']
            pasos = res['pasos']
        except Exception as e:
            error = str(e)
    return render_template('operaciones_matrices.html', resultado=resultado, pasos=pasos, error=error)

@routes_bp.route('/biseccion', methods=['GET', 'POST'])
def biseccion_view():
    resultado = None
    error = None
    pasos = None
    plot_data = None
    funcion = ''
    limite_inferior = ''
    limite_superior = ''
    if request.method == 'POST':
        try:
            # If client submitted a preview image, reuse it instead of regenerating
            preview_image_b64 = request.form.get('preview_image', '')
            funcion = request.form.get('funcion', '').strip()
            limite_inferior = request.form.get('limite_inferior', '').strip()
            limite_superior = request.form.get('limite_superior', '').strip()

            if preview_image_b64:
                # Client provided a PNG base64 for preview; use it directly
                plot_data = preview_image_b64
                # If limits are empty, try to detect a good interval for the algorithm by sampling
                if not limite_inferior or not limite_superior:
                    try:
                        from app.logic.biseccion import evaluar
                        # sample across a wide range and look for sign change
                        import math
                        a = -10.0
                        b = 10.0
                        n = 800
                        xs = [a + i*(b-a)/(n-1) for i in range(n)]
                        ys = []
                        for x in xs:
                            try:
                                ys.append(evaluar(funcion, x))
                            except Exception:
                                ys.append(float('nan'))
                        crossing = None
                        for i in range(n-1):
                            y1 = ys[i]
                            y2 = ys[i+1]
                            if not (isinstance(y1, float) and isinstance(y2, float)):
                                continue
                            if math.isnan(y1) or math.isnan(y2):
                                continue
                            if y1 * y2 <= 0:
                                frac = abs(y1) / (abs(y1) + abs(y2)) if (abs(y1) + abs(y2)) != 0 else 0.5
                                crossing = xs[i] + (xs[i+1]-xs[i]) * frac
                                break
                        if crossing is not None:
                            limite_inferior = str(crossing - 2)
                            limite_superior = str(crossing + 2)
                        else:
                            # fallback small default interval
                            limite_inferior = '-1'
                            limite_superior = '1'
                    except Exception:
                        limite_inferior = '-1'
                        limite_superior = '1'
            else:
                from io import BytesIO
                import base64
                import matplotlib
                matplotlib.use('Agg')
                import matplotlib.pyplot as plt
                from app.logic.biseccion import evaluar
                from app.logic.utils import parse_input_number

                # Parse endpoints using parse_input_number (accepts fractions, ln, etc.)
                a = parse_input_number(limite_inferior)
                b = parse_input_number(limite_superior)

                # Generate plot data sampling the function between a and b
                xs = []
                ys = []
                # If a == b, expand a bit for plotting
                if a == b:
                    a -= 1
                    b += 1
                n_points = 401
                for i in range(n_points):
                    x = a + i * (b - a) / (n_points - 1)
                    xs.append(x)
                    try:
                        y = evaluar(funcion, x)
                    except Exception:
                        y = float('nan')
                    ys.append(y)

                fig, ax = plt.subplots(figsize=(6, 3.5))
                ax.axhline(0, color='black', linewidth=0.8)
                ax.plot(xs, ys, color='C0')
                ax.set_xlabel('x')
                ax.set_ylabel('f(x)')
                ax.grid(True, linestyle=':', linewidth=0.6)
                fig.tight_layout()
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100)
                plt.close(fig)
                buf.seek(0)
                plot_data = base64.b64encode(buf.read()).decode('ascii')

            # Run bisection algorithm (uses internal parsing/evaluador)
            raiz, tabla, iteraciones = biseccion(funcion, (limite_inferior, limite_superior))
            resultado = {'raiz': raiz, 'tabla': tabla, 'iteraciones': iteraciones}
        except Exception as e:
            error = str(e)
    return render_template('biseccion.html', resultado=resultado, error=error, pasos=pasos,
                           funcion=funcion, limite_inferior=limite_inferior, limite_superior=limite_superior,
                           plot_data=plot_data)

@routes_bp.route('/biseccion/preview', methods=['POST'])
def biseccion_preview():
    """Genera un PNG base64 con el gráfico de la función entre los límites proporcionados.
    Devuelve JSON: { plot_data: 'base64...' } o { error: 'mensaje' }.
    """
    try:
        from io import BytesIO
        import base64
        import math
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from app.logic.biseccion import evaluar
        from app.logic.utils import parse_input_number

        funcion = request.form.get('funcion', '').strip()
        limite_inferior = request.form.get('limite_inferior', '').strip()
        limite_superior = request.form.get('limite_superior', '').strip()
        if not funcion:
            return jsonify({'error': 'Función vacía'}), 400

        # If limits not provided or empty, use a default sampling and try to detect crossing
        a = None
        b = None
        try:
            if limite_inferior != '':
                a = parse_input_number(limite_inferior)
            if limite_superior != '':
                b = parse_input_number(limite_superior)
        except Exception as e:
            return jsonify({'error': f'Error en los límites: {e}'}), 400

        # Default sampling range
        if a is None or b is None or a == b:
            # initial range
            a = -5.0 if a is None else a
            b = 5.0 if b is None else b

        # Sample and try to find crossing; if crossing found and original limits were empty, zoom and resample
        n_points = 800
        xs = [a + i * (b - a) / (n_points - 1) for i in range(n_points)]
        ys = []
        for x in xs:
            try:
                ys.append(evaluar(funcion, x))
            except Exception:
                ys.append(float('nan'))

        # detect first sign change
        crossing = None
        for i in range(len(xs)-1):
            y1 = ys[i]
            y2 = ys[i+1]
            if not (isinstance(y1, float) and isinstance(y2, float)):
                continue
            if math.isnan(y1) or math.isnan(y2):
                continue
            if y1 * y2 <= 0:
                # linear interpolate
                try:
                    frac = abs(y1) / (abs(y1) + abs(y2)) if (abs(y1) + abs(y2)) != 0 else 0.5
                    crossing = xs[i] + (xs[i+1] - xs[i]) * frac
                    break
                except Exception:
                    crossing = xs[i]
                    break

        if crossing is not None and (request.form.get('limite_inferior','') == '' or request.form.get('limite_superior','') == ''):
            # zoom around crossing
            a = crossing - 2
            b = crossing + 2
            xs = [a + i * (b - a) / (n_points - 1) for i in range(n_points)]
            ys = []
            for x in xs:
                try:
                    ys.append(evaluar(funcion, x))
                except Exception:
                    ys.append(float('nan'))

        # create the plot
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.axhline(0, color='black', linewidth=0.8)
        ax.plot(xs, ys, color='#1f77b4', linewidth=1.8)
        # if crossing is not None:
        #     ax.axvline(crossing, color='#ff7f0e', linestyle='--', linewidth=1.2)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True, linestyle=':', linewidth=0.6, color='#444')
        ax.set_facecolor('#1a1c2a')
        fig.patch.set_facecolor('#101216')
        # style ticks/labels light
        ax.tick_params(colors='#dbeafe')
        ax.xaxis.label.set_color('#dbeafe')
        ax.yaxis.label.set_color('#dbeafe')
        for spine in ax.spines.values():
            spine.set_color('#2b3347')

        fig.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=120, facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        plot_data = base64.b64encode(buf.read()).decode('ascii')
        return jsonify({'plot_data': plot_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route('/falsa_posicion', methods=['GET', 'POST'])
def falsa_posicion_view():
    resultado = None
    error = None
    pasos = None
    if request.method == 'POST':
        try:
            pass

        except Exception as e:
            error = str(e)
    return render_template('falsa_posicion.html', resultado=resultado, error=error, pasos=pasos)

@routes_bp.route('/falsa_posicion/preview', methods=['POST'])
def falsa_posicion_preview():
    pass