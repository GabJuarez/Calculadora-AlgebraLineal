window.addEventListener('DOMContentLoaded', function() {
    generarMatriz();
    document.getElementById('filas').addEventListener('change', generarMatriz);
    document.getElementById('columnas').addEventListener('change', generarMatriz);
    document.querySelector('form').addEventListener('submit', function(e) {
        if (!validarMatriz()) {
            e.preventDefault();
        }
    });
});

function generarMatriz() {
    const filas = parseInt(document.getElementById('filas').value);
    const columnas = parseInt(document.getElementById('columnas').value);
    let tabla = '<table>';
    for (let i = 0; i < filas; i++) {
        tabla += '<tr>';
        for (let j = 0; j < columnas; j++) {
            tabla += `<td><input type="text" name="celda_${i}_${j}" required placeholder="Ej: 1/2, -3, 4.5" oninput="validarCelda(this)"></td>`;
        }
        tabla += '</tr>';
    }
    tabla += '</table>';
    document.getElementById('matriz').innerHTML = tabla;
}

function validarCelda(input) {
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

function valorConvertido(valor) {
    valor = valor.trim().replace(/\s+/g, '');
    if (/^-?\d+$/.test(valor)) {
        return parseInt(valor, 10);
    } else if (/^-?\d+\.\d+$/.test(valor)) {
        return parseFloat(valor);
    } else if (/^-?\d+\/\d+$/.test(valor)) {
        return valor; // Se envía como string para que Python lo convierta a Fraction
    } else {
        return valor; // Si no es válido, se envía como string (será validado en Python)
    }
}

function validarMatriz() {
    const filas = parseInt(document.getElementById('filas').value);
    const columnas = parseInt(document.getElementById('columnas').value);
    let valido = true;
    let mensaje = '';
    const regex = /^-?\d+(\.\d+)?$|^-?\d+\/\d+$/;
    for (let i = 0; i < filas; i++) {
        for (let j = 0; j < columnas; j++) {
            const input = document.querySelector(`[name='celda_${i}_${j}']`);
            let valor = input.value.trim().replace(/\s+/g, '');
            if (!regex.test(valor)) {
                valido = false;
                mensaje = `Valor inválido en la celda (${i+1}, ${j+1}): "${valor}". Usa enteros, decimales con punto o fracciones tipo a/b.`;
                input.focus();
                break;
            }
            // Convierte el valor antes de enviar (opcional, solo si usas AJAX)
            input.value = valorConvertido(valor);
        }
        if (!valido) break;
    }
    if (!valido) {
        alert(mensaje);
    }
    return valido;
}
