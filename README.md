# Herramientas de emprendimiento · Centro de Desarrollo Profesional

Alumni Sabana · Universidad de La Sabana

Cuatro páginas HTML autónomas. Sin dependencias, sin CDN, sin proceso de
compilación: cada archivo publicable lleva dentro sus estilos, su
JavaScript y sus imágenes en base64. Se abren con doble clic y
funcionan sin conexión.

| Página | Archivo | Estado |
|---|---|---|
| Portada | `index.html` | publicada |
| Ficha de identificación de negocio | `ficha-negocio.html` | publicada |
| Tablero de apoyo financiero | `tablero-financiero.html` | publicada |
| Guía de campañas publicitarias | `guia-de-campanas.html` | publicada |
| Chat de ideación | — | por construir |

## Cómo está organizado

**Nunca edites un HTML de la raíz.** Los genera `construir.sh` y el
siguiente build los sobreescribe sin avisar.

```
├── index.html                    ← se genera
├── ficha-negocio.html            ← se genera
├── tablero-financiero.html       ← se genera
├── guia-de-campanas.html         ← se genera
├── construir.sh                  ← genera las cuatro y las comprueba
└── src/
    ├── fuente.html               ← la portada: AQUÍ se edita
    ├── build.sh                  ← incrusta los logos en la portada
    ├── aplicar.py                ← viste las dos herramientas y monta la guía
    ├── _comun.py                 ← paleta, pie y barra de volver
    ├── _guia_campanas.py         ← el armazón de la guía: cabecera y cifras
    ├── _tablero_campanas.py      ← el contenido de la guía: canales y piezas
    ├── _crest.txt, _logo_*.txt   ← imágenes en base64
    └── originales/               ← los dos HTML tal como llegaron
```

Las dos primeras herramientas se construyen **transformando** un archivo
que llegó hecho. La guía de campañas no: se monta entera desde `src/`,
porque no existía. Por eso no tiene nada en `originales/`.

`aplicar.py` parte **siempre** de `src/originales/`. Es deliberado: si
partiera del resultado anterior, ejecutarlo dos veces duplicaría el pie
y la barra de volver. Esto hace que el build sea repetible.

## Publicar un cambio

```sh
./construir.sh          # genera las cuatro páginas y las comprueba
git add -A
git commit -m "Qué cambió y por qué"
git push
```

Vercel publica solo al recibir el push. Si `construir.sh` falla, no
hagas push: termina con código 1 y dice qué comprobación no pasó.

## Tareas frecuentes

**Cambiar un texto de la portada** → `src/fuente.html`.

**Activar una herramienta que está en «Próximamente»**
1. En `src/fuente.html`, añade su dirección al bloque `DIRECCIONES`.
2. En su `<article>`, quita el atributo `data-pronto`, la
   `<span class="marca-pronto">` y cambia el `<span class="boton-pronto">`
   por `<a class="boton" data-destino="…" href="#">`.

**Cambiar el texto o los canales de la guía de campañas** →
`src/_tablero_campanas.py`. Ese archivo es solo el contenido y no sabe
dónde se muestra; el armazón de la página está en `src/_guia_campanas.py`.

**Cambiar el pie o la paleta de las dos herramientas** → `src/_comun.py`.
Está en un solo sitio a propósito: el pie del Centro se ha reescrito ya
varias veces y teniéndolo duplicado un cambio siempre se quedaba a medias
en uno de los dos archivos.

**Forzar que el navegador lea la versión nueva** → sube `VERSION` en
`src/fuente.html` y en `src/aplicar.py`. Los navegadores cachean estas
páginas con fuerza; sin cambiar la marca, alguien puede seguir viendo la
anterior durante días.

## Lo que este build comprueba antes de dejarte publicar

- Las cuatro declaran `<meta charset>`, sin lo cual se rompen las tildes.
- No queda ningún marcador `LOGO_` sin sustituir.
- El pie del Centro está, y una sola vez.
- La barra de «Volver» está, y una sola vez.
- No hay emoji.
- El JavaScript de las cuatro es sintácticamente válido. Un error de coma
  no se ve al abrir la página: los botones simplemente dejan de
  responder.
- La guía de campañas ya no está dentro del tablero. Si volviera a
  colarse allí habría dos copias de lo mismo, y solo una recibiría las
  correcciones.
- La guía lee la clave del tablero, y **no** escribe en ella.

## Sobre los datos

Ninguna de las cuatro envía nada a un servidor. El tablero y la guía de
campañas guardan en el `localStorage` del navegador; la ficha vive solo en
memoria mientras la pestaña está abierta.

La guía **lee** la clave del tablero (`tf_dashboard_v1`) para no volver a
preguntar unas cifras que la persona ya escribió, y guarda lo suyo en una
clave aparte. Nunca escribe en la del tablero: tres números tecleados de
memoria aquí borrarían el registro detallado de allí sin que nadie se
entere. Cuando eso cambie, **primero se cambia lo que
promete el pie y después el código**, nunca al revés: decirle a alguien
que su trabajo está guardado cuando no lo está le hace perder el trabajo.
