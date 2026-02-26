# 🛠️ Django — Módulo 6 · Guía Práctica (Clase 4)

### Archivos Estáticos, Limpieza de Estilos y Migración a Bootstrap

> Esta guía continúa el proyecto **`catalogoapp`** de las Clases anteriores. No vamos a crear nada desde cero; vamos a **profesionalizar** el diseño del proyecto que ya funciona.

---

## Contexto: el problema que vamos a resolver

Si abres tu archivo `templates/base.html`, verás que **todo el CSS del proyecto está metido dentro de una etiqueta `<style>` directamente en el HTML**. Eso funcionó hasta ahora, pero tiene varios problemas:

- Si quieres reutilizar esos estilos en otro proyecto, no puedes copiarlos fácilmente.
- El navegador del usuario **no puede guardar en caché** el CSS embebido (lo descarga cada vez).
- Mezclar HTML con CSS hace que el archivo sea difícil de leer y mantener.
- No es una práctica profesional.

Además, varios templates de la Clase 3 tienen estilos escritos directamente en las etiquetas HTML con `style="..."` (estilos inline). Estos son aún peores: si quieres cambiar un color, tienes que buscarlo en cada archivo.

> 🎯 **Meta de esta práctica:** Extraer TODO el CSS a archivos estáticos, configurar Django para servirlos, limpiar los estilos inline, y finalmente migrar el diseño a Bootstrap.

---

## Ejercicio 1 — Crear la estructura de archivos estáticos

Vamos a crear la carpeta `static/` con la organización profesional que vimos en la teoría.

### 1.1 Crear las carpetas

En la **raíz del proyecto** (al mismo nivel que `manage.py`), crea esta estructura de carpetas:

```bash
mkdir -p static/css static/js static/images
```

Tu proyecto debería quedar así:

```text
catalogoapp/                    ← Raíz del proyecto
├── config/
│   ├── settings.py
│   └── urls.py
├── core/
│   └── ...
├── productos/
│   └── ...
├── templates/
│   └── base.html
├── static/                     ← 📦 NUEVA CARPETA
│   ├── css/                    ← 🎨 Aquí irán los estilos
│   ├── js/                     ← ⚡ Aquí irá el JavaScript
│   └── images/                 ← 🖼️ Aquí irán imágenes
├── manage.py
└── db.sqlite3
```

### 1.2 Verificar

Navega a la carpeta `static/` y confirma que existen las tres subcarpetas (`css/`, `js/`, `images/`). Aún están vacías, pero pronto las llenaremos.

---

## Ejercicio 2 — Configurar Django para servir archivos estáticos

Django no encuentra los archivos estáticos automáticamente. Debemos decirle **dónde buscarlos**.

### 2.1 Abrir `config/settings.py`

Busca al final del archivo la línea que dice:

```python
STATIC_URL = 'static/'
```

### 2.2 Agregar las configuraciones estáticas

**Debajo** de `STATIC_URL`, agrega estas dos líneas:

```python
STATIC_URL = 'static/'

# Carpetas donde Django busca archivos estáticos durante el desarrollo
STATICFILES_DIRS = [BASE_DIR / 'static']

# Carpeta donde se empaquetan los estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**¿Qué hace cada línea?**

| Configuración      | Significado                                                               |
| ------------------ | ------------------------------------------------------------------------- |
| `STATIC_URL`       | La dirección web pública donde el navegador pedirá los archivos           |
| `STATICFILES_DIRS` | Le dice a Django: "busca mis estáticos en esta carpeta" (para desarrollo) |
| `STATIC_ROOT`      | Donde se empaquetarán todos los estáticos cuando subamos a producción     |

### 2.3 Verificar

Ejecuta el servidor (`python manage.py runserver`). Si arranca sin errores, la configuración está correcta. Aún no verás cambios visuales porque no hemos movido nada todavía.

---

## Ejercicio 3 — Extraer el CSS de `base.html` a un archivo estático

Este es el ejercicio más importante. Vamos a **sacar todo el CSS** que está dentro de la etiqueta `<style>` en `base.html` y moverlo a un archivo `.css` independiente.

### 3.1 Crear el archivo CSS

Crea el archivo `static/css/base.css` y **copia dentro** todo el contenido que está entre `<style>` y `</style>` en tu `templates/base.html`.

El archivo `static/css/base.css` debería quedar así (es el mismo CSS, pero ahora vive en su propio archivo):

```css
/* static/css/base.css */

/* ── Reset y base ── */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: sans-serif;
}

/* ── Navbar ── */
nav {
  background: #2c3e50;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
nav a {
  color: white;
  text-decoration: none;
  font-size: 1rem;
}
nav a:hover {
  text-decoration: underline;
}
nav form {
  margin-left: auto;
  display: flex;
  gap: 4px;
}
nav form input {
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
}
nav form button {
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

/* ── Contenido principal ── */
main {
  max-width: 900px;
  margin: 30px auto;
  padding: 0 20px;
}
h1 {
  color: #2c3e50;
  margin-bottom: 16px;
}

/* ── Listas de productos ── */
.lista-productos {
  list-style: none;
  padding: 0;
}
.lista-productos li {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}
.precio {
  font-size: 1.2rem;
  color: #27ae60;
  font-weight: bold;
}
.no-disponible {
  color: #e74c3c;
  font-size: 0.85rem;
}
.descuento {
  color: red;
}
.ahorro {
  color: green;
}
del {
  color: grey;
}

/* ── Botones y links ── */
.btn {
  display: inline-block;
  margin-top: 8px;
  padding: 8px 16px;
  background: #2ecc71;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9rem;
}
.btn:hover {
  background: #27ae60;
}

/* ── Estilos de la Clase 3 (extraídos del inline) ── */
.stock-info {
  color: grey;
}
.stock-bajo {
  color: #e67e22;
  font-weight: bold;
}
.stock-ok {
  color: #27ae60;
}
.btn-quitar {
  color: #e74c3c;
  margin-left: 15px;
  text-decoration: none;
}
.btn-vaciar {
  color: white;
  background: #e74c3c;
  padding: 8px 16px;
  border-radius: 6px;
  text-decoration: none;
  display: inline-block;
  margin-top: 10px;
}
.btn-vaciar:hover {
  background: #c0392b;
}
.badge-carrito {
  background: #e74c3c;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  margin-left: 4px;
}
.link-producto {
  color: #2c3e50;
  text-decoration: none;
}
.link-producto:hover {
  text-decoration: underline;
}
.precio-grande {
  font-size: 1.5rem;
}
```

### 3.2 Modificar `base.html` para usar el archivo estático

Ahora abre `templates/base.html` y haz **dos cambios**:

**Cambio 1:** Agrega `{% load static %}` en la **primera línea** del archivo (antes de `<!DOCTYPE html>`).

**Cambio 2:** Reemplaza **toda** la etiqueta `<style>...</style>` por un `<link>` que apunte al archivo CSS:

Tu `base.html` debería quedar así:

```html
{% load static %}
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CatálogoApp{% endblock %}</title>

    <!-- Antes aquí había 100 líneas de CSS embebido. Ahora solo hay esto: -->
    <link rel="stylesheet" href="{% static 'css/base.css' %}" />
  </head>
  <body>
    <nav>
      <a href="{% url 'home' %}">🏠 Inicio</a>
      <a href="{% url 'lista_productos' %}">📦 Catálogo</a>
      <a href="{% url 'ver_carrito' %}">
        🛒 Carrito {% if request.session.carrito %}
        <span class="badge-carrito">
          {{ request.session.carrito|length }}
        </span>
        {% endif %}
      </a>

      <form action="{% url 'buscar_producto' %}" method="GET">
        <input type="text" name="q" placeholder="Buscar producto..." />
        <button type="submit">🔍</button>
      </form>
    </nav>

    <main>{% block content %}{% endblock %}</main>
  </body>
</html>
```

### 3.3 Verificar

1. Ejecuta el servidor (`python manage.py runserver`).
2. Abre el navegador y entra a cualquier página del proyecto.
3. La página **debe verse exactamente igual que antes**: mismos colores, mismos bordes, misma navbar.
4. Si se ve sin estilos (todo blanco y desordenado), revisa que:
   - El archivo `static/css/base.css` existe y tiene contenido.
   - Pusiste `{% load static %}` en la primera línea de `base.html`.
   - Escribiste correctamente `{% static 'css/base.css' %}` en el `<link>`.
   - La configuración de `STATICFILES_DIRS` en `settings.py` es correcta.

> ✅ **Si se ve igual que antes, felicidades.** Acabas de completar tu primera migración de estilos embebidos a archivos estáticos.

---

## Ejercicio 4 — Limpiar los estilos inline de los templates

En la Clase 3 agregamos funcionalidades rápidamente y dejamos varios estilos escritos directamente en las etiquetas HTML (usando `style="..."`). Ahora que tenemos clases CSS limpias en `base.css`, vamos a eliminar esos estilos inline.

### 4.1 Limpiar `productos/templates/lista_productos.html`

Abre el archivo y busca los estilos inline que quedaron de la Clase 3. Reemplaza cada uno por la clase CSS correspondiente:

**Busca esto (stock):**

```html
<small style="color: grey;">(Quedan {{ p.stock }} unidades)</small>
```

**Reemplaza por:**

```html
<small class="stock-info">(Quedan {{ p.stock }} unidades)</small>
```

**Busca esto (stock bajo, si lo tienes):**

```html
<small style="color: #e67e22; font-weight: bold;"></small>
```

**Reemplaza por:**

```html
<small class="stock-bajo"></small>
```

**Busca esto (agotado):**

```html
<span class="no-disponible" style="font-weight: bold;"></span>
```

**Reemplaza por (quita el style):**

```html
<span class="no-disponible"></span>
```

**Busca esto (link del nombre del producto):**

```html
<a
  href="{% url 'detalle_producto' p.id %}"
  style="color: #2c3e50; text-decoration: none;"
></a>
```

**Reemplaza por:**

```html
<a href="{% url 'detalle_producto' p.id %}" class="link-producto"></a>
```

### 4.2 Limpiar `productos/templates/carrito.html`

**Busca esto (botón quitar):**

```html
<a
  href="{% url 'quitar_del_carrito' p.id %}"
  style="color: #e74c3c; margin-left: 15px; text-decoration: none;"
>
  [❌ Quitar]
</a>
```

**Reemplaza por:**

```html
<a href="{% url 'quitar_del_carrito' p.id %}" class="btn-quitar">
  [❌ Quitar]
</a>
```

**Busca esto (botón vaciar):**

```html
<a
  href="{% url 'vaciar_carrito' %}"
  style="color: white; background: #e74c3c; padding: 8px 16px; border-radius: 6px; text-decoration: none;"
>
  🗑️ Vaciar todo el carrito
</a>
```

**Reemplaza por:**

```html
<a href="{% url 'vaciar_carrito' %}" class="btn-vaciar">
  🗑️ Vaciar todo el carrito
</a>
```

### 4.3 Limpiar `productos/templates/detalle_producto.html`

**Busca todos los `style="..."` y reemplaza:**

| Antes (inline)                                           | Después (clase CSS)            |
| -------------------------------------------------------- | ------------------------------ |
| `style="font-size: 1.5rem;"` en `.precio`                | `class="precio precio-grande"` |
| `style="color: #27ae60;"` en stock                       | `class="stock-ok"`             |
| `style="color: #e67e22;"` en stock bajo                  | `class="stock-bajo"`           |
| `style="color: #2c3e50; text-decoration: none;"` en link | `class="link-producto"`        |

### 4.4 Limpiar `templates/base.html`

**Busca esto (badge del carrito):**

```html
<span
  style="background: #e74c3c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 4px;"
></span>
```

**Reemplaza por:**

```html
<span class="badge-carrito"></span>
```

> 💡 Si ya lo hicimos en el Ejercicio 3, verifica que no quedó ningún `style="..."` residual.

### 4.5 Verificar

1. Ejecuta el servidor y recorre TODAS las páginas:
   - Home
   - Catálogo (con productos con descuento, stock normal, stock bajo y agotado)
   - Detalle de un producto
   - Carrito (con productos agregados)
   - Búsqueda
2. Todo debe verse **exactamente igual** que antes.
3. Abre cada template y confirma que **no queda ningún `style="..."`** en las etiquetas HTML.

> 🎉 **Si todo se ve igual y no hay estilos inline, tu código ahora es profesional.** Los estilos viven donde deben vivir: en un archivo `.css` separado.

---

## Ejercicio 5 — Cambio de decisión: Migración a Bootstrap

> 📢 **Noticia del equipo de diseño:** _"Se ha tomado la decisión de que el proyecto usará Bootstrap para garantizar un diseño 100% responsivo y adaptable a celulares, tablets y pantallas grandes. Debes integrar Bootstrap y reemplazar los estilos actuales por componentes de Bootstrap."_

Es momento de darle un giro visual al proyecto. Vamos a instalar Bootstrap y aplicar sus componentes a cada template.

### 5.1 Agregar Bootstrap al `base.html`

Abre `templates/base.html` y agrega los CDN de Bootstrap en el `<head>` (antes de nuestro CSS personalizado) y el JavaScript de Bootstrap antes del cierre de `</body>`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CatálogoApp{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    <!-- Nuestro CSS personalizado (va DESPUÉS de Bootstrap para poder sobreescribir) -->
    <link rel="stylesheet" href="{% static 'css/base.css' %}" />
  </head>
  <body>
    <!-- Navbar de Bootstrap -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'home' %}">🛒 CatálogoApp</a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'lista_productos' %}"
                >📦 Catálogo</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'ver_carrito' %}">
                🛒 Carrito {% if request.session.carrito %}
                <span class="badge bg-danger">
                  {{ request.session.carrito|length }}
                </span>
                {% endif %}
              </a>
            </li>
          </ul>

          <form
            class="d-flex"
            action="{% url 'buscar_producto' %}"
            method="GET"
          >
            <input
              class="form-control me-2"
              type="text"
              name="q"
              placeholder="Buscar producto..."
            />
            <button class="btn btn-outline-light" type="submit">🔍</button>
          </form>
        </div>
      </div>
    </nav>

    <main class="container mt-4">{% block content %}{% endblock %}</main>

    <footer class="text-center mt-5 py-3 bg-light">
      <p class="mb-0">© 2026 CatálogoApp · Todos los derechos reservados</p>
    </footer>

    <!-- Bootstrap JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

**¿Qué cambió?**

| Antes (CSS propio)      | Ahora (Bootstrap)                                 |
| ----------------------- | ------------------------------------------------- |
| `<nav>` con CSS manual  | `navbar navbar-expand-lg navbar-dark bg-dark`     |
| Links sueltos           | `navbar-nav`, `nav-item`, `nav-link`              |
| Badge con CSS propio    | `badge bg-danger` (clase de Bootstrap)            |
| Form con CSS propio     | `d-flex`, `form-control`, `btn btn-outline-light` |
| `<main>` con CSS manual | `container mt-4`                                  |
| Sin footer              | Footer con `text-center`, `bg-light`              |
| Sin menú hamburguesa    | `navbar-toggler` para celulares                   |

> 📱 **Dato clave:** La clase `navbar-expand-lg` hace que en pantallas grandes se vea la navbar completa, pero en celulares aparezca un **menú hamburguesa** (☰) automáticamente.

### 5.2 Verificar la navbar

1. Ejecuta el servidor.
2. Abre el navegador en pantalla completa → debes ver la navbar con todos los links horizontales.
3. Achica la ventana del navegador (o usa las herramientas de desarrollo con F12 → modo responsive) → debes ver el ícono hamburguesa (☰). Al hacer clic, se despliega el menú.

---

### 5.3 Migrar `core/templates/home.html`

Abre el archivo y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Inicio{% endblock %} {% block content
%}
<div class="text-center py-5">
  <h1 class="display-4">🛒 Bienvenido al Catálogo</h1>
  <p class="lead text-muted">Explora todos nuestros productos disponibles.</p>
  <a class="btn btn-success btn-lg mt-3" href="{% url 'lista_productos' %}">
    Ver catálogo →
  </a>
</div>
{% endblock %}
```

**Clases de Bootstrap usadas:**

- `text-center` → Centra todo el texto.
- `display-4` → Título grande y elegante.
- `lead text-muted` → Subtítulo gris claro.
- `btn btn-success btn-lg` → Botón verde grande.

---

### 5.4 Migrar `productos/templates/lista_productos.html`

Abre el archivo y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Catálogo de Productos{% endblock %}
{% block content %}
<h1 class="mb-4">🛒 Catálogo de Productos</h1>

{% if productos %}
<div class="row">
  {% for p in productos %}
  <div class="col-12 col-md-6 col-lg-4 mb-4">
    <div class="card h-100">
      <div class="card-body">
        <h5 class="card-title">
          <a
            href="{% url 'detalle_producto' p.id %}"
            class="text-decoration-none text-dark"
          >
            {{ p.nombre }}
          </a>
        </h5>

        {% if p.descuento > 0 %}
        <p class="card-text">
          <del class="text-muted">${{ p.precio }}</del>
          <span class="badge bg-danger">{{ p.descuento }}% OFF</span><br />
          <span class="fs-4 fw-bold text-success">${{ p.precio_final }}</span
          ><br />
          <small class="text-success">¡Ahorras ${{ p.ahorro_monto }}!</small>
        </p>
        {% else %}
        <p class="card-text">
          <span class="fs-4 fw-bold text-success">${{ p.precio }}</span>
        </p>
        {% endif %} {% if p.hay_stock %}
        <a
          href="{% url 'agregar_al_carrito' p.id %}"
          class="btn btn-success btn-sm"
        >
          🛒 Agregar al carrito
        </a>
        {% if p.stock_bajo %}
        <span class="badge bg-warning text-dark mt-2">
          ⚠️ ¡Últimas {{ p.stock }} unidades!
        </span>
        {% else %}
        <small class="text-muted d-block mt-2"
          >(Quedan {{ p.stock }} unidades)</small
        >
        {% endif %} {% else %}
        <span class="badge bg-danger">🚫 Producto Agotado</span>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>
{% else %}
<div class="alert alert-info">No hay productos cargados todavía.</div>
{% endif %} {% endblock %}
```

**Clases de Bootstrap clave:**

| Clase                      | ¿Qué hace?                                 |
| -------------------------- | ------------------------------------------ |
| `row`                      | Crea una fila del sistema de grilla        |
| `col-12 col-md-6 col-lg-4` | 1 columna en celular, 2 en tablet, 3 en PC |
| `card h-100`               | Tarjeta con altura completa                |
| `badge bg-danger`          | Etiqueta roja para descuento               |
| `badge bg-warning`         | Etiqueta naranja para stock bajo           |
| `btn btn-success btn-sm`   | Botón verde pequeño                        |
| `text-muted`               | Texto gris                                 |

---

### 5.5 Migrar `productos/templates/carrito.html`

**Reemplaza todo** el contenido por:

```html
{% extends "base.html" %} {% block title %}Mi Carrito{% endblock %} {% block
content %}
<h1 class="mb-4">🛒 Mi Carrito</h1>

{% if productos %}
<ul class="list-group mb-4">
  {% for p in productos %}
  <li class="list-group-item d-flex justify-content-between align-items-center">
    <div>
      <strong>{{ p.nombre }}</strong> —
      <span class="text-success fw-bold">${{ p.precio_final }}</span>
    </div>
    <a
      href="{% url 'quitar_del_carrito' p.id %}"
      class="btn btn-outline-danger btn-sm"
    >
      ❌ Quitar
    </a>
  </li>
  {% endfor %}
</ul>

<h3>Total: <span class="text-success">${{ total }}</span></h3>

<a href="{% url 'vaciar_carrito' %}" class="btn btn-danger mt-3">
  🗑️ Vaciar todo el carrito
</a>
{% else %}
<div class="alert alert-secondary">
  <p class="mb-2">Tu carrito está vacío.</p>
  <a class="btn btn-success" href="{% url 'lista_productos' %}"
    >Ir al catálogo →</a
  >
</div>
{% endif %} {% endblock %}
```

**Clases de Bootstrap clave:**

- `list-group` → Lista estilizada con bordes.
- `d-flex justify-content-between` → Distribuye elementos a los extremos.
- `btn btn-outline-danger` → Botón con borde rojo (para "Quitar").
- `btn btn-danger` → Botón rojo sólido (para "Vaciar todo").
- `alert alert-secondary` → Caja gris de información.

---

### 5.6 Migrar `productos/templates/detalle_producto.html`

**Reemplaza todo** el contenido por:

```html
{% extends "base.html" %} {% block title %}{{ producto.nombre }}{% endblock %}
{% block content %}
<div class="card">
  <div class="card-body">
    <h1 class="card-title">{{ producto.nombre }}</h1>

    {% if producto.descripcion %}
    <p class="card-text text-muted">{{ producto.descripcion }}</p>
    {% endif %}

    <hr />

    {% if producto.descuento > 0 %}
    <p>
      Precio original: <del class="text-muted">${{ producto.precio }}</del>
      <span class="badge bg-danger">{{ producto.descuento }}% OFF</span>
    </p>
    <p class="fs-3 fw-bold text-success">${{ producto.precio_final }}</p>
    <p class="text-success">¡Ahorras ${{ producto.ahorro_monto }}!</p>
    {% else %}
    <p class="fs-3 fw-bold text-success">${{ producto.precio }}</p>
    {% endif %}

    <p>
      {% if producto.hay_stock %} {% if producto.stock_bajo %}
      <span class="badge bg-warning text-dark">
        ⚠️ ¡Últimas {{ producto.stock }} unidades!
      </span>
      {% else %}
      <span class="text-success fw-bold">✅ En stock</span>
      <small class="text-muted"
        >({{ producto.stock }} unidades disponibles)</small
      >
      {% endif %} {% else %}
      <span class="badge bg-danger">🚫 Sin stock</span>
      {% endif %}
    </p>

    {% if producto.hay_stock %}
    <a
      href="{% url 'agregar_al_carrito' producto.id %}"
      class="btn btn-success mt-2"
    >
      🛒 Agregar al carrito
    </a>
    {% endif %}
  </div>
</div>

<a href="{% url 'lista_productos' %}" class="btn btn-outline-secondary mt-3">
  ← Volver al catálogo
</a>
{% endblock %}
```

---

### 5.7 Migrar `productos/templates/buscar.html`

**Reemplaza todo** el contenido por:

```html
{% extends "base.html" %} {% block title %}Resultados de Búsqueda{% endblock %}
{% block content %}
<h1 class="mb-4">🔍 Resultados para "{{ query }}"</h1>

{% if resultados %}
<ul class="list-group mb-4">
  {% for p in resultados %}
  <li class="list-group-item d-flex justify-content-between align-items-center">
    <div>
      <strong>
        <a
          href="{% url 'detalle_producto' p.id %}"
          class="text-decoration-none text-dark"
        >
          {{ p.nombre }}
        </a>
      </strong>
      —
      <span class="text-success fw-bold">${{ p.precio_final }}</span>
    </div>
    <a
      href="{% url 'agregar_al_carrito' p.id %}"
      class="btn btn-success btn-sm"
    >
      🛒 Agregar
    </a>
  </li>
  {% endfor %}
</ul>
{% elif query %}
<div class="alert alert-warning">
  No se encontraron productos con ese nombre.
</div>
{% endif %}

<a href="{% url 'lista_productos' %}" class="btn btn-outline-secondary">
  ← Volver al catálogo
</a>
{% endblock %}
```

---

### 5.8 Limpiar `static/css/base.css`

Ahora que Bootstrap se encarga de la mayoría de los estilos, nuestro archivo `base.css` puede ser mucho más pequeño. **Reemplaza todo** su contenido por:

```css
/* static/css/base.css */
/* Solo estilos personalizados que Bootstrap NO cubre */

/* Ajuste del contenido principal */
main {
  min-height: 70vh;
}
```

> 💡 Al dejar nuestro `base.css` casi vacío, demostramos que Bootstrap se encarga de casi todo el diseño. Si en el futuro necesitamos un estilo particular que Bootstrap no cubra, lo agregamos aquí.

### 5.9 Verificar la migración completa

Ejecuta el servidor y recorre **TODAS** las páginas. Para cada una, verifica en pantalla completa Y achicando la ventana (simular celular):

| Página       | Qué verificar                                                           |
| ------------ | ----------------------------------------------------------------------- |
| **Home**     | Título centrado, botón verde grande, se ve bien en celular              |
| **Catálogo** | Tarjetas (cards) en grilla: 1 por fila en celular, 2 en tablet, 3 en PC |
| **Detalle**  | Card con toda la info del producto, badge de descuento/stock            |
| **Carrito**  | Lista con botones "Quitar" a la derecha, botón rojo "Vaciar"            |
| **Búsqueda** | Lista de resultados con botón "Agregar"                                 |
| **Navbar**   | En PC: links horizontales. En celular: menú hamburguesa (☰)            |

---

## Resumen de lo Practicado

En esta clase recorriste **tres transformaciones profesionales**:

| Ejercicio | Qué hiciste                                                | Habilidad clave                               |
| --------- | ---------------------------------------------------------- | --------------------------------------------- |
| 1-2       | Creaste la carpeta `static/` y configuraste `settings.py`  | Arquitectura de estáticos en Django           |
| 3         | Extrajiste el CSS embebido a `static/css/base.css`         | Separación de responsabilidades               |
| 4         | Eliminaste todos los `style="..."` inline de los templates | Código limpio y mantenible                    |
| 5         | Migraste TODO el diseño a Bootstrap                        | Framework CSS, diseño responsivo, componentes |

> 🚀 _"Tu proyecto ahora tiene arquitectura profesional de estáticos, cero estilos inline, y un diseño 100% responsivo con Bootstrap. Eso es lo que se espera en la industria."_
