# ══════════════════════════════════════════════════════════════
#  DESCARGAR LA FICHA · Y SABER QUÉ FALTA
#
#  Dos cosas que el asistente de corrido dejó pendientes:
#
#  1 · La ficha solo se podía copiar al portapapeles. El pie dice
#      «copia tu ficha antes de salir», porque nada se guarda: si
#      el único camino es un portapapeles que se pierde al copiar
#      otra cosa, la advertencia no sirve de nada. Ahora se
#      descarga como archivo y se puede imprimir o guardar en PDF.
#
#  2 · Con las preguntas de corrido es fácil pasar una por alto y
#      quedarse en «7 de 8» sin ver cuál falta. El bloque del CIIU
#      es el candidato natural: está arriba, y quien baja a
#      escribir su ciudad puede no volver a mirarlo.
#      Ahora la racha, al no estar completa, dice cuál falta y
#      lleva hasta ella.
# ══════════════════════════════════════════════════════════════

CSS = """
/* ═══════════════ QUÉ FALTA ═══════════════ */
.falta-aviso {
  display: flex; align-items: center; gap: .6rem; flex-wrap: wrap;
  margin: 1.1rem 0 0;
  background: #FBEFDD; border: 1px solid #E4C89B;
  border-left: 3px solid #8A5200;
  border-radius: 0 6px 6px 0;
  padding: .7rem .95rem;
  font-size: .88rem; color: var(--ink);
}
.falta-aviso b { color: #8A5200; }
.falta-aviso button {
  background: #8A5200; color: #FFFFFF;
  border: 0; border-radius: 4px;
  padding: .4rem .8rem; cursor: pointer;
  font-family: var(--sans); font-size: .82rem; font-weight: 600;
}
.falta-aviso button:hover { background: #6E4200; }

/* El bloque al que se salta parpadea una vez, para que quien
   llega sepa cuál de todos es. */
@keyframes bloque-senala {
  0%, 100% { box-shadow: none; }
  35%      { box-shadow: 0 0 0 4px rgba(138,82,0,.35); }
}
.bloque-senalado { animation: bloque-senala 1.1s ease-out 2; }
@media (prefers-reduced-motion: reduce) { .bloque-senalado { animation: none; } }

/* ═══════════════ EL RESULTADO, SIN RECUADRO ═══════════════
   La ficha terminada es la página entera, no una tarjeta dentro de
   la página: encerrarla en un marco la hacía ver como un apartado
   más del formulario. Fondo blanco y nada más. */
.card.bloque.resultado-final {
  border: 0;
  box-shadow: none;
  background: #FFFFFF;
}

/* ═══════════════ DESCARGAR ═══════════════ */
/* Sin recuadro. Llevaba borde azul por los cuatro lados y, pegado
   al bloque de acciones que ya tiene el suyo, se veían dos marcos
   encajados uno dentro de otro. Basta una línea arriba para
   separarlo de lo anterior. */
.descargar {
  border: 0;
  border-top: 1px solid var(--line);
  background: transparent;
  padding: 1rem 0 .2rem;
}
.descargar h3 {
  margin: 0 0 .2rem; font-size: .95rem;
  font-family: var(--sans); font-weight: 700;
}
.descargar p { margin: 0 0 .75rem; font-size: .84rem; color: var(--text); line-height: 1.5; }
.descargar-fila { display: flex; gap: .5rem; flex-wrap: wrap; }
.descargar .btn { border-radius: 4px; }

@media print {
  /* Nada de esto tiene sentido en papel: son botones. La fila de
     acciones —«Ver / copiar ficha en texto», «Volver a mis
     respuestas», «Empezar de nuevo»— salía impresa en el PDF como
     texto suelto que no lleva a ninguna parte. */
  .falta-aviso, .descargar, .actions-row { display: none !important; }
}
"""


JS = r"""
  /* ══════════════════════════════════════════════════════════
     QUÉ FALTA POR CONTESTAR
     ══════════════════════════════════════════════════════════ */
  const NOMBRE_BLOQUE = {
    actividad_desc:       "qué vende tu negocio",
    sector:               "el sector",
    ciiu:                 "confirmar el código CIIU",
    ubicacion:            "la ciudad y el departamento",
    figura:               "la figura jurídica",
    infraestructura:      "el espacio y el canal de venta",
    escala:               "el personal",
    sector_especifico:    "las preguntas de tu sector",
    contratacion_estatal: "si trabajas con el Estado"
  };

  function pintarQueFalta() {
    const previo = document.getElementById("faltaAviso");
    if (previo) previo.remove();

    const pend = preguntasIds().filter(id => !contestado(id));
    if (!pend.length) return;

    const aviso = el("div", { class: "falta-aviso", id: "faltaAviso" });
    const nombres = pend.map(id => NOMBRE_BLOQUE[id] || id);
    const texto = pend.length === 1
      ? "Falta una pregunta: " + nombres[0] + "."
      : "Faltan " + pend.length + " preguntas: " + nombres.join(", ") + ".";
    aviso.appendChild(el("b", {}, texto.split(":")[0] + ":"));
    aviso.appendChild(el("span", {}, texto.slice(texto.indexOf(":") + 1)));

    const ir = el("button", { type: "button" }, "Ir a la que falta");
    ir.addEventListener("click", () => {
      const destino = document.getElementById("bloque-" + pend[0]);
      if (!destino) return;
      destino.scrollIntoView({ behavior: "smooth", block: "center" });
      destino.classList.add("bloque-senalado");
      setTimeout(() => destino.classList.remove("bloque-senalado"), 2400);
    });
    aviso.appendChild(ir);
    main.appendChild(aviso);
  }

  /* ══════════════════════════════════════════════════════════
     DESCARGAR LA FICHA
     ----------------------------------------------------------
     Nada se guarda: al recargar se pierde todo. Así que lo
     mínimo es poder llevársela.
     ══════════════════════════════════════════════════════════ */
  /* Aquí vivían «nombreArchivo» y «descargarTexto», que armaban el
     .txt. Se fueron con su botón: una función sin quien la llame
     solo deja a quien lea esto buscando el botón que la usa. */


  /* Un solo botón, y en PDF.
     Eran tres —archivo de texto, PDF y portapapeles— y sobraban
     dos: el .txt pierde el formato de la ficha y el portapapeles se
     borra al copiar cualquier otra cosa, que es justo lo que no
     sirve cuando el aviso dice «guárdala antes de salir».

     El PDF sale del diálogo de impresión del navegador, donde hay
     que elegir «Guardar como PDF». Se dice en el texto, porque
     quien pulsa «Descargar en PDF» y ve aparecer una impresora
     piensa que se equivocó de botón. */
  function bloqueDescargar(plainText) {
    const caja = el("div", { class: "descargar" });
    caja.appendChild(el("h3", {}, "Guarda tu ficha antes de salir"));
    caja.appendChild(el("p", {}, "Esta herramienta todavía no guarda nada: al cerrar o recargar la pestaña se pierde. Se abrirá el cuadro de impresión: elige «Guardar como PDF» como destino."));

    const fila = el("div", { class: "descargar-fila" });

    const bPdf = el("button", { class: "btn btn-primary", type: "button" }, "Descargar en PDF");
    bPdf.addEventListener("click", () => window.print());
    fila.appendChild(bPdf);

    caja.appendChild(fila);
    return caja;
  }
"""
