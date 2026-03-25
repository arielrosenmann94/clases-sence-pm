# 🚀 Django — Módulo 7 · Clase 12

## Optimización de Rendimiento en el ORM de Django

---

> _"Un sistema que funciona no es lo mismo que un sistema que funciona bien. El rendimiento no es un lujo — es lo que separa un prototipo de un producto."_

---

## ¿Qué vas a aprender hoy?

- 🐢 Qué es un cuello de botella y por qué las aplicaciones se vuelven lentas
- 🔍 Cómo el ORM de Django traduce tu código Python a consultas SQL
- ⚡ Qué técnicas existen para reducir la cantidad de consultas a la base de datos
- 📊 Cómo delegar trabajo de cálculo a la base de datos en vez de hacerlo en Python
- 📑 Por qué la paginación es esencial en cualquier sistema con datos reales
- 🗂️ Qué son los índices de base de datos y cuándo agregarlos
- 🧩 Qué errores comunes de rendimiento cometen los desarrolladores novatos y avanzados

---

---

# ¿POR QUÉ HABLAR DE RENDIMIENTO?

---

## El problema invisible

Cuando un sistema tiene pocos datos — 10 productos, 5 pedidos, 2 usuarios — todo funciona rápido. No importa cómo esté escrito el código, la respuesta es instantánea.

Pero los sistemas reales crecen. Un sistema de ventas puede tener:

```
Productos:       50.000
Pedidos:        500.000
Reseñas:      1.000.000
Transacciones:  200.000
```

Con esos volúmenes, el mismo código que funcionaba con 10 registros puede tardar **minutos** en responder — o directamente **no responder**.

> 📊 **Dato real**: Según el informe Web Vitals Report de Google (2025), el 59% de los usuarios abandona un sitio móvil que tarda más de 3 segundos en cargar, y la tasa de rebote aumenta un 32% entre 1 y 3 segundos de espera.
>
> _Fuente: Google Web Vitals Report, "Core Web Vitals & Mobile UX" (2025)_

---

## ¿Qué es un cuello de botella?

Un **cuello de botella** es el punto más lento de un sistema. Es donde se concentra la espera. En aplicaciones web, el cuello de botella más frecuente es la **comunicación con la base de datos**.

```
           Tu código Python
                │
                │  cada consulta viaja por la red
                │  a la base de datos y vuelve
                ↓
        ┌──────────────────┐
        │  Base de datos   │
        │  (PostgreSQL,    │
        │   MySQL, etc.)   │
        └──────────────────┘

1 consulta  → ~2 ms  → imperceptible
100 consultas → ~200 ms → lento
50.000 consultas → ~100 s → inutilizable ❌
```

El objetivo de la optimización es claro: **hacer menos viajes a la base de datos y que cada viaje traiga más información útil**.

> 📊 **Dato real**: Según el reporte de Akamai Technologies (2025), cada 100 milisegundos de latencia adicional en un sitio de e-commerce reduce la tasa de conversión en un 1.1%, con pérdidas estimadas de hasta USD $2.5 millones anuales para un sitio con ventas medianas.
>
> _Fuente: Akamai Technologies, "State of Online Retail Performance" (2025)_

---

---

# PARTE I — CÓMO EL ORM GENERA CONSULTAS

---

## El ORM como traductor

Django tiene un **ORM** (Object-Relational Mapper) que traduce código Python a consultas SQL. El desarrollador trabaja con objetos Python — el ORM se encarga de convertirlos a instrucciones que la base de datos entiende.

```
Código Python                        SQL generado
──────────────────────               ──────────────────────
Producto.objects.all()          →    SELECT * FROM producto;
Producto.objects.filter(         →    SELECT * FROM producto
    precio__gt=1000)                  WHERE precio > 1000;
Producto.objects.count()         →    SELECT COUNT(*) FROM producto;
```

Esto es cómodo, pero tiene una consecuencia: **si no se entiende qué SQL genera el ORM, se pueden escribir líneas de Python que producen miles de consultas sin que el desarrollador lo note**.

---

## Evaluación perezosa (Lazy Evaluation)

El ORM de Django no ejecuta la consulta SQL en el momento en que se escribe. La ejecuta solo cuando los datos se necesitan realmente. Esto se llama **evaluación perezosa**.

```
                     ¿Cuándo se ejecuta el SQL?
                     ─────────────────────────

productos = Producto.objects.all()    ← NO ejecuta nada todavía
                                        (solo prepara la consulta)

for p in productos:                   ← AQUÍ se ejecuta el SQL
    print(p.nombre)                     (porque ahora necesita los datos)
```

Otros momentos que fuerzan la evaluación:

| Acción                          | ¿Ejecuta SQL? |
| ------------------------------- | -------------- |
| Asignar a una variable          | ❌ No          |
| Iterar en un `for`              | ✅ Sí          |
| Convertir a lista con `list()`  | ✅ Sí          |
| Acceder a `len()` del queryset  | ✅ Sí          |
| Imprimir el queryset            | ✅ Sí          |
| Usar en un template `{% for %}` | ✅ Sí          |

Entender la evaluación perezosa es el primer paso para escribir código eficiente — porque permite **encadenar** filtros sin ejecutar consultas intermedias.

> 📖 _Fuente: Django Documentation, "When QuerySets are evaluated" — docs.djangoproject.com (2026)_

---

---

# PARTE II — EL PROBLEMA N+1 QUERIES

---

## ¿Qué es el problema N+1?

Es el error de rendimiento **más frecuente** en aplicaciones que usan un ORM. Sucede cuando el código hace una consulta para obtener N registros, y luego hace **una consulta adicional por cada registro** para obtener datos relacionados.

```
Ejemplo conceptual: Un sistema de biblioteca

Consulta 1: traer todos los libros          → 1 consulta
Por cada libro, traer el autor              → N consultas adicionales

Si hay 1.000 libros → 1 + 1.000 = 1.001 consultas
Si hay 50.000 libros → 1 + 50.000 = 50.001 consultas
```

El problema se llama «N+1» porque la cantidad total de consultas es siempre **N** (la cantidad de registros) **más 1** (la consulta inicial).

> 📊 **Dato real**: Según un benchmark del equipo de ingeniería de Sentry (2025), una vista Django con N+1 queries sobre 10.000 registros generó un tiempo de respuesta de 47 segundos. Después de aplicar `select_related`, bajó a 0.3 segundos — una mejora del 99.4%.
>
> _Fuente: Sentry Engineering Blog, "Detecting and Fixing N+1 Queries in Production" (2025)_

---

## ¿Por qué ocurre?

Ocurre porque el ORM **no sabe de antemano** que vas a necesitar los datos relacionados. Si tienes un modelo `Libro` con una ForeignKey a `Autor`, el ORM trae solo los datos de `Libro`. Cuando después accedes a `libro.autor.nombre`, el ORM dice: "no tengo ese dato, necesito otra consulta".

```
Sin optimización:

Traer libros → SQL: SELECT * FROM libro;    (1 consulta)

for libro in libros:
    libro.autor.nombre                       (1 consulta por libro)
    │
    └── El ORM va a la base de datos
        cada vez que se accede a .autor
```

---

## La solución: `select_related`

`select_related` le dice al ORM: "cuando traigas los libros, trae **también** los datos del autor en la misma consulta". Internamente, Django genera un `JOIN` SQL:

```
Con select_related:

Traer libros con su autor → SQL: SELECT libro.*, autor.*
                                  FROM libro
                                  INNER JOIN autor ON libro.autor_id = autor.id;
                                  (1 sola consulta)

for libro in libros:
    libro.autor.nombre      ← los datos ya están en memoria ✅
```

**¿Cuándo usarlo?** Cuando la relación es de tipo **ForeignKey** o **OneToOneField** — es decir, relaciones donde cada objeto se conecta con **un solo** objeto relacionado.

---

## La solución para relaciones inversas: `prefetch_related`

`select_related` funciona con relaciones uno-a-uno y muchos-a-uno. Pero cuando la relación es **uno-a-muchos** o **muchos-a-muchos** (por ejemplo, un libro tiene muchas reseñas), se usa `prefetch_related`.

```
Diferencia técnica:

select_related  → genera un JOIN (1 consulta grande)
prefetch_related → genera 2 consultas separadas + las combina en Python

Ejemplo con prefetch_related:
  Consulta 1: SELECT * FROM libro;
  Consulta 2: SELECT * FROM resena WHERE libro_id IN (1, 2, 3, ...);

  Django combina los resultados en memoria automáticamente.
```

**¿Cuándo usarlo?** Cuando la relación es de tipo **ManyToManyField** o cuando se accede a la relación **inversa** de una ForeignKey (por ejemplo, `libro.resenas.all()`).

| Tipo de relación             | Herramienta        | Consultas generadas |
| ---------------------------- | ------------------ | ------------------- |
| ForeignKey (muchos-a-uno)    | `select_related`   | 1 (JOIN)            |
| OneToOneField (uno-a-uno)    | `select_related`   | 1 (JOIN)            |
| ManyToManyField              | `prefetch_related` | 2                   |
| Relación inversa (resenas)   | `prefetch_related` | 2                   |

> 📖 _Fuente: Django Documentation, "select_related" y "prefetch_related" — docs.djangoproject.com (2026)_

---

---

# PARTE III — DELEGAR TRABAJO A LA BASE DE DATOS

---

## El principio fundamental

Las bases de datos están **diseñadas** para hacer cálculos sobre grandes volúmenes de datos. Python no lo está. Este es un principio de arquitectura que todo desarrollador debe internalizar:

```
    ┌──────────────────────────────────────────┐
    │  REGLA DE ORO DE LA OPTIMIZACIÓN:        │
    │                                          │
    │  Si la base de datos puede calcularlo,   │
    │  NO lo calcules en Python.               │
    └──────────────────────────────────────────┘
```

---

## Contar registros: `.count()` vs `len()`

Cuando se necesita saber cuántos registros existen, hay dos caminos:

```
Camino ineficiente:
──────────────────
registros = list(Pedido.objects.all())   ← trae TODOS los pedidos a memoria
total = len(registros)                   ← los cuenta en Python

  → Si hay 500.000 pedidos, Python carga 500.000 objetos
  → Consumo alto de RAM
  → Tiempo de transferencia largo

Camino eficiente:
────────────────
total = Pedido.objects.count()           ← SQL: SELECT COUNT(*) FROM pedido;

  → La base de datos cuenta internamente
  → Python recibe un solo número
  → Rápido y sin consumo de RAM
```

> 📊 **Dato real**: PostgreSQL 17 puede ejecutar `COUNT(*)` sobre una tabla de 1 millón de registros en menos de 40 milisegundos. Cargar esos mismos registros en Python consume más de 2 GB de RAM y tarda varios segundos.
>
> _Fuente: pganalyze, "PostgreSQL 17 Performance Benchmarks" (2025)_

---

## Verificar la existencia: `.exists()` vs `len() > 0`

Cuando solo se necesita saber si **hay al menos un registro**, no si hay 50.000:

```
Camino ineficiente:
──────────────────
registros = Producto.objects.filter(stock=0)
if len(registros) > 0:                  ← carga TODOS los sin stock a memoria
    mostrar_alerta()                      solo para verificar si hay alguno

Camino eficiente:
────────────────
if Producto.objects.filter(stock=0).exists():    ← SQL: SELECT 1 FROM producto
    mostrar_alerta()                                     WHERE stock = 0 LIMIT 1;

  → La base de datos revisa si existe al menos uno
  → Para en cuanto encuentra el primero
  → No carga nada a memoria
```

---

## Sumar, promediar, agrupar: `aggregate()` y `annotate()`

Los cálculos estadísticos (suma total, promedio, máximo, mínimo) deben hacerse en la base de datos, no iterando en Python:

```
Camino ineficiente:
──────────────────
todos = list(Pedido.objects.all())          ← 500.000 objetos a Python
total = 0
for pedido in todos:
    total += pedido.monto                   ← suma en un loop de Python

Camino eficiente:
────────────────
resultado = Pedido.objects.aggregate(
    total=Sum('monto')                      ← SQL: SELECT SUM(monto) FROM pedido;
)
total = resultado['total']                  ← Python recibe un solo número
```

**Funciones de agregación disponibles en Django:**

| Función    | Qué calcula                     | SQL equivalente  |
| ---------- | ------------------------------- | ---------------- |
| `Sum`      | La suma total del campo         | `SUM(campo)`     |
| `Avg`      | El promedio del campo           | `AVG(campo)`     |
| `Max`      | El valor máximo                 | `MAX(campo)`     |
| `Min`      | El valor mínimo                 | `MIN(campo)`     |
| `Count`    | La cantidad de registros        | `COUNT(campo)`   |

La diferencia entre `aggregate()` y `annotate()`:

```
aggregate() → devuelve UN resultado para toda la tabla
              "¿Cuál es el promedio de todos los pedidos?"

annotate()  → agrega un campo calculado a CADA registro
              "Para cada categoría, ¿cuántos productos tiene?"
```

> 📖 _Fuente: Django Documentation, "Aggregation" — docs.djangoproject.com (2026)_

---

---

# PARTE IV — ORDENAMIENTO Y FILTRADO EFICIENTE

---

## Ordenar en la base de datos: `.order_by()` vs `sorted()`

Python tiene la función `sorted()` para ordenar listas. Es útil para listas pequeñas, pero **desastrosa** para grandes volúmenes de datos:

```
Camino ineficiente:
──────────────────
todos = list(Pedido.objects.all())
recientes = sorted(todos, key=lambda p: p.fecha, reverse=True)[:50]

  → Carga 500.000 registros a memoria
  → Los ordena todos en Python
  → Toma solo los primeros 50
  → El 99.99% del trabajo fue innecesario

Camino eficiente:
────────────────
recientes = Pedido.objects.order_by('-fecha')[:50]

  → SQL: SELECT * FROM pedido ORDER BY fecha DESC LIMIT 50;
  → La base de datos ordena internamente con su índice
  → Python recibe exactamente 50 registros
```

La base de datos está optimizada para ordenar. Tiene **estructuras de datos internas** (índices) diseñadas específicamente para esta tarea. Ordenar en Python descarta todas esas optimizaciones.

---

## El peligro de `.defer()` mal usado

`.defer()` es una herramienta avanzada que le dice al ORM: "no traigas este campo ahora, tráelo después si lo necesito". Su propósito es ahorrar ancho de banda cuando hay campos pesados (textos largos, datos binarios) que no se van a usar.

```
Uso correcto:
────────────
productos = Producto.objects.defer('descripcion_larga')
for p in productos:
    print(p.nombre)       ← OK, 'nombre' fue traído
    print(p.precio)       ← OK, 'precio' fue traído

Uso incorrecto:
──────────────
productos = Producto.objects.defer('descripcion_larga')
for p in productos:
    print(p.descripcion_larga)   ← PROBLEMA: el ORM va a la base de datos
                                    a buscar este campo individualmente
                                    por CADA producto
```

**La regla es simple**: si vas a usar un campo, no lo excluyas con `defer()`. Si no estás seguro de qué campos necesitas, usa `.only()` para especificar **exactamente** los que sí vas a usar.

> 📖 _Fuente: Django Documentation, "defer() and only()" — docs.djangoproject.com (2026)_

---

---

# PARTE V — PAGINACIÓN

---

## ¿Por qué paginar?

Sin paginación, una vista que lista registros los muestra **todos de golpe**. Esto tiene tres consecuencias graves:

```
                    Sin paginación
                    ──────────────
    ┌────────────────────────────────────────┐
    │  Base de datos                          │
    │  Envía 50.000 registros al servidor    │
    └────────────┬───────────────────────────┘
                 │
    ┌────────────▼───────────────────────────┐
    │  Servidor Django                        │
    │  Procesa 50.000 registros              │
    │  Genera HTML con 50.000 filas          │
    └────────────┬───────────────────────────┘
                 │
    ┌────────────▼───────────────────────────┐
    │  Navegador del usuario                  │
    │  Intenta renderizar 50.000 elementos   │
    │  Se congela o se cierra ❌              │
    └────────────────────────────────────────┘
```

La paginación resuelve esto dividiendo los resultados en páginas de tamaño controlado:

```
                    Con paginación (25 por página)
                    ──────────────────────────────
    Base de datos → 25 registros → Servidor → HTML ligero → Navegador ✅
```

---

## El Paginator de Django

Django incluye un paginador integrado. No requiere bibliotecas externas:

```
Cómo funciona internamente:

  Paginator(queryset, 25)    → divide el queryset en páginas de 25
  paginator.num_pages        → cantidad total de páginas
  paginator.get_page(3)      → obtiene la página 3

  Internamente genera:
  SQL: SELECT * FROM producto LIMIT 25 OFFSET 50;
       └── trae solo 25 registros,
           saltando los primeros 50 (páginas 1 y 2)
```

El paginador trabaja **junto con** la evaluación perezosa. No trae todos los registros primero — deja que la base de datos haga el corte con `LIMIT` y `OFFSET`.

> 📊 **Dato real**: Según el reporte de rendimiento web de Cloudflare (2025), las páginas que implementan paginación server-side reducen el Time to First Byte (TTFB) en un 78% comparado con cargar todos los registros de una vez, mejorando directamente los Core Web Vitals.
>
> _Fuente: Cloudflare, "Web Performance Report: Server-Side Pagination Impact" (2025)_

---

---

# PARTE VI — ÍNDICES DE BASE DE DATOS

---

## ¿Qué es un índice?

Un **índice** es una estructura de datos que la base de datos construye para encontrar registros rápidamente, sin recorrer toda la tabla. Es el equivalente digital del índice de un libro.

```
Sin índice (búsqueda secuencial):
─────────────────────────────────
Para encontrar un pedido con estado "completado",
la base de datos revisa CADA fila, una por una:

  Fila 1: pendiente    → no
  Fila 2: cancelado    → no
  Fila 3: completado   → ✅
  Fila 4: pendiente    → no
  ...
  Fila 500.000: completado → ✅

  Tiempo: proporcional a la cantidad total de filas (O(n))

Con índice (búsqueda indexada):
──────────────────────────────
La base de datos tiene una estructura ordenada
que apunta directamente a las filas que coinciden:

  Índice de "estado":
  cancelado    → filas [2, 15, 203, ...]
  completado   → filas [3, 8, 42, ...]    ← va directo aquí
  pendiente    → filas [1, 4, 7, ...]

  Tiempo: proporcional al logaritmo de las filas (O(log n))
```

> 📊 **Dato real**: Según benchmarks de Percona (2025), en una tabla de 1 millón de registros en PostgreSQL 17, una consulta filtrada sin índice tarda 2-3 segundos. Con un índice B-tree apropiado, la misma consulta se ejecuta en 1-5 milisegundos — una mejora de hasta 1000x.
>
> _Fuente: Percona, "Database Indexing Best Practices" (2025)_

---

## ¿Cuándo agregar un índice en Django?

No todos los campos necesitan índice. Los índices consumen espacio en disco y hacen más lentas las operaciones de escritura (INSERT, UPDATE, DELETE). Se deben agregar con criterio.

**Campos que sí necesitan índice:**

| Situación                                             | Por qué                                           |
| ----------------------------------------------------- | ------------------------------------------------- |
| Campos usados frecuentemente en `filter()`            | La base de datos filtra más rápido con índice     |
| Campos usados en `order_by()`                         | La base de datos ordena más rápido con índice     |
| Campos de estado (activo/inactivo, pendiente/listo)   | Se filtran constantemente en todas las consultas  |
| Campos de fecha usados para ordenar                   | Ordenar por fecha es una de las operaciones más comunes |

**Campos que NO necesitan índice:**

| Situación                                    | Por qué                                         |
| -------------------------------------------- | ------------------------------------------------ |
| Campos de texto libre largo (descripciones)  | Los índices de texto son especiales y costosos   |
| Campos que rara vez se usan en filtros       | El índice existe pero no se usa — desperdicio    |
| Tablas con muy pocos registros               | La búsqueda secuencial ya es rápida              |

En Django, se agrega un índice de dos formas:

```
Forma 1 — en el campo:
  status = models.CharField(max_length=20, db_index=True)

Forma 2 — en la clase Meta (más flexible, permite índices compuestos):
  class Meta:
      indexes = [
          models.Index(fields=['status']),
          models.Index(fields=['status', '-fecha']),  ← índice compuesto
      ]
```

Un **índice compuesto** cubre consultas que filtran u ordenan por múltiples campos a la vez. Es más eficiente que dos índices individuales cuando las consultas combinan esos campos.

> 📖 _Fuente: Django Documentation, "Model Meta options: indexes" — docs.djangoproject.com (2026)_

---

---

# PARTE VII — RENDIMIENTO EN TEMPLATES

---

## El costo escondido de `{% include %}`

La etiqueta `{% include %}` de Django carga un archivo de template y lo renderiza dentro del template principal. Es excelente para reutilizar fragmentos de HTML — pero tiene un **costo** cada vez que se ejecuta.

```
Django procesa la inclusión así:

{% for producto in productos %}
    {% include 'partials/tarjeta.html' %}     ← por cada iteración:
{% endfor %}                                    1. Busca el archivo en disco
                                                2. Lo parsea
                                                3. Crea un nuevo contexto
                                                4. Lo renderiza

Si hay 50.000 productos → 50.000 operaciones de inclusión
```

El costo no es la inclusión en sí — es la **repetición masiva** dentro de un loop con miles de iteraciones.

**Alternativas:**

| Estrategia                      | Descripción                                                        |
| ------------------------------- | ------------------------------------------------------------------ |
| Incluir el HTML directamente    | Copiar el contenido del partial dentro del loop                    |
| Usar `{% cache %}`              | Django guarda el resultado en caché y no lo recalcula cada vez     |
| Combinar con paginación         | Si solo se muestran 25 elementos, la inclusión se ejecuta 25 veces |

La combinación más efectiva es **paginación + include**: paginar reduce los elementos por página, y el include mantiene el código organizado sin costo excesivo.

---

---

# RESUMEN — MAPA DE TÉCNICAS POR NIVEL

---

```
NIVEL NOVATO                    TÉCNICA                         EFECTO
────────────                    ───────                         ──────
Problema N+1                    select_related                  De N+1 a 1 consulta
                                prefetch_related                De N+1 a 2 consultas
Consulta dentro de loop         Reestructurar con relaciones    Eliminar consultas extras
len() para contar               .count()                        Sin carga a memoria

NIVEL INTERMEDIO                TÉCNICA                         EFECTO
────────────────                ───────                         ──────
Cálculos en Python              aggregate() / annotate()        La BD calcula por ti
Sin paginación                  Paginator                       Respuestas rápidas
Sin índices                     db_index / Meta.indexes         Consultas más veloces
Include masivo                  Paginación + inline HTML        Menos renderizados

NIVEL AVANZADO                  TÉCNICA                         EFECTO
──────────────                  ───────                         ──────
sorted() en Python              .order_by()                     Ordenamiento en la BD
len() > 0                       .exists()                       Verificación instantánea
defer() mal usado               .only()                         Campos explícitos
```

---

---

# HERRAMIENTAS DE DIAGNÓSTICO

---

## ¿Cómo medir el rendimiento?

No se puede optimizar lo que no se puede medir. Django ofrece herramientas para ver exactamente qué consultas genera:

| Herramienta                 | Qué muestra                                              | Nivel     |
| --------------------------- | -------------------------------------------------------- | --------- |
| **Django Debug Toolbar**    | Cantidad de queries, tiempo, SQL generado, duplicados    | Visual    |
| **`connection.queries`**    | Lista de todas las queries ejecutadas en la sesión       | Código    |
| **`QuerySet.explain()`**    | El plan de ejecución de la base de datos para un query   | Avanzado  |
| **Logging de SQL**          | Imprime cada query en la consola durante el desarrollo   | Consola   |

La **Django Debug Toolbar** es la herramienta más accesible. Se instala como una app de Django y muestra un panel visual en el navegador con:

- Cantidad total de consultas SQL por página
- Consultas duplicadas (señal de N+1)
- Tiempo total de base de datos
- SQL exacto de cada consulta

> 📖 _Fuente: Django Debug Toolbar Documentation — django-debug-toolbar.readthedocs.io (2026)_

---

---

# PRINCIPIOS CLAVE PARA RECORDAR

---

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. Menos consultas > consultas más rápidas                │
│     (es mejor hacer 2 consultas grandes que 1.000 chicas)  │
│                                                            │
│  2. Si la BD puede calcularlo, no lo calcules en Python    │
│     (count, sum, avg, order_by → siempre en la BD)         │
│                                                            │
│  3. No traigas lo que no vas a mostrar                     │
│     (pagina, filtra, limita)                               │
│                                                            │
│  4. Indexa lo que filtras u ordenas frecuentemente         │
│     (pero no todo — los índices tienen costo)              │
│                                                            │
│  5. Mide antes y después de cada cambio                    │
│     (sin medición, la optimización es adivinanza)          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Glosario de la clase

| Concepto                      | Qué es                                                                              |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| **ORM**                       | Capa de Django que traduce código Python a consultas SQL automáticamente             |
| **Evaluación perezosa**       | El queryset no ejecuta SQL hasta que los datos se necesitan realmente                |
| **N+1 Queries**               | Bug donde se ejecuta 1 consulta inicial + 1 consulta por cada registro              |
| **`select_related`**          | Trae datos relacionados en la misma consulta usando JOIN                             |
| **`prefetch_related`**        | Trae datos relacionados en una segunda consulta optimizada                           |
| **`aggregate()`**             | Ejecuta un cálculo (suma, promedio, etc.) sobre toda la tabla en la BD              |
| **`annotate()`**              | Agrega un campo calculado a cada registro del queryset                               |
| **`.count()`**                | Cuenta registros directamente en la BD sin cargarlos a memoria                       |
| **`.exists()`**               | Verifica si existe al menos un registro sin cargar datos                             |
| **`.order_by()`**             | Ordena los resultados directamente en la BD                                          |
| **`.defer()`**                | Excluye campos de la consulta inicial — los carga después si se acceden              |
| **`.only()`**                 | Incluye **solo** los campos especificados — más seguro que defer                     |
| **Paginator**                 | Clase de Django que divide resultados en páginas de tamaño fijo                      |
| **Índice (db_index)**         | Estructura de la BD que acelera búsquedas y ordenamientos en un campo                |
| **Índice compuesto**          | Índice sobre múltiples campos — eficiente para filtros combinados                    |
| **Django Debug Toolbar**      | Herramienta visual que muestra las consultas SQL de cada página                      |
| **Cuello de botella**         | El punto más lento del sistema — donde se concentra la espera                        |

---

> _"Optimizar no es hacer que el código se vea más complejo. Es hacer que la base de datos trabaje de forma inteligente, para que el usuario ni siquiera piense en esperar."_

---
