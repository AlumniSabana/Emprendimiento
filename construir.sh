#!/bin/sh
# ══════════════════════════════════════════════════════════════
#  RECONSTRUYE LAS CUATRO PÁGINAS PUBLICABLES
#
#  Uso:  ./construir.sh
#
#  Lo que se edita a mano vive en src/. Lo que se publica son los
#  cuatro HTML de la raíz, y los genera este script. Nunca edites un
#  HTML de la raíz: el siguiente «construir.sh» lo sobreescribe.
#
#    src/fuente.html ........ la portada, con los logos por sustituir
#    src/aplicar.py ......... viste las herramientas y monta la guía
#    src/originales/ ........ los dos HTML tal como llegaron
#
#  Se parte SIEMPRE de src/originales/. Así el resultado no depende
#  de cuántas veces se haya ejecutado antes: aplicar.py dos veces
#  sobre su propia salida duplicaría el pie y la barra de volver.
#
#  La guía de campañas es distinta de las otras dos: no viene de
#  src/originales/ porque no llegó hecha. aplicar.py la monta entera
#  desde _guia_campanas.py y _tablero_campanas.py.
# ══════════════════════════════════════════════════════════════
set -e
cd "$(dirname "$0")"

echo "── 1 · Las tres herramientas ──────────────────────────"
cp src/originales/tablerofinanciero.html src/tablero-financiero.html
cp src/originales/fichanegocio.html      src/ficha-negocio.html
( cd src && python3 aplicar.py )
mv src/tablero-financiero.html src/ficha-negocio.html src/guia-de-campanas.html .

echo "── 2 · La portada ─────────────────────────────────────"
( cd src && ./build.sh )
mv src/emprendimiento-alumni-sabana.html index.html

echo "── 3 · Comprobaciones ─────────────────────────────────"
python3 - <<'PY'
import io, re, sys
fallos = []

def mirar(arch, pruebas):
    s = io.open(arch, encoding='utf-8').read()
    for nombre, cond in pruebas:
        if not cond(s):
            fallos.append(f"{arch}: {nombre}")
            print(f"   FALLA · {arch}: {nombre}")
        else:
            print(f"   ok    · {arch}: {nombre}")

comunes = [
    ("declara la codificación",   lambda s: '<meta charset="UTF-8">' in s),
    ("no quedan logos sin poner", lambda s: 'LOGO_' not in s),
    ("lleva el pie del Centro",   lambda s: 'desarrolloprofesional@unisabana.edu.co' in s),
]
herramienta = comunes + [
    ("la barra de volver está, y una sola vez",
        lambda s: s.count('class="volver-barra"') == 1),
    ("el pie aparece una sola vez",
        lambda s: s.count('<footer class="pie">') == 1),
    ("sin emoji",
        lambda s: not [c for c in s if ord(c) > 0x1F000]),
]

mirar('index.html', comunes + [
    ("enlaza a la ficha",   lambda s: 'ficha-negocio.html' in s),
    ("enlaza al tablero",   lambda s: 'tablero-financiero.html' in s),
    ("enlaza a la guía",    lambda s: 'guia-de-campanas.html' in s),
])
mirar('ficha-negocio.html', herramienta + [
    # Los enlaces van en cada DOCUMENTO y llevan al trámite, no a la
    # portada de la entidad. Si alguien vuelve a poner una portada
    # pelada, el enlace «funciona» pero deja a la persona buscando.
    ("los enlaces llevan al trámite, no a una portada",
        lambda s: 'vue.gov.co/tramites-y-consultas/' in s
              and 'registro-unico-proponentes-rup' in s),
    ("el RUT enlaza a su propia página",
        lambda s: 'RUT/Paginas/Inscripcion-y-actualizacion-RUT' in s),
    # El RUES se quitó a propósito: responde 200 con página vacía a
    # cualquier dirección, así que un enlace roto ahí es indetectable.
    ("no vuelve a colgar de rues.org.co",
        lambda s: 'rues.org.co' not in s),
    ("cada tarjeta lleva su casilla de completado",
        lambda s: 'casillaHecho' in s and 'aria-checked' in s),
    ("está el aviso de vigencia",
        lambda s: 'aviso-vigencia' in s and 'vencido' in s),
    # La Resolución 1732 de 2026 fue revocada por la 2080 de 2026.
    # Decirle a un negocio de salud que puede acogerse a ella lo
    # manda a habilitarse con una norma que no existe.
    ("no afirma que la Resolución 1732 esté vigente",
        lambda s: 'la Resolución 1732 de 2026 reemplaza' not in s),
    ("dice que rige la 3100 de 2019",
        lambda s: 'En salud rige la Resolución 3100 de 2019' in s),
    ("un solo botón de descarga, y en PDF",
        lambda s: 'Descargar en PDF' in s
              and 'Descargar como archivo' not in s
              and 'Copiar al portapapeles' not in s),
])
mirar('tablero-financiero.html', herramienta + [
    # La guía salió del tablero a su propia página. Si un día vuelve
    # a colarse una pestaña aquí, habría dos copias de lo mismo y
    # solo una recibiría las correcciones.
    ("la guía de campañas ya no está dentro",
        lambda s: 'panelCampanas' not in s),
    # Cinco grupos plegables, y en este orden.
    ("el índice tiene los cinco grupos, en orden",
        lambda s: [g for g in re.findall(r'group:"([^"]+)"', s)]
                  == ["Guía", "Datos del mes", "Cálculos", "Rutina", "Resumen"]),
    ("los grupos se pliegan",
        lambda s: 'navgroup-btn' in s and 'aria-expanded' in s),
    ("los cálculos llevan su explicación en palabras sencillas",
        lambda s: 'no perder ni ganar' in s and 'Cuántos meses aguantas' in s),
    # La guía de uso salió de Rutina para ser el primer grupo: es lo
    # que alguien necesita cuando entra y no sabe qué es un runway.
    ("la guía de uso ya no está dentro de Rutina",
        lambda s: '{group:"Rutina", items:[\n    {id:"cierre"' in s),
])
mirar('guia-de-campanas.html', herramienta + [
    # Lee el localStorage del tablero para no volver a preguntar lo
    # que la persona ya escribió. Si la clave se pierde en un
    # refactor, la página sigue funcionando pero pide las cifras
    # otra vez, y nadie se entera hasta que alguien se queja.
    ("lee las cifras del tablero",
        lambda s: 'tf_dashboard_v1' in s),
    # Se lee esa clave, nunca se escribe: escribir ahí pisaría el
    # registro detallado del tablero con tres números de memoria.
    ("no escribe en la clave del tablero",
        lambda s: 'setItem(CLAVE_TABLERO' not in s
              and 'setItem("tf_dashboard_v1"' not in s),
    ("sabe que se muestra suelta",
        lambda s: 'window.CAMPANAS_SUELTA = true;' in s),
    # El enlace a Pomelli tiene que ser el general. Una dirección
    # «/campaigns/<código>» es la de una campaña guardada dentro de
    # UNA cuenta: a los demás les sale la pantalla de inicio de
    # sesión de Google y nunca llegan a la campaña.
    ("el enlace a Pomelli es el público",
        lambda s: 'labs.google/pomelli' in s and '/pomelli/campaigns/' not in s),
    ("dice que Pomelli está en inglés",
        lambda s: 'En inglés' in s or 'en inglés' in s),
])

# El JavaScript de las tres tiene que ser válido. Un error de coma
# no se ve al abrir la página: los botones dejan de responder y ya.
import subprocess, tempfile
for arch in ('index.html', 'ficha-negocio.html', 'tablero-financiero.html',
             'guia-de-campanas.html'):
    s = io.open(arch, encoding='utf-8').read()
    js = "".join(re.findall(r'<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>', s, re.S))
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as fh:
        fh.write(js); ruta = fh.name
    r = subprocess.run(['node', '--check', ruta], capture_output=True, text=True)
    if r.returncode:
        fallos.append(f"{arch}: JavaScript inválido")
        print(f"   FALLA · {arch}: JavaScript inválido\n{r.stderr[:300]}")
    else:
        print(f"   ok    · {arch}: JavaScript válido")

if fallos:
    print("\nNO se publica: " + str(len(fallos)) + " comprobación(es) fallaron.")
    sys.exit(1)
print("\nLas cuatro páginas están listas para publicar.")
PY
