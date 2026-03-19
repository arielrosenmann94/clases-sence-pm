# 🔐 Módulo 7 — Clase 7b

## Variables de Entorno: El Secreto Mejor Guardado de tu Proyecto

> **AE 7.4** — Utiliza migraciones para la propagación de cambios al esquema de base de datos acorde al framework Django.

---

## 🗺️ Índice

| #      | Tema                                                      |
| ------ | --------------------------------------------------------- |
| **1**  | Recap: ¿Dónde Estamos?                                    |
| **2**  | La Historia que Cambió Todo: $36,000 Dólares en 3 Minutos |
| 2.1    | ¿Qué son las variables de entorno?                        |
| 2.2    | Lo que NO es un .env (La Gran Confusión)                  |
| **3**  | El Problema Real: Secretos en el Código                   |
| 3.1    | La anatomía de un `settings.py` peligroso                 |
| 3.2    | ¿Qué puede salir mal? (Riesgos reales)                    |
| **4**  | La Solución: Archivos .env                                |
| 4.1    | Instalación y configuración                               |
| 4.2    | Paso a paso: Del `settings.py` hardcodeado al `.env`      |
| 4.3    | Tipos de datos en `.env`                                  |
| **5**  | El Patrón Profesional: `.env.example`                     |
| 5.1    | ¿Qué es y por qué existe?                                 |
| 5.2    | Cómo onboardear a un nuevo dev con `.env.example`         |
| **6**  | El `.gitignore`: La Última Línea de Defensa               |
| **7**  | "Ya la Cagué": Qué Hacer Si Subiste Secretos a Git        |
| **8**  | Entornos Múltiples: dev, staging, producción              |
| **9**  | 🤖 Los Bots de GitHub que Escanean tus Secretos           |
| **10** | Buenas Prácticas Profesionales                            |
| **11** | Tabla Resumen y Checklist                                 |

---

---

> _"En 2024, más de 12.8 millones de secretos fueron expuestos en repositorios públicos de GitHub. No porque los desarrolladores fueran incompetentes — sino porque nadie les enseñó a usar un archivo .env."_
>
> — GitGuardian, State of Secrets Sprawl Report (2024)

---

---

# 📚 1. Recap: ¿Dónde Estamos?

En la Clase 6a aprendimos que las migraciones controlan la **estructura** de la base de datos. Pero hay algo que Django necesita ANTES de poder conectarse a la base de datos, antes de poder enviar emails, antes de hacer cualquier cosa:

**La configuración.**

Y esa configuración vive en `settings.py`. Y dentro de `settings.py` hay datos que **jamás deberían ver la luz pública**: contraseñas, claves secretas, credenciales de APIs.

| Lo que ya sabemos                   | Lo que vamos a aprender hoy                                   |
| :---------------------------------- | :------------------------------------------------------------ |
| `settings.py` configura Django      | Qué datos de `settings.py` son **peligrosos**                 |
| Las migraciones van a Git           | Qué archivos **NUNCA** deben ir a Git                         |
| El proyecto tiene una SECRET_KEY    | Por qué esa clave **vale dinero** si cae en manos equivocadas |
| Usamos `pip install` para librerías | Cómo usar `python-dotenv` para proteger tu configuración      |

---

---

# 💥 2. La Historia que Cambió Todo: $36,000 Dólares en 3 Minutos

---

Esto no es ciencia ficción. Esto pasó de verdad.

En 2015, Andrew Hoffman — un desarrollador — pusheó accidentalmente sus **claves de acceso de AWS** (Amazon Web Services) a un repositorio público de GitHub. Lo que pasó después lo cambió todo:

```
Minuto 0:    Andrew hace "git push" con sus credenciales de AWS en el código
Minuto 1:    Un bot automatizado detecta las claves en GitHub
Minuto 2:    El bot lanza 140 servidores EC2 en Amazon para minar criptomonedas
Minuto 3:    La factura empieza a acumularse: $6 dólares por segundo
Hora 4:      Andrew recibe un email de AWS: "Actividad inusual detectada"
Final:       $36,000 dólares de factura. En cuatro horas.
```

Andrew tuvo suerte: AWS le condonó la deuda como gesto comercial. **La mayoría no tiene esa suerte.**

### ¿Cómo pudo ser evitado?

Con **un archivo `.env`** y **una línea en `.gitignore`**. Literalmente. Eso es lo que vamos a aprender hoy.

> 💡 **Dato escalofriante:** Según GitGuardian (2024), se detectaron **12.8 millones de secretos** expuestos en repositorios públicos de GitHub solo en 2024. El 90% de los secretos filtrados siguen activos 5 días después de ser expuestos.

---

## 2.1 ¿Qué Son las Variables de Entorno?

Una variable de entorno es un **valor que vive FUERA de tu código** pero que tu código puede leer. Es como una nota secreta que solo tu aplicación puede ver.

### La Analogía del Buzón

Imagina que tu aplicación es una casa:

```
❌ SIN variables de entorno (lo que hacemos mal):
   Tu contraseña del WiFi está escrita en un CARTEL GIGANTE
   en la puerta de tu casa. Cualquiera que pase la ve.

✅ CON variables de entorno (lo correcto):
   Tu contraseña del WiFi está en un papel DENTRO de un buzón
   con llave. Solo quien tiene la llave (tu app) puede leerla.
```

En términos técnicos:

```
Variable de entorno = Un par CLAVE=VALOR que existe en el
                      sistema operativo, no en tu código.

Ejemplo:
  SECRET_KEY=django-insecure-abc123xyz
  DATABASE_PASSWORD=mi_clave_super_segura
  EMAIL_HOST_PASSWORD=smtp_password_real
```

Tu código Python puede leer estas variables así:

```python
import os

# Lee la variable de entorno llamada 'SECRET_KEY'
clave = os.environ.get('SECRET_KEY')
# ↑ Busca el valor en el sistema operativo, NO en tu código
```

---

## 2.2 Lo que NO es un .env (La Gran Confusión)

---

Esto es **extremadamente importante**. Muchos estudiantes confunden estos dos conceptos porque suenan parecido:

| Concepto            | ¿Qué es?                                              | Comando                 |
| :------------------ | :---------------------------------------------------- | :---------------------- |
| **Entorno virtual** | Una carpeta aislada con Python y librerías instaladas | `python -m venv .venv`  |
| **Archivo `.env`**  | Un archivo de texto con variables de configuración    | Lo creas tú manualmente |

```
⚠️ NO SON LO MISMO. NO TIENEN NADA QUE VER.

.venv/  ← CARPETA. Contiene Python aislado y paquetes pip.
         Se crea con "python -m venv .venv".
         Es tu LABORATORIO de trabajo.

.env   ← ARCHIVO. Contiene contraseñas y configuraciones.
         Se crea manualmente con un editor.
         Es tu CAJA FUERTE de secretos.
```

### ¿Por qué se confunden?

Porque ambos empiezan con punto (`.`) y tienen la letra "env" en el nombre. Pero la similitud termina ahí:

| Pregunta                    | Entorno Virtual (`.venv/`)            | Archivo `.env`                       |
| :-------------------------- | :------------------------------------ | :----------------------------------- |
| ¿Es un archivo o carpeta?   | Una **carpeta** con miles de archivos | **Un solo** archivo de texto         |
| ¿Qué contiene?              | Python, pip, librerías instaladas     | Claves, contraseñas, configuraciones |
| ¿Se sube a Git?             | **NO** (por tamaño)                   | **NO** (por seguridad)               |
| ¿Se comparte con el equipo? | No, cada dev crea el suyo             | No, cada dev crea el suyo            |
| ¿Qué problema resuelve?     | Aislar dependencias de Python         | Proteger datos sensibles del código  |
| ¿Cómo se activa?            | `source .venv/bin/activate`           | Se lee automáticamente al iniciar    |

> 💡 **Regla para nunca olvidar:** El entorno virtual (`.venv`) es **dónde corren tus herramientas**. El archivo `.env` es **dónde guardas tus secretos**. Uno es el taller. El otro es la caja fuerte.

---

---

# 🚨 3. El Problema Real: Secretos en el Código

---

## 3.1 La Anatomía de un `settings.py` Peligroso

Cuando Django crea un proyecto nuevo con `django-admin startproject`, genera un `settings.py` con esto:

```python
# settings.py — PELIGROSO (así viene por defecto)

# ⚠️ PROBLEMA 1: La clave secreta está visible en el código
SECRET_KEY = 'django-insecure-g7&k@!m2$x#j9p4z5w8v6n1c3b0a'
# ↑ Si alguien ve este archivo, tiene tu clave secreta.
#   Con ella puede falsificar sesiones, cookies, y tokens CSRF.

# ⚠️ PROBLEMA 2: Debug activado — muestra errores internos a todos
DEBUG = True
# ↑ En producción, esto expone rutas, variables, y código interno.

# ⚠️ PROBLEMA 3: Base de datos con credenciales expuestas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mi_base_datos',
        'USER': 'admin',
        'PASSWORD': 'SuperClave123!',  # ← Contraseña VISIBLE
        'HOST': '192.168.1.100',       # ← IP del servidor VISIBLE
        'PORT': '5432',
    }
}

# ⚠️ PROBLEMA 4: Credenciales de email expuestas
EMAIL_HOST_PASSWORD = 'mi_password_smtp_real'
# ↑ Cualquiera puede enviar emails desde tu cuenta.
```

**Todo esto está en texto plano.** Si haces `git push`, **el mundo entero puede verlo.**

---

## 3.2 ¿Qué Puede Salir Mal? (Riesgos Reales)

| Dato expuesto          | ¿Qué puede hacer un atacante?                                | Nivel de riesgo |
| :--------------------- | :----------------------------------------------------------- | :-------------- |
| `SECRET_KEY`           | Falsificar sesiones de usuario, crear tokens de admin falsos | 🔴 CRÍTICO      |
| `DATABASE PASSWORD`    | Leer, modificar o borrar TODOS los datos de tu base de datos | 🔴 CRÍTICO      |
| `EMAIL_HOST_PASSWORD`  | Enviar spam o phishing desde tu dirección de email           | 🟠 ALTO         |
| `DEBUG = True`         | Ver rutas internas, variables, y trazas completas de errores | 🟠 ALTO         |
| API keys (Stripe, AWS) | Generar cargos económicos, usar servicios a tu nombre        | 🔴 CRÍTICO      |
| `ALLOWED_HOSTS`        | Si está vacío, ataques de Host Header Injection              | 🟡 MEDIO        |

> ⚠️ **Dato real:** El 83% de las brechas de seguridad en aplicaciones web involucran credenciales hardcodeadas o mal gestionadas (Verizon DBIR, 2024).

---

---

# ✅ 4. La Solución: Archivos .env

---

## 4.1 Instalación y Configuración

Existen dos librerías principales para manejar archivos `.env` en Django. Vamos a ver ambas:

### Opción A: `python-dotenv` (la más simple)

```bash
# Instalar la librería
pip install python-dotenv

# No olvides actualizar tu requirements.txt
pip freeze > requirements.txt
```

### Opción B: `django-environ` (la más completa para Django)

```bash
# Instalar la librería
pip install django-environ

# No olvides actualizar tu requirements.txt
pip freeze > requirements.txt
```

### ¿Cuál elegir?

| Característica          | `python-dotenv`             | `django-environ`                 |
| :---------------------- | :-------------------------- | :------------------------------- |
| Instalación             | `pip install python-dotenv` | `pip install django-environ`     |
| Complejidad             | Mínima                      | Baja                             |
| Conversión de tipos     | Manual (`int()`, `bool()`)  | Automática (`.bool()`, `.int()`) |
| Lectura de DATABASE_URL | No incluida                 | Sí, con `db_url()`               |
| Ideal para              | Proyectos pequeños          | Proyectos Django profesionales   |
| Comunidad               | Muy grande (uso general)    | Grande (específica para Django)  |

> 💡 **Recomendación:** Para este curso usaremos `django-environ` porque está diseñada específicamente para Django y convierte tipos automáticamente. En tu carrera profesional, te encontrarás ambas.

---

## 4.2 Paso a Paso: Del `settings.py` Hardcodeado al `.env`

---

### Paso 1 — Crear el archivo `.env` en la raíz del proyecto

El archivo `.env` va en la **misma carpeta donde está `manage.py`**:

```
mi_proyecto/
├── manage.py
├── .env              ← AQUÍ VA
├── .env.example      ← Y este también (lo veremos después)
├── .gitignore
├── requirements.txt
└── config/
    ├── __init__.py
    ├── settings.py   ← Este lee el .env
    ├── urls.py
    └── wsgi.py
```

### Paso 2 — Escribir las variables en el `.env`

```bash
# .env — Archivo de variables de entorno
# ⚠️ ESTE ARCHIVO NUNCA SE SUBE A GIT

# Clave secreta de Django
SECRET_KEY=django-insecure-g7&k@!m2$x#j9p4z5w8v6n1c3b0a

# Modo debug (True solo en desarrollo)
DEBUG=True

# Hosts permitidos (separados por coma)
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=mi_base_datos
DB_USER=admin
DB_PASSWORD=SuperClave123!
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST_PASSWORD=mi_password_smtp_real
```

> ⚠️ **Reglas del archivo `.env`:**
>
> - **NO uses espacios** alrededor del `=` → ✅ `DEBUG=True` → ❌ `DEBUG = True`
> - **NO uses comillas** a menos que el valor tenga espacios → ✅ `DB_NAME=mi_base` → ❌ `DB_NAME="mi_base"`
> - **Cada variable en su propia línea**
> - **Los comentarios empiezan con `#`**

### Paso 3 — Modificar `settings.py` para leer del `.env`

**Con `django-environ`:**

```python
# settings.py — SEGURO (lee del archivo .env)

import environ
# ↑ Importamos la librería django-environ

import os
# ↑ Para construir rutas de archivos

from pathlib import Path
# ↑ Para manejar rutas de forma moderna

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializar environ
env = environ.Env(
    # ↑ Creamos una instancia de Env
    DEBUG=(bool, False),
    # ↑ Definimos el tipo y valor por defecto de DEBUG
    #   Si no existe en el .env, será False (lo más seguro)
)

# Leer el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# ↑ Le decimos a django-environ DÓNDE está el archivo .env
#   BASE_DIR es la carpeta donde está manage.py

# ─── Ahora leemos las variables del .env ───

SECRET_KEY = env('SECRET_KEY')
# ↑ Lee la variable SECRET_KEY del archivo .env
#   Si no existe, lanza un error (es obligatoria)

DEBUG = env('DEBUG')
# ↑ Lee DEBUG del .env y lo convierte a booleano automáticamente
#   'True' → True, 'False' → False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
# ↑ Lee ALLOWED_HOSTS y lo convierte a lista automáticamente
#   'localhost,127.0.0.1' → ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
# ↑ El segundo argumento es el valor por defecto si no existe
```

### El Flujo Completo (Antes vs. Después)

```
ANTES (peligroso):
┌─────────────────────────────┐
│ settings.py                 │
│                             │
│ SECRET_KEY = 'abc123...'    │──→ git push ──→ GitHub ──→ 🌍 TODO EL MUNDO VE
│ DB_PASSWORD = 'clave123'    │
│ EMAIL_PASS = 'smtp_pass'   │
└─────────────────────────────┘

DESPUÉS (seguro):
┌─────────────────────────────┐     ┌──────────────────────┐
│ settings.py                 │     │ .env (NO va a Git)   │
│                             │     │                      │
│ SECRET_KEY = env('SECRET_') │──→  │ SECRET_KEY=abc123... │  ← Solo en tu máquina
│ DB_PASSWORD = env('DB_PASS')│     │ DB_PASSWORD=clave123 │
│ EMAIL_PASS = env('EMAIL_')  │     │ EMAIL_PASS=smtp_pass │
└─────────────────────────────┘     └──────────────────────┘
         │                                     │
         ▼                                     ▼
   ✅ Se sube a Git                    ❌ NUNCA se sube a Git
   (no tiene secretos)                 (solo existe en tu compu)
```

---

## 4.3 Tipos de Datos en `.env`

El archivo `.env` solo guarda **texto plano**. Todo es un string. La librería `django-environ` se encarga de convertir los tipos:

```bash
# .env — Todo es texto plano
SECRET_KEY=mi-clave-secreta-123
DEBUG=True
MAX_CONNECTIONS=10
ALLOWED_HOSTS=localhost,127.0.0.1,mi-dominio.com
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
```

```python
# settings.py — django-environ convierte los tipos automáticamente

SECRET_KEY = env('SECRET_KEY')
# ↑ Tipo: str → 'mi-clave-secreta-123'

DEBUG = env.bool('DEBUG', default=False)
# ↑ Tipo: bool → True
#   Convierte 'True'/'true'/'1'/'yes'/'on' → True
#   Convierte 'False'/'false'/'0'/'no'/'off' → False

MAX_CONNECTIONS = env.int('MAX_CONNECTIONS', default=5)
# ↑ Tipo: int → 10
#   Convierte el string '10' al número entero 10

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
# ↑ Tipo: list → ['localhost', '127.0.0.1', 'mi-dominio.com']
#   Separa por comas automáticamente

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}
# ↑ Tipo: dict → Parsea la URL completa a un diccionario de conexión
#   Esto es exclusivo de django-environ y es muy poderoso
```

| Método             | Tipo que devuelve | Ejemplo en `.env`              | Resultado en Python                 |
| :----------------- | :---------------- | :----------------------------- | :---------------------------------- |
| `env('VAR')`       | `str`             | `VAR=hola`                     | `'hola'`                            |
| `env.bool('VAR')`  | `bool`            | `VAR=True`                     | `True`                              |
| `env.int('VAR')`   | `int`             | `VAR=42`                       | `42`                                |
| `env.float('VAR')` | `float`           | `VAR=3.14`                     | `3.14`                              |
| `env.list('VAR')`  | `list`            | `VAR=a,b,c`                    | `['a', 'b', 'c']`                   |
| `env.db('VAR')`    | `dict`            | `VAR=postgres://u:p@h:5432/db` | `{'ENGINE': ..., 'NAME': ..., ...}` |

---

---

# 📋 5. El Patrón Profesional: `.env.example`

---

## 5.1 ¿Qué es y Por Qué Existe?

Si el `.env` NO se sube a Git (porque tiene secretos), ¿cómo sabe un nuevo desarrollador qué variables necesita crear?

Para eso existe el `.env.example`: un **template** del `.env` que SÍ se sube a Git, pero **sin valores reales**.

```bash
# .env.example — ESTE SÍ VA A GIT
# Copia este archivo como .env y completa los valores reales

# Clave secreta de Django (genera una nueva con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
SECRET_KEY=tu_clave_secreta

# Modo debug (True en desarrollo, False en producción)
DEBUG=True

# Hosts permitidos
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=nombre_de_tu_base
DB_USER=tu_usuario
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# Email (opcional en desarrollo)
EMAIL_HOST_PASSWORD=
```

### La diferencia visual:

```
.env (SECRETO — NO va a Git):          .env.example (PÚBLICO — SÍ va a Git):
┌────────────────────────────┐          ┌────────────────────────────┐
│ SECRET_KEY=g7&k@!m2$x#j9  │          │ SECRET_KEY=                │
│ DEBUG=True                 │          │ DEBUG=True                 │
│ DB_PASSWORD=SuperClave123! │          │ DB_PASSWORD=               │
│ EMAIL_PASS=smtp_real_pass  │          │ EMAIL_PASS=                │
└────────────────────────────┘          └────────────────────────────┘
     ↑ Con valores reales                    ↑ Sin valores secretos
     ↑ Solo en TU máquina                    ↑ En el repo para TODOS
```

---

## 5.2 Cómo Onboardear a un Nuevo Dev con `.env.example`

Cuando un nuevo desarrollador se une al equipo, el proceso es así:

```
Paso 1:  Clona el repositorio
         $ git clone https://github.com/equipo/proyecto.git

Paso 2:  Ve que existe .env.example pero NO existe .env
         (porque .env está en .gitignore)

Paso 3:  Copia el template
         $ cp .env.example .env

Paso 4:  Completa los valores reales
         (se los pasa el líder del equipo por un canal seguro,
          NUNCA por email ni Slack público)

Paso 5:  Instala dependencias y migra
         $ pip install -r requirements.txt
         $ python manage.py migrate

Paso 6:  ¡Listo! El proyecto funciona con SUS credenciales
```

> 💡 **¿Por qué es tan importante?** Sin `.env.example`, cada nuevo desarrollador tiene que adivinar qué variables necesita. Con `.env.example`, el onboarding pasa de 2 horas de frustración a 5 minutos. Esto es lo que separa a los equipos profesionales de los amateurs.

---

---

# 🛡️ 6. El `.gitignore`: La Última Línea de Defensa

---

El archivo `.gitignore` le dice a Git qué archivos **nunca debe rastrear**. Si el `.env` no está en `.gitignore`, un `git add .` lo sube al repositorio.

### Un `.gitignore` profesional para Django:

```bash
# .gitignore — Archivos que NUNCA deben ir a Git

# ─── Variables de entorno (SECRETOS) ───
.env
.env.local
.env.production
# ↑ NUNCA subas archivos con credenciales

# ─── Entorno virtual ───
.venv/
venv/
env/
# ↑ Cada dev crea el suyo con "python -m venv .venv"

# ─── Base de datos local (SQLite) ───
db.sqlite3
*.sqlite3
# ↑ Cada dev tiene su propia base de datos de desarrollo

# ─── Python ───
__pycache__/
*.py[cod]
*.pyo
# ↑ Archivos compilados que Python genera automáticamente

# ─── IDE ───
.vscode/
.idea/
*.swp
# ↑ Configuración personal de cada editor

# ─── Archivos del sistema ───
.DS_Store
Thumbs.db
```

---

---

# 🚨 7. "Ya la Cagué": Qué Hacer Si Subiste Secretos a Git

---

Esto les va a pasar. No es cuestión de "si", es cuestión de "cuándo". Lo importante es saber **cómo reaccionar rápido**. Veamos los 3 escenarios más comunes:

---

## Escenario 1: Subí el archivo `.env` al repositorio

Hiciste `git add .` sin tener `.env` en tu `.gitignore`. Ahora tu archivo `.env` con todas las contraseñas está en GitHub.

### 🚨 Protocolo de Emergencia (haz esto EN ORDEN):

```bash
# ─── PASO 1: Agregar .env al .gitignore (para que no vuelva a pasar) ───
echo ".env" >> .gitignore

# ─── PASO 2: Eliminar .env del rastreo de Git (sin borrar el archivo local) ───
git rm --cached .env
# ↑ --cached = "sacalo de Git pero NO borres mi archivo local"
#   Sin --cached, Git te borra el archivo de tu computadora también

# ─── PASO 3: Hacer commit de la corrección ───
git commit -m "fix: eliminar .env del repositorio y agregar a .gitignore"

# ─── PASO 4: Pushear la corrección ───
git push
```

> ⚠️ **PERO ESTO NO ES SUFICIENTE.** Aunque ya no esté en el último commit, Git **recuerda todo**. Cualquiera puede ver el archivo `.env` en el historial de commits. Sigue al Paso 5.

```bash
# ─── PASO 5: CAMBIAR TODAS LAS CONTRASEÑAS ───
# Esta es la parte más importante y la que nadie quiere hacer.
# DEBES cambiar cada secreto que estaba en el .env:

# - Generar una nueva SECRET_KEY de Django:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# - Cambiar la contraseña de la base de datos
# - Revocar y regenerar todas las API keys (AWS, Stripe, etc.)
# - Cambiar la contraseña del email SMTP
# - Actualizar tu .env local con los nuevos valores
```

> 🔴 **¿Por qué cambiar las contraseñas es obligatorio?** Porque aunque borres el archivo, los bots ya lo escanearon (recuerda: tardan menos de 24 segundos). Las claves antiguas **ya están comprometidas**. Borrar el archivo no "des-compromete" las claves.

---

## Escenario 2: Puse las contraseñas hardcodeadas en `settings.py`

Nunca creaste un `.env`. Directamente pusiste `SECRET_KEY = 'mi-clave-real'` y `DB_PASSWORD = 'SuperClave123!'` en `settings.py`. Y ese settings.py lleva 20 commits subido con las contraseñas visibles.

### 🚨 Protocolo de Recuperación:

```bash
# ─── PASO 1: Instalar django-environ ───
pip install django-environ
pip freeze > requirements.txt

# ─── PASO 2: Crear el archivo .env ───
# Mover TODOS los valores sensibles del settings.py al .env
touch .env

# ─── PASO 3: Editar settings.py para que lea del .env ───
# (seguir el paso a paso de la Sección 4.2 de esta clase)

# ─── PASO 4: Agregar .env a .gitignore ───
echo ".env" >> .gitignore

# ─── PASO 5: Commit y push ───
git add .gitignore settings.py requirements.txt
git commit -m "fix: migrar secretos de settings.py a .env"
git push

# ─── PASO 6: CAMBIAR TODAS LAS CONTRASEÑAS ───
# Mismo proceso del Escenario 1:
# Las claves viejas siguen visibles en el historial de Git
```

---

## Escenario 3: Los secretos están enterrados en commits antiguos

Este es el peor caso. Tus contraseñas no están en el commit actual (ya las moviste al `.env`), pero si alguien revisa el historial de Git, puede ver los commits antiguos donde las contraseñas estaban en `settings.py`.

### ¿Cómo ve alguien tus secretos antiguos?

```bash
# Cualquiera con acceso al repo puede hacer esto:
git log --all -p -- settings.py
# ↑ Muestra TODOS los cambios históricos de settings.py
#   Incluyendo cuando tenías SECRET_KEY='abc123' hardcodeado
```

### 🚨 Opciones para limpiar el historial:

**Opción A: BFG Repo-Cleaner (la más fácil)**

```bash
# BFG es una herramienta diseñada específicamente para esto
# Descárgala de: https://rtyley.github.io/bfg-repo-cleaner/

# Paso 1: Clonar el repo en modo "espejo"
git clone --mirror https://github.com/tu-usuario/tu-repo.git

# Paso 2: Crear un archivo con los textos a eliminar
echo "SuperClave123!" >> passwords.txt
echo "django-insecure-g7&k@!m2" >> passwords.txt
echo "mi_password_smtp_real" >> passwords.txt

# Paso 3: Ejecutar BFG para reemplazar esos textos en todo el historial
java -jar bfg.jar --replace-text passwords.txt tu-repo.git

# Paso 4: Limpiar y pushear
cd tu-repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**Opción B: Si el repo es pequeño o personal**

A veces la solución más práctica es:

1. Cambiar TODAS las contraseñas
2. Crear un repositorio nuevo
3. Copiar el código actual (sin el historial)
4. Pushear como proyecto nuevo

```bash
# Copia nuclear: empezar el historial de Git desde cero
rm -rf .git
git init
git add .
git commit -m "inicio limpio del proyecto"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push --force origin main
```

> ⚠️ **Cuidado:** `git push --force` reescribe el historial remoto. Si trabajas en equipo, **avísales antes** porque van a tener que re-clonar el repo.

---

## 📋 Resumen del Protocolo de Emergencia

```
┌──────────────────────────────────────────────────────────┐
│        🚨 PROTOCOLO: SECRETO EXPUESTO EN GIT 🚨          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. NO entres en pánico (pero actúa RÁPIDO)              │
│                                                          │
│  2. CAMBIA todas las contraseñas y claves expuestas      │
│     → SECRET_KEY nueva                                   │
│     → DB_PASSWORD nueva                                  │
│     → API keys: REVOCAR y regenerar                      │
│     → SMTP password nuevo                                │
│                                                          │
│  3. AGREGA .env a .gitignore                             │
│     $ echo ".env" >> .gitignore                          │
│                                                          │
│  4. ELIMINA el archivo del rastreo de Git                │
│     $ git rm --cached .env                               │
│                                                          │
│  5. LIMPIA el historial (BFG o repo nuevo)               │
│                                                          │
│  6. COMMIT y PUSH la corrección                          │
│                                                          │
│  7. VERIFICA que no queden secretos:                     │
│     $ git log --all -p | grep "PASSWORD"                 │
│     (no debería encontrar nada)                          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

> 💡 **La lección más importante:** Es **mucho más fácil** configurar bien el `.env` y el `.gitignore` desde el primer commit que arreglar el desastre después. Por eso esta clase existe.

---

---

# 🌍 8. Entornos Múltiples: dev, staging, producción

---

En un proyecto profesional, tu aplicación corre en diferentes servidores con diferentes configuraciones:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DESARROLLO    │    │    STAGING       │    │   PRODUCCIÓN    │
│   (tu compu)    │    │   (servidor de   │    │  (el servidor   │
│                 │    │    pruebas)      │    │   real)         │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ DEBUG=True      │    │ DEBUG=True      │    │ DEBUG=False     │
│ DB=sqlite3      │    │ DB=postgres     │    │ DB=postgres     │
│ HOST=localhost  │    │ HOST=staging.com│    │ HOST=app.com    │
│ EMAIL=consola   │    │ EMAIL=test@     │    │ EMAIL=real@     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
      ↑                       ↑                       ↑
   .env local            .env en staging          .env en prod
   (tu máquina)          (otro servidor)          (servidor real)
```

### ¿Por qué importa?

Porque **el mismo código** se ejecuta en los tres entornos, pero con **diferentes configuraciones**. Gracias al archivo `.env`, no necesitas cambiar `settings.py` para cada entorno — solo cambias el contenido del `.env`.

```python
# settings.py — El MISMO código funciona en TODOS los entornos

DEBUG = env.bool('DEBUG', default=False)
# ↑ En desarrollo: .env dice DEBUG=True  → muestra errores detallados
# ↑ En producción: .env dice DEBUG=False → muestra página de error genérica

DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}
# ↑ En desarrollo: usa SQLite (simple, sin instalar nada)
# ↑ En producción: usa PostgreSQL (robusto, escalable)
```

> 💡 **Esto es clave:** El código NO cambia entre entornos. Solo cambia el `.env`. Esto evita el clásico error de "funciona en mi máquina pero no en producción".

---

---

# 🤖 9. Los Bots de GitHub que Escanean tus Secretos

---

Esto es lo que nadie les cuenta y es lo más aterrador de toda la clase.

Existen **bots automatizados** que escanean repositorios públicos de GitHub **las 24 horas del día, los 7 días de la semana**. Algunos son buenos (buscan secretos para notificarte). Otros son maliciosos (buscan secretos para explotarlos).

### El Ciclo de un Secreto Expuesto

```
Segundo 0:    Haces "git push" con una clave de API en tu código
Segundo 1-5:  Los bots de GitHub ya escanearon tu commit
Segundo 10:   Un bot malicioso detecta que es una clave de AWS
Segundo 30:   El bot ya está usando tu clave para lanzar servidores
Minuto 5:     Tienes cargos acumulándose en tu cuenta
Hora 1:       Si no te diste cuenta, ya van cientos de dólares
```

### ¿Quiénes son estos bots?

| Bot / Servicio             | ¿Qué hace?                                        | ¿Bueno o malo?     |
| :------------------------- | :------------------------------------------------ | :----------------- |
| **GitHub Secret Scanning** | Escanea tu repo y te avisa si encuentra secretos  | 🟢 Bueno (GitHub)  |
| **GitGuardian**            | Monitorea repos públicos y privados por secretos  | 🟢 Bueno (empresa) |
| **TruffleHog**             | Herramienta open source que busca secretos en Git | 🟢 Bueno (tool)    |
| **Bots de minería**        | Buscan claves de AWS/GCP para minar criptomonedas | 🔴 Malicioso       |
| **Bots de spam**           | Buscan credenciales SMTP para enviar phishing     | 🔴 Malicioso       |
| **Scrapers genéricos**     | Recopilan cualquier credencial para venderla      | 🔴 Malicioso       |

> 🔗 **Dónde obtener las herramientas buenas:**
>
> - **GitHub Secret Scanning** — Viene integrado en GitHub, solo actívalo en: [github.com/settings/security](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)
> - **GitGuardian** — Plan gratuito para repos personales: [gitguardian.com](https://www.gitguardian.com/)
> - **TruffleHog** — Instalación con `pip install trufflehog` o desde: [github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog)

### Dato que te va a quitar el sueño

> 🔴 **GitGuardian (2024):** En promedio, un secreto expuesto en GitHub es detectado por bots maliciosos en **menos de 24 segundos**. Sí, **segundos**. El 90% de los secretos filtrados permanecen activos por al menos 5 días.

### GitHub Secret Scanning: Tu Aliado

GitHub tiene un sistema de protección integrado desde 2023 llamado **Push Protection**. Si intentas hacer push de algo que parece una API key, GitHub te bloquea el push y te avisa:

```
remote: ─────────────────────────────────────────────────────
remote: ── GitHub Personal Access Token found ──
remote:
remote:   commit: a]3f2b1c...
remote:   file: settings.py:7
remote:
remote:  Push blocked. To push, remove the secret or use
remote:  "git secret scan --allow" to bypass.
remote: ─────────────────────────────────────────────────────
```

Pero **no dependas solo de esto**. La mejor protección es que el secreto **nunca esté en tu código** en primer lugar. Para eso existe el `.env`.

---

---

# ✅ 10. Buenas Prácticas Profesionales

---

### 1. NUNCA hardcodees secretos en el código

```python
# ❌ MAL — El secreto está en el código
SECRET_KEY = 'django-insecure-abc123xyz'

# ✅ BIEN — El secreto viene del .env
SECRET_KEY = env('SECRET_KEY')
```

### 2. Siempre ten un `.env.example` actualizado

Cada vez que agregues una nueva variable al `.env`, agrégala también al `.env.example` (sin el valor real).

### 3. Usa valores por defecto seguros

```python
# ✅ Si no hay .env, DEBUG es False por seguridad
DEBUG = env.bool('DEBUG', default=False)

# ✅ Si no hay ALLOWED_HOSTS, no permite ningún host
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

### 4. Valida que las variables críticas existan

```python
# ✅ Si SECRET_KEY no está en .env, Django NO arranca
SECRET_KEY = env('SECRET_KEY')
# ↑ Sin default = obligatoria. Si falta, lanza ImproperlyConfigured
```

### 5. Nunca compartas secretos por canales inseguros

```
❌ MAL:  Enviar contraseñas por email, Slack público, o WhatsApp
✅ BIEN: Usar un gestor de contraseñas (1Password, Bitwarden)
✅ BIEN: Compartir por canal cifrado (Signal, Slack DM cifrado)
✅ BIEN: Usar un gestor de secretos (AWS Secrets Manager, Vault)
```

### 6. Rota tus secretos periódicamente

Cambia tus claves cada cierto tiempo, especialmente:

- Cuando un miembro del equipo se va
- Cuando sospechas que alguien pudo ver las credenciales
- Como política estándar cada 3-6 meses

### 7. Verifica tu `.gitignore` ANTES del primer commit

```bash
# Verifica que .env está en .gitignore ANTES de hacer cualquier commit
cat .gitignore | grep .env

# Si no aparece, agrégalo inmediatamente:
echo ".env" >> .gitignore
```

---

---

# 🏁 11. Tabla Resumen y Checklist

---

## Tabla de Conceptos Clave

| Concepto         | ¿Qué es?                                                            | ¿Va a Git?                  |
| :--------------- | :------------------------------------------------------------------ | :-------------------------- |
| `.env`           | Archivo con variables secretas (claves, contraseñas)                | ❌ NUNCA                    |
| `.env.example`   | Template del `.env` sin valores reales, para que el equipo lo copie | ✅ SÍ                       |
| `.gitignore`     | Archivo que le dice a Git qué archivos ignorar                      | ✅ SÍ                       |
| `django-environ` | Librería que lee el `.env` y convierte tipos automáticamente        | ✅ SÍ (en requirements.txt) |
| `python-dotenv`  | Librería alternativa más simple para leer archivos `.env`           | ✅ SÍ (en requirements.txt) |
| `.venv/`         | Entorno virtual (¡NO es lo mismo que `.env`!)                       | ❌ NUNCA                    |

## Tabla de Comandos

| Acción                                 | Comando                                                                                                      |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| Instalar django-environ                | `pip install django-environ`                                                                                 |
| Instalar python-dotenv                 | `pip install python-dotenv`                                                                                  |
| Crear el `.env`                        | `touch .env` (y luego editarlo)                                                                              |
| Copiar el template                     | `cp .env.example .env`                                                                                       |
| Verificar que `.env` está en gitignore | `cat .gitignore \| grep .env`                                                                                |
| Generar una SECRET_KEY nueva           | `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |

## ✅ Checklist de Seguridad (Revisa Esto en CADA Proyecto)

- [ ] El archivo `.env` existe y contiene las variables secretas
- [ ] El archivo `.env` está listado en `.gitignore`
- [ ] El archivo `.env.example` existe y NO tiene valores reales
- [ ] El `settings.py` lee las variables con `env()`, NO tiene secretos hardcodeados
- [ ] `DEBUG` tiene `default=False` como valor por defecto
- [ ] Las variables críticas (`SECRET_KEY`) NO tienen valor por defecto
- [ ] El `requirements.txt` incluye `django-environ` o `python-dotenv`
- [ ] Las contraseñas se comparten por canales seguros, NO por email/Slack

---

---

## 📚 Bibliografía y Fuentes

- _GitGuardian. (2024). The State of Secrets Sprawl 2024: 12.8 million hardcoded secrets detected._ [https://www.gitguardian.com/state-of-secrets-sprawl-report-2024](https://www.gitguardian.com/state-of-secrets-sprawl-report-2024)

- _Verizon. (2024). Data Breach Investigations Report (DBIR) 2024._ [https://www.verizon.com/business/resources/reports/dbir/](https://www.verizon.com/business/resources/reports/dbir/)

- _Django Software Foundation. (2024). Django Settings — Security considerations._ [https://docs.djangoproject.com/en/stable/topics/settings/](https://docs.djangoproject.com/en/stable/topics/settings/)

- _django-environ contributors. (2024). django-environ documentation._ [https://django-environ.readthedocs.io/](https://django-environ.readthedocs.io/)

- _Saulet, T. (2024). python-dotenv documentation._ [https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

- _GitHub. (2024). Secret scanning and push protection._ [https://docs.github.com/en/code-security/secret-scanning](https://docs.github.com/en/code-security/secret-scanning)

- _Hoffman, A. (2015). Dev put AWS keys on GitHub. Then BAD things happened._ [https://www.theregister.com/2015/01/06/dev_blunder_shows_github_crawling_with_credential_stealing_bots/](https://www.theregister.com/2015/01/06/dev_blunder_shows_github_crawling_with_credential_stealing_bots/)

---
