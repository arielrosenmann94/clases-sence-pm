<!-- =========================================================
Archivo: ejercicio_dml_gym_respuestas.md
Tema: Respuestas — Ejercicio DML Gimnasio "IronFit"
========================================================= -->

# 🏋️ Ejercicio DML IronFit — Respuestas del Mentor

---

---

# 🟢 Nivel Fácil

---

## Requerimiento 1: Insertar socio

```sql
INSERT INTO socios (nombre, email, telefono, id_membresia, saldo)
VALUES ('Pablo Guzmán', 'pablo@mail.com', '912345013', 2, 40000);
-- id_membresia = 2 → Full
-- fecha_registro se llena sola (DEFAULT NOW())
-- activo se llena solo (DEFAULT TRUE)
```

---

## Requerimiento 2: Actualizar especialidad

```sql
-- Buena práctica: verificar primero
SELECT nombre, especialidad FROM instructores WHERE nombre = 'Felipe Morales';
-- Felipe Morales | Funcional

UPDATE instructores
SET especialidad = 'HIIT'
WHERE nombre = 'Felipe Morales';

-- Verificar
SELECT nombre, especialidad FROM instructores WHERE nombre = 'Felipe Morales';
-- Felipe Morales | HIIT ← ✅
```

---

## Requerimiento 3: Sumar saldo

```sql
-- Verificar saldo actual
SELECT nombre, saldo FROM socios WHERE nombre = 'Antonia Lagos';
-- Antonia Lagos | 5000

UPDATE socios
SET saldo = saldo + 20000       -- SUMAR, no reemplazar
WHERE nombre = 'Antonia Lagos';

-- Verificar
SELECT nombre, saldo FROM socios WHERE nombre = 'Antonia Lagos';
-- Antonia Lagos | 25000 ← ✅
```

> **Error común**: escribir `SET saldo = 20000` → eso REEMPLAZA el saldo.
> Lo correcto es `SET saldo = saldo + 20000` → eso SUMA al saldo existente.

---

## Requerimiento 4: Insertar inscripciones

```sql
INSERT INTO inscripciones (id_socio, id_clase, asistio) VALUES
  (12, 1,  false),    -- Gaspar → Yoga Matinal
  (12, 9,  false),    -- Gaspar → Pilates Core
  (12, 10, false);    -- Gaspar → Funcional Express
-- asistio = false porque todavía no ha ido
```

---

## Requerimiento 5: Desactivar instructor

```sql
UPDATE instructores
SET activo = FALSE
WHERE nombre = 'Felipe Morales';
-- NO usamos DELETE porque podría tener clases asociadas (FK)
-- y además queremos conservar su historial
```

---

---

# 🟡 Nivel Avanzado

---

## Requerimiento 6: Cobro mensual con transacción

```sql
-- ═══════════════════════════════════════════════
-- COBRO MENSUAL A TOMÁS NÚÑEZ
-- Saldo: $35,000 | Membresía Full: $34,990
-- Saldo esperado después del cobro: $10
-- ═══════════════════════════════════════════════

BEGIN;
-- Todo lo que sigue es TEMPORAL hasta el COMMIT o ROLLBACK

-- Paso 1: Ver datos actuales
SELECT
  s.nombre, s.saldo,
  m.nombre AS membresia, m.precio_mensual
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
WHERE s.id = 10;
-- Tomás Núñez | 35000 | Full | 34990

-- Paso 2: Verificar que alcanza
-- 35000 >= 34990 → ✅ SÍ alcanza

-- Paso 3: Descontar membresía del saldo
UPDATE socios
SET saldo = saldo - (
    SELECT m.precio_mensual
    FROM membresias m
    JOIN socios s ON s.id_membresia = m.id
    WHERE s.id = 10
)
WHERE id = 10;

-- Paso 4: Registrar el pago
INSERT INTO pagos (id_socio, monto, metodo, concepto)
VALUES (
  10,
  (SELECT precio_mensual FROM membresias
   WHERE id = (SELECT id_membresia FROM socios WHERE id = 10)),
  'débito',
  'mensualidad'
);

-- Paso 5: Verificar resultado
SELECT nombre, saldo FROM socios WHERE id = 10;
-- Tomás Núñez | 10.00 ← ✅ (35000 - 34990 = 10)

COMMIT;
-- ✅ Cambios grabados: saldo descontado + pago registrado
```

---

## Requerimiento 7: Cobro fallido con ROLLBACK

```sql
-- ═══════════════════════════════════════════════
-- COBRO FALLIDO A IGNACIO PARRA
-- Saldo: $2,000 | Membresía Estudiante: $14,990
-- $2,000 < $14,990 → NO ALCANZA
-- ═══════════════════════════════════════════════

-- Verificar ANTES de empezar
SELECT nombre, saldo FROM socios WHERE id = 8;
-- Ignacio Parra | 2000.00

BEGIN;
-- Abrimos la "burbuja protectora"
-- Todo cambio es temporal hasta que hagamos COMMIT o ROLLBACK

-- Paso 1: Intentar descontar (aunque sabemos que no alcanza)
UPDATE socios
SET saldo = saldo - 14990
WHERE id = 8;
-- Se ejecuta TEMPORALMENTE → saldo queda en -12990

-- Paso 2: Verificar resultado
SELECT nombre, saldo FROM socios WHERE id = 8;
-- Ignacio Parra | -12990.00 ← 🚨 ¡SALDO NEGATIVO!

-- Paso 3: DESHACER TODO
ROLLBACK;
-- ══════════════════════════════════════════════════════════
-- ¿QUÉ HACE ROLLBACK?
-- Cancela TODOS los cambios hechos desde el BEGIN.
-- La base de datos vuelve al ESTADO EXACTO de antes del BEGIN.
-- Es como si el UPDATE nunca hubiera existido.
-- ══════════════════════════════════════════════════════════

-- Verificar que se deshizo
SELECT nombre, saldo FROM socios WHERE id = 8;
-- Ignacio Parra | 2000.00 ← ✅ Volvió a su valor original

-- ¿QUÉ PASARÍA SIN TRANSACCIÓN?
-- Si hubiéramos hecho el UPDATE sin BEGIN/ROLLBACK:
--   UPDATE socios SET saldo = saldo - 14990 WHERE id = 8;
-- El saldo quedaría en -12990 DE FORMA PERMANENTE 😱
-- No habría forma de deshacerlo (salvo hacer otro UPDATE manual)
```

**Respuesta a la pregunta:**

```sql
-- Para evitar saldos negativos automáticamente:
ALTER TABLE socios ADD CONSTRAINT chk_saldo_positivo CHECK (saldo >= 0);
-- Ahora si alguien intenta un UPDATE que deje saldo < 0,
-- PostgreSQL lo RECHAZA con un error, sin necesidad de ROLLBACK.
```

---

## Requerimiento 8: Upgrade de membresía

```sql
-- ═══════════════════════════════════════════════
-- UPGRADE: SOFÍA DE BÁSICA ($19,990) A FULL ($34,990)
-- Diferencia: $15,000
-- Saldo actual: $25,000 → Saldo final esperado: $10,000
-- ═══════════════════════════════════════════════

BEGIN;

-- Paso 1: Ver estado actual
SELECT s.nombre, s.saldo, m.nombre AS membresia, m.precio_mensual
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
WHERE s.id = 3;
-- Sofía Cárdenas | 25000 | Básica | 19990

-- Paso 2: Actualizar membresía a Full
UPDATE socios
SET id_membresia = (SELECT id FROM membresias WHERE nombre = 'Full')
WHERE id = 3;

-- Paso 3: Cobrar la diferencia
UPDATE socios
SET saldo = saldo - 15000      -- 34990 - 19990 = 15000
WHERE id = 3;

-- Paso 4: Registrar el pago
INSERT INTO pagos (id_socio, monto, metodo, concepto)
VALUES (3, 15000, 'tarjeta', 'upgrade');

-- Paso 5: Verificar
SELECT s.nombre, s.saldo, m.nombre AS membresia
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
WHERE s.id = 3;
-- Sofía Cárdenas | 10000 | Full ← ✅

-- Saldo suficiente → confirmar
COMMIT;
```

---

---

# 🔴 Nivel Experto — Desafíos de Pensar

---

## Requerimiento 9: Clases con más de 3 inscritos

```sql
SELECT
  c.nombre AS clase,
  i.nombre AS instructor,
  COUNT(ins.id) AS total_inscritos
FROM clases c
JOIN instructores i ON c.id_instructor = i.id
JOIN inscripciones ins ON ins.id_clase = c.id
GROUP BY c.id, c.nombre, i.nombre
HAVING COUNT(ins.id) > 3
ORDER BY total_inscritos DESC;
```

---

## Requerimiento 10: Ingresos por membresía

```sql
SELECT
  m.nombre AS membresia,
  COUNT(p.id) AS cantidad_pagos,
  SUM(p.monto) AS total_recaudado
FROM membresias m
JOIN socios s ON s.id_membresia = m.id
JOIN pagos p ON p.id_socio = s.id
GROUP BY m.nombre
ORDER BY total_recaudado DESC;
```

---

## Requerimiento 11: Inscritos que nunca asistieron

```sql
-- Socios que tienen inscripciones pero NINGUNA con asistio = true
SELECT s.nombre, s.email
FROM socios s
JOIN inscripciones ins ON ins.id_socio = s.id
GROUP BY s.id, s.nombre, s.email
HAVING COUNT(ins.id) FILTER (WHERE ins.asistio = true) = 0;
-- FILTER: cuenta solo las que cumplen la condición
-- Si el conteo de asistencias = 0, nunca fue
```

**Alternativa sin FILTER:**

```sql
SELECT s.nombre, s.email
FROM socios s
WHERE s.id IN (SELECT DISTINCT id_socio FROM inscripciones)  -- tiene inscripciones
  AND s.id NOT IN (                                           -- pero nunca asistió
    SELECT DISTINCT id_socio FROM inscripciones WHERE asistio = true
  );
```

---

## Requerimiento 12: Tasa de asistencia por instructor

```sql
SELECT
  i.nombre AS instructor,
  i.especialidad,
  COUNT(ins.id) AS total_inscripciones,
  COUNT(ins.id) FILTER (WHERE ins.asistio = true) AS asistencias,
  ROUND(
    COUNT(ins.id) FILTER (WHERE ins.asistio = true) * 100.0
    / COUNT(ins.id),
    1
  ) AS tasa_asistencia
FROM instructores i
JOIN clases c ON c.id_instructor = i.id
JOIN inscripciones ins ON ins.id_clase = c.id
GROUP BY i.id, i.nombre, i.especialidad
ORDER BY tasa_asistencia DESC;
```

---

## Requerimiento 13: Socios con saldo para 2+ meses

```sql
SELECT
  s.nombre,
  s.saldo,
  m.nombre AS membresia,
  m.precio_mensual,
  FLOOR(s.saldo / m.precio_mensual) AS meses_restantes
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
WHERE s.activo = true
  AND s.saldo / m.precio_mensual >= 2
ORDER BY meses_restantes DESC;
-- FLOOR: redondea hacia abajo (3.7 → 3 meses)
```

---

## Requerimiento 14: Socios sin inscripciones

```sql
SELECT
  s.nombre,
  s.email,
  m.nombre AS membresia
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
WHERE s.id NOT IN (
    SELECT DISTINCT id_socio FROM inscripciones
);

-- Alternativa con LEFT JOIN:
SELECT
  s.nombre, s.email, m.nombre AS membresia
FROM socios s
JOIN membresias m ON s.id_membresia = m.id
LEFT JOIN inscripciones ins ON ins.id_socio = s.id
WHERE ins.id IS NULL;     -- Si el LEFT JOIN no encuentra nada → NULL
```

---

## Requerimiento 15: Reporte ejecutivo

```sql
WITH
activos AS (
    SELECT COUNT(*) AS total FROM socios WHERE activo = true
),
ingresos AS (
    SELECT COALESCE(SUM(monto), 0) AS total FROM pagos
),
clase_popular AS (
    SELECT c.nombre, COUNT(ins.id) AS inscritos
    FROM clases c
    JOIN inscripciones ins ON ins.id_clase = c.id
    GROUP BY c.id, c.nombre
    ORDER BY inscritos DESC
    LIMIT 1
),
mejor_instructor AS (
    SELECT
        i.nombre,
        ROUND(
            COUNT(ins.id) FILTER (WHERE ins.asistio = true) * 100.0
            / COUNT(ins.id), 1
        ) AS tasa
    FROM instructores i
    JOIN clases c ON c.id_instructor = i.id
    JOIN inscripciones ins ON ins.id_clase = c.id
    GROUP BY i.id, i.nombre
    ORDER BY tasa DESC
    LIMIT 1
),
sin_clases AS (
    SELECT ROUND(
        COUNT(*) FILTER (
            WHERE s.id NOT IN (SELECT DISTINCT id_socio FROM inscripciones)
        ) * 100.0 / COUNT(*), 1
    ) AS porcentaje
    FROM socios s
    WHERE s.activo = true
)

SELECT '1. Socios activos' AS metrica,      a.total::TEXT AS valor FROM activos a
UNION ALL
SELECT '2. Ingreso total',                  '$' || i.total::TEXT FROM ingresos i
UNION ALL
SELECT '3. Clase más popular',              cp.nombre || ' (' || cp.inscritos || ' inscritos)' FROM clase_popular cp
UNION ALL
SELECT '4. Mejor instructor',              mi.nombre || ' (' || mi.tasa || '% asistencia)' FROM mejor_instructor mi
UNION ALL
SELECT '5. % socios sin clases',           sc.porcentaje || '%' FROM sin_clases sc;
```

---

---

## 🧹 Limpieza

```sql
DROP TABLE IF EXISTS inscripciones, pagos, clases,
  instructores, socios, membresias CASCADE;
```
