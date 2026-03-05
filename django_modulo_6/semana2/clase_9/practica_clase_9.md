# Django — Módulo 6 · Clase 9

## Práctica: Proteger el formulario del CV con login

---

> _"El formulario que construiste en la clase anterior puede editarlo cualquiera que conozca la URL. Esta clase lo vas a proteger para que solo el dueño del CV pueda acceder."_

---

## ¿Qué vamos a hacer?

En la clase 8 crearon un formulario para cargar o editar el contenido del CV desde una página propia de la aplicación — sin pasar por el admin.

El problema: esa página es pública. Cualquier persona que conozca la URL puede editarlo.

Hoy aplicamos lo que vimos en la teoría:

1. Crear la pantalla de login para el proyecto
2. Proteger la vista del formulario con `@login_required`
3. Agregar el link de cerrar sesión en la interfaz

---

---

# Paso 1 — Conectar las URLs de autenticación

---

**¿Por qué hay que hacer esto?** Django tiene las vistas de login y logout escritas, pero no las activa automáticamente. Hay que agregarlas al sistema de rutas del proyecto.

Abrir el archivo `urls.py` del **proyecto** (no el de la app) y agregar las rutas:

```python
# urls.py del PROYECTO (el que tiene path('admin/', ...))
from django.contrib.auth import views as auth_views   # ← vistas de auth de Django
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nombre_app.urls')),     # ← las urls de la app del CV

    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #    ↑ URL para el formulario de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #    ↑ URL para cerrar sesión (no necesita template)
]
```

**Claves a recordar:**

- `template_name='login.html'` — le dice a Django qué template usar para el formulario
- `name='login'` y `name='logout'` — los nombres que se usarán con `{% url %}` en los templates

---

# Paso 2 — Configurar las redirecciones en `settings.py`

---

**¿Por qué hace falta?** Por defecto, después del login Django va a `/accounts/profile/` — que no existe. Hay que decirle adónde ir.

Abrir `settings.py` y agregar al final:

```python
# settings.py

LOGIN_REDIRECT_URL  = '/'         # ← adónde ir después de un login OK (cambiar por la URL del CV)
LOGIN_URL           = '/login/'   # ← adónde ir si alguien sin sesión toca una vista protegida
LOGOUT_REDIRECT_URL = '/login/'   # ← adónde ir después de cerrar sesión
```

**Tip**: cambiar `'/'` por la URL de la vista del CV. Si la URL tiene nombre, también se puede usar el string del nombre: `'/cv/'`.

---

# Paso 3 — Crear el template del formulario de login

---

**¿Por qué se crea manualmente?** Django sabe cómo verificar las credenciales, pero el HTML del formulario es responsabilidad del developer — ahí se aplica el diseño del proyecto.

Crear el archivo `templates/login.html`. Si ya tienen un `base.html`, extenderlo:

```html
<!-- templates/login.html -->
{% extends 'base.html' %} {% block content %}

<div class="container my-5">
  <div class="row justify-content-center">
    <div class="col-md-5">
      <h2 class="mb-4">Iniciar sesión</h2>

      <!-- Este bloque solo aparece si el usuario o contraseña están mal -->
      {% if form.errors %}
      <div class="alert alert-danger">
        Usuario o contraseña incorrectos. Intenta de nuevo.
      </div>
      {% endif %}

      <form method="POST">
        {% csrf_token %}
        <!-- next guarda la URL original a la que quería ir el usuario -->
        <input type="hidden" name="next" value="{{ next }}" />

        <div class="mb-3">
          <label class="form-label">Usuario</label>
          <input type="text" name="username" class="form-control" autofocus />
          <!-- name="username" y name="password" son los nombres que espera LoginView -->
        </div>
        <div class="mb-3">
          <label class="form-label">Contraseña</label>
          <input type="password" name="password" class="form-control" />
        </div>

        <button type="submit" class="btn btn-primary w-100">Entrar</button>
      </form>
    </div>
  </div>
</div>

{% endblock %}
```

**Puntos importantes:**

- `name="username"` y `name="password"` son **obligatorios** exactamente así. `LoginView` espera esos nombres.
- `{% csrf_token %}` es obligatorio en todo formulario POST. Sin eso, Django rechaza el envío.
- `name="next" value="{{ next }}"` guarda adónde quería ir el usuario antes de ser mandado al login.

---

# Paso 4 — Proteger la vista del formulario del CV

---

**Este es el cambio principal.** La vista que crearon en la clase 8 (la que usa el `ModelForm` del CV) necesita el decorador `@login_required`.

Abrir `views.py` y agregar el decorador **encima** de la vista:

```python
# views.py
from django.contrib.auth.decorators import login_required   # ← importar el decorador
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NombreDelModelo
from .forms import NombreDelModeloForm

@login_required           # ← esta línea protege toda la vista
def editar_cv(request):   # ← si el usuario no tiene sesión, nunca llega aquí
    objeto = NombreDelModelo.objects.first()

    if request.method == 'POST':
        form = NombreDelModeloForm(request.POST, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Guardado correctamente.')
            return redirect('nombre_url_cv')
        else:
            messages.error(request, 'Hay errores en el formulario.')
    else:
        form = NombreDelModeloForm(instance=objeto)

    return render(request, 'nombre_app/formulario.html', {'form': form})
```

**¿Qué cambia respecto a la clase 8?** Solo se agrega `@login_required` y la importación. El resto de la vista no cambia.

**¿Qué pasa si alguien sin sesión intenta entrar a `/editar/`?**
Django lo redirige automáticamente a `/login/?next=/editar/`. Después del login, lo lleva de vuelta a `/editar/`.

---

# Paso 5 — Agregar logout en la interfaz

---

**¿Por qué hace falta?** El usuario necesita un botón para cerrar sesión. Si no existe en el template, no hay forma de salir sin borrar las cookies manualmente.

En el `base.html`, dentro del navbar, agregar:

```html
<!-- Dentro del navbar de base.html -->
{% if user.is_authenticated %}
<!-- Si tiene sesión: mostrar su nombre y el botón de salir -->
<span class="navbar-text me-3">Hola, {{ user.username }}</span>
<a href="{% url 'logout' %}" class="btn btn-outline-secondary btn-sm"
  >Cerrar sesión</a
>
{% else %}
<!-- Si no tiene sesión: mostrar link al login -->
<a href="{% url 'login' %}" class="btn btn-outline-primary btn-sm"
  >Iniciar sesión</a
>
{% endif %}
```

**`user` ya está disponible** en todos los templates sin pasarlo en el contexto — Django lo incluye automáticamente gracias al context processor `auth`.

---

# Paso 6 — Crear el superusuario (si no existe)

---

**¿Por qué hace falta?** Para iniciar sesión en la app hace falta que exista al menos un usuario. Si todavía no crearon uno, este es el momento.

En la terminal, con el entorno virtual activo:

```
python manage.py createsuperuser
```

Django va a pedir tres datos:

- `Username` — el nombre de usuario para iniciar sesión
- `Email address` — puede dejarse vacío apretando Enter
- `Password` — la contraseña (no se muestra mientras se escribe, es normal)

---

# Paso 7 — Probar el flujo completo

---

1. Correr el servidor: `python manage.py runserver`
2. Abrir el navegador y navegar directamente a la URL del formulario (sin iniciar sesión)
3. Verificar que Django redirige automáticamente al login
4. Iniciar sesión con el usuario creado
5. Verificar que después del login llega al formulario
6. Guardar un cambio y ver el mensaje flash
7. Cerrar sesión desde el navbar
8. Verificar que vuelve al login

---

---

# Checklist de entrega

---

- [ ] Las rutas de login y logout están en el `urls.py` del proyecto
- [ ] Las 3 variables (`LOGIN_REDIRECT_URL`, `LOGIN_URL`, `LOGOUT_REDIRECT_URL`) están en `settings.py`
- [ ] Existe el template `login.html` con los campos `username` y `password`
- [ ] El template de login tiene `{% csrf_token %}`
- [ ] El template de login tiene el campo `next` oculto
- [ ] La vista del formulario del CV tiene `@login_required`
- [ ] El navbar tiene `{% if user.is_authenticated %}` con el botón de cerrar sesión
- [ ] Al ingresar a la URL del formulario sin sesión, Django redirige al login
- [ ] Después del login, el sistema lleva al usuario al formulario (no al inicio)
- [ ] El botón de cerrar sesión funciona y redirige al login

---

## Preguntas para pensar después de terminar

- Si hubiera dos usuarios — el dueño del CV y un visitante — ¿cómo diferenciarías quién puede editar y quién no?
- ¿Qué diferencia hay entre que el formulario sea accesible pero vacío y que sea inaccesible con 403?
- ¿Por qué el campo `next` en el formulario de login es importante para la experiencia del usuario?
- Si sacan el `@login_required`, ¿la vista sigue funcionando? ¿Qué cambia?

---
