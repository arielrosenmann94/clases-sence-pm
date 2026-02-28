# 🏗️ Django — Módulo 6 · Clase 5

### Arquitectura de Proyectos Django: Decisiones que Definen el Futuro

---

> _"La arquitectura no es lo que ves en pantalla. Es todo lo que decidiste antes de escribir la primera línea de código."_

---

## Clase 5: qué vas a aprender hoy

Antes de programar funcionalidades, los equipos profesionales toman decisiones importantes sobre **cómo organizar el proyecto**. Esas decisiones impactan la escalabilidad, el mantenimiento y la legibilidad del código.

- 🗂️ Entenderás los **patrones de estructura de carpetas** que usan los proyectos reales.
- ⚖️ Compararás las **variantes arquitectónicas** y cuándo conviene cada una.
- 📋 Aprenderás las **reglas** que todo proyecto define antes de arrancar.
- 📄 Al final construiremos un **documento de decisiones** listo para pasarle a un equipo o a una IA.

> 🎯 Meta: que puedas sentarte con un equipo el lunes y tomar decisiones de arquitectura fundamentadas — no por intuición, sino por criterio técnico.

---

---

# PARTE 1: LA ESTRUCTURA DE UN PROYECTO DJANGO

---

## 1. ¿Por qué importa la estructura?

Imagina que llegas a trabajar a una empresa que tiene su cocina así:

> Las tazas están en el baño, los cuchillos en la habitación, la sal en el armario del garaje y la sartén debajo del sofá.

La comida podría terminar siendo igual de rica... pero perderías horas buscando cosas.

En programación pasa exactamente lo mismo. Un proyecto **técnicamente funcional** puede ser un **infierno de mantenimiento** si la estructura es caótica.

> 🧠 **Regla de oro:** Una buena estructura permite que cualquier desarrollador nuevo encuentre cualquier archivo en menos de 30 segundos sin preguntar.

---

## 2. La estructura mínima que crea Django por defecto

Cuando ejecutas `django-admin startproject nombre_proyecto`, Django te da esto:

```text
nombre_proyecto/            ← Carpeta raíz del repositorio
│
├── nombre_proyecto/        ← Paquete de configuración (confuso: mismo nombre)
│   ├── __init__.py
│   ├── settings.py         ← Configuración global
│   ├── urls.py             ← URLs raíz
│   ├── asgi.py             ← Configuración ASGI (async)
│   └── wsgi.py             ← Configuración WSGI (deploy)
│
└── manage.py               ← Herramienta de comandos de Django
```

Este es el punto de partida **mínimo**. Pero los proyectos reales necesitan más.

> ⚠️ **El problema más común del principiante:** Dejar el paquete de configuración con el mismo nombre que la carpeta raíz. Es confuso. Los equipos profesionales lo renombran inmediatamente.

---

## 3. La primera decisión: renombrar la carpeta de configuración

**Convención profesional:** renombrar el paquete de configuración a algo neutro y descriptivo, como `config/`.

```text
# ❌ Confuso — Django por defecto
mi_tienda/
    mi_tienda/           ← ¿Esto es la app? ¿La config? Imposible saberlo.
        settings.py
    manage.py

# ✅ Claro — Convención profesional
mi_tienda/
    config/              ← Unívoco: aquí está la configuración del proyecto
        settings.py
    manage.py
```

Se puede crear el proyecto directamente con el nombre `config`:

```bash
django-admin startproject config .
```

El punto `.` indica "en el directorio actual", evitando la doble carpeta anidada.

---

---

# PARTE 2: VARIANTES ARQUITECTÓNICAS

---

## 4. ¿De qué depende la estructura que elijo?

Esta es la pregunta clave y la respuesta más importante de esta clase:

> **La estructura no la determina el tamaño del equipo. La determina el propósito del proyecto y su diseño de escalabilidad.**

Un desarrollador solo puede construir un sistema bancario complejo que necesita la estructura más avanzada. Un equipo de diez personas puede hacer un prototipo que no necesita más que la estructura más simple. **La pregunta correcta no es "¿cuántos somos?", sino "¿qué necesita este sistema y cómo va a crecer?"**

Para responder eso, hay que hacerse estas preguntas antes de arrancar:

| Pregunta sobre el proyecto                                                      | Qué define                     |
| ------------------------------------------------------------------------------- | ------------------------------ |
| ¿Cuántos dominios de negocio distintos maneja? (usuarios, pagos, inventario...) | Cuántas apps necesito          |
| ¿Va a desplegarse en un servidor real con entornos separados?                   | Si necesito settings divididos |
| ¿Tendrá distintos tipos de usuario con distintos permisos?                      | Qué sistema de auth usar       |
| ¿Hay archivos que suben los usuarios (fotos, documentos)?                       | Si necesito media configurado  |
| ¿Va a crecer en funcionalidades después del lanzamiento?                        | Si necesito diseño escalable   |
| ¿Convive con una app móvil o frontend separado?                                 | Si necesito una API REST       |

Con esas respuestas en mano, se elige la estructura.

---

## 5. Las tres estructuras más usadas en proyectos reales

---

### Estructura A: Monolítica Plana

> _"Todo en un solo lugar, moverse rápido, validar la idea."_

```text
mi_proyecto/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                    ← Una sola app con toda la lógica
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   └── core/
│       ├── list.html
│       └── detail.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
└── requirements.txt
```

**¿Cuándo corresponde esta estructura?**

Cuando el proyecto es un **prototipo**, un **ejercicio de validación** o una herramienta interna simple con una sola funcionalidad central. La clave no es la cantidad de personas, sino el **alcance** y el **horizonte** del proyecto. Si el objetivo es lanzar algo rápido para probar si funciona la idea, esta estructura es la correcta. Si ya sabes que el proyecto va a escalar, empezar así es construir sobre arena.

**Ventajas:**

- Sin overhead de configuración.
- Se mueve rápido en las primeras etapas.

**Limitaciones:**

- A medida que crece, todo se mezcla en los mismos archivos.
- Muy difícil de reorganizar después sin romper cosas.

---

### Estructura B: Multi-App por Dominio de Negocio

> _"Cada área del negocio tiene su propio espacio."_

```text
mi_proyecto/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/                    ← 📦 Todas las apps organizadas por dominio
│   ├── __init__.py
│   ├── products/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   └── admin.py
│   ├── users/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   └── orders/
│       ├── models.py
│       ├── views.py
│       └── ...
│
├── templates/               ← 📄 Templates centralizados
│   ├── base.html
│   ├── products/
│   │   ├── list.html
│   │   └── detail.html
│   └── users/
│       └── profile.html
│
├── static/                  ← 🎨 Estáticos centralizados
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                   ← 🖼️ Archivos subidos por usuarios
│
├── manage.py
└── requirements.txt
```

**¿Cuándo corresponde esta estructura?**

Cuando el proyecto tiene **dominios de negocio claramente separados** y se sabe desde el diseño que cada área va a tener sus propios modelos, vistas, reglas y URLs. Un e-commerce necesita `products`, `orders`, `users`, `payments` — son cuatro mundos distintos que no deberían mezclarse. Esto no es una decisión de cuánta gente trabaja en el proyecto: es una decisión de diseño.

**Ventajas:**

- Separación clara de responsabilidades.
- Cada dominio se puede testear y modificar de forma independiente.
- El código se autodocumenta por la sola estructura de carpetas.

**Limitaciones:**

- Requiere más decisiones al inicio.
- Las dependencias entre apps deben diseñarse con cuidado.

---

### Estructura C: Multi-App con Environments Separados

> _"El sistema vive en múltiples entornos y cada uno tiene su propia configuración."_

```text
mi_proyecto/
│
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          ← Configuración común a todos los entornos
│   │   ├── local.py         ← Solo para desarrollo local
│   │   ├── staging.py       ← Para el entorno de pruebas/QA
│   │   └── production.py    ← Para el servidor real (secretos excluidos)
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   └── ...                  ← (igual que Estructura B)
│
├── templates/
├── static/
├── media/
│
├── requirements/            ← 📋 Dependencias separadas por entorno
│   ├── base.txt             ← Librerías comunes (Django, Pillow...)
│   ├── local.txt            ← Solo para desarrollo (django-debug-toolbar...)
│   └── production.txt       ← Solo para producción (gunicorn, psycopg2...)
│
├── .env                     ← 🔑 Variables de entorno (NUNCA al repositorio)
├── .env.example             ← Plantilla de .env sin valores reales
├── .gitignore
├── manage.py
└── README.md
```

**¿Cuándo corresponde esta estructura?**

Cuando el sistema **vive en un servidor real** y tiene una vida útil más allá del desarrollo. Todo proyecto que va a producción necesita separar las configuraciones: en local usamos SQLite, en producción usamos PostgreSQL; en local mostramos los errores en pantalla, en producción los escribimos en un log. Intentar manejar eso con un solo `settings.py` es mezclar responsabilidades que tienen propósitos distintos.

**Ventajas:**

- Configuración diferente por entorno sin tocar un solo archivo.
- Los secretos nunca llegan al repositorio.
- Permite despliegues reproducibles y controlados.

**Limitaciones:**

- Curva de aprendizaje más alta.
- Requiere disciplina para mantener los environments sincronizados.

---

### ¿Cómo decido cuál usar?

```text
¿El proyecto ya tiene un diseño con dominios de negocio separados?
    │
    ├── No → Estructura A (Plana)
    │
    └── Sí
           │
           ├── ¿Va a vivir en un servidor real con entornos diferenciados?
           │       │
           │       ├── No → Estructura B (Multi-App)
           │       │
           │       └── Sí → Estructura C (Multi-App + Environments)
           │
           └── ¿Es una API REST sin templates HTML?
                   │
                   └── Sí → Estructura C + Django REST Framework
```

| Criterio de diseño                             | A — Plana   | B — Multi-App | C — Multi-Env |
| ---------------------------------------------- | ----------- | ------------- | ------------- |
| Proyecto de un solo dominio de negocio         | ✅          | ⚠️ Excesivo   | ❌ Excesivo   |
| Múltiples dominios de negocio separados        | ❌          | ✅            | ✅            |
| Se despliega en servidor real                  | ❌          | ⚠️ Parcial    | ✅            |
| Requiere entornos staging / QA                 | ❌          | ❌            | ✅            |
| Tiene secretos que NO pueden ir al repositorio | ⚠️ Riesgoso | ⚠️ Parcial    | ✅ Completo   |
| Es una API REST (sin templates)                | ❌          | ⚠️ Incompleto | ✅ + DRF      |

---

---

# PARTE 3: REGLAS QUE SE DEFINEN ANTES DE COMENZAR

---

## 6. El conjunto de decisiones del proyecto

Todo proyecto profesional define estas reglas antes de escribir la primera línea de código de negocio. Se documentan en el `README.md` o en un archivo `ARCHITECTURE.md`.

---

### 🔵 Decisión 1: Nomenclatura de apps

**¿Las apps van en singular o plural? ¿En qué idioma?**

```text
# ❌ Mezcla caótica — lo peor que puede pasarle a un proyecto
apps/
    products/       ← inglés plural
    usuario/        ← español singular
    pedidos/        ← español plural
    Payment/        ← inglés singular con mayúscula

# ✅ Convención unificada — inglés, plural, snake_case
apps/
    products/
    users/
    orders/
    payments/
    product_reviews/     ← nombre compuesto: snake_case
```

> ✅ **Convención recomendada:** nombres en **inglés**, en **plural**, en **minúsculas**, usando **snake_case** para nombres compuestos. Define la regla una vez, aplícala en todo el proyecto sin excepción.

---

### 🔵 Decisión 2: Idioma del código fuente

**¿El código va en español o inglés?**

```python
# ❌ Mezcla caótica — el peor error posible
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)   # ¡inglés mezclado!
    email_usuario = models.EmailField()             # redundante
```

```python
# ✅ Convención consistente — código en inglés, comentarios en español
class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
```

**Regla recomendada:**

- **Código fuente** (variables, funciones, clases, URLs, modelos): en **inglés**.
- **Comentarios y documentación técnica**: en el **idioma del equipo**.
- **Contenido que ve el usuario** (textos, labels, errores en pantalla): en el **idioma del producto**.

---

### 🔵 Decisión 3: Dónde viven los templates

**¿Templates dentro de cada app o centralizados en la raíz?**

```text
# Opción A: Templates dentro de cada app
apps/
    products/
        templates/
            products/
                list.html
    users/
        templates/
            users/
                profile.html

# Opción B: Templates centralizados ← Más Usada
templates/
    base.html
    products/
        list.html
    users/
        profile.html
```

| Opción                          | Ventaja                                      | Limitación                           |
| ------------------------------- | -------------------------------------------- | ------------------------------------ |
| **A — dentro de cada app**      | La app es portable, se puede reutilizar sola | Difícil visualizar toda la capa HTML |
| **B — centralizados** _(recom)_ | Vista clara de toda la interfaz del proyecto | La app no es completamente portable  |

> 💡 Para proyectos que no se empaquetan como librerías externas, los **templates centralizados** son siempre la mejor opción.

---

### 🔵 Decisión 4: Variables de entorno desde el inicio

**Nunca hardcodear secretos en el código.** Esta regla se define antes de escribir la primera línea.

```python
# ❌ NUNCA HACER ESTO — el secreto queda expuesto en el repositorio para siempre
SECRET_KEY = 'django-insecure-abc123xyz987'
DATABASES = {
    'default': {
        'PASSWORD': 'super_secreto_123',  # 💀 Esto queda en git forever
    }
}
```

```python
# ✅ La forma correcta: leer de variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DATABASES = {
    'default': {
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}
```

```bash
# .env — NUNCA al repositorio (va en .gitignore)
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DB_NAME=mi_base
DB_USER=mi_usuario
DB_PASSWORD=mi_password

# .env.example — SÍ al repositorio, sin valores reales
DJANGO_SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
```

> 🔐 **Regla crítica:** El archivo `.env` se agrega al `.gitignore` ANTES del primer commit. Si alguna vez lo subiste por error, el secreto está comprometido aunque lo borres después. Git guarda la historia completa.

---

### 🔵 Decisión 5: El `.gitignore` estándar de Django

El `.gitignore` se crea **antes del primer `git add`**. Nunca después.

```gitignore
# Entorno virtual — nunca al repositorio
venv/
env/
.venv/

# Secretos — CRÍTICO
.env

# Base de datos local
db.sqlite3

# Python compilado
__pycache__/
*.pyc
*.pyo

# Archivos de medios subidos por usuarios
media/

# Archivos de colección estática (se regeneran)
staticfiles/

# Sistema operativo
.DS_Store
Thumbs.db
```

---

### 🔵 Decisión 6: El `requirements.txt` desde el día 1

¿Alguna vez escuchaste "en mi computadora funciona"? Ese problema se resuelve con `requirements.txt`.

```bash
# Genera el archivo con todas las dependencias instaladas
pip freeze > requirements.txt

# Instala exactamente las mismas dependencias en otro entorno
pip install -r requirements.txt
```

> 📌 **Actualizar siempre que instales algo nuevo.** Si instalas `pip install pillow` y no actualizas el archivo, el próximo entorno no tendrá esa dependencia.

---

### 🔵 Decisión 7: Sistema de autenticación

Django trae su propio sistema de usuarios. El error más común es **empezar con el modelo `User` por defecto** y querer cambiarlo cuando el proyecto ya tiene datos en base de datos — en ese punto, la migración es un proceso doloroso y riesgoso.

La decisión correcta: **definir el modelo de usuario antes de la primera migración**.

```python
# ❌ Usar el User de Django por defecto y después querer agregar campos
# Cuando quieras agregar 'telefono' o 'avatar', tendrás que crear un perfil
# aparte o hacer migraciones complejas

# ✅ Crear un modelo CustomUser desde el inicio — aunque esté vacío
# apps/users/models.py

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Por ahora puede estar vacío — pero después puedes agregar campos fácilmente
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
```

```python
# settings.py — decirle a Django que use nuestro modelo en lugar del default
AUTH_USER_MODEL = 'users.User'
```

> ⚠️ **Regla crítica:** `AUTH_USER_MODEL` se define **antes de la primera migración**. Si ya corriste `migrate`, cambiar el modelo de usuario requiere borrar la base de datos o hacer migraciones manuales muy complejas.

---

### 🔵 Decisión 8: Sistema de permisos y roles

**¿Quién puede ver qué y quién puede hacer qué?**

Django tiene un sistema de permisos integrado basado en **Groups** (grupos de usuarios) y **Permissions** (permisos por modelo). Antes de necesitarlos, hay que decidir qué modelo de permisos usar.

#### Opción A — Permisos simples (staff/no-staff)

Para proyectos donde hay solo dos niveles: usuarios del panel admin y usuarios normales.

```python
# Proteger una vista para que solo accedan usuarios autenticados
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ...

# Proteger para que solo accedan usuarios con acceso al admin
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def panel_interno(request):
    ...
```

#### Opción B — Grupos y Permisos de Django

Para proyectos donde hay distintos roles con distintas capacidades. Los Groups se crean en el panel admin de Django y se asignan a usuarios.

```python
# Proteger una vista para un permiso específico del modelo
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('products.add_product', raise_exception=True)
def create_product(request):
    # Solo usuarios con permiso de crear productos pueden entrar
    ...
```

```python
# En el template: mostrar o esconder elementos según permiso
{% if perms.products.add_product %}
    <a href="{% url 'products:create' %}">Agregar producto</a>
{% endif %}
```

#### Opción C — Roles personalizados (campo en el modelo)

Para proyectos con lógica de negocio compleja donde los roles no coinciden exactamente con los permisos de Django.

```python
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        MANAGER = 'manager', 'Gerente'
        OPERATOR = 'operator', 'Operador'
        CLIENT = 'client', 'Cliente'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT
    )

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
```

> 📋 **Decisión de diseño:** Definir el sistema de roles **antes de crear los primeros modelos**. Cambiar el sistema de permisos a mitad del proyecto implica reescribir vistas, templates y tests.

---

### 🔵 Decisión 9: Estructura de URLs con namespaces

Cuando el proyecto crece y tiene muchas apps, los nombres de URL pueden **colisionar**:

```python
# ❌ Problema: dos apps con name='list' — ¿cuál usa el template?
# products/urls.py
path('', views.list, name='list')

# users/urls.py
path('', views.list, name='list')
```

La solución son los **namespaces**:

```python
# apps/products/urls.py
app_name = 'products'          # ← Define el namespace de la app

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('create/', views.product_create, name='create'),
]
```

```html
<!-- En el template, se usa el namespace como prefijo -->
<a href="{% url 'products:list' %}">Ver todos los productos</a>
<a href="{% url 'products:detail' pk=5 %}">Ver producto 5</a>
```

> ✅ **Regla:** Toda app define su `app_name`. Sin namespaces, el proyecto no puede escalar sin colisiones de nombres.

---

### 🔵 Decisión 10: Estilo de vistas (FBV vs CBV)

Existen dos estilos de vistas en Django. Cada proyecto elige uno y lo aplica consistentemente.

```python
# FBV — Function Based Views (más explícitas, más fácil de leer)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

# CBV — Class Based Views (más concisas, más potentes)
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
```

**Convención de nombres recomendada:**

| Acción   | FBV              | CBV                 |
| -------- | ---------------- | ------------------- |
| Listado  | `product_list`   | `ProductListView`   |
| Detalle  | `product_detail` | `ProductDetailView` |
| Crear    | `product_create` | `ProductCreateView` |
| Editar   | `product_update` | `ProductUpdateView` |
| Eliminar | `product_delete` | `ProductDeleteView` |

> ✅ **Regla:** Decidir FBV o CBV antes de crear la primera vista. Mezclar estilos sin criterio dificulta leer el código.

---

### 🔵 Decisión 11: Organización de los modelos

Los modelos son el corazón del proyecto. Cómo se organizan define la calidad de toda la base de datos.

**Reglas a definir antes de crear el primer modelo:**

```python
# ❌ Modelo sin buenas prácticas
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()           # FloatField tiene problemas de precisión
    fecha = models.DateTimeField()         # ¿Creación? ¿Modificación? ¿Expiración?
    activo = models.BooleanField()         # Sin default

# ✅ Modelo con buenas prácticas desde el inicio
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)   # Precisión monetaria
    is_active = models.BooleanField(default=True)                  # Default explícito
    created_at = models.DateTimeField(auto_now_add=True)           # Se setea al crear
    updated_at = models.DateTimeField(auto_now=True)               # Se actualiza solo

    class Meta:
        ordering = ['-created_at']           # Orden por defecto de las consultas
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name                     # Siempre definir __str__
```

**Campos que todo modelo debería considerar:**

| Campo        | Tipo                          | Para qué sirve                                |
| ------------ | ----------------------------- | --------------------------------------------- |
| `created_at` | `DateTimeField(auto_now_add)` | Saber cuándo se creó el registro              |
| `updated_at` | `DateTimeField(auto_now)`     | Saber cuándo se modificó por última vez       |
| `is_active`  | `BooleanField(default=True)`  | Soft delete: desactivar sin borrar de la base |
| `slug`       | `SlugField(unique=True)`      | URLs amigables para SEO                       |
| `uuid`       | `UUIDField`                   | ID público que no expone el ID interno        |

> 📌 **Decisión clave:** ¿El proyecto usa **hard delete** (borrar físicamente de la BD) o **soft delete** (marcar como inactivo)? Esta decisión afecta todos los modelos y todas las consultas.

---

### 🔵 Decisión 12: Manejo de archivos de medios (Media)

Si los usuarios pueden subir archivos (fotos de perfil, documentos, imágenes de productos), el proyecto necesita configurar **Media** desde el inicio.

```python
# settings.py
import os

MEDIA_URL = '/media/'                        # URL pública para acceder a los archivos
MEDIA_ROOT = BASE_DIR / 'media'             # Carpeta local donde se guardan
```

```python
# config/urls.py — solo en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... tus urls
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python
# Modelo con archivo de imagen
class Product(models.Model):
    image = models.ImageField(
        upload_to='products/%Y/%m/',   # Organiza por año/mes automáticamente
        null=True,
        blank=True
    )
```

> ⚠️ **Regla:** La carpeta `media/` va en el `.gitignore`. Cada entorno tiene sus propios archivos. En producción, los medios se sirven desde un almacenamiento externo (S3, Cloudinary, etc.), no desde el propio servidor.

---

### 🔵 Decisión 13: Señales (Signals) de Django

Las señales son el mecanismo de Django para **reaccionar automáticamente a eventos** sin acoplar el código. Por ejemplo: "cuando se crea un usuario, enviarle un email de bienvenida" o "cuando se confirma un pedido, descontar del stock".

```python
# apps/users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Se ejecuta automáticamente cuando se crea un usuario nuevo
        send_mail(
            subject='Bienvenido',
            message=f'Hola {instance.name}, tu cuenta fue creada.',
            from_email='noreply@misitio.com',
            recipient_list=[instance.email],
        )
```

```python
# apps/users/apps.py — registrar las señales al iniciar la app
class UsersConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        import apps.users.signals  # noqa: importar el módulo activa las señales
```

**¿Cuándo usar señales y cuándo no?**

| Usar señales cuando...                                             | No usar señales cuando...                                        |
| ------------------------------------------------------------------ | ---------------------------------------------------------------- |
| La lógica pertenece a un modelo diferente al que dispara el evento | La lógica puede ir directamente en el método `save()` del modelo |
| El efecto es un "efecto colateral" (enviar email, notificar)       | El orden de ejecución es crítico y debe ser predecible           |
| Quieres mantener las apps desacopladas                             | Hace más difícil seguir el flujo del código                      |

---

### 🔵 Decisión 14: Tests desde el inicio

Un proyecto sin tests es un proyecto que no puede cambiar con confianza. La decisión es definir qué se testea antes de que el proyecto crezca.

```python
# apps/products/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            price='99.99',
        )

    def test_product_str_returns_name(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_is_active_by_default(self):
        self.assertTrue(self.product.is_active)


class ProductViewTest(TestCase):
    def test_list_view_returns_200(self):
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('products:list'))
        self.assertTemplateUsed(response, 'products/list.html')
```

```bash
# Correr todos los tests
python manage.py test

# Correr tests de una app específica
python manage.py test apps.products
```

> ✅ **Convención:** cada app tiene su propio archivo `tests.py` o carpeta `tests/`. Por cada modelo: un test del `__str__` y de los defaults. Por cada vista: un test del status code y del template usado.

---

---

# PARTE 4: CASOS DE USO REALES

---

## 7. Tres tipos de proyecto — tres conjuntos de decisiones

### 📦 Caso A: E-commerce para una PyME

**Descripción del sistema:** tienda online con catálogo de productos, carrito de compras, sistema de pedidos y panel de administración.

**Decisiones tomadas:**

```text
Estructura:        Multi-App (B)
Apps:              products / orders / users / payments
Templates:         Centralizados en templates/
Settings:          Un solo settings.py (MVP primero, environments después)
Base de datos:     PostgreSQL
Auth:              AbstractUser personalizado (campo phone, avatar)
Roles:             Groups de Django: Cliente / Gerente / Admin
Permisos:          @login_required en todas las vistas de pedidos y perfil
Soft delete:       is_active en todos los modelos de negocio
Media:             ImageField en Product con upload_to='products/%Y/%m/'
Nomenclatura:      inglés, plural, snake_case
Idioma del código: inglés
Vistas:            CBV para CRUD, FBV para lógica especial (checkout)
Namespaces:        Sí, en todas las apps
.gitignore:        Configurado antes del primer commit
.env:              Con SECRET_KEY y DATABASE_URL
```

---

### 🏥 Caso B: Sistema interno de gestión para una clínica

**Descripción del sistema:** gestión de turnos médicos, historia clínica de pacientes y reportes. Acceso solo para personal interno.

**Decisiones tomadas:**

```text
Estructura:        Multi-App con Environments (C)
Apps:              appointments / patients / doctors / reports
Templates:         Centralizados
Settings:          local.py / production.py separados
Base de datos:     PostgreSQL
Auth:              AbstractUser con campo role (Recepcionista / Médico / Admin)
Permisos:          Todos los views con @login_required + @permission_required
Regla de datos:    Nunca exponer datos de pacientes sin validar permiso
Soft delete:       Sí — los registros médicos nunca se borran, se archivan
Signals:           post_save en Appointment → notificación al médico asignado
Tests:             Obligatorios para todos los flujos de permisos
.env:              Con datos de conexión a BD y claves de email
```

**Regla de seguridad del proyecto:**

```python
# Mixin para proteger TODAS las vistas del sistema
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AppointmentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'appointments.view_appointment'
    model = Appointment
    template_name = 'appointments/list.html'
```

---

### 🌍 Caso C: API REST para una app móvil

**Descripción del sistema:** backend Django que sirve datos JSON a una app iOS/Android. No hay templates HTML.

**Decisiones tomadas:**

```text
Estructura:        Multi-App con Environments (C) + DRF
Apps:              users / products / orders
Templates:         No hay — solo respuestas JSON
Settings:          base.py / local.py / production.py
Auth:              JWT Tokens (no sessions)
Versioning:        URLs con versión: /api/v1/ — /api/v2/
CORS:              Solo orígenes conocidos (dominio de la app)
Roles:             Campo role en el modelo User
Permisos:          IsAuthenticated + permisos personalizados de DRF
Media:             Almacenamiento en S3 (no local)
Signals:           No (lógica en serializers y servicios)
Tests:             Obligatorios para todos los endpoints
```

---

---

# PARTE 5: EL DOCUMENTO DE DECISIONES DEL PROYECTO

---

## 8. ¿Por qué documentar las decisiones?

Cuando un proyecto crece o cuando alguien nuevo se incorpora (ya sea un desarrollador o una IA), la primera pregunta siempre es: **¿cómo está organizado esto y por qué?**

Un documento de decisiones arquitectónicas responde esa pregunta sin necesidad de leer todo el código.

> 🤖 **Para las IAs también:** cuando le pasás tu documento de decisiones a una IA al inicio de una conversación, todas las respuestas van a estar alineadas con tus convenciones. No va a sugerir código en español si definiste inglés. No va a mezclar FBV con CBV. No va a hardcodear secretos.

---

## 9. Plantilla de Decisiones Arquitectónicas del Proyecto

Este es el documento que construimos durante la clase. Se completa una vez al inicio del proyecto y se actualiza si alguna decisión cambia.

---

```markdown
# 📋 Decisiones Arquitectónicas — [Nombre del Proyecto]

## Descripción general del sistema

[Qué hace el sistema, para quién está hecho, cuál es su propósito principal]

---

## Estructura

| Decisión                 | Valor elegido                       |
| ------------------------ | ----------------------------------- |
| Tipo de estructura       | [Plana / Multi-App / Multi-Entorno] |
| Carpeta de configuración | config/                             |
| Carpeta de apps          | apps/                               |
| Ubicación de templates   | [En cada app / Centralizados]       |
| Ubicación de estáticos   | static/ (centralizado)              |
| Carpeta de medios        | media/                              |

---

## Código

| Decisión                 | Valor elegido                             |
| ------------------------ | ----------------------------------------- |
| Idioma del código fuente | [inglés / español]                        |
| Idioma de comentarios    | [idioma del equipo]                       |
| Idioma del contenido UI  | [idioma del producto]                     |
| Nomenclatura de apps     | [plural / singular] en [inglés / español] |
| Estilo de vistas         | [FBV / CBV / mixto con criterio]          |
| Namespaces en URLs       | [Sí / No]                                 |

---

## Modelos

| Decisión                | Valor elegido                  |
| ----------------------- | ------------------------------ |
| Campo created_at        | [Sí / No] en todos los modelos |
| Campo updated_at        | [Sí / No] en todos los modelos |
| Soft delete (is_active) | [Sí / No]                      |
| **str** obligatorio     | Sí en todos los modelos        |
| Precios en DecimalField | [Sí / No]                      |
| UUID como ID público    | [Sí / No]                      |

---

## Autenticación y Permisos

| Decisión             | Valor elegido                             |
| -------------------- | ----------------------------------------- |
| Modelo de usuario    | [AbstractUser / User default]             |
| AUTH_USER_MODEL      | [users.User / auth.User]                  |
| Campos extra en User | [phone / avatar / role / ninguno]         |
| Sistema de roles     | [Groups de Django / Campo role / Ninguno] |
| Roles del sistema    | [lista de roles definidos]                |
| Vistas protegidas    | [Todas / Solo las autenticadas / Ninguna] |
| Método de protección | [@login_required / LoginRequiredMixin]    |

---

## Archivos de Medios

| Decisión                  | Valor elegido             |
| ------------------------- | ------------------------- |
| Maneja archivos de medios | [Sí / No]                 |
| En desarrollo             | Carpeta local media/      |
| En producción             | [S3 / Cloudinary / Local] |
| MEDIA configurado         | [Sí / No]                 |

---

## Entorno y Configuración

| Decisión                 | Valor elegido                           |
| ------------------------ | --------------------------------------- |
| Variables de entorno     | .env con python-dotenv                  |
| Settings separados       | [Sí: base/local/production / No: único] |
| Requirements separados   | [Sí: base/local/production / No: único] |
| .gitignore configurado   | Antes del primer commit                 |
| Base de datos local      | SQLite                                  |
| Base de datos producción | [PostgreSQL / MySQL / SQLite]           |

---

## Señales y Lógica de Negocio

| Decisión            | Valor elegido                    |
| ------------------- | -------------------------------- |
| Usa signals         | [Sí / No]                        |
| Lógica en modelos   | [Sí — métodos en el modelo / No] |
| Lógica en servicios | [Sí — capa de servicios / No]    |

---

## Tests

| Decisión           | Valor elegido                           |
| ------------------ | --------------------------------------- |
| Tests obligatorios | [Sí / No]                               |
| Qué se testea      | [Modelos / Vistas / Formularios / Todo] |
| Ubicación de tests | [tests.py por app / carpeta tests/]     |

---

## Apps del proyecto

| App     | Responsabilidad principal |
| ------- | ------------------------- |
| [app 1] | [descripción breve]       |
| [app 2] | [descripción breve]       |
| [app 3] | [descripción breve]       |

---

## Convenciones de nomenclatura

- Modelos: `PascalCase` en singular (`Product`, `Order`)
- Vistas FBV: `snake_case` con acción al final (`product_list`, `product_detail`)
- Vistas CBV: `PascalCase` con sufijo `View` (`ProductListView`)
- URLs: `kebab-case` (`/product-list/`, `/order-detail/`)
- Templates: `snake_case.html` organizados por carpeta de app (`products/list.html`)
- Variables de entorno: `UPPER_SNAKE_CASE` (`DJANGO_SECRET_KEY`)
```

---

## 📋 Tabla resumen de toda la clase

| Decisión                 | Opciones                                   | Criterio para elegir                                  |
| ------------------------ | ------------------------------------------ | ----------------------------------------------------- |
| Estructura de carpetas   | Plana / Multi-App / Multi-Entorno          | Propósito y escalabilidad del proyecto                |
| Carpeta de configuración | `config/` / `core/` / mismo nombre app     | `config/` — neutro y descriptivo                      |
| Nomenclatura de apps     | Inglés plural / Español singular / Mezcla  | Inglés plural, siempre consistente                    |
| Idioma del código        | Inglés / Español / Mezcla                  | Inglés para código, equipo para comentarios           |
| Ubicación de templates   | En cada app / Centralizados                | Centralizados salvo que la app sea reutilizable       |
| Modelo de usuario        | Default `User` / `AbstractUser`            | `AbstractUser` siempre, antes de la primera migración |
| Sistema de roles         | Groups / Campo role / Decoradores simples  | Según complejidad del control de acceso               |
| Protección de vistas     | Sin protección / `@login_required` / Mixin | Definir cuál es la regla base del proyecto            |
| Soft delete              | Hard delete / `is_active`                  | `is_active` en modelos de negocio críticos            |
| Señales (signals)        | Con signals / Sin signals                  | Usar para efectos colaterales entre apps              |
| Namespaces en URLs       | Con / Sin                                  | Siempre con namespaces                                |
| Estilo de vistas         | FBV / CBV / Mixto                          | Elegir uno y aplicarlo consistentemente               |
| Variables de entorno     | Hardcodeadas / `.env`                      | `.env` desde el día 1                                 |
| Tests                    | Opcionales / Obligatorios                  | Definir qué se testea antes de que el proyecto crezca |
| Media                    | Sin media / Con media configurado          | Configurar desde el inicio si hay uploads             |

---

> 🚀 _"Todo desarrollador senior fue primero alguien que aprendió que la arquitectura no se improvisa: se decide, se documenta y se respeta. Y cuando volvés a ese proyecto seis meses después — o cuando se lo pasás a una IA — ese documento vale más que mil líneas de código."_

---
