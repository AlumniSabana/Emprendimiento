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
    # «goBack» movía el índice del asistente paso a paso, que dejó de
    # leerse al pasar la ficha a scroll de corrido: el botón repintaba
    # lo mismo y no llevaba a ninguna parte.
    #
    # Queda UNA mención, dentro del navRow original. Ese navRow está
    # sobrescrito por el de _ficha_corrido.py —se declara después, en
    # el mismo ámbito— así que nunca se ejecuta. Se cuenta en vez de
    # exigir cero: si aparecieran dos, sería que el botón del
    # resultado volvió a colgar de goBack.
    ("el botón del resultado ya no cuelga de goBack",
        lambda s: s.count('onclick: goBack') == 1),
    ("y lleva de vuelta a las preguntas",
        lambda s: 'Volver a mis respuestas' in s),
    ("el resultado va sin recuadro",
        lambda s: 'resultado-final' in s),
    # Las columnas de la rejilla dependen de cuántas entidades hay,
    # para que la última fila no quede con una tarjeta suelta.
    ("la rejilla de entidades se equilibra",
        lambda s: 'columnasPara' in s and 'COLUMNAS_POR_CANTIDAD' in s),
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
    # Los gastos fijos también se pueden subir en CSV.
    ("los gastos fijos se pueden importar",
        lambda s: 'bloqueImportarFijos' in s and 'impfZona' in s),
    # Los cuatro cálculos llevan su dibujo.
    # Los dibujos viajan dentro de un JSON, así que sus comillas van
    # escapadas: se busca la forma escapada, no «viewBox="0 0 300 250"».
    ("los cuatro cálculos llevan dibujo",
        lambda s: all(k in s for k in ('"precio":', '"equilibrio":', '"runway":', '"asignacion":'))
              and s.count(r'<svg viewBox=\"0 0 300 250\"') == 4),
    # El vídeo va colgado del título del término: si el título se
    # renombra y el mapa de vídeos no, el vídeo desaparece sin ruido.
    ("el apartado retitulado conserva su vídeo",
        lambda s: '"A dónde va cada peso que entra"' in s
              and 'Separación negocio / personal' not in s),
    # Los cuatro porcentajes van dos y dos, no tres y uno suelto.
    ("los porcentajes van en dos filas de dos",
        lambda s: 'style="margin-top:16px; max-width:33%"' not in s
              and s.count('allocField("sueldo"') == 1),
    # Pasarse del 100% y quedarse corto no son el mismo error.
    ("avisa distinto al pasarse del 100%",
        lambda s: 'Te estás repartiendo más de lo que entra' in s
              and 'Falta por asignar' in s),
    # La barra encogía los segmentos para que cupieran, así que 110%
    # se veía igual que 100%: llena de lado a lado.
    ("la barra usa el ancho proporcional, no el crudo",
        lambda s: 'style="width:\'+Math.max(w,0)+\'%' in s),
    ("y marca dónde quedó el 100%",
        lambda s: 'alloc-limite' in s),
    # El árbol de la guía.
    ("la guía lleva el árbol que crece",
        lambda s: 'bloqueArbol()' in s and 'arbol-caja' in s),
    ("el árbol tiene sus seis etapas",
        lambda s: s.count('Aquí está la semilla') >= 1
              and s.count('dando fruto') >= 1),
    ("cuenta lo que de verdad puede saber",
        lambda s: 'Secciones abiertas' in s and 'Videos abiertos' in s),
    # Cada término de la guía dice a qué paso pertenece.
    ("cada término de la guía lleva su paso",
        lambda s: 'subtituloPaso' in s and 'paso-guia' in s),
    # Las claves de PASOS son títulos de GUIDE: si uno se renombra
    # allí y aquí no, ese término se queda mudo sin que nada falle.
    ("los pasos cubren los doce términos",
        lambda s: (lambda titulos, pasos: all(t in pasos for t in titulos))(
            re.findall(r'\{t:"([^"]+)"', s[s.find('var GUIDE = ['):]),
            s[s.find('var PASOS_GUIA'):s.find('var CLASES_PASO')])),
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
    # Tres secciones que se recorren de lado, no bajando.
    ("va en tres secciones horizontales",
        lambda s: s.count('class="diapo"') == 3
              and 'pasos-barra' in s and 'translateX' in s),
    ("las piezas y la IA no se quedaron en la primera",
        lambda s: 'id="piezas"' in s and 'id="ia"' in s),
    # La sección de Gemini dice qué falta para encenderla en vez de
    # limitarse a un botón gris.
    ("la sección de IA explica qué falta",
        lambda s: 'Qué falta para encenderlo' in s
              and 'clave de API' in s),
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
