# ══════════════════════════════════════════════════════════════
#  IMPORTAR INGRESOS DESDE UNA HOJA DE CÁLCULO
#
#  Quien factura treinta ventas al mes no las teclea una a una:
#  abandona la herramienta. Esto lee un CSV —lo que Excel y Google
#  Sheets exportan con «Guardar como»— y llena la tabla.
#
#  ── POR QUÉ CSV Y NO .XLSX ────────────────────────────────────
#  Un .xlsx es un ZIP con XML dentro: leerlo pide una librería de
#  ~400 KB. El tablero pesa 75 KB, no carga nada de internet y
#  funciona sin conexión. Meter esa librería multiplicaría por
#  siete el archivo y añadiría una dependencia de terceros a una
#  herramienta institucional que hoy no tiene ninguna.
#
#  El CSV se parsea con ~60 líneas y sale del mismo Excel.
#
#  ── LO QUE HAY QUE ACERTAR ────────────────────────────────────
#  Los números en Colombia se escriben «1.250.000,50»: el punto
#  separa miles y la coma decimales. Interpretarlo al modo inglés
#  convertiría 1.250.000 en 1,25 y el tablero mostraría cifras
#  absurdas sin avisar. Eso se resuelve en «aCifra()».
# ══════════════════════════════════════════════════════════════

CSS = """
/* ═══════════════ IMPORTAR DESDE HOJA DE CÁLCULO ═══════════════ */
.imp-zona {
  border: 1.5px dashed var(--line-strong); border-radius: 10px;
  padding: 1.1rem 1.2rem; margin-top: 14px;
  background: var(--paper-sunken);
  transition: border-color .15s, background .15s;
}
.imp-zona.encima { border-color: var(--accent); background: var(--accent-soft); }
.imp-cab { display: flex; align-items: center; gap: .7rem; flex-wrap: wrap; }
.imp-cab h4 { margin: 0; font-size: 14px; }
.imp-ayuda { color: var(--ink-soft); font-size: 12.5px; margin: 6px 0 0; line-height: 1.6; }
.imp-ayuda code {
  font-family: var(--font-mono); font-size: 11.5px;
  background: var(--paper-raised); border: 1px solid var(--line);
  border-radius: 3px; padding: .05em .3em;
}
.imp-acciones { display: flex; gap: .5rem; flex-wrap: wrap; margin-top: 10px; }
.imp-resultado { margin-top: 10px; font-size: 13px; line-height: 1.6; }
.imp-ok    { color: var(--good); font-weight: 600; }
.imp-aviso { color: var(--warn); }
.imp-mal   { color: var(--critical); font-weight: 600; }
.imp-detalle {
  margin: 6px 0 0; padding-left: 1.1rem; color: var(--ink-soft);
  font-size: 12.5px; line-height: 1.55;
}
.imp-zona input[type=file] { display: none; }
@media print { .imp-zona { display: none !important; } }
"""


JS = r"""
/* ══════════════════════════════════════════════════════════
   IMPORTAR INGRESOS DESDE CSV
   ══════════════════════════════════════════════════════════ */

/* Un CSV bien formado puede llevar comas dentro de comillas
   («Distribuidora Gómez, S.A.S.»). Partir por comas a secas
   rompería ese nombre en dos columnas y desplazaría el resto de
   la fila. Se recorre carácter a carácter. */
function csvFilas(texto){
  var filas = [], campo = "", fila = [], enComillas = false;
  texto = texto.replace(/^﻿/, "");          /* BOM de Excel */
  for(var i = 0; i < texto.length; i++){
    var c = texto[i];
    if(enComillas){
      if(c === '"'){
        if(texto[i+1] === '"'){ campo += '"'; i++; }
        else enComillas = false;
      } else campo += c;
    } else if(c === '"'){ enComillas = true; }
    else if(c === ',' || c === ';' || c === '\t'){ fila.push(campo); campo = ""; }
    else if(c === '\n'){ fila.push(campo); filas.push(fila); fila = []; campo = ""; }
    else if(c !== '\r'){ campo += c; }
  }
  if(campo !== "" || fila.length){ fila.push(campo); filas.push(fila); }
  return filas.filter(function(f){ return f.some(function(x){ return String(x).trim() !== ""; }); });
}

/* «1.250.000,50» es un millón doscientos cincuenta mil en
   Colombia. Leerlo como si fuera inglés daría 1,25 y el tablero
   mostraría cifras absurdas sin avisar de nada.

   La regla: si hay coma, la coma es el decimal y los puntos son
   miles. Si solo hay puntos, se miran los dígitos tras el último:
   exactamente dos podría ser decimal, tres o más es separador de
   miles. Ante la duda con dos dígitos se elige decimal, porque
   «1.50» como mil quinientos es más raro que como uno cincuenta. */
function aCifra(txt){
  var s = String(txt == null ? "" : txt).trim();
  if(!s) return null;
  s = s.replace(/[^\d.,\-]/g, "");               /* fuera $ y espacios */
  if(!s || s === "-") return null;
  var negativo = s.charAt(0) === "-";
  s = s.replace(/-/g, "");
  if(s.indexOf(",") >= 0){
    s = s.replace(/\./g, "").replace(",", ".");
  } else {
    var p = s.lastIndexOf(".");
    if(p >= 0){
      var decimales = s.length - p - 1;
      if(decimales === 3) s = s.replace(/\./g, "");   /* 1.250 = mil doscientos cincuenta */
      else if(decimales > 3) s = s.replace(/\./g, "");
      /* con 1 o 2 dígitos se deja como decimal */
    }
  }
  var n = parseFloat(s);
  if(!isFinite(n)) return null;
  return negativo ? -n : n;
}

/* El mes puede venir de mil formas. Se aceptan las que de verdad
   salen de Excel y de la gente; lo que no se entienda se reporta
   en vez de inventar una fecha. */
var MESES_ES = {ene:1,feb:2,mar:3,abr:4,may:5,jun:6,jul:7,ago:8,sep:9,set:9,oct:10,nov:11,dic:12};
function aMes(txt, respaldo){
  var s = String(txt == null ? "" : txt).trim().toLowerCase();
  if(!s) return respaldo;
  var m;
  if((m = s.match(/^(\d{4})[-\/](\d{1,2})/)))            /* 2026-09 · 2026/9 */
    return m[1] + "-" + ("0"+m[2]).slice(-2);
  if((m = s.match(/^(\d{1,2})[-\/](\d{1,2})[-\/](\d{4})/))) /* 05/09/2026 */
    return m[3] + "-" + ("0"+m[2]).slice(-2);
  if((m = s.match(/^(\d{4})(\d{2})$/)))                   /* 202609 */
    return m[1] + "-" + m[2];
  if((m = s.match(/([a-záéíóú]{3,})[^\d]*(\d{4})/))){     /* septiembre de 2026 */
    var k = m[1].slice(0,3).replace(/[áéíóú]/g, function(c){
      return {"á":"a","é":"e","í":"i","ó":"o","ú":"u"}[c]; });
    if(MESES_ES[k]) return m[2] + "-" + ("0"+MESES_ES[k]).slice(-2);
  }
  return null;
}

/* Encuentra qué columna es cuál. Si la primera fila trae nombres
   reconocibles se usan; si no, se asume el orden de la tabla que
   la persona está viendo (cliente, mes, monto). */
function columnasDe(cabecera){
  var norm = cabecera.map(function(c){
    return String(c||"").trim().toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "");
  });
  function buscar(claves){
    for(var i = 0; i < norm.length; i++)
      for(var j = 0; j < claves.length; j++)
        if(norm[i].indexOf(claves[j]) >= 0) return i;
    return -1;
  }
  var c = buscar(["cliente","nombre","proyecto","descripcion","concepto"]);
  var m = buscar(["mes","fecha","periodo"]);
  var v = buscar(["monto","valor","importe","total","ingreso","precio","pago"]);
  var hayCabecera = (c >= 0 || v >= 0);
  return {
    cliente: c >= 0 ? c : 0,
    mes:     m >= 0 ? m : 1,
    monto:   v >= 0 ? v : 2,
    hayCabecera: hayCabecera
  };
}

function importarIngresosCSV(texto){
  var filas = csvFilas(texto);
  if(!filas.length) return {añadidos:0, avisos:["El archivo está vacío."]};

  var col = columnasDe(filas[0]);
  var datos = col.hayCabecera ? filas.slice(1) : filas;
  var mesActual = new Date().toISOString().slice(0,7);
  var nuevos = [], avisos = [];

  datos.forEach(function(f, i){
    var linea = (col.hayCabecera ? i + 2 : i + 1);
    var monto = aCifra(f[col.monto]);
    if(monto === null){
      avisos.push("Fila " + linea + ": no se entendió el monto (" +
                  (String(f[col.monto]||"").trim() || "vacío") + ").");
      return;
    }
    var mes = aMes(f[col.mes], null);
    if(mes === null){
      mes = mesActual;
      if(String(f[col.mes]||"").trim())
        avisos.push("Fila " + linea + ": no se entendió el mes (" +
                    String(f[col.mes]).trim() + "), se usó el mes actual.");
    }
    nuevos.push({
      id: uid(),
      client: String(f[col.cliente] == null ? "" : f[col.cliente]).trim(),
      month: mes,
      amount: Math.round(monto)
    });
  });

  if(nuevos.length){
    state.income = state.income.concat(nuevos);
    saveState();
  }
  return {añadidos: nuevos.length, avisos: avisos};
}

function pintarResultadoImport(res){
  var caja = document.getElementById("impResultado");
  if(!caja) return;
  var h = "";
  if(res.añadidos > 0){
    h += '<p class="imp-ok">Se agregaron ' + res.añadidos +
         (res.añadidos === 1 ? " ingreso." : " ingresos.") + '</p>';
  } else {
    h += '<p class="imp-mal">No se pudo leer ningún ingreso del archivo.</p>';
  }
  if(res.avisos.length){
    var muestra = res.avisos.slice(0, 5);
    h += '<p class="imp-aviso">' + res.avisos.length +
         (res.avisos.length === 1 ? " fila necesita revisión:" : " filas necesitan revisión:") + '</p>';
    h += '<ul class="imp-detalle">' + muestra.map(function(a){
      return "<li>" + esc(a) + "</li>"; }).join("");
    if(res.avisos.length > muestra.length)
      h += "<li>y " + (res.avisos.length - muestra.length) + " más.</li>";
    h += "</ul>";
  }
  caja.innerHTML = h;
}

function leerArchivoIngresos(archivo){
  if(!archivo) return;
  var nombre = (archivo.name || "").toLowerCase();
  var caja = document.getElementById("impResultado");
  if(/\.xlsx?$/.test(nombre)){
    if(caja) caja.innerHTML = '<p class="imp-mal">Este es un archivo de Excel. ' +
      'Ábrelo y usa <strong>Archivo → Guardar como → CSV</strong>, luego sube ese archivo.</p>';
    return;
  }
  function procesar(texto){
    try{
      var res = importarIngresosCSV(texto);
      /* Primero repintar y DESPUÉS escribir el resultado: renderAll()
         reconstruye el panel entero, así que un mensaje escrito antes
         desaparecía con él. Se veía como si no hubiera pasado nada,
         aunque las filas sí se habían agregado. */
      renderAll();
      pintarResultadoImport(res);
    }catch(err){
      if(caja) caja.innerHTML = '<p class="imp-mal">No se pudo leer el archivo: ' +
        esc(String(err && err.message || err)) + '</p>';
    }
  }

  /* Excel en Windows exporta en Latin-1: leído como UTF-8 salen
     «Gu?rrez» en vez de «Gutiérrez». Se lee en UTF-8 y, si aparece
     el carácter de reemplazo, se relee en Latin-1. */
  var lector = new FileReader();
  lector.onerror = function(){
    if(caja) caja.innerHTML = '<p class="imp-mal">No se pudo abrir el archivo.</p>';
  };
  lector.onload = function(e){
    var t = String(e.target.result || "");
    if(t.indexOf("�") < 0){ procesar(t); return; }
    var l2 = new FileReader();
    l2.onerror = lector.onerror;
    l2.onload = function(e2){ procesar(String(e2.target.result || "")); };
    l2.readAsText(archivo, "ISO-8859-1");
  };
  lector.readAsText(archivo, "UTF-8");
}

function bloqueImportar(){
  return (
    '<div class="imp-zona" id="impZona">' +
      '<div class="imp-cab">' +
        '<h4>¿Tienes tus ventas en una hoja de cálculo?</h4>' +
      '</div>' +
      '<p class="imp-ayuda">Súbelas de una vez en vez de escribirlas una a una. ' +
        'En Excel o Google Sheets usa <strong>Archivo → Guardar como → CSV</strong>. ' +
        'Se esperan tres columnas: <code>cliente</code>, <code>mes</code>, <code>monto</code>. ' +
        'Si la hoja no tiene títulos, se toma ese mismo orden. ' +
        'Los montos pueden venir como <code>1.250.000</code> o <code>$1.250.000</code>.</p>' +
      '<div class="imp-acciones">' +
        '<button class="btn small" id="impBtn" type="button">Elegir archivo CSV</button>' +
        '<button class="btn small ghost" id="impEjemplo" type="button">Descargar ejemplo</button>' +
      '</div>' +
      '<input type="file" id="impArchivo" accept=".csv,text/csv,text/plain">' +
      '<div class="imp-resultado" id="impResultado"></div>' +
    '</div>'
  );
}

/* Un ejemplo descargable ahorra la pregunta «¿y cómo tiene que
   verse el archivo?», que es la que llega siempre. */
function descargarEjemploCSV(){
  var hoy = new Date().toISOString().slice(0,7);
  var csv = "cliente,mes,monto\n" +
            "Panadería El Trigal," + hoy + ",450000\n" +
            "Cafetería Luna," + hoy + ",1.250.000\n" +
            "Distribuidora Gómez," + hoy + ",890500\n";
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob(["﻿" + csv], {type:"text/csv;charset=utf-8"}));
  a.download = "ejemplo-ingresos.csv";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
}
"""
