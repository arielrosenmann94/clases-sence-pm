# 🍦 Resumen Pedagógico: "Two Scoops of Django"

> **"Two Scoops of Django"** (por Daniel Feldroy y Audrey Roy Greenfeld) no es un libro para aprender Django desde cero. Es un libro sobre **cómo hacer las cosas correctamente** cuando ya se domina lo básico. Es la recopilación de años de errores y aciertos de dos de los desarrolladores más experimentados de la comunidad.

A continuación, se presenta un resumen de las enseñanzas más valiosas del libro, explicadas de forma sencilla y listas para aplicar en proyectos reales.

---

## 1. Regla de Oro: Manténgalo simple y estándar

Django tiene su manera de hacer las cosas (el "Django Way"). El libro insiste en que no se debe intentar reinventar la rueda ni luchar contra el framework.

- **No cree su propio sistema de usuarios** desde cero si puede extender el que provee Django.
- **No utilice microframeworks dentro de Django** para problemas que Django ya resuelve de manera eficiente (como usar SQLAlchemy en lugar del ORM de Django sin una justificación de peso).
- **Adopte las convenciones**: Si Django espera que las plantillas se ubiquen en una carpeta `templates`, colóquelas allí. Las convenciones ahorran tiempo de discusión y facilitan que nuevos desarrolladores comprendan su código en 5 minutos en lugar de 5 días.

---

## 2. La estructura del proyecto: El patrón "Core" o "Config"

El comando por defecto `django-admin startproject miproyecto` crea una carpeta `miproyecto/miproyecto`, lo cual resulta confuso porque mezcla el nombre del proyecto general con la carpeta de configuraciones.

**La recomendación de Two Scoops:**
Renombrar la carpeta interna de configuración a `config` o `core`.

```text
miproyecto/              ← Repositorio Git
├── manage.py
├── requirements.txt
├── config/              ← ⚙️ ¡AQUÍ van settings y urls globales!
│   ├── settings.py
│   └── urls.py
├── usuarios/            ← 📦 App
├── productos/           ← 📦 App
└── ventas/              ← 📦 App
```

¿Por qué? Porque elimina la redundancia y deja claro a simple vista dónde se encuentran las configuraciones globales.

---

## 3. Configuraciones (`settings`) en múltiples archivos

A medida que un proyecto crece, no es conveniente tener un único `settings.py` con las configuraciones del entorno local, las del servidor de pruebas y las de producción mezcladas con declaraciones `if / else`. Esto representa un riesgo significativo (por ejemplo, borrar la base de datos de producción por error).

**La recomendación:**
Crear un directorio `settings/` y dividir las configuraciones:

```text
config/
└── settings/
    ├── __init__.py
    ├── base.py       ← Configuraciones comunes (INSTALLED_APPS, etc.)
    ├── local.py      ← Base de datos SQLite, DEBUG=True
    ├── test.py       ← Para ejecutar pruebas automatizadas
    └── production.py ← PostgreSQL, DEBUG=False, contraseñas seguras
```

---

## 4. El mantra: "Fat Models, Thin Views" (Modelos robustos, Vistas delgadas)

Esta es probablemente **la regla arquitectónica más importante** del libro.

**El problema:**
Los desarrolladores principiantes suelen colocar toda la lógica (cálculos matemáticos, validaciones complejas, envío de correos electrónicos) dentro de `views.py`. Esto provoca que las vistas sean excesivamente extensas y muy difíciles de probar.

**La solución de Two Scoops:**
Mueva la "lógica de negocio" a métodos específicos dentro de sus clases en `models.py`.

**❌ Incorrecto (Lógica en la Vista):**

```python
def procesar_compra(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if producto.stock > 0 and producto.activo:
        # 20 líneas de código calculando impuestos,
        # descontando stock, enviando un correo electrónico...
```

**✅ Correcto (Lógica en el Modelo):**

```python
# models.py
class Producto(models.Model):
    # campos...
    def hay_stock_y_esta_activo(self):
        return self.stock > 0 and self.activo

    def procesar_compra_y_notificar(self, usuario):
        # La lógica compleja se ubica aquí

# views.py
def procesar_compra(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    if producto.hay_stock_y_esta_activo():
        producto.procesar_compra_y_notificar(request.user)
```

**Resultado:** Vistas que son fáciles de leer (le indican al modelo _qué_ hacer) y modelos independientes que saben _cómo_ hacerlo.

---

## 5. Diseño de Apps: Pequeñas y con un propósito único

Una "App" en Django no equivale al proyecto entero. Es un componente que realiza **una sola tarea de manera eficiente**.

**La regla general:**
Si el nombre de su aplicación es genérico como `core`, `main`, o `general` (y agrupa múltiples funcionalidades distintas), el diseño es incorrecto. Si su aplicación se denomina `usuarios_y_pagos_y_notificaciones`, también es incorrecto.

**Ejemplos de aplicaciones bien definidas:**

- `usuarios` (gestiona el registro y los perfiles)
- `productos` (gestiona el catálogo)
- `pagos` (gestiona la facturación)

Si una aplicación contiene más de 10 a 15 modelos, probablemente sea necesario dividirla en dos o tres unidades más pequeñas.

---

## 6. Secretos fuera del control de versiones (Git)

**¡Nunca exponga contraseñas, claves de API o la `SECRET_KEY` de Django a repositorios como GitHub!**

**La recomendación de Two Scoops:**
Utilice variables de entorno. Herramientas como `django-environ` o `python-decouple` permiten leer configuraciones sensibles desde un archivo `.env` que debe mantenerse **fuera** del control de versiones (añadiéndolo al archivo `.gitignore`).

```python
# settings.py
import environ

env = environ.Env()
# Lee de un archivo .env si este existe
environ.Env.read_env()

# Si el valor no se encuentra en el .env, se produce un error (esto es seguro)
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
```

---

## 7. Modelos: TimeStampedModel y orden

**El problema:** En la gran mayoría de los proyectos, casi todas las tablas requieren registrar _cuándo_ se creó un registro y _cuándo_ fue modificado por última vez. Declarar estos dos campos repetidamente es tedioso y propenso a errores u olvidos.

**La solución:** Crear una clase abstracta base y heredar de ella.

```python
# core/models.py
from django.db import models

class TimeStampedModel(models.Model):
    """
    Una clase base abstracta que provee los campos
    'creado_en' y 'modificado_en' a los modelos que la hereden.
    """
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # Esto indica a Django: No cree una tabla real para este modelo

# productos/models.py
class Producto(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    # Al heredar, la clase Producto obtiene automáticamente creado_en y modificado_en
```

---

## 8. Evite las importaciones con asterisco (`import *`)

Utilizar dependencias como `from .models import *` es una mala práctica en Python y el libro lo desaconseja estrictamente en el desarrollo con Django.

**¿Por qué?**

- Contamina el "espacio de nombres" (namespace).
- Si otro desarrollador revisa el código, no sabrá exactamente qué modelos se están utilizando en esa vista.
- Los entornos de desarrollo integrados (IDEs como Visual Studio Code o PyCharm) pierden capacidad para autocompletar o detectar errores adecuadamente.

**Utilice siempre importaciones explícitas:**
`from .models import Producto, Categoria`

---

## 9. Seguridad: Nunca confíe en el usuario final

- No utilice diccionarios de datos directos provenientes de `request.POST` o `request.GET` para ejecutar consultas a la base de datos sin antes validarlos empleando **Formularios de Django** o **Serializadores (en Django REST Framework)**.
- Los formularios no se limitan a generar campos de texto en HTML; su función principal y más poderosa es **limpiar y validar datos**.

---

## Resumen Final

_Two Scoops of Django_ se fundamenta en **la coherencia y la facilidad de mantenimiento**. El código que se escribe hoy será revisado por otra persona (o por usted mismo) meses más adelante. Si respeta las convenciones del framework (el "Django Way"), organiza adecuadamente las configuraciones, mantiene vistas ligeras, aplicaciones específicas y protege las credenciales, su proyecto podrá mantenerse y escalar durante años sin transformarse en un sistema difícil de comprender o actualizar ("código espagueti").
