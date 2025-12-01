document.addEventListener("DOMContentLoaded", () => {
  const botonesResenas = document.querySelectorAll(".btn-toggle-reviews");
  for (const boton of botonesResenas) {
    boton.addEventListener("click", () => {
      const idPanel = boton.dataset.target;
      const panel = document.getElementById(idPanel);
      if (!panel) return;

      const visible = !panel.hasAttribute("hidden");
      if (visible) {
        panel.setAttribute("hidden", "hidden");
        boton.textContent = "Ver reseñas";
      } else {
        panel.removeAttribute("hidden");
        boton.textContent = "Ocultar reseñas";
      }
    });
  }
});
