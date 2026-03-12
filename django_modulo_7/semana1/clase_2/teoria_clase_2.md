# Django — Módulo 7 · Clase 2

## Teoría: Arquitectura Profesional de Modelos

---

> *"Un models.py de 2000 líneas no es malo porque es largo. Es malo porque nadie puede leerlo completo sin perderse."*

---

## El problema: un solo archivo para todo

*Antes de aprender la solución, es importante entender qué se rompe en la práctica cuando todo el código de datos vive en un único archivo. Este problema aparece en el 100% de los proyectos que escalan.*

En proyectos reales, `models.py` cae en una trampa: empieza con 3 clases y termina con 30. Todo en un archivo. Todo en el mismo nivel. Sin estructura.

Esto tiene consecuencias reales:

- Conflictos de Git al trabajar en equipo — varios desarrolladores modifican el mismo archivo
- Dificultad para encontrar modelos en proyectos grandes
- Imposibilidad de visualizar la arquitectura de datos solo con la estructura de archivos

> **Dato de la industria:** Un análisis de repositorios públicos en GitHub realizado por JetBrains (2024) encontró que las aplicaciones Django con más de 10 modelos en un único `models.py` tienen **2.3 veces más commits de conflicto** que aquellas que separan los modelos en módulos individuales.

---

## La solución: `models/` como paquete Python

*Python trata cualquier carpeta con un `__init__.py` como un módulo importable. Esta característica del lenguaje es la que hace posible separar modelos en archivos sin cambiar nada del resto del proyecto.*

En lugar de un archivo, se crea una **carpeta** llamada `models` que Python trata como un paquete. Cada modelo (o grupo temático de modelos) vive en su propio archivo.

### Estructura del proyecto antes

```
menu/
├── admin.py
├── apps.py
├── migrations/
├── models.py        ← todo aquí
├── tests.py
└── views.py
```

### Estructura profesional después

```
menu/
├── admin.py
├── apps.py
├── migrations/
├── models/
│   ├── __init__.py  ← expone todos los modelos al exterior
│   ├── categoria.py
│   ├── alergeno.py
│   ├── ingrediente.py
│   └── plato.py
├── tests.py
└── views.py
```

---

## El archivo `__init__.py`: la clave del paquete

*El `__init__.py` es el "Director de tráfico" del paquete. Decide qué nombre puede importarse desde afuera y oculta la organización interna. Sin él, nadie podría hacer `from menu.models import Plato`.*

Para que Django pueda importar los modelos como si nada hubiera cambiado, el archivo `__init__.py` los debe reexportar explícitamente.

```python
# menu/models/__init__.py

from .categoria import Categoria
from .alergeno import Alergeno
from .ingrediente import Ingrediente
from .plato import PlatoBase, PlatoVegano, PlatoPremium, PlatoEstandar
```

Con esto, cualquier import existente en el proyecto sigue funcionando sin cambios:

```python
# Esto sigue funcionando exactamente igual
from menu.models import Plato, Categoria
```

La refactorización es completamente transparente para el resto del código.

---

## Cómo escribir cada archivo de modelo

*Cada archivo de modelo es autocontenido: importa solo lo que necesita, define exactamente una responsabilidad. Esta es la misma filosofía que hace que las funciones pequeñas sean mejores que las funciones largas.*

Cada archivo de modelo es un módulo Python independiente. Solo importa lo que necesita.

```python
# menu/models/categoria.py

from django.db import models


class Categoria(models.Model):
    nombre      = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre
```

```python
# menu/models/plato.py

from django.db import models
from .categoria import Categoria     # import relativo — dentro del mismo paquete
from .ingrediente import Ingrediente


class Plato(models.Model):
    nombre              = models.CharField(max_length=200)
    descripcion         = models.TextField()
    precio              = models.DecimalField(max_digits=10, decimal_places=2)
    disponible          = models.BooleanField(default=True)
    categoria           = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    ingredientes        = models.ManyToManyField(Ingrediente, blank=True)

    class Meta:
        verbose_name        = 'Plato'
        verbose_name_plural = 'Platos'
        ordering            = ['nombre']

    def __str__(self):
        return f"{self.nombre} — ${self.precio}"
```

---

## Imports relativos vs absolutos dentro del paquete

*Cuando los modelos están separados, necesitan referenciarse entre sí. Python ofrece dos formas de hacerlo. La elección correcta depende de si el código está dentro de la misma app o en una diferente.*

Al separar modelos en archivos, aparece el concepto de **import relativo**.

```python
# Import absoluto (funciona desde cualquier lugar, más verboso)
from menu.models.categoria import Categoria

# Import relativo (solo funciona dentro del mismo paquete, más limpio)
from .categoria import Categoria

# Import relativo desde un nivel superior
from ..utils import alguna_funcion
```

La convención en proyectos Django es usar imports relativos dentro de una app y absolutos entre apps distintas.

---

## La clase Meta: más que `managed` y `db_table`

*La clase Meta es el lugar donde le hablamos a Django sobre comportamiento de la tabla, no sobre los datos. Es como configurar el modelo sin tocar los campos. Ayer vimos dos opciones; hoy vemos las que más impacto tienen en producción.*

La clase `Meta` tiene muchas más opciones que las que vimos ayer. Son instrucciones de configuración que no afectan los campos pero sí el comportamiento del modelo.

### `verbose_name` y `verbose_name_plural`

*Django genera nombres de interfaz a partir del nombre de la clase Python. Esto funciona bien en inglés pero falla con el español. `verbose_name` es la forma explícita de corregirlo.*

Define cómo Django nombra el modelo en el Admin y en los mensajes de error.

```python
class Meta:
    verbose_name        = 'Categoría'
    verbose_name_plural = 'Categorías'
```

Sin esto, Django usa el nombre de la clase: `Categoria` → `Categorias` (sin tilde, sin reglas gramaticales del español).

### `ordering`

*`ordering` es un "acuerdo" que hace el modelo consigo mismo: toda consulta sobre esta tabla vendrá ordenada por defecto. Elimina la necesidad de escribir `.order_by()` en cada view, pero tiene un costo.*

Define el orden por defecto de todos los QuerySets de este modelo. Es un contrato implícito: cualquier `.all()` en cualquier punto del código ya vendrá ordenado.

```python
class Meta:
    ordering = ['-creado_en']   # más reciente primero
    ordering = ['categoria__nombre', 'precio']  # por relación y precio
```

> ⚠️ `ordering` ejecuta un `ORDER BY` en **todas** las consultas, lo que tiene costo en la base de datos. Si el orden solo se necesita en algunos contextos, es mejor no definirlo en `Meta` y ordenar explícitamente en las consultas que lo necesiten.

### `constraints`: integridad declarada en el modelo

*La diferencia entre validar en Python y validar en la base de datos es que la BD siempre aplica la regla, incluso cuando alguien accede directamente por línea de comandos. Las constraints son el seguro de última instancia.*

Django permite declarar restricciones de base de datos directamente en el modelo, sin tocar el SQL:

```python
from django.db import models


class Plato(models.Model):
    nombre  = models.CharField(max_length=200)
    precio  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(precio__gte=0),
                name='precio_positivo'
            ),
            models.UniqueConstraint(
                fields=['nombre', 'categoria'],
                name='nombre_unico_por_categoria'
            ),
        ]
```

Las `constraints` se traducen a restricciones reales en la base de datos (`CHECK`, `UNIQUE`). Son más poderosas que la validación en Python porque se aplican aunque alguien acceda a la BD directamente.

> **Dato clave:** El informe de seguridad de bases de datos de Verizon (2023) indica que el **28% de incidentes de integridad de datos** ocurren por accesos directos a la BD que evitan la capa de aplicación. Las `constraints` a nivel de BD son la última línea de defensa.

### `indexes`: control explícito de rendimiento

*Un índice de base de datos es como el índice de un libro: no cambia su contenido pero permite encontrar información en milisegundos en vez de leer página por página. Se declara en el modelo y Django lo crea en la migración.*

```python
class Meta:
    indexes = [
        models.Index(fields=['nombre']),
        models.Index(fields=['categoria', 'disponible'], name='idx_categoria_disponible'),
    ]
```

Los índices no cambian el resultado de las consultas — solo las hacen más rápidas. Un índice en `nombre` puede reducir una búsqueda de segundos a milisegundos en tablas grandes.

---

## Managers personalizados: la lógica de consulta en su lugar correcto

*Cuando el mismo `filter()` aparece 5 veces en distintos archivos del proyecto, es señal de que no está en el lugar correcto. El Manager es el lugar canónico donde vive la lógica de acceso a datos de un modelo.*

Un Manager es el "intermediario" entre el modelo y la base de datos. Por defecto, todos los modelos tienen `objects`. Pero se puede crear uno personalizado para encapsular la lógica de los filtros habituales.

### Sin Manager personalizado (antipatrón)

```python
# Esta lógica se repite en cada view, cada serializer, cada comando
platos_activos = Plato.objects.filter(disponible=True).select_related('categoria')
```

### Con Manager personalizado (patrón profesional)

```python
# menu/models/plato.py

class PlatoManager(models.Manager):
    def disponibles(self):
        return self.filter(disponible=True).select_related('categoria')

    def por_categoria(self, categoria_nombre):
        return self.filter(
            disponible=True,
            categoria__nombre=categoria_nombre
        ).select_related('categoria')


class Plato(models.Model):
    # ... campos ...
    objects = PlatoManager()
```

Ahora en cualquier vista o comando:

```python
# Limpio, legible, con el contexto de la lógica de negocio
Plato.objects.disponibles()
Plato.objects.por_categoria('Postres')
```

Esta técnica sigue el principio **Fat Model, Thin View**: la lógica compleja vive en el modelo, no en las vistas.

---

## Propiedades calculadas en el modelo

*No todo cálculo sobre los datos de un modelo debe vivir en la vista o en el template. `@property` permite agregar comportamiento al modelo que se calcula en Python, sin necesitar un campo nuevo ni una consulta adicional.*

Un modelo puede tener métodos que comportan como atributos — se calculan en Python, no en la base de datos, y no son campos.

```python
class Plato(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def precio_con_iva(self):
        return self.precio * 1.19

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(",", ".")
```

Se usan como si fueran campos:

```python
plato = Plato.objects.get(id=1)
print(plato.precio_con_iva)     # Calcula en Python
print(plato.precio_formateado)  # "$12.990"
```

> La diferencia con un campo real: `@property` **no se puede usar en `filter()` ni en `order_by()`** porque no existe en la base de datos. Para eso se necesita `annotate()`.

---

## `annotate()`: propiedades calculadas en la base de datos

*Cuando necesitamos un valor calculado que depende de múltiples filas (contar, promediar, sumar), el cálculo debe ocurrir en la base de datos, no en Python. `annotate()` es la herramienta para eso.*

Cuando el cálculo debe poder filtrarse o sortearse, se necesita `annotate()`:

```python
from django.db.models import Count, Avg

# Categorías con conteo de platos
Categoria.objects.annotate(
    total_platos=Count('plato')
).order_by('-total_platos')

# Precio promedio por categoría
Categoria.objects.annotate(
    precio_promedio=Avg('plato__precio')
)
```

`annotate()` añade columnas calculadas al QuerySet. A diferencia de `@property`, estos valores sí pueden usarse en `filter()`, `order_by()` y `values()`.

---

## La migración como artefacto de equipo

*Una migración es un contrato escrito entre el código y la base de datos. En un equipo, ese contrato debe ser compartido, revisado y versionado como cualquier otro archivo del proyecto. Ignorar esto genera los conflictos más difíciles de resolver.*

Hoy la mayoría de los proyectos Django son colaborativos. Las migraciones son el punto donde más frecuentemente surgen problemas de integración.

### Reglas profesionales para migraciones en equipo

**Regla 1:** Las migraciones se commitean junto con el código que las genera. Nunca una sin la otra.

**Regla 2:** No editar migraciones generadas automáticamente a menos que sea estrictamente necesario. Si hay que hacerlo, documentarlo con un comentario.

**Regla 3:** Cuando dos ramas generan migraciones conflictivas con el mismo número:

```bash
python manage.py makemigrations --merge
```

Esto genera una migración de "merge" que reconcilia ambas ramas.

**Regla 4:** Las migraciones de datos (cambiar valores existentes, no esquema) van en archivos separados con `RunPython`:

```python
# migrations/0005_poblar_categorias.py
from django.db import migrations


def poblar_categorias(apps, schema_editor):
    Categoria = apps.get_model('menu', 'Categoria')
    Categoria.objects.create(nombre='Sin categoría', descripcion='Categoría por defecto')


class Migration(migrations.Migration):
    dependencies = [('menu', '0004_categoria')]
    operations = [
        migrations.RunPython(poblar_categorias, migrations.RunPython.noop),
    ]
```

---

## `abstract = True`: herencia de modelos sin tabla propia

*En cualquier sistema hay campos que se repiten en todos los modelos: fecha de creación, quién lo modificó, si está activo. En lugar de copiarlos en cada clase, se definen una vez en un modelo base que no crea tabla propia.*

Django permite crear modelos "base" que no generan tabla en la BD pero sí comparten campos con sus herederos.

```python
class ModeloBase(models.Model):
    creado_en    = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo       = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Plato(ModeloBase):
    nombre = models.CharField(max_length=200)
    # Hereda creado_en, actualizado_en, activo


class Ingrediente(ModeloBase):
    nombre = models.CharField(max_length=100)
    # Hereda creado_en, actualizado_en, activo
```

Este patrón (llamado **Timestamped Model**) es tan común que la librería `django-model-utils` lo ofrece como clase reutilizable. Elimina la necesidad de repetir los campos de auditoría en cada modelo.

---

## Cuándo separar modelos en apps distintas

*La carpeta `models/` resuelve el problema de legibilidad. Pero hay un nivel más profundo: si dos grupos de modelos no se necesitan mutuamente, probablemente no deberían estar en la misma app.*

La estructura de carpeta `models/` resuelve el problema de legibilidad dentro de una app. Pero a veces el problema de arquitectura es más profundo: los modelos no deberían estar en la misma app.

Un criterio práctico:

| Situación | Acción recomendada |
| --------- | ------------------ |
| Modelos que siempre se consultan juntos | Mantener en la misma app |
| Modelos que tienen lógica de negocio independiente | Separar en apps |
| Modelos que podrían reutilizarse en otro proyecto | Separar en app propia |
| App con más de 15 modelos | Evaluar separación |

> **Dato real:** Django mismo está organizado en apps internas: `auth` (usuarios), `contenttypes`, `sessions`, `admin`. Cada una es independiente y puede reemplazarse. Esta arquitectura modular es lo que permitió que el Admin de Django existiera como algo "enchufable" al proyecto.

---

## 30 Preguntas Frecuentes

**1. ¿El `__init__.py` de `models/` puede estar vacío?**
Puede, pero entonces los imports del estilo `from menu.models import Plato` dejarían de funcionar. Debe reexportar todos los modelos que el resto del proyecto necesita.

**2. ¿Qué pasa con las migraciones al pasar de `models.py` a `models/`?**
Las migraciones no cambian. Django genera el mismo SQL sin importar si el modelo viene de un archivo o de un paquete. La refactorización es transparente.

**3. ¿Es obligatorio un archivo por modelo?**
No. Se puede agrupar modelos relacionados en el mismo archivo. Por ejemplo, `menu/models/relaciones.py` con todas las tablas intermedias de ManyToMany.

**4. ¿Los imports relativos funcionan en tests?**
Sí. Los tests usan el mismo sistema de imports de Python.

**5. ¿`verbose_name` afecta la base de datos?**
No. Solo afecta la interfaz de Django (Admin, mensajes de error, formularios).

**6. ¿`ordering` en Meta se puede sobreescribir en un QuerySet?**
Sí. `Plato.objects.all().order_by('precio')` ignora el `ordering` de Meta para esa consulta específica.

**7. ¿Se puede quitar el ordenamiento de Meta temporalmente?**
Sí. `.order_by()` sin argumentos cancela cualquier orden, incluyendo el de Meta.

**8. ¿`CheckConstraint` reemplaza la validación en el modelo?**
No. `CheckConstraint` opera en la BD. La validación del modelo (método `clean()`) opera en Python, antes de guardar. Son complementarias.

**9. ¿Cuántos Managers puede tener un modelo?**
Tantos como sean necesarios. Pero el primero definido en el modelo se convierte en el Manager por defecto.

**10. ¿`@property` se puede serializar con DRF?**
Sí, agregando el nombre de la propiedad a los campos del serializer con `read_only=True`.

**11. ¿`annotate()` trae datos de la BD en una sola consulta?**
Sí. La anotación se calcula en el `SELECT` con funciones SQL (`COUNT`, `AVG`, `SUM`).

**12. ¿Un modelo abstracto puede tener relaciones ForeignKey?**
Sí, pero con cuidado. El modelo relacionado debe existir en el contexto de todos los herederos.

**13. ¿Las constantes de `choices` deben definirse dentro del modelo?**
Por convención sí, como variables de clase. Opcionalmente, con Python 3.11+, se usan `TextChoices` o `IntegerChoices`:
```python
class Estado(models.TextChoices):
    ACTIVO   = 'activo',   'Activo'
    INACTIVO = 'inactivo', 'Inactivo'
```

**14. ¿`RunPython` se puede revertir?**
Solo si se provee la función de reversa como segundo argumento. `migrations.RunPython.noop` acepta la reversa sin hacer nada.

**15. ¿`abstract=True` y `managed=False` son compatibles?**
Sí. Un modelo puede ser abstracto y tener cualquier configuración en Meta, excepto que `abstract=True` hace que `managed` sea irrelevante (no hay tabla).

**16. ¿Un Manager personalizado afecta el Admin?**
Solo si el Admin usa `.objects` directamente. El Admin llama al `default_manager` del modelo.

**17. ¿`indexes` en Meta y `db_index=True` en un campo son equivalentes?**
`db_index=True` agrega un índice simple en ese campo. `indexes` en Meta permite índices compuestos y con nombre.

**18. ¿Cuándo usar `UniqueConstraint` vs `unique=True` en el campo?**
`unique=True` es para un campo individual. `UniqueConstraint` permite unicidad compuesta (combinación de campos) y se puede nombrar.

**19. ¿Los imports relativos dentro de `models/` pueden crear imports circulares?**
Sí, si dos modelos se referencian mutuamente. La solución es usar strings en la ForeignKey: `models.ForeignKey('Categoria', ...)` en lugar de importar la clase.

**20. ¿Las propiedades `@property` se muestran en el Admin?**
No automáticamente. Pero se pueden agregar a `list_display` o `readonly_fields` en el `ModelAdmin`.

**21. ¿`annotate()` y `aggregate()` son lo mismo?**
No. `annotate()` agrega una columna calculada a **cada fila** del QuerySet. `aggregate()` devuelve **un único valor** calculado sobre todo el QuerySet.

**22. ¿Se puede filtrar por una `@property`?**
No. Solo se puede filtrar por campos o anotaciones que existan en la base de datos.

**23. ¿El Manager por defecto siempre se llama `objects`?**
No. Se puede cambiar: `mi_manager = PlatoManager()` y luego usar `Plato.mi_manager.all()`. Pero es una convención muy arraigada llamarlo `objects`.

**24. ¿El paquete `models/` cambia la forma en que se escribe `app_label` en Meta?**
No. `app_label` sigue siendo el nombre de la app, no la ruta completa.

**25. ¿Se puede tener un `models/` bajo múltiples apps?**
Sí. Cada app tiene su propio directorio de modelos independiente.

**26. ¿`RunPython` puede acceder a todos los modelos del proyecto?**
Sí, usando `apps.get_model('app', 'Modelo')`. No se importan directamente para evitar el "congelamiento" de modelos en el momento de la migración.

**27. ¿Las propiedades calculadas con `annotate()` se pueden ordenar?**
Sí. `Categoria.objects.annotate(total=Count('plato')).order_by('-total')`.

**28. ¿`constraints` declaradas en Meta se aplican a todos los motores?**
Depende. `CheckConstraint` no es soportada en todas las versiones de SQLite antiguas. PostgreSQL las soporta completamente.

**29. ¿Qué diferencia hay entre un Manager y un QuerySet personalizado?**
Un Manager puede tener cualquier método. Un QuerySet personalizado permite encadenar métodos (`.disponibles().por_precio(10000)`), lo que es más flexible.

**30. ¿En qué orden se definen los modelos cuando se usan imports circulares con strings?**
No importa. Con `ForeignKey('NombreDelModelo', ...)` Django resuelve la referencia al momento de inicializar la app, no al importar.

---
