<!-- =========================================================
Archivo: sql_clase_interactiva.md
Tema: Clase — DML + Integridad Referencial + Transaccionalidad
AE3: Utilizar lenguaje DML para manipulación de datos.
========================================================= -->

# 🎮 SQL en Acción — Manipulación de Datos y Transaccionalidad

---

---

# 📚 PARTE 1 — TEORÍA (~60 min)

---

## 🗺️ ¿Qué vamos a aprender hoy?

| Tema                      | Pregunta clave                                         |
| ------------------------- | ------------------------------------------------------ |
| 🔤 DML                    | ¿Cómo agrego, cambio y borro datos?                    |
| 🔗 Integridad Referencial | ¿Cómo evito que mis datos se contradigan?              |
| 🏦 Principios ACID        | ¿Cómo garantizo que una operación compleja sea segura? |
| 🔄 Transacciones          | ¿Cómo confirmo o deshago cambios?                      |

---

---

## 1️⃣ DML — Data Manipulation Language

---

### ¿Qué es DML?

**DML** = **Data Manipulation Language** (Lenguaje de Manipulación de Datos).

Es la parte de SQL que nos permite **tocar los datos** dentro de las tablas.

> Hasta ahora aprendimos a **crear tablas** (DDL) y a **consultar datos** (SELECT).  
> Hoy pasamos de **leer** a **escribir**.

---

### Los 4 comandos DML

| Comando  | ¿Qué hace?                | Analogía                                 |
| -------- | ------------------------- | ---------------------------------------- |
| `INSERT` | Agrega filas nuevas       | Escribir un renglón nuevo en un cuaderno |
| `UPDATE` | Modifica filas existentes | Borrar con corrector y escribir encima   |
| `DELETE` | Elimina filas             | Arrancar la hoja del cuaderno            |
| `SELECT` | Lee datos                 | Leer el cuaderno sin tocarlo             |

> `SELECT` técnicamente es DML pero **no modifica nada**.
> Lo usamos para **verificar** lo que hicimos con los otros tres.

---

### DML vs DDL — No confundir

|              | **DML**                        | **DDL**                                  |
| ------------ | ------------------------------ | ---------------------------------------- |
| **Sigla**    | Data **Manipulation** Language | Data **Definition** Language             |
| **Afecta**   | Los **datos** (las filas)      | La **estructura** (las tablas, columnas) |
| **Comandos** | INSERT, UPDATE, DELETE         | CREATE, ALTER, DROP                      |
| **Analogía** | Escribir en el cuaderno        | Diseñar el cuaderno                      |

> **DDL** = crear/modificar/borrar **tablas**.  
> **DML** = crear/modificar/borrar **datos dentro de las tablas**.

---

### INSERT — Agregar datos

```sql
INSERT INTO nombre_tabla (columna1, columna2, columna3)
VALUES (valor1, valor2, valor3);
```

| Parte                          | Significado                     |
| ------------------------------ | ------------------------------- |
| `INSERT INTO nombre_tabla`     | ¿En qué tabla quiero insertar?  |
| `(columna1, columna2, ...)`    | ¿Qué columnas voy a llenar?     |
| `VALUES (valor1, valor2, ...)` | ¿Con qué valores? (mismo orden) |

#### Ejemplo concreto

```sql
INSERT INTO productos (nombre, precio, stock)
VALUES ('Coca-Cola 500ml', 990, 24);
```

> **Leámoslo en español**: _"Inserta en la tabla productos, en las columnas nombre, precio y stock, los valores Coca-Cola 500ml, 990 y 24."_

---

### INSERT — Varias filas a la vez

En lugar de repetir INSERT, podemos insertar múltiples filas con una sola sentencia:

```sql
INSERT INTO productos (nombre, precio, stock) VALUES
  ('Coca-Cola 500ml',  990, 24),
  ('Sprite 500ml',     890, 20),
  ('Papas Lays',      1200, 15);
```

- Cada fila va entre paréntesis `(...)`.
- Se separan por comas `,`.
- Un solo `;` al final.

---

### INSERT — ID Autogenerado

Cuando una columna es `SERIAL` (PostgreSQL) o `AUTO_INCREMENT` (MySQL), **no la incluimos** en el INSERT.

```sql
-- La columna "id" es SERIAL → la DB la genera sola
INSERT INTO productos (nombre, precio, stock)
VALUES ('Galletas', 800, 30);
-- El id se asigna automáticamente: 1, 2, 3, ...
```

**¿Por qué usamos IDs autogenerados?**

- Evitas duplicados → la DB garantiza que cada ID sea único.
- Es más rápido → no necesitas buscar "¿cuál fue el último ID?"
- Escala bien → con miles de registros, es imposible hacerlo a mano.

---

### UPDATE — Modificar datos

```sql
UPDATE nombre_tabla
SET columna = nuevo_valor
WHERE condición;
```

| Parte                 | Significado                           |
| --------------------- | ------------------------------------- |
| `UPDATE nombre_tabla` | ¿Qué tabla quiero modificar?          |
| `SET columna = valor` | ¿Qué columna cambio y a qué valor?    |
| `WHERE condición`     | ¿Cuáles filas? (¡NUNCA olvidar esto!) |

#### Ejemplo concreto

```sql
UPDATE productos
SET precio = 1090
WHERE nombre = 'Coca-Cola 500ml';
```

> **En español**: _"Actualiza la tabla productos, cambia el precio a 1090, pero solo donde el nombre sea Coca-Cola 500ml."_

---

### ⚠️ UPDATE sin WHERE — El error más caro del mundo

```sql
-- ❌ ESTO CAMBIA EL PRECIO DE TODOS LOS PRODUCTOS A 0
UPDATE productos SET precio = 0;
```

> **Un UPDATE sin WHERE afecta TODAS las filas de la tabla.**  
> En producción, esto puede significar perder datos de miles de clientes.

**Buena práctica 🔑**: Antes de un UPDATE, haz un SELECT con el mismo WHERE:

```sql
-- Primero verifico
SELECT * FROM productos WHERE nombre = 'Coca-Cola 500ml';

-- Si es correcto, recién ahí actualizo
UPDATE productos SET precio = 1090
WHERE nombre = 'Coca-Cola 500ml';
```

---

### UPDATE — Con cálculos

Podemos usar el valor actual de la columna para calcular el nuevo:

```sql
-- Aumentar un 10% el salario de todos los de IT
UPDATE empleados
SET salario = salario * 1.10
WHERE departamento = 'IT';
```

> `salario * 1.10` = salario actual + 10%.

---

### DELETE — Eliminar datos

```sql
DELETE FROM nombre_tabla
WHERE condición;
```

| Parte                      | Significado                           |
| -------------------------- | ------------------------------------- |
| `DELETE FROM nombre_tabla` | ¿De qué tabla quiero borrar?          |
| `WHERE condición`          | ¿Cuáles filas? (¡NUNCA olvidar esto!) |

#### Ejemplo concreto

```sql
DELETE FROM productos
WHERE nombre = 'Galletas';
```

> **En español**: _"Elimina de la tabla productos las filas donde el nombre sea Galletas."_

---

### ⚠️ DELETE sin WHERE — El otro error más caro

```sql
-- ❌ BORRA TODOS LOS REGISTROS DE LA TABLA
DELETE FROM productos;
```

> **Misma regla que UPDATE**: siempre verifica con SELECT antes de borrar.

---

### DELETE vs TRUNCATE vs DROP

| Comando            | ¿Qué hace?                             | ¿La tabla sigue existiendo? | ¿Se puede deshacer? |
| ------------------ | -------------------------------------- | --------------------------- | ------------------- |
| `DELETE` sin WHERE | Borra todas las **filas**              | ✅ Sí                       | ✅ Con ROLLBACK     |
| `TRUNCATE TABLE`   | Borra todas las **filas** (más rápido) | ✅ Sí                       | Depende del motor   |
| `DROP TABLE`       | Borra la **tabla completa**            | ❌ No                       | ❌ No               |

---

### AutoCommit — ¿Se guardan solos los cambios?

| Modo               | Comportamiento                                                    |
| ------------------ | ----------------------------------------------------------------- |
| `AutoCommit = ON`  | Cada sentencia se guarda **inmediatamente**. No hay vuelta atrás. |
| `AutoCommit = OFF` | Los cambios quedan **pendientes** hasta que confirmes o deshagas. |

> En Supabase, por defecto el AutoCommit está **ON**.

---

---

## 2️⃣ Integridad Referencial

---

### ¿Qué es la integridad referencial?

Es la regla que garantiza que **las relaciones entre tablas sean consistentes**.

> _"No puede existir un pedido de un cliente que no existe."_  
> _"No puede existir un producto en una categoría que no existe."_

La base de datos **nos protege**: si intentamos algo inválido, nos lanza un error.

---

### ¿Cómo funciona? — PK y FK

| Concepto             | ¿Qué es?                                        | Ejemplo                                               |
| -------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| **PK** (Primary Key) | El ID **único** de cada fila                    | `clientes.id = 1`                                     |
| **FK** (Foreign Key) | Un enlace que **apunta** a una PK de otra tabla | `pedidos.id_cliente = 1` → apunta a `clientes.id = 1` |

```
    ┌──────────────────┐
    │    clientes       │
    │  id (PK) │ nombre │        ┌───────────────────────┐
    │  ────────┼────────│        │      pedidos           │
    │     1    │ María  │◄───FK──│ id │ id_cliente │ total │
    │     2    │ Pedro  │        │  1 │     1      │  5000 │
    └──────────────────┘        │  2 │     2      │  3000 │
                                 └───────────────────────┘
```

> El `id_cliente` del pedido **debe existir** en la tabla `clientes`.
> Si intento poner `id_cliente = 999` y no existe → **ERROR**.

---

### Insertar CON integridad referencial

**La regla de oro del INSERT**:

> **Primero el padre, después el hijo.**

```sql
-- ✅ CORRECTO: primero la categoría (padre)
INSERT INTO categorias (nombre) VALUES ('Bebidas');

-- ✅ DESPUÉS el producto (hijo que apunta al padre)
INSERT INTO productos (nombre, precio, stock, id_categoria)
VALUES ('Agua 1L', 500, 50, 1);
```

```sql
-- ❌ ERROR: insertar hijo sin padre
INSERT INTO productos (nombre, precio, stock, id_categoria)
VALUES ('Agua 1L', 500, 50, 999);
-- ERROR: la categoría 999 NO existe → FK rechaza
```

---

### Actualizar CON integridad referencial

Al actualizar, la FK también nos protege:

```sql
-- ❌ ERROR: cambiar a una categoría que no existe
UPDATE productos SET id_categoria = 999
WHERE nombre = 'Agua 1L';

-- ✅ CORRECTO: cambiar a una categoría válida
UPDATE productos SET id_categoria = 2
WHERE nombre = 'Agua 1L';
```

---

### Eliminar CON integridad referencial

**La regla de oro del DELETE**:

> **Primero el hijo, después el padre.** (al revés que INSERT)

```sql
-- ❌ ERROR: borrar padre que tiene hijos
DELETE FROM clientes WHERE id = 1;
-- ERROR: hay pedidos que referencian a este cliente

-- ✅ CORRECTO: borrar hijos primero
DELETE FROM pedidos WHERE id_cliente = 1;
DELETE FROM clientes WHERE id = 1;
```

---

### ON DELETE CASCADE — Borrado automático en cascada

Si queremos que al borrar un padre **se borren automáticamente sus hijos**:

```sql
CREATE TABLE pedidos (
  id          SERIAL PRIMARY KEY,
  id_cliente  INT NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    ON DELETE CASCADE
);
```

| Opción               | ¿Qué pasa al borrar el padre?     | ¿Cuándo usarlo?                                 |
| -------------------- | --------------------------------- | ----------------------------------------------- |
| `RESTRICT` (default) | **No deja** borrar                | Cuando quieres proteger los datos               |
| `CASCADE`            | Borra los hijos automáticamente   | Cuando los hijos no tienen sentido sin el padre |
| `SET NULL`           | Pone `NULL` en la FK de los hijos | Cuando el hijo puede quedar "sin padre"         |

---

### Resumen visual: Orden de operaciones

```
INSERTAR:  Abuelos → Padres → Hijos → Nietos (Sin FK → Con FK)
ELIMINAR:  Nietos → Hijos → Padres → Abuelos (Con FK → Sin FK)
EDITAR:    Nietos → Hijos → Padres → Abuelos (Con FK → Sin FK) (previo a evaluación)
```

> Para construir, empiezo desde la base. Para demoler, desde arriba.

---

---

## 3️⃣ Principios ACID

---

### ¿Qué son las propiedades ACID?

Son las **4 reglas** que garantizan que las operaciones en una base de datos sean **confiables y seguras**.

---

### A — Atomicidad

> **"Todo o nada."**

Una transacción es una **unidad indivisible**: o se ejecutan **todas** las operaciones, o **ninguna**.

**Ejemplo**: Transferencia bancaria. Si el dinero sale de la cuenta A pero no llega a la cuenta B → sin atomicidad el dinero desaparece. Con atomicidad, la operación entera se deshace.

---

### C — Consistencia

> **"De un estado válido a otro estado válido."**

La base de datos siempre debe cumplir sus reglas (PK, FK, CHECK, NOT NULL) antes y después de cada transacción.

**Ejemplo**: Si una cuenta tiene `CHECK (saldo >= 0)`, una transferencia que dejaría el saldo en negativo **no se permite**.

---

### I — Aislamiento (Isolation)

> **"Las transacciones no se molestan entre sí."**

Si dos personas hacen operaciones al mismo tiempo, cada una ve la base de datos como si fuera la única trabajando.

---

### D — Durabilidad

> **"Una vez confirmado, es para siempre."**

Cuando haces `COMMIT`, los cambios se guardan de forma **permanente**, incluso si se corta la luz un segundo después.

---

### ACID en una tabla

| Principio          | Pregunta que responde    | Si NO existiera...                        |
| ------------------ | ------------------------ | ----------------------------------------- |
| **A**tomicidad     | ¿Se hizo todo?           | El dinero se pierde en una transferencia  |
| **C**onsistencia   | ¿Los datos son válidos?  | Saldos negativos, pedidos sin clientes    |
| **(I)**Aislamiento | ¿Se mezclan operaciones? | Ves datos "a medias" de otra persona      |
| **D**urabilidad    | ¿Se guardó de verdad?    | Confirmaste pero al reiniciar desapareció |

---

---

## 4️⃣ Transacciones en SQL

---

### ¿Qué es una transacción?

Una transacción es un **grupo de operaciones SQL** que se ejecutan como **una sola unidad**.

> Piensa en una transferencia bancaria:
>
> 1. Sacar dinero de la cuenta A.
> 2. Poner dinero en la cuenta B.
>
> Estas dos operaciones **deben ser una sola**: si falla una, la otra también debe deshacerse.

---

### Los 3 comandos de transacciones

| Comando    | ¿Qué hace?                  | Analogía                       |
| ---------- | --------------------------- | ------------------------------ |
| `BEGIN`    | Abre un "modo borrador"     | Abrir un documento sin guardar |
| `COMMIT`   | Guarda permanentemente      | Ctrl+S (guardar)               |
| `ROLLBACK` | Deshace todo desde el BEGIN | Ctrl+Z (deshacer todo)         |

```sql
BEGIN;      -- 🟢 Empieza la transacción

  -- operaciones SQL aquí...

COMMIT;     -- ✅ Confirmar: guardar todo de forma permanente
-- o --
ROLLBACK;   -- ❌ Deshacer: volver al estado antes del BEGIN
```

---

### Ejemplo: Transferencia bancaria SEGURA

```sql
BEGIN;
  UPDATE cuentas SET saldo = saldo - 200 WHERE id = 1;
  UPDATE cuentas SET saldo = saldo + 200 WHERE id = 2;
  SELECT * FROM cuentas WHERE id IN (1, 2);
COMMIT;
```

---

### Ejemplo: Algo salió mal → ROLLBACK

```sql
BEGIN;
  UPDATE cuentas SET saldo = saldo - 10000 WHERE id = 1;
  UPDATE cuentas SET saldo = saldo + 10000 WHERE id = 2;
  -- 😱 Transferí de más...
ROLLBACK;  -- Todo vuelve a como estaba
```

---

### ¿Cuándo usar transacciones?

| Situación                                              | ¿Necesito transacción? |
| ------------------------------------------------------ | ---------------------- |
| Insertar un solo registro                              | No necesariamente      |
| Transferencia bancaria (2+ operaciones)                | ✅ Siempre             |
| Actualizar varias tablas relacionadas                  | ✅ Recomendado         |
| Operaciones que si fallan a la mitad dejan datos rotos | ✅ Obligatorio         |

---

### Resumen Teoría

| Concepto           | Lo más importante                                     |
| ------------------ | ----------------------------------------------------- |
| **DML**            | INSERT (agregar), UPDATE (modificar), DELETE (borrar) |
| **WHERE**          | **Nunca olvidarlo** en UPDATE y DELETE                |
| **Buena práctica** | Siempre hacer SELECT antes de UPDATE/DELETE           |
| **Integridad**     | FK garantiza que las relaciones sean válidas          |
| **Orden INSERT**   | Padres → Hijos                                        |
| **Orden DELETE**   | Hijos → Padres                                        |
| **CASCADE**        | Borra hijos automáticamente al borrar el padre        |
| **ACID**           | Atomicidad, Consistencia, Aislamiento, Durabilidad    |
| **BEGIN/COMMIT**   | Agrupa operaciones y confirma                         |
| **ROLLBACK**       | Deshace todo si algo sale mal                         |

---

---

---

# 🎮 PARTE 2 — PRÁCTICA POR EQUIPOS (~2 horas)

> Vamos a trabajar **por equipos**.
> Cada equipo elige un nombre, se registra en la base de datos y trabaja junto en todos los desafíos.
> Al final veremos cómo les fue a todos.

---

## ⚙️ Setup: Preparar Supabase

> Ejecuten este bloque en el **SQL Editor** de Supabase para crear todas las tablas.

```sql
-- =============================================
-- 🛠️ SETUP COMPLETO — el profe ejecuta esto
-- =============================================

-- Limpiar todo
DROP TABLE IF EXISTS desafio_final CASCADE;
DROP TABLE IF EXISTS movimientos CASCADE;
DROP TABLE IF EXISTS cuentas_bancarias CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS pedidos_cascade CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS integrantes CASCADE;
DROP TABLE IF EXISTS equipos CASCADE;

-- ─────────────────────────────────────────────
-- 👥 Equipos (tabla padre)
-- ─────────────────────────────────────────────
CREATE TABLE equipos (
  id              SERIAL PRIMARY KEY,
  nombre_equipo   VARCHAR(50) NOT NULL UNIQUE,
  fecha_registro  TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────────
-- 🧑 Integrantes (tabla hija → equipos)
-- ─────────────────────────────────────────────
CREATE TABLE integrantes (
  id              SERIAL PRIMARY KEY,
  id_equipo       INT NOT NULL,
  nombre          VARCHAR(80) NOT NULL,
  fecha_registro  TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (id_equipo) REFERENCES equipos(id)
);

-- ─────────────────────────────────────────────
-- 🏪 Categorías
-- ─────────────────────────────────────────────
CREATE TABLE categorias (
  id          SERIAL PRIMARY KEY,
  nombre      VARCHAR(50) NOT NULL UNIQUE
);

-- ─────────────────────────────────────────────
-- 🏪 Productos
-- ─────────────────────────────────────────────
CREATE TABLE productos (
  id            SERIAL PRIMARY KEY,
  nombre        VARCHAR(80) NOT NULL,
  precio        NUMERIC(10,2) NOT NULL CHECK (precio > 0),
  stock         INT DEFAULT 0 CHECK (stock >= 0),
  id_categoria  INT,
  activo        BOOLEAN DEFAULT true,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

-- ─────────────────────────────────────────────
-- 👤 Clientes
-- ─────────────────────────────────────────────
CREATE TABLE clientes (
  id        SERIAL PRIMARY KEY,
  nombre    VARCHAR(80) NOT NULL,
  email     VARCHAR(120) UNIQUE NOT NULL,
  ciudad    VARCHAR(50) DEFAULT 'Santiago'
);

-- ─────────────────────────────────────────────
-- 📦 Pedidos
-- ─────────────────────────────────────────────
CREATE TABLE pedidos (
  id            SERIAL PRIMARY KEY,
  id_cliente    INT NOT NULL,
  id_producto   INT NOT NULL,
  cantidad      INT NOT NULL CHECK (cantidad > 0),
  total         NUMERIC(10,2),
  fecha_pedido  TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (id_cliente)  REFERENCES clientes(id),
  FOREIGN KEY (id_producto) REFERENCES productos(id)
);

-- ─────────────────────────────────────────────
-- 🏦 Cuentas bancarias
-- ─────────────────────────────────────────────
CREATE TABLE cuentas_bancarias (
  id        SERIAL PRIMARY KEY,
  titular   VARCHAR(80) NOT NULL,
  saldo     NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (saldo >= 0)
);

-- ─────────────────────────────────────────────
-- 💰 Movimientos bancarios
-- ─────────────────────────────────────────────
CREATE TABLE movimientos (
  id          SERIAL PRIMARY KEY,
  id_cuenta   INT NOT NULL,
  tipo        VARCHAR(20) NOT NULL,
  monto       NUMERIC(12,2) NOT NULL,
  fecha       TIMESTAMP DEFAULT NOW(),
  descripcion TEXT,
  FOREIGN KEY (id_cuenta) REFERENCES cuentas_bancarias(id)
);

-- ─────────────────────────────────────────────
-- 🏁 Registro del desafío final
-- ─────────────────────────────────────────────
CREATE TABLE desafio_final (
  id              SERIAL PRIMARY KEY,
  id_equipo       INT NOT NULL,
  paso            INT NOT NULL,
  descripcion     VARCHAR(200),
  fecha_completado TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (id_equipo) REFERENCES equipos(id)
);
```

---

---

## 🏁 Paso 0: Inscripción de Equipos (15 min)

Cada equipo va a practicar su **primer INSERT** registrándose en la base de datos.

Esto es un ejercicio real de SQL: van a insertar datos en dos tablas relacionadas
(`equipos` e `integrantes`) respetando la integridad referencial.

### Paso 0.1 — Registrar el equipo

> Cada equipo elige un nombre creativo y lo inserta.
> La columna `fecha_registro` se llena **automáticamente** con la fecha y hora actual — eso es lo que hace el `DEFAULT NOW()` que vimos en la teoría.

```sql
-- Cambien 'Mi Equipo Genial' por el nombre que eligieron
INSERT INTO equipos (nombre_equipo)
VALUES ('Mi Equipo Genial');
```

> **¿Por qué no escribimos la fecha?**
> Porque en la tabla `equipos` la columna `fecha_registro` tiene `DEFAULT NOW()`.
> Eso significa que si no le damos valor, PostgreSQL automáticamente pone la fecha y hora de este momento.

### Paso 0.2 — Verificar que el equipo quedó registrado

```sql
SELECT * FROM equipos;
```

> Fíjense: aparece su equipo con un **id automático** (gracias a `SERIAL`) y una **fecha automática** (gracias a `DEFAULT NOW()`).
> ¡Dos columnas que se llenaron solas!

### Paso 0.3 — Registrar a cada integrante

> Ahora cada integrante del equipo se registra.
> La tabla `integrantes` tiene una **FK hacia equipos**.
> Eso significa que el `id_equipo` que pongan **debe existir** en la tabla `equipos`.

```sql
-- Primero: buscar el id de su equipo
SELECT id, nombre_equipo FROM equipos;

-- Luego: cada integrante se inserta
-- (reemplacen el id_equipo y el nombre)
INSERT INTO integrantes (id_equipo, nombre)
VALUES (1, 'Nombre del integrante');
```

> **¿Qué pasa si pongo un id_equipo que no existe?**
> La FK lo impide. Pruébenlo:

```sql
-- Esto debería dar ERROR:
INSERT INTO integrantes (id_equipo, nombre)
VALUES (999, 'Fantasma');
-- ERROR: el equipo 999 no existe → integridad referencial en acción 🛡️
```

### Paso 0.4 — Ver todo el equipo junto

> Ahora hacemos un JOIN para ver los equipos con sus integrantes:

```sql
SELECT
  e.nombre_equipo,
  i.nombre AS integrante,
  i.fecha_registro
FROM equipos e
JOIN integrantes i ON e.id = i.id_equipo
ORDER BY e.nombre_equipo, i.nombre;
```

> ¿Se acuerdan del JOIN de la clase pasada?
> Aquí lo usamos para **unir** la información de dos tablas relacionadas.

---

---

## 🏪 Paso 1: Misión Kiosco — INSERT (20 min)

Cada equipo va a armar su sección del kiosco insertando categorías y productos.

### Paso 1.1 — Insertar categorías

> Solo **un integrante** del equipo inserta las categorías (la restricción `UNIQUE` no permite nombres repetidos).

```sql
-- Cada equipo elige 2 categorías y las inserta
INSERT INTO categorias (nombre) VALUES
  ('Bebidas'),
  ('Snacks');
```

> Si les da error `UNIQUE` → otro equipo ya tomó esa categoría. ¡Elijan otra!

### Paso 1.2 — Insertar productos

> Todo el equipo participa. Deben insertar **mínimo 5 productos**.
> Recuerden: la columna `id_categoria` es una FK → el valor **debe existir** en `categorias`.

```sql
-- Primero: ver qué categorías existen y sus IDs
SELECT * FROM categorias;

-- Luego: insertar productos con un id_categoria válido
INSERT INTO productos (nombre, precio, stock, id_categoria) VALUES
  ('Coca-Cola 500ml',  990, 24, 1),
  ('Sprite 500ml',     890, 20, 1),
  ('Papas Lays',      1200, 15, 2),
  ('Ramitas',          600, 30, 2),
  ('Galletas Tritón', 1500, 12, 2);
```

### Paso 1.3 — Verificar

```sql
-- ¿Cuántos productos hay por categoría?
SELECT
  c.nombre AS categoria,
  COUNT(p.id) AS total_productos,
  SUM(p.stock) AS stock_total
FROM categorias c
LEFT JOIN productos p ON c.id = p.id_categoria
GROUP BY c.nombre
ORDER BY total_productos DESC;
```

### Paso 1.4 — Desafío: el INSERT que falla

> Intenten insertar un producto con una categoría que **NO existe**:

```sql
INSERT INTO productos (nombre, precio, stock, id_categoria)
VALUES ('Producto Fantasma', 100, 1, 999);
-- ¿Qué error les da?
-- Ese error es la INTEGRIDAD REFERENCIAL protegiéndonos
```

---

---

## 🔫 Paso 2: Ciber-Lunes — UPDATE (20 min)

Hoy es Ciber-Lunes y hay que hacer ajustes masivos de precios y stock.

### Paso 2.1 — Inflación selectiva

> Subir un **15%** el precio de todo lo que cueste menos de $1000.

```sql
-- ANTES: ver quiénes se ven afectados (BUENA PRÁCTICA 🔑)
SELECT nombre, precio FROM productos WHERE precio < 1000;

-- ACTUALIZAR
UPDATE productos
SET precio = ROUND(precio * 1.15, 2)
WHERE precio < 1000;

-- VERIFICAR que los cambios se aplicaron
SELECT nombre, precio FROM productos ORDER BY precio;
```

> **¿Por qué usamos `ROUND()`?**
> Porque `890 * 1.15 = 1023.5` y queremos solo 2 decimales.

### Paso 2.2 — Restock de emergencia

> Todo lo que tenga stock menor a 15 recibe **+20 unidades** más.

```sql
SELECT nombre, stock FROM productos WHERE stock < 15;

UPDATE productos
SET stock = stock + 20
WHERE stock < 15;

SELECT nombre, stock FROM productos ORDER BY stock;
```

### Paso 2.3 — El UPDATE más peligroso

> Lean esto y discutan en equipo **antes de ejecutar**:

```sql
UPDATE productos SET precio = 0;
```

> **Pregunta**: ¿Qué pasaría si ejecutan esto?
>
> **Respuesta**: Sin `WHERE` → cambia el precio de **TODOS** los productos a 0.
> Pero el `CHECK (precio > 0)` lo impide. ¡Doble protección! 🛡️
>
> **Moraleja**: Siempre usar WHERE. Pero por si te olvidas, las restricciones te salvan.

### Paso 2.4 — Corrección libre

> El equipo elige **UNA** de estas misiones:
>
> **A**: Desactivar (`activo = false`) todos los productos de una categoría.
> **B**: Cambiar el nombre de un producto.
> **C**: Intentar poner `precio = NULL` a un producto. ¿Funciona? ¿Por qué no?

---

---

## 💣 Paso 3: Campo Minado — DELETE (15 min)

Eliminar datos sin romper la integridad referencial.

### Paso 3.1 — Preparar datos de prueba

```sql
INSERT INTO clientes (nombre, email, ciudad) VALUES
  ('María García',   'maria@mail.com',   'Santiago'),
  ('Pedro López',    'pedro@mail.com',   'Valparaíso'),
  ('Ana Martínez',   'ana@mail.com',     'Concepción'),
  ('Luis Rodríguez', 'luis@mail.com',    'Santiago');

INSERT INTO pedidos (id_cliente, id_producto, cantidad, total) VALUES
  (1, 1, 3, 2970),
  (2, 3, 2, 2400),
  (1, 2, 1, 890),
  (3, 1, 5, 4950);
```

### Paso 3.2 — DELETE seguro ✅

> Borrar a Luis Rodríguez (que **NO** tiene pedidos).

```sql
-- Verificar que no tiene pedidos
SELECT * FROM pedidos WHERE id_cliente = 4;
-- Resultado vacío → se puede borrar sin problemas

DELETE FROM clientes WHERE nombre = 'Luis Rodríguez';
```

### Paso 3.3 — DELETE con FK 💥

> Intentar borrar a María García (que **SÍ** tiene pedidos).

```sql
DELETE FROM clientes WHERE nombre = 'María García';
-- ❌ ERROR: hay pedidos que la referencian
```

> **Pregunta para el equipo**: ¿Cómo resolverían esto?
>
> **Solución**: borrar primero los pedidos de María, y luego borrarla a ella:

```sql
DELETE FROM pedidos WHERE id_cliente = 1;
DELETE FROM clientes WHERE nombre = 'María García';
```

### Paso 3.4 — Diferencias entre DELETE, TRUNCATE y DROP

| Comando            | Borra filas | Borra la tabla | ¿Se puede deshacer? |
| ------------------ | :---------: | :------------: | :-----------------: |
| `DELETE` sin WHERE |     ✅      |       ❌       |   ✅ Con ROLLBACK   |
| `TRUNCATE`         |     ✅      |       ❌       |       Depende       |
| `DROP TABLE`       |     ✅      |       ✅       |         ❌          |

---

---

## 🔗 Paso 4: CASCADE en Acción (20 min)

### Paso 4.1 — Inserción respetando el orden

> Cada equipo inserta datos en el orden correcto:
> categoría (padre) → producto (hijo) → cliente → pedido (nieto).

```sql
-- 1. Categoría (no tiene FK → se puede insertar libremente)
INSERT INTO categorias (nombre) VALUES ('Electrónica');

-- 2. Producto (tiene FK → la categoría DEBE existir antes)
INSERT INTO productos (nombre, precio, stock, id_categoria)
VALUES ('Audífonos Bluetooth', 15990, 50,
  (SELECT id FROM categorias WHERE nombre = 'Electrónica'));

-- 3. Cliente (no tiene FK → se puede insertar cuando quieran)
INSERT INTO clientes (nombre, email)
VALUES ('Carlos Sánchez', 'carlos@mail.com');

-- 4. Pedido (tiene FK hacia cliente Y producto → ambos deben existir)
INSERT INTO pedidos (id_cliente, id_producto, cantidad, total)
VALUES (
  (SELECT id FROM clientes WHERE email = 'carlos@mail.com'),
  (SELECT id FROM productos WHERE nombre = 'Audífonos Bluetooth'),
  2, 31980);
```

### Paso 4.2 — Probar ON DELETE CASCADE

> Creamos una tabla temporal con CASCADE y vemos qué pasa:

```sql
CREATE TABLE pedidos_cascade (
  id          SERIAL PRIMARY KEY,
  id_cliente  INT NOT NULL,
  cantidad    INT NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE
);

-- Insertar un pedido para Carlos
INSERT INTO pedidos_cascade (id_cliente, cantidad)
VALUES (
  (SELECT id FROM clientes WHERE email = 'carlos@mail.com'),
  1);

-- Verificar que existe
SELECT * FROM pedidos_cascade;

-- Ahora borrar a Carlos de la tabla clientes...
DELETE FROM clientes WHERE email = 'carlos@mail.com';

-- ¿Qué pasó con el pedido?
SELECT * FROM pedidos_cascade;
-- 😱 ¡Se borró automáticamente! Eso es CASCADE.
```

> **Discusión en equipo (2 min)**:
>
> - ¿Cuándo conviene usar CASCADE?
> - ¿Cuándo sería peligroso?

---

---

## 🏦 Paso 5: El Banco — Transacciones (25 min)

### Paso 5.1 — Crear el banco

```sql
INSERT INTO cuentas_bancarias (titular, saldo) VALUES
  ('Cuenta A - María',  500000),
  ('Cuenta B - Pedro',  300000),
  ('Cuenta C - Ana',   1000000),
  ('Cuenta D - Luis',    50000);

SELECT * FROM cuentas_bancarias;
```

### Paso 5.2 — Transferencia SIN transacción (¡peligro!)

> **Lean esto sin ejecutar**. ¿Qué pasa si se corta la luz entre los dos UPDATE?

```sql
UPDATE cuentas_bancarias SET saldo = saldo - 200000 WHERE id = 1;
-- 💥 CORTE DE LUZ AQUÍ
UPDATE cuentas_bancarias SET saldo = saldo + 200000 WHERE id = 2;
```

> María perdió $200,000 pero Pedro NO los recibió. El dinero desapareció. 💸

### Paso 5.3 — Transferencia CON transacción (segura ✅)

```sql
BEGIN;
  UPDATE cuentas_bancarias SET saldo = saldo - 200000 WHERE id = 1;
  UPDATE cuentas_bancarias SET saldo = saldo + 200000 WHERE id = 2;

  -- Verificar ANTES de confirmar
  SELECT titular, saldo FROM cuentas_bancarias WHERE id IN (1, 2);
COMMIT;

-- Verificar resultado final
SELECT * FROM cuentas_bancarias;
```

> Con `BEGIN` + `COMMIT`, ambos UPDATE son una **unidad indivisible**.
> Si algo falla, ninguno se guarda. Eso es **Atomicidad** (la A de ACID).

### Paso 5.4 — ROLLBACK: la máquina del tiempo ⏪

```sql
BEGIN;
  UPDATE cuentas_bancarias SET saldo = saldo - 900000 WHERE id = 3;
  UPDATE cuentas_bancarias SET saldo = saldo + 900000 WHERE id = 4;

  -- Verifico... 😱 ¡Transferí de más!
  SELECT titular, saldo FROM cuentas_bancarias WHERE id IN (3, 4);

ROLLBACK;

-- Todo volvió a como estaba ✅
SELECT * FROM cuentas_bancarias;
```

### Paso 5.5 — Debate ACID

> Para cada principio ACID, piensen en equipo: **¿qué pasaría si no existiera?**
>
> | Principio        | Sin este principio...                               |
> | ---------------- | --------------------------------------------------- |
> | **A**tomicidad   | El dinero se pierde a la mitad de una transferencia |
> | **C**onsistencia | Podrían existir saldos negativos                    |
> | **I**solamiento  | Dos transferencias simultáneas se mezclan           |
> | **D**urabilidad  | Confirmaste pero al reiniciar desapareció           |

---

---

## 🏆 Paso 6: Desafío Final (25 min)

Llegó el momento de aplicar **todo lo aprendido** en un ejercicio completo.

Cada equipo debe completar **los 6 pasos en orden** y registrar el avance en la tabla `desafio_final`.

> Cuando completen cada paso, registren el avance con el INSERT que aparece debajo.
> La columna `fecha_completado` se graba **automáticamente** con la hora exacta.

### Desafío paso 1 — INSERT con FK

> Insertar **2 clientes** y **3 productos** nuevos. Los productos deben pertenecer a una categoría que ya exista.

```sql
-- (Escriban sus propios INSERT aquí)

-- Cuando terminen → registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  1, 'INSERT de clientes y productos completado'
);
```

### Desafío paso 2 — INSERT con doble FK

> Insertar **2 pedidos** vinculando los clientes y productos que acaban de crear.
> Recuerden: `pedidos` tiene FK hacia `clientes` Y hacia `productos`.

```sql
-- (Sus INSERT de pedidos aquí)

-- Registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  2, 'INSERT de pedidos completado'
);
```

### Desafío paso 3 — UPDATE con cálculo

> Subir un **20%** el precio de todos los productos que tengan stock mayor a 25.
> Recuerden: primero SELECT para verificar, luego UPDATE.

```sql
-- SELECT de verificación
-- UPDATE con WHERE
-- SELECT de confirmación

-- Registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  3, 'UPDATE de precios completado'
);
```

### Desafío paso 4 — DELETE seguro

> Elegir un cliente que **NO tenga pedidos** y eliminarlo.
> Si todos tienen pedidos, crear uno nuevo y borrarlo.

```sql
-- Verificar quién no tiene pedidos
-- DELETE seguro

-- Registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  4, 'DELETE seguro completado'
);
```

### Desafío paso 5 — Transacción completa (BEGIN/COMMIT)

> Hacer una transferencia de **$100,000** de la Cuenta C (Ana) a la Cuenta B (Pedro)
> usando `BEGIN` y `COMMIT`.

```sql
BEGIN;
  -- UPDATE cuenta origen
  -- UPDATE cuenta destino
  -- SELECT para verificar
COMMIT;

-- Registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  5, 'Transacción bancaria completada'
);
```

### Desafío paso 6 — ROLLBACK de emergencia

> Intentar transferir **$2,000,000** de Luis (Cuenta D, que solo tiene $50,000).
> Verificar que no se puede y usar ROLLBACK.

```sql
BEGIN;
  -- UPDATE que intenta sacar más dinero del disponible
  -- Verificar el resultado
ROLLBACK;

-- Registrar avance:
INSERT INTO desafio_final (id_equipo, paso, descripcion)
VALUES (
  (SELECT id FROM equipos WHERE nombre_equipo = 'Mi Equipo'),
  6, 'ROLLBACK de emergencia completado'
);
```

---

### 📊 Ver el avance de todos

> Esta consulta muestra cómo va cada equipo:

```sql
SELECT
  e.nombre_equipo,
  df.paso,
  df.descripcion,
  df.fecha_completado
FROM desafio_final df
JOIN equipos e ON df.id_equipo = e.id
ORDER BY df.paso, df.fecha_completado;
```

---

---

## 🎓 Cierre

### Resumen de lo que aprendimos hoy

| Concepto                   | Lo más importante                                                   |
| -------------------------- | ------------------------------------------------------------------- |
| `INSERT INTO ... VALUES`   | Agrega filas. Respetar FK y tipos de dato.                          |
| `UPDATE ... SET ... WHERE` | Modifica datos. **Nunca sin WHERE.**                                |
| `DELETE FROM ... WHERE`    | Elimina filas. **Nunca sin WHERE.** Verificar FK.                   |
| Integridad referencial     | FK garantiza relaciones válidas entre tablas.                       |
| Orden de operaciones       | INSERT: padres → hijos. DELETE: hijos → padres.                     |
| `ON DELETE CASCADE`        | Borra hijos automáticamente al borrar padre.                        |
| `BEGIN` / `COMMIT`         | Agrupa operaciones y confirma todo junto.                           |
| `ROLLBACK`                 | Deshace todo lo hecho desde el BEGIN.                               |
| ACID                       | **A**tomicidad, **C**onsistencia, **A**islamiento, **D**urabilidad. |

---

### Ver los equipos y sus integrantes

```sql
SELECT
  e.nombre_equipo,
  e.fecha_registro AS equipo_creado,
  i.nombre AS integrante,
  i.fecha_registro AS se_unio
FROM equipos e
JOIN integrantes i ON e.id = i.id_equipo
ORDER BY e.nombre_equipo, i.nombre;
```

---

## 🔧 Limpieza final (opcional)

```sql
DROP TABLE IF EXISTS desafio_final, movimientos, cuentas_bancarias,
  pedidos, pedidos_cascade, clientes, productos, categorias,
  integrantes, equipos CASCADE;
```
