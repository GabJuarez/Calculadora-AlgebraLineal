// operaciones_matrices.js
// JS para el template de operaciones entre matrices

function generarInputsMatriz(id, filas, columnas) {
    let contenedor = document.getElementById(id);
    contenedor.innerHTML = '';
    let tabla = document.createElement('table');
    for (let i = 0; i < filas; i++) {
        let tr = document.createElement('tr');
        for (let j = 0; j < columnas; j++) {
            let td = document.createElement('td');
            let input = document.createElement('input');
            input.type = 'number';
            input.name = `${id}_${i}_${j}`;
            input.step = 'any';
            input.className = 'input_matriz';
            td.appendChild(input);
            tr.appendChild(td);
        }
        tabla.appendChild(tr);
    }
    contenedor.appendChild(tabla);
}

function inicializarMatrices() {
    generarInputsMatriz('matriz_a',
        document.getElementById('filas_a').value,
        document.getElementById('columnas_a').value);
    generarInputsMatriz('matriz_b',
        document.getElementById('filas_b').value,
        document.getElementById('columnas_b').value);
}

document.addEventListener('DOMContentLoaded', function() {
    inicializarMatrices();
    document.getElementById('filas_a').addEventListener('input', function() {
        generarInputsMatriz('matriz_a', this.value, document.getElementById('columnas_a').value);
        ajustarMultiplicacion();
    });
    document.getElementById('columnas_a').addEventListener('input', function() {
        generarInputsMatriz('matriz_a', document.getElementById('filas_a').value, this.value);
        ajustarMultiplicacion();
    });
    document.getElementById('filas_b').addEventListener('input', function() {
        generarInputsMatriz('matriz_b', this.value, document.getElementById('columnas_b').value);
        ajustarMultiplicacion();
    });
    document.getElementById('columnas_b').addEventListener('input', function() {
        generarInputsMatriz('matriz_b', document.getElementById('filas_b').value, this.value);
        ajustarMultiplicacion();
    });
    document.getElementById('operacion').addEventListener('change', function() {
        ajustarMultiplicacion();
    });
});

function ajustarMultiplicacion() {
    let operacion = document.getElementById('operacion').value;
    let columnasA = parseInt(document.getElementById('columnas_a').value);
    let filasB = parseInt(document.getElementById('filas_b').value);
    if (operacion === 'multiplicacion') {
        document.getElementById('filas_b').value = columnasA;
        document.getElementById('filas_b').setAttribute('disabled', 'true');
    } else {
        document.getElementById('filas_b').removeAttribute('disabled');
    }
    generarInputsMatriz('matriz_b', document.getElementById('filas_b').value, document.getElementById('columnas_b').value);
}

function limpiarMatrices() {
    generarInputsMatriz('matriz_a', document.getElementById('filas_a').value, document.getElementById('columnas_a').value);
    generarInputsMatriz('matriz_b', document.getElementById('filas_b').value, document.getElementById('columnas_b').value);
    document.getElementById('escalar_a').value = '';
    document.getElementById('escalar_b').value = '';
}

