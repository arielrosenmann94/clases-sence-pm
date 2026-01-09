# Clases SENCE — Python con Django (material de apoyo y demos)

## Resumen ejecutivo

Este repositorio reúne **archivos de práctica y material de clases** usados en múltiples sesiones del programa SENCE orientado a formación Full-Stack con foco en **fundamentos web y herramientas base** que luego se conectan con el trabajo en **Python/Django** (entorno, estructura de proyecto, navegación, assets, flujo de trabajo con Git, y componentes UI).

El contenido está organizado como un conjunto de **demos autocontenidas** (principalmente HTML/CSS/JS/Bootstrap/jQuery) que se pueden abrir en el navegador para explicar conceptos y realizar ejercicios guiados.

---
## Qué incluye el proyecto (visión general)

- **Fundamentos HTML**: estructura, secciones, páginas y plantillas simples.
- **CSS básico**: estilos mínimos, layout y presentación.
- **Bootstrap**: ejemplos de maquetación rápida con componentes.
- **JavaScript (intro)**: manipulación básica y eventos.
- **jQuery (eventos y utilidades)**: eventos comunes, scroll, formularios, efectos, demos de AJAX.
- **Git (flujo de trabajo)**: material y práctica para control de versiones y repositorios remotos.
- **Páginas de ejemplo**: páginas simples tipo “sitio público” (contacto, términos, etc.).
- **Assets reutilizables**: carpetas de CSS/JS/IMG para usar en ejercicios.

---

## Estructura del repositorio (alto nivel)

- `assets/`
  - Recursos compartidos para demos.
  - Subcarpetas típicas: `css/`, `js/`, `img/`.

- `jquery/`
  - Conjunto de demos enfocadas a jQuery:
    - Eventos comunes (click, hover, scroll, teclado, submit, etc.).
    - Formularios.
    - Efectos (ej.: fade).
    - AJAX (ejemplos de consumo/flujo).

- `components/`
  - Componentes HTML reutilizables para ejercicios (p. ej. tarjetas, botones).

- `paginas/`
  - Páginas de ejemplo tipo “sitio público” (p. ej. contacto, términos).

- Archivos HTML en la raíz (demos por tema)
  - `clase_html.html`, `estructura_html.html`: estructura base y prácticas HTML.
  - `clase_css.html`: introducción práctica a CSS.
  - `clase_js_uno.html`, `clase2_js.html`: fundamentos de JavaScript.
  - `clase_boostrap.html`, `ejemplo-boostrap.html`: maquetación con Bootstrap.
  - `evento_scroll.html`, `velocidad_reaccion.html`: ejercicios interactivos (eventos/UX).
  - `funciones.html`: práctica de funciones y lógica simple.
  - `git.html`: material/práctica de Git en contexto de clase.

- `notas.md`
  - Notas breves de clase y lineamientos de ejercicios.

> Nota: el repositorio contiene múltiples ejercicios “sueltos” (no necesariamente un único proyecto integrado). La intención es pedagógica: abrir, modificar y practicar.

---

## Cómo usar este repositorio (para clases)

### Opción A — Abrir directamente en el navegador
- Haz doble clic sobre cualquiera de los `.html` y se abrirá en tu navegador.
- Ideal para revisar conceptos rápidamente o mostrar en clase.

### Opción B — Servidor local (recomendado)
Levanta un servidor local para evitar problemas de rutas relativas y trabajar como “sitio”:

```bash
cd ruta/al/repositorio
python3 -m http.server 8000


