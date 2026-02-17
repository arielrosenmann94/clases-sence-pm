<!-- =========================================================
Archivo: sql_select.md
Tema: SQL Básico — SELECT: consultar datos con y sin JOIN
========================================================= -->

# SQL Básico (curso) — SELECT: consultar datos con y sin JOIN

Este documento cubre todo lo necesario para **consultar datos** en tablas:

1. Sintaxis básica de `SELECT`
2. Filtrar con `WHERE`
3. Ordenar con `ORDER BY`
4. Limitar resultados con `LIMIT`
5. Eliminar duplicados con `DISTINCT`
6. Alias con `AS`
7. Funciones de agregación (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
8. Agrupar con `GROUP BY`
9. Filtrar grupos con `HAVING`
10. Subconsultas básicas
11. **JOIN**: combinar datos de varias tablas
12. Tipos de JOIN (`INNER`, `LEFT`, `RIGHT`, `FULL`)
13. JOIN con más de 2 tablas
14. Errores comunes al consultar

> Enfoque: **simple, pedagógico y práctico**.
> Pensado para estudiantes que recién comienzan.

---

## Tablas de ejemplo (usadas en todo el documento)

Para que los ejemplos sean claros, trabajaremos con estas tablas:

```sql
-- =============================================
-- EJECUTAR ESTO PRIMERO para poder practicar
-- (puedes ejecutar este bloque las veces que quieras,
--  el DROP borra las tablas si ya existen)
-- =============================================

-- Borrar tablas si ya existen (orden: hijas primero, padres después)
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  precio NUMERIC(10,2),
  stock INT DEFAULT 0,
  id_categoria INT,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

CREATE TABLE clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  ciudad VARCHAR(50)
);

CREATE TABLE ventas (
  id INT PRIMARY KEY,
  fecha DATE,
  id_cliente INT,
  id_producto INT,
  cantidad INT,
  FOREIGN KEY (id_cliente) REFERENCES clientes(id),
  FOREIGN KEY (id_producto) REFERENCES productos(id)
);
```

**Datos de ejemplo:**

```sql
INSERT INTO categorias VALUES (1,'Bebidas'), (2,'Snacks'), (3,'Lácteos');

INSERT INTO productos VALUES
  (1, 'Agua 1L',      990,  50, 1),
  (2, 'Coca Cola 2L', 1990, 30, 1),
  (3, 'Papas Fritas', 1500, 20, 2),
  (4, 'Yogurt',       890,  40, 3),
  (5, 'Leche 1L',     1200, 0,  3),
  (6, 'Galletas',     800,  15, NULL);

INSERT INTO clientes VALUES
  (1, 'Ana López',   'ana@mail.com',   'Santiago'),
  (2, 'Pedro Soto',  'pedro@mail.com', 'Valparaíso'),
  (3, 'María Díaz',  NULL,             'Santiago'),
  (4, 'Juan Pérez',  'juan@mail.com',  'Concepción');

INSERT INTO ventas VALUES
  (1, '2026-02-01', 1, 1, 3),
  (2, '2026-02-01', 1, 3, 2),
  (3, '2026-02-02', 2, 2, 1),
  (4, '2026-02-03', 3, 4, 5),
  (5, '2026-02-03', 1, 2, 2);
```

---

# PARTE 1: Consultas sin JOIN (una sola tabla)

---

## 1) SELECT básico

### 1.1 Seleccionar todas las columnas

```sql
SELECT * FROM productos;
```

- `*` significa "todas las columnas".
- Devuelve todas las filas de la tabla.

### 1.2 Seleccionar columnas específicas

```sql
SELECT nombre, precio FROM productos;
```

- Solo muestra `nombre` y `precio`.
- Es **mejor práctica** que usar `*` (más rápido y claro).

### 1.3 Columnas calculadas

Puedes crear columnas nuevas con operaciones:

```sql
SELECT nombre, precio, precio * 1.19 AS precio_con_iva
FROM productos;
```

| nombre       | precio | precio_con_iva |
| ------------ | ------ | -------------- |
| Agua 1L      | 990    | 1178.10        |
| Coca Cola 2L | 1990   | 2368.10        |

---

## 2) WHERE — filtrar filas

### 2.1 Operadores de comparación

```sql
-- Igual
SELECT * FROM productos WHERE precio = 990;

-- Distinto
SELECT * FROM productos WHERE precio != 990;
-- También funciona: WHERE precio <> 990

-- Mayor / Menor
SELECT * FROM productos WHERE precio > 1000;
SELECT * FROM productos WHERE precio <= 1500;
```

### 2.2 Operadores lógicos (AND, OR, NOT)

```sql
-- Dos condiciones (ambas deben cumplirse)
SELECT * FROM productos
WHERE precio > 500 AND stock > 0;

-- Al menos una condición
SELECT * FROM productos
WHERE id_categoria = 1 OR id_categoria = 2;

-- Negar una condición
SELECT * FROM productos
WHERE NOT id_categoria = 3;
```

### 2.3 BETWEEN — rango de valores

```sql
SELECT * FROM productos
WHERE precio BETWEEN 800 AND 1500;
```

Equivale a: `WHERE precio >= 800 AND precio <= 1500`

### 2.4 IN — lista de valores

```sql
SELECT * FROM productos
WHERE id_categoria IN (1, 2);
```

Equivale a: `WHERE id_categoria = 1 OR id_categoria = 2`

### 2.5 LIKE — buscar patrones en texto

```sql
-- Empieza con 'A'
SELECT * FROM productos WHERE nombre LIKE 'A%';

-- Termina con 'L'
SELECT * FROM productos WHERE nombre LIKE '%L';

-- Contiene 'Cola'
SELECT * FROM productos WHERE nombre LIKE '%Cola%';
```

| Comodín | Significado                      | Ejemplo                      |
| ------- | -------------------------------- | ---------------------------- |
| `%`     | Cualquier cantidad de caracteres | `'%Cola%'` → contiene "Cola" |
| `_`     | Exactamente 1 carácter           | `'_ua'` → "Jua", "Lua"       |

> `LIKE` distingue mayúsculas. Para ignorarlas usa `ILIKE` (PostgreSQL):

```sql
SELECT * FROM productos WHERE nombre ILIKE '%coca%';
```

### 2.6 IS NULL / IS NOT NULL

```sql
-- Productos sin categoría
SELECT * FROM productos WHERE id_categoria IS NULL;

-- Productos con categoría
SELECT * FROM productos WHERE id_categoria IS NOT NULL;

-- Clientes sin email
SELECT * FROM clientes WHERE email IS NULL;
```

> ⚠️ Nunca uses `= NULL`. Siempre `IS NULL`.
> `NULL` no es un valor, es la **ausencia** de valor.

---

## 3) ORDER BY — ordenar resultados

### 3.1 Orden ascendente (por defecto)

```sql
SELECT * FROM productos ORDER BY precio;
-- o explícitamente:
SELECT * FROM productos ORDER BY precio ASC;
```

### 3.2 Orden descendente

```sql
SELECT * FROM productos ORDER BY precio DESC;
```

### 3.3 Ordenar por varias columnas

```sql
SELECT * FROM productos
ORDER BY id_categoria ASC, precio DESC;
```

- Primero ordena por categoría (1, 2, 3...).
- Dentro de cada categoría, ordena por precio de mayor a menor.

### 3.4 Ordenar por posición de columna

```sql
SELECT nombre, precio FROM productos
ORDER BY 2 DESC;
```

- `2` se refiere a la segunda columna del SELECT (`precio`).

> ⚠️ Es menos legible. Preferir nombre de columna.

---

## 4) LIMIT y OFFSET — limitar resultados

### 4.1 Obtener las primeras N filas

```sql
-- Los 3 productos más baratos
SELECT * FROM productos
ORDER BY precio ASC
LIMIT 3;
```

### 4.2 Saltar filas (paginación)

```sql
-- Página 2 (saltando los primeros 3)
SELECT * FROM productos
ORDER BY precio ASC
LIMIT 3 OFFSET 3;
```

- `LIMIT 3`: muestra 3 filas.
- `OFFSET 3`: salta las primeras 3.

### 4.3 El producto más caro

```sql
SELECT * FROM productos
ORDER BY precio DESC
LIMIT 1;
```

---

## 5) DISTINCT — eliminar duplicados

### 5.1 Valores únicos de una columna

```sql
SELECT DISTINCT ciudad FROM clientes;
```

**Resultado:**

| ciudad     |
| ---------- |
| Santiago   |
| Valparaíso |
| Concepción |

(Santiago aparece 1 sola vez aunque hay 2 clientes de Santiago.)

### 5.2 Combinación única de columnas

```sql
SELECT DISTINCT ciudad, id_categoria
FROM clientes, productos;
```

---

## 6) AS — alias (nombres temporales)

### 6.1 Alias para columnas

```sql
SELECT nombre AS producto, precio AS valor
FROM productos;
```

| producto | valor |
| -------- | ----- |
| Agua 1L  | 990   |

### 6.2 Alias para cálculos

```sql
SELECT nombre, precio * stock AS valor_inventario
FROM productos;
```

### 6.3 Alias para tablas

```sql
SELECT p.nombre, p.precio
FROM productos AS p;
```

- Útil cuando trabajas con varias tablas (JOIN).
- `p` es un "apodo" corto para `productos`.

> El `AS` es opcional en muchos casos: `FROM productos p` también funciona.

---

## 7) Funciones de agregación

Las funciones de agregación operan sobre **varias filas** y devuelven **un solo valor**.

### 7.1 COUNT — contar filas

```sql
-- Total de productos
SELECT COUNT(*) FROM productos;
-- Resultado: 6

-- Productos con categoría (no cuenta NULL)
SELECT COUNT(id_categoria) FROM productos;
-- Resultado: 5
```

### 7.2 SUM — sumar valores

```sql
SELECT SUM(stock) AS stock_total FROM productos;
-- Resultado: 155
```

### 7.3 AVG — promedio

```sql
SELECT AVG(precio) AS precio_promedio FROM productos;
-- Resultado: 1228.33
```

### 7.4 MIN y MAX

```sql
SELECT MIN(precio) AS mas_barato, MAX(precio) AS mas_caro
FROM productos;
-- Resultado: 800 | 1990
```

### 7.5 Combinando varias funciones

```sql
SELECT
  COUNT(*) AS total,
  SUM(precio) AS suma,
  AVG(precio) AS promedio,
  MIN(precio) AS minimo,
  MAX(precio) AS maximo
FROM productos;
```

---

## 8) GROUP BY — agrupar filas

### 8.1 ¿Para qué sirve?

Agrupa las filas que tienen el **mismo valor** en una columna, para aplicar funciones de agregación **por grupo**.

### 8.2 Ejemplo: contar productos por categoría

```sql
SELECT id_categoria, COUNT(*) AS total_productos
FROM productos
GROUP BY id_categoria;
```

| id_categoria | total_productos |
| ------------ | --------------- |
| 1            | 2               |
| 2            | 1               |
| 3            | 2               |
| NULL         | 1               |

### 8.3 Ejemplo: precio promedio por categoría

```sql
SELECT id_categoria, AVG(precio) AS precio_promedio
FROM productos
GROUP BY id_categoria;
```

### 8.4 Regla importante

> Toda columna en el `SELECT` que **no** sea función de agregación **debe** estar en el `GROUP BY`.

```sql
-- ✅ Correcto
SELECT id_categoria, COUNT(*) FROM productos GROUP BY id_categoria;

-- ❌ Error
SELECT id_categoria, nombre, COUNT(*) FROM productos GROUP BY id_categoria;
-- 'nombre' no está en GROUP BY ni es función de agregación
```

---

## 9) HAVING — filtrar grupos

### 9.1 ¿Para qué sirve?

`HAVING` filtra **después** de agrupar. Es como un `WHERE` pero para grupos.

### 9.2 Ejemplo: categorías con más de 1 producto

```sql
SELECT id_categoria, COUNT(*) AS total
FROM productos
GROUP BY id_categoria
HAVING COUNT(*) > 1;
```

| id_categoria | total |
| ------------ | ----- |
| 1            | 2     |
| 3            | 2     |

### 9.3 Diferencia entre WHERE y HAVING

|                                      | WHERE                | HAVING                 |
| ------------------------------------ | -------------------- | ---------------------- |
| ¿Cuándo filtra?                      | **Antes** de agrupar | **Después** de agrupar |
| ¿Qué filtra?                         | Filas individuales   | Grupos                 |
| ¿Puede usar funciones de agregación? | ❌ No                | ✅ Sí                  |

```sql
-- WHERE filtra filas, HAVING filtra grupos
SELECT id_categoria, AVG(precio) AS promedio
FROM productos
WHERE stock > 0           -- primero quita productos sin stock
GROUP BY id_categoria
HAVING AVG(precio) > 1000; -- después quita categorías baratas
```

---

## 10) Subconsultas básicas

### 10.1 Subconsulta en WHERE

Una subconsulta es un `SELECT` dentro de otro `SELECT`:

```sql
-- Productos más caros que el promedio
SELECT nombre, precio
FROM productos
WHERE precio > (SELECT AVG(precio) FROM productos);
```

### 10.2 Subconsulta con IN

```sql
-- Clientes que han comprado algo
SELECT nombre FROM clientes
WHERE id IN (SELECT id_cliente FROM ventas);
```

### 10.3 Subconsulta con NOT IN

```sql
-- Clientes que NUNCA han comprado
SELECT nombre FROM clientes
WHERE id NOT IN (SELECT id_cliente FROM ventas);
```

---

# PARTE 2: Consultas con JOIN (varias tablas)

---

## 11) ¿Qué es un JOIN?

### 11.1 El problema

Los datos están **separados en varias tablas**. Si quieres ver el nombre del producto **junto** con el nombre de su categoría, necesitas **combinar** las tablas.

### 11.2 La solución: JOIN

`JOIN` une filas de dos tablas basándose en una **condición** (generalmente FK = PK).

### 11.3 Diagrama mental

```
productos                    categorias
+---------+-----------+      +----+---------+
| nombre  | id_cat    | ---> | id | nombre  |
+---------+-----------+      +----+---------+
| Agua    | 1         |      | 1  | Bebidas |
| Papas   | 2         |      | 2  | Snacks  |
+---------+-----------+      +----+---------+

Resultado del JOIN:
+-------+---------+
| Agua  | Bebidas |
| Papas | Snacks  |
+-------+---------+
```

---

## 12) INNER JOIN — el más común

### 12.1 ¿Qué hace?

Devuelve **solo las filas que tienen coincidencia** en ambas tablas.

> Si un producto no tiene categoría (NULL), **no aparece**.
> Si una categoría no tiene productos, **no aparece**.

### 12.2 Sintaxis

```sql
SELECT columnas
FROM tabla1
INNER JOIN tabla2 ON tabla1.columna = tabla2.columna;
```

### 12.3 Ejemplo: productos con su categoría

```sql
SELECT
  p.nombre AS producto,
  p.precio,
  c.nombre AS categoria
FROM productos p
INNER JOIN categorias c ON p.id_categoria = c.id;
```

**Explicación letra por letra:**

| Fragmento                  | Significado                                                                                                            |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `FROM productos p`         | Leo la tabla `productos` y le pongo el apodo **`p`** (para no escribir "productos" cada vez)                           |
| `INNER JOIN categorias c`  | Uno con la tabla `categorias`, que tiene el apodo **`c`**                                                              |
| `ON p.id_categoria = c.id` | La condición de unión: "une cada producto con la categoría donde `productos.id_categoria` sea igual a `categorias.id`" |
| `p.nombre`                 | La columna `nombre` de la tabla `productos` (uso `p.` para decir "de productos")                                       |
| `c.nombre`                 | La columna `nombre` de la tabla `categorias` (uso `c.` para decir "de categorias")                                     |
| `AS producto`              | Renombra `p.nombre` a "producto" en el resultado (solo visual, no cambia la tabla)                                     |
| `AS categoria`             | Renombra `c.nombre` a "categoria" en el resultado                                                                      |
| `p.precio`                 | La columna `precio` de productos (no necesita `AS` porque no hay ambigüedad)                                           |

> **¿Por qué usar `p.` y `c.`?** Porque ambas tablas tienen una columna `nombre`. Si escribes solo `nombre`, la DB no sabe cuál de las dos quieres y da error de **columna ambigua**.

| producto     | precio | categoria |
| ------------ | ------ | --------- |
| Agua 1L      | 990    | Bebidas   |
| Coca Cola 2L | 1990   | Bebidas   |
| Papas Fritas | 1500   | Snacks    |
| Yogurt       | 890    | Lácteos   |
| Leche 1L     | 1200   | Lácteos   |

> "Galletas" no aparece porque tiene `id_categoria = NULL` (no hay coincidencia).

### 12.4 Solo JOIN (sin INNER)

`JOIN` solo, sin escribir `INNER`, funciona igual:

```sql
SELECT p.nombre, c.nombre AS categoria
FROM productos p
JOIN categorias c ON p.id_categoria = c.id;
```

> `JOIN` = `INNER JOIN` (son sinónimos).

---

## 13) LEFT JOIN — todo de la izquierda

### 13.1 ¿Qué hace?

Devuelve **todas las filas de la tabla izquierda**, y las coincidencias de la derecha. Si no hay coincidencia, pone `NULL`.

### 13.2 Ejemplo: todos los productos, con o sin categoría

```sql
SELECT
  p.nombre AS producto,
  c.nombre AS categoria
FROM productos p
LEFT JOIN categorias c ON p.id_categoria = c.id;
```

**Explicación letra por letra:**

| Fragmento                  | Significado                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------- |
| `FROM productos p`         | Tabla principal (izquierda): `productos` con apodo `p`                                            |
| `LEFT JOIN categorias c`   | Uno con `categorias` (apodo `c`), pero **mantengo todas las filas de la izquierda** (`productos`) |
| `ON p.id_categoria = c.id` | La condición: une donde `id_categoria` del producto coincida con `id` de la categoría             |
| `p.nombre AS producto`     | Nombre del producto, renombrado a "producto"                                                      |
| `c.nombre AS categoria`    | Nombre de la categoría. Si no hay match, será **NULL**                                            |

> La diferencia con `INNER JOIN`: aquí `LEFT JOIN` dice "muéstrame TODOS los productos, y si alguno no tiene categoría, pon NULL en vez de esconderlo".

| producto     | categoria |
| ------------ | --------- |
| Agua 1L      | Bebidas   |
| Coca Cola 2L | Bebidas   |
| Papas Fritas | Snacks    |
| Yogurt       | Lácteos   |
| Leche 1L     | Lácteos   |
| **Galletas** | **NULL**  |

> Galletas ahora sí aparece, con categoría `NULL`.

### 13.3 ¿Cuándo usar LEFT JOIN?

Cuando quieres ver **todos los registros** de una tabla, incluso si no tienen relación con la otra.

Ejemplos:

- Todos los clientes, hayan comprado o no.
- Todos los productos, tengan categoría o no.

### 13.4 Encontrar huérfanos (filas sin relación)

```sql
-- Productos sin categoría
SELECT p.nombre
FROM productos p
LEFT JOIN categorias c ON p.id_categoria = c.id
WHERE c.id IS NULL;
```

---

## 14) RIGHT JOIN — todo de la derecha

### 14.1 ¿Qué hace?

Es el espejo de `LEFT JOIN`. Devuelve **todas las filas de la tabla derecha**, y las coincidencias de la izquierda.

### 14.2 Ejemplo: todas las categorías, tengan productos o no

```sql
SELECT
  c.nombre AS categoria,
  p.nombre AS producto
FROM productos p
RIGHT JOIN categorias c ON p.id_categoria = c.id;
```

**Explicación letra por letra:**

| Fragmento                  | Significado                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------ |
| `FROM productos p`         | Tabla izquierda: `productos` con apodo `p`                                                       |
| `RIGHT JOIN categorias c`  | Uno con `categorias` (apodo `c`), pero **mantengo todas las filas de la derecha** (`categorias`) |
| `ON p.id_categoria = c.id` | Misma condición: une por la FK                                                                   |
| `c.nombre AS categoria`    | Nombre de la categoría (siempre tendrá valor porque es la tabla "protegida" por RIGHT)           |
| `p.nombre AS producto`     | Nombre del producto. Si una categoría no tiene productos → **NULL**                              |

| categoria | producto     |
| --------- | ------------ |
| Bebidas   | Agua 1L      |
| Bebidas   | Coca Cola 2L |
| Snacks    | Papas Fritas |
| Lácteos   | Yogurt       |
| Lácteos   | Leche 1L     |

> Si existiera una categoría sin productos, aparecería con producto `NULL`.

### 14.3 En la práctica

`RIGHT JOIN` se usa poco. Generalmente puedes invertir el orden de las tablas y usar `LEFT JOIN`:

```sql
-- Esto es equivalente al RIGHT JOIN anterior
SELECT c.nombre AS categoria, p.nombre AS producto
FROM categorias c
LEFT JOIN productos p ON p.id_categoria = c.id;
```

---

## 15) FULL JOIN — todo de ambas tablas

### 15.1 ¿Qué hace?

Devuelve **todas las filas de ambas tablas**. Donde no hay coincidencia, pone `NULL`.

### 15.2 Ejemplo

```sql
SELECT
  p.nombre AS producto,
  c.nombre AS categoria
FROM productos p
FULL JOIN categorias c ON p.id_categoria = c.id;
```

**Explicación letra por letra:**

| Fragmento                  | Significado                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| `FROM productos p`         | Tabla izquierda: `productos`                                          |
| `FULL JOIN categorias c`   | Uno con `categorias`, **manteniendo todas las filas de AMBAS tablas** |
| `ON p.id_categoria = c.id` | Condición de unión (igual que siempre)                                |

**Resultado:**

- Producto con categoría → muestra ambos datos.
- Producto sin categoría (Galletas) → muestra producto, categoría = `NULL`.
- Categoría sin productos → muestra categoría, producto = `NULL`.
- Es la unión más "generosa": no esconde nada.

### 15.3 ¿Cuándo usar FULL JOIN?

Cuando necesitas ver **todo** de ambos lados, sin perder nada. Es poco común en aplicaciones normales, pero útil para auditorías o reportes.

---

## 16) Resumen visual de los JOIN

```
INNER JOIN          LEFT JOIN           RIGHT JOIN          FULL JOIN
┌───┬───┐          ┌───┬───┐          ┌───┬───┐          ┌───┬───┐
│ A │ B │          │ A │ B │          │ A │ B │          │ A │ B │
│   │███│          │███│███│          │   │███│          │███│███│
│   │███│          │███│███│          │███│███│          │███│███│
│   │   │          │███│   │          │███│███│          │███│███│
└───┴───┘          └───┴───┘          └───┴───┘          └───┴───┘
Solo coincidencias  Todo A + coinc.    Coinc. + todo B    Todo A + todo B
```

| JOIN         | Tabla izquierda | Tabla derecha  | Sin coincidencia          |
| ------------ | --------------- | -------------- | ------------------------- |
| `INNER JOIN` | Solo con match  | Solo con match | No aparece                |
| `LEFT JOIN`  | **Todas**       | Solo con match | NULL en derecha           |
| `RIGHT JOIN` | Solo con match  | **Todas**      | NULL en izquierda         |
| `FULL JOIN`  | **Todas**       | **Todas**      | NULL en el lado sin match |

---

## 17) JOIN con más de 2 tablas

### 17.1 Encadenar JOINs

Puedes unir 3, 4 o más tablas encadenando `JOIN`:

```sql
SELECT
  v.id AS venta,
  v.fecha,
  c.nombre AS cliente,
  p.nombre AS producto,
  v.cantidad,
  cat.nombre AS categoria
FROM ventas v
INNER JOIN clientes c ON v.id_cliente = c.id
INNER JOIN productos p ON v.id_producto = p.id
INNER JOIN categorias cat ON p.id_categoria = cat.id;
```

**Explicación letra por letra:**

| Fragmento                    | Significado                                                                               |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| `FROM ventas v`              | Tabla principal: `ventas` con apodo **`v`**                                               |
| `INNER JOIN clientes c`      | Uno ventas con `clientes` (apodo **`c`**)                                                 |
| `ON v.id_cliente = c.id`     | Condición: "el `id_cliente` de la venta debe coincidir con el `id` del cliente"           |
| `INNER JOIN productos p`     | También uno con `productos` (apodo **`p`**)                                               |
| `ON v.id_producto = p.id`    | Condición: "el `id_producto` de la venta debe coincidir con el `id` del producto"         |
| `INNER JOIN categorias cat`  | También uno con `categorias` (apodo **`cat`**, no `c` porque `c` ya se usó para clientes) |
| `ON p.id_categoria = cat.id` | Condición: "la categoría del producto debe coincidir con el `id` de categorías"           |
| `v.id AS venta`              | El ID de la venta, renombrado a "venta"                                                   |
| `v.fecha`                    | La fecha viene de la tabla ventas                                                         |
| `c.nombre AS cliente`        | El nombre del cliente (de la tabla `clientes`)                                            |
| `p.nombre AS producto`       | El nombre del producto (de la tabla `productos`)                                          |
| `v.cantidad`                 | La cantidad viene de ventas                                                               |
| `cat.nombre AS categoria`    | El nombre de la categoría (de la tabla `categorias`)                                      |

> **¿Por qué `cat` y no `c`?** Porque `c` ya se usó para `clientes`. Cada alias debe ser **único** en la consulta. Puedes usar cualquier nombre: `cat`, `ca`, `categ`, etc.

| venta | fecha      | cliente    | producto     | cantidad | categoria |
| ----- | ---------- | ---------- | ------------ | -------- | --------- |
| 1     | 2026-02-01 | Ana López  | Agua 1L      | 3        | Bebidas   |
| 2     | 2026-02-01 | Ana López  | Papas Fritas | 2        | Snacks    |
| 3     | 2026-02-02 | Pedro Soto | Coca Cola 2L | 1        | Bebidas   |
| 4     | 2026-02-03 | María Díaz | Yogurt       | 5        | Lácteos   |
| 5     | 2026-02-03 | Ana López  | Coca Cola 2L | 2        | Bebidas   |

### 17.2 Mezclando tipos de JOIN

```sql
SELECT
  c.nombre AS cliente,
  v.id AS venta,
  p.nombre AS producto
FROM clientes c
LEFT JOIN ventas v ON v.id_cliente = c.id
LEFT JOIN productos p ON v.id_producto = p.id;
```

- Muestra **todos** los clientes, incluso los que no compraron (Juan Pérez aparece con venta y producto `NULL`).

---

## 18) JOIN con agregación

### 18.1 Total de ventas por cliente

```sql
SELECT
  c.nombre AS cliente,
  COUNT(v.id) AS total_compras,
  SUM(v.cantidad) AS unidades_totales
FROM clientes c
LEFT JOIN ventas v ON v.id_cliente = c.id
GROUP BY c.nombre
ORDER BY total_compras DESC;
```

| cliente    | total_compras | unidades_totales |
| ---------- | ------------- | ---------------- |
| Ana López  | 3             | 7                |
| Pedro Soto | 1             | 1                |
| María Díaz | 1             | 5                |
| Juan Pérez | 0             | NULL             |

### 18.2 Ingreso total por producto

```sql
SELECT
  p.nombre AS producto,
  SUM(v.cantidad * p.precio) AS ingreso_total
FROM productos p
INNER JOIN ventas v ON v.id_producto = p.id
GROUP BY p.nombre
ORDER BY ingreso_total DESC;
```

### 18.3 Categoría más vendida

```sql
SELECT
  cat.nombre AS categoria,
  SUM(v.cantidad) AS unidades_vendidas
FROM ventas v
INNER JOIN productos p ON v.id_producto = p.id
INNER JOIN categorias cat ON p.id_categoria = cat.id
GROUP BY cat.nombre
ORDER BY unidades_vendidas DESC
LIMIT 1;
```

---

## 19) Orden de ejecución de una consulta

> Aunque escribes `SELECT` primero, la DB **ejecuta** en este orden:

| Paso | Cláusula           | Qué hace                    |
| ---- | ------------------ | --------------------------- |
| 1    | `FROM` / `JOIN`    | Define las tablas y las une |
| 2    | `WHERE`            | Filtra filas individuales   |
| 3    | `GROUP BY`         | Agrupa filas                |
| 4    | `HAVING`           | Filtra grupos               |
| 5    | `SELECT`           | Elige columnas y calcula    |
| 6    | `DISTINCT`         | Elimina duplicados          |
| 7    | `ORDER BY`         | Ordena resultados           |
| 8    | `LIMIT` / `OFFSET` | Recorta cantidad de filas   |

> Esto explica por qué no puedes usar un alias del `SELECT` en el `WHERE` (se ejecuta después).

---

## 20) Errores comunes al consultar

**Error 1: Columna ambigua (sin alias de tabla)**
❌ `SELECT nombre FROM productos JOIN categorias ON ...`
→ ¿`nombre` de qué tabla? Ambas tienen `nombre`.
✅ `SELECT p.nombre FROM productos p JOIN categorias c ON ...`

**Error 2: Usar WHERE en vez de HAVING**
❌ `SELECT id_cat, COUNT(*) FROM productos GROUP BY id_cat WHERE COUNT(*) > 1;`
✅ `SELECT id_cat, COUNT(*) FROM productos GROUP BY id_cat HAVING COUNT(*) > 1;`

**Error 3: Olvidar GROUP BY con funciones de agregación**
❌ `SELECT id_categoria, COUNT(*) FROM productos;`
✅ `SELECT id_categoria, COUNT(*) FROM productos GROUP BY id_categoria;`

**Error 4: Usar = NULL en vez de IS NULL**
❌ `WHERE email = NULL`
✅ `WHERE email IS NULL`

**Error 5: JOIN sin ON**
❌ `SELECT * FROM productos JOIN categorias;`
→ Sin `ON` hace un producto cartesiano (cada fila con cada fila).
✅ `SELECT * FROM productos JOIN categorias ON productos.id_categoria = categorias.id;`

**Error 6: Confundir LEFT JOIN con INNER JOIN**
Si usas `LEFT JOIN` pero filtras por una columna de la tabla derecha en el `WHERE`, se comporta como `INNER JOIN`:
❌ `... LEFT JOIN categorias c ON ... WHERE c.nombre = 'Bebidas';`
✅ `... LEFT JOIN categorias c ON ... AND c.nombre = 'Bebidas';`
(Mover la condición al `ON` para mantener el efecto del LEFT JOIN.)

---

## 21) Diccionario de SELECT y JOIN

- **SELECT**: elige qué columnas o datos mostrar.
- **FROM**: indica de qué tabla(s) leer.
- **WHERE**: filtra filas antes de agrupar.
- **ORDER BY**: ordena los resultados (ASC/DESC).
- **LIMIT**: limita la cantidad de filas devueltas.
- **OFFSET**: salta filas (para paginación).
- **DISTINCT**: elimina filas duplicadas.
- **AS**: alias, nombre temporal para columnas o tablas.
- **COUNT / SUM / AVG / MIN / MAX**: funciones de agregación.
- **GROUP BY**: agrupa filas con el mismo valor.
- **HAVING**: filtra grupos (se usa con GROUP BY).
- **JOIN**: combina filas de dos o más tablas.
- **INNER JOIN**: solo filas con coincidencia en ambas tablas.
- **LEFT JOIN**: todas las filas de la izquierda + coincidencias de la derecha.
- **RIGHT JOIN**: coincidencias de la izquierda + todas las filas de la derecha.
- **FULL JOIN**: todas las filas de ambas tablas, con o sin coincidencia.
- **ON**: condición de unión entre tablas (generalmente FK = PK).
- **Subconsulta**: un SELECT dentro de otro SELECT.
- **Producto cartesiano**: JOIN sin ON → cada fila con cada fila (casi nunca deseado).
