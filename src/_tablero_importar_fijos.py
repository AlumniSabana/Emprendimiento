# ══════════════════════════════════════════════════════════════
#  IMPORTAR LOS GASTOS FIJOS DESDE UN CSV
#
#  Los ingresos ya se podían subir en bloque; los gastos fijos no,
#  y son los que más pereza dan de escribir: arriendo, servicios,
#  plataformas, nómina, contador, internet… Quince filas que casi
#  siempre ya están en una hoja de cálculo.
#
#  ── QUÉ SE REAPROVECHA ────────────────────────────────────────
#  Todo lo difícil ya estaba resuelto en _tablero_importar.py y se
#  vuelve a usar tal cual: partir el CSV respetando las comas entre
#  comillas, entender «1.250.000» y «$1.250.000» a la colombiana, y
#  releer en Latin-1 cuando Excel de Windows escribe «Gutiérrez»
#  como «Gutiérrez». Aquí solo cambia qué columnas se buscan.
#
#  ── POR QUÉ NO LLEVA MES ──────────────────────────────────────
#  Un gasto fijo es el mismo todos los meses: por eso el tablero lo
#  guarda sin fecha. Pedir una columna de mes daría a entender que
#  hay que subir uno por cada mes del año.
#
#  Si el archivo trae una columna de mes igualmente, se ignora sin
#  protestar: es lo que pasa cuando alguien exporta su tabla de
#  gastos completa, y rechazar el archivo por eso sería absurdo.
# ══════════════════════════════════════════════════════════════

JS = r"""
/* ══════════════════════════════════════════════════════════
   IMPORTAR GASTOS FIJOS
   ══════════════════════════════════════════════════════════ */

/* Qué columna es el concepto y cuál el monto. Se buscan por
   nombre; si la hoja no trae títulos, se asume el orden de la
   tabla que la persona está viendo: concepto, monto. */
function columnasFijos(cabecera){
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
  var c = buscar(["concepto","gasto","nombre","descripcion","detalle","rubro","item"]);
  var v = buscar(["monto","valor","importe","total","costo","precio","mensual"]);
  return {
    concepto: c >= 0 ? c : 0,
    monto:    v >= 0 ? v : 1,
    hayCabecera: (c >= 0 || v >= 0)
  };
}

function importarFijosCSV(texto){
  var filas = csvFilas(texto);
  if(!filas.length) return {añadidos:0, avisos:["El archivo está vacío."]};

  var col = columnasFijos(filas[0]);
  var datos = col.hayCabecera ? filas.slice(1) : filas;
  var nuevos = [], avisos = [];

  datos.forEach(function(f, i){
    var linea = (col.hayCabecera ? i + 2 : i + 1);

    /* Una fila totalmente vacía no es un error: es la línea en
       blanco que Excel deja al final de casi todo archivo. */
    var vacia = f.every(function(c){ return !String(c == null ? "" : c).trim(); });
    if(vacia) return;

    var monto = aCifra(f[col.monto]);
    if(monto === null){
      avisos.push("Fila " + linea + ": no se entendió el monto (" +
                  (String(f[col.monto]||"").trim() || "vacío") + ").");
      return;
    }
    var nombre = String(f[col.concepto] == null ? "" : f[col.concepto]).trim();
    if(!nombre){
      avisos.push("Fila " + linea + ": sin concepto, se guardó como «Sin nombre».");
      nombre = "Sin nombre";
    }
    nuevos.push({ id: uid(), name: nombre, amount: Math.round(monto) });
  });

  if(nuevos.length){
    state.fixedExpenses = state.fixedExpenses.concat(nuevos);
    saveState();
  }
  return {añadidos: nuevos.length, avisos: avisos};
}

function pintarResultadoFijos(res){
  var caja = document.getElementById("impfResultado");
  if(!caja) return;
  var h = "";
  if(res.añadidos > 0){
    h += '<p class="imp-ok">Se agregaron ' + res.añadidos +
         (res.añadidos === 1 ? " gasto fijo." : " gastos fijos.") + '</p>';
  } else {
    h += '<p class="imp-mal">No se pudo leer ningún gasto del archivo.</p>';
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

function leerArchivoFijos(archivo){
  if(!archivo) return;
  var nombre = (archivo.name || "").toLowerCase();
  var caja = document.getElementById("impfResultado");
  if(/\.xlsx?$/.test(nombre)){
    if(caja) caja.innerHTML = '<p class="imp-mal">Este es un archivo de Excel. ' +
      'Ábrelo y usa <strong>Archivo → Guardar como → CSV</strong>, luego sube ese archivo.</p>';
    return;
  }
  function procesar(texto){
    try{
      var res = importarFijosCSV(texto);
      /* Repintar primero y escribir el mensaje después: renderAll()
         reconstruye el panel y se llevaría por delante el aviso. */
      renderAll();
      pintarResultadoFijos(res);
    }catch(err){
      if(caja) caja.innerHTML = '<p class="imp-mal">No se pudo leer el archivo: ' +
        esc(String(err && err.message || err)) + '</p>';
    }
  }
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

function bloqueImportarFijos(){
  return (
    '<div class="imp-zona" id="impfZona">' +
      '<div class="imp-cab">' +
        '<h4>¿Ya tienes tus gastos fijos en una hoja?</h4>' +
      '</div>' +
      '<p class="imp-ayuda">Súbelos de una vez en vez de escribirlos uno a uno. ' +
        'En Excel o Google Sheets usa <strong>Archivo → Guardar como → CSV</strong>. ' +
        'Se esperan dos columnas: <code>concepto</code> y <code>monto</code>. ' +
        'Si la hoja no tiene títulos, se toma ese mismo orden. ' +
        'No hace falta el mes: un gasto fijo se repite todos los meses.</p>' +
      '<div class="imp-acciones">' +
        '<button class="btn small" id="impfBtn" type="button">Elegir archivo CSV</button>' +
        '<button class="btn small ghost" id="impfEjemplo" type="button">Descargar ejemplo</button>' +
      '</div>' +
      '<input type="file" id="impfArchivo" accept=".csv,text/csv,text/plain">' +
      '<div class="imp-resultado" id="impfResultado"></div>' +
    '</div>'
  );
}

function descargarEjemploFijosCSV(){
  var csv = "concepto,monto\n" +
            "Arriendo del local,1.200.000\n" +
            "Servicios (agua, luz, gas),320000\n" +
            "Internet y telefonía,145000\n" +
            "Contador,250000\n";
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob(["﻿" + csv], {type:"text/csv;charset=utf-8"}));
  a.download = "ejemplo-gastos-fijos.csv";
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
}
"""


#  Los manejadores del panel de gastos fijos. Se enganchan igual
#  que los de ingresos, dentro de attachHandlers().
HANDLERS = """
  var impfBtn = root.querySelector("#impfBtn");
  var impfArchivo = root.querySelector("#impfArchivo");
  if(impfBtn && impfArchivo){
    impfBtn.addEventListener("click", function(){ impfArchivo.click(); });
    impfArchivo.addEventListener("change", function(e){
      leerArchivoFijos(e.target.files && e.target.files[0]);
      e.target.value = "";
    });
  }
  var impfEjemplo = root.querySelector("#impfEjemplo");
  if(impfEjemplo) impfEjemplo.addEventListener("click", descargarEjemploFijosCSV);
  var impfZona = root.querySelector("#impfZona");
  if(impfZona){
    ["dragenter","dragover"].forEach(function(ev){
      impfZona.addEventListener(ev, function(e){
        e.preventDefault(); impfZona.classList.add("encima"); });
    });
    ["dragleave","drop"].forEach(function(ev){
      impfZona.addEventListener(ev, function(e){
        e.preventDefault(); impfZona.classList.remove("encima"); });
    });
    impfZona.addEventListener("drop", function(e){
      leerArchivoFijos(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
    });
  }
"""
