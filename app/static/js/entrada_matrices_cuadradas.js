window.addEventListener('DOMContentLoaded', function() {
    generarMatrizCuadrada();
    document.getElementById('filas').addEventListener('change', generarMatrizCuadrada);
    document.getElementById('columnas').addEventListener('change', generarMatrizCuadrada);
    document.querySelector('form').addEventListener('submit', function(e) {
        if (!validarMatrizCuadrada()) {
            e.preventDefault();
        }
    });
});

function generarMatrizCuadrada() {
    const filas = parseInt(document.getElementById('filas').value);
    const columnas = parseInt(document.getElementById('columnas').value);
    let tabla = '<table>';
    for (let i = 0; i < filas; i++) {
        tabla += '<tr>';
        for (let j = 0; j < columnas; j++) {
            tabla += `<td><input type="text" name="matriz[${i}][${j}]" required placeholder="Ej: 1/2, -3, 4.5" oninput="validarCeldaCuadrada(this)"></td>`;
        }
        tabla += '</tr>';
    }
    tabla += '</table>';
    document.getElementById('matriz').innerHTML = tabla;
}

function validarCeldaCuadrada(input) {
    const regex = /^-?\d+(\.\d+)?$|^-?\d+\/\d+$/;
    let valor = input.value.trim().replace(/\s+/g, '');
    if (valor === '') {
        input.setCustomValidity('Este campo es obligatorio');
        input.style.backgroundColor = '';
        return;
    }
    if (!regex.test(valor)) {
        input.setCustomValidity('Valor inválido. Usa enteros, decimales con punto o fracciones tipo a/b.');
        input.style.backgroundColor = '#ffdddd';
    } else {
        input.setCustomValidity('');
        input.style.backgroundColor = '';
    }
}

function valorConvertidoCuadrada(valor) {
    valor = valor.trim().replace(/\s+/g, '');
    if (/^-?\d+$/.test(valor)) {
        return parseInt(valor, 10);
    } else if (/^-?\d+\.\d+$/.test(valor)) {
        return parseFloat(valor);
    } else if (/^-?\d+\/\d+$/.test(valor)) {
        return valor;
    } else {
        return valor;
    }
}

function validarMatrizCuadrada() {
    const filas = parseInt(document.getElementById('filas').value);
    const columnas = parseInt(document.getElementById('columnas').value);
    let valido = true;
    let mensaje = '';
    const regex = /^-?\d+(\.\d+)?$|^-?\d+\/\d+$/;
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            const input = document.querySelector(`[name='matriz[${i}][${j}]']`);
            let valor = input.value.trim().replace(/\s+/g, '');
            if (!regex.test(valor)) {
                valido = false;
                mensaje = `Valor inválido en la celda (${i+1}, ${j+1}): "${valor}". Usa enteros, decimales con punto o fracciones tipo a/b.`;
                input.focus();
                break;
            }
            input.value = valorConvertidoCuadrada(valor);
        }
        if (!valido) break;
    }
    if (!valido) {
        alert(mensaje);
    }
    return valido;
}

