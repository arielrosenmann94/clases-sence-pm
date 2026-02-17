<!-- =========================================================
Archivo: sql_insert.md
Tema: SQL Básico — INSERT: insertar datos en tablas
========================================================= -->

# SQL Básico (curso) — INSERT: insertar datos en tablas

Este documento cubre todo lo necesario para **insertar datos** en tablas existentes:

1. Sintaxis básica de `INSERT INTO`
2. Insertar una fila completa
3. Insertar especificando columnas
4. Insertar varias filas a la vez
5. Usar `DEFAULT` en INSERT
6. Insertar con datos de otra tabla (`INSERT INTO … SELECT`)
7. Insertar con `RETURNING` (obtener lo insertado)
8. Manejo de conflictos (`ON CONFLICT`)
9. Orden de inserción cuando hay FK
10. Errores comunes al insertar

> Enfoque: **simple, pedagógico y práctico**.
> Pensado para estudiantes que recién comienzan.

---

## 0) Idea base

- `INSERT` agrega **filas nuevas** a una tabla.
- Cada fila debe respetar:
  - Los **tipos de datos** de cada columna.
  - Las **restricciones** (PK, FK, NOT NULL, UNIQUE, CHECK, etc.).
- Si algo no cumple → la base de datos **rechaza** la inserción con un error.

---

## ⚙️ Preparación: tablas para practicar

> **Copia y ejecuta este bloque ANTES de probar los ejemplos del documento.**
> Así tendrás las tablas listas para ir probando cada sección.

```sql
-- =============================================
-- EJECUTAR ESTO PRIMERO para poder practicar
-- (puedes ejecutar este bloque las veces que quieras,
--  el DROP borra las tablas si ya existen)
-- =============================================

-- Borrar tablas si ya existen (orden: hijas primero, padres después)
DROP TABLE IF EXISTS productos_baratos CASCADE;
DROP TABLE IF EXISTS productos_respaldo CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- Tabla padre: categorías
CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

-- Tabla hija: productos (con FK hacia categorías)
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  precio NUMERIC(10,2),
  stock INT DEFAULT 0,
  activo BOOLEAN DEFAULT true,
  id_categoria INT,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

-- Tabla con ID autogenerado
CREATE TABLE clientes (
  id BIGSERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  rut VARCHAR(12)
);

-- Tabla para practicar INSERT...SELECT (sección 6)
CREATE TABLE productos_respaldo (
  id INT,
  nombre VARCHAR(50),
  precio NUMERIC(10,2)
);

CREATE TABLE productos_baratos (
  id INT,
  nombre VARCHAR(50),
  precio NUMERIC(10,2)
);
```

> ⚠️ Si quieres empezar de cero (borrar todo y volver a crear), ejecuta:
>
> ```sql
> DROP TABLE IF EXISTS productos_baratos, productos_respaldo, productos, categorias, clientes CASCADE;
> ```
>
> Y luego vuelve a ejecutar el bloque de arriba.

---

## 1) Sintaxis básica

### 1.1 Fórmula general

```sql
INSERT INTO nombre_tabla (columna1, columna2, columna3)
VALUES (valor1, valor2, valor3);
```

- `INSERT INTO`: indica en qué tabla insertar.
- `(columna1, columna2, ...)`: lista de columnas a las que darás valor.
- `VALUES (...)`: los valores en el **mismo orden** que las columnas.

### 1.2 Reglas de los valores

| Tipo de dato       | Cómo escribir el valor | Ejemplo                 |
| ------------------ | ---------------------- | ----------------------- |
| `INT` / `NUMERIC`  | Sin comillas           | `42`, `3.14`            |
| `VARCHAR` / `TEXT` | Entre comillas simples | `'Coca Cola'`           |
| `DATE`             | Entre comillas simples | `'2026-02-10'`          |
| `TIMESTAMP`        | Entre comillas simples | `'2026-02-10 15:30:00'` |
| `BOOLEAN`          | Sin comillas           | `true`, `false`         |
| `NULL`             | Sin comillas           | `NULL`                  |

> ⚠️ Siempre comillas **simples** (`'texto'`), nunca dobles (`"texto"`).
> Las comillas dobles en SQL se usan para nombres de objetos, no para valores.

---

## 2) Insertar una fila completa

Si das valores a **todas** las columnas (en el orden en que fueron creadas), puedes omitir la lista de columnas:

```sql
INSERT INTO categorias
VALUES (1, 'Bebidas');
```

Equivale a:

```sql
INSERT INTO categorias (id, nombre)
VALUES (1, 'Bebidas');
```

> ⚠️ Aunque funciona, es **mejor práctica** siempre escribir las columnas.
> Si alguien agrega una columna nueva a la tabla, el INSERT sin columnas puede fallar.

---

## 3) Insertar especificando columnas (recomendado)

### 3.1 Ejemplo básico

```sql
INSERT INTO productos (id, nombre, precio)
VALUES (1, 'Agua 1L', 990);
```

- Solo insertas las columnas que necesitas.
- Las columnas no mencionadas reciben `NULL` o su `DEFAULT`.

### 3.2 Omitiendo columnas opcionales

Supongamos esta tabla:

```sql
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  precio NUMERIC(10,2),
  activo BOOLEAN DEFAULT true
);
```

Puedes insertar sin `precio` ni `activo`:

```sql
INSERT INTO productos (id, nombre)
VALUES (1, 'Agua 1L');
```

**Resultado:**

| id  | nombre  | precio | activo |
| --- | ------- | ------ | ------ |
| 1   | Agua 1L | NULL   | true   |

- `precio` queda `NULL` (no tiene DEFAULT).
- `activo` queda `true` (tiene DEFAULT).

### 3.3 El orden de las columnas lo decides tú

No necesitas seguir el orden de la tabla:

```sql
INSERT INTO productos (nombre, id, precio)
VALUES ('Jugo 1L', 2, 1500);
```

Lo importante es que los **valores coincidan** con el orden de las columnas que escribiste.

---

## 4) Insertar varias filas a la vez

En lugar de hacer un INSERT por cada fila, puedes insertar múltiples filas en una sola sentencia:

```sql
INSERT INTO categorias (id, nombre)
VALUES
  (1, 'Bebidas'),
  (2, 'Snacks'),
  (3, 'Lácteos'),
  (4, 'Limpieza');
```

- Cada fila va entre paréntesis.
- Se separan por comas.
- Solo un `;` al final.

> ✅ Esto es más rápido y más limpio que hacer 4 INSERT separados.

### 4.1 Ejemplo con más columnas

```sql
INSERT INTO productos (id, nombre, precio, id_categoria)
VALUES
  (1, 'Agua 1L',    990,  1),
  (2, 'Coca Cola',  1290, 1),
  (3, 'Papas Lay',  1500, 2),
  (4, 'Yogurt',     890,  3);
```

---

## 5) Usar DEFAULT en INSERT

### 5.1 La palabra clave DEFAULT

Puedes usar `DEFAULT` como valor para que la base de datos use el valor por defecto definido:

```sql
INSERT INTO productos (id, nombre, precio, activo)
VALUES (5, 'Galletas', 800, DEFAULT);
```

- `activo` tomará el valor `DEFAULT` definido en la tabla (ej: `true`).

### 5.2 DEFAULT para columnas autogeneradas

Si la PK es `SERIAL` o `BIGSERIAL`, usas `DEFAULT` para que la DB genere el ID:

```sql
-- Tabla con ID autogenerado
CREATE TABLE clientes (
  id BIGSERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

INSERT INTO clientes (id, nombre)
VALUES (DEFAULT, 'Ana López');
```

O simplemente omites la columna `id`:

```sql
INSERT INTO clientes (nombre)
VALUES ('Ana López');
```

Ambas formas son equivalentes.

---

## 6) INSERT con datos de otra tabla (INSERT INTO … SELECT)

### 6.1 Copiar datos de una tabla a otra

Puedes insertar filas que vienen de un `SELECT` en vez de escribir los valores a mano:

```sql
INSERT INTO productos_respaldo (id, nombre, precio)
SELECT id, nombre, precio
FROM productos;
```

- Copia **todas** las filas de `productos` a `productos_respaldo`.
- Las columnas del `SELECT` deben coincidir en cantidad y tipo con las del `INSERT`.

### 6.2 Copiar con filtro

```sql
INSERT INTO productos_baratos (id, nombre, precio)
SELECT id, nombre, precio
FROM productos
WHERE precio < 1000;
```

- Solo copia los productos con precio menor a 1000.

### 6.3 Copiar transformando datos

```sql
INSERT INTO reporte_ventas (producto, total)
SELECT nombre, precio * cantidad
FROM detalle_venta;
```

- Puedes usar expresiones y cálculos en el `SELECT`.

---

## 7) RETURNING — obtener lo que se insertó

### 7.1 ¿Para qué sirve?

En PostgreSQL, puedes agregar `RETURNING` para que el INSERT te devuelva las filas insertadas. Muy útil cuando la DB genera valores automáticos (como IDs).

### 7.2 Obtener el ID generado

```sql
INSERT INTO clientes (nombre)
VALUES ('Pedro Soto')
RETURNING id;
```

**Resultado:** te muestra el `id` que la DB asignó (ej: `1`).

### 7.3 Obtener varias columnas

```sql
INSERT INTO clientes (nombre)
VALUES ('María Díaz')
RETURNING id, nombre;
```

### 7.4 Obtener todo lo insertado

```sql
INSERT INTO clientes (nombre)
VALUES ('Juan Pérez')
RETURNING *;
```

> `RETURNING` es exclusivo de PostgreSQL (no todos los motores lo tienen).

---

## 8) Manejo de conflictos — ON CONFLICT (UPSERT)

### 8.1 ¿Qué problema resuelve?

Si intentas insertar una fila con un valor PK o UNIQUE que **ya existe**, la DB da error. `ON CONFLICT` te permite decidir qué hacer en ese caso.

### 8.2 Ignorar si ya existe (DO NOTHING)

```sql
INSERT INTO categorias (id, nombre)
VALUES (1, 'Bebidas')
ON CONFLICT (id) DO NOTHING;
```

- Si `id = 1` ya existe → no hace nada (no da error).
- Si no existe → inserta normalmente.

### 8.3 Actualizar si ya existe (DO UPDATE)

```sql
INSERT INTO productos (id, nombre, precio)
VALUES (1, 'Agua 1L', 1090)
ON CONFLICT (id) DO UPDATE
SET nombre = EXCLUDED.nombre,
    precio = EXCLUDED.precio;
```

- Si `id = 1` ya existe → actualiza `nombre` y `precio` con los valores nuevos.
- `EXCLUDED` hace referencia a los valores que intentaste insertar.

> Esto se conoce como **UPSERT** (UPDATE + INSERT).

### 8.4 ON CONFLICT con UNIQUE

También funciona con columnas UNIQUE:

```sql
INSERT INTO clientes (rut, nombre, email)
VALUES ('12345678-9', 'Ana', 'ana@mail.com')
ON CONFLICT (rut) DO UPDATE
SET email = EXCLUDED.email;
```

> `ON CONFLICT` es exclusivo de PostgreSQL.

---

## 9) Orden de inserción cuando hay FK

### 9.1 La regla de oro

> **Primero insertar en la tabla padre, después en la tabla hija.**

Si `productos` tiene FK hacia `categorias`:

```sql
-- ✅ Correcto: primero la tabla padre
INSERT INTO categorias (id, nombre) VALUES (1, 'Bebidas');
INSERT INTO productos (id, nombre, id_categoria) VALUES (1, 'Agua', 1);
```

```sql
-- ❌ Error: insertar hijo antes que padre
INSERT INTO productos (id, nombre, id_categoria) VALUES (1, 'Agua', 1);
-- ERROR: la categoría 1 no existe todavía
INSERT INTO categorias (id, nombre) VALUES (1, 'Bebidas');
```

### 9.2 Para eliminar es al revés

> **Primero borrar hijos, después padres.**

```sql
-- ✅ Correcto
DELETE FROM productos WHERE id_categoria = 1;
DELETE FROM categorias WHERE id = 1;
```

### 9.3 Con varias tablas encadenadas

Si tienes: `regiones` → `comunas` → `clientes`

Insertar en orden: `regiones` → `comunas` → `clientes`.
Borrar en orden: `clientes` → `comunas` → `regiones`.

---

## 10) Ejemplos prácticos completos

### 10.1 Sistema de tienda (flujo completo)

```sql
-- 1. Crear tablas
CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  precio NUMERIC(10,2) CHECK (precio > 0),
  id_categoria INT NOT NULL,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

-- 2. Insertar categorías (tabla padre primero)
INSERT INTO categorias (id, nombre) VALUES
  (1, 'Bebidas'),
  (2, 'Snacks');

-- 3. Insertar productos (tabla hija después)
INSERT INTO productos (id, nombre, precio, id_categoria) VALUES
  (1, 'Agua 1L', 990, 1),
  (2, 'Coca Cola 2L', 1990, 1),
  (3, 'Papas Fritas', 1500, 2);

-- 4. Verificar
SELECT * FROM categorias;
SELECT * FROM productos;
```

### 10.2 Insertar con ID autogenerado

```sql
CREATE TABLE alumnos (
  id BIGSERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  fecha_registro DATE DEFAULT CURRENT_DATE
);

INSERT INTO alumnos (nombre, email) VALUES
  ('Ana López', 'ana@mail.com'),
  ('Pedro Soto', 'pedro@mail.com'),
  ('María Díaz', 'maria@mail.com');

-- Ver qué IDs se generaron
SELECT * FROM alumnos;
```

---

## 11) Errores comunes al insertar

**Error 1: Violar PK (ID duplicado)**
❌ `INSERT INTO categorias (id, nombre) VALUES (1, 'Otra');` → si `id = 1` ya existe.
✅ Usar un ID diferente, o usar `SERIAL`/`BIGSERIAL` para autogenerar.

**Error 2: Violar FK (referencia inexistente)**
❌ `INSERT INTO productos (id, nombre, id_categoria) VALUES (1, 'X', 999);`
→ Si categoría 999 no existe.
✅ Primero insertar la categoría, o verificar que exista.

**Error 3: Violar NOT NULL**
❌ `INSERT INTO productos (id) VALUES (1);`
→ Si `nombre` es `NOT NULL` y no le diste valor.
✅ Siempre incluir las columnas obligatorias.

**Error 4: Violar UNIQUE**
❌ Insertar dos clientes con el mismo email si es UNIQUE.
✅ Verificar antes, o usar `ON CONFLICT`.

**Error 5: Violar CHECK**
❌ `INSERT INTO productos (id, nombre, precio) VALUES (1, 'X', -500);`
→ Si hay `CHECK (precio > 0)`.
✅ Asegurarse de que el valor cumpla la condición.

**Error 6: Tipo de dato incorrecto**
❌ `INSERT INTO productos (id, nombre, precio) VALUES (1, 'X', 'caro');`
→ `precio` espera un número, no texto.
✅ Usar el tipo correcto: `990` en vez de `'caro'`.

**Error 7: Comillas incorrectas**
❌ `VALUES (1, "Agua");` → comillas dobles no son para valores.
✅ `VALUES (1, 'Agua');` → comillas simples.

---

## 12) Diccionario de INSERT

- **INSERT INTO**: comando para agregar filas nuevas a una tabla.
- **VALUES**: lista de valores a insertar.
- **DEFAULT**: usa el valor por defecto definido en la tabla.
- **SERIAL / BIGSERIAL**: tipo de dato que autogenera IDs secuenciales.
- **RETURNING**: devuelve las filas insertadas (PostgreSQL).
- **ON CONFLICT**: define qué hacer si hay conflicto de PK o UNIQUE.
- **DO NOTHING**: ignora la fila conflictiva (no inserta ni actualiza).
- **DO UPDATE**: actualiza la fila existente con los valores nuevos (UPSERT).
- **EXCLUDED**: referencia a los valores que se intentaron insertar (en ON CONFLICT).
- **INSERT INTO … SELECT**: inserta filas que provienen de una consulta.
- **UPSERT**: patrón que combina INSERT + UPDATE en una sola operación.
