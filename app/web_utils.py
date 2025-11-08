def matriz_desde_formulario(request, filas_name='filas', columnas_name='columnas', celda_prefix='celda_'):
    """
    Construye una matriz a partir de los datos enviados en un formulario HTML.
    Acepta dos convenciones de nombres de inputs:
      - celdas con nombre tipo 'celda_i_j' (legacy)
      - celdas con nombre tipo 'matriz[i][j]'

    Parametros:
        request: objeto request de Flask (o similar con .form mapping)
        filas_name: nombre del campo para filas
        columnas_name: nombre del campo para columnas
        celda_prefix: prefijo para los campos de cada celda (legacy)
    Devuelve:
        matriz: lista de listas con los valores convertidos a int/float cuando sea posible
    """
    import re
    from app.logic.utils import parse_input_number

    # Extraer filas/columnas; permitir que vengan como int ya o como string
    filas_raw = request.form.get(filas_name)
    columnas_raw = request.form.get(columnas_name)
    if filas_raw is None or columnas_raw is None:
        raise ValueError('Campos de filas/columnas no encontrados en el formulario')
    try:
        filas = int(filas_raw)
        columnas = int(columnas_raw)
    except Exception:
        raise ValueError('Valores de filas/columnas inválidos')

    matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

    # Pattern for new style: matriz[0][1]
    pat_new = re.compile(r"^matriz\[(\d+)\]\[(\d+)\]$")
    # Pattern for legacy: celda_0_1
    pat_legacy = re.compile(rf'^{re.escape(celda_prefix)}(\d+)_(\d+)$')

    # iterate over keys in form and fill matrix where applicable
    for key, raw_val in request.form.items():
        raw_val = raw_val.strip() if isinstance(raw_val, str) else raw_val
        if raw_val is None:
            continue
        m_new = pat_new.match(key)
        m_legacy = pat_legacy.match(key)
        if m_new:
            i = int(m_new.group(1))
            j = int(m_new.group(2))
        elif m_legacy:
            i = int(m_legacy.group(1))
            j = int(m_legacy.group(2))
        else:
            continue
        if 0 <= i < filas and 0 <= j < columnas:
            val = raw_val
            # try converting using parse_input_number; if fails keep raw string
            try:
                converted = parse_input_number(val)
                # if it's a whole number, cast to int for nicer display
                if abs(converted - int(converted)) < 1e-12:
                    matriz[i][j] = int(round(converted))
                else:
                    matriz[i][j] = converted
            except Exception:
                # fallback: if looks like fraction keep as 'a/b' string, else leave original trimmed
                s = str(val).strip().replace(' ', '')
                matriz[i][j] = s

    return matriz
