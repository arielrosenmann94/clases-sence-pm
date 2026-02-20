<!-- =========================================================
Archivo: resumen_unidad_completo.md
Tema: Última Clase SQL — Resumen + Triggers + SQL Injection
========================================================= -->

# 📋 Última Clase SQL — Resumen de la Unidad + Triggers + SQL Injection

> **Objetivo:** Cerrar la unidad con un resumen general, profundizar en Triggers
> y aprender sobre SQL Injection (seguridad).

---

## 📖 Tabla de Contenidos

1. [Mapa General de la Unidad](#mapa-general-de-la-unidad)
2. [Resumen: Todo lo que vimos](#resumen-todo-lo-que-vimos)
3. [Triggers — Automatización en la Base de Datos](#triggers--automatización-en-la-base-de-datos)
4. [SQL Injection — Seguridad](#sql-injection--seguridad)

---

---

# Mapa General de la Unidad

```
 📐 DISEÑO                    🏗️ ESTRUCTURA               📊 DATOS
 ──────────                   ──────────────               ────────
 ER Modelo                    DDL (CREATE, ALTER, DROP)    DML (INSERT, UPDATE, DELETE)
 Normalización (1NF→3NF)      Tipos de datos               SELECT (WHERE, ORDER BY, LIMIT)
 Entidades/Relaciones         Constraints (PK, FK, etc.)   JOIN (INNER, LEFT, RIGHT, FULL)
                                                           GROUP BY / HAVING
                                                           Subconsultas

 ⚡ MUNDO REAL                🛡️ SEGURIDAD                🤖 AUTOMATIZACIÓN
 ──────────                   ──────────                   ──────────────────
 NULL y sus trampas           SQL Injection                Triggers
 Índices / Performance        Prepared Statements          Funciones (PL/pgSQL)
 Problema N+1                 Mínimo Privilegio            Procedimientos Almacenados
 CASE WHEN / CTE              ORM / WAF                    Auditoría automática
```

---

---

# Resumen: Todo lo que vimos

## DDL — Lenguaje de Definición de Datos (Estructura)

| Comando        | ¿Qué hace?                             |
| -------------- | -------------------------------------- |
| `CREATE TABLE` | Crea una tabla nueva                   |
| `ALTER TABLE`  | Modifica una tabla existente           |
| `DROP TABLE`   | Elimina una tabla completa             |
| `TRUNCATE`     | Vacía todas las filas (la tabla sigue) |

## DML — Lenguaje de Manipulación de Datos

| Comando  | ¿Qué hace?                              |
| -------- | --------------------------------------- |
| `INSERT` | Agrega filas nuevas a una tabla         |
| `UPDATE` | Modifica valores de filas existentes    |
| `DELETE` | Elimina filas de una tabla              |
| `SELECT` | Consulta y lee datos (no modifica nada) |

## Tipos de Datos

| Tipo           | ¿Qué guarda?                    | Ejemplo               |
| -------------- | ------------------------------- | --------------------- |
| `INT`          | Números enteros                 | 42, 100, -5           |
| `NUMERIC(p,s)` | Decimales exactos (para dinero) | 29990.50              |
| `VARCHAR(n)`   | Texto de largo variable         | 'María López'         |
| `TEXT`         | Texto largo                     | Descripciones         |
| `DATE`         | Fecha                           | '2026-02-20'          |
| `TIMESTAMP`    | Fecha y hora                    | '2026-02-20 14:30:00' |
| `BOOLEAN`      | Verdadero o falso               | TRUE / FALSE          |
| `SERIAL`       | ID autoincremental              | 1, 2, 3, ...          |

## Restricciones (Constraints)

| Restricción   | ¿Qué hace?                          |
| ------------- | ----------------------------------- |
| `PRIMARY KEY` | Identifica cada fila de forma única |
| `FOREIGN KEY` | Enlace a otra tabla                 |
| `NOT NULL`    | Campo obligatorio                   |
| `UNIQUE`      | No permite valores repetidos        |
| `DEFAULT`     | Valor automático si no se da uno    |
| `CHECK`       | Valida una condición personalizada  |

## Consultas (SELECT)

| Cláusula   | ¿Qué hace?                                |
| ---------- | ----------------------------------------- |
| `WHERE`    | Filtra filas por condición                |
| `ORDER BY` | Ordena resultados (ASC / DESC)            |
| `LIMIT`    | Limita cantidad de resultados             |
| `DISTINCT` | Elimina duplicados                        |
| `AS`       | Alias (nombre temporal)                   |
| `GROUP BY` | Agrupa filas para funciones de agregación |
| `HAVING`   | Filtra después de agrupar                 |
| `JOIN`     | Combina datos de varias tablas            |

## Funciones de Agregación

| Función   | ¿Qué hace?    |
| --------- | ------------- |
| `COUNT()` | Contar filas  |
| `SUM()`   | Sumar valores |
| `AVG()`   | Promedio      |
| `MIN()`   | Valor mínimo  |
| `MAX()`   | Valor máximo  |

## Tipos de JOIN

| JOIN         | ¿Qué devuelve?                                  |
| ------------ | ----------------------------------------------- |
| `INNER JOIN` | Solo filas con coincidencia en ambas tablas     |
| `LEFT JOIN`  | Todo de la izquierda + coincidencias de la otra |
| `RIGHT JOIN` | Todo de la derecha + coincidencias de la otra   |
| `FULL JOIN`  | Todo de ambas tablas                            |

## Modelo ER (Entidad-Relación)

| Tipo de Relación | Lectura             | En SQL...                   |
| ---------------- | ------------------- | --------------------------- |
| 1:1              | Uno tiene uno       | FK en cualquiera de las dos |
| 1:N              | Uno tiene muchos ⭐ | FK en la tabla del lado N   |
| N:M              | Muchos con muchos   | Tabla intermedia con 2 FKs  |

## Transacciones (ACID)

| Principio        | Significado                               |
| ---------------- | ----------------------------------------- |
| **A**tomicidad   | Todo o nada                               |
| **C**onsistencia | De estado válido a otro estado válido     |
| **I**solamiento  | Las transacciones no se molestan entre sí |
| **D**urabilidad  | Una vez confirmado, es permanente         |

---

---

---

# Triggers — Automatización en la Base de Datos

---

## ¿Qué es un Trigger?

Un **Trigger** es código que se ejecuta **solo, automáticamente**, cuando alguien hace
un INSERT, UPDATE o DELETE en una tabla.

> Tú no lo llamas. Se dispara solo.

**Ejemplo del mundo real:**

- Sin trigger: cada vez que alguien compra, un empleado anota la venta a mano.
- Con trigger: la venta se registra **sola** cada vez que alguien compra.

---

## ¿Dónde se programa un trigger?

Los triggers se programan **directamente en la base de datos**, no en tu aplicación (no en Python, Java ni JavaScript).

```
┌────────────────────────────┐
│   Tu aplicación            │    ← Tu código (Python, Java, JS, etc.)
│   (frontend / backend)     │
└────────────┬───────────────┘
             │ Se conecta a...
             ▼
┌────────────────────────────┐
│   Servidor de Base de Datos│    ← PostgreSQL, MySQL, etc.
│   (local o remoto/nube)    │
│                            │
│   AQUÍ VIVEN LOS TRIGGERS  │    ← El trigger se guarda y ejecuta ACÁ
│   Se ejecutan DENTRO de    │
│   la base de datos.        │
└────────────────────────────┘
```

**¿Se pueden usar en servidores remotos?** Sí. Los triggers funcionan en:

| Lugar                             | Ejemplo                            |
| --------------------------------- | ---------------------------------- |
| Tu computadora local              | PostgreSQL instalado en tu PC      |
| Un servidor en la nube            | AWS RDS, Google Cloud SQL, Azure   |
| Una plataforma como Supabase      | Supabase usa PostgreSQL por debajo |
| Cualquier servidor con PostgreSQL | Un servidor de tu empresa          |

> El trigger vive **dentro de la base de datos**, sin importar dónde esté esa base de datos. Cuando alguien hace un INSERT, UPDATE o DELETE, el trigger se dispara automáticamente **en el servidor donde esté la BD**.

---

## ¿Cuándo se ejecuta?

| Momento  | Significado                                 | ¿Cuándo usarlo?                            |
| -------- | ------------------------------------------- | ------------------------------------------ |
| `BEFORE` | Se ejecuta **antes** de guardar el cambio   | Cuando quieres **cambiar o validar** datos |
| `AFTER`  | Se ejecuta **después** de guardar el cambio | Cuando quieres **registrar o reaccionar**  |

---

## NEW y OLD

Dentro de un trigger hay dos variables especiales para acceder a los datos:

| Variable | Qué contiene                     | Disponible en   |
| -------- | -------------------------------- | --------------- |
| `NEW`    | La fila **nueva** (lo que viene) | INSERT y UPDATE |
| `OLD`    | La fila **vieja** (lo que había) | UPDATE y DELETE |

```sql
NEW.precio   -- el precio NUEVO (el que se quiere guardar)
OLD.precio   -- el precio VIEJO (el que había antes)
NEW.nombre   -- el nombre que se está insertando
OLD.nombre   -- el nombre que se está borrando
```

### Resumen: ¿Cuándo existe cada variable?

| Evento | `OLD`        | `NEW`        |
| ------ | ------------ | ------------ |
| INSERT | ❌ No existe | ✅ Sí existe |
| UPDATE | ✅ Sí existe | ✅ Sí existe |
| DELETE | ✅ Sí existe | ❌ No existe |

> **¿Qué significa ❌ y ✅ acá?**
>
> - ✅ = **la variable EXISTE** y la puedes usar en tu código.
> - ❌ = **la variable NO EXISTE** porque no tiene sentido.
>
> **¿Por qué?**
>
> - En un **INSERT** no hay fila vieja (estás creando una nueva), entonces `OLD` no existe.
> - En un **DELETE** no hay fila nueva (estás borrando), entonces `NEW` no existe.
> - En un **UPDATE** sí hay ambas: la vieja (`OLD`) y la nueva (`NEW`).
>
> ❌ **no significa que se elimina algo**, significa que la variable **no está disponible** para usar.

---

## Las dos piezas de un Trigger

En PostgreSQL necesitas **dos cosas**:

1. Una **función** → el código (qué hacer).
2. Un **trigger** → la regla (cuándo ejecutar la función).

```
FUNCIÓN (el código)  ←──  TRIGGER (la regla que la conecta a la tabla)
```

---

## ⚙️ Tablas para practicar

> **Copia y ejecuta este bloque ANTES de probar los ejemplos.**

```sql
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

---

## Pieza 1: La función — Palabra por palabra

```sql
CREATE OR REPLACE FUNCTION fn_ejemplo()
RETURNS TRIGGER AS $$
BEGIN
  -- aquí va tu código
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

| Código             | Qué significa                                                       |
| ------------------ | ------------------------------------------------------------------- |
| `CREATE`           | "Quiero crear algo nuevo"                                           |
| `OR REPLACE`       | "Si ya existe, reemplázala"                                         |
| `FUNCTION`         | "Lo que estoy creando es una función"                               |
| `fn_ejemplo()`     | El nombre que le doy (los `()` están vacíos porque no recibe datos) |
| `RETURNS TRIGGER`  | "Esta función es para ser usada por un trigger"                     |
| `AS $$`            | "Aquí empieza el código" (ver explicación de `$$` abajo)            |
| `BEGIN`            | "Inicio del bloque de código"                                       |
| `RETURN NEW;`      | "Devuelve la fila nueva para que la operación continúe"             |
| `END;`             | "Fin del bloque de código"                                          |
| `$$`               | "Aquí termina el código" (cierra el `$$` de arriba)                 |
| `LANGUAGE plpgsql` | "El lenguaje usado es PL/pgSQL" (el lenguaje de PostgreSQL)         |

### ¿Qué son los `$$`?

Los `$$` son **delimitadores de texto** en PostgreSQL. Funcionan como las comillas, pero para bloques grandes de código.

```
Comillas normales:   'texto simple'
Dólar-dólar:         $$ bloque de código largo $$
```

**¿Por qué no usar comillas simples `'...'`?**

Porque dentro del código del trigger vas a usar comillas simples para textos (como `'productos'` o `'INSERT'`). Si usaras comillas para delimitar TODO el bloque, se confundiría:

```sql
-- ❌ PROBLEMA: las comillas internas chocan con las externas
CREATE FUNCTION ... AS '
  INSERT INTO auditoria VALUES ('productos');  -- ← ¡ERROR! PostgreSQL no sabe
';                                             --   dónde termina qué

-- ✅ SOLUCIÓN: $$ no choca con las comillas internas
CREATE FUNCTION ... AS $$
  INSERT INTO auditoria VALUES ('productos');  -- ← Sin problema
$$;
```

> **Pensalo así:** `$$` es como un "abre llaves" `{` y "cierra llaves" `}` pero para SQL.
> El primer `$$` = abre. El segundo `$$` = cierra.

### ¿Qué retornar?

| Situación              | Qué poner      | Efecto                    |
| ---------------------- | -------------- | ------------------------- |
| BEFORE INSERT o UPDATE | `RETURN NEW;`  | Permite la operación      |
| BEFORE DELETE          | `RETURN OLD;`  | Permite el borrado        |
| AFTER (cualquiera)     | `RETURN NULL;` | Se ignora (ya se ejecutó) |
| Cancelar la operación  | `RETURN NULL;` | En BEFORE: cancela todo   |

---

## Pieza 2: El trigger — Palabra por palabra

```sql
CREATE TRIGGER trg_ejemplo
BEFORE UPDATE ON productos
FOR EACH ROW
EXECUTE FUNCTION fn_ejemplo();
```

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

> Esas dos piezas juntas forman el trigger completo.

---

---

## Ejemplo 1 — Actualizar fecha automáticamente

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

> **¿Qué pasaría?** Si alguien hace `UPDATE productos SET precio = 950000 WHERE id = 1;`, el trigger automáticamente pone la fecha actual en `updated_at` antes de guardar. El programador no necesita hacerlo.

---

## Ejemplo 2 — Calcular el total de una venta

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

> **¿Qué pasaría?** Al hacer `INSERT INTO ventas (id_producto, cantidad) VALUES (1, 3);` (sin poner total), el trigger busca el precio de la Laptop (900,000), lo multiplica por 3 y pone total = 2,700,000 automáticamente.

---

## Ejemplo 3 — Descontar stock al vender

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

> **¿Qué pasaría?** Si la Laptop tiene stock = 10 y alguien inserta una venta de 3 unidades, el trigger automáticamente hace 10 - 3 = 7 en el stock. Sin que nadie lo haga manualmente.

---

## Ejemplo 4 — Registrar auditoría

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

> **¿Qué pasaría?** Cada vez que alguien inserte, modifique o borre un producto, queda un registro en la tabla `auditoria` con qué se hizo, quién y cuándo. Como una cámara de seguridad en la base de datos.

---

## Ejemplo 5 — Guardar historial de salarios

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

> **¿Qué pasaría?** Si Lucía ganaba $850,000 y le suben el sueldo a $900,000, el trigger automáticamente guarda: "Lucía: antes 850,000 → ahora 900,000" en la tabla de log.

---

## Ejemplo 6 — Impedir un borrado

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

> **¿Qué pasaría?** Si alguien intenta `DELETE FROM productos WHERE nombre = 'Laptop'` y la Laptop tiene stock = 10, el trigger lanza un error: "No puedes borrar Laptop porque tiene 10 unidades en stock" y **cancela** el borrado.

---

---

## Procedimientos vs Funciones

| Aspecto              | PROCEDURE          | FUNCTION             |
| -------------------- | ------------------ | -------------------- |
| ¿Retorna valor?      | ❌ No              | ✅ Sí                |
| ¿Cómo se llama?      | `CALL sp_nombre()` | `SELECT fn_nombre()` |
| ¿Se usa en SELECT?   | ❌ No              | ✅ Sí                |
| ¿Se usa en triggers? | ❌ No              | ✅ Sí                |

### Procedimiento — Palabra por palabra

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

### Llamar al procedimiento — Palabra por palabra

```sql
CALL sp_transferir(1, 2, 100000);
```

| Código          | Qué significa                |
| --------------- | ---------------------------- |
| `CALL`          | "Ejecuta este procedimiento" |
| `sp_transferir` | El nombre del procedimiento  |
| `1`             | p_origen = cuenta 1 (Ana)    |
| `2`             | p_destino = cuenta 2 (Pedro) |
| `100000`        | p_monto = $100,000           |

> **¿Qué pasaría?** `CALL sp_transferir(1, 2, 100000)` le resta $100,000 a Ana (cuenta 1) y se los suma a Pedro (cuenta 2), y además registra el movimiento. Todo en un solo comando.

---

## Función (retorna valor) — Palabra por palabra

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

| Código                     | Qué significa                                       |
| -------------------------- | --------------------------------------------------- |
| `RETURNS NUMERIC`          | "Esta función devuelve un número" (no dice TRIGGER) |
| `DECLARE v_total NUMERIC;` | "Creo una variable llamada v_total"                 |
| `SUM(saldo)`               | "La suma de todos los saldos"                       |
| `INTO v_total`             | "Guarda esa suma dentro de mi variable"             |
| `RETURN v_total;`          | "Devuelve el resultado"                             |

### Llamar la función:

```sql
SELECT fn_saldo_total();
-- Resultado: 800000

-- Se puede usar dentro de consultas
SELECT dueno, saldo,
       ROUND(saldo / fn_saldo_total() * 100, 1) AS porcentaje
FROM cuentas;
```

---

## Administrar Triggers

```sql
-- Desactivar un trigger
ALTER TABLE productos DISABLE TRIGGER trg_auditoria_productos;

-- Desactivar TODOS los triggers de una tabla
ALTER TABLE productos DISABLE TRIGGER ALL;

-- Reactivar
ALTER TABLE productos ENABLE TRIGGER trg_auditoria_productos;
ALTER TABLE productos ENABLE TRIGGER ALL;

-- Borrar el trigger (la función queda)
DROP TRIGGER trg_auditoria_productos ON productos;

-- Borrar la función también
DROP FUNCTION fn_auditoria();

-- Ver triggers existentes
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
ORDER BY event_object_table;
```

| Código            | Qué significa                      |
| ----------------- | ---------------------------------- |
| `ALTER TABLE`     | "Quiero modificar la tabla"        |
| `DISABLE TRIGGER` | "Desactivar este trigger"          |
| `ENABLE TRIGGER`  | "Reactivar este trigger"           |
| `ALL`             | "Todos los triggers de esta tabla" |

> 💡 Útil para **cargas masivas**: desactivas, cargas miles de filas, reactivas.

---

## Errores comunes con Triggers

| Error                                | Causa                                  | Solución                          |
| ------------------------------------ | -------------------------------------- | --------------------------------- |
| `function does not return a trigger` | Falta `RETURNS TRIGGER`                | Agregar `RETURNS TRIGGER`         |
| `record "new" is not assigned`       | Usas `NEW` en un DELETE                | Usar `OLD` en DELETE              |
| `record "old" is not assigned`       | Usas `OLD` en un INSERT                | Usar `NEW` en INSERT              |
| El trigger no se dispara             | Está desactivado                       | `ENABLE TRIGGER`                  |
| Loop infinito                        | Trigger A modifica tabla que dispara A | Agregar condición o desactivar    |
| `RETURN NULL` en BEFORE              | Cancela la operación sin error         | Poner `RETURN NEW` o `RETURN OLD` |

---

## Resumen: ¿Cuándo usar cada cosa?

| Quiero...                            | Usar                       |
| ------------------------------------ | -------------------------- |
| Reaccionar automáticamente a cambios | **Trigger**                |
| Ejecutar código cuando yo decida     | **Procedimiento** (`CALL`) |
| Obtener un valor calculado           | **Función** (`SELECT`)     |
| Validar datos antes de guardar       | **Trigger BEFORE**         |
| Registrar cambios en un log          | **Trigger AFTER**          |

---

## Diccionario de Triggers

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
| `RETURN NEW`       | Permite la operación                               |
| `RETURN NULL`      | En BEFORE: cancela. En AFTER: se ignora            |
| `FUNCTION`         | Código que retorna un valor. Se llama con `SELECT` |
| `PROCEDURE`        | Código sin retorno. Se llama con `CALL`            |
| `DECLARE`          | Crear variables dentro de una función              |
| `INTO`             | Guardar resultado de SELECT en una variable        |
| `IS DISTINCT FROM` | Comparar valores (funciona bien con NULL)          |
| `PL/pgSQL`         | El lenguaje de programación de PostgreSQL          |

---

---

---

# SQL Injection — Seguridad

---

## ¿Qué es SQL Injection?

**SQL Injection (SQLi)** es una técnica de ataque donde un atacante **inserta o "inyecta" código SQL malicioso** a través de los campos de entrada de una aplicación (formularios, URLs, etc.) para manipular la base de datos.

> **Para los que recién empiezan en programación:** SQL Injection NO es un problema de la base de datos en sí. Es un problema de **cómo el programador escribe el código** que conecta la aplicación con la base de datos. Si el programador no tiene cuidado, un atacante puede "colar" comandos SQL a través de un simple formulario web.

### Analogía

Imaginá que tenés un portero en un edificio que deja pasar a cualquiera que diga _"soy residente"_. Un atacante podría decir:

> _"Soy residente, y además dejá pasar a todos mis amigos y abrí todas las puertas"_

El portero, sin verificar, ejecuta todo lo que le dijeron. **Eso es SQL Injection.**

---

## ¿Dónde ocurre SQL Injection?

SQL Injection ocurre en **cualquier lugar donde una aplicación reciba datos del usuario y los use para armar una consulta SQL**. No ocurre dentro de la base de datos directamente — ocurre en el código del programador.

```
┌──────────────────────────────────────────────────────────────┐
│  👤 USUARIO (o atacante)                                     │
│  Escribe algo en un formulario, URL, campo de búsqueda...   │
└──────────────────────┬───────────────────────────────────────┘
                       │ El texto viaja al servidor
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  💻 CÓDIGO DEL PROGRAMADOR (backend)                         │
│  Python, Java, PHP, Node.js, etc.                            │
│                                                              │
│  🔴 ACÁ ES DONDE OCURRE EL PROBLEMA                         │
│  Si el código MEZCLA el texto del usuario con el SQL         │
│  sin protegerlo, el atacante puede inyectar comandos.        │
└──────────────────────┬───────────────────────────────────────┘
                       │ Envía la consulta SQL armada
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  🗄️ BASE DE DATOS (PostgreSQL, MySQL, etc.)                  │
│  Ejecuta TODO lo que le llega. No sabe si es legítimo        │
│  o malicioso — simplemente ejecuta el SQL que recibe.        │
└──────────────────────────────────────────────────────────────┘
```

### ¿Qué tipo de aplicaciones son vulnerables?

| Tipo de aplicación                  | ¿Puede ser vulnerable? | ¿Dónde está el riesgo?                         |
| ----------------------------------- | ---------------------- | ---------------------------------------------- |
| Páginas web con login               | ✅ Sí                  | Campos de usuario y contraseña                 |
| Tiendas online                      | ✅ Sí                  | Buscador de productos, filtros, URLs           |
| APIs (aplicaciones móviles)         | ✅ Sí                  | Parámetros que envía la app al servidor        |
| Sistemas internos de empresas       | ✅ Sí                  | Cualquier formulario que consulte la BD        |
| Sitios con formularios de contacto  | ✅ Sí                  | Si los datos del formulario se guardan con SQL |
| Páginas estáticas sin base de datos | ❌ No                  | No usan SQL → no hay nada que inyectar         |

> **Regla simple:** Si tu aplicación usa SQL y recibe datos del usuario → puede ser vulnerable a SQL Injection si no se protege correctamente.

---

## ¿Por qué es tan peligroso?

| Impacto                      | Descripción                                                                             |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| 🔓 **Acceso no autorizado**  | El atacante puede saltear el login y acceder como administrador                         |
| 📋 **Robo de datos**         | Puede extraer toda la información de la base de datos (usuarios, contraseñas, tarjetas) |
| ✏️ **Modificación de datos** | Puede alterar registros, cambiar precios, notas, roles de usuario                       |
| 🗑️ **Eliminación de datos**  | Puede borrar tablas enteras o toda la base de datos                                     |
| 💻 **Ejecución de comandos** | En casos extremos, puede ejecutar comandos en el servidor                               |

> SQL Injection ha sido la **vulnerabilidad #1 del OWASP Top 10** durante más de una década. Es responsable de las filtraciones de datos más grandes de la historia.

---

## ¿Qué comandos SQL puede inyectar un atacante?

El atacante no inventa comandos nuevos — usa los **mismos comandos SQL que nosotros aprendimos**, pero los usa con intención maliciosa. Esta es la lista completa de lo que puede intentar inyectar:

### Comandos para ROBAR información

| Comando inyectado                                          | Qué logra el atacante                                          |
| ---------------------------------------------------------- | -------------------------------------------------------------- |
| `' OR '1'='1`                                              | Hace que toda condición sea verdadera → ve TODOS los registros |
| `' OR 1=1 --`                                              | Igual pero comentando el resto de la consulta                  |
| `UNION SELECT username, password FROM usuarios`            | Combina su consulta con otra para robar datos de otra tabla    |
| `UNION SELECT table_name FROM information_schema.tables`   | Descubre los nombres de TODAS las tablas de la base de datos   |
| `UNION SELECT column_name FROM information_schema.columns` | Descubre los nombres de TODAS las columnas                     |

### Comandos para DESTRUIR datos

| Comando inyectado               | Qué logra el atacante                                |
| ------------------------------- | ---------------------------------------------------- |
| `'; DROP TABLE usuarios; --`    | **Elimina la tabla completa** de usuarios            |
| `'; DROP TABLE productos; --`   | Elimina cualquier tabla que quiera                   |
| `'; DELETE FROM usuarios; --`   | Borra todas las filas de una tabla                   |
| `'; TRUNCATE TABLE pedidos; --` | Vacía una tabla entera (sin posibilidad de ROLLBACK) |

### Comandos para MODIFICAR datos

| Comando inyectado                                           | Qué logra el atacante                       |
| ----------------------------------------------------------- | ------------------------------------------- |
| `'; UPDATE usuarios SET rol = 'admin' WHERE id=1; --`       | Se da permisos de administrador             |
| `'; UPDATE productos SET precio = 1; --`                    | Cambia todos los precios a $1               |
| `'; UPDATE usuarios SET password = '1234'; --`              | Cambia la contraseña de todos los usuarios  |
| `'; INSERT INTO usuarios VALUES (999,'hacker','admin'); --` | Crea un usuario nuevo con permisos de admin |

### Comandos para SALTEAR el login

| Comando inyectado en el campo de usuario | Qué logra                                |
| ---------------------------------------- | ---------------------------------------- |
| `admin' --`                              | Entra como admin sin contraseña          |
| `' OR '1'='1' --`                        | Entra como el primer usuario de la tabla |
| `' OR 1=1 LIMIT 1 --`                    | Entra como el primer usuario             |
| `admin'/*`                               | Comenta con `/* */` en vez de `--`       |

### Los "trucos" que usa el atacante

| Truco          | Qué es                                                | Ejemplo            |
| -------------- | ----------------------------------------------------- | ------------------ |
| `'`            | Cierra la comilla que abrió el código del programador | La base de todo    |
| `--`           | Comentario SQL: ignora todo lo que viene después      | `admin' --`        |
| `/*...*/`      | Comentario de bloque                                  | `admin'/*`         |
| `;`            | Termina un comando y empieza otro                     | `'; DROP TABLE...` |
| `OR 1=1`       | Condición siempre verdadera                           | Ve todos los datos |
| `UNION SELECT` | Combina resultados de otra consulta                   | Roba datos         |

---

## ¿Cómo se produce? — Paso a paso

### El flujo normal (sin ataque)

```
Usuario escribe: "ariel"
                    ↓
La aplicación construye: SELECT * FROM usuarios WHERE nombre = 'ariel'
                    ↓
La base de datos ejecuta la consulta normalmente
                    ↓
Devuelve: los datos del usuario "ariel"
```

### El flujo con inyección (ataque)

```
Atacante escribe: ' OR '1'='1
                    ↓
La aplicación construye: SELECT * FROM usuarios WHERE nombre = '' OR '1'='1'
                    ↓
La base de datos evalúa: '1'='1' → siempre es VERDADERO
                    ↓
Devuelve: TODOS los usuarios de la tabla ☠️
```

### ¿Por qué funciona?

Porque la aplicación **concatena directamente** la entrada del usuario en la consulta SQL sin ninguna validación:

```python
# ❌ CÓDIGO VULNERABLE — Nunca hacer esto
query = "SELECT * FROM usuarios WHERE nombre = '" + input_usuario + "'"
```

**Desglosemos qué pasa letra por letra:**

```
El código arma el string así:

"SELECT * FROM usuarios WHERE nombre = '"  +  input_usuario  +  "'"
                                                    ↑
                                          El usuario pone: ' OR '1'='1

Resultado final:
SELECT * FROM usuarios WHERE nombre = '' OR '1'='1'
                                       │            │
                                       │            └── '1'='1' → SIEMPRE verdadero
                                       └── nombre = '' → falso, pero no importa
                                           porque el OR hace que TODO sea verdadero
```

> El problema es que el texto del usuario se **mezcla con el código SQL**, y la base de datos no puede distinguir entre los dos.

---

## Tipos de SQL Injection

### 1. 🎯 In-Band SQLi (Clásica)

El atacante usa el **mismo canal** para inyectar y recibir los resultados.

#### a) Error-Based

Provoca errores en la base de datos que **revelan información** en los mensajes de error.

```sql
-- El atacante introduce:
' AND 1=CONVERT(int, (SELECT TOP 1 table_name FROM information_schema.tables)) --

-- El error devuelve el nombre de una tabla real
```

**Palabra por palabra:**

| Código                      | Qué hace el atacante                                           |
| --------------------------- | -------------------------------------------------------------- |
| `'`                         | Cierra la comilla del valor original                           |
| `AND 1=CONVERT(int, ...)`   | Intenta convertir un texto (nombre de tabla) a número          |
| `information_schema.tables` | Tabla del sistema que contiene los nombres de TODAS las tablas |
| `--`                        | Comenta (ignora) el resto de la consulta original              |

> La conversión falla, pero el **mensaje de error** revela el nombre de la tabla. El atacante repite esto para descubrir toda la estructura.

#### b) Union-Based

Usa `UNION SELECT` para **combinar resultados** de otras tablas.

```sql
-- Input del atacante:
' UNION SELECT username, password FROM users --
```

**¿Qué pasa paso a paso?**

```sql
-- La consulta original era:
SELECT nombre, email FROM productos WHERE id = '...'

-- Con la inyección se convierte en:
SELECT nombre, email FROM productos WHERE id = ''
UNION
SELECT username, password FROM users --'
```

**Palabra por palabra:**

| Código                      | Qué hace                                                   |
| --------------------------- | ---------------------------------------------------------- |
| `'`                         | Cierra la comilla del id original (queda vacío: `id = ''`) |
| `UNION`                     | "Combina los resultados de esta consulta con otra"         |
| `SELECT username, password` | "De la otra consulta, traeme usuario y contraseña"         |
| `FROM users`                | "Desde la tabla de usuarios"                               |
| `--`                        | "Comenta todo lo que viene después" (ignora el `'` final)  |

> Ahora la página muestra los productos **y también los usuarios con sus contraseñas**.

### 2. 🔇 Blind SQLi (A ciegas)

El atacante **no ve los resultados directamente**, pero puede inferir información.

#### a) Boolean-Based

Hace preguntas de **verdadero/falso** y observa cómo cambia la página.

```sql
-- ¿La primera letra del usuario admin es 'a'?
' AND (SELECT SUBSTRING(username,1,1) FROM users WHERE id=1) = 'a' --
```

**Palabra por palabra:**

| Código                    | Qué hace                                        |
| ------------------------- | ----------------------------------------------- |
| `SUBSTRING(username,1,1)` | "Toma solo la primera letra del campo username" |
| `FROM users WHERE id=1`   | "Del usuario con id 1"                          |
| `= 'a'`                   | "¿Esa letra es 'a'?"                            |

> Si la página carga normalmente → la respuesta es **SÍ**.
> Si la página se rompe o cambia → la respuesta es **NO**.
> El atacante repite letra por letra hasta descubrir el nombre completo.

#### b) Time-Based

Usa **delays** (retrasos) para inferir información.

```sql
-- Si la primera letra es 'a', esperar 5 segundos
' AND IF((SELECT SUBSTRING(username,1,1) FROM users WHERE id=1)='a', SLEEP(5), 0) --
```

**Palabra por palabra:**

| Código         | Qué hace                                                    |
| -------------- | ----------------------------------------------------------- |
| `IF(condición` | "Si se cumple la condición..."                              |
| `SLEEP(5)`     | "...espera 5 segundos" (señal de que la respuesta es SÍ)    |
| `0`            | "...si no se cumple, no esperes" (respuesta inmediata = NO) |

> El atacante mide el tiempo de respuesta. Si tardó 5 segundos → la letra es 'a'.

---

## Ejemplos de ataque paso a paso

### Ejemplo 1: Bypass de Login

**Formulario de login normal:**

```
Usuario: admin
Contraseña: mi_password_123
```

**Consulta que genera la aplicación:**

```sql
SELECT * FROM usuarios
WHERE username = 'admin' AND password = 'mi_password_123'
```

**Ataque — el atacante escribe en el campo de usuario:**

```
admin' --
```

**Consulta resultante:**

```sql
SELECT * FROM usuarios
WHERE username = 'admin' --' AND password = 'lo_que_sea'
```

**Palabra por palabra:**

| Parte de la consulta            | Qué pasa                                               |
| ------------------------------- | ------------------------------------------------------ |
| `username = 'admin'`            | Busca el usuario admin (esto es válido)                |
| `--`                            | Los dos guiones **comentan** todo lo que viene después |
| `' AND password = 'lo_que_sea'` | **ESTO DESAPARECE** — está comentado                   |

> La verificación de contraseña **desaparece por completo**. El atacante entra como admin sin conocer la contraseña.

---

### Ejemplo 2: Extracción de datos con UNION

**URL normal:**

```
https://tienda.com/producto?id=5
```

**Consulta interna:**

```sql
SELECT nombre, precio FROM productos WHERE id = 5
```

**URL maliciosa:**

```
https://tienda.com/producto?id=5 UNION SELECT username, password FROM usuarios --
```

**Consulta resultante:**

```sql
SELECT nombre, precio FROM productos WHERE id = 5
UNION
SELECT username, password FROM usuarios --
```

> `UNION` combina dos consultas. Ahora la página muestra los productos **y también los usuarios con sus contraseñas**.

---

### Ejemplo 3: Eliminación de una tabla

**Input del atacante:**

```
'; DROP TABLE usuarios; --
```

**Consulta resultante:**

```sql
SELECT * FROM productos WHERE nombre = ''; DROP TABLE usuarios; --'
```

**Palabra por palabra:**

| Parte                  | Qué pasa                                                                |
| ---------------------- | ----------------------------------------------------------------------- |
| `nombre = ''`          | Busca un producto con nombre vacío (no encuentra nada, pero no importa) |
| `;`                    | Termina la primera consulta                                             |
| `DROP TABLE usuarios;` | **Ejecuta un SEGUNDO comando**: elimina toda la tabla usuarios          |
| `--`                   | Comenta lo que sobra                                                    |

> Esto ejecuta **dos comandos**: el SELECT vacío y luego `DROP TABLE usuarios`, eliminando **toda** la tabla de usuarios.

---

### Ejemplo 4: Bypass con OR

**El atacante escribe en ambos campos del login:**

```
Usuario: ' OR 1=1 --
Contraseña: (cualquier cosa)
```

**Consulta resultante:**

```sql
SELECT * FROM usuarios
WHERE username = '' OR 1=1 --' AND password = 'cualquier cosa'
```

**Palabra por palabra:**

| Parte           | Qué pasa                                                           |
| --------------- | ------------------------------------------------------------------ |
| `username = ''` | ¿El username es vacío? No, es falso                                |
| `OR 1=1`        | **PERO** 1=1 siempre es verdadero → toda la condición es verdadera |
| `--`            | Comenta la parte de la contraseña                                  |

> `1=1` siempre es verdadero, así que devuelve **todos los usuarios**. El sistema toma el primero (generalmente el admin).

---

---

## 🛡️ Formas de protegerse — Palabra por palabra

### 1. ✅ Consultas Parametrizadas (la defensa más efectiva)

**Separa el código SQL de los datos del usuario.**

```python
# ✅ Python con psycopg2 (PostgreSQL)
cursor.execute(
    "SELECT * FROM usuarios WHERE username = %s AND password = %s",
    (username, password)
)
```

**Palabra por palabra:**

| Código                                         | Qué significa                                           |
| ---------------------------------------------- | ------------------------------------------------------- |
| `"SELECT * FROM usuarios WHERE username = %s"` | La consulta SQL con **marcadores** `%s` en vez de datos |
| `%s`                                           | "Aquí va un dato, pero NO lo mezcles con el SQL"        |
| `(username, password)`                         | Los valores que la BD insertará **de forma segura**     |

```java
// ✅ Java con PreparedStatement
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM usuarios WHERE username = ? AND password = ?"
);
stmt.setString(1, username);
stmt.setString(2, password);
```

**Palabra por palabra:**

| Código                   | Qué significa                                                 |
| ------------------------ | ------------------------------------------------------------- |
| `?`                      | Marcador: "aquí irá un dato, pero no lo interpretes como SQL" |
| `setString(1, username)` | "En el primer `?`, pon el valor de username como TEXTO"       |
| `setString(2, password)` | "En el segundo `?`, pon el valor de password como TEXTO"      |

```javascript
// ✅ Node.js con pg (PostgreSQL)
const result = await pool.query(
  "SELECT * FROM usuarios WHERE username = $1 AND password = $2",
  [username, password],
);
```

**Palabra por palabra:**

| Código                 | Qué significa                           |
| ---------------------- | --------------------------------------- |
| `$1`                   | "El primer valor del array"             |
| `$2`                   | "El segundo valor del array"            |
| `[username, password]` | Los valores en orden, separados del SQL |

> **¿Por qué funciona?** Porque la base de datos recibe el SQL y los datos **por separado**. Primero compila la consulta y después inserta los valores. El input del usuario **nunca se interpreta como código SQL**.

---

### 2. ✅ ORM (Object-Relational Mapping)

Los frameworks modernos usan ORMs que generan consultas parametrizadas **automáticamente**.

```python
# ✅ Django ORM — seguro por defecto
user = User.objects.filter(username=username, password=password).first()
```

**Palabra por palabra:**

| Código                       | Qué significa                                             |
| ---------------------------- | --------------------------------------------------------- |
| `User.objects`               | "Accede a la tabla de usuarios"                           |
| `.filter(username=username)` | "Filtra donde username sea igual al valor de la variable" |
| `.first()`                   | "Trae solo el primer resultado"                           |

> Django internamente convierte esto en una consulta parametrizada. Nunca concatena.

```python
# ❌ VULNERABLE incluso con Django
User.objects.raw(f"SELECT * FROM users WHERE name = '{name}'")

# ✅ SEGURO con raw queries
User.objects.raw("SELECT * FROM users WHERE name = %s", [name])
```

> Incluso usando un ORM, si usás métodos de **consulta raw/cruda** sin parametrizar, seguís siendo vulnerable.

---

### 3. ✅ Validación y Sanitización de Entrada

Verificar que los datos del usuario cumplan con lo esperado **antes** de usarlos.

```python
# Validar que un ID sea numérico
def get_product(request, product_id):
    if not str(product_id).isdigit():
        return HttpResponse("ID inválido", status=400)

    # Ahora sí, usar el ID con consulta parametrizada
    cursor.execute("SELECT * FROM productos WHERE id = %s", [product_id])
```

**Reglas de validación:**

| Tipo de dato  | Validación                                  |
| ------------- | ------------------------------------------- |
| IDs numéricos | Solo dígitos (`int()` o regex `^\d+$`)      |
| Emails        | Formato válido con regex o librería         |
| Nombres       | Solo letras, espacios, tildes (whitelist)   |
| Fechas        | Formato específico (YYYY-MM-DD)             |
| Opciones      | Comparar contra lista de valores permitidos |

---

### 4. ✅ Principio de Mínimo Privilegio

La cuenta de base de datos que usa la aplicación debe tener **solo los permisos necesarios**.

```sql
-- Crear un usuario con permisos limitados
CREATE USER app_user WITH PASSWORD 'password_seguro';

-- Solo dar permisos de lectura e inserción
GRANT SELECT, INSERT ON productos TO app_user;
GRANT SELECT ON categorias TO app_user;

-- NUNCA dar estos permisos a la aplicación:
-- ❌ GRANT ALL PRIVILEGES
-- ❌ GRANT DROP
-- ❌ GRANT ALTER
-- ❌ Usar el usuario postgres/root directamente
```

**Palabra por palabra:**

| Código                            | Qué significa                                       |
| --------------------------------- | --------------------------------------------------- |
| `CREATE USER app_user`            | "Crea un usuario de base de datos llamado app_user" |
| `WITH PASSWORD 'password_seguro'` | "Con esta contraseña"                               |
| `GRANT SELECT, INSERT`            | "Solo dale permiso de leer e insertar"              |
| `ON productos`                    | "Solamente en esa tabla"                            |
| `TO app_user`                     | "A ese usuario"                                     |

> Así, incluso si hay una inyección exitosa, el atacante **no puede borrar tablas ni modificar la estructura**.

---

### 5. ✅ Procedimientos Almacenados Seguros

```sql
-- ✅ SEGURO — usa parámetros
CREATE OR REPLACE FUNCTION buscar_usuario(p_username TEXT)
RETURNS TABLE(id INT, username TEXT, email TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.username, u.email
    FROM usuarios u
    WHERE u.username = p_username;
END;
$$ LANGUAGE plpgsql;
```

**Palabra por palabra:**

| Código                          | Qué significa                                                        |
| ------------------------------- | -------------------------------------------------------------------- |
| `p_username TEXT`               | "Recibe un parámetro de texto llamado p_username"                    |
| `RETURNS TABLE(...)`            | "Devuelve una tabla con estas columnas"                              |
| `WHERE u.username = p_username` | "Filtra por el parámetro (la BD lo trata como DATO, no como código)" |

```sql
-- ❌ VULNERABLE — concatena strings dentro del procedimiento
CREATE OR REPLACE FUNCTION buscar_usuario_mal(p_username TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE 'SELECT * FROM usuarios WHERE username = ''' || p_username || '''';
END;
$$ LANGUAGE plpgsql;
```

| Código                          | Por qué es peligroso                                 |
| ------------------------------- | ---------------------------------------------------- |
| `EXECUTE '...' \|\| p_username` | Concatena el parámetro directamente en el SQL string |
|                                 | El input del usuario SE MEZCLA con el código SQL     |
|                                 | **Mismo problema que antes**: SQL Injection          |

---

### 6. ✅ WAF (Web Application Firewall)

Un WAF puede detectar y bloquear patrones de SQL Injection **antes de que lleguen a la aplicación**.

**Patrones que un WAF detecta:**

- `' OR 1=1`
- `UNION SELECT`
- `DROP TABLE`
- `'; --`
- Codificaciones evasivas (hex, URL encoding, etc.)

---

---

## 🔒 Checklist de seguridad contra SQL Injection

- [ ] **Usar consultas parametrizadas** en todas las interacciones con la BD
- [ ] **Usar un ORM** cuando sea posible
- [ ] **Validar toda entrada** del usuario (tipo, longitud, formato)
- [ ] **Aplicar mínimo privilegio** en las cuentas de base de datos
- [ ] **No mostrar errores de BD** al usuario final (usar mensajes genéricos)
- [ ] **Mantener el software actualizado** (BD, frameworks, librerías)
- [ ] **Usar HTTPS** para proteger datos en tránsito
- [ ] **Hashear contraseñas** — nunca almacenarlas en texto plano
- [ ] **Realizar auditorías de seguridad** periódicas

---

## ❌ Lo que NUNCA se debe hacer

```python
# ❌ Concatenar strings
query = "SELECT * FROM users WHERE name = '" + user_input + "'"

# ❌ Usar f-strings con SQL
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ❌ Usar .format()
query = "SELECT * FROM users WHERE name = '{}'".format(user_input)

# ❌ Usar % formatting
query = "SELECT * FROM users WHERE name = '%s'" % user_input
```

**¿Qué tienen en común?** Todos mezclan el input del usuario directamente con el código SQL. La base de datos no puede distinguir qué es código y qué es dato.

---

## Resumen visual de defensas

```
                    🛡️ CAPAS DE DEFENSA
┌──────────────────────────────────────────────────┐
│  Capa 1 — WAF (filtrado externo)                 │
│  ┌──────────────────────────────────────────────┐│
│  │  Capa 2 — Validación de entrada              ││
│  │  ┌──────────────────────────────────────────┐││
│  │  │  Capa 3 — Consultas parametrizadas       │││
│  │  │  ┌──────────────────────────────────────┐│││
│  │  │  │  Capa 4 — Mínimo privilegio en BD    ││││
│  │  │  │  ┌──────────────────────────────────┐││││
│  │  │  │  │  Capa 5 — Monitoreo y logging    │││││
│  │  │  │  └──────────────────────────────────┘││││
│  │  │  └──────────────────────────────────────┘│││
│  │  └──────────────────────────────────────────┘││
│  └──────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

> **La seguridad es por capas.** Ninguna defensa individual es suficiente. Combiná múltiples capas para una protección real.

---

## 🔗 Recursos adicionales

| Recurso                 | Enlace                                                                  | Descripción                          |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------ |
| **OWASP SQL Injection** | [owasp.org/sqli](https://owasp.org/www-community/attacks/SQL_Injection) | Guía oficial de referencia           |
| **PortSwigger Academy** | [portswigger.net](https://portswigger.net/web-security/sql-injection)   | Labs interactivos gratuitos          |
| **OWASP Top 10**        | [owasp.org/top10](https://owasp.org/www-project-top-ten/)               | Las 10 vulnerabilidades más críticas |

### 🧪 Entornos de práctica seguros

> Estos entornos están **diseñados para ser hackeados** de forma legal y educativa:

- **DVWA** (Damn Vulnerable Web Application) — App PHP vulnerable a propósito
- **SQLi-labs** — Laboratorio específico para practicar SQL Injection
- **Hack The Box** — Plataforma de CTF con máquinas vulnerables
- **TryHackMe** — Cursos guiados de ciberseguridad

---

> **⚠️ Aviso Legal:** Este contenido es **exclusivamente educativo**. Realizar ataques de SQL Injection contra sistemas sin autorización explícita es **ilegal** y puede acarrear consecuencias penales. Siempre practicá en entornos controlados y con permiso.
