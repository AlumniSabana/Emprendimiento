# ══════════════════════════════════════════════════════════════
#  ASPECTO DE FICHA INSTITUCIONAL
#
#  La ficha de negocio se ve como un formulario oficial —el de una
#  Secretaría de Salud, una Cámara de Comercio— y no como un
#  cuestionario web: rejilla de celdas con borde marcado, etiqueta
#  dentro de la celda, franja de título en negro.
#
#  ── QUÉ CAMBIA Y QUÉ NO ───────────────────────────────────────
#  Solo la presentación. Las nueve preguntas, su orden, su lógica
#  y el resultado son los mismos. Ni un renderer se toca: se
#  reescribe cómo se ven las piezas que ya pintan.
#
#  ── POR QUÉ NO SE COPIA EL DOCUMENTO ENTERO ───────────────────
#  El formulario de referencia lleva escudos de la Secretaría de
#  Salud y del Gobierno de Chiapas. Esta herramienta es de la
#  Universidad de La Sabana: usa su azul y su escudo. Se toma la
#  FORMA —la rejilla, las celdas, la franja— no la identidad de
#  otra institución, que sería suplantarla.
# ══════════════════════════════════════════════════════════════

CSS = """
/* ═══════════════ ASPECTO DE FICHA OFICIAL ═══════════════ */

/* El documento entero es una hoja: fondo blanco, borde negro
   marcado y nada de sombras. Un formulario impreso no flota. */
.card.bloque {
  border: 1px solid #C3CFE3;
  border-radius: 0;
  box-shadow: none;
  padding: 0;
  overflow: hidden;
}
.bloque + .bloque { margin-top: -2px; }   /* bordes compartidos */

/* La franja de sección: negra, centrada, en versales.
   Sustituye a la etiqueta pequeña de color que había antes. */
.bloque .section-tag {
  display: block; width: 100%;
  background: var(--accent-btn); color: #FFFFFF;
  border: 0; border-radius: 0;
  padding: .42rem .9rem;
  font-family: var(--sans);
  font-size: .72rem; font-weight: 700;
  letter-spacing: .1em; text-transform: uppercase;
  text-align: center;
}

/* La pregunta va en una celda con fondo gris, como los rótulos
   del formulario de referencia. */
.bloque .question {
  margin: 0;
  padding: .62rem .9rem;
  background: #E9EBF0;
  border-bottom: 1px solid #C3CFE3;
  font-family: var(--sans);
  font-size: .95rem; font-weight: 700;
  color: var(--ink); line-height: 1.4;
}
.bloque .hint {
  margin: 0;
  padding: .5rem .9rem;
  font-size: .82rem; line-height: 1.5;
  color: var(--text);
  border-bottom: 1px solid #C9CFDC;
  background: #FFFFFF;
}

/* Los campos: celda con borde, sin esquinas redondeadas.
   La caja de escritura ocupa la celda entera, como una casilla
   de formulario que se rellena. */
.bloque .field-group { padding: 0; }
.bloque textarea,
.bloque input[type="text"],
.bloque input[type="number"],
.bloque select {
  width: 100%;
  border: 0;
  border-bottom: 1px solid #C9CFDC;
  border-radius: 0;
  background: #FFFFFF;
  padding: .6rem .9rem;
  font-family: var(--sans);
  font-size: .93rem;
  color: var(--ink);
}
/* La caja de escritura se separa de la ayuda con su propia línea
   y un fondo apenas distinto: sin esto flotaban las dos juntas en
   el mismo blanco y no se veía dónde empezaba el campo. */
.bloque textarea,
.bloque input[type="text"],
.bloque input[type="number"] {
  border-top: 1px solid #C9CFDC;
  background: #FCFDFE;
}
.bloque textarea { min-height: 4.2rem; resize: vertical; }
.bloque textarea:focus,
.bloque input:focus,
.bloque select:focus {
  outline: 2px solid var(--accent-btn);
  outline-offset: -2px;
  background: #FBFCFE;
}

/* Las opciones: casillas en rejilla, con el rótulo dentro de su
   celda y borde entre una y otra. Es lo que hace que se lea como
   un formulario y no como una fila de botones. */
.bloque .btn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 0;
  padding: 0;
  border-bottom: 1px solid #C9CFDC;
  border-top: 1px solid #C9CFDC;
}
/* La última casilla de cada fila no lleva borde derecho: si no,
   queda una línea suelta contra el borde del documento. */
.bloque .choice-btn:last-child { border-right: 0; }
.bloque .choice-btn {
  border: 0;
  border-right: 1px solid #C9CFDC;
  border-bottom: 1px solid #C9CFDC;
  border-radius: 0;
  background: #FFFFFF;
  padding: .58rem .8rem .58rem 2.1rem;
  text-align: left;
  font-family: var(--sans);
  font-size: .88rem;
  color: var(--ink);
  position: relative;
  min-height: 2.5rem;
  display: flex; align-items: center;
  transition: background .12s;
}
/* La casilla de verificación, dibujada a la izquierda. Un
   formulario oficial tiene casillas, no botones que se iluminan. */
.bloque .choice-btn::before {
  content: "";
  position: absolute; left: .75rem; top: 50%;
  transform: translateY(-50%);
  width: 13px; height: 13px;
  border: 1.5px solid #6B7280;
  background: #FFFFFF;
}
.bloque .choice-btn:hover { background: #F3F5F9; }
.bloque .choice-btn.selected {
  background: var(--accent-soft);
  font-weight: 600;
  color: var(--accent-ink);
}
.bloque .choice-btn.selected::before {
  background: var(--accent-btn);
  border-color: var(--accent-btn);
}
/* La marca dentro de la casilla marcada. El «✓ » que el archivo
   original ponía como texto se retira: aquí lo dibuja la casilla. */
.bloque .choice-btn.selected::after {
  content: "";
  position: absolute; left: 1.03rem; top: 50%;
  width: 4px; height: 8px;
  border: solid #FFFFFF;
  border-width: 0 2px 2px 0;
  transform: translateY(-62%) rotate(45deg);
}

/* Pie de cada bloque: la marca de contestado, discreta y a la
   derecha, como un sello de casilla revisada. */
.bloque .bloque-hecho,
.bloque .bloque-pendiente {
  margin: 0;
  padding: .45rem .9rem;
  border-top: 0;
  background: #F5F6FA;
  font-size: .78rem;
}
.bloque .bloque-hecho { color: var(--accent-ink); }

/* Cabecera del documento: franja de título como la del formulario
   de referencia, con el nombre de la ficha en versales. */
.ficha-encabezado {
  border: 1px solid #C3CFE3;
  border-bottom: 0;
  background: var(--accent-btn);
  color: #FFFFFF;
  padding: .6rem 1rem;
  text-align: center;
  font-family: var(--sans);
  font-size: 1rem; font-weight: 700;
  letter-spacing: .06em; text-transform: uppercase;
}

/* Las subpreguntas que aparecen dentro de un bloque (el «¿atiende
   público?» de infraestructura) mantienen el mismo tratamiento. */
.bloque .field-group + .btn-grid,
.bloque .btn-grid + .question { border-top: 1px solid #C3CFE3; }

/* En pantallas estrechas, una casilla por fila: dos columnas de
   190 px no caben y partirían los rótulos largos. */
@media (max-width: 560px) {
  .bloque .btn-grid { grid-template-columns: 1fr; }
}

/* Al imprimir, el formulario ya está maquetado como documento:
   solo hay que quitar lo que es de pantalla. */
@media print {
  .card.bloque { break-inside: avoid; }
  .bloque .bloque-hecho, .bloque .bloque-pendiente { display: none; }
}
"""
