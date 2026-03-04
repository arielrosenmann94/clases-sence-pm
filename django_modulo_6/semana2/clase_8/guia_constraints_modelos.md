# Django — Guía de Referencia: Tipos de Campos y Constraints

## Modelos: campos y restricciones completas

---

> _"El modelo es el contrato de la aplicación con sus datos. Cuanto más preciso sea ese contrato, menos bugs aparecen en producción."_

---

## Parámetros comunes a todos los campos

Antes de ver cada tipo, estos parámetros aplican a **cualquier campo**:

| Parámetro            | Tipo       | Efecto                                                                                          |
| -------------------- | ---------- | ----------------------------------------------------------------------------------------------- |
| `null=True`          | bool       | Permite almacenar `NULL` en la base de datos. Para strings se prefiere `blank=True` en su lugar |
| `blank=True`         | bool       | Permite que el campo quede vacío en formularios (validación de Django, no de la DB)             |
| `default=valor`      | cualquiera | Valor por defecto si no se provee uno. Puede ser un valor fijo o una función callable           |
| `unique=True`        | bool       | El valor debe ser único en toda la tabla                                                        |
| `db_index=True`      | bool       | Crea un índice en la base de datos para acelerar búsquedas por ese campo                        |
| `verbose_name='...'` | str        | Nombre legible del campo para el admin y formularios                                            |
| `help_text='...'`    | str        | Texto de ayuda que aparece debajo del campo en formularios                                      |
| `editable=False`     | bool       | Excluye el campo de formularios y del admin                                                     |
| `choices=[...]`      | list       | Lista de tuplas `(valor_db, etiqueta_visible)` para restricted choices                          |
| `validators=[...]`   | list       | Lista de funciones validadoras que se ejecutan antes de guardar                                 |
| `primary_key=True`   | bool       | Convierte el campo en la clave primaria (reemplaza el `id` automático)                          |

---

---

# Parte I — Campos de texto

---

## `CharField`

Texto corto con largo máximo obligatorio.

```python
nombre = models.CharField(
    max_length=150,        # obligatorio — largo máximo en caracteres
    min_length=2,          # solo en formularios (no en DB) — usar validators en el modelo
    blank=True,            # permite vacío en formularios
    default='',            # valor por defecto
    unique=True,           # valor único en la tabla
)
```

**Parámetro exclusivo**: `max_length` (obligatorio).

---

## `TextField`

Texto sin límite de largo. Para descripciones, contenido, notas.

```python
descripcion = models.TextField(
    blank=True,
    default='',
)
```

> No tiene `max_length`. Si se necesita limitar el largo, usar un `validator` personalizado o hacerlo en el formulario.

---

## `EmailField`

Igual que `CharField` pero valida formato de email.

```python
email = models.EmailField(
    max_length=254,        # 254 es el límite estándar de email según RFC
    unique=True,
    blank=True,
)
```

---

## `URLField`

Valida que el texto sea una URL válida.

```python
sitio_web = models.URLField(
    max_length=200,
    blank=True,
)
```

---

## `SlugField`

Solo acepta letras, números, guiones y guiones bajos. Para URLs amigables.

```python
slug = models.SlugField(
    max_length=100,
    unique=True,
    allow_unicode=False,   # True para permitir caracteres Unicode (ej: tildes)
)
```

---

## `UUIDField`

Almacena un UUID (identificador único universal).

```python
import uuid

id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,    # genera un UUID automáticamente — notar que es la función, sin ()
    editable=False,
)
```

---

## `IPAddressField` y `GenericIPAddressField`

```python
ip = models.GenericIPAddressField(
    protocol='both',       # 'IPv4', 'IPv6' o 'both'
    unpack_ipv4=False,     # desempaqueta IPv4 mapeadas a IPv6
    blank=True,
    null=True,
)
```

---

---

# Parte II — Campos numéricos

---

## `IntegerField`

Enteros. Rango: -2.147.483.648 a 2.147.483.647.

```python
cantidad = models.IntegerField(
    default=0,
    null=True,
    blank=True,
)
```

**Variantes**:

| Campo                       | Rango                          |
| --------------------------- | ------------------------------ |
| `SmallIntegerField`         | -32.768 a 32.767               |
| `IntegerField`              | -2.147.483.648 a 2.147.483.647 |
| `BigIntegerField`           | -9.2 × 10¹⁸ a 9.2 × 10¹⁸       |
| `PositiveSmallIntegerField` | 0 a 32.767                     |
| `PositiveIntegerField`      | 0 a 2.147.483.647              |
| `PositiveBigIntegerField`   | 0 a 9.2 × 10¹⁸                 |

---

## `DecimalField`

Números decimales con precisión exacta. Usar para precios y cálculos financieros.

```python
precio = models.DecimalField(
    max_digits=10,         # total de dígitos (incluyendo decimales)
    decimal_places=2,      # dígitos después del punto
    default=0,
    null=True,
    blank=True,
)
```

**Ambos parámetros son obligatorios.**

> No usar `FloatField` para dinero — tiene errores de precisión de punto flotante.

---

## `FloatField`

Números de punto flotante (aproximados). Para coordenadas, medidas, porcentajes.

```python
latitud = models.FloatField(
    null=True,
    blank=True,
)
```

---

---

# Parte III — Campos de fecha y hora

---

## `DateField`

Solo fecha (sin hora).

```python
fecha_nacimiento = models.DateField(
    null=True,
    blank=True,
    auto_now=False,        # True → actualiza al guardar (cada save())
    auto_now_add=False,    # True → se establece solo al crear — luego no cambia
)
```

> `auto_now` y `auto_now_add` son mutuamente excluyentes con `default`.

---

## `TimeField`

Solo hora.

```python
hora_apertura = models.TimeField(
    null=True,
    blank=True,
    auto_now=False,
    auto_now_add=False,
)
```

---

## `DateTimeField`

Fecha y hora combinadas.

```python
creado    = models.DateTimeField(auto_now_add=True)   # solo al crear
modificado = models.DateTimeField(auto_now=True)       # al crear y cada vez que se guarda
```

---

## `DurationField`

Almacena una duración (`timedelta` de Python).

```python
duracion = models.DurationField(
    null=True,
    blank=True,
)
```

---

---

# Parte IV — Campos booleanos

---

## `BooleanField`

```python
activo = models.BooleanField(
    default=True,
)
```

## `NullBooleanField` (deprecado) → usar `BooleanField(null=True)`

```python
confirmado = models.BooleanField(
    null=True,             # permite True, False, o None
    blank=True,
    default=None,
)
```

---

---

# Parte V — Campos de archivo

---

## `FileField`

```python
documento = models.FileField(
    upload_to='documentos/',     # ruta relativa dentro de MEDIA_ROOT
    null=True,
    blank=True,
)
```

`upload_to` puede ser una función que recibe `(instance, filename)` y devuelve la ruta.

---

## `ImageField`

Igual que `FileField` pero valida que el archivo sea una imagen. Requiere la librería `Pillow`.

```python
foto = models.ImageField(
    upload_to='fotos/',
    null=True,
    blank=True,
    width_field='ancho',         # campo donde guardar el ancho automáticamente
    height_field='alto',         # campo donde guardar el alto automáticamente
)
```

---

---

# Parte VI — Campos de relaciones

---

## `ForeignKey` — relación muchos a uno

```python
categoria = models.ForeignKey(
    'Categoria',                 # modelo relacionado (string para evitar imports circulares)
    on_delete=models.CASCADE,    # obligatorio — qué hacer si se borra el objeto relacionado
    related_name='productos',    # nombre para acceder desde el lado inverso
    null=True,
    blank=True,
    db_index=True,               # por defecto True en ForeignKey
)
```

**Opciones de `on_delete`**:

| Opción        | Comportamiento                                        |
| ------------- | ----------------------------------------------------- |
| `CASCADE`     | Borra este objeto si se borra el relacionado          |
| `PROTECT`     | Lanza error si se intenta borrar el relacionado       |
| `SET_NULL`    | Pone `null` en este campo (requiere `null=True`)      |
| `SET_DEFAULT` | Asigna el valor `default` (requiere `default=...`)    |
| `DO_NOTHING`  | No hace nada — puede romper la integridad referencial |

---

## `ManyToManyField` — relación muchos a muchos

```python
etiquetas = models.ManyToManyField(
    'Etiqueta',
    blank=True,
    related_name='productos',
    through='ProductoEtiqueta',  # modelo intermedio personalizado (opcional)
)
```

---

## `OneToOneField` — relación uno a uno

```python
perfil = models.OneToOneField(
    'auth.User',
    on_delete=models.CASCADE,
    related_name='perfil',
)
```

---

---

# Parte VII — Constraints a nivel modelo (class Meta)

---

Los constraints definidos en `class Meta` aplican restricciones a nivel de base de datos — más robustos que las validaciones de formulario.

```python
class Producto(models.Model):
    nombre   = models.CharField(max_length=120)
    sku      = models.CharField(max_length=30)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    precio   = models.DecimalField(max_digits=10, decimal_places=2)
    stock    = models.PositiveIntegerField(default=0)

    class Meta:
        # Unicidad combinada de varios campos
        unique_together = [['nombre', 'categoria']]

        # Índices para acelerar búsquedas
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria', 'precio']),
        ]

        # Constraints con condiciones (Django 2.2+)
        constraints = [
            # El precio debe ser mayor a cero
            models.CheckConstraint(
                check=models.Q(precio__gt=0),
                name='precio_positivo'
            ),
            # El stock no puede ser negativo
            models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='stock_no_negativo'
            ),
            # SKU único dentro de cada categoría
            models.UniqueConstraint(
                fields=['sku', 'categoria'],
                name='sku_unico_por_categoria'
            ),
        ]

        # Orden por defecto en queries
        ordering = ['-creado']

        # Nombre de la tabla en la DB (opcional)
        db_table = 'tienda_productos'

        # Nombre legible en el admin
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
```

---

## Validators personalizados

Para restricciones que no existen en Django, se crean validators:

```python
from django.core.exceptions import ValidationError

def solo_mayores_de_edad(valor):
    from datetime import date
    hoy = date.today()
    edad = hoy.year - valor.year - ((hoy.month, hoy.day) < (valor.month, valor.day))
    if edad < 18:
        raise ValidationError('El usuario debe ser mayor de 18 años.')

class Perfil(models.Model):
    fecha_nacimiento = models.DateField(
        validators=[solo_mayores_de_edad]
    )
```

---

---

# Referencia rápida — tabla resumen

---

| Campo                  | Parámetros clave                              | Cuándo usarlo                             |
| ---------------------- | --------------------------------------------- | ----------------------------------------- |
| `CharField`            | `max_length` (oblig.)                         | Texto corto                               |
| `TextField`            | —                                             | Texto largo sin límite                    |
| `EmailField`           | `max_length`                                  | Correos — valida formato                  |
| `URLField`             | `max_length`                                  | URLs — valida formato                     |
| `SlugField`            | `max_length`, `allow_unicode`                 | URLs amigables                            |
| `UUIDField`            | `default=uuid.uuid4`                          | IDs únicos distribuidos                   |
| `IntegerField`         | —                                             | Enteros generales                         |
| `PositiveIntegerField` | —                                             | Solo valores >= 0                         |
| `DecimalField`         | `max_digits`, `decimal_places` (ambos oblig.) | Precios, finanzas                         |
| `FloatField`           | —                                             | Valores aproximados: coordenadas, medidas |
| `DateField`            | `auto_now`, `auto_now_add`                    | Solo fechas                               |
| `DateTimeField`        | `auto_now`, `auto_now_add`                    | Fecha y hora                              |
| `DurationField`        | —                                             | Duraciones (`timedelta`)                  |
| `BooleanField`         | `default`, `null`                             | Verdadero/falso                           |
| `FileField`            | `upload_to`                                   | Archivos genéricos                        |
| `ImageField`           | `upload_to`                                   | Imágenes (requiere Pillow)                |
| `ForeignKey`           | `on_delete` (oblig.)                          | Relación N→1                              |
| `ManyToManyField`      | `through`                                     | Relación N→N                              |
| `OneToOneField`        | `on_delete` (oblig.)                          | Relación 1→1                              |

---

> Cada constraint en el modelo es una regla que la base de datos hace cumplir siempre, independientemente del código que inserte datos. Eso es más seguro que cualquier validación en la vista.

---

---

# Parte VIII — Mensajes de error automáticos de Django

---

Cuando un campo falla la validación, Django muestra un mensaje de error predeterminado. Estos son los mensajes por campo — aparecen debajo del input en el formulario:

---

## Errores comunes a todos los campos

| Situación                      | Mensaje automático                |
| ------------------------------ | --------------------------------- |
| Campo obligatorio vacío        | `"Este campo es obligatorio."`    |
| Valor nulo donde no se permite | `"Este campo no puede ser nulo."` |

---

## Campos de texto

| Campo                   | Error                    | Mensaje automático                                                                        |
| ----------------------- | ------------------------ | ----------------------------------------------------------------------------------------- |
| `CharField`             | Supera `max_length`      | `"Asegúrese de que este valor tenga como máximo 100 caracteres (actualmente tiene 120)."` |
| `CharField`             | Menor que `min_length`   | `"Asegúrese de que este valor tenga al menos 3 caracteres (actualmente tiene 1)."`        |
| `EmailField`            | Formato inválido         | `"Introduzca una dirección de correo electrónico válida."`                                |
| `URLField`              | Formato inválido         | `"Introduzca una URL válida."`                                                            |
| `SlugField`             | Caracteres no permitidos | `"Introduzca un valor válido consistente en letras, números, guiones bajos o guiones."`   |
| `UUIDField`             | Formato inválido         | `"Introduzca un UUID válido."`                                                            |
| `GenericIPAddressField` | IP inválida              | `"Introduzca una dirección IPv4 o IPv6 válida."`                                          |

---

## Campos numéricos

| Campo          | Error                | Mensaje automático                                                 |
| -------------- | -------------------- | ------------------------------------------------------------------ |
| `IntegerField` | No es un número      | `"Introduzca un número entero."`                                   |
| `IntegerField` | Fuera de rango       | `"Asegúrese de que este valor sea mayor o igual que -2147483648."` |
| `DecimalField` | No es número         | `"Introduzca un número."`                                          |
| `DecimalField` | Demasiados dígitos   | `"Asegúrese de que haya no más de 10 dígitos en total."`           |
| `DecimalField` | Demasiados decimales | `"Asegúrese de que no haya más de 2 decimales."`                   |
| `FloatField`   | No es número         | `"Introduzca un número."`                                          |

---

## Campos de fecha y hora

| Campo           | Error            | Mensaje automático                    |
| --------------- | ---------------- | ------------------------------------- |
| `DateField`     | Formato inválido | `"Introduzca una fecha válida."`      |
| `TimeField`     | Formato inválido | `"Introduzca una hora válida."`       |
| `DateTimeField` | Formato inválido | `"Introduzca una fecha/hora válida."` |

---

## Campos de selección y archivos

| Campo         | Error               | Mensaje automático                                                              |
| ------------- | ------------------- | ------------------------------------------------------------------------------- |
| `ChoiceField` | Opción no existente | `"Seleccione una opción válida. X no es una de las opciones disponibles."`      |
| `FileField`   | Sin archivo         | `"No se ha subido ningún archivo."`                                             |
| `ImageField`  | No es imagen        | `"Suba una imagen válida. El archivo subido no es una imagen o está corrupto."` |

---

## Errores de unicidad (a nivel DB)

| Situación                 | Mensaje automático                                  |
| ------------------------- | --------------------------------------------------- |
| `unique=True` violado     | `"Ya existe Producto con este Nombre."`             |
| `unique_together` violado | `"Producto con este Nombre y Categoría ya existe."` |

---

## Cómo personalizar los mensajes

Todos los mensajes se pueden reemplazar con el parámetro `error_messages` en el campo del formulario:

```python
class ProductoForm(forms.ModelForm):
    class Meta:
        model  = Producto
        fields = ['nombre', 'precio', 'email']

    nombre = forms.CharField(
        max_length=120,
        error_messages={
            'required':   'El nombre del producto es obligatorio.',
            'max_length': 'El nombre no puede superar los 120 caracteres.',
        }
    )

    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        error_messages={
            'required': 'Debe ingresar un precio.',
            'invalid':  'Ingrese un número válido. Ejemplo: 19.99',
        }
    )
```

Las claves de `error_messages` corresponden al nombre del tipo de error. Los más comunes son:

| Clave                | Cuándo se usa                           |
| -------------------- | --------------------------------------- |
| `required`           | Campo vacío y obligatorio               |
| `max_length`         | Supera el largo máximo                  |
| `min_length`         | Menor al largo mínimo                   |
| `invalid`            | Formato incorrecto (email, URL, número) |
| `invalid_choice`     | Opción no válida en choices             |
| `max_value`          | Supera el valor máximo                  |
| `min_value`          | Menor al valor mínimo                   |
| `max_digits`         | Demasiados dígitos en decimal           |
| `max_decimal_places` | Demasiados decimales                    |

---

> Conocer los mensajes por defecto ayuda a decidir cuáles vale la pena personalizar. En interfaces para usuarios finales, siempre personalizar `required` e `invalid` — los mensajes de Django por defecto son técnicos para usuarios no técnicos.

---
