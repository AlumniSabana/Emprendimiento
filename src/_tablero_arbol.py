# ══════════════════════════════════════════════════════════════
#  EL ÁRBOL DE LA GUÍA
#
#  El Centro pidió «un estimulante de crecimiento por cada lección
#  que lean y por cada vídeo que vean, como un árbol creciendo».
#
#  ── QUÉ CUENTA ────────────────────────────────────────────────
#  Doce secciones de la guía y siete vídeos: diecinueve pasos. El
#  árbol pasa por seis etapas, de semilla a árbol con frutos.
#
#  ── LO QUE DICE EL RÓTULO ─────────────────────────────────────
#  «Has abierto 3 de 12 secciones», no «has leído 3 lecciones».
#  Abrir un acordeón es lo único que la página puede saber; decir
#  «leídas» sería afirmar algo que no le consta. La diferencia
#  parece menor hasta que alguien abre las doce en diez segundos y
#  la herramienta lo felicita por haber estudiado.
#
#  Con los vídeos pasa lo mismo: se cuenta el que se abre, no el
#  que se termina. YouTube no le cuenta a esta página cuánto se
#  vio, y montar su API para saberlo significaría cargar código de
#  Google en una herramienta que hoy funciona sin conexión.
#
#  ── POR QUÉ SE GUARDA ─────────────────────────────────────────
#  En el mismo sitio donde el tablero guarda todo lo demás. Un
#  árbol que vuelve a ser semilla cada vez que se cierra la pestaña
#  no estimula nada: se lee como que el trabajo no contó.
#
#  ── NO HAY PREMIO QUE PERDER ──────────────────────────────────
#  El árbol solo crece. No se marchita por no entrar, no hay rachas
#  que romper ni avisos de que se va a perder el progreso. Esto es
#  una guía de consulta de una herramienta financiera: quien la usa
#  está tratando de entender por qué no le cuadran las cuentas, y
#  presionarlo para que vuelva mañana sería usar su ansiedad como
#  motor. Crece cuando vuelve, y espera cuando no.
# ══════════════════════════════════════════════════════════════

VERDE       = "#158A5E"
VERDE_OSC   = "#0E6644"
VERDE_CLA   = "#4DA882"
TRONCO      = "#8A5200"
TRONCO_OSC  = "#6E4200"
TIERRA      = "#C9D3E4"
TIERRA_OSC  = "#A9B7CE"
FRUTO       = "#A3252F"
SEMILLA     = "#8A5200"


def _suelo():
    """La tierra, igual en las seis etapas: el árbol cambia, el
    suelo no. Si se moviera, el ojo leería que cambió la escena en
    vez de que creció la planta."""
    return (f'<ellipse cx="60" cy="134" rx="42" ry="7" fill="{TIERRA}"/>'
            f'<path d="M22 134 Q60 126 98 134" fill="none" '
            f'stroke="{TIERRA_OSC}" stroke-width="1.5"/>')


#  Las seis etapas. Cada una es un dibujo completo, no una capa que
#  se enciende: así cada estado se puede mirar y corregir solo.
ETAPAS = [
    # 0 · la semilla, todavía bajo tierra
    f"""{_suelo()}
  <ellipse cx="60" cy="130" rx="6" ry="4.5" fill="{SEMILLA}"/>
  <path d="M60 126 L60 122" stroke="{VERDE}" stroke-width="2" stroke-linecap="round"/>""",

    # 1 · el brote: dos hojas y poco más
    f"""{_suelo()}
  <path d="M60 132 L60 112" stroke="{VERDE_OSC}" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M60 118 Q47 112 45 120 Q54 124 60 118 Z" fill="{VERDE}"/>
  <path d="M60 115 Q73 109 75 117 Q66 121 60 115 Z" fill="{VERDE_CLA}"/>""",

    # 2 · tallo firme, cuatro hojas
    f"""{_suelo()}
  <path d="M60 132 L60 96" stroke="{TRONCO}" stroke-width="3" stroke-linecap="round"/>
  <path d="M60 120 Q44 113 41 123 Q53 128 60 120 Z" fill="{VERDE}"/>
  <path d="M60 116 Q76 109 79 119 Q67 124 60 116 Z" fill="{VERDE_CLA}"/>
  <path d="M60 104 Q47 98 45 106 Q55 110 60 104 Z" fill="{VERDE}"/>
  <path d="M60 100 Q73 94 75 102 Q65 106 60 100 Z" fill="{VERDE_CLA}"/>""",

    # 3 · ya es un arbolito: tronco, ramas y copa
    f"""{_suelo()}
  <path d="M60 132 L60 88" stroke="{TRONCO}" stroke-width="4" stroke-linecap="round"/>
  <path d="M60 104 L47 94 M60 100 L73 90" stroke="{TRONCO}" stroke-width="2.5" stroke-linecap="round"/>
  <circle cx="60" cy="76" r="17" fill="{VERDE}"/>
  <circle cx="47" cy="84" r="11" fill="{VERDE_CLA}"/>
  <circle cx="73" cy="84" r="11" fill="{VERDE_OSC}"/>""",

    # 4 · árbol joven, copa ancha
    f"""{_suelo()}
  <path d="M60 132 L60 80" stroke="{TRONCO}" stroke-width="5" stroke-linecap="round"/>
  <path d="M60 100 L44 88 M60 96 L76 84" stroke="{TRONCO}" stroke-width="3" stroke-linecap="round"/>
  <circle cx="60" cy="62" r="22" fill="{VERDE}"/>
  <circle cx="40" cy="74" r="15" fill="{VERDE_CLA}"/>
  <circle cx="80" cy="74" r="15" fill="{VERDE_OSC}"/>
  <circle cx="60" cy="80" r="14" fill="{VERDE}"/>""",

    # 5 · el árbol dando fruto
    f"""{_suelo()}
  <path d="M60 132 L60 76" stroke="{TRONCO_OSC}" stroke-width="6" stroke-linecap="round"/>
  <path d="M60 98 L41 84 M60 94 L79 80 M60 108 L48 100" stroke="{TRONCO_OSC}"
        stroke-width="3" stroke-linecap="round"/>
  <circle cx="60" cy="54" r="25" fill="{VERDE}"/>
  <circle cx="35" cy="70" r="17" fill="{VERDE_CLA}"/>
  <circle cx="85" cy="70" r="17" fill="{VERDE_OSC}"/>
  <circle cx="60" cy="76" r="17" fill="{VERDE}"/>
  <circle cx="44" cy="50" r="13" fill="{VERDE_CLA}"/>
  <circle cx="77" cy="50" r="13" fill="{VERDE_OSC}"/>
  <circle cx="47" cy="66" r="4" fill="{FRUTO}"/>
  <circle cx="72" cy="60" r="4" fill="{FRUTO}"/>
  <circle cx="60" cy="80" r="4" fill="{FRUTO}"/>
  <circle cx="63" cy="44" r="4" fill="{FRUTO}"/>""",
]


#  Qué se dice en cada etapa. Describe la planta, no felicita a la
#  persona: «vas muy bien» suena a aplauso automático y se nota.
ROTULOS = [
    "Aquí está la semilla.",
    "Salió el primer brote.",
    "Ya echó hojas.",
    "Se está haciendo árbol.",
    "Árbol joven, con buena copa.",
    "Árbol completo, y dando fruto.",
]


CSS = """
/* ═══════════════ EL AVISO DE LA ASIGNACIÓN ═══════════════
   Tres estados con tres pesos distintos. Pasarse del 100% es el
   único que es un error de verdad, así que es el único que grita:
   los otros dos informan. */
.alloc-aviso {
  margin: 14px 0 4px; padding: 11px 13px;
  border-radius: 0 8px 8px 0;
  font-size: 13px; line-height: 1.55;
}
.alloc-aviso b { display: block; margin-bottom: 2px; }
.alloc-aviso span { display: block; }

.alloc-aviso.pasado {
  background: var(--critical-soft);
  border: 1px solid var(--critical);
  border-left-width: 4px;
  color: var(--ink);
}
.alloc-aviso.pasado b { color: var(--critical); font-size: 13.5px; }

.alloc-aviso.corto {
  background: var(--warn-soft);
  border-left: 3px solid var(--warn);
  color: var(--ink);
}
.alloc-aviso.corto b { color: var(--warn); }

.alloc-aviso.bien {
  background: var(--good-soft);
  border-left: 3px solid var(--good);
  color: var(--ink);
}
.alloc-aviso.bien b { color: var(--good); }

/* La marca de dónde estaba el 100%, cuando se cruzó. Va encima de
   la barra, así que la barra tiene que dejar de recortar por los
   lados para que la etiqueta no se corte. */
.alloc-bar { position: relative; overflow: visible !important; }
.alloc-bar > .alloc-seg:first-child { border-radius: 7px 0 0 7px; }
.alloc-bar > .alloc-seg:last-of-type { border-radius: 0 7px 7px 0; }
.alloc-limite {
  position: absolute; top: -5px; bottom: -5px; width: 0;
  border-left: 2px dashed var(--critical);
  pointer-events: none;
}
.alloc-limite span {
  position: absolute; top: -17px; left: 50%; transform: translateX(-50%);
  font-family: var(--font-mono); font-size: 10px; font-weight: 700;
  color: var(--critical); background: var(--paper-raised);
  padding: 0 4px; white-space: nowrap;
}

/* ═══════════════ EL ÁRBOL DE LA GUÍA ═══════════════ */
.arbol-caja {
  display: flex; align-items: center; gap: 18px;
  background: var(--paper-raised); border: 1px solid var(--line);
  border-radius: 12px; padding: 16px 18px; margin-bottom: 16px;
  box-shadow: var(--shadow);
}
.arbol-dibujo {
  flex: none; width: 96px; height: 116px;
  display: flex; align-items: flex-end; justify-content: center;
}
.arbol-dibujo svg { width: 100%; height: 100%; overflow: visible; }

/* Al pasar de etapa, la planta entra creciendo desde su base. Es
   el único movimiento de la herramienta y dura poco: lo que tiene
   que notarse es que algo cambió, no la animación. */
@keyframes arbol-crece {
  from { transform: scale(.82); opacity: .3; }
  to   { transform: scale(1);   opacity: 1; }
}
.arbol-dibujo.creciendo svg {
  animation: arbol-crece .5s cubic-bezier(.2,.8,.3,1);
  transform-origin: 50% 90%;
}
@media (prefers-reduced-motion: reduce) {
  .arbol-dibujo.creciendo svg { animation: none; }
}

.arbol-texto { min-width: 0; flex: 1; }
.arbol-texto h3 { margin: 0 0 3px; font-size: 15px; }
.arbol-texto p { margin: 0 0 10px; font-size: 12.5px; color: var(--ink-soft); line-height: 1.5; }
.arbol-barra {
  height: 7px; border-radius: 99px; background: var(--paper-sunken);
  overflow: hidden; margin-bottom: 7px;
}
.arbol-barra span {
  display: block; height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, #4DA882, #158A5E);
  transition: width .5s cubic-bezier(.2,.8,.3,1);
}
.arbol-cuenta {
  display: flex; gap: 14px; flex-wrap: wrap;
  font-size: 11.5px; color: var(--ink-soft);
}
.arbol-cuenta b { color: var(--ink); font-variant-numeric: tabular-nums; }

@media (max-width: 560px) {
  .arbol-caja { flex-direction: column; align-items: flex-start; }
  .arbol-dibujo { width: 78px; height: 94px; align-self: center; }
}
@media print { .arbol-caja { display: none !important; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   EL ÁRBOL QUE CRECE CON LA GUÍA
   ══════════════════════════════════════════════════════════ */
var ARBOL_ETAPAS  = __ETAPAS__;
var ARBOL_ROTULOS = __ROTULOS__;

/* Lo visto, guardado donde el tablero guarda todo lo demás. */
function progresoGuia(){
  if(!state.guiaVistas || typeof state.guiaVistas !== "object") state.guiaVistas = {};
  if(!state.guiaVideos || typeof state.guiaVideos !== "object") state.guiaVideos = {};
  return state.guiaVistas;
}

function cuentaGuia(){
  progresoGuia();
  var secciones = Object.keys(state.guiaVistas).length;
  var videos    = Object.keys(state.guiaVideos).length;
  var totalSec  = GUIDE.length;
  /* Cuántos términos de la guía tienen vídeo. Se cuenta en vez de
     escribir el número a mano: al añadir o quitar uno en
     _tablero_videos.py, la barra sigue cuadrando sola. */
  var totalVid = 0;
  for(var k in VIDEOS_GUIA){ if(VIDEOS_GUIA[k]) totalVid++; }
  return {
    secciones: Math.min(secciones, totalSec), totalSec: totalSec,
    videos: Math.min(videos, totalVid),       totalVid: totalVid,
    hechos: Math.min(secciones, totalSec) + Math.min(videos, totalVid),
    total:  totalSec + totalVid
  };
}

function etapaArbol(c){
  if(c.hechos <= 0) return 0;
  /* Cinco saltos repartidos por igual sobre el total. El primero
     llega pronto a propósito: la planta tiene que moverse la
     primera vez que alguien abre algo, o no se entiende que el
     dibujo responde a lo que uno hace. */
  var paso = c.total / 5;
  return Math.min(5, Math.max(1, Math.ceil(c.hechos / paso)));
}

function bloqueArbol(){
  var c = cuentaGuia();
  var etapa = etapaArbol(c);
  var pct = c.total > 0 ? Math.round((c.hechos / c.total) * 100) : 0;

  return '<div class="arbol-caja">' +
    '<div class="arbol-dibujo" id="arbolDibujo" data-etapa="' + etapa + '">' +
      '<svg viewBox="0 0 120 145" role="img" aria-label="' +
        esc(ARBOL_ROTULOS[etapa] + " Has abierto " + c.hechos + " de " + c.total + ".") + '">' +
        ARBOL_ETAPAS[etapa] +
      '</svg>' +
    '</div>' +
    '<div class="arbol-texto">' +
      '<h3>' + esc(ARBOL_ROTULOS[etapa]) + '</h3>' +
      '<p>Crece cada vez que abres una sección o pones un video. ' +
         'Puedes volver cuando quieras: lo que ya abriste queda.</p>' +
      '<div class="arbol-barra"><span style="width:' + pct + '%"></span></div>' +
      '<div class="arbol-cuenta">' +
        '<span>Secciones abiertas <b>' + c.secciones + ' de ' + c.totalSec + '</b></span>' +
        '<span>Videos abiertos <b>' + c.videos + ' de ' + c.totalVid + '</b></span>' +
      '</div>' +
    '</div>' +
  '</div>';
}

/* Apuntar lo visto y repintar solo el árbol.
   No se llama a renderAll(): eso reconstruye el panel entero y
   cerraría de golpe el acordeón que la persona acaba de abrir. */
function apuntarGuia(tipo, clave){
  progresoGuia();
  var donde = (tipo === "video") ? state.guiaVideos : state.guiaVistas;
  if(donde[clave]) return;            /* ya estaba: no hay nada que celebrar */
  donde[clave] = true;
  saveState();
  repintarArbol();
}

function repintarArbol(){
  var viejo = document.querySelector(".arbol-caja");
  if(!viejo) return;
  var antes = document.getElementById("arbolDibujo");
  var etapaAntes = antes ? antes.getAttribute("data-etapa") : null;

  var temp = document.createElement("div");
  temp.innerHTML = bloqueArbol();
  var nuevo = temp.firstChild;
  viejo.parentNode.replaceChild(nuevo, viejo);

  /* La animación solo cuando de verdad cambió de etapa. Repetirla
     en cada clic la vuelve ruido. */
  var ahora = nuevo.querySelector("#arbolDibujo");
  if(ahora && etapaAntes !== null && ahora.getAttribute("data-etapa") !== etapaAntes){
    ahora.classList.add("creciendo");
  }
}
"""


def js():
    import json
    return (JS
            .replace("__ETAPAS__", json.dumps([e.strip() for e in ETAPAS], ensure_ascii=False))
            .replace("__ROTULOS__", json.dumps(ROTULOS, ensure_ascii=False)))
