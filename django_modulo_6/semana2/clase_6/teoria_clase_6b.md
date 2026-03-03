# 🎨 Django — Módulo 6 · Clase 6B

## Diseño antes del código: lo que nadie te cuenta en un curso

---

> _"Un template bien construido técnicamente pero visualmente pobre es como una casa con los planos perfectos y las paredes torcidas. La técnica importa. La presentación también."_

---

## Por qué un desarrollador necesita saber de diseño

No para ser diseñador. Para no sabotear el trabajo propio.

Cuando un developer entrega un proyecto con Bootstrap sin ninguna personalización, con texto negro sobre fondo blanco, sin criterio tipográfico ni paleta definida, el cliente lo ve como un prototipo — aunque el backend sea impecable.

El diseño no es decoración. Es comunicación. Es lo que hace que alguien le tenga o no le tenga confianza a un sitio en los primeros tres segundos.

Y hay una buena noticia: las reglas básicas de diseño son pocas, aprendibles, y aplicarlas correctamente diferencia a un developer promedio de uno que parece haber trabajado con diseñadores toca toda su vida.

---

---

# Parte I — Antes de abrir el editor

---

> _"El developer que empieza a codear sin haber pensado el diseño va a reescribir el CSS tres veces. El que piensa primero, codea una."_

---

## Las tres preguntas que ningún curso hace

Antes de elegir un color o una tipografía, hay que responder:

### 1. ¿Para quién es esto?

No es una pregunta de marketing. Es una pregunta de diseño.

Un CV de un desarrollador backend no debería verse igual que el de un artista gráfico. Un portfolio de un abogado no debería tener los mismos colores que el de un músico independiente.

El diseño habla antes de que el usuario lea una palabra. Si hay contradicción entre lo que el diseño transmite y lo que el contenido dice, el usuario desconfía.

**Ejercicio mental**: describí al usuario que va veamos este sitio con tres palabras. Esas palabras guían cada decisión de diseño.

---

### 2. ¿Qué tiene que sentir quien lo ve?

No qué tiene que entender — eso lo resuelve el contenido. Qué tiene que **sentir**.

- Confianza → colores sobrios, mucho espacio, tipografía clara
- Creatividad → asimetría, tipografía expresiva, colores inesperados
- Profesionalismo técnico → paleta fría, sin adornos, código que se ve bien
- Cercanía → tipografía amigable, colores cálidos, fotos reales

---

### 3. ¿Qué es lo más importante en la pantalla?

Cada página tiene una jerarquía. Hay una cosa que el usuario tiene que ver primero. Una cosa que tiene que hacer. Todo lo demás es apoyo.

Si todo compite por atención, nada gana. Un CV tiene una jerarquía clara: primero el nombre, después el cargo o perfil, después el contenido.

Define la jerarquía antes de abrir cualquier editor.

---

---

# Parte II — Color: cuántos colores necesita una paleta y cómo organizarlos

---

> _"Una paleta no es una lista de colores que te gustan. Es un sistema donde cada color tiene un rol."_

---

## ¿Cuántos colores tiene una paleta profesional?

Esta es la pregunta que los cursos no responden. La respuesta:

**Una paleta de interfaz completa tiene entre 5 y 8 colores**, organizados en grupos con roles específicos.

No 3. Tampoco 15.

Así se organiza:

| Grupo                 | Cantidad        | Qué contiene                                                      |
| --------------------- | --------------- | ----------------------------------------------------------------- |
| **Base / Neutros**    | 4–5 variaciones | Fondos, textos, bordes, dividers. Van del más oscuro al más claro |
| **Principal (Brand)** | 2–3 variaciones | Color de identidad + versión hover + versión claro/tint           |
| **Acento**            | 1–2 variaciones | El color que llama la atención: botones CTA, links                |
| **Estados**           | 4 colores fijos | Éxito (verde), Error (rojo), Advertencia (amarillo), Info (azul)  |

**Total real: 11 a 14 valores**, pero organizados — no aleatorios.

---

## La regla del 60-30-10 explica la proporción, no la cantidad

Los tres roles son proporciones de uso, no cantidad de códigos HEX:

| Rol            | Porcentaje de uso | Qué es                                                               |
| -------------- | ----------------- | -------------------------------------------------------------------- |
| **Dominante**  | 60%               | El tono base del fondo. Puede tener 4 variaciones de gris/oscuro     |
| **Secundario** | 30%               | Cards, secciones, navbar. Puede tener 2-3 variaciones                |
| **Acento**     | 10%               | Botones, links, highlights. Un solo color intenso, con versión hover |

Si pusiste 3 HEX distintos y el diseño se ve pobre, probablemente te faltan las **variaciones de cada rol**.

---

## Ejemplo de paleta completa — Perfil técnico (dark mode)

```css
:root {
  /* NEUTROS — fondos y textos */
  --bg-base: #0f172a; /* fondo principal */
  --bg-surface: #1e293b; /* cards, navbar */
  --bg-elevated: #334155; /* modales, dropdowns */
  --text-primary: #f1f5f9; /* texto principal */
  --text-muted: #94a3b8; /* subtítulos, labels */
  --border: #334155; /* separadores, borders */

  /* COLOR PRINCIPAL */
  --brand: #38bdf8; /* azul celeste */
  --brand-hover: #0ea5e9; /* hover — un tono más oscuro */
  --brand-tint: #0c4a6e; /* fondo sutil detrás de elementos brand */

  /* ESTADOS — siempre los mismos */
  --success: #22c55e;
  --error: #ef4444;
  --warning: #f59e0b;
  --info: #3b82f6;
}
```

> 💡 Bootstrap ya trae los colores de estado (`text-success`, `text-danger`, etc.). Solo necesitás definir los neutros y el brand propio.

---

## Ejemplo de paleta completa — Minimalista clara (uso general)

```css
:root {
  /* NEUTROS */
  --bg-base: #ffffff;
  --bg-surface: #f8fafc;
  --bg-elevated: #f1f5f9;
  --text-primary: #0f172a;
  --text-muted: #64748b;
  --border: #e2e8f0;

  /* COLOR PRINCIPAL */
  --brand: #6366f1; /* índigo/violeta */
  --brand-hover: #4f46e5;
  --brand-tint: #eef2ff; /* fondo muy suave para badges */

  /* ESTADOS */
  --success: #16a34a;
  --error: #dc2626;
  --warning: #d97706;
  --info: #2563eb;
}
```

---

## Ejemplo de paleta completa — Cálida (creativos, diseñadores, UX)

```css
:root {
  /* NEUTROS */
  --bg-base: #fffbf5;
  --bg-surface: #fff1dc;
  --bg-elevated: #ffe4b5;
  --text-primary: #1c1410;
  --text-muted: #6b5b45;
  --border: #e8d5b7;

  /* COLOR PRINCIPAL */
  --brand: #e67e22; /* naranja */
  --brand-hover: #ca6f1e;
  --brand-tint: #fef3e2;

  /* ESTADOS */
  --success: #27ae60;
  --error: #e74c3c;
  --warning: #f39c12;
  --info: #2980b9;
}
```

---

## Herramientas para construir paletas

| Herramienta                  | URL                         | Para qué sirve                                           |
| ---------------------------- | --------------------------- | -------------------------------------------------------- |
| **Coolors**                  | coolors.co                  | Generar y explorar paletas, exportar en HEX y CSS        |
| **Realtime Colors**          | realtimecolors.com          | Ver la paleta aplicada en un layout real antes de codear |
| **Canva Color Wheel**        | canva.com/colors            | Entender armonías: complementario, análogo, triádico     |
| **Paletton**                 | paletton.com                | Paletas científicamente armoniosas                       |
| **Coolors Contrast Checker** | coolors.co/contrast-checker | Verificar accesibilidad de cada combinación texto/fondo  |

---

> _"El diseño no se trata de hacer las cosas bonitas. Se trata de hacer las cosas claras. Lo bonito viene solo cuando lo claro está bien resuelto."_

### El truco de los diseñadores con HSL

Los developers suelen trabajar en HEX (`#3B82F6`). Los diseñadores trabajan en **HSL** (Hue, Saturation, Lightness) porque permite generar variaciones con precisión matemática:

```css
/* Una sola variable de matiz genera toda una escala coherente */
:root {
  --hue: 220; /* azul */

  --color-900: hsl(var(--hue), 90%, 10%); /* casi negro con matiz */
  --color-700: hsl(var(--hue), 70%, 25%);
  --color-500: hsl(var(--hue), 80%, 50%); /* el color puro */
  --color-300: hsl(var(--hue), 60%, 75%);
  --color-100: hsl(var(--hue), 30%, 95%); /* casi blanco con matiz */
}
```

Cambiás el matiz (`--hue`) y toda la paleta se adapta. Exactamente cómo trabajan Tailwind y Material Design internamente.

---

## Los errores de color más comunes

❌ **Demasiados colores de acento**: si el botón es naranja, los links son verde y los badges son rojo, el ojo no sabe dónde mirar. Un solo acento, siempre.

❌ **Bajo contraste**: texto gris claro sobre fondo blanco parece elegante pero es ilegible. El estándar WCAG pide contraste mínimo de **4.5:1** para texto normal. Verificar siempre con Coolors Contrast Checker.

❌ **Negro y blanco puros**: `#000000` sobre `#FFFFFF` cansa. La industria usa `#0F172A` sobre `#F8FAFC` — casi negro y casi blanco.

❌ **No definir los estados**: si no hay color de error, el usuario no sabe si algo falló. Los cuatro estados (éxito, error, advertencia, información) no son opcionales.

---

---

# Parte III — Tipografía: cuántas fuentes, cuál combinación

---

> _"La mejor tipografía es la que el usuario no nota. La peor es la que el usuario tiene que esforzarse para leer."_

---

## ¿Cuántas fuentes se usan en una interfaz?

Respuesta directa:

| Cantidad      | Cuándo                              | Resultado                                                  |
| ------------- | ----------------------------------- | ---------------------------------------------------------- |
| **1 fuente**  | Con pesos distintos (400, 600, 700) | Lo más limpio y coherente. La opción más segura            |
| **2 fuentes** | Títulos + cuerpo                    | Agrega personalidad sin desorden. Lo más usado             |
| **3 o más**   | Casi nunca justificado              | Muy difícil de equilibrar. Normalmente se ve desorganizado |

**La regla de los diseñadores**: si dudás, usá una sola fuente con distintos pesos. Poppins, Inter o Outfit con `400`, `600` y `700` resuelven el 90% de los proyectos.

---

## Tipos de fuentes y cuándo usarlos

| Tipo           | Qué son                                       | Cuándo usar                                         |
| -------------- | --------------------------------------------- | --------------------------------------------------- |
| **Sans-serif** | Sin remates (Inter, Roboto, Poppins)          | Interfaces digitales, texto de cuerpo, casi siempre |
| **Serif**      | Con remates (Merriweather, Georgia, Playfair) | Artículos largos, portfolios elegantes, impresión   |
| **Monospace**  | Ancho fijo (JetBrains Mono, Fira Code)        | Código, datos técnicos, terminales                  |
| **Display**    | Expresivas (Outfit, Raleway, Space Grotesk)   | Títulos grandes, logos, hero sections               |

---

## 5 combinaciones tipográficas por nicho — listas para usar

### 1. Perfil técnico / Developer Backend

> Transmite: precisión, seriedad, dominio técnico

**Fuentes**: `Space Grotesk` (títulos) + `Inter` (cuerpo)

```html
<link
  href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500&display=swap"
  rel="stylesheet"
/>
```

```css
html {
  font-family: "Inter", sans-serif;
  font-size: 16px;
  line-height: 1.6;
}
h1,
h2,
h3 {
  font-family: "Space Grotesk", sans-serif;
  font-weight: 700;
}
```

---

### 2. Portfolio creativo / UX Designer / Artista

> Transmite: creatividad, personalidad, originalidad

**Fuentes**: `Playfair Display` (títulos) + `Lato` (cuerpo)

```html
<link
  href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap"
  rel="stylesheet"
/>
```

```css
html {
  font-family: "Lato", sans-serif;
  font-size: 17px;
  line-height: 1.7;
}
h1,
h2,
h3 {
  font-family: "Playfair Display", serif;
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

---

### 3. Negocio / Empresa / Consultoría

> Transmite: confianza, profesionalismo, solidez

**Fuentes**: `Raleway` (títulos) + `Source Sans 3` (cuerpo)

```html
<link
  href="https://fonts.googleapis.com/css2?family=Raleway:wght@600;700&family=Source+Sans+3:wght@400;600&display=swap"
  rel="stylesheet"
/>
```

```css
html {
  font-family: "Source Sans 3", sans-serif;
  font-size: 16px;
  line-height: 1.6;
}
h1,
h2,
h3 {
  font-family: "Raleway", sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

### 4. Startup / Producto Digital / App

> Transmite: modernidad, dinamismo, frescura

**Fuentes**: `Poppins` sola, con pesos distintos

```html
<link
  href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
  rel="stylesheet"
/>
```

```css
html {
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  line-height: 1.6;
  font-weight: 400;
}
h1 {
  font-weight: 700;
  font-size: 2.5rem;
}
h2 {
  font-weight: 600;
  font-size: 1.75rem;
}
strong,
label,
.badge {
  font-weight: 500;
}
```

> 💡 Una sola fuente bien usada con 4 pesos distintos genera más coherencia que dos fuentes mal combinadas.

---

### 5. Académico / Periodismo / Blog de contenido largo

> Transmite: autoridad, legibilidad, profundidad

**Fuentes**: `Merriweather` (títulos y cuerpo largo) + `Open Sans` (UI: botones, labels, nav)

```html
<link
  href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap"
  rel="stylesheet"
/>
```

```css
html {
  font-family: "Merriweather", serif;
  font-size: 18px;
  line-height: 1.8;
}
h1,
h2,
h3 {
  font-weight: 700;
}
nav,
button,
label,
.badge {
  font-family: "Open Sans", sans-serif;
}
```

> Los artículos largos necesitan `font-size` más grande y `line-height` más amplio que una interfaz de app. Por eso la diferencia de 16px vs 18px importa.

---

## Las reglas que los diseñadores siguen siempre

| Regla                      | Valor recomendado                       | Por qué                                         |
| -------------------------- | --------------------------------------- | ----------------------------------------------- |
| Tamaño mínimo de cuerpo    | `16px`                                  | Menos de eso es difícil de leer en pantalla     |
| Line height de cuerpo      | `1.5` a `1.7`                           | Más ajustado cansa, más amplio desconecta       |
| Ancho máximo de columna    | `65ch`                                  | Punto óptimo entre 50 y 75 caracteres por línea |
| Pesos usados en una fuente | Mínimo 3: 400, 600, 700                 | Solo regular + bold crea poca jerarquía         |
| Mayúsculas en títulos      | Solo con `letter-spacing: 0.05em` o más | Sin tracking se ve apretado y difícil de leer   |

```css
/* El truco del max-width que nadie enseña */
.contenido-articulo {
  max-width: 65ch; /* se adapta al font-size, no al viewport */
  margin: 0 auto;
}
```

---

---

# Parte IV — Espaciado y jerarquía visual

---

> _"El espacio en blanco no es espacio vacío. Es el silencio que hace que la música se escuche."_

---

## El sistema de 8 puntos

La mayoría de los frameworks de diseño (y Bootstrap) usan un sistema basado en múltiplos de 8 para los espaciados:

```
4px   → separaciones mínimas (entre ícono y texto)
8px   → padding interno de elementos pequeños
16px  → espacio entre elementos relacionados
24px  → espacio entre secciones del mismo bloque
32px  → separación entre bloques distintos
48px  → separación entre secciones grandes
64px  → espacio generoso, hero sections
```

Cuando los espaciados siguen esta lógica, el diseño se siente consistente aunque el usuario nunca sepa por qué.

Bootstrap ya usa este sistema en sus clases `mt-1` (4px), `mt-2` (8px), `mt-3` (16px), `mt-4` (24px), `mt-5` (48px).

---

## Jerarquía visual: guiar el ojo

El ojo humano sigue un patrón predecible al escanear una pantalla. En idiomas occidentales, el patrón es en **F**: primero la parte superior, luego baja por el lado izquierdo con salidas horizontales.

Para una página de CV, la jerarquía típica:

```
1. NOMBRE (lo más grande, lo primero)
2. Cargo o perfil (ligeramente más pequeño, grisáceo)
3. Foto o elemento visual de apoyo
4. Links de contacto (iconos alineados)
──────────────────────────────────────────
5. Secciones (con títulos que dividen claramente)
6. Contenido de cada sección
7. Footer (mínimo, no compite)
```

Para que la jerarquía funcione:

- El `h1` debería ser **al menos el doble de tamaño** que el texto de cuerpo
- Los subtítulos de sección necesitan ser visualmente distintos: color de acento, border-bottom, o fondo diferente
- El contraste entre "importante" y "secundario" tiene que ser inmediato

---

---

# Parte V — Los tips que no están en los cursos

---

## No uses negro puro para el texto

`color: #000000` sobre fondo blanco tiene un contraste agresivo que cansa la vista en sesiones largas. Los diseñadores usan `#1A1A2E`, `#2D3748` o `#374151` — casi negro, con un leve matiz.

El ojo lo percibe como "más amable" sin saber por qué.

---

## El truco de las sombras con color

Las sombras negras (`box-shadow: 0 4px 6px rgba(0,0,0,0.1)`) funcionan pero se ven genéricas. Las sombras **con el color del elemento** se ven premium:

```css
.card {
  background: #6366f1;
  box-shadow: 0 8px 30px rgba(99, 102, 241, 0.35); /* sombra violeta */
}

.btn-primary {
  background: #e67e22;
  box-shadow: 0 4px 15px rgba(230, 126, 34, 0.4); /* sombra naranja */
}
```

---

## Bordes redondeados: el número mágico

Los `border-radius` muy pequeños (2-4px) se ven anticuados. Los muy grandes (50%) solo sirven para círculos. El rango que se ve moderno:

- Cards y contenedores: `border-radius: 12px` o `16px`
- Botones: `border-radius: 8px`
- Inputs: `border-radius: 8px`
- Chips y badges: `border-radius: 100px` (pill)

---

## Gradientes: solo en lugares específicos

Los gradientes en fondos de toda la página se ven de 2012. Los gradientes funcionan en:

- El hero de la página (primera sección que se ve)
- Elementos puntuales: el avatar, un badge, un banner
- Como overlay sobre imágenes

```css
/* Gradient en el hero — sutil, de oscuro a transparente */
.hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
}

/* Texto con gradient — solo para el nombre, efecto visual potente */
.nombre-gradient {
  background: linear-gradient(90deg, #6366f1, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

## El efecto glassmorphism (lo que se usa hoy)

El estilo de "vidrio esmerilado" que domina los portfolios de 2024-2025:

```css
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

Requiere un fondo con color o imagen detrás para que el efecto se vea. Sobre fondo blanco no hace nada.

---

## Hover states: el detalle que separa lo bueno de lo terminado

Un botón sin hover state se siente sin terminar. Un hover bien ejecutado comunica que la interfaz responde:

```css
.btn-accion {
  background: #6366f1;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  transition: all 0.2s ease; /* suaviza la transición */
  cursor: pointer;
}

.btn-accion:hover {
  background: #4f46e5; /* un tono más oscuro */
  transform: translateY(-2px); /* sube 2px — efecto de "levitar" */
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}
```

---

## La fuente de verdad: qué mirar para mejorar rápido

Los cuatro recursos que los diseñadores reales visitan constantemente:

| Recurso              | URL               | Para qué                                                       |
| -------------------- | ----------------- | -------------------------------------------------------------- |
| **Dribbble**         | dribbble.com      | Inspiración de UI, tendencias actuales                         |
| **Awwwards**         | awwwards.com      | Los mejores sitios del mundo, premiados                        |
| **Refactoring UI**   | refactoringui.com | Libro de diseño para developers, por los creadores de Tailwind |
| **Checklist Design** | checklist.design  | Qué debería tener cada componente                              |

---

---

# Parte VI — Frameworks CSS: más allá de Bootstrap

---

> _"Bootstrap no es el único framework. Es el más conocido. Saber qué más existe te permite elegir la herramienta correcta para cada proyecto."_

---

Todos los que siguen se integran igual que Bootstrap en Django: un link en el `<head>` del `base.html` y listo. No requieren instalación especial ni configuración en `settings.py`.

---

## Bootstrap 5

El más usado en el mundo del desarrollo web con Django. Ofrece una grilla de 12 columnas, decenas de componentes (navbar, cards, modales, badges, alerts) y un sistema de utilidades CSS muy completo. Su ventaja es la documentación masiva y la cantidad de ejemplos y templates gratuitos disponibles. Su desventaja: todos los sitios se parecen si no se personaliza.

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
/>
```

---

## Tailwind CSS

Funciona diferente: en lugar de componentes predefinidos, ofrece clases de utilidad que se aplican directamente en el HTML. Permite construir cualquier diseño sin escribir CSS propio. Muy popular en la industria actualmente. Requiere un poco más de aprendizaje inicial, pero da control total sobre el resultado sin sobreescribir nada. Se puede usar vía CDN en modo "play" sin build.

```html
<script src="https://cdn.tailwindcss.com"></script>
```

---

## Bulma

Framework basado en Flexbox, sin una línea de JavaScript incluida. Más liviano que Bootstrap y con una sintaxis de clases más clara e intuitiva. Ideal para proyectos donde no se necesita la maquinaria completa de Bootstrap pero sí se quiere una grilla flexible y componentes básicos bien resueltos. Las clases se leen como español natural: `is-primary`, `is-large`, `has-text-centered`.

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css"
/>
```

---

## UIkit

Framework más completo y con componentes más avanzados que Bootstrap: sliders, offcanvas, parallax, notificaciones, sticky elements. Tiene su propia capa de JavaScript. Ideal para proyectos que necesitan una interfaz rica en interacción sin llegar a usar React o Vue. La curva de aprendizaje es mayor, pero la documentación es excelente.

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/uikit@3.17.0/dist/css/uikit.min.css"
/>
<script src="https://cdn.jsdelivr.net/npm/uikit@3.17.0/dist/js/uikit.min.js"></script>
```

---

## Materialize CSS

Implementación del sistema de diseño **Material Design** de Google. Ofrece los componentes visuales que se ven en las apps de Android y Google Workspace: elevaciones, ripple effects en botones, FABs, colores vivos. Buena opción cuando el cliente pide un diseño "estilo Google" o cuando el proyecto es una app web interna.

```html
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
```

---

---

## La stack para diseños de alto impacto

> _"Bootstrap da estructura. Lo que viene a continuación agrega movimiento, interactividad y ese "wow" que separa un portfolio de otro."_

Estas cuatro herramientas se combinan con cualquier framework CSS y se cargan igual: vía CDN en el template. Juntas reproducen la experiencia visual de sitios de agencias y studios digitales, sin salir de Django.

---

## Alpine.js

Librería de JavaScript liviana (15kb) que agrega interactividad directamente en los atributos HTML, sin escribir JavaScript complejo ni usar React. Permite abrir/cerrar modales, cambiar pestañas, mostrar/ocultar elementos, hacer contadores y más, todo desde el HTML. Se lee como si el HTML pensara. Es el complemento perfecto de cualquier framework CSS dentro de Django.

```html
<script
  defer
  src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"
></script>

<!-- Ejemplo: botón que muestra/oculta un div -->
<div x-data="{ abierto: false }">
  <button @click="abierto = !abierto">Ver más</button>
  <p x-show="abierto">Contenido oculto que aparece al hacer clic.</p>
</div>
```

---

## GSAP (GreenSock Animation Platform)

La librería de animaciones más potente del ecosistema web. Usada por agencias, estudios de diseño y sitios premiados en Awwwards. Permite animar cualquier propiedad CSS con control total de tiempos, curvas de easing y secuencias. Funciona sobre cualquier elemento del DOM, sin dependencias. Si viste un sitio con animaciones que se sienten premium y fluidas, probablemente hay GSAP detrás.

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"></script>

<script>
  // Anima el h1 al cargar — fade in desde abajo
  gsap.from("h1", { opacity: 0, y: 40, duration: 0.8, ease: "power3.out" });
</script>
```

---

## AOS — Animate On Scroll

Permite que los elementos aparezcan con animación cuando el usuario hace scroll y los descubre. Se configura con atributos HTML: `data-aos="fade-up"`, `data-aos-delay="200"`. No requiere escribir JavaScript. El resultado es esa sensación de sitio moderno donde el contenido "entra" a medida que se baja. Simple, liviano y con excelentes resultados visuales con mínimo esfuerzo.

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css"
/>
<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
<script>
  AOS.init({ duration: 700, once: true });
</script>

<!-- Uso en cualquier elemento del template -->
<div data-aos="fade-up" data-aos-delay="100">
  <h2>Esta sección aparece animada al hacer scroll</h2>
</div>
```

---

## Swiper.js

La librería de carousels y sliders más usada en producción. Soporta swipe táctil en móvil, autoplay, paginación, navegación por flechas, efectos de transición (fade, cube, cards), lazy loading de imágenes y mucho más. Resulta indispensable para galerías de proyectos, testimonios, portfolios de imágenes o cualquier contenido que deba mostrarse en secuencia.

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
/>
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>

<div class="swiper">
  <div class="swiper-wrapper">
    <div class="swiper-slide">Proyecto 1</div>
    <div class="swiper-slide">Proyecto 2</div>
  </div>
  <div class="swiper-pagination"></div>
</div>
<script>
  new Swiper(".swiper", { pagination: { el: ".swiper-pagination" } });
</script>
```

---

## ¿Cuál elegir?

| Si necesitás...                          | Usá          |
| ---------------------------------------- | ------------ |
| Componentes listos, máxima documentación | Bootstrap 5  |
| Control total del diseño sin CSS propio  | Tailwind CSS |
| Algo más limpio que Bootstrap, sin JS    | Bulma        |
| Componentes avanzados e interactivos     | UIkit        |
| Estética de app móvil Google             | Materialize  |
| Interactividad sin JavaScript complejo   | Alpine.js    |
| Animaciones premium y fluidas            | GSAP         |
| Elementos que aparecen al hacer scroll   | AOS          |
| Carousels táctiles con efecto premium    | Swiper.js    |

---

---

---

# Parte VII — Neuromarketing aplicado al diseño web

---

> _"El usuario no lee el sitio. Lo escanea, lo siente y decide en milisegundos. El diseño que ignora cómo funciona el cerebro trabaja en contra de sí mismo."_

---

El neuromarketing estudia cómo el cerebro responde a estímulos visuales y de comunicación. Estas son las investigaciones con mayor impacto directo en decisiones de diseño web:

---

## 1. La primera impresión visual dura 50 milisegundos

**Fuente**: Lindgaard, G. et al. (2006). _Attention web designers: You have 50 milliseconds to make a good first impression_. Behaviour & Information Technology.

El cerebro forma una opinión sobre la credibilidad de un sitio en 50ms — antes de leer una sola palabra. Esa impresión es casi imposible de revertir después. El diseño visual no es accesorio: es la primera comunicación que el sitio hace.

**Aplicación directa**: el hero de la página (lo visible sin scrollear) es la decisión de diseño más importante. Color, tipografía y espaciado hablan antes que el contenido.

---

## 2. Escáner en F: el ojo no lee, escanea

**Fuente**: Nielsen, J. & Pernice, K. (2006). _Eyetracking Web Usability_. Nielsen Norman Group. (10 años de investigación, 232 usuarios, eye-tracking)

El ojo sigue un patrón en F al escanear pantallas: lee la parte superior de izquierda a derecha, baja por el lado izquierdo, y hace salidas horizontales en los primeros ítems de cada sección. Las palabras al final de una línea rara vez se leen en el primer escaneo.

**Aplicación directa**: la información más importante va a la izquierda y arriba. Los primeros 2-3 palabras de cada línea y título son los únicos que se garantizan ser leídos.

---

## 3. Ley de Hick — más opciones, menos decisiones

**Fuente**: Hick, W.E. (1952). _On the rate of gain of information_. Quarterly Journal of Experimental Psychology. / Hyman, R. (1953). _Stimulus information as a determinant of reaction time_.

A mayor cantidad de opciones, mayor el tiempo que toma decidir — y mayor la probabilidad de no decidir nada. La relación es logarítmica: duplicar las opciones no duplica el tiempo, pero sí lo aumenta de forma predecible.

**Aplicación directa**: los menús de navegación con más de 5-7 ítems aumentan la tasa de abandono. El formulario de contacto con menos campos convierte más que el completo. La página de producto con un solo CTA convierte más que la que tiene tres.

---

## 4. El color azul genera confianza institucional

**Fuente**: Labrecque, L.I. & Milne, G.R. (2012). _Exciting red and competent blue: the importance of color in marketing_. Journal of the Academy of Marketing Science.

El azul activa percepción de competencia, confianza y confiabilidad. El rojo activa excitación y urgencia. El verde se asocia a crecimiento y acción positiva. Estas asociaciones son cross-culturales y no son arbitrarias — tienen correlatos medibles en actividad neuronal.

**Aplicación directa**: un sitio de servicios profesionales o tecnología que usa azul como color principal tiene una ventaja inicial de credibilidad. No es una regla absoluta, pero es el punto de partida más seguro para perfiles que necesitan transmitir confianza.

---

## 5. La velocidad de carga es una variable de neuromarketing

**Fuente**: Deloitte & Google (2019). _Milliseconds make millions_. Investigación sobre 37 marcas de retail, viajes y finanzas en múltiples países.

Una mejora de 0.1 segundos en el tiempo de carga se correlaciona con un aumento del **8% en conversión** en retail y **10% en páginas de viajes**. El cerebro percibe las esperas como fricciones, y la fricción genera desconfianza antes de que el usuario pueda articular por qué.

**Aplicación directa en Django**: no cargar 9 pesos de una fuente cuando se usan 3. No incluir animaciones en JavaScript que bloqueen el render inicial. Archivos CSS y JS al final del body o con `defer`.

---

## 6. La prueba social reduce la incertidumbre del cerebro

**Fuente**: Cialdini, R.B. (1984). _Influence: The Psychology of Persuasion_. Harper Collins. (Replicado extensivamente en estudios de UX y conversión.)

Frente a la incertidumbre, el cerebro usa el comportamiento de otros como atajo de decisión. Ver que otros hicieron algo reduce el costo cognitivo de decidir. En diseño web, los números concretos generan más confianza que los adjetivos.

**Aplicación directa**: "127 proyectos entregados" convierte mejor que "muchos años de experiencia". "Usado por 4.200 estudiantes" genera más confianza que "curso popular". En un CV: cantidad de proyectos, clientes o tecnologías que se dominan, no solo la lista.

---

## 7. La dirección de la mirada guía la atención

**Fuente**: Langton, S.R.H. (2000). _The mutual influence of gaze and head orientation in the analysis of social attention direction_. Quarterly Journal of Experimental Psychology. / Investigación de eye-tracking de Nielsen Norman Group.

Los seres humanos seguimos instintivamente la dirección de la mirada de otras personas. En una interfaz web, si hay una imagen de una persona mirando hacia un elemento (un botón, un formulario, un texto clave), la atención del usuario se dirige automáticamente hacia ese elemento.

**Aplicación directa**: si en el hero de un portfolio hay una foto de perfil, orientarla levemente hacia el texto o el botón de contacto aumenta la atención sobre ese elemento sin que el usuario lo note conscientemente.

---

## 8. La carga cognitiva reduce la confianza

**Fuente**: Sweller, J. (1988). _Cognitive load during problem solving: Effects on learning_. Cognitive Science. / Miller, G.A. (1956). _The magical number seven, plus or minus two_.

El cerebro tiene una capacidad limitada de procesar información en simultáneo. Cuando una interfaz supera esa capacidad (demasiados elementos, demasiado contraste, demasiada información), la respuesta emocional es incomodidad y desconfianza.

**Aplicación directa**: el espacio en blanco no es espacio vacío — reduce la carga cognitiva y hace que el sitio "se sienta" más inteligente y confiable. Menos elementos por página, con mayor claridad jerárquica, produce una experiencia más positiva aunque el contenido sea idéntico.

---

## Resumen de principios con aplicación directa

| Principio                     | Fuente                       | Aplicación en diseño                                  |
| ----------------------------- | ---------------------------- | ----------------------------------------------------- |
| Primera impresión en 50ms     | Lindgaard et al., 2006       | El hero define la credibilidad antes que el contenido |
| Patrón F de lectura           | Nielsen & Pernice, 2006      | Lo importante va a la izquierda y arriba              |
| Ley de Hick                   | Hick, 1952                   | Menús cortos, un solo CTA por página                  |
| Color azul = confianza        | Labrecque & Milne, 2012      | Perfiles profesionales/tech se benefician del azul    |
| 0.1s de carga = 8% conversión | Deloitte & Google, 2019      | Optimizar carga de fuentes, CSS y JS                  |
| Prueba social                 | Cialdini, 1984               | Números concretos > adjetivos                         |
| Dirección de mirada           | Langton, 2000                | La foto de perfil orienta la atención                 |
| Carga cognitiva               | Sweller, 1988 / Miller, 1956 | Espacio en blanco = confianza                         |

---

---

# Cierre — El cuestionario de diseño completo

---

Respondé estas preguntas antes de escribir el primer template. Cada respuesta te dice exactamente qué herramienta usar.

---

## 🎯 Sobre el proyecto

- [ ] ¿Para quién es el sitio? ¿Qué tres adjetivos lo describen?
- [ ] ¿Cuál es la acción principal que el usuario debe hacer (o la información que debe ver primero)?
- [ ] ¿El sitio necesita transmitir calidez o frialdad? ¿Cercanía o distancia profesional?

---

## 🎨 Decisiones de color

- [ ] ¿Hay una identidad de marca ya definida (logo con colores)? Si sí → tomá el color del logo como brand.
- [ ] ¿El sitio será **oscuro** (dark mode) o **claro** (light mode)?
- [ ] ¿Define los 4 grupos de la paleta: neutros, brand, acento, estados?
- [ ] ¿Las combinaciones de texto/fondo pasan el contraste mínimo 4.5:1?

**¿Gradientes o colores planos?**

| Si el sitio transmite...          | Entonces...                                                    |
| --------------------------------- | -------------------------------------------------------------- |
| Tecnología, precisión, datos      | Colores planos con acento vibrante. Gradientes solo en el hero |
| Creatividad, arte, movimiento     | Gradientes permitidos en secciones, textos con gradient        |
| Corporativo, consultoría          | Colores planos siempre. Sin gradientes                         |
| Startup, producto digital moderno | Gradientes sutiles + glassmorphism en cards                    |
| Portfolio personal / CV           | Depende del nicho al que apuntás (ver columna anterior)        |

---

## 🔤 Decisiones tipográficas

- [ ] ¿Cuántas fuentes? (1 con pesos distintos o 2 máximo)
- [ ] ¿Cuál de las 5 combinaciones del documento encaja con el nicho?
- [ ] ¿Cargué solo los pesos que uso? (Cargar 9 pesos de una fuente penaliza la velocidad de carga)
- [ ] ¿El tamaño base es mínimo 16px? ¿El line-height entre 1.5 y 1.7?

---

## ✨ Decisiones de estilo visual

**¿Animaciones o estático?**

| Si...                                 | Entonces...                                             |
| ------------------------------------- | ------------------------------------------------------- |
| El sitio es una app o dashboard       | Solo micro-animaciones en hover y transiciones (0.2s)   |
| Es un portfolio creativo              | Animaciones de entrada al scroll (sutiles)              |
| Es un sitio corporativo o informativo | Sin animaciones. El movimiento distrae del contenido    |
| Es un CV de developer                 | Hover en cards y botones. Nada más. Que el código hable |

**¿Sombras con color o neutras?**

| Si tengo un color de acento definido | Sombras con ese color (`rgba` del brand)               |
| ------------------------------------ | ------------------------------------------------------ |
| Si el diseño es muy neutro           | Sombras negras muy sutiles (`rgba(0,0,0,0.08)`)        |
| Si el fondo es oscuro                | Sin sombra, usar `border: 1px solid` con opacidad baja |

**¿Bordes redondeados o rectos?**

| Personalidad del sitio     | Border-radius                                |
| -------------------------- | -------------------------------------------- |
| Moderno, amigable, startup | 12px–16px en cards, 8px en botones           |
| Serio, corporativo         | 4px–6px. Casi recto                          |
| Muy minimalista            | 0px. Sin redondeo                            |
| Muy creativo / playful     | border-radius asimétrico (3px 16px 16px 3px) |

**¿Glassmorphism o sólido?**

| Usar glassmorphism                             | No usar glassmorphism                 |
| ---------------------------------------------- | ------------------------------------- |
| Hay un fondo con color/gradiente/imagen detrás | El fondo es blanco puro               |
| El sitio tiene una estética de app moderna     | El sitio es informativo o corporativo |
| Las cards son secundarias, no el foco          | Las cards son el elemento principal   |

---

## 📐 Espaciado y estructura

- [ ] ¿Define el espaciado base (múltiplos de 8)?
- [ ] ¿Determiné la jerarquía: qué va primero, qué es secundario?
- [ ] ¿El contenido tiene un ancho máximo definido? (recomendado: 1200px para layout, 65ch para texto)
- [ ] ¿Los botones e interactivos tienen hover state con `transition`?

---

> Una vez que puedes responder todo este cuestionario, el template es solo traducción. El trabajo de diseño ya está hecho.

---
