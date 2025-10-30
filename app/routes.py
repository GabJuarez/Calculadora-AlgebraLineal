from flask import Blueprint, render_template, request
from app import (gauss_jordan, resolver_cramer, gauss_jordan_pasos,
                 eliminacion_gaussiana, matriz_desde_formulario, traspuesta,
                 matriz_triangular,calcular_determinante)
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

@routes_bp.route('/multiplicacion_matrices', methods=['GET', 'POST'])
def multiplicacion_matrices_view():
    resultado = None
    error = None
    if request.method == 'POST':
        try:
            from app.logic.multiplicacion_matrices import multiplicar_y_formatear
            a_texto = request.form.get('matriz_a', '')
            b_texto = request.form.get('matriz_b', '')
            resultado = multiplicar_y_formatear(a_texto, b_texto)
        except Exception as e:
            error = str(e)
    return render_template('multiplicacion_matrices.html', resultado=resultado, error=error)



