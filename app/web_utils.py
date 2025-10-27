def matriz_desde_formulario(request, filas_name='filas', columnas_name='columnas', celda_prefix='celda_'):
    """
    Construye una matriz a partir de los datos enviados en un formulario HTML.
    Parametros:
        request: objeto request de Flask
        filas_name: nombre del campo para filas
        columnas_name: nombre del campo para columnas
        celda_prefix: prefijo para los campos de cada celda
    Devuelve:
        matriz: lista de listas con los valores convertidos
    """
    import re
    filas = int(request.form[filas_name])
    columnas = int(request.form[columnas_name])
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = request.form.get(f'{celda_prefix}{i}_{j}', '').strip().replace(' ', '')
            if valor.isdigit() or (valor.startswith('-') and valor[1:].isdigit()):
                fila.append(int(valor))
            elif re.match(r'^-?\d+\.\d+$', valor):
                fila.append(float(valor))
            else:
                fila.append(valor)
        matriz.append(fila)
    return matriz

