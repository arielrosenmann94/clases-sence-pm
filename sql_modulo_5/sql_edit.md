<!-- =========================================================
Archivo: sql_edit.md
Tema: SQL Básico — Editar y modificar tablas existentes
========================================================= -->

# SQL Básico (curso) — Editar tablas, columnas, tipos y restricciones

Este documento cubre todo lo necesario para **modificar** objetos que ya existen en la base de datos:

1. Renombrar tablas
2. Renombrar columnas
3. Agregar columnas (con y sin restricciones)
4. Eliminar columnas
5. Cambiar tipos de datos
6. Agregar y quitar restricciones (`NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`)
7. Agregar y quitar claves foráneas (FK)
8. Agregar y quitar claves primarias (PK)
9. Eliminar tablas (`DROP TABLE`)
10. Vaciar tablas (`TRUNCATE`)
11. Errores comunes al modificar tablas

> Enfoque: **simple, pedagógico y práctico**.
> Pensado para estudiantes que recién comienzan.

---

## 0) La sentencia ALTER TABLE

`ALTER TABLE` es el comando que permite **cambiar la estructura** de una tabla que ya existe, sin tener que borrarla y recrearla.

```sql
ALTER TABLE nombre_tabla
  acción;
```

> Idea simple: `ALTER TABLE` = "quiero cambiar algo de esta tabla".

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
DROP TABLE IF EXISTS venta_detalle CASCADE;
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- Tabla de categorías
CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL
);

-- Tabla de productos (con FK hacia categorías)
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  precio NUMERIC(10,2),
  id_categoria INT,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

-- Tabla de clientes
CREATE TABLE clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  telefono VARCHAR(20),
  dir VARCHAR(100),
  email VARCHAR(100)
);

-- Tabla de ventas (para practicar PK compuesta y FK)
CREATE TABLE ventas (
  id INT PRIMARY KEY,
  fecha DATE
);

CREATE TABLE venta_detalle (
  id_venta INT,
  id_producto INT,
  cantidad INT,
  PRIMARY KEY (id_venta, id_producto),
  FOREIGN KEY (id_venta) REFERENCES ventas(id),
  FOREIGN KEY (id_producto) REFERENCES productos(id)
);

-- Insertar datos de ejemplo para tener filas con las que trabajar
INSERT INTO categorias (id, nombre) VALUES
  (1, 'Bebidas'),
  (2, 'Snacks'),
  (3, 'Lácteos');

INSERT INTO productos (id, nombre, precio, id_categoria) VALUES
  (1, 'Agua 1L',      990,  1),
  (2, 'Coca Cola 2L', 1990, 1),
  (3, 'Papas Fritas', 1500, 2),
  (4, 'Yogurt',       890,  3);

INSERT INTO clientes (id, nombre, telefono, dir, email) VALUES
  (1, 'Ana López',  '+56912345678', 'Av. Siempre Viva 123', 'ana@mail.com'),
  (2, 'Pedro Soto', '+56987654321', 'Calle Falsa 456',      'pedro@mail.com');
```

> ⚠️ Si quieres empezar de cero (borrar todo y volver a crear), ejecuta:
>
> ```sql
> DROP TABLE IF EXISTS venta_detalle, ventas, productos, categorias, clientes CASCADE;
> ```
>
> Y luego vuelve a ejecutar el bloque de arriba.

---

## 1) Renombrar una tabla

Cambiar el nombre completo de la tabla:

```sql
ALTER TABLE productos
RENAME TO articulos;
```

- **Antes**: la tabla se llamaba `productos`.
- **Después**: se llama `articulos`.
- Todas las relaciones (FK) que apuntan a esta tabla **se actualizan automáticamente** en PostgreSQL.

> ⚠️ Cuidado: si tienes consultas SQL escritas a mano (en vistas, funciones, etc.), debes actualizarlas tú.

---

## 2) Renombrar columnas

Cambiar el nombre de una columna dentro de la tabla:

```sql
ALTER TABLE productos
RENAME COLUMN nombre TO nombre_producto;
```

- **Antes**: la columna se llamaba `nombre`.
- **Después**: se llama `nombre_producto`.
- Los datos no se pierden, solo cambia el nombre.

### 2.1 Ejemplo práctico

```sql
-- Renombrar varias columnas (una sentencia por cada una)
ALTER TABLE clientes
RENAME COLUMN telefono TO telefono_principal;

ALTER TABLE clientes
RENAME COLUMN dir TO direccion;
```

> Cada `RENAME COLUMN` es una sentencia separada.

---

## 3) Agregar columnas

### 3.1 Agregar una columna simple

```sql
ALTER TABLE productos
ADD COLUMN precio NUMERIC(10,2);
```

- La columna `precio` se agrega al final de la tabla.
- Todas las filas existentes tendrán `NULL` en esa columna.

### 3.2 Agregar columna con NOT NULL y DEFAULT

Si quieres que la columna sea obligatoria desde el inicio:

```sql
ALTER TABLE productos
ADD COLUMN activo BOOLEAN NOT NULL DEFAULT true;
```

- Las filas existentes recibirán el valor `true` automáticamente.
- Las filas nuevas que no especifiquen `activo` también serán `true`.

> ⚠️ Si agregas `NOT NULL` **sin** `DEFAULT`, la DB dará error si ya hay filas en la tabla (porque no sabe qué valor ponerles).

### 3.3 Agregar columna con UNIQUE

```sql
ALTER TABLE clientes
ADD COLUMN email VARCHAR(100) UNIQUE;
```

### 3.4 Agregar columna con CHECK

```sql
ALTER TABLE productos
ADD COLUMN stock INT CHECK (stock >= 0);
```

### 3.5 Agregar varias columnas a la vez

En PostgreSQL puedes hacer varias en una sola sentencia:

```sql
ALTER TABLE productos
ADD COLUMN color VARCHAR(30),
ADD COLUMN peso NUMERIC(6,2);
```

---

## 4) Eliminar columnas

### 4.1 Eliminar una columna

```sql
ALTER TABLE productos
DROP COLUMN color;
```

- La columna y **todos sus datos** se eliminan permanentemente.
- Si otra tabla tiene una FK que apunta a esa columna, la DB dará error.

### 4.2 Eliminar forzando dependencias (CASCADE)

```sql
ALTER TABLE productos
DROP COLUMN id_categoria CASCADE;
```

- `CASCADE` elimina también las FK y restricciones que dependan de esa columna.

> ⚠️ Usa `CASCADE` con **mucho cuidado** — puede borrar restricciones en otras tablas.

### 4.3 Eliminar solo si existe (IF EXISTS)

Para evitar error si la columna ya fue borrada:

```sql
ALTER TABLE productos
DROP COLUMN IF EXISTS color;
```

---

## 5) Cambiar el tipo de dato de una columna

### 5.1 Cambio simple (compatible)

Si el cambio es compatible (ej: hacer un `VARCHAR` más grande):

```sql
ALTER TABLE productos
ALTER COLUMN nombre TYPE VARCHAR(120);
```

- **Antes**: `VARCHAR(50)`.
- **Después**: `VARCHAR(120)`.
- Los datos existentes no se pierden.

### 5.2 Cambio con conversión (USING)

Si el tipo nuevo no es directamente compatible, necesitas indicar **cómo convertir**:

```sql
ALTER TABLE productos
ALTER COLUMN precio TYPE INT USING precio::INT;
```

- Convierte `NUMERIC` a `INT` truncando los decimales.
- `USING` le dice a la DB cómo transformar los datos existentes.

### 5.3 Convertir texto a número

```sql
ALTER TABLE clientes
ALTER COLUMN edad TYPE INT USING edad::INT;
```

> Solo funciona si **todos** los valores existentes son numéricos válidos. Si hay textos como `"abc"`, dará error.

### 5.4 Convertir número a texto

```sql
ALTER TABLE productos
ALTER COLUMN codigo TYPE VARCHAR(20) USING codigo::VARCHAR;
```

Este cambio es seguro porque cualquier número se puede representar como texto.

### 5.5 Reducir tamaño de VARCHAR

```sql
ALTER TABLE clientes
ALTER COLUMN nombre TYPE VARCHAR(30);
```

> ⚠️ Si alguna fila tiene un valor más largo que 30 caracteres → **error**. Primero verifica:

```sql
SELECT nombre, LENGTH(nombre)
FROM clientes
WHERE LENGTH(nombre) > 30;
```

---

## 6) Agregar y quitar NOT NULL

### 6.1 Hacer una columna obligatoria (SET NOT NULL)

```sql
ALTER TABLE productos
ALTER COLUMN nombre SET NOT NULL;
```

> ⚠️ Si ya hay filas con `NULL` en esa columna → **error**. Primero actualiza:

```sql
-- Paso 1: corregir los NULL existentes
UPDATE productos
SET nombre = 'Sin nombre'
WHERE nombre IS NULL;

-- Paso 2: ahora sí agregar la restricción
ALTER TABLE productos
ALTER COLUMN nombre SET NOT NULL;
```

### 6.2 Quitar la obligatoriedad (DROP NOT NULL)

```sql
ALTER TABLE productos
ALTER COLUMN nombre DROP NOT NULL;
```

- Ahora la columna acepta `NULL` nuevamente.

---

## 7) Agregar y quitar DEFAULT

### 7.1 Agregar un valor por defecto

```sql
ALTER TABLE productos
ALTER COLUMN activo SET DEFAULT true;
```

- Solo afecta filas **futuras**. Las filas existentes no cambian.

### 7.2 Quitar un valor por defecto

```sql
ALTER TABLE productos
ALTER COLUMN activo DROP DEFAULT;
```

- La columna ya no tiene valor por defecto; al insertar sin especificar, será `NULL`.

---

## 8) Agregar y quitar UNIQUE

### 8.1 Agregar UNIQUE a una columna existente

```sql
ALTER TABLE clientes
ADD CONSTRAINT uq_email UNIQUE (email);
```

- `uq_email` es el **nombre** que le das a la restricción (puedes elegir el que quieras).
- Si ya hay valores duplicados en la columna → **error**.

### 8.2 UNIQUE en varias columnas (combinación única)

```sql
ALTER TABLE venta_detalle
ADD CONSTRAINT uq_venta_producto UNIQUE (id_venta, id_producto);
```

- La **combinación** debe ser única, no cada columna por separado.

### 8.3 Quitar UNIQUE

```sql
ALTER TABLE clientes
DROP CONSTRAINT uq_email;
```

> Para saber el nombre de la restricción puedes usar `\d clientes` en psql o ver en DBeaver → Constraints.

---

## 9) Agregar y quitar CHECK

### 9.1 Agregar CHECK a una columna existente

```sql
ALTER TABLE productos
ADD CONSTRAINT chk_precio_positivo CHECK (precio > 0);
```

- Si ya hay filas que no cumplen la condición → **error**.

### 9.2 Quitar CHECK

```sql
ALTER TABLE productos
DROP CONSTRAINT chk_precio_positivo;
```

---

## 10) Agregar y quitar FK (clave foránea)

### 10.1 ¿Qué es una FK y por qué agregarla después?

Una **FK (Foreign Key / Clave Foránea)** es una restricción que dice:

> "El valor de esta columna **debe existir** en otra tabla."

**¿Por qué agregarla después de crear la tabla?** Porque en la vida real pasa mucho:

- Creaste las tablas sin relaciones y ahora quieres conectarlas.
- El profesor pidió "ahora agreguen la relación entre tablas".
- Olvidaste la FK al crear la tabla.
- Necesitas conectar una tabla nueva con una que ya existía.

### 10.2 Escenario completo (ejemplo real)

Supongamos que ya tienes estas tablas **sin relación**:

```sql
-- Ya existe
CREATE TABLE categorias (
  id INT PRIMARY KEY,
  nombre VARCHAR(50)
);

-- Ya existe, pero SIN FK
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  id_categoria INT        -- esta columna existe pero no tiene FK
);
```

Ahora quieres que `productos.id_categoria` **apunte** a `categorias.id`.

### 10.3 Agregar FK cuando la columna YA existe

```sql
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

**Explicación letra por letra:**

| Fragmento                    | Significado                                                                                                    |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `ALTER TABLE productos`      | "Quiero modificar la tabla `productos`"                                                                        |
| `ADD CONSTRAINT`             | "Voy a agregar una restricción (regla)"                                                                        |
| `fk_productos_categoria`     | El **nombre** que tú eliges para esta FK (puedes poner el que quieras, pero se recomienda `fk_tabla_relacion`) |
| `FOREIGN KEY (id_categoria)` | "La columna que será FK es `id_categoria`"                                                                     |
| `REFERENCES categorias(id)`  | "Debe apuntar a la columna `id` de la tabla `categorias`"                                                      |

> **Traducción humana:** "Cada valor de `productos.id_categoria` debe existir en `categorias.id`. Si alguien intenta poner una categoría que no existe → error."

### 10.4 Agregar FK cuando la columna NO existe todavía

Si la tabla `productos` no tiene la columna `id_categoria`, primero debes crearla:

```sql
-- Paso 1: crear la columna
ALTER TABLE productos
ADD COLUMN id_categoria INT;

-- Paso 2: crear la FK
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

> Son **dos sentencias separadas**: primero la columna, después la restricción.

### 10.5 Agregar FK obligatoria (NOT NULL)

Si quieres que **todo producto DEBA tener categoría** (no puede ser NULL):

```sql
-- Paso 1: crear la columna como obligatoria (con DEFAULT si ya hay datos)
ALTER TABLE productos
ADD COLUMN id_categoria INT NOT NULL DEFAULT 1;

-- Paso 2: crear la FK
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

> ⚠️ El `DEFAULT 1` asume que la categoría con `id = 1` ya existe. Sin DEFAULT, dará error si la tabla ya tiene filas.

### 10.6 FK con acción al borrar (ON DELETE)

¿Qué pasa si borras una categoría que tiene productos? Puedes definir el comportamiento:

```sql
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id)
ON DELETE CASCADE;
```

**Opciones de ON DELETE:**

| Opción                   | Qué hace al borrar la categoría                    | ¿Cuándo usarlo?                                  |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------ |
| `CASCADE`                | Borra también los productos de esa categoría       | Cuando los hijos no tienen sentido sin el padre  |
| `SET NULL`               | Pone `NULL` en `id_categoria` de los productos     | Cuando los productos pueden quedar sin categoría |
| `RESTRICT` (por defecto) | **No deja** borrar la categoría si tiene productos | Cuando quieres proteger los datos                |

```sql
-- Ejemplo con SET NULL
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id)
ON DELETE SET NULL;
```

### 10.7 ⚠️ Verificar datos ANTES de agregar la FK

Si la tabla ya tiene datos, puede haber valores "huérfanos" (que apuntan a categorías que no existen). La FK **no se puede crear** si hay datos inválidos.

**Paso 1: buscar datos huérfanos**

```sql
SELECT id, nombre, id_categoria
FROM productos
WHERE id_categoria IS NOT NULL
  AND id_categoria NOT IN (SELECT id FROM categorias);
```

Si esta consulta devuelve filas → esos datos son el problema.

**Paso 2: corregir los huérfanos**

Opción A — Ponerlos en NULL:

```sql
UPDATE productos
SET id_categoria = NULL
WHERE id_categoria NOT IN (SELECT id FROM categorias);
```

Opción B — Asignarles una categoría válida:

```sql
UPDATE productos
SET id_categoria = 1
WHERE id_categoria NOT IN (SELECT id FROM categorias);
```

**Paso 3: ahora sí crear la FK**

```sql
ALTER TABLE productos
ADD CONSTRAINT fk_productos_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id);
```

### 10.8 Quitar una FK

```sql
ALTER TABLE productos
DROP CONSTRAINT fk_productos_categoria;
```

> Para saber el nombre de la FK: usa `\d productos` en psql, o en DBeaver → tabla → pestaña "Constraints" / "Foreign Keys".

### 10.9 Ejemplo completo paso a paso

```sql
-- 1. Tenemos estas tablas sin relación
CREATE TABLE proveedores (
  id INT PRIMARY KEY,
  nombre VARCHAR(50)
);

CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  precio NUMERIC(10,2)
);

-- 2. Insertamos datos
INSERT INTO proveedores VALUES (1, 'Coca Cola Chile'), (2, 'Nestlé');
INSERT INTO productos VALUES (1, 'Coca Cola 2L', 1990), (2, 'Yogurt', 890);

-- 3. Ahora queremos conectar productos con proveedores
-- Paso A: agregar la columna
ALTER TABLE productos
ADD COLUMN id_proveedor INT;

-- Paso B: llenar los datos existentes
UPDATE productos SET id_proveedor = 1 WHERE nombre = 'Coca Cola 2L';
UPDATE productos SET id_proveedor = 2 WHERE nombre = 'Yogurt';

-- Paso C: crear la FK
ALTER TABLE productos
ADD CONSTRAINT fk_productos_proveedor
FOREIGN KEY (id_proveedor) REFERENCES proveedores(id);

-- 4. Verificar la estructura
-- En psql: \d productos
-- Debe mostrar la FK al final
```

---

## 11) Agregar y quitar PK (clave primaria)

### 11.1 Agregar PK (si la tabla no tiene)

```sql
ALTER TABLE logs
ADD CONSTRAINT pk_logs PRIMARY KEY (id);
```

> ⚠️ Requisitos: la columna no debe tener `NULL` ni valores duplicados.

### 11.2 Agregar PK compuesta

```sql
ALTER TABLE inscripciones
ADD CONSTRAINT pk_inscripciones PRIMARY KEY (id_alumno, id_curso);
```

### 11.3 Quitar PK

```sql
ALTER TABLE logs
DROP CONSTRAINT pk_logs;
```

> Si hay FK en otras tablas que apuntan a esta PK, primero debes quitar esas FK.

---

## 12) Eliminar una tabla completa (DROP TABLE)

### 12.1 Eliminar tabla

```sql
DROP TABLE productos;
```

- Elimina la tabla, su estructura y **todos sus datos**.
- Si hay FK en otras tablas que apuntan aquí → **error**.

### 12.2 Eliminar con CASCADE

```sql
DROP TABLE categorias CASCADE;
```

- Elimina la tabla **y** todas las FK que apuntan a ella (en otras tablas).

### 12.3 Eliminar solo si existe

```sql
DROP TABLE IF EXISTS productos;
```

- No da error si la tabla no existe.

### 12.4 Eliminar varias tablas

```sql
DROP TABLE IF EXISTS venta_detalle, productos, categorias;
```

> Orden importa: primero las tablas hijas (con FK), después las padres.

---

## 13) Vaciar una tabla sin borrarla (TRUNCATE)

### 13.1 Vaciar todos los datos

```sql
TRUNCATE TABLE productos;
```

- Borra **todas las filas**, pero la tabla sigue existiendo con su estructura.
- Es mucho más rápido que `DELETE FROM productos;` para tablas grandes.

### 13.2 Vaciar con CASCADE (si tiene FK)

```sql
TRUNCATE TABLE categorias CASCADE;
```

- También vacía las tablas que tienen FK apuntando a `categorias`.

### 13.3 Diferencia entre DELETE y TRUNCATE

| Característica               | `DELETE`         | `TRUNCATE`         |
| ---------------------------- | ---------------- | ------------------ |
| Borra filas específicas      | ✅ (con `WHERE`) | ❌ (borra todo)    |
| Velocidad en tablas grandes  | Lento            | Rápido             |
| Se puede deshacer (ROLLBACK) | ✅               | Depende del motor  |
| Activa triggers              | ✅               | ❌ (en PostgreSQL) |

---

## 14) Resumen de acciones ALTER TABLE

| Acción            | Sintaxis                                                                     |
| ----------------- | ---------------------------------------------------------------------------- |
| Renombrar tabla   | `ALTER TABLE t RENAME TO nuevo;`                                             |
| Renombrar columna | `ALTER TABLE t RENAME COLUMN col TO nuevo;`                                  |
| Agregar columna   | `ALTER TABLE t ADD COLUMN col TIPO;`                                         |
| Eliminar columna  | `ALTER TABLE t DROP COLUMN col;`                                             |
| Cambiar tipo      | `ALTER TABLE t ALTER COLUMN col TYPE NUEVO;`                                 |
| Agregar NOT NULL  | `ALTER TABLE t ALTER COLUMN col SET NOT NULL;`                               |
| Quitar NOT NULL   | `ALTER TABLE t ALTER COLUMN col DROP NOT NULL;`                              |
| Agregar DEFAULT   | `ALTER TABLE t ALTER COLUMN col SET DEFAULT val;`                            |
| Quitar DEFAULT    | `ALTER TABLE t ALTER COLUMN col DROP DEFAULT;`                               |
| Agregar UNIQUE    | `ALTER TABLE t ADD CONSTRAINT nombre UNIQUE (col);`                          |
| Quitar UNIQUE     | `ALTER TABLE t DROP CONSTRAINT nombre;`                                      |
| Agregar CHECK     | `ALTER TABLE t ADD CONSTRAINT nombre CHECK (cond);`                          |
| Quitar CHECK      | `ALTER TABLE t DROP CONSTRAINT nombre;`                                      |
| Agregar FK        | `ALTER TABLE t ADD CONSTRAINT nombre FOREIGN KEY (col) REFERENCES otra(id);` |
| Quitar FK         | `ALTER TABLE t DROP CONSTRAINT nombre;`                                      |
| Agregar PK        | `ALTER TABLE t ADD CONSTRAINT nombre PRIMARY KEY (col);`                     |
| Quitar PK         | `ALTER TABLE t DROP CONSTRAINT nombre;`                                      |

---

## 15) Errores comunes al editar tablas

**Error 1: SET NOT NULL cuando hay NULLs**
❌ `ALTER TABLE productos ALTER COLUMN precio SET NOT NULL;`
→ Falla si alguna fila tiene `precio = NULL`.
✅ Primero: `UPDATE productos SET precio = 0 WHERE precio IS NULL;`

**Error 2: Agregar FK con datos inválidos**
❌ `ALTER TABLE productos ADD FOREIGN KEY (id_cat) REFERENCES categorias(id);`
→ Falla si hay valores en `id_cat` que no existen en `categorias`.
✅ Primero: verificar y corregir los datos huérfanos.

**Error 3: Cambiar tipo incompatible sin USING**
❌ `ALTER TABLE t ALTER COLUMN edad TYPE INT;` (si `edad` es `VARCHAR`)
✅ `ALTER TABLE t ALTER COLUMN edad TYPE INT USING edad::INT;`

**Error 4: DROP TABLE sin considerar FK**
❌ `DROP TABLE categorias;` → Falla si `productos` tiene FK hacia ella.
✅ `DROP TABLE categorias CASCADE;` o primero quitar la FK.

**Error 5: Reducir VARCHAR sin verificar datos**
❌ `ALTER TABLE t ALTER COLUMN nombre TYPE VARCHAR(10);`
→ Falla si hay valores más largos que 10.
✅ Primero consultar: `SELECT nombre FROM t WHERE LENGTH(nombre) > 10;`

**Error 6: Agregar UNIQUE con duplicados**
❌ `ALTER TABLE t ADD CONSTRAINT uq UNIQUE (email);`
→ Falla si hay emails repetidos.
✅ Primero buscar duplicados:

```sql
SELECT email, COUNT(*)
FROM clientes
GROUP BY email
HAVING COUNT(*) > 1;
```

---

## 16) Diccionario de edición

- **ALTER TABLE**: modificar la estructura de una tabla existente.
- **RENAME**: cambiar nombre (tabla o columna).
- **ADD COLUMN**: agregar columna nueva.
- **DROP COLUMN**: eliminar columna (con sus datos).
- **ALTER COLUMN**: cambiar propiedades de una columna (tipo, null, default).
- **TYPE**: nuevo tipo de dato para una columna.
- **USING**: indica cómo convertir datos al cambiar tipo.
- **SET NOT NULL**: hacer obligatoria una columna.
- **DROP NOT NULL**: permitir NULL en una columna.
- **SET DEFAULT**: asignar valor por defecto.
- **DROP DEFAULT**: quitar valor por defecto.
- **ADD CONSTRAINT**: agregar una restricción (UNIQUE, CHECK, FK, PK).
- **DROP CONSTRAINT**: quitar una restricción por nombre.
- **CASCADE**: propagar la acción a objetos dependientes.
- **IF EXISTS**: evitar error si el objeto no existe.
- **DROP TABLE**: eliminar tabla completa (estructura + datos).
- **TRUNCATE**: vaciar datos sin eliminar la estructura.
