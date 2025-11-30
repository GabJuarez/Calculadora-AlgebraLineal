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
    const op = document.getElementById('operacion');
    const filasA = parseInt(document.getElementById('filas_a').value, 10) || 0;
    const colsA = parseInt(document.getElementById('columnas_a').value, 10) || 0;
    const filasB = parseInt(document.getElementById('filas_b').value, 10) || 0;
    const colsB = parseInt(document.getElementById('columnas_b').value, 10) || 0;

    generarInputsMatriz('matriz_a', filasA, colsA);

    // si la operación es multiplicar, sincronizamos filas de B con columnas de A
    if (op && (op.value === 'Multiplicación')) {
        document.getElementById('filas_b').value = colsA;
        generarInputsMatriz('matriz_b', colsA, colsB);
    } else {
        generarInputsMatriz('matriz_b', filasB, colsB);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    inicializarMatrices();

    document.getElementById('filas_a').addEventListener('input', function() {
        const filas = parseInt(this.value, 10) || 0;
        const columnas = parseInt(document.getElementById('columnas_a').value, 10) || 0;
        generarInputsMatriz('matriz_a', filas, columnas);
    });

    document.getElementById('columnas_a').addEventListener('input', function() {
        const columnasA = parseInt(this.value, 10) || 0;
        const filasA = parseInt(document.getElementById('filas_a').value, 10) || 0;
        const filasBInput = document.getElementById('filas_b');
        const colsB = parseInt(document.getElementById('columnas_b').value, 10) || 0;

        // siempre regenerar A
        generarInputsMatriz('matriz_a', filasA, columnasA);

        // si la operación es multiplicar, sincronizar filas de B con columnas de A
        const op = document.getElementById('operacion');
        if (op && (op.value === 'Multiplicación' || op.value === 'multiplicacion')) {
            filasBInput.value = columnasA;
            generarInputsMatriz('matriz_b', columnasA, colsB);
        } else {
            // en otras operaciones, B mantiene su tamaño independiente
            const filasB = parseInt(filasBInput.value, 10) || 0;
            generarInputsMatriz('matriz_b', filasB, colsB);
        }
    });

    document.getElementById('filas_b').addEventListener('input', function() {
        const filasB = parseInt(this.value, 10) || 0;
        const colsB = parseInt(document.getElementById('columnas_b').value, 10) || 0;

        // siempre regenerar B
        generarInputsMatriz('matriz_b', filasB, colsB);

        // si la operación es multiplicar, sincronizar columnas de A con filas de B
        const op = document.getElementById('operacion');
        if (op && (op.value === 'multiplicar' || op.value === 'multiplicacion')) {
            const columnasAInput = document.getElementById('columnas_a');
            columnasAInput.value = filasB;
            const filasA = parseInt(document.getElementById('filas_a').value, 10) || 0;
            generarInputsMatriz('matriz_a', filasA, filasB);
        }
    });

    document.getElementById('columnas_b').addEventListener('input', function() {
        const filasB = parseInt(document.getElementById('filas_b').value, 10) || 0;
        const columnasB = parseInt(this.value, 10) || 0;
        generarInputsMatriz('matriz_b', filasB, columnasB);
    });

    document.getElementById('operacion').addEventListener('change', function() {
        // Al cambiar la operación, si es multiplicar sincronizamos B.filas = A.columnas
        const op = this.value;
        const columnasA = parseInt(document.getElementById('columnas_a').value, 10) || 0;
        const colsB = parseInt(document.getElementById('columnas_b').value, 10) || 0;
        if (op === 'Multiplicación' || op === 'multiplicacion') {
            document.getElementById('filas_b').value = columnasA;
            generarInputsMatriz('matriz_b', columnasA, colsB);
        } else {
            // si se cambia a otra operación, no forzamos sincronía; solo regeneramos con valores actuales
            const filasB = parseInt(document.getElementById('filas_b').value, 10) || 0;
            const filasA = parseInt(document.getElementById('filas_a').value, 10) || 0;
            const columnasA = parseInt(document.getElementById('columnas_a').value, 10) || 0;
            generarInputsMatriz('matriz_a', filasA, columnasA);
            generarInputsMatriz('matriz_b', filasB, colsB);
        }
    });
});

function limpiarMatrices() {
    generarInputsMatriz('matriz_a', parseInt(document.getElementById('filas_a').value, 10) || 0, parseInt(document.getElementById('columnas_a').value, 10) || 0);
    generarInputsMatriz('matriz_b', parseInt(document.getElementById('filas_b').value, 10) || 0, parseInt(document.getElementById('columnas_b').value, 10) || 0);
    document.getElementById('escalar_a').value = '';
    document.getElementById('escalar_b').value = '';
}
