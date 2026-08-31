/**
 * Ficha de Identificación de Negocio
 * Asistente por botones que recoge la información mínima para saber qué
 * trámites, entidades, documentos y costos le corresponden a cada
 * emprendedor. NO calcula ni entrega la ruta completa de legalización:
 * solo identifica al negocio y muestra el mapa de entidades/documentos
 * que le aplican, con enlaces oficiales para gestionarlos.
 */

(() => {
  "use strict";

  // ---------------------------------------------------------------------
  // Estado
  // ---------------------------------------------------------------------
  const state = {
    actividadDescripcion: "",
    sector: null,
    ciiuCode: null,
    ciiuLabel: null,
    ciiuConfirmado: null,

    ciudad: "",
    departamento: "",
    variosMunicipios: null,
    domicilioPrincipal: "",

    figuraJuridica: null, // 'natural' | 'sas'
    figuraHelperUsado: false,

    espacio: null, // 'local_propio' | 'local_arrendado' | 'casa' | 'sin_espacio_fijo'
    atencionPublico: null,
    canalVenta: null, // 'online' | 'presencial' | 'ambos'

    activos: "",
    ingresos: "",
    numPersonal: "",
    vinculoPersonal: [], // array de strings

    // Sector-específico
    saludInvasivos: null,
    saludTitulados: null,
    alimentosTipo: null, // 'elabora' | 'envasa_marca' | 'revende'
    alimentosMarcaPropia: null,
    bellezaRompeBarrera: null,
    techDatosTerceros: null,
    eduTipo: null, // 'formal' | 'etdh' | 'libre'
    transporteFlotaPropia: null,
    transporteTipo: null, // 'pasajeros' | 'carga'

    contratacionEstatal: null,
  };

  const SECTORES = [
    { id: "salud", label: "Salud" },
    { id: "alimentos", label: "Alimentos y bebidas" },
    { id: "belleza", label: "Belleza y estética" },
    { id: "comercio", label: "Comercio o tienda física" },
    { id: "tecnologia", label: "Tecnología o software" },
    { id: "profesionales", label: "Servicios profesionales" },
    { id: "educacion", label: "Educación o formación" },
    { id: "manufactura", label: "Manufactura o artesanías" },
    { id: "transporte", label: "Transporte o domicilios" },
    { id: "construccion", label: "Construcción" },
    { id: "otro", label: "Otro" },
  ];

  const SECTOR_LABEL = Object.fromEntries(SECTORES.map((s) => [s.id, s.label]));

  // ---------------------------------------------------------------------
  // Sugerencia de código CIIU (orientativa, no oficial)
  // ---------------------------------------------------------------------
  function suggestCIIU(sector, descripcion) {
    const d = (descripcion || "").toLowerCase();
    const has = (...words) => words.some((w) => d.includes(w));

    switch (sector) {
      case "salud":
        if (has("odont", "dental")) return { code: "8622", label: "Actividades de la práctica odontológica" };
        if (has("psicolog", "terapia", "terapeuta")) return { code: "8690", label: "Otras actividades de atención de la salud humana" };
        return { code: "8621", label: "Actividades de la práctica médica, sin internación" };
      case "alimentos":
        if (has("panaderia", "panadería", "pasteleria", "pastelería", "reposteria", "repostería"))
          return { code: "1081", label: "Elaboración de productos de panadería" };
        if (has("restaurante", "comida", "café", "cafeteria", "cafetería", "cocina"))
          return { code: "5611", label: "Expendio a la mesa de comidas preparadas" };
        if (has("bebida", "jugo", "gaseosa", "cerveza"))
          return { code: "1104", label: "Elaboración de bebidas no alcohólicas / producción de aguas minerales" };
        if (has("elabora", "produce", "fabrica", "fábrica"))
          return { code: "1079", label: "Elaboración de otros productos alimenticios n.c.p." };
        return { code: "4711", label: "Comercio al por menor de alimentos, bebidas y tabaco" };
      case "belleza":
        if (has("tatuaje", "piercing", "perforacion", "perforación"))
          return { code: "9609", label: "Otras actividades de servicios personales n.c.p." };
        return { code: "9602", label: "Peluquería y otros tratamientos de belleza" };
      case "comercio":
        return { code: "4719", label: "Comercio al por menor en establecimientos no especializados" };
      case "tecnologia":
        if (has("app", "software", "desarrollo", "programa", "programación"))
          return { code: "6201", label: "Actividades de desarrollo de sistemas informáticos (planificación, análisis, diseño, programación, pruebas)" };
        return { code: "6202", label: "Actividades de consultoría informática y de gestión de instalaciones informáticas" };
      case "profesionales":
        if (has("contable", "contador", "contaduria", "contaduría"))
          return { code: "6920", label: "Actividades de contabilidad, teneduría de libros, auditoría financiera y asesoría tributaria" };
        if (has("abogado", "juridico", "jurídico", "legal"))
          return { code: "6910", label: "Actividades jurídicas" };
        if (has("marketing", "publicidad", "mercadeo"))
          return { code: "7310", label: "Publicidad" };
        return { code: "7020", label: "Actividades de consultoría de gestión" };
      case "educacion":
        if (has("idioma", "ingles", "inglés"))
          return { code: "8550", label: "Actividades de enseñanza deportiva y recreativa / enseñanza cultural" };
        return { code: "8559", label: "Otros tipos de educación n.c.p." };
      case "manufactura":
        if (has("ropa", "textil", "confeccion", "confección"))
          return { code: "1410", label: "Confección de prendas de vestir, excepto prendas de piel" };
        if (has("joyeria", "joyería", "bisuteria", "bisutería"))
          return { code: "3211", label: "Fabricación de joyas y artículos conexos" };
        return { code: "3299", label: "Otras industrias manufactureras n.c.p." };
      case "transporte":
        if (has("domicilio", "mensajeria", "mensajería", "paqueteo"))
          return { code: "5320", label: "Actividades de mensajería" };
        if (has("carga", "mercancia", "mercancía", "encomienda"))
          return { code: "4923", label: "Transporte de carga por carretera" };
        return { code: "4922", label: "Transporte terrestre mixto / transporte de pasajeros" };
      case "construccion":
        if (has("remodela", "acabado", "pintura", "electric"))
          return { code: "4330", label: "Terminación y acabado de edificios y obras de ingeniería civil" };
        return { code: "4111", label: "Construcción de edificios residenciales" };
      default:
        return null;
    }
  }

  // ---------------------------------------------------------------------
  // Utilidades
  // ---------------------------------------------------------------------
  const main = document.getElementById("main");
  const progressBar = document.getElementById("progressBar");
  const progressLabel = document.getElementById("progressLabel");

  function fmtCOP(value) {
    const n = Number(String(value).replace(/[^\d]/g, ""));
    if (!n) return "";
    return "$" + n.toLocaleString("es-CO");
  }

  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined) continue;
      if (k === "class") node.className = v;
      else if (k === "html") node.innerHTML = v;
      else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
      else if (k === "disabled") node.disabled = !!v;
      else node.setAttribute(k, v);
    }
    (Array.isArray(children) ? children : [children]).forEach((c) => {
      if (c === null || c === undefined) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function choiceButton(label, selected, onClick, sub) {
    const btn = el("button", {
      class: "choice-btn" + (selected ? " selected" : ""),
      type: "button",
      onclick: onClick,
    }, [label, sub ? el("small", {}, sub) : null]);
    return btn;
  }

  // ---------------------------------------------------------------------
  // Definición de pasos
  // ---------------------------------------------------------------------
  const STEP_IDS = [
    "actividad_desc",
    "sector",
    "ciiu",
    "ubicacion",
    "figura",
    "infraestructura",
    "escala",
    "sector_especifico",
    "contratacion_estatal",
    "resultado",
  ];

  let currentIndex = 0;

  function sectorTieneSubpreguntas(sector) {
    return ["salud", "alimentos", "belleza", "tecnologia", "educacion", "transporte"].includes(sector);
  }

  function isApplicable(stepId) {
    if (stepId === "sector_especifico") return sectorTieneSubpreguntas(state.sector);
    return true;
  }

  function totalApplicableCount() {
    return STEP_IDS.filter(isApplicable).length;
  }

  function applicableIndexOf(stepId) {
    return STEP_IDS.filter(isApplicable).indexOf(stepId);
  }

  function goTo(index, direction = 1) {
    let i = index;
    while (i >= 0 && i < STEP_IDS.length && !isApplicable(STEP_IDS[i])) {
      i += direction;
    }
    currentIndex = Math.max(0, Math.min(STEP_IDS.length - 1, i));
    render();
  }

  function goNext() { goTo(currentIndex + 1, 1); }
  function goBack() { goTo(currentIndex - 1, -1); }

  // ---------------------------------------------------------------------
  // Render principal
  // ---------------------------------------------------------------------
  function updateProgress(sectionLabel) {
    const total = totalApplicableCount();
    const pos = applicableIndexOf(STEP_IDS[currentIndex]) + 1;
    const pct = Math.round((pos / total) * 100);
    progressBar.style.width = pct + "%";
    progressLabel.textContent = `Paso ${pos} de ${total} · ${sectionLabel}`;
  }

  function render() {
    main.innerHTML = "";
    const stepId = STEP_IDS[currentIndex];
    const renderer = STEP_RENDERERS[stepId];
    const card = el("div", { class: "card" });
    main.appendChild(card);
    renderer(card);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function navRow(card, { onNext, nextLabel = "Siguiente", nextDisabled = false, showBack = true }) {
    const row = el("div", { class: "nav-row" });
    row.appendChild(
      showBack && currentIndex > 0
        ? el("button", { class: "btn btn-ghost", type: "button", onclick: goBack }, "← Atrás")
        : el("span", {})
    );
    row.appendChild(
      el("button", {
        class: "btn btn-primary",
        type: "button",
        disabled: nextDisabled ? "true" : null,
        onclick: (e) => {
          if (e.currentTarget.disabled) return;
          onNext();
        },
      }, nextLabel)
    );
    card.appendChild(row);
  }

  // ---------------------------------------------------------------------
  // Paso 1 · Actividad — descripción libre
  // ---------------------------------------------------------------------
  function renderActividadDesc(card) {
    updateProgress("Actividad");
    card.appendChild(el("span", { class: "section-tag" }, "1. Actividad"));
    card.appendChild(el("p", { class: "question" }, "Cuéntame en tus palabras: ¿qué vende o qué servicio presta tu negocio?"));
    card.appendChild(el("p", { class: "hint" }, "No hay respuesta correcta o incorrecta, entre más detalle des, mejor te podemos orientar."));

    const group = el("div", { class: "field-group" });
    const textarea = el("textarea", {
      placeholder: "Ej: Vendo arepas y jugos naturales en un local en el centro de la ciudad…",
      oninput: (e) => {
        state.actividadDescripcion = e.target.value;
        nextBtn.disabled = state.actividadDescripcion.trim().length < 5;
      },
    });
    textarea.value = state.actividadDescripcion;
    group.appendChild(textarea);
    card.appendChild(group);

    navRow(card, {
      onNext: goNext,
      nextDisabled: state.actividadDescripcion.trim().length < 5,
    });
    const nextBtn = card.querySelector(".btn-primary");
  }

  // ---------------------------------------------------------------------
  // Paso 2 · Sector
  // ---------------------------------------------------------------------
  function renderSector(card) {
    updateProgress("Actividad");
    card.appendChild(el("span", { class: "section-tag" }, "1. Actividad"));
    card.appendChild(el("p", { class: "question" }, "¿Cuál de estos sectores describe mejor tu negocio?"));
    card.appendChild(el("p", { class: "hint" }, "Elige la opción que más se acerque. Esto nos ayuda a sugerirte el código de actividad económica y las preguntas que siguen."));

    const grid = el("div", { class: "btn-grid" });
    SECTORES.forEach((s) => {
      grid.appendChild(
        choiceButton(s.label, state.sector === s.id, () => {
          state.sector = s.id;
          state.ciiuConfirmado = null;
          const suggestion = suggestCIIU(s.id, state.actividadDescripcion);
          state.ciiuCode = suggestion ? suggestion.code : null;
          state.ciiuLabel = suggestion ? suggestion.label : null;
          render();
        })
      );
    });
    card.appendChild(grid);

    navRow(card, { onNext: goNext, nextDisabled: !state.sector });
  }

  // ---------------------------------------------------------------------
  // Paso 3 · CIIU sugerido
  // ---------------------------------------------------------------------
  function renderCIIU(card) {
    updateProgress("Actividad");
    card.appendChild(el("span", { class: "section-tag" }, "1. Actividad"));
    card.appendChild(el("p", { class: "question" }, "Con lo que nos contaste, este sería tu código CIIU sugerido"));
    card.appendChild(el("p", { class: "hint" }, "El código CIIU clasifica tu actividad económica y define qué impuestos, tarifas y requisitos aplican. Es una sugerencia inicial: la confirmas o la ajustas en tu Cámara de Comercio o con tu contador."));

    if (state.ciiuCode) {
      card.appendChild(
        el("div", { class: "explainer" }, [
          el("strong", {}, `CIIU ${state.ciiuCode}`),
          ` — ${state.ciiuLabel}`,
        ])
      );
    } else {
      card.appendChild(
        el("div", { class: "explainer" }, "Con el sector \"Otro\" no podemos sugerir un código automáticamente. Descríbelo con más detalle a tu Cámara de Comercio para que te asignen el CIIU correcto.")
      );
    }

    const grid = el("div", { class: "btn-grid" });
    grid.appendChild(
      choiceButton("✓ Confirmo que este código está bien", state.ciiuConfirmado === true, () => {
        state.ciiuConfirmado = true;
        render();
      })
    );
    grid.appendChild(
      choiceButton("No estoy seguro / prefiero confirmarlo después", state.ciiuConfirmado === false && state.ciiuConfirmado !== null, () => {
        state.ciiuConfirmado = false;
        render();
      })
    );
    card.appendChild(grid);

    navRow(card, { onNext: goNext, nextDisabled: state.ciiuConfirmado === null && !!state.ciiuCode });
  }

  // ---------------------------------------------------------------------
  // Paso 4 · Ubicación
  // ---------------------------------------------------------------------
  function renderUbicacion(card) {
    updateProgress("Ubicación");
    card.appendChild(el("span", { class: "section-tag" }, "2. Ubicación"));
    card.appendChild(el("p", { class: "question" }, "¿En qué ciudad y departamento va a operar tu negocio?"));
    card.appendChild(el("p", { class: "hint" }, "Ojo: la jurisdicción de la Cámara de Comercio no siempre coincide con el municipio. Confírmala directamente con tu Cámara de Comercio, no la asumas."));

    const ciudadGroup = el("div", { class: "field-group" });
    ciudadGroup.appendChild(el("label", { class: "field-label" }, "Ciudad o municipio principal"));
    const ciudadInput = el("input", {
      type: "text",
      value: state.ciudad,
      placeholder: "Ej: Chía",
      oninput: (e) => { state.ciudad = e.target.value; refreshNext(); },
    });
    ciudadGroup.appendChild(ciudadInput);
    card.appendChild(ciudadGroup);

    const deptoGroup = el("div", { class: "field-group" });
    deptoGroup.appendChild(el("label", { class: "field-label" }, "Departamento"));
    const deptoInput = el("input", {
      type: "text",
      value: state.departamento,
      placeholder: "Ej: Cundinamarca",
      oninput: (e) => { state.departamento = e.target.value; refreshNext(); },
    });
    deptoGroup.appendChild(deptoInput);
    card.appendChild(deptoGroup);

    card.appendChild(el("p", { class: "question", style: "font-size:0.98rem;margin-top:18px;" }, "¿Vas a operar en más de un municipio?"));
    const grid = el("div", { class: "btn-grid" });
    grid.appendChild(choiceButton("No, solo en uno", state.variosMunicipios === false, () => { state.variosMunicipios = false; state.domicilioPrincipal = ""; render(); }));
    grid.appendChild(choiceButton("Sí, en varios", state.variosMunicipios === true, () => { state.variosMunicipios = true; render(); }));
    card.appendChild(grid);

    if (state.variosMunicipios === true) {
      const domGroup = el("div", { class: "field-group", style: "margin-top:12px;" });
      domGroup.appendChild(el("label", { class: "field-label" }, "¿Cuál es tu domicilio principal (la sede desde la que se dirige el negocio)?"));
      const domInput = el("input", {
        type: "text",
        value: state.domicilioPrincipal,
        placeholder: "Ej: Chía, Cundinamarca",
        oninput: (e) => { state.domicilioPrincipal = e.target.value; refreshNext(); },
      });
      domGroup.appendChild(domInput);
      card.appendChild(domGroup);
    }

    function isValid() {
      const base = state.ciudad.trim().length > 1 && state.departamento.trim().length > 1 && state.variosMunicipios !== null;
      if (state.variosMunicipios === true) return base && state.domicilioPrincipal.trim().length > 1;
      return base;
    }

    navRow(card, { onNext: goNext, nextDisabled: !isValid() });
    function refreshNext() {
      card.querySelector(".btn-primary").disabled = !isValid();
    }
  }

  // ---------------------------------------------------------------------
  // Paso 5 · Figura jurídica
  // ---------------------------------------------------------------------
  function renderFigura(card) {
    updateProgress("Figura jurídica");
    card.appendChild(el("span", { class: "section-tag" }, "3. Figura jurídica"));
    card.appendChild(el("p", { class: "question" }, "¿Bajo qué figura vas a operar tu negocio?"));

    const grid = el("div", { class: "btn-grid" });
    grid.appendChild(choiceButton("Persona natural", state.figuraJuridica === "natural", () => { state.figuraJuridica = "natural"; state.figuraHelperUsado = false; render(); }));
    grid.appendChild(choiceButton("Sociedad (SAS u otra)", state.figuraJuridica === "sas", () => { state.figuraJuridica = "sas"; state.figuraHelperUsado = false; render(); }));
    grid.appendChild(choiceButton("No sé, ayúdame a decidir", state.figuraHelperUsado, () => { state.figuraHelperUsado = true; state.figuraJuridica = null; render(); }));
    card.appendChild(grid);

    if (state.figuraHelperUsado && !state.figuraJuridica) {
      card.appendChild(
        el("div", { class: "explainer" }, [
          el("p", { style: "margin:0 0 8px;" }, "Como persona natural, tú y tu negocio son la misma persona ante la ley: si el negocio tiene deudas, responden también tus bienes personales, pero los trámites son más simples y baratos."),
          el("p", { style: "margin:0;" }, "Una SAS es una persona jurídica aparte: separa tu patrimonio personal del de la empresa (tu responsabilidad se limita a lo que aportes), permite tener socios y facilita crecer o buscar inversionistas, aunque implica más trámites."),
        ])
      );
      renderFiguraHelper(card);
    } else {
      navRow(card, { onNext: goNext, nextDisabled: !state.figuraJuridica });
    }
  }

  function renderFiguraHelper(card) {
    if (!state._figuraHelperState) {
      state._figuraHelperState = { socios: null, protegerBienes: null, crecerRapido: null };
    }
    const hs = state._figuraHelperState;

    const q = (label, key, opts) => {
      card.appendChild(el("p", { class: "question", style: "font-size:0.98rem;margin-top:14px;" }, label));
      const grid = el("div", { class: "btn-grid" });
      opts.forEach(([val, txt]) => {
        grid.appendChild(choiceButton(txt, hs[key] === val, () => { hs[key] = val; render(); }));
      });
      card.appendChild(grid);
    };

    q("¿Vas a emprender tú solo/a o con más personas (socios)?", "socios", [
      [false, "Solo yo"],
      [true, "Con más personas"],
    ]);
    q("Si el negocio tuviera problemas de plata o demandas, ¿te preocupa que te puedan pedir tus bienes personales (carro, casa, ahorros)?", "protegerBienes", [
      [true, "Sí, prefiero proteger mis bienes"],
      [false, "No me preocupa tanto"],
    ]);
    q("¿Piensas crecer rápido, buscar inversionistas o tener varios socios en el futuro?", "crecerRapido", [
      [true, "Sí"],
      [false, "No, quiero algo simple"],
    ]);

    const allAnswered = hs.socios !== null && hs.protegerBienes !== null && hs.crecerRapido !== null;
    if (allAnswered) {
      const recomienda = hs.socios || hs.protegerBienes || hs.crecerRapido ? "sas" : "natural";
      const texto = recomienda === "sas"
        ? "Con lo que nos cuentas, una Sociedad (SAS) probablemente te conviene más: protege tus bienes personales y te deja crecer con socios o inversionistas."
        : "Con lo que nos cuentas, empezar como Persona natural probablemente te conviene más: es más simple y barato mientras validas tu negocio.";
      card.appendChild(el("div", { class: "explainer" }, texto));
      const grid = el("div", { class: "btn-grid" });
      grid.appendChild(choiceButton(`Confirmar: ${recomienda === "sas" ? "Sociedad (SAS)" : "Persona natural"}`, false, () => {
        state.figuraJuridica = recomienda;
        state.figuraHelperUsado = false;
        render();
      }));
      grid.appendChild(choiceButton("Prefiero la otra opción", false, () => {
        state.figuraJuridica = recomienda === "sas" ? "natural" : "sas";
        state.figuraHelperUsado = false;
        render();
      }));
      card.appendChild(grid);
    }
    navRow(card, { onNext: goNext, nextDisabled: !state.figuraJuridica });
  }

  // ---------------------------------------------------------------------
  // Paso 6 · Infraestructura
  // ---------------------------------------------------------------------
  function renderInfraestructura(card) {
    updateProgress("Infraestructura");
    card.appendChild(el("span", { class: "section-tag" }, "4. Infraestructura"));
    card.appendChild(el("p", { class: "question" }, "¿Cómo funciona el espacio donde trabajas?"));

    const grid = el("div", { class: "btn-grid" });
    const opciones = [
      ["local_propio", "Local o punto de venta propio"],
      ["local_arrendado", "Local o punto de venta arrendado"],
      ["casa", "Trabajo desde casa"],
      ["sin_espacio_fijo", "No tengo un espacio fijo (voy donde el cliente, trabajo en la calle, etc.)"],
    ];
    opciones.forEach(([val, txt]) => {
      grid.appendChild(choiceButton(txt, state.espacio === val, () => {
        state.espacio = val;
        if (val === "sin_espacio_fijo") state.atencionPublico = false;
        else state.atencionPublico = null;
        render();
      }));
    });
    card.appendChild(grid);

    if (state.espacio && state.espacio !== "sin_espacio_fijo") {
      const preguntaTxt = state.espacio === "casa"
        ? "¿Recibes clientes o público en tu casa?"
        : "¿Ese espacio recibe visitas o atención directa de clientes o público?";
      card.appendChild(el("p", { class: "question", style: "font-size:0.98rem;margin-top:14px;" }, preguntaTxt));
      const grid2 = el("div", { class: "btn-grid" });
      grid2.appendChild(choiceButton("Sí", state.atencionPublico === true, () => { state.atencionPublico = true; render(); }));
      grid2.appendChild(choiceButton("No", state.atencionPublico === false, () => { state.atencionPublico = false; render(); }));
      card.appendChild(grid2);
    }

    if (state.espacio) {
      card.appendChild(el("p", { class: "question", style: "font-size:0.98rem;margin-top:14px;" }, "¿Cómo vendes principalmente?"));
      const grid3 = el("div", { class: "btn-grid" });
      [["online", "Solo en línea"], ["presencial", "Solo presencial"], ["ambos", "En línea y presencial"]].forEach(([val, txt]) => {
        grid3.appendChild(choiceButton(txt, state.canalVenta === val, () => { state.canalVenta = val; render(); }));
      });
      card.appendChild(grid3);
    }

    const valido = state.espacio && (state.espacio === "sin_espacio_fijo" || state.atencionPublico !== null) && state.canalVenta;
    navRow(card, { onNext: goNext, nextDisabled: !valido });
  }

  // ---------------------------------------------------------------------
  // Paso 7 · Escala
  // ---------------------------------------------------------------------
  function renderEscala(card) {
    updateProgress("Escala");
    card.appendChild(el("span", { class: "section-tag" }, "5. Escala"));
    card.appendChild(el("p", { class: "question" }, "Ahora hablemos de números (estimados, no tienen que ser exactos)"));

    const activosGroup = el("div", { class: "field-group" });
    activosGroup.appendChild(el("label", { class: "field-label" }, "Activos iniciales estimados (en pesos, COP)"));
    const activosInput = el("input", {
      type: "text", inputmode: "numeric", value: state.activos,
      placeholder: "Ej: 8.000.000",
      oninput: (e) => { state.activos = e.target.value; refreshNext(); },
    });
    activosGroup.appendChild(activosInput);
    card.appendChild(activosGroup);

    const ingresosGroup = el("div", { class: "field-group" });
    ingresosGroup.appendChild(el("label", { class: "field-label" }, "Ingresos mensuales proyectados (en pesos, COP)"));
    const ingresosInput = el("input", {
      type: "text", inputmode: "numeric", value: state.ingresos,
      placeholder: "Ej: 3.000.000",
      oninput: (e) => { state.ingresos = e.target.value; refreshNext(); },
    });
    ingresosGroup.appendChild(ingresosInput);
    card.appendChild(ingresosGroup);

    const numGroup = el("div", { class: "field-group" });
    numGroup.appendChild(el("label", { class: "field-label" }, "¿Cuántas personas van a trabajar contigo (sin contarte a ti)?"));
    const numInput = el("input", {
      type: "text", inputmode: "numeric", value: state.numPersonal,
      placeholder: "Ej: 0",
      oninput: (e) => { state.numPersonal = e.target.value; refreshNext(); },
    });
    numGroup.appendChild(numInput);
    card.appendChild(numGroup);

    card.appendChild(el("p", { class: "question", style: "font-size:0.98rem;margin-top:6px;" }, "¿Bajo qué vínculo va a trabajar esa gente contigo? (elige todas las que apliquen)"));
    const grid = el("div", { class: "btn-grid" });
    const vinculos = [
      ["ninguno", "Nadie más, trabajo solo/a"],
      ["empleados", "Empleados con contrato laboral"],
      ["contratistas", "Contratistas por prestación de servicios"],
      ["socios", "Socios que también trabajan en el negocio"],
    ];
    vinculos.forEach(([val, txt]) => {
      grid.appendChild(choiceButton(txt, state.vinculoPersonal.includes(val), () => {
        if (val === "ninguno") {
          state.vinculoPersonal = state.vinculoPersonal.includes("ninguno") ? [] : ["ninguno"];
        } else {
          state.vinculoPersonal = state.vinculoPersonal.filter((v) => v !== "ninguno");
          if (state.vinculoPersonal.includes(val)) {
            state.vinculoPersonal = state.vinculoPersonal.filter((v) => v !== val);
          } else {
            state.vinculoPersonal.push(val);
          }
        }
        render();
      }));
    });
    card.appendChild(grid);

    function isValid() {
      return state.activos.trim() !== "" && state.ingresos.trim() !== "" && state.numPersonal.trim() !== "" && state.vinculoPersonal.length > 0;
    }

    navRow(card, { onNext: goNext, nextDisabled: !isValid() });
    function refreshNext() { card.querySelector(".btn-primary").disabled = !isValid(); }
  }

  // ---------------------------------------------------------------------
  // Paso 8 · Sector específico
  // ---------------------------------------------------------------------
  function renderSectorEspecifico(card) {
    updateProgress("Tu sector");
    card.appendChild(el("span", { class: "section-tag" }, `6. Sobre tu sector: ${SECTOR_LABEL[state.sector]}`));

    const yesNo = (label, key, hint) => {
      card.appendChild(el("p", { class: "question" }, label));
      if (hint) card.appendChild(el("p", { class: "hint" }, hint));
      const grid = el("div", { class: "btn-grid" });
      grid.appendChild(choiceButton("Sí", state[key] === true, () => { state[key] = true; render(); }));
      grid.appendChild(choiceButton("No", state[key] === false, () => { state[key] = false; render(); }));
      card.appendChild(grid);
    };

    let valido = false;

    if (state.sector === "salud") {
      yesNo("¿Realizas procedimientos invasivos (que implican cortar, inyectar o entrar al cuerpo del paciente)?", "saludInvasivos");
      if (state.saludInvasivos !== null) {
        yesNo("¿Quienes atienden a los pacientes son profesionales de la salud con título y tarjeta profesional?", "saludTitulados");
      }
      valido = state.saludInvasivos !== null && state.saludTitulados !== null;
    }

    if (state.sector === "alimentos") {
      card.appendChild(el("p", { class: "question" }, "¿Tú elaboras/preparas los alimentos, los envasas con tu marca, o solo revendes productos ya empacados de otra marca?"));
      const grid = el("div", { class: "btn-grid" });
      [["elabora", "Los elaboro o preparo yo"], ["envasa_marca", "Los envaso con mi propia marca"], ["revende", "Solo revendo productos ya empacados de otra marca"]].forEach(([val, txt]) => {
        grid.appendChild(choiceButton(txt, state.alimentosTipo === val, () => {
          state.alimentosTipo = val;
          state.alimentosMarcaPropia = val === "envasa_marca" ? true : (val === "revende" ? false : state.alimentosMarcaPropia);
          render();
        }));
      });
      card.appendChild(grid);
      if (state.alimentosTipo === "elabora") {
        yesNo("¿Vendes esos alimentos bajo una marca propia (nombre, logo o etiqueta tuya)?", "alimentosMarcaPropia");
      }
      valido = state.alimentosTipo && state.alimentosMarcaPropia !== null;
    }

    if (state.sector === "belleza") {
      yesNo(
        "¿Alguno de tus procedimientos rompe la barrera de la piel (tatuajes, piercings, microblading, uñas con corte, etc.)?",
        "bellezaRompeBarrera",
        "Esto determina si necesitas inscribirte en el REPS ante la secretaría de salud."
      );
      valido = state.bellezaRompeBarrera !== null;
    }

    if (state.sector === "tecnologia") {
      yesNo(
        "¿Tu negocio trata o almacena datos personales de tus clientes o de terceros (nombres, cédulas, historiales, etc.)?",
        "techDatosTerceros"
      );
      valido = state.techDatosTerceros !== null;
    }

    if (state.sector === "educacion") {
      card.appendChild(el("p", { class: "question" }, "¿Qué tipo de educación ofreces?"));
      const grid = el("div", { class: "btn-grid" });
      [
        ["formal", "Educación formal (colegio, universidad)"],
        ["etdh", "ETDH — cursos técnicos o certificados de trabajo"],
        ["libre", "Cursos libres o talleres cortos, sin título oficial"],
      ].forEach(([val, txt]) => {
        grid.appendChild(choiceButton(txt, state.eduTipo === val, () => { state.eduTipo = val; render(); }));
      });
      card.appendChild(grid);
      valido = !!state.eduTipo;
    }

    if (state.sector === "transporte") {
      yesNo("¿Tienes flota propia de vehículos?", "transporteFlotaPropia");
      card.appendChild(el("p", { class: "question", style: "margin-top:14px;" }, "¿Transportas principalmente pasajeros o carga?"));
      const grid = el("div", { class: "btn-grid" });
      [["pasajeros", "Pasajeros"], ["carga", "Carga"]].forEach(([val, txt]) => {
        grid.appendChild(choiceButton(txt, state.transporteTipo === val, () => { state.transporteTipo = val; render(); }));
      });
      card.appendChild(grid);
      valido = state.transporteFlotaPropia !== null && !!state.transporteTipo;
    }

    navRow(card, { onNext: goNext, nextDisabled: !valido });
  }

  // ---------------------------------------------------------------------
  // Paso 9 · Contratación estatal (universal)
  // ---------------------------------------------------------------------
  function renderContratacionEstatal(card) {
    updateProgress("Una última pregunta");
    card.appendChild(el("span", { class: "section-tag" }, "6. Cualquier sector" ));
    card.appendChild(el("p", { class: "question" }, "¿Piensas contratar con el Estado (alcaldías, gobernaciones, entidades públicas)?"));
    card.appendChild(el("p", { class: "hint" }, "Esto aplica sin importar tu sector, y define si más adelante necesitas inscribirte en el Registro Único de Proponentes (RUP)."));

    const grid = el("div", { class: "btn-grid" });
    grid.appendChild(choiceButton("Sí", state.contratacionEstatal === true, () => { state.contratacionEstatal = true; render(); }));
    grid.appendChild(choiceButton("No, por ahora no", state.contratacionEstatal === false, () => { state.contratacionEstatal = false; render(); }));
    card.appendChild(grid);

    navRow(card, { onNext: goNext, nextDisabled: state.contratacionEstatal === null, nextLabel: "Ver mi ficha →" });
  }

  // ---------------------------------------------------------------------
  // Lógica de derivación
  // ---------------------------------------------------------------------
  function computeDerivacion() {
    const triggers = [];
    const entidades = new Map(); // nombre -> { tipo: 'baseline'|'trigger', items: [] }
    const openQuestions = [];

    function addEntidad(nombre, tipo, items) {
      if (!entidades.has(nombre)) entidades.set(nombre, { tipo, items: [] });
      const e = entidades.get(nombre);
      if (tipo === "trigger") e.tipo = "trigger";
      items.forEach((i) => { if (!e.items.includes(i)) e.items.push(i); });
    }

    // Baseline para (casi) cualquier negocio formal
    addEntidad("Cámara de Comercio", "baseline", ["Matrícula mercantil (o de establecimiento, si aplica)"]);
    addEntidad("DIAN", "baseline", ["Inscripción en el RUT (Registro Único Tributario)"]);

    if (state.sector === "profesionales" && state.espacio !== "local_propio" && state.espacio !== "local_arrendado" && state.vinculoPersonal.includes("ninguno")) {
      openQuestions.push("Si ejerces una profesión liberal de forma totalmente independiente y sin establecimiento, es posible que no debas matricularte en la Cámara de Comercio (Art. 19 del Código de Comercio). Confírmalo directamente con tu Cámara de Comercio.");
    }

    // Sede con atención al público
    if (state.atencionPublico === true) {
      triggers.push("Sede con atención al público → matrícula de establecimiento de comercio, concepto de uso de suelo y concepto técnico de bomberos.");
      addEntidad("Alcaldía / Curaduría municipal", "trigger", ["Concepto de uso de suelo", "Concepto técnico de bomberos (Cuerpo de Bomberos)"]);
      addEntidad("Cámara de Comercio", "trigger", ["Matrícula del establecimiento de comercio"]);
    }

    // Salud o estética invasiva → REPS
    const requiereREPS = state.sector === "salud" || (state.sector === "belleza" && state.bellezaRompeBarrera === true);
    if (requiereREPS) {
      triggers.push("Salud o estética invasiva → inscripción en el REPS ante la secretaría de salud departamental o distrital.");
      addEntidad("Secretaría de Salud departamental o distrital", "trigger", [
        "Inscripción en el REPS (Registro Especial de Prestadores de Salud)",
        "Habilitación de servicios de salud (la habilitación y las visitas de verificación son gratuitas)",
      ]);
      openQuestions.push("En salud, la Resolución 1732 de 2026 reemplaza a la 3100 de 2019, con 12 meses de transición: si te inscribes por primera vez puedes acogerte a cualquiera de las dos. Verifica con tu secretaría de salud cuál te conviene más.");
    }
    if (state.sector === "salud" && state.saludTitulados === false) {
      openQuestions.push("Nos dijiste que quienes atienden no todos tienen título y tarjeta profesional: en salud esto es obligatorio para habilitar el servicio. Revisa este punto antes de avanzar.");
    }

    // Alimentos con marca propia → INVIMA
    if (state.sector === "alimentos" && state.alimentosMarcaPropia === true) {
      triggers.push("Alimentos con marca propia → registro, permiso o notificación sanitaria ante INVIMA, además del concepto sanitario municipal.");
      addEntidad("INVIMA", "trigger", ["Registro, permiso o notificación sanitaria (según el tipo de alimento)"]);
      addEntidad("Secretaría de Salud municipal", "trigger", ["Concepto sanitario del establecimiento"]);
    } else if (state.sector === "alimentos") {
      openQuestions.push("Aunque no tengas marca propia, si preparas o manipulas alimentos para vender es probable que necesites un concepto sanitario del establecimiento. Confírmalo con la secretaría de salud de tu municipio.");
    }

    // Datos personales de terceros
    if (state.sector === "tecnologia" && state.techDatosTerceros === true) {
      triggers.push("Datos personales de terceros → política de tratamiento de datos y, si superas los topes, Registro Nacional de Bases de Datos (RNBD) ante la SIC.");
      addEntidad("Superintendencia de Industria y Comercio (SIC)", "trigger", [
        "Política de tratamiento de datos personales",
        "Registro Nacional de Bases de Datos (RNBD), solo si superas los topes vigentes",
      ]);
      openQuestions.push("Para saber si debes inscribirte en el RNBD, verifica en sic.gov.co si tu negocio supera los topes vigentes de bases de datos.");
    }

    // Empleados → ARL + PILA
    if (state.vinculoPersonal.includes("empleados")) {
      triggers.push("Empleados → afiliación a ARL antes del primer día laborado y aportes a través de PILA.");
      addEntidad("ARL / Sistema de Seguridad Social (PILA)", "trigger", [
        "Afiliación a ARL antes del primer día trabajado",
        "Aportes mensuales a salud, pensión, ARL y parafiscales vía PILA",
      ]);
    }
    if (state.vinculoPersonal.includes("contratistas")) {
      openQuestions.push("Los contratistas por prestación de servicios generalmente cotizan ellos mismos su seguridad social como independientes; verifica si en tu caso también debes afiliarlos a ARL según el nivel de riesgo de la actividad.");
    }

    // Contratación estatal → RUP
    if (state.contratacionEstatal === true) {
      triggers.push("Piensa contratar con el Estado → Registro Único de Proponentes (RUP).");
      addEntidad("Cámara de Comercio", "trigger", ["Registro Único de Proponentes (RUP)"]);
    }

    if (!state.ciiuConfirmado) {
      openQuestions.push("El código CIIU sugerido todavía no está confirmado. Verifícalo con tu Cámara de Comercio antes de matricularte, porque de este código dependen impuestos y requisitos.");
    }
    if (state.variosMunicipios === true) {
      openQuestions.push("Vas a operar en varios municipios: revisa si necesitas registros, permisos o conceptos de uso de suelo adicionales en cada uno, no solo en tu domicilio principal.");
    }
    openQuestions.push("La jurisdicción de tu Cámara de Comercio no siempre coincide con el municipio: confírmala directamente con ellos antes de matricularte.");

    return { triggers, entidades, openQuestions };
  }

  // ---------------------------------------------------------------------
  // Paso 10 · Resultado — Ficha + mapa + enlaces
  // ---------------------------------------------------------------------
  function renderResultado(card) {
    progressBar.style.width = "100%";
    progressLabel.textContent = "Ficha lista";

    const { triggers, entidades, openQuestions } = computeDerivacion();

    card.appendChild(el("span", { class: "section-tag" }, "Resultado"));
    card.appendChild(el("p", { class: "question" }, "Esta es la ficha de identificación de tu negocio"));
    card.appendChild(el("p", { class: "hint" }, "Con esto ya sabemos qué trámites, entidades y documentos te corresponden a ti — todavía no es la ruta paso a paso, es la base para construirla."));

    const infraTxt = (() => {
      const espacioTxt = { local_propio: "local propio", local_arrendado: "local arrendado", casa: "trabaja desde casa", sin_espacio_fijo: "sin espacio fijo" }[state.espacio];
      const atencionTxt = state.atencionPublico ? "con atención al público" : "sin atención al público";
      const canalTxt = { online: "venta en línea", presencial: "venta presencial", ambos: "venta en línea y presencial" }[state.canalVenta];
      return `${espacioTxt}, ${atencionTxt}, ${canalTxt}`;
    })();

    const personalTxt = (() => {
      if (state.vinculoPersonal.includes("ninguno")) return "Trabaja solo/a, sin personal por ahora";
      const map = { empleados: "empleados (contrato laboral)", contratistas: "contratistas (prestación de servicios)", socios: "socios que también trabajan" };
      return `${state.numPersonal} persona(s) — vínculo: ${state.vinculoPersonal.map((v) => map[v]).join(", ")}`;
    })();

    const ficha = el("div", { class: "ficha-card" }, [
      el("h2", {}, "FICHA DE IDENTIFICACIÓN"),
      el("p", { class: "ficha-sub" }, "Orientación general — no es asesoría jurídica ni contable."),
      el("dl", {}, [
        row("Actividad", state.actividadDescripcion),
        row("Sector", SECTOR_LABEL[state.sector] || "—"),
        row("CIIU sugerido", state.ciiuCode ? `${state.ciiuCode} — ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado por el usuario)" : " (pendiente de confirmar)"}` : "Por definir con la Cámara de Comercio"),
        row("Ciudad y departamento", `${state.ciudad}, ${state.departamento}` + (state.variosMunicipios ? ` (domicilio principal: ${state.domicilioPrincipal})` : "")),
        row("Figura jurídica", state.figuraJuridica === "sas" ? "Sociedad (SAS u otra)" : "Persona natural"),
        row("Infraestructura", infraTxt),
        row("Activos e ingresos estimados", `Activos: ${fmtCOP(state.activos) || "—"} · Ingresos mensuales: ${fmtCOP(state.ingresos) || "—"}`),
        row("Personal", personalTxt),
      ]),
    ]);
    card.appendChild(ficha);

    function row(label, value) {
      return el("div", { class: "ficha-row" }, [el("dt", {}, label), el("dd", {}, value || "—")]);
    }

    // Disparadores activados
    const mapSection1 = el("div", { class: "map-section" }, [
      el("h3", {}, "Disparadores activados"),
      triggers.length
        ? el("ul", { class: "tag-list" }, triggers.map((t) => el("li", {}, t)))
        : el("p", { class: "hint" }, "Con lo que nos contaste, no se activó ningún requisito especial más allá de la matrícula mercantil y el RUT. Igual revisa las preguntas abiertas."),
    ]);
    card.appendChild(mapSection1);

    // Mapa de entidades / documentos
    const mapSection2 = el("div", { class: "map-section" }, [
      el("h3", {}, "Mapa de entidades y documentos que te corresponden"),
    ]);
    const grid = el("div", { class: "entity-grid" });
    for (const [nombre, info] of entidades.entries()) {
      grid.appendChild(
        el("div", { class: `entity-card ${info.tipo}` }, [
          el("h4", {}, nombre),
          el("ul", {}, info.items.map((i) => el("li", {}, i))),
        ])
      );
    }
    mapSection2.appendChild(grid);
    card.appendChild(mapSection2);

    // Enlaces oficiales para gestionar documentos
    const linksSection = el("div", { class: "map-section" }, [
      el("h3", {}, "Gestiona tus documentos base aquí"),
      el("p", { class: "hint" }, "Estos dos trámites son el punto de partida para casi cualquier negocio formal en Colombia."),
      el("div", { class: "link-row" }, [
        el("a", { class: "link-btn", href: "https://www.rues.org.co", target: "_blank", rel: "noopener noreferrer" }, "🏛️ Cámara de Comercio · RUES"),
        el("a", { class: "link-btn", href: "https://www.confecamaras.co", target: "_blank", rel: "noopener noreferrer" }, "🔎 Confirmar tu Cámara de Comercio"),
        el("a", { class: "link-btn", href: "https://www.dian.gov.co", target: "_blank", rel: "noopener noreferrer" }, "🧾 RUT · DIAN"),
        el("a", { class: "link-btn", href: "https://www.vue.gov.co", target: "_blank", rel: "noopener noreferrer" }, "🧮 Preliquidador · Ventanilla Única Empresarial"),
      ]),
    ]);
    card.appendChild(linksSection);

    // Preguntas abiertas
    const openSection = el("div", { class: "map-section" }, [
      el("h3", {}, "Preguntas abiertas que faltan resolver"),
      el("ul", { class: "open-list" }, openQuestions.map((q) => el("li", {}, q))),
    ]);
    card.appendChild(openSection);

    // Texto plano copiable, en el formato exacto pedido
    const plainText = buildPlainTextFicha(triggers, entidades, openQuestions);
    const copyBox = el("pre", { class: "copy-box", id: "copyBox" }, plainText);
    card.appendChild(copyBox);

    const actions = el("div", { class: "actions-row" }, [
      el("button", {
        class: "btn btn-primary", type: "button",
        onclick: () => {
          copyBox.classList.toggle("visible");
          if (navigator.clipboard) {
            navigator.clipboard.writeText(plainText).catch(() => {});
          }
        },
      }, "📋 Ver / copiar ficha en texto"),
      el("button", { class: "btn btn-ghost", type: "button", onclick: goBack }, "← Atrás"),
      el("button", {
        class: "btn btn-ghost", type: "button",
        onclick: () => {
          if (confirm("¿Quieres empezar de nuevo? Se perderán las respuestas actuales.")) {
            location.reload();
          }
        },
      }, "Empezar de nuevo"),
    ]);
    card.appendChild(actions);

    card.appendChild(
      el("p", { class: "disclaimer-inline" },
        "Esto todavía no es tu ruta de legalización completa (pasos, orden, tiempos y costos exactos). Es la ficha base que define qué te corresponde a ti según tu actividad, ubicación, figura jurídica y escala."
      )
    );
  }

  function buildPlainTextFicha(triggers, entidades, openQuestions) {
    const infraTxt = (() => {
      const espacioTxt = { local_propio: "local propio", local_arrendado: "local arrendado", casa: "trabaja desde casa", sin_espacio_fijo: "sin espacio fijo" }[state.espacio];
      const atencionTxt = state.atencionPublico ? "con atención al público" : "sin atención al público";
      const canalTxt = { online: "venta en línea", presencial: "venta presencial", ambos: "venta en línea y presencial" }[state.canalVenta];
      return `${espacioTxt}, ${atencionTxt}, ${canalTxt}`;
    })();
    const personalTxt = (() => {
      if (state.vinculoPersonal.includes("ninguno")) return "Trabaja solo/a, sin personal por ahora";
      const map = { empleados: "empleados (contrato laboral)", contratistas: "contratistas (prestación de servicios)", socios: "socios que también trabajan" };
      return `${state.numPersonal} persona(s) — vínculo: ${state.vinculoPersonal.map((v) => map[v]).join(", ")}`;
    })();
    const entidadesFlat = [...entidades.keys()];

    return [
      "FICHA DE IDENTIFICACIÓN",
      `Actividad: ${state.actividadDescripcion}`,
      `Sector: ${SECTOR_LABEL[state.sector] || "—"}`,
      `CIIU sugerido: ${state.ciiuCode ? `${state.ciiuCode} — ${state.ciiuLabel}${state.ciiuConfirmado ? " (confirmado)" : " (pendiente de confirmar)"}` : "Por definir con la Cámara de Comercio"}`,
      `Ciudad y departamento: ${state.ciudad}, ${state.departamento}${state.variosMunicipios ? ` (domicilio principal: ${state.domicilioPrincipal})` : ""}`,
      `Figura jurídica: ${state.figuraJuridica === "sas" ? "Sociedad (SAS u otra)" : "Persona natural"}`,
      `Infraestructura: ${infraTxt}`,
      `Activos e ingresos estimados: Activos ${fmtCOP(state.activos) || "—"}, ingresos mensuales ${fmtCOP(state.ingresos) || "—"}`,
      `Personal: ${personalTxt}`,
      `Disparadores activados: [${triggers.length ? triggers.join(" | ") : "ninguno adicional a la matrícula mercantil y el RUT"}]`,
      `Entidades que le corresponden: [${entidadesFlat.join(", ")}]`,
      `Preguntas abiertas que faltan resolver: [${openQuestions.join(" | ")}]`,
    ].join("\n");
  }

  // ---------------------------------------------------------------------
  // Registro de renderers y arranque
  // ---------------------------------------------------------------------
  const STEP_RENDERERS = {
    actividad_desc: renderActividadDesc,
    sector: renderSector,
    ciiu: renderCIIU,
    ubicacion: renderUbicacion,
    figura: renderFigura,
    infraestructura: renderInfraestructura,
    escala: renderEscala,
    sector_especifico: renderSectorEspecifico,
    contratacion_estatal: renderContratacionEstatal,
    resultado: renderResultado,
  };

  render();
})();
