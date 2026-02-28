# 🐍 Django — Módulo 6 · Clase 4 (Parte 2)

### El Lenguaje de Templates de Django (DTL) y Contexto Global

---

> _"El template no es solo HTML. Es un motor que habla su propio idioma."_

---

## ¿De qué hablaremos hoy?

En la parte anterior aprendimos **cómo conectar** los templates con estáticos, Bootstrap y URLs. Ahora vamos a aprender **el idioma que hablan los templates de Django** para mostrar, filtrar y transformar datos.

- 🔤 El **Django Template Language (DTL)**: variables, filtros y etiquetas.
- 🌐 Los **Context Processors**: cómo hacer que cierta información llegue a TODOS los templates automáticamente, sin tener que pasarla en cada vista.

---

---

# PARTE 1: EL LENGUAJE DE TEMPLATES DE DJANGO (DTL)

---

## 1. ¿Qué es el DTL?

Cuando Django procesa un archivo `.html`, lo lee como si fuera un documento con un **idioma especial** mezclado con HTML común. Ese idioma es el **Django Template Language (DTL)**.

El DTL tiene tres elementos principales:

| Elemento             | Sintaxis                 | ¿Para qué?                                       |
| -------------------- | ------------------------ | ------------------------------------------------ |
| **Variables**        | `{{ variable }}`         | Mostrar un valor                                 |
| **Filtros**          | `{{ variable\|filtro }}` | Transformar un valor antes de mostrarlo          |
| **Etiquetas (Tags)** | `{% etiqueta %}`         | Ejecutar lógica (condicionales, bucles, bloques) |

> 🏭 **Analogía:** Piensa en el template como una **fábrica de papel**. El HTML es la hoja en blanco. Las variables `{{ }}` son los datos que entran. Los filtros `|` son las máquinas que procesan esos datos. Y las etiquetas `{% %}` son los operarios que toman decisiones.

---

## 2. Variables `{{ }}`

Ya las conocemos de clases anteriores. Una variable muestra el valor que la vista envió en el **contexto**.

```python
# views.py — la vista envía un contexto
return render(request, 'home.html', {
    'nombre': 'Ana',
    'precio': 15990,
    'producto': producto_obj,  # un objeto del modelo Producto
})
```

```html
<!-- template — se usan las variables -->
<p>Hola, {{ nombre }}</p>
→ Hola, Ana
<p>Precio: ${{ precio }}</p>
→ Precio: $15990
<p>Producto: {{ producto.nombre }}</p>
→ Producto: Televisor
<p>Precio final: {{ producto.precio_final }} → Precio final: 12990</p>
```

> 💡 Cuando la variable es un objeto del modelo, podemos acceder a sus atributos y métodos usando el punto `.`. Django no necesita paréntesis para llamar a métodos sin argumentos.

---

## 3. Filtros `|` — Las máquinas transformadoras

Un filtro transforma el valor de una variable **justo antes de mostrarlo**. Se escribe con el carácter pipe `|` después de la variable.

**Sintaxis:**

```
{{ variable|filtro }}
{{ variable|filtro:argumento }}
```

### Los filtros más usados en proyectos reales

---

#### `|upper` y `|lower` — Cambiar mayúsculas/minúsculas

```html
{{ 'hola mundo'|upper }} → HOLA MUNDO {{ 'HOLA MUNDO'|lower }} → hola mundo
```

---

#### `|length` — Contar elementos

Funciona con textos y con listas.

```html
{{ 'Django'|length }} → 6 {{ request.session.carrito|length }} → 3 (si hay 3
items)
```

> 🎯 **Usamos esto en nuestro proyecto:** El badge del carrito muestra la cantidad con `{{ request.session.carrito|length }}`.

---

#### `|truncatechars` — Recortar texto largo

Muy útil para mostrar descripciones en tarjetas sin que desborden.

```html
{{ producto.descripcion|truncatechars:80 }}
```

Si `descripcion` tiene 200 caracteres, solo mostrará los primeros 80 y agregará `...` al final.

**Ejemplo real:**

```
"Este televisor Samsung de 55 pulgadas ofrece resolución 4K Ultra HD con..."
```

---

#### `|truncatewords` — Recortar por palabras

Similar al anterior pero corta por palabras completas, no por caracteres.

```html
{{ producto.descripcion|truncatewords:10 }} → "Este televisor Samsung de 55
pulgadas ofrece resolución 4K Ultra..."
```

---

#### `|date` — Formatear fechas

```html
{{ mensaje.fecha|date:"d/m/Y" }} → 15/03/2026 {{ mensaje.fecha|date:"d \d\e F
\d\e Y" }} → 15 de Marzo de 2026 {{ mensaje.fecha|date:"H:i" }} → 14:30
```

**Códigos de formato más comunes:**

| Código | Significa     | Ejemplo |
| ------ | ------------- | ------- |
| `d`    | Día con cero  | `05`    |
| `j`    | Día sin cero  | `5`     |
| `m`    | Mes numérico  | `03`    |
| `F`    | Mes completo  | `Marzo` |
| `Y`    | Año 4 dígitos | `2026`  |
| `H:i`  | Hora:Minutos  | `14:30` |

---

#### `|default` — Valor por defecto si está vacío

Si una variable no tiene valor (`None`, vacío, `0`), muestra un texto alternativo.

```html
{{ producto.descripcion|default:"Sin descripción disponible." }} {{
usuario.telefono|default:"No registrado" }}
```

---

#### `|floatformat` — Formatear decimales

Controla cuántos decimales mostrar.

```html
{{ producto.precio|floatformat:0 }} → 15990 (sin decimales) {{
producto.precio|floatformat:2 }} → 15990.00 (2 decimales)
```

---

#### `|linebreaks` y `|linebreaksbr` — Respetar saltos de línea

Cuando un texto tiene saltos de línea (`\n`), el HTML por defecto los ignora. Estos filtros los convierten en etiquetas `<br>` o `<p>`.

```html
{{ mensaje.contenido|linebreaks }} → Envuelve cada párrafo en
<p></p>
{{ mensaje.contenido|linebreaksbr }} → Reemplaza \n por <br />
```

---

#### `|add` — Sumar un valor

```html
{{ producto.stock|add:10 }} → Si stock=5, muestra: 15
```

---

#### `|yesno` — Convertir booleanos en texto

```html
{{ producto.disponible|yesno:"Disponible,Agotado,Desconocido" }} → Si True →
"Disponible" → Si False → "Agotado" → Si None → "Desconocido"
```

---

### Encadenar filtros

Los filtros se pueden **encadenar**: el resultado del primero entra al segundo.

```html
{{ producto.descripcion|truncatewords:15|upper }} → Recorta a 15 palabras Y las
pone en mayúscusas {{ nombre|lower|truncatechars:20 }} → Todo en minúsculas Y
recortado a 20 caracteres
```

---

#### `|capfirst` y `|title` — Capitalizar texto

```html
{{ 'hola mundo'|capfirst }} → Hola mundo (solo la primera letra) {{ 'hola
mundo'|title }} → Hola Mundo (primera letra de cada palabra)
```

Muy útil para mostrar nombres de productos o autores con formato correcto.

---

#### `|wordcount` — Contar palabras

```html
{{ producto.descripcion|wordcount }} → 42 (si la descripción tiene 42 palabras)
```

---

#### `|join` — Unir una lista en un texto

Si tienes una lista de elementos, los une con el separador que elijas.

```html
{{ categorias|join:", " }} → Electrónica, Hogar, Ropa
```

---

#### `|first` y `|last` — Primer y último elemento

```html
{{ productos|first }} → El primer producto de la lista {{ productos|last }} → El
último producto de la lista
```

---

#### `|slice` — Recortar una lista

Equivalente al slicing de Python. Toma solo una parte de la lista.

```html
{{ productos|slice:":3" }} → Solo los primeros 3 productos {{
productos|slice:"2:5" }} → Del tercero al quinto
```

**Ejemplo práctico — mostrar solo los últimos 5 productos en la home:**

```html
{% for p in productos|slice:":5" %}
<p>{{ p.nombre }}</p>
{% endfor %}
```

---

#### `|safe` — Confiar en el HTML de una variable

Por defecto, Django **escapa** todo el HTML que viene en variables para evitar ataques. Si necesitas mostrar HTML guardado en la base de datos (ej: texto con formato), usas `|safe`.

```html
<!-- Sin |safe: Django escapa el HTML (lo muestra como texto) -->
{{ noticia.contenido }} → &lt;p&gt;Texto con
&lt;b&gt;negritas&lt;/b&gt;&lt;/p&gt;

<!-- Con |safe: Django respeta el HTML -->
{{ noticia.contenido|safe }} → Texto con negritas
```

> ⚠️ **Cuidado:** Solo usa `|safe` con contenido que tú o tu sistema guardaron. Nunca con contenido escrito por usuarios desconocidos (riesgo de ataque XSS).

---

#### `|striptags` — Eliminar etiquetas HTML

Lo contrario de `|safe`: elimina todas las etiquetas HTML de una variable.

```html
{{ noticia.contenido|striptags }} → Convierte "
<p>Hola <b>mundo</b></p>
" en "Hola mundo"
```

Útil para mostrar un preview de texto sin formato.

---

#### `|pluralize` — Pluralizar en inglés (o con argumento en español)

```html
{{ productos|length }} producto{{ productos|length|pluralize }} → 1 producto
(cuando hay 1) → 3 productos (cuando hay más de 1)

<!-- Con argumento personalizado para español -->
{{ errores|length }} error{{ errores|length|pluralize:"es" }} → 1 error → 3
errores
```

---

#### `|filesizeformat` — Formatear tamaño de archivos

```html
{{ archivo.tamanio|filesizeformat }} → 1.5 MB (en vez de mostrar 1572864 bytes)
```

---

#### `|divisibleby` — ¿Es divisible por N?

Devuelve `True` o `False`. Muy usado dentro de `{% if %}` para crear patrones.

```html
{% if forloop.counter|divisibleby:2 %}
<!-- Cada fila par tendrá fondo distinto -->
{% endif %}
```

---

#### `|urlize` — Convertir URLs en links clicables

Si una variable tiene texto que incluye una URL (`https://...`), `|urlize` la convierte automáticamente en un `<a href>`.

```html
{{ comentario.texto|urlize }} → "Mira esto: https://google.com" se convierte en
→ "Mira esto: <a href="https://google.com">https://google.com</a>"
```

---

#### `|make_list` — Convertir texto en lista de caracteres

```html
{{ 'django'|make_list }} → ['d', 'j', 'a', 'n', 'g', 'o']
```

No es muy común, pero sirve para procesar texto carácter a carácter.

---

### Tabla resumen de filtros (completa)

| Filtro              | Uso                       | Resultado ejemplo       |
| ------------------- | ------------------------- | ----------------------- |
| `\|upper`           | Mayúsculas                | `"HOLA"`                |
| `\|lower`           | Minúsculas                | `"hola"`                |
| `\|capfirst`        | Primera letra mayúscula   | `"Hola mundo"`          |
| `\|title`           | Cada palabra en mayúscula | `"Hola Mundo"`          |
| `\|length`          | Contar caracteres/items   | `6`                     |
| `\|wordcount`       | Contar palabras           | `42`                    |
| `\|truncatechars:N` | Recortar a N caracteres   | `"Texto cor..."`        |
| `\|truncatewords:N` | Recortar a N palabras     | `"Hola mundo con..."`   |
| `\|date:"formato"`  | Formatear fecha           | `"15/03/2026"`          |
| `\|default:"texto"` | Valor si está vacío       | `"Sin datos"`           |
| `\|floatformat:N`   | Decimales                 | `"15990.00"`            |
| `\|linebreaks`      | Saltos de línea a `<p>`   | HTML formateado         |
| `\|yesno:"a,b,c"`   | Booleano a texto          | `"Disponible"`          |
| `\|join:"sep"`      | Unir lista                | `"A, B, C"`             |
| `\|first`           | Primer elemento           | primer objeto           |
| `\|last`            | Último elemento           | último objeto           |
| `\|slice:":N"`      | Recortar lista            | primeros N elementos    |
| `\|safe`            | Confiar en el HTML        | Renderiza HTML          |
| `\|striptags`       | Eliminar HTML             | Texto limpio            |
| `\|pluralize`       | Pluralizar                | `"errores"`             |
| `\|filesizeformat`  | Tamaño legible            | `"1.5 MB"`              |
| `\|divisibleby:N`   | ¿Divisible por N?         | `True` / `False`        |
| `\|urlize`          | URLs → links clicables    | `<a href="...">...</a>` |
| `\|add:N`           | Sumar un valor            | `15` (si stock=5 +10)   |

> _"Los filtros son las tijeras del template: recortan, transforman y presentan los datos exactamente como los necesitas."_

---

## 4. Etiquetas (Tags) `{% %}` — La lógica del template

Las etiquetas ejecutan **lógica real** dentro del template. Ya conocemos algunas: `{% for %}`, `{% if %}`, `{% extends %}`, `{% block %}`. Vamos a profundizar y ver algunas nuevas.

---

### `{% if %}`, `{% elif %}`, `{% else %}` — Tomar decisiones

Es como el `if/elif/else` de Python. Permite mostrar contenido condicionalmente.

```html
{% if producto.stock > 10 %}
<span class="text-success">✅ Stock suficiente</span>
{% elif producto.stock > 0 %}
<span class="text-warning">⚠️ Pocas unidades</span>
{% else %}
<span class="text-danger">🚫 Sin stock</span>
{% endif %}
```

**Operadores disponibles dentro de `{% if %}`:**

| Operador          | Significado              | Ejemplo                              |
| ----------------- | ------------------------ | ------------------------------------ |
| `==`              | Igual                    | `{% if nombre == 'Ana' %}`           |
| `!=`              | Distinto                 | `{% if estado != 'activo' %}`        |
| `>` `<` `>=` `<=` | Comparación numérica     | `{% if precio > 1000 %}`             |
| `in`              | Está dentro de una lista | `{% if p.id in carrito %}`           |
| `not`             | Negación                 | `{% if not disponible %}`            |
| `and`             | Y lógico                 | `{% if precio > 0 and disponible %}` |
| `or`              | O lógico                 | `{% if sin_stock or sin_precio %}`   |

---

### `{% for %}` — Iterar sobre listas

Recorre cualquier lista o queryset.

```html
{% for producto in productos %}
<p>{{ forloop.counter }}. {{ producto.nombre }}</p>
{% empty %}
<p>No hay productos disponibles.</p>
{% endfor %}
```

**Variables especiales disponibles dentro de `{% for %}`:**

| Variable           | Valor                              | Ejemplo de uso           |
| ------------------ | ---------------------------------- | ------------------------ |
| `forloop.counter`  | Número de iteración (empieza en 1) | `1, 2, 3...`             |
| `forloop.counter0` | Número de iteración (empieza en 0) | `0, 1, 2...`             |
| `forloop.first`    | `True` si es la primera vuelta     | `{% if forloop.first %}` |
| `forloop.last`     | `True` si es la última vuelta      | `{% if forloop.last %}`  |

**Ejemplo práctico — alternar el color de filas:**

```html
{% for p in productos %}
<tr class="{% if forloop.counter|divisibleby:2 %}table-light{% endif %}">
  <td>{{ p.nombre }}</td>
  <td>${{ p.precio }}</td>
</tr>
{% endfor %}
```

> El `{% empty %}` se muestra **solo si la lista está vacía**. Reemplaza el clásico `{% if productos %}...{% else %}...{% endif %}`.

---

### `{% with %}` — Variables temporales dentro del template

Crea una variable temporal para no repetir expresiones largas.

```html
<!-- Sin {% with %}: repetición -->
<p>Precio: ${{ producto.precio_final }}</p>
<p>Ahorro: ${{ producto.ahorro_monto }}</p>
<p>¿Vale la pena? {% if producto.ahorro_monto > 1000 %}Sí{% endif %}</p>

<!-- Con {% with %}: más limpio -->
{% with precio=producto.precio_final ahorro=producto.ahorro_monto %}
<p>Precio: ${{ precio }}</p>
<p>Ahorro: ${{ ahorro }}</p>
<p>¿Vale la pena? {% if ahorro > 1000 %}Sí{% endif %}</p>
{% endwith %}
```

Muy útil cuando usas el mismo valor complejo varias veces seguidas.

---

### `{% url %}` — Generar URLs

```html
<a href="{% url 'lista_productos' %}">Catálogo</a>
<a href="{% url 'detalle_producto' producto.id %}">Ver {{ producto.nombre }}</a>
```

---

### `{% include %}` — Incluir otro template

Permite insertar el contenido de un template dentro de otro. Ideal para **componentes reutilizables** como tarjetas de productos, sidebars o formularios.

```html
<!-- base.html o cualquier template -->
{% include 'componentes/tarjeta_producto.html' with producto=p %}
```

```html
<!-- componentes/tarjeta_producto.html (el fragmento reutilizable) -->
<div class="card">
  <div class="card-body">
    <h5>{{ producto.nombre }}</h5>
    <p>${{ producto.precio_final }}</p>
  </div>
</div>
```

**¿Cuándo usarlo?**

- Si en varias páginas muestras el mismo bloque HTML (tarjetas, alertas, formularios).
- En vez de copiar y pegar, haces un `{% include %}` desde todas las páginas.

> 🧩 **Analogía:** `{% extends %}` dice _"soy hijo de base.html"_. `{% include %}` dice _"inserta ese pedazo de HTML aquí dentro"_. Son conceptos distintos: herencia vs inclusión.

---

### `{% now %}` — Mostrar la fecha/hora actual

Muestra la fecha actual sin necesidad de pasarla desde la vista.

```html
<footer>© {% now "Y" %} Mi Sitio</footer>
→ © 2026 Mi Sitio {% now "d/m/Y H:i" %} → 26/02/2026 21:37
```

Usa los mismos códigos de formato que el filtro `|date`.

---

### `{% cycle %}` — Alternar entre valores

Alterna cíclicamente entre los valores que le des, una vez por iteración del `{% for %}`.

```html
{% for p in productos %}
<tr class="{% cycle 'table-light' 'table-white' %}">
  <td>{{ p.nombre }}</td>
</tr>
{% endfor %} → Fila 1: table-light → Fila 2: table-white → Fila 3: table-light
(vuelve a empezar) → ...
```

Alternativa más limpia que el `|divisibleby` para alternar clases.

---

### `{% ifchanged %}` — Mostrar algo solo cuando cambia el valor

Dentro de un `{% for %}`, muestra contenido solo cuando el valor cambia entre una iteración y la siguiente.

```html
{% for producto in productos %} {% ifchanged producto.categoria.nombre %}
<h3>{{ producto.categoria.nombre }}</h3>
<!-- Solo se muestra cuando cambia la categoría -->
{% endifchanged %}
<p>{{ producto.nombre }}</p>
{% endfor %}
```

**Resultado:**

```
📂 Electrónica
  Televisor 55"
  Parlante Bluetooth
📂 Hogar
  Silla Ergonómica
  Escritorio
```

Organiza listas agrupadas automáticamente sin escribir lógica extra.

---

### `{# Esto es un comentario #}` — Comentarios en templates

El HTML tiene `<!-- comentarios -->` que se envían al navegador (cualquiera los puede ver). Los comentarios del DTL **no se envían al navegador** nunca.

```html
<!-- Este comentario HTML SÍ llega al navegador -->
{# Este comentario DTL NO llega al navegador. Útil para notas del desarrollador.
#} {% comment %} Este bloque entero es un comentario de varias líneas. Django lo
ignora completamente. Útil para "apagar" bloques de código temporalmente. {%
endcomment %}
```

---

> _"Un template bien escrito con DTL se lee casi como español: 'Para cada producto en la lista, si tiene descuento, muestra el precio final'. Eso es programar con claridad."_

---

---

# PARTE 2: CONTEXT PROCESSORS — DATOS GLOBALES

---

## 5. El problema: datos que necesitan todos los templates

Imagina que en CADA página de tu sitio quieres mostrar:

- El **nombre del usuario** logueado en la navbar.
- La **cantidad de ítems** en el carrito.
- La **fecha de hoy** en el footer.

Con lo que sabemos hasta ahora, tendrías que **pasar ese dato en el contexto de CADA vista**:

```python
# Esto sería sin context processors — ¡repetición en cada vista!
def lista_productos(request):
    return render(request, 'lista.html', {
        'productos': productos,
        'items_carrito': len(request.session.get('carrito', [])),  # ← repetido
        'fecha_hoy': date.today(),  # ← repetido
    })

def detalle_producto(request, producto_id):
    return render(request, 'detalle.html', {
        'producto': producto,
        'items_carrito': len(request.session.get('carrito', [])),  # ← repetido
        'fecha_hoy': date.today(),  # ← repetido
    })

# ... y así en las 20 vistas del proyecto
```

Esto rompe el principio **DRY** completamente. ¿No debería haber una forma de enviar datos a TODOS los templates de una sola vez?

---

## 6. ¿Qué es un Context Processor?

Un **Context Processor** es una función de Python que Django ejecuta **automáticamente en CADA request** y agrega variables al contexto de TODOS los templates.

> 🏛️ **Analogía:** Imagina que el alcalde de una ciudad (Django) tiene un asistente (context processor) que sale cada mañana a buscar información del día (temperatura, noticias, alertas). Cuando cualquier funcionario (vista) necesita información para preparar un informe (template), ese asistente ya puso la información en la mesa antes que nadie llegue. Nadie tiene que pedirla.

---

## 7. Los Context Processors que Django ya incluye

Django trae context processors activados por defecto. Están configurados en `settings.py`:

```python
TEMPLATES = [
    {
        # ...
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',    # ← request disponible
                'django.contrib.auth.context_processors.auth',   # ← user disponible
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Gracias a estos, en cualquier template puedes usar:**

| Variable disponible | ¿De dónde viene?              | Ejemplo de uso en template       |
| ------------------- | ----------------------------- | -------------------------------- |
| `{{ request }}`     | `context_processors.request`  | `{{ request.user.username }}`    |
| `{{ user }}`        | `context_processors.auth`     | `{% if user.is_authenticated %}` |
| `{{ messages }}`    | `context_processors.messages` | `{% for msg in messages %}`      |

> 🎯 **Eso explica algo que ya usamos:** En `base.html` escribimos `{{ request.session.carrito|length }}` directamente en el template ¡sin pasarlo en el contexto de ninguna vista! Funciona porque `request` siempre está disponible gracias al context processor `context_processors.request`.

---

## 8. Crear un Context Processor personalizado

Para datos propios del proyecto (como el nombre del sitio, información global de configuración, etc.), podemos crear nuestros propios context processors.

**Paso 1:** Crear el archivo de context processors en la app `core`:

```python
# core/context_processors.py

def datos_globales(request):
    """
    Este diccionario se agrega automáticamente al contexto
    de TODOS los templates del proyecto.
    """
    from datetime import date

    return {
        'nombre_sitio': 'CatálogoApp',     # Nombre del sitio, siempre disponible
        'anio_actual': date.today().year,  # Año actual para el footer
        'version_app': '1.0.0',            # Versión de la aplicación
    }
```

**Paso 2:** Registrarlo en `settings.py`:

```python
# config/settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.datos_globales',   # ← El nuestro
            ],
        },
    },
]
```

```html
<!-- templates/base.html -->
<title>{{ nombre_sitio }}</title>

<footer>
  <p>© {{ anio_actual }} {{ nombre_sitio }}</p>
  <small>v{{ version_app }}</small>
</footer>
```

Ahora `nombre_sitio`, `anio_actual` y `version_app` están disponibles en **absolutamente todos los templates** del proyecto, sin tener que pasarlos en ninguna vista.

---

## 9. ¿Cuándo usar un Context Processor vs el contexto de la vista?

Esta es una pregunta de diseño importante:

**🔵 Datos que van en el contexto de la VISTA** (específicos de una página):

| Tipo de dato                               | ¿Por qué aquí?                          |
| ------------------------------------------ | --------------------------------------- |
| Lista de todos los productos del catálogo  | Solo la página del catálogo la necesita |
| Un producto específico (detalle)           | Solo la página de detalle lo necesita   |
| Resultados de una búsqueda                 | Solo la página de búsqueda los muestra  |
| Productos dentro del carrito               | Solo la página del carrito los usa      |
| Total a pagar en el carrito                | Solo la página del carrito lo calcula   |
| Mensajes de error de un formulario         | Solo la página con ese formulario       |
| Una categoría para filtrar productos       | Solo esa página de categoría específica |
| Datos de un usuario en su página de perfil | Solo la página de perfil del usuario    |

**🟢 Datos que van en un Context Processor** (necesarios en todas las páginas):

| Tipo de dato                                 | ¿Por qué aquí?               |
| -------------------------------------------- | ---------------------------- |
| Nombre del sitio web (en `<title>` y navbar) | Aparece en TODAS las páginas |
| Año actual (en el footer)                    | Aparece en TODAS las páginas |
| Versión de la aplicación (en el footer)      | Aparece en TODAS las páginas |
| Usuario logueado (nombre en el navbar)       | Aparece en TODAS las páginas |
| Contador del carrito (badge en el navbar)    | Aparece en TODAS las páginas |
| Links del menú principal (si son dinámicos)  | Aparece en TODAS las páginas |
| Redes sociales del footer                    | Aparece en TODAS las páginas |
| Idioma o configuración regional del sitio    | Aparece en TODAS las páginas |
| Aviso de mantenimiento o banner global       | Aparece en TODAS las páginas |

> 📐 **Regla simple:** Si un dato aparece en el `base.html` o en algo que todas las páginas heredan → Context Processor. Si es específico de una sola página → contexto de la vista.

---

## 10. El flujo completo con todo lo aprendido

Ahora podemos ver el ciclo completo de cómo llega la información a un template:

```text
El usuario entra a misitio.com/productos/
        │
        ▼
┌─────────────────────────────────┐
│         urls.py                 │
│  Ruta: path('', lista_view)     │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│    Context Processors           │  ← Se ejecutan SIEMPRE, automáticamente
│  + nombre_sitio = "CatálogoApp" │
│  + anio_actual = 2026           │
│  + items_en_carrito = 3         │
│  + request = (el request)       │
│  + user = (usuario actual)      │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│         views.py                │  ← La vista agrega sus propios datos
│  lista_view(request)            │
│  contexto = {                   │
│      'productos': [...]         │  ← Solo lo que necesita ESTA página
│  }                              │
└───────────────┬─────────────────┘
                ▼
┌─────────────────────────────────┐
│       template.html             │  ← Recibe TODO: datos de la vista + globales
│  {{ nombre_sitio }}   ← global  │
│  {{ anio_actual }}    ← global  │
│  {{ productos }}      ← de vista│
│  {{ user.username }}  ← global  │
└───────────────┬─────────────────┘
                ▼
        Navegador del usuario
```

---

## 📋 Resumen de la parte 2

| Concepto              | Sintaxis                                                        | ¿Para qué?                               |
| --------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| **Variable**          | `{{ variable }}`                                                | Mostrar un dato del contexto             |
| **Filtro**            | `{{ var\|filtro }}`                                             | Transformar el dato antes de mostrarlo   |
| **Filtros clave**     | `\|length`, `\|truncatechars`, `\|date`, `\|default`, `\|yesno` | Transformaciones comunes                 |
| **Etiqueta if**       | `{% if %}...{% elif %}...{% else %}...{% endif %}`              | Lógica condicional                       |
| **Etiqueta for**      | `{% for x in lista %}...{% empty %}...{% endfor %}`             | Iterar listas                            |
| **Etiqueta with**     | `{% with var=expresion %}...{% endwith %}`                      | Variable temporal                        |
| **Comentario DTL**    | `{# comentario #}`                                              | Notas que no llegan al navegador         |
| **Context Processor** | Función en `context_processors.py`                              | Datos disponibles en TODOS los templates |
| **Registro**          | `settings.py → TEMPLATES → context_processors`                  | Activar el processor                     |
| **Uso**               | `{{ variable_global }}` en cualquier template                   | Sin tocar ninguna vista                  |

---

> 🚀 _"Ahora ya sabes hablar el idioma de los templates de Django. Y más importante: sabes dónde poner cada dato para que llegue exactamente donde tiene que llegar."_
