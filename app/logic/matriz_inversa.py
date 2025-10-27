from app.logic.utils import crear_matriz_identidad, fraccion_str, subindice
from fractions import Fraction

def gauss_jordan_pasos(A):
    n = len(A)
    # Convertir todos los elementos a Fraction
    A_frac = [[Fraction(str(x)) for x in fila] for fila in A]
    I = crear_matriz_identidad(n)
    I_frac = [[Fraction(str(x)) for x in fila] for fila in I]
    aumentada = [A_frac[i] + I_frac[i] for i in range(n)]
    pasos = [("Matriz aumentada inicial [Matriz | I]", [[fraccion_str(x) for x in fila] for fila in aumentada])]

    for i in range(n):
        pivote = aumentada[i][i]
        if pivote == 0:
            for k in range(i + 1, n):
                if aumentada[k][i] != 0:
                    aumentada[i], aumentada[k] = aumentada[k], aumentada[i]
                    pivote = aumentada[i][i]
                    pasos.append((f"F{subindice(i+1)} ↔ F{subindice(k+1)}", [[fraccion_str(x) for x in fila] for fila in aumentada]))
                    break
            else:
                raise ValueError("La matriz no tiene inversa.")
        aumentada[i] = [x / pivote for x in aumentada[i]]
        pasos.append((f"F{subindice(i+1)} → F{subindice(i+1)} ÷ {fraccion_str(pivote)}", [[fraccion_str(x) for x in fila] for fila in aumentada]))
        for j in range(n):
            if j != i:
                factor = aumentada[j][i]
                if factor != 0:
                    aumentada[j] = [a - factor * b for a, b in zip(aumentada[j], aumentada[i])]
                    pasos.append((f"F{subindice(j+1)} → F{subindice(j+1)} − {fraccion_str(factor)} × F{subindice(i+1)}", [[fraccion_str(x) for x in fila] for fila in aumentada]))
    inversa = [fila[n:] for fila in aumentada]
    inversa_str = [[fraccion_str(x) for x in fila] for fila in inversa]
    pasos.append(("Matriz inversa obtenida", inversa_str))
    return inversa_str, pasos

if __name__ == "__main__":
    matriz = [
        [5, 2],
        [-7, -3]
    ]

    inversa, pasos = gauss_jordan_pasos(matriz)
    print("Matriz Inversa:")
    for fila in inversa:
        print("\t".join(fila))
    print("\nPasos:")
    for descripcion, matriz_paso in pasos:
        print(descripcion)
        for fila in matriz_paso:
            print("\t".join(fila))
        print()

