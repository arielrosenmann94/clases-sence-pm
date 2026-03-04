# Django — Módulo 6 · Clase 8

## Práctica: Formulario para el CV — sin usar el admin

---

> _"El admin es para el developer. Un formulario propio es para el usuario. Esa diferencia define si hiciste una herramienta o una aplicación."_

---

## ¿Qué vamos a hacer?

Hasta ahora cargaron los datos del CV desde el panel de administración de Django (`/admin`). Eso está bien para desarrollar, pero no es lo que un usuario real usaría.

Hoy van a crear una **página dentro de su propia app** con un formulario que hace exactamente lo mismo que el admin: guardar o editar datos del modelo. La diferencia es que este formulario lo diseñan ustedes, vive en su sitio, y pueden darle el estilo que quieran.

---

## Antes de empezar — leer esto

Este ejercicio es genérico a propósito. No sabemos exactamente cómo llamaron a su modelo ni qué campos tiene. Por eso, en todos los ejemplos de código aparece `NombreDelModelo` y `campo1`, `campo2` como placeholders.

**Lo primero que tienen que hacer antes de escribir código** es tomar nota de:

1. ¿Cómo se llama su modelo? (ejemplo: `Perfil`, `Experiencia`, `Proyecto`)
2. ¿Qué campos tiene ese modelo?
3. ¿Tiene un solo objeto (como el perfil del CV) o puede tener muchos (como proyectos)?

Con eso claro, reemplazar los placeholders en el código y todo va a encajar.

---

---

## `forms.Form` vs `ModelForm` — la diferencia clave

---

En la clase anterior usaron `forms.Form`. Hoy usan `ModelForm`. No son herramientas distintas — son el mismo mecanismo con un nivel de integración diferente.

**`forms.Form`** es el formulario base. Cada campo se define a mano:

```python
class ContactoForm(forms.Form):
    nombre  = forms.CharField(max_length=100)    # ← escrito a mano
    email   = forms.EmailField()                 # ← escrito a mano
    mensaje = forms.CharField(widget=forms.Textarea)  # ← escrito a mano
```

Cuando el formulario se valida, los datos quedan en `cleaned_data`. El desarrollador decide qué hacer con ellos: guardarlos, enviarlos por email, mostrarlos. Django no sabe nada de la base de datos.

---

**`ModelForm`** hace lo mismo, pero lee el modelo y genera los campos automáticamente:

```python
class PerfilForm(forms.ModelForm):
    class Meta:
        model  = Perfil                           # ← le dice qué modelo leer
        fields = ['nombre', 'email', 'mensaje']   # ← elige qué campos mostrar
```

Django lee la definición del modelo `Perfil`, ve que `nombre` es `CharField(max_length=100)`, y genera automáticamente el campo del formulario con esa misma restricción. No hay que repetirlo.

---

### La diferencia en una tabla

| Pregunta                              | `forms.Form`                                | `ModelForm`                         |
| ------------------------------------- | ------------------------------------------- | ----------------------------------- |
| ¿Cómo se definen los campos?          | A mano, uno por uno                         | Automáticamente desde el modelo     |
| ¿Sabe de la base de datos?            | No                                          | Sí                                  |
| ¿Cómo se guarda?                      | El developer escribe el código del `save()` | `form.save()` — una línea           |
| ¿Se puede editar un objeto existente? | No directamente                             | Sí — con `instance=objeto`          |
| ¿Cuándo usarlo?                       | Contacto, búsqueda, filtros                 | Crear o editar registros del modelo |

---

### La analogía

Imaginen que tienen que llenar una ficha de trabajo. Con `forms.Form` diseñan la ficha desde cero: deciden qué campos tiene, qué tipo, qué largo máximo. Con `ModelForm` la ficha ya existe — la diseñaron cuando crearon el modelo — y solo eligen qué campos de esa ficha mostrar hoy.

Si el modelo cambia (agregan un campo), el `ModelForm` lo incorpora automáticamente. El `forms.Form` habría que actualizarlo a mano.

---

> `forms.Form` cuando el formulario no tiene relación directa con un modelo. `ModelForm` cuando el objetivo es crear o editar un registro en la base de datos. Esa regla cubre el 95% de los casos.

---

# Paso 1 — Crear el formulario en `forms.py`

---

**¿Por qué existe `forms.py`?** Es el archivo donde Django espera encontrar los formularios. Separarlo de las vistas mantiene el código organizado — si en el futuro quieren usar el mismo formulario en dos vistas distintas, solo lo importan, no lo copian.

Si ya tienen un archivo `forms.py` en su app, agregar el código ahí. Si no existe, crearlo en la misma carpeta donde están `views.py` y `models.py`.

```python
# forms.py

from django import forms
from .models import NombreDelModelo   # ← cambiar por el nombre real de su modelo

class NombreDelModeloForm(forms.ModelForm):

    class Meta:
        model  = NombreDelModelo          # ← el modelo que usa este formulario
        fields = ['campo1', 'campo2']     # ← los campos que quieren mostrar

        widgets = {
            'campo1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escriba aquí...'
            }),
            'campo2': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción...'
            }),
        }
```

**¿Qué hace `class Meta`?** Es una clase dentro de la clase que le dice al ModelForm cómo configurarse: qué modelo usar, qué campos mostrar, y qué HTML generar para cada uno.

**¿Qué es `widgets`?** Es el diccionario que conecta el nombre de un campo con el HTML que va a generar. Si no se define un widget, Django elige uno por defecto. Definirlo sirve para agregar clases de Bootstrap como `form-control`.

**¿Qué campos poner en `fields`?** Solo los que el usuario debería poder editar. Los campos que se generan solos (como `creado`, `modificado`, `id`) no van — Django los maneja internamente.

---

---

# Paso 2 — Crear la vista en `views.py`

---

**¿Qué hace la vista?** Tiene dos situaciones posibles:

- El usuario entró a la página por primera vez (GET) → mostrar el formulario vacío o pre-poblado
- El usuario envió el formulario (POST) → validar y guardar

Estas dos situaciones se manejan en la misma vista, separadas por el `if request.method == 'POST'`.

---

### Si su modelo tiene UN SOLO objeto (ej: el perfil del CV)

En este caso no se crea un objeto nuevo — se edita el que ya existe.

```python
# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import NombreDelModelo
from .forms import NombreDelModeloForm

def editar_perfil(request):
    # Buscar el objeto que ya existe en la base de datos
    # .first() devuelve el primero que encuentre, o None si no hay ninguno
    objeto = NombreDelModelo.objects.first()

    if request.method == 'POST':
        # El formulario recibe los datos enviados (request.POST)
        # y también el objeto existente (instance=objeto)
        # Así Django sabe que tiene que ACTUALIZAR, no crear uno nuevo
        form = NombreDelModeloForm(request.POST, instance=objeto)

        if form.is_valid():
            form.save()
            messages.success(request, 'Guardado correctamente.')
            return redirect('nombre_url_cv')    # ← cambiar por la URL de su CV

        else:
            messages.error(request, 'Hubo errores. Revisa el formulario.')

    else:
        # GET: mostrar el formulario con los datos actuales del objeto
        form = NombreDelModeloForm(instance=objeto)

    return render(request, 'nombre_app/formulario.html', {'form': form})
```

**¿Por qué `instance=objeto`?** Sin `instance`, Django crea un objeto nuevo cada vez. Con `instance`, Django sabe que tiene que modificar ese objeto específico — hace un `UPDATE` en la base de datos en lugar de un `INSERT`.

---

### Si su modelo puede tener MUCHOS objetos (ej: proyectos, experiencias)

En este caso sí se crea un objeto nuevo.

```python
def agregar_proyecto(request):
    if request.method == 'POST':
        # Sin instance= porque es un objeto nuevo
        form = NombreDelModeloForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Agregado correctamente.')
            return redirect('nombre_url_cv')    # ← cambiar por la URL de su CV

        else:
            messages.error(request, 'Hubo errores. Revisa el formulario.')

    else:
        form = NombreDelModeloForm()

    return render(request, 'nombre_app/formulario.html', {'form': form})
```

---

---

# Paso 3 — Registrar la URL

---

**¿Por qué hay que registrar la URL?** Django no descubre las vistas automáticamente. Cada vista tiene que estar conectada a una URL en `urls.py`. Sin eso, la vista existe pero es inaccesible.

En el archivo `urls.py` de la app (no el del proyecto principal):

```python
# urls.py de la app

from django.urls import path
from . import views

urlpatterns = [
    # ... las URLs que ya tenían ...

    path('editar/', views.editar_perfil, name='editar_perfil'),
    # o si es lista:
    # path('agregar/', views.agregar_proyecto, name='agregar_proyecto'),
]
```

El `name=` es importante — es el identificador que se usa en `{% url 'editar_perfil' %}` dentro de los templates y en `redirect('editar_perfil')` dentro de las vistas.

---

---

# Paso 4 — Crear el template

---

**¿Dónde va el archivo?** En `templates/nombre_app/formulario.html`. Si ya tienen templates en el proyecto, seguir la misma estructura de carpetas que vienen usando.

```html
{% extends 'base.html' %} {% block content %}

<div class="container my-5">
  <div class="row justify-content-center">
    <div class="col-md-7">
      <h2 class="mb-4">Editar perfil</h2>

      <!-- Mostrar mensajes flash si los hay -->
      {% if messages %} {% for message in messages %}
      <div
        class="alert alert-{{ message.tags }} alert-dismissible fade show"
        role="alert"
      >
        {{ message }}
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
        ></button>
      </div>
      {% endfor %} {% endif %}

      <!-- El formulario -->
      <form method="POST" novalidate>
        {% csrf_token %}
        <!-- ↑ OBLIGATORIO en todo formulario POST. Sin esto Django rechaza el envío con error 403 -->

        {% for field in form %}
        <div class="mb-3">
          <label for="{{ field.id_for_label }}" class="form-label">
            {{ field.label }}
          </label>

          {{ field }}
          <!-- ↑ Esto renderiza el input del campo con el widget que definieron en forms.py -->

          <!-- Mostrar errores de validación debajo del campo -->
          {% for error in field.errors %}
          <div class="text-danger small mt-1">{{ error }}</div>
          {% endfor %}

          <!-- Mostrar texto de ayuda si el campo tiene help_text -->
          {% if field.help_text %}
          <div class="form-text">{{ field.help_text }}</div>
          {% endif %}
        </div>
        {% endfor %}

        <div class="d-flex gap-2 mt-4">
          <button type="submit" class="btn btn-primary">Guardar</button>
          <a href="{% url 'nombre_url_cv' %}" class="btn btn-outline-secondary"
            >Cancelar</a
          >
          <!-- ↑ cambiar 'nombre_url_cv' por la URL real del CV -->
        </div>
      </form>
    </div>
  </div>
</div>

{% endblock %}
```

---

---

# Paso 5 — Agregar una validación personalizada

---

**¿Por qué validar en el formulario si Django ya valida tipos?** Django valida que el dato sea del tipo correcto (número, email, fecha). Pero no sabe las reglas de negocio: que el título no puede ser genérico, que la fecha de inicio no puede ser futura, que el nombre debe tener más de 2 caracteres. Esas reglas las escribe el developer.

Volver a `forms.py` y agregar un método de validación para alguno de los campos. El método se llama `clean_` + el nombre exacto del campo:

```python
class NombreDelModeloForm(forms.ModelForm):
    class Meta:
        model  = NombreDelModelo
        fields = ['campo1', 'campo2']

    def clean_campo1(self):
        # Obtener el valor que ingresó el usuario
        valor = self.cleaned_data.get('campo1', '')

        # Limpiar espacios al inicio y al final
        valor = valor.strip()

        # Aplicar la regla que necesiten. Ejemplos:
        if len(valor) < 3:
            raise forms.ValidationError(
                'Este campo debe tener al menos 3 caracteres.'
            )

        # IMPORTANTE: siempre devolver el valor al final
        return valor
```

**¿Qué pasa si no se devuelve el valor?** Django reemplaza el campo en `cleaned_data` con lo que devuelve este método. Si no se devuelve nada, el campo queda como `None` aunque el usuario haya escrito algo. Siempre `return valor` al final.

---

---

# Checklist antes de mostrar el resultado

---

- [ ] El `ModelForm` tiene los campos correctos del modelo
- [ ] Los widgets tienen `class: 'form-control'`
- [ ] La vista maneja GET y POST correctamente
- [ ] El template tiene `{% csrf_token %}` dentro del `<form>`
- [ ] Los errores de validación aparecen debajo de cada campo
- [ ] Se muestra un mensaje flash al guardar correctamente
- [ ] Después de guardar redirige al CV (no queda en el formulario vacío)
- [ ] Hay al menos una validación personalizada con `clean_campo()`

---

## Preguntas para pensar después de terminar

- ¿Qué diferencia hay entre el `instance=` en el GET y en el POST? ¿Por qué se usa en los dos?
- ¿Qué pasaría si sacaran el `{% csrf_token %}` del template?
- ¿En qué parte del template aparece el error si el `clean()` general (cruzado) lanza un `ValidationError`?
- Si quisieran agregar un segundo modelo con su propio formulario, ¿qué archivos habría que modificar?

---
