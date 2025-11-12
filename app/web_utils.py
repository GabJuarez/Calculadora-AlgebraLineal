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

def generate_preview_plot_for_function(funcion: str, limite_inferior: str = '', limite_superior: str = '', n_points: int = 800):
    """Helper: genera plot PNG base64 para la función dada, intenta detectar crossing si límites vacíos."""
    from io import BytesIO
    import base64
    import math
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from app.logic.biseccion import evaluar
    from app.logic.utils import parse_input_number

    # parse limits if provided
    a = None
    b = None
    if limite_inferior != '':
        a = parse_input_number(limite_inferior)
    if limite_superior != '':
        b = parse_input_number(limite_superior)

    if a is None or b is None or a == b:
        a = -5.0 if a is None else a
        b = 5.0 if b is None else b

    xs = [a + i * (b - a) / (n_points - 1) for i in range(n_points)]
    ys = []
    for x in xs:
        try:
            ys.append(evaluar(funcion, x))
        except Exception:
            ys.append(float('nan'))

    # detect crossing and zoom if limits were empty
    crossing = None
    for i in range(len(xs)-1):
        y1 = ys[i]
        y2 = ys[i+1]
        if not (isinstance(y1, float) and isinstance(y2, float)):
            continue
        if math.isnan(y1) or math.isnan(y2):
            continue
        if y1 * y2 <= 0:
            try:
                frac = abs(y1) / (abs(y1) + abs(y2)) if (abs(y1) + abs(y2)) != 0 else 0.5
                crossing = xs[i] + (xs[i+1] - xs[i]) * frac
                break
            except Exception:
                crossing = xs[i]
                break

    if crossing is not None and (limite_inferior == '' or limite_superior == ''):
        a = crossing - 2
        b = crossing + 2
        xs = [a + i * (b - a) / (n_points - 1) for i in range(n_points)]
        ys = []
        for x in xs:
            try:
                ys.append(evaluar(funcion, x))
            except Exception:
                ys.append(float('nan'))

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.axhline(0, color='black', linewidth=0.8)
    ax.plot(xs, ys, color='#1f77b4', linewidth=1.8)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.grid(True, linestyle=':', linewidth=0.6, color='#444')
    ax.set_facecolor('#1a1c2a')
    fig.patch.set_facecolor('#101216')
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
    return plot_data


# New helper: detecta intervalos razonables cuando no vienen límites
def generar_grafico_por_defecto(funcion: str, a: float = -10.0, b: float = 10.0, n: int = 800, pad: float = 2.0):
    """Muestra la misma lógica de muestreo que la generación de preview pero sólo devuelve límites.

    Devuelve (limite_inferior_str, limite_superior_str). Si no encuentra cruce devuelve ('-1','1').
    """
    try:
        from app.logic.biseccion import evaluar
        import math
        xs = [a + i * (b - a) / (n - 1) for i in range(n)]
        ys = []
        for x in xs:
            try:
                ys.append(evaluar(funcion, x))
            except Exception:
                ys.append(float('nan'))
        crossing = None
        for i in range(n - 1):
            y1 = ys[i]; y2 = ys[i + 1]
            if not (isinstance(y1, float) and isinstance(y2, float)):
                continue
            if math.isnan(y1) or math.isnan(y2):
                continue
            if y1 * y2 <= 0:
                frac = abs(y1) / (abs(y1) + abs(y2)) if (abs(y1) + abs(y2)) != 0 else 0.5
                crossing = xs[i] + (xs[i + 1] - xs[i]) * frac
                break
        if crossing is not None:
            return str(crossing - pad), str(crossing + pad)
        return '-1', '1'
    except Exception:
        return '-1', '1'
