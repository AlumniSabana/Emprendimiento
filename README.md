# Herramientas de emprendimiento · Centro de Desarrollo Profesional

Alumni Sabana · Universidad de La Sabana

Tres páginas HTML autónomas. Sin dependencias, sin CDN, sin proceso de
compilación: cada archivo publicable lleva dentro sus estilos, su
JavaScript y sus imágenes en base64. Se abren con doble clic y
funcionan sin conexión.

| Página | Archivo | Estado |
|---|---|---|
| Portada | `index.html` | publicada |
| Ficha de identificación de negocio | `ficha-negocio.html` | publicada |
| Tablero de apoyo financiero | `tablero-financiero.html` | publicada |
| Chat de ideación | — | por construir |
| Guía de campañas publicitarias | — | por construir |

## Cómo está organizado

**Nunca edites un HTML de la raíz.** Los genera `construir.sh` y el
siguiente build los sobreescribe sin avisar.

```
├── index.html                    ← se genera
├── ficha-negocio.html            ← se genera
├── tablero-financiero.html       ← se genera
├── construir.sh                  ← genera las tres y las comprueba
└── src/
    ├── fuente.html               ← la portada: AQUÍ se edita
    ├── build.sh                  ← incrusta los logos en la portada
    ├── aplicar.py                ← viste las dos herramientas
    ├── _comun.py                 ← paleta, pie y barra de volver
    ├── _crest.txt, _logo_*.txt   ← imágenes en base64
    └── originales/               ← los dos HTML tal como llegaron
```

`aplicar.py` parte **siempre** de `src/originales/`. Es deliberado: si
partiera del resultado anterior, ejecutarlo dos veces duplicaría el pie
y la barra de volver. Esto hace que el build sea repetible.

## Publicar un cambio

```sh
./construir.sh          # genera las tres páginas y las comprueba
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

**Cambiar el pie o la paleta de las dos herramientas** → `src/_comun.py`.
Está en un solo sitio a propósito: el pie del Centro se ha reescrito ya
varias veces y teniéndolo duplicado un cambio siempre se quedaba a medias
en uno de los dos archivos.

**Forzar que el navegador lea la versión nueva** → sube `VERSION` en
`src/fuente.html` y en `src/aplicar.py`. Los navegadores cachean estas
páginas con fuerza; sin cambiar la marca, alguien puede seguir viendo la
anterior durante días.

## Lo que este build comprueba antes de dejarte publicar

- Las tres declaran `<meta charset>`, sin lo cual se rompen las tildes.
- No queda ningún marcador `LOGO_` sin sustituir.
- El pie del Centro está, y una sola vez.
- La barra de «Volver» está, y una sola vez.
- No hay emoji.
- El JavaScript de las tres es sintácticamente válido. Un error de coma
  no se ve al abrir la página: los botones simplemente dejan de
  responder.

## Sobre los datos

Ninguna de las tres envía nada a un servidor. El tablero guarda en el
`localStorage` del navegador; la ficha vive solo en memoria mientras la
pestaña está abierta. Cuando eso cambie, **primero se cambia lo que
promete el pie y después el código**, nunca al revés: decirle a alguien
que su trabajo está guardado cuando no lo está le hace perder el trabajo.
