# 🐍 Django — Módulo 6 · Clase 7

## Formularios en Django: Parte I

---

> _"Un formulario bien hecho no es solo un input y un botón. Es el contrato entre el usuario y la aplicación: yo te doy datos, tú me das algo útil a cambio."_

---

## Contexto: ¿Por qué Django tiene su propio sistema de formularios?

Antes de Django Forms existía el approach manual: un `<form>` en HTML, un `request.POST['campo']` en la vista, validaciones escritas a mano, y el desarrollador rezando para que el usuario no enviara texto donde esperaba un número.

Django Forms resuelve ese problema con una capa que centraliza tres responsabilidades:

1. **Definición** — se declara en Python qué campos tiene el formulario y qué tipo de dato acepta cada uno. Por ejemplo: "el campo `email` solo acepta texto con formato de correo electrónico" o "el campo `edad` solo acepta números enteros". Esta definición vive en un solo lugar (`forms.py`) y es la fuente de verdad para todo lo demás.

2. **Validación** — cuando el usuario envía el formulario, Django revisa automáticamente que los datos sean correctos antes de que el código los use. Si el campo `email` recibe un texto sin arroba, Django lo detecta y genera el mensaje de error correspondiente sin que haya que escribir ese control a mano.

3. **Renderización** — el formulario sabe cómo mostrarse en el template. Cada campo conoce su label, su tipo de input HTML y los errores que le corresponden. Se puede mostrar todo con una sola línea o campo por campo con control total del diseño.

El resultado es menos código, más seguridad y menos bugs.

> 💡 **Tip**: cuando escuches "Django Forms" en una entrevista o proyecto, pensá en estas tres palabras: **definir, validar, renderizar**. Todo lo demás es detalle de implementación.

---

---

# Parte I — Formularios HTML vs Django Forms

---

## El problema con los formularios HTML puros

```html
<!-- HTML puro: el form lo escribe el desarrollador a mano -->
<form method="POST" action="/buscar/">
  <input type="text" name="query" placeholder="Buscar..." />
  <button type="submit">Buscar</button>
</form>
```

```python
# views.py — validación manual, propensa a errores
def buscar(request):
    query = request.POST.get('query', '')
    if not query:
        # error — hay que manejarlo manualmente
        return render(request, 'buscar.html', {'error': 'Campo vacío'})
    if len(query) > 200:
        return render(request, 'buscar.html', {'error': 'Demasiado largo'})
    # ... más validaciones manuales
```

Cada campo necesita su propia lógica. Si hay 10 campos, hay 10 bloques de validación. Si hay un cambio, hay que rastrearlo en múltiples lugares.

> ⚠️ **Dato importante**: este approach manual es exactamente cómo se construían sitios web en los años 2000. Funcionaba — pero escalar o mantener ese código era una pesadilla. Django Forms nació para resolver ese dolor.

---

## La solución: Django Forms

```python
# forms.py — definición centralizada
from django import forms

class BusquedaForm(forms.Form):
    query = forms.CharField(
        label='Buscar',
        max_length=200,
        min_length=2
    )
```

```python
# views.py — validación automática
def buscar(request):
    form = BusquedaForm(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['query']
        # los datos ya están validados y limpios
        resultados = Producto.objects.filter(nombre__icontains=query)
        return render(request, 'resultados.html', {'resultados': resultados})
    return render(request, 'buscar.html', {'form': form})
```

**`form.is_valid()`** hace todo el trabajo de validación. Si falla, los errores quedan disponibles en `form.errors` para mostrarlos en el template.

---

## Tabla comparativa

| Aspecto              | HTML puro + vista manual     | Django Forms                 |
| -------------------- | ---------------------------- | ---------------------------- |
| Definición de campos | En el HTML a mano            | En `forms.py` centralizado   |
| Validación de tipos  | Manual en la vista           | Automática por tipo de campo |
| Mensajes de error    | Escritos a mano              | Generados automáticamente    |
| Protección CSRF      | Hay que implementarla        | `{% csrf_token %}` integrado |
| Reutilización        | Copiar y pegar               | Importar la clase            |
| Mantenimiento        | Cambios en múltiples lugares | Cambio en un solo lugar      |

> _"La diferencia entre un formulario HTML y un Django Form es la misma que entre escribir una lista de compras a mano y tener una app que la organiza sola."_

---

---

# Parte II — Anatomía de un formulario Django

---

## El archivo `forms.py`

Por convención, los formularios van en un archivo `forms.py` dentro de la app:

```
mi_app/
├── models.py
├── views.py
├── forms.py       ← aquí
└── urls.py
```

> 💡 **¿Por qué un archivo separado?** Se podría poner los formularios directamente en `views.py`, pero separarlos en `forms.py` mantiene el código organizado. A medida que la app crece, esto marca la diferencia entre un proyecto mantenible y un archivo de 800 líneas imposible de leer.

---

## Tipos de campos disponibles

### Campos de texto

| Campo        | Tipo Python | Uso típico                                           |
| ------------ | ----------- | ---------------------------------------------------- |
| `CharField`  | `str`       | Texto corto: nombre, título, búsqueda                |
| `EmailField` | `str`       | Correo electrónico — valida el formato `@`           |
| `URLField`   | `str`       | Links — valida que sea una URL válida                |
| `SlugField`  | `str`       | Identificadores para URLs amigables (`mi-articulo`)  |
| `UUIDField`  | `UUID`      | Identificadores únicos universales                   |
| `RegexField` | `str`       | Texto que debe cumplir un patrón regex personalizado |

### Campos numéricos

| Campo          | Tipo Python | Uso típico                              |
| -------------- | ----------- | --------------------------------------- |
| `IntegerField` | `int`       | Edad, cantidad, año                     |
| `FloatField`   | `float`     | Medidas, coordenadas, valores continuos |
| `DecimalField` | `Decimal`   | Precios, porcentajes — precisión exacta |

### Campos de fecha y hora

| Campo           | Tipo Python | Uso típico                                 |
| --------------- | ----------- | ------------------------------------------ |
| `DateField`     | `date`      | Solo fecha: cumpleaños, fecha de entrega   |
| `TimeField`     | `time`      | Solo hora: horario de turno                |
| `DateTimeField` | `datetime`  | Fecha y hora combinadas: reservas, eventos |
| `DurationField` | `timedelta` | Duración: tiempo estimado de una tarea     |

### Campos de selección

| Campo                 | Tipo Python  | Uso típico                                                  |
| --------------------- | ------------ | ----------------------------------------------------------- |
| `ChoiceField`         | `str`        | Dropdown con opciones fijas                                 |
| `MultipleChoiceField` | `list`       | Selección múltiple — varios checkboxes                      |
| `TypedChoiceField`    | configurable | Como `ChoiceField` pero convierte el valor al tipo correcto |

### Campos booleanos

| Campo              | Tipo Python     | Uso típico                              |
| ------------------ | --------------- | --------------------------------------- |
| `BooleanField`     | `bool`          | Checkbox obligatorio — aceptar términos |
| `NullBooleanField` | `bool` o `None` | Tres estados: sí / no / sin respuesta   |

### Campos de archivo

| Campo        | Tipo Python | Uso típico                                      |
| ------------ | ----------- | ----------------------------------------------- |
| `FileField`  | archivo     | Subida de archivos genéricos                    |
| `ImageField` | imagen      | Subida de imágenes — valida que sea imagen real |

### Campos especiales

| Campo                   | Tipo Python  | Uso típico                                 |
| ----------------------- | ------------ | ------------------------------------------ |
| `GenericIPAddressField` | `str`        | Dirección IP v4 o v6                       |
| `SplitDateTimeField`    | `datetime`   | Fecha y hora en dos inputs separados       |
| `ComboField`            | configurable | Combina múltiples validaciones en un campo |

> 💡 **Tip**: en el día a día el 80% de los formularios usa solo: `CharField`, `EmailField`, `IntegerField`, `DecimalField`, `BooleanField`, `ChoiceField` y `DateField`. Los demás existen para casos específicos — no hace falta memorizarlos, pero sí saber que existen para buscarlos cuando los necesites.

---

## Parámetros comunes de cada campo

```python
class EjemploForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre completo',      # texto visible del label
        max_length=100,               # largo máximo
        min_length=2,                 # largo mínimo
        required=True,                # obligatorio (True por defecto)
        help_text='Tal como figura en el documento.'  # texto de ayuda
    )

    edad = forms.IntegerField(
        label='Edad',
        min_value=18,                 # valor mínimo
        max_value=99,                 # valor máximo
        required=False                # campo opcional
    )

    opcion = forms.ChoiceField(
        label='Nivel',
        choices=[                     # lista de tuplas (valor, etiqueta)
            ('basico', 'Básico'),
            ('intermedio', 'Intermedio'),
            ('avanzado', 'Avanzado'),
        ]
    )
```

---

## El flujo completo: GET y POST

Un formulario tiene dos momentos de vida:

```
GET  → el usuario llega a la página → se muestra el formulario vacío
POST → el usuario envía el formulario → se valida y procesa
```

```python
# views.py
def mi_formulario(request):
    if request.method == 'POST':
        form = MiForm(request.POST)      # formulario con datos del usuario
        if form.is_valid():
            # datos validados y limpios
            datos = form.cleaned_data
            # procesar...
            return redirect('exito')
    else:
        form = MiForm()                  # formulario vacío para GET

    return render(request, 'formulario.html', {'form': form})
```

> La clave del patrón: si `is_valid()` devuelve `False`, la vista renderiza el template de nuevo — esta vez con el formulario que ya contiene los errores integrados.

> 💡 **Tip**: fíjate que si el método es `POST`, el formulario se crea con `MiForm(request.POST)`. Si es `GET`, se crea vacío con `MiForm()`. Ese patrón es el mismo en el 95% de las vistas con formulario en Django — aprendelo de memoria.

> _"El flujo GET/POST de un formulario es como una conversación: primero el usuario escucha (GET), después habla (POST). La vista tiene que estar lista para ambas situaciones."_

---

---

# Parte III — CSRF: por qué es obligatorio

---

## Qué es CSRF

Imaginate que estás logueado en tu banco. En otra pestaña, abrís un sitio malicioso. Ese sitio, sin que te des cuenta, envía un formulario a la URL de tu banco usando tu sesión activa — como si fueras tú quien lo hizo.

Eso es **CSRF** (_Cross-Site Request Forgery_): un ataque donde una página externa ejecuta acciones en otra app usando la sesión del usuario sin su consentimiento.

## Cómo Django lo resuelve

Django genera un **token secreto único por sesión** y lo incluye en cada formulario como campo oculto. Cuando llega el POST, Django verifica que ese token esté presente y coincida. Si no coincide — o si no está — rechaza la solicitud con `403 Forbidden`.

Una página externa no puede conocer ese token, así que no puede falsificar el formulario.

```html
<form method="POST">
  {% csrf_token %} ← Django inserta el campo oculto con el token {{ form.as_p }}
  <button type="submit">Enviar</button>
</form>
```

```html
<form method="POST">
  {% csrf_token %} {{ form.as_p }}
  <button type="submit">Enviar</button>
</form>
```

Lo que genera `{% csrf_token %}` en el HTML final:

```html
<input
  type="hidden"
  name="csrfmiddlewaretoken"
  value="Abc123XyzRandomToken..."
/>
```

> **Regla**: todo `<form method="POST">` en Django debe tener `{% csrf_token %}` dentro. Sin eso, Django rechaza el envío.

> 💡 **Tip**: si el servidor devuelve error `403 Forbidden` al enviar un formulario, lo primero que hay que revisar es si falta el `{% csrf_token %}`. Es el error más común al empezar con formularios en Django.

> _"La seguridad no es una capa que se agrega al final. CSRF es el ejemplo perfecto de cómo Django la integra desde el principio, sin que tengas que pensar en eso."_

---

---

# Parte IV — Renderización en el template

---

## Métodos de renderización rápida

Django ofrece tres métodos para renderizar todo el formulario de una vez:

```html
{{ form.as_p }} → cada campo envuelto en
<p>
  {{ form.as_ul }} → cada campo en un
  <li>
    {{ form.as_table }} → campos en una tabla
    <tr></tr>
  </li>
</p>
```

Son prácticos para prototipos rápidos pero limitan el control sobre el HTML generado.

> 💡 **Tip**: `{{ form.as_p }}` es perfecto para ver si el formulario funciona antes de preocuparse por el diseño. Primero verifica que la lógica esté bien, después pasá a la renderización manual con Bootstrap.

---

## Renderización manual — control total

Para integrar con Bootstrap u otro framework, se renderiza campo por campo:

```html
<form method="POST" novalidate>
  {% csrf_token %}

  <!-- Campo individual -->
  <div class="mb-3">
    <label for="{{ form.nombre.id_for_label }}" class="form-label">
      {{ form.nombre.label }}
    </label>
    <input
      type="text"
      id="{{ form.nombre.id_for_label }}"
      name="{{ form.nombre.html_name }}"
      class="form-control {% if form.nombre.errors %}is-invalid{% endif %}"
      value="{{ form.nombre.value|default:'' }}"
    />
    {% for error in form.nombre.errors %}
    <div class="invalid-feedback">{{ error }}</div>
    {% endfor %}
  </div>

  <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

---

## Mostrar errores generales del formulario

Algunos errores no corresponden a un campo específico (errores de lógica cruzada entre campos). Se muestran con `non_field_errors`:

```html
{% if form.non_field_errors %}
<div class="alert alert-danger">
  {% for error in form.non_field_errors %}
  <p>{{ error }}</p>
  {% endfor %}
</div>
{% endif %}
```

---

---

# Parte V — `form.cleaned_data`: los datos ya validados

---

Cuando el usuario envía un formulario, los datos llegan como texto puro — todo es `str`. Django los recibe, los valida y los convierte al tipo correcto. El resultado de esa conversión se llama `cleaned_data`.

Pensalo así: `request.POST` es la materia prima en bruto. `cleaned_data` es el producto ya procesado, verificado y listo para usar.

```python
if form.is_valid():
    nombre  = form.cleaned_data['nombre']   # str
    edad    = form.cleaned_data['edad']     # int — ya no es el string "25"
    precio  = form.cleaned_data['precio']   # Decimal
    activo  = form.cleaned_data['activo']   # bool — ya no es el string "on"
```

**¿Por qué no usar `request.POST` directamente?**

`request.POST['edad']` devuelve `"25"` (un string). Si el campo recibió `"veinticinco"`, no hay error — pero el código va a romper cuando intente usarlo como número. `cleaned_data` garantiza que el dato es un `int` o lanza error antes de llegar ahí.

```python
# MAL — sin pasar por el formulario
edad = int(request.POST['edad'])   # explota si el usuario escribió letras

# BIEN — usando cleaned_data
edad = form.cleaned_data['edad']   # ya es int, ya fue validado
```

> 💡 **Tip**: `cleaned_data` solo existe si `is_valid()` devolvió `True`. Si intentas acceder a `cleaned_data` antes de validar, Django lanza un error. El orden importa: primero `is_valid()`, después `cleaned_data`.

> _"`cleaned_data` es como el control de calidad de una fábrica: los datos que salen de ahí ya pasaron todas las pruebas. Puedes usarlos con confianza."_

---

---

# Parte VI — Ejemplo completo: formulario de suscripción

---

**Contexto**: una app de newsletter con un formulario de suscripción que pide nombre y email.

### `forms.py`

```python
from django import forms

class SuscripcionForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=80,
        min_length=2
    )
    email = forms.EmailField(
        label='Correo electrónico'
    )
    acepta_terminos = forms.BooleanField(
        label='Acepto los términos y condiciones',
        required=True
    )
```

### `views.py`

```python
from django.shortcuts import render, redirect
from .forms import SuscripcionForm

def suscribir(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email  = form.cleaned_data['email']
            # en este punto los datos son válidos y están limpios
            # se podrían guardar, enviar email, etc.
            return render(request, 'confirmacion.html', {'nombre': nombre})
    else:
        form = SuscripcionForm()

    return render(request, 'suscripcion.html', {'form': form})
```

### `urls.py` de la app

```python
from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('suscribir/', views.suscribir, name='suscribir'),
]
```

### `templates/suscripcion.html`

```html
{% extends 'base.html' %} {% block content %}

<div class="container my-5">
  <h1>Suscribirse al Newsletter</h1>

  <form method="POST" novalidate>
    {% csrf_token %}

    <div class="mb-3">
      <label for="{{ form.nombre.id_for_label }}" class="form-label">
        {{ form.nombre.label }}
      </label>
      <input
        type="text"
        id="{{ form.nombre.id_for_label }}"
        name="nombre"
        class="form-control {% if form.nombre.errors %}is-invalid{% endif %}"
        value="{{ form.nombre.value|default:'' }}"
      />
      {% for error in form.nombre.errors %}
      <div class="invalid-feedback">{{ error }}</div>
      {% endfor %}
    </div>

    <div class="mb-3">
      <label for="{{ form.email.id_for_label }}" class="form-label">
        {{ form.email.label }}
      </label>
      <input
        type="email"
        id="{{ form.email.id_for_label }}"
        name="email"
        class="form-control {% if form.email.errors %}is-invalid{% endif %}"
        value="{{ form.email.value|default:'' }}"
      />
      {% for error in form.email.errors %}
      <div class="invalid-feedback">{{ error }}</div>
      {% endfor %}
    </div>

    <div class="mb-3 form-check">
      <input
        type="checkbox"
        id="{{ form.acepta_terminos.id_for_label }}"
        name="acepta_terminos"
        class="form-check-input {% if form.acepta_terminos.errors %}is-invalid{% endif %}"
      />
      <label
        for="{{ form.acepta_terminos.id_for_label }}"
        class="form-check-label"
      >
        {{ form.acepta_terminos.label }}
      </label>
    </div>

    <button type="submit" class="btn btn-primary">Suscribirse</button>
  </form>
</div>

{% endblock %}
```

### `templates/confirmacion.html`

```html
{% extends 'base.html' %} {% block content %}

<div class="container my-5 text-center">
  <h1>¡Gracias, {{ nombre }}!</h1>
  <p>La suscripción fue registrada correctamente.</p>
  <a href="{% url 'newsletter:suscribir' %}" class="btn btn-outline-primary">
    Volver
  </a>
</div>

{% endblock %}
```

---

---

# Resumen de la Parte I

---

| Concepto                              | Descripción                                                           |
| ------------------------------------- | --------------------------------------------------------------------- |
| `forms.Form`                          | Clase base para formularios no ligados a modelos                      |
| `forms.CharField`, `EmailField`, etc. | Tipos de campo con validación automática                              |
| `form.is_valid()`                     | Ejecuta toda la validación. Devuelve `True` o `False`                 |
| `form.cleaned_data`                   | Diccionario con los datos ya validados y convertidos al tipo correcto |
| `form.errors`                         | Diccionario con los errores por campo                                 |
| `{% csrf_token %}`                    | Token de seguridad obligatorio en todo POST                           |
| `{{ form.as_p }}`                     | Renderización rápida — útil para prototipos                           |
| Renderización manual                  | Campo por campo, necesario para integración con Bootstrap             |

---

> _"La validación manual es una trampa. Parece simple al empezar y se convierte en un laberinto cuando el formulario crece. Django Forms fue diseñado exactamente para ese momento."_

---
