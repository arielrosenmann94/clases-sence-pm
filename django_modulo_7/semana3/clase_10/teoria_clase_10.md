# 🏗️ Módulo 7 — Clase 10

## CRUD en Django — Parte I

> **AE 7.6** — Implementar una aplicación web MVC que realiza operaciones CRUD en la base de datos utilizando los componentes del framework Django para dar solución a un problema.

---

## 🗺️ Índice

| #      | Tema                                                 |
| :----- | :--------------------------------------------------- |
| **1**  | Recap: Conexión con lo anterior                      |
| **2**  | Proyecto vs. Aplicación en Django                    |
| **3**  | Inicialización del Proyecto y la Aplicación          |
| **4**  | Registro de la Aplicación en `settings.py`           |
| **5**  | Definición del Modelo con el ORM                     |
| **6**  | Creación de la Base de Datos: Migraciones            |
| **7**  | Vistas Basadas en Clases para CRUD                   |
| **8**  | CSRF y Formularios Seguros                           |
| **9**  | Enrutamiento y Configuración de URLs                 |
| **10** | Operaciones CRUD con el ORM                          |
| **11** | Integración en el Patrón MTV (Modelo-Template-Vista) |
| **12** | Demo: Creación del Proyecto CRUD desde Cero          |

---

---

# 📚 1. Recap: Conexión con lo Anterior

---

En las clases anteriores trabajamos con herramientas avanzadas de consulta del ORM. Hoy damos un giro: pasamos de **consultar datos** a **construir aplicaciones completas** que permiten crear, leer, actualizar y eliminar registros desde el navegador.

| Clase anterior                            | Esta clase                                        |
| :---------------------------------------- | :------------------------------------------------ |
| Consultas con `raw()` y cursores          | Crear vistas que **escriben** en la base de datos |
| Parámetros seguros contra inyección SQL   | Formularios protegidos con token CSRF             |
| `select_related()` y `prefetch_related()` | Vistas genéricas que **automatizan** el CRUD      |
| Procedimientos almacenados                | Proyecto Django completo desde cero               |

> 💡 Todo lo que aprendimos sobre consultas **sigue vigente**. Las vistas CRUD usan el ORM por debajo — solo que ahora lo conectamos con formularios HTML y URLs.

---

---

# 🏠 2. Proyecto vs. Aplicación en Django

---

Antes de escribir una sola línea de código, hay que entender la diferencia entre estas dos piezas fundamentales:

```
PROYECTO                                APLICACIÓN (APP)
────────────────────                    ────────────────────
Es la "ciudad entera"                   Es un "edificio" dentro de la ciudad
Uno solo por sitio web                  Puede haber muchos dentro del proyecto
Contiene la configuración global        Contiene modelos, vistas, templates
settings.py, urls.py, wsgi.py          models.py, views.py, urls.py
Se crea con django-admin startproject   Se crea con python manage.py startapp
```

### ¿Por qué separar en aplicaciones?

```
┌────────────────────────────────────────────────────────┐
│  PROYECTO: sistema_ventas                              │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ clientes │  │ productos│  │  ventas  │              │
│  │  (app)   │  │  (app)   │  │  (app)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
│                                                        │
│  Cada app maneja UNA funcionalidad.                    │
│  Se pueden reutilizar en otros proyectos.              │
│  El código queda organizado y mantenible.              │
└────────────────────────────────────────────────────────┘
```

### La Analogía del Hospital

```
HOSPITAL (Proyecto)                      DJANGO (Proyecto)
─────────────────────                    ─────────────────────
El hospital como institución             El proyecto como un todo
Tiene una dirección general (config)     Tiene settings.py (configuración)
Tiene varios departamentos               Tiene varias apps

Departamento de Urgencias = una app      App "clientes"
Departamento de Pediatría = otra app     App "productos"
Departamento de Cirugía  = otra app      App "ventas"

Cada departamento tiene:                 Cada app tiene:
  - Su propio equipo                       - Sus propios modelos
  - Sus propios procedimientos             - Sus propias vistas
  - Sus propios registros                  - Sus propios templates
  - Pero comparten el hospital             - Pero comparten el proyecto
```

> 📚 **Fuente:** Django Software Foundation. (2024). _Django overview_. https://docs.djangoproject.com/en/stable/intro/overview/

---

---

# 🚀 3. Inicialización del Proyecto y la Aplicación

---

## Paso 1: Crear el proyecto

```bash
# Crear el proyecto principal
django-admin startproject mi_proyecto_crud

# Entrar al directorio del proyecto
cd mi_proyecto_crud
```

Esto genera la siguiente estructura:

```
mi_proyecto_crud/
├── manage.py                  ← Herramienta de línea de comandos
└── mi_proyecto_crud/          ← Carpeta de configuración
    ├── __init__.py
    ├── settings.py            ← Configuración del proyecto
    ├── urls.py                ← Rutas principales
    ├── asgi.py
    └── wsgi.py
└── templates/                 ← Plantillas HTML
    └── base.html
    └── clientes
        └── base_cliente.html
        └── cliente_list.html
    └── otra_app
        └── base_otra_app.html
└── static/                    ← Archivos estáticos de la app
    └── css/
    └── js/
    └── img/

```

## Paso 2: Crear la aplicación

```bash
# Crear la app "clientes" dentro del proyecto
python manage.py startapp clientes
```

Esto genera:

```
clientes/
├── __init__.py
├── admin.py                   ← Registro de modelos en el panel admin
├── apps.py                    ← Configuración de la app
├── migrations/                ← Carpeta para migraciones
│   └── __init__.py
├── models.py                  ← Definición de modelos (ORM)
├── tests.py                   ← Tests
└── views.py                   ← Lógica de las vistas
└── templates/                 ← Plantillas HTML
    └── clientes/
        └── base_cliente.html
        └── cliente_list.html
└── static/
    └── clientes/           ← Archivos estáticos de la app
        └── css/
            └── style.css
        └── js/
        └── img/

Link para importar archivos estáticos:
{% static 'clientes/css/style.css' %}
```

## Paso 3: Verificar que funciona

```bash
# Ejecutar el servidor de desarrollo
python manage.py runserver
```

Si ves el cohete de Django en `http://127.0.0.1:8000/` → ✅ el proyecto está vivo.

> 💡 **Importante:** Crear una app no es suficiente. Django no sabe que existe hasta que la **registras** en `settings.py`.

> 📚 **Fuente:** Django Software Foundation. (2024). _Writing your first Django app, part 1_. https://docs.djangoproject.com/en/stable/intro/tutorial01/

---

---

# ⚙️ 4. Registro de la Aplicación en `settings.py`

---

Para que Django reconozca una app como parte activa del proyecto, es necesario registrarla en la sección `INSTALLED_APPS` del archivo `settings.py`.

## ¿Por qué es necesario?

```
SIN registrar la app                    CON la app registrada
────────────────────────                ────────────────────────
Django ignora los modelos               Django detecta los modelos
makemigrations no genera nada           makemigrations crea migraciones
Los templates no se encuentran          Los templates se buscan automáticamente
El admin no muestra la app              El admin puede mostrar sus modelos
```

## ¿Cómo se hace?

```python
# mi_proyecto_crud/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Librerias externas

    # Apps propias ← AQUÍ se registran
    'clientes',
]
```

## Configurar la carpeta de templates

Además, para que Django encuentre los templates HTML, es buena práctica configurar la ruta de templates:

```python
# settings.py — dentro de la configuración TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← Carpeta global de templates
        'APP_DIRS': True,                   # ← Busca también en cada app
        # ...
    },
]
```

Luego crear la carpeta:

```bash
mkdir templates
```

> ⚠️ **Error común:** Olvidar registrar la app. Síntoma: `makemigrations` dice "No changes detected" aunque acabas de crear un modelo. Siempre verifica `INSTALLED_APPS` primero.

> 📚 **Fuente:** Django Software Foundation. (2024). _Applications_. https://docs.djangoproject.com/en/stable/ref/applications/

---

---

# 📋 5. Definición del Modelo con el ORM

---

Django permite representar estructuras de datos mediante clases llamadas **Modelos**. El ORM (Object-Relational Mapper) convierte automáticamente estas clases en tablas SQL.

## ¿Qué es el ORM?

```
TU CÓDIGO PYTHON                         LA BASE DE DATOS
──────────────────                        ──────────────────
class Cliente(models.Model):    ──────►   CREATE TABLE clientes_cliente (
    nombre = CharField()        ──────►       nombre VARCHAR(100),
    email = EmailField()        ──────►       email VARCHAR(254),
    ...                                       ...
                                          );

Cliente.objects.create(...)     ──────►   INSERT INTO clientes_cliente ...
Cliente.objects.filter(...)     ──────►   SELECT * FROM clientes_cliente WHERE ...
cliente.delete()                ──────►   DELETE FROM clientes_cliente WHERE ...
```

> 💡 **El ORM es el traductor.** Tú escribes Python → él escribe SQL. No necesitas tocar la base de datos directamente.

## Ejemplo: Modelo Cliente

```python
# clientes/models.py

from django.db import models

class Cliente(models.Model):
    nombre         = models.CharField(max_length=100)
    apellido       = models.CharField(max_length=100)
    email          = models.EmailField(unique=True)
    telefono       = models.CharField(max_length=20, blank=True)
    direccion      = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} "

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
```

### Desglose de cada campo

| Campo            | Tipo            | ¿Qué hace?                                                |
| :--------------- | :-------------- | :-------------------------------------------------------- |
| `nombre`         | `CharField`     | Texto corto, máximo 100 caracteres                        |
| `email`          | `EmailField`    | Texto que Django valida como email válido                 |
| `telefono`       | `CharField`     | Texto libre para teléfono, `blank=True` → puede ser vacío |
| `direccion`      | `TextField`     | Texto largo sin límite de caracteres                      |
| `fecha_registro` | `DateTimeField` | Se llena automáticamente al crear el registro             |

### ¿Y el `__str__`?

El método `__str__` define **cómo se muestra** el objeto cuando lo imprimes o lo ves en el panel de admin:

```
Sin __str__:  "Cliente object (1)"     ← No dice nada útil
Con __str__:  "Ana López (ana@mail.com)"  ← Legible y útil
```

### La Analogía de la Planilla

```
Un Modelo es como una PLANILLA de datos:
─────────────────────────────────────────
La clase es el diseño de la planilla (las columnas)
Cada instancia es una fila de datos en esa planilla
Los campos son las columnas (nombre, email, teléfono)
Las restricciones son las reglas (unique, max_length, blank)
```

> 📚 **Fuente:** Django Software Foundation. (2024). _Models_. https://docs.djangoproject.com/en/stable/topics/db/models/

---

---

# 🗄️ 6. Creación de la Base de Datos: Migraciones

---

Una vez definido un modelo, necesitamos decirle a Django: **"crea la tabla en la base de datos"**. Esto se hace con **migraciones**.

## ¿Qué son las migraciones?

```
MODELO PYTHON                     MIGRACIÓN                        BASE DE DATOS
─────────────────                 ────────────────                 ─────────────────
class Cliente(...)   ──────►      0001_initial.py   ──────►       CREATE TABLE ...
  nombre = CharField              (archivo que                     (tabla real en
  email  = EmailField              describe los                     SQLite/PostgreSQL)
                                   cambios)
```

Las migraciones son **el puente** entre tu código Python y la estructura SQL. Son archivos que Django genera automáticamente y que describen los cambios a aplicar.

## Proceso de dos pasos

### Paso 1: Crear la migración

```bash
python manage.py makemigrations
```

```
Output esperado:
──────────────────────────────
Migrations for 'clientes':
  clientes/migrations/0001_initial.py
    - Create model Cliente
```

Este comando **no toca la base de datos**. Solo genera el archivo `0001_initial.py` que describe qué tablas y columnas crear.

### Paso 2: Aplicar la migración

```bash
python manage.py migrate
```

```
Output esperado:
──────────────────────────────
Operations to perform:
  Apply all migrations: admin, auth, clientes, contenttypes, sessions
Running migrations:
  Applying clientes.0001_initial... OK
```

Este comando **sí modifica la base de datos**: ejecuta el SQL que crea la tabla.

## Verificar el estado

```bash
# Ver todas las migraciones y su estado
python manage.py showmigrations

# Output:
# clientes
#  [X] 0001_initial     ← [X] = aplicada ✅
#                          [ ] = pendiente ❌
```

### La Analogía del Arquitecto

```
EL ARQUITECTO                              LAS MIGRACIONES
──────────────────                         ──────────────────
1. Dibuja el plano del edificio            1. makemigrations genera el "plano"
   (no construye nada aún)                    (0001_initial.py)

2. Le pasa el plano al constructor         2. migrate ejecuta el "plano"
   que construye la estructura                y crea las tablas

3. Si quiere agregar un piso,              3. Si agregas un campo al modelo,
   dibuja un nuevo plano                      makemigrations genera otro archivo

4. El constructor aplica el cambio         4. migrate aplica los cambios
   sin demoler lo anterior                    sin perder los datos existentes
```

> ⚠️ **Error común:** Ejecutar `makemigrations` y olvidar ejecutar `migrate`. El modelo existe en Python pero la tabla no existe en la base de datos → todo falla cuando intentas guardar datos.

> 📚 **Fuente:** Django Software Foundation. (2024). _Migrations_. https://docs.djangoproject.com/en/stable/topics/migrations/

---

---

# 🖥️ 7. Vistas Basadas en Clases para CRUD

---

Django facilita el desarrollo CRUD con **vistas genéricas basadas en clases** (CBV — Class-Based Views). Estas vistas encapsulan comportamientos comunes como listar, crear, editar o eliminar registros, evitando código repetitivo.

## ¿Por qué usar clases en vez de funciones?

```
VISTA COMO FUNCIÓN                       VISTA COMO CLASE
──────────────────                       ──────────────────
Escribes todo a mano                     Django ya tiene la lógica hecha
Repites código en cada CRUD              Heredas y personalizas solo lo necesario
Más control pero más trabajo             Menos código, misma funcionalidad
Buena para lógica muy personalizada      Perfecta para operaciones estándar
```

## Las 5 vistas genéricas del CRUD

| Vista        | Operación  | ¿Qué hace?                                 | Template esperado             |
| :----------- | :--------- | :----------------------------------------- | :---------------------------- |
| `ListView`   | **Read**   | Lista todos los registros                  | `cliente_list.html`           |
| `DetailView` | **Read**   | Muestra un registro individual             | `cliente_detail.html`         |
| `CreateView` | **Create** | Muestra formulario y guarda nuevo registro | `cliente_form.html`           |
| `UpdateView` | **Update** | Muestra formulario con datos y actualiza   | `cliente_form.html`           |
| `DeleteView` | **Delete** | Confirma y elimina un registro             | `cliente_confirm_delete.html` |

## Implementación completa

```python
# clientes/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'
    # Django busca TODOS los clientes y los pasa al template
    # como la variable "clientes"


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
    # Django busca el cliente por su PK (primary key)
    # y lo pasa al template como "cliente"


class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'email', 'telefono', 'direccion']
    success_url = reverse_lazy('clientes:lista')
    # Django genera un formulario con esos campos
    # Si el usuario envía datos válidos → guarda y redirige


class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'email', 'telefono', 'direccion']
    success_url = reverse_lazy('clientes:lista')
    # Igual que Create, pero el formulario viene
    # con los datos actuales del cliente ya cargados


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:lista')
    # Muestra una página de confirmación
    # Si el usuario confirma → elimina el registro
```

### ¿Qué es `reverse_lazy`?

```
reverse_lazy('clientes:lista')
          │         │
          │         └── Nombre de la URL (definida en urls.py)
          └── Namespace de la app

→ Genera la URL "/clientes/" de forma automática
→ Si cambias la URL en urls.py, no necesitas cambiar la vista
→ "lazy" porque se resuelve al momento de usarse, no al importarse
```

> 💡 **Convención de nombres:** Django busca templates con nombres predeterminados basados en el modelo. `ClienteListView` busca `cliente_list.html`, `ClienteCreateView` busca `cliente_form.html`. Puedes cambiarlos con `template_name`.

> 📚 **Fuente:** Django Software Foundation. (2024). _Built-in class-based generic views_. https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/

---

---

# 🛡️ 8. CSRF y Formularios Seguros

---

## ¿Qué es CSRF?

CSRF (Cross-Site Request Forgery) es un ataque donde un sitio malicioso engaña al navegador del usuario para que envíe acciones a tu sitio web sin su consentimiento.

```
EL ATAQUE CSRF:
────────────────
1. El usuario está logueado en tu sitio (tiene cookies activas)
2. Visita un sitio malicioso
3. Ese sitio tiene un formulario oculto que apunta a TU servidor:
   <form action="https://tu-sitio.com/clientes/eliminar/5/" method="POST">
4. El navegador envía la petición CON las cookies del usuario
5. Tu servidor la procesa como si fuera legítima → elimina el cliente 5

¿Cómo lo evitamos?
Con un TOKEN CSRF que solo tu sitio puede generar.
El sitio malicioso no puede adivinar ese token.
```

## ¿Cómo funciona el token?

```
┌─────────────────────────────────────────────────────────────────┐
│  1. El usuario abre tu formulario                               │
│     → Django genera un token ÚNICO y secreto                    │
│     → Lo mete dentro del HTML del formulario como campo oculto  │
│                                                                 │
│  2. El usuario envía el formulario                              │
│     → El navegador envía el token junto con los datos           │
│                                                                 │
│  3. Django recibe la petición                                   │
│     → Verifica que el token coincide                            │
│     → Si coincide → ACEPTA la petición ✅                       │
│     → Si no coincide → RECHAZA la petición ❌ (403 Forbidden)   │
│                                                                 │
│  El sitio malicioso no tiene el token → su petición es rechazada│
└─────────────────────────────────────────────────────────────────┘
```

## ¿Cómo se usa en el template?

```html
<!-- En CADA formulario con method="POST" -->
<form method="POST">
  {% csrf_token %}

  <!-- Campos del formulario -->
  {{ form.as_p }}

  <button type="submit">Guardar</button>
</form>
```

El `{% csrf_token %}` genera un campo oculto tipo:

```html
<input type="hidden" name="csrfmiddlewaretoken" value="abc123xyz789..." />
```

> ⚠️ **Regla obligatoria:** Todo formulario que use `method="POST"` en Django debe incluir `{% csrf_token %}`. Sin él, Django devuelve un error **403 Forbidden**.

> 📚 **Fuente:** Django Software Foundation. (2024). _Cross Site Request Forgery protection_. https://docs.djangoproject.com/en/stable/howto/csrf/

> 📚 **Fuente:** OWASP Foundation. (2024). _Cross-Site Request Forgery Prevention Cheat Sheet_. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html

---

---

# 🔗 9. Enrutamiento y Configuración de URLs

---

Django maneja la navegación a través de archivos `urls.py`. Para una aplicación CRUD, debemos crear rutas que conecten cada URL con su vista correspondiente.

## Estructura del enrutamiento

```
USUARIO ESCRIBE EN EL NAVEGADOR:        DJANGO BUSCA EN:
────────────────────────────────         ────────────────────
/clientes/                    ──────►   urls.py del proyecto
                                             │
                                             ▼
                                        include('clientes.urls')
                                             │
                                             ▼
                                        urls.py de la app clientes
                                             │
                                             ▼
                                        ClienteListView
                                             │
                                             ▼
                                        cliente_list.html → Respuesta al usuario
```

## URLs del proyecto principal

```python
# mi_proyecto_crud/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),  # ← Delega a la app
]
```

## URLs de la aplicación

```python
# clientes/urls.py  (crear este archivo)

from django.urls import path
from . import views

app_name = 'cli'  # ← Namespace para evitar colisiones

urlpatterns = [
    # Listar todos los clientes
    path('', views.ClienteListView.as_view(), name='lista'),
    misitioweb.com/clientes/
    # Ver detalle de un cliente
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detalle'),
    misitioweb.com/clientes/122
    # Crear un nuevo cliente
    path('nuevo/', views.ClienteCreateView.as_view(), name='crear'),
    misitioweb.com/clientes/nuevo
    # Editar un cliente existente
    path('editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='editar'),
    misitioweb.com/clientes/editar/122
    # Eliminar un cliente
    path('eliminar/<int:pk>/', views.ClienteDeleteView.as_view(), name='eliminar'),
    misitioweb.com/clientes/eliminar/122
]
```

### Desglose de una ruta

```
path('editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='editar')
      │        │                      │                          │
      │        │                      │                          └── Nombre para
      │        │                      │                              referenciar en
      │        │                      │                              templates y vistas
      │        │                      └── La vista que maneja esta URL
      │        │                          .as_view() convierte la clase en vista
      │        └── Captura un número entero de la URL
      │            y lo pasa a la vista como "pk"
      └── La URL parcial (se suma a /clientes/)
          URL completa: /clientes/editar/5/
```

### ¿Qué es `<int:pk>`?

```
URL: /clientes/editar/5/
                      │
                      └── Este "5" es el pk (primary key) del cliente
                          Django lo captura y se lo pasa a la vista
                          La vista busca: Cliente.objects.get(pk=5)
```

### Usar las URLs en templates

```html
<!-- En vez de escribir URLs a mano, usamos el tag url -->

<!-- Link a la lista -->
<a href="{% url 'cli:lista' %}">Ver todos los clientes</a>

<!-- Link al detalle del cliente con pk=5 -->
<a href="{% url 'cli:detalle' cliente.pk %}">Ver detalle</a>

<!-- Link para editar -->
<a href="{% url 'cli:editar' cliente.pk %}">Editar</a>

<!-- Link para eliminar -->
<a href="{% url 'cli:eliminar' cliente.pk %}">Eliminar</a>
```

> 💡 **Ventaja de usar nombres:** Si cambias la URL de `/editar/` a `/modificar/`, solo cambias el `urls.py`. Todos los templates se actualizan automáticamente porque usan el **nombre**, no la URL literal.

> 📚 **Fuente:** Django Software Foundation. (2024). _URL dispatcher_. https://docs.djangoproject.com/en/stable/topics/http/urls/

---

---

# 🔄 10. Operaciones CRUD con el ORM

---

Django permite realizar las cuatro operaciones fundamentales (Crear, Leer, Actualizar, Eliminar) directamente con código Python, sin escribir SQL.

## Las 4 operaciones

### 🟢 CREATE — Crear un registro

```python
# Forma 1: create() — crea y guarda en un solo paso
nuevo_cliente = Cliente.objects.create(
    nombre='Ana López',
    email='ana@correo.com',
    telefono='+56912345678',
    direccion='Av. Siempre Viva 123'
)
# Django ejecuta: INSERT INTO clientes_cliente (nombre, email, ...) VALUES (...)

# Forma 2: instanciar y luego .save()
otro_cliente = Cliente(
    nombre='Carlos Pérez',
    email='carlos@correo.com'
)
otro_cliente.save()  # ← Aquí se guarda en la BD
```

### 🔵 READ — Leer registros

```python
# Obtener TODOS los registros
todos = Cliente.objects.all()

# Obtener UN registro por su clave primaria
cliente = Cliente.objects.get(pk=1)

# Filtrar registros
activos = Cliente.objects.filter(nombre__icontains='ana')

# Obtener el primero que coincida
primero = Cliente.objects.filter(email__endswith='@gmail.com').first()
```

### 🟡 UPDATE — Actualizar un registro

```python
# Forma 1: obtener, modificar, guardar
cliente = Cliente.objects.get(pk=1)
cliente.telefono = '+56987654321'
cliente.save()
# Django ejecuta: UPDATE clientes_cliente SET telefono='...' WHERE id=1

# Forma 2: actualizar masivamente (sin cargar objetos)
Cliente.objects.filter(direccion='').update(direccion='Sin dirección')
# Actualiza TODOS los que no tienen dirección — en un solo SQL
```

### 🔴 DELETE — Eliminar un registro

```python
# Eliminar UN registro
cliente = Cliente.objects.get(pk=1)
cliente.delete()
# Django ejecuta: DELETE FROM clientes_cliente WHERE id=1

# Eliminar varios registros a la vez
Cliente.objects.filter(fecha_registro__year=2023).delete()
# Elimina todos los clientes registrados en 2023
```

## Tabla resumen

| Operación  | Método del ORM              | SQL equivalente            |
| :--------- | :-------------------------- | :------------------------- |
| **Create** | `.objects.create()`         | `INSERT INTO ... VALUES`   |
| **Read**   | `.objects.all()` / `.get()` | `SELECT * FROM ...`        |
| **Update** | `.save()` / `.update()`     | `UPDATE ... SET ... WHERE` |
| **Delete** | `.delete()`                 | `DELETE FROM ... WHERE`    |

> 💡 **Importante:** Las vistas genéricas (`CreateView`, `UpdateView`, `DeleteView`) ejecutan estas mismas operaciones del ORM por debajo. La diferencia es que las vistas las conectan con formularios HTML y la navegación del usuario.

> 📚 **Fuente:** Django Software Foundation. (2024). _Making queries_. https://docs.djangoproject.com/en/stable/topics/db/queries/

---

---

# 🧩 11. Integración en el Patrón MTV

---

Django sigue una variante del patrón MVC llamada **MTV** (Modelo-Template-Vista):

```
MVC CLÁSICO                              DJANGO (MTV)
──────────────────                       ──────────────────
Model       → Datos                      Model     → models.py
View        → Lo que ve el usuario       Template  → archivos .html
Controller  → Lógica de la aplicación    View      → views.py

¿Por qué lo renombra Django?
Porque en Django, la "vista" de MVC es el template (HTML),
y la "vista" de Django es lo que en MVC se llama "controlador".
Es solo una diferencia de nombres, el concepto es el mismo.
```

## Flujo completo de una operación CRUD

```
┌──── PASO 1 ────────────────────────────────────────────────┐
│ El usuario escribe: /clientes/nuevo/                       │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──── PASO 2 ────────────────────────────────────────────────┐
│ Django busca en urls.py → encuentra ClienteCreateView      │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──── PASO 3 ────────────────────────────────────────────────┐
│ La VISTA (views.py) se activa                              │
│                                                            │
│ Si es GET → genera un formulario vacío                     │
│ Si es POST → recibe los datos del formulario               │
│   → Valida los datos                                       │
│   → Si son válidos → usa el MODELO para guardar en la BD   │
│   → Si no son válidos → devuelve el formulario con errores │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──── PASO 4 ────────────────────────────────────────────────┐
│ El MODELO (models.py) interactúa con la base de datos      │
│                                                            │
│ Cliente.objects.create(nombre='Ana', email='ana@mail.com') │
│ → INSERT INTO clientes_cliente ...                         │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──── PASO 5 ────────────────────────────────────────────────┐
│ El TEMPLATE (cliente_form.html) renderiza la respuesta     │
│                                                            │
│ → Si fue exitoso: redirige a la lista con un mensaje       │
│ → Si hubo errores: muestra el formulario con los errores   │
└────────────────────────────────────────────────────────────┘
```

### ¿Dónde encaja el CSRF en este flujo?

```
GET /clientes/nuevo/
    │
    ▼
Template genera formulario CON token CSRF
    │
    ▼
Usuario llena el formulario y presiona "Guardar"
    │
    ▼
POST /clientes/nuevo/  (con token CSRF incluido)
    │
    ▼
Django verifica el token ← Si no coincide → 403 Forbidden
    │
    ▼ (token válido)
Vista procesa los datos → Modelo guarda en BD → Redirige
```

> 📚 **Fuente:** Django Software Foundation. (2024). _FAQ: General — Django appears to be a MVC framework_. https://docs.djangoproject.com/en/stable/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names

---

---

# 🎯 12. Demo: Creación del Proyecto CRUD desde Cero

---

## ¿En qué consiste?

Vamos a construir paso a paso una aplicación Django completa que permita gestionar clientes con todas las operaciones CRUD.

## Pasos de la demo

### Parte 1: Proyecto y App

```
1. Crear el proyecto con: django-admin startproject mi_proyecto_crud
2. Crear la app: python manage.py startapp clientes
3. Registrar "clientes" en INSTALLED_APPS (settings.py)
4. Ejecutar el servidor para verificar
5. Crear la carpeta templates y configurar el path en settings.py
```

### Parte 2: Modelo y Base de Datos

```
1. Definir el modelo Cliente en models.py
   (nombre, email, telefono, direccion, fecha_registro)
2. Ejecutar makemigrations
3. Ejecutar migrate
4. Verificar con showmigrations
5. Registrar el modelo en admin.py:

   from django.contrib import admin
   from .models import Cliente

   admin.site.register(Cliente)

6. Crear superusuario: python manage.py createsuperuser
7. Verificar en /admin/ que se ve el modelo Cliente
```

### Parte 3: Vistas y URLs

```
1. Crear las 5 vistas genéricas en views.py
2. Crear el archivo urls.py en la app clientes
3. Incluir las URLs de la app en el urls.py del proyecto
4. Crear los templates básicos:
   - clientes/cliente_list.html
   - clientes/cliente_form.html
   - clientes/cliente_detail.html
   - clientes/cliente_confirm_delete.html
```

### Estructura final esperada

```
mi_proyecto_crud/
├── manage.py
├── mi_proyecto_crud/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── clientes/
│   ├── __init__.py
│   ├── admin.py           ← Cliente registrado
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py          ← Modelo Cliente definido
│   ├── tests.py
│   ├── urls.py            ← 5 rutas CRUD
│   └── views.py           ← 5 vistas genéricas
└── templates/
    └── clientes/
        ├── cliente_list.html
        ├── cliente_form.html
        ├── cliente_detail.html
        └── cliente_confirm_delete.html
```

---

# 🏁 Resumen de la Clase

---

| Concepto             | Herramienta / Archivo                         | Para qué sirve                                     |
| :------------------- | :-------------------------------------------- | :------------------------------------------------- |
| **Proyecto Django**  | `django-admin startproject`                   | Crear la estructura base con configuración         |
| **Aplicación (App)** | `python manage.py startapp`                   | Módulo funcional independiente dentro del proyecto |
| **Registro de App**  | `INSTALLED_APPS` en `settings.py`             | Que Django reconozca la app y sus modelos          |
| **Modelo**           | `models.py`                                   | Definir la estructura de datos (tablas)            |
| **Migraciones**      | `makemigrations` + `migrate`                  | Crear las tablas en la base de datos               |
| **Vistas genéricas** | `ListView`, `CreateView`, etc.                | CRUD automático con mínimo código                  |
| **Token CSRF**       | `{% csrf_token %}`                            | Proteger formularios contra ataques                |
| **URLs con nombre**  | `path(..., name='nombre')`                    | Navegación flexible y mantenible                   |
| **Operaciones ORM**  | `.create()`, `.get()`, `.save()`, `.delete()` | Interactuar con la BD sin SQL                      |
| **Patrón MTV**       | Modelo + Template + Vista                     | Separación de responsabilidades                    |

---

## 📚 Bibliografía y Fuentes

- Django Software Foundation. (2024). _Django overview_. https://docs.djangoproject.com/en/stable/intro/overview/
- Django Software Foundation. (2024). _Writing your first Django app_. https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Django Software Foundation. (2024). _Models_. https://docs.djangoproject.com/en/stable/topics/db/models/
- Django Software Foundation. (2024). _Migrations_. https://docs.djangoproject.com/en/stable/topics/migrations/
- Django Software Foundation. (2024). _Built-in class-based generic views_. https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/
- Django Software Foundation. (2024). _Cross Site Request Forgery protection_. https://docs.djangoproject.com/en/stable/howto/csrf/
- Django Software Foundation. (2024). _URL dispatcher_. https://docs.djangoproject.com/en/stable/topics/http/urls/
- Django Software Foundation. (2024). _Making queries_. https://docs.djangoproject.com/en/stable/topics/db/queries/
- OWASP Foundation. (2024). _Cross-Site Request Forgery Prevention Cheat Sheet_. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
