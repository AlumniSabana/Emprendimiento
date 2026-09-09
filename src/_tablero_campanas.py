# ══════════════════════════════════════════════════════════════
#  GUÍA DE CAMPAÑAS PUBLICITARIAS · EL CONTENIDO
#
#  La etapa 3 de la portada, «Crecimiento de negocio».
#
#  ── DÓNDE VIVE ────────────────────────────────────────────────
#  En su propia página: guia-de-campanas.html. Estuvo dentro del
#  tablero, en una pestaña, y se sacó porque es una etapa distinta
#  del recorrido: quien ya vende y solo quiere saber dónde
#  anunciarse no debería entrar a un tablero financiero para
#  encontrarla.
#
#  Este archivo es SOLO el contenido —el CSS y el JS de la guía—.
#  El armazón de la página (cabecera, campos de cifras, lectura del
#  tablero) vive en _guia_campanas.py. Separados así, el contenido
#  no sabe dónde se muestra, y por eso la única bifurcación que hay
#  es «CAMPANAS_SUELTA», para los dos textos que cambian.
#
#  ── LO QUE LA HACE ÚTIL ───────────────────────────────────────
#  El presupuesto sale de sus ingresos reales, no de una cifra
#  inventada. Y comprueba que invertir eso no lo deje por debajo
#  de su punto de equilibrio: es la diferencia entre una guía y
#  un consejo genérico de internet.
#
#  Si alguien factura 2 millones y su punto de equilibrio está en
#  1,8, no le sobran 200 mil para publicidad: le sobran cero. Eso
#  hay que decirlo, aunque sea la respuesta incómoda.
#
#  ── EL PLAN ES POR REGLAS, NO POR IA ──────────────────────────
#  El semáforo del Centro pone «investigación de mercados» en uso
#  condicionado. Un plan armado con reglas explícitas —las que se
#  leen abajo— no es investigación de mercados: es la misma tabla
#  que daría un asesor con la misma información.
#
#  El botón de «afinar con IA» queda construido pero DESACTIVADO,
#  con su nota, hasta que el Centro autorice. Activarlo es quitar
#  «CAMPANAS_IA_ACTIVA = false».
# ══════════════════════════════════════════════════════════════

CSS = """
/* ═══════════════ GUÍA DE CAMPAÑAS ═══════════════ */
.camp-aviso {
  background: var(--warn-soft); border: 1px solid var(--gold);
  border-left: 3px solid var(--gold);
  border-radius: 0 8px 8px 0; padding: 12px 14px; margin-bottom: 16px;
  font-size: 13px; line-height: 1.6; color: var(--ink);
}
.camp-aviso b { color: var(--gold); }

.camp-cifras {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px; margin-bottom: 18px;
}
.camp-cifra {
  background: var(--paper-sunken); border: 1px solid var(--line);
  border-radius: 9px; padding: 12px 14px;
}
.camp-cifra .k {
  display: block; font-size: 10.5px; letter-spacing: .1em;
  text-transform: uppercase; color: var(--ink-soft); margin-bottom: 4px;
}
.camp-cifra .v {
  display: block; font-family: var(--font-mono); font-size: 19px;
  font-weight: 600; color: var(--ink); font-variant-numeric: tabular-nums;
}
.camp-cifra .n { display: block; font-size: 11.5px; color: var(--ink-soft); margin-top: 3px; }
.camp-cifra.alerta { border-color: var(--critical); background: var(--critical-soft); }
.camp-cifra.alerta .v { color: var(--critical); }

/* Cada canal es una ficha con su porqué, no una lista de nombres. */
.camp-canal {
  border: 1px solid var(--line); border-radius: 10px;
  padding: 14px 16px; margin-bottom: 12px; background: var(--paper-raised);
}
.camp-canal-cab {
  display: flex; align-items: baseline; gap: 10px;
  flex-wrap: wrap; margin-bottom: 6px;
}
.camp-canal h4 { margin: 0; font-size: 15px; }
.camp-canal .orden {
  font-family: var(--font-mono); font-size: 10.5px; font-weight: 700;
  letter-spacing: .1em; color: var(--gold);
}
.camp-canal .plata {
  margin-left: auto; font-family: var(--font-mono); font-size: 13px;
  font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums;
}
.camp-canal p { margin: 0 0 8px; font-size: 13px; line-height: 1.6; color: var(--ink-soft); }
.camp-canal .porque {
  font-size: 12.5px; color: var(--ink); background: var(--accent-soft);
  border-radius: 6px; padding: 8px 10px; line-height: 1.55;
}
.camp-canal .porque b { color: var(--accent); }

.camp-medir { margin-top: 6px; }
.camp-medir li { font-size: 13px; line-height: 1.65; color: var(--ink-soft); }

/* ── Las piezas de ejemplo ──
   Recreadas en CSS y no incrustadas como imagen: pesan casi nada,
   se ven nítidas en cualquier pantalla, y si el Centro cambia un
   mensaje se edita el texto sin volver a generar la pieza. Además
   así llevan el azul institucional exacto, no el que aproximó la
   herramienta que las generó. */
.camp-piezas {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px; margin: 14px 0 16px;
}
.pieza {
  /* «min-height» y no «aspect-ratio».
     Con la proporción fija, la caja no puede crecer: en una columna
     estrecha el texto más largo desbordaba y la palabra «EJEMPLO» se
     cortaba contra el borde de abajo. Una pieza de redes sí tiene
     proporción fija, pero esto no es la pieza: es su vista previa, y
     vale más que se lea entera a que conserve el 4:5 exacto.
     El mínimo mantiene el aire de cartel cuando el texto es corto. */
  min-height: 260px;
  border-radius: 12px; overflow: hidden;
  background: linear-gradient(168deg, #0A2166 0%, var(--accent) 62%);
  color: #FFFFFF;
  padding: 20px 18px;
  display: flex; flex-direction: column;
  border: 1px solid rgba(255,255,255,.12);
  box-shadow: 0 12px 28px -14px rgba(0,20,89,.5);
}
.pieza .marca {
  font-family: var(--font-display);
  font-size: 15px; line-height: 1.1; font-weight: 600;
  text-align: center; color: #FFFFFF;
  padding-bottom: 10px; margin-bottom: 14px;
  border-bottom: 1px solid rgba(255,255,255,.28);
}
.pieza .marca span { display: block; }
.pieza h5 {
  font-family: var(--font-display);
  font-size: clamp(17px, 2.4vw, 21px); line-height: 1.15;
  margin: 0 0 10px; text-align: center; font-weight: 600;
  text-wrap: balance;
}
.pieza p {
  /* 13.5 y no 12.5: el contraste ya era correcto (9:1), lo que se
     veía apagado era la escala junto a un titular de 21 px. */
  font-size: 13.5px; line-height: 1.5; text-align: center;
  color: #C8D6EC; margin: 0 0 auto;
}
.pieza .pie-pieza {
  font-size: 10.5px; letter-spacing: .09em; text-transform: uppercase;
  text-align: center; color: #8FA5C6; margin-top: 14px;
}
.camp-fuente {
  border: 1px solid var(--line); border-radius: 10px;
  padding: 14px 16px; margin-top: 16px; background: var(--paper-raised);
}
.camp-fuente h4 { margin: 0 0 4px; font-size: 14px; }
/* «> p» y no «p» a secas. Las piezas viven DENTRO de este bloque, y
   con el selector suelto esta regla —que va después y tiene la misma
   especificidad— le ganaba a «.pieza p» y pintaba de gris pizarra el
   texto de las piezas, sobre su fondo azul oscuro: 2:1 de contraste,
   ilegible. Se veía apagado y se atribuyó al tamaño de letra; era
   esto. El hijo directo deja fuera lo que está dentro de las piezas. */
.camp-fuente > p { margin: 0 0 10px; font-size: 12.5px; color: var(--ink-soft); line-height: 1.6; }
.camp-fuente a.btn { text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }

/* ── El bloque de Pomelli ──
   Separado del texto de las piezas por una línea: es una
   herramienta de terceros, no una parte más de la guía, y
   conviene que se lea como tal antes de pulsar el botón. */
.camp-pomelli { border-top: 1px solid var(--line); margin-top: 14px; padding-top: 14px; }
.camp-pomelli h4 {
  margin: 0 0 8px; font-size: 14px;
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.camp-pomelli p { margin: 0 0 9px; font-size: 12.5px; color: var(--ink-soft); line-height: 1.65; }
.camp-pomelli p b { color: var(--ink); }
/* El idioma, junto al nombre y no enterrado en el párrafo: es lo
   primero que alguien necesita saber antes de decidir si entra. */
.camp-idioma {
  font-family: var(--font-sans); font-size: 10px; font-weight: 700;
  letter-spacing: .08em; text-transform: uppercase;
  color: var(--gold); background: var(--gold-soft);
  border-radius: 999px; padding: 3px 9px; white-space: nowrap;
}
.camp-pomelli .camp-nota {
  background: var(--paper-sunken); border-radius: 7px;
  padding: 9px 11px; font-size: 12px; margin-bottom: 11px;
}

/* El botón de IA, desactivado hasta que el Centro autorice. */
.camp-ia {
  border: 1px dashed var(--line-strong); border-radius: 10px;
  padding: 14px 16px; margin-top: 18px; background: var(--paper-sunken);
}
.camp-ia h4 { margin: 0 0 4px; font-size: 14px; }
.camp-ia p { margin: 0 0 10px; font-size: 12.5px; color: var(--ink-soft); line-height: 1.6; }
.camp-ia button[disabled] {
  background: transparent; color: var(--ink-soft);
  border: 1px solid var(--line-strong); border-radius: 6px;
  padding: 8px 14px; font-size: 13px; font-weight: 600;
  cursor: not-allowed; font-family: var(--font-sans);
}
@media print { .camp-ia { display: none !important; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   GUÍA DE CAMPAÑAS PUBLICITARIAS
   ══════════════════════════════════════════════════════════ */

/* Mientras el Centro no autorice el uso de IA para esto —el
   semáforo pone «investigación de mercados» en condicionado— el
   botón de afinar con Gemini queda visible pero desactivado.
   Para activarlo: poner true, y añadir la ruta /campanas en
   auth.js copiando el patrón de /observaciones. */
var CAMPANAS_IA_ACTIVA = false;

/* Qué porcentaje de los ingresos es razonable invertir. No es una
   cifra inventada: por debajo del punto de equilibrio no sobra
   nada, y en tracción temprana pasar del 10% suele salir del
   sueldo del dueño antes que de la ganancia. */
function presupuestoCampana(){
  var ing = incomeForMonth(currentMonthStr());
  var fijos = totalFixed();
  var libre = ing - fijos;
  if(!isFinite(ing) || ing <= 0) return {estado:"sin-datos", monto:0, ing:0, libre:0};
  if(libre <= 0)                 return {estado:"sin-margen", monto:0, ing:ing, libre:libre};
  /* El 30% de lo que sobra, con techo del 10% de lo que entra:
     el que apenas cubre gastos no debe poner el margen entero en
     publicidad, y el que va holgado tampoco necesita más. */
  var monto = Math.min(libre * 0.30, ing * 0.10);
  return {estado:"ok", monto: Math.round(monto/10000)*10000, ing:ing, libre:libre};
}

/* Los canales según el tipo de negocio. El orden importa: es por
   dónde empezar, no una lista de opciones. */
var CANALES = {
  freelancer: [
    {n:"LinkedIn y tu red directa", pct:0,
     q:"Escribe a diez personas que ya te conocen y cuéntales qué haces ahora. No es publicidad, es recordar que existes.",
     por:"Un servicio por horas se contrata por confianza, no por anuncio. La primera venta casi siempre viene de alguien que ya te conoce."},
    {n:"Contenido en LinkedIn", pct:0,
     q:"Un caso real al mes: qué problema tenía el cliente, qué hiciste, qué cambió. Sin cifras confidenciales.",
     por:"Demuestra criterio, que es lo que se compra en un servicio. Cuesta tiempo, no dinero."},
    {n:"Anuncios en LinkedIn o Google", pct:100,
     q:"Solo cuando los dos anteriores ya traigan clientes. Empieza por el servicio que más margen te deja.",
     por:"Pagar por llegar a desconocidos antes de saber qué mensaje convierte es quemar presupuesto aprendiendo."}
  ],
  productos: [
    {n:"Instagram o TikTok orgánico", pct:0,
     q:"El producto en uso, no el producto solo. Tres publicaciones por semana, constantes.",
     por:"Un producto se vende por deseo y se ve. La constancia importa más que la producción."},
    {n:"Google Maps y ficha de negocio", pct:0,
     q:"Registra el negocio con fotos, horario y dirección. Pide reseñas a los clientes que ya tienes.",
     por:"Quien busca «cerca de mí» tiene la intención de comprar hoy. Es gratis y casi nadie lo hace bien."},
    {n:"Anuncios en Meta (Instagram y Facebook)", pct:100,
     q:"Empieza por tu ciudad y por el producto que ya se vende solo. Sube el presupuesto cuando sepas cuánto te cuesta cada venta.",
     por:"Con producto físico puedes medir cuánto cuesta traer una venta y decidir con esa cifra, no con intuición."}
  ],
  otro: [
    {n:"Tu red directa", pct:0,
     q:"Cuéntale a quien ya te conoce qué vendes ahora. Diez conversaciones antes de un peso en publicidad.",
     por:"La primera venta casi nunca viene de un anuncio, y te dice qué mensaje funciona."},
    {n:"Google Maps y redes", pct:0,
     q:"Registra el negocio y publica con constancia. Elige UNA red, la que ya usas.",
     por:"Dos redes a medias rinden menos que una bien llevada."},
    {n:"Anuncios pagados", pct:100,
     q:"Cuando ya sepas qué mensaje hace que te compren. Empieza pequeño y mide.",
     por:"Pagar por difundir un mensaje que aún no funciona multiplica el problema, no las ventas."}
  ]
};

/* La guía se muestra en dos sitios y el texto no puede ser el mismo
   en los dos. Dentro del tablero, «faltan tus cifras» se resuelve
   yendo a otra pestaña; como página aparte, se resuelve llenando los
   campos de arriba, y el titular sobra porque ya lo lleva la cabecera.

   La página suelta lo anuncia poniendo «window.CAMPANAS_SUELTA = true»
   antes de este bloque. El tablero no pone nada, así que allí vale
   «false» y todo sigue como estaba.

   Se mira en «window» y no con «typeof CAMPANAS_SUELTA»: este código
   va dentro de un IIFE en las dos páginas, y un «var» aquí dentro se
   iza al principio de esa función. Con «typeof» el valor global
   quedaba tapado por el local todavía sin asignar, así que la página
   suelta se veía como si estuviera dentro del tablero. Costó una
   prueba en rojo descubrirlo: no da error, solo cambia dos frases. */
var CAMPANAS_SUELTA = (typeof window !== "undefined") && window.CAMPANAS_SUELTA === true;

function panelCampanas(){
  var tipo = state.bizType || "otro";
  var p = presupuestoCampana();
  var be = breakevenUnits();
  var canales = CANALES[tipo] || CANALES.otro;

  var h = CAMPANAS_SUELTA ? '' :
    '<div class="panel-head"><h2>Guía de campañas publicitarias</h2>' +
    '<p>Por dónde empezar a darte a conocer, con lo que tu negocio puede pagar de verdad.</p></div>';

  /* Sin cifras no hay guía honesta: lo que saldría es un consejo
     genérico disfrazado de recomendación personalizada. */
  if(p.estado === "sin-datos"){
    return h + '<div class="card"><div class="camp-aviso">' +
      '<b>Faltan tus cifras.</b> ' +
      (CAMPANAS_SUELTA
        ? 'Escribe arriba lo que entra al mes y lo que se va en gastos fijos. '
        : 'Registra los ingresos y los gastos fijos del mes en las pestañas de arriba. ') +
      'Sin eso, cualquier presupuesto de campaña que te proponga aquí sería inventado.</div></div>';
  }

  h += '<div class="card">';

  if(p.estado === "sin-margen"){
    h += '<div class="camp-aviso"><b>Todavía no es momento de invertir en publicidad.</b> ' +
      'Tus gastos fijos (' + money(totalFixed()) + ') se llevan todo lo que entra (' + money(p.ing) + '). ' +
      'Publicidad ahora saldría de tu bolsillo, no del negocio. Primero cierra esa brecha: ' +
      'sube precios, baja gastos fijos, o vende más con lo que ya tienes.</div>';
    h += '<p style="font-size:13px;color:var(--ink-soft);line-height:1.65">' +
      'Lo de abajo sigue sirviendo: los dos primeros canales de tu tipo de negocio no cuestan dinero, solo tiempo.</p>';
  } else {
    h += '<div class="camp-cifras">' +
      '<div class="camp-cifra"><span class="k">Entra al mes</span><span class="v">' + money(p.ing) + '</span></div>' +
      '<div class="camp-cifra"><span class="k">Te queda tras gastos fijos</span><span class="v">' + money(p.libre) + '</span></div>' +
      '<div class="camp-cifra"><span class="k">Para campaña</span><span class="v">' + money(p.monto) + '</span>' +
        '<span class="n">30% de lo que te queda, con techo del 10% de lo que entra</span></div>' +
      '</div>';
    if(be != null){
      h += '<div class="camp-aviso" style="background:var(--accent-soft);border-color:var(--accent-strong);border-left-color:var(--accent)">' +
        '<b>Compruébalo contra tu punto de equilibrio.</b> Necesitas ' + be + ' ' +
        (be === 1 ? bizLabels().item : bizLabels().itemPlural) +
        ' al mes solo para cubrir gastos. La campaña tiene que traerte por encima de eso para que valga la pena.</div>';
    }
  }

  h += '<h3 style="margin-top:18px">Por dónde empezar, en este orden</h3>';
  canales.forEach(function(c, i){
    var plata = (p.estado === "ok" && c.pct > 0)
      ? money(Math.round(p.monto * c.pct / 100))
      : "Sin costo";
    h += '<div class="camp-canal">' +
      '<div class="camp-canal-cab"><span class="orden">PASO ' + (i+1) + '</span>' +
      '<h4>' + esc(c.n) + '</h4><span class="plata">' + plata + '</span></div>' +
      '<p>' + esc(c.q) + '</p>' +
      '<div class="porque"><b>Por qué este orden:</b> ' + esc(c.por) + '</div>' +
      '</div>';
  });

  h += '<h3 style="margin-top:18px">Qué medir</h3><ul class="camp-medir">' +
    '<li><b>Cuánto te cuesta traer un cliente:</b> lo que gastaste dividido entre los clientes nuevos del mes. ' +
    'Si eso supera lo que te deja cada cliente, la campaña te está costando dinero.</li>' +
    '<li><b>De dónde llegaron:</b> pregúntaselo a cada cliente nuevo. Es la medición más barata y la más fiable.</li>' +
    '<li><b>Si subieron las ventas:</b> compara el mes de campaña con el anterior' +
    (CAMPANAS_SUELTA
      ? ' en el Tablero de apoyo financiero, en la pestaña de Ingresos.'
      : ' en la pestaña de Ingresos.') + '</li>' +
    '</ul>';

  h += bloqueEjemplos();
  h += bloqueCampanaIA();
  h += '</div>';
  return h;
}

/* ══════════════════════════════════════════════════════════
   EJEMPLOS DE PIEZAS
   ----------------------------------------------------------
   Cuatro piezas reales, generadas con Pomelli a partir de la
   página del Centro. Se recrean en CSS en vez de incrustarse
   como imagen: así llevan el azul institucional exacto y el
   texto se puede corregir sin regenerar nada.

   Están aquí porque ver una pieza terminada explica mejor «a
   qué se parece esto» que cualquier párrafo describiéndolo.
   ══════════════════════════════════════════════════════════ */
var PIEZAS_EJEMPLO = [
  {t:"Mes del Emprendimiento: activa tu idea",
   d:"Estructura tu negocio paso a paso, de forma autónoma y gratuita.",
   marca:false},
  {t:"Guías financieras y legales gratis",
   d:"Herramientas interactivas para transformar tu proyecto en empresa real.",
   marca:false},
  {t:"Aprende a tu propio ritmo",
   d:"Acceso directo a contenido de planeación sin registro previo.",
   marca:true},
  {t:"Haz realidad tu empresa hoy",
   d:"Aprovecha los recursos digitales de tu comunidad universitaria.",
   marca:true}
];

function bloqueEjemplos(){
  var h = '<div class="camp-fuente">' +
    '<h4>Las piezas gráficas</h4>' +
    '<p>Este plan te dice qué publicar y dónde, pero no diseña las imágenes. ' +
    'Para eso hay herramientas gratuitas que las generan a partir de la página web de tu negocio. ' +
    'Estos cuatro ejemplos se hicieron así, con la página del Centro:</p>';

  h += '<div class="camp-piezas">';
  PIEZAS_EJEMPLO.forEach(function(p){
    h += '<div class="pieza">';
    if(p.marca) h += '<div class="marca"><span>Alumni</span><span>Sabana</span></div>';
    h += '<h5>' + esc(p.t) + '</h5>' +
         '<p>' + esc(p.d) + '</p>' +
         '<div class="pie-pieza">Ejemplo</div>' +
         '</div>';
  });
  h += '</div>';

  h += bloquePomelli();
  h += '</div>';
  return h;
}

/* ══════════════════════════════════════════════════════════
   POMELLI
   ----------------------------------------------------------
   Qué es, en qué idioma está y para qué sirve DENTRO de este
   plan. Sin eso, el botón es un enlace a una página en inglés
   que pide iniciar sesión: quien no sabe qué va a encontrar,
   se devuelve.

   El enlace es a la página general y no a una campaña concreta.
   Una dirección del tipo «/campaigns/<código>» es la de una
   campaña guardada DENTRO de una cuenta: a quien no tenga esa
   cuenta le sale la pantalla de inicio de sesión de Google, y
   si entra con la suya llega a su propio Pomelli vacío, no a la
   campaña que se quiso mostrar. Las piezas de esa campaña ya
   están arriba, recreadas.
   ══════════════════════════════════════════════════════════ */
function bloquePomelli(){
  return '<div class="camp-pomelli">' +
    '<h4>Pomelli, de Google <span class="camp-idioma">En inglés</span></h4>' +

    '<p>Es gratis y funciona así: le das la dirección de tu página web y la lee para ' +
    'sacar lo que llama tu «ADN de marca», que son tus colores, tus tipografías y tu ' +
    'forma de hablar. Con eso te propone ideas de campaña y te arma las piezas: la ' +
    'imagen y el texto listos para publicar. Puedes editar lo que genere y descargarlo. ' +
    'Necesitas una cuenta de Google y tarda unos minutos en analizar la página.</p>' +

    '<p><b>Para qué te sirve aquí.</b> Este plan te dice en qué canal empezar, con ' +
    'cuánto y qué medir, pero no diseña las imágenes. Pomelli cubre justo esa parte, y ' +
    'la cubre bien en los pasos 1 y 2, que son los que no cuestan dinero: si vas a ' +
    'publicar constante en redes, el trabajo de tener algo decente que publicar cada ' +
    'semana es el que suele hacer que la gente abandone.</p>' +

    '<p class="camp-nota">Está todo en inglés, aunque puede generar las piezas en ' +
    'español si se lo pides. Google lo ofrece por ahora en unos pocos países, así que ' +
    'puede que no te abra desde Colombia. Y revisa siempre lo que genere antes de ' +
    'publicarlo: a veces cambia detalles del producto o del logo.</p>' +

    '<a class="btn small" href="https://labs.google/pomelli" target="_blank" rel="noopener noreferrer">' +
    'Abrir Pomelli ↗</a>' +
    '</div>';
}

/* El botón de IA: construido, visible y desactivado.
   Se deja a la vista a propósito, para que el Centro vea qué se
   activaría, en vez de esconderlo hasta que alguien se acuerde. */
function bloqueCampanaIA(){
  if(CAMPANAS_IA_ACTIVA){
    return '<div class="camp-ia"><h4>Afinar este plan con IA</h4>' +
      '<p>Se enviarán tu tipo de negocio y tus cifras al servicio de IA de la Universidad para adaptar el plan a tu caso. No se envía el nombre de tus clientes.</p>' +
      '<button class="btn small" id="campIA" type="button">Afinar con IA</button></div>';
  }
  return '<div class="camp-ia"><h4>Afinar este plan con IA</h4>' +
    '<p>Pendiente de autorización del Centro de Desarrollo Profesional para el uso de inteligencia artificial en esta herramienta. ' +
    'El plan de arriba está armado con reglas, no con IA.</p>' +
    '<button type="button" disabled>Disponible próximamente</button></div>';
}
"""
