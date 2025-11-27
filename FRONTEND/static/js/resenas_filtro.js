// static/js/resenas_filtro.js

 
function qs(selector, ctx) {
  return (ctx || document).querySelector(selector);
}

function qsa(selector, ctx) {
  return Array.from((ctx || document).querySelectorAll(selector));
}

 
function normalizarTexto(s) {
  return String(s || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

 
function updateMateriasCounter() {
  const n = qsa("input[name='materias']:checked").length;
  const el = qs(".materias-counter");
  if (!el) return;
  el.textContent = n ? `${n} seleccionada${n === 1 ? "" : "s"}` : "";
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm   = qs("#searchForm");
  const filtersForm  = qs("#filtersForm");
  const materiaInput = qs("#materiaFilter");

 
  if (searchForm) {
 
  }

 
  if (filtersForm) {
    qsa("input[name='materias']").forEach((cb) => {
      cb.addEventListener("change", () => {
        updateMateriasCounter();
        filtersForm.submit();
      });
    });

 
    qsa(".filter-actions [data-action]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const marcar = btn.dataset.action === "all";
        qsa("input[name='materias']").forEach((cb) => {
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
      qsa("#materiasList label").forEach((label) => {
        const baseName =
          label.dataset.name ||
          (qs(".cklabel", label)?.textContent || label.textContent || "");
        const nameNorm = normalizarTexto(baseName);
        const mostrar = !termNorm || nameNorm.includes(termNorm);
        label.style.display = mostrar ? "" : "none";
      });
    };
    materiaInput.addEventListener("input", aplicarFiltroListaMaterias);
    aplicarFiltroListaMaterias();
  }


  updateMateriasCounter();
});
