function aceptarDatos() {
    mostrarToast("Gracias por aceptar el uso de tus datos.");
}

function rechazarDatos() {
    mostrarToast("No se usarán tus datos personales.");
}


function mostrarOpciones() {
    const opciones = document.getElementById("opciones-privacidad");
    opciones.style.display = opciones.style.display === "none" ? "block" : "none";
}

function confirmarBloque(idBloque, acepta) {
    const bloque = document.getElementById(idBloque);
    const icono = acepta ? "✔" : "✖";
    const texto = acepta ? "Preferencia aceptada" : "Preferencia rechazada";

bloque.innerHTML = `
    <div class="confirmacion-linea">
    <span>${texto}</span>
    <span style="font-size: 1.5rem;">${icono}</span>
    </div>
    `;
}
