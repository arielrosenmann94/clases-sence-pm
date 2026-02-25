# 🐍 Django — Módulo 6 · Clase 2

### Teoría: Anatomía del proyecto, configuración y arquitectura de código

---

# El código que escribiste hoy es mejor que el que escribiste ayer. Eso es suficiente.

---

## Dónde estamos

En la **Clase 1** construimos el proyecto desde cero y comprendimos la arquitectura MVT (Modelo, Vista, Template, URLs), el ORM, las migraciones y el panel de administración.

En esta clase vamos adentro del proyecto que Django generó: **¿qué es cada archivo que se creó solo?** ¿Por qué existe? ¿Qué se puede y qué no se debe tocar?

---

## 1. Los archivos que Django genera al crear un proyecto

Cuando se ejecuta `django-admin startproject catalogoapp`, Django crea esta estructura:

```text
catalogoapp/              ← carpeta raíz
├── manage.py             ← consola de gestión del proyecto
└── catalogoapp/          ← carpeta de configuración
    ├── __init__.py       ← marca la carpeta como paquete Python
    ├── settings.py       ← configuración central del proyecto
    ├── urls.py           ← enrutador raíz (mapa de todas las URLs)
    ├── wsgi.py           ← protocolo de servidor sincrónico (legacy)
    └── asgi.py           ← protocolo de servidor asíncrono (moderno)
```

Cada archivo tiene una responsabilidad específica.

---

### 1.1 El archivo `apps.py` (Identidad de la aplicación)

A diferencia de los archivos que vimos arriba (que son globales del proyecto), el archivo `apps.py` vive dentro de cada aplicación (como `productos/`). Contiene una clase de configuración que Django usa para registrar la aplicación.

```python
# productos/apps.py
from django.apps import AppConfig

class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productos'
```

#### `AppConfig`

Esta clase es el "DNI" de la aplicación. Le indica a Django cómo se llama el módulo y qué tipo de clave primaria usar por defecto en sus modelos. No se suele modificar a menudo, pero es vital porque es lo que Django busca cuando agregamos la app a `INSTALLED_APPS`.

---

> [!IMPORTANT]
>
> ### 🛑 No confundir: Carpeta "config" vs. Clase "AppConfig"
>
> Es muy común confundir estos términos porque ambos usan la palabra "config":
>
> 1.  **Carpeta `config/` (Proyecto):** Es el **contenedor global**. Es una carpeta física que creamos para guardar `settings.py`. Es la arquitectura del sitio.
> 2.  **Clase `AppConfig` (Aplicación):** Es un **objeto Python**. Vive dentro de `apps.py` de cada app. Es la configuración interna de ese módulo específico.
>
> **Regla nemotécnica:** La carpeta `config` es la caja que guarda todo el proyecto. La clase `AppConfig` es la etiqueta que tiene cada pieza adentro de la caja.

---

### 1.2 `manage.py`

Herramienta de línea de comandos que permite ejecutar tareas del proyecto Django. Es el punto de entrada para todos los comandos del framework. No contiene código del proyecto; actúa como un intermediario entre la terminal y Django.

```bash
python manage.py runserver      # inicia el servidor de desarrollo
python manage.py makemigrations # detecta cambios en los modelos
python manage.py migrate        # aplica migraciones a la BD
python manage.py createsuperuser
python manage.py shell          # abre consola Python con Django cargado
```

> ⚠️ Este archivo no debe modificarse. Existe uno por proyecto.

---

### `__init__.py`

Archivo vacío que le indica a Python que la carpeta `catalogoapp/` debe tratarse como un **paquete** (un módulo importable). Sin este archivo, Python no puede importar nada desde esa carpeta. Django lo genera automáticamente y no necesita ser editado.

```python
# __init__.py está vacío (esto es intencional y correcto)
```

---

### `wsgi.py` — Web Server Gateway Interface

Archivo de entrada del servidor para el modo **sincrónico** (el modo tradicional de Django). WSGI es el estándar de comunicación entre un servidor web (nginx, Apache) y la aplicación Python para proyectos que no necesitan características asíncronas.

```python
# wsgi.py — no modificar salvo para configurar despliegue
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogoapp.settings')
application = get_wsgi_application()
```

> 💡 Se usa en producción con servidores como **Gunicorn** o **uWSGI**. En desarrollo, `manage.py runserver` lo usa internamente de forma automática.

---

### `asgi.py` — Asynchronous Server Gateway Interface

Archivo de entrada del servidor para el modo **asíncrono**. ASGI es el estándar moderno que reemplaza a WSGI cuando el proyecto necesita WebSockets, HTTP/2 o conexiones persistentes en tiempo real.

```python
# asgi.py — puerta de entrada del servidor asíncrono
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogoapp.settings')
application = get_asgi_application()
```

#### ¿Cuándo se usa ASGI en lugar de WSGI?

| Tipo de proyecto                | Protocolo recomendado |
| ------------------------------- | --------------------- |
| Sitio web tradicional (HTTP)    | WSGI                  |
| Chat en tiempo real             | **ASGI**              |
| Notificaciones push / WebSocket | **ASGI**              |
| API REST convencional           | WSGI                  |
| Streaming de datos en vivo      | **ASGI**              |

Django adoptó ASGI en la versión 3.0 (2019). Esto fue el primer paso hacia la programación asíncrona nativa que llegó a completarse con el `AsyncPaginator` de Django 6.0.

> 💡 En la mayoría de los proyectos de este curso se usa WSGI. ASGI se activa explícitamente cuando se necesitan funciones asíncronas avanzadas.

---

### `urls.py` del proyecto (el enrutador raíz)

Es el **punto de entrada de todas las URLs** del proyecto. Cuando Django recibe una solicitud, este archivo es lo primero que consulta. En proyectos con varias apps, este archivo delega a los `urls.py` de cada app usando `include()`.

```python
# catalogoapp/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),  # delega a la app productos
]
```

> 💡 Este archivo fue el punto en el que se enlazó la app `productos` al proyecto en la Clase 1.

---

## 2. El archivo `settings.py` — Sección por sección

`settings.py` es el **centro nervioso** del proyecto. Controla desde el motor de base de datos hasta los parámetros de seguridad. Conocerlo en detalle es indispensable para cualquier desarrollador Django.

---

### 2.1 Configuraciones fundamentales

#### `SECRET_KEY`

Clave criptográfica que Django usa para firmar cookies, tokens CSRF y sesiones. Funciona como la "llave maestra" del proyecto. Si alguien la obtiene, puede falsificar sesiones y tokens. Nunca debe compartirse ni subirse a un repositorio público.

```python
SECRET_KEY = 'django-insecure-xxxxxxxxxxxx'
```

---

#### `DEBUG`

Controla si Django muestra información detallada del error cuando algo falla. En desarrollo es conveniente tenerlo activo para ver los errores. En producción **siempre debe estar en `False`** para no exponer código fuente al público.

```python
DEBUG = True   # desarrollo
DEBUG = False  # producción (obligatorio)
```

> ⚠️ Publicar un proyecto en producción con `DEBUG = True` expone el código fuente, las rutas internas y el contenido de `settings.py` a cualquier visitante que provoque un error HTTP 500.

---

#### `ALLOWED_HOSTS`

Lista de dominios o direcciones IP desde los que el proyecto acepta solicitudes HTTP. Cuando `DEBUG = False`, Django rechaza cualquier solicitud que provenga de un dominio no incluido en esta lista. Protege contra ataques de host spoofing.

```python
ALLOWED_HOSTS = []                                       # desarrollo
ALLOWED_HOSTS = ['midominio.com', 'www.midominio.com']  # producción
```

---

### 2.2 Aplicaciones instaladas (`INSTALLED_APPS`)

Lista de todas las aplicaciones que Django reconoce. Sin registrar una app, Django no puede encontrar sus modelos, migraciones ni templates. Cada vez que se crea una app con `startapp`, hay que agregarla aquí.

```python
INSTALLED_APPS = [
    'django.contrib.admin',       # panel de administración
    'django.contrib.auth',        # autenticación de usuarios
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # gestión de sesiones
    'django.contrib.messages',
    'django.contrib.staticfiles', # archivos estáticos
    # apps propias:
    'productos',
]
```

---

### 2.3 Base de datos (`DATABASES`)

Indica qué motor de base de datos y qué credenciales usar. El mismo código Python funciona con distintos motores; solo cambia esta sección para pasar de SQLite a PostgreSQL sin modificar ningún modelo.

#### SQLite — solo para desarrollo

Archivo de base de datos guardado en disco. No requiere instalar nada extra. No es apto para producción porque no soporta múltiples usuarios simultáneos de forma robusta.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL — recomendado para producción

Motor relacional robusto, open source y oficialmente recomendado por el equipo de Django para entornos de producción.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_base_de_datos',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### 2.4 Idioma y zona horaria

#### `LANGUAGE_CODE`

Define el idioma de la interfaz del panel de administración y los mensajes de error del sistema. El código `'es'` activa el español neutro. No afecta el idioma del contenido de la aplicación, solo el del framework.

```python
LANGUAGE_CODE = 'es'      # español neutro
LANGUAGE_CODE = 'en-us'   # inglés americano (por defecto)
```

---

#### `TIME_ZONE`

Define la zona horaria del servidor. Django almacena todas las fechas en UTC internamente y las convierte al timezone local al mostrarlas. Permite que el mismo proyecto funcione correctamente en cualquier región.

```python
TIME_ZONE = 'America/Santiago'
TIME_ZONE = 'America/Bogota'
TIME_ZONE = 'America/Mexico_City'
```

---

#### `USE_TZ`

Habilita el soporte de zona horaria. Cuando está activo, todos los objetos `datetime` del proyecto contienen información de zona horaria, evitando errores al comparar fechas creadas en distintos momentos o regiones. Siempre debe estar en `True`.

```python
USE_TZ = True  # siempre True
```

---

### 2.5 Archivos estáticos

Django distingue dos tipos de archivos no dinámicos:

#### `STATIC_URL` y `STATICFILES_DIRS`

Los **archivos estáticos** son los recursos del diseño del sitio: CSS, JavaScript e imágenes que son parte del código. `STATIC_URL` es la dirección desde la que el navegador los solicita. `STATICFILES_DIRS` indica dónde buscarlos en el servidor durante el desarrollo.

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

#### `MEDIA_URL` y `MEDIA_ROOT`

Los **archivos de medios** son los archivos subidos por los usuarios: fotos de perfil, documentos adjuntos, imágenes de productos. A diferencia de los estáticos, estos se generan dinámicamente y no forman parte del código del proyecto.

```python
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 2.6 Configuraciones de seguridad

Estas configuraciones no están activas por defecto porque requieren HTTPS activo en el servidor. Es fundamental conocerlas antes de publicar cualquier proyecto en producción.

> ⚠️ Este grupo de configuraciones **solo funciona correctamente con HTTPS** activo. En desarrollo local se mantienen en `False` o desactivadas.

---

#### `SESSION_COOKIE_SECURE`

Obliga a que la cookie de sesión del usuario solo se transmita por HTTPS. Sin esta protección, la cookie puede ser interceptada en redes no seguras (Wi-Fi público). Si se activa sin HTTPS, el usuario no podrá iniciar sesión.

```python
SESSION_COOKIE_SECURE = False  # desarrollo
SESSION_COOKIE_SECURE = True   # producción (con HTTPS)
```

---

#### `CSRF_COOKIE_SECURE`

Obliga a que la cookie CSRF, que protege contra solicitudes falsificadas entre sitios, se transmita únicamente por HTTPS. Trabaja en conjunto con `SESSION_COOKIE_SECURE` para garantizar que todo el intercambio de seguridad sea cifrado.

```python
CSRF_COOKIE_SECURE = False  # desarrollo
CSRF_COOKIE_SECURE = True   # producción (con HTTPS)
```

---

#### `SESSION_COOKIE_HTTPONLY`

Impide que el código JavaScript del navegador lea la cookie de sesión. Sin esta protección, un script malicioso inyectado en la página podría robar la cookie y suplantar al usuario autenticado (ataque XSS seguido de robo de sesión).

```python
SESSION_COOKIE_HTTPONLY = True  # siempre True
```

---

#### `X_FRAME_OPTIONS`

Controla si el sitio puede ser embebido en un `<iframe>` de otro dominio. Protege contra ataques de Clickjacking, donde un atacante superpone el sitio legítimo en un iframe invisible y engaña al usuario para que haga clic en algo sin saberlo.

```python
X_FRAME_OPTIONS = 'SAMEORIGIN'  # iframes solo desde el mismo dominio
X_FRAME_OPTIONS = 'DENY'        # nunca en iframes (máxima protección)
```

---

#### `SECURE_SSL_REDIRECT`

Redirige automáticamente todas las solicitudes HTTP al equivalente HTTPS. Garantiza que ningún usuario acceda al sitio por HTTP plano (sin cifrado), incluso si escribe la dirección manualmente sin el `https://`.

```python
SECURE_SSL_REDIRECT = False  # desarrollo
SECURE_SSL_REDIRECT = True   # producción (con HTTPS configurado)
```

---

#### `SECURE_HSTS_SECONDS`

Activa el encabezado HTTP Strict Transport Security (HSTS). Le indica al navegador que durante el período definido siempre use HTTPS para este dominio, incluso si el usuario escribe `http://` manualmente. Es el nivel más alto de protección de transporte.

```python
SECURE_HSTS_SECONDS = 0          # desactivado (desarrollo)
SECURE_HSTS_SECONDS = 31536000   # 1 año (producción, con HTTPS activo)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

---

#### Tabla resumen: desarrollo vs. producción

| Configuración             | Desarrollo     | Producción              |
| ------------------------- | -------------- | ----------------------- |
| `DEBUG`                   | `True`         | **`False`**             |
| `ALLOWED_HOSTS`           | `[]`           | **`['midominio.com']`** |
| `SESSION_COOKIE_SECURE`   | `False`        | **`True`**              |
| `CSRF_COOKIE_SECURE`      | `False`        | **`True`**              |
| `SESSION_COOKIE_HTTPONLY` | `True`         | `True`                  |
| `X_FRAME_OPTIONS`         | `'SAMEORIGIN'` | `'SAMEORIGIN'`          |
| `SECURE_SSL_REDIRECT`     | `False`        | **`True`**              |
| `SECURE_HSTS_SECONDS`     | `0`            | **`31536000`**          |

---

## 3. Arquitectura de un proyecto que crece — Estructura de carpetas profesional

A medida que el proyecto crece y se agregan más apps, la carpeta raíz puede volverse difícil de leer. La comunidad Django ha consolidado un patrón de organización que separa claramente la configuración de los módulos de negocio.

### La estructura por defecto

```text
catalogoapp/
├── manage.py
└── catalogoapp/          ← ¡mismo nombre que la carpeta raíz!
    ├── settings.py
    └── urls.py
```

Genera confusión al crecer el proyecto porque dos carpetas comparten el nombre.

### La estructura profesional — patrón `config`

```text
catalogoapp/              ← carpeta raíz (repositorio Git)
├── manage.py
├── config/               ← ⚙️ configuración global del proyecto
│   ├── settings.py
│   └── urls.py
├── core/                 ← páginas genéricas (home, about...)
├── productos/            ← módulo de negocio: catálogo
└── usuarios/             ← módulo de negocio: cuentas
```

La convención recomendada es crear el proyecto con:

```bash
django-admin startproject config .
```

Esto posiciona la carpeta de configuración con un nombre que describe su función, no el nombre del negocio.

| Criterio                   | Por defecto                  | Con `config/`            |
| -------------------------- | ---------------------------- | ------------------------ |
| Claridad visual            | Confusa (nombres duplicados) | Clara                    |
| Escalabilidad              | Mínimos proyectos            | Proyectos en crecimiento |
| Convención de la comunidad | Documentación oficial        | Proyectos reales         |

---

## 4. Principio arquitectónico — Modelos robustos, vistas delgadas

La documentación oficial de Django establece que los modelos deben _"incluir toda la lógica relevante del dominio"_ (principio **Include all relevant domain logic**). En la práctica, esto significa que **la lógica de negocio vive en el modelo, no en la vista**.

### El problema — vista sobrecargada

Una vista que hace demasiadas cosas es difícil de leer, de mantener y de reutilizar. Esto ocurre cuando la lógica se acumula directamente en `views.py`:

```python
# ❌ Vista sobrecargada — hace demasiado
def procesar_pedido(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if producto.stock <= 0 or not producto.activo:
        return HttpResponse('Sin stock')
    precio = producto.precio * Decimal('1.19')
    producto.stock -= 1
    producto.save()
    Pedido.objects.create(usuario=request.user, producto=producto, precio=precio)
    return redirect('gracias')
```

**Problemas:** si el cálculo de impuestos cambia, hay que buscarlo en `views.py`. Si otra vista necesita el mismo cálculo, el código se duplica.

### La solución — modelo robusto, vista delgada

```python
# ✅ Modelo con lógica propia — cada método hace una sola cosa
class Producto(models.Model):

    def tiene_stock(self):
        """Verifica si el producto está disponible."""
        return self.stock > 0 and self.activo

    def precio_con_impuestos(self):
        """Calcula el precio final con IVA incluido."""
        return self.precio * Decimal('1.19')

    def registrar_pedido(self, usuario):
        """Descuenta stock y crea el registro del pedido."""
        self.stock -= 1
        self.save()
        Pedido.objects.create(
            usuario=usuario,
            producto=self,
            precio=self.precio_con_impuestos()
        )
```

```python
# ✅ Vista limpia — le indica al modelo qué hacer
def procesar_pedido(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if not producto.tiene_stock():
        return HttpResponse('Sin stock')
    producto.registrar_pedido(request.user)
    return redirect('gracias')
```

**Ventajas:** la vista tiene 4 líneas. Si el IVA cambia, se edita un solo método en el modelo. Cualquier otra vista puede reutilizar `registrar_pedido()` sin duplicar código.

---

## 5. Diseño de apps — Responsabilidad única

Cada app de Django debe tener un propósito claro y delimitado. Es la misma idea del principio de responsabilidad única (SRP) aplicada al framework.

**Señales de que una app tiene demasiadas responsabilidades:**

- Su nombre es genérico (`main`, `general`, `utils`).
- Su `models.py` tiene más de 10 clases que no se relacionan entre sí.
- Su `views.py` mezcla lógica de ventas, usuarios y notificaciones.

**Ejemplos de diseño correcto:**

| App        | Qué gestiona                             |
| ---------- | ---------------------------------------- |
| `core`     | Páginas genéricas (home, about, contact) |
| `usuarios` | Registro, login, perfil                  |
| `catalogo` | Productos, categorías, búsqueda          |
| `carrito`  | Lógica del carrito de compras            |
| `pagos`    | Procesamiento de transacciones           |

---

## 6. Introducción a los Formularios de Django (Forms)

### ¿Qué es un formulario web?

Un formulario web es el mecanismo a través del cual un usuario envía datos al servidor. Ejemplos cotidianos: un formulario de registro, un campo de búsqueda, un formulario de contacto o un campo para publicar un comentario.

En HTML plano, un formulario se ve así:

```html
<form method="POST" action="/buscar/">
  <input type="text" name="nombre" />
  <input type="number" name="precio" />
  <button type="submit">Enviar</button>
</form>
```

Cuando el usuario presiona "Enviar", el navegador envía todos los valores al servidor mediante una solicitud POST. El servidor los recibe y debe procesarlos.

---

### El problema del formulario HTML básico

El HTML genera el campo y lo envía, pero **no valida nada**. Un usuario malintencionado puede:

- Dejar el campo `precio` vacío y romper la aplicación.
- Escribir texto donde se espera un número.
- Enviar datos con caracteres especiales que alteren la base de datos.
- Modificar el HTML con las herramientas del navegador y enviar valores que no debería poder enviar.

**El servidor nunca debe confiar en lo que llega del navegador.**

---

### ¿Qué hace un Form de Django?

Un **Form de Django** es una clase Python que describe qué campos tiene el formulario y qué reglas de validación aplica a cada uno. Django genera automáticamente el HTML del formulario y también valida los datos cuando llegan del usuario.

```
HTML plano                   Form de Django
─────────────────────────    ─────────────────────────────────
Dibuja los campos      ✅    Dibuja los campos             ✅
Envía los datos        ✅    Envía los datos               ✅
Valida en el servidor  ❌    Valida en el servidor         ✅
Muestra errores        ❌    Muestra errores automáticos   ✅
Limpia los datos       ❌    Limpia los datos              ✅
```

---

### Primer Form de Django — ejemplo básico

El caso más simple: un formulario para buscar un producto por nombre.

#### Paso 1 — Crear el formulario en `forms.py`

Cada app puede tener su propio archivo `forms.py`. Este archivo no lo genera Django automáticamente; hay que crearlo a mano.

```python
# productos/forms.py
from django import forms

class BusquedaForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre del producto',   # texto que aparece en la etiqueta
        max_length=100,                # longitud máxima permitida
        required=True                  # campo obligatorio
    )
```

#### Paso 2 — Usar el formulario en la vista

```python
# productos/views.py
from django.shortcuts import render
from .forms import BusquedaForm
from .models import Producto

def buscar_producto(request):
    resultados = []

    if request.method == 'POST':
        form = BusquedaForm(request.POST)   # carga los datos enviados
        if form.is_valid():                  # Django valida los campos
            nombre = form.cleaned_data['nombre']   # dato limpio y seguro
            resultados = Producto.objects.filter(nombre__icontains=nombre)
            #SELECT * FROM producto WHERE nombre LIKE '%nombre%';
    else:
        form = BusquedaForm()    # formulario vacío para mostrar al usuario

    return render(request, 'buscar.html', {'form': form, 'resultados': resultados})
```

#### `form.is_valid()`

Método que ejecuta todas las validaciones definidas en el Form. Si todos los campos pasan la validación, devuelve `True` y los datos validados quedan disponibles en `form.cleaned_data`. Si alguna validación falla, devuelve `False` y el Form guarda los mensajes de error correspondientes.

#### `form.cleaned_data`

Diccionario que contiene los datos del formulario ya **validados y limpiados**. Solo está disponible después de que `is_valid()` devuelve `True`. Los valores están convertidos al tipo Python correcto (un campo `IntegerField` entrega un `int`, un `DateField` entrega un `date`, etc.).

#### Paso 3 — Mostrar el formulario en el template

```html
<!-- productos/templates/buscar.html -->
<form method="POST">
  {% csrf_token %} {{ form.as_p }}
  <button type="submit">Buscar</button>
</form>

{% if resultados %}
<ul>
  {% for producto in resultados %}
  <li>{{ producto.nombre }} — ${{ producto.precio }}</li>
  {% endfor %}
</ul>
{% endif %}
```

#### `{% csrf_token %}`

Etiqueta de template obligatoria en todos los formularios que usan el método POST. Inserta un token de seguridad oculto que Django verifica al recibir la solicitud. Sin este token, Django rechaza el formulario con un error 403. Esta es la protección CSRF que se vio en la Clase 1.

#### `{{ form.as_p }}`

Renderiza todos los campos del formulario envueltos en etiquetas `<p>`. Django genera automáticamente el HTML de cada campo con su etiqueta y, si hay errores de validación, los muestra también. Existen otras variantes: `{{ form.as_table }}` y `{{ form.as_ul }}`.

---

### Tipos de campos disponibles en un Form

| Campo          | Tipo de dato esperado  | Validación automática         |
| -------------- | ---------------------- | ----------------------------- |
| `CharField`    | Texto                  | Longitud máxima, `required`   |
| `IntegerField` | Número entero          | Que sea un número, mín/máx    |
| `DecimalField` | Número decimal         | Precisión, mín/máx            |
| `EmailField`   | Correo electrónico     | Formato de email válido       |
| `BooleanField` | Verdadero/Falso        | Checkbox marcado              |
| `DateField`    | Fecha                  | Formato de fecha válido       |
| `ChoiceField`  | Selección de una lista | Que el valor esté en la lista |

---

## 7. Herencia de Templates — El sistema DRY de Django

### El problema: código HTML repetido

Hasta ahora, cada template del proyecto (`home.html`, `lista_productos.html`, `buscar.html`, `carrito.html`) tiene su propia estructura HTML completa: `<!DOCTYPE>`, `<head>`, estilos, `<body>`. Si se necesita cambiar el nombre del sitio o agregar un menú de navegación, hay que editar **todos** los archivos uno por uno.

Esto viola el principio **DRY** (Don't Repeat Yourself — No te repitas), uno de los pilares de Django.

---

### La solución: `{% extends %}` y `{% block %}`

Django permite crear un **template base** que contiene la estructura común (el HTML, el `<head>`, la navbar, el footer), y definir **bloques vacíos** que cada página hijo rellena con su propio contenido.

```
base.html (padre)
├── HTML, head, navbar, footer  ← se escribe UNA sola vez
├── {% block title %}           ← espacio reservado para el título
└── {% block content %}         ← espacio reservado para el contenido

lista_productos.html (hijo)
├── {% extends "base.html" %}   ← hereda todo del padre
├── {% block title %} Catálogo  ← rellena solo el título
└── {% block content %} ...     ← rellena solo el contenido
```

---

### Cómo funciona `{% extends %}`

La etiqueta `{% extends "base.html" %}` **debe ser la primera línea** del template hijo. Le dice a Django: _"No generes tu propio HTML. Usa todo lo que tiene `base.html` y solo reemplaza los bloques que yo defina."_

```html
<!-- lista_productos.html -->
{% extends "base.html" %} {% block title %}Catálogo{% endblock %} {% block
content %}
<h1>🛒 Catálogo de Productos</h1>
<!-- ... contenido específico de esta página ... -->
{% endblock %}
```

---

### Cómo funciona `{% block %}`

Un bloque es un **espacio con nombre** que el padre define y el hijo puede rellenar. Si el hijo no define un bloque, se usa el contenido por defecto del padre (si lo tiene).

```html
<!-- En base.html (padre) -->
{% block title %}Mi Sitio{% endblock %}
<!-- Si el hijo no define 'title', se muestra "Mi Sitio" -->
```

---

### El template `base.html` — Ejemplo completo

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CatálogoApp{% endblock %}</title>
  </head>
  <body>
    <nav>
      <a href="{% url 'home' %}">🏠 Inicio</a>
      <a href="{% url 'lista_productos' %}">📦 Catálogo</a>
      <a href="{% url 'ver_carrito' %}">� Carrito</a>

      <form
        action="{% url 'buscar_producto' %}"
        method="GET"
        style="margin-left: auto;"
      >
        <input type="text" name="q" placeholder="Buscar producto..." />
        <button type="submit">🔍</button>
      </form>
    </nav>

    <main>{% block content %}{% endblock %}</main>
  </body>
</html>
```

Observa que la navbar usa `{% url 'nombre' %}` en lugar de rutas fijas como `/productos/`. Esto garantiza que si las URLs cambian en `urls.py`, los links se actualizan automáticamente.

---

### Un template hijo que hereda

```html
<!-- productos/templates/lista_productos.html -->
{% extends "base.html" %} {% block title %}Catálogo de Productos{% endblock %}
{% block content %}
<h1>🛒 Catálogo de Productos</h1>
<ul>
  {% for p in productos %}
  <li>{{ p.nombre }} — ${{ p.precio_final }}</li>
  {% endfor %}
</ul>
{% endblock %}
```

Este archivo **no tiene** `<!DOCTYPE>`, `<head>`, ni `<nav>`. Todo eso lo hereda de `base.html`. Si mañana se necesita agregar un footer, se agrega una sola vez en `base.html` y todas las páginas lo muestran automáticamente.

---

### ¿Dónde se guarda `base.html`?

El template base se coloca en una carpeta `templates/` en la **raíz del proyecto** (no dentro de ninguna app), porque es compartido por todas las aplicaciones.

```text
catalogoapp/
├── config/
├── core/
├── productos/
└── templates/        ← carpeta global de templates
    └── base.html
```

Para que Django lo encuentre, hay que registrar esta carpeta en `settings.py`:

```python
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],   # ← agregar esta línea
        ...
    },
]
```

---

### Diagrama completo de herencia

```
templates/base.html          (estructura HTML + navbar + footer)
    │
    ├── core/templates/home.html              (solo el contenido de inicio)
    ├── productos/templates/lista_productos.html  (solo el catálogo)
    ├── productos/templates/buscar.html           (solo el buscador)
    └── productos/templates/carrito.html          (solo el carrito)
```

Cada página mantiene su identidad pero comparte la misma estructura visual. Un cambio en `base.html` se refleja instantáneamente en todas las páginas del sitio.

---

## 📚 Referencias

- 📖 [Django 6.0 — Documentación oficial](https://docs.djangoproject.com/en/6.0/)
- 📖 [Django Forms — Documentación oficial](https://docs.djangoproject.com/en/6.0/topics/forms/)
- 📖 [Django Templates — Herencia](https://docs.djangoproject.com/en/6.0/ref/templates/language/#template-inheritance)
- 📖 [Django Design Philosophies](https://docs.djangoproject.com/en/6.0/misc/design-philosophies/)
- 📖 [Django Security — Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
