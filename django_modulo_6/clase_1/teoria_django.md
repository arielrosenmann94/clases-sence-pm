# 🐍 Django — Módulo 6 · Teoría Completa

### AE6.1: Características fundamentales del framework Django

---

## 1. Historia y contexto de Django

Django nació en **2003** dentro de la redacción del periódico Lawrence Journal-World en Kansas, Estados Unidos. Los programadores Adrian Holovaty y Simon Willison lo desarrollaron para poder publicar contenido periodístico de forma ágil. En **2005** fue liberado como software libre bajo la licencia BSD y comenzó su expansión global.

El nombre proviene del guitarrista de jazz **Django Reinhardt**, símbolo de elegancia y virtuosismo — valores que el framework busca transmitir en el código.

### Línea de tiempo — hitos clave

#### 🏗️ 2003 — Nacimiento interno

Adrian Holovaty y Simon Willison crean Django dentro del periódico Lawrence Journal-World para agilizar la publicación de noticias bajo presión editorial. Era una herramienta interna, no un proyecto concebido para el mundo exterior.

#### 🌐 2005 — Open source

Django se publica bajo la licencia BSD y queda disponible para toda la comunidad Python. El código fuente abierto impulsó miles de contribuidores y proyectos, convirtiendo una herramienta periodística en un estándar de la industria.

#### 🎯 2008 — Django 1.0 — primera versión estable

Tres años de uso en producción dieron paso a la primera versión estable. Se consolidan el ORM, el panel de administración automático y el sistema de templates: los tres pilares que definen a Django hasta hoy.

#### 🔗 2010 — Django 1.2 — soporte multi-base de datos

Se introduce la capacidad de conectar múltiples bases de datos en un mismo proyecto. Una app puede leer de PostgreSQL y escribir en MySQL simultáneamente, abriendo Django a arquitecturas empresariales más complejas.

#### 🐍 2017 — Django 2.0 — solo Python 3

Django abandona Python 2 de forma definitiva, simplificando el sistema de URLs con tipos declarativos (`<int:id>`, `<str:slug>`). Una ruptura limpia que modernizó el ecosistema y eliminó años de deuda técnica.

#### ⚡ 2019 — Django 3.0 — soporte asíncrono ASGI

**ASGI** (Asynchronous Server Gateway Interface) es el protocolo de comunicación entre el servidor web y la aplicación Python. Reemplaza a **WSGI**, el estándar anterior que solo podía manejar **una solicitud a la vez por hilo**.

|                                      | WSGI (anterior)       | ASGI (nuevo)                            |
| ------------------------------------ | --------------------- | --------------------------------------- |
| Modelo                               | Un hilo por solicitud | Un proceso atiende miles de solicitudes |
| WebSockets                           | ❌                    | ✅                                      |
| HTTP/2                               | ❌                    | ✅                                      |
| Chat / notificaciones en tiempo real | ❌                    | ✅                                      |
| Alta concurrencia                    | Limitada              | ✅                                      |

> 🏦 **Analogía:** WSGI es como un banco con un cajero: atiende a uno, el resto espera en fila. ASGI es como una app de mensajería: gestiona miles de conversaciones simultáneas sin que una bloquee a las demás.

Con Django 3.0 se dio el primer paso. Eso habilitó luego las vistas `async/await` en Django 4.x y el sistema de Background Tasks nativo en Django 6.0.

#### 🔒 2022 — Django 4.0 — seguridad y modernización

Mejoras en la protección CSRF, soporte de zona horaria por usuario y rediseño visual del panel admin. Se profundiza el soporte async en vistas y middleware, haciendo la programación asíncrona más accesible para desarrolladores comunes.

#### 🧩 2024 — Django 5.0 — faceted filtering y field groups

El admin gana filtros con conteo de registros por opción. Se introducen los "field groups" para agrupar campos relacionados en formularios. Soporte nativo para claves primarias compuestas en modelos con relaciones complejas.

#### 🌟 Abril 2025 — Django 5.2 LTS — largo plazo

Versión LTS (Long Term Support) con soporte garantizado hasta **abril de 2028**. Es la versión recomendada para proyectos en producción que priorizan la estabilidad sobre incorporar las últimas novedades del framework.

#### 🚀 Diciembre 2025 — Django 6.0 — la versión actual

Lanzado el **3 de diciembre de 2025**, Django 6.0 incorpora tareas en segundo plano nativas, Content Security Policy integrado, template partials y una API de email modernizada. Requiere Python 3.12 o superior.

---

## 2. ¿Qué es Django?

Django es un **framework de desarrollo web de alto nivel** escrito en Python. Su objetivo es permitir el desarrollo **rápido, limpio y pragmático** de aplicaciones web, minimizando el código repetitivo.

Su lema oficial es:

> _"The web framework for perfectionists with deadlines."_
> ("El framework web para perfeccionistas con fechas de entrega.")

### Filosofía: "Baterías incluidas"

A diferencia de microframeworks como Flask, Django viene con todo lo necesario desde el primer momento:

| Componente               | ¿Qué hace?                                               |
| ------------------------ | -------------------------------------------------------- |
| ORM                      | Interactúa con la BD sin escribir SQL                    |
| Panel Admin              | Interfaz de gestión automática para los modelos          |
| Sistema de autenticación | Login, logout, permisos, grupos, usuarios                |
| Sistema de templates     | Motor de plantillas HTML con lógica integrada            |
| Sistema de formularios   | Generación y validación de formularios                   |
| Sistema de URLs          | Enrutamiento declarativo y limpio                        |
| Sistema de migraciones   | Versionado automático del esquema de BD                  |
| Seguridad integrada      | Protección contra XSS, CSRF, SQL Injection, Clickjacking |
| Caché                    | Sistema de caché configurable (memoria, Redis, etc.)     |

---

## 3. Arquitectura Modelo-Vista-Template (MVT)

### ¿Qué es un patrón de arquitectura?

Un patrón de arquitectura es una **forma organizada de dividir el código** de una aplicación según su responsabilidad. Esto facilita el mantenimiento, la escalabilidad y el trabajo en equipo.

Django usa el patrón **MVT**, una variante del clásico **MVC** (Modelo-Vista-Controlador).

### Comparación MVT vs MVC

| Concepto en MVC | Equivalente en Django (MVT) | Responsabilidad                     |
| --------------- | --------------------------- | ----------------------------------- |
| Modelo          | **Modelo** (`models.py`)    | Datos y lógica de negocio con la BD |
| Controlador     | **Vista** (`views.py`)      | Lógica de la solicitud HTTP         |
| Vista           | **Template** (`*.html`)     | Presentación al usuario             |
| Router          | **URLs** (`urls.py`)        | Enrutamiento de solicitudes         |

> 💡 En Django, el "Controlador" de MVC se llama "Vista", y la "Vista" de MVC se llama "Template". El framework maneja el routing por su cuenta, por eso se llama MVT y no MVC.

### Flujo completo de una solicitud

```
┌────────────────────────────────────────────────────────────┐
│                    CICLO DE UNA PETICIÓN                   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. Navegador  ──── GET /productos/ ──▶  urls.py           │
│                                              │             │
│  2. urls.py  ─── coincide path() ──▶  views.py            │
│                                              │             │
│  3. views.py  ─── consulta ORM ──▶  models.py             │
│                                              │             │
│  4. models.py  ─── query SQL ──▶  Base de Datos           │
│                                              │             │
│  5. BD  ─── devuelve registros ──▶  views.py              │
│                                              │             │
│  6. views.py  ─── render() ──▶  template.html             │
│                                              │             │
│  7. template.html  ─── HTML generado ──▶  Navegador       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Responsabilidades de cada capa

#### 🗄️ Modelo (`models.py`)

- Define la **estructura de los datos** (tablas, columnas, relaciones).
- Contiene la **lógica de negocio** relacionada con los datos.
- Se comunica con la base de datos a través del **ORM**.
- Es completamente **independiente** de la presentación.

#### ⚙️ Vista (`views.py`)

- Es el **punto de entrada** de cada solicitud HTTP.
- Decide **qué datos** consultar y **cómo procesarlos**.
- Llama al modelo cuando necesita datos.
- Llama al template cuando quiere devolver una respuesta HTML.
- También puede devolver JSON, archivos, redirecciones, etc.

#### 🖼️ Template (`*.html`)

- Es un archivo HTML que puede incluir **lógica básica** (bucles, condicionales).
- Recibe datos de la vista a través de un **contexto** (diccionario Python).
- Usa el **Django Template Language (DTL)** para mostrar los datos.
- No contiene lógica de negocio; solo presentación.

#### 🗺️ URLs (`urls.py`)

- Define el **mapa de rutas** del sitio.
- Asocia patrones de URL con funciones de vista.
- Soporta captura de parámetros dinámicos (ej: `/productos/42/`).
- Permite organizar rutas por app con `include()`.

---

## 4. El ORM de Django — Object Relational Mapping

El **ORM** (Mapeo Objeto-Relacional) de Django permite interactuar con la base de datos usando Python en lugar de SQL.

### Analogía

Imaginá que la base de datos es un archivo de Excel con filas y columnas. El ORM te permite trabajar con esas filas como si fueran **objetos Python**, sin tener que abrir el Excel manualmente ni escribir fórmulas complejas.

### Comparación SQL vs ORM

| Operación     | SQL puro                                       | Django ORM                                                 |
| ------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| Obtener todos | `SELECT * FROM producto;`                      | `Producto.objects.all()`                                   |
| Filtrar       | `SELECT * FROM producto WHERE precio < 100;`   | `Producto.objects.filter(precio__lt=100)`                  |
| Obtener uno   | `SELECT * FROM producto WHERE id=1;`           | `Producto.objects.get(id=1)`                               |
| Crear         | `INSERT INTO producto VALUES (...);`           | `Producto.objects.create(nombre='...', precio=99)`         |
| Actualizar    | `UPDATE producto SET nombre='...' WHERE id=1;` | `p = Producto.objects.get(id=1); p.nombre='...'; p.save()` |
| Eliminar      | `DELETE FROM producto WHERE id=1;`             | `Producto.objects.get(id=1).delete()`                      |

### Tipos de campos en los modelos

| Campo                                      | Tipo de dato         | Uso típico                 |
| ------------------------------------------ | -------------------- | -------------------------- |
| `CharField(max_length=n)`                  | Texto corto          | Nombres, títulos           |
| `TextField()`                              | Texto largo          | Descripciones, contenido   |
| `IntegerField()`                           | Número entero        | Cantidades, edades         |
| `DecimalField(max_digits, decimal_places)` | Decimal              | Precios, porcentajes       |
| `BooleanField()`                           | Verdadero/Falso      | Estados, activación        |
| `DateField()`                              | Fecha                | Nacimiento, vencimiento    |
| `DateTimeField()`                          | Fecha y hora         | Timestamps, creación       |
| `ForeignKey()`                             | Clave foránea        | Relación muchos-a-uno      |
| `ManyToManyField()`                        | Relación N:N         | Tags, categorías múltiples |
| `OneToOneField()`                          | Relación 1:1         | Perfil de usuario          |
| `EmailField()`                             | Email con validación | Correos electrónicos       |
| `URLField()`                               | URL con validación   | Sitios web, imágenes       |
| `ImageField()`                             | Ruta de imagen       | Fotos de perfil, portadas  |

---

## 5. Migraciones — El sistema de versionado de la base de datos

### ¿Qué es una migración?

Una migración es un **archivo Python generado automáticamente** que describe los cambios que deben aplicarse al esquema de la base de datos. Funciona como un **sistema de control de versiones** (similar a Git) pero para la estructura de la BD.

### ¿Por qué existen las migraciones?

Sin migraciones, cada vez que modificaras un modelo tendrías que:

1. Conectarte manualmente a la base de datos.
2. Escribir el SQL de `ALTER TABLE`, `CREATE TABLE`, `DROP COLUMN`, etc.
3. Asegurarte de hacerlo en todos los entornos (desarrollo, staging, producción).
4. Coordinar esto con el equipo de trabajo.

Las migraciones automatizan todo ese proceso.

### El flujo de migraciones

```
1. Modificás models.py  (ejemplo: agregás un campo nuevo)
        ↓
2. python manage.py makemigrations
   → Django detecta el cambio
   → Genera un archivo en tareas/migrations/0002_tarea_prioridad.py
        ↓
3. python manage.py migrate
   → Django lee el archivo de migración
   → Ejecuta el SQL correspondiente en la BD
   → Registra que esa migración ya fue aplicada
```

### Anatomía de un archivo de migración

```python
# tareas/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []   # depende de otras migraciones anteriores

    operations = [
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),  # generado automáticamente
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('completada', models.BooleanField(default=False)),
                ('creada_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
```

> ⚠️ Nunca edites los archivos de migración a mano salvo que sepas exactamente lo que haces. Están pensados para ser generados automáticamente.

### Comandos esenciales de migraciones

| Comando                                | ¿Qué hace?                                                    |
| -------------------------------------- | ------------------------------------------------------------- |
| `python manage.py makemigrations`      | Detecta cambios en los modelos y genera archivos de migración |
| `python manage.py migrate`             | Aplica todas las migraciones pendientes a la BD               |
| `python manage.py showmigrations`      | Lista todas las migraciones y cuáles ya fueron aplicadas      |
| `python manage.py sqlmigrate app 0001` | Muestra el SQL que genera una migración específica            |
| `python manage.py migrate app 0001`    | Revierte al estado de una migración anterior                  |

### ¿Qué pasa si no corro `makemigrations` después de cambiar un modelo?

Django no aplica ningún cambio a la BD. Si intentás usar el nuevo campo o tabla, obtendrás un error porque la BD no tiene esa estructura todavía. Las migraciones son el **puente** entre el código Python y la base de datos real.

---

## 6. El Panel de Administración

El panel `admin` es una de las características que distingue a Django de otros frameworks. Con solo dos líneas de código, tienes una interfaz web completa para gestionar todos tus datos.

### ¿Qué permite hacer el admin?

- Crear, leer, modificar y eliminar registros (CRUD completo).
- Buscar y filtrar registros.
- Gestionar usuarios, grupos y permisos.
- Visualizar relaciones entre modelos.
- Exportar datos.

### Personalización del admin

Django Admin es altamente personalizable. Se puede controlar qué columnas se muestran, qué campos son filtrables, qué campos son buscables, etc.:

```python
# admin.py personalizado
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'precio', 'disponible')   # columnas en la lista
    list_filter   = ('disponible',)                       # filtros laterales
    search_fields = ('nombre', 'descripcion')             # barra de búsqueda
    ordering      = ('nombre',)                           # orden por defecto
```

---

## 7. Seguridad integrada en Django

Django protege automáticamente contra los ataques web más comunes:

| Vulnerabilidad                        | ¿Qué es?                                 | ¿Cómo Django la previene?                       |
| ------------------------------------- | ---------------------------------------- | ----------------------------------------------- |
| **SQL Injection**                     | Insertar SQL malicioso en una consulta   | El ORM escapa automáticamente todos los valores |
| **XSS** (Cross-Site Scripting)        | Inyectar JavaScript en la página         | Los templates escapan el contenido por defecto  |
| **CSRF** (Cross-Site Request Forgery) | Falsificar solicitudes desde otro sitio  | Token CSRF obligatorio en los formularios       |
| **Clickjacking**                      | Embeber la página en un iframe malicioso | Header `X-Frame-Options` automático             |
| **Contraseñas**                       | Almacenarlas en texto plano              | Hashing seguro con PBKDF2, bcrypt, Argon2       |

---

## 8. Ventajas de Django en el mundo profesional

### Para el desarrollador

- **Velocidad de desarrollo**: Lo que en otro framework tomaría semanas, en Django puede hacerse en días.
- **Convenciones claras**: La estructura de proyecto es estándar. Cualquier desarrollador Django se orienta rápidamente en un proyecto nuevo.
- **Documentación excepcional**: Considerada una de las mejores de cualquier framework web.
- **Comunidad activa**: Millones de desarrolladores, paquetes de terceros (`django-rest-framework`, `django-allauth`, `django-debug-toolbar`, etc.).

### Para la empresa

- **Seguridad out of the box**: Reduce el riesgo de vulnerabilidades por descuido.
- **Escalabilidad**: Instagram, Pinterest, Disqus, Mozilla y National Geographic usan o usaron Django.
- **ORM multi-base de datos**: SQLite en desarrollo, PostgreSQL en producción, sin cambiar el código.
- **Admin gratuito**: Ahorra semanas de desarrollo para interfaces internas.

### Casos de uso ideales

- Aplicaciones web con base de datos relacional.
- APIs REST (especialmente con Django REST Framework).
- CMS y portales de contenido.
- Sistemas de gestión empresarial (ERP, CRM).
- E-commerce y plataformas de marketplace.

---

## 9. Django 5 y Django 6 — Actualidad del framework

> 📅 **Django 6.0** fue lanzado el **3 de diciembre de 2025** y es la versión más reciente. **Django 5.2 LTS** (abril 2025) es la recomendada para producción con soporte hasta abril de 2028.

---

### Novedades de Django 5.x (2024-2025)

#### Faceted filtering en el Admin (Django 5.0)

El panel de administración ahora muestra cuántos registros corresponden a cada opción de filtro. Si filtrás por "disponible", ves `Sí (12) / No (3)`. Facilita enormemente la navegación en tablas con miles de registros.

```python
class ProductoAdmin(admin.ModelAdmin):
    list_filter = ('disponible', 'categoria')
    show_facets = admin.ShowFacets.ALWAYS   # ← nuevo en Django 5.0
```

#### Field groups en formularios (Django 5.0)

Permite agrupar campos relacionados bajo una misma etiqueta visual en los templates, simplificando formularios complejos como rangos de fechas o pares de campos que conceptualmente van juntos.

#### Claves primarias compuestas (Django 5.0)

Django permite definir que la unicidad de un registro esté dada por la combinación de varios campos, sin necesidad de un `id` autoincremental. Útil para tablas de relación o bases de datos heredadas.

#### Django 5.2 LTS — Versión de largo plazo

Lanzado en **abril de 2025**, recibe soporte de seguridad hasta **abril de 2028**. Es la versión recomendada para proyectos empresariales que necesitan estabilidad a largo plazo.

---

### Novedades de Django 6.0 — Lanzado el 3 de diciembre de 2025

Django 6.0 es la versión **más reciente y actual** del framework. Sus cambios más importantes:

#### 🔄 Framework de tareas en segundo plano (Background Tasks)

Django incorpora por primera vez un sistema nativo para ejecutar código fuera del ciclo HTTP, sin necesidad de instalar Celery para casos simples como enviar emails o procesar datos.

```python
# Django 6.0 — tareas nativas
from django.tasks import background_task

@background_task
def enviar_email_bienvenida(usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.enviar_bienvenida()
```

> 💡 No reemplaza a Celery para flujos complejos, pero elimina la dependencia externa para casos sencillos.

#### 🛡️ Soporte nativo de Content Security Policy (CSP)

Django 6.0 incluye soporte integrado para la cabecera HTTP `Content-Security-Policy`, que previene ataques XSS bloqueando la carga de scripts o recursos no autorizados. Antes requería paquetes de terceros.

```python
# settings.py — Django 6.0
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src":  ["'self'"],
    }
}
```

#### 🧩 Template Partials

El Django Template Language incorpora soporte para **fragmentos reutilizables** dentro de un mismo archivo de template. Permite encapsular porciones de HTML con nombre, haciendo los templates más modulares.

```html
{% partialdef card_producto %}
<div class="card">
  <h3>{{ producto.nombre }}</h3>
  <p>${{ producto.precio }}</p>
</div>
{% endpartialdef %} {# Se usa así en cualquier parte del template: #} {% partial
card_producto with producto=p %}
```

#### 📧 API de Email modernizada

Django 6.0 reemplaza la vieja API de email por `email.message.EmailMessage` nativa de Python moderno. Ofrece mejor manejo de Unicode, adjuntos y headers, con una interfaz más limpia y consistente.

#### 🐍 Python 3.12+ requerido

Django 6.0 **elimina el soporte para Python 3.10 y 3.11** y requiere como mínimo Python 3.12. Esto permite aprovechar mejoras de rendimiento y las nuevas características del lenguaje moderno.

#### ⚡ AsyncPaginator y AsyncPage

Se agregan clases de paginación asíncrona para consultas que devuelven grandes volúmenes de datos, completando el soporte async iniciado en versiones anteriores.

---

### Tabla comparativa — evolución de Django

| Característica              | Django 4.x     | Django 5.x     | Django 6.0 ✅  |
| --------------------------- | -------------- | -------------- | -------------- |
| Python mínimo               | 3.8            | 3.10           | **3.12**       |
| ORM async                   | Básico         | Mejorado       | AsyncPaginator |
| Admin facets                | ❌             | ✅             | ✅             |
| Field groups en forms       | ❌             | ✅             | ✅             |
| Background tasks nativo     | ❌             | ❌             | **✅**         |
| Content Security Policy     | ❌ (3rd party) | ❌ (3rd party) | **✅ nativo**  |
| Template Partials           | ❌             | ❌             | **✅**         |
| API de Email moderna        | ❌             | ❌             | **✅**         |
| Claves primarias compuestas | Limitado       | ✅             | ✅             |

---

### Ciclo de vida de versiones

| Versión              | Lanzamiento    | Soporte hasta  |
| -------------------- | -------------- | -------------- |
| Django 4.2 LTS       | Abril 2023     | Abril 2026     |
| Django 5.0           | Diciembre 2023 | Agosto 2025    |
| Django 5.1           | Agosto 2024    | Abril 2026     |
| Django 5.2 LTS ⭐    | Abril 2025     | **Abril 2028** |
| Django 6.0 🆕        | Diciembre 2025 | Agosto 2026    |
| Django 6.1 (próximo) | Agosto 2026    | —              |

> ⭐ **Para producción:** Django 5.2 LTS — estabilidad y soporte extendido hasta 2028.
> 🆕 **Más reciente:** Django 6.0 para proyectos nuevos que quieran las últimas características.

---

## 10. El ecosistema Django

Django no existe solo. A su alrededor existe un ecosistema rico de paquetes que extienden sus capacidades:

| Paquete                         | ¿Para qué sirve?                                        |
| ------------------------------- | ------------------------------------------------------- |
| `djangorestframework`           | Construir APIs REST robustas                            |
| `django-allauth`                | Autenticación social (Google, GitHub, etc.)             |
| `django-debug-toolbar`          | Panel de depuración para desarrollo                     |
| `celery` + `django-celery-beat` | Tareas en segundo plano y programadas                   |
| `django-storages`               | Almacenamiento en la nube (S3, GCS, etc.)               |
| `django-filter`                 | Filtros avanzados para vistas y APIs                    |
| `django-crispy-forms`           | Renderizado elegante de formularios                     |
| `Pillow`                        | Procesamiento de imágenes (necesario para `ImageField`) |
| `psycopg2`                      | Driver para PostgreSQL                                  |
| `whitenoise`                    | Servir archivos estáticos en producción                 |

---

## 📚 Referencias

- 📖 [Django Official Documentation](https://docs.djangoproject.com/en/)
