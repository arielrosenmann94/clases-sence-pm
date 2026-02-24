# 🛠️ Django — Módulo 6 · Guía Práctica (Clase 2)

### Arquitectura Profesional, Lógica de Negocio y Sesiones

> Esta guía continúa el proyecto **`catalogoapp`** iniciado en la Clase 1. A través de este ejercicio, transformaremos un proyecto básico en una aplicación con estructura profesional y funcionalidades de negocio reales.

---

## Introducción

En esta segunda clase, nuestro objetivo es "limpiar" el código heredado y agregar nuevas responsabilidades al sistema. No crearemos un proyecto nuevo; refactorizaremos el existente para que cumpla con los estándares de la industria.

---

## Paso 1 — Refactorización Arquitectónica (`config/`)

Actualmente, tu carpeta de configuración se llama igual que el proyecto (`catalogoapp/`). Vamos a cambiarla al nombre estándar **`config`** para evitar confusiones.

### 1.1 Renombrar la carpeta

Cierra tu servidor de desarrollo (`Ctrl+C`) y renombra la carpeta interna:
De: `catalogoapp/catalogoapp/`  
A: **`catalogoapp/config/`**

### 1.2 Actualizar `manage.py`

Abre `manage.py` en la raíz y cambia la referencia a los settings:

```python
# manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Antes decía catalogoapp.settings
```

### 1.3 Actualizar `config/settings.py`

Abre `config/settings.py` y busca las siguientes líneas para actualizarlas:

```python
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
```

### 1.4 Actualizar `wsgi.py` y `asgi.py`

En ambos archivos (`config/wsgi.py` y `config/asgi.py`), cambia la línea del módulo de configuración:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

### 1.5 Verificar la refactorización

Ejecuta el servidor: `python manage.py runserver`. Si el cohete (o tu home) carga sin errores, has migrado con éxito a una arquitectura profesional.

### 1.6 Observación: El otro "Config"

Abre el archivo `productos/apps.py`. Verás una clase llamada `ProductosConfig`.

> 💡 **No te confundas:** Aunque ambos usan la palabra "Config", la carpeta `config/` es la arquitectura de tu proyecto entero, mientras que la clase en `apps.py` es solo la configuración interna de esa aplicación específica.

---

## Paso 2 — Preparación del Catálogo

Para que las funcionalidades matemáticas y de búsqueda tengan sentido, necesitamos datos.

1. Ingresa al panel de administración: `http://127.0.0.1:8000/admin/`.
2. Asegúrate de tener al menos **10 productos** cargados.
3. Agrégales nombres variados y precios distintos.

---

## Paso 3 — Lógica de Negocio en el Modelo ("Fat Models")

Siguiendo el principio de _"Include all relevant domain logic"_, vamos a dotar al modelo `Producto` de la capacidad de calcular ofertas.

### 3.1 Actualizar el Modelo

Abre `productos/models.py` y agrega un campo de descuento y un método de cálculo:

```python
from decimal import Decimal

class Producto(models.Model):
    # ... campos anteriores ...
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0, help_text="Porcentaje de descuento (0-100)")

    def precio_final(self):
        """Calcula el precio aplicando el descuento si existe."""
        if self.descuento > 0:
            rebaja = self.precio * (Decimal(self.descuento) / Decimal(100))
            return self.precio - rebaja
        return self.precio

    def ahorro_monto(self):
        """Devuelve cuánto dinero se ahorra el cliente."""
        return self.precio - self.precio_final()
```

### 3.2 Aplicar Migraciones

Como agregamos el campo `descuento`, debemos migrar:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3.3 Actualizar el Template

Abre `productos/templates/lista_productos.html` y muestra la oferta:

```html
<li>
  <strong>{{ p.nombre }}</strong> <br />
  {% if p.descuento > 0 %}
  <del style="color: grey;">${{ p.precio }}</del>
  <span style="color: red;">{{ p.descuento }}% OFF</span> <br />
  <span style="font-size: 1.2rem; font-weight: bold;"
    >${{ p.precio_final }}</span
  >
  <p style="color: green;">¡Ahorras ${{ p.ahorro_monto }}!</p>
  {% else %}
  <span style="font-size: 1.2rem;">${{ p.precio }}</span>
  {% endif %}
</li>
```

---

## Paso 4 — Carrito de Compras Básico (Uso de Sesiones)

Vamos a usar el objeto `request.session` para que el usuario pueda "guardar" productos mientras navega.

### 4.1 La Vista para Agregar

Abre `productos/views.py` y añade esta lógica sencilla:

```python
from django.shortcuts import redirect

def agregar_al_carrito(request, producto_id):
    # Inicializamos el carrito en la sesión si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    # Agregamos el ID del producto a la lista
    carrito = request.session['carrito']
    carrito.append(producto_id)
    request.session['carrito'] = carrito # Guardamos cambios explícitamente

    return redirect('lista_productos')

def ver_carrito(request):
    ids_en_carrito = request.session.get('carrito', [])
    productos = Producto.objects.filter(id__in=ids_en_carrito)

    total = sum(p.precio_final() for p in productos)

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total
    })
```

### 4.2 Configurar las URLs

En `productos/urls.py`:

```python
path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
path('carrito/', ver_carrito, name='ver_carrito'),
```

### 4.3 Botón en el Catálogo

En `lista_productos.html`, agrega el botón para cada producto:

```html
<a href="{% url 'agregar_al_carrito' p.id %}">🛒 Agregar al carrito</a>
```

---

## Paso 5 — Formulario de Búsqueda (Django Forms)

Implementaremos la búsqueda de productos usando la clase `forms.Form`.

### 5.1 Crear `productos/forms.py`

```python
from django import forms

class BusquedaProductoForm(forms.Form):
    query = forms.CharField(
        label='Buscar por nombre',
        max_length=100,
        required=True
    )
```

### 5.2 Vista con Formulario

En `productos/views.py`:

```python
def buscar_producto(request):
    form = BusquedaProductoForm()
    resultados = []

    if request.method == 'POST':
        form = BusquedaProductoForm(request.POST)
        if form.is_valid():
            termino = form.cleaned_data['query']
            resultados = Producto.objects.filter(nombre__icontains=termino)

    return render(request, 'buscar.html', {'form': form, 'resultados': resultados})
```

---

## Entrega Final

Al terminar, tu proyecto debe permitir:

1. Navegar por `/productos/` con la nueva estructura de carpetas `config/`.
2. Ver productos con descuentos calculados automáticamente.
3. Agregar productos al carrito y ver el total acumulado en `/productos/carrito/`.
4. Buscar productos de manera segura mediante un formulario de Django.
