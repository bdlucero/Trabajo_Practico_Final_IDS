const formulario = document.getElementById('formulario_resena');

formulario.addEventListener('submit', function (event) {
    if (!formulario.checkValidity()) {
        return; 
    }
    alert("¡Gracias por dejar tu reseña!");
});