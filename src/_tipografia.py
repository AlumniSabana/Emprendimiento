# ══════════════════════════════════════════════════════════════
#  LA TIPOGRAFÍA DEL CENTRO
#
#  Las mismas tres pilas que usan «Estudio de Pitch», «Construye tu
#  portafolio» y la portada de empleabilidad. Copiadas literalmente
#  de estudio-de-pitch.html para que no haya dos verdades.
#
#  ── POR QUÉ SON FUENTES DEL SISTEMA ───────────────────────────
#  Ni Iowan Old Style ni Segoe UI se descargan: ya están en el
#  equipo. Por eso las herramientas del CDP abren sin conexión y
#  sin esperar a que llegue una fuente. Cada pila lleva sus
#  alternativas para Windows, macOS y Linux, en ese orden.
#
#  Iowan Old Style existe en macOS; en Windows entra Palatino
#  Linotype, y en Linux acaba en Georgia. Las tres son serif de
#  transición y se parecen lo suficiente como para que el diseño
#  aguante en cualquiera.
#
#  ── QUÉ SUSTITUYE ─────────────────────────────────────────────
#  Fraunces (titulares) e IBM Plex (texto y cifras) venían en los
#  dos HTML originales. Se cambian por decisión del Centro: las
#  cinco herramientas tienen que leerse como un solo servicio.
# ══════════════════════════════════════════════════════════════

DISPLAY = '"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif'
BODY    = '"Segoe UI",system-ui,-apple-system,"Helvetica Neue",Arial,sans-serif'
MONO    = 'ui-monospace,"Cascadia Mono",Consolas,"SF Mono",Menlo,monospace'


# Cada archivo declara sus fuentes con nombres distintos. Aquí se
# dice qué variable de cada uno recibe cuál de las tres pilas.
FICHA = {
    '--serif':    DISPLAY,
    '--sans':     BODY,
    '--sans-pie': BODY,
    '--mono':     MONO,
}

TABLERO = {
    '--font-display': DISPLAY,
    '--font-sans':    BODY,
    '--font-body':    BODY,
    '--font-mono':    MONO,
    '--sans-pie':     BODY,
}


CSS_EXTRA = """
/* ═══════════════ TIPOGRAFÍA DEL CENTRO ═══════════════
   Los dos archivos originales cargaban Fraunces e IBM Plex desde
   Google Fonts. Ya no se usan, así que cualquier @import o <link>
   que quede es una petición a un servidor externo que retrasa la
   apertura y no pinta nada. Si alguno sobrevive al filtro de
   aplicar.py, esta regla asegura al menos que ninguna caja se
   quede esperando a una fuente que no va a llegar. */
body { font-family: var(--sans, var(--font-sans, """ + BODY + """)); }
"""
