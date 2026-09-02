#!/bin/sh
# ══════════════════════════════════════════════════════════════
#  RECONSTRUYE LAS TRES PÁGINAS PUBLICABLES
#
#  Uso:  ./construir.sh
#
#  Lo que se edita a mano vive en src/. Lo que se publica son los
#  tres HTML de la raíz, y los genera este script. Nunca edites un
#  HTML de la raíz: el siguiente «construir.sh» lo sobreescribe.
#
#    src/fuente.html ........ la portada, con los logos por sustituir
#    src/aplicar.py ......... viste las dos herramientas
#    src/originales/ ........ los dos HTML tal como llegaron
#
#  Se parte SIEMPRE de src/originales/. Así el resultado no depende
#  de cuántas veces se haya ejecutado antes: aplicar.py dos veces
#  sobre su propia salida duplicaría el pie y la barra de volver.
# ══════════════════════════════════════════════════════════════
set -e
cd "$(dirname "$0")"

echo "── 1 · Las dos herramientas ───────────────────────────"
cp src/originales/tablerofinanciero.html src/tablero-financiero.html
cp src/originales/fichanegocio.html      src/ficha-negocio.html
( cd src && python3 aplicar.py )
mv src/tablero-financiero.html src/ficha-negocio.html .

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
])
mirar('ficha-negocio.html', herramienta)
mirar('tablero-financiero.html', herramienta)

# El JavaScript de las tres tiene que ser válido. Un error de coma
# no se ve al abrir la página: los botones dejan de responder y ya.
import subprocess, tempfile
for arch in ('index.html', 'ficha-negocio.html', 'tablero-financiero.html'):
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
print("\nLas tres páginas están listas para publicar.")
PY
