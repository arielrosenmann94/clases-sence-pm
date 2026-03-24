# 🛠️ Django — Módulo 7 · Clase 11

## El Sitio Administrativo de Django

---

> _"Un sistema sin panel de administración obliga al desarrollador a hacer el trabajo de un operador. El admin de Django rompe esa trampa desde el día uno."_

---

## ¿Qué vas a aprender hoy?

- 🏗️ Qué es el sitio administrativo y por qué existe
- ⚙️ Qué aplicaciones lo hacen funcionar
- 👑 Qué es un superusuario y en qué se diferencia de un usuario normal
- 📋 Cómo Django muestra modelos en el panel sin que escribas HTML
- 🎨 Qué herramientas existen para personalizar esa visualización
- 🔐 Cómo funciona el sistema de usuarios, grupos y permisos
- 🛡️ Cómo se protegen las vistas de la aplicación según permisos
- 📡 Qué son las señales y para qué sirven en auditoría

---

---

# EL PROBLEMA QUE EL ADMIN RESUELVE

---

## ¿Por qué existe el sitio administrativo?

Cuando un desarrollador construye un sistema con Django, los datos viven en una base de datos. Para agregar, editar o eliminar esos datos existen dos caminos:

**Camino 1 — Sin admin:** Abrir una terminal, entrar al shell de Django (un intérprete Python especial), importar el modelo, crear el objeto manualmente en código Python, confirmarlo. Esto requiere conocimientos de programación y acceso al servidor.

**Camino 2 — Con admin:** Abrir el navegador, ir a `/admin/`, completar un formulario visual, hacer clic en Guardar.

El **sitio administrativo de Django** es una interfaz web completa, generada automáticamente, que permite gestionar todos los datos del sistema sin código, sin SQL, y sin conocimientos técnicos avanzados.

> 💡 **¿Para quién es el admin?**
> No es para los usuarios finales del sistema. Es para el equipo interno: administradores, editores de contenido, operadores de datos. Los usuarios finales tienen su propia interfaz pública.

---

## ¿Qué genera Django automáticamente?

Cuando registras un modelo en el admin, Django crea sin que escribas HTML:

```
                    Modelo "Producto"
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    Lista paginada   Formulario       Confirmación
    de todos los     para crear       de eliminación
    productos        y editar
```

Cada elemento tiene validación, mensajes de éxito, paginación y navegación. Todo generado en tiempo real a partir de la definición del modelo.

---

---

# PARTE I — LAS BASES DEL SISTEMA

---

## Las aplicaciones que hacen funcionar el admin

El sitio administrativo no es una sola aplicación — es el resultado de seis aplicaciones de Django trabajando juntas. Todas vienen incluidas en cualquier proyecto nuevo dentro de `INSTALLED_APPS`:

```
INSTALLED_APPS = [
    'django.contrib.admin',         ← el panel en sí
    'django.contrib.auth',          ← usuarios, grupos, permisos
    'django.contrib.contenttypes',  ← registro interno de modelos
    'django.contrib.sessions',      ← gestión de sesión activa
    'django.contrib.messages',      ← mensajes de éxito/error
    'django.contrib.staticfiles',   ← CSS y JS del panel
]
```

| Aplicación             | Su rol en el admin                                                |
| ---------------------- | ----------------------------------------------------------------- |
| `contrib.admin`        | Genera las páginas, los formularios y las URLs del panel          |
| `contrib.auth`         | Verifica quién entra y qué puede hacer                            |
| `contrib.contenttypes` | Le dice al admin qué modelos existen en el proyecto               |
| `contrib.sessions`     | Recuerda quién está logueado entre una página y la siguiente      |
| `contrib.messages`     | Muestra «Producto guardado exitosamente» después de cada acción   |
| `contrib.staticfiles`  | Carga los estilos visuales del panel (el CSS gris característico) |

> ⚠️ Si falta cualquiera de estas seis apps, el panel deja de funcionar. Son una cadena de dependencias — no piezas independientes.

---

## La URL del panel

El panel vive en una URL que se configura en `urls.py` del proyecto. Una sola línea registra automáticamente todas las rutas internas:

```python
path('admin/', admin.site.urls)
```

Con esa línea, Django genera automáticamente:

| URL                                | Qué muestra                          |
| ---------------------------------- | ------------------------------------ |
| `/admin/`                          | Formulario de login del panel        |
| `/admin/tienda/producto/`          | Lista de todos los productos         |
| `/admin/tienda/producto/add/`      | Formulario para crear un producto    |
| `/admin/tienda/producto/3/change/` | Formulario para editar el producto 3 |
| `/admin/tienda/producto/3/delete/` | Confirmación de eliminación          |

Estas URLs no las escribe el desarrollador. Django las construye a partir de los modelos registrados.

---

---

# PARTE II — EL SUPERUSUARIO

---

## Tres niveles de acceso en Django

Django distingue tres tipos de usuario según sus atributos:

```
           Usuario Normal                  Staff                   Superusuario
               👤                           👮                          👑
               │                            │                            │
        is_staff = False            is_staff = True             is_staff = True
        is_superuser = False        is_superuser = False        is_superuser = True
               │                            │                            │
        No accede al admin           Accede al admin             Accede al admin
        No tiene permisos          Solo los asignados          TODOS los permisos
```

**El superusuario** no tiene restricciones. No importa qué permisos existan en el sistema: el superusuario siempre puede hacer todo. Es el administrador de administradores.

---

## ¿Cómo Django protege las contraseñas?

Este es un concepto de seguridad fundamental que todo desarrollador debe entender:

Django **nunca guarda contraseñas**. Guarda el resultado de una función matemática llamada **hash**.

```
Contraseña real → Función hash → Resultado almacenado
"mi_clave_123"  →    PBKDF2    → "pbkdf2_sha256$260000$..."

                                           ↓
                            Esto es lo que está en la base de datos.
                            No hay forma matemática de revertirlo.
```

Cuando alguien inicia sesión:

```
Contraseña ingresada → Función hash → Resultado
        ↓                                 ↓
                     ¿Son iguales? → Sí ✅ / No ❌
```

Django compara hashes — nunca texto plano. Si alguien roba la base de datos, no puede recuperar las contraseñas originales.

> 💡 El algoritmo por defecto de Django es **PBKDF2 con SHA256** — uno de los más seguros para almacenamiento de contraseñas.

---

---

# PARTE III — REGISTRAR MODELOS EN EL ADMIN

---

## El archivo `admin.py`

Cada app de Django tiene un archivo `admin.py`. Su propósito es exclusivo: decirle al panel qué modelos debe mostrar y cómo presentarlos.

```
  tienda/
  ├── models.py    ← define la estructura de los datos
  ├── admin.py     ← define cómo el panel muestra esos datos
  ├── views.py
  └── urls.py
```

La relación entre ambos archivos es:

```
models.py                      admin.py
──────────                     ──────────
class Producto: ────────────→  admin.site.register(Producto)
  nombre                           ↓
  precio                    Django genera el CRUD visual
  stock                     automáticamente
```

---

## El método `__str__` y su importancia en el admin

Cuando el panel lista los objetos de un modelo, necesita mostrarlos como texto. El método `__str__` del modelo le dice exactamente qué texto mostrar:

```
Sin __str__                     Con __str__
──────────────────              ──────────────────
Producto object (1)             Teclado Mecánico
Producto object (2)             Mouse Inalámbrico
Producto object (3)             Monitor 4K
```

`__str__` no es exclusivo del admin. Funciona en cualquier lugar donde Python necesite representar el objeto como texto (el shell, los logs, los templates).

---

## Qué significa «registrar» un modelo

Registrar un modelo en el admin es una declaración: "este modelo debe ser visible y editable desde el panel". Sin ese registro, el modelo existe en la base de datos pero el admin no lo conoce.

```python
# La declaración más simple posible:
admin.site.register(Producto)
```

Con esta línea, Django hace en tiempo real:

1. Detecta todos los campos del modelo `Producto`
2. Genera un formulario HTML con esos campos
3. Agrega validaciones automáticas según el tipo de campo
4. Crea las 4 URLs del CRUD (listar, crear, editar, eliminar)
5. Muestra la sección "TIENDA → Productos" en el panel

---

---

# PARTE IV — PERSONALIZAR LA VISTA DEL ADMIN

---

## El problema del registro básico

El registro básico muestra el modelo, pero con limitaciones claras:

- La lista tiene **una sola columna** (el texto del `__str__`)
- No existe un **buscador**
- No existen **filtros** laterales
- El **orden** es el que devuelve la base de datos — arbitrario

Para todos estos problemas existe `ModelAdmin`.

---

## ¿Qué es `ModelAdmin`?

`ModelAdmin` es una clase de Django que configura **cómo un modelo se presenta en el panel**. No modifica los datos — solo la visualización y la experiencia de uso.

```
       Modelo (datos)           ModelAdmin (presentación)
       ──────────────           ────────────────────────
       - nombre                 - qué columnas mostrar
       - precio                 - qué campos buscar
       - stock                  - qué filtros habilitar
       - categoria              - cómo ordenar la lista
```

Las cuatro configuraciones principales:

| Atributo        | Qué controla                              | Ejemplo                         |
| --------------- | ----------------------------------------- | ------------------------------- |
| `list_display`  | Las columnas de la tabla en el listado    | `('nombre', 'precio', 'stock')` |
| `search_fields` | Los campos donde busca el buscador        | `('nombre', 'categoria')`       |
| `list_filter`   | Los filtros clickeables del panel lateral | `('categoria',)`                |
| `ordering`      | El orden por defecto de la lista          | `('nombre',)` o `('-precio',)`  |

El prefijo `-` en `ordering` indica orden descendente (de mayor a menor).

---

## El decorador `@admin.register`

Django ofrece dos formas de registrar un modelo con su `ModelAdmin`. Son equivalentes — producen exactamente el mismo resultado:

```python
# Forma 1 — registro explícito al final
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')

admin.site.register(Producto, ProductoAdmin)

# Forma 2 — decorador (forma moderna, preferida)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
```

La forma con decorador es preferida porque mantiene el modelo y su configuración juntos visualmente. Proyectos profesionales la usan siempre.

---

## Personalizar el nombre y encabezado del panel

Por defecto el panel muestra el texto «Django administration». Se puede cambiar con tres variables:

```
admin.site.site_header = "Administración de Mi Tienda"
                               ↑ Texto del encabezado grande (visible en todas las páginas)

admin.site.site_title  = "Panel Admin"
                               ↑ Texto en la pestaña del navegador

admin.site.index_title = "Bienvenido al Panel de Control"
                               ↑ Subtítulo en la página de inicio del admin
```

---

## Inlines — gestionar relaciones desde la misma página

Cuando dos modelos están relacionados por una ForeignKey, los **Inlines** permiten ver y editar el modelo secundario desde dentro de la página del modelo principal.

**La situación sin Inlines:**

```
Para agregar imágenes a un producto el administrador debe:
1. Ir a /admin/tienda/producto/  → editar el producto
2. Ir a /admin/tienda/imagen/   → agregar la imagen, seleccionar el producto
   Dos secciones distintas para completar una tarea lógicamente unida.
```

**La situación con Inlines:**

```
Dentro de /admin/tienda/producto/3/change/  (la página del producto)
├── Campos del Producto (nombre, precio, stock...)
└── SECCIÓN IMAGENES (el Inline)
    ├── Imagen 1: url=... alt=...
    ├── Imagen 2: url=... alt=...
    └── [Formulario vacío para agregar Imagen 3]
   Una sola página para gestionar ambos modelos.
```

Existen dos variantes visuales de Inline:

| Tipo            | Presentación                                        |
| --------------- | --------------------------------------------------- |
| `TabularInline` | Tabla compacta — cada objeto en una fila horizontal |
| `StackedInline` | Bloques verticales — cada objeto ocupa más espacio  |

El atributo `extra` define cuántos formularios vacíos se muestran para agregar nuevos registros relacionados.

---

---

# PARTE V — USUARIOS, GRUPOS Y PERMISOS

---

## El modelo de autorización de Django

Django tiene un sistema integrado para controlar quién puede hacer qué. Se organiza en tres capas:

```
        ┌──────────────────────────────────────────┐
        │              USUARIO                      │
        │   - nombre, email, contraseña            │
        │   - is_staff, is_active, is_superuser     │
        └─────────────────┬────────────────────────┘
                          │ pertenece a
             ┌────────────▼────────────┐
             │          GRUPO          │
             │    (colección de        │
             │      permisos)          │
             └────────────┬────────────┘
                          │ tiene
             ┌────────────▼────────────┐
             │        PERMISO          │
             │  acción específica      │
             │  sobre un modelo        │
             └─────────────────────────┘
```

Un usuario puede tener permisos de dos formas:

- **Directamente** — asignados uno por uno al usuario
- **A través de grupos** — el usuario pertenece a un grupo que tiene los permisos

Ambas formas son transparentes: `user.has_perm('tienda.change_producto')` devuelve `True` sin importar por qué camino llegó el permiso.

---

## Los cuatro permisos automáticos

Cuando Django migra un modelo, genera automáticamente cuatro permisos en la tabla `auth_permission`. Para el modelo `Producto` de la app `tienda`:

| Permiso                  | Permite                      |
| ------------------------ | ---------------------------- |
| `tienda.add_producto`    | Crear nuevos registros       |
| `tienda.change_producto` | Editar registros existentes  |
| `tienda.delete_producto` | Eliminar registros           |
| `tienda.view_producto`   | Ver registros (solo lectura) |

El formato siempre es: `nombre_de_app.accion_nombre_modelo` — todo en minúsculas.

Estos permisos aparecen automáticamente en el panel y se pueden asignar a cualquier usuario o grupo.

---

## Permisos personalizados

Los cuatro permisos automáticos cubren las operaciones básicas. Pero las aplicaciones reales tienen necesidades del negocio que van más allá:

- Solo el jefe de contenidos puede **aprobar** un documento antes de publicarlo
- Solo contabilidad puede **exportar** el listado completo de ventas
- Solo el gerente puede **ver el precio de costo** de un producto

Para eso existen los **permisos personalizados**, que se definen dentro del modelo en la clase `Meta`:

```python
class Documento(models.Model):
    titulo    = models.CharField(max_length=255)
    contenido = models.TextField()

    class Meta:
        permissions = [
            ('puede_aprobar',  'Puede aprobar documentos'),
            ('puede_exportar', 'Puede exportar el listado completo'),
        ]
        # Tupla: ('codename', 'Descripción legible')
        # codename: identificador interno — sin espacios, todo en minúsculas
        # Descripción: texto en español que aparece en el panel admin
```

Después de ejecutar las migraciones, estos permisos aparecen en el panel y pueden asignarse como cualquier otro. Se verifican con:

```python
user.has_perm('tienda.puede_aprobar')   # True o False
```

---

## Grupos — administrar permisos por rol

Un **grupo** es una colección de permisos con un nombre. Es la herramienta para gestionar permisos a escala.

**El problema sin grupos:**

```
10 permisos × 50 usuarios = 500 asignaciones manuales
Si cambia un permiso → hay que actualizar 50 usuarios uno por uno
```

**La solución con grupos:**

```
Grupo "Editores" = [add_producto, change_producto, view_producto]
                       ↓
Agregar 50 usuarios al grupo "Editores"
= cada usuario hereda automáticamente los 3 permisos
                       ↓
Si cambia un permiso en el grupo → los 50 usuarios se actualizan solos
```

La verificación funciona de forma transparente. El código que verifica permisos no necesita saber si el permiso viene directo o de un grupo:

```python
# Esta línea funciona igual sin importar cómo llegó el permiso
if request.user.has_perm('tienda.change_producto'):
    # tiene el permiso — ya sea directo o heredado del grupo
```

> 💡 **Recomendación profesional**: siempre verificar con `has_perm()`, no con el nombre del grupo. Si el grupo «Editores» se renombra a «Contentistas», el código que verifica `has_perm()` sigue funcionando. El que verifica el nombre del grupo se rompe.

---

## Personalizar el admin de usuarios

El panel ya tiene una sección para gestionar usuarios (`/admin/auth/user/`). Esta sección también puede configurarse con `UserAdmin`, que funciona igual que `ModelAdmin` pero está diseñada para el modelo `User` de Django.

```python
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    list_filter   = ('is_staff', 'is_active', 'groups')
```

> ⚠️ **Importante**: El modelo `User` de Django ya viene registrado por defecto. Para reemplazarlo con la versión personalizada hay que primero desregistrarlo con `admin.site.unregister(User)` y luego registrar el personalizado. Si no se hace el paso de desregistrar, Django lanza un error `AlreadyRegistered`.

---

---

# PARTE VI — PROTEGER VISTAS CON MIXINS

---

## El problema: las vistas públicas son accesibles para cualquiera

Gestionar permisos en el admin es útil, pero no es suficiente. El admin es el panel de gestión interna. La aplicación pública tiene sus propias vistas, y si no están protegidas, cualquier persona con la URL puede acceder.

```
Situación sin protección:
URL /productos/5/editar/ → cualquier persona puede acceder
                           sin importar si inició sesión
                           sin importar si tiene permiso
```

Los **Mixins** de Django resuelven esto en las vistas de clase.

---

## `LoginRequiredMixin` — exigir sesión activa

Un Mixin es una clase que agrega comportamiento sin reemplazar la funcionalidad de la vista principal. `LoginRequiredMixin` agrega un solo comportamiento: verificar que el usuario tiene una sesión activa antes de ejecutar la vista.

```
Cómo funciona:

Usuario visita /productos/5/editar/
       ↓
LoginRequiredMixin verifica: ¿hay sesión activa?
       │
       ├── NO  → Redirige a LOGIN_URL
       │         (guarda la URL original en ?next= para volver después del login)
       │
       └── SÍ  → La vista se ejecuta ✅
```

El Mixin **siempre va primero** en la lista de herencia de la clase:

```python
class EditarProductoView(LoginRequiredMixin, UpdateView):
#                        ↑ primero         ↑ después
```

Esto no es convención — es técnico. Python resuelve la herencia múltiple de izquierda a derecha (MRO). Si `UpdateView` fuera primero, la vista ejecutaría su lógica antes de verificar el login.

---

## `PermissionRequiredMixin` — exigir un permiso específico

Tener sesión no siempre es suficiente. En muchos casos necesitas verificar que además de estar logueado, el usuario tiene un permiso específico.

`PermissionRequiredMixin` combina ambas verificaciones:

```
Cómo funciona (con ambos Mixins):

Usuario visita /productos/5/editar/
       ↓
① LoginRequiredMixin — ¿hay sesión?
       ├── NO  → Redirige a /login/?next=/productos/5/editar/
       └── SÍ  → continúa ↓

② PermissionRequiredMixin — ¿tiene 'tienda.change_producto'?
       ├── NO  → Error HTTP 403 (Acceso denegado)
       └── SÍ  → continúa ↓

③ La vista UpdateView se ejecuta ✅
```

El atributo `raise_exception = True` controla qué sucede cuando el usuario tiene sesión pero no tiene el permiso:

| `raise_exception` | Comportamiento                                        |
| ----------------- | ----------------------------------------------------- |
| `True`            | Muestra error 403 — correcto para alguien ya logueado |
| `False` (defecto) | Redirige al login — confuso para alguien ya logueado  |

El orden en la herencia sigue la misma lógica: de más general a más específico:

```python
class EditarProductoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#                        ↑ 1° verifica     ↑ 2° verifica           ↑ 3° ejecuta
#                           sesión            permiso                  la vista
```

---

## Las tres variables de redirección en `settings.py`

`LoginRequiredMixin` necesita saber adónde enviar al usuario cuando no tiene sesión. Estas variables centralizan ese comportamiento:

```python
LOGIN_URL           = '/login/'
# Adónde redirigir cuando se detecta que no hay sesión activa

LOGIN_REDIRECT_URL  = '/dashboard/'
# Adónde ir después de un login exitoso (cuando no hay ?next= en la URL)

LOGOUT_REDIRECT_URL = '/login/'
# Adónde ir después de cerrar sesión
```

Sin `LOGIN_URL`, Django usa `/accounts/login/` por defecto — una URL que generalmente no existe en el proyecto y provoca un error 404.

---

## Páginas de error personalizadas

Cuando Django detecta un error 403 (acceso denegado), busca automáticamente el archivo `templates/403.html` y lo muestra. No necesita configuración adicional para eso.

Si se desea una vista más compleja para el error, se puede definir un `handler403` en el `urls.py` del proyecto, que apunta a una función de vista personalizada.

Los errores que Django puede personalizar con templates propios:

| Código | Error        | Template   | Cuándo ocurre                               |
| ------ | ------------ | ---------- | ------------------------------------------- |
| 400    | Bad Request  | `400.html` | Request mal formado                         |
| 403    | Forbidden    | `403.html` | El usuario no tiene permiso                 |
| 404    | Not Found    | `404.html` | La URL no existe o el objeto no se encontró |
| 500    | Server Error | `500.html` | Error interno del servidor                  |

---

---

# PARTE VII — SEÑALES Y AUDITORÍA

---

## ¿Qué es una señal?

Una **señal** (signal) es un mecanismo de Django que permite ejecutar código automáticamente cuando ocurre un evento en la base de datos, sin modificar la vista ni el admin que causó el evento.

```
           Vista o Admin
                │
                │ guarda un Producto
                ↓
         Base de datos
                │
                │ dispara el evento post_save
                ↓
    ┌───────────────────────┐
    │    Tu función         │
    │    se ejecuta         │
    │    automáticamente ✅  │
    └───────────────────────┘
```

La función «escucha» el evento pero **no interfiere** con él. El guardado ya ocurrió antes de que la función se ejecute.

---

## Las señales más utilizadas

| Señal         | Cuándo se dispara                                          |
| ------------- | ---------------------------------------------------------- |
| `post_save`   | Después de guardar un objeto (ya sea creación o edición)   |
| `post_delete` | Después de eliminar un objeto                              |
| `pre_save`    | Antes de guardar — permite modificar el objeto antes       |
| `pre_delete`  | Antes de eliminar — permite hacer validaciones o respaldos |

El decorador `@receiver` conecta una función Python a una señal de un modelo específico:

```python
@receiver(post_save, sender=Producto)
def registrar_cambio(sender, instance, created, **kwargs):
    # sender   → el modelo (Producto)
    # instance → el objeto concreto que se guardó
    # created  → True si fue creado, False si fue editado
```

---

## ¿Para qué sirven en un sistema real?

En producción, las señales no usan `print()`. Se conectan a sistemas reales:

| Uso                | Qué hace la señal                                              |
| ------------------ | -------------------------------------------------------------- |
| **Auditoría**      | Guarda en una tabla quién hizo qué cambio y cuándo             |
| **Notificaciones** | Envía un email o una notificación cuando se crea un objeto     |
| **Sincronización** | Actualiza datos en otro sistema cuando algo cambia aquí        |
| **Caché**          | Invalida el caché cuando un registro se modifica               |
| **Logs**           | Registra las operaciones en el sistema de logging del servidor |

Las señales son la forma correcta de separar estas responsabilidades sin mezclarlas dentro de las vistas o del admin.

---

---

# RESUMEN — Lo que Django hace solo vs. lo que define el developer

---

```
DJANGO LO HACE SOLO                 EL DEVELOPER LO DEFINE
────────────────────────────────    ────────────────────────────────
Formularios del admin               Qué modelos registrar
Validación de campos                Cómo presentar cada modelo
Hash de contraseñas                 Permisos personalizados
4 permisos por modelo               Grupos y sus permisos
Login/Logout funcional              Qué vistas requieren sesión
Sesiones entre páginas              Qué vistas requieren permiso
Tabla auth_permission               Template del error 403
Variable 'user' en templates        Señales de auditoría
```

---

## Glosario de la clase

| Concepto                      | Qué es                                                                 |
| ----------------------------- | ---------------------------------------------------------------------- |
| **Sitio administrativo**      | Interfaz web generada por Django para gestionar datos sin SQL          |
| **Superusuario**              | Usuario con acceso total al sistema — `is_staff` y `is_superuser=True` |
| **Hash de contraseña**        | Resultado matemático unidireccional que Django usa en lugar del texto  |
| **`admin.py`**                | Archivo donde se registran los modelos y se configura su visualización |
| **`admin.site.register`**     | Declaración que agrega un modelo al panel del admin                    |
| **`ModelAdmin`**              | Clase para personalizar cómo se presenta un modelo en el panel         |
| **`list_display`**            | Columnas que aparecen en la tabla del listado                          |
| **`search_fields`**           | Campos que usa el buscador del listado                                 |
| **`list_filter`**             | Campos que generan filtros clickeables en el panel lateral             |
| **`TabularInline`**           | Editar modelo relacionado como tabla dentro del modelo principal       |
| **`StackedInline`**           | Idem pero con formato vertical, más espacio por objeto                 |
| **Permiso**                   | Autorización para una acción específica sobre un modelo                |
| **Grupo**                     | Colección de permisos con nombre — se asigna a usuarios                |
| **`has_perm()`**              | Verifica si el usuario tiene un permiso — directo o por grupo          |
| **`LoginRequiredMixin`**      | Clase que exige sesión activa antes de ejecutar la vista               |
| **`PermissionRequiredMixin`** | Clase que exige un permiso específico antes de ejecutar la vista       |
| **`raise_exception`**         | Si `True`, sin permiso devuelve 403 en lugar de redirigir al login     |
| **Señal (signal)**            | Evento de Django que ejecuta código automático al cambiar la BD        |
| **`post_save`**               | Señal que se dispara después de guardar un objeto                      |
| **`@receiver`**               | Decorador que conecta una función a una señal de un modelo             |
| **`LOGIN_URL`**               | URL de login — a donde redirige cuando no hay sesión activa            |
| **`handler403`**              | Variable que apunta a la vista personalizada del error 403             |

---

> _"El panel de administración de Django es una herramienta de equipo, no un atajo para el desarrollador. Bien configurado, le da a cada persona del equipo exactamente el acceso que necesita — y ningún acceso más."_

---
