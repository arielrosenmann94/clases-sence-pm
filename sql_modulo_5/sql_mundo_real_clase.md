<!-- =========================================================
Archivo: sql_mundo_real_clase.md
Tema: SQL en el Mundo Real — Lo que Todo Programador Debe Saber
Duración: ~1h 30min (100% teoría)
Motor: PostgreSQL
========================================================= -->

# 🌍 SQL en el Mundo Real — Lo que Nadie te Enseña en los Tutoriales

---

---

# 📚 TEORÍA

---

## 🗺️ ¿Qué vamos a aprender hoy?

| Tema                       | Pregunta clave                                                  |
| -------------------------- | --------------------------------------------------------------- |
| 🕳️ NULL                    | ¿Por qué `NULL` causa más bugs que cualquier error de sintaxis? |
| 🔧 ALTER TABLE             | ¿Cómo modifico una tabla que ya existe en producción?           |
| ⚡ Performance             | ¿Por qué mi consulta tarda 30 segundos en vez de 0.1?           |
| 🧊 Índices                 | ¿Cómo hace SQL para buscar entre millones de filas tan rápido?  |
| 🧠 SQL avanzado            | ¿Qué usan los seniors que los juniors no conocen?               |
| 🗑️ Borrar datos            | ¿Realmente se borran o solo se esconden?                        |
| 🔄 Transacciones           | ¿Cómo protejo operaciones complejas? ¿Qué es un SAVEPOINT?      |
| 🕐 Fechas y zonas horarias | ¿Por qué la hora está mal en mi app?                            |
| 🤖 SQL y la IA             | ¿Cómo se preparan los datos para la Inteligencia Artificial?    |
| 💼 SQL en tu carrera       | ¿Qué piden en entrevistas técnicas?                             |

---

---

---

## 🤖 Antes de empezar — ¿Qué tiene que ver SQL con la Inteligencia Artificial?

---

### La pregunta que todos se hacen

> "ChatGPT, Spotify, Netflix, Google Maps... ¿cómo saben lo que quiero?"

La respuesta corta: **datos**. Muchos datos. Y esos datos viven en **bases de datos** que se consultan con **SQL**.

---

### La analogía: La cocina 🍳

```
🥕 Los DATOS        = los ingredientes (están en la base de datos)
📋 SQL              = la receta (cómo seleccionar y preparar los ingredientes)
🧑‍🍳 La IA            = el chef (toma los ingredientes preparados y crea el plato)
```

**Sin ingredientes bien preparados, el chef no puede cocinar nada.**

Un modelo de IA no puede aprender de datos desordenados, incompletos o con errores.
SQL es la herramienta que **limpia, organiza y prepara** esos datos.

---

### ¿Cómo se prepara data para una IA? (versión simple)

```
Paso 1: RECOLECTAR
  → Los datos se guardan en tablas SQL
    (compras, clics, reproducciones, calificaciones...)

Paso 2: LIMPIAR con SQL
  → Quitar datos vacíos (NULL)
  → Quitar duplicados
  → Corregir errores (fechas imposibles, valores negativos)

Paso 3: TRANSFORMAR con SQL
  → Unir tablas con JOIN para crear un "dataset" completo
  → Calcular promedios, conteos, categorías
  → Crear columnas nuevas ("¿cuántas veces compró en 30 días?")

Paso 4: EXPORTAR
  → El dataset limpio se entrega a la IA para que aprenda
```

---

### Ejemplo real: Recomendaciones de Spotify

Imagina que Spotify quiere recomendar canciones. Necesita preparar un dataset:

```sql
-- SQL que arma el dataset para la IA:
SELECT
    u.edad,
    u.pais,
    g.nombre AS genero_favorito,
    COUNT(r.id) AS canciones_escuchadas_mes,
    AVG(r.duracion_segundos) AS promedio_duracion,
    COUNT(r.id) FILTER (WHERE r.completa = true) AS canciones_completas,
    CASE
        WHEN COUNT(r.id) > 100 THEN 'heavy_user'
        WHEN COUNT(r.id) > 30  THEN 'regular'
        ELSE 'casual'
    END AS tipo_usuario
FROM usuarios u
JOIN reproducciones r ON r.id_usuario = u.id
JOIN canciones c ON c.id = r.id_cancion
JOIN generos g ON g.id = c.id_genero
WHERE r.fecha >= NOW() - INTERVAL '30 days'
GROUP BY u.id, u.edad, u.pais, g.nombre;
```

**¿Notan algo?** Esa consulta usa TODO lo que estamos aprendiendo:

- `JOIN` para unir 4 tablas
- `WHERE` con fechas
- `GROUP BY` + `COUNT` + `AVG`
- `FILTER` para contar condicionalmente
- `CASE WHEN` para clasificar
- `INTERVAL` para filtrar por tiempo

**SQL es la base invisible detrás de la IA.** Sin datos bien preparados, no hay magia.

---

### En resumen

| Sin SQL...                                | Con SQL...                                    |
| ----------------------------------------- | --------------------------------------------- |
| La IA tiene datos sucios y desordenados   | La IA recibe un dataset limpio y estructurado |
| El modelo aprende basura → predice basura | El modelo aprende bien → predice bien         |
| No sabes qué datos tienes                 | Puedes explorar, filtrar y entender tus datos |

> **"Garbage in, garbage out"** — Si le das basura a la IA, te devuelve basura.
> SQL es lo que convierte datos crudos en información útil.

---

---

---

## 1️⃣ NULL — El Fantasma de las Bases de Datos

---

### La trampa más peligrosa de SQL

`NULL` no es cero. `NULL` no es un texto vacío. `NULL` no es "false".

> **NULL significa "NO SÉ"** — es la **ausencia total de valor**.

---

### Las trampas de NULL (todas causan bugs reales)

---

### Trampa 1: NULL no es igual a nada, ni siquiera a sí mismo

```sql
-- ¿Esto es verdadero o falso?
SELECT NULL = NULL;
-- Resultado: NULL (¡ni true ni false!)

-- ¿Y esto?
SELECT NULL != NULL;
-- Resultado: NULL (¡tampoco!)
```

```
En cualquier lenguaje de programación:
  None == None  →  True ✅  (Python)
  null === null →  true ✅  (JavaScript)

En SQL:
  NULL = NULL   →  NULL 😱  (ni true ni false)
```

**¿Por qué?** Porque si no sé la edad de Juan y no sé la edad de Pedro, **no puedo afirmar que tengan la misma edad**. No sé ≠ No sé.

---

### Trampa 2: WHERE ignora los NULL

```sql
-- Tabla usuarios:
-- | id | nombre | edad |
-- |----|--------|------|
-- | 1  | Juan   | 25   |
-- | 2  | Ana    | 30   |
-- | 3  | Pedro  | NULL |
-- | 4  | María  | 28   |

-- Dame los que NO tienen 30 años:
SELECT * FROM usuarios WHERE edad != 30;
-- Resultado: Juan (25), María (28)
-- ❌ ¿Y Pedro? ¡DESAPARECIÓ!
-- NULL != 30 es NULL, y SQL trata NULL como "no cumple la condición"
```

**Pedro NO aparece** porque `NULL != 30` no es TRUE, es NULL. Y SQL solo muestra filas donde la condición es **estrictamente TRUE**.

---

### Trampa 3: Operaciones con NULL dan NULL

```sql
SELECT 100 + NULL;      -- NULL (no sé + 100 = no sé)
SELECT 'Hola' || NULL;  -- NULL (texto + no sé = no sé)
SELECT AVG(NULL);        -- NULL
```

Esto significa que si UNA columna tiene NULL, puede **contaminar** todo el cálculo.

---

### ¿Cómo protegerse? Las herramientas anti-NULL

```sql
-- IS NULL / IS NOT NULL (la forma correcta de preguntar por NULL)
SELECT * FROM usuarios WHERE edad IS NULL;      -- Pedro
SELECT * FROM usuarios WHERE edad IS NOT NULL;  -- Juan, Ana, María

-- COALESCE(valor, alternativa) — "Si es NULL, usa esto otro"
SELECT nombre, COALESCE(edad, 0) AS edad FROM usuarios;
-- Pedro → 0 (en vez de NULL)

-- NULLIF(a, b) — "Si a = b, devuelve NULL"
SELECT NULLIF(stock, 0);  -- Evita dividir por cero:
SELECT total / NULLIF(cantidad, 0);  -- Si cantidad es 0, devuelve NULL en vez de error
```

---

### Regla de oro para programadores

```
1. Si un campo puede ser NULL → usa COALESCE en cálculos
2. Nunca compares con = NULL → usa IS NULL
3. Si un campo DEBE tener valor → ponle NOT NULL en la tabla
4. En WHERE, recuerda que NULL no pasa filtros
```

---

---

---

## 2️⃣ ALTER TABLE — Modificar Tablas en Producción

---

### El escenario real

> Tu app ya está en producción con 50,000 usuarios.
> El cliente dice: "Necesito que los usuarios tengan teléfono obligatorio".
>
> **No puedes borrar la tabla y recrearla.** Hay datos reales ahí.
> Necesitas MODIFICARLA sin perder nada.

Para eso existe `ALTER TABLE` — el bisturí del DDL.

---

### Las 4 operaciones más comunes

---

### Agregar una columna

```sql
-- Agregar teléfono a una tabla que ya existe:
ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20);

-- Los usuarios existentes tendrán telefono = NULL
-- (porque la columna no existía cuando se crearon)
```

**¿Y si quiero que sea obligatorio?** Cuidado:

```sql
-- ❌ ESTO FALLA si ya hay datos:
ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20) NOT NULL;
-- ERROR: la columna tiene valores NULL en filas existentes

-- ✅ SOLUCIÓN: agregar con un valor por defecto
ALTER TABLE usuarios ADD COLUMN telefono VARCHAR(20) NOT NULL DEFAULT 'sin teléfono';
-- Todos los existentes quedan con 'sin teléfono'
```

---

### Renombrar una columna

```sql
ALTER TABLE usuarios RENAME COLUMN telefono TO celular;
-- telefono → celular (los datos no se pierden)
```

---

### Cambiar el tipo de dato

```sql
-- De VARCHAR(20) a VARCHAR(50) (ampliar)
ALTER TABLE usuarios ALTER COLUMN celular TYPE VARCHAR(50);

-- ⚠️ Achicar o cambiar tipo puede fallar si hay datos incompatibles
-- Ejemplo: cambiar VARCHAR a INT falla si hay letras en los datos
```

---

### Agregar o quitar restricciones

```sql
-- Hacer una columna obligatoria:
ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL;

-- Hacerla opcional de nuevo:
ALTER TABLE usuarios ALTER COLUMN email DROP NOT NULL;

-- Agregar un CHECK:
ALTER TABLE productos ADD CONSTRAINT chk_precio CHECK (precio > 0);

-- Agregar una UNIQUE:
ALTER TABLE usuarios ADD CONSTRAINT uq_email UNIQUE (email);
```

---

### Regla de oro en producción

```
⚠️ ALTER TABLE en producción puede:
  - Bloquear la tabla mientras se ejecuta (en tablas grandes)
  - Fallar si los datos existentes violan la nueva restricción
  - Romper queries que usan el nombre antiguo de una columna

✅ Buena práctica:
  1. Probar en un entorno de desarrollo primero
  2. Hacer backup antes de ejecutar
  3. Ejecutar en horarios de bajo tráfico
```

---

---

---

## 3️⃣ Performance — ¿Por Qué Mi Consulta es Tan Lenta?

---

### La historia del programador desesperado

> "Mi consulta funciona perfecto en desarrollo con 100 filas.
> En producción con 5 millones de filas, tarda 45 segundos.
> El cliente está furioso."

Esto pasa **todos los días** en empresas reales. Veamos por qué y cómo solucionarlo.

---

### ¿Cómo busca SQL sin índices? — Full Table Scan

Imagina un libro de 1,000 páginas **sin índice al final**. Si buscas la palabra "transacción", tienes que leer **cada página** del principio al fin.

```sql
SELECT * FROM usuarios WHERE email = 'juan@mail.com';

-- Sin índice en "email":
-- SQL recorre TODAS las filas de la tabla, una por una.
-- 100 filas     → 0.001 segundos ✅
-- 1,000,000 filas → 12 segundos 🐌
-- 50,000,000 filas → timeout ☠️
```

Esto se llama **Full Table Scan** — SQL lee cada fila y pregunta "¿es esta?".

---

---

## 4️⃣ Índices — El Truco que Acelera Todo

---

### La analogía perfecta: El índice de un libro 📖

Un libro de 1,000 páginas tiene un **índice al final** que dice:

```
Transacción ......... pág 342
Trigger ............. pág 458
Truncate ............ pág 129
```

Con el índice, vas **directo** a la página 342. Sin el índice, lees las 1,000 páginas.

**Un índice en SQL hace exactamente eso** pero con los datos de una tabla.

---

### ¿Cómo se crea un índice?

```sql
-- Crear un índice en la columna email:
CREATE INDEX idx_usuarios_email ON usuarios(email);

-- Ahora esta consulta es INSTANTÁNEA:
SELECT * FROM usuarios WHERE email = 'juan@mail.com';
-- En vez de recorrer 5 millones de filas, va DIRECTO al resultado.
```

---

### ¿Dónde poner índices?

```
✅ SÍ poner índice:
   - Columnas que usas en WHERE frecuentemente
   - Columnas que usas en JOIN (las FK)
   - Columnas que usas en ORDER BY
   - Columnas con valores únicos (email, RUT)

❌ NO poner índice en todo:
   - Cada índice OCUPA espacio en disco
   - Cada índice RALENTIZA los INSERT/UPDATE/DELETE
   - (porque cada vez que insertas un dato, también hay que actualizar el índice)
```

**Regla:** Los índices aceleran las **lecturas** pero ralentizan las **escrituras**. Hay que buscar el equilibrio.

---

### EXPLAIN — Radiografía de una consulta

`EXPLAIN` te muestra **qué hace SQL internamente** para ejecutar tu consulta:

```sql
EXPLAIN SELECT * FROM usuarios WHERE email = 'juan@mail.com';

-- SIN índice:
-- Seq Scan on usuarios  (costo alto)
-- → "Seq Scan" = recorrido secuencial = lento 🐌

-- CON índice:
-- Index Scan using idx_usuarios_email  (costo bajo)
-- → "Index Scan" = usó el índice = rápido ⚡
```

**Si ves "Seq Scan" en una tabla grande → probablemente necesitas un índice.**

---

### El problema N+1 (lo más común en apps web)

¿Por qué tu app tarda tanto si las consultas son "simples"?

Imagina que tienes una página que muestra **100 pedidos con el nombre del cliente**:

```
Lo que quieres mostrar:
  Pedido #001 — Juan Pérez — $50,000
  Pedido #002 — Ana Torres — $30,000
  Pedido #003 — Juan Pérez — $15,000
  ...
  Pedido #100 — María López — $22,000
```

---

### ❌ La forma MALA (N+1 consultas):

```sql
-- Consulta 1: Traer todos los pedidos
SELECT * FROM pedidos;
-- Resultado: 100 pedidos ✅

-- Ahora, por CADA pedido, el sistema hace una consulta aparte:

-- Consulta 2: ¿Quién hizo el pedido #001?
SELECT nombre FROM clientes WHERE id = 5;       -- Juan Pérez

-- Consulta 3: ¿Quién hizo el pedido #002?
SELECT nombre FROM clientes WHERE id = 12;      -- Ana Torres

-- Consulta 4: ¿Quién hizo el pedido #003?
SELECT nombre FROM clientes WHERE id = 5;       -- Juan Pérez (¡otra vez!)

-- Consulta 5: ¿Quién hizo el pedido #004?
SELECT nombre FROM clientes WHERE id = 8;       -- Pedro Soto

-- ... así 100 veces más ...

-- Consulta 101: ¿Quién hizo el pedido #100?
SELECT nombre FROM clientes WHERE id = 23;      -- María López
```

```
Total: 1 consulta + 100 consultas = 101 consultas 🐌
Cada consulta viaja del servidor → base de datos → servidor
101 viajes de ida y vuelta = LENTO
```

---

### ✅ La forma BUENA (1 sola consulta con JOIN):

```sql
-- UNA sola consulta que trae TODO junto:
SELECT
    p.id AS pedido,
    c.nombre AS cliente,
    p.total
FROM pedidos p
JOIN clientes c ON p.id_cliente = c.id;

-- Resultado inmediato:
-- | pedido | cliente      | total  |
-- |--------|-------------|--------|
-- | 001    | Juan Pérez  | 50000  |
-- | 002    | Ana Torres  | 30000  |
-- | 003    | Juan Pérez  | 15000  |
-- | ...    | ...         | ...    |
-- | 100    | María López | 22000  |
```

```
Total: 1 sola consulta ⚡
1 viaje de ida y vuelta = RÁPIDO
```

---

### La analogía del supermercado 🛒

```
N+1 = Ir al supermercado 100 veces, cada vez por 1 producto:
  🚗 Viaje 1: Comprar leche
  🚗 Viaje 2: Comprar pan
  🚗 Viaje 3: Comprar huevos
  ... 97 viajes más ...
  = Todo el día perdido 🐌

JOIN = Hacer 1 solo viaje con la lista completa:
  🚗 Viaje 1: Comprar leche, pan, huevos, y todo lo demás
  = 20 minutos ⚡
```

---

### ¿Por qué pasa esto?

Los frameworks (Django, Rails, Laravel) a veces hacen N+1 **sin que te des cuenta**, porque cargan los datos "de a poco" (lazy loading). Por eso es importante saber SQL: para **detectar** cuándo tu app está haciendo 101 consultas donde debería hacer 1.

**Si tu app es lenta, lo primero que debes revisar es si tienes un problema N+1.**

---

---

---

## 5️⃣ SQL Avanzado — Lo que Usan los Seniors

---

### ¿Por qué aprender esto?

Hasta ahora sabes hacer SELECT, WHERE, JOIN, GROUP BY. Con eso resuelves el 70% de los problemas.

Pero hay un 30% donde necesitas **algo más**. Estas 3 herramientas **separan a un junior de un senior**:

| Herramienta          | ¿Qué hace?                                   | Analogía                                               |
| -------------------- | -------------------------------------------- | ------------------------------------------------------ |
| **CASE WHEN**        | Toma decisiones dentro de SQL                | El IF/ELSE de cualquier lenguaje                       |
| **CTE (WITH)**       | Divide consultas grandes en pasos con nombre | Receta de cocina paso a paso                           |
| **Window Functions** | Calcula algo por grupo SIN perder las filas  | Cada alumno ve SU nota y el promedio del curso al lado |

---

---

### CASE WHEN — Tomar decisiones dentro de SQL

Tu jefe dice: "Necesito una lista de clientes clasificados como VIP, Regular o En Riesgo según su saldo."

Sin CASE WHEN, tendrías que hacer 3 consultas separadas. Con CASE WHEN, lo haces en **una sola**:

```sql
SELECT
  nombre,
  saldo,
  CASE                                    -- "Evalúa lo siguiente:"
    WHEN saldo >= 100000 THEN '🟢 VIP'    -- "Si el saldo es ≥ 100,000 → VIP"
    WHEN saldo >= 50000  THEN '🔵 Regular' -- "Si no, si es ≥ 50,000 → Regular"
    ELSE '🔴 En riesgo'                    -- "Si no cumple nada → En riesgo"
  END AS segmento                          -- "Llama a esa columna 'segmento'"
FROM clientes;
```

**Resultado:**

```
| nombre          | saldo   | segmento     |
|-----------------|---------|-------------|
| Lucía Fernández | 120000  | 🟢 VIP      |
| Nicolás Bravo   | 45000   | 🔴 En riesgo |
| Catalina Vidal  | 80000   | 🔵 Regular   |
```

**Léelo como español:**

```
CASO
  CUANDO saldo >= 100000  ENTONCES 'VIP'
  CUANDO saldo >= 50000   ENTONCES 'Regular'
  SI NO                           'En riesgo'
FIN como segmento
```

**Es literalmente un IF/ELSE pero escrito en SQL.**

---

### CTE (WITH) — Dividir Consultas en Pasos

---

### El problema

Las consultas complejas se vuelven **imposibles de leer** cuando están anidadas:

```sql
-- 🤯 ¿Qué hace esto? Buena suerte entendiéndolo:
SELECT * FROM (
    SELECT id_cliente, SUM(total) as compras FROM (
        SELECT * FROM pedidos WHERE fecha > NOW() - INTERVAL '30 days'
    ) sub1 GROUP BY id_cliente
) sub2 WHERE sub2.compras > 100000;
```

Esto es como escribir una oración de 200 palabras sin puntos ni comas. **Funciona, pero nadie la entiende.**

---

### La solución: dividir en pasos con nombre

Un CTE es como una **receta de cocina**: divides el proceso en pasos y cada paso tiene un nombre.

```sql
-- 📋 Paso 1: Filtrar solo los pedidos del último mes
WITH pedidos_recientes AS (
    SELECT * FROM pedidos
    WHERE fecha > NOW() - INTERVAL '30 days'
),

-- 📋 Paso 2: Sumar las compras por cliente
compras_por_cliente AS (
    SELECT id_cliente, SUM(total) AS compras
    FROM pedidos_recientes          -- ← usa el paso 1 por su nombre
    GROUP BY id_cliente
)

-- 📋 Paso 3: Mostrar solo los que compraron más de $100,000
SELECT * FROM compras_por_cliente   -- ← usa el paso 2 por su nombre
WHERE compras > 100000;
```

---

### ¿Ven la diferencia?

```
SIN CTE:
  SELECT * FROM (SELECT ... FROM (SELECT ... FROM ...) ...) ...
  → Una maraña imposible de leer 🤯

CON CTE:
  Paso 1: pedidos_recientes = ...
  Paso 2: compras_por_cliente = ... (usa paso 1)
  Paso 3: Resultado final (usa paso 2)
  → Se lee de arriba hacia abajo, como un libro ✅
```

**Léelo como español:**

```
CON pedidos_recientes COMO (
    seleccionar pedidos del último mes
),
compras_por_cliente COMO (
    sumar las compras usando pedidos_recientes
)
SELECCIONAR desde compras_por_cliente DONDE compras > 100000
```

**Es como decir:** "Primero prepara esto, luego calcula esto, y al final dame el resultado."

---

### Window Functions — Calcular Sin Perder Filas

---

### El problema

Imagina esta tabla de empleados:

```
| nombre  | departamento | sueldo  |
|---------|-------------|---------|
| Ana     | Ventas      | 800000  |
| Pedro   | Ventas      | 650000  |
| María   | Ventas      | 900000  |
| Juan    | TI          | 1200000 |
| Sofía   | TI          | 950000  |
```

Tu jefe pregunta: **"Quiero ver CADA empleado con su sueldo Y el promedio de su departamento al lado."**

---

### ¿Con GROUP BY?

```sql
SELECT departamento, AVG(sueldo) FROM empleados GROUP BY departamento;

-- Resultado:
-- | departamento | avg     |
-- |-------------|---------|
-- | Ventas      | 783333  |
-- | TI          | 1075000 |

-- ❌ Problema: ¡perdiste los nombres y los sueldos individuales!
-- GROUP BY COLAPSA las filas en una sola por grupo
```

---

### ✅ Con Window Function

```sql
SELECT
    nombre,
    departamento,
    sueldo,
    AVG(sueldo) OVER (PARTITION BY departamento) AS promedio_depto
    --                 ↑                              ↑
    --                 "Para cada departamento"        "columna nueva"
FROM empleados;
```

**Resultado:**

```
| nombre  | departamento | sueldo  | promedio_depto |
|---------|-------------|---------|---------------|
| Ana     | Ventas      | 800000  | 783333        |  ← cada uno ve
| Pedro   | Ventas      | 650000  | 783333        |  ← el promedio
| María   | Ventas      | 900000  | 783333        |  ← de SU depto
| Juan    | TI          | 1200000 | 1075000       |
| Sofía   | TI          | 950000  | 1075000       |
```

**¡Todas las filas siguen ahí!** Cada empleado ve su sueldo Y el promedio de su departamento.

---

### La analogía: El examen 📝

```
GROUP BY = El profesor muestra SOLO el promedio del curso → 6.2
  (los alumnos no ven SU propia nota)

Window Function = Cada alumno ve SU nota Y el promedio al lado:
  Ana     → 6.8 (promedio curso: 6.2)
  Pedro   → 5.5 (promedio curso: 6.2)
  María   → 7.0 (promedio curso: 6.2)
```

---

### Léelo como español

```sql
AVG(sueldo) OVER (PARTITION BY departamento)
```

```
PROMEDIO del sueldo
   SOBRE (PARTICIONADO POR departamento)

= "Calcula el promedio del sueldo,
   pero hazlo SEPARADO para cada departamento,
   y ponlo al lado de cada fila"
```

---

### Las más útiles (resumen rápido)

| Función        | ¿Qué hace?               | Ejemplo                                |
| -------------- | ------------------------ | -------------------------------------- |
| `ROW_NUMBER()` | Numera filas: 1, 2, 3... | "El 1° más vendido, el 2°, el 3°..."   |
| `RANK()`       | Numera con empates       | Si 2 empatan en 1°, el siguiente es 3° |
| `LAG()`        | Ve la fila anterior      | "Ventas de este mes vs mes pasado"     |
| `SUM() OVER`   | Acumulado progresivo     | "Ventas acumuladas enero a diciembre"  |

---

### Ejemplo final: Top 3 sueldos por departamento

```sql
-- Paso 1 (CTE): Numerar empleados dentro de cada depto
WITH ranking AS (
    SELECT
        nombre,
        departamento,
        sueldo,
        ROW_NUMBER() OVER (               -- "Numera las filas..."
            PARTITION BY departamento      -- "...dentro de cada departamento..."
            ORDER BY sueldo DESC           -- "...ordenando de mayor a menor sueldo"
        ) AS posicion
    FROM empleados
)

-- Paso 2: Solo mostrar los top 3
SELECT * FROM ranking WHERE posicion <= 3;
```

**Esto combina CTE + Window Function** — y se pregunta en entrevistas técnicas constantemente.

---

---

---

## 6️⃣ Soft Delete vs Hard Delete — ¿Borrar de Verdad?

---

### El dilema del DELETE

```sql
-- Un usuario pide "borrar mi cuenta"
DELETE FROM usuarios WHERE id = 42;
-- ✅ Se borró
-- ❌ Pero... ¿y sus pedidos? ¿y sus facturas? ¿y las estadísticas?
```

---

### Hard Delete vs Soft Delete

| Tipo            | Qué hace                                           | Consecuencias                                                 |
| --------------- | -------------------------------------------------- | ------------------------------------------------------------- |
| **Hard Delete** | `DELETE FROM usuarios WHERE id = 42`               | Se borra para siempre. Si hay FKs → falla o borra en cascada. |
| **Soft Delete** | `UPDATE usuarios SET activo = false WHERE id = 42` | El registro sigue ahí, pero marcado como inactivo.            |

---

### ¿Cómo funciona el Soft Delete?

```sql
-- La tabla tiene una columna "activo" o "eliminado"
CREATE TABLE usuarios (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(80),
    email   VARCHAR(120),
    activo  BOOLEAN DEFAULT TRUE,              -- ← esta columna
    fecha_eliminacion TIMESTAMP DEFAULT NULL    -- ← cuándo se "borró"
);

-- "Borrar" un usuario:
UPDATE usuarios
SET activo = false, fecha_eliminacion = NOW()
WHERE id = 42;

-- Todas las consultas normales filtran por activo:
SELECT * FROM usuarios WHERE activo = true;
-- El usuario 42 ya no aparece, pero sigue en la BD para auditoría
```

---

### ¿Cuándo usar cada uno?

```
SOFT DELETE cuando:
  ✅ Necesitas historial (auditoría, legal)
  ✅ El usuario podría querer "reactivarse"
  ✅ Otros datos dependen de ese registro (pedidos, facturas)
  ✅ Tu empresa necesita cumplir regulaciones

HARD DELETE cuando:
  ✅ Son datos temporales (sesiones, tokens, logs viejos)
  ✅ Ley de protección de datos obliga a borrar de verdad
  ✅ La tabla crece demasiado y necesitas liberar espacio
```

**En la industria, más del 80% de las aplicaciones usan Soft Delete.**

---

---

---

## 7️⃣ Transacciones y SAVEPOINT — Protege tus Operaciones

---

### ¿Qué es una transacción?

> Una transacción es un **grupo de operaciones que deben ejecutarse TODAS o NINGUNA**.

---

### La analogía: La transferencia bancaria 🏦

```
Juan quiere transferir $100,000 a Ana:

  Paso 1: Restar $100,000 de la cuenta de Juan
  Paso 2: Sumar $100,000 a la cuenta de Ana

¿Qué pasa si se cae la luz entre el paso 1 y el paso 2?

  Sin transacción: Juan perdió $100,000 y Ana no recibió nada 😱
  Con transacción: Se DESHACE todo automáticamente ✅
```

---

### BEGIN / COMMIT / ROLLBACK

```sql
-- BEGIN   → Abre la burbuja protectora
-- COMMIT  → Confirma todo (graba los cambios)
-- ROLLBACK → Deshace todo (como si nada hubiera pasado)

BEGIN;

  UPDATE cuentas SET saldo = saldo - 100000 WHERE id = 1;  -- Juan -$100,000
  UPDATE cuentas SET saldo = saldo + 100000 WHERE id = 2;  -- Ana  +$100,000

  -- Verificar que todo está bien:
  SELECT nombre, saldo FROM cuentas WHERE id IN (1, 2);

  -- Si está bien:
  COMMIT;     -- ✅ Cambios grabados permanentemente

  -- Si algo salió mal:
  -- ROLLBACK;  -- ❌ Se deshace TODO, saldos vuelven a como estaban
```

---

### ¿Qué pasa internamente?

```
BEGIN
  ┌──────────────────────────────────────┐
  │  🔒 Los cambios son TEMPORALES       │
  │  Solo tú los ves                     │
  │  Otros usuarios ven los datos        │
  │  como estaban ANTES del BEGIN        │
  │                                      │
  │  UPDATE ... ← temporal               │
  │  INSERT ... ← temporal               │
  │  DELETE ... ← temporal               │
  └──────────────────────────────────────┘
       │                    │
    COMMIT              ROLLBACK
       │                    │
  ✅ Se graban         ❌ Se borran
  los cambios          los cambios
  permanentemente      como si nada
```

---

---

### SAVEPOINT — Puntos de guardado parciales 🎮

---

### La analogía: El videojuego

En un videojuego, no guardas solo al principio y al final. **Guardas en puntos intermedios** para no perder todo el progreso si fallas:

```
🎮 Nivel 1: Completado → GUARDAR ✅
🎮 Nivel 2: Completado → GUARDAR ✅
🎮 Nivel 3: Mueres → Vuelves al guardado del Nivel 2
   (No pierdes Nivel 1 ni Nivel 2)
```

**SAVEPOINT hace exactamente eso dentro de una transacción.**

---

### ¿Cómo funciona?

```sql
BEGIN;

  -- Paso 1: Registrar un pedido
  INSERT INTO pedidos (id_cliente, total) VALUES (1, 50000);

  SAVEPOINT despues_del_pedido;  -- 💾 Guardar progreso aquí

  -- Paso 2: Descontar del inventario
  UPDATE productos SET stock = stock - 1 WHERE id = 5;

  SAVEPOINT despues_del_stock;   -- 💾 Guardar progreso aquí

  -- Paso 3: Intentar cobrar
  UPDATE clientes SET saldo = saldo - 50000 WHERE id = 1;

  -- Verificar: ¿el saldo quedó negativo?
  SELECT saldo FROM clientes WHERE id = 1;
  -- Resultado: -10000 ← 🚨 ¡No alcanza!

  -- Deshacer SOLO el paso 3, manteniendo pasos 1 y 2:
  ROLLBACK TO despues_del_stock;

  -- El pedido sigue registrado ✅
  -- El stock sigue descontado ✅
  -- El cobro se deshizo ✅

  -- Registrar que el cobro falló:
  UPDATE pedidos SET estado = 'pendiente_pago' WHERE id_cliente = 1;

COMMIT;
```

---

### SAVEPOINT vs ROLLBACK completo

```
Sin SAVEPOINT:
  BEGIN → paso 1 → paso 2 → paso 3 (falla) → ROLLBACK
  ❌ Se pierden los 3 pasos

Con SAVEPOINT:
  BEGIN → paso 1 → 💾 SAVEPOINT → paso 2 → 💾 SAVEPOINT → paso 3 (falla)
  → ROLLBACK TO savepoint_2
  ✅ Se pierden solo los pasos después del savepoint
```

---

### ¿Cuándo usar SAVEPOINT?

| Escenario                         | Por qué                                                         |
| --------------------------------- | --------------------------------------------------------------- |
| Proceso con múltiples pasos       | Si un paso falla, no pierdes los anteriores                     |
| Pruebas dentro de una transacción | Probar algo, y si falla, volver atrás sin perder todo           |
| Importación de datos masivos      | Si una fila falla, registrar el error y continuar con las demás |
| Operaciones condicionales         | "Intenta esto, si no funciona, intenta esto otro"               |

---

### Ejemplo real: Proceso de compra en un e-commerce

```sql
BEGIN;

  -- 1. Crear la orden
  INSERT INTO ordenes (id_cliente, fecha, estado)
  VALUES (42, NOW(), 'procesando');
  SAVEPOINT orden_creada;

  -- 2. Reservar productos del carrito
  UPDATE productos SET stock = stock - 2 WHERE id = 10;
  UPDATE productos SET stock = stock - 1 WHERE id = 25;
  SAVEPOINT stock_reservado;

  -- 3. Intentar cobrar al cliente
  UPDATE clientes SET saldo = saldo - 89970 WHERE id = 42;

  -- Verificar saldo
  -- Si saldo < 0 → ROLLBACK TO stock_reservado (se deshace el cobro)
  -- Si saldo >= 0 → seguimos

  -- 4. Registrar el pago
  INSERT INTO pagos (id_cliente, monto, metodo)
  VALUES (42, 89970, 'tarjeta');

  -- 5. Actualizar estado de la orden
  UPDATE ordenes SET estado = 'completada' WHERE id_cliente = 42;

COMMIT;  -- Todo confirmado ✅
```

---

---

---

## 8️⃣ Fechas y Zonas Horarias — El Dolor de Cabeza Universal

---

### El problema

> "En mi computador dice 14:00, en el servidor dice 17:00, en la base de datos dice 20:00. ¿Cuál es la hora correcta?"

---

### ¿Por qué pasa esto?

```
Chile:           UTC-3  (14:00 hora local = 17:00 UTC)
España:          UTC+1  (14:00 hora local = 13:00 UTC)
Japón:           UTC+9  (14:00 hora local = 05:00 UTC)
Servidor AWS:    UTC+0  (usa UTC siempre)
```

Si tu app guarda `14:00` sin decir **de qué zona horaria**... nadie sabe qué hora es realmente.

---

### La regla de oro

> **SIEMPRE guarda las fechas en UTC. Convierte a hora local solo al MOSTRAR al usuario.**

```sql
-- TIMESTAMP → sin zona horaria (peligroso)
CREATE TABLE eventos (
    fecha TIMESTAMP  -- ¿14:00 de dónde? 🤷
);

-- TIMESTAMPTZ → con zona horaria (correcto)
CREATE TABLE eventos (
    fecha TIMESTAMPTZ DEFAULT NOW()  -- Guarda en UTC automáticamente ✅
);
```

---

### Funciones útiles de fecha en PostgreSQL

```sql
-- Fecha/hora actual
NOW()                                    -- 2025-02-18 20:44:16-03
CURRENT_DATE                             -- 2025-02-18
CURRENT_TIME                             -- 20:44:16-03

-- Extraer partes
EXTRACT(YEAR FROM fecha)                 -- 2025
EXTRACT(MONTH FROM fecha)               -- 2
EXTRACT(DOW FROM fecha)                  -- 2 (día de la semana, 0=domingo)

-- Agrupar por mes (útil para reportes)
DATE_TRUNC('month', fecha)               -- 2025-02-01 00:00:00

-- Aritmética de fechas
NOW() - INTERVAL '30 days'               -- Hace 30 días
NOW() + INTERVAL '1 year'                -- Dentro de 1 año
fecha2 - fecha1                           -- Diferencia entre dos fechas

-- Edad (super útil)
AGE(NOW(), fecha_nacimiento)             -- '32 years 5 mons 12 days'
```

---

### Ejemplo real: Reportes mensuales

```sql
-- ¿Cuántas ventas hubo por mes?
SELECT
    DATE_TRUNC('month', fecha_venta) AS mes,
    COUNT(*) AS total_ventas,
    SUM(monto) AS ingresos
FROM ventas
WHERE fecha_venta >= NOW() - INTERVAL '1 year'
GROUP BY DATE_TRUNC('month', fecha_venta)
ORDER BY mes;
```

---

---

---

## 9️⃣ SQL en Tu Carrera — ¿Qué Viene Después?

---

### Roles que usan SQL todos los días

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  👨‍💻 Backend Developer                                │
│  "Escribo las queries que usa la app"                │
│  → CRUD, JOINs, transacciones, optimización          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  📊 Data Analyst                                     │
│  "Extraigo insights de los datos para el negocio"    │
│  → SELECT complejos, GROUP BY, reportes, dashboards  │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  🔧 Data Engineer                                    │
│  "Construyo los pipelines que mueven los datos"      │
│  → ETL, CTEs masivos, performance, Data Warehouses   │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  🛡️ DBA (Database Administrator)                     │
│  "Mantengo la base de datos segura y rápida"         │
│  → Índices, backups, replicación, tuning             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

### ¿Qué preguntan en entrevistas técnicas?

Preguntas reales que hacen en empresas de tecnología:

---

### Nivel Junior

```
"Dame los clientes que hicieron más de 5 compras el último mes"

→ Necesitas: JOIN + WHERE con fechas + GROUP BY + HAVING
```

```sql
SELECT c.nombre, COUNT(p.id) AS total_compras
FROM clientes c
JOIN pedidos p ON p.id_cliente = c.id
WHERE p.fecha >= NOW() - INTERVAL '30 days'
GROUP BY c.id, c.nombre
HAVING COUNT(p.id) > 5;
```

---

### Nivel Mid

```
"Dame el segundo producto más vendido de cada categoría"

→ Necesitas: CTE + ROW_NUMBER + PARTITION BY
```

```sql
WITH ranking AS (
    SELECT
        c.nombre AS categoria,
        p.nombre AS producto,
        SUM(d.cantidad) AS unidades,
        ROW_NUMBER() OVER (
            PARTITION BY c.nombre
            ORDER BY SUM(d.cantidad) DESC
        ) AS posicion
    FROM categorias c
    JOIN productos p ON p.id_categoria = c.id
    JOIN detalle_pedidos d ON d.id_producto = p.id
    GROUP BY c.nombre, p.nombre
)
SELECT * FROM ranking WHERE posicion = 2;
```

---

### Nivel Senior

```
"Compara las ventas de cada mes con el mes anterior
 y calcula el porcentaje de crecimiento"

→ Necesitas: CTE + LAG + aritmética
```

```sql
WITH ventas_mensuales AS (
    SELECT
        DATE_TRUNC('month', fecha) AS mes,
        SUM(total) AS ventas
    FROM pedidos
    GROUP BY DATE_TRUNC('month', fecha)
)
SELECT
    mes,
    ventas,
    LAG(ventas) OVER (ORDER BY mes) AS mes_anterior,
    ROUND(
        (ventas - LAG(ventas) OVER (ORDER BY mes))
        * 100.0 / LAG(ventas) OVER (ORDER BY mes),
        1
    ) AS crecimiento_pct
FROM ventas_mensuales
ORDER BY mes;
```

---

### ¿Qué estudiar después de este curso?

| Prioridad | Tema                    | Por qué                                             |
| --------- | ----------------------- | --------------------------------------------------- |
| 🥇        | **Índices y EXPLAIN**   | Lo primero que te piden optimizar en el trabajo     |
| 🥇        | **Transacciones**       | Sin esto no puedes manejar dinero ni datos críticos |
| 🥈        | **Window Functions**    | Te diferencian de un junior inmediatamente          |
| 🥈        | **CTEs y subconsultas** | Necesarias para cualquier reporte no trivial        |
| 🥉        | **Vistas y funciones**  | Reutilizar lógica SQL como un profesional           |
| 🥉        | **Triggers**            | Automatizar acciones en la base de datos            |

---

### El consejo más importante

> **SQL no es una herramienta "vieja". Es la BASE de todo.**
>
> Django usa SQL. Laravel usa SQL. Spring usa SQL.
> React muestra datos que vienen de SQL.
> Los modelos de IA se entrenan con datos que vienen de SQL.
> Las fintech, los bancos, los hospitales, Netflix, Spotify — **todo es SQL por dentro.**
>
> Un programador que domina SQL tiene ventaja en CUALQUIER área.

---

### Resumen Final

| Concepto             | Lo más importante                                                                 |
| -------------------- | --------------------------------------------------------------------------------- |
| **NULL**             | No es cero ni vacío. Es "no sé". Usa `IS NULL` y `COALESCE`.                      |
| **ALTER TABLE**      | Modifica tablas en producción. Siempre con backup y pruebas previas.              |
| **Índices**          | Aceleran lecturas, ralentizan escrituras. Ponlos en columnas de WHERE y JOIN.     |
| **EXPLAIN**          | Radiografía de tu consulta. Si ves "Seq Scan" en tabla grande → necesitas índice. |
| **N+1**              | 100 consultas donde debería haber 1. Solución: usar JOIN.                         |
| **CTE (WITH)**       | Tabla temporal que hace tu SQL legible y mantenible.                              |
| **Window Functions** | Cálculos sobre grupos sin colapsar filas. ROW_NUMBER, RANK, LAG.                  |
| **CASE WHEN**        | IF/ELSE dentro de SQL para clasificar datos.                                      |
| **Soft Delete**      | No borres datos, márcalos como inactivos.                                         |
| **Transacciones**    | BEGIN/COMMIT/ROLLBACK: todo o nada.                                               |
| **SAVEPOINT**        | Puntos de guardado parciales dentro de una transacción.                           |
| **TIMESTAMPTZ**      | Guarda fechas en UTC, convierte al mostrar.                                       |
| **DATE_TRUNC**       | Agrupa fechas por mes/año para reportes.                                          |

---
