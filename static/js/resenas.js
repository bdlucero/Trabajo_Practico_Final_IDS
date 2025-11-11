document.addEventListener('DOMContentLoaded', function () {

    let contenedor_valoracion_total = document.getElementById('valoracion_promedio');
    let valoracion_total = document.getElementById('valoracion_total').innerText;
    mostrarEstrellas(contenedor_valoracion_total, parseInt(valoracion_total));


    let resenas = document.querySelectorAll('.resena');
    resenas.forEach(function (resena) {
        let contenedor_estrellas = resena.querySelector('.valoracion_resena');
        let calificacion = parseInt(resena.querySelector('.calificacion').innerText);
        mostrarEstrellas(contenedor_estrellas, calificacion);
    });

});


function mostrarEstrellas(container, calificacion) {
    const template = document.getElementById('star-rating-template');
    const clone = document.importNode(template.content, true);

    let radios = clone.querySelectorAll('.star-rating-template input[type="radio"]');
    radios.forEach((radio, index) => {
        if (index < calificacion) {
            radio.checked = true;
            radio.nextElementSibling.style.color = 'gold';
        }
    });

    container.appendChild(clone);
}