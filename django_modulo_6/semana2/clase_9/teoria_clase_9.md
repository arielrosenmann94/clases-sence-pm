# 🔐 Django — Módulo 6 · Clase 9

## Autenticación y Autorización

---

> _"Hasta ahora, cualquiera con la URL podía ver todo. Hoy cambia eso."_

---

## ¿De qué trata esta clase?

Toda aplicación real necesita responder dos preguntas:

- **¿Quién eres?** → Autenticación
- **¿Qué puedes hacer?** → Autorización

Django trae todo esto listo para usar. No hay que construirlo desde cero.

---

---

# Parte I — Qué trae Django por defecto

---

> Sin instalar nada extra, Django ya tiene un sistema de usuarios completo.

Cuando se crea un proyecto nuevo con `django-admin startproject`, Django incluye automáticamente en `INSTALLED_APPS`:

```
django.contrib.auth
```

Eso activa:

| Qué            | Para qué sirve                                  |
| -------------- | ----------------------------------------------- |
| Modelo `User`  | Guarda los usuarios del sistema                 |
| Login / Logout | Vistas predefinidas listas para usar            |
| Sesiones       | Recuerda al usuario entre requests              |
| Permisos       | Controla qué puede hacer cada usuario           |
| Grupos         | Agrupa usuarios por rol                         |
| Hasheo         | Las contraseñas nunca se guardan en texto plano |

---

## Las tablas que crea Django

Al correr `migrate` por primera vez, Django crea estas tablas automáticamente:

| Tabla              | Contenido                         |
| ------------------ | --------------------------------- |
| `auth_user`        | Todos los usuarios                |
| `auth_group`       | Los grupos (Editores, Admins…)    |
| `auth_permission`  | Todos los permisos disponibles    |
| `auth_user_groups` | Qué usuario pertenece a qué grupo |

**No se crean manualmente.** Django las genera con las migraciones iniciales.

---

---

# Parte II — Login y Logout

---

> Django ya tiene las vistas de login y logout escritas. Solo hay que conectar las URLs.

---

## Paso 1 — Conectar las URLs

```python
# urls.py
from django.contrib.auth import views as auth_views   # importa las vistas de auth que Django ya tiene escritas
from django.urls import path

urlpatterns = [
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #    ↑ URL       ↑ vista de Django ya hecha       ↑ qué template usar       ↑ nombre para {% url %}
    path('logout/', auth_views.LogoutView.as_view(),                          name='logout'),
    #    ↑ URL       ↑ vista de Django ya hecha — no necesita template
]
```

**`LoginView`** → recibe el formulario, verifica usuario y contraseña contra la BD, y si es correcto crea la sesión.
**`LogoutView`** → destruye la sesión activa. No muestra ninguna página — solo redirige.

---

## Paso 2 — Configurar redirecciones en `settings.py`

El destino por defecto después del login es `/accounts/profile/` — que no existe.
Hay que indicarle adónde ir:

```python
# settings.py
LOGIN_REDIRECT_URL  = '/dashboard/'   # ← adónde ir DESPUÉS de un login exitoso
LOGIN_URL           = '/login/'       # ← adónde redirigir si alguien sin sesión toca una vista protegida
LOGOUT_REDIRECT_URL = '/login/'       # ← adónde ir DESPUÉS de cerrar sesión
```

**Sin estas 3 líneas**, Django usa `/accounts/profile/` como destino por defecto — una URL que generalmente no existe y da un error 404.

---

## Paso 3 — El template del formulario de login

Django espera recibir exactamente dos campos: `username` y `password`.

```html
<!-- templates/login.html -->
{% extends 'base.html' %} {% block content %}

<form method="POST">
  {% csrf_token %}
  <input type="hidden" name="next" value="{{ next }}" />

  {% if form.errors %}
  <div class="alert alert-danger">Usuario o contraseña incorrectos.</div>
  {% endif %}

  <div class="mb-3">
    <label class="form-label">Usuario</label>
    <input type="text" name="username" class="form-control" autofocus />
  </div>
  <div class="mb-3">
    <label class="form-label">Contraseña</label>
    <input type="password" name="password" class="form-control" />
  </div>

  <button type="submit" class="btn btn-primary w-100">Entrar</button>
</form>

{% endblock %}
```

**`{{ next }}`** → variable que Django pone automáticamente. Dice adónde volver después del login.
**`{% if form.errors %}`** → solo aparece si el usuario o la contraseña estuvieron mal.

---

## Acceder al usuario en una vista

```python
def dashboard(request):
    # request.user siempre existe — Django lo inyecta en cada request automáticamente
    # Si no hay sesión activa → request.user es AnonymousUser (objeto especial, no tiene username real)
    # Si hay sesión activa    → request.user es el objeto User de la base de datos

    if request.user.is_authenticated:   # → True si hay sesión, False si es anónimo
        nombre = request.user.username  # → el nombre de usuario guardado en auth_user
    else:
        nombre = "visitante"            # → fallback para usuarios sin sesión

    return render(request, 'dashboard.html', {'nombre': nombre})
```

**`request.user`** es el objeto más importante de la sesión. Tiene: `.username`, `.email`, `.is_staff`, `.is_superuser`, `.groups`, `.has_perm()`.

Y en **cualquier template**, sin pasarlo en el contexto, `user` ya está disponible:

```html
{% if user.is_authenticated %} Hola, {{ user.username }}
<a href="{% url 'logout' %}">Cerrar sesión</a>
{% else %}
<a href="{% url 'login' %}">Iniciar sesión</a>
{% endif %}
```

---

---

# Parte III — Proteger vistas

---

> Tener login no es suficiente. Hay que decidir qué vistas requieren sesión.

---

## Para vistas de función: `@login_required`

```python
from django.contrib.auth.decorators import login_required   # importar el decorador

@login_required           # ← intercepta el request ANTES de ejecutar la vista
def dashboard(request):   # ← si el usuario no tiene sesión, nunca llega aquí
    return render(request, 'dashboard.html')
```

**¿Qué hace exactamente `@login_required`?**

1. Verifica si `request.user.is_authenticated` es `True`.
2. Si es `False` → redirige a `LOGIN_URL` + `?next=/dashboard/`.
3. Si es `True` → ejecuta la vista normalmente.

**El `?next=`** guarda la URL original. Después del login, `LoginView` lleva al usuario de vuelta ahí automaticamente.

---

## Para vistas de clase: `LoginRequiredMixin`

```python
from django.contrib.auth.mixins import LoginRequiredMixin   # importar el mixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):   # ← LoginRequiredMixin SIEMPRE primero a la izquierda
    template_name = 'dashboard.html'                    # ← el template que renderiza si el usuario tiene sesión
```

**¿Por qué el Mixin va primero?** Python resuelve la herencia múltiple de izquierda a derecha (MRO). Si `LoginRequiredMixin` va despues de `TemplateView`, la vista se ejecuta antes de verificar la sesión.

**Equivalencia**: `LoginRequiredMixin` en una vista de clase = `@login_required` en una vista de función. Hacen exactamente lo mismo.

---

---

# Parte IV — Permisos

---

> Autenticación = sesión activa. Permiso = qué puede hacer con esa sesión.

---

## Django genera 4 permisos por modelo automáticamente

Cuando se migra un modelo llamado `Producto` en una app `tienda`:

| Permiso                  | Qué permite                 |
| ------------------------ | --------------------------- |
| `tienda.add_producto`    | Crear nuevos productos      |
| `tienda.change_producto` | Editar productos existentes |
| `tienda.delete_producto` | Eliminar productos          |
| `tienda.view_producto`   | Ver productos               |

Aparecen solos en `auth_permission`. Se asignan desde el Admin.

---

## Verificar un permiso en una vista de función

```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required                                                  # primera barrera: ¿tiene sesión?
@permission_required('tienda.change_producto', raise_exception=True)  # segunda barrera: ¿tiene este permiso?
def editar_producto(request, pk):   # ← solo llega aquí si pasó las dos barreras
    ...
```

**El orden de los decoradores importa**: se aplican de abajo hacia arriba. Primero se verifica el permiso, luego el login. Ponerlos en ese orden garantiza que si el usuario no tiene sesión, va al login — no al 403.

**`raise_exception=True`** → si el usuario YA tiene sesión pero no tiene el permiso → muestra error 403. Sin ese parámetro, Django lo mandaría de vuelta al login, lo cual es confuso para alguien que ya inició sesión.

---

## Verificar un permiso de forma manual

```python
from django.core.exceptions import PermissionDenied   # excepción especial que dispara el error 403

@login_required                                       # primero verificar que tiene sesión
def editar_producto(request, pk):
    if not request.user.has_perm('tienda.change_producto'):  # ← verifica el permiso dentro de la vista
        raise PermissionDenied                               # ← lanza la excepción → Django muestra 403.html
    # si llegó hasta aquí, tiene el permiso
    ...
```

**¿Cuándo usar la verificación manual vs el decorador?**

- Decorador `@permission_required` → cuando el permiso aplica a **toda** la vista.
- Verificación manual → cuando el permiso aplica solo a **parte** del código (por ejemplo, solo al guardar, no al mostrar el formulario).

---

## Para vistas de clase: `PermissionRequiredMixin`

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView

class EditarProductoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    #                    ↑ verifica sesión   ↑ verifica permiso     ↑ vista que edita un registro
    model               = Producto                    # ← el modelo que edita esta vista
    fields              = ['nombre', 'precio']        # ← qué campos muestra el formulario
    template_name       = 'producto_form.html'        # ← el template del formulario
    permission_required = 'tienda.change_producto'    # ← el permiso que se verifica
    raise_exception     = True                        # ← si no tiene permiso → 403 (no redirige al login)
```

**El orden de los Mixins**: primero `LoginRequired`, luego `PermissionRequired`, luego la vista base. Mismo principio que con los decoradores — de más general a más específico.

---

## Permisos personalizados

Cuando los 4 automáticos no alcanzan, se definen en el modelo:

```python
class Documento(models.Model):
    titulo    = models.CharField(max_length=255)
    contenido = models.TextField()

    class Meta:
        permissions = [                                         # ← lista de permisos extra para este modelo
            ('puede_aprobar',  'Puede aprobar documentos'),     # ← (codename, descripción legible)
            ('puede_publicar', 'Puede publicar documentos'),   # ← el codename es lo que va en has_perm()
        ]
```

**Importante**: después de agregar `Meta.permissions`, hay que correr:

1. `python manage.py makemigrations` → genera el archivo de migración
2. `python manage.py migrate` → crea los permisos en `auth_permission`

Recién ahí aparecen en el Admin y se pueden verificar con `has_perm('app.puede_aprobar')`.

---

---

# Parte V — Grupos

---

> Un grupo = una colección de permisos con nombre. En lugar de asignar 10 permisos a cada usuario, se crea un grupo y se agregan usuarios al grupo.

---

## Flujo de trabajo con grupos

```
Crear grupo "Editores"
       ↓
Asignarle permisos al grupo
       ↓
Agregar usuarios al grupo
       ↓
El usuario hereda todos los permisos del grupo
```

---

## Código

```python
from django.contrib.auth.models import Group, Permission   # importar los modelos necesarios

# Paso 1: crear el grupo
editores = Group.objects.create(name='Editores')   # ← crea una fila en auth_group

# Paso 2: buscar el permiso y asignarlo al grupo
permiso = Permission.objects.get(codename='change_producto')  # ← busca el permiso en auth_permission
editores.permissions.add(permiso)    # ← vincula el permiso al grupo (relación many-to-many)

# Paso 3: agregar el usuario al grupo
usuario.groups.add(editores)   # ← el usuario hereda TODOS los permisos del grupo
```

**Lo importante**: `has_perm('tienda.change_producto')` devuelve `True` si el usuario tiene ese permiso, ya sea asignado directamente o a través de un grupo. El código de verificación no cambia — es transparente.

---

## Verificar en una vista

```python
if request.user.groups.filter(name='Editores').exists():  # ← filtra los grupos del usuario por nombre
    # el usuario pertenece al grupo Editores → hacer algo
    pass
```

**¿Cuándo verificar grupos vs permisos?**

| Verificar grupo                                               | Verificar permiso                                     |
| ------------------------------------------------------------- | ----------------------------------------------------- |
| `user.groups.filter(name='Editores').exists()`                | `user.has_perm('app.change_producto')`                |
| Útil si la lógica depende del rol (no del permiso específico) | Más flexible: un permiso puede estar en varios grupos |
| Si se renombra el grupo, hay que actualizar el código         | Los permisos son estables aunque cambien los grupos   |

**Recomendación**: usar `has_perm()`. Si el día de mañana el grupo "Editores" se divide en "Editores Básicos" y "Editores Senior", el código de verificación no cambia.

---

---

# Parte VI — Accesos no autorizados

---

> Hay que decidir qué ve el usuario cuando no puede entrar.

---

## Los tres escenarios

| Situación                                       | Qué ocurre                      | Código |
| ----------------------------------------------- | ------------------------------- | ------ |
| Sin sesión, vista con `@login_required`         | Redirige a `/login/?next=/url/` | 302    |
| Con sesión, sin permiso, `raise_exception=True` | Muestra página de error         | 403    |
| Con sesión, sin permiso, sin `raise_exception`  | Redirige al login (confuso)     | 302    |

---

## La página 403

Django busca `403.html` automáticamente cuando se lanza `PermissionDenied`.
Solo hay que crear el archivo:

```html
<!-- templates/403.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1 class="display-1 text-danger">403</h1>
  <h2>Acceso denegado</h2>
  <p class="text-muted">No tienes permiso para ver esta página.</p>
  <a href="{% url 'home' %}" class="btn btn-primary">Volver al inicio</a>
</div>

{% endblock %}
```

---

## El parámetro `next`

`@login_required` agrega `?next=/url-protegida/` cuando redirige al login.
`LoginView` lo lee y, después del login, lleva al usuario a esa URL.

En el template del login, hay que asegurarse de pasar `next`:

```html
<input type="hidden" name="next" value="{{ next }}" />
```

Sin esa línea, después del login el usuario va a `LOGIN_REDIRECT_URL` y pierde la página a la que quería llegar.

---

---

# Flujo completo de autenticación

---

```
Usuario visita /dashboard/
        ↓
¿Tiene sesión activa?
        │
        ├── NO  → Redirige a /login/?next=/dashboard/
        │              ↓
        │         Completa el formulario
        │              ↓
        │         Django verifica credenciales
        │              ↓
        │         Crea sesión → redirige a /dashboard/
        │
        └── SÍ  → ¿Tiene el permiso requerido?
                        │
                        ├── NO  → Error 403
                        │
                        └── SÍ  → Ejecuta la vista ✅
```

---

---

# Lo que Django hace automáticamente

---

| Django lo hace solo         | El developer lo define           |
| --------------------------- | -------------------------------- |
| Hasheo de contraseñas       | Qué rutas requieren login        |
| Tokens de sesión            | Qué vistas requieren permisos    |
| CSRF en login               | Template del formulario de login |
| Permisos básicos por modelo | Permisos personalizados          |
| Tabla `auth_permission`     | Grupos y asignación de usuarios  |
| Redirección con `?next=`    | Template del 403                 |

---

> _"La autenticación de Django sigue el mismo principio que todo el framework: las decisiones comunes ya están tomadas. El developer elige qué proteger y con qué nivel — no cómo funciona el cifrado."_

---
