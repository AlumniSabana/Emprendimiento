#!/bin/sh
# ══════════════════════════════════════════════════════════════
#  MONTA LA PORTADA DE EMPRENDIMIENTO
#
#  Uso:  ./build.sh
#
#  Incrusta los tres logos en base64 dentro de fuente.html y deja
#  el resultado en emprendimiento-alumni-sabana.html: un solo
#  archivo, sin carpeta de imágenes al lado, que se abre con doble
#  clic y funciona sin internet.
#
#  Después comprueba la sintaxis del JavaScript. Un error de coma
#  en el bloque DIRECCIONES no se ve al abrir la página —los
#  botones simplemente dejan de llevar a ninguna parte—, así que
#  se detecta aquí y no en producción.
# ══════════════════════════════════════════════════════════════
cd "$(dirname "$0")"

python3 - <<'PY'
import io
def img(n): return "data:image/png;base64," + open(n).read().strip()
s = io.open("fuente.html", encoding="utf8").read()
s = (s.replace("LOGO_ALUMNI", img("_logo_claro.txt"))
      .replace("LOGO_USABANA_NAVY", img("_logo_usabana_navy.txt"))
      .replace("LOGO_USABANA_BLANCO", img("_logo_usabana_blanco.txt")))
assert "LOGO_" not in s, "quedó un logo sin sustituir"
io.open("emprendimiento-alumni-sabana.html", "w", encoding="utf8").write(s)
PY

python3 - <<'PY'
import re, io
h = io.open("emprendimiento-alumni-sabana.html", encoding="utf8").read()
io.open("_check.js", "w", encoding="utf8").write(re.findall(r"<script>(.*?)</script>", h, re.S)[-1])
PY
node --check _check.js && rm -f _check.js && echo "SINTAXIS JS OK"
