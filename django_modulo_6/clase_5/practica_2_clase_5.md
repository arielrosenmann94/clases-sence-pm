# 🏗️ Django — Módulo 6 · Clase 5

## Práctica C — "Detecta, Corrige y Decide"

---

> _"Los errores de arquitectura más costosos no se ven en pantalla. Se ven seis meses después cuando el proyecto no puede crecer."_

---

## Consigna — Dos etapas

Esta práctica tiene **dos partes que se hacen en orden**:

1. **ETAPA 1:** Analizás un proyecto existente con problemas de arquitectura, detectás los errores y los corregís.
2. **ETAPA 2:** Con el proyecto ya corregido en mente, completás el Documento de Decisiones como si fueras el arquitecto que lo diseñó desde cero.

---

---

# ETAPA 1: Detecta y Corrige los problemas

---

## El proyecto: "GestorAlke"

Un equipo recibió el siguiente proyecto Django heredado. El sistema gestiona **empleados, liquidaciones de sueldo y reportes de presentismo** para una empresa mediana.

A continuación se muestra la estructura de carpetas, los archivos de configuración y algunos modelos. Analizá todo con atención.

---

### Estructura de carpetas

```text
GestorAlke/
│
├── GestorAlke/                  ← Carpeta de configuración
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── empleados/                   ← App de empleados
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── lista_empleados.html
│
├── Liquidaciones/               ← App de liquidaciones
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── lista.html
│       └── detalle.html
│
├── reportes/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── static/
│   └── estilos.css
│
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

### `settings.py`

```python
SECRET_KEY = 'django-insecure-abc123supersecretakey99'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestoralke_db',
        'USER': 'postgres',
        'PASSWORD': 'admin1234',
        'HOST': 'localhost',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'empleados',
    'Liquidaciones',
    'reportes',
]

STATIC_URL = '/static/'
```

---

### `empleados/models.py`

```python
from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    last_salary = models.FloatField()
    fecha_ingreso = models.DateField()
    dni = models.IntegerField()
    activo = models.BooleanField()
    foto = models.ImageField()
```

---

### `liquidaciones/models.py`

```python
from django.db import models

class Liquidacion(models.Model):
    empleado_id = models.IntegerField()     # Guarda el ID del empleado a mano
    monto = models.FloatField()
    periodo = models.CharField(max_length=50)
    pagado = models.BooleanField()
```

---

### `reportes/views.py`

```python
from django.shortcuts import render
from empleados.models import Empleado

def reporte_general(request):
    empleados = Empleado.objects.all()
    return render(request, 'reportes/general.html', {'empleados': empleados})

def reporte_mensual(request):
    empleados = Empleado.objects.all()
    return render(request, 'reportes/mensual.html', {'empleados': empleados})
```

---

### `empleados/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:id>/', views.detalle, name='detalle'),
]
```

### `liquidaciones/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:id>/', views.detalle, name='detalle'),
]
```

---

### No existe ningún archivo `.gitignore` en el repositorio.

### No existe ningún archivo `.env`.

---

## Tu tarea — Etapa 1

Completa la siguiente tabla con **todos los problemas que encontrás**. Para cada uno indica dónde está el error, cuál es el problema y cómo lo corregirías.

| #   | Ubicación del error | ¿Qué está mal? | ¿Cómo lo corregís? |
| --- | ------------------- | -------------- | ------------------ |
| 1   |                     |                |                    |
| 2   |                     |                |                    |
| 3   |                     |                |                    |
| 4   |                     |                |                    |
| 5   |                     |                |                    |
| 6   |                     |                |                    |
| 7   |                     |                |                    |
| 8   |                     |                |                    |
| 9   |                     |                |                    |
| 10  |                     |                |                    |

> 💡 Hay más de 10 problemas distribuidos por el proyecto. Intentá encontrarlos todos.

---

---

# ETAPA 2: Completa el Documento de Decisiones

---

Ahora que corregiste el proyecto, completa el **Documento de Decisiones Arquitectónicas** como si hubieras diseñado GestorAlke desde cero y correctamente.

---

### Estructura

| Decisión                       | Tu elección |
| ------------------------------ | ----------- |
| Tipo de estructura             |             |
| Carpeta de configuración       |             |
| Carpeta de apps                |             |
| Ubicación de templates         |             |
| Settings separados por entorno |             |

---

### Apps del proyecto (con los nombres corregidos)

| App | Responsabilidad principal |
| --- | ------------------------- |
|     |                           |
|     |                           |
|     |                           |

---

### Código

| Decisión                 | Tu elección |
| ------------------------ | ----------- |
| Idioma del código fuente |             |
| Nomenclatura de apps     |             |
| Estilo de vistas         |             |
| Namespaces en URLs       |             |

---

### Modelos

| Decisión                        | Tu elección | 💬 Justificación |
| ------------------------------- | ----------- | ---------------- |
| Tipo de campo para sueldos      |             |                  |
| Relación Liquidación → Empleado |             |                  |
| Soft delete en Empleado         |             |                  |
| Campo `created_at`              |             |                  |

---

### Entorno y Seguridad

| Decisión                   | Tu elección |
| -------------------------- | ----------- |
| ¿`SECRET_KEY` en `.env`?   |             |
| ¿Datos de BD en `.env`?    |             |
| `.gitignore` creado cuándo |             |
| ¿`db.sqlite3` en el repo?  |             |

---

## ✍️ Pregunta de reflexión final

> Contestala en 3-5 líneas al pie de este documento.

**¿Cuál de todos los errores del proyecto original te parece el más grave y por qué? ¿Cuál hubiera sido el más difícil de corregir si el proyecto ya tuviera datos de producción?**

---

_Completá ambas etapas antes de que el instructor muestre la corrección._
