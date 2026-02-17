<!-- =========================================================
Archivo: sql_dml.md
Tema: SQL Básico — DML: INSERT, UPDATE y DELETE
Clase: Sentencias para la manipulación de datos y
       transaccionalidad – Parte 1
AE3: Utilizar lenguaje de manipulación de datos DML para la
     modificación de los datos existentes en una base de datos.
========================================================= -->

# SQL Básico (curso) — DML: INSERT, UPDATE y DELETE

Este documento cubre paso a paso las operaciones **DML** (Data Manipulation Language)
para **insertar**, **actualizar** y **eliminar** datos en una base de datos:

1. ¿Qué es DML y para qué se utiliza?
2. AutoCommit, COMMIT y ROLLBACK
3. INSERT INTO — agregar registros
4. ID autogenerado e incremental
5. UPDATE — actualizar registros
6. DELETE — eliminar registros
7. Ejercicio integrador (INSERT + UPDATE + DELETE)

> Enfoque: **simple, pedagógico y práctico**.
> Pensado para estudiantes que recién comienzan.

---

## 0) Repaso rápido

En la clase anterior trabajamos:

- Consultas anidadas (subconsultas).
- Funciones de agrupación (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).
- Distintos tipos de `JOIN` (`INNER`, `LEFT`, `RIGHT`, `FULL`).

Hoy pasamos de **leer** datos a **modificarlos**.

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
DROP TABLE IF EXISTS transacciones CASCADE;
DROP TABLE IF EXISTS monedas CASCADE;
DROP TABLE IF EXISTS empleados CASCADE;
DROP TABLE IF EXISTS inventario CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- ─────────────────────────────────────────────
-- Tabla: usuarios
-- ─────────────────────────────────────────────
CREATE TABLE usuarios (
  user_id     BIGSERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  correo      VARCHAR(150) UNIQUE NOT NULL,
  contrasena  VARCHAR(255) NOT NULL,
  saldo       NUMERIC(12,2) DEFAULT 0,
  fecha_creacion DATE DEFAULT CURRENT_DATE
);

-- ─────────────────────────────────────────────
-- Tabla: monedas
-- ─────────────────────────────────────────────
CREATE TABLE monedas (
  currency_id     SERIAL PRIMARY KEY,
  currency_name   VARCHAR(50) NOT NULL,
  currency_symbol VARCHAR(10) NOT NULL
);

-- ─────────────────────────────────────────────
-- Tabla: transacciones (FK → usuarios)
-- ─────────────────────────────────────────────
CREATE TABLE transacciones (
  transaction_id    BIGSERIAL PRIMARY KEY,
  sender_user_id    INT NOT NULL,
  receiver_user_id  INT NOT NULL,
  valor             NUMERIC(12,2) NOT NULL,
  transaction_date  TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (sender_user_id)   REFERENCES usuarios(user_id),
  FOREIGN KEY (receiver_user_id) REFERENCES usuarios(user_id)
);

-- ─────────────────────────────────────────────
-- Tabla: inventario (para ejercicio INSERT)
-- ─────────────────────────────────────────────
CREATE TABLE inventario (
  id                   SERIAL PRIMARY KEY,
  nombre_producto      VARCHAR(100) NOT NULL,
  precio               NUMERIC(10,2) NOT NULL,
  cantidad_disponible  INT DEFAULT 0
);

-- ─────────────────────────────────────────────
-- Tabla: empleados (para ejercicio integrador)
-- ─────────────────────────────────────────────
CREATE TABLE empleados (
  id_empleado    SERIAL PRIMARY KEY,
  nombre         VARCHAR(50) NOT NULL,
  apellido       VARCHAR(50) NOT NULL,
  salario        NUMERIC(10,2) NOT NULL,
  fecha_ingreso  DATE NOT NULL,
  departamento   VARCHAR(50) NOT NULL
);
```

> ⚠️ Si quieres empezar de cero (borrar todo y volver a crear), ejecuta:
>
> ```sql
> DROP TABLE IF EXISTS transacciones, monedas, empleados, inventario, usuarios CASCADE;
> ```
>
> Y luego vuelve a ejecutar el bloque de arriba.

---

## 1) ¿Qué es DML y para qué se utiliza?

### 1.1 Definición

**DML** = **Data Manipulation Language** (Lenguaje de Manipulación de Datos).

Es la parte de SQL que permite **interactuar con los datos** almacenados en las tablas:

| Comando  | ¿Qué hace?                           | ¿Modifica datos? |
| -------- | ------------------------------------ | ---------------- |
| `INSERT` | Agrega filas nuevas                  | ✅ Sí            |
| `UPDATE` | Modifica valores de filas existentes | ✅ Sí            |
| `DELETE` | Elimina filas existentes             | ✅ Sí            |
| `SELECT` | Lee / consulta datos                 | ❌ No            |

> `SELECT` técnicamente es parte del DML, pero **no modifica datos**.
> Lo usamos para **verificar** los cambios que hacemos con INSERT, UPDATE y DELETE.

### 1.2 ¿Por qué es importante?

- **Insertar**: agregar nuevos clientes, productos, ventas, etc.
- **Actualizar**: corregir un precio, cambiar un nombre, ajustar un saldo.
- **Eliminar**: borrar registros obsoletos, duplicados o incorrectos.

Sin DML, la base de datos tendría tablas vacías o con datos desactualizados.

### 1.3 DML vs DDL (no confundir)

| Aspecto  | DML                            | DDL                              |
| -------- | ------------------------------ | -------------------------------- |
| Sigla    | Data **Manipulation** Language | Data **Definition** Language     |
| Afecta a | Los **datos** (filas)          | La **estructura** (tablas, cols) |
| Ejemplos | INSERT, UPDATE, DELETE         | CREATE, ALTER, DROP              |

> DDL = crear/modificar/borrar **tablas**.
> DML = crear/modificar/borrar **datos dentro de las tablas**.

---

## 2) AutoCommit, COMMIT y ROLLBACK

### 2.1 ¿Qué es una transacción?

Una **transacción** es un grupo de operaciones que deben ejecutarse **todas juntas** o **ninguna**.
Piensa en una transferencia bancaria: si sacas dinero de una cuenta, **tiene** que llegar a la otra.

### 2.2 AutoCommit

| Modo               | Comportamiento                                                     |
| ------------------ | ------------------------------------------------------------------ |
| `AutoCommit = ON`  | Cada sentencia se guarda **inmediatamente**. No se puede deshacer. |
| `AutoCommit = OFF` | Los cambios quedan **pendientes** hasta confirmar o deshacer.      |

### 2.3 COMMIT y ROLLBACK

```sql
-- Con AutoCommit = OFF, los cambios no se guardan hasta que digas COMMIT
BEGIN;  -- Inicia la transacción

INSERT INTO usuarios (nombre, correo, contrasena)
VALUES ('Test', 'test@mail.com', '1234');

-- Si todo está bien:
COMMIT;   -- ✅ Guarda los cambios de forma permanente

-- Si algo salió mal:
ROLLBACK; -- ❌ Deshace todos los cambios desde el BEGIN
```

- `COMMIT` = confirmar y guardar.
- `ROLLBACK` = deshacer y volver al estado anterior.

> 💡 Es útil desactivar AutoCommit cuando trabajas con **varias operaciones que dependen entre sí**
> (ejemplo: una transferencia donde se debe debitar Y acreditar).

### 2.4 Ejemplo práctico de transacción

```sql
-- Transferencia de $1000 de usuario 1 a usuario 2
BEGIN;

UPDATE usuarios SET saldo = saldo - 1000 WHERE user_id = 1;
UPDATE usuarios SET saldo = saldo + 1000 WHERE user_id = 2;

-- Si ambos UPDATE funcionaron bien:
COMMIT;

-- Si algo falló (ejemplo: saldo insuficiente):
-- ROLLBACK;
```

> ⚠️ Si el sistema se cae entre los dos UPDATE y no hay transacción,
> el dinero se pierde. Por eso usamos `BEGIN` + `COMMIT`.

---

## 3) INSERT INTO — agregar registros

### 3.1 Sintaxis básica

```sql
INSERT INTO nombre_tabla (columna1, columna2, columna3)
VALUES (valor1, valor2, valor3);
```

| Parte                          | Significado                        |
| ------------------------------ | ---------------------------------- |
| `INSERT INTO nombre_tabla`     | En qué tabla insertar              |
| `(columna1, columna2, ...)`    | Las columnas a las que das valor   |
| `VALUES (valor1, valor2, ...)` | Los valores, en el **mismo orden** |

### 3.2 Ejemplo: agregar un producto al inventario

```sql
INSERT INTO inventario (nombre_producto, precio, cantidad_disponible)
VALUES ('Laptop HP', 900000, 15);
```

**Explicación paso a paso:**

1. `INSERT INTO inventario` → quiero agregar una fila a la tabla `inventario`.
2. `(nombre_producto, precio, cantidad_disponible)` → estas son las columnas que voy a llenar.
3. `VALUES ('Laptop HP', 900000, 15)` → estos son los valores para cada columna.
4. La columna `id` **no la incluimos** porque es `SERIAL` (autogenerada).

**Verificar:**

```sql
SELECT * FROM inventario;
```

**Resultado:**

| id  | nombre_producto | precio    | cantidad_disponible |
| --- | --------------- | --------- | ------------------- |
| 1   | Laptop HP       | 900000.00 | 15                  |

### 3.3 Ejemplo: agregar un usuario

```sql
INSERT INTO usuarios (nombre, correo, contrasena)
VALUES ('Juan', 'juan@example.com', 'clave123');
```

- `user_id` → se genera automáticamente (es `BIGSERIAL`).
- `saldo` → queda en `0` (su valor `DEFAULT`).
- `fecha_creacion` → se llena con la fecha de hoy (`DEFAULT CURRENT_DATE`).

**Verificar:**

```sql
SELECT * FROM usuarios;
```

| user_id | nombre | correo           | contrasena | saldo | fecha_creacion |
| ------- | ------ | ---------------- | ---------- | ----- | -------------- |
| 1       | Juan   | juan@example.com | clave123   | 0.00  | 2026-02-13     |

### 3.4 Insertar varias filas a la vez

En lugar de hacer un INSERT por cada fila, puedes insertar múltiples filas en una sola sentencia:

```sql
INSERT INTO usuarios (nombre, correo, contrasena, saldo) VALUES
  ('Ana López',    'ana@mail.com',    'pass456', 50000),
  ('Pedro Soto',   'pedro@mail.com',  'pass789', 30000),
  ('María Díaz',   'maria@mail.com',  'passabc', 75000);
```

- Cada fila va entre paréntesis.
- Se separan por comas.
- Solo un `;` al final.

> ✅ Esto es más rápido y más limpio que hacer 3 INSERT separados.

**Verificar:**

```sql
SELECT * FROM usuarios;
```

### 3.5 Insertar respetando FK (orden de tablas)

Recuerda: si una tabla tiene **Foreign Key**, primero debes insertar en la **tabla padre**.

```sql
-- ✅ PASO 1: Insertar usuarios PRIMERO (tabla padre)
INSERT INTO usuarios (nombre, correo, contrasena, saldo) VALUES
  ('Carlos', 'carlos@mail.com', 'pass111', 100000),
  ('Laura',  'laura@mail.com',  'pass222', 80000);

-- ✅ PASO 2: Insertar transacciones DESPUÉS (tabla hija)
INSERT INTO transacciones (sender_user_id, receiver_user_id, valor) VALUES
  (1, 2, 15000),
  (2, 3, 5000),
  (3, 1, 22000);
```

```sql
-- ❌ ERROR: si intentas insertar una transacción con un user_id que NO existe
INSERT INTO transacciones (sender_user_id, receiver_user_id, valor)
VALUES (999, 1, 1000);
-- ERROR: la FK falla porque el usuario 999 no existe
```

### 3.6 Insertar monedas

```sql
INSERT INTO monedas (currency_name, currency_symbol) VALUES
  ('Peso Chileno',        'CLP'),
  ('Dólar Estadounidense', 'USD'),
  ('Euro',                 'EUR');
```

**Verificar:**

```sql
SELECT * FROM monedas;
```

| currency_id | currency_name        | currency_symbol |
| ----------- | -------------------- | --------------- |
| 1           | Peso Chileno         | CLP             |
| 2           | Dólar Estadounidense | USD             |
| 3           | Euro                 | EUR             |

---

## 4) ID autogenerado e incremental

### 4.1 ¿Qué es?

Cuando una columna tiene un **ID autogenerado**, la base de datos **crea el valor automáticamente**
cada vez que insertas una fila. No necesitas preocuparte por asignar un número único manualmente.

### 4.2 ¿Cómo se configura?

Depende del motor de base de datos:

| Motor de BD | Cómo se escribe                     | Ejemplo                                |
| ----------- | ----------------------------------- | -------------------------------------- |
| PostgreSQL  | `SERIAL` o `BIGSERIAL`              | `id SERIAL PRIMARY KEY`                |
| MySQL       | `AUTO_INCREMENT`                    | `id INT AUTO_INCREMENT PRIMARY KEY`    |
| SQL Server  | `IDENTITY(1,1)`                     | `id INT IDENTITY(1,1) PRIMARY KEY`     |
| SQLite      | `INTEGER PRIMARY KEY AUTOINCREMENT` | `id INTEGER PRIMARY KEY AUTOINCREMENT` |

### 4.3 Ejemplo en PostgreSQL

```sql
CREATE TABLE alumnos (
  id    SERIAL PRIMARY KEY,  -- ID autogenerado
  nombre VARCHAR(50) NOT NULL,
  email  VARCHAR(100)
);
```

```sql
-- No incluimos "id" en el INSERT → la DB lo genera
INSERT INTO alumnos (nombre, email) VALUES
  ('Lucía',  'lucia@mail.com'),
  ('Pedro',  'pedro@mail.com'),
  ('Andrea', 'andrea@mail.com');
```

**Verificar:**

```sql
SELECT * FROM alumnos;
```

| id  | nombre | email           |
| --- | ------ | --------------- |
| 1   | Lucía  | lucia@mail.com  |
| 2   | Pedro  | pedro@mail.com  |
| 3   | Andrea | andrea@mail.com |

> Los IDs 1, 2, 3 se generaron **automáticamente**, uno por cada fila insertada.

### 4.4 Ejemplo en MySQL

```sql
CREATE TABLE alumnos (
  id     INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  email  VARCHAR(100)
);

-- El INSERT funciona igual: no incluyes "id"
INSERT INTO alumnos (nombre, email)
VALUES ('Lucía', 'lucia@mail.com');
```

### 4.5 ¿Por qué usar IDs autogenerados?

- **Evitas duplicados**: la DB se encarga de que cada ID sea único.
- **Es más rápido**: no necesitas verificar cuál fue el último ID.
- **Escala bien**: con miles o millones de registros, es inviable asignar IDs a mano.

---

## 5) 🏋️ Ejercicio 1: Aplicando INSERT INTO

### Contexto

Practicaremos cómo insertar registros en una tabla con **ID autogenerado**.

### Consigna

Trabajar con la tabla `inventario` (que ya creamos en la preparación).

### Paso a paso

**Paso 1 — Insertar un producto:**

```sql
INSERT INTO inventario (nombre_producto, precio, cantidad_disponible)
VALUES ('Monitor Samsung 27"', 250000, 10);
```

**Paso 2 — Verificar:**

```sql
SELECT * FROM inventario;
```

| id  | nombre_producto     | precio    | cantidad_disponible |
| --- | ------------------- | --------- | ------------------- |
| 1   | Laptop HP           | 900000.00 | 15                  |
| 2   | Monitor Samsung 27" | 250000.00 | 10                  |

> El ID se asignó automáticamente (2, porque el 1 ya existía).

**Paso 3 — Insertar más productos:**

```sql
INSERT INTO inventario (nombre_producto, precio, cantidad_disponible) VALUES
  ('Teclado Mecánico',    45000,  30),
  ('Mouse Inalámbrico',   25000,  50),
  ('Auriculares Gaming',  89000,  20);
```

**Paso 4 — Verificar todos:**

```sql
SELECT * FROM inventario;
```

**Paso 5 — Insertar uno más y observar el ID:**

```sql
INSERT INTO inventario (nombre_producto, precio, cantidad_disponible)
VALUES ('Webcam HD', 35000, 25);

SELECT * FROM inventario;
```

> 💡 **Reflexión**: ¿Cómo te facilita el ID autogenerado el trabajo con miles de productos
> sin asignar manualmente un identificador único cada vez?

---

## 6) DELETE — eliminar registros

### 6.1 Sintaxis básica

```sql
DELETE FROM nombre_tabla
WHERE condición;
```

| Parte             | Significado                                       |
| ----------------- | ------------------------------------------------- |
| `DELETE FROM`     | Indica de qué tabla eliminar                      |
| `nombre_tabla`    | El nombre de la tabla                             |
| `WHERE condición` | Solo elimina las filas que cumplan esta condición |

> ⚠️ **MUY IMPORTANTE**: Si omites el `WHERE`, se eliminan **TODAS** las filas de la tabla.

```sql
-- ❌ PELIGROSO: borra TODOS los registros de la tabla
DELETE FROM inventario;

-- ✅ SEGURO: solo borra lo que cumple la condición
DELETE FROM inventario
WHERE nombre_producto = 'Webcam HD';
```

### 6.2 Ejemplo: eliminar un producto específico

```sql
DELETE FROM inventario
WHERE nombre_producto = 'Webcam HD';
```

**Explicación paso a paso:**

1. `DELETE FROM inventario` → quiero eliminar filas de la tabla `inventario`.
2. `WHERE nombre_producto = 'Webcam HD'` → solo las filas donde el producto se llame "Webcam HD".
3. La fila completa se elimina (no solo una columna, **toda la fila**).

**Verificar:**

```sql
SELECT * FROM inventario;
```

> El producto "Webcam HD" ya no aparece.

### 6.3 Ejemplo: eliminar por condición numérica

```sql
-- Eliminar productos con precio menor a 30000
DELETE FROM inventario
WHERE precio < 30000;
```

### 6.4 Ejemplo: eliminar por fecha

Primero insertemos algunos usuarios con fechas antiguas:

```sql
INSERT INTO usuarios (nombre, correo, contrasena, fecha_creacion) VALUES
  ('Usuario Viejo 1', 'viejo1@mail.com', 'pass', '2019-06-15'),
  ('Usuario Viejo 2', 'viejo2@mail.com', 'pass', '2019-11-20');
```

Ahora eliminamos usuarios creados antes del 2020:

```sql
-- Paso 1: Ver qué usuarios se eliminarán
SELECT * FROM usuarios
WHERE fecha_creacion < '2020-01-01';

-- Paso 2: Eliminar
DELETE FROM usuarios
WHERE fecha_creacion < '2020-01-01';

-- Paso 3: Verificar
SELECT * FROM usuarios;
```

> 💡 **Buena práctica**: Antes de hacer un DELETE, haz un SELECT con la misma condición WHERE
> para verificar **qué filas se van a eliminar**. Así evitas errores.

### 6.5 DELETE solo borra filas, no columnas

Si quieres "limpiar" el valor de una columna pero **conservar la fila**,
no uses DELETE. Usa UPDATE y pon el valor en `NULL`:

```sql
-- ❌ Esto borra la fila COMPLETA
DELETE FROM usuarios WHERE user_id = 1;

-- ✅ Esto solo limpia el saldo, pero conserva la fila
UPDATE usuarios SET saldo = NULL WHERE user_id = 1;
```

### 6.6 Cuidado con las FK al borrar

Si la fila que quieres borrar está **referenciada por otra tabla** (FK), la DB dará error:

```sql
-- ❌ Error: no puedes borrar un usuario si tiene transacciones
DELETE FROM usuarios WHERE user_id = 1;
-- ERROR: hay transacciones que referencian a este usuario

-- ✅ Primero borrar las transacciones del usuario, luego el usuario
DELETE FROM transacciones WHERE sender_user_id = 1 OR receiver_user_id = 1;
DELETE FROM usuarios WHERE user_id = 1;
```

> ⚠️ **NOTA**: Asegúrate de tener una copia de seguridad o de estar **100% seguro** de que
> los registros a eliminar son los correctos antes de ejecutar DELETE.

---

## 7) UPDATE — actualizar registros

### 7.1 Sintaxis básica

```sql
UPDATE nombre_tabla
SET columna1 = nuevo_valor1,
    columna2 = nuevo_valor2
WHERE condición;
```

| Parte                 | Significado                                      |
| --------------------- | ------------------------------------------------ |
| `UPDATE nombre_tabla` | Qué tabla modificar                              |
| `SET columna = valor` | Qué columna cambiar y su nuevo valor             |
| `WHERE condición`     | Solo modifica las filas que cumplan la condición |

> ⚠️ **MUY IMPORTANTE**: Si omites el `WHERE`, se actualizan **TODAS** las filas de la tabla.

```sql
-- ❌ PELIGROSO: cambia el precio de TODOS los productos
UPDATE inventario SET precio = 0;

-- ✅ SEGURO: solo cambia el precio de un producto específico
UPDATE inventario SET precio = 950000
WHERE nombre_producto = 'Laptop HP';
```

### 7.2 Ejemplo: actualizar un valor específico

```sql
UPDATE inventario
SET precio = 950000
WHERE nombre_producto = 'Laptop HP';
```

**Explicación paso a paso:**

1. `UPDATE inventario` → quiero modificar la tabla `inventario`.
2. `SET precio = 950000` → quiero cambiar el precio a 950000.
3. `WHERE nombre_producto = 'Laptop HP'` → solo en las filas donde el producto sea "Laptop HP".

**Verificar:**

```sql
SELECT * FROM inventario WHERE nombre_producto = 'Laptop HP';
```

### 7.3 Ejemplo: actualizar con cálculo (aumento porcentual)

```sql
-- Aumentar un 10% el salario de empleados con más de 5 años
UPDATE empleados
SET salario = salario * 1.10
WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '5 years';
```

**Desglose de la fórmula:**

- `salario * 1.10` → multiplica el salario actual por 1.10 (= +10%).
- `CURRENT_DATE - INTERVAL '5 years'` → calcula la fecha de hace 5 años.
- Solo se modifican los empleados cuya `fecha_ingreso` sea **anterior** a esa fecha.

### 7.4 Ejemplo: actualizar varias columnas a la vez

```sql
UPDATE usuarios
SET nombre = 'Juan Carlos',
    correo = 'juancarlos@mail.com'
WHERE user_id = 1;
```

- Cambia **dos columnas** en una sola sentencia.
- Solo para el usuario con `user_id = 1`.

### 7.5 Ejemplo: aumentar un 15% transacciones menores a $50

```sql
-- Antes: ver las transacciones afectadas
SELECT * FROM transacciones WHERE valor < 50;

-- Actualizar
UPDATE transacciones
SET valor = valor * 1.15
WHERE valor < 50;

-- Después: verificar
SELECT * FROM transacciones;
```

### 7.6 Buenas prácticas con UPDATE

1. **Siempre usa WHERE** (a menos que realmente quieras modificar todo).
2. **Haz un SELECT antes** con la misma condición para verificar qué filas se modificarán.
3. **Usa transacciones** (`BEGIN` / `COMMIT` / `ROLLBACK`) cuando los cambios son críticos.

```sql
-- Buena práctica: verificar primero
SELECT * FROM empleados WHERE departamento = 'RRHH';

-- Si las filas son las correctas, ejecutar el UPDATE
UPDATE empleados SET salario = salario * 1.05
WHERE departamento = 'RRHH';
```

---

## 8) 🏋️ Ejercicio 2: INSERT + UPDATE + DELETE integrado

### Contexto

Ya practicamos las tres operaciones por separado. Ahora las combinamos en un flujo completo
usando la tabla `empleados`.

### Consigna

Trabajar sobre la tabla `empleados` con las columnas:
`id_empleado` (PK auto), `nombre`, `apellido`, `salario`, `fecha_ingreso`, `departamento`.

### Parte A — Alta masiva (INSERT) — 10 min

Insertar cinco empleados:

```sql
INSERT INTO empleados (nombre, apellido, salario, fecha_ingreso, departamento) VALUES
  ('Lucía',    'Pérez',    85000,  '2024-02-01', 'IT'),
  ('Andrés',   'Gómez',    72000,  '2023-06-15', 'RRHH'),
  ('Camila',   'Fernández', 91000, '2022-03-10', 'IT'),
  ('Diego',    'Muñoz',    65000,  '2025-01-05', 'RRHH'),
  ('Sofía',    'Ruiz',     68000,  '2025-01-10', 'Marketing');
```

**Verificar:**

```sql
SELECT * FROM empleados;
```

| id_empleado | nombre | apellido  | salario  | fecha_ingreso | departamento |
| ----------- | ------ | --------- | -------- | ------------- | ------------ |
| 1           | Lucía  | Pérez     | 85000.00 | 2024-02-01    | IT           |
| 2           | Andrés | Gómez     | 72000.00 | 2023-06-15    | RRHH         |
| 3           | Camila | Fernández | 91000.00 | 2022-03-10    | IT           |
| 4           | Diego  | Muñoz     | 65000.00 | 2025-01-05    | RRHH         |
| 5           | Sofía  | Ruiz      | 68000.00 | 2025-01-10    | Marketing    |

### Parte B — Ajustes salariales y movimientos (UPDATE) — 12 min

**B.1 — Aumentar un 7% a quienes ganen menos de $80,000:**

```sql
-- Verificar quiénes se ven afectados
SELECT nombre, apellido, salario
FROM empleados
WHERE salario < 80000;
```

| nombre | apellido | salario  |
| ------ | -------- | -------- |
| Andrés | Gómez    | 72000.00 |
| Diego  | Muñoz    | 65000.00 |
| Sofía  | Ruiz     | 68000.00 |

```sql
-- Aplicar el aumento
UPDATE empleados
SET salario = salario * 1.07
WHERE salario < 80000;

-- Verificar
SELECT nombre, apellido, salario FROM empleados;
```

> `salario * 1.07` = salario actual + 7%.

**B.2 — Sumar $5,000 fijos a quienes tengan más de 3 años de antigüedad:**

```sql
-- ¿Quiénes tienen más de 3 años? (ingresaron antes de febrero 2023)
SELECT nombre, apellido, fecha_ingreso
FROM empleados
WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '3 years';
```

```sql
-- Aplicar el bono
UPDATE empleados
SET salario = salario + 5000
WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '3 years';

-- Verificar
SELECT * FROM empleados;
```

**B.3 — Cambiar a Sofía Ruiz al departamento Ventas:**

```sql
UPDATE empleados
SET departamento = 'Ventas'
WHERE nombre = 'Sofía' AND apellido = 'Ruiz';

-- Verificar
SELECT * FROM empleados WHERE nombre = 'Sofía';
```

### Parte C — Depuración (DELETE) — 6 min

**Eliminar todos los empleados de RRHH:**

```sql
-- Verificar quiénes se eliminarán
SELECT * FROM empleados WHERE departamento = 'RRHH';

-- Eliminar
DELETE FROM empleados
WHERE departamento = 'RRHH';

-- Verificar resultado final
SELECT * FROM empleados;
```

### Parte D — Verificación final

```sql
SELECT * FROM empleados ORDER BY id_empleado;
```

Deberían quedar solo los empleados de **IT**, **Marketing** (ahora **Ventas**) y ninguno de RRHH.

---

## 9) Errores comunes

### Al insertar (INSERT)

| Error                    | Causa                                          | Solución                           |
| ------------------------ | ---------------------------------------------- | ---------------------------------- |
| Violar PK (ID duplicado) | Insertar con un ID que ya existe               | Usar ID autoincremental            |
| Violar FK                | El valor referenciado no existe en tabla padre | Insertar primero en la tabla padre |
| Violar NOT NULL          | No dar valor a una columna obligatoria         | Incluir la columna en el INSERT    |
| Violar UNIQUE            | Valor duplicado en columna única               | Verificar antes o usar ON CONFLICT |
| Tipo de dato incorrecto  | Texto donde se espera número, etc.             | Revisar tipos de la tabla          |

### Al actualizar (UPDATE)

| Error                      | Causa                           | Solución                   |
| -------------------------- | ------------------------------- | -------------------------- |
| Actualizar todas las filas | Olvidar el WHERE                | Siempre incluir WHERE      |
| Valor resultante inválido  | Cálculo produce valor no válido | Verificar con SELECT antes |

### Al eliminar (DELETE)

| Error                    | Causa                            | Solución                            |
| ------------------------ | -------------------------------- | ----------------------------------- |
| Borrar todas las filas   | Olvidar el WHERE                 | Siempre incluir WHERE               |
| FK impide borrar         | Hay registros hijos que dependen | Borrar hijos primero, luego padres  |
| Borrar datos incorrectos | Condición WHERE mal escrita      | Hacer SELECT con la misma condición |

---

## 10) Resumen y diccionario

### Lo que aprendimos hoy

✅ Diferenciar los componentes principales de DML.
✅ Insertar datos en una tabla con `INSERT INTO`.
✅ Crear y usar IDs autogenerados (`SERIAL`, `AUTO_INCREMENT`).
✅ Actualizar registros con `UPDATE ... SET ... WHERE`.
✅ Eliminar registros con `DELETE FROM ... WHERE`.
✅ Entender AutoCommit, `COMMIT` y `ROLLBACK`.

### Diccionario DML

| Término          | Significado                                                 |
| ---------------- | ----------------------------------------------------------- |
| `INSERT INTO`    | Comando para agregar filas nuevas a una tabla               |
| `VALUES`         | Lista de valores a insertar                                 |
| `UPDATE`         | Comando para modificar valores de filas existentes          |
| `SET`            | Define qué columnas cambiar y sus nuevos valores            |
| `DELETE FROM`    | Comando para eliminar filas de una tabla                    |
| `WHERE`          | Condición que filtra qué filas se afectan                   |
| `COMMIT`         | Confirma y guarda los cambios de forma permanente           |
| `ROLLBACK`       | Deshace los cambios y vuelve al estado anterior             |
| `BEGIN`          | Inicia una transacción explícita                            |
| `AutoCommit`     | Modo que confirma cada sentencia automáticamente            |
| `SERIAL`         | Tipo PostgreSQL que autogenera IDs secuenciales             |
| `AUTO_INCREMENT` | Equivalente de SERIAL en MySQL                              |
| `IDENTITY`       | Equivalente de SERIAL en SQL Server                         |
| `CASCADE`        | Al borrar tabla padre, borra también los hijos relacionados |
