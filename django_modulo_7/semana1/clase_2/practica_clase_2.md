# Django — Módulo 7 · Clase 2

## Práctica: Tu Propia Base de Datos en la Nube

---

## El objetivo

Hoy abandonamos la base de datos compartida de ayer. Cada estudiante va a crear su propia base de datos PostgreSQL en la nube, conectar Django exclusivamente a ella, y organizar los modelos de manera profesional usando la estructura de carpetas `models/`.

---

## Paso 1 — Limpiar el proyecto base

Abre el proyecto que construiste en la Clase 1 y **elimina** lo siguiente:

- Todo el contenido de `menu/models.py` (o la carpeta `menu/models/` si ya existe)
- Todo el contenido de `menu/admin.py`
- Los archivos de migraciones dentro de `menu/migrations/` **excepto** el archivo `__init__.py`

El proyecto queda como nueva base para este ejercicio. No se toca `settings.py` todavía.

---

## Paso 2 — Crear tu propia cuenta en Supabase

Supabase es el servicio de base de datos en la nube que usaremos. Es gratuito para proyectos de práctica.

🔗 **[https://supabase.com](https://supabase.com)**

1. Ingresa a la URL y crea una cuenta con tu mail o con tu cuenta de GitHub
2. Una vez dentro, haz clic en **"New project"**
3. Elige un nombre para el proyecto (por ejemplo: `django-practica`)
4. Elige una región — selecciona **South America** si está disponible, o **US East**
5. Crea una contraseña para la base de datos y **guárdala** — no la puedes recuperar después
6. Espera unos segundos mientras Supabase provisiona la base de datos

Una vez creado el proyecto, ve a **Project Settings → Database** para obtener tus credenciales.

---

## Paso 3 — Configurar la conexión en Django (una sola base de datos)

En la Clase 1 teníamos una configuración de dos bases de datos (`default` y `supabase_ro`). Hoy usamos **una sola**: la tuya en Supabase.

Reemplaza el bloque `DATABASES` completo en `settings.py` por este, usando **tus propias credenciales**:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "la-contraseña-que-creaste",
        "HOST": "db.xxxxxxxxxxxxxxxxxx.supabase.co",
        "PORT": "5432",
    }
}
```

> ℹ️ El `HOST` lo encontras en **Project Settings → Database → Connection info → Host**. Tiene el formato `db.xxxxxxxxxxxx.supabase.co`.

Verifica que la conexión funciona ejecutando:

```bash
python manage.py migrate
```

Si no hay errores, Django se conectó correctamente y creó sus tablas internas en tu base de datos.

---

## Paso 4 — Crear la estructura de carpetas `models/`

En lugar de un único `models.py`, vas a crear una **carpeta** que organiza los modelos por responsabilidad.

Dentro de la app `menu`, **elimina** el archivo `models.py` y crea la siguiente estructura:

```
menu/
├── models/
│   ├── __init__.py
│   ├── categoria.py
│   ├── marca.py
│   ├── producto.py
│   ├── variante.py
│   ├── imagen.py
│   ├── cliente.py
│   ├── direccion.py
│   ├── carrito.py
│   ├── carrito_item.py
│   ├── pedido.py
│   ├── linea_pedido.py
│   ├── pago.py
│   ├── cupon.py
│   ├── resena.py
│   └── notificacion.py
```

---

## Paso 5 — Los 15 modelos a implementar

Debes implementar los siguientes 15 modelos. Cada uno vive en su propio archivo. La descripción es intencional: el código lo escribes tú, no se entrega el modelo hecho. Si flatan campos los debes agregar.

| #   | Archivo           | Modelo         | Descripción breve                                         |
| --- | ----------------- | -------------- | --------------------------------------------------------- |
| 1   | `categoria.py`    | `Categoria`    | Nombre y descripción de la categoría de producto          |
| 2   | `marca.py`        | `Marca`        | Nombre y país de origen de la marca                       |
| 3   | `producto.py`     | `Producto`     | Nombre, precio, descripción, categoría (FK) y marca (FK)  |
| 4   | `variante.py`     | `Variante`     | Talla, color y stock de cada variante de un producto (FK) |
| 5   | `imagen.py`       | `Imagen`       | URL de imagen y producto al que pertenece (FK)            |
| 6   | `cliente.py`      | `Cliente`      | Nombre, email y teléfono del cliente                      |
| 7   | `direccion.py`    | `Direccion`    | Dirección de envío vinculada a un cliente (FK)            |
| 8   | `carrito.py`      | `Carrito`      | Carrito de compras activo vinculado a un cliente (FK)     |
| 9   | `carrito_item.py` | `CarritoItem`  | Producto y cantidad dentro de un carrito (FKs)            |
| 10  | `pedido.py`       | `Pedido`       | Fecha, estado y total del pedido de un cliente (FK)       |
| 11  | `linea_pedido.py` | `LineaPedido`  | Producto, precio unitario y cantidad en un pedido (FKs)   |
| 12  | `pago.py`         | `Pago`         | Método, monto y estado del pago de un pedido (FK)         |
| 13  | `cupon.py`        | `Cupon`        | Código, descuento y fecha de vencimiento                  |
| 14  | `resena.py`       | `Resena`       | Calificación y comentario de un cliente sobre un producto |
| 15  | `notificacion.py` | `Notificacion` | Mensaje y estado (leído/no leído) para un cliente (FK)    |

---

## Paso 6 — El archivo `__init__.py`

Para que el resto del proyecto pueda importar los modelos normalmente, el archivo `menu/models/__init__.py` debe reexportarlos todos:

```python
# menu/models/__init__.py

from .categoria    import Categoria
from .marca        import Marca
from .producto     import Producto
from .variante     import Variante
from .imagen       import Imagen
from .cliente      import Cliente
from .direccion    import Direccion
from .carrito      import Carrito
from .carrito_item import CarritoItem
from .pedido       import Pedido
from .linea_pedido import LineaPedido
from .pago         import Pago
from .cupon        import Cupon
from .resena       import Resena
from .notificacion import Notificacion
```

---

## Paso 7 — Migraciones y verificación

Una vez que tengas los 15 modelos escritos:

```bash
python manage.py makemigrations menu
python manage.py migrate
```

Si todo funciona, Django habrá creado las 15 tablas en tu base de datos de Supabase.

Verifica en el **Table Editor** de Supabase que las tablas existen.

---

## Validación

La práctica está completa cuando puedes mostrar en Supabase:

- Las 15 tablas creadas en el Table Editor
- Al menos 3 modelos registrados en `admin.py` y visibles en el Django Admin
- El archivo `menu/models/__init__.py` con los 15 imports

---
