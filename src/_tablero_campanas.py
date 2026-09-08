# ══════════════════════════════════════════════════════════════
#  GUÍA DE CAMPAÑAS PUBLICITARIAS
#
#  La etapa 3 de la portada —«Crecimiento de negocio»— dejó de ser
#  «Próximamente». Vive DENTRO del tablero y no como herramienta
#  aparte, porque ahí ya están el tipo de negocio y las cifras: la
#  persona no vuelve a escribir lo que ya escribió.
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

function panelCampanas(){
  var tipo = state.bizType || "otro";
  var p = presupuestoCampana();
  var be = breakevenUnits();
  var canales = CANALES[tipo] || CANALES.otro;

  var h = '<div class="panel-head"><h2>Guía de campañas publicitarias</h2>' +
    '<p>Por dónde empezar a darte a conocer, con lo que tu negocio puede pagar de verdad.</p></div>';

  /* Sin cifras no hay guía honesta: lo que saldría es un consejo
     genérico disfrazado de recomendación personalizada. */
  if(p.estado === "sin-datos"){
    return h + '<div class="card"><div class="camp-aviso">' +
      '<b>Faltan tus cifras.</b> Registra los ingresos y los gastos fijos del mes en las pestañas de arriba. ' +
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
    '<li><b>Si subieron las ventas:</b> compara el mes de campaña con el anterior en la pestaña de Ingresos.</li>' +
    '</ul>';

  h += bloqueCampanaIA();
  h += '</div>';
  return h;
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
