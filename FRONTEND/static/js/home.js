function aceptarDatos() {
    mostrarToast("Gracias por aceptar el uso de tus datos.");
}

function rechazarDatos() {
    mostrarToast("No se usarán tus datos personales.");
}

function mostrarToast(mensaje) {
    const toast = document.getElementById("popup-confirmacion");
    toast.textContent = mensaje;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3000);
}

document.getElementById("btn-lupa").onclick = function() {
    const input = document.getElementById("input-busqueda");
    input.style.display = input.style.display === "none" ? "inline-block" : "none";
    input.focus();
};

function mostrarOpciones() {
    const opciones = document.getElementById("opciones-privacidad");
    opciones.style.display = opciones.style.display === "none" ? "block" : "none";
}
//                     //


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
