# 🚀 Django — Módulo 7 · Clase 13

## Guía de Despliegue en Producción: Render + Supabase + Cloudflare

---

> _"El código solo vive cuando el mundo puede verlo. El deploy es el puente entre tu computador y tus usuarios."_

---

## ¿Qué vas a aprender hoy?

- 🌐 Cómo hacer **deploy** de un proyecto Django en **Render + Supabase**
- 🔗 Cómo conectar un **dominio personalizado** usando Cloudflare
- 🔒 Configuración de seguridad avanzada — settings divididos en base / local / producción
- ⚙️ Gestión de variables de entorno, bases de datos remotas y archivos estáticos

---

# PARTE I — DEPLOY EN PRODUCCIÓN: RENDER + SUPABASE

---

## ¿Por qué Render y Supabase?

Desplegar un proyecto Django en producción requiere un **servidor web** y una **base de datos**. Para proyectos educativos y startups, la combinación de Render (servidor) y Supabase (base de datos PostgreSQL) ofrece una opción gratuita, moderna y profesional.

```
Arquitectura del deploy:
────────────────────────

              Internet
                 │
                 ▼
    ┌─────────────────────┐
    │      RENDER          │    ← Ejecuta tu proyecto Django
    │  (Web Service)       │       Sirve las vistas y la lógica
    │                      │
    │  gunicorn + Django   │
    └─────────┬───────────┘
              │ conexión segura
              ▼
    ┌─────────────────────┐
    │     SUPABASE         │    ← Base de datos PostgreSQL
    │  (PostgreSQL)        │       en la nube
    │                      │
    │  Datos, migraciones  │
    └─────────────────────┘
```

> 📊 **Dato real**: Según el informe "State of Cloud Hosting" de Datadog (2025), el 34% de los desarrolladores web individuales y equipos pequeños utilizan plataformas PaaS (Platform as a Service) como Render, Fly.io o Railway para sus deploys, frente al 22% que configura servidores manualmente en AWS o DigitalOcean.
>
> _Fuente: Datadog, "State of Cloud Hosting" (2025)_

---

## Paso 0 — Requisitos previos

Antes de comenzar el deploy, asegurarse de tener:

```
Cuentas necesarias (todas gratuitas):
─────────────────────────────────────

✅ Cuenta en GitHub       → https://github.com
✅ Cuenta en Render       → https://render.com
✅ Cuenta en Supabase     → https://supabase.com
✅ Proyecto Django funcionando localmente
✅ Repositorio Git con el código del proyecto
```

---

## Paso 1 — Preparar el proyecto Django para producción

### 1.1 Instalar dependencias de producción

```bash
# Instalar las dependencias necesarias para producción
pip install gunicorn psycopg2-binary dj-database-url python-decouple whitenoise
```

| Paquete           | Para qué sirve                                             |
| ----------------- | ---------------------------------------------------------- |
| `gunicorn`        | Servidor WSGI para producción (reemplaza `runserver`)      |
| `psycopg2-binary` | Driver de Python para conectarse a PostgreSQL              |
| `dj-database-url` | Convierte URLs de base de datos en configuración de Django |
| `python-decouple` | Lee variables de entorno desde un archivo `.env`           |
| `whitenoise`      | Sirve archivos estáticos directamente desde Django         |

### 1.2 Generar el archivo `requirements.txt`

```bash
pip freeze > requirements.txt
```

> ⚠️ **Importante:** Render busca este archivo para instalar las dependencias. Si no existe, el deploy falla.

### 1.3 Crear el archivo `build.sh`

Este script se ejecuta cada vez que Render despliega una nueva versión. Debe estar en la **raíz del proyecto** (al mismo nivel que `manage.py`):

```bash
#!/usr/bin/env bash
# build.sh — Script de construcción para Render

set -o errexit    # Detener si hay un error

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate
```

Hacerlo ejecutable:

```bash
chmod a+x build.sh
```

### 1.4 Configurar Settings: estructura dividida por entorno

Un proyecto profesional **no usa un solo `settings.py`** para todo. La buena práctica es dividirlo en tres archivos según el entorno, de modo que desarrollo local y producción tengan configuraciones distintas pero compartan la base común.

```
Estructura recomendada de settings:
────────────────────────────────────

mi_proyecto/
├── settings/
│   ├── __init__.py      ← vacío, hace que la carpeta sea un paquete Python
│   ├── base.py          ← configuración COMPARTIDA entre todos los entornos
│   ├── local.py         ← configuración SOLO para desarrollo en tu computador
│   └── production.py    ← configuración SOLO para el servidor Render
├── wsgi.py
├── urls.py
└── asgi.py
```

```
¿Cómo sabe Django qué settings usar?
──────────────────────────────────────

Django lee la variable de entorno DJANGO_SETTINGS_MODULE.
En Render, se configura como variable de entorno:

  DJANGO_SETTINGS_MODULE = mi_proyecto.settings.production

En local, se puede exportar en la terminal o agregar al .env:

  DJANGO_SETTINGS_MODULE = mi_proyecto.settings.local
```

---

#### Archivo `settings/base.py` — configuración compartida

Este archivo contiene todo lo que es igual en todos los entornos: aplicaciones instaladas, middleware, URL root, templates, internacionalización y contraseñas.

```python
# settings/base.py
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# ↑ tres .parent porque base.py está dentro de settings/

# ─── SEGURIDAD ──────────────────────────────────────────────

# Leído siempre desde variable de entorno — NUNCA hardcodear
SECRET_KEY = config('SECRET_KEY')

# ─── APLICACIONES INSTALADAS ────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tus apps aquí:
    'clinica',
]

# ─── MIDDLEWARE ─────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← siempre en todas
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_proyecto.wsgi.application'

# ─── VALIDACIÓN DE CONTRASEÑAS ──────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── INTERNACIONALIZACIÓN ───────────────────────────────────

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ─── ARCHIVOS ESTÁTICOS ────────────────────────────────────

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─── CLAVE PRIMARIA POR DEFECTO ─────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

#### Archivo `settings/local.py` — desarrollo local

Este archivo importa todo de `base.py` y agrega o sobreescribe solo lo que cambia en tu computador (DEBUG activo, base de datos SQLite, sin HTTPS).

```python
# settings/local.py
from .base import *

# ─── MODO DEPURACIÓN ────────────────────────────────────────

DEBUG = True

# Acepta cualquier host en desarrollo (más cómodo)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ─── BASE DE DATOS ──────────────────────────────────────────

# SQLite local — simple, sin configurar nada extra
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── EMAIL ──────────────────────────────────────────────────

# En desarrollo, los emails se imprimen en la consola en vez de enviarse
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ─── SEGURIDAD RELAJADA (solo desarrollo) ───────────────────

# En local NO usamos HTTPS, así que desactivamos algunas protecciones
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

---

#### Archivo `settings/production.py` — servidor Render

Este archivo importa todo de `base.py` y aplica la configuración segura para producción. Es el que usa Render.

```python
# settings/production.py
import dj_database_url
from .base import *
from decouple import config

# ─── MODO DEPURACIÓN ────────────────────────────────────────

# OBLIGATORIO: False en producción
# Con DEBUG=True en producción se exponen rutas internas, errores
# detallados y configuración del proyecto a cualquier visitante
DEBUG = False

# ─── HOSTS PERMITIDOS ───────────────────────────────────────

# Solo acepta peticiones desde estos dominios
# Coma separados, sin espacios
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
# Ejemplo de valor en Render:
# ALLOWED_HOSTS = cuatro-patas.onrender.com,cuatropatas.cl,www.cuatropatas.cl

# ─── BASE DE DATOS ──────────────────────────────────────────

# Lee la URL de conexión desde la variable de entorno DATABASE_URL
# La convierte al formato que Django entiende
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}
# conn_max_age=600 → mantiene la conexión abierta hasta 10 minutos
# (evita reconectarse a Supabase en cada petición)

# ─── EMAIL ──────────────────────────────────────────────────

# En producción se usa un servidor SMTP real (ej: Gmail, SendGrid)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# ─── SEGURIDAD HTTPS ────────────────────────────────────────

# Redirige todas las peticiones HTTP a HTTPS automáticamente
# (el usuario escribe http:// → el servidor responde con 301 a https://)
SECURE_SSL_REDIRECT = True

# Le dice a Django que confíe en el header HTTP_X_FORWARDED_PROTO
# Render y Cloudflare actúan como proxies: Django recibe HTTP internamente,
# pero el usuario real llega por HTTPS. Este header le dice a Django
# que la conexión con el usuario SÍ es HTTPS.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─── HSTS (HTTP Strict Transport Security) ─────────────────

# Le indica al navegador que SIEMPRE use HTTPS para este dominio
# durante los próximos N segundos (incluso si el usuario escribe http://)
SECURE_HSTS_SECONDS = 31536000          # 1 año = 365 * 24 * 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # aplica también a subdominos (www, api, etc.)
SECURE_HSTS_PRELOAD = True              # permite registrar el dominio en lista HSTS global

# ⚠️ CUIDADO: una vez activo HSTS, si remueves HTTPS el sitio se vuelve
# inaccesible durante SECURE_HSTS_SECONDS segundos. Activarlo solo cuando
# HTTPS esté completamente configurado y funcionando.

# ─── COOKIES SEGURAS ────────────────────────────────────────

# La cookie de sesión solo se envía por HTTPS (nunca por HTTP sin cifrar)
SESSION_COOKIE_SECURE = True

# La cookie del token CSRF solo se envía por HTTPS
CSRF_COOKIE_SECURE = True

# La cookie de sesión no es accesible desde JavaScript del navegador
# (previene ataques XSS que intenten robar la sesión)
SESSION_COOKIE_HTTPONLY = True

# Tiempo máximo de sesión (en segundos)
SESSION_COOKIE_AGE = 3600  # 1 hora

# Expirar la sesión cuando el usuario cierra el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # False = la sesión dura SESSION_COOKIE_AGE

# ─── PROTECCIÓN XSS Y CLICKJACKING ─────────────────────────

# Envía el header X-Content-Type-Options: nosniff
# Impide que el navegador "adivine" el tipo de contenido y ejecute
# scripts disfrazados de imágenes u otros archivos
SECURE_CONTENT_TYPE_NOSNIFF = True

# Activa el filtro XSS del navegador (para navegadores antiguos)
SECURE_BROWSER_XSS_FILTER = True

# ─── LOGGING EN PRODUCCIÓN ─────────────────────────────────

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',  # solo mostrar WARNING y ERROR en producción
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

---

#### Resumen visual de las diferencias entre entornos

```
CONFIGURACIÓN         LOCAL (local.py)          PRODUCCIÓN (production.py)
─────────────         ────────────────          ──────────────────────────
DEBUG                 True                      False
Base de datos         SQLite (archivo local)    PostgreSQL (Supabase)
ALLOWED_HOSTS         localhost, 127.0.0.1      dominio real de Render
HTTPS                 No                        Sí (forzado)
SESSION_COOKIE_SECURE False                     True
CSRF_COOKIE_SECURE    False                     True
SECURE_SSL_REDIRECT   False                     True
HSTS                  No                        Sí (1 año)
Email                 Consola (imprime en log)  SMTP real (Gmail, SendGrid)
Logging               Todo (DEBUG)              Solo WARNING y ERROR
```

---

#### Actualizar `wsgi.py` para usar el settings correcto

```python
# wsgi.py
import os
from django.core.wsgi import get_wsgi_application

# Por defecto apunta a local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings.local')

application = get_wsgi_application()
```

En Render agregar la variable de entorno:

```
DJANGO_SETTINGS_MODULE = mi_proyecto.settings.production
```

#### Actualizar `manage.py` para funcionar en local

```python
# manage.py — cambiar la línea del default
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings.local')
```

---

### 1.5 Crear un **ÚNICO** archivo `.env` para desarrollo local

En tu computador (desarrollo local), vas a crear **un único archivo** llamado exactamente `.env` en la raíz de tu proyecto (al mismo nivel que `manage.py`).

Este archivo **NUNCA** se sube a GitHub porque contiene tus claves secretas. En producción (Render), no se usa un archivo `.env`, sino que las variables se cargan directamente en el panel de control (lo veremos en el Paso 3.3).

```bash
# .env (archivo local — NO subir a Git)
DJANGO_SETTINGS_MODULE=mi_proyecto.settings.local
SECRET_KEY=tu-clave-secreta-de-desarrollo-super-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 1.6 Proteger el archivo en `.gitignore`

Para asegurarnos de que el `.env` jamás llegue a tu repositorio público, agrégalo a tu `.gitignore` antes de hacer el próximo commit:

```
# .gitignore — agregar estas líneas al final del archivo
.env
db.sqlite3
staticfiles/
__pycache__/
*.pyc
```

### 1.7 Subir todo a GitHub

```bash
git add .
git commit -m "Configuración para deploy en producción"
git push origin main
```

---

## Paso 2 — Crear la base de datos en Supabase

### 2.1 Crear un nuevo proyecto

```
1. Ir a https://supabase.com → Sign In
2. Click en "New Project"
3. Completar:
   ┌──────────────────────────────────────────┐
   │  Name:        cuatro-patas-db             │ ← nombre descriptivo
   │  Database Password: [generar una segura]  │ ← GUARDAR ESTA CLAVE
   │  Region:      South America (São Paulo)   │ ← la más cercana a Chile
   │  Plan:        Free                        │
   └──────────────────────────────────────────┘
4. Click en "Create new project"
5. Esperar ~2 minutos mientras se provisiona
```

### 2.2 Obtener la URL de conexión

```
1. En el dashboard de Supabase, ir a:
   Project Settings → Database

2. En la sección "Connection string", seleccionar "URI"

3. La URL tiene este formato:
   postgresql://postgres.[ref]:[PASSWORD]@aws-0-sa-east-1.pooler.supabase.com:6543/postgres

4. IMPORTANTE: Reemplazar [PASSWORD] con la contraseña
   que definieron al crear el proyecto

5. COPIAR esta URL completa — la necesitaremos en Render
```

```
Estructura de la URL de conexión:
──────────────────────────────────

postgresql://postgres.abc123:MiClave@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
│            │               │       │                                    │    │
│            usuario         │       host del servidor                   │    nombre BD
│                            │                                           │
│                            contraseña                                  puerto
│
protocolo
```

> ⚠️ **Seguridad**: La URL de conexión contiene la contraseña. **NUNCA** la pongan directamente en el código ni la suban a GitHub. Siempre usarla como variable de entorno.

---

## Paso 3 — Crear el servicio web en Render

### 3.1 Nuevo Web Service

```
1. Ir a https://render.com → Dashboard
2. Click en "New +" → "Web Service"
3. Conectar con GitHub:
   → Seleccionar el repositorio del proyecto
   → Click en "Connect"
```

### 3.2 Configuración del servicio

```
Completar el formulario:
────────────────────────

┌──────────────────────────────────────────────────────┐
│                                                      │
│  Name:             cuatro-patas                      │
│  Region:           Oregon (US West) o South America  │
│  Branch:           main                              │
│  Runtime:          Python 3                          │
│                                                      │
│  Build Command:    bash build.sh                     │
│  Start Command:    gunicorn config.wsgi:application  │
│                    └── asume que tu carpeta base se  │
│                        llama "config"                │
│                                                      │
│  Instance Type:    Free                              │
│                                                      │
└──────────────────────────────────────────────────────┘
```

> ⚠️ **Cuidado con el Build Command por defecto.** A veces Render detecta mal el proyecto y pone por defecto `mix phx.digest` (que es de Elixir/Phoenix). **Debes borrar eso** y escribir exactamente `bash build.sh`.
>
> ⚠️ **El Start Command es crítico.** El valor `config` debe coincidir con el nombre de la carpeta que contiene `wsgi.py`. Si tu proyecto se llama de otra forma, ajusta el comando (ej: `gunicorn mi_proyecto.wsgi:application`).

### 3.3 Variables de entorno

Antes de crear el servicio, agregar las variables de entorno yendo a la pestaña **"Environment"**:

```
Variables de entorno en Render:
──────────────────────────────

┌─────────────────────┬────────────────────────────────────────────────┐
│  Key                │  Value                                         │
├─────────────────────┼────────────────────────────────────────────────┤
│  SECRET_KEY              │  una-clave-larga-aleatoria-y-unica                  │
│  DEBUG                   │  False                                              │
│  ALLOWED_HOSTS           │  cuatro-patas.onrender.com                          │
│  DATABASE_URL            │  postgresql://postgres.abc...@supabase.com/postgres │
│  DJANGO_SETTINGS_MODULE  │  mi_proyecto.settings.production                    │
│  PYTHON_VERSION          │  3.12.3                                             │
└─────────────────────┴────────────────────────────────────────────────┘
```

Para generar un `SECRET_KEY` seguro:

```python
# Ejecutar en una terminal de Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
# Resultado: 'a3$k9#mz!p4q8r2v5w...'
```

### 3.4 Crear el servicio

```
1. Click en "Create Web Service"
2. Render clona el repositorio, ejecuta build.sh
   y inicia gunicorn
3. Esperar 3-5 minutos para el primer deploy
4. Si todo está bien, se ve:
   ✅ "Your service is live"
   URL: https://cuatro-patas.onrender.com
```

---

## Paso 4 — Verificar el deploy

### 4.1 Verificar que el sitio carga

```
1. Abrir https://cuatro-patas.onrender.com
   → Debe mostrar tu sitio Django

2. Si aparece un error 500:
   → Revisar los logs en Render (pestaña "Logs")
   → Los errores más comunes son:
      • ALLOWED_HOSTS incorrecto
      • DATABASE_URL mal formateada
      • Falta alguna dependencia en requirements.txt
```

### 4.2 Crear el superusuario en producción

Render permite abrir una **shell** directamente desde el dashboard:

```
1. En Render → tu servicio → pestaña "Shell"
2. Ejecutar:
   python manage.py createsuperuser
3. Completar usuario, email y contraseña
4. Ahora se puede acceder al admin en:
   https://cuatro-patas.onrender.com/admin/
```

### 4.3 Verificar la conexión con Supabase

```
En la shell de Render, verificar que las tablas existen:

python manage.py showmigrations

→ Debe mostrar [X] en todas las migraciones
→ Si alguna aparece como [ ], ejecutar:
   python manage.py migrate
```

---

## Paso 5 — Problemas comunes y soluciones

| Problema                                | Causa probable                                        | Solución                                        |
| --------------------------------------- | ----------------------------------------------------- | ----------------------------------------------- |
| Error 500 al cargar el sitio            | `ALLOWED_HOSTS` no incluye el dominio de Render       | Agregar `*.onrender.com` a `ALLOWED_HOSTS`      |
| "DisallowedHost"                        | Falta el dominio en `ALLOWED_HOSTS`                   | Agregar el dominio exacto como variable de env  |
| Los estilos CSS no cargan               | `collectstatic` no se ejecutó o WhiteNoise falta      | Verificar `build.sh` y middleware               |
| Error de conexión a la BD               | `DATABASE_URL` mal formateada o contraseña errónea    | Revisar la URL en Supabase                      |
| "ModuleNotFoundError: gunicorn"         | `gunicorn` no está en `requirements.txt`              | Ejecutar `pip freeze > requirements.txt`        |
| Las migraciones fallan                  | Incompatibilidad SQLite → PostgreSQL                  | Revisar campos con defaults incompatibles       |
| "Password authentication failed"        | La contraseña de Supabase tiene caracteres especiales | Codificar caracteres especiales en la URL       |
| El sitio se "duerme" después de un rato | El plan Free de Render suspende servicios inactivos   | Normal en plan gratuito, se reactiva al visitar |

---

## Diagrama completo del flujo de deploy

```
DESARROLLO LOCAL                              PRODUCCIÓN
────────────────                              ──────────

  Código Python                                Código Python
  SQLite (db.sqlite3)                          PostgreSQL (Supabase)
  python manage.py runserver                   gunicorn proyecto.wsgi
  DEBUG=True                                   DEBUG=False
  Archivos estáticos servidos por Django        WhiteNoise sirve estáticos
       │                                              ▲
       │                                              │
       ▼                                              │
  ┌──────────┐    git push     ┌──────────┐    deploy │
  │  GitHub   │ ──────────────→│  Render   │──────────┘
  │ (código)  │                │ (servidor)│
  └──────────┘                └──────┬─────┘
                                     │
                                     │ DATABASE_URL
                                     ▼
                              ┌──────────────┐
                              │   Supabase   │
                              │ (PostgreSQL) │
                              └──────────────┘
```

---

# PARTE II — DOMINIO PERSONALIZADO CON CLOUDFLARE DNS (OPCIONAL)

---

## ¿Por qué un dominio propio?

Por defecto, Render asigna un subdominio como `cuatro-patas.onrender.com`. Para un proyecto profesional o un portafolio, es preferible tener un dominio como `cuatropatas.cl` o `miportfolio.dev`.

```
Antes:  https://cuatro-patas.onrender.com
Después: https://www.cuatropatas.cl           ← mucho más profesional
```

---

## Paso 1 — Comprar un dominio

```
Registradores recomendados para Chile:
──────────────────────────────────────

Para dominios .cl:
  → NIC Chile: https://www.nic.cl
    Precio: ~$15.000 CLP/año (referencia 2025)

Para dominios internacionales (.com, .dev, .io):
  → Namecheap: https://www.namecheap.com
  → Google Domains (ahora Squarespace): https://domains.squarespace.com
  → Porkbun: https://porkbun.com
    Precio: desde USD $5-15/año dependiendo de la extensión
```

> 📖 _Fuente: NIC Chile, "Tarifas vigentes" — nic.cl (2025)_

---

## Paso 2 — Configurar Cloudflare como DNS

Cloudflare es un servicio gratuito que gestiona los DNS de tu dominio, además de ofrecer CDN, protección DDoS y certificados SSL automáticos.

### 2.1 Crear cuenta y agregar el dominio

```
1. Ir a https://dash.cloudflare.com → Sign Up (es gratuito)

2. Click en "Add a Site"
   → Ingresar: cuatropatas.cl
   → Seleccionar plan "Free"
   → Click en "Continue"

3. Cloudflare escanea los registros DNS existentes
   → Puede encontrar registros previos del registrador
   → Los importa automáticamente
```

### 2.2 Cambiar los nameservers en el registrador

```
Cloudflare te asigna dos nameservers, por ejemplo:
  → aria.ns.cloudflare.com
  → todd.ns.cloudflare.com

Ir al registrador (NIC Chile, Namecheap, etc.) y reemplazar
los nameservers actuales por los de Cloudflare.

En NIC Chile:
  1. Iniciar sesión en https://www.nic.cl
  2. Ir a "Mis dominios" → seleccionar el dominio
  3. "Modificar DNS" → reemplazar por los de Cloudflare
  4. Guardar

⚠️ El cambio de nameservers puede tardar entre 1 y 48 horas
   en propagarse globalmente. En la práctica, suele tomar
   entre 15 minutos y 2 horas.
```

---

## Paso 3 — Configurar el dominio en Render

### 3.1 Agregar el dominio personalizado en Render

```
1. En Render → tu servicio → Settings → Custom Domains

2. Click en "Add Custom Domain"
   → Ingresar: cuatropatas.cl
   → Click en "Verify"

3. Render muestra la información del registro DNS que necesitas crear:
   ┌──────────────────────────────────────────────────────┐
   │  Tipo:   CNAME                                       │
   │  Nombre: www                                         │
   │  Valor:  cuatro-patas.onrender.com                   │
   │                                                       │
   │  (Para el dominio raíz sin www:)                      │
   │  Tipo:   A                                            │
   │  Nombre: @                                            │
   │  Valor:  216.24.57.1  (IP de Render — verificar       │
   │          en la documentación actual de Render)        │
   └──────────────────────────────────────────────────────┘
```

### 3.2 Crear los registros DNS en Cloudflare

```
En Cloudflare → DNS → Records → Add Record:

Registro 1 (subdominio www):
┌───────┬────────┬──────────────────────────────┬───────┐
│ Type  │ Name   │ Content                      │ Proxy │
├───────┼────────┼──────────────────────────────┼───────┤
│ CNAME │ www    │ cuatro-patas.onrender.com    │ ☁️ On │
└───────┴────────┴──────────────────────────────┴───────┘

Registro 2 (dominio raíz — sin www):
┌───────┬────────┬──────────────────────────────┬───────┐
│ Type  │ Name   │ Content                      │ Proxy │
├───────┼────────┼──────────────────────────────┼───────┤
│ A     │ @      │ 216.24.57.1                  │ ☁️ On │
└───────┴────────┴──────────────────────────────┴───────┘

⚠️ La IP de Render puede cambiar. Verificar siempre en:
   https://docs.render.com/custom-domains
```

---

## Paso 4 — Configurar SSL en Cloudflare

```
1. En Cloudflare → SSL/TLS → Overview
2. Seleccionar modo "Full (strict)"
   ┌─────────────────────────────────────────────┐
   │  Off          → sin HTTPS                    │
   │  Flexible     → HTTPS solo hasta Cloudflare  │
   │  Full         → HTTPS hasta Render (cert)     │
   │  Full (strict)→ HTTPS verificado ✅           │ ← ELEGIR ESTE
   └─────────────────────────────────────────────┘

3. Render genera un certificado SSL gratuito con Let's Encrypt
   automáticamente para dominios personalizados verificados.
```

---

## Paso 5 — Actualizar Django para el dominio personalizado

```python
# settings.py — actualizar ALLOWED_HOSTS

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# En Render, actualizar la variable de entorno:
# ALLOWED_HOSTS = cuatro-patas.onrender.com,cuatropatas.cl,www.cuatropatas.cl
```

```python
# settings.py — configuraciones de seguridad para producción con HTTPS

# Redirigir todo el tráfico HTTP a HTTPS
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

# Confiar en el header del proxy (Render/Cloudflare)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Headers de seguridad HSTS
SECURE_HSTS_SECONDS = 31536000     # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## Paso 6 — Redirigir www a dominio raíz (o viceversa)

En Cloudflare se puede configurar una **regla de redirección** para que `www.cuatropatas.cl` redirija a `cuatropatas.cl` (o al revés):

```
En Cloudflare → Rules → Redirect Rules → Create Rule:

┌──────────────────────────────────────────────────┐
│  Rule name:    Redirect www a raíz               │
│                                                   │
│  If:   hostname equals "www.cuatropatas.cl"       │
│  Then: Dynamic redirect                           │
│        Status code: 301 (permanente)              │
│        URL: https://cuatropatas.cl${http.request  │
│             .uri.path}                            │
└──────────────────────────────────────────────────┘
```

---

## Diagrama completo con dominio personalizado

```
                    Usuario escribe: cuatropatas.cl
                              │
                              ▼
                    ┌──────────────────┐
                    │   Cloudflare     │  ← DNS + CDN + SSL
                    │   (gratuito)     │
                    └────────┬─────────┘
                             │
                             │  proxy inverso
                             ▼
                    ┌──────────────────┐
                    │     Render       │  ← Servidor Django
                    │  gunicorn+Django │
                    └────────┬─────────┘
                             │
                             │  DATABASE_URL
                             ▼
                    ┌──────────────────┐
                    │    Supabase      │  ← PostgreSQL
                    │   (gratuito)     │
                    └──────────────────┘
```

---

# RESUMEN — MAPA DE LA GUÍA

---

```
TEMA                          QUÉ APRENDIMOS                      CONCEPTO CLAVE
────                          ────────────────                     ──────────────
Deploy Render+Supabase        Configurar proyecto para prod        gunicorn, whitenoise
                              Conectar BD PostgreSQL remota        DATABASE_URL, build.sh

Dominio personalizado         DNS con Cloudflare                   CNAME, A record
                              SSL automático                       HTTPS, HSTS
```

---

# PRINCIPIOS CLAVE PARA RECORDAR

---

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. En producción, NUNCA uses DEBUG=True ni runserver       │
│     (gunicorn + whitenoise + PostgreSQL)                    │
│                                                            │
│  2. Las credenciales van en variables de entorno            │
│     (SECRET_KEY, DATABASE_URL — nunca en el código)         │
│                                                            │
│  3. El deploy no es el final — es el PRINCIPIO              │
│     (monitorear, mantener, iterar)                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Glosario de Despliegue

| Concepto              | Qué es                                                                              |
| --------------------- | ----------------------------------------------------------------------------------- |
| **Render**            | Plataforma PaaS que ejecuta aplicaciones web en la nube                             |
| **Supabase**          | Servicio que provee bases de datos PostgreSQL gestionadas en la nube                |
| **`gunicorn`**        | Servidor WSGI de producción que reemplaza a `manage.py runserver`                   |
| **`whitenoise`**      | Middleware que permite a Django servir archivos estáticos en producción             |
| **`dj-database-url`** | Librería que convierte una URL de base de datos en configuración de Django          |
| **`python-decouple`** | Librería que lee variables de entorno desde un archivo `.env`                       |
| **`build.sh`**        | Script que Render ejecuta para construir el proyecto en cada deploy                 |
| **`DATABASE_URL`**    | Variable de entorno con la URL de conexión a la base de datos PostgreSQL            |
| **`ALLOWED_HOSTS`**   | Lista de dominios desde los que Django acepta peticiones                            |
| **`collectstatic`**   | Comando que agrupa todos los archivos estáticos en una sola carpeta para producción |
| **Cloudflare**        | Servicio gratuito de DNS, CDN y protección web                                      |
| **Nameservers**       | Servidores que traducen nombres de dominio a direcciones IP                         |
| **Registro CNAME**    | Registro DNS que apunta un subdominio a otro dominio                                |
| **Registro A**        | Registro DNS que apunta un dominio a una dirección IP                               |
| **SSL/TLS**           | Protocolo de cifrado que habilita HTTPS                                             |
| **HSTS**              | Header de seguridad que fuerza al navegador a usar siempre HTTPS                    |
| **PaaS**              | Platform as a Service — servicio que gestiona el servidor por el desarrollador      |

---
