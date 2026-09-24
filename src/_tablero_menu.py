# ══════════════════════════════════════════════════════════════
#  EL ÍNDICE LATERAL: CINCO GRUPOS QUE SE ABREN Y SE CIERRAN
#
#  ── QUÉ CAMBIÓ ────────────────────────────────────────────────
#  Eran cuatro rótulos fijos (Resumen, Datos del mes, Cálculos,
#  Rutina) con sus once opciones siempre a la vista. Ahora son
#  cinco grupos plegables:
#
#      1 · Guía            ← antes era una opción dentro de Rutina
#      2 · Datos del mes
#      3 · Cálculos
#      4 · Rutina
#      5 · Resumen         ← antes estaba de primero
#
#  ── POR QUÉ LA GUÍA VA PRIMERO ────────────────────────────────
#  Estaba enterrada en «Rutina», penúltima de once, y es lo que
#  alguien necesita cuando abre esto por primera vez y no sabe qué
#  es un punto de equilibrio. El resumen, en cambio, no tiene nada
#  que resumir hasta que hay cifras cargadas: de primero mostraba
#  guiones a quien acababa de entrar.
#
#  ── QUÉ SE ABRE SOLO ──────────────────────────────────────────
#  El grupo de la pestaña activa. Al entrar en «Precio mínimo» y
#  recargar, «Cálculos» aparece abierto: si todo empezara cerrado,
#  la opción marcada quedaría escondida dentro de un grupo
#  plegado, y parecería que se perdió.
#
#  Se recuerda además qué grupos dejó abiertos la persona, en la
#  misma clave donde el tablero ya guarda lo demás.
# ══════════════════════════════════════════════════════════════

#  ── LOS CÁLCULOS, EN PALABRAS DE QUIEN NO ES CONTADOR ─────────
#  El Centro pidió explicarlos «muy bien y en palabras más
#  sencillas para los emprendedores».
#
#  Cada explicación responde a la pregunta que alguien se hace de
#  verdad, no a la definición de manual. «Punto de equilibrio» no
#  significa nada; «cuánto tengo que vender para no perder plata»
#  sí. Van dentro del grupo Cálculos, arriba, y se leen una vez:
#  quien ya sabe lo que es, cierra el grupo y sigue.
EXPLICACIONES = {
    "Cálculos": [
        ("Precio mínimo",
         "Lo mínimo que puedes cobrar sin perder dinero. Si cobras menos "
         "que eso, cada venta te cuesta plata en vez de dejarte."),
        ("Punto de equilibrio",
         "Cuánto tienes que vender en el mes para no perder ni ganar. "
         "Por debajo de esa cifra estás poniendo de tu bolsillo."),
        ("Runway",
         "Cuántos meses aguantas con la plata que tienes hoy si dejaras "
         "de vender mañana. Es el tiempo que te queda para reaccionar."),
        ("Asignación de dinero",
         "Cómo repartir lo que entra: cuánto es para el negocio, cuánto "
         "para impuestos y cuánto puedes sacar para ti sin ahogarlo."),
    ],
}


CSS = """
/* ═══════════════ GRUPOS PLEGABLES DEL ÍNDICE ═══════════════ */
/* El rótulo deja de ser un <div> muerto y pasa a ser un botón:
   se puede pulsar, tabular y leer con lector de pantalla. */
.navgroup-btn {
  display: flex; align-items: center; gap: 8px; width: 100%;
  background: none; border: 0; cursor: pointer;
  padding: 12px 14px 7px;
  font-family: inherit;
  font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase;
  font-weight: 700; color: #A9BEDE;
  text-align: left;
  transition: color .15s;
}
.navgroup-btn:hover { color: #FFFFFF; }
.navgroup-btn:focus-visible { outline: 2px solid #FFFFFF; outline-offset: -2px; }

/* El triángulo gira en vez de cambiar de símbolo: así el ojo sigue
   el mismo objeto y entiende «esto se abrió», no «apareció otra
   cosa». Y sin animación para quien la tenga desactivada. */
.navgroup-btn .flecha {
  flex: none; font-size: 9px; line-height: 1;
  transition: transform .18s ease;
  transform: rotate(90deg);
}
.navgroup-btn[aria-expanded="false"] .flecha { transform: rotate(0deg); }
@media (prefers-reduced-motion: reduce) { .navgroup-btn .flecha { transition: none; } }

.navgroup-btn .cuantos {
  margin-left: auto; font-size: 9.5px; letter-spacing: .06em;
  color: #7F97BE; font-weight: 600;
}
/* Cerrado, pero con la pestaña activa dentro: un punto avisa dónde
   está, para que nadie crea que su opción desapareció. */
.navgroup-btn .aqui {
  width: 5px; height: 5px; border-radius: 50%;
  background: #FFFFFF; margin-left: auto;
}

.navgroup-cuerpo[hidden] { display: none; }

/* ═══════════════ QUÉ SIGNIFICA CADA CÁLCULO ═══════════════ */
.navgroup-nota {
  margin: 2px 10px 8px; padding: 9px 11px;
  background: rgba(255,255,255,.055);
  border-left: 2px solid rgba(169,190,222,.5);
  border-radius: 0 6px 6px 0;
}
.navgroup-nota dt {
  font-size: 11px; font-weight: 700; color: #E7EEF9;
  margin-bottom: 1px;
}
.navgroup-nota dd {
  margin: 0 0 7px; font-size: 11px; line-height: 1.5; color: #B9C9E2;
}
.navgroup-nota dd:last-child { margin-bottom: 0; }

/* En el menú de móvil no hay grupos: son pastillas en una fila, y
   plegarlas ahí no ahorra nada. */
@media print { .navgroup-btn { color: #000; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   ÍNDICE LATERAL PLEGABLE
   ══════════════════════════════════════════════════════════ */

/* Las explicaciones de los cálculos, en palabras sencillas. */
var NOTAS_GRUPO = __EXPLICACIONES__;

/* Qué grupos están abiertos. Arranca con el de la pestaña activa,
   y se recuerda en el mismo sitio donde el tablero guarda todo. */
function gruposAbiertos(){
  if(!state.navAbierto || typeof state.navAbierto !== "object"){
    state.navAbierto = {};
    var actual = grupoDeTab(state.activeTab);
    if(actual) state.navAbierto[actual] = true;
  }
  return state.navAbierto;
}

function grupoDeTab(id){
  for(var i = 0; i < TABS.length; i++){
    for(var j = 0; j < TABS[i].items.length; j++){
      if(TABS[i].items[j].id === id) return TABS[i].group;
    }
  }
  return null;
}

function buildNav(container, mobile){
  container.innerHTML = "";

  /* El menú de móvil es una fila de pastillas: sin grupos, sin
     nada que plegar. Se deja tal como estaba. */
  if(mobile){
    TABS.forEach(function(group){
      group.items.forEach(function(item){
        container.appendChild(botonTab(item));
      });
    });
    return;
  }

  var abiertos = gruposAbiertos();
  var grupoActivo = grupoDeTab(state.activeTab);

  TABS.forEach(function(group){
    var abierto = abiertos[group.group] === true;
    var tieneLaActiva = group.group === grupoActivo;

    var cab = document.createElement("button");
    cab.className = "navgroup-btn";
    cab.type = "button";
    cab.setAttribute("aria-expanded", abierto ? "true" : "false");

    var cuerpoId = "navgrupo-" + group.group.replace(/[^A-Za-z]/g, "");
    cab.setAttribute("aria-controls", cuerpoId);
    cab.innerHTML =
      '<span class="flecha" aria-hidden="true">&#9654;</span>' +
      esc(group.group) +
      (abierto
        ? '<span class="cuantos">' + group.items.length + '</span>'
        : (tieneLaActiva
            ? '<span class="aqui" aria-hidden="true"></span>'
            : '<span class="cuantos">' + group.items.length + '</span>'));

    cab.addEventListener("click", function(){
      var ab = gruposAbiertos();
      ab[group.group] = !(ab[group.group] === true);
      saveState();
      buildNav(container, false);
    });
    container.appendChild(cab);

    var cuerpo = document.createElement("div");
    cuerpo.className = "navgroup-cuerpo";
    cuerpo.id = cuerpoId;
    if(!abierto) cuerpo.hidden = true;

    /* Si el grupo tiene explicación, va antes de sus opciones. */
    var notas = NOTAS_GRUPO[group.group];
    if(notas && notas.length){
      var dl = document.createElement("dl");
      dl.className = "navgroup-nota";
      notas.forEach(function(par){
        var dt = document.createElement("dt");
        dt.textContent = par[0];
        var dd = document.createElement("dd");
        dd.textContent = par[1];
        dl.appendChild(dt); dl.appendChild(dd);
      });
      cuerpo.appendChild(dl);
    }

    group.items.forEach(function(item){
      cuerpo.appendChild(botonTab(item));
    });
    container.appendChild(cuerpo);
  });
}

/* El botón de cada opción, igual que antes. Se saca aparte porque
   ahora lo usan el índice lateral y el menú de móvil. */
function botonTab(item){
  var btn = document.createElement("button");
  btn.className = "tab-btn" + (state.activeTab === item.id ? " active" : "");
  btn.setAttribute("data-tab", item.id);
  btn.innerHTML = '<span class="dot"></span>' + esc(item.label);
  btn.addEventListener("click", function(){
    state.activeTab = item.id;
    /* Al cambiar de pestaña se abre su grupo: si alguien llega
       desde el menú de móvil o desde un enlace, el índice tiene
       que mostrar dónde está parado. */
    var g = grupoDeTab(item.id);
    if(g) gruposAbiertos()[g] = true;
    saveState();
    renderAll();
    window.scrollTo(0, 0);
  });
  return btn;
}
"""


def js():
    import json
    return JS.replace("__EXPLICACIONES__", json.dumps(EXPLICACIONES, ensure_ascii=False))
