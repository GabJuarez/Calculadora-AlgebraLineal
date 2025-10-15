from warnings import catch_warnings
import os
import platform
from gauss_jordan import *


def limpiar_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

    # Limpiar terminal no se si dejarlo porque pues en pycharm no tiene ningun efecto, ademas deberia de implementar un .sleep() para que espere antes de limpiar

def obtener_tamanio_matrices():
    while True:
        try:
            tamanio_matrizA = int(input('Ingrese tamanio matriz A: '))
            tamanio_matrizB = int(input('Ingrese tamanio matriz B: '))

            if tamanio_matrizA > 0 and tamanio_matrizB > 0:
                return tamanio_matrizA, tamanio_matrizB
            else:
                print('Debes ingresar numeros positivos jeje')
                limpiar_terminal()
        except ValueError:
            print('Debes ingresar numeros enteros')
            limpiar_terminal()
        except Exception as e:
            print(f'Error: {e}')
            limpiar_terminal()

    return matriz

obtener_tamanio_matrices()