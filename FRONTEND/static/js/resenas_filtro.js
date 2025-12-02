function normalizarTexto(texto) {
    return String(texto || "")
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

function materiasSeleccionadas() {
    return Array.from(document.querySelectorAll("input[name='materias']:checked"))
        .map(cb => cb.value);
}

function actualizarContadorMaterias() {
    const cantidad = materiasSeleccionadas().length;
    const contador = document.querySelector(".materias-counter");
    if (!contador) return;

    contador.textContent = cantidad
        ? `${cantidad} seleccionada${cantidad === 1 ? "" : "s"}`
        : "";
}

function aplicarFiltrosResenas() {
    const campoBusqueda = document.querySelector("#q");
    const texto = normalizarTexto(campoBusqueda ? campoBusqueda.value : "");
    const seleccionadas = materiasSeleccionadas();

    const tarjetas = document.querySelectorAll(".card3.scalex");
    tarjetas.forEach(card => {
        const codMateria = card.dataset.materia || "";
        const textoCard = normalizarTexto(card.textContent || "");

        let visible = true;

        if (seleccionadas.length > 0 && !seleccionadas.includes(codMateria)) {
            visible = false;
        }

        if (texto && !textoCard.includes(texto)) {
            visible = false;
        }

        card.style.display = visible ? "" : "none";
    });
}

function filtrarListaMaterias() {
    const input = document.querySelector("#materiaFilter");
    if (!input) return;

    const termino = normalizarTexto(input.value);

    document.querySelectorAll("#materiasList label").forEach(label => {
        const baseName =
            label.dataset.name ||
            label.querySelector(".cklabel")?.textContent ||
            label.textContent ||
            "";

        const nombre = normalizarTexto(baseName);
        label.style.display = !termino || nombre.includes(termino) ? "" : "none";
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const formularioBusqueda = document.querySelector("#searchForm");
    const formularioFiltros  = document.querySelector("#filtersForm");
    const campoBusqueda      = document.querySelector("#q");
    const filtroMateria      = document.querySelector("#materiaFilter");

    if (formularioBusqueda && campoBusqueda) {
        formularioBusqueda.addEventListener("submit", (e) => {
            e.preventDefault();
            aplicarFiltrosResenas();
        });
        campoBusqueda.addEventListener("input", aplicarFiltrosResenas);
    }

    if (formularioFiltros) {
        document.querySelectorAll("input[name='materias']").forEach(cb => {
            cb.addEventListener("change", () => {
                actualizarContadorMaterias();
                aplicarFiltrosResenas();
            });
        });

        document.querySelectorAll(".filter-actions [data-action]").forEach(boton => {
            boton.addEventListener("click", () => {
                const marcar = boton.dataset.action === "all";
                document.querySelectorAll("input[name='materias']").forEach(cb => {
                    cb.checked = marcar;
                });
                actualizarContadorMaterias();
                aplicarFiltrosResenas();
            });
        });
    }

    if (filtroMateria) {
        filtroMateria.addEventListener("input", filtrarListaMaterias);
        filtrarListaMaterias();
    }

    actualizarContadorMaterias();
    aplicarFiltrosResenas();
});


 