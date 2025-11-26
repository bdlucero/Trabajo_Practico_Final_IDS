const PAGE_SIZE = 12;

const FORMATOS = [
  { value: "pdf",                label: "PDF" },
  { value: "imagen",             label: "Imagen" },
  { value: "carpeta comprimida", label: "Carpeta comprimida" },
  { value: "repositorio",        label: "Repositorio" },
];

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

document.addEventListener("DOMContentLoaded", () => {
  const searchForm   = qs("#searchForm");
  const filtersForm  = qs("#filtersForm");
  const qInput       = qs("#q");
  const sortSelect   = qs("#sort");
  const sortHidden   = qs("#sortHidden");
  const materiaInput = qs("#materiaFilter");
  const clearFilters = qs("#clearFilters");
  const formatoList  = qs("#formatoList");

  if (formatoList) {
    formatoList.innerHTML = FORMATOS.map(f => `
      <label class="formato-item">
        <input class="ck" type="checkbox" name="formato" value="${f.value}">
        <span class="ckbox"></span>
        <span class="cklabel">${f.label}</span>
      </label>
    `).join("");
  }

  if (searchForm && qInput) {
    searchForm.addEventListener("submit", () => {
    });
  }

  if (filtersForm) {
    filtersForm.addEventListener("submit", () => {
    });
  }

  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      if (sortHidden) {
        sortHidden.value = sortSelect.value;
      }
      if (filtersForm) {
        filtersForm.submit();
      }
    });
  }

  qsa(".filter-actions [data-action]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const marcar = btn.dataset.action === "all";
      qsa("input[name='materias']").forEach((cb) => {
        cb.checked = marcar;
      });
      updateMateriasCounter();
    });
  });

  if (materiaInput) {
    const aplicarFiltroMaterias = () => {
      const termNorm = normalizarTexto(materiaInput.value);
      qsa("#materiasList label").forEach((label) => {
        const baseName =
          label.dataset.name ||
          (qs(".cklabel", label)?.textContent || label.textContent || "");
        const nameNorm = normalizarTexto(baseName);
        label.style.display = termNorm && !nameNorm.includes(termNorm) ? "none" : "";
      });
    };

    materiaInput.addEventListener("input", aplicarFiltroMaterias);
    aplicarFiltroMaterias();
  }

  if (clearFilters && filtersForm) {
    clearFilters.addEventListener("click", (e) => {
      e.preventDefault();
      qsa("#filtersForm input[type='checkbox']").forEach((cb) => {
        cb.checked = false;
      });

      if (materiaInput) {
        materiaInput.value = "";
        const evt = new Event("input");
        materiaInput.dispatchEvent(evt);
      }

      updateMateriasCounter();

      if (sortHidden) {
        sortHidden.value = "-fecha";
      }

      filtersForm.submit();
    });
  }

  updateMateriasCounter();
  qsa("input[name='materias']").forEach((cb) => {
    cb.addEventListener("change", updateMateriasCounter);
  });
});

function updateMateriasCounter() {
  const n = qsa("input[name='materias']:checked").length;
  const el = qs(".materias-counter");
  if (!el) return;
  el.textContent = n ? `${n} seleccionada${n === 1 ? "" : "s"}` : "";
}

document.addEventListener("DOMContentLoaded", () => {

  const toggleButtons = qsa(".btn-toggle-reviews");
  toggleButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const panel = document.getElementById(targetId);
      if (!panel) return;

      const visible = !panel.hasAttribute("hidden");
      if (visible) {
        panel.setAttribute("hidden", "hidden");
        btn.textContent = "Ver reseñas";
      } else {
        panel.removeAttribute("hidden");
        btn.textContent = "Ocultar reseñas";
      }
    });
  });
});

