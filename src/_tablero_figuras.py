# ══════════════════════════════════════════════════════════════
#  DIBUJOS DE REFERENCIA PARA LOS CUATRO CÁLCULOS
#
#  El Centro pidió «imágenes de referencia para que el emprendedor
#  comprenda bien», en el espacio libre de la derecha.
#
#  ── POR QUÉ DIBUJADOS Y NO FOTOS ──────────────────────────────
#  Son esquemas, no ilustraciones: lo que hay que entender es una
#  relación entre cantidades (dónde se cruzan los ingresos con los
#  gastos, cuándo se acaba la caja), y eso una foto no lo enseña.
#
#  Van en SVG escrito a mano, no en PNG, por tres razones
#  prácticas: pesan unos pocos kilobytes contra varios cientos, se
#  ven nítidos en cualquier pantalla y al imprimir, y llevan el
#  azul institucional exacto. Además la herramienta sigue siendo un
#  único archivo que abre sin conexión, que es su premisa.
#
#  ── QUÉ MUESTRA CADA UNO ──────────────────────────────────────
#  El mecanismo, no el adorno. El de punto de equilibrio es el
#  cruce de las dos rectas, que es LA imagen del concepto; el de
#  runway es la caja bajando hasta cero. Si alguien mira solo el
#  dibujo y el rótulo, ya entendió de qué se trata.
#
#  Los números que aparecen son de ejemplo y están marcados como
#  tales: el dibujo explica la idea, las cifras propias están al
#  lado, en la tarjeta.
# ══════════════════════════════════════════════════════════════

#  Paleta, la misma de la herramienta. Se escriben los valores y no
#  «var(--accent)» porque dentro de un SVG algunos navegadores
#  antiguos no resuelven las variables en «fill» y el dibujo sale
#  en negro.
AZUL      = "#001459"
AZUL_MED  = "#25409A"
AZUL_CLA  = "#7FA6D0"
AZUL_SUAVE= "#E3EAF7"
LINEA     = "#C3CFE3"
TINTA     = "#0A1330"
TINTA_SUA = "#4B5670"
AMBAR     = "#8A5200"
AMBAR_SUA = "#FBEFDD"
VERDE     = "#158A5E"
VERDE_SUA = "#E4F2EC"
ROJO      = "#A3252F"
ROJO_SUA  = "#FAE8E9"


# ── 1 · PRECIO MÍNIMO ─────────────────────────────────────────
# Una barra que se construye de abajo arriba: lo que cuesta
# producirlo, más la parte de los gastos fijos que le toca, más lo
# que quieres ganar. El precio mínimo es la suma, no un número que
# se elige mirando a la competencia.
PRECIO = f"""
<svg viewBox="0 0 300 250" role="img" aria-labelledby="figPrecioT figPrecioD">
  <title id="figPrecioT">Cómo se arma el precio mínimo</title>
  <desc id="figPrecioD">Una barra apilada: el costo directo, más la parte
  de gastos fijos que le corresponde, más el margen. La suma es el precio
  mínimo. Cobrar por debajo de esa línea da pérdida.</desc>

  <!-- la barra, de abajo hacia arriba -->
  <rect x="58" y="176" width="74" height="44" fill="{AZUL}" rx="3"/>
  <rect x="58" y="126" width="74" height="48" fill="{AZUL_MED}" rx="3"/>
  <rect x="58" y="86"  width="74" height="38" fill="{VERDE}" rx="3"/>

  <!-- rótulos de cada tramo -->
  <text x="140" y="203" font-size="11" fill="{TINTA}">Lo que te cuesta</text>
  <text x="140" y="216" font-size="10" fill="{TINTA_SUA}">hacerlo o prestarlo</text>
  <text x="140" y="148" font-size="11" fill="{TINTA}">Su parte de los</text>
  <text x="140" y="161" font-size="10" fill="{TINTA_SUA}">gastos fijos</text>
  <text x="140" y="109" font-size="11" fill="{TINTA}">Lo que quieres</text>
  <text x="140" y="122" font-size="10" fill="{TINTA_SUA}">ganar</text>

  <!-- la línea del precio mínimo -->
  <line x1="40" y1="80" x2="290" y2="80" stroke="{AZUL}" stroke-width="2"
        stroke-dasharray="5 3"/>
  <text x="40" y="70" font-size="11.5" font-weight="700" fill="{AZUL}">Precio mínimo</text>

  <!-- la zona de pérdida, debajo de la línea -->
  <rect x="10" y="86" width="40" height="134" fill="{ROJO_SUA}" rx="3"/>
  <text x="30" y="153" font-size="10" fill="{ROJO}" text-anchor="middle"
        transform="rotate(-90 30 153)">Cobrar aquí es perder</text>
</svg>
"""

PRECIO_PIE = ("Cobrar menos no es más barato para el cliente: es poner tú "
              "la diferencia, venta tras venta.")


# ── 2 · PUNTO DE EQUILIBRIO ───────────────────────────────────
# El cruce de las dos rectas. Es LA imagen del concepto: por
# debajo del cruce se pierde, por encima se gana, y el cruce
# mismo es el número que calcula la tarjeta.
EQUILIBRIO = f"""
<svg viewBox="0 0 300 250" role="img" aria-labelledby="figEqT figEqD">
  <title id="figEqT">Dónde está el punto de equilibrio</title>
  <desc id="figEqD">Dos líneas sobre unos ejes: los gastos, que casi no
  cambian vendas lo que vendas, y los ingresos, que suben con cada venta.
  Donde se cruzan está el punto de equilibrio: antes se pierde, después se
  gana.</desc>

  <!-- ejes -->
  <line x1="46" y1="44" x2="46" y2="196" stroke="{LINEA}" stroke-width="1.5"/>
  <line x1="46" y1="196" x2="290" y2="196" stroke="{LINEA}" stroke-width="1.5"/>
  <text x="46" y="36" font-size="10" fill="{TINTA_SUA}">Dinero</text>
  <text x="290" y="212" font-size="10" fill="{TINTA_SUA}" text-anchor="end">Ventas del mes</text>

  <!-- zonas: pierdes antes del cruce, ganas después -->
  <path d="M46 196 L177 196 L177 123 Z" fill="{ROJO_SUA}"/>
  <path d="M177 123 L177 196 L290 196 L290 62 Z" fill="{VERDE_SUA}"/>

  <!-- la recta de gastos: casi plana, porque no dependen de lo que vendas.
       El rótulo va al ARRANQUE de la línea y no al final: al final chocaba
       con el texto del punto de equilibrio, que ocupa el centro alto. -->
  <line x1="46" y1="130" x2="290" y2="118" stroke="{AMBAR}" stroke-width="2.5"/>
  <text x="50" y="124" font-size="10.5" fill="{AMBAR}" font-weight="600">Tus gastos</text>

  <!-- la recta de ingresos: sube con cada venta -->
  <line x1="46" y1="196" x2="290" y2="62" stroke="{AZUL}" stroke-width="2.5"/>
  <text x="290" y="56" font-size="10.5" fill="{AZUL}" text-anchor="end" font-weight="600">Lo que vendes</text>

  <!-- el cruce -->
  <line x1="177" y1="123" x2="177" y2="196" stroke="{TINTA}" stroke-width="1"
        stroke-dasharray="3 3"/>
  <circle cx="177" cy="123" r="5" fill="#FFFFFF" stroke="{TINTA}" stroke-width="2.5"/>
  <text x="177" y="92" font-size="11" font-weight="700" fill="{TINTA}" text-anchor="middle">Punto de</text>
  <text x="177" y="104" font-size="11" font-weight="700" fill="{TINTA}" text-anchor="middle">equilibrio</text>

  <text x="128" y="182" font-size="10" fill="{ROJO}" text-anchor="middle">Pierdes</text>
  <text x="236" y="182" font-size="10" fill="{VERDE}" text-anchor="middle">Ganas</text>
</svg>
"""

EQUILIBRIO_PIE = ("Hasta ese punto solo estás cubriendo gastos. Lo que "
                  "vendas de ahí en adelante ya te queda.")


# ── 3 · RUNWAY ────────────────────────────────────────────────
# La caja bajando mes a mes hasta cero. El número que importa no
# es cuánta plata hay, sino cuántos meses faltan para que no haya.
RUNWAY = f"""
<svg viewBox="0 0 300 250" role="img" aria-labelledby="figRwT figRwD">
  <title id="figRwT">Qué mide el runway</title>
  <desc id="figRwD">Barras que bajan mes a mes: la plata que tienes hoy se
  va gastando hasta llegar a cero. El runway son los meses que faltan para
  ese momento.</desc>

  <line x1="42" y1="176" x2="286" y2="176" stroke="{LINEA}" stroke-width="1.5"/>

  <!-- la caja bajando -->
  <rect x="50"  y="56"  width="30" height="120" fill="{AZUL}" rx="3"/>
  <rect x="94"  y="86"  width="30" height="90"  fill="{AZUL_MED}" rx="3"/>
  <rect x="138" y="116" width="30" height="60"  fill="{AZUL_CLA}" rx="3"/>
  <rect x="182" y="146" width="30" height="30"  fill="{AMBAR}" rx="3"/>
  <rect x="226" y="170" width="30" height="6"   fill="{ROJO}" rx="2"/>

  <text x="65"  y="192" font-size="9.5" fill="{TINTA_SUA}" text-anchor="middle">hoy</text>
  <text x="109" y="192" font-size="9.5" fill="{TINTA_SUA}" text-anchor="middle">mes 1</text>
  <text x="153" y="192" font-size="9.5" fill="{TINTA_SUA}" text-anchor="middle">mes 2</text>
  <text x="197" y="192" font-size="9.5" fill="{TINTA_SUA}" text-anchor="middle">mes 3</text>
  <text x="241" y="192" font-size="9.5" fill="{ROJO}" text-anchor="middle" font-weight="700">mes 4</text>

  <text x="46" y="44" font-size="11" fill="{TINTA}">La plata que tienes hoy</text>

  <!-- la flecha del tiempo que queda -->
  <line x1="50" y1="212" x2="241" y2="212" stroke="{TINTA}" stroke-width="1.5"/>
  <line x1="50" y1="208" x2="50" y2="216" stroke="{TINTA}" stroke-width="1.5"/>
  <line x1="241" y1="208" x2="241" y2="216" stroke="{TINTA}" stroke-width="1.5"/>
  <text x="145" y="226" font-size="11" font-weight="700" fill="{TINTA}" text-anchor="middle">Esto es tu runway</text>
</svg>
"""

RUNWAY_PIE = ("Los meses que te quedan si dejaras de vender mañana. No mide "
              "cuánta plata tienes, sino cuánto tiempo te da.")


# ── 4 · ASIGNACIÓN DE DINERO ──────────────────────────────────
# Un ingreso que se parte en cuatro antes de tocarlo. Los colores
# son los mismos que usa la leyenda de la tarjeta, para que el
# dibujo y las cifras se lean como una sola cosa.
ASIGNACION = f"""
<svg viewBox="0 0 300 250" role="img" aria-labelledby="figAsT figAsD">
  <title id="figAsT">Cómo se reparte cada ingreso</title>
  <desc id="figAsD">Lo que entra se divide en cuatro partes apenas llega:
  operación, impuestos, reserva y el sueldo del dueño. Cada parte va a lo
  suyo y no se mezcla con las demás.</desc>

  <!-- lo que entra -->
  <rect x="88" y="14" width="124" height="34" rx="6" fill="{AZUL_SUAVE}"
        stroke="{AZUL}" stroke-width="1.5"/>
  <text x="150" y="36" font-size="12" font-weight="700" fill="{AZUL}" text-anchor="middle">Lo que entra</text>

  <!-- el reparto -->
  <path d="M150 48 L150 62 M150 62 L48 62 L48 78 M150 62 L116 62 L116 78
           M150 62 L184 62 L184 78 M150 62 L252 62 L252 78"
        fill="none" stroke="{AZUL_CLA}" stroke-width="1.5"/>

  <!-- los cuatro baldes -->
  <rect x="20" y="78" width="56" height="52" rx="5" fill="{AZUL}"/>
  <text x="48" y="100" font-size="10" fill="#FFFFFF" text-anchor="middle">Operar</text>
  <text x="48" y="113" font-size="9" fill="#C7D6F0" text-anchor="middle">el negocio</text>

  <rect x="88" y="78" width="56" height="52" rx="5" fill="{AMBAR}"/>
  <text x="116" y="100" font-size="10" fill="#FFFFFF" text-anchor="middle">Impuestos</text>
  <text x="116" y="113" font-size="9" fill="{AMBAR_SUA}" text-anchor="middle">no es tuyo</text>

  <rect x="156" y="78" width="56" height="52" rx="5" fill="{TINTA_SUA}"/>
  <text x="184" y="100" font-size="10" fill="#FFFFFF" text-anchor="middle">Reserva</text>
  <text x="184" y="113" font-size="9" fill="#D9E1EE" text-anchor="middle">meses flojos</text>

  <rect x="224" y="78" width="56" height="52" rx="5" fill="{VERDE}"/>
  <text x="252" y="100" font-size="10" fill="#FFFFFF" text-anchor="middle">Tu sueldo</text>
  <text x="252" y="113" font-size="9" fill="{VERDE_SUA}" text-anchor="middle">fijo y claro</text>

  <!-- la caja que NO hay que usar como cuenta personal -->
  <rect x="20" y="152" width="260" height="46" rx="6" fill="{ROJO_SUA}"
        stroke="{ROJO}" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="150" y="171" font-size="10.5" fill="{ROJO}" text-anchor="middle" font-weight="600">Sin repartir, todo se ve como plata tuya</text>
  <text x="150" y="187" font-size="10" fill="{ROJO}" text-anchor="middle">y el IVA de marzo se gasta en febrero.</text>
</svg>
"""

ASIGNACION_PIE = ("Se reparte apenas entra, no a fin de mes: para entonces "
                  "ya no se sabe de quién era cada peso.")


#  pestaña -> (rótulo, dibujo, pie)
#
#  El pie va en HTML y no dentro del SVG. Se intentó al revés y las
#  frases largas se salían del dibujo por la derecha: el texto de un
#  SVG no se parte solo en varias líneas, así que una frase de 50
#  caracteres se sale del lienzo y el navegador la recorta. En HTML
#  ajusta sola, se puede seleccionar y crece si alguien tiene el
#  navegador configurado con letra grande.
FIGURAS = {
    "precio":     ("Cómo se arma el precio mínimo", PRECIO, PRECIO_PIE),
    "equilibrio": ("Dónde está el punto de equilibrio", EQUILIBRIO, EQUILIBRIO_PIE),
    "runway":     ("Qué mide el runway", RUNWAY, RUNWAY_PIE),
    "asignacion": ("Cómo se reparte cada ingreso", ASIGNACION, ASIGNACION_PIE),
}


CSS = """
/* ═══════════════ DIBUJOS DE LOS CÁLCULOS ═══════════════
   El dibujo va a la derecha del contenido, ocupando el espacio que
   antes quedaba vacío. El encabezado del panel cruza las dos
   columnas; las tarjetas se quedan en la primera. Sin forzar la
   columna, la segunda tarjeta de «Precio mínimo» se subía al lado
   del dibujo y la lectura saltaba de una columna a otra. */
.panel.con-figura {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 312px;
  gap: 0 18px;
  align-items: start;
}
.panel.con-figura > .panel-head { grid-column: 1 / -1; }
.panel.con-figura > .card { grid-column: 1; }
.panel.con-figura > .calc-figura { grid-column: 2; grid-row: 2; }

.calc-figura {
  background: var(--paper-raised); border: 1px solid var(--line);
  border-radius: 12px; padding: 14px 15px 12px;
  box-shadow: var(--shadow);
}
.calc-figura h3 {
  font-size: 12.5px; margin: 0 0 9px; color: var(--ink);
  line-height: 1.3;
}
.calc-figura svg { display: block; width: 100%; height: auto; }
.calc-figura .pie-figura {
  margin: 8px 0 0; font-size: 11px; line-height: 1.5;
  color: var(--ink-soft);
}

/* Por debajo de 1120 px la columna de 312 px deja al contenido sin
   sitio: los campos de porcentaje de «Asignación» se apretaban en
   tres columnas de 90 px. Se apila y el dibujo pasa debajo. */
@media (max-width: 1120px) {
  .panel.con-figura { display: block; }
  .calc-figura { margin-top: 16px; }
}
@media print {
  .panel.con-figura { display: block; }
  .calc-figura { border-color: #999; box-shadow: none; page-break-inside: avoid; }
}
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   EL DIBUJO DE CADA CÁLCULO
   Se añade al panel y se marca el panel para que lo coloque a la
   derecha. Las pestañas sin dibujo no cambian en nada.
   ══════════════════════════════════════════════════════════ */
var FIGURAS_CALCULO = __FIGURAS__;

function bloqueFigura(tab){
  var f = FIGURAS_CALCULO[tab];
  if(!f) return "";
  return '<aside class="calc-figura">' +
           '<h3>' + esc(f[0]) + '</h3>' +
           f[1] +
           '<p class="pie-figura">' + esc(f[2]) + '</p>' +
         '</aside>';
}
"""


def js():
    import json
    datos = {k: [rotulo, svg.strip(), pie]
             for k, (rotulo, svg, pie) in FIGURAS.items()}
    return JS.replace("__FIGURAS__", json.dumps(datos, ensure_ascii=False))
