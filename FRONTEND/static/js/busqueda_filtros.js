function normalizarTexto(texto) {
  return String(texto || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function actualizarContadorMaterias() {
  const cantidadSeleccionadas = document.querySelectorAll("input[name='materias']:checked").length;
  const elementoContador = document.querySelector(".materias-counter");
  if (!elementoContador) return;
  elementoContador.textContent = cantidadSeleccionadas
    ? `${cantidadSeleccionadas} seleccionada${cantidadSeleccionadas === 1 ? "" : "s"}`
    : "";
}

document.addEventListener("DOMContentLoaded", () => {
  const formularioFiltros    = document.querySelector("#filtersForm");
  const selectorOrden        = document.querySelector("#sort");
  const campoOrdenOculto     = document.querySelector("#sortHidden");
  const campoFiltroMateria   = document.querySelector("#materiaFilter");
  const botonLimpiarFiltros  = document.querySelector("#clearFilters");

  if (selectorOrden) {
    selectorOrden.addEventListener("change", () => {
      if (campoOrdenOculto) {
        campoOrdenOculto.value = selectorOrden.value;
      }
      if (formularioFiltros) {
        formularioFiltros.submit();
      }
    });
  }

  const botonesFiltro = document.querySelectorAll(".filter-actions [data-action]");
  for (const boton of botonesFiltro) {
    boton.addEventListener("click", () => {
      const marcar = boton.dataset.action === "all";
      const checkboxesMaterias = document.querySelectorAll("input[name='materias']");
      for (const checkbox of checkboxesMaterias) {
        checkbox.checked = marcar;
      }
      actualizarContadorMaterias();
    });
  }

  if (campoFiltroMateria) {
    const filtrarMaterias = () => {
      const terminoNormalizado = normalizarTexto(campoFiltroMateria.value);
      const etiquetas = document.querySelectorAll("#materiasList label");
      for (const label of etiquetas) {
        const nombreBase =
          label.dataset.name ||
          ((label.querySelector(".cklabel") && label.querySelector(".cklabel").textContent) ||
           label.textContent ||
           "");
        const nombreNormalizado = normalizarTexto(nombreBase);
        if (terminoNormalizado && !nombreNormalizado.includes(terminoNormalizado)) {
          label.style.display = "none";
        } else {
          label.style.display = "";
        }
      }
    };

    campoFiltroMateria.addEventListener("input", filtrarMaterias);
    filtrarMaterias();
  }

  if (botonLimpiarFiltros && formularioFiltros) {
    botonLimpiarFiltros.addEventListener("click", (evento) => {
      evento.preventDefault();

      const checkboxesFiltros = document.querySelectorAll("#filtersForm input[type='checkbox']");
      for (const checkbox of checkboxesFiltros) {
        checkbox.checked = false;
      }

      if (campoFiltroMateria) {
        campoFiltroMateria.value = "";
        const eventoInput = new Event("input");
        campoFiltroMateria.dispatchEvent(eventoInput);
      }

      actualizarContadorMaterias();

      if (campoOrdenOculto) {
        campoOrdenOculto.value = "-fecha";
      }

      formularioFiltros.submit();
    });
  }

  actualizarContadorMaterias();

  const checkboxesMaterias = document.querySelectorAll("input[name='materias']");
  for (const checkbox of checkboxesMaterias) {
    checkbox.addEventListener("change", actualizarContadorMaterias);
  }
});
