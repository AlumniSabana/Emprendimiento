# ══════════════════════════════════════════════════════════════
#  LA FICHA, DE CORRIDO
#
#  Convierte el asistente de «una pregunta por pantalla» a una
#  sola página que se recorre hacia abajo, con racha de avance.
#
#  ── POR QUÉ ASÍ Y NO REESCRIBIENDO ────────────────────────────
#  Los diez renderers (renderSector, renderCIIU…) reciben un
#  «card» y pintan dentro. Ninguno sabe dónde está ese card ni
#  cuántos hay. Lo único que asume navegación es navRow().
#
#  Así que NO se toca ni un renderer: se cambia el motor que los
#  llama. render() deja de pintar uno y pinta todos, y navRow()
#  deja de ser «Atrás / Siguiente» para ser una marca de bloque
#  contestado. Un cálculo, una pregunta y un texto siguen
#  exactamente donde estaban, que es lo que hace este cambio
#  revisable.
#
#  ── LOS BLOQUES QUE DEPENDEN DE OTROS ─────────────────────────
#  «ciiu» necesita la descripción de la actividad y
#  «sector_especifico» solo aplica a ciertos sectores. No se
#  bloquean: aparecen en cuanto tienen la información que
#  necesitan, con una animación breve para que se note que
#  llegaron.
# ══════════════════════════════════════════════════════════════

CSS = """
/* ═══════════════ FICHA DE CORRIDO ═══════════════ */

/* La barra de «Paso 3 de 10» sobra: contaba una navegación que ya
   no existe, y la racha de arriba dice lo mismo mejor. Se oculta
   en vez de borrarla del marcado porque los renderers todavía la
   referencian, y quitarla obligaría a tocar los diez. */
.progress-wrap { display: none !important; }

/* Cada pregunta es un bloque de la misma página. El card ya
   existía; aquí solo se le da aire entre uno y otro y un ancla
   para que el desplazamiento no deje el título pegado arriba. */
.bloque { scroll-margin-top: calc(var(--alto-volver) + 76px); }
.bloque + .bloque { margin-top: 1.15rem; }

/* Un bloque que aparece porque ya se puede contestar. La
   animación es corta a propósito: avisa, no entretiene. */
@keyframes bloque-entra {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: none; }
}
.bloque-nuevo { animation: bloque-entra .32s ease-out; }
@media (prefers-reduced-motion: reduce) { .bloque-nuevo { animation: none; } }

/* La marca de «ya contestaste esto». Sustituye a la fila de
   botones Atrás/Siguiente, que en una página de corrido no
   tiene sentido. */
.bloque-hecho {
  display: flex; align-items: center; gap: .45rem;
  margin-top: 1rem; padding-top: .85rem;
  border-top: 1px solid var(--line);
  color: var(--accent-ink); font-size: .82rem; font-weight: 600;
}
.bloque-hecho .tic {
  display: inline-flex; align-items: center; justify-content: center;
  width: 18px; height: 18px; border-radius: 50%;
  background: var(--accent-soft); color: var(--accent-ink);
  font-size: .68rem; flex: none;
}
.bloque-pendiente {
  margin-top: 1rem; padding-top: .85rem;
  border-top: 1px solid var(--line);
  color: var(--text-muted); font-size: .82rem;
}

/* ── La racha ──
   Va pegada arriba, bajo la barra de volver, porque su trabajo
   es acompañar mientras se baja. Si se quedara en la cabecera
   dejaría de verse justo cuando empieza a servir. */
.racha {
  position: sticky; top: var(--alto-volver); z-index: 40;
  background: var(--surface);
  border-bottom: 1px solid var(--line);
  padding: .6rem 0;
}
.racha-env {
  max-width: 760px; margin: 0 auto;
  padding: 0 clamp(1rem, 4vw, 1.5rem);
  display: flex; align-items: center; gap: .85rem;
}
.racha-barra {
  flex: 1; height: 6px; border-radius: 3px;
  background: var(--surface-2); overflow: hidden;
}
.racha-relleno {
  height: 100%; width: 0%; border-radius: 3px;
  background: var(--accent-btn);
  transition: width .45s cubic-bezier(.4,0,.2,1);
}
.racha-cuenta {
  font-family: var(--mono); font-size: .78rem;
  color: var(--text); font-weight: 600; white-space: nowrap;
}
/* Las estrellas: una por cada tramo de preguntas. Se encienden
   al llegar, no antes, y la que acaba de encenderse late una vez. */
.racha-estrellas { display: flex; gap: .22rem; flex: none; }
.estrella {
  width: 17px; height: 17px; display: block;
  color: var(--line-strong);
  transition: color .3s, transform .3s;
}
.estrella.on { color: #C9971F; }
@keyframes estrella-late {
  0% { transform: scale(1); } 45% { transform: scale(1.42); } 100% { transform: scale(1); }
}
.estrella.late { animation: estrella-late .5s ease-out; }
@media (prefers-reduced-motion: reduce) { .estrella.late { animation: none; } }

/* El aviso de racha conseguida. Aparece un momento y se va: no
   se puede cerrar porque no interrumpe nada. */
.racha-aviso {
  position: fixed; left: 50%; bottom: 1.6rem; transform: translateX(-50%) translateY(0);
  z-index: 60; max-width: min(92vw, 380px);
  background: var(--accent-btn); color: var(--accent-contrast);
  border-radius: 9px; padding: .8rem 1.15rem;
  box-shadow: 0 10px 30px -10px rgba(0,20,89,.5);
  font-size: .88rem; line-height: 1.45;
  display: flex; align-items: center; gap: .7rem;
  opacity: 0; pointer-events: none;
  transition: opacity .3s, transform .3s;
}
.racha-aviso.ver { opacity: 1; transform: translateX(-50%) translateY(-6px); }
/* A la derecha y no centrado: centrado abajo se planta justo
   encima de la fila de opciones que la persona está eligiendo. */
@media (min-width: 720px) {
  .racha-aviso { left: auto; right: 1.5rem; transform: translateY(0); }
  .racha-aviso.ver { transform: translateY(-6px); }
}
.racha-aviso b { display: block; font-size: .93rem; }
.racha-aviso .ico { font-size: 1.3rem; flex: none; }
@media (prefers-reduced-motion: reduce) { .racha-aviso { transition: opacity .3s; } }
@media (max-width: 560px) { .racha-env { gap: .6rem; } .racha-estrellas { gap: .15rem; } }
@media print { .racha, .racha-aviso { display: none !important; } }
"""


# El <div> de la racha, que se inserta después de la barra de volver.
MARCADO = """<div class="racha" id="racha" hidden>
  <div class="racha-env">
    <div class="racha-estrellas" id="rachaEstrellas" aria-hidden="true"></div>
    <div class="racha-barra"><div class="racha-relleno" id="rachaRelleno"></div></div>
    <span class="racha-cuenta" id="rachaCuenta" role="status" aria-live="polite"></span>
  </div>
</div>
<div class="racha-aviso" id="rachaAviso" role="status" aria-live="polite">
  <span class="ico" aria-hidden="true">&#9733;</span>
  <span><b id="rachaAvisoT"></b><span id="rachaAvisoD"></span></span>
</div>
"""


# ── El motor nuevo ────────────────────────────────────────────
# Sustituye a render(), navRow() y updateProgress(). Se inyecta
# justo antes de la llamada final a render().
MOTOR = r"""
  /* ══════════════════════════════════════════════════════════
     DE CORRIDO, CON RACHA
     ----------------------------------------------------------
     Antes: un paso visible y nueve escondidos.
     Ahora: todos los que ya se pueden contestar, en una página.

     «contestado(id)» decide si un bloque cuenta como hecho. Es
     la misma condición que antes desactivaba el botón Siguiente,
     así que no inventa criterios nuevos.
     ══════════════════════════════════════════════════════════ */
  const RACHA_CADA = 2;        /* una estrella por cada 2 respuestas */

  const rachaCaja      = document.getElementById("racha");
  const rachaEstrellas = document.getElementById("rachaEstrellas");
  const rachaRelleno   = document.getElementById("rachaRelleno");
  const rachaCuenta    = document.getElementById("rachaCuenta");
  const rachaAviso     = document.getElementById("rachaAviso");
  const rachaAvisoT    = document.getElementById("rachaAvisoT");
  const rachaAvisoD    = document.getElementById("rachaAvisoD");

  let estrellasDadas = 0;
  let avisoTimer = null;

  /* Qué bloques están contestados.
     NO se reimplementa el criterio de cada uno: cada renderer ya
     lo calcula y se lo entrega a navRow() como «nextDisabled».
     Este mapa lo recoge de ahí mientras se pinta.

     Duplicarlos aquí era la alternativa, y habría bastado con que
     alguien cambiara una validación dentro de su renderer para
     que la racha empezara a mentir sin que nadie lo notara. */
  const hechoPorBloque = new Map();
  let bloqueEnCurso = null;

  function contestado(id) { return hechoPorBloque.get(id) === true; }

  /* Un bloque se muestra cuando tiene la información que necesita.
     No es un candado: es que antes no tendría nada que enseñar. */
  function visible(id) {
    if (!isApplicable(id)) return false;
    if (id === "ciiu") return (state.actividadDescripcion || "").trim().length >= 5;
    if (id === "resultado") return preguntasIds().every(contestado);
    return true;
  }

  function preguntasIds() {
    return STEP_IDS.filter(id => id !== "resultado" && isApplicable(id));
  }

  function estrellaSVG() {
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("viewBox", "0 0 24 24");
    s.setAttribute("class", "estrella");
    s.setAttribute("fill", "currentColor");
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    p.setAttribute("d", "M12 2.6l2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5L2.6 9.4l6.5-.9z");
    s.appendChild(p);
    return s;
  }

  function mostrarAvisoRacha(titulo, detalle) {
    rachaAvisoT.textContent = titulo;
    rachaAvisoD.textContent = detalle;
    rachaAviso.classList.add("ver");
    clearTimeout(avisoTimer);
    avisoTimer = setTimeout(() => rachaAviso.classList.remove("ver"), 3400);
  }

  function pintarRacha() {
    const ids = preguntasIds();
    const hechas = ids.filter(contestado).length;
    const total = ids.length;
    /* Las metas se reparten sobre el total, no cada N a secas: con
       9 preguntas y una estrella cada 2 salían 5 metas y la última
       pedía 10 respuestas que no existen. Quedaba una estrella
       imposible de encender, que es justo lo contrario de animar.
       Ahora la última estrella cae exactamente al completar. */
    const metas = Math.max(1, Math.floor(total / RACHA_CADA));
    const porMeta = total / metas;
    const ganadas = Math.min(metas, Math.floor(hechas / porMeta));

    rachaCaja.hidden = false;
    rachaRelleno.style.width = Math.round((hechas / total) * 100) + "%";
    rachaCuenta.textContent = hechas + " de " + total;

    if (rachaEstrellas.children.length !== metas) {
      rachaEstrellas.innerHTML = "";
      for (let i = 0; i < metas; i++) rachaEstrellas.appendChild(estrellaSVG());
    }
    Array.from(rachaEstrellas.children).forEach((s, i) => {
      s.classList.toggle("on", i < ganadas);
    });

    if (ganadas > estrellasDadas) {
      const nueva = rachaEstrellas.children[ganadas - 1];
      if (nueva) { nueva.classList.add("late"); setTimeout(() => nueva.classList.remove("late"), 520); }
      if (hechas >= total) {
        mostrarAvisoRacha("¡Ficha completa!", "Baja para ver tus trámites, entidades y documentos.");
      } else {
        mostrarAvisoRacha("¡" + ganadas + (ganadas === 1 ? " estrella!" : " estrellas!"),
                          "Llevas " + hechas + " de " + total + ". Te faltan " + (total - hechas) + ".");
      }
    }
    estrellasDadas = ganadas;
  }

  /* navRow ya no navega: marca el bloque como contestado o dice
     qué falta. Conserva el nombre y la firma porque la llaman
     los diez renderers y no se van a tocar. */
  function navRow(card, opciones) {
    const o = opciones || {};
    const listo = !o.nextDisabled;
    if (bloqueEnCurso) hechoPorBloque.set(bloqueEnCurso, listo);

    if (!listo) {
      card.appendChild(el("p", { class: "bloque-pendiente" }, "Contesta para continuar."));
      return;
    }
    const fila = el("div", { class: "bloque-hecho" });
    fila.appendChild(el("span", { class: "tic", "aria-hidden": "true" }, "✓"));
    fila.appendChild(el("span", {}, "Listo"));
    card.appendChild(fila);
  }

  /* updateProgress la llaman los renderers; con la racha arriba
     ya no hace falta la barra de pasos, pero se conserva la
     función vacía para no tocarlos. */
  function updateProgress() {}

  let vistos = new Set();
  let repintando = false;

  /* Los campos de texto actualizan el estado pero NO repintaban:
     su «oninput» solo tocaba el botón Siguiente de su propia
     tarjeta. Con navegación por pasos bastaba; de corrido, la
     racha y los bloques que dependen de ese texto se quedaban
     congelados hasta que la persona tocara otra cosa.

     Se repinta con retardo y no en cada tecla: repintar mientras
     alguien escribe una frase entera es trabajo tirado, y aunque
     el foco se restaura, hacerlo 40 veces se nota. */
  let repintarTimer = null;
  function repintarPronto() {
    clearTimeout(repintarTimer);
    repintarTimer = setTimeout(render, 420);
  }

  main.addEventListener("input", (e) => {
    const t = e.target;
    if (t && (t.tagName === "TEXTAREA" || t.tagName === "INPUT")) repintarPronto();
  });

  function render() {
    /* Se recuerda dónde estaba el cursor para devolverlo después:
       repintar todo con cada tecla movería el foco al principio y
       escribir sería imposible. */
    const act = document.activeElement;
    const focoId = act && act.id ? act.id : null;
    const selIni = act && act.selectionStart != null ? act.selectionStart : null;
    const selFin = act && act.selectionEnd != null ? act.selectionEnd : null;

    main.innerHTML = "";
    const aMostrar = STEP_IDS.filter(visible);

    aMostrar.forEach(id => {
      const card = el("div", { class: "card bloque" });
      card.id = "bloque-" + id;
      if (!vistos.has(id)) card.classList.add("bloque-nuevo");
      main.appendChild(card);
      /* El renderer llamará a navRow() y allí se registra si este
         bloque quedó contestado. «resultado» no llama a navRow,
         así que se marca aparte. */
      bloqueEnCurso = id;
      hechoPorBloque.set(id, id === "sector_especifico" || id === "resultado");
      STEP_RENDERERS[id](card);
      bloqueEnCurso = null;
    });

    aMostrar.forEach(id => vistos.add(id));
    pintarRacha();

    /* «resultado» solo se muestra cuando todas están contestadas,
       pero eso no se sabe hasta terminar de pintar: cada navRow()
       lo va registrando sobre la marcha. Así que la vuelta en que
       se completa la última pregunta, el resultado todavía no
       estaba en la lista. Se repinta una vez, y solo una: el
       guardián «repintando» evita que se llame a sí misma. */
    if (!repintando && visible("resultado") && aMostrar.indexOf("resultado") < 0) {
      repintando = true;
      render();
      repintando = false;
    }

    if (focoId) {
      const otra = document.getElementById(focoId);
      if (otra && typeof otra.focus === "function") {
        otra.focus({ preventScroll: true });
        if (selIni != null && otra.setSelectionRange) {
          try { otra.setSelectionRange(selIni, selFin); } catch (_) {}
        }
      }
    }
  }
"""
