import re
import unicodedata

def normalizar_ecuacion(ecuacion: str) -> str:
    ecuacion = unicodedata.normalize("NFKC", ecuacion)
    reemplazos = {"−": "-", "×": "*", "÷": "/", "⁺": "+", "⁻": "-", "∙": "*", "⋅": "*"}
    ecuacion = re.sub(r"[\u200B\u200C\u200D\u2060]", "", ecuacion)
    for viejo, nuevo in reemplazos.items():
        ecuacion = ecuacion.replace(viejo, nuevo)
    return ecuacion.strip()


def agregar_multiplicacion_implicita(ecuacion, variables):
    for var in variables:
        ecuacion = re.sub(rf'(?<![\w])([\d\.]+)({var})(?![\w])', r'\1*\2', ecuacion)
    return ecuacion
