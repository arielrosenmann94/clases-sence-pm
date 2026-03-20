# 🔍 Módulo 7 — Clase 8

## Consultas Personalizadas con el ORM y SQL en Django

> **AE 7.5** — Realizar consultas de filtrado de datos y consultas personalizadas utilizando el ORM y sentencias SQL para recuperación de información de la base de datos acorde al framework Django dando solución a un problema.

---

## 🗺️ Índice

| #     | Herramienta           | Para qué sirve                                                                               |
| :---- | :-------------------- | :------------------------------------------------------------------------------------------- |
| **1** | Recap                 | Mapa de lo que se verá hoy y conexión con clases anteriores                                  |
| **2** | `F()`                 | Comparar dos campos del mismo modelo dentro de una consulta, sin traer datos a Python        |
| **3** | `Q()`                 | Escribir condiciones con OR o NOT en los filtros, algo que `filter()` solo no puede hacer    |
| **4** | `annotate()`          | Agregar una columna calculada a cada fila del resultado, como contar pedidos por cliente     |
| **5** | `aggregate()`         | Obtener un único número de toda la tabla, como el total de ventas o el promedio de edad      |
| **6** | `raw()`               | Escribir SQL propio que devuelve objetos del modelo, cuando el ORM no alcanza                |
| **7** | `connection.cursor()` | Ejecutar cualquier SQL sin restricciones del ORM: INSERT, UPDATE, funciones de base de datos |

---

---

# 📚 1. Recap: Lo que viene hoy

---

Esta clase completa y profundiza los temas del AE 7.5. Lo que ya vimos en clases anteriores no se repite, pero aquí vas a entender cómo usar estas herramientas para **resolver problemas reales**.

| Lo que viene hoy        | Ejemplo de problema real que resuelve                                 |
| :---------------------- | :-------------------------------------------------------------------- |
| `F()` comparando campos | Filtrar registros donde un campo supera a otro campo del mismo modelo |
| `Q()` con lógica OR/NOT | Buscar algo en nombre O en email al mismo tiempo                      |
| `annotate()`            | "Mostrar cuántos pedidos tiene CADA cliente"                          |
| `aggregate()`           | "¿Cuál es el total de ventas del mes?"                                |
| `raw()`                 | Escribir SQL propio cuando el ORM no es suficiente                    |
| `cursor()`              | SQL sin ninguna restricción de Django                                 |

---

---

# 📊 2. Comparación entre Campos con `F()`

---

## El problema que resuelve

Imagina que tienes un modelo con dos campos numéricos:  
`campo_a` y `campo_b`.

¿Cómo filtras los registros donde `campo_a > campo_b`?  
Con un `filter` normal **no puedes**, porque filter solo compara con valores fijos, no con otros campos del mismo modelo.

**`F()` resuelve esto.** Le dice a Django: _"compara este campo con el valor de OTRO campo del mismo modelo, sin traer nada a Python"_.

---

## Sintaxis

```python
from django.db.models import F

# Registros donde campo_a es mayor que campo_b
MiModelo.objects.filter(campo_a__gt=F('campo_b'))

# Registros donde campo_a es el doble de campo_b
MiModelo.objects.filter(campo_a__gte=F('campo_b') * 2)

# También sirve para actualizar masivamente
MiModelo.objects.update(campo_a=F('campo_a') + 1)
# ↑ suma 1 a campo_a en TODOS los registros, en un solo SQL
```

---

## ¿Por qué es importante?

```
Sin F()
──────────────────────────────────────
1. Django trae TODOS los registros a Python
2. Python los recorre uno por uno y compara
3. Con 100.000 registros = 100.000 objetos en RAM

Con F()
──────────────────────────────────────
1. Django genera un SQL con la comparación
2. La base de datos la resuelve internamente
3. A Python llegan solo los resultados ya filtrados

→ Menos memoria, menos tiempo, más escalable
```

> 💡 **Regla:** Si necesitas comparar un campo con **otro campo** → `F()`. Si comparas con un **valor fijo** (ej: `edad > 30`) → filter normal.

> 📚 **Fuente:** Django Software Foundation. (2024). _Query Expressions — F()_. https://docs.djangoproject.com/en/stable/ref/models/expressions/#f-expressions

---

---

# 🔎 3. Consultas Compuestas con `Q()`

---

## El problema que resuelve

Con `filter()` todas las condiciones se combinan con **AND**.  
Pero a veces necesitas **OR** (o esto, o aquello) o **NOT** (que no sea esto).

Por ejemplo:  
_"Quiero los registros donde campo_a sea 1 **OR** campo_b sea 2"_  
→ Con filter encadenado esto no es posible. `Q()` lo resuelve.

---

## Sintaxis y operadores

```python
from django.db.models import Q

# OR: uno u otro
MiModelo.objects.filter(
    (Q(campo_a=1) | Q(campo_b=2))
)

# AND explícito: los dos a la vez
MiModelo.objects.filter(
    Q(campo_a=1) & Q(campo_b=2)
)

# NOT: que no cumpla la condición
MiModelo.objects.filter(
    ~Q(campo_a=1)
)

# Combinación: (AND + OR)
MiModelo.objects.filter(
    Q(campo_a=1) | Q(campo_b=2),
    campo_c=True  # esto es un AND extra al resultado anterior
)
```

---

## Tabla de operadores

| Operador | Símbolo | Significado                  |
| :------- | :------ | :--------------------------- |
| OR       | `\|`    | Al menos uno de los dos      |
| AND      | `&`     | Los dos a la vez             |
| NOT      | `~`     | Lo contrario de la condición |

---

## Ejemplo: filtros que se arman dinámicamente

```python
from django.db.models import Q

filtro = Q()  # Q vacío = sin filtro (trae todo)

if busqueda:
    filtro &= Q(nombre__icontains=busqueda) | Q(email__icontains=busqueda)

if solo_activos:
    filtro &= Q(activo=True)

resultados = MiModelo.objects.filter(filtro)
```

> Construir un `Q()` vacío y agregarle condiciones dinámicamente es el patrón estándar para buscadores y filtros en Django.

> 📚 **Fuente:** Django Software Foundation. (2024). _Complex lookups with Q objects_. https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects

---

---

# 📈 4. `annotate()` — Un Valor Calculado por Cada Fila

---

## El problema que resuelve

Imagina que tienes un modelo `Cliente` y un modelo `Pedido` relacionado.  
Quieres mostrar una lista de clientes **y al lado cuántos pedidos tiene cada uno**.

No puedes hacer eso con un filter. Necesitas `annotate()`.

---

## ¿Qué hace `annotate()`?

Agrega una **columna extra calculada** a cada objeto del QuerySet. Es como añadir una columna virtual que no existe en la base de datos pero se calcula al vuelo.

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Agrega una columna "total_pedidos" a cada cliente
clientes = Cliente.objects.annotate(
    total_pedidos=Count('pedidos')
)

# Ahora cada cliente tiene el atributo .total_pedidos
for c in clientes:
    print(f"{c.nombre}: {c.total_pedidos} pedidos")
```

---

## Funciones disponibles

| Función          | ¿Qué calcula?                             |
| :--------------- | :---------------------------------------- |
| `Count('campo')` | Cuenta cuántos registros relacionados hay |
| `Sum('campo')`   | Suma los valores                          |
| `Avg('campo')`   | Calcula el promedio                       |
| `Max('campo')`   | Trae el valor más alto                    |
| `Min('campo')`   | Trae el valor más bajo                    |

---

## Combinaciones útiles

```python
from django.db.models import Count, Sum

# Los 5 clientes con más pedidos
top = Cliente.objects.annotate(
    total_pedidos=Count('pedidos')
).order_by('-total_pedidos')[:5]

# Clientes con al menos 1 pedido (filter después de annotate)
con_pedidos = Cliente.objects.annotate(
    total_pedidos=Count('pedidos')
).filter(total_pedidos__gt=0)
```

> 💡 `annotate()` devuelve un **QuerySet** — se puede encadenar con `filter()`, `order_by()`, `[:5]`, etc.

> 📚 **Fuente:** Django Software Foundation. (2024). _Aggregation — annotate()_. https://docs.djangoproject.com/en/stable/topics/db/aggregation/

---

---

# 📊 5. `aggregate()` — Un Valor Global de Toda la Tabla

---

## La diferencia con `annotate()`

```
annotate()   →  una cifra POR CADA fila    →  retorna un QuerySet
aggregate()  →  una cifra DE TODA la tabla →  retorna un diccionario
```

```python
from django.db.models import Count, Avg, Sum, Max, Min

# ¿Cuántos clientes hay en total?
Cliente.objects.aggregate(total=Count('id'))
# → {'total': 150}

# ¿Cuál es el promedio de edad?
Cliente.objects.aggregate(promedio=Avg('edad'))
# → {'promedio': 32.5}

# ¿Cuánto se facturó en total?
Pedido.objects.aggregate(ventas=Sum('total'))
# → {'ventas': Decimal('45230.00')}

# Múltiples cálculos a la vez
Pedido.objects.aggregate(
    ventas=Sum('total'),
    maximo=Max('total'),
    minimo=Min('total'),
)
# → {'ventas': ..., 'maximo': ..., 'minimo': ...}
```

---

## ¿Cuándo usar cada uno?

| Pregunta                                 | Herramienta   |
| :--------------------------------------- | :------------ |
| ¿Cuántos pedidos tiene **cada** cliente? | `annotate()`  |
| ¿Cuántos pedidos hay **en total**?       | `aggregate()` |
| ¿Cuál es el gasto **de cada** cliente?   | `annotate()`  |
| ¿Cuál es el total facturado **del mes**? | `aggregate()` |

> 📚 **Fuente:** Django Software Foundation. (2024). _Aggregation_. https://docs.djangoproject.com/en/stable/topics/db/aggregation/

---

---

# 🗄️ 6. SQL Personalizado con `raw()`

---

## ¿Cuándo usar `raw()`?

Cuando el ORM de Django no puede generar la consulta que necesitas —  
o cuando ya tienes el SQL escrito y sabes que funciona —  
usas `raw()` para ejecutarlo directamente.

**`raw()` ejecuta SQL y devuelve objetos del modelo**, igual que un QuerySet normal.

---

## Sintaxis

```python
# raw() siempre recibe el SQL como string
resultados = MiModelo.objects.raw("SELECT * FROM mi_tabla WHERE activo = true")

for obj in resultados:
    print(obj.nombre)  # accedes a los campos como atributos normales
```

---

## ⚠️ Seguridad: NUNCA concatenes variables en el SQL

```python
# ✅ CORRECTO — usa parámetros con %s
nombre_buscado = "Ana"
resultados = MiModelo.objects.raw(
    "SELECT * FROM mi_tabla WHERE nombre = %s",
    [nombre_buscado]
)

# ❌ PELIGROSO — vulnerable a inyección SQL
resultados = MiModelo.objects.raw(
    f"SELECT * FROM mi_tabla WHERE nombre = '{nombre_buscado}'"
)
```

> ⚠️ **La inyección SQL** ocurre cuando un usuario malintencionado mete código SQL dentro de un dato. Si concatenas, el atacante puede manipular la consulta entera. Con `%s` y la lista de parámetros, Django escapa los valores automáticamente.

> 📚 **Fuente:** Django Software Foundation. (2024). _Performing raw SQL queries — raw()_. https://docs.djangoproject.com/en/stable/topics/db/sql/#performing-raw-queries

---

---

# 🖱️ 7. SQL de Control Total con `connection.cursor()`

---

## ¿Cuándo usar `cursor()` en vez de `raw()`?

| `raw()`                            | `connection.cursor()`                                 |
| :--------------------------------- | :---------------------------------------------------- |
| Devuelve objetos del modelo        | Devuelve filas crudas (tuplas)                        |
| Necesita un modelo base            | No necesita ningún modelo                             |
| Para SELECT que mapean a un modelo | Para cualquier SQL: INSERT, UPDATE, DELETE, funciones |
| Más cómodo de usar                 | Más control, más flexible                             |

---

## Sintaxis con `with` (recomendada)

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT nombre, email FROM mi_tabla WHERE activo = %s", [True])
    filas = cursor.fetchall()
    # filas = [(nombre1, email1), (nombre2, email2), ...]

for nombre, email in filas:
    print(nombre, email)
```

El `with` garantiza que el cursor se cierra correctamente aunque ocurra un error.

---

## Métodos para obtener los resultados

| Método                | Devuelve                             |
| :-------------------- | :----------------------------------- |
| `cursor.fetchone()`   | Una sola fila (o `None` si no hay)   |
| `cursor.fetchall()`   | Todas las filas como lista de tuplas |
| `cursor.fetchmany(n)` | Las próximas N filas                 |

---

## Convertir filas a diccionarios

Por defecto `cursor` devuelve tuplas. Para obtener diccionarios con nombres de columna:

```python
with connection.cursor() as cursor:
    cursor.execute("SELECT nombre, email FROM mi_tabla")
    columnas = [col[0] for col in cursor.description]
    filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

# filas = [{'nombre': ..., 'email': ...}, ...]
```

> 💡 `cursor.description` contiene los metadatos de cada columna del resultado, incluyendo el nombre.

---

## ⚠️ Seguridad: misma regla que `raw()`

```python
# ✅ Siempre con parámetros
cursor.execute("SELECT * FROM mi_tabla WHERE id = %s", [el_id])

# ❌ Nunca con f-strings o concatenación
cursor.execute(f"SELECT * FROM mi_tabla WHERE id = {el_id}")
```

> 📚 **Fuente:** Django Software Foundation. (2024). _Executing custom SQL directly_. https://docs.djangoproject.com/en/stable/topics/db/sql/#executing-custom-sql-directly

---

---

# 🐛 Práctica: Debugging en Django

---

## Repositorio de la práctica

```
arielrosenmann94/bugs
```

🔗 https://github.com/arielrosenmann94/bugs

Esta práctica consiste en **encontrar y corregir errores** en un proyecto Django que utiliza los conceptos vistos en esta clase. El proyecto tiene bugs intencionales que deberás identificar y solucionar.

> 📖 **Las instrucciones completas, los pasos a seguir y los criterios de evaluación están en el README del repositorio.** Léanlo con atención antes de comenzar.

---

# 🏁 Resumen

---

| Herramienta           | Cuándo usarla                                              | Retorna         |
| :-------------------- | :--------------------------------------------------------- | :-------------- |
| `F()`                 | Comparar un campo con **otro campo** del mismo modelo      | QuerySet        |
| `Q()`                 | Condiciones con **OR** o **NOT**                           | QuerySet        |
| `annotate()`          | Un valor calculado **por cada fila**                       | QuerySet        |
| `aggregate()`         | Un valor calculado **sobre toda la tabla**                 | Diccionario     |
| `raw()`               | SQL propio que necesita devolver **objetos del modelo**    | RawQuerySet     |
| `connection.cursor()` | SQL propio con **control total**, sin limitaciones del ORM | Tuplas / cursor |

---

## 📚 Referencias (APA 7ª ed.)

Django Software Foundation. (2024). _Query Expressions (F, Q)_. https://docs.djangoproject.com/en/stable/ref/models/expressions/

Django Software Foundation. (2024). _Complex lookups with Q objects_. https://docs.djangoproject.com/en/stable/topics/db/queries/#complex-lookups-with-q-objects

Django Software Foundation. (2024). _Aggregation_. https://docs.djangoproject.com/en/stable/topics/db/aggregation/

Django Software Foundation. (2024). _Performing raw SQL queries_. https://docs.djangoproject.com/en/stable/topics/db/sql/




