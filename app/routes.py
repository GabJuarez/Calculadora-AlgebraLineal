from flask import Blueprint, render_template, request
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
    if request.method == 'POST':
        try:
            funcion = request.form['funcion']
            a = float(request.form['limite_inferior'])
            b = float(request.form['limite_superior'])
            raiz, tabla, iteraciones = biseccion(funcion, (a, b))
            resultado = {'raiz': raiz, 'tabla': tabla, 'iteraciones': iteraciones}
        except Exception as e:
            error = str(e)
    return render_template('biseccion.html', resultado=resultado, error=error, pasos=pasos)
