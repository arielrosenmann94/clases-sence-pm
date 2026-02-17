<!-- =========================================================
Archivo: actividad_ecommerce.md
Tema: Actividad Evaluada — Diseño y Manipulación de un E-Commerce
Duración: 1 hora (en clase)
Nivel: Avanzado
Motor: PostgreSQL (Supabase)
========================================================= -->

# 🛒 Actividad Evaluada: Diseño de un Sistema E-Commerce

> **Duración**: 1 hora  
> **Modalidad**: Individual  
> **Motor**: PostgreSQL (Supabase — SQL Editor)  
> **Evaluación**: Se evalúa que cada requerimiento esté resuelto correctamente y que los scripts se puedan ejecutar en orden sin errores.

---

## 📋 Contexto

Una empresa de comercio electrónico te contrata para diseñar y poner en marcha su base de datos desde cero. El sistema debe manejar **clientes**, **categorías de productos**, **productos**, **órdenes de compra** y el **detalle de cada orden**.

Tu trabajo tiene 3 etapas:

1. **Crear la estructura** (tablas con restricciones).
2. **Poblar y manipular los datos** (INSERT, UPDATE, DELETE).
3. **Garantizar la seguridad** de operaciones críticas (transacciones).

---

---

## Etapa 1 — Estructura de la Base de Datos (DDL)

### Requerimiento 1: Tabla `categorias`

Crea una tabla `categorias` con las siguientes columnas:

| Columna       | Tipo                         | Restricciones  |
| ------------- | ---------------------------- | -------------- |
| `id`          | Entero autoincremental       | Clave primaria |
| `nombre`      | Texto (máximo 50 caracteres) | No nulo, único |
| `descripcion` | Texto libre                  | Opcional       |

---

### Requerimiento 2: Tabla `clientes`

Crea una tabla `clientes` con las siguientes columnas:

| Columna          | Tipo                          | Restricciones                        |
| ---------------- | ----------------------------- | ------------------------------------ |
| `id`             | Entero autoincremental        | Clave primaria                       |
| `nombre`         | Texto (máximo 80 caracteres)  | No nulo                              |
| `email`          | Texto (máximo 120 caracteres) | No nulo, único                       |
| `telefono`       | Texto (máximo 20 caracteres)  | Opcional                             |
| `ciudad`         | Texto (máximo 50 caracteres)  | Valor por defecto: `'Santiago'`      |
| `fecha_registro` | Fecha y hora                  | Valor por defecto: fecha/hora actual |

---

### Requerimiento 3: Tabla `productos`

Crea una tabla `productos` con las siguientes columnas:

| Columna        | Tipo                               | Restricciones                               |
| -------------- | ---------------------------------- | ------------------------------------------- |
| `id`           | Entero autoincremental             | Clave primaria                              |
| `nombre`       | Texto (máximo 100 caracteres)      | No nulo                                     |
| `precio`       | Numérico (10 dígitos, 2 decimales) | No nulo, debe ser mayor a 0                 |
| `stock`        | Entero                             | Valor por defecto: 0, no puede ser negativo |
| `id_categoria` | Entero                             | Clave foránea → `categorias(id)`            |
| `activo`       | Booleano                           | Valor por defecto: `true`                   |

---

### Requerimiento 4: Tabla `ordenes`

Crea una tabla `ordenes` con las siguientes columnas:

| Columna       | Tipo                               | Restricciones                           |
| ------------- | ---------------------------------- | --------------------------------------- |
| `id`          | Entero autoincremental             | Clave primaria                          |
| `id_cliente`  | Entero                             | No nulo, clave foránea → `clientes(id)` |
| `fecha_orden` | Fecha y hora                       | Valor por defecto: fecha/hora actual    |
| `estado`      | Texto (máximo 20 caracteres)       | Valor por defecto: `'pendiente'`        |
| `total`       | Numérico (12 dígitos, 2 decimales) | Valor por defecto: 0                    |

---

### Requerimiento 5: Tabla `detalle_orden`

Crea una tabla `detalle_orden` con las siguientes columnas:

| Columna           | Tipo                               | Restricciones                            |
| ----------------- | ---------------------------------- | ---------------------------------------- |
| `id`              | Entero autoincremental             | Clave primaria                           |
| `id_orden`        | Entero                             | No nulo, clave foránea → `ordenes(id)`   |
| `id_producto`     | Entero                             | No nulo, clave foránea → `productos(id)` |
| `cantidad`        | Entero                             | No nulo, debe ser mayor a 0              |
| `precio_unitario` | Numérico (10 dígitos, 2 decimales) | No nulo                                  |
| `subtotal`        | Numérico (12 dígitos, 2 decimales) | No nulo                                  |

> **Pista**: Esta tabla tiene **dos claves foráneas** (una hacia `ordenes` y otra hacia `productos`). Piensa en qué orden debes crear las tablas para que las FK no fallen.

---

---

## Etapa 2 — Manipulación de Datos (DML)

### Requerimiento 6: Insertar datos base

Inserta los siguientes datos **en el orden correcto** (respetando las FK):

**Categorías** (3 mínimo):

| nombre      | descripcion                            |
| ----------- | -------------------------------------- |
| Electrónica | Dispositivos y accesorios tecnológicos |
| Ropa        | Vestuario y moda                       |
| Hogar       | Muebles y decoración                   |

**Clientes** (4 mínimo):

| nombre          | email           | ciudad     |
| --------------- | --------------- | ---------- |
| Valentina Rojas | vale@mail.com   | Santiago   |
| Matías Torres   | matias@mail.com | Valparaíso |
| Camila Fuentes  | cami@mail.com   | Concepción |
| Sebastián Díaz  | seba@mail.com   | Santiago   |

**Productos** (6 mínimo — al menos 2 por categoría):

| nombre              | precio | stock | categoría   |
| ------------------- | ------ | ----- | ----------- |
| Audífonos Bluetooth | 24990  | 50    | Electrónica |
| Cargador USB-C      | 8990   | 100   | Electrónica |
| Polera Algodón      | 12990  | 80    | Ropa        |
| Jeans Slim          | 29990  | 40    | Ropa        |
| Lámpara LED         | 15990  | 30    | Hogar       |
| Cojín Decorativo    | 9990   | 60    | Hogar       |

---

### Requerimiento 7: Crear una orden completa

Crea **una orden** para el cliente Valentina Rojas que contenga:

- 2 Audífonos Bluetooth
- 1 Polera Algodón

Para esto debes:

1. Insertar un registro en `ordenes` (con el `id_cliente` correcto).
2. Insertar **2 registros** en `detalle_orden` (uno por cada producto).
3. Calcular el `subtotal` de cada línea (`cantidad × precio_unitario`).
4. Actualizar el `total` de la orden en `ordenes` con la suma de los subtotales.

---

### Requerimiento 8: Ajuste de precios

La empresa necesita los siguientes cambios:

1. Subir un **10%** el precio de todos los productos de la categoría **Electrónica**.
2. Aplicar un **descuento de $2,000** a todos los productos que cuesten más de **$20,000**.
3. Desactivar (`activo = false`) todos los productos que tengan **stock = 0**.

> Recuerda la **buena práctica**: haz un `SELECT` con el mismo `WHERE` antes de cada `UPDATE` para verificar qué filas se verán afectadas.

---

### Requerimiento 9: Eliminar datos con cuidado

1. Intenta eliminar al cliente **Sebastián Díaz**.
   - Si tiene órdenes asociadas, explica **por qué falla** y cuál sería la solución (no es necesario ejecutarla).
   - Si no tiene órdenes, elimínalo normalmente.

2. Elimina todos los productos que estén desactivados (`activo = false`) **solo si no tienen detalle de órdenes asociadas**. Verifica primero.

---

---

## Etapa 3 — Transacciones

### Requerimiento 10: Procesamiento de orden con transacción

Crea una **nueva orden** para el cliente **Matías Torres** que contenga:

- 3 Cargadores USB-C
- 1 Lámpara LED

Todo el proceso debe hacerse dentro de una **transacción** (`BEGIN` / `COMMIT`):

1. Insertar la orden en `ordenes`.
2. Insertar los 2 detalles en `detalle_orden`.
3. **Descontar el stock** de cada producto según la cantidad comprada.
4. Actualizar el `total` de la orden.
5. Verificar con un `SELECT` que los saldos de stock sean correctos **antes de hacer COMMIT**.

---

### Requerimiento 11: Simulación de error con ROLLBACK

Simula el siguiente escenario:

1. Inicia una transacción (`BEGIN`).
2. Intenta crear una orden para **Camila Fuentes** con **200 Jeans Slim** (más de los que hay en stock).
3. Descuenta el stock.
4. Verifica con un `SELECT` que el stock quedó **negativo o en un valor irreal**.
5. Deshaz todo con `ROLLBACK`.
6. Verifica que el stock volvió a su valor original.

> **Pregunta**: ¿Qué restricción de la tabla podría haber evitado este problema automáticamente? Escríbelo como comentario SQL (`-- tu respuesta`).

---

---

## 📊 Consultas de Validación

Cuando termines todos los requerimientos, ejecuta estas consultas para verificar tu trabajo:

```sql
-- 1. Resumen de productos por categoría
SELECT
  c.nombre AS categoria,
  COUNT(p.id) AS total_productos,
  ROUND(AVG(p.precio), 0) AS precio_promedio,
  SUM(p.stock) AS stock_total
FROM categorias c
LEFT JOIN productos p ON c.id = p.id_categoria
WHERE p.activo = true
GROUP BY c.nombre
ORDER BY total_productos DESC;

-- 2. Órdenes con sus detalles
SELECT
  o.id AS orden,
  cl.nombre AS cliente,
  p.nombre AS producto,
  d.cantidad,
  d.precio_unitario,
  d.subtotal,
  o.total AS total_orden,
  o.estado
FROM ordenes o
JOIN clientes cl ON o.id_cliente = cl.id
JOIN detalle_orden d ON d.id_orden = o.id
JOIN productos p ON d.id_producto = p.id
ORDER BY o.id, d.id;

-- 3. Conteo general
SELECT 'Categorías' AS tabla, COUNT(*) AS registros FROM categorias
UNION ALL SELECT 'Clientes', COUNT(*) FROM clientes
UNION ALL SELECT 'Productos', COUNT(*) FROM productos
UNION ALL SELECT 'Órdenes', COUNT(*) FROM ordenes
UNION ALL SELECT 'Detalles', COUNT(*) FROM detalle_orden;
```

---

## 🧹 Limpieza (ejecutar al final)

```sql
DROP TABLE IF EXISTS detalle_orden, ordenes, productos,
  clientes, categorias CASCADE;
```
