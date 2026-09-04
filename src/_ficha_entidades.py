# ══════════════════════════════════════════════════════════════
#  EL TÍTULO DE CADA ENTIDAD ES SU ENLACE
#
#  Antes había dos bloques: el mapa de entidades y, más abajo,
#  «Gestiona tus documentos base aquí» con cuatro botones sueltos.
#  Quien leía «Cámara de Comercio» tenía que bajar a buscar el
#  botón correspondiente, y solo cuatro de las ocho entidades
#  tenían botón.
#
#  Ahora el nombre de cada entidad lleva directo a su sitio.
#
#  ── LOS ENLACES ───────────────────────────────────────────────
#  Todos son sitios oficiales del Estado colombiano, verificados
#  uno a uno. Las dos entidades sin dirección fija —la Alcaldía y
#  la Secretaría de Salud dependen del municipio de cada quien—
#  se dejan sin enlace en vez de mandar a un portal genérico que
#  no es el suyo.
# ══════════════════════════════════════════════════════════════

#  nombre de la entidad  ->  (dirección oficial, qué se hace ahí)
ENLACES = {
    "Cámara de Comercio": (
        "https://www.rues.org.co",
        "Consulta el RUES y encuentra tu Cámara de Comercio"),
    "DIAN": (
        "https://www.dian.gov.co",
        "Inscripción y actualización del RUT"),
    "ARL / Sistema de Seguridad Social (PILA)": (
        "https://www.miplanilla.com",
        "Aportes a seguridad social por PILA"),
    "INVIMA": (
        "https://www.invima.gov.co/tramites-y-servicios",
        "Trámites y registros sanitarios"),
    "Superintendencia de Industria y Comercio (SIC)": (
        "https://www.sic.gov.co",
        "Registro de marca y protección al consumidor"),
    # Sin enlace a propósito: dependen del municipio de cada quien.
    # Mandar a un portal nacional sería mandar al sitio equivocado.
    "Alcaldía / Curaduría municipal": (None, None),
    "Secretaría de Salud departamental o distrital": (None, None),
    "Secretaría de Salud municipal": (None, None),
}


CSS = """
/* ═══════════════ EL TÍTULO ES EL ENLACE ═══════════════ */
.entity-card h4 a {
  color: var(--accent-ink);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color .15s, color .15s;
  display: inline-flex; align-items: baseline; gap: .3rem;
}
.entity-card h4 a:hover {
  color: var(--accent-btn);
  border-bottom-color: currentColor;
}
.entity-card h4 a .flecha { font-size: .82em; }
/* Las entidades sin enlace no fingen tenerlo: el nombre va en
   texto plano y una nota explica por qué. */
.entity-card .sin-enlace {
  display: block; margin-top: .35rem;
  font-size: .76rem; color: var(--text-muted); line-height: 1.45;
}
"""


JS = r"""
  /* El nombre de cada entidad, enlazado a su sitio oficial. */
  var ENLACES_ENTIDAD = __ENLACES__;

  function tituloEntidad(nombre) {
    var e = ENLACES_ENTIDAD[nombre];
    var url = e && e[0];
    if (!url) {
      var h = el("h4", {}, nombre);
      h.appendChild(el("span", { class: "sin-enlace" },
        "Depende de tu municipio: búscala por el nombre de tu alcaldía."));
      return h;
    }
    var a = el("a", {
      href: url, target: "_blank", rel: "noopener noreferrer",
      title: e[1] || ""
    }, nombre);
    a.appendChild(el("span", { class: "flecha", "aria-hidden": "true" }, "↗"));
    return el("h4", {}, [a]);
  }
"""


def js():
    import json
    return JS.replace("__ENLACES__", json.dumps(ENLACES, ensure_ascii=False))
