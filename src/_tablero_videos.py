# ══════════════════════════════════════════════════════════════
#  VIDEOS EXPLICATIVOS EN LA GUÍA DE USO
#
#  Cada término del tablero (punto de equilibrio, runway, flujo de
#  caja…) puede llevar un vídeo de YouTube que lo explique.
#
#  ── CÓMO SE AÑADE UN VÍDEO ────────────────────────────────────
#  Abajo, en VIDEOS, pon el identificador del vídeo junto a su
#  término. El identificador es lo que va después de «v=» en la
#  dirección de YouTube:
#
#      https://www.youtube.com/watch?v=dQw4w9WgXcQ
#                                     └────┬────┘
#                                    esto es lo que se pega
#
#  Los términos sin vídeo simplemente no muestran nada. No hace
#  falta ponerlos todos ni hacerlo de una vez.
#
#  ── POR QUÉ NO VIENEN YA PUESTOS ──────────────────────────────
#  Se buscaron, pero no se pudo comprobar uno por uno que sigan
#  disponibles, que estén en español y que el Centro quiera
#  avalarlos. Un enlace sin verificar dentro de una herramienta
#  de la Universidad lleva, con el tiempo, a un vídeo borrado o a
#  contenido que nadie revisó. El mecanismo está listo; los
#  enlaces los decide el Centro.
#
#  ── PRIVACIDAD ────────────────────────────────────────────────
#  El vídeo NO se carga al abrir la página: se ve la carátula y
#  solo al pulsar se inserta el reproductor. Así YouTube no sabe
#  quién abrió la herramienta, únicamente quién decidió ver un
#  vídeo. Se usa youtube-nocookie.com por lo mismo.
# ══════════════════════════════════════════════════════════════

#  término del tablero  ->  identificador de YouTube  ('' = sin vídeo)
#
#  Se eligieron los más cortos y directos de los verificados, no los
#  más completos: quien está llenando el tablero quiere entender un
#  término y volver, no ver una clase de veinte minutos.
#
#  Los cinco puestos existen y son públicos, comprobado uno a uno
#  con la API de YouTube. Lo que NO se pudo comprobar es el
#  contenido: si el Centro quiere avalar cada explicación, conviene
#  verlos antes de publicar. Quitar uno es borrar su identificador.
VIDEOS = {
    "Facturación vs. ganancia real":        "",
    "Ingresos por cliente y mes":           "",
    # «Gastos fijos y gastos variables», Aprende Con Ame.
    # El mismo vídeo sirve para los dos términos.
    "Gastos fijos":                         "OqCo9Fljxmw",
    "Gastos variables":                     "OqCo9Fljxmw",
    # «EL FLUJO DE CAJA Explicado Fácil y con Ejemplos»,
    # Contabilidad para Todos.
    "Flujo de caja proyectado":             "zIVOrdu2w1I",
    "Calculadora de precio mínimo":         "",
    # «Punto de equilibrio | Concepto FINANCIERO», Pablo
    # Aguirregomezcorta. Se prefiere al de nueve minutos: explica
    # el concepto sin el desarrollo completo del ejercicio.
    "Punto de equilibrio":                  "NkbrYt291ZU",
    # Sin vídeo: los que hay hablan de startups levantando capital
    # de inversores, no de un negocio que vive de lo que vende.
    "Runway (alerta de caja)":              "",
    # «¿Cómo separar las finanzas personales de las del negocio?»,
    # CoreWoman.
    "Separación negocio / personal":        "S2vwqa4H1uU",
    # Estos cuatro no son conceptos generales de finanzas: son
    # maneras de trabajar que definió este tablero. Un vídeo externo
    # no puede explicarlos porque no existen fuera de la herramienta.
    "Semáforo financiero":                  "",
    "Errores comunes en tracción temprana": "",
    "Rutina de cierre mensual":             "",
}


CSS = """
/* ═══════════════ VIDEOS DE LA GUÍA ═══════════════ */
.vid { margin-top: 14px; }
.vid-btn {
  display: flex; align-items: center; gap: .7rem; width: 100%;
  background: var(--paper-sunken); border: 1px solid var(--line);
  border-radius: 9px; padding: .7rem .85rem; cursor: pointer;
  text-align: left; font-family: inherit; color: var(--ink);
  transition: border-color .15s, background .15s;
}
.vid-btn:hover { border-color: var(--accent-strong); background: var(--accent-soft); }
.vid-play {
  flex: none; width: 34px; height: 34px; border-radius: 50%;
  background: var(--accent); color: #FFFFFF;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; padding-left: 3px;
}
.vid-txt { min-width: 0; }
.vid-txt b { display: block; font-size: 13px; font-weight: 600; }
.vid-txt span { font-size: 12px; color: var(--ink-soft); }
.vid-marco {
  position: relative; width: 100%; aspect-ratio: 16 / 9;
  margin-top: 10px; border-radius: 9px; overflow: hidden;
  background: #000; border: 1px solid var(--line);
}
.vid-marco iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
@media print { .vid { display: none !important; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   VIDEOS DE LA GUÍA
   El reproductor se inserta al pulsar, no al abrir la página:
   así YouTube solo sabe de quien decidió ver un vídeo.
   ══════════════════════════════════════════════════════════ */
var VIDEOS_GUIA = __VIDEOS__;

function bloqueVideo(titulo){
  var id = VIDEOS_GUIA[titulo];
  if(!id) return "";
  return (
    '<div class="vid">' +
      '<button class="vid-btn" type="button" data-video="' + esc(id) + '">' +
        '<span class="vid-play" aria-hidden="true">&#9654;</span>' +
        '<span class="vid-txt"><b>Ver explicación en video</b>' +
        '<span>Se abre aquí mismo, sin salir de la herramienta.</span></span>' +
      '</button>' +
    '</div>'
  );
}

document.addEventListener("click", function(e){
  var b = e.target.closest ? e.target.closest("[data-video]") : null;
  if(!b) return;
  var id = b.getAttribute("data-video");
  var caja = b.parentNode;
  var marco = document.createElement("div");
  marco.className = "vid-marco";
  var f = document.createElement("iframe");
  f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?rel=0&autoplay=1";
  f.title = "Video explicativo";
  f.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture";
  f.setAttribute("allowfullscreen", "");
  f.referrerPolicy = "strict-origin-when-cross-origin";
  marco.appendChild(f);
  caja.innerHTML = "";
  caja.appendChild(marco);
});
"""


def js():
    """El JS con el mapa de vídeos ya incrustado."""
    import json
    return JS.replace("__VIDEOS__", json.dumps(VIDEOS, ensure_ascii=False))
