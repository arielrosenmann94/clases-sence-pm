# 🚀 Práctica Clase 9: Profesionalizando tu Proyecto de CV

## Objetivos de la Práctica
- [ ] **Refactorizar** la configuración de Django en entornos separados.
- [ ] **Conectar** tu base de datos de producción a la nube con Supabase.
- [ ] **Automatizar** la carga de datos iniciales con un comando personalizado.

---

## 📁 Tarea 1: La Gran División de Settings

> "El 45% de las brechas de seguridad en aplicaciones web se deben a configuraciones incorrectas en el servidor."
> — *Fuente: OWASP Top 10 Report (2025 Prediction)*

En el mundo profesional, nunca usamos el mismo `settings.py` para programar en nuestro PC que para el servidor real.

### Instrucciones:
1. Crea una carpeta llamada `settings/` dentro de tu carpeta de configuración (donde está `urls.py`).
2. Crea un archivo `__init__.py` dentro de esa carpeta.
3. Divide tu configuración actual en tres archivos:
   - `base.py`: Lo que no cambia (INSTALLED_APPS, MIDDLEWARE, etc.).
   - `development.py`: Para tu PC (DEBUG = True, SQLite).
   - `production.py`: Para la nube (DEBUG = False, Supabase).

### Tip Pro:
En tu `__init__.py`, usa este código para elegir el entorno:
```python
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .production import *
else:
    from .development import *
```

---

## ⚡ Tarea 2: Conexión a la Nube (Supabase)

> "Las bases de datos como servicio (DBaaS) reducen el tiempo de administración en un 60% frente a la autogestión."
> — *Fuente: Gartner Cloud Infrastructure Report (2024)*

Vamos a dejar de usar SQLite en producción y pasaremos a un PostgreSQL real en **Supabase**.

### Pasos:
1. Crea un proyecto en [Supabase](https://supabase.com/).
2. Copia la **Connection String** (URI) de la sección "Database Settings".
3. En tu archivo `.env`, agrega:
   `DATABASE_URL=postgres://tu_usuario:tu_password@tu_host:5432/postgres`
4. En `production.py`, configura Django para usar esa URL:
```python
import dj_database_url
from .base import *

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}
```

---

## 🛠️ Tarea 3: El Comando Mágico `see_cv`

A veces necesitamos que la base de datos se llene sola con nuestra información básica. Para eso crearemos un **Management Command**.

### Requisitos:
Crea la siguiente estructura de carpetas en tu app principal:
`tu_app/management/commands/see_cv.py`

### El Código:
El comando debe permitir ejecutar `python manage.py see_cv` y realizar lo siguiente:
- Verificar si ya existe un perfil de CV.
- Si no existe, crearlo con tus datos (Nombre, Profesión, Bio).
- Si existe, mostrar un mensaje: "El CV ya está poblado".

```python
from django.core.management.base import BaseCommand
from tu_app.models import Perfil  # Ajusta a tu modelo

class Command(BaseCommand):
    help = 'Puebla el CV con información inicial'

    def handle(self, *args, **kwargs):
        perfil, created = Perfil.objects.get_or_create(
            nombre="Tu Nombre",
            defaults={'profesion': 'Fullstack Developer', 'bio': 'Estudiante de Python'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('¡CV poblado con éxito!'))
        else:
            self.stdout.write(self.style.WARNING('El CV ya tiene datos.'))
```

---

## 📝 Resumen del Entregable
1. Tu repositorio Git debe mostrar la carpeta `settings/`.
2. Tu archivo `.env.example` debe incluir la variable `DATABASE_URL`.
3. Al ejecutar `python manage.py see_cv`, la base de datos debe tener tus datos listos.

---

> [!IMPORTANT]
> **No olvides el .gitignore**: Nunca subas tu archivo `.env` con las contraseñas de Supabase a GitHub.
