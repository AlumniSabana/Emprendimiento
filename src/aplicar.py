# ══════════════════════════════════════════════════════════════
#  VISTE LAS DOS HERRAMIENTAS CON LA IDENTIDAD DE LA UNIVERSIDAD
#
#  Uso:  python3 aplicar.py
#
#  Toca tres cosas y solo tres:
#    1. La paleta: la institucional sustituye a la anterior.
#    2. El modo oscuro: se retira. La identidad de la Universidad
#       no cambia según la preferencia del sistema.
#    3. El pie: el mismo de las otras tres herramientas del CDP.
#
#  NO toca la lógica: ni un cálculo, ni un paso del asistente, ni
#  una fórmula. Si algo de eso cambia, es un error.
# ══════════════════════════════════════════════════════════════

import io, re
from _comun import PALETA, PIE_CSS, pie, barra_volver
import _ficha_corrido, _tablero_importar, _tablero_videos, _tipografia

VERSION = "2026.08.31"

# Ninguno de los dos archivos declaraba la codificación. Servidos
# desde Vercel funcionaban por casualidad; abiertos como archivo
# local, cada tilde y cada «ñ» salía rota. Es lo primero que va.
CABEZA = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n'
          '<meta charset="UTF-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
          '<meta name="color-scheme" content="light">\n'
          '<meta name="theme-color" content="#001459">\n')


def encabezar(s, descripcion):
    """Cierra el documento: cabeza con codificación y cuerpo. Los dos
    archivos venían como fragmentos sueltos, sin <html> ni <head>."""
    s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">\n', '', 1)
    s = CABEZA + '<meta name="description" content="' + descripcion + '">\n' + s
    s = s.replace('</style>', '</style>\n</head>\n<body>', 1)
    return s.rstrip() + '\n</body>\n</html>\n' 


def anadir_tokens(s):
    """Declara los tokens institucionales que el pie y el índice usan
    y que estos archivos no tenían. Se añaden al :root existente en
    vez de crear otro, para que no haya dos sitios donde mirar."""
    marca = 'color-scheme: light;'
    if marca in s:
        return s.replace(marca, PALETA.strip() + '\n  ' + marca, 1)
    # La ficha no declara color-scheme: se cuelga del primer token.
    return s.replace('--bg:', PALETA.strip() + '\n    --bg:', 1)


def quitar_modo_oscuro(s):
    """Retira los dos bloques de tema oscuro (el de media query y el
    de data-theme). Se hace por conteo de llaves y no con una
    expresión regular perezosa, que se comería el bloque siguiente."""
    fuera = 0
    for marca in ('@media (prefers-color-scheme: dark)', ':root[data-theme="dark"]'):
        i = s.find(marca)
        while i != -1:
            j, nivel = s.index('{', i), 0
            k = j
            while k < len(s):
                if s[k] == '{': nivel += 1
                elif s[k] == '}':
                    nivel -= 1
                    if nivel == 0: break
                k += 1
            s = s[:i] + s[k + 1:]
            fuera += 1
            i = s.find(marca)
    return s, fuera


def quitar_guiones(s, frases):
    """Reescribe las frases donde el guión largo hacía de pausa.

    Se hace con una lista explícita y NO con un reemplazo global de
    «—». El guión largo tiene dos papeles distintos en estos
    archivos: separar frases, y marcar «todavía no hay dato» en las
    cifras del tablero (Runway, Punto de equilibrio). Cambiar el
    segundo por «0» diría que el runway es cero, que es una
    afirmación falsa y además alarmante. Así que se tocan una a una
    las de redacción y el marcador se queda.

    Si una frase de la lista no aparece, se avisa: significa que el
    archivo de origen cambió y el reemplazo se quedó sin efecto."""
    n = 0
    for viejo, nuevo in frases:
        if viejo not in s:
            print('   AVISO · no se encontró para reescribir:', viejo[:60])
            continue
        s = s.replace(viejo, nuevo)
        n += 1
    return s, n


def quitar_fuentes_de_google(s):
    """Retira las descargas de Fraunces, Public Sans e IBM Plex.

    Los dos archivos las traían de fonts.googleapis.com. Al pasar a
    las fuentes del sistema esas peticiones ya no pintan nada: solo
    retrasan la apertura y, sin conexión, la dejan esperando.

    Quitarlas es lo que hace de verdad que estas herramientas
    funcionen sin internet, que es lo que su propio pie promete."""
    n = 0
    patrones = [
        r'<link[^>]*rel="preconnect"[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*',
        r'<link[^>]*fonts\.googleapis\.com/css2[^>]*>\s*',
        r'@import\s+url\([^)]*fonts\.googleapis\.com[^)]*\)\s*;',
    ]
    for pat in patrones:
        s, k = re.subn(pat, '', s, flags=re.I)
        n += k
    return s, n


def sustituir_tokens(s, mapa):
    """Reescribe los valores de las variables CSS que ya existen, sin
    tocar sus nombres: así ninguna regla del archivo se queda
    apuntando a una variable que dejó de existir.

    Reescribe TODAS las declaraciones de cada nombre, no la primera.
    Con «count=1» la que se reescribía era la que acababa de inyectar
    PALETA, y la propia del archivo —el crema #fbfaf3 de las tarjetas
    de la ficha, su tinta verdosa— se quedaba intacta más abajo y
    ganaba por orden. Se veía: la ficha seguía saliendo color hueso.

    El nombre se ancla con «(?<![\\w-])» para que «--line» no muerda
    a «--line-strong», que es otra variable con otro papel."""
    n = 0
    for viejo, nuevo in mapa.items():
        patron = re.compile(r'(?<![\w-])(' + re.escape(viejo) + r'\s*:\s*)([^;]+)(;)')
        s, hechos = patron.subn(lambda m: m.group(1) + nuevo + m.group(3), s)
        n += hechos
    return s, n


# ══════════════════════════════════════════════════════════════
#  1 · TABLERO FINANCIERO
# ══════════════════════════════════════════════════════════════
t = io.open('tablero-financiero.html', encoding='utf-8').read()
t, fuera_t = quitar_modo_oscuro(t)
t = anadir_tokens(t)

# El tablero usaba un verde de archivo y un ocre. Cada variable
# suya pasa a su equivalente institucional, conservando el papel
# que cumplía: acento, superficie elevada, línea, estado.
t, n_t = sustituir_tokens(t, {
    '--ink':          '#0A1330',
    '--ink-soft':     '#4B5670',
    '--paper':        '#EEF1F8',
    '--paper-raised': '#FFFFFF',
    '--paper-sunken': '#F5F7FC',
    '--line':         '#D9E1EE',
    '--line-strong':  '#C3CFE3',
    '--accent':       '#001459',
    '--accent-strong':'#25409A',
    '--accent-soft':  '#E3EAF7',
    # El dorado de la numeración pasa al ámbar institucional: no hay
    # oro en la paleta de la Universidad.
    '--gold':         '#8A5200',
    '--gold-soft':    '#FBEFDD',
    '--good':         '#158A5E',
    '--good-soft':    '#E4F2EC',
    '--warn':         '#8A5200',
    '--warn-soft':    '#FBEFDD',
    '--critical':     '#A3252F',
    '--critical-soft':'#FAE8E9',
    '--shadow':       '0 1px 2px rgba(0,20,89,.05), 0 8px 24px -16px rgba(0,20,89,.22)',
})

# El índice lateral va sobre azul institucional, como en las otras
# tres herramientas: es lo que hace que se reconozcan de un vistazo.
t = t.replace(
    '.sidebar{\n  width:232px; flex:0 0 232px; background:var(--paper-raised); border-right:1px solid var(--line);',
    '.sidebar{\n  width:232px; flex:0 0 232px; background:var(--azul); border-right:1px solid var(--azul);')

# Sobre el azul institucional, todo lo del índice necesita su propia
# escala de contraste. Sin esto el texto queda gris sobre azul.
t = t.replace('''.brand .kicker{ font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--accent); font-weight:600; }''',
'''.brand .kicker{ font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:#A9BEDE; font-weight:600; }''')
t = t.replace('''.brand h1{ font-size:21px; margin-top:4px; line-height:1.15; }''',
'''.brand h1{ font-size:21px; margin-top:4px; line-height:1.15; color:#FFFFFF; }''')
t = t.replace('''.brand .sub{ color:var(--ink-soft); font-size:12px; margin-top:6px; }''',
'''.brand .sub{ color:#A9BEDE; font-size:12px; margin-top:6px; }''')
t = t.replace('''.navgroup-label{ font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-soft); padding:14px 8px 4px; }''',
'''.navgroup-label{ font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:#8FA5C6; padding:14px 8px 4px; }''')
t = t.replace('''  border:1px solid transparent; background:transparent; color:var(--ink-soft); cursor:pointer; font-size:13.5px; font-weight:500;''',
'''  border:1px solid transparent; background:transparent; color:#C7D6F0; cursor:pointer; font-size:13.5px; font-weight:500;''')
t = t.replace('''.tab-btn:hover{ background:var(--paper-sunken); color:var(--ink); }''',
'''.tab-btn:hover{ background:rgba(255,255,255,.08); color:#FFFFFF; }''')
t = t.replace('''.tab-btn.active{ background:var(--accent-soft); color:var(--accent-strong); font-weight:600; }''',
'''.tab-btn.active{ background:rgba(255,255,255,.13); color:#FFFFFF; font-weight:600; }''')
t = t.replace('''.tab-btn .dot{ width:6px; height:6px; border-radius:50%; background:var(--line-strong); flex:0 0 auto; }''',
'''.tab-btn .dot{ width:6px; height:6px; border-radius:50%; background:rgba(255,255,255,.35); flex:0 0 auto; }''')
t = t.replace('''.tab-btn.active .dot{ background:var(--accent); }''',
'''.tab-btn.active .dot{ background:#FFFFFF; }''')
t = t.replace('''.bizrow input, .bizrow select{ width:100%; }''',
'''.bizrow input, .bizrow select{ width:100%; }
.bizrow .field label{ color:#A9BEDE; }''')
# La barra móvil comparte los botones del índice, pero va sobre papel.
t = t.replace('''  .mobile-tabbar{ display:flex; overflow-x:auto; gap:6px; padding:8px 14px 14px; border-top:1px solid var(--line); }''',
'''  .mobile-tabbar{ display:flex; overflow-x:auto; gap:6px; padding:8px 14px 14px; border-top:1px solid var(--line); background:var(--azul); }''')

t = t.replace('--font-display:', '--sans-pie:' + _tipografia.BODY + ';\n  --font-display:')

# ── La tipografía del Centro ──
# Iowan Old Style, Segoe UI y la mono del sistema, como en Pitch y
# el portafolio. Fraunces e IBM Plex se van.
t, n_ft = sustituir_tokens(t, _tipografia.TABLERO)
t, n_dt = quitar_fuentes_de_google(t)

# ── Fuera los guiones largos de redacción ──
# Cada frase se reescribe entera, no se le quita el guión y ya: una
# frase a la que se le arranca la pausa sin recolocar las palabras
# queda peor escrita que con el guión.
t, n_gt = quitar_guiones(t, [
    ('<h3>Empieza aquí — 5 pasos (≈15 min)</h3>',
     '<h3>Empieza aquí: 5 pasos (≈15 min)</h3>'),
    ('<h3>Proyección de caja — 6 meses</h3>',
     '<h3>Proyección de caja a 6 meses</h3>'),
    ('<h2>Flujo de caja proyectado — 6 meses</h2>',
     '<h2>Flujo de caja proyectado a 6 meses</h2>'),
    ('necesitas al mes solo para no perder dinero — antes de empezar a ganar.',
     'necesitas al mes solo para no perder dinero, antes de empezar a ganar.'),
    ('Actúa ya — reduce gastos o consigue ingresos inmediatos.',
     'Actúa ya: reduce gastos o consigue ingresos inmediatos.'),
    ("+labels[k]+' — <span class=\"mono\">",
     "+labels[k]+': <span class=\"mono\">"),
    ('Defínelos tú — deben sumar 100%.',
     'Defínelos tú. Deben sumar 100%.'),
    ('Revísalos cada trimestre — suelen crecer sin que nadie lo note.',
     'Revísalos cada trimestre: suelen crecer sin que nadie lo note.'),
    ('tu margen se está comiendo a sí mismo — revisa proveedores o precios.',
     'tu margen se está comiendo a sí mismo: revisa proveedores o precios.'),
    ('o subes precios o reduces gastos — no hay tercera opción sostenible.',
     'o subes precios o reduces gastos. No hay tercera opción sostenible.'),
    ('el problema no es de ventas — es de estructura de costos o de precio.',
     'el problema no es de ventas, sino de estructura de costos o de precio.'),
    ('Amarillo: ganancia ajustada o runway corto — hay que actuar pronto. '
     'Rojo: pérdida o runway crítico — decisión inmediata.',
     'Amarillo: ganancia ajustada o runway corto, hay que actuar pronto. '
     'Rojo: pérdida o runway crítico, decisión inmediata.'),
    ('empieza por la calculadora de precio mínimo — resuelve la causa más común.',
     'empieza por la calculadora de precio mínimo: resuelve la causa más común.'),
    ('hazlo hoy antes de seguir tomando decisiones — los números viejos engañan.',
     'hazlo hoy antes de seguir tomando decisiones: los números viejos engañan.'),
    ('Once secciones — tu referencia rápida del tablero.',
     'Once secciones, tu referencia rápida del tablero.'),
])

PIE_TABLERO = pie(
    servicio=(
        '<p><strong>Tablero Financiero</strong> es una herramienta de trabajo autónomo del '
        'Centro de Desarrollo Profesional, Alumni Sabana, para emprendimientos en tracción temprana.</p>'
        '<p>Traduce lo que facturas en lo que de verdad ganas: precio mínimo por hora, punto de '
        'equilibrio, runway y separación entre la caja del negocio y la personal. No es contabilidad '
        'oficial, no reemplaza a un contador y no sustituye una asesoría personalizada.</p>'
    ),
    datos=(
        '<p>Por ahora, todo lo que registras se guarda <strong>únicamente en este navegador</strong> '
        'y en este equipo: no se envía a ningún servidor y nadie más lo puede consultar. Si limpias '
        'los datos del navegador o abres la herramienta en otro computador, empiezas de cero.</p>'
        '<p><strong>Próximamente</strong> podrás guardarlo en tu cuenta Alumni Sabana y recuperarlo '
        'desde cualquier computador, igual que en las demás herramientas del Centro.</p>'
        '<p>Las cifras que escribas son estimaciones tuyas y su exactitud es tu responsabilidad. '
        'Los resultados son orientativos.</p>'
    ),
    version=VERSION)

# ── Importar ingresos desde una hoja de cálculo ──
# El bloque va bajo la tabla de ingresos, dentro de su misma tarjeta.
# Va tras cerrar la tabla y antes de cerrar la tarjeta: así queda
# dentro del mismo bloque «Registro de ingresos», que es donde la
# persona está mirando cuando piensa «esto una a una, no».
_ancla_imp = """      '</tbody></table></div>'+
    '</div>'+
    monthlySummaryCard(byMonth, "Ingresos por mes")"""
if _ancla_imp not in t:
    raise SystemExit('ERROR: no se encontró el cierre de la tabla de ingresos')
t = t.replace(_ancla_imp, """      '</tbody></table></div>'+
      bloqueImportar()+
    '</div>'+
    monthlySummaryCard(byMonth, "Ingresos por mes")""", 1)

# Los eventos del importador, junto a los que ya existen.
_ancla_ev = """  var addIncome = root.querySelector("#addIncome");"""
if _ancla_ev not in t:
    raise SystemExit('ERROR: no se encontró el enganche de eventos de ingresos')
t = t.replace(_ancla_ev, """  var impBtn = root.querySelector("#impBtn");
  var impArchivo = root.querySelector("#impArchivo");
  if(impBtn && impArchivo){
    impBtn.addEventListener("click", function(){ impArchivo.click(); });
    impArchivo.addEventListener("change", function(e){
      leerArchivoIngresos(e.target.files && e.target.files[0]);
      e.target.value = "";           /* permite subir el mismo archivo dos veces */
    });
  }
  var impEjemplo = root.querySelector("#impEjemplo");
  if(impEjemplo) impEjemplo.addEventListener("click", descargarEjemploCSV);
  var impZona = root.querySelector("#impZona");
  if(impZona){
    ["dragenter","dragover"].forEach(function(ev){
      impZona.addEventListener(ev, function(e){
        e.preventDefault(); impZona.classList.add("encima"); });
    });
    ["dragleave","drop"].forEach(function(ev){
      impZona.addEventListener(ev, function(e){
        e.preventDefault(); impZona.classList.remove("encima"); });
    });
    impZona.addEventListener("drop", function(e){
      leerArchivoIngresos(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
    });
  }

""" + _ancla_ev, 1)

# ── Videos en la guía de uso ──
# Cada término de la guía puede llevar su vídeo. Los que no tengan
# enlace en _tablero_videos.py no muestran nada.
# Se ancla en «+esc(g.red)+», que es código y no texto: los rótulos
# de alrededor ya los reescribió quitar_guiones más arriba.
_ancla_vid = "+esc(g.red)+'</div></div>'+"
if _ancla_vid not in t:
    raise SystemExit('ERROR: no se encontró el cuerpo del acordeón de la guía')
t = t.replace(_ancla_vid, "+esc(g.red)+'</div>'+bloqueVideo(g.t)+'</div>'+", 1)

t = t.replace('</style>', _tablero_importar.CSS + _tablero_videos.CSS + '\n</style>', 1)

# El JS de los dos módulos va DENTRO del IIFE del tablero, justo
# antes de que se cierre.
#
# Se intentó ponerlo después de «</script>» y falló con «esc is not
# defined»: todo el tablero vive dentro de «(function(){ … })()», así
# que esc(), state y saveState() no existen fuera. Aquí sí los ve.
_cierre = '/* ============================ INIT ============================ */'
if _cierre not in t:
    raise SystemExit('ERROR: no se encontró el bloque INIT del tablero')
t = t.replace(_cierre,
              _tablero_importar.JS + '\n' + _tablero_videos.js() + '\n\n' + _cierre, 1)

t = encabezar(t, 'Tablero financiero del Centro de Desarrollo Profesional de la Universidad de La Sabana: precio minimo, punto de equilibrio, runway y flujo de caja para emprendimientos en traccion temprana.')
t = t.replace('</style>', PIE_CSS + '\n</style>', 1)
# La barra de vuelta, lo primero del cuerpo.
t = t.replace('<body>\n', '<body>\n' + barra_volver(), 1)

# El índice lateral es «sticky» con «top:0; height:100vh». Con la
# barra encima, esos 100vh son la altura de la ventana ENTERA
# empezando 51 px más abajo: al bajar, el índice se salía por arriba
# y sus últimas opciones («Guía de uso», «Cierre mensual») quedaban
# fuera de alcance. Se comprobó midiendo: top llegaba a -473 px.
# Se le resta la altura de la barra y se pega justo debajo de ella.
t = t.replace(
    'display:flex; flex-direction:column; position:sticky; top:0; height:100vh; overflow-y:auto;',
    'display:flex; flex-direction:column; position:sticky; top:var(--alto-volver);\n'
    '  height:calc(100vh - var(--alto-volver)); overflow-y:auto;')
t = t.replace('</body>', PIE_TABLERO + '\n</body>', 1)
io.open('tablero-financiero.html', 'w', encoding='utf-8').write(t)
print('tablero  · tokens:', n_t, '· oscuros:', fuera_t, '· guiones:', n_gt,
      '· fuentes:', n_ft, '· descargas de Google fuera:', n_dt)


# ══════════════════════════════════════════════════════════════
#  2 · FICHA DE NEGOCIO
# ══════════════════════════════════════════════════════════════
f = io.open('ficha-negocio.html', encoding='utf-8').read()
f, fuera_f = quitar_modo_oscuro(f)
f = anadir_tokens(f)

f, n_f = sustituir_tokens(f, {
    '--bg':               '#EEF1F8',
    '--bg-line':          'rgba(0,20,89,0.035)',
    '--surface':          '#FFFFFF',
    '--surface-2':        '#F5F7FC',
    '--ink':              '#0A1330',
    '--text':             '#4B5670',
    '--text-muted':       '#8895A4',
    '--line':             '#D9E1EE',
    '--line-strong':      '#C3CFE3',
    # El ocre de sello pasa al azul institucional, que es el color
    # de acción en las herramientas del Centro.
    '--accent':           '#25409A',
    '--accent-btn':       '#001459',
    '--accent-ink':       '#001459',
    '--accent-soft':      '#E3EAF7',
    '--accent-contrast':  '#FFFFFF',
    # El segundo acento (verde teal) pasa al azul medio: en la
    # paleta de la Universidad no hay un segundo color de marca.
    '--accent-2':         '#25409A',
    '--accent-2-soft':    '#E3EAF7',
    '--danger':           '#A3252F',
    '--shadow-sm':        '0 1px 2px rgba(0,20,89,.05)',
    '--shadow-lg':        '0 1px 2px rgba(0,20,89,.05), 0 8px 24px -16px rgba(0,20,89,.22)',
})

f = f.replace('--serif:', '--sans-pie: ' + _tipografia.BODY + ';\n    --serif:')

# ── La tipografía del Centro ──
f, n_ff = sustituir_tokens(f, _tipografia.FICHA)
f, n_df = quitar_fuentes_de_google(f)

# ── Fuera el emoji de la cabecera ──
# El 📇 era el único emoji de las dos herramientas. Se va entero, no
# se sustituye por otro símbolo: la cabecera se sostiene con la
# tipografía, que es lo que hacen las demás herramientas del Centro.
# Con el badge vacío quedaría un recuadro gris flotando, así que se
# quita también el <span> y la regla que lo dibujaba.
f = f.replace('<span class="brand-badge" aria-hidden="true">📇</span>\n', '')
f = f.replace('<span class="brand-badge" aria-hidden="true">📇</span>', '')
# Sin el badge, «.brand» se queda con un solo hijo y su «gap» ya no
# separa nada, pero el título arrancaba desplazado por el recuadro.
# Vuelve al margen.
f = f.replace('.brand { display: flex; align-items: flex-start; gap: 0.85rem; margin-bottom: 1.1rem; }',
              '.brand { display: flex; align-items: flex-start; margin-bottom: 1.1rem; }')

# ── Fuera los guiones largos de redacción ──
f, n_gf = quitar_guiones(f, [
    ('Ficha de identificación de negocio — el primer paso antes de ver tu ruta de trámites',
     'Ficha de identificación de negocio. El primer paso antes de ver tu ruta de trámites'),
    ('["etdh", "ETDH — cursos técnicos o certificados de trabajo"]',
     '["etdh", "ETDH: cursos técnicos o certificados de trabajo"]'),
    ('te corresponden a ti — todavía no es la ruta paso a paso, es la base para construirla.',
     'te corresponden a ti. Todavía no es la ruta paso a paso, es la base para construirla.'),
    ('"Orientación general — no es asesoría jurídica ni contable."',
     '"Orientación general. No es asesoría jurídica ni contable."'),
    ('return `${state.numPersonal} persona(s) — vínculo: ',
     'return `${state.numPersonal} persona(s), vínculo: '),
    ('` — ${state.ciiuLabel}`',
     '`: ${state.ciiuLabel}`'),
    ('`${state.ciiuCode} — ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado por el usuario)"',
     '`${state.ciiuCode}: ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado por el usuario)"'),
    ('`${state.ciiuCode} — ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado)"',
     '`${state.ciiuCode}: ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado)"'),
    # Comentarios internos del código: no los ve nadie en pantalla,
    # pero si el criterio es «sin guiones largos», vale para todo el
    # archivo y no solo para lo visible.
    ('// Paso 1 · Actividad — descripción libre',
     '// Paso 1 · Actividad: descripción libre'),
    ('// Paso 10 · Resultado — Ficha + mapa + enlaces',
     '// Paso 10 · Resultado: ficha, mapa y enlaces'),
    ('TOKENS — "Ledger de negocio"', 'TOKENS · "Ledger de negocio"'),
])

# ── La pregunta de contratación estatal, más ancha ──
# «¿Piensas contratar con el Estado?» se leía como «¿vas a ganarte una
# licitación?», y mucha gente que sí entra en el supuesto respondía que
# no: quien le vende a una empresa de servicios públicos, quien es
# proveedor de un contratista, quien maneja productos regulados por una
# entidad estatal. El RUP y los requisitos les aplican igual, así que
# una respuesta equivocada aquí les borra un trámite de su ficha.
f, n_est = quitar_guiones(f, [
    ('"¿Piensas contratar con el Estado (alcaldías, gobernaciones, entidades públicas)?"',
     '"¿Piensas trabajar con el Estado o el gobierno: venderles, ser proveedor de '
     'entidades relacionadas, o manejar productos vinculados a ellas?"'),
    ('"Esto aplica sin importar tu sector, y define si más adelante necesitas '
     'inscribirte en el Registro Único de Proponentes (RUP)."',
     '"Cuenta también si le vendes a alcaldías, gobernaciones, entidades públicas, '
     'empresas estatales o a un contratista de ellas. Aplica sin importar tu sector '
     'y define si más adelante necesitas inscribirte en el Registro Único de '
     'Proponentes (RUP)."'),
    # La ficha de resultado tiene que decir lo mismo que la pregunta.
    ('"Piensa contratar con el Estado → Registro Único de Proponentes (RUP)."',
     '"Piensa trabajar con el Estado o entidades relacionadas: Registro Único de '
     'Proponentes (RUP)."'),
])
n_f += n_est

# El asistente vive en una columna estrecha; el pie es de ancho
# completo, así que sale del contenedor.
f = f.replace('.app-shell {\n    max-width: 760px;', '.app-shell {\n    max-width: 760px;')

PIE_FICHA = pie(
    servicio=(
        '<p><strong>Ficha de Identificación de Negocio</strong> es una herramienta de trabajo '
        'autónomo del Centro de Desarrollo Profesional, Alumni Sabana, para quien está formalizando '
        'un emprendimiento en Colombia.</p>'
        '<p>Recoge lo mínimo que define a tu negocio (actividad, ubicación, figura jurídica, '
        'infraestructura y escala) y te devuelve el mapa de entidades y documentos que te '
        'corresponden. <strong>No es asesoría jurídica ni contable</strong>, no reemplaza a tu '
        'Cámara de Comercio ni a un profesional, y todavía no es la ruta de legalización completa.</p>'
    ),
    datos=(
        '<p>Por ahora, lo que respondes <strong>no se guarda en ninguna parte</strong>: vive solo en '
        'la memoria de esta pestaña mientras la tienes abierta. Al recargar o cerrarla empiezas de '
        'cero, así que copia tu ficha antes de salir.</p>'
        '<p><strong>Próximamente</strong> podrás guardarla en tu cuenta Alumni Sabana y recuperarla '
        'desde cualquier computador, igual que en las demás herramientas del Centro.</p>'
        '<p>El código CIIU que se sugiere es orientativo y no oficial: confírmalo con tu Cámara de '
        'Comercio antes de matricularte, porque de él dependen impuestos y requisitos.</p>'
    ),
    version=VERSION)

f = encabezar(f, 'Ficha de identificacion de negocio del Centro de Desarrollo Profesional de la Universidad de La Sabana: que tramites, entidades y documentos le corresponden a tu emprendimiento en Colombia.')
# ── La ficha, de corrido ──
# El motor nuevo sustituye a render(), navRow() y updateProgress().
# Se inserta justo antes de la llamada final a render(), así que las
# definiciones viejas quedan arriba y estas las pisan: en JavaScript
# la última declaración de una función es la que manda.
# Las etiquetas venían numeradas por tema, no por paso: tres bloques
# seguidos decían «1. Actividad». En una sola página eso se lee como
# una numeración rota. Se deja el tema, que es lo que informa.
for _viejo, _nuevo in [
    ('"1. Actividad"',        '"Actividad"'),
    ('"2. Ubicación"',        '"Ubicación"'),
    ('"3. Figura jurídica"',  '"Figura jurídica"'),
    ('"4. Infraestructura"',  '"Infraestructura"'),
    ('"5. Escala"',           '"Escala"'),
    ('"6. Cualquier sector"', '"Cualquier sector"'),
]:
    f = f.replace('section-tag" }, ' + _viejo, 'section-tag" }, ' + _nuevo)

# Sin botón «Siguiente» ya no hay «.btn-primary» en las tarjetas, y
# los tres sitios que lo desactivaban escriben sobre null: cada tecla
# lanzaba «Cannot set properties of null». El estado sí se guarda
# —esas líneas se conservan—, solo se protege el acceso al botón.
for _v, _n in [
    ('nextBtn.disabled = state.actividadDescripcion.trim().length < 5;',
     'if (nextBtn) nextBtn.disabled = state.actividadDescripcion.trim().length < 5;'),
    ('card.querySelector(".btn-primary").disabled = !isValid();',
     'var _b = card.querySelector(".btn-primary"); if (_b) _b.disabled = !isValid();'),
]:
    if _v not in f:
        raise SystemExit('ERROR: no se encontró para proteger: ' + _v[:50])
    f = f.replace(_v, _n)

f = f.replace('</style>', _ficha_corrido.CSS + '\n</style>', 1)
antes = '  render();\n})();'
if antes not in f:
    raise SystemExit('ERROR: no se encontró la llamada final a render() en la ficha')
f = f.replace(antes, _ficha_corrido.MOTOR + '\n' + antes, 1)

f = f.replace('</style>', PIE_CSS + '\n</style>', 1)
f = f.replace('<body>\n', '<body>\n' + barra_volver() + _ficha_corrido.MARCADO, 1)
f = f.replace('</body>', PIE_FICHA + '\n</body>', 1)
io.open('ficha-negocio.html', 'w', encoding='utf-8').write(f)
print('ficha    · tokens:', n_f, '· oscuros:', fuera_f, '· guiones:', n_gf,
      '· fuentes:', n_ff, '· descargas de Google fuera:', n_df)
