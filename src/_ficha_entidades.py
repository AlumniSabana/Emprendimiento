# ══════════════════════════════════════════════════════════════
#  MAPA DE ENTIDADES: CADA DOCUMENTO CON SU ENLACE Y SU CASILLA
#
#  ── QUÉ CAMBIÓ Y POR QUÉ ──────────────────────────────────────
#  Antes el enlace estaba en el NOMBRE DE LA ENTIDAD y llevaba a
#  su página principal. Quien leía «Registro Único de Proponentes
#  (RUP)» pulsaba «Cámara de Comercio», caía en una portada con
#  veinte opciones y tenía que buscar el RUP por su cuenta.
#
#  Ahora el enlace está en CADA DOCUMENTO y lleva a la página del
#  trámite. El nombre de la entidad vuelve a ser texto: es un
#  rótulo, no un destino.
#
#  ── POR QUÉ CASI TODO APUNTA A vue.gov.co ─────────────────────
#  La Ventanilla Única Empresarial es del Ministerio de Comercio,
#  Industria y Turismo, y está hecha para esto: un trámite por
#  página, en lenguaje de emprendedor, con selector de ciudad.
#
#  Se prefirió a rues.org.co, que era el enlace anterior, por una
#  razón práctica: el RUES es una aplicación de JavaScript que
#  responde «200 OK» con una página vacía a CUALQUIER dirección,
#  incluso a una inventada. Con eso no hay forma de comprobar si
#  un enlace sigue vivo. La VUE devuelve 404 de verdad cuando la
#  ruta no existe, así que un enlace roto se puede detectar.
#
#  ── CÓMO SE COMPROBARON ───────────────────────────────────────
#  Uno a uno, mirando el código de respuesta Y el contenido: hay
#  páginas del Estado que responden «200 OK» y muestran un error
#  dentro. Se descartaron dos de la DIAN por eso.
#
#  Dos salvedades que conviene conocer:
#
#  · www.sic.gov.co no envía el certificado intermedio. Los
#    navegadores lo resuelven solos y la página abre bien, pero
#    cualquier comprobador automático va a fallar ahí. No es que
#    el enlace esté roto.
#
#  · prestadores.minsalud.gov.co no responde desde fuera de
#    Colombia. No se pudo abrir para comprobarlo; se confirmó por
#    otra vía (está indexado con su título exacto y lo enlazan
#    varias secretarías departamentales de salud). Si alguien del
#    Centro puede abrirlo desde Colombia, conviene confirmarlo.
# ══════════════════════════════════════════════════════════════

#  documento exacto (tal como lo escribe la ficha)
#      -> (dirección del trámite, qué se encuentra ahí)
#
#  La clave tiene que coincidir LETRA POR LETRA con el texto que
#  genera computeDerivacion() en la ficha. Si allí se reescribe un
#  documento y aquí no, ese documento se queda sin enlace: no se
#  rompe nada, simplemente deja de llevar a ninguna parte. Por eso
#  el build avisa si alguna clave deja de aparecer.
DOCUMENTOS = {
    # ── Cámara de Comercio ──
    "Matrícula mercantil (o de establecimiento, si aplica)": (
        "https://www.vue.gov.co/tramites-y-consultas/creacion-empresa-persona-natural-juridica",
        "Cómo matricularte, con los datos de la Cámara de tu ciudad"),
    "Matrícula del establecimiento de comercio": (
        "https://www.vue.gov.co/tramites-y-consultas/creacion-empresa-persona-natural-juridica",
        "Cómo matricular el establecimiento, por ciudad"),
    "Registro Único de Proponentes (RUP)": (
        "https://www.vue.gov.co/tramites-y-consultas/registro-unico-proponentes-rup",
        "Requisitos, tarifas y plazos del RUP"),

    # ── DIAN ──
    "Inscripción en el RUT (Registro Único Tributario)": (
        "https://www.dian.gov.co/impuestos/RUT/Paginas/Inscripcion-y-actualizacion-RUT.aspx",
        "Inscripción y actualización del RUT, con los instructivos paso a paso"),

    # ── Salud ──
    # El REPS: única dirección que no se pudo abrir desde aquí.
    "Inscripción en el REPS (Registro Especial de Prestadores de Salud)": (
        "https://prestadores.minsalud.gov.co/habilitacion/",
        "Registro Especial de Prestadores de Servicios de Salud"),
    # La norma misma, que es lo que hay que leer para habilitar.
    "Habilitación de servicios de salud (la habilitación y las visitas de verificación son gratuitas)": (
        "https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-3100-de-2019.pdf",
        "Resolución 3100 de 2019, la norma vigente de habilitación (PDF)"),

    # ── INVIMA ──
    "Registro, permiso o notificación sanitaria (según el tipo de alimento)": (
        "https://www.invima.gov.co/biblioteca/pasos-obtener-registro-sanitario-alimentos-invima",
        "Guía de pasos para registro, permiso y notificación sanitaria de alimentos"),

    # ── Superintendencia de Industria y Comercio ──
    "Política de tratamiento de datos personales": (
        "https://www.sic.gov.co/content/sobre-la-protecci%C3%B3n-de-datos-personales",
        "Qué exige la Ley 1581 sobre datos personales"),
    "Registro Nacional de Bases de Datos (RNBD), solo si superas los topes vigentes": (
        "https://www.sic.gov.co/registro-nacional-de-bases-de-datos",
        "Quiénes deben inscribirse en el RNBD y desde qué topes"),

    # ── Seguridad social ──
    "Afiliación a ARL antes del primer día trabajado": (
        "https://www.vue.gov.co/tramites-y-consultas/afiliacion-al-sistema-general-de-riesgos-laborales-sgrl",
        "Afiliación al Sistema General de Riesgos Laborales"),
    "Aportes mensuales a salud, pensión, ARL y parafiscales vía PILA": (
        "https://www.minsalud.gov.co/Proteccion-Social/Paginas/pila.aspx",
        "Qué es la PILA y cómo se liquidan los aportes"),

    # ── Sin enlace, a propósito ──
    # Los trámites municipales no tienen una página nacional. Cada
    # alcaldía tiene la suya, y mandar a un portal genérico sería
    # mandar al sitio equivocado con aspecto de sitio correcto.
    "Concepto de uso de suelo": (None, None),
    "Concepto técnico de bomberos (Cuerpo de Bomberos)": (None, None),
    "Concepto sanitario del establecimiento": (None, None),
}


#  El aviso que pidió el Centro: tener el papel no basta si está
#  vencido. Es la confusión más común —«eso ya lo saqué»— y la que
#  aparece cuando alguien va a contratar o lo visita un inspector.
#  El texto va detrás de un «Tenerlo no basta: tiene que estar
#  vigente.» en negrita, así que empieza donde esa frase termina.
AVISO_VIGENCIA = (
    "La matrícula mercantil se renueva cada año, el RUT se actualiza cuando "
    "cambian tus datos, y los conceptos y registros sanitarios tienen fecha de "
    "vencimiento. Si ya tienes alguno, confirma que siga al día antes de "
    "marcarlo: ante una visita o un contrato, un documento vencido cuenta "
    "igual que no tenerlo."
)


CSS = """
/* ═══════════════ CADA DOCUMENTO, SU ENLACE ═══════════════ */
/* El nombre de la entidad vuelve a ser texto: es un rótulo, no un
   destino. Lo que lleva a alguna parte es cada documento. */
.entity-card h4 { padding-right: 2.2rem; }

.entity-card ul li a {
  color: var(--accent-ink);
  text-decoration: none;
  border-bottom: 1px solid rgba(0,20,89,.25);
  transition: border-color .15s, color .15s;
}
.entity-card ul li a:hover {
  color: var(--accent-btn);
  border-bottom-color: currentColor;
}
.entity-card ul li a .flecha { font-size: .82em; margin-left: .15rem; }
.entity-card ul li a:focus-visible {
  outline: 2px solid var(--accent-btn); outline-offset: 2px; border-radius: 2px;
}

/* Las entidades sin dirección fija no fingen tenerla. */
.entity-card .sin-enlace {
  display: block; margin: -.2rem 0 .5rem;
  font-size: .76rem; color: var(--text-muted); line-height: 1.45;
}

/* ═══════════════ LA CASILLA DE «YA LO TENGO» ═══════════════
   Va sobre el borde de la tarjeta, arriba a la derecha. Sobre el
   borde y no dentro porque así se lee como una marca puesta en el
   recuadro, y no como un campo más del contenido. */
.entity-card { position: relative; }
.entity-card .hecho {
  position: absolute; top: -11px; right: 12px;
  width: 26px; height: 26px; padding: 0;
  border: 1px solid var(--line-strong, #C3CFE3);
  border-radius: 50%;
  background: var(--surface, #FFFFFF);
  color: transparent;
  font-size: 14px; line-height: 1;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: background .15s, border-color .15s, color .15s;
}
.entity-card .hecho:hover { border-color: var(--accent-btn); }
.entity-card .hecho:focus-visible {
  outline: 2px solid var(--accent-btn); outline-offset: 2px;
}
/* Marcada: se rellena y aparece el chulo. */
.entity-card .hecho[aria-checked="true"] {
  background: var(--accent-btn, #001459);
  border-color: var(--accent-btn, #001459);
  color: #FFFFFF;
}
/* La tarjeta entera baja un tono cuando está lista, para que de un
   vistazo se vea lo que falta sin tener que leer las casillas. */
.entity-card.ya-esta { background: #F3F6FB; }
.entity-card.ya-esta h4 { color: var(--text-muted); }

/* ═══════════════ EL AVISO DE VIGENCIA ═══════════════ */
.aviso-vigencia {
  margin: .2rem 0 .9rem;
  background: #FBEFDD; border: 1px solid #E4C89B;
  border-left: 3px solid #8A5200;
  border-radius: 0 6px 6px 0;
  padding: .65rem .9rem;
  font-size: .84rem; line-height: 1.55; color: var(--ink);
}
.aviso-vigencia b { color: #8A5200; }

/* En papel, la casilla vacía se imprime vacía y la marcada con su
   chulo: así el PDF sirve de lista para ir tachando lo que falta.

   El color se deja SIN tocar en la casilla sin marcar. Al ponerle
   «color:#000» a todas, el chulo —que en pantalla se esconde con
   «color:transparent»— aparecía en las cinco tarjetas del PDF, y
   la lista salía entera marcada sin haber marcado nada. */
@media print {
  .entity-card .hecho {
    border-color: #555; background: transparent;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  .entity-card .hecho[aria-checked="true"] { background: transparent; color: #000; }
  .entity-card.ya-esta { background: transparent; }
  .entity-card ul li a { border-bottom: 0; color: #000; }
}
"""


JS = r"""
  /* ══════════════════════════════════════════════════════════
     CADA DOCUMENTO CON SU ENLACE
     ══════════════════════════════════════════════════════════ */
  var ENLACES_DOC = __DOCUMENTOS__;

  /* Las entidades que dependen del municipio siguen diciéndolo. */
  var SIN_DIRECCION_FIJA = {
    "Alcaldía / Curaduría municipal": true,
    "Secretaría de Salud departamental o distrital": true,
    "Secretaría de Salud municipal": true
  };

  function tituloEntidad(nombre) {
    var h = el("h4", {}, nombre);
    if (SIN_DIRECCION_FIJA[nombre]) {
      h.appendChild(el("span", { class: "sin-enlace" },
        "Depende de tu municipio: búscala por el nombre de tu alcaldía."));
    }
    return h;
  }

  /* Un documento: con enlace si lo tiene, en texto si no. */
  function documentoLi(texto) {
    var e = ENLACES_DOC[texto];
    var url = e && e[0];
    if (!url) return el("li", {}, texto);

    var a = el("a", {
      href: url, target: "_blank", rel: "noopener noreferrer",
      title: e[1] || ""
    }, texto);
    a.appendChild(el("span", { class: "flecha", "aria-hidden": "true" }, "↗"));
    return el("li", {}, [a]);
  }

  /* ══════════════════════════════════════════════════════════
     LA CASILLA DE «YA LO TENGO»
     ----------------------------------------------------------
     Vive solo mientras la pestaña está abierta, igual que el
     resto de la ficha. No se guarda en el navegador a propósito:
     la ficha entera no se guarda, y marcar unas casillas que sí
     sobreviven mientras las respuestas se pierden haría creer que
     el trabajo quedó a salvo. Lo que sí conserva las marcas es el
     PDF: se descarga con los chulos puestos y sirve de lista.
     ══════════════════════════════════════════════════════════ */
  var ENTIDADES_LISTAS = {};

  function casillaHecho(nombre) {
    var marcada = ENTIDADES_LISTAS[nombre] === true;
    var b = el("button", {
      type: "button",
      class: "hecho",
      role: "checkbox",
      "aria-checked": marcada ? "true" : "false",
      "aria-label": "Ya tengo lo de " + nombre,
      title: "Marca esta entidad cuando ya tengas sus documentos"
    }, "✓");

    b.addEventListener("click", function () {
      var ahora = b.getAttribute("aria-checked") !== "true";
      ENTIDADES_LISTAS[nombre] = ahora;
      b.setAttribute("aria-checked", ahora ? "true" : "false");
      var tarjeta = b.parentNode;
      if (tarjeta && tarjeta.classList) tarjeta.classList.toggle("ya-esta", ahora);
    });
    return b;
  }
"""


def js():
    import json
    return JS.replace("__DOCUMENTOS__", json.dumps(DOCUMENTOS, ensure_ascii=False))
