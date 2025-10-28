from flask import Blueprint, render_template, request
from app.logic import gauss_jordan, resolver_cramer, gauss_jordan_pasos
from app import matriz_desde_formulario
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
def cramer():
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
def gaussJordan():
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
def matrizInversa():
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

