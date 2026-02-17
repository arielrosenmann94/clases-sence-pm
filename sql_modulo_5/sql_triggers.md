<!-- =========================================================
Archivo: sql_triggers.md
Tema: SQL — Triggers, Funciones y Procedimientos
========================================================= -->

# SQL — Triggers, Funciones y Procedimientos

1. ¿Qué es un Trigger?
2. BEFORE y AFTER
3. NEW y OLD
4. Crear un Trigger paso a paso
5. Ejemplos prácticos
6. Procedimientos almacenados
7. Funciones
8. Errores comunes

> Enfoque: **simple, pedagógico y práctico**.
> Cada bloque de código se explica **palabra por palabra**.

---

## ⚙️ Preparación: tablas para practicar

> **Copia y ejecuta este bloque ANTES de probar los ejemplos.**

```sql
-- =============================================
-- EJECUTAR ESTO PRIMERO
-- =============================================

DROP TABLE IF EXISTS auditoria CASCADE;
DROP TABLE IF EXISTS ventas CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS empleados CASCADE;
DROP TABLE IF EXISTS log_salarios CASCADE;
DROP TABLE IF EXISTS cuentas CASCADE;
DROP TABLE IF EXISTS movimientos CASCADE;

CREATE TABLE productos (
  id          SERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  precio      NUMERIC(10,2) NOT NULL,
  stock       INT DEFAULT 0,
  updated_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ventas (
  id            SERIAL PRIMARY KEY,
  id_producto   INT REFERENCES productos(id),
  cantidad      INT NOT NULL,
  total         NUMERIC(12,2),
  fecha         TIMESTAMP DEFAULT NOW()
);

CREATE TABLE auditoria (
  id          SERIAL PRIMARY KEY,
  tabla       VARCHAR(50),
  operacion   VARCHAR(10),
  detalle     TEXT,
  usuario     VARCHAR(100) DEFAULT CURRENT_USER,
  fecha       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE empleados (
  id        SERIAL PRIMARY KEY,
  nombre    VARCHAR(100) NOT NULL,
  salario   NUMERIC(10,2) NOT NULL
);

CREATE TABLE log_salarios (
  id            SERIAL PRIMARY KEY,
  id_empleado   INT,
  salario_antes NUMERIC(10,2),
  salario_nuevo NUMERIC(10,2),
  fecha         TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cuentas (
  id     SERIAL PRIMARY KEY,
  dueno  VARCHAR(100) NOT NULL,
  saldo  NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE movimientos (
  id         SERIAL PRIMARY KEY,
  id_origen  INT,
  id_destino INT,
  monto      NUMERIC(12,2),
  fecha      TIMESTAMP DEFAULT NOW()
);

-- Datos de ejemplo
INSERT INTO productos (nombre, precio, stock) VALUES
  ('Laptop',   900000, 10),
  ('Monitor',  250000, 20),
  ('Teclado',   45000, 50);

INSERT INTO empleados (nombre, salario) VALUES
  ('Lucía',  850000),
  ('Andrés', 720000);

INSERT INTO cuentas (dueno, saldo) VALUES
  ('Ana',   500000),
  ('Pedro', 300000);
```

---

# PARTE 1: ¿Qué es un Trigger?

---

## 1) Definición

Un **Trigger** es código que se ejecuta **solo, automáticamente**, cuando alguien hace
un INSERT, UPDATE o DELETE en una tabla.

> Tú no lo llamas. Se dispara solo.

**Ejemplo del mundo real:**

- Sin trigger: cada vez que alguien compra, un empleado anota la venta a mano.
- Con trigger: la venta se registra **sola** cada vez que alguien compra.

---

## 2) ¿Cuándo se ejecuta?

Hay dos momentos:

| Momento  | Significado                                 |
| -------- | ------------------------------------------- |
| `BEFORE` | Se ejecuta **antes** de guardar el cambio   |
| `AFTER`  | Se ejecuta **después** de guardar el cambio |

**¿Cuál usar?**

- `BEFORE` → cuando quieres **cambiar o validar** los datos antes de que se guarden.
- `AFTER` → cuando quieres **registrar o reaccionar** a un cambio ya guardado.

---

## 3) NEW y OLD

Dentro de un trigger hay dos variables especiales para acceder a los datos:

| Variable | Qué contiene                     | Disponible en   |
| -------- | -------------------------------- | --------------- |
| `NEW`    | La fila **nueva** (lo que viene) | INSERT y UPDATE |
| `OLD`    | La fila **vieja** (lo que había) | UPDATE y DELETE |

```sql
-- Ejemplos:
NEW.precio   -- el precio NUEVO (el que se quiere guardar)
OLD.precio   -- el precio VIEJO (el que había antes)
NEW.nombre   -- el nombre que se está insertando
OLD.nombre   -- el nombre que se está borrando
```

---

## 4) Las dos piezas de un Trigger

En PostgreSQL necesitas **dos cosas**:

1. Una **función** → el código (qué hacer).
2. Un **trigger** → la regla (cuándo ejecutar la función).

```
FUNCIÓN (el código)  ←──  TRIGGER (la regla que la conecta a la tabla)
```

---

# PARTE 2: Crear un Trigger paso a paso

---

## 5) Pieza 1: La función

```sql
CREATE OR REPLACE FUNCTION fn_ejemplo()
RETURNS TRIGGER AS $$
BEGIN
  -- aquí va tu código
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código             | Qué significa                                                        |
| ------------------ | -------------------------------------------------------------------- |
| `CREATE`           | "Quiero crear algo nuevo"                                            |
| `OR REPLACE`       | "Si ya existe, reemplázala"                                          |
| `FUNCTION`         | "Lo que estoy creando es una función"                                |
| `fn_ejemplo()`     | El nombre que le doy (los `()` están vacíos porque no recibe datos)  |
| `RETURNS TRIGGER`  | "Esta función es para ser usada por un trigger"                      |
| `AS $$`            | "Aquí empieza el código" (`$$` es un delimitador, como abrir llaves) |
| `BEGIN`            | "Inicio del bloque de código"                                        |
| `RETURN NEW;`      | "Devuelve la fila nueva para que la operación continúe"              |
| `END;`             | "Fin del bloque de código"                                           |
| `$$`               | "Aquí termina el código" (cierra el `$$` de arriba)                  |
| `LANGUAGE plpgsql` | "El lenguaje usado es PL/pgSQL" (el lenguaje de PostgreSQL)          |

### ¿Qué retornar?

| Situación              | Qué poner      | Efecto                    |
| ---------------------- | -------------- | ------------------------- |
| BEFORE INSERT o UPDATE | `RETURN NEW;`  | Permite la operación      |
| BEFORE DELETE          | `RETURN OLD;`  | Permite el borrado        |
| AFTER (cualquiera)     | `RETURN NULL;` | Se ignora (ya se ejecutó) |
| Cancelar la operación  | `RETURN NULL;` | En BEFORE: cancela todo   |

---

## 6) Pieza 2: El trigger

```sql
CREATE TRIGGER trg_ejemplo
BEFORE UPDATE ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_ejemplo();
```

**Palabra por palabra:**

| Código             | Qué significa                                     |
| ------------------ | ------------------------------------------------- |
| `CREATE TRIGGER`   | "Quiero crear un trigger"                         |
| `trg_ejemplo`      | El nombre que le doy al trigger                   |
| `BEFORE`           | "Ejecutar ANTES de la operación"                  |
| `UPDATE`           | "Cuando alguien haga un UPDATE"                   |
| `ON productos`     | "En la tabla productos"                           |
| `FOR EACH ROW`     | "Ejecutar una vez POR CADA FILA que se modifique" |
| `EXECUTE FUNCTION` | "La función que debe ejecutar es..."              |
| `fn_ejemplo()`     | El nombre de la función creada antes              |

> Listo. Esas dos piezas juntas forman el trigger completo.

---

# PARTE 3: Ejemplos prácticos

---

## 7) Ejemplo 1 — Actualizar fecha automáticamente

**Problema:** quiero que cada vez que modifique un producto, la columna `updated_at`
se actualice sola con la fecha y hora actual.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_poner_fecha()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código           | Qué significa                                                    |
| ---------------- | ---------------------------------------------------------------- |
| `NEW.updated_at` | "En la fila que se está modificando, toma la columna updated_at" |
| `= NOW()`        | "Ponle la fecha y hora actual"                                   |
| `RETURN NEW;`    | "Devuelve la fila con el cambio para que se guarde"              |

### El trigger:

```sql
CREATE TRIGGER trg_fecha_producto
BEFORE UPDATE ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_poner_fecha();
```

**Frase completa:** "Antes de cada UPDATE en la tabla productos, por cada fila, ejecuta fn_poner_fecha."

### Probar:

```sql
-- Ver la fecha actual del producto 1
SELECT nombre, updated_at FROM productos WHERE id = 1;

-- Modificar el precio
UPDATE productos SET precio = 950000 WHERE id = 1;

-- Ver que updated_at cambió solo
SELECT nombre, precio, updated_at FROM productos WHERE id = 1;
```

---

## 8) Ejemplo 2 — Calcular el total de una venta

**Problema:** al vender, quiero que `total = precio × cantidad` se calcule solo.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_calcular_total()
RETURNS TRIGGER AS $$
DECLARE
  v_precio NUMERIC;
BEGIN
  SELECT precio INTO v_precio
  FROM productos
  WHERE id = NEW.id_producto;

  NEW.total = v_precio * NEW.cantidad;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                       | Qué significa                                          |
| ---------------------------- | ------------------------------------------------------ |
| `DECLARE`                    | "Voy a crear variables para usar después"              |
| `v_precio NUMERIC;`          | "Creo una variable llamada v_precio, de tipo número"   |
| `SELECT precio`              | "Busca el valor de la columna precio"                  |
| `INTO v_precio`              | "Y guárdalo dentro de mi variable v_precio"            |
| `FROM productos`             | "Desde la tabla productos"                             |
| `WHERE id = NEW.id_producto` | "Donde el id coincida con el producto de esta venta"   |
| `NEW.total`                  | "En la venta que se está insertando, la columna total" |
| `= v_precio * NEW.cantidad`  | "Ponle el resultado de precio × cantidad"              |
| `RETURN NEW;`                | "Devuelve la fila con el total ya calculado"           |

### El trigger:

```sql
CREATE TRIGGER trg_total_venta
BEFORE INSERT ON ventas
FOR EACH ROW
EXECUTE FUNCTION fn_calcular_total();
```

**Frase completa:** "Antes de cada INSERT en ventas, por cada fila, ejecuta fn_calcular_total."

### Probar:

```sql
-- Insertar una venta SIN poner el total
INSERT INTO ventas (id_producto, cantidad) VALUES (1, 3);

-- Ver que el total se calculó solo
SELECT * FROM ventas;
```

| id  | id_producto | cantidad | total      |
| --- | ----------- | -------- | ---------- |
| 1   | 1           | 3        | 2700000.00 |

> Total = 900,000 (precio Laptop) × 3 = 2,700,000. ¡Se calculó solo!

---

## 9) Ejemplo 3 — Descontar stock al vender

**Problema:** cuando se registra una venta, restar la cantidad del stock.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_descontar_stock()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE productos
  SET stock = stock - NEW.cantidad
  WHERE id = NEW.id_producto;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                             | Qué significa                                        |
| ---------------------------------- | ---------------------------------------------------- |
| `UPDATE productos`                 | "Quiero modificar la tabla productos"                |
| `SET stock = stock - NEW.cantidad` | "Al stock actual, réstale la cantidad que se vendió" |
| `WHERE id = NEW.id_producto`       | "Solo al producto que se vendió"                     |
| `RETURN NULL;`                     | "Es un AFTER, el retorno se ignora"                  |

### El trigger:

```sql
CREATE TRIGGER trg_stock_venta
AFTER INSERT ON ventas
FOR EACH ROW
EXECUTE FUNCTION fn_descontar_stock();
```

**Frase completa:** "Después de cada INSERT en ventas, por cada fila, ejecuta fn_descontar_stock."

### Probar:

```sql
-- Ver stock antes
SELECT nombre, stock FROM productos WHERE id = 1;
-- Resultado: Laptop, stock = 10

-- Vender 3 laptops
INSERT INTO ventas (id_producto, cantidad) VALUES (1, 3);

-- Ver stock después
SELECT nombre, stock FROM productos WHERE id = 1;
-- Resultado: Laptop, stock = 7  (10 - 3 = 7)
```

---

## 10) Ejemplo 4 — Registrar auditoría

**Problema:** quiero guardar un registro cada vez que alguien inserte, modifique o borre un producto.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_auditoria()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    INSERT INTO auditoria (tabla, operacion, detalle)
    VALUES ('productos', 'INSERT', 'Nuevo: ' || NEW.nombre);
    RETURN NEW;

  ELSIF TG_OP = 'UPDATE' THEN
    INSERT INTO auditoria (tabla, operacion, detalle)
    VALUES ('productos', 'UPDATE',
            'Cambió ' || OLD.nombre || ' → ' || NEW.nombre);
    RETURN NEW;

  ELSIF TG_OP = 'DELETE' THEN
    INSERT INTO auditoria (tabla, operacion, detalle)
    VALUES ('productos', 'DELETE', 'Borrado: ' || OLD.nombre);
    RETURN OLD;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra (lo nuevo):**

| Código                    | Qué significa                                                |
| ------------------------- | ------------------------------------------------------------ |
| `TG_OP`                   | Variable especial. Contiene qué operación disparó el trigger |
| `= 'INSERT'`              | "¿La operación fue un INSERT?"                               |
| `IF ... THEN`             | "Si se cumple esto, entonces haz lo siguiente"               |
| `ELSIF ... THEN`          | "Si no, pero si se cumple esto otro, haz lo siguiente"       |
| `END IF;`                 | "Fin de las condiciones"                                     |
| `OLD.nombre`              | "El nombre que tenía ANTES del cambio"                       |
| `NEW.nombre`              | "El nombre que tiene DESPUÉS del cambio"                     |
| <code>&#124;&#124;</code> | Operador para **unir textos** (como un `+` de cadenas)       |

### El trigger:

```sql
CREATE TRIGGER trg_auditoria_productos
AFTER INSERT OR UPDATE OR DELETE ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_auditoria();
```

**Palabra por palabra:**

| Código                       | Qué significa                                 |
| ---------------------------- | --------------------------------------------- |
| `AFTER`                      | "Después de la operación"                     |
| `INSERT OR UPDATE OR DELETE` | "Cuando alguien haga INSERT, UPDATE O DELETE" |
| `ON productos`               | "En la tabla productos"                       |

### Probar:

```sql
-- Insertar un producto
INSERT INTO productos (nombre, precio, stock) VALUES ('Webcam', 35000, 25);

-- Modificar su precio
UPDATE productos SET precio = 38000 WHERE nombre = 'Webcam';

-- Borrarlo
DELETE FROM productos WHERE nombre = 'Webcam';

-- Ver todo lo que quedó registrado
SELECT * FROM auditoria;
```

---

## 11) Ejemplo 5 — Guardar historial de salarios

**Problema:** cada vez que cambien el salario de un empleado, guardar cuánto ganaba antes y cuánto gana ahora.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_log_salario()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.salario IS DISTINCT FROM NEW.salario THEN
    INSERT INTO log_salarios (id_empleado, salario_antes, salario_nuevo)
    VALUES (NEW.id, OLD.salario, NEW.salario);
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                                     | Qué significa                              |
| ------------------------------------------ | ------------------------------------------ |
| `OLD.salario IS DISTINCT FROM NEW.salario` | "¿El salario viejo es DIFERENTE al nuevo?" |
| `IF ... THEN`                              | "Si sí cambió, entonces haz esto"          |
| `OLD.salario`                              | "Lo que ganaba antes"                      |
| `NEW.salario`                              | "Lo que va a ganar ahora"                  |

> `IS DISTINCT FROM` es como `!=` pero funciona correctamente con `NULL`.

### El trigger:

```sql
CREATE TRIGGER trg_log_salario
AFTER UPDATE ON empleados
FOR EACH ROW
EXECUTE FUNCTION fn_log_salario();
```

### Probar:

```sql
-- Subir el sueldo de Lucía
UPDATE empleados SET salario = 900000 WHERE nombre = 'Lucía';

-- Ver el log
SELECT * FROM log_salarios;
```

| id  | id_empleado | salario_antes | salario_nuevo |
| --- | ----------- | ------------- | ------------- |
| 1   | 1           | 850000.00     | 900000.00     |

---

## 12) Ejemplo 6 — Impedir un borrado

**Problema:** no quiero que nadie pueda borrar productos que tengan stock mayor a 0.

### La función:

```sql
CREATE OR REPLACE FUNCTION fn_proteger_producto()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.stock > 0 THEN
    RAISE EXCEPTION 'No puedes borrar "%" porque tiene % unidades en stock',
      OLD.nombre, OLD.stock;
  END IF;

  RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                  | Qué significa                                             |
| ----------------------- | --------------------------------------------------------- |
| `IF OLD.stock > 0 THEN` | "Si el producto que quieren borrar tiene stock mayor a 0" |
| `RAISE EXCEPTION`       | "Lanza un error y CANCELA la operación"                   |
| `'No puedes borrar...'` | Mensaje de error que verá el usuario                      |
| `%`                     | Se reemplaza por el valor que viene después de la coma    |
| `OLD.nombre, OLD.stock` | Los valores que reemplazan a los `%`                      |
| `RETURN OLD;`           | "Si pasó la validación (stock = 0), permite el borrado"   |

### El trigger:

```sql
CREATE TRIGGER trg_proteger_producto
BEFORE DELETE ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_proteger_producto();
```

> Es `BEFORE` porque necesitamos poder **cancelar** la operación.

### Probar:

```sql
-- Intentar borrar Laptop (tiene stock = 10)
DELETE FROM productos WHERE nombre = 'Laptop';
-- ERROR: No puedes borrar "Laptop" porque tiene 10 unidades en stock

-- Poner stock en 0 y luego borrar → sí funciona
UPDATE productos SET stock = 0 WHERE nombre = 'Laptop';
DELETE FROM productos WHERE nombre = 'Laptop';
```

---

# PARTE 4: Procedimientos almacenados

---

## 13) ¿Qué es un Procedimiento?

Un **Procedimiento** es código guardado en la base de datos que tú llamas **manualmente**.

| Aspecto             | Trigger                    | Procedimiento       |
| ------------------- | -------------------------- | ------------------- |
| ¿Cuándo se ejecuta? | **Solo** (automáticamente) | **Tú lo llamas**    |
| ¿Cómo lo llamas?    | No se llama, se dispara    | Con `CALL nombre()` |

---

## 14) Crear un Procedimiento

```sql
CREATE OR REPLACE PROCEDURE sp_transferir(
  p_origen  INT,
  p_destino INT,
  p_monto   NUMERIC
)
LANGUAGE plpgsql AS $$
BEGIN
  UPDATE cuentas SET saldo = saldo - p_monto WHERE id = p_origen;
  UPDATE cuentas SET saldo = saldo + p_monto WHERE id = p_destino;

  INSERT INTO movimientos (id_origen, id_destino, monto)
  VALUES (p_origen, p_destino, p_monto);
END;
$$;
```

**Palabra por palabra:**

| Código                        | Qué significa                                        |
| ----------------------------- | ---------------------------------------------------- |
| `CREATE OR REPLACE PROCEDURE` | "Crear (o reemplazar) un procedimiento"              |
| `sp_transferir`               | El nombre (`sp_` = stored procedure)                 |
| `p_origen INT`                | Parámetro: el ID de la cuenta origen (número entero) |
| `p_destino INT`               | Parámetro: el ID de la cuenta destino                |
| `p_monto NUMERIC`             | Parámetro: cuánta plata transferir                   |
| `LANGUAGE plpgsql AS $$`      | "El código está en PL/pgSQL, comienza aquí"          |
| `saldo = saldo - p_monto`     | "Al saldo de la cuenta origen, réstale el monto"     |
| `WHERE id = p_origen`         | "Solo a la cuenta de origen"                         |
| `saldo = saldo + p_monto`     | "Al saldo de la cuenta destino, súmale el monto"     |

### Llamar al procedimiento:

```sql
CALL sp_transferir(1, 2, 100000);
```

**Palabra por palabra:**

| Código          | Qué significa                |
| --------------- | ---------------------------- |
| `CALL`          | "Ejecuta este procedimiento" |
| `sp_transferir` | El nombre del procedimiento  |
| `1`             | p_origen = cuenta 1 (Ana)    |
| `2`             | p_destino = cuenta 2 (Pedro) |
| `100000`        | p_monto = $100,000           |

### Probar:

```sql
-- Ver saldos antes
SELECT * FROM cuentas;
-- Ana: 500,000  |  Pedro: 300,000

-- Transferir $100,000 de Ana a Pedro
CALL sp_transferir(1, 2, 100000);

-- Ver saldos después
SELECT * FROM cuentas;
-- Ana: 400,000  |  Pedro: 400,000

-- Ver el movimiento registrado
SELECT * FROM movimientos;
```

---

# PARTE 5: Funciones (retornan un valor)

---

## 15) Diferencia entre Procedimiento y Función

| Aspecto              | PROCEDURE          | FUNCTION             |
| -------------------- | ------------------ | -------------------- |
| ¿Retorna valor?      | ❌ No              | ✅ Sí                |
| ¿Cómo se llama?      | `CALL sp_nombre()` | `SELECT fn_nombre()` |
| ¿Se usa en SELECT?   | ❌ No              | ✅ Sí                |
| ¿Se usa en triggers? | ❌ No              | ✅ Sí                |

---

## 16) Crear una Función

```sql
CREATE OR REPLACE FUNCTION fn_saldo_total()
RETURNS NUMERIC AS $$
DECLARE
  v_total NUMERIC;
BEGIN
  SELECT SUM(saldo) INTO v_total FROM cuentas;
  RETURN v_total;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                     | Qué significa                                       |
| -------------------------- | --------------------------------------------------- |
| `RETURNS NUMERIC`          | "Esta función devuelve un número" (no dice TRIGGER) |
| `DECLARE v_total NUMERIC;` | "Creo una variable llamada v_total"                 |
| `SUM(saldo)`               | "La suma de todos los saldos"                       |
| `INTO v_total`             | "Guarda esa suma dentro de mi variable"             |
| `RETURN v_total;`          | "Devuelve el resultado"                             |

### Llamar la función:

```sql
-- Las funciones se llaman con SELECT
SELECT fn_saldo_total();
-- Resultado: 800000

-- Puedes usarla dentro de consultas
SELECT dueno, saldo,
       ROUND(saldo / fn_saldo_total() * 100, 1) AS porcentaje
FROM cuentas;
```

| dueno | saldo     | porcentaje |
| ----- | --------- | ---------- |
| Ana   | 400000.00 | 50.0       |
| Pedro | 400000.00 | 50.0       |

---

# PARTE 6: Administrar Triggers

---

## 17) Desactivar y reactivar

```sql
-- Desactivar un trigger (deja de funcionar temporalmente)
ALTER TABLE productos DISABLE TRIGGER trg_auditoria_productos;

-- Desactivar TODOS los triggers de una tabla
ALTER TABLE productos DISABLE TRIGGER ALL;

-- Reactivar
ALTER TABLE productos ENABLE TRIGGER trg_auditoria_productos;
ALTER TABLE productos ENABLE TRIGGER ALL;
```

**Palabra por palabra:**

| Código            | Qué significa                      |
| ----------------- | ---------------------------------- |
| `ALTER TABLE`     | "Quiero modificar la tabla"        |
| `DISABLE TRIGGER` | "Desactivar este trigger"          |
| `ENABLE TRIGGER`  | "Reactivar este trigger"           |
| `ALL`             | "Todos los triggers de esta tabla" |

> 💡 Útil para **cargas masivas**: desactivas, cargas miles de filas, reactivas.

---

## 18) Eliminar

```sql
-- Borrar el trigger (la función queda)
DROP TRIGGER trg_auditoria_productos ON productos;

-- Borrar la función también
DROP FUNCTION fn_auditoria();
```

---

## 19) Ver triggers existentes

```sql
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
ORDER BY event_object_table;
```

---

# PARTE 7: Resumen

---

## 20) Errores comunes

| Error                                | Causa                                    | Solución                          |
| ------------------------------------ | ---------------------------------------- | --------------------------------- |
| `function does not return a trigger` | Falta `RETURNS TRIGGER`                  | Agregar `RETURNS TRIGGER`         |
| `record "new" is not assigned`       | Usas `NEW` en un DELETE                  | Usar `OLD` en DELETE              |
| `record "old" is not assigned`       | Usas `OLD` en un INSERT                  | Usar `NEW` en INSERT              |
| El trigger no se dispara             | Está desactivado                         | `ENABLE TRIGGER`                  |
| Loop infinito                        | Trigger A modifica tabla B que dispara B | Agregar condición o desactivar    |
| `RETURN NULL` en BEFORE              | Cancela la operación sin error           | Poner `RETURN NEW` o `RETURN OLD` |

---

## 21) Tabla resumen: NEW y OLD

| Evento | `OLD` | `NEW` |
| ------ | ----- | ----- |
| INSERT | ❌    | ✅    |
| UPDATE | ✅    | ✅    |
| DELETE | ✅    | ❌    |

---

## 22) Tabla resumen: cuándo usar cada cosa

| Quiero...                            | Usar                       |
| ------------------------------------ | -------------------------- |
| Reaccionar automáticamente a cambios | **Trigger**                |
| Ejecutar código cuando yo decida     | **Procedimiento** (`CALL`) |
| Obtener un valor calculado           | **Función** (`SELECT`)     |
| Validar datos antes de guardar       | **Trigger BEFORE**         |
| Registrar cambios en un log          | **Trigger AFTER**          |

---

## 23) Diccionario

| Término            | Qué es                                             |
| ------------------ | -------------------------------------------------- |
| `TRIGGER`          | Código que se ejecuta solo al modificar datos      |
| `BEFORE`           | Antes de guardar                                   |
| `AFTER`            | Después de guardar                                 |
| `FOR EACH ROW`     | Se ejecuta por cada fila afectada                  |
| `NEW`              | La fila nueva (INSERT/UPDATE)                      |
| `OLD`              | La fila vieja (UPDATE/DELETE)                      |
| `TG_OP`            | Variable: dice si fue INSERT, UPDATE o DELETE      |
| `RAISE EXCEPTION`  | Lanza un error y cancela todo                      |
| `RAISE NOTICE`     | Muestra un mensaje (no es error)                   |
| `RETURN NEW`       | Permite la operación                               |
| `RETURN NULL`      | En BEFORE: cancela. En AFTER: se ignora            |
| `FUNCTION`         | Código que retorna un valor. Se llama con `SELECT` |
| `PROCEDURE`        | Código sin retorno. Se llama con `CALL`            |
| `DECLARE`          | Crear variables dentro de una función              |
| `INTO`             | Guardar resultado de SELECT en una variable        |
| `IS DISTINCT FROM` | Comparar valores (funciona bien con NULL)          |
| `DISABLE TRIGGER`  | Apagar un trigger temporalmente                    |
| `DROP TRIGGER`     | Borrar un trigger permanentemente                  |
| `PL/pgSQL`         | El lenguaje de programación de PostgreSQL          |
