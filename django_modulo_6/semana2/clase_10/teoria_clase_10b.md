# 🧩 Django — Módulo 6 · Clase 10

### Mi Primera Arquitectura de Componentes

---

> _"Antes de construir un edificio, los arquitectos dibujan los planos. Antes de crear una interfaz web, hacemos lo mismo."_

---

## ¿Qué vamos a aprender hoy?

Esta clase es una **introducción paso a paso** al mundo de los componentes. No necesitas saber nada previo sobre diseño. Solo necesitas entender HTML básico y ganas de ordenar las cosas.

- 🧱 Entenderás qué es un **componente** y por qué cambia todo.
- 📁 Aprenderás a **organizar tus archivos HTML** como un profesional.
- 🪄 Crearás tu primer componente reutilizable en Django usando `{% include %}`.
- 🎨 Entenderás la diferencia entre **HEX, HSL y REM** para escribir colores y tamaños en CSS.
- 📋 Al final completarás una **Plantilla de Decisiones** antes de comenzar tu próximo proyecto.

> 🎯 Meta: Que al terminar esta clase puedas identificar los "ladrillos" que componen cualquier página web y sepas organizarlos en Django.

---

---

# PARTE 1: EL PROBLEMA DEL CÓDIGO REPETIDO

---

## 1. Imagina Este Escenario

Estás construyendo una página web. Tienes un botón azul que quedó muy bien:

```html
<button
  style="background-color: #3182ce; color: white; padding: 10px 20px; border-radius: 6px;"
>
  Guardar
</button>
```

Lo copias y lo pegas en 10 páginas distintas de tu proyecto.

**Tres semanas después**, el cliente dice:

> _"Quiero los botones de color naranja y más grandes."_

Abres 10 archivos. Editas el mismo código 10 veces. En el archivo 7 te equivocas. El botón queda raro. Te olvidaste del archivo 9. Todo el mundo ve un botón diferente en esa sección.

Esto tiene un nombre: **Código Espagueti**. Y tiene solución.

> **💡 Dato Neuromarketing (Consistencia Visual):**
> Estudios de percepción visual demuestran que los usuarios tardan solo **0.05 segundos** en percibir si una interfaz es consistente o no. Una inconsistencia de colores entre páginas reduce la confianza del usuario hasta en un **38%**.
> _(Fuente: Lindgaard et al., Behaviour & Information Technology, 2006)_

---

## 2. La Solución: Componentes Reutilizables

El botón se escribe **una sola vez en un solo archivo**. Donde necesites un botón, simplemente llamas a ese archivo.

Si el cliente pide cambiar el color, vas a **ese único archivo**, cambias una línea y el cambio se aplica automáticamente en las 10 páginas.

Eso es un **componente**.

---

---

# PARTE 2: EL MUNDO DE LOS COMPONENTES

---

## 3. La Analogía de la Química: Átomos, Moléculas, Organismos

Así como la materia se construye desde lo más pequeño hasta lo más complejo, las interfaces también:

- Un **átomo** en química es el elemento más pequeño e indivisible. El Hidrógeno (H). El Oxígeno (O). Solo existen.
- Una **molécula** se forma cuando dos o más átomos se unen con sentido: H₂O (agua).
- Un **organismo** es un sistema complejo compuesto de muchas moléculas funcionando juntas.

En diseño web la analogía es perfecta:

| Nivel         | En Química                 | En la interfaz web                                  |
| ------------- | -------------------------- | --------------------------------------------------- |
| **Átomo**     | Hidrógeno (H), Oxígeno (O) | Un botón, un campo de texto, una etiqueta de estado |
| **Molécula**  | Agua (H₂O)                 | Una tarjeta (título + descripción + botón juntos)   |
| **Organismo** | Una célula completa        | Una barra de navegación entera, el pie de página    |
| **Página**    | Un tejido vivo             | La vista completa que el usuario ve en pantalla     |

**El poder de la analogía:**  
Si redefines el átomo "Hidrógeno" (cambias la firma del botón azul a naranja), automáticamente cambia el agua (molécula → la tarjeta que usa el botón), y cambia todo el organismo (el navbar que tiene la tarjeta).

**Un cambio. Un archivo. Miles de pantallas actualizadas.**

> **💡 Dato Neuromarketing (Jerarquía Visual):**
> Investigaciones de _Eye Tracking_ (seguimiento del ojo) demuestran que los usuarios escanean pantallas en un patrón "F": de izquierda a derecha en la parte superior, luego verticalmente hacia abajo. Los componentes con jerarquía clara (título grande → subtítulo pequeño → botón) guían naturalmente el ojo por ese camino sin que el usuario tenga que esforzarse.
> _(Fuente: Nielsen Norman Group — "F-Shaped Pattern for Reading Web Content")_

---

## 4. ¿Cómo se Llaman los Componentes en Django?

En Django, los componentes se llaman **Partials** (del inglés: plantilla parcial).

Un **Partial** es un archivo `.html` que contiene solo una parte de la interfaz. Vive en la carpeta `components/` y puede ser llamado desde cualquier otra página del proyecto usando la etiqueta `{% include %}`.

---

---

# PARTE 3: CÓDIGO PASO A PASO — DEL ÁTOMO A LA PÁGINA

---

## 5. La Estructura de Carpetas

Antes de crear el primer componente, creamos la estructura de carpetas que los albergará:

```text
templates/
├── base.html
└── components/
    ├── atoms/
    │   └── button.html
    ├── molecules/
    │   └── card.html
    └── organisms/
        └── navbar.html
```

---

## 6. Nivel 1 — El Átomo: El Botón

Creamos `templates/components/atoms/button.html`:

```django
<button class="c-btn c-btn--{{ color|default:'primary' }}">
    {{ texto|default:'Aceptar' }}
</button>
```

**Explicación línea a línea:**

| Línea                                    | Qué hace                                                                                                                                      |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `<button`                                | Abre la etiqueta HTML estándar de botón.                                                                                                      |
| `class="c-btn`                           | Aplica la clase base `c-btn` que tendrá el estilo compartido de todos los botones.                                                            |
| `c-btn--{{ color\|default:'primary' }}"` | Genera una segunda clase dinámica. Si el padre pasa `color="danger"`, la clase resultante es `c-btn--danger`. Si no pasa nada, usa `primary`. |
| `{{ texto\|default:'Aceptar' }}`         | Muestra el texto del botón. Si el padre pasa `texto="Guardar"`, muestra "Guardar". Si no pasa nada, muestra "Aceptar".                        |
| `</button>`                              | Cierra la etiqueta de botón.                                                                                                                  |

**¿Cómo se usa este átomo desde otra página?**

```django
{% include "components/atoms/button.html" with texto="Guardar" color="primary" %}
{% include "components/atoms/button.html" with texto="Eliminar" color="danger" %}
{% include "components/atoms/button.html" %}
```

**Explicación línea a línea:**

| Línea                  | Qué hace                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------ |
| `{% include "..." %}`  | Le dice a Django: "ve a ese archivo y pega su contenido aquí".                                         |
| `with texto="Guardar"` | Le pasa el valor `"Guardar"` a la variable `texto` del partial.                                        |
| `color="primary"`      | Le pasa el valor `"primary"` a la variable `color` del partial.                                        |
| Línea 3 sin `with`     | No pasa ninguna variable. El botón mostrará los valores por defecto: texto "Aceptar", color "primary". |

---

## 7. Nivel 2 — La Molécula: La Tarjeta

Una molécula combina átomos. Creamos `templates/components/molecules/card.html`:

```django
<article class="c-card">
    <h3 class="c-card__title">{{ titulo|default:'Sin título' }}</h3>
    <p class="c-card__body">{{ descripcion }}</p>
    {% include "components/atoms/button.html" with texto=texto_boton color="primary" %}
</article>
```

**Explicación línea a línea:**

| Línea                                     | Qué hace                                                                                                                                        |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `<article class="c-card">`                | Usa el elemento HTML semántico `<article>` (una pieza de contenido independiente). La clase `c-card` le dará el diseño de tarjeta desde el CSS. |
| `<h3>{{ titulo... }}</h3>`                | Muestra el título. Si el padre no pasa `titulo`, usa `'Sin título'` por defecto.                                                                |
| `<p>{{ descripcion }}</p>`                | Muestra el texto de descripción que el padre envíe.                                                                                             |
| `{% include "...button.html" with ... %}` | Aquí la molécula invoca a su átomo hijo. Le pasa `texto_boton` (que recibió del padre) y fija el color como `"primary"`.                        |
| `</article>`                              | Cierra la tarjeta.                                                                                                                              |

**¿Cómo se usa esta molécula desde una página?**

```django
{% include "components/molecules/card.html" with titulo="Python Avanzado" descripcion="Aprende las herramientas del lenguaje." texto_boton="Ver Curso" %}
```

**Explicación:**

| Parte                                         | Qué hace                                                                                 |
| --------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `{% include "components/molecules/card.html"` | Llama al partial de la tarjeta.                                                          |
| `with titulo="Python Avanzado"`               | Le pasa el título que aparecerá en el `<h3>`.                                            |
| `descripcion="Aprende las herramientas..."`   | Le pasa el texto que aparecerá en el `<p>`.                                              |
| `texto_boton="Ver Curso"`                     | Le pasa el texto del botón. La tarjeta lo reenviará internamente al átomo `button.html`. |

---

## 8. Nivel 3 — El Organismo: La Barra de Navegación

Un organismo es una sección grande de la pantalla. Creamos `templates/components/organisms/navbar.html`:

```django
<nav class="c-navbar">
    <a href="/" class="c-navbar__logo">Mi Plataforma</a>
    <ul class="c-navbar__links">
        <li><a href="/cursos/">Cursos</a></li>
        <li><a href="/perfil/">Perfil</a></li>
    </ul>
    {% include "components/atoms/button.html" with texto="Cerrar Sesión" color="danger" %}
</nav>
```

**Explicación línea a línea:**

| Línea                                              | Qué hace                                                                                                                                 |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `<nav class="c-navbar">`                           | Usa el elemento semántico `<nav>`. El CSS de `c-navbar` aplicará flexbox para distribuir horizontalmente logo, links y botón.            |
| `<a href="/">Mi Plataforma</a>`                    | El logo o nombre del sitio que lleva al inicio al hacer clic. La clase `c-navbar__logo` le aplicará el tamaño y peso de fuente correcto. |
| `<ul class="c-navbar__links">`                     | Lista de enlaces de navegación. El CSS los mostrará en fila horizontal.                                                                  |
| `{% include "components/atoms/button.html" ... %}` | El organismo reutiliza el mismo átomo de botón que ya existe. No duplica código.                                                         |
| `</nav>`                                           | Cierra el organismo de navegación.                                                                                                       |

**¿Cómo se usa este organismo desde `base.html`?**

```django
<!DOCTYPE html>
<html>
<head>
    <title>Mi Plataforma</title>
</head>
<body>

{% include "components/organisms/navbar.html" %}

<main>
    {% block content %}{% endblock %}
</main>

</body>
</html>
```

**Explicación:**

| Línea                                              | Qué hace                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `{% include "components/organisms/navbar.html" %}` | Inserta el organismo del navbar. Como no tiene datos que variar, no necesita `with`. |
| `{% block content %}{% endblock %}`                | Zona reservada donde los templates hijos insertarán su contenido propio.             |

---

> **💡 Dato Neuromarketing (Efecto de Fluidez Cognitiva):**
> Cuando el cerebro reconoce un patrón visual que ya vio antes (como un navbar siempre en el mismo lugar con el mismo formato), lo procesa casi sin esfuerzo. Las interfaces con componentes consistentes se perciben como más intuitivas y reducen la fatiga mental del usuario hasta en un **22%**.
> _(Fuente: Reber, Schwarz & Winkielman, "Processing Fluency", Personality and Social Psychology Review, 2004)_

---

---

# PARTE 4: LOS COLORES Y TAMAÑOS EN CSS (HEX, HSL y REM)

---

## 9. Tres Formas de Escribir Colores y Tamaños

Para escribir los estilos de nuestros componentes de forma profesional, existen tres sistemas:

---

### 🟦 HEX — El Sistema Clásico

```css
color: #3182ce; /* Azul */
color: #ffffff; /* Blanco */
color: #e53e3e; /* Rojo */
```

Cada color HEX es un código de 6 caracteres que mezcla Rojo (`RR`), Verde (`GG`) y Azul (`BB`).

**Limitación:** No puedes derivar variantes matemáticamente. Para hacer un azul más oscuro para el hover, tienes que inventar otro número a mano.

---

### 🌈 HSL — El Sistema Moderno (Recomendado)

```css
color: hsl(210 65% 45%); /* Azul medio */
color: hsl(210 65% 85%); /* Azul clarito — solo cambié el 3° número */
color: hsl(210 65% 25%); /* Azul oscuro  — solo cambié el 3° número */
```

| Control         | Rango         | Qué controla                                             |
| --------------- | ------------- | -------------------------------------------------------- |
| **Tono**        | `0` a `360`   | El color en sí. 0=Rojo, 120=Verde, 210=Azul, 60=Amarillo |
| **Saturación**  | `0%` a `100%` | Qué tan vivo o gris. 0%=Gris, 100%=Intensidad máxima     |
| **Luminosidad** | `0%` a `100%` | Oscuro ↔ Claro. 0%=Negro, 50%=Normal, 100%=Blanco        |

**Ventaja:** Con un solo token HSL puedes generar toda una familia de variantes del mismo color ajustando la Luminosidad.

---

### 📐 REM — Para Tamaños (No para Colores)

```css
font-size: 1rem; /* ≈ 16px por defecto  */
font-size: 1.5rem; /* ≈ 24px              */
padding: 0.5rem; /* ≈ 8px               */
```

REM respeta la configuración de accesibilidad del navegador del usuario. Si alguien aumenta la fuente base para ver mejor, todo el diseño escala proporcionalmente. Los pixeles fijos (`px`) lo ignoran y rompen la experiencia.

---

### La Regla del Equipo

| Sistema | Para qué          | Cuándo usarlo                                      |
| ------- | ----------------- | -------------------------------------------------- |
| **HEX** | Colores           | Cuando copias un color de Figma o un diseñador     |
| **HSL** | Colores           | Siempre que definas tus propias variables de color |
| **REM** | Tamaños y medidas | Siempre para fuentes, márgenes y espaciados        |

---

---

# PARTE 5: PLANTILLA DE DECISIONES (DEFINITIVA)

---

## 10. El Documento de Decisiones del Proyecto

Antes de crear el primer componente, responde estas preguntas. Toma 20 minutos y evita horas de reescritura.

---

### 📋 Plantilla: Arquitectura de Componentes

**Proyecto:** `___________________________`  
**Fecha:** `_____________`  
**Equipo:** `___________________________`

---

#### Sección 1: Colores del Sistema (Tokens)

| Variable CSS       | Valor HSL o HEX                  | Descripción                        |
| ------------------ | -------------------------------- | ---------------------------------- |
| `--clr-primary`    | `hsl(___ ___% ___%)` o `#______` | Color principal (botones, links)   |
| `--clr-secondary`  | `hsl(___ ___% ___%)` o `#______` | Color secundario o de acento       |
| `--clr-danger`     | `hsl(___ ___% ___%)` o `#______` | Acciones de peligro o eliminación  |
| `--clr-surface`    | `hsl(___ ___% ___%)` o `#______` | Fondo de tarjetas y formularios    |
| `--clr-background` | `hsl(___ ___% ___%)` o `#______` | Fondo general de la página         |
| `--clr-text-main`  | `hsl(___ ___% ___%)` o `#______` | Color del texto principal          |
| `--clr-text-muted` | `hsl(___ ___% ___%)` o `#______` | Color de textos secundarios/fechas |

---

#### Sección 2: Tamaños del Sistema (Tokens en rem)

| Variable CSS  | Valor REM  | Equivalente aproximado |
| ------------- | ---------- | ---------------------- |
| `--text-sm`   | `0.875rem` | ~14px                  |
| `--text-base` | `1rem`     | ~16px (base)           |
| `--text-lg`   | `1.25rem`  | ~20px                  |
| `--text-xl`   | `1.5rem`   | ~24px                  |
| `--space-2`   | `0.5rem`   | ~8px                   |
| `--space-4`   | `1rem`     | ~16px                  |
| `--space-6`   | `1.5rem`   | ~24px                  |
| `--space-8`   | `2rem`     | ~32px                  |
| `--radius-md` | `0.5rem`   | ~8px                   |
| `--radius-lg` | `0.75rem`  | ~12px                  |

---

#### Sección 3: Breakpoints Responsivos (Mobile-First)

| Nombre      | `min-width` | Qué cambia en el layout            |
| ----------- | ----------- | ---------------------------------- |
| **Base**    | _(ninguno)_ | Celular vertical — todo en columna |
| **Tablet**  | `768px`     |                                    |
| **Desktop** | `1024px`    |                                    |
| **TV/Wide** | `1440px`    |                                    |

---

#### Sección 4: Inventario de Átomos

| Archivo                    | ¿Qué muestra?                  | Variables que recibe (props) | ¿Creado? |
| -------------------------- | ------------------------------ | ---------------------------- | -------- |
| `atoms/button.html`        | Un botón de acción             | `texto`, `color`, `tipo`     | [ ]      |
| `atoms/badge.html`         | Una etiqueta de estado         | `texto`, `color`             | [ ]      |
| `atoms/input.html`         | Un campo de formulario         | `nombre`, `label`, `tipo`    | [ ]      |
| `atoms/_____________.html` | `____________________________` | `__________________________` | [ ]      |
| `atoms/_____________.html` | `____________________________` | `__________________________` | [ ]      |

---

#### Sección 5: Inventario de Moléculas

| Archivo                        | ¿Qué muestra?                  | Átomos que usa internamente  | ¿Creado? |
| ------------------------------ | ------------------------------ | ---------------------------- | -------- |
| `molecules/card.html`          | Una tarjeta con acción         | `button.html`                | [ ]      |
| `molecules/form_group.html`    | Label + Input + mensaje error  | `input.html`                 | [ ]      |
| `molecules/_____________.html` | `____________________________` | `__________________________` | [ ]      |
| `molecules/_____________.html` | `____________________________` | `__________________________` | [ ]      |

---

#### Sección 6: Inventario de Organismos

| Archivo                            | ¿Qué muestra?                  | Moléculas/Átomos que usa     | ¿Creado? |
| ---------------------------------- | ------------------------------ | ---------------------------- | -------- |
| `organisms/navbar.html`            | Barra de navegación superior   | `button.html`                | [ ]      |
| `organisms/footer.html`            | Pie de página                  | _(ninguno)_                  | [ ]      |
| `organisms/_________________.html` | `____________________________` | `__________________________` | [ ]      |

---

#### Sección 7: Mapa de Vistas

| Template de la vista           | Organismos que incluye | Moléculas que incluye directamente |
| ------------------------------ | ---------------------- | ---------------------------------- |
| `base.html`                    | `navbar`, `footer`     | _(ninguna — es solo el esqueleto)_ |
| `pages/home.html`              |                        |                                    |
| `pages/dashboard.html`         |                        |                                    |
| `____________________________` |                        |                                    |

---

#### Sección 8: Reglas del Equipo

| Regla                                      | Decisión             |
| ------------------------------------------ | -------------------- |
| ¿Se permite `style=""` directo en el HTML? | ❌ Nunca             |
| Prefijo para clases de componentes         | `c-` (c-btn, c-card) |
| Sistema de colores a usar                  | HSL / HEX / Ambos    |
| Sistema de tamaños a usar                  | REM / px             |
| ¿Se usa JavaScript externo?                |                      |
| ¿Se usa librería CSS externa?              |                      |

---

---

# GLOSARIO COMPLETO

---

## 11. Etiquetas, Variables y Filtros de Django en Partials

### 📌 Etiquetas (Tags) — Lo que va entre `{% %}`

| Etiqueta                 | Qué hace                                                  | Ejemplo                                        |
| ------------------------ | --------------------------------------------------------- | ---------------------------------------------- |
| `{% include %}`          | Inserta un partial (componente) en la posición actual     | `{% include "components/atoms/button.html" %}` |
| `{% include ... with %}` | Inserta un partial pasándole variables                    | `{% include "..." with texto="Guardar" %}`     |
| `{% include ... only %}` | Aísla el partial: solo ve las variables que se le pasan   | `{% include "..." with texto="Ok" only %}`     |
| `{% extends %}`          | Hereda la estructura HTML de otro template base           | `{% extends 'base.html' %}`                    |
| `{% block %}`            | Define una zona reemplazable en la herencia de templates  | `{% block content %}{% endblock %}`            |
| `{% for ... in ... %}`   | Itera sobre una lista o QuerySet de Django                | `{% for curso in cursos %}`                    |
| `{% endfor %}`           | Cierra el bloque `{% for %}`                              | `{% endfor %}`                                 |
| `{% empty %}`            | Se ejecuta si la lista del `{% for %}` está vacía         | `{% empty %} <p>No hay resultados.</p>`        |
| `{% if %}`               | Condición. Ejecuta el bloque si la condición es verdadera | `{% if user.is_authenticated %}`               |
| `{% else %}`             | Alternativa cuando el `{% if %}` no se cumple             | `{% else %} <p>Debes iniciar sesión.</p>`      |
| `{% endif %}`            | Cierra el bloque `{% if %}`                               | `{% endif %}`                                  |
| `{% url %}`              | Genera la URL de una vista por su nombre                  | `{% url 'cursos:listado' %}`                   |
| `{% static %}`           | Genera la ruta a un archivo estático (CSS, imagen)        | `{% static 'css/index.css' %}`                 |
| `{% load static %}`      | Activa el sistema de archivos estáticos de Django         | `{% load static %}` (al inicio del template)   |
| `{% csrf_token %}`       | Inserta el token de seguridad en formularios              | `<form> {% csrf_token %} </form>`              |
| `{# comentario #}`       | Comentario de una línea (no aparece en el HTML final)     | `{# Este partial espera la prop "color" #}`    |

---

### 📌 Variables y Filtros — Lo que va entre `{{ }}`

| Variable / Filtro                 | Qué hace                                                         | Ejemplo                                     |
| --------------------------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| `{{ variable }}`                  | Muestra el valor de una variable                                 | `{{ curso.nombre }}`                        |
| `{{ objeto.campo }}`              | Accede a un campo de un objeto del modelo Django                 | `{{ course.profesor }}`                     |
| `{{ variable\|default:'...' }}`   | Si la variable es vacía, usa el valor por defecto                | `{{ tipo\|default:'button' }}`              |
| `{{ variable\|lower }}`           | Convierte el texto a minúsculas                                  | `{{ nombre\|lower }}`                       |
| `{{ variable\|upper }}`           | Convierte el texto a mayúsculas                                  | `{{ nombre\|upper }}`                       |
| `{{ variable\|title }}`           | Primera letra de cada palabra en mayúscula                       | `{{ nombre\|title }}`                       |
| `{{ variable\|truncatechars:N }}` | Recorta el texto a N caracteres                                  | `{{ descripcion\|truncatechars:80 }}`       |
| `{{ variable\|date:"d M Y" }}`    | Formatea un campo de fecha                                       | `{{ curso.fecha\|date:"d/m/Y" }}`           |
| `{{ variable\|length }}`          | Devuelve cuántos elementos tiene una lista                       | `{{ cursos\|length }}`                      |
| `{{ variable\|yesno:"Sí,No" }}`   | Convierte un boolean (`True`/`False`) en texto legible           | `{{ activo\|yesno:"Activo,Inactivo" }}`     |
| `{{ forloop.counter }}`           | El número de iteración actual (desde 1) dentro de un `{% for %}` | `{{ forloop.counter }}. {{ curso.nombre }}` |
| `{{ forloop.first }}`             | `True` solo en la primera iteración del `{% for %}`              | `{% if forloop.first %} ... {% endif %}`    |
| `{{ forloop.last }}`              | `True` solo en la última iteración del `{% for %}`               | `{% if forloop.last %} ... {% endif %}`     |

---

> **💡 Dato Neuromarketing (Color y Decisiones):**
> Un estudio de HubSpot con 2,000 participantes demostró que los botones con una apariencia unificada y consistente en toda la plataforma generan un **175% más de clics** que los botones que aparecen con distintas apariencias en cada sección. Un sistema de átomos resuelve esto por diseño.
> _(Fuente: HubSpot Blog — "The Button Color A/B Test", 2012)_
