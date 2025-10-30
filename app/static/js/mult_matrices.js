// Selecciona los elementos del DOM
const form = document.getElementById("matrix-form");
const resultDiv = document.getElementById("result");

// Maneja el envío del formulario
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Evita el envío estándar del formulario

    // Obtén los valores de las matrices desde los textareas
    const matrixA = document.getElementById("matrix-a").value.trim();
    const matrixB = document.getElementById("matrix-b").value.trim();

    // Verifica que ambos campos tengan contenido
    if (!matrixA || !matrixB) {
        resultDiv.textContent = "Por favor, ingresa ambas matrices.";
        return;
    }

    try {
        // Envía las matrices al backend
        const response = await fetch("/multiplicar_matrices", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ matrixA, matrixB }),
        });

        // Maneja la respuesta del backend
        if (response.ok) {
            const data = await response.json();
            resultDiv.textContent = `Resultado:\n${data.result}`;
        } else {
            const error = await response.json();
            resultDiv.textContent = `Error: ${error.message}`;
        }
    } catch (err) {
        resultDiv.textContent = "Ocurrió un error al procesar las matrices.";
        console.error(err);
    }
});
