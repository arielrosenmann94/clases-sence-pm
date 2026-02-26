# 🐛 Django — Módulo 6 · Práctica de Debugging (Clase 4)

### Agrega una App de Contacto a tu Proyecto (con errores ocultos)

> **Instrucciones:** Sigue cada paso copiando y pegando el código exactamente como está. Cuando ejecutes el servidor o entres a una URL, Django te mostrará errores. Tu trabajo es **leer el error, encontrar el problema y corregirlo** antes de pasar al siguiente paso. Hay **al menos 10 errores** escondidos en el código.

> 📝 Para cada error, anota: qué decía Django, en qué archivo estaba el problema y cómo lo solucionaste.

---

## Paso 1 — Crear la app

Ejecuta en la terminal desde la raíz de tu proyecto `catalogoapp`:

```bash
python manage.py startapp contacto
```

---

## Paso 2 — Registrar la app

Abre `config/settings.py` y agrega la app a `INSTALLED_APPS`. Copia y pega esta lista completa:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'productos',
    'core',
    'contactos',                   # ← Copia esto tal cual
]
```

Ejecuta el servidor:

```bash
python manage.py runserver
```

> 🐛 **¿El servidor arrancó?** Si no, lee el error y corrígelo.

---

## Paso 3 — Crear el modelo

Abre `contacto/models.py` y **reemplaza todo** el contenido por:

```python
# contacto/models.py
from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_lenght=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"
```

Ejecuta las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

> 🐛 **¿Funcionó?** Si no, lee el error y corrígelo.

---

## Paso 4 — Registrar en el Admin

Abre `contacto/admin.py` y **reemplaza todo** por:

```python
# contacto/admin.py
from django.contrib import admin
from .models import MensajeContacto

admin.site.register(MensajeDeContacto)
```

Ejecuta el servidor y entra a `http://127.0.0.1:8000/admin/`.

> 🐛 **¿Aparece el modelo en el admin?** Si no, lee el error y corrígelo.

---

## Paso 5 — Crear el formulario

Crea el archivo `contacto/forms.py` y pega:

```python
# contacto/forms.py
from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
```

> ✅ Este archivo no tiene errores.

---

## Paso 6 — Crear la vista

Abre `contacto/views.py` y **reemplaza todo** por:

```python
# contacto/views.py
from django.shortcuts import render
from .forms import ContactoForm

def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacto_exito')
    else:
        form = ContactoForm()

    return render(request, 'contacto/formulario.html', {'form': form})

def contacto_exito_view(request):
    return render(request, 'contacto/exito.html')
```

---

## Paso 7 — Crear las URLs de la app

Crea el archivo `contacto/urls.py` y pega:

```python
# contacto/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto_view, name='contacto'),
    path('exito/', views.contacto_exito, name='contacto_exito'),
]
```

> 🐛 **Revisa bien los nombres.**

---

## Paso 8 — Conectar al proyecto principal

Abre `config/urls.py` y **agrega** la ruta de contacto. Tu archivo completo debe quedar así:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('productos/', include('productos.urls')),
    path('contacto/', include('contacto.url')),
]
```

Ejecuta el servidor y entra a `http://127.0.0.1:8000/contacto/`.

> 🐛 **¿Cargó la página?** Si no, lee el error cuidadosamente. Puede haber más de un error acumulado.

---

## Paso 9 — Crear los templates

Primero crea la carpeta:

```bash
mkdir -p contacto/templates/contacto
```

Crea el archivo `contacto/templates/contacto/formulario.html` y pega:

```html
{% extends "base.html" %} {% block titulo %}Contacto{% endblock %} {% block
content %}
<div class="container mt-4">
  <h1>📩 Contáctanos</h1>
  <p class="text-muted">Envíanos un mensaje y te responderemos pronto.</p>

  <form method="POST">
    {% csrf_token %} {% for field in form %}
    <div class="mb-3">
      <label for="{{ field.id_for_label }}" class="form-label">
        {{ field.label }}
      </label>
      {{ field }} {% if field.errors %}
      <div class="text-danger">{{ field.errors }}</div>
      {% endif %}
    </div>
    {% endfor %}

    <button type="submit" class="btn btn-success">Enviar mensaje</button>
  </form>
</div>
{% endblock %}
```

Crea el archivo `contacto/templates/contacto/exito.html` y pega:

```html
{% extends "base.html" %} {% block titulo %}Mensaje Enviado{% endblock %} {%
block content %}
<div class="container mt-4 text-center">
  <h1>✅ ¡Mensaje enviado!</h1>
  <p>Gracias por contactarnos. Te responderemos pronto.</p>
  <a href="{% url 'home' %}" class="btn btn-primary mt-3">Volver al inicio</a>
</div>
{% endblock %}
```

Ejecuta el servidor y entra a `http://127.0.0.1:8000/contacto/`.

> 🐛 **¿Cargó el formulario?** Recuerda: a esta altura puede que tengas errores de pasos anteriores que aún no corregiste.

---

## Paso 10 — Agregar link en la navbar

Abre `templates/base.html` y agrega este link dentro de la navbar, junto a los otros:

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'formulario_contacto' %}">📩 Contacto</a>
</li>
```

Recarga cualquier página.

> 🐛 **¿Funciona el link?** Si no, revisa el nombre.

---

## Paso 11 — Probar el formulario

1. Entra a `http://127.0.0.1:8000/contacto/`.
2. Completa todos los campos y haz clic en **"Enviar mensaje"**.

> 🐛 **¿Funcionó el envío?** Si no, busca errores en `views.py` (puede faltar algo).

---

## Paso 12 — Aplicar estilos Bootstrap a los campos del formulario

Los campos del formulario se ven sin estilo porque Django genera `<input>` sin clases de Bootstrap. Abre `contacto/forms.py` y **reemplaza todo** por:

```python
# contacto/forms.py
from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
```

Recarga la página de contacto. Los campos ahora deberían verse con el estilo Bootstrap.

---

## Paso 13 — Verificar en el admin

1. Entra a `http://127.0.0.1:8000/admin/`.
2. Busca la sección **Contacto → Mensaje contactos**.
3. Verifica que aparece el mensaje que enviaste con nombre, email, asunto y fecha.

---

## Para entregar

Cuando hayas corregido todos los errores, responde:

1. ¿Cuántos errores encontraste en total?
2. ¿Cuál fue el más difícil de resolver y por qué?
3. ¿Qué error de Django te dio la pista más clara para solucionarlo?
4. ¿Cuál fue un error que Django **no** te avisó (error silencioso)?

---

> 🧠 _"Leer errores de Django es una habilidad. Cuantos más leas, más rápido los resolverás."_
