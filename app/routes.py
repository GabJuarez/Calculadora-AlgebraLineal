from flask import Blueprint, render_template, request, jsonify
from app import (gauss_jordan, resolver_cramer, gauss_jordan_pasos,
                 eliminacion_gaussiana, matriz_desde_formulario, traspuesta,
                 matriz_triangular,calcular_determinante, biseccion, operar_matrices,
                 falsa_posicion, generate_preview_plot_for_function, generar_grafico_por_defecto)
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
                        li, ls = generar_grafico_por_defecto(funcion)
                        limite_inferior = li
                        limite_superior = ls
                    except Exception:
                        limite_inferior = '-1'
                        limite_superior = '1'
            else:
                # Generar la imagen en servidor reutilizando el helper genérico
                try:
                    plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=401)
                except Exception:
                    plot_data = None

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
    try:
        funcion = request.form.get('funcion', '').strip()
        limite_inferior = request.form.get('limite_inferior', '').strip()
        limite_superior = request.form.get('limite_superior', '').strip()
        if not funcion:
            return jsonify({'error': 'Función vacía'}), 400
        plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=800)
        return jsonify({'plot_data': plot_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@routes_bp.route('/falsa_posicion', methods=['GET', 'POST'])
def falsa_posicion_view():
    resultado = None
    error = None
    pasos = None
    plot_data = None
    funcion = ''
    limite_inferior = ''
    limite_superior = ''
    if request.method == 'POST':
        try:
            funcion = request.form.get('funcion', '').strip()
            limite_inferior = request.form.get('limite_inferior', '').strip()
            limite_superior = request.form.get('limite_superior', '').strip()

            preview_image_b64 = request.form.get('preview_image', '')
            if preview_image_b64:
                plot_data = preview_image_b64
                # If limits are empty, try to detect an interval to use for the algorithm like in biseccion
                if not limite_inferior or not limite_superior:
                    try:
                        li, ls = generar_grafico_por_defecto(funcion)
                        limite_inferior = li
                        limite_superior = ls
                    except Exception:
                        limite_inferior = '-1'
                        limite_superior = '1'
            else:
                # generate plot based on provided limits
                try:
                    plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=401)
                except Exception as e:
                    # ignore plot failures but keep going to attempt calculation
                    plot_data = None

            raiz, tabla, iteraciones = falsa_posicion(funcion, (limite_inferior, limite_superior))
            resultado = {'raiz': raiz, 'tabla': tabla, 'iteraciones': iteraciones}
        except Exception as e:
            error = str(e)
    return render_template('falsa_posicion.html', resultado=resultado, error=error, pasos=pasos,
                           funcion=funcion, limite_inferior=limite_inferior, limite_superior=limite_superior,
                           plot_data=plot_data)


@routes_bp.route('/falsa_posicion/preview', methods=['POST'])
def falsa_posicion_preview():
    try:
        funcion = request.form.get('funcion', '').strip()
        limite_inferior = request.form.get('limite_inferior', '').strip()
        limite_superior = request.form.get('limite_superior', '').strip()
        if not funcion:
            return jsonify({'error': 'Función vacía'}), 400
        plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=800)
        return jsonify({'plot_data': plot_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_bp.route('/newton', methods=['GET', 'POST'])
def newton_view():
    resultado = None
    error = None
    pasos = None
    plot_data = None
    funcion = ''
    x0 = ''
    limite_inferior = ''
    limite_superior = ''
    if request.method == 'POST':
        try:
            funcion = request.form.get('funcion', '').strip()
            x0 = request.form.get('x0', '').strip()
            limite_inferior = request.form.get('limite_inferior', '').strip()
            limite_superior = request.form.get('limite_superior', '').strip()
            preview_image_b64 = request.form.get('preview_image', '')
            if preview_image_b64:
                plot_data = preview_image_b64
            else:
                try:
                    plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=401)
                except Exception:
                    plot_data = None

            from app.logic.newton_raphson import newton_raphson as _newton
            raiz, tabla, iteraciones, f_en_raiz = _newton(funcion, x0)
            resultado = {'raiz': raiz, 'tabla': tabla, 'iteraciones': iteraciones, 'f_en_raiz': f_en_raiz}
        except Exception as e:
            error = str(e)
    return render_template('newton_raphson.html', resultado=resultado, error=error, pasos=pasos,
                           funcion=funcion, x0=x0, plot_data=plot_data,
                           limite_inferior=limite_inferior, limite_superior=limite_superior)


@routes_bp.route('/newton/preview', methods=['POST'])
def newton_preview():
    try:
        funcion = request.form.get('funcion', '').strip()
        limite_inferior = request.form.get('limite_inferior', '').strip()
        limite_superior = request.form.get('limite_superior', '').strip()
        if not funcion:
            return jsonify({'error': 'Función vacía'}), 400
        plot_data = generate_preview_plot_for_function(funcion, limite_inferior, limite_superior, n_points=800)
        return jsonify({'plot_data': plot_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
