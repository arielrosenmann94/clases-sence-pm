<!-- =========================================================
Archivo: actividad_streaming.md
Tema: Actividad Progresiva — Plataforma de Streaming "ChileFlix"
Niveles: Básico (DDL + Transacciones) → Avanzado (CTEs, Subconsultas, Window Functions)
Motor: PostgreSQL (Supabase)
========================================================= -->

# 🎬 ChileFlix — Construye tu Plataforma de Streaming

---

---

## 📋 Contexto

Acabas de ser contratado como **Database Engineer** en **ChileFlix**, una nueva plataforma de streaming chilena que compite con Netflix y Disney+.

Tu misión: diseñar la base de datos desde cero, cargar datos, procesar suscripciones de forma segura y generar los reportes que el equipo de negocio necesita para tomar decisiones.

La actividad tiene **3 niveles progresivos**:

| Nivel             | Tema                    | Qué practicarás                                            |
| ----------------- | ----------------------- | ---------------------------------------------------------- |
| 🟢 **Básico**     | Estructura              | DDL: `CREATE TABLE`, tipos de datos, PK, FK, restricciones |
| 🟡 **Intermedio** | Operaciones seguras     | Transacciones: `BEGIN`, `COMMIT`, `ROLLBACK`               |
| 🔴 **Avanzado**   | Inteligencia de negocio | `WITH` (CTEs), subconsultas, `CASE`, funciones de ventana  |

---

---

---

# 🟢 NIVEL 1 — Construcción de la Base de Datos (DDL)

> Diseña las tablas de ChileFlix desde cero. Presta atención al orden de creación (padres → hijos).

---

## Requerimiento 1: Tabla `planes`

Cada plan de suscripción tiene un nombre, precio mensual y cantidad máxima de pantallas simultáneas.

| Columna          | Tipo                      | Restricciones               |
| ---------------- | ------------------------- | --------------------------- |
| `id`             | Entero autoincremental    | Clave primaria              |
| `nombre`         | Texto (máx 30 caracteres) | No nulo, único              |
| `precio_mensual` | Numérico (8,2)            | No nulo, debe ser mayor a 0 |
| `max_pantallas`  | Entero                    | No nulo, debe ser mayor a 0 |

---

## Requerimiento 2: Tabla `usuarios`

Cada usuario tiene un perfil con sus datos y un plan asociado.

| Columna          | Tipo                       | Restricciones                        |
| ---------------- | -------------------------- | ------------------------------------ |
| `id`             | Entero autoincremental     | Clave primaria                       |
| `nombre`         | Texto (máx 80 caracteres)  | No nulo                              |
| `email`          | Texto (máx 120 caracteres) | No nulo, único                       |
| `fecha_registro` | Timestamp                  | Valor por defecto: fecha/hora actual |
| `id_plan`        | Entero                     | No nulo, FK → `planes(id)`           |
| `activo`         | Booleano                   | Valor por defecto: `true`            |
| `saldo`          | Numérico (10,2)            | No nulo, valor por defecto: 0        |

---

## Requerimiento 3: Tabla `categorias`

| Columna  | Tipo                      | Restricciones  |
| -------- | ------------------------- | -------------- |
| `id`     | Entero autoincremental    | Clave primaria |
| `nombre` | Texto (máx 50 caracteres) | No nulo, único |

---

## Requerimiento 4: Tabla `peliculas`

Cada película tiene un título, duración, año de estreno y categoría.

| Columna        | Tipo                       | Restricciones                  |
| -------------- | -------------------------- | ------------------------------ |
| `id`           | Entero autoincremental     | Clave primaria                 |
| `titulo`       | Texto (máx 150 caracteres) | No nulo                        |
| `anio_estreno` | Entero                     | No nulo                        |
| `duracion_min` | Entero                     | No nulo, debe ser mayor a 0    |
| `rating`       | Numérico (3,1)             | Debe estar entre 0.0 y 10.0    |
| `id_categoria` | Entero                     | No nulo, FK → `categorias(id)` |

---

## Requerimiento 5: Tabla `visualizaciones`

Registra cada vez que un usuario ve una película (historial de reproducciones).

| Columna       | Tipo                   | Restricciones                        |
| ------------- | ---------------------- | ------------------------------------ |
| `id`          | Entero autoincremental | Clave primaria                       |
| `id_usuario`  | Entero                 | No nulo, FK → `usuarios(id)`         |
| `id_pelicula` | Entero                 | No nulo, FK → `peliculas(id)`        |
| `fecha_vista` | Timestamp              | Valor por defecto: fecha/hora actual |
| `completada`  | Booleano               | Valor por defecto: `false`           |

---

## Requerimiento 6: Tabla `pagos`

Registra cada cobro mensual realizado a un usuario.

| Columna      | Tipo                      | Restricciones                           |
| ------------ | ------------------------- | --------------------------------------- |
| `id`         | Entero autoincremental    | Clave primaria                          |
| `id_usuario` | Entero                    | No nulo, FK → `usuarios(id)`            |
| `monto`      | Numérico (10,2)           | No nulo, debe ser mayor a 0             |
| `fecha_pago` | Timestamp                 | Valor por defecto: fecha/hora actual    |
| `metodo`     | Texto (máx 30 caracteres) | No nulo, valor por defecto: `'tarjeta'` |

---

## Requerimiento 7: Cargar datos iniciales

Inserta los datos **en el orden correcto** (padres → hijos):

### Planes:

| nombre     | precio_mensual | max_pantallas |
| ---------- | -------------- | ------------- |
| Básico     | 4990           | 1             |
| Estándar   | 7990           | 2             |
| Premium    | 11990          | 4             |
| Estudiante | 2990           | 1             |

### Categorías:

| nombre          |
| --------------- |
| Acción          |
| Comedia         |
| Drama           |
| Terror          |
| Ciencia Ficción |
| Documental      |
| Animación       |

### Usuarios (8 mínimo):

| nombre          | email           | plan       | saldo |
| --------------- | --------------- | ---------- | ----- |
| Valentina Rojas | vale@mail.com   | Premium    | 50000 |
| Matías Torres   | matias@mail.com | Estándar   | 25000 |
| Camila Fuentes  | cami@mail.com   | Básico     | 10000 |
| Sebastián Díaz  | seba@mail.com   | Estudiante | 5000  |
| Isidora Muñoz   | isi@mail.com    | Premium    | 80000 |
| Tomás Herrera   | tomas@mail.com  | Estándar   | 15000 |
| Francisca López | fran@mail.com   | Básico     | 3000  |
| Joaquín Araya   | joaco@mail.com  | Estudiante | 1000  |

### Películas (12 mínimo — al menos 1 por categoría):

| titulo              | anio_estreno | duracion_min | rating | categoría       |
| ------------------- | ------------ | ------------ | ------ | --------------- |
| El Agente Invisible | 2024         | 128          | 7.5    | Acción          |
| Misión Extrema      | 2023         | 135          | 8.2    | Acción          |
| Risa Loca           | 2024         | 95           | 6.8    | Comedia         |
| Noche de Comedia    | 2022         | 102          | 7.1    | Comedia         |
| El Último Adiós     | 2023         | 142          | 9.0    | Drama           |
| Camino al Oscar     | 2024         | 118          | 8.7    | Drama           |
| La Casa Oscura      | 2023         | 98           | 6.5    | Terror          |
| Gritos en la Niebla | 2024         | 91           | 5.8    | Terror          |
| Galaxia Perdida     | 2024         | 155          | 8.9    | Ciencia Ficción |
| Planeta Cero        | 2022         | 130          | 7.3    | Ciencia Ficción |
| Océanos Secretos    | 2023         | 85           | 8.4    | Documental      |
| Mi Vecino Totoro 2  | 2024         | 110          | 9.2    | Animación       |

### Visualizaciones (15+ registros variados):

Genera al menos 15 visualizaciones mezclando usuarios y películas diferentes.
Algunos deben tener `completada = true` y otros `false`.

### Pagos (10+ registros):

Genera al menos 10 pagos con diferentes usuarios, montos y métodos (`'tarjeta'`, `'transferencia'`, `'débito'`).

---

---

---

# 🟡 NIVEL 2 — Operaciones Seguras (Transacciones)

> Todo cobro y cambio de plan debe ser **atómico**: o se hace completo, o no se hace nada.

---

## Requerimiento 8: Cobro mensual con transacción

Simula el cobro mensual al usuario **Valentina Rojas**:

1. Inicia una transacción (`BEGIN`).
2. Obtén el precio de su plan actual.
3. Verifica con un `SELECT` que su saldo sea suficiente.
4. Descuenta el precio del plan de su saldo.
5. Registra el pago en la tabla `pagos`.
6. Verifica con un `SELECT` que el saldo quedó correcto.
7. Confirma con `COMMIT`.

---

## Requerimiento 9: Cobro fallido con ROLLBACK

Simula un cobro al usuario **Joaquín Araya** (saldo: $1,000, plan Estudiante: $2,990):

1. Inicia una transacción (`BEGIN`).
2. Descuenta el precio del plan de su saldo.
3. Verifica con `SELECT` → el saldo quedó **negativo**.
4. Deshaz todo con `ROLLBACK`.
5. Verifica que su saldo volvió a $1,000.

> **Pregunta**: ¿Qué restricción (`CHECK`) podrías agregar a la columna `saldo` para que el sistema **rechace automáticamente** esta operación? Escríbelo como comentario SQL.

---

## Requerimiento 10: Cambio de plan (upgrade)

El usuario **Matías Torres** quiere pasar de plan **Estándar** ($7,990) a **Premium** ($11,990). En una sola transacción:

1. `BEGIN`.
2. Actualiza su `id_plan` al plan Premium.
3. Calcula la diferencia de precio ($11,990 - $7,990 = $4,000).
4. Descuenta la diferencia de su saldo.
5. Registra el pago de $4,000 con método `'upgrade'`.
6. Verifica con un `SELECT` que el plan y saldo son correctos.
7. `COMMIT`.

---

## Requerimiento 11: Cancelación de cuenta

El usuario **Francisca López** cancela su cuenta. En una sola transacción:

1. `BEGIN`.
2. Cambia su columna `activo` a `false`.
3. Registra un último pago de $0 con método `'cancelacion'` (para auditoría).
4. Verifica con `SELECT` que la cuenta está inactiva.
5. `COMMIT`.

---

---

---

# 🔴 NIVEL 3 — Inteligencia de Negocio (Consultas Avanzadas)

> El CEO de ChileFlix necesita reportes para la reunión de directorio.
> Usa **subconsultas**, **CTEs** (`WITH`), y **funciones de ventana** para generarlos.

---

## Requerimiento 12: Películas más vistas que el promedio

Usando una **subconsulta**, encuentra todas las películas que tienen **más visualizaciones que el promedio general**.

```
Pista de estructura:
SELECT titulo, (conteo de visualizaciones)
FROM peliculas
WHERE (conteo de visualizaciones de esta película) > (promedio general de visualizaciones)
```

---

## Requerimiento 13: Usuarios que nunca han visto nada

Usando `NOT IN` o `NOT EXISTS`, encuentra los usuarios que **no tienen ninguna visualización registrada**.

---

## Requerimiento 14: Categoría más popular por visualizaciones

Usando un **CTE** (`WITH`), calcula cuántas visualizaciones tiene cada categoría y ordénalas de mayor a menor.

```sql
-- Estructura sugerida:
WITH vistas_por_categoria AS (
  -- tu consulta aquí: JOIN peliculas + visualizaciones + categorias
  -- GROUP BY categoria
)
SELECT * FROM vistas_por_categoria
ORDER BY total_vistas DESC;
```

---

## Requerimiento 15: Reporte de ingresos por plan

Usando un **CTE**, genera un reporte que muestre:

- Nombre del plan
- Cantidad de usuarios en ese plan
- Total de ingresos (SUM de pagos) por plan
- Ingreso promedio por usuario en ese plan

---

## Requerimiento 16: Top 3 películas por categoría (Window Function)

Usando `ROW_NUMBER()` o `RANK()`, obtén las **3 películas con mejor rating** dentro de cada categoría.

```sql
-- Estructura sugerida:
WITH ranking AS (
  SELECT
    c.nombre AS categoria,
    p.titulo,
    p.rating,
    ROW_NUMBER() OVER (
      PARTITION BY c.nombre
      ORDER BY p.rating DESC
    ) AS posicion
  FROM peliculas p
  JOIN categorias c ON p.id_categoria = c.id
)
SELECT * FROM ranking
WHERE posicion <= 3
ORDER BY categoria, posicion;
```

---

## Requerimiento 17: Usuarios más activos — Ranking completo

Genera un **ranking de usuarios** por cantidad de películas vistas, mostrando:

- Posición en el ranking (`RANK()`)
- Nombre del usuario
- Plan actual
- Total de películas vistas
- Total de películas completadas
- Porcentaje de completitud (`completadas / vistas * 100`)

```sql
-- Estructura sugerida:
WITH actividad AS (
  -- tu consulta aquí
)
SELECT
  RANK() OVER (ORDER BY total_vistas DESC) AS posicion,
  -- resto de columnas
FROM actividad;
```

---

## Requerimiento 18: Análisis de retención — ¿Quién pagó pero no ve nada?

El equipo de marketing necesita saber qué usuarios **han pagado** (tienen registros en `pagos`) pero **no han visto ninguna película en los últimos 30 días**.

Usa un CTE para obtener la última visualización de cada usuario y compárala con la fecha actual.

---

## Requerimiento 19: Reporte ejecutivo con CASE

Genera un reporte que clasifique a cada usuario en un **segmento de engagement**:

| Películas vistas | Segmento    |
| ---------------- | ----------- |
| 0                | 🔴 Inactivo |
| 1 a 3            | 🟡 Casual   |
| 4 a 7            | 🟢 Activo   |
| 8 o más          | 🔵 Superfan |

```sql
-- Usa CASE WHEN para asignar el segmento:
CASE
  WHEN total_vistas = 0 THEN '🔴 Inactivo'
  WHEN total_vistas BETWEEN 1 AND 3 THEN '🟡 Casual'
  WHEN total_vistas BETWEEN 4 AND 7 THEN '🟢 Activo'
  ELSE '🔵 Superfan'
END AS segmento
```

---

## Requerimiento 20: Dashboard del CEO (consulta integradora)

Una **única consulta** con múltiples CTEs que muestre el siguiente resumen ejecutivo:

```
═══════════════════════════════════════════════
         DASHBOARD CHILEFLIX — Febrero 2025
═══════════════════════════════════════════════

📊 Métricas generales:
   - Total de usuarios activos
   - Total de ingresos del mes
   - Película más vista
   - Categoría más popular
   - Promedio de películas por usuario

📈 Por plan:
   - Usuarios por plan
   - Ingresos por plan
   - Tasa de actividad por plan (% que vio algo)
```

```sql
-- Estructura sugerida:
WITH
metricas AS ( ... ),
por_plan AS ( ... ),
pelicula_top AS ( ... )
SELECT ...
```

---

---

## 🧹 Limpieza final

```sql
DROP TABLE IF EXISTS pagos, visualizaciones, peliculas,
  categorias, usuarios, planes CASCADE;
```
