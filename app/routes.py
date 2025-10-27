from cupshelpers.debug import nonfatalException
from flask import render_template, request
from app.logic import gauss_jordan
import re
from main import app

def validar_matriz(matriz):
    """
    Valida que todos los elementos de la matriz sean enteros, decimales o fracciones tipo a/b.
    Devuelve True si es válida, de lo contrario lanza ValueError.
    """
    regex = re.compile(r'^-?\d+$|^-?\d+\.\d+$|^-?\d+/\d+$')
    for fila in matriz:
        for val in fila:
            # Si es int o float, es válido
            if isinstance(val, (int, float)):
                continue
            val_str = str(val).strip().replace(' ', '')
            if not val_str or not regex.fullmatch(val_str):
                raise ValueError(f"Todos los elementos deben ser números o fracciones. Valor inválido: '{val}'")
    return True
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/cramer', methods=['GET', 'POST'])
# def cramer():
#     resultado = None
#     error = None
#     pasos = None
#     if request.method == 'POST':
#         try:
#
#     return render_template('cramer.html')


@app.route('/gauss_jordan', methods=['GET', 'POST'])
def gaussJordan():
    resultado = None
    error = None
    pasos = None
    if request.method == 'POST':
        try:
            filas = int(request.form['filas'])
            columnas = int(request.form['columnas'])
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    valor = request.form.get(f'celda_{i}_{j}', '').strip().replace(' ', '')
                    # Si el valor es un número, conviértelo a int o float
                    if valor.isdigit() or (valor.startswith('-') and valor[1:].isdigit()):
                        fila.append(int(valor))
                    elif re.match(r'^-?\d+\.\d+$', valor):
                        fila.append(float(valor))
                    else:
                        fila.append(valor)  # Fracción tipo a/b o string
                matriz.append(fila)
            validar_matriz(matriz)
            matriz_reducida, soluciones, pasos = gauss_jordan(matriz)
            resultado = {'matriz_reducida': matriz_reducida, 'soluciones': soluciones}
        except Exception as e:
            error = str(e)
    return render_template('gauss_jordan.html', resultado=resultado, error=error, pasos=pasos)

@app.route('/eliminacion_gaussiana')
def Gauss():
    return render_template('eliminacion_gaussiana.html')

@app.route('/entrada_matrices')
def entrada_matrices():
    return render_template('entrada_matrices.html')
