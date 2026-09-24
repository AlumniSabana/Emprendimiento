# ══════════════════════════════════════════════════════════════
#  QUÉ PASO LE TOCA A CADA TÉRMINO DE LA GUÍA
#
#  El Centro pidió que cada viñeta de la guía diga «a qué paso
#  pertenece», para que quede claro qué hay que llenar para que el
#  Resumen esté completo.
#
#  ── LOS PASOS SON LOS QUE YA EXISTÍAN ─────────────────────────
#  No se inventan: el panel de Resumen ya trae «Empieza aquí: 5
#  pasos» y esos son. Lo que faltaba era la otra mitad del puente:
#  desde la guía no se veía a cuál de los cinco correspondía cada
#  término, así que quien leía «Runway» no sabía que le tocaba
#  escribir su caja actual para que el Resumen dejara de salir en
#  guiones.
#
#  ── LA DISTINCIÓN QUE IMPORTA ─────────────────────────────────
#  Hay dos clases de término, y confundirlas es lo que hace que
#  alguien se quede esperando a que aparezca un número:
#
#   · «escribe»  — hay que meter datos a mano en alguna pestaña.
#   · «calcula»  — sale solo en cuanto estén los datos que necesita,
#                  y se dice CUÁLES, porque «se calcula solo» sin
#                  más deja pensando que está roto.
#   · «lectura»  — no alimenta el Resumen: es criterio, no dato.
#
#  Poner «Paso 3» en algo que no se llena sería peor que no poner
#  nada: mandaría a buscar un campo que no existe.
# ══════════════════════════════════════════════════════════════

#  título del término  ->  (clase, paso, dónde / qué necesita)
#
#  La clave es el título tal cual aparece en GUIDE. Si allí se
#  renombra uno y aquí no, ese término se queda sin subtítulo: no
#  se rompe nada, pero deja de guiar. El build lo comprueba.
PASOS = {
    "Facturación vs. ganancia real": (
        "lectura", None,
        "Léelo antes de empezar: es la idea que sostiene todo lo demás"),

    "Ingresos por cliente y mes": (
        "escribe", 2,
        "Se llena en Ingresos, del grupo Datos del mes"),

    "Gastos fijos": (
        "escribe", 3,
        "Se llena en Gastos fijos, del grupo Datos del mes"),

    "Gastos variables": (
        "escribe", 3,
        "Se llena en Gastos variables, del grupo Datos del mes"),

    "Flujo de caja proyectado": (
        "calcula", None,
        "Sale solo con tus ingresos y tus gastos (pasos 2 y 3)"),

    "Calculadora de precio mínimo": (
        "escribe", 5,
        "Se llena en Precio mínimo: horas, sueldo objetivo y gastos"),

    "Punto de equilibrio": (
        "calcula", None,
        "Sale solo con tus ingresos y tus gastos (pasos 2 y 3)"),

    "Runway (alerta de caja)": (
        "escribe", 4,
        "Escribe tu caja actual en Runway; el resto sale de tus gastos"),

    # El título lo cambia aplicar.py; aquí va el nuevo.
    "A dónde va cada peso que entra": (
        "escribe", None,
        "Se define en Asignación de dinero, cuando ya tengas ingresos"),

    "Semáforo financiero": (
        "calcula", None,
        "Sale solo en el Resumen cuando los pasos 1 a 4 están completos"),

    "Errores comunes en tracción temprana": (
        "lectura", None,
        "No se llena: es para revisar cada cierto tiempo"),

    "Rutina de cierre mensual": (
        "lectura", None,
        "Se hace en Cierre mensual, una vez al mes"),
}


#  Cómo se rotula cada clase.
CLASES = {
    "escribe": "Lo escribes tú",
    "calcula": "Se calcula solo",
    "lectura": "Solo para leer",
}


CSS = """
/* ═══════════════ EL PASO DE CADA TÉRMINO ═══════════════
   Va bajo el título del acordeón, visible con la viñeta cerrada:
   el sentido de esto es poder recorrer la lista y ver de un vistazo
   qué falta por llenar, sin abrir las doce. */
.accordion-head { flex-wrap: wrap; }
.accordion-head .titulo-y-paso { flex: 1; min-width: 0; }
.accordion-head .titulo-y-paso h4 { margin: 0; }

.paso-guia {
  display: flex; align-items: center; gap: 7px; flex-wrap: wrap;
  margin-top: 3px;
  font-size: 11.5px; line-height: 1.45; color: var(--ink-soft);
}
.paso-guia .etq {
  flex: none;
  font-family: var(--font-mono); font-size: 9.5px; font-weight: 700;
  letter-spacing: .07em; text-transform: uppercase;
  border-radius: 99px; padding: 2px 8px;
}
/* Lo que hay que llenar destaca; lo demás informa sin llamar. */
.paso-guia.escribe .etq { background: var(--accent-soft); color: var(--accent-strong); }
.paso-guia.calcula .etq { background: var(--good-soft);   color: var(--good); }
.paso-guia.lectura .etq { background: var(--paper-sunken); color: var(--ink-soft); }

.paso-guia .num {
  flex: none; font-family: var(--font-mono); font-size: 10.5px;
  font-weight: 700; color: var(--gold);
}
@media print { .paso-guia .etq { border: 1px solid #999; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   EL PASO AL QUE PERTENECE CADA TÉRMINO DE LA GUÍA
   ══════════════════════════════════════════════════════════ */
var PASOS_GUIA   = __PASOS__;
var CLASES_PASO  = __CLASES__;

function subtituloPaso(titulo){
  var p = PASOS_GUIA[titulo];
  if(!p) return "";
  var clase = p[0], num = p[1], donde = p[2];
  return '<div class="paso-guia ' + clase + '">' +
           '<span class="etq">' + esc(CLASES_PASO[clase]) + '</span>' +
           (num ? '<span class="num">Paso ' + num + '</span>' : '') +
           '<span>' + esc(donde) + '</span>' +
         '</div>';
}
"""


def js():
    import json
    return (JS
            .replace("__PASOS__", json.dumps(PASOS, ensure_ascii=False))
            .replace("__CLASES__", json.dumps(CLASES, ensure_ascii=False)))
