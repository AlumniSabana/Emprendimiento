# ══════════════════════════════════════════════════════════════
#  CAMPOS DE CIFRAS: SOLO NÚMEROS, Y CON PUNTOS DE MILES
#
#  Los tres campos numéricos de la ficha —activos, ingresos y
#  número de personas— eran «type: text». El teclado del móvil
#  mostraba números por «inputmode», pero el campo aceptaba
#  cualquier cosa: «cinco millones», «8 mill», «$8.000.000 aprox».
#
#  Y la validación solo miraba que no estuviera vacío, así que
#  todo eso pasaba. Después «fmtCOP» no sabía qué hacer con ello y
#  la ficha final mostraba un guión donde debía ir la cifra, o algo
#  peor: un número recortado a la primera parte que sí entendía.
#
#  ── QUÉ HACE ──────────────────────────────────────────────────
#  1. Solo deja escribir dígitos. Letras, símbolos y espacios se
#     descartan mientras se teclea.
#  2. Pone los puntos de miles al vuelo: «5000000» se ve
#     «5.000.000». Un número de siete cifras sin separar es
#     ilegible, y ahí es donde alguien se equivoca de un cero en
#     los activos de su propio negocio.
#  3. El cursor se queda donde estaba. Reformatear un campo
#     mientras alguien escribe suele mandar el cursor al final: si
#     corriges el segundo dígito de «5.000.000», el siguiente que
#     teclees aparece al final. Se cuentan los dígitos a la
#     izquierda del cursor y se restaura esa posición.
#
#  ── EL DE PERSONAS NO LLEVA PUNTOS ────────────────────────────
#  «¿Cuántas personas van a trabajar contigo?» son 0, 2, 15. Poner
#  «1.500» ahí sería absurdo, así que ese campo solo filtra
#  dígitos y no formatea.
# ══════════════════════════════════════════════════════════════

#  ── LA AYUDA DE «ACTIVOS» E «INGRESOS» ───────────────────────
#  Son los dos términos donde la gente se traba en esa pantalla, y
#  el vídeo vive en el tablero, no en la ficha. Así que aquí va la
#  explicación en una línea, junto al campo, y el vídeo completo
#  queda en la Guía de uso del tablero para quien quiera más.

AYUDAS = {
    "activos": ("Todo lo que ya tiene el negocio y se puede valorar: "
                "equipos, herramientas, inventario, muebles, dinero en caja. "
                "No cuentan las deudas."),
    "ingresos": ("Lo que esperas que ENTRE al mes por ventas, antes de "
                 "descontar gastos. No es lo que te queda: eso es la ganancia."),
}


CSS = """
/* ═══════════════ CAMPOS DE CIFRAS ═══════════════ */
/* La explicación bajo la etiqueta, en la misma celda. */
.bloque .ayuda-campo {
  display: block;
  margin: .1rem .9rem .45rem;
  font-size: .78rem; line-height: 1.45;
  color: var(--text-muted);
}
/* Los dígitos alineados a la derecha se comparan mejor: es lo que
   hace cualquier planilla contable. Y en tabular-nums todos los
   números ocupan lo mismo, así que la cifra no «baila» al escribir. */
.bloque input.cifra {
  font-variant-numeric: tabular-nums;
  letter-spacing: .01em;
}
"""


JS = r"""
  /* ══════════════════════════════════════════════════════════
     SOLO DÍGITOS, CON PUNTOS DE MILES
     ══════════════════════════════════════════════════════════ */

  /* Deja únicamente los dígitos de lo que se haya escrito o pegado. */
  function soloDigitos(txt) {
    return String(txt == null ? "" : txt).replace(/\D+/g, "");
  }

  /* «5000000» -> «5.000.000». El punto es el separador de miles en
     Colombia; la coma es decimal, y aquí no hay decimales porque
     nadie estima los activos de su negocio con centavos. */
  function conPuntosDeMiles(digitos) {
    if (!digitos) return "";
    return digitos.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  /* Vigila un campo para que solo acepte cifras.
     «formatear» decide si además se ponen los puntos de miles. */
  function vigilarCifra(input, alCambiar, formatear) {
    function limpiar() {
      var antes = input.value;
      var cursor = input.selectionStart;

      /* Cuántos dígitos hay a la izquierda del cursor. Es lo único
         que no cambia al reformatear, así que sirve de ancla para
         devolver el cursor a su sitio. */
      var digitosIzquierda = soloDigitos(antes.slice(0, cursor)).length;

      var digitos = soloDigitos(antes);
      var nuevo = formatear ? conPuntosDeMiles(digitos) : digitos;

      if (nuevo !== antes) {
        input.value = nuevo;
        /* Recolocar el cursor tras el mismo dígito que antes. */
        var pos = 0, vistos = 0;
        while (pos < nuevo.length && vistos < digitosIzquierda) {
          if (/\d/.test(nuevo[pos])) vistos++;
          pos++;
        }
        try { input.setSelectionRange(pos, pos); } catch (_) {}
      }
      if (alCambiar) alCambiar(digitos);
    }

    input.addEventListener("input", limpiar);
    /* Al pegar, el navegador dispara «input» después, así que
       «limpiar» ya se encarga. Pero un pegado con letras deja el
       campo un instante sucio; esto lo adelanta. */
    input.addEventListener("paste", function () { setTimeout(limpiar, 0); });
    /* Bloquear las teclas que no son dígito evita el parpadeo de
       ver la letra aparecer y desaparecer. Se dejan pasar las de
       control: borrar, tabular, flechas, y los atajos con Ctrl/Cmd. */
    input.addEventListener("keydown", function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      if (e.key && e.key.length === 1 && !/\d/.test(e.key)) e.preventDefault();
    });
  }
"""
