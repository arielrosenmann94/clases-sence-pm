# 🛠️ Django — Módulo 6 · Guía Práctica (Clase 2)

### Arquitectura Profesional, Lógica de Negocio y Sesiones

> Esta guía continúa el proyecto **`catalogoapp`** iniciado en la Clase 1. A través de este ejercicio, transformaremos un proyecto básico en una aplicación con estructura profesional y funcionalidades de negocio reales.

---

## Introducción

En esta segunda clase, nuestro objetivo es "limpiar" el código heredado y agregar nuevas responsabilidades al sistema. No crearemos un proyecto nuevo; refactorizaremos el existente para que cumpla con los estándares de la industria.

---

## Paso 1 — Refactorización Arquitectónica (`config/`)

Actualmente, tu carpeta de configuración se llama igual que el proyecto (`catalogoapp/`). Vamos a cambiarla al nombre estándar **`config`** para evitar confusiones.

### 1.1 Renombrar la carpeta

Cierra tu servidor de desarrollo (`Ctrl+C`) y renombra la carpeta interna:
De: `catalogoapp/catalogoapp/`  
A: **`catalogoapp/config/`**

### 1.2 Actualizar `manage.py`

Abre `manage.py` en la raíz y cambia la referencia a los settings:

```python
# manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Antes decía catalogoapp.settings
```

### 1.3 Actualizar `config/settings.py`

Abre `config/settings.py` y busca las siguientes líneas para actualizarlas:

```python
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
```

### 1.4 Actualizar `wsgi.py` y `asgi.py`

En ambos archivos (`config/wsgi.py` y `config/asgi.py`), cambia la línea del módulo de configuración:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

### 1.5 Verificar la refactorización

Ejecuta el servidor: `python manage.py runserver`. Si el cohete (o tu home) carga sin errores, has migrado con éxito a una arquitectura profesional.

### 1.6 Observación: El otro "Config"

Abre el archivo `productos/apps.py`. Verás una clase llamada `ProductosConfig`.

> 💡 **No te confundas:** Aunque ambos usan la palabra "Config", la carpeta `config/` es la arquitectura de tu proyecto entero, mientras que la clase en `apps.py` es solo la configuración interna de esa aplicación específica.

---

## Paso 2 — Preparación del Catálogo

Para que las funcionalidades matemáticas y de búsqueda tengan sentido, necesitamos datos.

1. Ingresa al panel de administración: `http://127.0.0.1:8000/admin/`.
2. Asegúrate de tener al menos **10 productos** cargados.
3. Agrégales nombres variados y precios distintos.

---

## Paso 3 — Lógica de Negocio en el Modelo ("Fat Models")

Siguiendo el principio de _"Include all relevant domain logic"_, vamos a dotar al modelo `Producto` de la capacidad de calcular ofertas.

### 3.1 Actualizar el Modelo

Abre `productos/models.py` y agrega un campo de descuento y un método de cálculo:

```python
from decimal import Decimal

class Producto(models.Model):
    # ... campos anteriores ...
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0, help_text="Porcentaje de descuento (0-100)")

    def precio_final(self):
        """Calcula el precio aplicando el descuento si existe."""
        if self.descuento > 0:
            rebaja = self.precio * (Decimal(self.descuento) / Decimal(100))
            return self.precio - rebaja
        return self.precio

    def ahorro_monto(self):
        """Devuelve cuánto dinero se ahorra el cliente."""
        return self.precio - self.precio_final()
```

### 3.2 Aplicar Migraciones

Como agregamos el campo `descuento`, debemos migrar:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3.3 Actualizar el Template

Abre `productos/templates/lista_productos.html` y muestra la oferta:

```html
<!-- productos/templates/lista_productos.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Catálogo de Productos</title>
    <style>
      body {
        font-family: sans-serif;
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
      }
      h1 {
        color: #2c3e50;
      }
      ul {
        list-style: none;
        padding: 0;
      }
      li {
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
    </style>
  </head>
  <body>
    <h1>🛒 Catálogo de Productos</h1>

    {% if productos %}
    <ul>
      {% for p in productos %}
      <li>
        <strong>{{ p.nombre }}</strong> <br />
        {% if p.descuento > 0 %}
        <del style="color: grey;">${{ p.precio }}</del>
        <span style="color: red;">{{ p.descuento }}% OFF</span> <br />
        <span style="font-size: 1.2rem; font-weight: bold;"
          >${{ p.precio_final }}</span
        >
        <p style="color: green;">¡Ahorras ${{ p.ahorro_monto }}!</p>
        {% else %}
        <span style="font-size: 1.2rem;">${{ p.precio }}</span>
        {% endif %}
        <a href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar al carrito</a>
      </li>
      {% endfor %}
    </ul>
    {% else %}
    <p>
      No hay productos cargados todavía. Ingresá al
      <a href="/admin/">panel de administración</a> para agregar algunos.
    </p>
    {% endif %}
  </body>
</html>
```

---

## Paso 4 — Carrito de Compras Básico (Uso de Sesiones)

Vamos a usar el objeto `request.session` para que el usuario pueda "guardar" productos mientras navega.

### 4.1 La Vista para Agregar

Abre `productos/views.py` y añade esta lógica sencilla:

```python
from django.shortcuts import redirect

def agregar_al_carrito(request, producto_id):
    # Inicializamos el carrito en la sesión si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    # Agregamos el ID del producto a la lista
    carrito = request.session['carrito']
    carrito.append(producto_id)
    request.session['carrito'] = carrito # Guardamos cambios explícitamente

    return redirect('lista_productos')

def ver_carrito(request):
    ids_en_carrito = request.session.get('carrito', [])
    productos = Producto.objects.filter(id__in=ids_en_carrito)

    total = sum(p.precio_final() for p in productos)

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total
    })
```

### 4.2 Configurar las URLs

En `productos/urls.py`:

```python
path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
path('carrito/', ver_carrito, name='ver_carrito'),
```

### 4.3 Botón en el Catálogo

En `lista_productos.html`, agrega el botón para cada producto:

```html
<a href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar al carrito</a>
```

---

## Paso 5 — Formulario de Búsqueda (Django Forms)

Implementaremos la búsqueda de productos usando la clase `forms.Form`.

### 5.1 Crear `productos/forms.py`

```python
from django import forms

class BusquedaProductoForm(forms.Form):
    query = forms.CharField(
        label='Buscar por nombre',
        max_length=100,
        required=True
    )
```

### 5.2 Vista con Formulario

En `productos/views.py`:

````python
def buscar_producto(request):
    form = BusquedaProductoForm()
    resultados = []

    if request.method == 'POST':
        form = BusquedaProductoForm(request.POST)
        if form.is_valid():
            termino = form.cleaned_data['query']
            resultados = Producto.objects.filter(nombre__icontains=termino)

    return render(request, 'buscar.html', {'form': form, 'resultados': resultados})

### 5.3 Crear el template de búsqueda

Crea el archivo `productos/templates/buscar.html` con el siguiente contenido:

```html
<!-- productos/templates/buscar.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscador de Productos</title>
    <style>
      body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
      h1 { color: #2c3e50; }
    </style>
</head>
<body>
    <h1>🔍 Buscar en el Catálogo</h1>

    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Buscar</button>
    </form>

    {% if resultados %}
      <h2>Resultados:</h2>
      <ul>
      {% for p in resultados %}
        <li>{{ p.nombre }} — ${{ p.precio }}</li>
      {% endfor %}
      </ul>
    {% endif %}
</body>
</html>
````

### 5.4 Crear el template del carrito

En el Paso 4 creamos la vista `ver_carrito`, pero nos falta su template. Crea el archivo `productos/templates/carrito.html`:

```html
<!-- productos/templates/carrito.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mi Carrito</title>
    <style>
      body {
        font-family: sans-serif;
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
      }
      h1 {
        color: #2c3e50;
      }
      li {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        list-style: none;
      }
      ul {
        padding: 0;
      }
    </style>
  </head>
  <body>
    <h1>🛒 Mi Carrito</h1>

    {% if productos %}
    <ul>
      {% for p in productos %}
      <li>{{ p.nombre }} — ${{ p.precio_final }}</li>
      {% endfor %}
    </ul>
    <h2>Total: ${{ total }}</h2>
    {% else %}
    <p>Tu carrito está vacío.</p>
    <a href="{% url 'lista_productos' %}">Ir al catálogo →</a>
    {% endif %}
  </body>
</html>
```

### 5.5 Configurar todas las URLs

Abre `productos/urls.py` y **reemplaza todo** su contenido por:

```python
# productos/urls.py
from django.urls import path
from .views import lista_productos, buscar_producto, agregar_al_carrito, ver_carrito

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('buscar/', buscar_producto, name='buscar_producto'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
]
```

### 5.6 Verificar

Ejecuta el servidor y prueba:

| URL                   | Qué debe pasar                                                 |
| --------------------- | -------------------------------------------------------------- |
| `/productos/`         | Lista de productos con descuentos y botón "Agregar al carrito" |
| `/productos/buscar/`  | Formulario de búsqueda funcional                               |
| `/productos/carrito/` | Lista de productos agregados con total                         |

---

## Paso 6 — Template Base y Navegación (Herencia de Templates)

Ahora que todo funciona, tenemos un problema: cada template repite `<!DOCTYPE>`, `<head>`, `<style>` y no hay forma de navegar entre páginas sin escribir las URLs manualmente. Vamos a resolver ambos problemas de un solo golpe.

### 6.1 Crear la carpeta global de templates

En la **raíz del proyecto** (al mismo nivel que `manage.py`), crea una carpeta `templates/`:

```bash
mkdir templates
```

### 6.2 Registrar la carpeta en `settings.py`

Abre `config/settings.py`, busca la variable `TEMPLATES` y agrega la ruta en `DIRS`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # ← agregar esta línea
        'APP_DIRS': True,
        # ...
    },
]
```

### 6.3 Crear `templates/base.html`

Este archivo concentrará **todo el CSS** y la **barra de navegación con buscador**. Crea `templates/base.html`:

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CatálogoApp{% endblock %}</title>
    <style>
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
    </style>
  </head>
  <body>
    <nav>
      <a href="{% url 'home' %}">🏠 Inicio</a>
      <a href="{% url 'lista_productos' %}">📦 Catálogo</a>
      <a href="{% url 'ver_carrito' %}">🛒 Carrito</a>

      <form action="{% url 'buscar_producto' %}" method="GET">
        <input type="text" name="q" placeholder="Buscar producto..." />
        <button type="submit">🔍</button>
      </form>
    </nav>

    <main>{% block content %}{% endblock %}</main>
  </body>
</html>
```

> 💡 **Todo el CSS del proyecto ahora vive en un solo lugar.** Si quieres cambiar un color o un tamaño de fuente, solo editas `base.html`.

### 6.4 Actualizar `core/templates/home.html`

Abre `core/templates/home.html` y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Inicio{% endblock %} {% block content
%}
<h1>🛒 Bienvenido al Catálogo</h1>
<p>Explora todos nuestros productos disponibles.</p>
<br />
<a class="btn" href="{% url 'lista_productos' %}">Ver catálogo →</a>
{% endblock %}
```

> 💡 Ya no hay `<!DOCTYPE>`, `<head>` ni `<style>`. Todo eso lo hereda de `base.html`.

### 6.5 Actualizar `productos/templates/lista_productos.html`

Abre el archivo y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Catálogo de Productos{% endblock %}
{% block content %}
<h1>🛒 Catálogo de Productos</h1>

{% if productos %}
<ul class="lista-productos">
  {% for p in productos %}
  <li>
    <strong>{{ p.nombre }}</strong>
    {% if not p.disponible %}
    <span class="no-disponible">(Sin stock)</span>
    {% endif %}
    <br />
    {% if p.descuento > 0 %}
    <del>${{ p.precio }}</del>
    <span class="descuento">{{ p.descuento }}% OFF</span><br />
    <span class="precio">${{ p.precio_final }}</span>
    <p class="ahorro">¡Ahorras ${{ p.ahorro_monto }}!</p>
    {% else %}
    <span class="precio">${{ p.precio }}</span>
    {% endif %}
    <br />
    <p>{{ p.descripcion }}</p>
    <a class="btn" href="{% url 'agregar_al_carrito' p.id %}"
      >🛒 Agregar al carrito</a
    >
  </li>
  {% endfor %}
</ul>
{% else %}
<p>No hay productos cargados todavía.</p>
{% endif %} {% endblock %}
```

> 💡 Los estilos como `style="color: red;"` fueron reemplazados por clases CSS (`class="descuento"`). Esas clases están definidas en `base.html`.

### 6.6 Actualizar `productos/templates/carrito.html`

Abre el archivo que creaste en el Paso 5.4 y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Mi Carrito{% endblock %} {% block
content %}
<h1>🛒 Mi Carrito</h1>

{% if productos %}
<ul class="lista-productos">
  {% for p in productos %}
  <li>{{ p.nombre }} — <span class="precio">${{ p.precio_final }}</span></li>
  {% endfor %}
</ul>
<h2>Total: ${{ total }}</h2>
{% else %}
<p>Tu carrito está vacío.</p>
<a class="btn" href="{% url 'lista_productos' %}">Ir al catálogo →</a>
{% endif %} {% endblock %}
```

### 6.7 Migrar la búsqueda a la navbar

En el Paso 5 creaste la búsqueda con un formulario POST en una página separada. Ahora que el buscador vive **directamente en la navbar** (el `<form>` que escribimos en `base.html`), vamos a simplificar la vista para que reciba la búsqueda por GET.

> 💡 **¿Por qué cambiamos de POST a GET?** Los buscadores usan GET porque el término aparece en la URL (ej: `/productos/buscar/?q=laptop`). Esto permite compartir el link de una búsqueda y usar el botón "Atrás" del navegador. POST se usa cuando se envían datos sensibles (contraseñas, pagos).

Abre `productos/views.py`, **busca** la función `buscar_producto` y **reemplázala** por:

```python
# Antes usaba POST y el Form. Ahora usa GET directamente desde la navbar.
def buscar_producto(request):
    query = request.GET.get('q', '')
    resultados = []

    if query:
        resultados = Producto.objects.filter(nombre__icontains=query)

    return render(request, 'buscar.html', {'resultados': resultados, 'query': query})
```

### 6.8 Actualizar `productos/templates/buscar.html`

Como el formulario ahora vive en la navbar, este template solo necesita mostrar los resultados. Abre `productos/templates/buscar.html` y **reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Resultados de Búsqueda{% endblock %}
{% block content %}
<h1>🔍 Resultados para "{{ query }}"</h1>

{% if resultados %}
<ul class="lista-productos">
  {% for p in resultados %}
  <li>
    <strong>{{ p.nombre }}</strong> —
    <span class="precio">${{ p.precio_final }}</span>
    <a class="btn" href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar</a>
  </li>
  {% endfor %}
</ul>
{% elif query %}
<p>No se encontraron productos con ese nombre.</p>
{% endif %}

<br />
<a href="{% url 'lista_productos' %}">← Volver al catálogo</a>
{% endblock %}
```

### 6.9 Verificar

Ejecuta el servidor (`python manage.py runserver`) y comprueba:

| Acción                                           | Qué debes ver                                              |
| ------------------------------------------------ | ---------------------------------------------------------- |
| Entrar a cualquier página                        | La **navbar** aparece en todas con los links y el buscador |
| Hacer clic en "📦 Catálogo"                      | Lista de productos con descuentos y botones de agregar     |
| Hacer clic en "🛒 Agregar al carrito"            | Vuelve al catálogo (el producto se guardó en la sesión)    |
| Hacer clic en "🛒 Carrito"                       | Muestra los productos agregados y el total                 |
| Escribir un nombre en el buscador y presionar 🔍 | Muestra solo los productos que coinciden                   |

---

## Entrega Final

Al terminar, tu proyecto debe tener:

1. Estructura de carpetas con `config/` en lugar del nombre duplicado.
2. Al menos 10 productos cargados con precios y descuentos variados.
3. Modelo `Producto` con métodos `precio_final()` y `ahorro_monto()`.
4. Carrito funcional que guarda productos en la sesión.
5. Buscador integrado en la barra de navegación.
6. Un **solo** `base.html` que contiene todo el CSS y la navbar, sin código repetido en ningún template.
