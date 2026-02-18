<!-- =========================================================
Archivo: ejercicio_dml_gym.md
Tema: Ejercicio DML — Gimnasio "IronFit"
Estructura: DDL listo + 5 fáciles + 3 avanzados + 7 de pensar
Motor: PostgreSQL (Supabase)
========================================================= -->

# 🏋️ Ejercicio DML — Gimnasio IronFit

---

## ⚙️ Paso 1: Copiar y ejecutar este bloque completo

> Esto crea todas las tablas y carga los datos. **No modifiques nada, solo cópialo y ejecútalo.**

```sql
-- ═══════════════════════════════════════════════
-- 🧹 LIMPIEZA
-- ═══════════════════════════════════════════════
DROP TABLE IF EXISTS inscripciones CASCADE;
DROP TABLE IF EXISTS pagos CASCADE;
DROP TABLE IF EXISTS clases CASCADE;
DROP TABLE IF EXISTS instructores CASCADE;
DROP TABLE IF EXISTS socios CASCADE;
DROP TABLE IF EXISTS membresias CASCADE;

-- ═══════════════════════════════════════════════
-- 📐 ESTRUCTURA (DDL)
-- ═══════════════════════════════════════════════

CREATE TABLE membresias (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(30) NOT NULL UNIQUE,
  precio_mensual  NUMERIC(8,2) NOT NULL CHECK (precio_mensual > 0),
  duracion_meses  INT NOT NULL CHECK (duracion_meses > 0),
  incluye_clases  BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE socios (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(80) NOT NULL,
  email           VARCHAR(120) NOT NULL UNIQUE,
  telefono        VARCHAR(20),
  fecha_registro  TIMESTAMP DEFAULT NOW(),
  id_membresia    INT NOT NULL,
  activo          BOOLEAN DEFAULT TRUE,
  saldo           NUMERIC(10,2) NOT NULL DEFAULT 0,
  FOREIGN KEY (id_membresia) REFERENCES membresias(id)
);

CREATE TABLE instructores (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(80) NOT NULL,
  especialidad    VARCHAR(50) NOT NULL,
  activo          BOOLEAN DEFAULT TRUE
);

CREATE TABLE clases (
  id              SERIAL PRIMARY KEY,
  nombre          VARCHAR(50) NOT NULL,
  id_instructor   INT NOT NULL,
  dia_semana      VARCHAR(15) NOT NULL,
  hora            TIME NOT NULL,
  cupo_maximo     INT NOT NULL CHECK (cupo_maximo > 0),
  FOREIGN KEY (id_instructor) REFERENCES instructores(id)
);

CREATE TABLE inscripciones (
  id              SERIAL PRIMARY KEY,
  id_socio        INT NOT NULL,
  id_clase        INT NOT NULL,
  fecha           TIMESTAMP DEFAULT NOW(),
  asistio         BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (id_socio) REFERENCES socios(id),
  FOREIGN KEY (id_clase) REFERENCES clases(id)
);

CREATE TABLE pagos (
  id              SERIAL PRIMARY KEY,
  id_socio        INT NOT NULL,
  monto           NUMERIC(10,2) NOT NULL CHECK (monto > 0),
  fecha_pago      TIMESTAMP DEFAULT NOW(),
  metodo          VARCHAR(30) NOT NULL DEFAULT 'efectivo',
  concepto        VARCHAR(50) NOT NULL DEFAULT 'mensualidad',
  FOREIGN KEY (id_socio) REFERENCES socios(id)
);

-- ═══════════════════════════════════════════════
-- 📦 DATOS
-- ═══════════════════════════════════════════════

INSERT INTO membresias (nombre, precio_mensual, duracion_meses, incluye_clases) VALUES
  ('Básica',       19990, 1,  false),    -- id 1
  ('Full',         34990, 1,  true),     -- id 2
  ('Trimestral',   29990, 3,  true),     -- id 3
  ('Anual',        24990, 12, true),     -- id 4
  ('Estudiante',   14990, 1,  true);     -- id 5

INSERT INTO instructores (nombre, especialidad) VALUES
  ('Carolina Méndez',  'Yoga'),           -- id 1
  ('Roberto Silva',    'CrossFit'),       -- id 2
  ('Macarena Pinto',   'Spinning'),       -- id 3
  ('Andrés Quiroga',   'Boxeo'),          -- id 4
  ('Javiera Rojas',    'Pilates'),        -- id 5
  ('Felipe Morales',   'Funcional');      -- id 6

INSERT INTO socios (nombre, email, telefono, id_membresia, saldo) VALUES
  ('Lucía Fernández',   'lucia@mail.com',      '912345001', 4, 120000),  -- id 1, Anual
  ('Nicolás Bravo',     'nico@mail.com',        '912345002', 2, 45000),   -- id 2, Full
  ('Sofía Cárdenas',    'sofia@mail.com',       '912345003', 1, 25000),   -- id 3, Básica
  ('Benjamín Reyes',    'benja@mail.com',       '912345004', 5, 15000),   -- id 4, Estudiante
  ('Catalina Vidal',    'cata@mail.com',        '912345005', 2, 80000),   -- id 5, Full
  ('Martín Espinoza',   'martin@mail.com',      '912345006', 3, 60000),   -- id 6, Trimestral
  ('Antonia Lagos',     'antonia@mail.com',      '912345007', 1, 5000),    -- id 7, Básica
  ('Ignacio Parra',     'nacho@mail.com',       '912345008', 5, 2000),    -- id 8, Estudiante
  ('Fernanda Castillo', 'fer@mail.com',         '912345009', 4, 95000),   -- id 9, Anual
  ('Tomás Núñez',       'tomas.n@mail.com',     '912345010', 2, 35000),   -- id 10, Full
  ('Renata Mendoza',    'renata@mail.com',       '912345011', 3, 70000),   -- id 11, Trimestral
  ('Gaspar Olivares',   'gaspar@mail.com',      '912345012', 1, 10000);   -- id 12, Básica

INSERT INTO clases (nombre, id_instructor, dia_semana, hora, cupo_maximo) VALUES
  ('Yoga Matinal',         1, 'Lunes',     '07:30', 20),    -- id 1
  ('Yoga Relax',           1, 'Miércoles', '19:00', 15),    -- id 2
  ('CrossFit Intenso',     2, 'Martes',    '08:00', 12),    -- id 3
  ('CrossFit Open',        2, 'Jueves',    '18:00', 12),    -- id 4
  ('Spinning Power',       3, 'Lunes',     '18:30', 25),    -- id 5
  ('Spinning Noche',       3, 'Viernes',   '20:00', 25),    -- id 6
  ('Boxeo Básico',         4, 'Miércoles', '17:00', 10),    -- id 7
  ('Boxeo Avanzado',       4, 'Sábado',    '10:00', 8),     -- id 8
  ('Pilates Core',         5, 'Martes',    '09:00', 18),    -- id 9
  ('Funcional Express',    6, 'Jueves',    '07:00', 15);    -- id 10

INSERT INTO inscripciones (id_socio, id_clase, asistio) VALUES
  (1, 1,  true),   (1, 9,  true),   (1, 2,  true),   (1, 5,  false),
  (2, 3,  true),   (2, 4,  true),   (2, 5,  true),   (2, 7,  true),
  (2, 10, true),   (3, 5,  true),   (3, 6,  false),
  (4, 3,  true),   (4, 10, true),   (4, 7,  false),
  (5, 1,  true),   (5, 2,  true),   (5, 9,  true),   (5, 3,  true),
  (5, 5,  true),   (5, 6,  true),
  (6, 3,  true),   (6, 4,  true),   (6, 10, true),
  (9, 1,  true),   (9, 2,  true),   (9, 9,  false),
  (10, 5, true),   (10, 7, true),   (10, 8, true),
  (11, 1, true),   (11, 9, true),   (11, 2, true),   (11, 5, false),
  (12, 6, false);

INSERT INTO pagos (id_socio, monto, metodo, concepto) VALUES
  (1,  24990, 'tarjeta',       'mensualidad'),
  (1,  24990, 'tarjeta',       'mensualidad'),
  (2,  34990, 'transferencia', 'mensualidad'),
  (2,  34990, 'transferencia', 'mensualidad'),
  (3,  19990, 'efectivo',      'mensualidad'),
  (4,  14990, 'tarjeta',       'mensualidad'),
  (5,  34990, 'tarjeta',       'mensualidad'),
  (5,  34990, 'tarjeta',       'mensualidad'),
  (5,  34990, 'débito',        'mensualidad'),
  (6,  29990, 'transferencia', 'mensualidad'),
  (9,  24990, 'tarjeta',       'mensualidad'),
  (9,  24990, 'tarjeta',       'mensualidad'),
  (10, 34990, 'débito',        'mensualidad'),
  (11, 29990, 'transferencia', 'mensualidad'),
  (12, 19990, 'efectivo',      'mensualidad');
```

### Verificación rápida

```sql
SELECT 'membresias' AS tabla, COUNT(*) AS filas FROM membresias
UNION ALL SELECT 'socios', COUNT(*) FROM socios
UNION ALL SELECT 'instructores', COUNT(*) FROM instructores
UNION ALL SELECT 'clases', COUNT(*) FROM clases
UNION ALL SELECT 'inscripciones', COUNT(*) FROM inscripciones
UNION ALL SELECT 'pagos', COUNT(*) FROM pagos;
```

Resultado esperado:

| tabla         | filas |
| ------------- | ----- |
| membresias    | 5     |
| socios        | 12    |
| instructores  | 6     |
| clases        | 10    |
| inscripciones | 34    |
| pagos         | 15    |

---

---

---

# 🟢 Nivel Fácil (Requerimientos 1 al 5)

---

### Requerimiento 1

Inserta un nuevo socio llamado **"Pablo Guzmán"** con email **"pablo@mail.com"**, teléfono **"912345013"**, membresía **Full**, y un saldo de **$40,000**.

---

### Requerimiento 2

El instructor **Felipe Morales** cambió de especialidad. Actualiza su especialidad de "Funcional" a **"HIIT"**.

---

### Requerimiento 3

La socia **Antonia Lagos** cargó saldo en su cuenta. Súmale **$20,000** a su saldo actual.

---

### Requerimiento 4

Inserta **3 nuevas inscripciones**: el socio **Gaspar Olivares** (id 12) se inscribió en **Yoga Matinal** (id 1), **Pilates Core** (id 9) y **Funcional Express** (id 10). Marca que todavía no asistió a ninguna.

---

### Requerimiento 5

El instructor **Felipe Morales** dejó de trabajar en el gimnasio. Márcalo como inactivo (`activo = false`). **No lo elimines.**

---

---

---

# 🟡 Nivel intermedio (Requerimientos 6 al 8)

---

### Requerimiento 6: Cobro de mensualidad con transacción

Realiza el cobro mensual al socio **Tomás Núñez** (id 10). En una **transacción** (`BEGIN`/`COMMIT`):

1. Identifica su membresía y el precio correspondiente.
2. Verifica que su saldo sea suficiente.
3. Descuenta el precio de la membresía de su saldo.
4. Registra el pago en la tabla `pagos` con método `'débito'` y concepto `'mensualidad'`.
5. Verifica con un `SELECT` que el saldo final es correcto antes de confirmar.

---

### Requerimiento 7: Cobro fallido con ROLLBACK

Intenta cobrar la mensualidad al socio **Ignacio Parra** (id 8, saldo: $2,000, membresía Estudiante: $14,990):

1. Inicia la transacción.
2. Descuenta el precio de la membresía.
3. Verifica con un `SELECT` → el saldo quedó **negativo**.
4. Deshaz todo con `ROLLBACK`.
5. Verifica que el saldo volvió a $2,000.

> **Pregunta**: ¿Qué restricción agregarías a la columna `saldo` para evitar que esto pase automáticamente?

---

### Requerimiento 8: Cambio de membresía (upgrade)

La socia **Sofía Cárdenas** (id 3) quiere cambiar de membresía **Básica** ($19,990) a **Full** ($34,990). En una transacción:

1. Actualiza su `id_membresia` a Full.
2. Cobra la diferencia ($34,990 - $19,990 = $15,000) descontándola de su saldo.
3. Registra el pago con concepto `'upgrade'`.
4. Verifica que el plan y saldo son correctos.
5. Si todo está bien → `COMMIT`. Si el saldo no alcanza → `ROLLBACK`.

---

---

---

# 🔴 Nivel nivel avanzado — Desafíos de Pensar (Requerimientos 9 al 15)

> Aquí **no te damos la consulta armada**. Te damos lo que el negocio necesita saber y tú decides cómo resolverlo.

---

### Requerimiento 9

El dueño del gimnasio pregunta: **¿Cuáles clases tienen más de 3 inscritos?** Muestra el nombre de la clase, el instructor que la dicta y la cantidad de inscritos. Ordena de mayor a menor.

---

### Requerimiento 10

El área de finanzas necesita saber: **¿Cuánto dinero ha generado cada tipo de membresía en total?** Muestra el nombre de la membresía, la cantidad de pagos y el monto total recaudado.

---

### Requerimiento 11

El equipo de retención quiere saber: **¿Cuáles socios están inscritos en clases pero nunca han asistido a ninguna?** Es decir, tienen inscripciones pero todas con `asistio = false`. Muestra nombre y email.

---

### Requerimiento 12

Para evaluar a los instructores: **¿Cuál es la tasa de asistencia (porcentaje) de cada instructor?** Es decir, del total de inscripciones en sus clases, ¿qué porcentaje efectivamente asistió? Ordena del mejor al peor.

---

### Requerimiento 13

El dueño quiere premiar la fidelidad: **¿Cuáles socios tienen saldo suficiente para cubrir al menos 2 meses más de su membresía actual?** Muestra nombre, saldo, precio de la membresía y cuántos meses les alcanza (redondeado hacia abajo).

---

### Requerimiento 14

Para una campaña de marketing: **¿Cuáles socios NUNCA se han inscrito en ninguna clase?** Muestra nombre, email y el nombre de su membresía.

---

### Requerimiento 15

El directorio pide un reporte ejecutivo que responda en **una sola consulta**:

1. ¿Cuántos socios activos hay?
2. ¿Cuál es el ingreso total del gimnasio?
3. ¿Cuál es la clase más popular (más inscritos)?
4. ¿Cuál es el instructor con mejor tasa de asistencia?
5. ¿Qué porcentaje de socios nunca se inscribió en una clase?

---

---

## 🧹 Limpieza final

```sql
DROP TABLE IF EXISTS inscripciones, pagos, clases,
  instructores, socios, membresias CASCADE;
```
