# 📖 Guía Completa: `class Meta` en Django

## Todo lo que puedes configurar dentro de un modelo

> Esta guía cubre **todas las opciones** de `class Meta` disponibles en Django. Está pensada como lectura de referencia y consulta.

---

## 🗺️ Índice

| # | Opción | Para qué sirve |
|:--|:-------|:---------------|
| 1 | `ordering` | Definir el orden por defecto de los resultados |
| 2 | `verbose_name` / `verbose_name_plural` | Nombre legible del modelo en el admin |
| 3 | `db_table` | Cambiar el nombre de la tabla en la base de datos |
| 4 | `db_table_comment` | Comentario visible dentro de la base de datos |
| 5 | `unique_together` | Combinaciones de campos que deben ser únicas |
| 6 | `constraints` | Restricciones avanzadas a nivel de base de datos |
| 7 | `indexes` | Índices para acelerar búsquedas |
| 8 | `abstract` | Crear modelos base que no generan tabla propia |
| 9 | `proxy` | Crear variantes de un modelo sin tabla nueva |
| 10 | `managed` | Decidir si Django controla la tabla o no |
| 11 | `permissions` / `default_permissions` | Permisos personalizados y control de los 4 por defecto |
| 12 | `get_latest_by` | Campo para usar con `.latest()` y `.earliest()` |
| 13 | `default_related_name` | Nombre por defecto para relaciones inversas |
| 14 | `order_with_respect_to` | Ordenar objetos hijos respecto a su padre |
| 15 | `app_label` | Asignar un modelo a una app específica |
| 16 | `default_manager_name` / `base_manager_name` | Cambiar el manager por defecto |
| 17 | `required_db_vendor` / `required_db_features` | Restringir modelo a un motor de BD específico |
| 18 | `select_on_save` / `db_tablespace` | Opciones avanzadas de bajo nivel |
| 19 | `Meta` en `ModelForm` | Opciones especiales para formularios |

---

---

# 1. `ordering` — El Orden por Defecto

---

Cuando haces `MiModelo.objects.all()`, Django no garantiza ningún orden a menos que lo definas.

Con `ordering` en `Meta` defines el orden que se aplicará **automáticamente** a todas las consultas:

```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        # ↑ todos los querysets vienen ordenados A-Z por nombre
```

### Opciones de orden

| Sintaxis | Significado |
|:---------|:-----------|
| `['nombre']` | Ascendente (A → Z, 1 → 99) |
| `['-nombre']` | Descendente (Z → A, 99 → 1) |
| `['categoria', 'nombre']` | Primero por categoría, luego por nombre |
| `['-fecha_creacion']` | Los más recientes primero |

> ⚠️ `ordering` agrega un `ORDER BY` a **todas** las consultas de ese modelo. Si no lo necesitas siempre, es mejor usar `.order_by()` solo cuando lo requieras.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — ordering*. https://docs.djangoproject.com/en/stable/ref/models/options/#ordering

---

---

# 2. `verbose_name` y `verbose_name_plural`

---

Estos definen cómo aparece el nombre del modelo en el **panel de administración** y en mensajes del sistema:

```python
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
```

### ¿Qué pasa si NO los defines?

Django genera el nombre automáticamente a partir del nombre de la clase:

| Clase | `verbose_name` automático | `verbose_name_plural` automático |
|:------|:--------------------------|:---------------------------------|
| `Categoria` | "categoria" | "categorias" |
| `UserProfile` | "user profile" | "user profiles" |
| `ProductoVenta` | "producto venta" | "producto ventas" |

El problema es que **no maneja tildes ni reglas del español**, por eso conviene definirlos manualmente.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — verbose_name*. https://docs.djangoproject.com/en/stable/ref/models/options/#verbose-name

---

---

# 3. `db_table` — Nombrar la Tabla

---

Por defecto Django crea la tabla como `nombre_app_nombre_modelo`. Pero puedes cambiarla:

```python
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'clientes'
        # ↑ en vez de "miapp_cliente", la tabla se llama "clientes"
```

### ¿Cuándo usarlo?

| Situación | ¿Conviene usar `db_table`? |
|:----------|:--------------------------|
| Proyecto nuevo desde cero | No — el nombre automático funciona bien |
| Conectar Django a una base de datos que ya existe | **Sí** — necesitas que coincida con la tabla existente |
| Migración desde otro framework | **Sí** — para no renombrar tablas |

> ⚠️ Si cambias `db_table` después de hacer migraciones, necesitas crear una nueva migración. Django renombrará la tabla en la base de datos.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — db_table*. https://docs.djangoproject.com/en/stable/ref/models/options/#db-table

---

---

# 4. `db_table_comment` — Comentario en la Tabla

---

Agrega un comentario visible directamente dentro de la base de datos. Útil para personas que acceden a la BD sin pasar por Django:

```python
class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()

    class Meta:
        db_table_comment = 'Respuestas a preguntas del formulario de evaluación'
```

Este comentario aparece cuando alguien ejecuta `\dt+` en PostgreSQL o `SHOW TABLE STATUS` en MySQL. No afecta el comportamiento de Django, solo documenta la tabla para quienes trabajan directamente con la base de datos.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — db_table_comment*. https://docs.djangoproject.com/en/stable/ref/models/options/#db-table-comment

---

---

# 5. `unique_together` — Combinaciones únicas

---

A veces un solo campo no necesita ser único, pero **la combinación de dos o más campos sí**:

```python
class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = [['estudiante', 'curso']]
        # ↑ un estudiante no puede inscribirse dos veces al mismo curso
        #   pero puede inscribirse en muchos cursos diferentes
```

### ¿Cómo funciona?

```
estudiante_id=1, curso_id=1  ← ✅ primera vez, se acepta
estudiante_id=1, curso_id=2  ← ✅ diferente curso, se acepta
estudiante_id=2, curso_id=1  ← ✅ diferente estudiante, se acepta
estudiante_id=1, curso_id=1  ← ❌ REPETIDO, Django lanza IntegrityError
```

> ⚠️ Django recomienda usar `constraints` con `UniqueConstraint` (sección 5) en vez de `unique_together` para proyectos nuevos.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — unique_together*. https://docs.djangoproject.com/en/stable/ref/models/options/#unique-together

---

---

# 6. `constraints` — Restricciones Avanzadas

---

Es la versión moderna y más potente de `unique_together` (sección 5). Permite definir restricciones complejas directamente en la base de datos:

```python
from django.db.models import UniqueConstraint, CheckConstraint, Q

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        constraints = [
            # No puede haber dos productos con el mismo nombre
            UniqueConstraint(
                fields=['nombre'],
                name='producto_nombre_unico'
            ),

            # El precio siempre debe ser positivo
            CheckConstraint(
                check=Q(precio__gt=0),
                name='producto_precio_positivo'
            ),
        ]
```

### Tipos de constraints

| Tipo | ¿Qué hace? |
|:-----|:-----------|
| `UniqueConstraint` | Garantiza que una combinación de campos sea única |
| `CheckConstraint` | Verifica que una condición se cumpla siempre |

> 💡 `CheckConstraint` es muy útil: puedes impedir datos inválidos directamente en la base de datos, no solo en el formulario. Si alguien introduce datos por SQL o por otro sistema, la restricción sigue protegiendo.

> 📚 **Fuente:** Django Software Foundation. (2024). *Constraints reference*. https://docs.djangoproject.com/en/stable/ref/models/constraints/

---

---

# 7. `indexes` — Índices para Buscar más Rápido

---

Un índice es como el **índice de un libro**: en vez de leer todas las páginas para encontrar un tema, vas directo a la página correcta.

En la base de datos funciona igual: si buscas frecuentemente por un campo, un índice acelera esa búsqueda.

```python
from django.db.models import Index

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    ciudad = models.CharField(max_length=50)

    class Meta:
        indexes = [
            Index(fields=['email'], name='idx_cliente_email'),
            Index(fields=['ciudad', 'nombre'], name='idx_cliente_ciudad_nombre'),
        ]
```

### ¿Cuándo crear un índice?

| Situación | ¿Índice? |
|:----------|:---------|
| Campo que usas mucho en `filter()` | **Sí** |
| Campo que usas en `order_by()` frecuentemente | **Sí** |
| Campo que rara vez se busca | **No** — el índice ocupa espacio sin beneficio |
| Tabla con pocos registros (< 1000) | **No** — el beneficio es insignificante |

> ⚠️ Los índices aceleran las **lecturas** pero hacen más lentas las **escrituras** (INSERT, UPDATE, DELETE), porque la BD debe actualizar el índice cada vez.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model index reference*. https://docs.djangoproject.com/en/stable/ref/models/indexes/

---

---

# 8. `abstract` — Modelos Base sin Tabla

---

Un modelo abstracto **no crea tabla en la base de datos**. Solo sirve para que otros modelos hereden sus campos y métodos:

```python
class ModeloBase(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ↑ NO se crea tabla para ModeloBase

# Estos modelos heredan los 3 campos de ModeloBase
class Cliente(ModeloBase):
    nombre = models.CharField(max_length=100)
    # tiene: nombre + creado_en + actualizado_en + activo

class Producto(ModeloBase):
    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # tiene: titulo + precio + creado_en + actualizado_en + activo
```

### ¿Para qué sirve?

Evita repetir los mismos campos en múltiples modelos. Si 10 modelos necesitan `creado_en` y `actualizado_en`, los defines **una vez** en el modelo abstracto.

> 📚 **Fuente:** Django Software Foundation. (2024). *Abstract base classes*. https://docs.djangoproject.com/en/stable/topics/db/models/#abstract-base-classes

---

---

# 9. `proxy` — Variantes sin Tabla Nueva

---

Un modelo proxy **usa la misma tabla** que el modelo original, pero puede tener sus propios métodos, managers o comportamiento en el admin:

```python
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    despachado = models.BooleanField(default=False)

class PedidoPendiente(Pedido):
    class Meta:
        proxy = True
        # ↑ NO crea tabla nueva, usa la tabla de Pedido

    class PendienteManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(despachado=False)

    objects = PendienteManager()

# Uso:
PedidoPendiente.objects.all()
# ↑ solo trae los pedidos no despachados
```

### ¿Cuándo usarlo?

| Situación | ¿Proxy? |
|:----------|:--------|
| Quieres una vista filtrada del mismo modelo | **Sí** |
| Quieres métodos distintos para un subconjunto | **Sí** |
| Necesitas campos adicionales | **No** — un proxy no puede agregar campos |

> 📚 **Fuente:** Django Software Foundation. (2024). *Proxy models*. https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models

---

---

# 10. `managed` — ¿Django Controla la Tabla?

---

```python
class TablaExterna(models.Model):
    codigo = models.CharField(max_length=20, primary_key=True)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'tabla_que_ya_existe_en_la_bd'
```

Con `managed = False` le dices a Django:

- **No** crees esta tabla con `migrate`
- **No** la borres ni la modifiques
- **Sí** déjame hacer consultas con el ORM sobre ella

Esto es útil cuando trabajas con una **base de datos que ya existe** y cuyas tablas son administradas por otro sistema o equipo.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — managed*. https://docs.djangoproject.com/en/stable/ref/models/options/#managed

---

---

# 11. `permissions` y `default_permissions` — Permisos

---

Django crea automáticamente 4 permisos por modelo: `add`, `change`, `delete`, `view`. Pero puedes agregar permisos propios:

```python
class Reporte(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()

    class Meta:
        permissions = [
            ('exportar_reporte', 'Puede exportar reportes a PDF'),
            ('aprobar_reporte', 'Puede aprobar reportes'),
        ]
```

Después de hacer `migrate`, estos permisos quedan disponibles para asignar a usuarios o grupos desde el admin o con código:

```python
# Verificar si un usuario tiene el permiso
if usuario.has_perm('miapp.exportar_reporte'):
    # puede exportar
```

### `default_permissions` — Controlar los 4 permisos automáticos

Por defecto Django crea 4 permisos por modelo: `add`, `change`, `delete`, `view`. Puedes cambiar o quitar este comportamiento:

```python
class ModeloSoloLectura(models.Model):
    dato = models.TextField()

    class Meta:
        default_permissions = ('view',)
        # ↑ solo crea permiso de ver, no de agregar/editar/borrar

class ModeloSinPermisos(models.Model):
    dato = models.TextField()

    class Meta:
        default_permissions = ()
        # ↑ no crea ningún permiso automático
```

> 📚 **Fuente:** Django Software Foundation. (2024). *Custom permissions*. https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions

---

---

# 12. `get_latest_by` — Para `.latest()` y `.earliest()`

---

```python
class Articulo(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField()

    class Meta:
        get_latest_by = 'fecha_publicacion'

# Uso:
ultimo = Articulo.objects.latest()
# ↑ devuelve el artículo con la fecha_publicacion más reciente

primero = Articulo.objects.earliest()
# ↑ devuelve el más antiguo
```

Sin `get_latest_by`, llamar a `.latest()` o `.earliest()` sin argumentos lanza un error.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — get_latest_by*. https://docs.djangoproject.com/en/stable/ref/models/options/#get-latest-by

---

---

# 13. `default_related_name` — Relaciones Inversas

---

Cuando haces una ForeignKey, Django crea automáticamente un atributo inverso llamado `modelo_set`. Puedes cambiarlo para todo el modelo:

```python
class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    texto = models.TextField()

    class Meta:
        default_related_name = 'comentarios'

# Sin default_related_name:
articulo.comentario_set.all()

# Con default_related_name:
articulo.comentarios.all()
# ↑ más legible y natural
```

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — default_related_name*. https://docs.djangoproject.com/en/stable/ref/models/options/#default-related-name

---

---

# 14. `order_with_respect_to` — Ordenar Hijos Respecto al Padre

---

Hace que los objetos relacionados tengan un **orden editable** respecto a su objeto padre:

```python
class Pregunta(models.Model):
    texto = models.TextField()

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto = models.TextField()

    class Meta:
        order_with_respect_to = 'pregunta'
        # ↑ las respuestas de cada pregunta tienen un orden propio
```

Al usar `order_with_respect_to`, Django agrega internamente un campo `_order` y te da dos métodos:

```python
# Obtener el orden actual de las respuestas de una pregunta
pregunta = Pregunta.objects.get(id=1)
pregunta.get_respuesta_order()
# → [1, 2, 3]  (IDs en orden)

# Cambiar el orden
pregunta.set_respuesta_order([3, 1, 2])
```

> ⚠️ No se puede usar `order_with_respect_to` junto con `ordering` — son mutuamente excluyentes.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — order_with_respect_to*. https://docs.djangoproject.com/en/stable/ref/models/options/#order-with-respect-to

---

---

# 15. `app_label` — Asignar Modelo a una App

---

Si defines un modelo **fuera de una app** listada en `INSTALLED_APPS`, necesitas decirle manualmente a qué app pertenece:

```python
class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        app_label = 'mi_app'
        # ↑ Django tratará este modelo como si perteneciera a 'mi_app'
```

En la práctica, casi nunca se usa porque los modelos se definen dentro de su app. Pero aparece en proyectos grandes donde los modelos se organizan en paquetes separados.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — app_label*. https://docs.djangoproject.com/en/stable/ref/models/options/#app-label

---

---

# 16. `default_manager_name` y `base_manager_name`

---

Controlan **qué manager** usa Django en distintos contextos:

```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    # Manager personalizado que filtra solo activos
    activos = ActivoManager()
    # Manager original sin filtro
    objects = models.Manager()

    class Meta:
        default_manager_name = 'objects'
        # ↑ cuando Django necesite un manager (ej: admin), usará 'objects'
```

| Opción | ¿Cuándo se usa ese manager? |
|:-------|:---------------------------|
| `default_manager_name` | Para el admin, serialización, y código que usa `Model._default_manager` |
| `base_manager_name` | Para relaciones y operaciones internas del ORM |

> 💡 Si solo tienes `objects`, no necesitas estas opciones. Son útiles cuando defines **múltiples managers** y quieres controlar cuál es el principal.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — default_manager_name*. https://docs.djangoproject.com/en/stable/ref/models/options/#default-manager-name

---

---

# 17. `required_db_vendor` y `required_db_features`

---

Restringen el modelo para que solo funcione con un **motor de base de datos específico**:

```python
class ModeloPostgreSQL(models.Model):
    datos = models.JSONField()

    class Meta:
        required_db_vendor = 'postgresql'
        # ↑ este modelo solo se crea si usas PostgreSQL
        #   en SQLite o MySQL, Django lo ignora durante migrate
```

```python
class ModeloGIS(models.Model):
    ubicacion = models.PointField()

    class Meta:
        required_db_features = ['gis_enabled']
        # ↑ solo se crea si la BD soporta GIS (PostGIS, SpatiaLite)
```

### Vendors disponibles

| Valor | Motor |
|:------|:------|
| `'sqlite'` | SQLite |
| `'postgresql'` | PostgreSQL |
| `'mysql'` | MySQL / MariaDB |
| `'oracle'` | Oracle |

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — required_db_vendor*. https://docs.djangoproject.com/en/stable/ref/models/options/#required-db-vendor

---

---

# 18. `select_on_save` y `db_tablespace` — Opciones de Bajo Nivel

---

Estas opciones se usan en situaciones muy específicas:

### `select_on_save`

```python
class MiModelo(models.Model):
    dato = models.TextField()

    class Meta:
        select_on_save = True
        # ↑ Django hace un SELECT antes de cada UPDATE al guardar
        #   Necesario solo con ciertos triggers de PostgreSQL
```

Por defecto es `False`. Solo se activa cuando hay triggers `ON UPDATE` en la BD que devuelven `NULL`, lo que confunde al algoritmo de guardado de Django.

### `db_tablespace`

```python
class MiModelo(models.Model):
    dato = models.TextField()

    class Meta:
        db_tablespace = 'mi_tablespace'
        # ↑ almacena esta tabla en un tablespace específico de la BD
```

Los tablespaces son una forma de organizar dónde se almacenan físicamente las tablas dentro del motor de BD. Solo es relevante en PostgreSQL y Oracle con configuraciones avanzadas de almacenamiento.

> 📚 **Fuente:** Django Software Foundation. (2024). *Model Meta options — select_on_save*. https://docs.djangoproject.com/en/stable/ref/models/options/#select-on-save

---

---

# 19. `Meta` en `ModelForm` — Opciones para Formularios

---

La clase `Meta` también se usa dentro de `ModelForm` para controlar qué campos aparecen en el formulario:

```python
from django import forms

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'ciudad']
        # ↑ solo estos 3 campos aparecen en el formulario

        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Escribe tu nombre'}),
        }
```

### Opciones disponibles en `ModelForm.Meta`

| Opción | ¿Qué controla? |
|:-------|:---------------|
| `model` | A qué modelo corresponde el formulario |
| `fields` | Lista de campos a incluir (o `'__all__'` para todos) |
| `exclude` | Lista de campos a excluir |
| `widgets` | Personalizar el widget HTML de cada campo |
| `labels` | Texto personalizado para la etiqueta de cada campo |
| `help_texts` | Texto de ayuda debajo de cada campo |
| `error_messages` | Mensajes de error personalizados |

> 📚 **Fuente:** Django Software Foundation. (2024). *ModelForm — Selecting fields*. https://docs.djangoproject.com/en/stable/topics/forms/modelforms/#selecting-the-fields-to-use

---

---

# 📋 Resumen General

---

| Opción | Una frase |
|:-------|:---------|
| `ordering` | Orden por defecto de todos los querysets |
| `verbose_name` / `verbose_name_plural` | Nombre legible en el admin |
| `db_table` | Nombre personalizado de la tabla |
| `db_table_comment` | Comentario visible dentro de la base de datos |
| `unique_together` | Combinación de campos que no se puede repetir |
| `constraints` | Restricciones avanzadas (versión moderna de unique_together) |
| `indexes` | Acelerar búsquedas frecuentes |
| `abstract` | Modelo base que no crea tabla |
| `proxy` | Variante de un modelo que usa la misma tabla |
| `managed` | Que Django no toque una tabla existente |
| `permissions` | Permisos personalizados para users |
| `default_permissions` | Controlar los 4 permisos automáticos |
| `get_latest_by` | Campo para `.latest()` y `.earliest()` |
| `default_related_name` | Nombre de la relación inversa |
| `order_with_respect_to` | Ordenar hijos respecto a su padre |
| `app_label` | Asignar modelo a una app específica |
| `default_manager_name` | Cambiar el manager principal |
| `base_manager_name` | Cambiar el manager base para relaciones |
| `required_db_vendor` | Restringir a un motor de BD específico |
| `required_db_features` | Restringir a BDs con ciertas capacidades |
| `select_on_save` | SELECT antes de UPDATE al guardar |
| `db_tablespace` | Almacenar tabla en un tablespace específico |

> 📚 **Referencia completa:** Django Software Foundation. (2024). *Model Meta options*. https://docs.djangoproject.com/en/stable/ref/models/options/

---
