# 🛠️ Django — Módulo 6 · Guía Práctica (Clase 3)

### Robustecimiento del Proyecto: Stock, Carrito Inteligente y Navbar Dinámica

> Esta guía continúa el proyecto **`catalogoapp`** de las Clases 1 y 2. No vamos a crear nada desde cero; vamos a **mejorar** lo que ya existe. Cada ejercicio te hará recorrer el ciclo completo de Django: **Modelo → Migración → Vista → URL → Template**.

---

## Ejercicio 1 — Control de Inventario (Stock)

Actualmente puedes agregar productos al carrito infinitamente, aunque no haya existencia real. Vamos a arreglar eso agregando un campo de stock al modelo.

### 1.1 Modificar el Modelo

Abre `productos/models.py`. Este archivo ya tiene tu modelo `Producto` con los campos de la Clase 2. Vamos a agregar el campo `stock` y un método que nos diga si hay disponibilidad.

**Busca** tu clase `Producto` y agrégale estas líneas. Tu modelo completo debería quedar así:

```python
# productos/models.py
from django.db import models
from decimal import Decimal

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    descuento = models.IntegerField(default=0, help_text="Porcentaje de descuento (0-100)")
    stock = models.PositiveIntegerField(default=10)  # ← LÍNEA NUEVA

    def precio_final(self):
        """Calcula el precio aplicando el descuento si existe."""
        if self.descuento > 0:
            rebaja = self.precio * (Decimal(self.descuento) / Decimal(100))
            return self.precio - rebaja
        return self.precio

    def ahorro_monto(self):
        """Devuelve cuánto dinero se ahorra el cliente."""
        return self.precio - self.precio_final()

    def hay_stock(self):                              # ← MÉTODO NUEVO
        """Devuelve True si el producto tiene stock disponible."""
        return self.stock > 0

    def __str__(self):
        return self.nombre
```

**Explicación de las líneas nuevas:**

- `stock = models.PositiveIntegerField(default=10)` → Un número entero que no acepta valores negativos. Todos los productos empiezan con 10 unidades.
- `def hay_stock(self)` → Es un método del modelo (Fat Model). Devuelve `True` o `False`. Así el template puede preguntar `{% if p.hay_stock %}` sin hacer cálculos.

### 1.2 Migrar el cambio

Como modificamos la estructura de la base de datos (agregamos una columna nueva), debemos ejecutar las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

> 💡 Si Django pregunta por un valor por defecto, acepta la opción `1` (usar el default que definimos).

### 1.3 Verificar en el Admin

Entra a `http://127.0.0.1:8000/admin/`, abre cualquier producto y verifica que ahora aparece el campo **Stock** con valor 10. Cambia el stock de uno o dos productos a **0** para poder probar la lógica de "Agotado" más adelante.

### 1.4 Actualizar el Template del Catálogo

Abre `productos/templates/lista_productos.html`. **Busca** la línea que tiene el botón de agregar al carrito:

```html
<a class="btn" href="{% url 'agregar_al_carrito' p.id %}"
  >🛒 Agregar al carrito</a
>
```

**Reemplaza** esa línea por el siguiente bloque completo:

```html
{% if p.hay_stock %}
<a class="btn" href="{% url 'agregar_al_carrito' p.id %}"
  >🛒 Agregar al carrito</a
>
<small style="color: grey;">(Quedan {{ p.stock }} unidades)</small>
{% else %}
<span class="no-disponible" style="font-weight: bold;"
  >🚫 Producto Agotado</span
>
{% endif %}
```

**Explicación línea a línea:**

- `{% if p.hay_stock %}` → Llama al método que acabamos de crear en el modelo. Si devuelve `True`, muestra el botón.
- `{{ p.stock }}` → Muestra el número de unidades disponibles.
- `{% else %}` → Si `hay_stock` devuelve `False` (stock = 0), entra aquí.
- `class="no-disponible"` → Usa la clase CSS que ya definimos en `base.html` (color rojo).

### 1.5 Verificar

Ejecuta el servidor (`python manage.py runserver`) y entra a `/productos/`. Los productos con stock > 0 deben mostrar el botón verde y la cantidad. Los productos con stock = 0 deben mostrar "🚫 Producto Agotado" en rojo, sin botón.

---

## Ejercicio 2 — Eliminar Productos del Carrito

Hasta ahora solo podemos "Agregar" al carrito. Si el usuario se equivoca, no tiene forma de quitar un producto específico. Vamos a resolver esto creando una nueva vista, una nueva URL y actualizando el template.

### 2.1 Crear la Vista

Abre `productos/views.py`. Al final del archivo, **agrega** esta nueva función:

```python
def quitar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', [])   # Obtenemos la lista actual

    if producto_id in carrito:                      # Verificamos que el producto esté
        carrito.remove(producto_id)                 # Eliminamos UNA ocurrencia del ID
        request.session['carrito'] = carrito         # Guardamos los cambios en la sesión

    return redirect('ver_carrito')                  # Volvemos a la página del carrito
```

**Explicación línea a línea:**

- `request.session.get('carrito', [])` → Obtiene la lista de IDs del carrito. Si no existe, devuelve una lista vacía (`[]`).
- `carrito.remove(producto_id)` → Elimina **solo la primera** aparición de ese ID. Si el usuario agregó el mismo producto 3 veces, solo se elimina una.
- `request.session['carrito'] = carrito` → Volvemos a guardar la lista modificada en la sesión. **Sin esta línea, el cambio no se guarda.**

### 2.2 Importar la nueva vista

En el mismo archivo `productos/views.py`, **verifica** que al principio tengas el import de `redirect`:

```python
from django.shortcuts import render, redirect
```

### 2.3 Configurar la URL

Abre `productos/urls.py`. **Reemplaza todo** su contenido por:

```python
# productos/urls.py
from django.urls import path
from .views import (
    lista_productos,
    buscar_producto,
    agregar_al_carrito,
    ver_carrito,
    quitar_del_carrito,        # ← NUEVA
)

urlpatterns = [
    path('', lista_productos, name='lista_productos'),
    path('buscar/', buscar_producto, name='buscar_producto'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),  # ← NUEVA
    path('carrito/', ver_carrito, name='ver_carrito'),
]
```

**Explicación de la línea nueva:**

- `path('carrito/quitar/<int:producto_id>/', ...)` → Cuando el navegador visite `/productos/carrito/quitar/5/`, Django pasará el número `5` como argumento `producto_id` a la vista `quitar_del_carrito`.

### 2.4 Actualizar el Template del Carrito

Abre `productos/templates/carrito.html`. **Reemplaza todo** su contenido por:

```html
{% extends "base.html" %} {% block title %}Mi Carrito{% endblock %} {% block
content %}
<h1>🛒 Mi Carrito</h1>

{% if productos %}
<ul class="lista-productos">
  {% for p in productos %}
  <li>
    <strong>{{ p.nombre }}</strong> —
    <span class="precio">${{ p.precio_final }}</span>
    <a
      href="{% url 'quitar_del_carrito' p.id %}"
      style="color: #e74c3c; margin-left: 15px; text-decoration: none;"
    >
      [❌ Quitar]
    </a>
  </li>
  {% endfor %}
</ul>
<h2>Total: ${{ total }}</h2>
{% else %}
<p>Tu carrito está vacío.</p>
<a class="btn" href="{% url 'lista_productos' %}">Ir al catálogo →</a>
{% endif %} {% endblock %}
```

**Explicación de lo nuevo:**

- `{% url 'quitar_del_carrito' p.id %}` → Genera la URL `/productos/carrito/quitar/5/` automáticamente, usando el ID del producto actual del ciclo `{% for %}`.
- El estilo `color: #e74c3c` es rojo para que el usuario entienda que es una acción destructiva (eliminar).

### 2.5 Verificar

1.  Agrega 2 o 3 productos al carrito desde el catálogo.
2.  Entra a `/productos/carrito/`.
3.  Haz clic en **[❌ Quitar]** en uno de ellos.
4.  Verifica que se elimina solo ese producto y el total se recalcula.

---

## Ejercicio 3 — Contador Dinámico en la Navbar

Actualmente el link del carrito en la navbar dice "🛒 Carrito" sin importar si hay productos o no. Vamos a hacerlo inteligente: que muestre un contador rojo con la cantidad de productos agregados.

### 3.1 Modificar `templates/base.html`

Abre `templates/base.html`. **Busca** esta línea dentro de la `<nav>`:

```html
<a href="{% url 'ver_carrito' %}">🛒 Carrito</a>
```

**Reemplázala** por:

```html
<a href="{% url 'ver_carrito' %}">
  🛒 Carrito {% if request.session.carrito %}
  <span
    style="background: #e74c3c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 4px;"
  >
    {{ request.session.carrito|length }}
  </span>
  {% endif %}
</a>
```

**Explicación línea a línea:**

- `{% if request.session.carrito %}` → Verifica si existe la lista `carrito` en la sesión y si tiene al menos un elemento.
- `{{ request.session.carrito|length }}` → El filtro `|length` cuenta cuántos elementos tiene la lista. Si hay 3 productos, muestra "3".
- El `<span>` con fondo rojo (`#e74c3c`) y bordes redondeados (`border-radius: 12px`) crea una "insignia" (badge) como las que ves en las apps de tu celular.
- `{% endif %}` → Si el carrito está vacío, no se muestra nada extra.

### 3.2 Verificar

1.  Navega a cualquier página del sitio.
2.  Verifica que la navbar muestra "🛒 Carrito" sin número (porque el carrito está vacío).
3.  Agrega un producto desde el catálogo.
4.  Observa que ahora la navbar muestra "🛒 Carrito **1**" con una insignia roja.
5.  Agrega otro producto y verifica que el número sube a **2**.
6.  Entra al carrito, quita un producto, y verifica que el número baja a **1**.

---

## Ejercicio 4 — Vaciar el Carrito Completo

A veces el usuario quiere empezar de cero. Vamos a agregar un botón para vaciar todo el carrito de una vez.

### 4.1 Crear la Vista

Abre `productos/views.py` y **agrega** esta función al final:

```python
def vaciar_carrito(request):
    if 'carrito' in request.session:  # Si existe la clave 'carrito' en la sesión
        del request.session['carrito'] # La eliminamos por completo
    return redirect('ver_carrito')    # Volvemos a la página del carrito (ahora vacío)
```

**Explicación línea a línea:**

- `del request.session['carrito']` → A diferencia de `.remove()` que quita un solo elemento, `del` **elimina toda la lista** de la sesión. Es como tirar todo el carrito a la basura.

### 4.2 Configurar la URL

Abre `productos/urls.py`. **Agrega** esta importación y esta ruta:

En los imports, agrega `vaciar_carrito`:

```python
from .views import (
    lista_productos,
    buscar_producto,
    agregar_al_carrito,
    ver_carrito,
    quitar_del_carrito,
    vaciar_carrito,           # ← NUEVA
)
```

En `urlpatterns`, agrega la ruta:

```python
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),  # ← NUEVA
```

### 4.3 Agregar el Botón en el Template

Abre `productos/templates/carrito.html`. **Busca** la línea:

```html
<h2>Total: ${{ total }}</h2>
```

**Agrega debajo** de esa línea:

```html
<br />
<a
  href="{% url 'vaciar_carrito' %}"
  style="color: white; background: #e74c3c; padding: 8px 16px; border-radius: 6px; text-decoration: none;"
>
  🗑️ Vaciar todo el carrito
</a>
```

**Explicación:**

- El botón solo aparece cuando hay productos (porque está dentro del bloque `{% if productos %}`).
- Usamos fondo rojo (`#e74c3c`) para indicar que es una acción destructiva.

### 4.4 Verificar

1.  Agrega varios productos al carrito.
2.  Entra a `/productos/carrito/`.
3.  Haz clic en **"🗑️ Vaciar todo el carrito"**.
4.  Verifica que el carrito queda vacío y el contador de la navbar desaparece.

---

## Ejercicio 5 — Página de Detalle del Producto

Actualmente, si el usuario quiere ver más información de un producto, no puede. Solo ve el nombre y el precio en la lista. Vamos a crear una página individual para cada producto.

### 5.1 Crear la Vista

Abre `productos/views.py` y **agrega** esta función al final:

```python
from django.shortcuts import get_object_or_404  # ← Agrega este import arriba del archivo

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})
```

**Explicación línea a línea:**

- `get_object_or_404(Producto, id=producto_id)` → Busca un producto por su ID. Si no existe, Django muestra automáticamente una página de error 404 en lugar de romper el sitio. Es más seguro que usar `Producto.objects.get()` directamente.
- `{'producto': producto}` → Pasamos el producto encontrado al template para que lo muestre.

### 5.2 Configurar la URL

Abre `productos/urls.py`. **Agrega** la importación y la ruta:

En los imports:

```python
from .views import (
    lista_productos,
    buscar_producto,
    agregar_al_carrito,
    ver_carrito,
    quitar_del_carrito,
    vaciar_carrito,
    detalle_producto,         # ← NUEVA
)
```

En `urlpatterns`:

```python
    path('<int:producto_id>/', detalle_producto, name='detalle_producto'),  # ← NUEVA
```

> 💡 Esta ruta va **al final** de `urlpatterns` para que no interfiera con las otras rutas como `buscar/` o `carrito/`.

### 5.3 Crear el Template

Crea un archivo nuevo: `productos/templates/detalle_producto.html` con este contenido:

```html
{% extends "base.html" %} {% block title %}{{ producto.nombre }}{% endblock %}
{% block content %}
<h1>{{ producto.nombre }}</h1>

{% if producto.descripcion %}
<p>{{ producto.descripcion }}</p>
{% endif %}

<hr />

{% if producto.descuento > 0 %}
<p>
  Precio original: <del>${{ producto.precio }}</del>
  <span class="descuento">{{ producto.descuento }}% OFF</span>
</p>
<p class="precio" style="font-size: 1.5rem;">${{ producto.precio_final }}</p>
<p class="ahorro">¡Ahorras ${{ producto.ahorro_monto }}!</p>
{% else %}
<p class="precio" style="font-size: 1.5rem;">${{ producto.precio }}</p>
{% endif %}

<p>
  {% if producto.hay_stock %}
  <strong style="color: #27ae60;">✅ En stock</strong>
  ({{ producto.stock }} unidades disponibles) {% else %}
  <strong class="no-disponible">🚫 Sin stock</strong>
  {% endif %}
</p>

<br />

{% if producto.hay_stock %}
<a class="btn" href="{% url 'agregar_al_carrito' producto.id %}"
  >🛒 Agregar al carrito</a
>
{% endif %}

<br /><br />
<a href="{% url 'lista_productos' %}">← Volver al catálogo</a>
{% endblock %}
```

**Explicación de las partes clave:**

- `{{ producto.nombre }}` → Ya no usamos `p` (del ciclo `{% for %}`), sino `producto` porque esta vez la vista pasó un solo objeto, no una lista.
- Reutilizamos los mismos métodos del modelo: `precio_final`, `ahorro_monto`, `hay_stock`. Todo lo que aprendimos en ejercicios anteriores se aplica aquí también.
- Las clases CSS (`precio`, `descuento`, `ahorro`, `no-disponible`, `btn`) ya están definidas en `base.html`, así que el template se ve bien sin agregar estilos nuevos.

### 5.4 Agregar el Link en el Catálogo

Abre `productos/templates/lista_productos.html`. **Busca** la línea:

```html
<strong>{{ p.nombre }}</strong>
```

**Reemplázala** por:

```html
<strong
  ><a
    href="{% url 'detalle_producto' p.id %}"
    style="color: #2c3e50; text-decoration: none;"
    >{{ p.nombre }}</a
  ></strong
>
```

Ahora el nombre de cada producto es un link que lleva a su página de detalle.

### 5.5 Verificar

1.  Entra al catálogo (`/productos/`).
2.  Haz clic en el **nombre** de cualquier producto.
3.  Verifica que se abre una página individual con toda su información: nombre, descripción, precio con descuento, stock disponible y botón de agregar.
4.  Prueba con un producto sin stock y verifica que no aparece el botón de agregar.
5.  Haz clic en "← Volver al catálogo" y verifica que regresa a la lista.

---

## Resumen de lo Practicado

En esta clase recorriste el ciclo de Django **cinco veces**:

**Ejercicio 1 – Stock:** Agregaste un campo al modelo, migraste y usaste `{% if %}` en el template.

**Ejercicio 2 – Quitar del carrito:** Creaste una vista nueva, configuraste una URL con parámetro dinámico y actualizaste el template del carrito.

**Ejercicio 3 – Contador en navbar:** Usaste el filtro `|length` de Django para acceder a datos de sesión directamente desde el template.

**Ejercicio 4 – Vaciar carrito:** Aprendiste a eliminar datos completos de la sesión con `del` y a crear botones de acción destructiva.

**Ejercicio 5 – Detalle de producto:** Creaste una vista, URL, y template completamente nuevos. Usaste `get_object_or_404` para manejar errores. Reutilizaste todos los métodos del modelo aprendidos en clases anteriores.

Si completaste los cinco ejercicios, ya dominas el ciclo fundamental de desarrollo en Django.
