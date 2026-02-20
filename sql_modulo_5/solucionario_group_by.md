# 📊 Solucionario: Gimnasio de SQL (GROUP BY)

Este documento contiene las respuestas y la explicación pedagógica paso a paso para el profesor de los 5 niveles del gimnasio de SQL.

---

## 🏋️ Nivel 1: El Clásico (Agrupación Simple)

**Objetivo:** Mostrar cuánto dinero total vendió cada sucursal.

### ✅ La Solución Esperada

```sql
SELECT
    sucursal,
    SUM(monto) AS total_vendido
FROM lateral_ventas_mercado
GROUP BY sucursal;
```

### 🧠 Explicación para la clase

1.  **¿Qué hace el SQL por debajo?** Primero toma toda la tabla original. Luego mira el `GROUP BY sucursal` y dice: _"Ok, voy a crear cajas. Una caja dirá 'Norte', otra 'Sur' y otra 'Este'"_.
2.  Empieza a recorrer la tabla tirando cada fila a su caja correspondiente.
3.  Al final, entra a la caja 'Norte', agarra todos los valores de la columna `monto` de esa caja y los suma (`SUM()`). Así comprime 4 filas en 1 sola con el total.

---

## 🏋️ Nivel 2: Sub-grupos Múltiples (Agrupaciones Combinadas)

**Objetivo:** Mostrar la venta total, pero desglosada por sucursal y por departamento.

### ✅ La Solución Esperada

```sql
SELECT
    sucursal,
    departamento,
    SUM(monto) AS total_vendido
FROM lateral_ventas_mercado
GROUP BY sucursal, departamento;
```

### 🧠 Explicación para la clase

1.  **Punto clave:** Si pones dos columnas en el `GROUP BY`, el motor ya no crea la caja "Norte". Ahora crea la caja "Norte - Electrónica" y otra caja separada llamada "Norte - Ropa".
2.  **Regla de Oro:** Todo lo que pongas en el `SELECT` (que no sea una función matemática como SUM, COUNT, etc.) **DEBE** estar presente obligatoriamente en el `GROUP BY`. Si intentas poner el `empleado` en el SELECT, SQL dará error, porque las cajas son por sucursal/departamento, no sabemos de qué empleado específico hablar cuando la fila ya está colapsada y sumada.

---

## 🏋️ Nivel 3: El Guardián de la Puerta (Uso del HAVING)

**Objetivo:** Mostrar a los empleados que lograron más de $400 en total.

### ✅ La Solución Esperada

```sql
SELECT
    empleado,
    SUM(monto) AS total_ventas
FROM lateral_ventas_mercado
GROUP BY empleado
HAVING SUM(monto) > 400;
```

### 🧠 Explicación para la clase

1.  **El error común (Por qué WHERE falla):** Pregúntales a los alumnos qué pasa si intentan:
    `WHERE monto > 400 ... GROUP BY empleado`
    El `WHERE` actúa **ANTES** de que se armen las cajas. Si Juan hizo dos ventas de $300, el WHERE dirá _"300 no es mayor a 400, ¡lo borro!"_. Descartará las dos ventas de Juan, y cuando se arme la caja de Juan, estará vacía. ¡Pero Juan en total tenía $600!
2.  **La magia del HAVING:** El HAVING es el único portero discotequero que trabaja **DESPUÉS** de que las cajas están armadas y sumadas. Actúa sobre el resultado agregado: _"¿La caja de Juan sumó más de 400? Sí, déjala pasar. ¿La de Ana? No, bótala entera"_.

---

## 🏋️ Nivel 4: La Radiografía Completa (Múltiples Agregaciones a la vez)

**Objetivo:** Mostrar cantidad de transacciones, venta mínima, máxima y promedio por departamento.

### ✅ La Solución Esperada

```sql
SELECT
    departamento,
    COUNT(id_venta) AS cantidad_transacciones,
    MIN(monto) AS venta_minima,
    MAX(monto) AS venta_maxima,
    ROUND(AVG(monto), 2) AS promedio_venta
FROM lateral_ventas_mercado
GROUP BY departamento;
```

### 🧠 Explicación para la clase

1.  Una vez que la caja (`GROUP BY departamento`) está sellada, puedes hacerle todas las preguntas estadísticas que quieras dentro del `SELECT`.
2.  `COUNT(id_venta)` o `COUNT(*)` sencillamente cuenta cuántas "cartas" (filas) cayeron dentro de esa caja.
3.  `MIN`, `MAX` y `AVG` abren la caja, revisan los montos, calculan lo pedido y lo muestran como una columna nueva, todo en un solo paso.

---

## 🕵️ Nivel 5: Desafío Jefe - El Tesoro de los Piratas Exigentes

**Objetivo:** Sumar TODAS las joyas de un pirata, pero solo si en su cofre entero hay al menos un "Diamante Negro".

### ✅ La Solución Esperada (Usando filtrado lógico en el HAVING)

```sql
SELECT
    nombre_pirata,
    SUM(cantidad) AS total_joyas
FROM lateral_botin_pirata
GROUP BY nombre_pirata
HAVING SUM(CASE WHEN tipo_joya = 'Diamante Negro' THEN 1 ELSE 0 END) > 0;
```

### 🧠 Explicación para la clase (El Pensamiento Lateral)

1.  **¿Por qué WHERE arruina todo?** Si pones `WHERE tipo_joya = 'Diamante Negro'`, SQL bota todas las monedas de oro a la basura. Cuando la caja de Barbarroja se suma, ¡solo tendrá sus diamantes, perderá su oro!
2.  Necesitamos que el oro y los rubíes ENTREN al `GROUP BY` para sumarlos.
3.  Pero una vez creada la caja, necesitamos una forma matemática de decir: _"¿Contiene este grupo algún Diamante Negro en alguna de sus filas originales?"_
4.  **El truco del CASE WHEN dentro del HAVING:** Inventamos un contador imaginario. Para cada joya dentro de la caja de Barbarroja: si es diamante negro le sumamos 1, sino, 0. Si el total de ese contador inventado es mayor a 0, significa que **había al menos uno** escondido ahí adentro, ¡así que autorizo a mostrar a Barbarroja y su total de joyas reales!
