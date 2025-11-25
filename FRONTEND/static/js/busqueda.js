// configuracion para que pueda el que el front end se pueda comunicar
//con la api del backend usamos el atributo data-api-url del DOM

const APP_ROOT = document.getElementById("app");

const API_URL = (APP_ROOT && APP_ROOT.dataset.apiUrl)
  ? APP_ROOT.dataset.apiUrl
  : "http://127.0.0.1:5050/api/publicaciones";

const API_BASE = API_URL.replace(/\/publicaciones.*/i, "");
const API_ORIGIN = new URL(API_URL, window.location.origin).origin;

// tamaños
const PAGE_SIZE = 12;

// Formatos disponibles 
const FORMATOS = [
  { value: "pdf",                label: "PDF" },
  { value: "imagen",             label: "Imagen" },
  { value: "carpeta comprimida", label: "Carpeta comprimida" },
  { value: "repositorio",        label: "Repositorio" },
];

// buscadores
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

let currentPage = 1;

// Normaliza texto para comparar sin tildes y sin mayúsculas
function normalizarTexto(s) {
  return String(s || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

document.addEventListener("DOMContentLoaded", () => {
  const searchForm   = $("#searchForm");
  const filtersForm  = $("#filtersForm");
  const qInput       = $("#q");
  const sortSelect   = $("#sort");
  const materiaInput = $("#materiaFilter");
  const clearFilters = $("#clearFilters");
  const formatoList  = $("#formatoList");

  // Armar lista de formatos
  if (formatoList) {
    formatoList.innerHTML = FORMATOS.map(f => `
      <label class="formato-item">
        <input class="ck" type="checkbox" name="formato" value="${f.value}">
        <span class="ckbox"></span>
        <span class="cklabel">${f.label}</span>
      </label>
    `).join("");
  }

  // Buscar por texto
  if (searchForm && qInput) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault();
      currentPage = 1;
      loadPublicaciones();
    });
  }

  // Aplicar filtros
  if (filtersForm) {
    filtersForm.addEventListener("submit", (e) => {
      e.preventDefault();
      currentPage = 1;
      loadPublicaciones();
    });
  }

  // Orden
  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      currentPage = 1;
      loadPublicaciones();
    });
  }

  // Seleccionar todo / limpiar materias
  $$(".filter-actions [data-action]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const marcar = btn.dataset.action === "all";
      $$("input[name='materias']").forEach((cb) => (cb.checked = marcar));
      updateMateriasCounter();
    });
  });

  // Filtro de materias: al principio NO se muestra nada.
  if (materiaInput) {
    const aplicarFiltroMaterias = () => {
      const termNorm = normalizarTexto(materiaInput.value);
      $$("#materiasList label").forEach((label) => {
        const baseName =
          label.dataset.name ||
          (label.querySelector(".cklabel")?.textContent || label.textContent || "");
        const nameNorm = normalizarTexto(baseName);
        label.style.display = termNorm && nameNorm.includes(termNorm) ? "" : "none";
      });
    };

    materiaInput.addEventListener("input", aplicarFiltroMaterias);
    aplicarFiltroMaterias();  // arranca oculto
  }

  // Limpiar filtros
  if (clearFilters && filtersForm) {
    clearFilters.addEventListener("click", () => {
      $$("#filtersForm input[type='checkbox']").forEach((cb) => (cb.checked = false));
      if (materiaInput) {
        materiaInput.value = "";
        const evt = new Event("input");
        materiaInput.dispatchEvent(evt);
      }
      currentPage = 1;
      loadPublicaciones();
      updateMateriasCounter();
    });
  }

  updateMateriasCounter();
});

// Cuenta materias seleccionadas
function updateMateriasCounter() {
  const n = $$("input[name='materias']:checked").length;
  const el = $(".materias-counter");
  if (!el) return;
  el.textContent = n ? `${n} seleccionada${n === 1 ? "" : "s"}` : "";
}

//  CARGA DE PUBLICACIONES  

function loadPublicaciones() {
  const grid   = $("#grid");
  const empty  = $("#empty");
  const cnt    = $("#resultsCount");
  const pag    = $("#pagination");
  const qInput = $("#q");
  const sortSelect = $("#sort");

  if (!grid || !empty || !cnt || !pag) return;

  cnt.textContent = "Buscando...";
  grid.innerHTML = "";
  empty.hidden = true;
  pag.hidden = true;
  pag.innerHTML = "";

  const params = new URLSearchParams();
  if (qInput && qInput.value.trim()) {
    params.append("q", qInput.value.trim());
  }
  params.append("page", String(currentPage));
  params.append("page_size", String(PAGE_SIZE));
  if (sortSelect) {
    params.append("sort", sortSelect.value || "-fecha");
  }

  $$("input[name='materias']:checked").forEach((cb) => {
    params.append("materias", cb.value);
  });
  $$("input[name='formato']:checked").forEach((cb) => {
    params.append("formato", cb.value);
  });

  const xhr = new XMLHttpRequest();
  xhr.open("GET", `${API_URL}?${params.toString()}`);
  xhr.responseType = "json";

  xhr.onload = () => {
    const status = xhr.status || 0;
    if (status < 200 || status >= 300) {
      cnt.textContent = "Error al buscar";
      return;
    }

    const data   = xhr.response || {};
    const items  = Array.isArray(data.items) ? data.items : [];
    const total  = Number(data.total || 0);
    const page   = Number(data.page || 1);
    const pages  = Number(data.pages || 1);

    currentPage = page;

    cnt.textContent = total
      ? `${total} resultado${total === 1 ? "" : "s"}`
      : "Sin resultados";

    if (!items.length) {
      empty.hidden = false;
      grid.hidden = true;
    } else {
      empty.hidden = true;
      grid.hidden = false;
      grid.innerHTML = items.map(renderCard).join("");
      attachCardHandlers();     // <-- muy importante
    }

    renderPagination(page, pages);
  };

  xhr.onerror = () => {
    cnt.textContent = "Error al buscar";
  };

  xhr.send();
}

// RENDER DE UNA PUBLICACION

function renderCard(p) {
  let url = p.url ?? "#";

  if (url && url.startsWith("/")) {
    url = API_ORIGIN + url;
  }

  const titulo   = esc(p.titulo ?? "Sin título");
  const autor    = esc(p.autor_nombre ?? "Anónimo");
  const fecha    = esc(p.creado_en ?? "");
  const formato  = esc(p.formato ?? "");
  const desc     = esc(p.descripcion ?? "");
  const materias = Array.isArray(p.materias) ? p.materias : [];

  const tags = materias
    .map((m) => `<span class="badge">${esc(m.nombre ?? "")}</span>`)
    .join("");

  const esArchivoSubido = (p.url || "").startsWith("/uploads/");
  const textoVer = (formato === "pdf" || formato === "imagen")
    ? "Ver / previsualizar"
    : "Abrir enlace";

  const botonDescarga = esArchivoSubido
    ? `<a class="btn btn-ghost" href="${url}" download>Descargar</a>`
    : "";

  let botonContacto = "";
  if (p.autor_email) {
    const mail = String(p.autor_email);
    const subject = encodeURIComponent("Consulta sobre tu publicación en SkillMatch UBA");
    const body = encodeURIComponent(
      `Hola, te contacto desde SkillMatch UBA por tu publicación "${p.titulo ?? ""}".`
    );
    const mailto = `mailto:${mail}?subject=${subject}&body=${body}`;

    botonContacto = `
      <a class="btn btn-ghost" href="${mailto}">
        Contactar autor
      </a>`;
  }

  // Bloque de reseñas (inicialmente oculto)
  const bloqueResenas = `
    <div class="card-reseñas" data-role="panel-reseñas" hidden>
      <div class="lista-reseñas" data-role="lista-reseñas">
        <p class="muted sin-resenas">Esta publicación todavía no tiene reseñas.</p>
      </div>
      <div class="form-reseña">
        <label>Tu reseña</label>
        <textarea rows="3" data-role="texto-reseña"></textarea>
        <div class="rating-row">
          <label>Calificación</label>
          <select data-role="rating">
            <option value="5">5 ★</option>
            <option value="4">4 ★</option>
            <option value="3">3 ★</option>
            <option value="2">2 ★</option>
            <option value="1">1 ★</option>
          </select>
          <button type="button" class="btn btn-primary btn-enviar-reseña">
            Enviar reseña
          </button>
        </div>
      </div>
    </div>
  `;

  return `
    <li class="card" data-pub-id="${p.id}">
      <h3><a href="${url}" target="_blank" rel="noopener">${titulo}</a></h3>
      <div class="meta">
        <span>Por ${autor}</span>
        ${fecha ? ` • <span>${fecha}</span>` : ""}
        ${formato ? `<span class="badge">${formato}</span>` : ""}
      </div>
      <div class="tags">${tags}</div>
      ${desc ? `<p class="desc">${desc}</p>` : ""}
      <div class="actions">
        <a class="btn btn-primary" href="${url}" target="_blank" rel="noopener">
          ${textoVer}
        </a>
        ${botonDescarga}
        ${botonContacto}
        <button type="button" class="btn btn-ghost btn-toggle-reviews">
          Ver reseñas
        </button>
      </div>
      ${bloqueResenas}
    </li>
  `;
}

// HANDLERS DE LAS CARDS

function attachCardHandlers() {
  $$(".card").forEach((card) => {
    const pubId         = card.dataset.pubId;
    const toggleBtn     = $(".btn-toggle-reviews", card);
    const panelResenas  = $("[data-role='panel-reseñas']", card);
    const listaResenas  = $("[data-role='lista-reseñas']", card);
    const textoResena   = $("[data-role='texto-reseña']", card);
    const ratingSelect  = $("[data-role='rating']", card);
    const enviarBtn     = $(".btn-enviar-reseña", card);

    if (toggleBtn && panelResenas && listaResenas) {
      toggleBtn.addEventListener("click", () => {
        const visible = !panelResenas.hidden;
        if (visible) {
          panelResenas.hidden = true;
          toggleBtn.textContent = "Ver reseñas";
        } else {
          panelResenas.hidden = false;
          toggleBtn.textContent = "Ocultar reseñas";
          cargarResenas(pubId, listaResenas);
        }
      });
    }

    if (enviarBtn && textoResena && ratingSelect) {
      enviarBtn.addEventListener("click", () => {


        const comentario = textoResena.value.trim();
        const calificacion = ratingSelect.value;

        if (!calificacion) {
          alert("Seleccioná una calificación.");
          return;
        }

        enviarResena(pubId, comentario, calificacion, listaResenas, textoResena);
      });
    }
  });
}

/* ===================== RESEÑAS: GET y POST (XHR) ===================== */

function cargarResenas(pubId, listaEl) {
  if (!listaEl) return;

  listaEl.innerHTML = "<p class='muted'>Cargando reseñas...</p>";

  const xhr = new XMLHttpRequest();
  xhr.open("GET", `${API_BASE}/publicaciones/${pubId}/comentarios`);
  xhr.responseType = "json";

  xhr.onload = () => {
    if (xhr.status < 200 || xhr.status >= 300) {
      listaEl.innerHTML = "<p class='muted'>No se pudieron cargar las reseñas.</p>";
      return;
    }

    const data = xhr.response || [];
    if (!data.length) {
      listaEl.innerHTML = "<p class='muted sin-resenas'>Esta publicación todavía no tiene reseñas.</p>";
      return;
    }

    listaEl.innerHTML = data.map((r) => {
      const txt = esc(r.comentario || "");
      const cal = Number(r.calificacion || 0);
      const estrellas = "★".repeat(cal) + "☆".repeat(5 - cal);
      const fecha = r.fecha_resena ? esc(r.fecha_resena) : "";
      return `
        <div class="reseña-item">
          <div class="reseña-head">
            <span class="stars">${estrellas}</span>
            ${fecha ? `<span class="reseña-fecha">${fecha}</span>` : ""}
          </div>
          ${txt ? `<p>${txt}</p>` : ""}
        </div>
      `;
    }).join("");
  };

  xhr.onerror = () => {
    listaEl.innerHTML = "<p class='muted'>Error de red al cargar reseñas.</p>";
  };

  xhr.send();
}

function enviarResena(pubId, comentario, calificacion, listaEl, textareaEl) {
  const payload = {
    calificacion: calificacion,
    comentario: comentario,
  };

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `${API_BASE}/publicaciones/${pubId}/comentarios`);
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onload = () => {
    if (xhr.status < 200 || xhr.status >= 300) {
      alert("No se pudo guardar la reseña.");
      return;
    }
    alert("Reseña guardada correctamente.");
    if (textareaEl) {
      textareaEl.value = "";
    }
    if (listaEl) {
      cargarResenas(pubId, listaEl);
    }
  };

  xhr.onerror = () => {
    alert("Error de red al enviar la reseña.");
  };

  xhr.send(JSON.stringify(payload));
}

/* ===================== Paginación ===================== */

function renderPagination(page, pages) {
  const pag = $("#pagination");
  if (!pag) return;

  if (pages <= 1) {
    pag.hidden = true;
    pag.innerHTML = "";
    return;
  }

  pag.hidden = false;
  let html = "";

  if (page > 1) {
    html += `<button type="button" data-page="${page - 1}">Anterior</button>`;
  }

  html += `<span> Página ${page} de ${pages} </span>`;

  if (page < pages) {
    html += `<button type="button" data-page="${page + 1}">Siguiente</button>`;
  }

  pag.innerHTML = html;

  $$("#pagination [data-page]").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentPage = Number(btn.dataset.page);
      loadPublicaciones();
    });
  });
}

/* ===================== util: escape HTML ===================== */

function esc(s) {
  return String(s).replace(/[&<>"']/g, (m) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[m]));
}
