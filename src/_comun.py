# ══════════════════════════════════════════════════════════════
#  LO QUE COMPARTEN LAS DOS HERRAMIENTAS
#  Paleta institucional y pie de página, en un solo sitio.
#
#  Se inyecta en los dos HTML con aplicar.py. Está aquí y no
#  duplicado en cada archivo porque el pie de las herramientas del
#  CDP se ha reescrito ya tres veces: teniéndolo una sola vez, el
#  siguiente cambio no puede quedarse a medias en uno de los dos.
# ══════════════════════════════════════════════════════════════

import io

CREST = io.open('_crest.txt', encoding='utf-8').read().strip()

# La portada desde la que se entra a las dos herramientas.
#
# Es «./» y no un nombre de archivo: en el repositorio la portada se
# publica como index.html, así que la raíz del sitio YA es la portada.
# Poner «index.html» funcionaría, pero deja la dirección fea
# (misitio.com/index.html) y obliga a cambiarlo aquí el día que se
# publique en un subdirectorio. Con «./» el enlace es correcto en los
# tres sitios: en Vercel, en un subdirectorio y abriendo el archivo
# desde el disco.
PORTADA = './'

# ── LA PALETA ─────────────────────────────────────────────────
# La institucional de la Universidad de La Sabana, idéntica a la
# de «Estudio de Pitch» y «Construye tu portafolio». El azul
# #001459 es el oficial; los tonos 700/500/300 son sus derivados.
#
# No hay modo oscuro, y es deliberado: la identidad de la
# Universidad se mantiene igual en cualquier dispositivo y no
# depende de la preferencia del sistema. Las dos herramientas
# traían un tema oscuro completo; se retira por eso.
PALETA = """
  /* Superficies y texto: neutros con matiz azul */
  --paper: #EEF1F8;
  --surface: #FFFFFF;
  --surface-2: #F5F7FC;
  --ink: #0A1330;
  --ink-soft: #4B5670;
  --ink-faint: #8895A4;
  --rule: #D9E1EE;
  --rule-soft: #E9EEF7;

  /* Color institucional */
  --azul: #001459;
  --azul-700: #1E306E;
  --azul-500: #25409A;
  --azul-300: #7FA6D0;
  --azul-soft: #E3EAF7;

  /* Estados. El ámbar NO es el rojo de alerta: un dato pendiente
     no es un error, y pintarlo de rojo hace que quien lo lee
     cierre la herramienta en vez de completarlo. */
  --ok: #158A5E;
  --ok-soft: #E4F2EC;
  --ambar: #8A5200;
  --ambar-soft: #FBEFDD;
  --alerta: #A3252F;
  --alerta-soft: #FAE8E9;

  --on-azul: #FFFFFF;
  --shadow: 0 1px 2px rgba(0,20,89,.05), 0 8px 24px -16px rgba(0,20,89,.22);
"""

# ── EL PIE ────────────────────────────────────────────────────
PIE_CSS = """
/* ═══════════════ PIE INSTITUCIONAL ═══════════════
   Idéntico al de «Estudio de Pitch» y «Construye tu portafolio»,
   para que las herramientas del Centro se lean como un solo
   servicio y no como cinco páginas sueltas. */
/* Sin «margin-top». Lo llevaba, y en el tablero dejaba una franja
   de papel de 48 px entre el final del índice lateral azul y el
   pie azul: dos bloques del mismo color separados por una línea
   clara que parecía un error de montaje. El aire que necesita el
   pie ya lo pone su propio «padding» de arriba. */
footer.pie { background: var(--azul); color: #B9C9E2; padding: 3rem 0 1.6rem; }

/* ═══════════════ VOLVER A LA PORTADA ═══════════════
   Arriba, antes de nada. Estuvo en el pie y era un error: para
   salir de una herramienta había que recorrerla entera hasta el
   final. La salida se busca donde se entró, no al fondo.

   No es fijo ni flotante: en el tablero cualquier elemento fijo
   tapa una columna de cifras, y en la ficha se comería el paso
   del asistente. Va en el flujo, lo primero del documento. */
/* La altura de la barra vive en una variable porque el índice
   lateral del tablero la necesita para calcular la suya. Si aquí
   cambia el «padding», allí se ajusta solo. */
:root { --alto-volver: 51px; }
.volver-barra {
  background: var(--azul);
  border-bottom: 1px solid rgba(255,255,255,.14);
  position: sticky; top: 0; z-index: 50;
}
.volver-barra .env {
  max-width: 1440px; margin: 0 auto;
  padding: .62rem clamp(1.1rem, 4vw, 2.75rem);
  display: flex; align-items: center; gap: .9rem; flex-wrap: wrap;
}
.volver-barra a {
  display: inline-flex; align-items: center; gap: .5rem;
  color: #FFFFFF; text-decoration: none;
  font-family: var(--sans-pie); font-size: .87rem; font-weight: 600;
  padding: .3rem .2rem; border-radius: 4px;
  transition: color .15s;
}
.volver-barra a:hover { color: #C7D6F0; }
.volver-barra a:hover .flecha { transform: translateX(-3px); }
.volver-barra .flecha {
  font-size: 1.05em; line-height: 1;
  transition: transform .15s;
}
.volver-barra small { color: #A9BEDE; font-size: .78rem; line-height: 1.5; }
.volver-barra a:focus-visible { outline: 2px solid #FFFFFF; outline-offset: 2px; }
@media (max-width: 560px) { .volver-barra small { display: none; } }
@media print { .volver-barra { display: none !important; } }
.pie-envoltura { max-width: 1440px; margin: 0 auto; padding: 0 clamp(1.1rem, 4vw, 2.75rem); }
.pie-rejilla {
  display: grid; grid-template-columns: 1.15fr 1fr 1.35fr 1fr;
  gap: 2.5rem; padding-bottom: 2.2rem; border-bottom: 1px solid rgba(255,255,255,.17);
}
.pie-logo { height: 48px; width: auto; display: block; margin-bottom: 1.15rem; }
.pie-col h4 {
  font-family: var(--sans-pie); font-size: .68rem; letter-spacing: .14em;
  text-transform: uppercase; color: #FFFFFF; font-weight: 700; margin: 0 0 .9rem;
}
.pie-col p { font-size: .82rem; line-height: 1.65; color: #B9C9E2; margin: 0 0 .7rem; }
.pie-col p:last-child { margin-bottom: 0; }
.pie-col strong { color: #E7EEF9; font-weight: 600; }
.pie-marca p { font-size: .78rem; color: #9FB2CE; }
.pie-enlace {
  color: #C7D6F0; text-decoration: none; border-bottom: 1px solid rgba(199,214,240,.4);
  padding-bottom: 1px; transition: color .15s, border-color .15s;
}
.pie-enlace:hover { color: #FFFFFF; border-bottom-color: #FFFFFF; }
.pie-legal {
  display: flex; justify-content: space-between; gap: 1.25rem; flex-wrap: wrap;
  padding-top: 1.4rem; font-size: .74rem; color: #8FA5C6; line-height: 1.6;
}
.pie-legal .pie-enlace { font-weight: 500; color: #B9C9E2; }
@media (max-width: 1000px) { .pie-rejilla { grid-template-columns: 1fr 1fr; gap: 2rem; } }
@media (max-width: 640px)  { .pie-rejilla { grid-template-columns: 1fr; } }
@media print { footer.pie { display: none !important; } }
"""


def barra_volver():
    """La barra de vuelta a la portada. Va como primer elemento del
    <body>, antes de la herramienta."""
    return f"""<div class="volver-barra">
  <div class="env">
    <a href="{PORTADA}"><span class="flecha" aria-hidden="true">&larr;</span> Volver a las herramientas</a>
    <small>Herramientas de emprendimiento &middot; Centro de Desarrollo Profesional</small>
  </div>
</div>
"""


def pie(servicio, datos, version):
    """El pie completo. «servicio» y «datos» son los dos párrafos que
    cambian de una herramienta a otra; el resto es idéntico."""
    return f"""
<footer class="pie">
  <div class="pie-envoltura">
    <div class="pie-rejilla">

      <div class="pie-col pie-marca">
        <img class="pie-logo" src="data:image/png;base64,{CREST}" alt="Universidad de La Sabana" width="241" height="64">
        <p>Institución de educación superior sujeta a inspección y vigilancia por el Ministerio de Educación Nacional.</p>
        <p>Carácter Académico: Universidad.</p>
      </div>

      <div class="pie-col">
        <h4>El servicio</h4>
        {servicio}
      </div>

      <!-- TRATAMIENTO DE DATOS · el bloque que hay que cambiar el día
           que estas herramientas guarden en la cuenta Alumni Sabana.
           Hoy dicen lo que de verdad hacen. Cuando se conecte
           Supabase, la frase de «por ahora» se sustituye por la del
           portafolio: «se guarda en tu cuenta de la Universidad, por
           eso lo recuperas desde cualquier computador». -->
      <div class="pie-col">
        <h4>Tratamiento de datos</h4>
        {datos}
        <p><a class="pie-enlace" href="https://www.unisabana.edu.co/politica-de-proteccion-de-datos" target="_blank" rel="noopener">Política de Protección de Datos de la Universidad ↗</a></p>
      </div>

      <div class="pie-col">
        <h4>Contacto</h4>
        <p>Centro de Desarrollo Profesional<br>Alumni Sabana</p>
        <p><a class="pie-enlace" href="mailto:desarrolloprofesional@unisabana.edu.co">desarrolloprofesional@unisabana.edu.co</a></p>
        <p>Contact center: (601) 861 5555</p>
        <p>Campus del Puente del Común<br>Km. 7, Autopista Norte de Bogotá<br>Chía, Cundinamarca, Colombia</p>
      </div>

    </div>

    <div class="pie-legal">
      <span>Universidad de La Sabana &middot; Personería Jurídica: Resolución 130 del 14 de enero de 1980, Ministerio de Educación Nacional<br>Versión del archivo: <b>{version}</b></span>
      <span><a class="pie-enlace" href="https://www.unisabana.edu.co/politica-de-proteccion-de-datos" target="_blank" rel="noopener">Política de Protección de Datos</a> &middot; Vigilada Mineducación</span>
    </div>
  </div>
</footer>
"""
