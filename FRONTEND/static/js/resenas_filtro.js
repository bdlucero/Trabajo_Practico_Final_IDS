function normalizarTexto(s) {
    return String(s || "")
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
}

function updateMateriasCounter() {
    const selected = document.querySelectorAll("input[name='materias']:checked").length;
    const counterEl = document.querySelector(".materias-counter");
    if (!counterEl) return;

    counterEl.textContent = selected
        ? `${selected} seleccionada${selected === 1 ? "" : "s"}`
        : "";
}

document.addEventListener("DOMContentLoaded", () => {

    const searchForm   = document.querySelector("#searchForm");
    const filtersForm  = document.querySelector("#filtersForm");
    const materiaInput = document.querySelector("#materiaFilter");
 
    if (filtersForm) {

        document.querySelectorAll("input[name='materias']").forEach(cb => {
            cb.addEventListener("change", () => {
                updateMateriasCounter();
                filtersForm.submit();
            });
        });

        document.querySelectorAll(".filter-actions [data-action]").forEach(btn => {
            btn.addEventListener("click", () => {
                const marcar = btn.dataset.action === "all";

                document.querySelectorAll("input[name='materias']").forEach(cb => {
                    cb.checked = marcar;
                });

                updateMateriasCounter();
                filtersForm.submit();
            });
        });
    }

    if (materiaInput) {

        const aplicarFiltroListaMaterias = () => {
            const termNorm = normalizarTexto(materiaInput.value);

            document.querySelectorAll("#materiasList label").forEach(label => {

                const baseName =
                    label.dataset.name ||
                    label.querySelector(".cklabel")?.textContent ||
                    label.textContent ||
                    "";

                const nameNorm = normalizarTexto(baseName);

                const visible = !termNorm || nameNorm.includes(termNorm);
                label.style.display = visible ? "" : "none";
            });
        };

        materiaInput.addEventListener("input", aplicarFiltroListaMaterias);

        aplicarFiltroListaMaterias();
    }

    updateMateriasCounter();
});
