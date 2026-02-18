<!-- =========================================================
Archivo: actividad_streaming_respuestas.md
Tema: Respuestas — Plataforma de Streaming "ChileFlix"
Notas: Código con explicación línea a línea
========================================================= -->

# 🎬 ChileFlix — Respuestas del Mentor

---

---

---

# 🟢 NIVEL 1 — Respuestas DDL

---

## Requerimiento 1: Tabla `planes`

```sql
CREATE TABLE planes (
  id              SERIAL PRIMARY KEY,       -- ID autoincremental: 1, 2, 3...
  nombre          VARCHAR(30) NOT NULL       -- Nombre del plan, obligatorio
                  UNIQUE,                    -- No puede haber dos planes con el mismo nombre
  precio_mensual  NUMERIC(8,2) NOT NULL      -- Precio con 2 decimales, obligatorio
                  CHECK (precio_mensual > 0),-- Validación: no acepta precios de $0 o negativos
  max_pantallas   INT NOT NULL               -- Pantallas simultáneas, obligatorio
                  CHECK (max_pantallas > 0)  -- No tiene sentido un plan con 0 pantallas
);
```

**¿Por qué esta tabla va primero?**
Porque `usuarios` tendrá una FK que apunta a `planes`. Si `planes` no existe todavía, la FK fallaría.

---

## Requerimiento 2: Tabla `usuarios`

```sql
CREATE TABLE usuarios (
  id              SERIAL PRIMARY KEY,           -- ID automático
  nombre          VARCHAR(80) NOT NULL,          -- Nombre obligatorio
  email           VARCHAR(120) NOT NULL UNIQUE,  -- Email obligatorio y único (no pueden registrarse
                                                 -- dos cuentas con el mismo email)
  fecha_registro  TIMESTAMP DEFAULT NOW(),       -- Se llena automáticamente con la fecha/hora actual
  id_plan         INT NOT NULL,                  -- Referencia al plan contratado
  activo          BOOLEAN DEFAULT TRUE,          -- Por defecto la cuenta está activa
  saldo           NUMERIC(10,2) NOT NULL         -- Saldo de la billetera virtual
                  DEFAULT 0,                     -- Empieza en $0 si no se indica otro valor
  FOREIGN KEY (id_plan) REFERENCES planes(id)    -- FK: el id_plan DEBE existir en la tabla planes
);
```

**Líneas clave:**

- `DEFAULT NOW()` → cada vez que se inserta un usuario, `fecha_registro` se llena sola con el momento exacto.
- `DEFAULT TRUE` → cuando se crea una cuenta, por defecto está activa (no hay que escribir `activo = true`).
- `FOREIGN KEY` → si alguien intenta insertar un `id_plan = 99` y no existe un plan con `id = 99`, PostgreSQL **rechaza** la inserción.

---

## Requerimiento 3: Tabla `categorias`

```sql
CREATE TABLE categorias (
  id      SERIAL PRIMARY KEY,              -- ID automático
  nombre  VARCHAR(50) NOT NULL UNIQUE      -- Nombre único y obligatorio
);
```

---

## Requerimiento 4: Tabla `peliculas`

```sql
CREATE TABLE peliculas (
  id              SERIAL PRIMARY KEY,             -- ID automático
  titulo          VARCHAR(150) NOT NULL,           -- Título obligatorio
  anio_estreno    INT NOT NULL,                    -- Año como número entero
  duracion_min    INT NOT NULL                     -- Duración en minutos
                  CHECK (duracion_min > 0),        -- No puede durar 0 o negativo
  rating          NUMERIC(3,1)                     -- Nota de 0.0 a 10.0
                  CHECK (rating >= 0 AND rating <= 10), -- Validación de rango
  id_categoria    INT NOT NULL,                    -- FK a categorías
  FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);
```

**¿Por qué `NUMERIC(3,1)` para el rating?**

```
NUMERIC(3,1) = 3 dígitos total, 1 decimal
Válidos:   9.5 ✅    10.0 ✅    0.0 ✅
Inválido:  100.5 ❌  (4 dígitos total, máximo es 3)
```

---

## Requerimiento 5: Tabla `visualizaciones`

```sql
CREATE TABLE visualizaciones (
  id           SERIAL PRIMARY KEY,                     -- ID automático
  id_usuario   INT NOT NULL,                           -- ¿Quién vio?
  id_pelicula  INT NOT NULL,                           -- ¿Qué vio?
  fecha_vista  TIMESTAMP DEFAULT NOW(),                -- ¿Cuándo la vio?
  completada   BOOLEAN DEFAULT FALSE,                  -- ¿La terminó? (por defecto: no)
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id),    -- FK a usuarios
  FOREIGN KEY (id_pelicula) REFERENCES peliculas(id)   -- FK a películas
);
```

**Nota:** Esta tabla tiene **dos FK** (apunta a dos padres diferentes). Es una **tabla de relación** que conecta usuarios con películas.

---

## Requerimiento 6: Tabla `pagos`

```sql
CREATE TABLE pagos (
  id          SERIAL PRIMARY KEY,                -- ID automático
  id_usuario  INT NOT NULL,                      -- ¿Quién pagó?
  monto       NUMERIC(10,2) NOT NULL             -- ¿Cuánto pagó?
              CHECK (monto > 0),                 -- No se aceptan pagos de $0
  fecha_pago  TIMESTAMP DEFAULT NOW(),           -- ¿Cuándo pagó? (automático)
  metodo      VARCHAR(30) NOT NULL               -- ¿Cómo pagó?
              DEFAULT 'tarjeta',                 -- Si no se dice, asume tarjeta
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
```

---

## Requerimiento 7: Cargar datos

```sql
-- ─────────────────────────────────────
-- PASO 1: Planes (no depende de nadie)
-- ─────────────────────────────────────
INSERT INTO planes (nombre, precio_mensual, max_pantallas) VALUES
  ('Básico',     4990,  1),
  ('Estándar',   7990,  2),
  ('Premium',    11990, 4),
  ('Estudiante', 2990,  1);

-- ─────────────────────────────────────
-- PASO 2: Categorías (no depende de nadie)
-- ─────────────────────────────────────
INSERT INTO categorias (nombre) VALUES
  ('Acción'),
  ('Comedia'),
  ('Drama'),
  ('Terror'),
  ('Ciencia Ficción'),
  ('Documental'),
  ('Animación');

-- ─────────────────────────────────────
-- PASO 3: Usuarios (depende de planes)
-- Nota: id_plan debe coincidir con los IDs generados en planes
-- Premium = 3, Estándar = 2, Básico = 1, Estudiante = 4
-- ─────────────────────────────────────
INSERT INTO usuarios (nombre, email, id_plan, saldo) VALUES
  ('Valentina Rojas',  'vale@mail.com',   3, 50000),  -- Premium
  ('Matías Torres',    'matias@mail.com', 2, 25000),  -- Estándar
  ('Camila Fuentes',   'cami@mail.com',   1, 10000),  -- Básico
  ('Sebastián Díaz',   'seba@mail.com',   4, 5000),   -- Estudiante
  ('Isidora Muñoz',    'isi@mail.com',    3, 80000),  -- Premium
  ('Tomás Herrera',    'tomas@mail.com',  2, 15000),  -- Estándar
  ('Francisca López',  'fran@mail.com',   1, 3000),   -- Básico
  ('Joaquín Araya',    'joaco@mail.com',  4, 1000);   -- Estudiante

-- ─────────────────────────────────────
-- PASO 4: Películas (depende de categorias)
-- Acción=1, Comedia=2, Drama=3, Terror=4, CiFi=5, Docu=6, Animación=7
-- ─────────────────────────────────────
INSERT INTO peliculas (titulo, anio_estreno, duracion_min, rating, id_categoria) VALUES
  ('El Agente Invisible',   2024, 128, 7.5, 1),  -- Acción
  ('Misión Extrema',        2023, 135, 8.2, 1),  -- Acción
  ('Risa Loca',             2024,  95, 6.8, 2),  -- Comedia
  ('Noche de Comedia',      2022, 102, 7.1, 2),  -- Comedia
  ('El Último Adiós',       2023, 142, 9.0, 3),  -- Drama
  ('Camino al Oscar',       2024, 118, 8.7, 3),  -- Drama
  ('La Casa Oscura',        2023,  98, 6.5, 4),  -- Terror
  ('Gritos en la Niebla',   2024,  91, 5.8, 4),  -- Terror
  ('Galaxia Perdida',       2024, 155, 8.9, 5),  -- Ciencia Ficción
  ('Planeta Cero',          2022, 130, 7.3, 5),  -- Ciencia Ficción
  ('Océanos Secretos',      2023,  85, 8.4, 6),  -- Documental
  ('Mi Vecino Totoro 2',    2024, 110, 9.2, 7);  -- Animación

-- ─────────────────────────────────────
-- PASO 5: Visualizaciones (depende de usuarios Y películas)
-- ─────────────────────────────────────
INSERT INTO visualizaciones (id_usuario, id_pelicula, completada) VALUES
  (1, 1, true),   -- Valentina vio El Agente Invisible (completa)
  (1, 5, true),   -- Valentina vio El Último Adiós (completa)
  (1, 9, true),   -- Valentina vio Galaxia Perdida (completa)
  (1, 12, false),  -- Valentina empezó Mi Vecino Totoro 2 (no terminó)
  (2, 2, true),   -- Matías vio Misión Extrema (completa)
  (2, 6, true),   -- Matías vio Camino al Oscar (completa)
  (2, 11, false),  -- Matías empezó Océanos Secretos (no terminó)
  (3, 3, true),   -- Camila vio Risa Loca (completa)
  (3, 4, true),   -- Camila vio Noche de Comedia (completa)
  (4, 7, false),  -- Sebastián empezó La Casa Oscura (no terminó)
  (5, 1, true),   -- Isidora vio El Agente Invisible (completa)
  (5, 5, true),   -- Isidora vio El Último Adiós (completa)
  (5, 9, true),   -- Isidora vio Galaxia Perdida (completa)
  (5, 12, true),   -- Isidora vio Mi Vecino Totoro 2 (completa)
  (5, 6, true),   -- Isidora vio Camino al Oscar (completa)
  (6, 10, true),  -- Tomás vio Planeta Cero (completa)
  (6, 8, false);  -- Tomás empezó Gritos en la Niebla (no terminó)
  -- Nota: Francisca (7) y Joaquín (8) no tienen visualizaciones

-- ─────────────────────────────────────
-- PASO 6: Pagos (depende de usuarios)
-- ─────────────────────────────────────
INSERT INTO pagos (id_usuario, monto, metodo) VALUES
  (1, 11990, 'tarjeta'),       -- Valentina pagó Premium
  (2, 7990,  'transferencia'), -- Matías pagó Estándar
  (3, 4990,  'débito'),        -- Camila pagó Básico
  (4, 2990,  'tarjeta'),       -- Sebastián pagó Estudiante
  (5, 11990, 'tarjeta'),       -- Isidora pagó Premium
  (5, 11990, 'tarjeta'),       -- Isidora pagó Premium (segundo mes)
  (6, 7990,  'transferencia'), -- Tomás pagó Estándar
  (1, 11990, 'tarjeta'),       -- Valentina pagó Premium (segundo mes)
  (2, 7990,  'débito'),        -- Matías pagó Estándar (segundo mes)
  (3, 4990,  'tarjeta');       -- Camila pagó Básico (segundo mes)
```

---

---

---

# 🟡 NIVEL 2 — Respuestas Transacciones

---

### ¿Cómo funciona una transacción? — Explicación conceptual

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   BEGIN;                 ← Abre una "burbuja protectora"    │
│   │                                                         │
│   ├── operación 1        ← Se ejecuta TEMPORALMENTE         │
│   ├── operación 2        ← Se ejecuta TEMPORALMENTE         │
│   ├── operación 3        ← Se ejecuta TEMPORALMENTE         │
│   │                                                         │
│   ├── COMMIT;            ← ✅ Todo sale bien → se GRABA     │
│   │   (las 3 ops se confirman de forma permanente)          │
│   │                                                         │
│   └── ROLLBACK;          ← ❌ Algo salió mal → se DESHACE   │
│       (las 3 ops se BORRAN como si nunca hubieran pasado)   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Reglas clave:**

1. Después de `BEGIN`, **nada es definitivo** → todo es temporal.
2. `COMMIT` = **confirmar** → los cambios se graban para siempre.
3. `ROLLBACK` = **deshacer** → la base de datos viaja en el tiempo al estado antes del `BEGIN`.
4. Si la conexión se cae entre BEGIN y COMMIT → se hace **ROLLBACK automático** (protección).

---

## Requerimiento 8: Cobro mensual exitoso

```sql
-- ═══════════════════════════════════════════════
-- COBRO MENSUAL A VALENTINA ROJAS
-- Saldo actual: $50,000 | Plan Premium: $11,990
-- Resultado esperado: saldo final = $38,010
-- ═══════════════════════════════════════════════

BEGIN;
-- A partir de aquí, NADA se graba de forma definitiva.
-- Todo queda en una "zona de prueba" temporal.

-- PASO 1: Ver el saldo actual y el precio del plan
-- (Esto es para verificar ANTES de hacer cambios)
SELECT
  u.nombre,
  u.saldo,
  p.nombre AS plan,
  p.precio_mensual
FROM usuarios u
JOIN planes p ON u.id_plan = p.id
WHERE u.email = 'vale@mail.com';
-- Resultado: Valentina | 50000 | Premium | 11990

-- PASO 2: Descontar el precio del plan del saldo
UPDATE usuarios
SET saldo = saldo - (
    SELECT precio_mensual       -- Subconsulta: busca el precio de su plan
    FROM planes
    WHERE id = (
        SELECT id_plan          -- Subconsulta anidada: busca qué plan tiene
        FROM usuarios
        WHERE email = 'vale@mail.com'
    )
)
WHERE email = 'vale@mail.com';
-- Valentina ahora tiene $50,000 - $11,990 = $38,010 (TEMPORAL)

-- PASO 3: Registrar el pago
INSERT INTO pagos (id_usuario, monto, metodo)
VALUES (
  (SELECT id FROM usuarios WHERE email = 'vale@mail.com'),  -- Busca su ID
  (SELECT precio_mensual FROM planes                        -- Busca el monto
   WHERE id = (SELECT id_plan FROM usuarios WHERE email = 'vale@mail.com')),
  'tarjeta'
);

-- PASO 4: Verificar que todo quedó bien ANTES de confirmar
SELECT
  u.nombre,
  u.saldo,
  p.nombre AS plan
FROM usuarios u
JOIN planes p ON u.id_plan = p.id
WHERE u.email = 'vale@mail.com';
-- Si el saldo es $38,010 → todo correcto

COMMIT;
-- ✅ AHORA SÍ se graba todo de forma permanente:
--    - El saldo se descontó
--    - El pago se registró
-- Si algo hubiera fallado, habríamos hecho ROLLBACK en vez de COMMIT.
```

---

## Requerimiento 9: Cobro fallido con ROLLBACK

```sql
-- ═══════════════════════════════════════════════
-- COBRO FALLIDO A JOAQUÍN ARAYA
-- Saldo actual: $1,000 | Plan Estudiante: $2,990
-- Resultado esperado: NO se cobra, saldo queda en $1,000
-- ═══════════════════════════════════════════════

-- ANTES DE EMPEZAR: verificar estado actual
SELECT nombre, saldo FROM usuarios WHERE email = 'joaco@mail.com';
-- Resultado: Joaquín Araya | 1000.00
-- Claramente $1,000 < $2,990 → NO ALCANZA para pagar

BEGIN;
-- Abrimos la burbuja protectora de la transacción.
-- Todo lo que hagamos aquí adentro es TEMPORAL.

-- PASO 1: Intentar descontar el plan (aunque sabemos que no alcanza)
UPDATE usuarios
SET saldo = saldo - 2990
WHERE email = 'joaco@mail.com';
-- El UPDATE se ejecutó TEMPORALMENTE.
-- PostgreSQL NO lo rechaza porque no hay CHECK (saldo >= 0) todavía.
-- Joaquín ahora tiene: $1,000 - $2,990 = -$1,990 (TEMPORAL)

-- PASO 2: Verificar el resultado
SELECT nombre, saldo FROM usuarios WHERE email = 'joaco@mail.com';
-- Resultado: Joaquín Araya | -1990.00  ← 😱 ¡SALDO NEGATIVO!

-- PASO 3: Detectamos el problema → DESHACEMOS TODO
ROLLBACK;
-- ❌ ROLLBACK deshace TODOS los cambios desde el BEGIN.
-- Es como si el UPDATE nunca hubiera existido.
-- La base de datos "viaja en el tiempo" al estado exacto de antes del BEGIN.

-- VERIFICACIÓN FINAL: ¿Se deshizo realmente?
SELECT nombre, saldo FROM usuarios WHERE email = 'joaco@mail.com';
-- Resultado: Joaquín Araya | 1000.00  ← ✅ ¡Volvió a $1,000!
-- El ROLLBACK funcionó: el dinero nunca se descontó de verdad.
```

**¿Qué habría pasado SIN transacción?**

```sql
-- Sin BEGIN/ROLLBACK, el UPDATE se ejecuta DE FORMA PERMANENTE:
UPDATE usuarios SET saldo = saldo - 2990 WHERE email = 'joaco@mail.com';
-- saldo = -1990 → ¡GRABADO! No hay vuelta atrás 😱
-- Por eso las transacciones son tan importantes en operaciones de dinero.
```

**Respuesta a la pregunta del ejercicio:**

```sql
-- Para evitar este problema automáticamente,
-- agregar un CHECK a la columna saldo:
ALTER TABLE usuarios ADD CONSTRAINT chk_saldo_positivo CHECK (saldo >= 0);
-- Ahora PostgreSQL RECHAZA cualquier UPDATE que deje el saldo negativo,
-- sin necesidad de que el programador lo verifique manualmente.
```

---

## Requerimiento 10: Cambio de plan (upgrade)

```sql
-- ═══════════════════════════════════════════════
-- UPGRADE: MATÍAS DE ESTÁNDAR ($7,990) A PREMIUM ($11,990)
-- Diferencia a cobrar: $4,000
-- Saldo actual: $25,000 → Saldo final esperado: $21,000
-- ═══════════════════════════════════════════════

BEGIN;

-- PASO 1: Ver estado actual
SELECT
  u.nombre, u.saldo,
  p.nombre AS plan_actual, p.precio_mensual
FROM usuarios u
JOIN planes p ON u.id_plan = p.id
WHERE u.email = 'matias@mail.com';
-- Matías | 25000 | Estándar | 7990

-- PASO 2: Actualizar su plan a Premium
UPDATE usuarios
SET id_plan = (SELECT id FROM planes WHERE nombre = 'Premium')  -- Busca el ID del plan Premium
WHERE email = 'matias@mail.com';

-- PASO 3: Cobrar la diferencia de precio
-- Premium ($11,990) - Estándar ($7,990) = $4,000
UPDATE usuarios
SET saldo = saldo - 4000
WHERE email = 'matias@mail.com';
-- saldo: $25,000 - $4,000 = $21,000 (TEMPORAL)

-- PASO 4: Registrar el pago del upgrade
INSERT INTO pagos (id_usuario, monto, metodo)
VALUES (
  (SELECT id FROM usuarios WHERE email = 'matias@mail.com'),
  4000,
  'upgrade'
);

-- PASO 5: Verificar que todo esté correcto
SELECT
  u.nombre, u.saldo,
  p.nombre AS plan_nuevo, p.precio_mensual
FROM usuarios u
JOIN planes p ON u.id_plan = p.id
WHERE u.email = 'matias@mail.com';
-- Matías | 21000 | Premium | 11990 ← ✅ Correcto

COMMIT;
-- ✅ Se grabó: cambio de plan + descuento de saldo + registro de pago.
-- Si cualquiera de los 3 pasos hubiera fallado,
-- habríamos hecho ROLLBACK y Matías seguiría en Estándar con $25,000.
```

---

## Requerimiento 11: Cancelación de cuenta

```sql
-- ═══════════════════════════════════════════════
-- CANCELACIÓN: FRANCISCA LÓPEZ
-- ═══════════════════════════════════════════════

BEGIN;

-- PASO 1: Desactivar la cuenta
UPDATE usuarios
SET activo = FALSE
WHERE email = 'fran@mail.com';

-- PASO 2: Registrar la cancelación en pagos (para auditoría)
INSERT INTO pagos (id_usuario, monto, metodo)
VALUES (
  (SELECT id FROM usuarios WHERE email = 'fran@mail.com'),
  0.01,              -- Monto simbólico (CHECK exige > 0)
  'cancelacion'      -- Método especial para identificar cancelaciones
);

-- PASO 3: Verificar
SELECT nombre, activo, saldo
FROM usuarios
WHERE email = 'fran@mail.com';
-- Francisca López | false | 3000 ← Cuenta inactiva, saldo intacto

COMMIT;
```

---

---

---

# 🔴 NIVEL 3 — Respuestas Consultas Avanzadas

---

## Requerimiento 12: Películas más vistas que el promedio

```sql
-- Objetivo: encontrar películas con MÁS visualizaciones que el promedio general

SELECT
  p.titulo,                                     -- Nombre de la película
  COUNT(v.id) AS total_vistas                   -- Cuántas veces fue vista
FROM peliculas p
JOIN visualizaciones v ON v.id_pelicula = p.id  -- Une películas con sus visualizaciones
GROUP BY p.id, p.titulo                          -- Agrupa por película
HAVING COUNT(v.id) > (                          -- Filtra: solo las que superan el promedio
    SELECT AVG(conteo)                          -- Subconsulta: calcula el promedio
    FROM (
        SELECT COUNT(*) AS conteo               -- Cuenta visualizaciones por película
        FROM visualizaciones
        GROUP BY id_pelicula
    ) AS sub                                    -- Alias obligatorio para subconsultas en FROM
)
ORDER BY total_vistas DESC;
```

**¿Cómo funciona la subconsulta?**

```
1. La subconsulta más interna cuenta las vistas de CADA película:
   El Agente Invisible: 2, Galaxia Perdida: 2, El Último Adiós: 2, etc.

2. La subconsulta intermedia calcula el PROMEDIO de esos conteos:
   Promedio = (2+2+2+2+2+1+1+1+1+1+1+1) / 12 ≈ 1.4

3. HAVING filtra: solo muestra películas con MÁS de 1.4 vistas
   → Las que tienen 2+ vistas pasan el filtro
```

---

## Requerimiento 13: Usuarios que nunca vieron nada

```sql
-- Opción A: con NOT IN
SELECT nombre, email
FROM usuarios
WHERE id NOT IN (                               -- "Dame los que NO están en esta lista"
    SELECT DISTINCT id_usuario                  -- Lista de todos los que ALGUNA VEZ vieron algo
    FROM visualizaciones
);

-- Opción B: con NOT EXISTS (más eficiente en tablas grandes)
SELECT u.nombre, u.email
FROM usuarios u
WHERE NOT EXISTS (                              -- "Dame los que NO tienen registros aquí"
    SELECT 1                                    -- No importa qué seleccionamos, solo si EXISTE
    FROM visualizaciones v
    WHERE v.id_usuario = u.id                   -- ¿Hay alguna visualización de ESTE usuario?
);
-- Resultado: Francisca López, Joaquín Araya
```

**Diferencia entre NOT IN y NOT EXISTS:**

- `NOT IN`: crea una lista completa y luego verifica si el ID está ahí. Puede ser lento con millones de registros.
- `NOT EXISTS`: verifica uno por uno sin crear una lista completa. Más eficiente en tablas grandes.
- Ambos dan el **mismo resultado**, la diferencia es de **rendimiento**.

---

## Requerimiento 14: Categoría más popular

```sql
WITH vistas_por_categoria AS (
    -- CTE: tabla temporal que calcula vistas por categoría
    SELECT
        c.nombre AS categoria,                          -- Nombre de la categoría
        COUNT(v.id) AS total_vistas                     -- Total de visualizaciones
    FROM categorias c
    JOIN peliculas p ON p.id_categoria = c.id           -- Categoría → Película
    JOIN visualizaciones v ON v.id_pelicula = p.id      -- Película → Visualización
    GROUP BY c.nombre                                    -- Agrupar por categoría
)
SELECT
    categoria,
    total_vistas
FROM vistas_por_categoria
ORDER BY total_vistas DESC;                              -- De más popular a menos popular
```

**¿Qué es un CTE (`WITH`)?**

```
WITH nombre_temporal AS (
    -- cualquier consulta SELECT
)
-- Ahora puedo usar "nombre_temporal" como si fuera una tabla

Es como crear una TABLA TEMPORAL que solo existe
durante esta consulta. Se destruye al terminar.

Ventaja: hace el código más LEGIBLE y ORGANIZADO.
En vez de una sola consulta gigante con subconsultas anidadas,
lo divides en bloques con nombre.
```

---

## Requerimiento 15: Ingresos por plan

```sql
WITH ingresos_plan AS (
    SELECT
        pl.nombre AS plan,                              -- Nombre del plan
        COUNT(DISTINCT u.id) AS total_usuarios,         -- Usuarios únicos en ese plan
        COALESCE(SUM(pa.monto), 0) AS total_ingresos    -- Suma de todos los pagos
                                                        -- COALESCE: si no hay pagos, mostrar 0
    FROM planes pl
    LEFT JOIN usuarios u ON u.id_plan = pl.id           -- LEFT JOIN: incluir planes sin usuarios
    LEFT JOIN pagos pa ON pa.id_usuario = u.id          -- LEFT JOIN: incluir usuarios sin pagos
    GROUP BY pl.nombre
)
SELECT
    plan,
    total_usuarios,
    total_ingresos,
    CASE
        WHEN total_usuarios > 0                         -- Evitar división por cero
        THEN ROUND(total_ingresos / total_usuarios, 0)
        ELSE 0
    END AS ingreso_promedio_por_usuario
FROM ingresos_plan
ORDER BY total_ingresos DESC;
```

**Funciones usadas:**

- `COALESCE(valor, alternativa)` → si `valor` es NULL, usa la `alternativa`. Aquí: si no hay pagos, muestra 0 en vez de NULL.
- `ROUND(número, decimales)` → redondea. `ROUND(12345.6789, 0)` → `12346`.
- `CASE WHEN ... THEN ... ELSE ... END` → condicional: "si hay usuarios, divide; si no, pon 0".

---

## Requerimiento 16: Top 3 por categoría (Window Function)

```sql
WITH ranking AS (
    SELECT
        c.nombre AS categoria,
        p.titulo,
        p.rating,
        ROW_NUMBER() OVER (                     -- Función de ventana: numera las filas
            PARTITION BY c.nombre               -- ← Reinicia la numeración POR CADA categoría
            ORDER BY p.rating DESC              -- ← Ordena de mayor a menor rating
        ) AS posicion                           -- La de mejor rating = posición 1
    FROM peliculas p
    JOIN categorias c ON p.id_categoria = c.id
)
SELECT categoria, titulo, rating, posicion
FROM ranking
WHERE posicion <= 3                             -- Solo las top 3 de cada categoría
ORDER BY categoria, posicion;
```

**¿Cómo funciona ROW_NUMBER() OVER (PARTITION BY ...)?**

```
Sin PARTITION BY → numera TODAS las filas del 1 al N
ROW_NUMBER() OVER (ORDER BY rating DESC)
  → 1. Totoro (9.2)
  → 2. El Último Adiós (9.0)
  → 3. Galaxia Perdida (8.9)
  → 4. ... etc

Con PARTITION BY categoría → REINICIA la numeración por cada categoría
ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY rating DESC)

  Acción:    1. Misión Extrema (8.2)     2. El Agente Invisible (7.5)
  Comedia:   1. Noche de Comedia (7.1)   2. Risa Loca (6.8)
  Drama:     1. El Último Adiós (9.0)    2. Camino al Oscar (8.7)
  Terror:    1. La Casa Oscura (6.5)     2. Gritos en la Niebla (5.8)
```

**Diferencia entre ROW_NUMBER y RANK:**

```
Ratings: 9.0, 9.0, 8.7

ROW_NUMBER: 1, 2, 3    (siempre números únicos, aunque empaten)
RANK:       1, 1, 3    (empate → mismo número, salta al siguiente)
DENSE_RANK: 1, 1, 2    (empate → mismo número, NO salta)
```

---

## Requerimiento 17: Ranking de usuarios activos

```sql
WITH actividad AS (
    SELECT
        u.nombre,
        pl.nombre AS plan,
        COUNT(v.id) AS total_vistas,                           -- Películas vistas (total)
        COUNT(v.id) FILTER (WHERE v.completada = true)         -- Solo las completadas
            AS completadas,
        CASE
            WHEN COUNT(v.id) > 0                               -- Evitar dividir por 0
            THEN ROUND(
                COUNT(v.id) FILTER (WHERE v.completada = true) -- completadas
                * 100.0                                        -- × 100 para porcentaje
                / COUNT(v.id),                                 -- ÷ total
                1                                              -- 1 decimal
            )
            ELSE 0
        END AS pct_completitud                                 -- Porcentaje de completitud
    FROM usuarios u
    JOIN planes pl ON u.id_plan = pl.id
    LEFT JOIN visualizaciones v ON v.id_usuario = u.id         -- LEFT JOIN: incluir los que no vieron nada
    WHERE u.activo = true                                      -- Solo usuarios activos
    GROUP BY u.id, u.nombre, pl.nombre
)
SELECT
    RANK() OVER (ORDER BY total_vistas DESC) AS posicion,      -- Ranking por vistas
    nombre,
    plan,
    total_vistas,
    completadas,
    pct_completitud || '%' AS completitud                      -- Concatena el símbolo %
FROM actividad
ORDER BY posicion;
```

**`FILTER (WHERE ...)` es una joya de PostgreSQL:**

```sql
-- En vez de esto (funciona pero es largo):
SUM(CASE WHEN completada = true THEN 1 ELSE 0 END)

-- Puedes escribir esto (más limpio):
COUNT(*) FILTER (WHERE completada = true)

-- FILTER aplica una condición SOLO a esa función de agregación
-- sin afectar al COUNT general.
```

---

## Requerimiento 18: Retención — Pagó pero no ve nada

```sql
WITH ultima_vista AS (
    -- CTE 1: Fecha de la última visualización de cada usuario
    SELECT
        id_usuario,
        MAX(fecha_vista) AS ultima_fecha        -- La más reciente
    FROM visualizaciones
    GROUP BY id_usuario
)
SELECT
    u.nombre,
    u.email,
    uv.ultima_fecha AS ultima_visualizacion,
    NOW() - uv.ultima_fecha AS dias_sin_ver     -- Resta de fechas = intervalo de tiempo
FROM usuarios u
JOIN pagos p ON p.id_usuario = u.id             -- Solo los que HAN PAGADO
LEFT JOIN ultima_vista uv ON uv.id_usuario = u.id
WHERE u.activo = true
  AND (
    uv.ultima_fecha IS NULL                     -- Nunca vio nada
    OR uv.ultima_fecha < NOW() - INTERVAL '30 days'  -- No vio nada en 30 días
  )
GROUP BY u.id, u.nombre, u.email, uv.ultima_fecha;
```

**`INTERVAL '30 days'` en PostgreSQL:**

```sql
NOW() - INTERVAL '30 days'   -- Resta 30 días a la fecha actual
-- Si hoy es 2025-02-17, el resultado es 2025-01-18

-- Otros ejemplos:
INTERVAL '1 hour'       -- 1 hora
INTERVAL '6 months'     -- 6 meses
INTERVAL '1 year'       -- 1 año
```

---

## Requerimiento 19: Segmentación con CASE

```sql
WITH actividad AS (
    SELECT
        u.nombre,
        u.email,
        pl.nombre AS plan,
        COUNT(v.id) AS total_vistas
    FROM usuarios u
    JOIN planes pl ON u.id_plan = pl.id
    LEFT JOIN visualizaciones v ON v.id_usuario = u.id
    WHERE u.activo = true
    GROUP BY u.id, u.nombre, u.email, pl.nombre
)
SELECT
    nombre,
    plan,
    total_vistas,
    CASE                                                -- CASE funciona como IF/ELSE
        WHEN total_vistas = 0 THEN '🔴 Inactivo'       -- 0 vistas
        WHEN total_vistas BETWEEN 1 AND 3 THEN '🟡 Casual'   -- 1 a 3
        WHEN total_vistas BETWEEN 4 AND 7 THEN '🟢 Activo'   -- 4 a 7
        ELSE '🔵 Superfan'                               -- 8 o más
    END AS segmento                                      -- Nombre de la columna resultante
FROM actividad
ORDER BY total_vistas DESC;
```

---

## Requerimiento 20: Dashboard del CEO

```sql
WITH
-- ─────────────────────────────────────
-- CTE 1: Métricas generales
-- ─────────────────────────────────────
metricas AS (
    SELECT
        (SELECT COUNT(*) FROM usuarios WHERE activo = true)
            AS usuarios_activos,
        (SELECT COALESCE(SUM(monto), 0) FROM pagos)
            AS ingresos_totales,
        (SELECT ROUND(AVG(vistas), 1) FROM (
            SELECT COUNT(*) AS vistas FROM visualizaciones GROUP BY id_usuario
        ) sub)
            AS promedio_peliculas_por_usuario
),

-- ─────────────────────────────────────
-- CTE 2: Película más vista
-- ─────────────────────────────────────
pelicula_top AS (
    SELECT
        p.titulo,
        COUNT(v.id) AS vistas
    FROM peliculas p
    JOIN visualizaciones v ON v.id_pelicula = p.id
    GROUP BY p.id, p.titulo
    ORDER BY vistas DESC
    LIMIT 1
),

-- ─────────────────────────────────────
-- CTE 3: Categoría más popular
-- ─────────────────────────────────────
categoria_top AS (
    SELECT
        c.nombre AS categoria,
        COUNT(v.id) AS vistas
    FROM categorias c
    JOIN peliculas p ON p.id_categoria = c.id
    JOIN visualizaciones v ON v.id_pelicula = p.id
    GROUP BY c.nombre
    ORDER BY vistas DESC
    LIMIT 1
),

-- ─────────────────────────────────────
-- CTE 4: Desglose por plan
-- ─────────────────────────────────────
por_plan AS (
    SELECT
        pl.nombre AS plan,
        COUNT(DISTINCT u.id) AS usuarios,
        COALESCE(SUM(pa.monto), 0) AS ingresos,
        ROUND(
            COUNT(DISTINCT v.id_usuario) * 100.0
            / NULLIF(COUNT(DISTINCT u.id), 0),  -- NULLIF evita dividir por 0
            1
        ) AS pct_activos
    FROM planes pl
    LEFT JOIN usuarios u ON u.id_plan = pl.id AND u.activo = true
    LEFT JOIN pagos pa ON pa.id_usuario = u.id
    LEFT JOIN visualizaciones v ON v.id_usuario = u.id
    GROUP BY pl.nombre
)

-- ─────────────────────────────────────
-- CONSULTA FINAL: Unir todo
-- ─────────────────────────────────────
SELECT '📊 MÉTRICAS GENERALES' AS seccion, '' AS detalle
UNION ALL
SELECT '   Usuarios activos',        m.usuarios_activos::TEXT FROM metricas m
UNION ALL
SELECT '   Ingresos totales',        '$' || m.ingresos_totales::TEXT FROM metricas m
UNION ALL
SELECT '   Promedio películas/user',  m.promedio_peliculas_por_usuario::TEXT FROM metricas m
UNION ALL
SELECT '   Película más vista',       pt.titulo || ' (' || pt.vistas || ' vistas)' FROM pelicula_top pt
UNION ALL
SELECT '   Categoría más popular',    ct.categoria || ' (' || ct.vistas || ' vistas)' FROM categoria_top ct
UNION ALL
SELECT '', ''
UNION ALL
SELECT '📈 POR PLAN', ''
UNION ALL
SELECT
    '   ' || plan,
    usuarios || ' usuarios | $' || ingresos || ' ingresos | ' || pct_activos || '% activos'
FROM por_plan
ORDER BY seccion;
```

---

---

## 🧹 Limpieza

```sql
DROP TABLE IF EXISTS pagos, visualizaciones, peliculas,
  categorias, usuarios, planes CASCADE;
```
