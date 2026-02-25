# 🛠️ Django — Módulo 6 · Guía Práctica

### De cero a una app con Models, Views, URLs y Templates

> Este documento es la guía práctica de la clase. Seguí cada paso en orden y sin saltear ninguno.
> Antes de comenzar, asegúrate de tener **Python 3.12+** instalado en tu computadora.

---

## ¿Cómo verificar que Python está instalado?

```bash
# Linux / Mac
python3 --version

# Windows
python --version
```

Si ves algo como `Python 3.12.0`, estás listo. Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/).

---

## Paso 1 — Preparar el entorno de trabajo

### 1.1 Crear la carpeta del proyecto

```bash
# Linux / Mac
mkdir catalogoapp
cd catalogoapp

# Windows (PowerShell o CMD)
mkdir catalogoapp
cd catalogoapp
```

### 1.2 Crear el entorno virtual

El entorno virtual aísla las dependencias de este proyecto del resto del sistema.

```bash
# Linux / Mac
python3 -m venv venv

# Windows
python -m venv venv
```

Esto genera una carpeta llamada `venv/` dentro de tu proyecto.

### 1.3 Activar el entorno virtual

```bash
# Linux / Mac
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat
```

✅ **¿Cómo sé que está activo?**
Al activarlo, verás el prefijo `(venv)` al inicio de la línea en la terminal:

```
(venv) usuario@maquina:~/catalogoapp$
```

> ⚠️ Si cerrás la terminal y volvés, tienes que activar el entorno de nuevo. El prefijo `(venv)` debe estar siempre visible cuando trabajás en el proyecto.

### 1.4 Instalar Django

```bash
# Linux / Mac / Windows (con el entorno activo)
pip install django
```

### 1.5 Verificar la instalación

```bash
# Linux / Mac / Windows
python -m django --version
```

Deberías ver algo como `6.0.1` o similar.

---

## Paso 2 — Crear el proyecto Django

Un **proyecto** Django es el contenedor principal. Cuando creás un proyecto se generan los archivos de configuración global.

```bash
# Linux / Mac / Windows
# El punto al final crea el proyecto en la carpeta actual (sin subcarpeta extra)
django-admin startproject catalogoapp .
```

> 💡 **¿Por qué el punto al final?** Sin el punto, Django crea una subcarpeta `catalogoapp/catalogoapp/`, lo que puede generar confusión. Con el punto, el proyecto queda organizado directamente en la carpeta donde estás.

### Estructura generada

```
catalogoapp/              ← tu carpeta de trabajo
├── venv/                 ← entorno virtual (no tocar)
├── manage.py             ← herramienta de comandos del proyecto
└── catalogoapp/          ← configuración del proyecto
    ├── __init__.py
    ├── settings.py       ← configuración global
    ├── urls.py           ← rutas principales
    ├── wsgi.py
    └── asgi.py
```

### Verificar que el proyecto funciona

```bash
# Linux / Mac / Windows
python manage.py runserver
```

Abre el navegador en `http://127.0.0.1:8000/`. Deberías ver la pantalla de bienvenida de Django 🎉

Para detener el servidor: `Ctrl + C`

---

## Paso 3 — Crear la aplicación

En Django, un **proyecto** puede tener múltiples **apps**. Cada app es un módulo independiente con su propia lógica. Vamos a crear una app llamada `productos`.

```bash
# Linux / Mac / Windows (con el servidor detenido)
python manage.py startapp productos
```

### Estructura generada

```
catalogoapp/
├── manage.py
├── catalogoapp/
│   └── (archivos del proyecto)
└── productos/               ← nuestra nueva app
    ├── migrations/          ← carpeta donde van los archivos de migración
    │   └── __init__.py
    ├── __init__.py
    ├── admin.py             ← registro de modelos en el panel admin
    ├── apps.py              ← configuración de la app
    ├── models.py            ← definición de modelos (tablas)
    ├── tests.py             ← tests (no usamos en esta clase)
    └── views.py             ← funciones de vista (lógica)
```

> ⚠️ `urls.py` **NO se crea automáticamente** dentro de la app. Lo vamos a crear nosotros más adelante.

### Registrar la app en el proyecto

Abre `catalogoapp/settings.py` y busca la lista `INSTALLED_APPS`. Agrega `'productos'` al final:

```python
# catalogoapp/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productos',    # ← agregar esta línea
]
```

> ❗ Si no registrás la app, Django no puede encontrar sus modelos, templates ni migraciones.

---

## Paso 4 — Definir el modelo

Un **modelo** es una clase Python que define la estructura de una tabla en la base de datos.

Abre `productos/models.py` y **reemplazá** todo el contenido con:

```python
# productos/models.py
from django.db import models


class Producto(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    disponible  = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
```

### ¿Qué significa cada campo?

| Campo         | Tipo                                            | Descripción                                      |
| ------------- | ----------------------------------------------- | ------------------------------------------------ |
| `nombre`      | `CharField(max_length=100)`                     | Texto corto, máximo 100 caracteres               |
| `descripcion` | `TextField(blank=True)`                         | Texto largo, puede estar vacío                   |
| `precio`      | `DecimalField(max_digits=10, decimal_places=2)` | Número decimal (ej: 1999.99)                     |
| `disponible`  | `BooleanField(default=True)`                    | Verdadero o Falso, por defecto True              |
| `creado_en`   | `DateTimeField(auto_now_add=True)`              | Fecha y hora, se asigna automáticamente al crear |

El método `__str__` define qué texto se muestra cuando Django necesita representar el objeto como texto (por ejemplo, en el panel admin).

---

## Paso 5 — Crear y aplicar las migraciones

Las migraciones son archivos que le dicen a la base de datos cómo debe estructurarse.

### Paso 5.1 — Generar las migraciones

```bash
# Linux / Mac / Windows
python manage.py makemigrations
```

Deberías ver algo como:

```
Migrations for 'productos':
  productos/migrations/0001_initial.py
    - Create model Producto
```

Esto generó el archivo `productos/migrations/0001_initial.py`.

### Paso 5.2 — Aplicar las migraciones

```bash
# Linux / Mac / Windows
python manage.py migrate
```

Deberías ver una lista de migraciones aplicadas que termina con `OK`.

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, productos, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying productos.0001_initial... OK
```

✅ Ahora la tabla `productos_producto` existe en la base de datos.

> 💡 Cada vez que modifiques `models.py` (agregues un campo, cambies un tipo, etc.), tienes que repetir los pasos 5.1 y 5.2.

---

## Paso 6 — Configurar el panel de administración

El panel admin de Django permite gestionar los datos sin escribir una sola línea de HTML.

### Paso 6.1 — Registrar el modelo en admin.py

Abre `productos/admin.py` y **reemplazá** todo el contenido con:

```python
# productos/admin.py
from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'precio', 'disponible', 'creado_en')
    list_filter   = ('disponible',)
    search_fields = ('nombre', 'descripcion')
    ordering      = ('nombre',)
```

> 💡 `@admin.register(Producto)` es equivalente a `admin.site.register(Producto, ProductoAdmin)`. El decorador es la forma moderna y más limpia.

### Paso 6.2 — Crear el superusuario

```bash
# Linux / Mac / Windows
python manage.py createsuperuser
```

Django te hará tres preguntas:

```
Username: admin
Email address: admin@ejemplo.com
Password: (escribe una contraseña, no se muestra al tipear)
Password (again): (repetila)
Superuser created successfully.
```

### Paso 6.3 — Ingresar al admin y cargar datos

```bash
# Linux / Mac / Windows
python manage.py runserver
```

Abre `http://127.0.0.1:8000/admin/`, inicia sesión y carga 3 o 4 productos de ejemplo. Los vas a necesitar para probar la vista en el siguiente paso.

---

## Paso 7 — Crear la Vista

La **vista** es la función que recibe la solicitud del usuario, consulta los datos y decide qué mostrar.

Abre `productos/views.py` y **reemplazá** todo el contenido con:

```python
# productos/views.py
from django.shortcuts import render
from .models import Producto


def lista_productos(request):
    # Consultamos todos los productos de la base de datos
    productos = Producto.objects.all()

    # Pasamos los productos al template como contexto
    contexto = {
        'productos': productos,
    }

    return render(request, 'lista_productos.html', contexto)
```

### ¿Qué hace cada parte?

```python
from django.shortcuts import render
# Importa la función que convierte un template HTML en una respuesta HTTP

from .models import Producto
# El punto (.) significa "importar desde esta misma app"

def lista_productos(request):
# Define la función. Django siempre pasa "request" como primer argumento.
# "request" contiene toda la info de la solicitud (usuario, método HTTP, etc.)

    productos = Producto.objects.all()
# Consulta TODOS los registros de la tabla Producto
# Equivale a: SELECT * FROM productos_producto;

    contexto = {'productos': productos}
# El diccionario "contexto" es el puente entre la vista y el template.
# La clave 'productos' será la variable que usaremos en el HTML.

    return render(request, 'lista_productos.html', contexto)
# render() une el template con los datos y devuelve el HTML final
```

---

## Paso 8 — Configurar las URLs

Las URLs le dicen a Django qué vista llamar cuando el usuario visita una dirección. Hay **dos archivos** que debemos configurar.

### Paso 8.1 — Crear urls.py dentro de la app

Este archivo **no existe todavía**. Tienes que crearlo a mano.

Dentro de la carpeta `productos/`, crea un nuevo archivo llamado **`urls.py`**:

```python
# productos/urls.py   ← ARCHIVO NUEVO (crearlo desde cero)
from django.urls import path
from .views import lista_productos

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
]
```

### Explicación del `path()`

```python
path('', lista_productos, name='lista_productos')
#     ↑        ↑                    ↑
#     │        │                    └── nombre interno para referenciar esta URL
#     │        └── función vista a ejecutar
#     └── fragmento de ruta RELATIVO (vacío porque el prefijo lo pone el proyecto)
```

El primer argumento `''` está vacío porque la URL completa `/productos/` la define el `urls.py` del proyecto. La app solo define lo que viene **después** de ese prefijo.

### Paso 8.2 — Conectar la app con el `urls.py` del proyecto principal

Ahora viene la parte más importante: Django, por defecto, **no sabe que nuestra app `productos` tiene rutas**. El proyecto solo mira su propio archivo principal.

Imaginalo como un **conmutador telefónico de una empresa**: llama un cliente al número principal (el proyecto) y la recepcionista tiene que transferir la llamada a la oficina de "Productos" (la app). La función `include()` es esa transferencia.

Abre **`catalogoapp/urls.py`** (el archivo que ya existía desde el principio) y **reemplazá** todo su contenido con:

```python
# catalogoapp/urls.py   ← ARCHIVO PRINCIPAL DEL PROYECTO
from django.contrib import admin
from django.urls import path, include   # ¡NO OLVIDES AGREGAR `include` AQUÍ!

urlpatterns = [
    # Esta ruta ya venía por defecto
    path('admin/', admin.site.urls),

    # Esta es la línea clave que agregamos nosotros:
    path('productos/', include('productos.urls')),
    #     ↑                       ↑
    #     │                       └── "Busca las rutas específicas dentro del archivo productos/urls.py"
    #     └── "Cuando alguien escriba tupagina.com/productos/..."
]
```

#### ¿Por qué lo hacemos así en dos pasos?

Django te obliga a ser ordenado. No ponemos todas las rutas juntas en el archivo principal porque si tuvieras 10 apps (usuarios, productos, ventas, blog, etc.) tendrías un archivo gigante y caótico de 500 líneas.

**Así funciona el viaje de la URL:**

```
1️⃣ El usuario escribe en su navegador:
   http://127.0.0.1:8000/productos/

2️⃣ El conserje del edificio (catalogoapp/urls.py) recibe la URL:
   "Ah, veo que la ruta empieza con /productos/"
   "Tengo instrucciones de mandar todo eso a la oficina productos.urls"
   → (Recorta la palabra 'productos/' de la ruta y pasa lo que sobra)

3️⃣ La oficina (productos/urls.py) recibe lo que sobró:
   En este caso, recibe '' (nada, una URL vacía).
   "Ah, tengo una ruta para la URL vacía: path('', lista_productos)"
   "¡A ejecutar la vista lista_productos!"
```

Este sistema modular te permite que si mañana quieres cambiar la dirección a `mis-ofertas/` en vez de `productos/`, **solo cambiás una línea** en el proyecto principal y todas las rutas de la app interna siguen funcionando mágicamente.

---

## Paso 9 — Crear el Template (HTML dinámico)

El **template** es el archivo HTML que recibe los datos de la vista y los muestra al usuario.

### Paso 9.1 — Crear la carpeta de templates

```bash
# Linux / Mac
mkdir -p productos/templates

# Windows (PowerShell o CMD)
mkdir productos\templates
```

### Paso 9.2 — Crear el archivo HTML

Dentro de `productos/templates/`, crea el archivo **`lista_productos.html`**:

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
        <strong>{{ p.nombre }}</strong>
        {% if not p.disponible %}
        <span class="no-disponible">(Sin stock)</span>
        {% endif %}
        <br />
        <span class="precio">${{ p.precio }}</span>
        <p>{{ p.descripcion }}</p>
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

### Glosario de la sintaxis DTL usada

| Elemento                    | ¿Qué hace?                                                       |
| --------------------------- | ---------------------------------------------------------------- |
| `{% if productos %}`        | Condicional: se ejecuta si la variable `productos` no está vacía |
| `{% for p in productos %}`  | Itera sobre cada elemento de la lista `productos`                |
| `{{ p.nombre }}`            | Muestra el valor del atributo `nombre` del objeto `p`            |
| `{% if not p.disponible %}` | Condicional negado: se ejecuta si `disponible` es `False`        |
| `{% endif %}`               | Cierra un bloque `if`                                            |
| `{% endfor %}`              | Cierra un bloque `for`                                           |

---

## Paso 10 — Verificar la estructura completa

Antes de correr el servidor, verifica que la estructura del proyecto esté así:

```
catalogoapp/
├── venv/
├── manage.py
├── catalogoapp/
│   ├── settings.py        ← 'productos' en INSTALLED_APPS
│   └── urls.py            ← incluye productos.urls
└── productos/
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/
    │   └── lista_productos.html    ← archivo HTML
    ├── admin.py           ← @admin.register(Producto)
    ├── models.py          ← class Producto
    ├── urls.py            ← path('', lista_productos)  ← CREADO A MANO
    └── views.py           ← def lista_productos(request)
```

### Checklist final antes de correr

- [ ] `venv` está activo (ves el prefijo `(venv)` en la terminal)
- [ ] `'productos'` está en `INSTALLED_APPS` en `settings.py`
- [ ] `productos/models.py` tiene la clase `Producto`
- [ ] Se corrió `makemigrations` y `migrate` sin errores
- [ ] `productos/admin.py` tiene `@admin.register(Producto)`
- [ ] Se creó el superusuario con `createsuperuser`
- [ ] Se cargaron algunos productos desde el admin
- [ ] `productos/views.py` tiene la función `lista_productos`
- [ ] `productos/urls.py` existe y apunta a `lista_productos`
- [ ] `catalogoapp/urls.py` incluye `'productos.urls'`
- [ ] `productos/templates/lista_productos.html` existe

---

## Paso 11 — Correr el servidor y probar

```bash
# Linux / Mac / Windows
python manage.py runserver
```

Abre las siguientes URLs en el navegador:

| URL                                | Qué debe mostrar                            |
| ---------------------------------- | ------------------------------------------- |
| `http://127.0.0.1:8000/`           | Error 404 (normal, no hay vista en la raíz) |
| `http://127.0.0.1:8000/admin/`     | Panel de administración                     |
| `http://127.0.0.1:8000/productos/` | Lista de productos ✅                       |

Si ves la lista de productos que cargaste desde el admin, **¡todo está funcionando correctamente!** 🎉

---

## Errores comunes y cómo resolverlos

| Error                                                                      | Causa probable                                            | Solución                                                        |
| -------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'django'`                            | El entorno virtual no está activo                         | Activá el venv (`source venv/bin/activate`)                     |
| `TemplateDoesNotExist: lista_productos.html`                               | El archivo HTML no existe o está en la carpeta incorrecta | Verifica que esté en `productos/templates/lista_productos.html` |
| `OperationalError: no such table: productos_producto`                      | No corriste `migrate`                                     | Corre `python manage.py migrate`                                |
| `Page not found (404)` en `/productos/`                                    | La URL no está configurada correctamente                  | Verifica `catalogoapp/urls.py` y `productos/urls.py`            |
| `ImportError: cannot import name 'lista_productos' from 'productos.views'` | La función no existe o tiene un nombre diferente          | Verifica `views.py`                                             |
| `django.core.exceptions.ImproperlyConfigured`                              | La app no está en `INSTALLED_APPS`                        | Agrega `'productos'` a `settings.py`                            |

---

## Resumen del flujo completo

```
1. Entorno virtual activo  →  pip install django
2. django-admin startproject catalogoapp .
3. python manage.py startapp productos
4. Agregar 'productos' a INSTALLED_APPS en settings.py
5. Definir class Producto en models.py
6. python manage.py makemigrations + migrate
7. Registrar Producto en admin.py
8. python manage.py createsuperuser
9. Iniciar servidor → cargar datos desde /admin/
10. Escribir función lista_productos(request) en views.py
11. Crear productos/urls.py con path('', lista_productos)
12. Conectar en catalogoapp/urls.py con include('productos.urls')
13. Crear productos/templates/lista_productos.html
14. python manage.py runserver → visitar /productos/
```

---

> 💬 **¿Algún paso no funcionó?** Revisa la tabla de errores comunes o consultá al docente. La mayoría de los problemas son por el orden de los pasos o por algún archivo en la carpeta incorrecta.

---

## 🏠 Paso 12 (Opcional) — Crear una Home personalizada

> ⚠️ **Nota sobre la pantalla de bienvenida de Django:** La pantalla del cohete 🚀 que muestra "The install worked successfully!" **desaparece en cuanto definís la primera URL** en `urlpatterns`. Es una pantalla de diagnóstico, no una página de inicio real. Una vez que empezás a configurar rutas, ya no se puede recuperar. Lo que necesitás a partir de ahora es crear tu propia pantalla de inicio.

---

### ¿Dónde conviene crear la home? — Decisión de arquitectura

La pantalla de inicio (`/`) no pertenece a ninguna app en particular (no es de `productos`, no es de `usuarios`). Es una página del **sitio en general**.

Por eso, la buena práctica (recomendada por _Two Scoops of Django_) es crear una app dedicada exclusivamente a páginas genéricas del sitio, comúnmente llamada **`core`** o **`pages`**:

```text
catalogoapp/
├── core/          ← 🏠 pages genéricas (home, about, contact...)
├── productos/     ← 📦 lógica de productos
└── usuarios/      ← 👤 lógica de usuarios
```

Así, si mañana la home cambia radicalmente (pasa de "lista de productos" a "página de marketing"), no tocás ni una sola línea de la app `productos`.

> ❗ **¿`core` es un renombre de la carpeta `catalogoapp/catalogoapp/`?**
> **No.** La carpeta `catalogoapp/catalogoapp/` (la que tiene `settings.py` y el `urls.py` global) **no se toca aquí**. Lo que hacemos es crear una **app Django completamente nueva** con `startapp core`, igual que hiciste con `startapp productos`.
>
> Renombrar esa carpeta interna a `config/` es una convención de proyectos profesionales que se hace **únicamente al inicio** de un proyecto vacío. En este tutorial no la aplicamos para no complicar el flujo.

---

### Paso 12.1 — Crear la app `core`

```bash
python manage.py startapp core
```

Registrala en `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'productos',
    'core',      # ← agregar
]
```

### Paso 12.2 — Crear la vista de inicio

Abre `core/views.py` y escribe:

```python
# core/views.py
from django.shortcuts import render


def home(request):
    """Vista de la página de inicio del sitio."""
    return render(request, 'home.html')
```

### Paso 12.3 — Crear el template de la home

Crea la carpeta de templates de la app `core`:

```bash
# Linux / Mac
mkdir -p core/templates

# Windows
mkdir core\templates
```

Dentro de `core/templates/`, crea `home.html`:

```html
<!-- core/templates/home.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Catálogo — Inicio</title>
    <style>
      body {
        font-family: sans-serif;
        text-align: center;
        padding: 60px 20px;
      }
      h1 {
        font-size: 2.5rem;
        color: #2c3e50;
      }
      p {
        color: #555;
        font-size: 1.1rem;
      }
      a {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 32px;
        background: #2ecc71;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-size: 1rem;
      }
      a:hover {
        background: #27ae60;
      }
    </style>
  </head>
  <body>
    <h1>🛒 Bienvenido al Catálogo</h1>
    <p>Explorá todos nuestros productos disponibles.</p>
    <a href="/productos/">Ver catálogo →</a>
  </body>
</html>
```

### Paso 12.4 — Crear `urls.py` de la app `core`

Este archivo **no existe todavía**. Crealo a mano dentro de la carpeta `core/`:

```python
# core/urls.py   ← ARCHIVO NUEVO
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

### Paso 12.5 — Conectar en el proyecto principal

Abre `catalogoapp/urls.py` y agrega la ruta de `core`:

```python
# catalogoapp/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('', include('core.urls')),   # ← la home en la raíz '/'
]
```

> 💡 La ruta de la home va con el prefijo `''` (vacío) porque queremos que responda exactamente en `http://127.0.0.1:8000/`.

### Resultado final

Ahora tienes tres URLs funcionales:

| URL                                | Qué muestra                                 |
| ---------------------------------- | ------------------------------------------- |
| `http://127.0.0.1:8000/`           | 🏠 Home personalizada con botón al catálogo |
| `http://127.0.0.1:8000/productos/` | 📦 Lista de productos                       |
| `http://127.0.0.1:8000/admin/`     | ⚙️ Panel de administración                  |

### Estructura final del proyecto

```
catalogoapp/
├── manage.py
├── catalogoapp/
│   ├── settings.py      ← 'productos' y 'core' en INSTALLED_APPS
│   └── urls.py          ← incluye core.urls y productos.urls
├── core/                ← 🆕 app de páginas genéricas
│   ├── views.py         ← def home(request)
│   ├── urls.py          ← path('', home)
│   └── templates/
│       └── home.html    ← página de inicio
└── productos/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        └── lista_productos.html
```
