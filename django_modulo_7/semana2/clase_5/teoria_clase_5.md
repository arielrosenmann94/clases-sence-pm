# 🌌 Módulo 7 — Clase 5
## Relaciones Avanzadas y el Puente entre Requisitos y Código

> **AE 7.3** — Implementar la capa de modelo de acceso a datos utilizando entidades con relaciones uno a uno, uno a muchos y muchos a muchos.
>
> ⚠️ Esta clase es 100% teórica. Continuamos con la práctica iniciada en la Clase 3 (MartilloVirtualDjango).

---

## 🗺️ Índice

| # | Tema |
|---|------|
| **1** | Recap rápido: Lo que cubrimos en la Semana 1 |
| **2** | ManyToManyField a Fondo |
| 2.1 | ¿Qué ocurre en la base de datos? |
| 2.2 | Operaciones: add, remove, set, clear |
| 2.3 | Consultas y filtros con M2M |
| **3** | Modelos Intermedios (`through`) |
| 3.1 | ¿Cuándo la tabla automática no alcanza? |
| 3.2 | Implementación paso a paso |
| 3.3 | Consultas sobre el modelo intermedio |
| **4** | `prefetch_related` vs `select_related` |
| 4.1 | El problema: N+1 en relaciones ManyToMany |
| 4.2 | select_related: JOIN en una sola consulta |
| 4.3 | prefetch_related: dos consultas inteligentes |
| 4.4 | Tabla de decisión |
| **5** | De la Historia del Cliente al Código Django |
| 5.1 | ¿Qué es una Historia de Usuario? |
| 5.2 | El método de los 4 pasos |
| 5.3 | Ejemplo completo: de la historia al QuerySet |
| 5.4 | Herramientas para agilizar la traducción |

---

---

# 📚 1. Recap: Lo que Cubrimos en la Semana 1

Antes de avanzar, recordemos dónde estamos parados:

| Clase | Tema Central | Lo Clave |
|-------|-------------|----------|
| **C1** | Fundamentos del ORM | Conexión, modelos, migraciones, consultas, lazy evaluation, Q Objects |
| **C2** | Arquitectura de Modelos | `models/` como paquete, `__init__.py`, relaciones conceptuales, `Meta` |
| **C3** | Optimización y Entornos Reales | `only`, `defer`, `iterator`, `bulk`, índices, `explain`, `atomic`, Figma |
| **C4** | Relaciones a Fondo (Parte I) | `ForeignKey` (SQL real), 5 opciones de `on_delete`, `related_name`, `OneToOneField`, señales, herramientas de seguridad |

### ¿Qué falta?

En la Clase 4 prometimos profundizar en `prefetch_related` y en `ManyToManyField`. Hoy cumplimos esa promesa, y además aprendemos a traducir requisitos de clientes reales en código Django.

---

---

# 🔗 2. ManyToManyField a Fondo

---

## 2.1 ¿Qué ocurre en la base de datos?

Cuando definimos una relación `ManyToMany`, Django crea automáticamente una **tercera tabla** que conecta las dos entidades. Esta tabla intermedia solo tiene dos columnas: los IDs de cada lado.

Sigamos con el proyecto ficticio **NebulaShop**. Imagina que un pedido puede tener muchos productos, y un producto puede estar en muchos pedidos:

```python
# tienda/models.py

class Pedido(models.Model):
    fecha       = models.DateTimeField(auto_now_add=True)
    cliente     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    completado  = models.BooleanField(default=False)

    productos = models.ManyToManyField(
        'Producto',
        related_name='pedidos',  # producto.pedidos.all()
        blank=True,              # Un pedido puede empezar vacío
    )

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Pedido #{self.id} — {self.cliente.username}"
```

**El SQL que Django genera al migrar:**

```sql
-- Tabla del Pedido (normal, sin sorpresas)
CREATE TABLE "tienda_pedido" (
    "id"          bigint NOT NULL PRIMARY KEY ...,
    "fecha"       timestamp NOT NULL,
    "cliente_id"  integer NOT NULL REFERENCES "auth_user" ("id"),
    "completado"  boolean NOT NULL DEFAULT FALSE
);

-- Tabla intermedia CREADA AUTOMÁTICAMENTE por Django
CREATE TABLE "tienda_pedido_productos" (
    "id"          bigint NOT NULL PRIMARY KEY ...,
    "pedido_id"   bigint NOT NULL REFERENCES "tienda_pedido" ("id"),
    "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id"),
    UNIQUE ("pedido_id", "producto_id")  -- ← Un producto no puede repetirse en el mismo pedido
);
```

**Tres cosas importantes:**

1. **Django nombra la tabla automáticamente:** `app_modelo_campo` → `tienda_pedido_productos`.
2. **La restricción `UNIQUE`** impide que el mismo producto aparezca dos veces en el mismo pedido.
3. **No hay campo M2M en ninguna tabla principal.** La relación vive 100% en la tabla intermedia. El campo `productos` en Python es solo una interfaz para acceder a ella.

> 💡 **Clave:** A diferencia de `ForeignKey` (que agrega una columna en la tabla hija), `ManyToManyField` no agrega ninguna columna en ninguna tabla. Crea una tabla completamente nueva.

---

## 2.2 Operaciones: add, remove, set, clear

Una vez que tenemos la relación definida, Django nos da cuatro métodos para manipularla:

```python
# Crear un pedido
pedido = Pedido.objects.create(cliente=user)

# Obtener algunos productos
telescopio = Producto.objects.get(nombre='Telescopio Refractor')
mapa       = Producto.objects.get(nombre='Mapa Estelar')
poster     = Producto.objects.get(nombre='Póster Galaxia')
```

### `.add()` — Agregar productos al pedido
```python
pedido.productos.add(telescopio, mapa)
# SQL: INSERT INTO tienda_pedido_productos (pedido_id, producto_id)
#      VALUES (1, 1), (1, 2)
# Ahora el pedido tiene 2 productos.
```

### `.remove()` — Quitar un producto del pedido
```python
pedido.productos.remove(mapa)
# SQL: DELETE FROM tienda_pedido_productos
#      WHERE pedido_id=1 AND producto_id=2
# El Mapa Estelar ya no está en el pedido. El producto sigue existiendo en la BD.
```

### `.set()` — Reemplazar todos los productos de golpe
```python
pedido.productos.set([telescopio, poster])
# Django hace un diff: quita lo que sobra, agrega lo que falta.
# El pedido ahora tiene EXACTAMENTE telescopio y poster. Nada más.
```

### `.clear()` — Vaciar el pedido
```python
pedido.productos.clear()
# SQL: DELETE FROM tienda_pedido_productos WHERE pedido_id=1
# El pedido queda sin productos. Los productos siguen existiendo.
```

> ⚠️ **Importante:** Ninguna de estas operaciones elimina los productos reales. Solo eliminan o crean filas en la **tabla intermedia**. El telescopio sigue existiendo en `tienda_producto`.

---

## 2.3 Consultas y filtros con M2M

Las consultas M2M funcionan igual que las de `ForeignKey`, usando el doble guión bajo `__`:

```python
# Desde el Pedido → buscar pedidos que contengan un producto específico
Pedido.objects.filter(productos__nombre='Telescopio Refractor')
# SQL: SELECT * FROM tienda_pedido
#      INNER JOIN tienda_pedido_productos ON ...
#      INNER JOIN tienda_producto ON ...
#      WHERE tienda_producto.nombre = 'Telescopio Refractor'

# Desde el Producto → buscar productos que estén en pedidos completados
Producto.objects.filter(pedidos__completado=True).distinct()
# ↑ .distinct() es OBLIGATORIO cuando cruzas M2M en dirección inversa

# Contar cuántos productos tiene un pedido
pedido.productos.count()
# SQL: SELECT COUNT(*) FROM tienda_pedido_productos WHERE pedido_id=1

# Verificar si un producto está en el pedido
pedido.productos.filter(id=telescopio.id).exists()
# Devuelve True o False — sin cargar el objeto
```

> 💡 **Regla de oro:** Siempre que filtres a través de una relación M2M en dirección inversa, usa `.distinct()`. Sin él, obtienes duplicados porque SQL genera una fila por cada coincidencia en la tabla intermedia.

---

---

# 🔀 3. Modelos Intermedios (`through`)

---

## 3.1 ¿Cuándo la tabla automática no alcanza?

La tabla intermedia que Django crea automáticamente solo tiene dos columnas: `pedido_id` y `producto_id`. Pero en la vida real, la relación misma tiene datos propios:

- ¿Cuántas **unidades** de cada producto hay en el pedido?
- ¿A qué **precio** se agregó? (el precio puede cambiar después)
- ¿Cuándo se **agregó** al pedido?

Para guardar estos datos, necesitamos un **modelo intermedio** explícito.

---

## 3.2 Implementación paso a paso

```python
# tienda/models.py

class ItemPedido(models.Model):
    """
    Modelo intermedio entre Pedido y Producto.
    Cada fila representa UN producto dentro de UN pedido,
    con datos propios de esa relación.
    """
    pedido = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='items',        # pedido.items.all()
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT,    # No borrar productos que ya están en pedidos
        related_name='en_pedidos',   # producto.en_pedidos.all()
    )
    cantidad      = models.PositiveIntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pedido', 'producto')
        # ↑ Un mismo producto no puede repetirse en el mismo pedido.
        #   Si se quieren 3 telescopios, se modifica la cantidad, no se crean 3 filas.

    def subtotal(self):
        return self.cantidad * self.precio_unidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Pedido #{self.pedido.id}"
```

Ahora conectamos el `ManyToManyField` con este modelo usando `through`:

```python
class Pedido(models.Model):
    fecha       = models.DateTimeField(auto_now_add=True)
    cliente     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    completado  = models.BooleanField(default=False)

    productos = models.ManyToManyField(
        'Producto',
        through='ItemPedido',        # ← Le dice a Django: "usa MI tabla, no la automática"
        related_name='pedidos',
        blank=True,
    )
```

> ⚠️ **Cambio importante:** Cuando usas `through`, ya NO puedes usar `.add()`, `.set()` ni `.create()` directamente. Debes crear las filas del modelo intermedio de forma explícita:

```python
# ❌ Ya NO funciona:
pedido.productos.add(telescopio)

# ✅ Forma correcta con through:
ItemPedido.objects.create(
    pedido=pedido,
    producto=telescopio,
    cantidad=2,
    precio_unidad=telescopio.precio,   # Guardamos el precio actual
)
```

---

## 3.3 Consultas sobre el modelo intermedio

La ventaja del modelo `through` es que podemos hacer consultas sobre los datos de la relación misma:

```python
# ¿Cuántas unidades totales tiene este pedido?
from django.db.models import Sum
total_items = pedido.items.aggregate(total=Sum('cantidad'))['total']

# ¿Cuál es el subtotal del pedido?
from django.db.models import F, Sum
subtotal = pedido.items.aggregate(
    total=Sum(F('cantidad') * F('precio_unidad'))
)['total']

# Productos que se han pedido más de 10 veces en TODOS los pedidos
from django.db.models import Sum
Producto.objects.annotate(
    total_vendido=Sum('en_pedidos__cantidad')
).filter(total_vendido__gt=10)
```

> 💡 **¿Cuándo usar `through`?** Siempre que la relación tenga datos propios: cantidad, precio, fecha, rol, puntuación, etc. Si la relación es solo "A está conectado con B" sin datos extra, la tabla automática de Django es suficiente.

---

---

# ⚡ 4. `prefetch_related` vs `select_related`

---

## 4.1 El problema: N+1 en relaciones ManyToMany

En la Clase 4 vimos cómo `select_related` resuelve el N+1 para `ForeignKey` y `OneToOneField`. Pero `select_related` **no funciona con ManyToMany**. ¿Por qué?

`select_related` hace un `JOIN` SQL. Un JOIN funciona bien cuando la relación es 1:1 o N:1 (cada fila del resultado tiene exactamente un padre). Pero en M2M, un pedido puede tener 10 productos y un producto puede estar en 50 pedidos. Un JOIN produciría filas duplicadas y resultados inconsistentes.

Para M2M, Django usa una estrategia diferente: `prefetch_related`.

---

## 4.2 `select_related` — Un JOIN, una consulta

Funciona con `ForeignKey` y `OneToOneField`. Django hace un solo `SELECT` con `JOIN`:

```python
# SIN select_related → N+1 (1 consulta por pedido + 1 por cada cliente)
pedidos = Pedido.objects.all()
for p in pedidos:
    print(p.cliente.username)   # ← Cada iteración dispara una consulta extra
# Total: 1 + N consultas (si hay 100 pedidos = 101 consultas)

# CON select_related → 1 sola consulta con JOIN
pedidos = Pedido.objects.select_related('cliente').all()
for p in pedidos:
    print(p.cliente.username)   # ← Ya está en memoria, cero consultas extra
# SQL: SELECT pedido.*, auth_user.*
#      FROM tienda_pedido
#      INNER JOIN auth_user ON pedido.cliente_id = auth_user.id
# Total: 1 consulta
```

---

## 4.3 `prefetch_related` — Dos consultas inteligentes

Funciona con `ManyToManyField` y relaciones inversas. Django hace **dos consultas separadas** y las junta en Python:

```python
# SIN prefetch_related → N+1
pedidos = Pedido.objects.all()
for p in pedidos:
    for prod in p.productos.all():  # ← Cada pedido dispara una consulta
        print(prod.nombre)
# Total: 1 + N consultas

# CON prefetch_related → exactamente 2 consultas
pedidos = Pedido.objects.prefetch_related('productos').all()
for p in pedidos:
    for prod in p.productos.all():  # ← Ya está en memoria
        print(prod.nombre)
# Consulta 1: SELECT * FROM tienda_pedido
# Consulta 2: SELECT * FROM tienda_producto
#             INNER JOIN tienda_pedido_productos ON ...
#             WHERE tienda_pedido_productos.pedido_id IN (1, 2, 3, ...)
# Total: 2 consultas (siempre 2, sin importar cuántos pedidos haya)
```

### ¿Cómo funciona internamente?

1. Django ejecuta la primera consulta y obtiene todos los pedidos.
2. Toma los IDs de esos pedidos y hace UNA segunda consulta con `WHERE pedido_id IN (...)`.
3. En Python, asigna los productos a cada pedido usando un diccionario.

El resultado es que en lugar de 101 consultas, siempre son exactamente 2.

---

## 4.4 Tabla de decisión

| Tipo de relación | Herramienta | Estrategia SQL | Consultas |
|:-----------------|:------------|:---------------|:----------|
| `ForeignKey` (de hijo a padre) | `select_related` | JOIN | 1 |
| `OneToOneField` | `select_related` | JOIN | 1 |
| `ManyToManyField` | `prefetch_related` | IN (...) | 2 |
| Relación inversa (de padre a hijos) | `prefetch_related` | IN (...) | 2 |

### Combinando ambas

Puedes usar las dos al mismo tiempo cuando una vista necesita datos de múltiples niveles:

```python
# Traer pedidos con su cliente (FK) Y sus productos (M2M) en solo 2 consultas
pedidos = Pedido.objects.select_related('cliente').prefetch_related('productos').all()

for p in pedidos:
    print(p.cliente.username)         # ← Ya en memoria (select_related)
    for prod in p.productos.all():
        print(f"  - {prod.nombre}")   # ← Ya en memoria (prefetch_related)

# Total: 2 consultas en lugar de potencialmente cientos
```

> 💡 **Regla profesional:** Si en tu template o vista haces un loop sobre objetos y dentro accedes a relaciones, SIEMPRE debes usar `select_related` o `prefetch_related`. De lo contrario, cada iteración golpea la base de datos.

---

---

# 🗺️ 5. De la Historia del Cliente al Código Django

---

En la industria, los requisitos no llegan como modelos de Django ni como diagramas ER. Llegan como **historias de usuario** escritas por un Product Owner, un cliente, o incluso un email informal. Saber traducirlas a código es lo que separa al desarrollador que espera instrucciones exactas del que resuelve problemas reales.

## 5.1 ¿Qué es una Historia de Usuario?

Es una frase corta que describe una funcionalidad desde la perspectiva del usuario:

```
"Como [tipo de usuario], quiero [acción], para [beneficio]."
```

Ejemplos reales:

- _"Como cliente, quiero agregar productos a mi carrito, para comprarlos después."_
- _"Como administrador, quiero ver qué productos se venden más, para decidir qué promocionar."_
- _"Como vendedor, quiero crear subastas con fecha de cierre, para que los compradores compitan."_

---

## 5.2 El Método de los 4 Pasos

Cada vez que recibes una historia de usuario, aplica estos 4 pasos para convertirla en código Django:

### Paso 1 — Subrayar los Sustantivos (→ Modelos)

Lee la historia y subraya los **sustantivos** principales. Cada sustantivo importante se convierte potencialmente en un modelo.

> _"Como **cliente**, quiero agregar **productos** a mi **carrito**, para comprarlos después."_

Sustantivos: `Cliente`, `Producto`, `Carrito` → 3 modelos candidatos.

### Paso 2 — Identificar los Verbos (→ Vistas / Operaciones)

Los **verbos** te dicen qué operaciones CRUD necesitas y qué vistas crear.

> _"...quiero **agregar** productos..."_

Verbo: `agregar` → Vista que recibe un producto y lo agrega al carrito → Operación **Create** en la tabla intermedia.

### Paso 3 — Dibujar las Flechas (→ Relaciones)

¿Cómo se conectan los sustantivos?

```
Cliente ──1:1──► Carrito (cada cliente tiene un carrito)
Carrito ──M2M──► Producto (un carrito puede tener muchos productos,
                          un producto puede estar en muchos carritos)
```

¿La relación M2M necesita datos propios? Sí → `cantidad`. Entonces necesitamos un modelo `through`:

```
Carrito ──M2M through ItemCarrito──► Producto
                    │
                    ├── cantidad
                    └── fecha_agregado
```

### Paso 4 — Escribir el QuerySet (→ Consultas)

Antes de escribir la vista completa, escribe primero el QuerySet que necesitas. Esto te obliga a pensar en la consulta de datos antes de pensar en el HTML.

```python
# "Ver los productos de mi carrito"
items = carrito.items.select_related('producto').all()

# "Ver cuánto cuesta mi carrito"
from django.db.models import F, Sum
total = carrito.items.aggregate(
    total=Sum(F('cantidad') * F('producto__precio'))
)['total']
```

---

## 5.3 Ejemplo Completo: De la Historia al QuerySet

Historia:
> _"Como administrador del restaurante, quiero ver cuáles son los 5 platos más pedidos del mes, para decidir qué promocionar."_

**Paso 1 — Sustantivos:** `Administrador` (ya existe: `User`), `Platos`, `Pedidos`, `Mes`.

**Paso 2 — Verbos:** `ver` → Vista Read (listado). `decidir qué promocionar` → Solo es el beneficio, no una acción técnica.

**Paso 3 — Relaciones:**
```
Pedido ──M2M through ItemPedido──► Plato
                  │
                  └── cantidad
```

**Paso 4 — QuerySet:**
```python
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

inicio_mes = timezone.now().replace(day=1)

top_5 = Producto.objects.filter(
    en_pedidos__pedido__fecha__gte=inicio_mes   # Solo pedidos de este mes
).annotate(
    total_vendido=Sum('en_pedidos__cantidad')    # Suma las cantidades
).order_by('-total_vendido')[:5]                 # Los 5 con más ventas

for p in top_5:
    print(f"{p.nombre}: {p.total_vendido} unidades")
```

> 💡 **¿Ven el patrón?** La historia del cliente se convirtió en 4 cosas concretas: modelos, relaciones, una vista y un QuerySet. No hubo adivinanza. Fue un proceso metódico.

---

## 5.4 Herramientas para Agilizar la Traducción

Cuando recibes muchas historias de usuario a la vez, estas técnicas ayudan a organizar el trabajo:

### 📋 Tabla de Mapeo Rápido

Antes de escribir código, llena esta tabla para cada historia:

| Historia | Sustantivos (Modelos) | Verbos (Vistas) | Relaciones | QuerySet clave |
|----------|----------------------|-----------------|------------|----------------|
| "Agregar productos al carrito" | Carrito, Producto, ItemCarrito | Crear (add) | M2M through | `ItemCarrito.objects.create(...)` |
| "Ver mis pedidos anteriores" | Pedido, Usuario | Listar (read) | FK | `Pedido.objects.filter(cliente=user)` |
| "Buscar productos por nombre" | Producto | Filtrar (read) | Ninguna | `.filter(nombre__icontains=q)` |

### 🎯 Criterios de Aceptación = Tests

Los criterios de aceptación de cada historia se convierten directamente en tests:

```
Criterio: "El carrito no debe permitir cantidades negativas."
```
```python
# tests.py
def test_cantidad_negativa_no_permitida(self):
    with self.assertRaises(ValidationError):
        ItemCarrito.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=-1
        )
```

### 📝 Del Email Informal al Modelo

A veces el cliente no escribe historias formales. Escribe un email:

> _"Necesito que los usuarios puedan guardar productos como favoritos y que después los puedan ver en una lista."_

Aplica el método:
1. **Sustantivos:** Usuarios, Productos, Favoritos → 3 modelos (Usuarios ya existe).
2. **Verbos:** guardar como favoritos, ver en una lista → Create + Read.
3. **Relación:** Usuario ──M2M──► Producto (a través de `Favorito`).
4. **¿Datos extra?** Solo `fecha_agregado` → modelo `through` simple.

```python
class Favorito(models.Model):
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    fecha    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')
```

---

---

# 🏁 Tabla Resumen de la Clase

| Concepto | Código / Herramienta | Cuándo usarlo |
|:---------|:--------------------|:-------------|
| **Relación Muchos a Muchos** | `ManyToManyField('Modelo')` | Dos entidades se conectan sin límite |
| **Tabla intermedia automática** | Django la crea solo | La relación no necesita datos propios |
| **Tabla intermedia manual** | `through='ModeloIntermedio'` | La relación tiene cantidad, precio, fecha, etc. |
| **Agregar a M2M** | `.add()` (sin through) o `Intermedio.objects.create()` | Conectar dos registros |
| **Quitar de M2M** | `.remove()` o `.clear()` | Desconectar sin borrar los registros originales |
| **Evitar N+1 en FK** | `select_related('campo')` | JOIN SQL — 1 consulta |
| **Evitar N+1 en M2M** | `prefetch_related('campo')` | IN query — 2 consultas |
| **Combinar ambos** | `.select_related().prefetch_related()` | Cuando la vista necesita datos de FK y M2M |
| **Historia → Modelos** | Subrayar sustantivos | Encontrar las entidades del sistema |
| **Historia → Vistas** | Identificar verbos | Saber qué operaciones CRUD implementar |
| **Historia → Relaciones** | Dibujar flechas entre sustantivos | Definir FK, 1:1 o M2M |
| **Historia → Queries** | Escribir el QuerySet primero | Pensar en datos antes de pensar en HTML |

---

## 📚 Bibliografía y Fuentes

- *Django Software Foundation. (2024). Many-to-many relationships.* [https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_many/](https://docs.djangoproject.com/en/stable/topics/db/examples/many_to_many/)
- *Django Software Foundation. (2024). Extra fields on many-to-many relationships.* [https://docs.djangoproject.com/en/stable/topics/db/models/#extra-fields-on-many-to-many-relationships](https://docs.djangoproject.com/en/stable/topics/db/models/#extra-fields-on-many-to-many-relationships)
- *Django Software Foundation. (2024). Database access optimization — prefetch_related.* [https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related](https://docs.djangoproject.com/en/stable/ref/models/querysets/#prefetch-related)
- *Mike Cohn. (2004). User Stories Applied: For Agile Software Development. Addison-Wesley.*
- *OWASP. (2024). Top 10 Proactive Controls.* [https://owasp.org/www-project-proactive-controls/](https://owasp.org/www-project-proactive-controls/)

---
