# Django — Módulo 6 · Clase 8

## ModelForms, Widgets y Validaciones

---

> _"Un ModelForm no es magia. Es la conclusión lógica de que si ya definiste el modelo, repetir la misma información en el formulario es trabajo duplicado — y el trabajo duplicado es el origen de los bugs."_

---

## Contexto de la Parte II

En la Parte I vimos `forms.Form`: formularios independientes que validan datos sin conocer nada de la base de datos. Son útiles para búsquedas, filtros, suscripciones, contacto.

Pero cuando el objetivo del formulario es **crear o editar un registro en la base de datos**, hay una herramienta más directa: **`ModelForm`**.

---

---

# Parte I — ModelForm: formularios ligados al modelo

---

## El principio

> Definiste el modelo una vez. El `ModelForm` lo lee y genera el formulario solo. No hay que repetir cada campo — eso es el principio DRY aplicado a formularios.

Un `ModelForm` lee la definición del modelo y genera el formulario automáticamente. Si el modelo tiene un campo `CharField(max_length=100)`, el formulario genera un `forms.CharField(max_length=100)` sin que haya que escribirlo.

```python
# models.py
class Producto(models.Model):
    nombre      = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    precio      = models.DecimalField(max_digits=10, decimal_places=2)
    disponible  = models.BooleanField(default=True)
    creado      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
```

```python
# forms.py
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['nombre', 'descripcion', 'precio', 'disponible']
        # fields = '__all__'        ← todos los campos
        # exclude = ['creado']      ← excluir campos específicos
```

---

## La diferencia clave: `form.save()`

> En `forms.Form` los datos llegan limpios a la vista y el desarrollador decide qué hacer con ellos. En `ModelForm`, `save()` hace ese trabajo en una sola línea.

El `ModelForm` tiene un método `save()` que no existe en `forms.Form`. Guarda el objeto en la base de datos directamente:

```python
# views.py
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()                          # ← guarda en la base de datos
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})
```

Para **editar** un objeto existente, se pasa `instance`. Django detecta que ya existe en la DB y hace un `UPDATE` en lugar de un `INSERT`.

```python
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)  # ← instancia existente
        if form.is_valid():
            form.save()                                        # ← actualiza, no crea
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)                 # ← formulario pre-poblado
    return render(request, 'producto_form.html', {'form': form})
```

---

## Tabla: `forms.Form` vs `ModelForm`

| Característica          | `forms.Form`                     | `ModelForm`                  |
| ----------------------- | -------------------------------- | ---------------------------- |
| Definición de campos    | Manual, uno por uno              | Automática desde el modelo   |
| Guarda en la DB         | No — hay que hacerlo manualmente | Sí — con `form.save()`       |
| Editar objeto existente | No aplica                        | Sí — con `instance=objeto`   |
| Válido para             | Búsquedas, filtros, contacto     | Crear/editar registros       |
| `form.cleaned_data`     | ✅                               | ✅                           |
| Validación automática   | ✅                               | ✅ + validaciones del modelo |

---

---

# Parte II — Widgets: controlar la apariencia de los campos

---

## Qué es un widget

> El widget es el HTML que produce el campo. El campo valida el dato; el widget decide cómo se ve. Se pueden usar por separado sin tocarse.

Un **widget** es el componente HTML que Django usa para renderizar un campo. Por defecto:

- `CharField` → `<input type="text">`
- `BooleanField` → `<input type="checkbox">`
- `TextField` → `<textarea>`

Los widgets se pueden sobreescribir para cambiar el HTML generado y agregar atributos como clases de Bootstrap.

---

## Personalizar widgets en un `ModelForm`

> El dict `widgets` dentro de `class Meta` enlaza el nombre del campo con su widget. Ahí se agregan clases CSS, placeholders y atributos HTML sin tocar el template.

```python
class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['nombre', 'descripcion', 'precio', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción breve...'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio (USD)',
            'disponible': 'Disponible para venta',
        }
```

---

## Widgets más usados

| Widget          | HTML generado             | Cuándo usar          |
| --------------- | ------------------------- | -------------------- |
| `TextInput`     | `<input type="text">`     | Texto corto          |
| `Textarea`      | `<textarea>`              | Texto largo          |
| `EmailInput`    | `<input type="email">`    | Email                |
| `NumberInput`   | `<input type="number">`   | Números              |
| `PasswordInput` | `<input type="password">` | Contraseñas          |
| `CheckboxInput` | `<input type="checkbox">` | Booleanos            |
| `Select`        | `<select>`                | Choices con dropdown |
| `DateInput`     | `<input type="date">`     | Fechas               |
| `HiddenInput`   | `<input type="hidden">`   | Campos ocultos       |

---

---

# Parte III — Validaciones personalizadas

---

## Validación por campo: `clean_<nombre_del_campo>()`

> Nombrar el método `clean_` seguido del nombre del campo le dice a Django que lo ejecute automáticamente al validar. Si lanza `ValidationError`, ese campo queda inaccesible en `cleaned_data`.

Django llama a estos métodos automáticamente durante `is_valid()`. Si el método lanza un `ValidationError`, el campo queda inválido:

```python
class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['nombre', 'precio', 'disponible']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # no se permiten nombres genéricos
        nombres_prohibidos = ['producto', 'item', 'cosa', 'test']
        if nombre.lower() in nombres_prohibidos:
            raise forms.ValidationError(
                f'"{nombre}" no es un nombre descriptivo. Usá un nombre específico.'
            )
        # siempre devolver el valor al final
        return nombre.strip()    # .strip() elimina espacios al inicio/fin

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return precio
```

> **Regla importante**: el método `clean_<campo>` siempre debe devolver el valor del campo al final, aunque no lo modifique. Django lo reemplaza en `cleaned_data` con lo que devuelve este método.

---

## Validación cruzada entre campos: `clean()`

> Si la regla depende de dos campos a la vez — como que la fecha de fin sea posterior a la de inicio — no hay un `clean_campo` correcto. El método `clean()` general es el lugar.

Cuando la validación depende de más de un campo a la vez, se usa el método general `clean()`:

```python
class RangoFechasForm(forms.Form):
    fecha_inicio = forms.DateField(label='Desde')
    fecha_fin    = forms.DateField(label='Hasta')

    def clean(self):
        datos = super().clean()    # ejecuta las validaciones individuales primero
        inicio = datos.get('fecha_inicio')
        fin    = datos.get('fecha_fin')

        if inicio and fin:
            if fin < inicio:
                raise forms.ValidationError(
                    'La fecha de fin no puede ser anterior a la de inicio.'
                )
        return datos
```

El error generado en `clean()` aparece en `form.non_field_errors` (no está asociado a un campo específico).

---

---

# Parte IV — Mensajes flash: retroalimentación al usuario

---

## El patrón PRG y los mensajes

> Si el usuario recarga la página después de un POST sin redirect, el browser reenvía el formulario. El redirect corta ese ciclo. Pero ¿cómo avisar que todo salió bien si no hay contexto? Con mensajes flash.

**PRG** = Post / Redirect / Get. Es el patrón estándar para procesar formularios:

```
Usuario envía POST → Vista procesa → Redirect → Usuario hace GET de la nueva URL
```

Sin este patrón, si el usuario recarga la página después de enviar el formulario, el browser pregunta "¿quiere reenviar el formulario?" y el registro se duplica.

Con `redirect()` ese problema desaparece — pero también desaparece el contexto. ¿Cómo mostrar "Registro guardado correctamente" después del redirect?

**Respuesta**: el **Messages Framework** de Django.

---

## Cómo usar los mensajes

```python
# views.py
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ProductoForm

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Hay errores en el formulario. Revisalo.')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})
```

---

## Mostrar los mensajes en el template

Los mensajes se ponen en `base.html` para que estén disponibles en todas las páginas:

```html
<!-- en base.html, justo después del navbar -->
{% if messages %}
<div class="container mt-3">
  {% for message in messages %}
  <div
    class="alert alert-{{ message.tags }} alert-dismissible fade show"
    role="alert"
  >
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>
  {% endfor %}
</div>
{% endif %}
```

---

## Niveles de mensaje disponibles

| Método                             | Tag Bootstrap   | Cuándo usar              |
| ---------------------------------- | --------------- | ------------------------ |
| `messages.success(request, '...')` | `alert-success` | Operación exitosa        |
| `messages.error(request, '...')`   | `alert-danger`  | Error al procesar        |
| `messages.warning(request, '...')` | `alert-warning` | Alerta, acción necesaria |
| `messages.info(request, '...')`    | `alert-info`    | Información neutral      |

---

---

# Parte V — Ejemplo completo: CRUD con ModelForm

---

**Contexto**: App de gestión de tareas pendientes. El usuario puede crear y editar tareas.

### `models.py`

```python
from django.db import models

class Tarea(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    titulo     = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    prioridad  = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    completada = models.BooleanField(default=False)
    creada     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-creada']
```

### `forms.py`

```python
from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model  = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'completada']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la tarea'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción opcional...'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'completada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if len(titulo) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres.')
        return titulo
```

### `views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tarea
from .forms import TareaForm

def lista_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas/lista.html', {'tareas': tareas})

def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea creada correctamente.')
            return redirect('lista_tareas')
        messages.error(request, 'Corrige los errores antes de continuar.')
    else:
        form = TareaForm()
    return render(request, 'tareas/form.html', {'form': form, 'titulo': 'Nueva tarea'})

def editar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarea "{tarea.titulo}" actualizada.')
            return redirect('lista_tareas')
        messages.error(request, 'Corrige los errores antes de continuar.')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'tareas/form.html', {'form': form, 'titulo': 'Editar tarea'})
```

### `urls.py` de la app

```python
from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('',              views.lista_tareas, name='lista_tareas'),
    path('nueva/',        views.crear_tarea,  name='crear_tarea'),
    path('<int:pk>/editar/', views.editar_tarea, name='editar_tarea'),
]
```

### `templates/tareas/form.html`

```html
{% extends 'base.html' %} {% block content %}
<div class="container my-5">
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card shadow-sm">
        <div class="card-header">
          <h4 class="mb-0">{{ titulo }}</h4>
        </div>
        <div class="card-body">
          <form method="POST" novalidate>
            {% csrf_token %} {% for field in form %}
            <div class="mb-3">
              <label for="{{ field.id_for_label }}" class="form-label"
                >{{ field.label }}</label
              >
              {{ field }} {% for error in field.errors %}
              <div class="text-danger small mt-1">{{ error }}</div>
              {% endfor %}
            </div>
            {% endfor %}
            <div class="d-flex gap-2 mt-4">
              <button type="submit" class="btn btn-primary">Guardar</button>
              <a
                href="{% url 'tareas:lista_tareas' %}"
                class="btn btn-outline-secondary"
                >Cancelar</a
              >
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

---

---

# Resumen de la Parte II

---

| Concepto                         | Descripción                                                       |
| -------------------------------- | ----------------------------------------------------------------- |
| `ModelForm`                      | Formulario generado automáticamente desde un modelo               |
| `class Meta`                     | Configura `model`, `fields`, `widgets`, `labels`                  |
| `form.save()`                    | Guarda el objeto en la base de datos                              |
| `form = ModelForm(instance=obj)` | Pre-popula el formulario con datos existentes (edición)           |
| `clean_<campo>()`                | Validación personalizada para un campo específico                 |
| `clean()`                        | Validación que involucra múltiples campos                         |
| `messages.success/error()`       | Mensajes flash que sobreviven un `redirect()`                     |
| Patrón PRG                       | Post → Redirect → Get — evita el reenvío duplicado de formularios |

---

> _"El ModelForm es el punto donde el modelo y el usuario se encuentran. Definís los datos una sola vez en el modelo, y el formulario los traduce a una interfaz web. Eso es DRY en acción."_

---
