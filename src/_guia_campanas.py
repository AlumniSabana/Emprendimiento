# ══════════════════════════════════════════════════════════════
#  GUÍA DE CAMPAÑAS · HERRAMIENTA APARTE
#
#  Vivía dentro del tablero, en una pestaña. Ahora es su propia
#  página, porque es la etapa 3 del recorrido —«Crecimiento»— y no
#  un apartado de la etapa 2. Quien ya tiene el negocio andando y
#  solo quiere saber dónde anunciarse no debería tener que entrar a
#  un tablero financiero para encontrarlo.
#
#  ── EL PROBLEMA QUE ABRÍA SEPARARLA ───────────────────────────
#  Dentro del tablero, el presupuesto salía de llamar a
#  incomeForMonth(), totalFixed() y breakevenUnits(): las cifras
#  que la persona ya había escrito. Fuera del tablero esas
#  funciones no existen, y volver a pedir todo sería montar un
#  segundo tablero.
#
#  ── CÓMO SE RESUELVE ──────────────────────────────────────────
#  El tablero guarda su estado en localStorage bajo la clave
#  «tf_dashboard_v1». Las dos páginas se publican en el mismo
#  sitio, así que comparten origen y esta puede LEER esa clave.
#
#    · Si la persona ya usó el tablero, aquí no escribe nada: sus
#      cifras aparecen solas, con una nota de dónde salieron.
#    · Si no lo ha usado, se le piden tres cosas —tipo de negocio,
#      lo que entra al mes, lo que se va en gastos fijos— y con eso
#      basta para el presupuesto y para la comprobación honesta.
#
#  Se LEE y nunca se escribe esa clave. Si esta página guardara
#  ahí, un número tecleado de memoria aquí pisaría el registro
#  detallado del tablero, y la persona perdería el desglose sin
#  enterarse. Lo que se escriba aquí vive en su propia clave.
#
#  ── LO QUE NO SE PUEDE TRAER ──────────────────────────────────
#  breakevenUnits() necesita el ticket promedio, que sale del
#  historial de ingresos y no de un campo. Cuando las cifras vienen
#  del tablero, el punto de equilibrio se muestra; cuando se
#  teclean aquí, no aparece esa comprobación. Es honesto: sin
#  historial no hay ticket promedio que calcular.
# ══════════════════════════════════════════════════════════════

VERSION_PAGINA = "2026.09.08"

#  La clave del tablero. Si algún día cambia allí, cambia aquí.
CLAVE_TABLERO = "tf_dashboard_v1"
CLAVE_PROPIA = "guia_campanas_v1"


# ══════════════════════════════════════════════════════════════
#  EL ARMAZÓN DE LA PÁGINA
#  Solo lo que el tablero daba y aquí no hay: el layout, la
#  cabecera y los campos. Las tarjetas de campaña, las piezas y
#  el bloque de IA vienen tal cual de _tablero_campanas.py.
# ══════════════════════════════════════════════════════════════

CSS_PAGINA = """
*{ box-sizing:border-box; margin:0; padding:0; }
html{ -webkit-text-size-adjust:100%; }
body{
  background:var(--paper); color:var(--ink);
  font-family:var(--font-body); font-size:14px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
/* Los encabezados NO llevan «color». Lo heredan de body, que ya es
   var(--ink), y así cualquier bloque que declare el suyo se lo pasa
   a los suyos.

   Llevarlo aquí costó una regresión: «color:var(--ink)» en esta
   regla ganaba por especificidad al blanco que .pieza hereda a sus
   hijos, y los titulares de las piezas de ejemplo salían azul marino
   sobre azul marino. Se veía el texto de apoyo y el titular no.
   Dentro del tablero no pasaba porque allí ninguna regla de elemento
   pinta los encabezados. */
h1,h2,h3,h4,h5{ font-family:var(--font-display); font-weight:600; line-height:1.2; }
a{ color:var(--accent); }
ul,ol{ padding-left:1.15rem; }

.envoltura{ max-width:940px; margin:0 auto; padding:0 clamp(1.1rem,4vw,2rem); }

/* La barra de «Volver» es sticky: al bajar queda flotando encima del
   contenido. Sin esto, al pulsar «Ver el plan» la página salta a
   #guia y la barra corta por la mitad las tres tarjetas de cifras,
   que es justo lo que la persona acaba de pedir ver. Se les reserva
   su alto. Vale para cualquier salto a un ancla, no solo ese. */
#cifras, #guia, .card, .camp-cifras { scroll-margin-top: calc(var(--alto-volver) + 12px); }

/* ── La cabecera azul ──
   La misma franja que abre las otras herramientas del Centro:
   es lo que hace que se reconozcan como un mismo servicio. */
.cab{ background:var(--azul); color:#FFFFFF; padding:2.6rem 0 2.8rem; }
.cab .eyebrow{
  display:block; font-size:.7rem; letter-spacing:.14em; text-transform:uppercase;
  color:#A9BEDE; font-weight:600; margin-bottom:.6rem;
}
.cab h1{ color:#FFFFFF; font-size:clamp(1.75rem,4.2vw,2.5rem); margin-bottom:.7rem; }
.cab p{ color:#C7D6F0; font-size:1rem; line-height:1.65; max-width:60ch; }

main{ padding:2.2rem 0 3rem; }

/* ── Los campos, cuando hay que pedirlos ── */
.campos{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }
.campo label{
  display:block; font-size:12px; font-weight:600; color:var(--ink);
  margin-bottom:5px;
}
.campo .pista{ display:block; font-size:11.5px; color:var(--ink-soft); font-weight:400; margin-top:2px; }
.campo input, .campo select{
  width:100%; font-family:inherit; font-size:14px; color:var(--ink);
  background:var(--paper-raised); border:1px solid var(--line-strong);
  border-radius:6px; padding:9px 11px;
}
.campo input{ font-variant-numeric:tabular-nums; letter-spacing:.01em; }
.campo input:focus, .campo select:focus{
  outline:2px solid var(--accent); outline-offset:1px; border-color:var(--accent);
}

/* ── De dónde salieron las cifras ──
   Quien ve un presupuesto tiene derecho a saber de dónde sale.
   Si vino del tablero se dice, y se ofrece cambiarlo. */
.origen{
  display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;
  font-size:12.5px; color:var(--ink-soft); margin-top:12px;
}
.origen button{
  background:none; border:none; padding:0; font:inherit;
  color:var(--accent); font-weight:600; cursor:pointer;
  text-decoration:underline; text-underline-offset:2px;
}

.btn{
  display:inline-block; background:var(--accent); color:#FFFFFF;
  border:1px solid var(--accent); border-radius:6px;
  padding:9px 16px; font-size:13.5px; font-weight:600;
  font-family:var(--font-sans); cursor:pointer; text-decoration:none;
}
.btn:hover{ background:var(--accent-strong); border-color:var(--accent-strong); }
.btn.small{ padding:7px 13px; font-size:13px; }
.btn:focus-visible{ outline:2px solid var(--ink); outline-offset:2px; }

/* Las tarjetas y el encabezado de panel, copiados del tablero para
   que las dos herramientas se lean igual. */
.card{
  background:var(--paper-raised); border:1px solid var(--line);
  border-radius:12px; padding:20px 22px; box-shadow:var(--shadow);
}
.card + .card{ margin-top:16px; }
.card h3{ font-size:15px; margin-bottom:4px; }
.panel-head{ margin-bottom:20px; }
.panel-head h2{ font-size:24px; }
.panel-head p{ color:var(--ink-soft); font-size:13.5px; margin-top:6px; max-width:62ch; }

/* ═══════════════ LOS TRES PASOS, DE LADO ═══════════════
   La guía se recorre de izquierda a derecha, no bajando. Son tres
   momentos distintos —cuánto puedes poner, con qué piezas, y
   afinarlo— y encadenarlos en una sola columna larga hacía que la
   parte de Pomelli pareciera una nota al pie del presupuesto.

   Cada paso es una diapositiva. Solo se ve una; las otras dos
   están al lado, fuera del marco. */
.pasos-barra{
  display:flex; gap:8px; margin-bottom:18px;
  list-style:none; padding:0;
}
.pasos-barra li{ flex:1 1 0; min-width:0; }
.pasos-barra button{
  width:100%; text-align:left; cursor:pointer;
  background:var(--paper-raised); border:1px solid var(--line);
  border-top:3px solid var(--line);
  border-radius:0 0 8px 8px; padding:9px 12px 10px;
  font-family:inherit; color:var(--ink-soft);
  transition:border-color .15s, color .15s, background .15s;
}
.pasos-barra button:hover{ border-color:var(--line-strong); border-top-color:var(--line-strong); }
.pasos-barra button:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
.pasos-barra .n{
  display:block; font-family:var(--font-mono); font-size:10px;
  font-weight:700; letter-spacing:.09em; text-transform:uppercase;
  margin-bottom:2px;
}
.pasos-barra .t{ display:block; font-size:13px; font-weight:600; line-height:1.3; }
.pasos-barra [aria-current="step"]{
  background:var(--paper-raised); border-top-color:var(--accent);
  color:var(--ink);
}
.pasos-barra [aria-current="step"] .n{ color:var(--accent); }
/* El paso ya visitado se marca, para saber por dónde se ha pasado
   sin tener que volver a entrar a mirar. */
.pasos-barra .visto .n::after{ content:" ·  visto"; color:var(--good); }

.marco{ overflow:hidden; }
.pista{
  display:flex; align-items:flex-start;
  width:300%;
  transition:transform .42s cubic-bezier(.3,.8,.35,1);
}
@media (prefers-reduced-motion: reduce){ .pista{ transition:none; } }
.diapo{
  width:33.3333%; flex:0 0 33.3333%;
  padding:2px;   /* deja respirar la sombra de las tarjetas */
}
/* Lo que no se está viendo no debe alcanzarse con el tabulador: si
   no, tabular desde el último campo salta a un botón invisible que
   está dos pantallas a la derecha. */
.diapo[aria-hidden="true"]{ visibility:hidden; }

.pasos-pie{
  display:flex; align-items:center; gap:12px; flex-wrap:wrap;
  margin-top:18px;
}
.pasos-pie .btn[disabled]{
  opacity:.4; cursor:not-allowed;
  background:transparent; color:var(--ink-soft); border-color:var(--line-strong);
}
.pasos-pie .cuenta{
  margin-left:auto; font-size:12px; color:var(--ink-soft);
  font-variant-numeric:tabular-nums;
}
.btn.ghost{
  background:transparent; color:var(--accent);
  border-color:var(--line-strong);
}
.btn.ghost:hover{ background:var(--accent-soft); border-color:var(--accent); color:var(--accent-strong); }

@media (max-width:640px){
  .pasos-barra{ gap:5px; }
  .pasos-barra .t{ font-size:11.5px; }
  .pasos-barra button{ padding:7px 8px 8px; }
}

@media print{
  .cab{ background:none; color:#000; padding:1rem 0; }
  .cab h1, .cab p, .cab .eyebrow{ color:#000; }
  .origen button{ display:none; }
  /* En papel no hay «siguiente»: se imprimen los tres pasos
     seguidos, que es lo que alguien espera de un PDF. */
  .pasos-barra, .pasos-pie{ display:none !important; }
  .marco{ overflow:visible; }
  .pista{ display:block; width:auto; transform:none !important; }
  .diapo{ width:auto; visibility:visible !important; page-break-inside:avoid; margin-bottom:18px; }
}
"""


#  El cuerpo. Los tres estados —pedir cifras, mostrar el plan— se
#  pintan desde JS dentro de #guia; lo de aquí es el armazón.
CUERPO = """
<header class="cab">
  <div class="envoltura">
    <span class="eyebrow">Crecimiento de negocio</span>
    <h1>Guía de campañas publicitarias</h1>
    <p>Por dónde empezar a darte a conocer, en orden y con lo que tu negocio puede pagar de verdad.</p>
  </div>
</header>

<main>
  <div class="envoltura">
    <ul class="pasos-barra" id="pasosBarra"></ul>

    <div class="marco" id="marco">
      <div class="pista" id="pista">
        <section class="diapo" id="paso-1" aria-label="Sección 1: tus cifras y tu plan">
          <div id="cifras"></div>
          <div id="guia"></div>
        </section>
        <section class="diapo" id="paso-2" aria-label="Sección 2: las piezas gráficas">
          <div id="piezas"></div>
        </section>
        <section class="diapo" id="paso-3" aria-label="Sección 3: afinar con inteligencia artificial">
          <div id="ia"></div>
        </section>
      </div>
    </div>

    <div class="pasos-pie">
      <button class="btn ghost" type="button" id="pasoAtras">&larr; Atrás</button>
      <button class="btn" type="button" id="pasoSig">Siguiente &rarr;</button>
      <span class="cuenta" id="pasoCuenta"></span>
    </div>
  </div>
</main>
"""


# ══════════════════════════════════════════════════════════════
#  EL JAVASCRIPT PROPIO DE LA PÁGINA
#
#  Recrea, con lo mínimo, las cuatro funciones del tablero de las
#  que dependía la guía: money(), esc(), bizLabels() y el estado.
#  No se copia el tablero entero: solo lo que panelCampanas() usa.
# ══════════════════════════════════════════════════════════════

JS_PAGINA = r"""
(function(){
"use strict";

/* ══════════════════════════════════════════════════════════
   LO QUE LA GUÍA ESPERABA DEL TABLERO
   Cuatro funciones y un objeto «state». Se recrean aquí con lo
   justo: la guía se copia sin tocar desde _tablero_campanas.py,
   así que tiene que encontrar lo mismo que encontraba allí.
   ══════════════════════════════════════════════════════════ */

var CLAVE_TABLERO = "__CLAVE_TABLERO__";
var CLAVE_PROPIA  = "__CLAVE_PROPIA__";

var fmtCOP = new Intl.NumberFormat("es-CO", {
  style:"currency", currency:"COP", maximumFractionDigits:0
});
function money(n){ if(!isFinite(n)) return "—"; return fmtCOP.format(Math.round(n)); }
function esc(s){
  return (s==null?"":String(s)).replace(/[&<>"']/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
  });
}
function currentMonthStr(){
  var d = new Date();
  return d.getFullYear() + "-" + String(d.getMonth()+1).padStart(2,"0");
}
function bizLabels(){
  var t = state.bizType;
  if(t==="freelancer") return {unit:"cliente", unitPlural:"clientes", item:"proyecto", itemPlural:"proyectos"};
  if(t==="productos")  return {unit:"cliente", unitPlural:"clientes", item:"producto/pedido", itemPlural:"pedidos"};
  return {unit:"cliente", unitPlural:"clientes", item:"proyecto o pedido", itemPlural:"proyectos o pedidos"};
}

/* El estado de ESTA página. «origen» dice de dónde salieron las
   cifras, que es lo que decide qué nota se muestra debajo. */
var state = {
  bizType: "otro",
  ingresos: 0,
  fijos: 0,
  equilibrio: null,   /* solo si vino del tablero: necesita historial */
  origen: "vacio"     /* vacio | tablero | manual */
};

/* Las tres funciones que la guía llama por su nombre del tablero.
   Aquí devuelven lo que tenga «state», venga de donde venga. */
function incomeForMonth(){ return state.ingresos; }
function totalFixed(){ return state.fijos; }
function breakevenUnits(){ return state.equilibrio; }

/* ══════════════════════════════════════════════════════════
   LEER EL TABLERO
   Mismo origen, misma clave. Se lee y NUNCA se escribe: si esta
   página guardara ahí, una cifra tecleada de memoria pisaría el
   registro detallado del tablero sin que nadie se entere.
   ══════════════════════════════════════════════════════════ */
function leerTablero(){
  var crudo;
  try{ crudo = localStorage.getItem(CLAVE_TABLERO); }catch(e){ return null; }
  if(!crudo) return null;

  var d;
  try{ d = JSON.parse(crudo); }catch(e){ return null; }
  if(!d || typeof d !== "object") return null;

  var mes = currentMonthStr();
  var ingresos = (d.income || []).reduce(function(s,e){
    return s + (e && e.month === mes ? (Number(e.amount)||0) : 0);
  }, 0);
  var fijos = (d.fixedExpenses || []).reduce(function(s,e){
    return s + (Number(e && e.amount)||0);
  }, 0);

  /* Un tablero abierto y nunca llenado no cuenta como cifras: sin
     ingresos del mes no hay presupuesto que calcular, y decir que
     «vienen del tablero» sería señalar a un sitio vacío. */
  if(ingresos <= 0) return null;

  return {
    bizType: d.bizType || "otro",
    ingresos: ingresos,
    fijos: fijos,
    equilibrio: equilibrioDe(d)
  };
}

/* El punto de equilibrio necesita el ticket promedio, que sale del
   historial de ingresos. Por eso solo existe cuando las cifras
   vienen del tablero: tecleando tres números no hay historial.
   Se replica el cálculo del tablero, no se inventa otro. */
function equilibrioDe(d){
  var ingresos = d.income || [];
  if(!ingresos.length) return null;

  /* Ticket promedio: lo que entra dividido entre las entradas. */
  var suma = 0, cuenta = 0;
  ingresos.forEach(function(e){
    var v = Number(e && e.amount)||0;
    if(v > 0){ suma += v; cuenta++; }
  });
  if(!cuenta) return null;
  var ticket = suma / cuenta;
  if(ticket <= 0) return null;

  /* Gastos fijos más el promedio de variables por mes. */
  var fijos = (d.fixedExpenses || []).reduce(function(s,e){
    return s + (Number(e && e.amount)||0);
  }, 0);
  var meses = {};
  (d.variableExpenses || []).forEach(function(e){
    if(!e || !e.month) return;
    meses[e.month] = (meses[e.month]||0) + (Number(e.amount)||0);
  });
  var claves = Object.keys(meses);
  var variables = claves.length
    ? claves.reduce(function(s,k){ return s + meses[k]; }, 0) / claves.length
    : 0;

  return Math.ceil((fijos + variables) / ticket);
}

/* Lo que se teclee aquí vive en su propia clave, nunca en la del
   tablero. Así las dos herramientas pueden convivir sin pisarse. */
function leerPropio(){
  try{
    var d = JSON.parse(localStorage.getItem(CLAVE_PROPIA) || "null");
    if(d && typeof d === "object" && (Number(d.ingresos)||0) > 0) return d;
  }catch(e){}
  return null;
}
function guardarPropio(){
  try{
    /* Se fusiona con lo que ya hubiera en vez de reemplazarlo: en
       esta misma clave vive también en qué paso se quedó la
       persona, y escribir el objeto entero lo borraba. Se veía como
       que la guía «se reiniciaba» al tocar una cifra. */
    var d = {};
    try{ d = JSON.parse(localStorage.getItem(CLAVE_PROPIA) || "{}") || {}; }catch(e){}
    d.bizType  = state.bizType;
    d.ingresos = state.ingresos;
    d.fijos    = state.fijos;
    localStorage.setItem(CLAVE_PROPIA, JSON.stringify(d));
  }catch(e){}
}

/* ══════════════════════════════════════════════════════════
   LOS CAMPOS
   Tres preguntas, no un tablero. Si el tablero ya las respondió,
   ni siquiera se muestran: se muestra de dónde salieron.
   ══════════════════════════════════════════════════════════ */

var TIPOS = [
  {v:"freelancer", n:"Servicios por horas o por proyecto"},
  {v:"productos",  n:"Productos físicos o pedidos"},
  {v:"otro",       n:"Otro, o una mezcla de los dos"}
];

var pidiendo = false;   /* true cuando los campos están a la vista */

function conPuntos(digitos){
  if(!digitos) return "";
  return String(digitos).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}
function soloDigitos(txt){ return String(txt==null?"":txt).replace(/\D+/g, ""); }

function pintarCifras(){
  var caja = document.getElementById("cifras");

  /* Cifras del tablero, y nadie ha pedido cambiarlas. */
  if(state.origen === "tablero" && !pidiendo){
    caja.innerHTML =
      '<div class="card"><div class="origen">' +
      '<span>Estas cifras vienen del Tablero de apoyo financiero: ' +
      money(state.ingresos) + ' de ingresos este mes y ' + money(state.fijos) +
      ' de gastos fijos.</span>' +
      '<button type="button" id="cambiar">Usar otras cifras</button>' +
      '</div></div>';
    document.getElementById("cambiar").addEventListener("click", function(){
      pidiendo = true; pintarCifras();
    });
    return;
  }

  /* Cifras tecleadas aquí y ya guardadas: la misma nota, con la
     opción de corregirlas. */
  if(state.origen === "manual" && !pidiendo){
    caja.innerHTML =
      '<div class="card"><div class="origen">' +
      '<span>Con ' + money(state.ingresos) + ' de ingresos al mes y ' +
      money(state.fijos) + ' de gastos fijos.</span>' +
      '<button type="button" id="cambiar">Cambiar las cifras</button>' +
      '</div></div>';
    document.getElementById("cambiar").addEventListener("click", function(){
      pidiendo = true; pintarCifras();
    });
    return;
  }

  /* Los campos. */
  var opciones = TIPOS.map(function(t){
    return '<option value="' + t.v + '"' +
      (state.bizType === t.v ? ' selected' : '') + '>' + esc(t.n) + '</option>';
  }).join("");

  caja.innerHTML =
    '<div class="card">' +
      '<h3>Tus cifras</h3>' +
      '<p style="font-size:13px;color:var(--ink-soft);margin:4px 0 14px;line-height:1.6">' +
        'Tres datos para que el presupuesto salga de tu negocio y no de una cifra inventada. ' +
        'Si ya usas el Tablero de apoyo financiero, se toman de allí solos.</p>' +
      '<div class="campos">' +
        '<div class="campo"><label for="cType">Qué vendes</label>' +
          '<select id="cType">' + opciones + '</select></div>' +
        '<div class="campo"><label for="cIng">Lo que entra al mes' +
          '<span class="pista">Ventas antes de descontar gastos</span></label>' +
          '<input id="cIng" type="text" inputmode="numeric" autocomplete="off" ' +
            'value="' + conPuntos(state.ingresos || "") + '" placeholder="0"></div>' +
        '<div class="campo"><label for="cFij">Gastos fijos al mes' +
          '<span class="pista">Arriendo, servicios, plataformas, sueldos</span></label>' +
          '<input id="cFij" type="text" inputmode="numeric" autocomplete="off" ' +
            'value="' + conPuntos(state.fijos || "") + '" placeholder="0"></div>' +
      '</div>' +
      '<div style="margin-top:14px"><button class="btn" type="button" id="verPlan">Ver el plan</button></div>' +
    '</div>';

  /* Solo dígitos, con puntos de miles. Mismo comportamiento que en
     la ficha: un número de siete cifras sin separar es donde
     alguien se equivoca de un cero en su propio negocio. */
  ["cIng","cFij"].forEach(function(id){
    var inp = document.getElementById(id);
    inp.addEventListener("input", function(){
      var izquierda = soloDigitos(inp.value.slice(0, inp.selectionStart)).length;
      var nuevo = conPuntos(soloDigitos(inp.value));
      if(nuevo === inp.value) return;
      inp.value = nuevo;
      var pos = 0, vistos = 0;
      while(pos < nuevo.length && vistos < izquierda){
        if(/\d/.test(nuevo[pos])) vistos++;
        pos++;
      }
      try{ inp.setSelectionRange(pos, pos); }catch(e){}
    });
    inp.addEventListener("keydown", function(e){
      if(e.ctrlKey || e.metaKey || e.altKey) return;
      if(e.key && e.key.length === 1 && !/\d/.test(e.key)) e.preventDefault();
    });
  });

  document.getElementById("cType").addEventListener("change", function(e){
    state.bizType = e.target.value;
  });

  document.getElementById("verPlan").addEventListener("click", function(){
    state.ingresos = Number(soloDigitos(document.getElementById("cIng").value)) || 0;
    state.fijos    = Number(soloDigitos(document.getElementById("cFij").value)) || 0;
    state.bizType  = document.getElementById("cType").value;
    /* Tecleadas a mano no hay historial, así que no hay punto de
       equilibrio que comprobar. Se dice callando: no se muestra. */
    state.equilibrio = null;
    state.origen = state.ingresos > 0 ? "manual" : "vacio";
    pidiendo = false;
    guardarPropio();
    pintar();
    document.getElementById("guia").scrollIntoView({behavior:"smooth", block:"start"});
  });
}

/* ══════════════════════════════════════════════════════════
   LOS TRES PASOS, DE IZQUIERDA A DERECHA
   ----------------------------------------------------------
   Tres momentos distintos: cuánto puedes poner y dónde, con qué
   piezas, y cómo afinarlo. Puestos uno debajo de otro, el de
   Pomelli parecía una nota al pie del presupuesto.

   La pista mide 300% y se mueve con «transform»: se desplaza el
   navegador con la tarjeta gráfica, sin volver a maquetar la
   página. Cambiar «margin-left» haría lo mismo a la vista y
   costaría un reflujo en cada paso.
   ══════════════════════════════════════════════════════════ */

/* Se llaman «secciones» y no «pasos» a propósito. Dentro del plan
   los tres canales ya van rotulados «PASO 1», «PASO 2», «PASO 3»
   —ese es el orden en que conviene atacarlos— y tener dos cosas
   distintas llamadas «Paso 1» en la misma pantalla es pedir que se
   confundan. */
var PASOS = [
  {n: "Sección 1", t: "Tus cifras y tu plan"},
  {n: "Sección 2", t: "Las piezas gráficas"},
  {n: "Sección 3", t: "Afinar con IA"}
];

var pasoActual = 0;
var pasosVistos = {0: true};

function irAPaso(i, conFoco){
  pasoActual = Math.max(0, Math.min(PASOS.length - 1, i));
  pasosVistos[pasoActual] = true;

  document.getElementById("pista").style.transform =
    "translateX(-" + (pasoActual * (100 / PASOS.length)) + "%)";

  /* Lo que no se ve se saca del tabulador y de los lectores de
     pantalla. Sin esto, tabular desde el último campo del paso 1
     salta a un botón que está dos pantallas a la derecha. */
  for(var k = 0; k < PASOS.length; k++){
    var d = document.getElementById("paso-" + (k + 1));
    if(!d) continue;
    var oculta = (k !== pasoActual);
    d.setAttribute("aria-hidden", oculta ? "true" : "false");
    d.inert = oculta;                    /* donde exista */
    var focables = d.querySelectorAll("a, button, input, select, textarea");
    for(var j = 0; j < focables.length; j++){
      if(oculta) focables[j].setAttribute("tabindex", "-1");
      else focables[j].removeAttribute("tabindex");
    }
  }

  pintarBarraPasos();
  pintarPiePasos();
  guardarPaso();

  /* Al cambiar de paso, la página sube al principio del marco: si
     no, se llega al paso 3 mirando su mitad de abajo, porque el
     scroll se quedó donde estaba en el paso anterior. */
  var marco = document.getElementById("marco");
  if(marco && marco.getBoundingClientRect().top < 0){
    marco.scrollIntoView({behavior: "smooth", block: "start"});
  }
  if(conFoco){
    var d = document.getElementById("paso-" + (pasoActual + 1));
    if(d){ d.setAttribute("tabindex", "-1"); d.focus({preventScroll: true}); }
  }
}

function pintarBarraPasos(){
  var barra = document.getElementById("pasosBarra");
  barra.innerHTML = PASOS.map(function(p, i){
    var actual = (i === pasoActual);
    return '<li><button type="button" data-paso="' + i + '"' +
      (actual ? ' aria-current="step"' : '') +
      (pasosVistos[i] && !actual ? ' class="visto"' : '') + '>' +
      '<span class="n">' + esc(p.n) + '</span>' +
      '<span class="t">' + esc(p.t) + '</span>' +
      '</button></li>';
  }).join("");
  Array.prototype.forEach.call(barra.querySelectorAll("[data-paso]"), function(b){
    b.addEventListener("click", function(){
      irAPaso(Number(b.getAttribute("data-paso")), true);
    });
  });
}

function pintarPiePasos(){
  var atras = document.getElementById("pasoAtras");
  var sig   = document.getElementById("pasoSig");
  atras.disabled = (pasoActual === 0);
  sig.disabled   = (pasoActual === PASOS.length - 1);
  sig.innerHTML  = (pasoActual === PASOS.length - 1)
    ? "Esta es la última sección"
    : "Siguiente: " + esc(PASOS[pasoActual + 1].t) + " &rarr;";
  document.getElementById("pasoCuenta").textContent =
    "Sección " + (pasoActual + 1) + " de " + PASOS.length;
}

/* En qué paso se quedó. Va en la clave propia de esta página, no
   en la del tablero. */
function guardarPaso(){
  try{
    var d = JSON.parse(localStorage.getItem(CLAVE_PROPIA) || "{}");
    d.paso = pasoActual;
    localStorage.setItem(CLAVE_PROPIA, JSON.stringify(d));
  }catch(e){}
}
function pasoGuardado(){
  try{
    var d = JSON.parse(localStorage.getItem(CLAVE_PROPIA) || "{}");
    var p = Number(d.paso);
    if(isFinite(p) && p >= 0 && p < PASOS.length) return p;
  }catch(e){}
  return 0;
}

function montarPasos(){
  document.getElementById("pasoAtras").addEventListener("click", function(){
    irAPaso(pasoActual - 1, true);
  });
  document.getElementById("pasoSig").addEventListener("click", function(){
    irAPaso(pasoActual + 1, true);
  });

  /* Flechas del teclado. Se ignoran mientras se escribe en un
     campo: ahí la flecha mueve el cursor, no la diapositiva. */
  document.addEventListener("keydown", function(e){
    var t = e.target || {};
    var escribiendo = /^(INPUT|SELECT|TEXTAREA)$/.test(t.tagName || "");
    if(escribiendo || e.ctrlKey || e.metaKey || e.altKey) return;
    if(e.key === "ArrowRight"){ irAPaso(pasoActual + 1, false); }
    else if(e.key === "ArrowLeft"){ irAPaso(pasoActual - 1, false); }
  });
}

function pintar(){
  pintarCifras();
  document.getElementById("guia").innerHTML   = panelCampanas();
  document.getElementById("piezas").innerHTML = bloqueEjemplos();
  document.getElementById("ia").innerHTML     = bloqueCampanaIA();

  /* Repintar deja botones y enlaces nuevos dentro de las tres
     diapositivas, incluidas las dos que no se están viendo. Hay que
     volver a sacarlos del tabulador o, tras tocar una cifra, el
     tabulador vuelve a saltar fuera de pantalla.
     Solo si los pasos ya están montados: la primera pintada ocurre
     antes de que exista la barra. */
  if(document.getElementById("pasosBarra").children.length){
    irAPaso(pasoActual, false);
  }
}

/* ══════════════════════════════════════════════════════════
   ARRANQUE
   El tablero manda sobre lo tecleado aquí: son cifras
   registradas mes a mes contra tres números de memoria.
   ══════════════════════════════════════════════════════════ */
var delTablero = leerTablero();
if(delTablero){
  state.bizType    = delTablero.bizType;
  state.ingresos   = delTablero.ingresos;
  state.fijos      = delTablero.fijos;
  state.equilibrio = delTablero.equilibrio;
  state.origen     = "tablero";
} else {
  var propio = leerPropio();
  if(propio){
    state.bizType  = propio.bizType || "otro";
    state.ingresos = Number(propio.ingresos)||0;
    state.fijos    = Number(propio.fijos)||0;
    state.origen   = "manual";
  }
}

__GUIA__

pintar();
montarPasos();
/* Se entra por donde se quedó, salvo la primera vez. */
irAPaso(pasoGuardado(), false);

})();
"""


def js(js_guia):
    """El JavaScript de la página, con la guía de campañas dentro.

    «js_guia» es el JS tal cual de _tablero_campanas.py: se inserta
    sin tocarlo, dentro del mismo IIFE, para que vea money(), esc(),
    state y las tres funciones de cifras. Una sola copia de la guía
    para las dos formas de mostrarla."""
    return (JS_PAGINA
            .replace("__CLAVE_TABLERO__", CLAVE_TABLERO)
            .replace("__CLAVE_PROPIA__", CLAVE_PROPIA)
            .replace("__GUIA__", js_guia))
