# 🏗️ Django — Módulo 6 · Clase 5

## Corrección y Justificación — Prácticas A y C

---

> _Este documento es para el instructor y para los estudiantes después de completar las prácticas. No leerlo antes de intentar resolverlas._

---

---

# CORRECCIÓN — PRÁCTICA A: "Arquitecto por un día" (ReservaFácil)

---

## Sobre el proyecto

ReservaFácil es una plataforma para que negocios gestionen turnos y clientes hagan reservas. Tiene roles diferenciados, va a producción desde el primer mes, va a tener app móvil en una segunda fase y maneja archivos de medios.

Estas condiciones ya determinan la mayoría de las decisiones.

---

## Documento de Decisiones — Respuesta correcta

### Estructura

| Decisión                       | Respuesta correcta                                   |
| ------------------------------ | ---------------------------------------------------- |
| Tipo de estructura             | **Multi-App con Environments (C)**                   |
| Carpeta de configuración       | `config/`                                            |
| Carpeta de apps                | `apps/`                                              |
| Ubicación de templates         | Centralizados en `templates/`                        |
| Settings separados por entorno | **Sí** — `base.py` / `local.py` / `production.py`    |
| Requirements separados         | **Sí** — `base.txt` / `local.txt` / `production.txt` |

**¿Por qué Estructura C?**
El brief dice explícitamente que el proyecto va a un servidor real desde el primer mes. Eso solo ya justifica settings separados. Sumar que va a tener app móvil (probablemente agregue DRF después) refuerza la decisión. Empezar con la Estructura B sería quedarse corto desde el diseño inicial.

---

### Apps del proyecto

| App             | Responsabilidad principal                           |
| --------------- | --------------------------------------------------- |
| `businesses`    | Registro y configuración de negocios (dueños)       |
| `services`      | Servicios ofrecidos (nombre, duración, precio)      |
| `bookings`      | Reservas: crear, confirmar, reprogramar, cancelar   |
| `users`         | Modelo de usuario personalizado + auth              |
| `notifications` | Envío de emails de confirmación (lógica de signals) |

**¿Por qué separar `notifications`?**
La lógica de emails puede crecer mucho (SMS, push, WhatsApp). Si está dentro de `bookings`, cualquier cambio en el canal de notificaciones requiere modificar la app de reservas. Separada, se puede modificar o reemplazar sin tocar el core de negocio.

**¿Por qué separar `businesses` de `services`?**
Un negocio puede tener muchos servicios. La gestión del negocio (nombre, dirección, foto, habilitación) es independiente de sus servicios (precio, duración). Si en el futuro se agrega categorías o búsqueda, se hace en `businesses` sin tocar `services`.

---

### Código

| Decisión                  | Respuesta correcta                    |
| ------------------------- | ------------------------------------- |
| Idioma del código fuente  | **Inglés**                            |
| Idioma de los comentarios | Español (idioma del equipo)           |
| Idioma del contenido UI   | Español (idioma del producto)         |
| Nomenclatura de apps      | **Inglés, plural, snake_case**        |
| Estilo de vistas          | CBV (proyecto con muchas vistas CRUD) |
| Namespaces en URLs        | **Sí, en todas las apps**             |

---

### Modelos

| Decisión                   | Respuesta correcta                         | Justificación                                                                                           |
| -------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| Campo `created_at`         | **Sí, en todos los modelos de negocio**    | Auditoría: saber cuándo se creó cada reserva, cada servicio, cada negocio                               |
| Campo `updated_at`         | **Sí, en todos los modelos de negocio**    | Detectar cambios sin necesitar historial completo                                                       |
| Soft delete (`is_active`)  | **Sí en `Business`, `Service`, `Booking`** | Una reserva cancelada no debe borrarse: puede necesitarse para reportes, disputas o estadísticas        |
| Tipo de campo para precios | **`DecimalField`**                         | `FloatField` tiene errores de precisión de punto flotante. `Decimal` es exacto para valores monetarios. |

---

### Autenticación y Permisos

| Decisión                       | Respuesta correcta                                               | Justificación                                                                                                                                 |
| ------------------------------ | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Modelo de usuario              | **`AbstractUser`**                                               | El brief ya menciona campos diferenciados por rol. Si usamos el User default y después queremos agregar campos, la migración es muy compleja. |
| `AUTH_USER_MODEL`              | `'users.User'`                                                   | Definido antes de la primera migración — esta ventana no se puede recuperar                                                                   |
| Campos extra en User           | `role`, `phone`, `avatar`                                        | Necesarios para diferencias entre tipos de usuario y para el perfil del negocio                                                               |
| Sistema de roles               | **Campo `role` con `TextChoices`**                               | Los tres roles tienen lógicas muy distintas. Los Groups de Django son para permisos por modelo, no para flujos de negocio tan diferenciados.  |
| Roles del sistema              | `ADMIN` / `BUSINESS_OWNER` / `CLIENT`                            | Los tres actores definidos en el brief                                                                                                        |
| Método de protección de vistas | `LoginRequiredMixin` + checks de `role` en cada vista de negocio | Toda vista de gestión de turnos y configuración del negocio requiere autenticación                                                            |

---

### Archivos de Medios

| Decisión                   | Respuesta correcta                 | Justificación                                                                              |
| -------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| Maneja archivos de medios  | **Sí**                             | El brief menciona explícitamente fotos de instalaciones y foto de perfil del local         |
| `MEDIA_URL` / `MEDIA_ROOT` | Configurados en `settings/base.py` | Deben estar disponibles en todos los entornos                                              |
| `upload_to` para fotos     | `'businesses/%Y/%m/'`              | Organiza por fecha para evitar carpetas enormes. En producción se redirige a S3 o similar. |

---

### Entorno y Configuración

| Decisión                 | Respuesta correcta               |
| ------------------------ | -------------------------------- |
| Variables de entorno     | `.env` con `python-dotenv`       |
| `.gitignore`             | Antes del primer commit          |
| Base de datos local      | SQLite (velocidad de desarrollo) |
| Base de datos producción | PostgreSQL                       |

---

### Signals

| Decisión          | Respuesta correcta       | Justificación                                                                                                                                                                                      |
| ----------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Usas signals?    | **Sí**                   | El brief dice que el email de confirmación es automático cuando se crea o modifica una reserva. Es el caso de uso ideal para signals: un efecto colateral en respuesta a un evento de otro modelo. |
| ¿Para qué evento? | `post_save` en `Booking` | Cuando el estado de la reserva cambia a `confirmed`, `rescheduled` o `cancelled`, se dispara el email.                                                                                             |

---

### Tests

| Decisión               | Respuesta correcta                                                                                                                |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| ¿Tests obligatorios?   | **Sí**                                                                                                                            |
| ¿Qué se testea mínimo? | `__str__` de todos los modelos, status 200 de todas las vistas públicas, flujo completo de reserva (crear → confirmar → cancelar) |

---

## Sobre la pregunta de reflexión

**Si el cliente dice que "es solo para probar la idea":**

Las decisiones que SÍ cambiarían:

- Settings separados → un solo `settings.py` (no hay entornos que gestionar todavía)
- Requirements separados → un solo `requirements.txt`
- PostgreSQL → SQLite local (más rápido de configurar)
- Estructura C → Estructura B o incluso A, según cuántos dominios realmente necesite el MVP

Las decisiones que NO cambiarían:

- `.env` para los secretos → aunque sea un prototipo, los secretos nunca van al repositorio
- `.gitignore` → siempre antes del primer commit
- `AbstractUser` → el costo de no hacerlo ahora puede ser inmenso después
- Nomenclatura consistente → el caos de nomenclatura no tiene relación con el propósito

---

---

# CORRECCIÓN — PRÁCTICA C: "Detecta, Corrige y Decide" (GestorAlke)

---

## ETAPA 1: Errores encontrados y su corrección

---

### Error 1 — Carpeta de configuración con el mismo nombre que el proyecto

**Ubicación:** Estructura de carpetas — `GestorAlke/GestorAlke/`

**¿Qué está mal?**
La carpeta de configuración tiene el mismo nombre que la carpeta raíz del proyecto. Es imposible distinguir a simple vista cuál es el paquete de la aplicación y cuál es la configuración.

**Corrección:**

```text
# ❌ Antes
GestorAlke/
    GestorAlke/        ← ambiguo

# ✅ Después
gestor_alke/
    config/            ← unívoco
```

**¿Por qué importa pedagógicamente?**
Esta es la primera confusión que tiene cualquier persona nueva que entra al proyecto. Una buena arquitectura permite orientarse en segundos, no en minutos.

---

### Error 2 — `SECRET_KEY` hardcodeada en `settings.py`

**Ubicación:** `settings.py` línea `SECRET_KEY = 'django-insecure-abc123...'`

**¿Qué está mal?**
La clave secreta de Django está escrita directamente en el código fuente. Si este archivo está en un repositorio (aunque sea privado), cualquier persona con acceso puede comprometer toda la seguridad del sistema.

**Corrección:**

```python
# .env
DJANGO_SECRET_KEY=django-insecure-abc123supersecretakey99

# settings.py
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

**¿Por qué importa pedagógicamente?**
Es un error de seguridad crítico, no de estilo. En producción, una `SECRET_KEY` expuesta puede comprometer las sesiones de todos los usuarios del sistema.

---

### Error 3 — Credenciales de base de datos hardcodeadas

**Ubicación:** `settings.py` — bloque `DATABASES`

**¿Qué está mal?**
El usuario y contraseña de PostgreSQL están en el código fuente. Si el repositorio se hace público por error (o si alguien del equipo cambia de empresa), esas credenciales quedan expuestas para siempre en el historial de git.

**Corrección:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
    }
}
```

---

### Error 4 — `DEBUG = True` sin control de entorno

**Ubicación:** `settings.py` — `DEBUG = True`

**¿Qué está mal?**
`DEBUG = True` muestra trazas de error completas en pantalla, incluyendo variables de entorno, rutas del servidor y configuración de la base de datos. Si este archivo llega a producción tal como está, cualquier error del sistema expone información sensible al usuario.

**Corrección:**

```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

---

### Error 5 — App `Liquidaciones` con mayúscula

**Ubicación:** Carpeta `Liquidaciones/` y `INSTALLED_APPS`

**¿Qué está mal?**
Las apps de Django siempre se nombran en **minúsculas**. `Liquidaciones` con L mayúscula viola la convención y puede causar problemas en sistemas de archivos case-sensitive (Linux en producción vs macOS en desarrollo).

**Corrección:**

```text
# ❌ Liquidaciones/
# ✅ liquidations/  (inglés, plural, minúsculas)
```

---

### Error 6 — Mezcla de idiomas en los nombres de campos

**Ubicación:** `empleados/models.py`

**¿Qué está mal?**
El modelo `Empleado` mezcla campos en español (`nombre`, `apellido`, `fecha_ingreso`) con un campo en inglés (`last_salary`). Esta inconsistencia dificulta leer el código y no cumple con ninguna convención definida.

**Corrección:**
Elegir **un solo idioma** y aplicarlo en todos los modelos. La convención recomendada es inglés:

```python
class Employee(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    ...
```

---

### Error 7 — Precios y montos en `FloatField`

**Ubicación:** `empleados/models.py` — `last_salary = models.FloatField()` y `liquidaciones/models.py` — `monto = models.FloatField()`

**¿Qué está mal?**
`FloatField` usa aritmética de punto flotante, que tiene errores de precisión. En el contexto de liquidaciones de sueldos, `3500.10 + 2800.90` puede dar `6300.9999999999995`. En sistemas financieros esto es inaceptable.

**Corrección:**

```python
salary = models.DecimalField(max_digits=10, decimal_places=2)
amount = models.DecimalField(max_digits=10, decimal_places=2)
```

**¿Por qué importa pedagógicamente?**
`DecimalField` existe precisamente para esto. Usar `FloatField` para dinero es un bug silencioso que puede no aparecer en desarrollo pero sí en producción con valores reales.

---

### Error 8 — Relación con `IntegerField` en lugar de `ForeignKey`

**Ubicación:** `liquidaciones/models.py` — `empleado_id = models.IntegerField()`

**¿Qué está mal?**
Guardar el ID del empleado como un número entero rompe la integridad referencial. Django no sabrá que ese número representa un empleado, no validará que exista, y no se podrá hacer consultas relacionadas (`liquidacion.employee.name`).

**Corrección:**

```python
from django.db import models
from apps.employees.models import Employee

class Liquidation(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,    # No borrar empleados con liquidaciones
        related_name='liquidations'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    ...
```

---

### Error 9 — Campos sin valores por defecto

**Ubicación:** `empleados/models.py` — `activo = models.BooleanField()`

**¿Qué está mal?**
Un `BooleanField` sin `default` obliga a especificar el valor manualmente en cada creación. Si no se especifica, Django lanza un error o usa `None`. La intención casi siempre es que un empleado nuevo empiece activo.

**Corrección:**

```python
is_active = models.BooleanField(default=True)
```

---

### Error 10 — `ImageField` sin `upload_to`

**Ubicación:** `empleados/models.py` — `foto = models.ImageField()`

**¿Qué está mal?**
Sin `upload_to`, todas las imágenes se guardan en la raíz de la carpeta `media/`. Con el tiempo se acumulan miles de archivos en un solo directorio, lo que degrada el rendimiento del sistema de archivos y hace imposible organizarlos.

**Corrección:**

```python
photo = models.ImageField(
    upload_to='employees/%Y/%m/',
    null=True,
    blank=True
)
```

---

### Error 11 — Colisión de nombres en URLs (sin namespaces)

**Ubicación:** `empleados/urls.py` y `liquidaciones/urls.py` — ambas tienen `name='lista'` y `name='detalle'`

**¿Qué está mal?**
Cuando dos apps tienen URLs con el mismo `name`, Django no puede distinguirlas. En los templates, `{% url 'lista' %}` podría apuntar a cualquiera de las dos dependiendo del orden en que están registradas en `config/urls.py`.

**Corrección:**

```python
# apps/employees/urls.py
app_name = 'employees'
urlpatterns = [
    path('', views.employee_list, name='list'),
    path('<int:pk>/', views.employee_detail, name='detail'),
]

# Template
{% url 'employees:list' %}
{% url 'liquidations:list' %}
```

---

### Error 12 — Ausencia de `.gitignore` y `db.sqlite3` en el repositorio

**Ubicación:** raíz del proyecto (no existe `.gitignore`)

**¿Qué está mal?**
Sin `.gitignore`, el archivo `db.sqlite3` (base de datos local con datos reales) y el entorno virtual pueden estar subidos al repositorio. La base de datos local puede contener datos de prueba sensibles y su presencia en el repo genera conflictos constantemente entre desarrolladores.

**Corrección:**

```gitignore
venv/
.env
db.sqlite3
__pycache__/
*.pyc
media/
staticfiles/
```

---

### Error 13 — Templates dentro de cada app sin estructura consistente

**Ubicación:** `empleados/templates/lista_empleados.html` vs `Liquidaciones/templates/lista.html`

**¿Qué está mal?**
No hay convención consistente de nombres. `lista_empleados.html` incluye el nombre de la app en el archivo; `lista.html` no. Además, los templates están dispersos dentro de cada app en lugar de estar centralizados.

**Corrección:**

```text
templates/
    employees/
        list.html
        detail.html
    liquidations/
        list.html
        detail.html
```

---

## ETAPA 2: Documento de Decisiones — Respuesta correcta

### Estructura

| Decisión                       | Respuesta correcta                                             |
| ------------------------------ | -------------------------------------------------------------- |
| Tipo de estructura             | Multi-App (B)                                                  |
| Carpeta de configuración       | `config/`                                                      |
| Carpeta de apps                | `apps/`                                                        |
| Ubicación de templates         | Centralizados en `templates/`                                  |
| Settings separados por entorno | Sí si va a producción; No si es uso interno solo en desarrollo |

### Apps del proyecto

| App            | Responsabilidad principal |
| -------------- | ------------------------- |
| `employees`    | Gestión de empleados      |
| `liquidations` | Liquidaciones de sueldo   |
| `attendance`   | Reportes de presentismo   |

### Código

| Decisión                 | Respuesta correcta         |
| ------------------------ | -------------------------- |
| Idioma del código fuente | Inglés                     |
| Nomenclatura de apps     | Inglés, plural, snake_case |
| Estilo de vistas         | CBV (muchas vistas CRUD)   |
| Namespaces en URLs       | Sí, en todas las apps      |

### Modelos

| Decisión                        | Respuesta correcta      | Justificación                                                          |
| ------------------------------- | ----------------------- | ---------------------------------------------------------------------- |
| Tipo de campo para sueldos      | `DecimalField`          | Exactitud monetaria obligatoria                                        |
| Relación Liquidación → Empleado | `ForeignKey`            | Integridad referencial                                                 |
| Soft delete en Empleado         | Sí — `is_active`        | Los empleados no se borran, se desactivan (historial de liquidaciones) |
| Campo `created_at`              | Sí en todos los modelos | Auditoría y trazabilidad                                               |

### Entorno y Seguridad

| Decisión                   | Respuesta correcta      |
| -------------------------- | ----------------------- |
| `SECRET_KEY` en `.env`     | Sí, siempre             |
| Datos de BD en `.env`      | Sí, siempre             |
| `.gitignore` creado cuándo | Antes del primer commit |
| `db.sqlite3` en el repo    | No — va en `.gitignore` |

---

## Sobre la pregunta de reflexión

**¿El error más grave?**

Los errores 2 y 3 (credenciales hardcodeadas) son los más graves desde el punto de vista de seguridad. Una `SECRET_KEY` o password de base de datos expuesta en el historial de git no puede "deshacerse": aunque se borre el archivo, git guarda la historia completa. Requeriría rotar todas las credenciales y regenerar la clave secreta, lo que invalida todas las sesiones activas.

**¿El más difícil de corregir si hay datos de producción?**

El Error 8 (relación con `IntegerField` en lugar de `ForeignKey`) es el más difícil de corregir si el sistema ya tiene datos. Cambiar la relación requiere una migración que puede fallar si hay IDs que no corresponden a empleados existentes, o que deje datos en un estado inconsistente. Es un ejemplo claro de por qué las decisiones de diseño de modelos se toman antes de producción.

---

> 🎓 _"Ver los errores en el código de otro siempre parece fácil. El desafío real es desarrollar el ojo para verlos en el propio código antes de que alguien más los encuentre en producción."_
