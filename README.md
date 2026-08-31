# Emprendimiento — Ficha de Identificación de Negocio

Primer módulo del proyecto: **dale identidad a tu negocio**. Antes de mostrarle a un
emprendedor la ruta completa de legalización, necesitamos entender qué hace, dónde
opera y bajo qué figura jurídica trabaja. Ese es el propósito de esta ficha: reunir
la información mínima para saber qué trámites, entidades, documentos y costos le
corresponden a este emprendedor y no a otro.

Este módulo **no entrega la ruta de trámites completa** (orden, tiempos, costos
exactos): solo identifica al negocio y muestra el mapa de entidades/documentos que
le aplican, con enlaces oficiales para empezar a gestionarlos.

## Cómo funciona

Es una aplicación web estática (HTML + CSS + JavaScript, sin frameworks ni paso de
build) con un asistente de preguntas por botones, en lenguaje simple y sin jerga
legal:

1. **Actividad** — qué vende o qué servicio presta, sector, y un código CIIU
   sugerido (a confirmar).
2. **Ubicación** — ciudad, departamento y domicilio principal si opera en varios
   municipios.
3. **Figura jurídica** — persona natural o sociedad (SAS u otra), con un asistente
   de decisión si el usuario no lo sabe.
4. **Infraestructura** — si tiene local o sede con atención al público, si es
   propio/arrendado/casa, y si vende en línea, presencial o ambos.
5. **Escala** — activos iniciales, ingresos mensuales proyectados y personal.
6. **Preguntas específicas del sector** (salud, alimentos, belleza, tecnología,
   educación o transporte) y la pregunta universal sobre contratación estatal.

Con esas respuestas, la app aplica la lógica de derivación (causa → efecto) y
genera:

- La **ficha de identificación** en el formato de salida acordado.
- Un **mapa de entidades y documentos** agrupado por entidad (Cámara de Comercio,
  DIAN, Alcaldía, Secretaría de Salud, INVIMA, SIC, ARL/PILA, RUP).
- **Enlaces oficiales** para gestionar los documentos base: Cámara de Comercio
  (RUES / Confecámaras), RUT (DIAN) y el preliquidador de la Ventanilla Única
  Empresarial (vue.gov.co).
- Las **preguntas abiertas** que todavía hay que resolver antes de avanzar a la
  ruta de trámites.

## Ejecutar el proyecto

No requiere instalación ni dependencias. Basta con abrir `index.html` en el
navegador, o servirlo con cualquier servidor estático, por ejemplo:

```bash
python3 -m http.server 8000
# luego abrir http://localhost:8000
```

## Estructura

```
index.html   Estructura de la página y encabezado/pie con el disclaimer legal
styles.css   Estilos de la app (tarjetas, botones de opción, ficha final)
app.js       Estado del asistente, preguntas, lógica de derivación y ficha final
```

## Alcance y límites

- Marco legal colombiano vigente 2026 (UVB $12.110, UVT $52.374, salario mínimo
  $1.750.905 + auxilio de transporte $249.095). En salud, contempla la transición
  de 12 meses entre la Resolución 3100 de 2019 y la 1732 de 2026.
- No inventa direcciones, tarifas exactas ni enlaces no verificados: cuando falta
  un dato preciso, remite al sitio oficial de la entidad o a vue.gov.co.
- Aclara siempre que es orientación general, no asesoría jurídica ni contable.
- La jurisdicción de la Cámara de Comercio no siempre coincide con el municipio:
  la app pide confirmarla, nunca la asume.

## Próximos pasos

Este módulo es la base para el siguiente: la ruta de legalización paso a paso
(trámites en orden, tiempos y costos estimados), que tomará como entrada la ficha
de identificación generada aquí.
