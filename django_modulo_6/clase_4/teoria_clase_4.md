# 🎨 Django — Módulo 6 · Clase 4

### Contenido Estático, Templates y Sistema de URLs

---

> _"Un sitio web sin diseño es como un libro sin portada: nadie lo quiere abrir."_

---

## Clase 4: qué vas a lograr hoy

Hoy vamos a darle **vida visual** a nuestro proyecto Django y a entender cómo se conectan las páginas entre sí.

- 🎨 Aprenderás qué son los **archivos estáticos** y cuáles existen.
- 📂 Verás **dónde se guardan**, cómo se organizan las carpetas y cómo se configuran.
- 🔗 Aprenderás a **incorporarlos en la template base** de tu proyecto.
- 🗺️ Entenderás cómo funciona el archivo **`urls.py`**: el GPS de todo proyecto Django.

> 🎯 Meta: que tu proyecto pase de "funciona" a "funciona **y se ve profesional**".

---

---

# PARTE 1: CONTENIDO ESTÁTICO EN DJANGO

---

## 1. ¿Qué es el contenido estático?

Cuando abres una página web bonita, ves colores, tipografías, imágenes, animaciones y botones interactivos. Todo eso **no sale de la base de datos**. Son archivos que viven guardados tal cual en el servidor y se envían al navegador **sin modificarse**.

> 🏠 **Analogía de la casa:**
> Imagina que tu proyecto Django es una **casa**.
>
> - El HTML es la **estructura**: paredes, pisos y techo.
> - Los archivos estáticos son la **decoración**: pintura, cuadros, luces y música de fondo.
> - Sin decoración, la casa "funciona"... pero nadie quiere vivir ahí.

### Definición simple

Un **archivo estático** es cualquier archivo que:

- ✅ Se envía al navegador **exactamente como está guardado**.
- ✅ Es **igual para todos los usuarios** (no depende de quién entre).
- ✅ **No se genera dinámicamente** (no viene de la base de datos).

---

## 2. ¿Cuáles son los tipos de archivos estáticos?

Existen **3 grandes familias** de archivos estáticos. Cada una cumple un rol diferente:

---

### 🎨 Tipo 1: CSS (Cascading Style Sheets — Hojas de Estilo)

**¿Qué hace?**
Define **cómo se ve** la página: colores, tamaños de letra, márgenes, fondos, bordes, posiciones de los elementos.

**Analogía:** Es la **pintura y el papel mural** de tu casa. Sin CSS, todo se ve como un documento de Word en blanco.

**Ejemplos de archivos CSS:**

- `base.css` → Estilos generales que aplican a todo el sitio.
- `productos.css` → Estilos específicos para la sección de productos.
- `formularios.css` → Estilos para que los formularios se vean profesionales.

**Ejemplo de qué hace un CSS:**

```css
/* Cambia el fondo de toda la página a gris claro */
body {
  background-color: #f5f5f5;
  font-family: "Arial", sans-serif;
}

/* Todos los botones se ven azules con texto blanco */
.btn-principal {
  background-color: #0d6efd;
  color: white;
  border-radius: 8px;
  padding: 10px 20px;
}
```

---

### ⚡ Tipo 2: JavaScript (JS)

**¿Qué hace?**
Agrega **comportamiento e interactividad** en el navegador del usuario. Todo lo que "se mueve" o "reacciona" sin recargar la página, lo hace JavaScript.

**Analogía:** Es la **electricidad** de la casa. Gracias a ella, los interruptores funcionan, las puertas automáticas se abren y las luces se encienden.

**Ejemplos de archivos JS:**

- `menu.js` → Abre y cierra el menú de navegación en celulares.
- `carrito.js` → Actualiza el contador del carrito sin recargar la página.
- `validar_formulario.js` → Verifica que el email tenga @ antes de enviarlo.

**Ejemplo de qué hace un JS:**

```javascript
// Cuando el usuario hace clic en el botón, muestra una alerta
document.getElementById("btn-comprar").addEventListener("click", function () {
  alert("¡Producto agregado al carrito!");
});
```

---

### 🖼️ Tipo 3: Imágenes, Íconos y Fuentes

**¿Qué hace?**
Son los **elementos visuales decorativos o informativos**: logos, banners, fotografías de productos, íconos de redes sociales, fuentes tipográficas personalizadas.

**Analogía:** Son los **cuadros, fotografías y adornos** que cuelgas en la pared de tu casa.

**Ejemplos de archivos:**

- `logo.png` → El logo de la empresa (aparece en el navbar).
- `banner_principal.jpg` → La imagen grande de la página de inicio.
- `favicon.ico` → El ícono pequeño que aparece en la pestaña del navegador.
- `icono-carrito.svg` → Ícono del carrito de compras.

---

### Resumen visual de los 3 tipos

| Tipo           | Rol                         | Analogía                        | Extensiones comunes            |
| -------------- | --------------------------- | ------------------------------- | ------------------------------ |
| **CSS**        | Define cómo se **ve**       | 🎨 Pintura y decoración         | `.css`                         |
| **JavaScript** | Define cómo se **comporta** | ⚡ Electricidad e interruptores | `.js`                          |
| **Imágenes**   | Elementos **visuales**      | 🖼️ Cuadros y fotografías        | `.png`, `.jpg`, `.svg`, `.ico` |

> 💡 _Estos archivos se llaman "estáticos" porque son siempre iguales. No importa si entra Juan o María: el logo será el mismo logo y el CSS aplicará el mismo diseño._

---

## 3. ¿Dónde se guardan? La organización de carpetas

### La regla de oro

En Django, los archivos estáticos se guardan en una carpeta llamada **`static/`** ubicada en la **raíz del proyecto** (al mismo nivel que `config/` y `templates/`).

Dentro de `static/`, los organizamos por tipo en **subcarpetas**:

```text
mi_proyecto/                    ← Raíz del proyecto
│
├── config/                     ← Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── mi_app/                     ← Tu aplicación (ej: productos)
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── templates/                  ← Todos los HTML
│   ├── base.html
│   └── productos/
│       ├── lista.html
│       └── detalle.html
│
├── static/                     ← 📦 TODOS LOS ESTÁTICOS VAN AQUÍ
│   │
│   ├── css/                    ← 🎨 Hojas de estilo
│   │   ├── base.css            ← Estilos globales del sitio
│   │   └── mi_app.css       ← Estilos solo para la sección productos
│   │
│   ├── js/                     ← ⚡ Archivos JavaScript
│   │   ├── menu.js             ← Lógica del menú hamburguesa
│   │   └── carrito.js          ← Lógica del carrito
│   │
│   └── images/                 ← 🖼️ Imágenes e íconos
│       ├── logo.png            ← Logo de la empresa
│       ├── banner.jpg          ← Imagen principal
│       └── favicon.ico         ← Ícono de la pestaña
│
├── manage.py
└── db.sqlite3
```

> 📐 **Buena práctica:** NUNCA mezcles archivos sueltos dentro de `static/`. Siempre usa subcarpetas (`css/`, `js/`, `images/`). Cuando tu proyecto crezca, lo agradecerás.

---

## 4. ¿Cómo se configuran? Las 3 llaves en `settings.py`

Django necesita **3 configuraciones** en el archivo `settings.py` para manejar los estáticos. Piensa en ellas como **3 llaves** que abren diferentes puertas:

---

### 🔑 Llave 1: `STATICFILES_DIRS` — "¿Dónde busco los estáticos?"

Le dice a Django: _"Mientras estoy en mi computadora desarrollando, mis archivos de diseño están guardados en esta carpeta."_

```python
# settings.py

STATICFILES_DIRS = [BASE_DIR / 'static']
```

**En palabras simples:**

- `BASE_DIR` = la carpeta raíz de tu proyecto.
- `/ 'static'` = dentro de esa raíz, busca la carpeta `static/`.
- Es como decirle a Django: _"La bodega de la decoración está en el primer piso, puerta azul."_

---

### 🔑 Llave 2: `STATIC_URL` — "¿Con qué dirección web los muestro?"

El navegador del usuario **no puede entrar** a las carpetas internas de tu servidor. Django crea una **dirección web pública** para que el navegador pueda pedir los archivos.

```python
# settings.py

STATIC_URL = '/static/'
```

**En palabras simples:**
Cuando el navegador necesite el archivo `base.css`, lo pedirá así:

```text
https://tusitio.com /static/ css/base.css
                    ^^^^^^^^
                    Esta parte la define STATIC_URL
```

Es como el **mostrador público** de una tienda: el cliente no entra a la bodega, le pides las cosas al mostrador y te las traen.

---

### 🔑 Llave 3: `STATIC_ROOT` — "¿Dónde empaco todo para producción?"

Cuando tu proyecto esté listo para subir a internet real, Django necesita juntar TODOS los estáticos (los tuyos, los del panel admin y los de cualquier librería externa) en una sola carpeta optimizada.

```python
# settings.py

STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**¿Cuándo se activa?**
Solo cuando ejecutas este comando de producción:

```bash
python manage.py collectstatic
```

> ⏳ **No te preocupes por esto ahora.** En esta etapa del curso trabajamos en desarrollo local. `STATIC_ROOT` lo usaremos cuando aprendamos a desplegar en un servidor real.

---

### Resumen de las 3 llaves

```text
┌──────────────────────────────────────────────────────────────┐
│                      settings.py                             │
│                                                              │
│  STATICFILES_DIRS → "Busca mis estáticos AQUÍ"    (local)    │
│  STATIC_URL       → "Muéstralos con esta RUTA"    (web)      │
│  STATIC_ROOT      → "Empácalos AQUÍ para subir"   (prod)     │
└──────────────────────────────────────────────────────────────┘
```

> _"Configurar bien desde el inicio es la diferencia entre un proyecto que crece ordenado y uno que explota a los 3 meses."_

---

---

# PARTE 2: INCORPORANDO ESTÁTICOS EN LA TEMPLATE BASE

---

## 5. ¿Qué es `base.html`? La plantilla madre del proyecto

Imagina que tienes 20 páginas en tu sitio web. TODAS necesitan el mismo navbar, el mismo `<head>` y el mismo footer. Si copias y pegas esas líneas en cada archivo HTML por separado y un día quieres cambiar el logo del navbar... tendrías que editarlo en **20 archivos distintos**. 😱

La solución fue crear un **template padre** (`base.html`) con toda la estructura común, y que cada página hija solo rellene las partes que cambian.

### Recordatorio de cómo funciona la herencia

```text
base.html (PADRE)
├── <head> con CSS y estilos         ← Se hereda a TODAS las páginas
├── <nav> con el menú               ← Se hereda a TODAS las páginas
├── {% block content %} VACÍO       ← Cada página hija lo rellena
└── <footer>                        ← Se hereda a TODAS las páginas

inicio.html (HIJA)
└── {% block content %}
    └── "¡Bienvenido a la tienda!"  ← Solo define SU contenido
```

> 🧩 **Analogía:** `base.html` es un **molde de torta**. Los `{% block %}` son los huecos para el relleno. Cada página hija elige su propio relleno sin tocar la forma de la torta.

---

## 6. Conectando los estáticos con `base.html`

Ahora que entendemos qué son los estáticos y dónde viven, vamos a **conectarlos con nuestro template base**. De este modo, TODAS las páginas hijas heredarán automáticamente el diseño.

### Paso 1: Pedir la llave — `{% load static %}`

En la **primera línea** de `base.html` (antes de `<!DOCTYPE html>`), escribimos:

```html
{% load static %}
```

**¿Qué hace?**
Le dice a Django: _"¡Voy a usar archivos de diseño! Activa el sistema para que puedas generar las rutas correctas."_

⚠️ Sin esta línea, las etiquetas `{% static %}` no funcionarán y tu página aparecerá sin estilos ni imágenes.

---

### Paso 2: Usar la etiqueta `{% static 'ruta' %}`

En lugar de escribir la ruta del archivo a mano, usamos la etiqueta especial de Django:

```html
<!-- ❌ MAL — ruta escrita a mano (se rompe al cambiar de servidor) -->
<link rel="stylesheet" href="/static/css/base.css" />

<!-- ✅ BIEN — Django genera la ruta correcta automáticamente -->
<link rel="stylesheet" href="{% static 'css/base.css' %}" />
```

> 🧠 _Regla mental:_ **Nunca escribas rutas de archivos estáticos a mano.** Siempre usa `{% static %}` y deja que Django las construya por ti.

---

### Paso 3: El `base.html` completo con archivos estáticos

Así queda un `base.html` profesional que integra **nuestros propios archivos estáticos** (CSS, JS, imágenes):

```html
{% load static %}
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- Título dinámico: cada página hija lo puede cambiar -->
    <title>{% block title %}Mi App{% endblock %}</title>

    <!-- Nuestro CSS personalizado (usa {% static %}) -->
    <link rel="stylesheet" href="{% static 'css/base.css' %}" />

    <!-- Favicon -->
    <link
      rel="icon"
      href="{% static 'images/favicon.ico' %}"
      type="image/x-icon"
    />
  </head>
  <body>
    <!-- Navbar compartida (TODAS las páginas la heredan) -->
    <nav class="navbar navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img src="{% static 'images/logo.png' %}" alt="Logo" height="30" />
          Mi Tienda
        </a>
      </div>
    </nav>

    <!-- Bloque de contenido: cada página hija rellena este espacio -->
    <main class="container mt-4">{% block content %} {% endblock %}</main>

    <!-- Footer compartido -->
    <footer class="text-center mt-5 py-3 bg-light">
      <p>© 2026 Mi Tienda · Todos los derechos reservados</p>
    </footer>

    <!-- Nuestro JS personalizado -->
    <script src="{% static 'js/menu.js' %}"></script>
  </body>
</html>
```

---

### Y una página hija que hereda todo

```html
{% extends "base.html" %} {% block title %}Página de Inicio{% endblock %} {%
block content %}
<h1>¡Bienvenido a nuestra tienda!</h1>
<p>Explora nuestro catálogo de productos.</p>
{% endblock %}
```

**¿Qué ocurre aquí?**

1. `{% extends "base.html" %}` → _"Soy hija de base.html, heredé todo: CSS, navbar, footer."_
2. `{% block title %}` → _"Cambio el título de la pestaña a 'Página de Inicio'."_
3. `{% block content %}` → _"Inyecto MI contenido donde el padre dejó el bloque vacío."_

La página hija **no necesita** repetir ni el `<head>`, ni el `{% load static %}`, ni el navbar, ni nada. Todo viene heredado del padre.

> 🎉 **Resultado:** escribe el diseño UNA vez en `base.html` y todas tus páginas se ven profesionales automáticamente.

---

### Nota: también puedes usar librerías externas como Bootstrap

Además de tus archivos estáticos personalizados, existen librerías de CSS/JS como **Bootstrap** que puedes cargar desde un CDN (sin descargar nada) para obtener diseño responsivo rápidamente. Esto se hace agregando un `<link>` adicional en el `<head>` del `base.html`. Lo veremos en la práctica más adelante.

---

### Contenido Dinámico: datos que cambian

Además de los estáticos (que son iguales para todos), los templates pueden mostrar **datos que vienen de la vista**.

La vista prepara un **Contexto** (un diccionario de Python) y lo manda al template:

**En la vista (`views.py`):**

```python
def inicio_view(request):
    contexto = {
        'usuario': 'Juan',
        'total_productos': 42,
    }
    return render(request, 'inicio.html', contexto)
```

**En el template:**

```html
<h1>¡Hola, {{ usuario }}!</h1>
<p>Tenemos {{ total_productos }} productos esperándote.</p>
```

**El navegador muestra:**

```text
¡Hola, Juan!
Tenemos 42 productos esperándote.
```

> 🔁 `{{ usuario }}` es un **espacio en blanco** que Django rellena justo antes de enviar la página. Si mañana entra María, verá "¡Hola, María!".

---

> _"Cada herramienta que aprendes hoy te acerca más a construir lo que imaginas. ¡No pares!"_

---

---

# PARTE 3: EL ARCHIVO `urls.py` — EL GPS DE DJANGO

---

## 7. ¿Qué es el archivo `urls.py`?

Cuando escribes una dirección en el navegador (por ejemplo `misitio.com/productos/`), esa dirección viaja por internet hasta llegar al servidor de Django. Ahí, algo tiene que decidir: **¿qué página muestro?**

Ese "algo" es el archivo **`urls.py`**. Es el **mapa de rutas** de tu proyecto.

> 🏢 **Analogía del Recepcionista:**
> Imagina un edificio de oficinas.
>
> - Llega una persona y dice: _"Vengo a la oficina de Productos."_
> - El recepcionista (`urls.py`) mira su lista de oficinas registradas.
> - Encuentra "Productos → Piso 3, Oficina B" y dirige a la persona.
> - Si la oficina no existe, el recepcionista dice: **"Error 404: no encontrada"**.

---

## 8. ¿Cómo está organizado el sistema de URLs?

En un proyecto Django con buena arquitectura, existen **dos niveles** de `urls.py`:

### Nivel 1: El recepcionista principal — `config/urls.py`

Este archivo vive en la carpeta de configuración. Su trabajo es **delegar** las solicitudes a la app correcta.

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),          # Panel de administración
    path('productos/', include('productos.urls')),       # Todo lo demás → app productos
]
```

**¿Qué hace `include()`?**
Le dice al recepcionista principal: _"Si la dirección empieza con vacío (la raíz), NO la resuelvas tú. Pásasela al recepcionista de la app productos."_

---

### Nivel 2: El recepcionista de la app — `productos/urls.py`

Este archivo vive dentro de la carpeta de tu app. Se encarga de las rutas **específicas** de esa funcionalidad.

```python
# productos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('contacto/', views.contacto_view, name='contacto'),
]
```

---

### El viaje completo de una URL

```text
Usuario escribe: misitio.com/catalogo/
        │
        ▼
┌──────────────────────────┐
│    config/urls.py        │  ← Recepcionista PRINCIPAL
│    "¿Quién se encarga?"  │
│    → include('productos')│
└───────────┬──────────────┘
            ▼
┌──────────────────────────┐
│   productos/urls.py      │  ← Recepcionista de la APP
│   "¿Es /catalogo/?"     │
│   ¡Sí! → catalogo_view  │
└───────────┬──────────────┘
            ▼
┌──────────────────────────┐
│      views.py            │  ← La oficina encargada
│   Consulta la BD         │
│   Prepara contexto       │
│   Renderiza template     │
└───────────┬──────────────┘
            ▼
┌──────────────────────────┐
│    template.html         │  ← La página final
│   HTML + datos + diseño  │
└───────────┬──────────────┘
            ▼
     Navegador del usuario
     (ve la página bonita) 🎉
```

---

## 9. Anatomía de una ruta: ¿qué significa cada parte?

Cada línea dentro de `urlpatterns` tiene **3 partes**:

```python
path('contacto/', views.contacto_view, name='contacto')
#     ▲               ▲                      ▲
#     │               │                      │
#  LA RUTA       LA VISTA              EL APODO
```

| Parte                 | ¿Qué es?                                            | Ejemplo               |
| --------------------- | --------------------------------------------------- | --------------------- |
| **La Ruta**           | Lo que el usuario escribe en la barra del navegador | `'contacto/'`         |
| **La Vista**          | La función de Python que se ejecutará               | `views.contacto_view` |
| **El Apodo** (`name`) | Un nombre interno para referirse a esta ruta        | `name='contacto'`     |

---

## 10. Tipos de URLs en Django

### Tipo 1: URLs Estáticas (Rutas Fijas)

Son las más simples. La dirección debe coincidir **exactamente** con lo que está programado. Siempre apuntan al mismo destino.

**¿Cuándo se usan?**
Para páginas que no dependen de ningún dato variable: Inicio, Nosotros, Contacto, Términos y Condiciones.

```python
urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('terminos/', views.terminos_view, name='terminos'),
]
```

**Funcionamiento:**

```text
misitio.com/             → ejecuta inicio_view
misitio.com/contacto/    → ejecuta contacto_view
misitio.com/nosotros/    → ejecuta nosotros_view
misitio.com/xyz/         → ERROR 404 (no existe en la lista)
```

---

### Tipo 2: URLs Dinámicas (Con captura de datos)

¿Qué pasa si tienes 10,000 productos en tu tienda? No puedes crear una ruta fija para cada uno (`producto/1/`, `producto/2/`... `producto/10000/`).

Para esto existen las **URLs dinámicas**: rutas que **atrapan** una parte de la dirección y se la envían a la vista como variable.

> 🎣 **Analogía:** La URL dinámica es una **red de pesca**. El `<int:producto_id>` atrapa el número de la dirección y se lo entrega a la vista.

**Código:**

```python
urlpatterns = [
    # Atrapa un NÚMERO ENTERO y lo llama 'producto_id'
    path('producto/<int:producto_id>/', views.detalle_view, name='detalle'),
]
```

**Funcionamiento:**

```text
misitio.com/producto/1/     → detalle_view recibe producto_id = 1
misitio.com/producto/42/    → detalle_view recibe producto_id = 42
misitio.com/producto/999/   → detalle_view recibe producto_id = 999
```

**¿Cómo llega el valor a la vista?**

```python
def detalle_view(request, producto_id):
    #                       ▲
    #     Este parámetro viene de la URL
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'detalle.html', {'producto': producto})
```

---

### Los convertidores de tipo: qué puede "atrapar" una URL

| Convertidor     | Qué atrapa                            | Ejemplo de URL         | Valor capturado   |
| --------------- | ------------------------------------- | ---------------------- | ----------------- |
| `<int:id>`      | Un número entero                      | `/producto/42/`        | `42`              |
| `<str:nombre>`  | Una cadena de texto                   | `/usuario/maria/`      | `"maria"`         |
| `<slug:titulo>` | Texto amigable (minúsculas + guiones) | `/blog/que-es-django/` | `"que-es-django"` |

**Ejemplos con cada tipo:**

```python
urlpatterns = [
    # Atrapa un número entero
    path('producto/<int:producto_id>/', views.detalle_view, name='detalle'),

    # Atrapa texto libre
    path('usuario/<str:nombre_usuario>/', views.perfil_view, name='perfil'),

    # Atrapa un slug (texto-amigable-para-url)
    path('blog/<slug:titulo_articulo>/', views.articulo_view, name='articulo'),
]
```

---

### El atributo `name`: apodos inteligentes (MUY IMPORTANTE)

En todas las rutas aparece `name='algo'`. Esto parece un detalle menor, pero es una de las **mejores prácticas más importantes** de Django.

**El problema SIN `name`:**

```html
<!-- Ruta escrita a mano en el template -->
<a href="/producto/5/">Ver Producto</a>
```

Si mañana decides cambiar la ruta de `/producto/` a `/articulo/`, tendrías que buscar y editar **cada link** en **cada archivo HTML** de todo el proyecto. 😱

**La solución CON `name`:**

```html
<!-- Django genera la ruta automáticamente usando el apodo -->
<a href="{% url 'detalle' producto_id=5 %}">Ver Producto</a>
```

Si cambias la ruta en `urls.py`, Django actualiza **automáticamente** todos los links que usen ese `name`. Cero ediciones manuales. ✅

> 🏷️ **Piensa en `name` como una etiqueta adhesiva.** No importa si mueves la caja de lugar: mientras la etiqueta diga "Producto", Django siempre sabrá encontrarla.

---

### ¿Cómo se usa `{% url %}` en los templates?

```html
<!-- Link a una ruta ESTÁTICA (sin parámetros) -->
<a href="{% url 'contacto' %}">Ir a Contacto</a>

<!-- Link a una ruta DINÁMICA (con parámetro entero) -->
<a href="{% url 'detalle' producto_id=42 %}">Ver Producto 42</a>

<!-- Link a una ruta DINÁMICA (con parámetro texto) -->
<a href="{% url 'perfil' nombre_usuario='maria' %}">Ver Perfil de María</a>
```

---

## 11. El viaje completo: de la URL a la pantalla (ejemplo real)

```text
1. 👤 El usuario escribe: misitio.com/producto/42/

2. 📋 config/urls.py revisa:
   "¿Alguien se encarga de esto?"
   → Sí, include('productos.urls')

3. 📋 productos/urls.py revisa:
   "¿Tengo algo como /producto/<int>/ ?"
   → ¡Sí! Atrapa el 42 y llama a detalle_view

4. ⚙️ views.py ejecuta:
   detalle_view(request, producto_id=42)
   → Busca en BD: Producto con id=42
   → Encuentra: "Televisor 50 pulgadas" · $299.990
   → Prepara contexto y renderiza template

5. 📄 template.html muestra:
   {{ producto.nombre }} → "Televisor 50 pulgadas"
   {{ producto.precio }} → "$299.990"
   Con diseño responsivo

6. 🎉 El navegador muestra la página lista
```

---

> _"No memorices código. Entiende el flujo. Cuando entiendas cómo viaja la información, podrás construir cualquier cosa."_

---

## 📋 Tabla resumen de toda la clase

| Concepto                 | ¿Qué hace?                           | Archivo clave    |
| ------------------------ | ------------------------------------ | ---------------- |
| Archivos estáticos       | CSS, JS, imágenes que no cambian     | `static/`        |
| `STATICFILES_DIRS`       | Dónde buscar estáticos en desarrollo | `settings.py`    |
| `STATIC_URL`             | Dirección pública para el navegador  | `settings.py`    |
| `STATIC_ROOT`            | Empaquetado para producción          | `settings.py`    |
| `{% load static %}`      | Activa la maquinaria de estáticos    | Template         |
| `{% static 'ruta' %}`    | Genera la URL del archivo estático   | Template         |
| Librerías externas (CDN) | Diseño responsivo con frameworks     | `<head>`         |
| `base.html`              | Template padre (estructura común)    | `templates/`     |
| `{% extends %}`          | Herencia de templates                | Template hijo    |
| `{% block %}`            | Bloques rellenables                  | Padre e hijo     |
| `{{ variable }}`         | Contenido dinámico desde la vista    | Template         |
| `config/urls.py`         | Recepcionista principal del proyecto | `config/`        |
| `app/urls.py`            | Recepcionista específico de la app   | App              |
| `path()`                 | Define una ruta URL                  | `urls.py`        |
| `include()`              | Delega rutas a otra app              | `config/urls.py` |
| `<int:id>`               | Captura dinámica (número)            | `urls.py`        |
| `<str:texto>`            | Captura dinámica (texto)             | `urls.py`        |
| `<slug:slug>`            | Captura dinámica (texto amigable)    | `urls.py`        |
| `name='...'`             | Apodo inteligente para una ruta      | `urls.py`        |
| `{% url 'name' %}`       | Genera link usando el apodo          | Template         |

---

> 🚀 _"Hoy aprendiste a vestir tu proyecto y a darle un mapa de rutas. Cada clase suma una capa de profesionalismo. ¡Sigue construyendo!"_
