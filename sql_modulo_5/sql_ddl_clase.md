<!-- =========================================================
Archivo: sql_ddl_clase.md
Tema: Sentencias para la Definición de Tablas — Parte 1
AE4: Implementar estructuras de datos relacionales usando DDL
========================================================= -->

# 🏗️ DDL — El Lenguaje que Construye el Mundo de los Datos

---

---

# 📚 PARTE 1 — TEORÍA

---

## 🗺️ ¿Qué vamos a aprender hoy?

| Tema                      | Pregunta clave                                      |
| ------------------------- | --------------------------------------------------- |
| 🏗️ DDL                    | ¿Cómo creo tablas, las modifico o las elimino?      |
| 📐 Tipos de datos         | ¿Qué tipo de información guarda cada columna?       |
| 🚧 CREATE TABLE           | ¿Cómo defino la estructura de una tabla desde cero? |
| 🔒 Restricción de nulidad | ¿Cómo obligo a que un campo siempre tenga valor?    |

---

---

## 1️⃣ DDL — Data Definition Language

---

### La gran analogía: El Arquitecto vs El Habitante

Imagina que estás construyendo un **edificio de departamentos**:

| Rol                  | ¿Qué hace?                                                                        | En SQL es... |
| -------------------- | --------------------------------------------------------------------------------- | ------------ |
| 🏗️ **El Arquitecto** | Diseña los planos: cuántos pisos, cuántas habitaciones, qué tamaño tiene cada una | **DDL**      |
| 🏠 **El Habitante**  | Pone los muebles, cambia la decoración, saca cosas                                | **DML**      |

> El **arquitecto** (DDL) decide que el edificio tendrá 10 pisos con departamentos de 2 y 3 habitaciones.
> El **habitante** (DML) pone su cama, su silla y su mesa dentro del departamento.
>
> **No puedes poner muebles si no existe el edificio primero.**
> Por eso DDL viene ANTES que DML.

---

### ¿Qué es DDL exactamente?

**DDL** = **Data Definition Language** (Lenguaje de **Definición** de Datos).

Es el conjunto de comandos SQL para **crear, modificar y eliminar la estructura** de la base de datos: tablas, columnas, restricciones, índices, vistas.

> **DDL no toca los datos** (las filas).
> DDL toca **la estructura** (las tablas y columnas donde los datos van a vivir).

---

### DDL vs DML — La diferencia definitiva

|                  | DDL 🏗️                               | DML 🏠                                 |
| ---------------- | ------------------------------------ | -------------------------------------- |
| **Sigla**        | Data **Definition** Language         | Data **Manipulation** Language         |
| **¿Qué afecta?** | La **estructura** (tablas, columnas) | Los **datos** (filas)                  |
| **Analogía**     | Diseñar el edificio                  | Amueblar los departamentos             |
| **Comandos**     | `CREATE`, `ALTER`, `DROP`            | `INSERT`, `UPDATE`, `DELETE`, `SELECT` |
| **Ejemplo**      | _"Crear una tabla con 5 columnas"_   | _"Insertar un cliente nuevo"_          |

> **DDL** = ¿Cómo se ve la tabla? (estructura)
> **DML** = ¿Qué hay dentro de la tabla? (datos)

---

### Los 3 comandos principales de DDL

| Comando        | ¿Qué hace?                   | Analogía                                           |
| -------------- | ---------------------------- | -------------------------------------------------- |
| `CREATE TABLE` | Crea una tabla nueva         | Construir un edificio nuevo                        |
| `ALTER TABLE`  | Modifica una tabla existente | Remodelar: agregar una habitación, tirar una pared |
| `DROP TABLE`   | Elimina una tabla completa   | Demoler el edificio entero                         |

```sql
-- CREAR una tabla
CREATE TABLE empleados ( ... );

-- MODIFICAR una tabla (agregar columna)
ALTER TABLE empleados ADD fecha_ingreso DATE;

-- ELIMINAR una tabla completa (estructura + datos)
DROP TABLE empleados;
```

---

### 🧨 La diferencia entre DROP, DELETE y TRUNCATE

Esta es una pregunta clásica de entrevista laboral:

| Comando                | Tipo | ¿Qué borra?                                            | ¿La tabla sigue existiendo? |
| ---------------------- | ---- | ------------------------------------------------------ | --------------------------- |
| `DELETE FROM tabla`    | DML  | Las **filas** (con WHERE = algunas, sin WHERE = todas) | ✅ Sí                       |
| `TRUNCATE TABLE tabla` | DDL  | **Todas** las filas (más rápido que DELETE)            | ✅ Sí                       |
| `DROP TABLE tabla`     | DDL  | **Todo**: filas + columnas + la tabla misma            | ❌ No                       |

> **DELETE** = vaciar los departamentos (el edificio sigue en pie).
> **TRUNCATE** = vaciar TODOS los departamentos de golpe (el edificio sigue).
> **DROP** = demoler el edificio completo. Ya no existe.

---

### Otros usos de DDL (para conocer)

DDL no solo sirve para tablas. También puede:

| Comando                          | ¿Qué hace?                                       |
| -------------------------------- | ------------------------------------------------ |
| `CREATE INDEX`                   | Crea un índice para acelerar búsquedas           |
| `CREATE VIEW`                    | Crea una "vista virtual" (una consulta guardada) |
| `CREATE DATABASE`                | Crea una base de datos nueva                     |
| `ALTER TABLE ... ADD CONSTRAINT` | Agrega restricciones (PK, FK, CHECK)             |

> Hoy nos enfocamos en **CREATE TABLE** porque es la base de todo.

---

---

## 2️⃣ Tipos de Datos — El Guardia de la Puerta

---

### ¿Por qué importan los tipos de datos?

Imagina que tienes un **formulario en papel** para registrar empleados:

```
Nombre:  [___________________]  ← Solo texto
Edad:    [___]                  ← Solo números
Email:   [___________________]  ← Texto con formato especial
Activo:  [Sí / No]             ← Solo dos opciones
```

¿Qué pasa si alguien escribe "veinticinco" en el campo de Edad? **No sirve**.
¿Y si pone un número en el campo de Nombre? **Tampoco**.

> Los **tipos de datos** en SQL son exactamente eso: un **guardia en la puerta** de cada columna
> que solo deja pasar el tipo de información correcto.

---

### Historia real: El bug del año 2000 (Y2K)

**Y2K** viene de "**Y**ear **2** **K**ilo" (Kilo = 1000, es decir, el año 2000).

En los años 60, la memoria de las computadoras era **carísima**. Para ahorrar espacio, los programadores guardaban el año con **solo 2 dígitos** en vez de 4:

- 1998 → `98`
- 1999 → `99`
- 2000 → `00` ← 😱 ¿Es el año 2000 o el año 1900?

Nadie pensó en el problema... hasta que se acercó el 31 de diciembre de 1999.
**El mundo entró en pánico**:

- 🏦 **Bancos**: ¿Tu crédito de 1999 a 2000 aparecería como un crédito de -99 años?
- ✈️ **Aviones**: ¿Los sistemas de vuelo confundirían el 2000 con 1900 y dejarían de funcionar?
- 🏥 **Hospitales**: ¿Los equipos médicos se reiniciarían a medianoche?
- 💡 **Centrales eléctricas**: ¿Se apagaría la luz en año nuevo?

Se gastaron **más de 300 mil millones de dólares** a nivel mundial para revisar y corregir todos los sistemas antes de la medianoche.

Al final no pasó nada catastrófico... **justamente porque se invirtió en arreglarlo a tiempo**.

> **Moraleja para hoy**: Elegir el tipo de dato correcto **desde el principio** puede evitar desastres.
> Un simple `INTEGER` de 2 dígitos en vez de 4 casi destruyó la economía mundial.
> Imagina lo que puede pasar si guardas un precio como texto o una fecha como un número suelto.

---

### Los tipos de datos en PostgreSQL

Los tipos de datos se organizan en **6 familias**:

---

### 🔢 Familia 1: Numéricos

Para guardar números: edades, precios, cantidades, etc.

| Tipo                | ¿Qué guarda?          | Rango / Ejemplo                   | Uso típico                     |
| ------------------- | --------------------- | --------------------------------- | ------------------------------ |
| `INTEGER` (o `INT`) | Números enteros       | -2 mil millones a +2 mil millones | Edades, cantidades, stock      |
| `SMALLINT`          | Enteros pequeños      | -32,768 a 32,767                  | Calificaciones, códigos cortos |
| `BIGINT`            | Enteros enormes       | Hasta 9 trillones                 | IDs en sistemas gigantes       |
| `NUMERIC(p,s)`      | Decimales exactos     | `NUMERIC(10,2)` → 12345678.99     | Precios, dinero                |
| `DECIMAL(p,s)`      | Igual que NUMERIC     | Sinónimo                          | Precios, dinero                |
| `FLOAT`             | Decimales aproximados | Con errores de redondeo           | Cálculos científicos           |

> **Para dinero** → siempre usar `NUMERIC` o `DECIMAL` (exactos).
> **Nunca `FLOAT` para dinero** → `0.1 + 0.2 = 0.30000000000000004` 😱

#### ¿Qué significa `NUMERIC(10,2)`?

```
NUMERIC(10, 2)
         │   │
         │   └── 2 dígitos DESPUÉS del punto decimal
         └────── 10 dígitos EN TOTAL (incluyendo los decimales)

Ejemplos válidos:  12345678.99  ✅ (10 dígitos total, 2 decimales)
                   99.50        ✅
Ejemplo inválido:  123456789.99 ❌ (11 dígitos total, máximo es 10)
```

---

### 📝 Familia 2: Texto (Caracteres)

Para guardar palabras, nombres, descripciones, emails, etc.

| Tipo         | ¿Qué guarda?                | Comportamiento                                      | Uso típico                        |
| ------------ | --------------------------- | --------------------------------------------------- | --------------------------------- |
| `CHAR(n)`    | Texto de largo **fijo**     | Siempre ocupa `n` caracteres (rellena con espacios) | Códigos fijos: RUT, código país   |
| `VARCHAR(n)` | Texto de largo **variable** | Ocupa solo lo necesario, máximo `n`                 | Nombres, emails, direcciones      |
| `TEXT`       | Texto **ilimitado**         | Sin límite de largo                                 | Descripciones largas, comentarios |

#### La diferencia entre CHAR y VARCHAR (con ejemplo)

```
CHAR(10):     'Hola      '  ← Siempre ocupa 10 caracteres (rellena con espacios)
VARCHAR(10):  'Hola'         ← Ocupa solo 4 caracteres (lo justo)
```

> **¿Cuándo usar CHAR?** Cuando TODOS los valores tienen el mismo largo:
>
> - RUT: `'12.345.678-9'` → siempre 12 caracteres
> - Código país: `'CL'`, `'AR'`, `'US'` → siempre 2 caracteres
>
> **¿Cuándo usar VARCHAR?** Para casi todo lo demás:
>
> - Nombres: `'Ana'` (3 caracteres) vs `'María Fernanda'` (14 caracteres)

---

### 📅 Familia 3: Fecha y Hora

Para guardar fechas, horas o ambas.

| Tipo        | ¿Qué guarda?  | Formato             | Ejemplo                 |
| ----------- | ------------- | ------------------- | ----------------------- |
| `DATE`      | Solo la fecha | AAAA-MM-DD          | `'2025-03-15'`          |
| `TIME`      | Solo la hora  | HH:MM:SS            | `'14:30:00'`            |
| `TIMESTAMP` | Fecha + hora  | AAAA-MM-DD HH:MM:SS | `'2025-03-15 14:30:00'` |

> `TIMESTAMP` es el más usado porque guarda **cuándo** pasó algo con exactitud.
> Perfecto para: fecha de registro, fecha de compra, logs de actividad.

#### El truco de `DEFAULT NOW()`

En PostgreSQL, podemos hacer que una columna de fecha se llene **automáticamente** con la fecha y hora actual:

```sql
CREATE TABLE clientes (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(80) NOT NULL,
  fecha_registro  TIMESTAMP DEFAULT NOW()  -- ← se llena sola
);

INSERT INTO clientes (nombre) VALUES ('María');
-- fecha_registro = '2025-02-17 18:35:00' ← automático
```

---

### ✅ Familia 4: Booleanos

Para guardar **verdadero o falso**. Solo dos opciones.

| Tipo      | Valores posibles | Uso típico                      |
| --------- | ---------------- | ------------------------------- |
| `BOOLEAN` | `TRUE` / `FALSE` | ¿Está activo? ¿Pagó? ¿Es admin? |

```sql
CREATE TABLE productos (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80),
  activo  BOOLEAN DEFAULT TRUE  -- Por defecto está activo
);
```

> Es como un **interruptor de luz**: encendido o apagado. No hay un "medio encendido".

---

### 🔑 Familia 5: Valores Únicos Autogenerados

Para crear **IDs automáticos** que nunca se repiten.

| Tipo             | ¿Qué hace?                                       | Motor      |
| ---------------- | ------------------------------------------------ | ---------- |
| `SERIAL`         | Genera enteros autoincrementales (1, 2, 3, 4...) | PostgreSQL |
| `BIGSERIAL`      | Igual pero para números enormes                  | PostgreSQL |
| `AUTO_INCREMENT` | Equivalente de SERIAL                            | MySQL      |

```sql
CREATE TABLE clientes (
  id  SERIAL PRIMARY KEY,  -- 1, 2, 3, 4, 5, ...
  nombre VARCHAR(80)
);

INSERT INTO clientes (nombre) VALUES ('Ana');   -- id = 1 (automático)
INSERT INTO clientes (nombre) VALUES ('Pedro'); -- id = 2 (automático)
INSERT INTO clientes (nombre) VALUES ('Luis');  -- id = 3 (automático)
```

> **No necesitas escribir el id.** La base de datos lo genera sola.
> Es como el **numerito** que sacas en la carnicería: automático y nunca se repite.

---

### 🌐 Familia 6: Tipos Modernos

Las bases de datos modernas soportan tipos avanzados que van más allá de texto y números:

| Tipo             | ¿Qué guarda?                  | Ejemplo                                  | Uso típico                       |
| ---------------- | ----------------------------- | ---------------------------------------- | -------------------------------- |
| `UUID`           | Identificador único universal | `'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'` | IDs imposibles de adivinar       |
| `JSON` / `JSONB` | Datos estructurados flexibles | `'{"color": "rojo", "talla": "M"}'`      | Configuraciones, datos variables |

#### UUID — El ID moderno

`UUID` genera identificadores de **32 caracteres hexadecimales** separados por guiones.
Son **prácticamente irrepetibles** en todo el universo (la probabilidad de colisión es casi cero).

```sql
-- Habilitar la extensión UUID en PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE usuarios (
  id       UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  nombre   VARCHAR(80) NOT NULL,
  email    VARCHAR(120) UNIQUE NOT NULL
);

INSERT INTO usuarios (nombre, email) VALUES ('Ana', 'ana@mail.com');
-- id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11' ← automático y único en el mundo
```

**¿SERIAL o UUID? ¿Cuándo usar cada uno?**

|                 | `SERIAL` (1, 2, 3...)                         | `UUID`                                          |
| --------------- | --------------------------------------------- | ----------------------------------------------- |
| **Ventaja**     | Simple, legible, ocupa poco espacio           | Imposible de adivinar, funciona entre sistemas  |
| **Desventaja**  | Predecible (si el id es 5, el siguiente es 6) | Largo y difícil de leer                         |
| **Usar cuando** | Proyectos internos, tablas simples            | APIs públicas, sistemas distribuidos, seguridad |

> **¿Por qué importa que sea impredecible?**
> Si tu URL es `mitienda.com/usuario/5`, alguien puede probar `/usuario/6`, `/usuario/7`...
> Con UUID: `mitienda.com/usuario/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11` → imposible de adivinar.

#### JSON / JSONB — Datos flexibles dentro de SQL

A veces necesitas guardar datos que **no tienen una estructura fija** (no sabes de antemano cuántas columnas necesitas).

```sql
CREATE TABLE productos (
  id          SERIAL PRIMARY KEY,
  nombre      VARCHAR(100) NOT NULL,
  atributos   JSONB  -- ← datos flexibles
);

-- Un celular tiene atributos diferentes a una polera:
INSERT INTO productos (nombre, atributos) VALUES
  ('iPhone 15', '{"color": "negro", "ram": "8GB", "pantalla": "6.1"}'::jsonb),
  ('Polera Nike', '{"talla": "M", "color": "azul", "material": "algodón"}'::jsonb);
```

> `JSONB` es como tener una **columna elástica**: cada fila puede guardar datos diferentes.
> Muy usado en e-commerce, configuraciones de usuario y APIs.

---

### Tabla resumen: ¿Qué tipo uso?

| Necesito guardar...                | Tipo recomendado | Ejemplo de valor                       |
| ---------------------------------- | ---------------- | -------------------------------------- |
| Un ID automático (simple)          | `SERIAL`         | 1, 2, 3, ...                           |
| Un ID seguro/imposible de adivinar | `UUID`           | 'a0eebc99-9c0b-4ef8-bb6d-...'          |
| Un nombre o texto corto            | `VARCHAR(n)`     | 'María López'                          |
| Un texto muy largo                 | `TEXT`           | 'Descripción completa del producto...' |
| Un precio o monto de dinero        | `NUMERIC(10,2)`  | 29990.50                               |
| Una cantidad entera                | `INTEGER`        | 42                                     |
| Una fecha                          | `DATE`           | '2025-03-15'                           |
| Fecha y hora exacta                | `TIMESTAMP`      | '2025-03-15 14:30:00'                  |
| ¿Sí o no?                          | `BOOLEAN`        | TRUE / FALSE                           |
| Un código fijo (RUT, país)         | `CHAR(n)`        | 'CL'                                   |
| Datos variables/flexibles          | `JSONB`          | '{"color": "rojo"}'                    |

---

### El error más común: tipo equivocado

```sql
-- ❌ MAL: guardar precio como texto
CREATE TABLE productos (
  precio VARCHAR(20)  -- '990' se guarda como texto
);
-- Problema: no puedes hacer SUM(precio) ni precio * 1.10 😱

-- ✅ BIEN: guardar precio como numérico
CREATE TABLE productos (
  precio NUMERIC(10,2)  -- 990.00 se guarda como número
);
-- Ahora SÍ puedes calcular: SUM(precio), AVG(precio), precio * 1.10 ✅
```

> Si guardas un número como texto, **pierdes el poder de calcular**.
> La base de datos no sabe que `'990'` es un número — para ella es solo letras.

---

---

## 3️⃣ CREATE TABLE — Construir desde Cero

---

### La sintaxis básica

```sql
CREATE TABLE nombre_tabla (
  columna1  TIPO_DE_DATO  RESTRICCIONES,
  columna2  TIPO_DE_DATO  RESTRICCIONES,
  columna3  TIPO_DE_DATO  RESTRICCIONES
);
```

| Parte           | ¿Qué es?                       | Ejemplo                   |
| --------------- | ------------------------------ | ------------------------- |
| `nombre_tabla`  | El nombre de la tabla          | `empleados`               |
| `columna`       | El nombre de cada campo        | `nombre`, `edad`, `email` |
| `TIPO_DE_DATO`  | Qué tipo de información guarda | `VARCHAR(80)`, `INTEGER`  |
| `RESTRICCIONES` | Reglas que debe cumplir        | `NOT NULL`, `PRIMARY KEY` |

---

### Ejemplo completo paso a paso

Vamos a crear una tabla para guardar empleados:

```sql
CREATE TABLE empleados (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(100) NOT NULL,
  email           VARCHAR(120) UNIQUE NOT NULL,
  salario         NUMERIC(10,2) NOT NULL CHECK (salario > 0),
  fecha_ingreso   DATE DEFAULT CURRENT_DATE,
  activo          BOOLEAN DEFAULT TRUE
);
```

#### Leámoslo línea por línea:

| Línea                                                | ¿Qué hace?                                           |
| ---------------------------------------------------- | ---------------------------------------------------- |
| `id SERIAL PRIMARY KEY`                              | ID automático (1, 2, 3...), es la clave primaria     |
| `nombre VARCHAR(100) NOT NULL`                       | Nombre de hasta 100 caracteres, **obligatorio**      |
| `email VARCHAR(120) UNIQUE NOT NULL`                 | Email, obligatorio y **no puede repetirse**          |
| `salario NUMERIC(10,2) NOT NULL CHECK (salario > 0)` | Salario obligatorio, **debe ser positivo**           |
| `fecha_ingreso DATE DEFAULT CURRENT_DATE`            | Fecha: si no la doy, usa la **fecha de hoy**         |
| `activo BOOLEAN DEFAULT TRUE`                        | Booleano: si no lo doy, por defecto es **verdadero** |

---

### Las restricciones más importantes

| Restricción         | ¿Qué hace?                              | Ejemplo                       |
| ------------------- | --------------------------------------- | ----------------------------- |
| `PRIMARY KEY`       | Identifica cada fila de forma **única** | `id SERIAL PRIMARY KEY`       |
| `NOT NULL`          | El campo es **obligatorio**             | `nombre VARCHAR(80) NOT NULL` |
| `UNIQUE`            | El valor **no puede repetirse**         | `email VARCHAR(120) UNIQUE`   |
| `DEFAULT valor`     | Si no se da valor, usa este             | `activo BOOLEAN DEFAULT TRUE` |
| `CHECK (condición)` | Valida que se cumpla una regla          | `CHECK (precio > 0)`          |
| `FOREIGN KEY`       | Enlace a otra tabla                     | `REFERENCES clientes(id)`     |

---

### CREATE TABLE con Clave Foránea (FK)

Cuando una tabla necesita **apuntar a otra tabla**, usamos FOREIGN KEY:

```sql
-- PRIMERO: la tabla "padre" (categorias)
CREATE TABLE categorias (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(50) NOT NULL UNIQUE
);

-- DESPUÉS: la tabla "hija" (productos) que apunta al padre
CREATE TABLE productos (
  id            SERIAL PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  precio        NUMERIC(10,2) NOT NULL CHECK (precio > 0),
  id_categoria  INT,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);
```

> `FOREIGN KEY (id_categoria) REFERENCES categorias(id)` significa:
> _"El valor de id_categoria DEBE existir como id en la tabla categorias."_
> Si no existe → **ERROR**. Eso es la integridad referencial que vimos la clase pasada.

---

### ¿En qué ORDEN creo las tablas?

```
CREAR:    Padres primero → Hijos después
          (categorias → productos → pedidos)

ELIMINAR: Hijos primero → Padres después
          (pedidos → productos → categorias)
```

> Si intentas crear `productos` antes que `categorias`, te dará error
> porque la FK apunta a una tabla que todavía no existe.

---

---

## 4️⃣ Restricción de Nulidad — NOT NULL

---

### ¿Qué es NULL?

`NULL` en SQL no significa "cero" ni "texto vacío". Significa **"no hay dato"**, **"desconocido"**, **"ausente"**.

```
0       → Es un valor: el número cero
''      → Es un valor: un texto vacío
NULL    → NO es un valor: es la AUSENCIA de valor
```

> Piensa en un formulario:
>
> - Poner `0` en Teléfono → significa que tu teléfono es 0 (raro, pero es un dato).
> - Dejar el campo vacío → significa **no sé / no aplica**. Eso es NULL.

---

### NOT NULL — "Este campo es obligatorio"

Al agregar `NOT NULL` a una columna, estamos diciendo:
**"Esta columna SIEMPRE debe tener un valor. No acepto campos vacíos."**

```sql
CREATE TABLE empleados (
  id       SERIAL PRIMARY KEY,
  nombre   VARCHAR(100) NOT NULL,   -- ← Obligatorio
  telefono VARCHAR(20)              -- ← Opcional (permite NULL)
);
```

```sql
-- ✅ Esto funciona:
INSERT INTO empleados (nombre, telefono)
VALUES ('Ana López', '912345678');

-- ✅ Esto también (teléfono queda NULL):
INSERT INTO empleados (nombre)
VALUES ('Pedro Soto');

-- ❌ Esto FALLA (nombre es NOT NULL):
INSERT INTO empleados (telefono)
VALUES ('987654321');
-- ERROR: el campo "nombre" no puede ser NULL
```

---

### ¿Cuándo usar NOT NULL?

| Columna          | ¿NOT NULL?          | ¿Por qué?                                 |
| ---------------- | ------------------- | ----------------------------------------- |
| `nombre`         | ✅ Sí               | Un cliente sin nombre no tiene sentido    |
| `email`          | ✅ Sí               | Necesitamos contactarlos                  |
| `telefono`       | ❌ No               | No todos tienen teléfono                  |
| `precio`         | ✅ Sí               | Un producto siempre tiene precio          |
| `descripcion`    | ❌ No               | Es un dato complementario                 |
| `fecha_registro` | ✅ Sí (con DEFAULT) | Siempre queremos saber cuándo se registró |

> **Regla de oro**: Si una fila **no tiene sentido** sin ese dato → `NOT NULL`.

---

### DEFAULT + NOT NULL — La combinación perfecta

¿Qué pasa si un campo es obligatorio pero tiene un valor "obvio" por defecto?

```sql
CREATE TABLE productos (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(100) NOT NULL,
  stock   INT NOT NULL DEFAULT 0,         -- Obligatorio, pero empieza en 0
  activo  BOOLEAN NOT NULL DEFAULT TRUE   -- Obligatorio, pero empieza activo
);
```

```sql
-- No necesito dar stock ni activo → usan el DEFAULT
INSERT INTO productos (nombre) VALUES ('Coca-Cola');
-- stock = 0, activo = true → se llenan solos ✅
```

> `DEFAULT` no es lo mismo que `NULL`. Con DEFAULT, el campo **sí tiene un valor** (el valor por defecto).
> Con NULL, el campo **no tiene valor** (está vacío).

---

### ALTER TABLE — Modificar una tabla existente

¿Y si ya creé la tabla y necesito cambiar algo? Para eso existe `ALTER TABLE`:

```sql
-- Agregar una columna nueva
ALTER TABLE empleados ADD telefono VARCHAR(20);

-- Eliminar una columna
ALTER TABLE empleados DROP COLUMN telefono;

-- Cambiar el tipo de dato de una columna
ALTER TABLE empleados ALTER COLUMN nombre TYPE VARCHAR(150);

-- Agregar una restricción NOT NULL
ALTER TABLE empleados ALTER COLUMN email SET NOT NULL;

-- Quitar una restricción NOT NULL
ALTER TABLE empleados ALTER COLUMN email DROP NOT NULL;

-- Renombrar una columna
ALTER TABLE empleados RENAME COLUMN nombre TO nombre_completo;

-- Renombrar la tabla completa
ALTER TABLE empleados RENAME TO personal;
```

> `ALTER TABLE` es como **remodelar** el edificio: agregas una habitación, cambias una puerta, tiras una pared.
> Pero el edificio sigue siendo el mismo.

---

### DROP TABLE — Eliminar una tabla

```sql
-- Eliminar la tabla (da error si no existe)
DROP TABLE empleados;

-- Eliminar solo si existe (no da error si no existe)
DROP TABLE IF EXISTS empleados;
```

> `IF EXISTS` es una **buena práctica**: evita errores si la tabla ya fue eliminada.

---

### Resumen Teoría

| Concepto         | Lo más importante                                                      |
| ---------------- | ---------------------------------------------------------------------- |
| **DDL**          | Lenguaje para definir la **estructura** (CREATE, ALTER, DROP)          |
| **DML**          | Lenguaje para manipular los **datos** (INSERT, UPDATE, DELETE, SELECT) |
| **CREATE TABLE** | Crea una tabla con columnas, tipos y restricciones                     |
| **ALTER TABLE**  | Modifica una tabla existente (agregar/quitar columnas)                 |
| **DROP TABLE**   | Elimina la tabla completa (estructura + datos)                         |
| **SERIAL**       | ID autoincremental (1, 2, 3...)                                        |
| **VARCHAR(n)**   | Texto de largo variable, máximo `n` caracteres                         |
| **NUMERIC(p,s)** | Número decimal exacto (para dinero usar esto)                          |
| **TIMESTAMP**    | Fecha y hora exacta                                                    |
| **BOOLEAN**      | Verdadero o falso                                                      |
| **NOT NULL**     | Campo obligatorio (no acepta valores vacíos)                           |
| **DEFAULT**      | Valor automático si no se da uno                                       |
| **UNIQUE**       | No permite valores repetidos                                           |
| **CHECK**        | Valida una condición (ej: `precio > 0`)                                |
| **PRIMARY KEY**  | Identificador único de cada fila                                       |
| **FOREIGN KEY**  | Enlace a otra tabla (integridad referencial)                           |

---
