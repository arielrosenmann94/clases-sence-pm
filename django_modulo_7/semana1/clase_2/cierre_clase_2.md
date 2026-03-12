# Cierre de Clase 2 — Módulo 7

# 🏗️ Los datos como arquitectura del negocio

---

# 1. Lo que hicieron hoy

> Hoy no crearon modelos.
> Hoy diseñaron la **arquitectura de información** de un negocio.

Cuando definieron que un `Producto` tiene una `ForeignKey` a `Categoria`, tomaron una decisión que impacta en la velocidad de las consultas, en la integridad de los datos y en la capacidad del sistema para escalar. Eso no es código — es arquitectura.

🔑 `Producto → ForeignKey → Categoria`

Esa línea impacta en:
- ⚡ Velocidad de las consultas
- 🛡️ Integridad de los datos
- 📈 Capacidad de escalar

**Un Software Architect gana entre un 30% y un 65% más que un Developer promedio.** La diferencia no es saber más lenguajes. Es pensar en **estructuras**, no solo en instrucciones.

*(U.S. Bureau of Labor Statistics, 2024; ZipRecruiter, 2024)*

---

# 2. El modelo de datos ES el negocio

Hay una pregunta que los fundadores de startups se hacen desde el primer día:

> *"¿Qué datos vamos a necesitar dentro de 5 años?"*

No es una pregunta técnica. Es una pregunta de negocio. Los dos casos más emblemáticos de la historia reciente lo demuestran.

---

### 📱 Facebook compra Instagram (2012)

Facebook pagó **mil millones de dólares** por Instagram. En ese momento, Instagram tenía solo 13 empleados y ningún ingreso. ¿Por qué valía mil millones? Porque tenía 30 millones de usuarios y el modelo de datos que representaba sus relaciones sociales y su historial visual.

Facebook no compró la aplicación. **Compró el modelo de datos.**

*(The New York Times, Abril 2012)*

---

### 🛒 Amazon compra Whole Foods (2017)

Amazon pagó **13.700 millones de dólares** por una cadena de supermercados. Muchos analistas no entendieron por qué. La respuesta fue la base de datos de comportamiento de compra de 500 tiendas físicas que Whole Foods tenía acumulada durante décadas.

Amazon quería entender cómo las personas compran comida **fuera de Internet.**

*(CNBC, Junio 2017)*

---

### 📊 El dato que lo confirma

Las organizaciones orientadas a datos son:

| Métrica | Ventaja |
|---------|---------|
| Adquisición de clientes | **23x** más propensas |
| Retención de clientes   | **6x** más propensas  |
| Rentabilidad             | **19x** más propensas |

Los datos que hoy guardamos en modelos como `Pedido`, `LineaPedido`, `Pago`, son exactamente el tipo de datos que tienen ese valor estratégico.

*(McKinsey Global Institute, 2024)*

---

# 3. Guardar datos ≠ Modelar datos

Guardar datos es fácil. Una planilla de Excel guarda datos. Un archivo de texto guarda datos. Modelar datos es diferente.

| Guardar | Modelar |
|---------|---------|
| Excel guarda datos | Definir **relaciones** entre conceptos |
| Un .txt guarda datos | Imponer **restricciones** del negocio |
| Cualquiera lo hace | Definir qué **preguntas** se podrán responder en el futuro |

---

### 🧪 Ejemplo concreto

Si guardamos el **precio** del producto dentro de `Pedido` y no en una `LineaPedido` separada, perdemos para siempre la capacidad de responder:

❌ *"¿Cuántos productos de menos de $10.000 se vendieron en marzo?"*

Ese dato no está borrado. **Nunca fue modelado.** Y cuando el CEO lo pida en un año, no hay respuesta posible. Las decisiones de modelado que se toman al principio definen qué preguntas se pueden responder en el futuro.

---

### ⚠️ ¿Qué dice la industria?

- **84%** de las migraciones de datos fallan por mala calidad en los datos
- Las organizaciones pierden **millones anuales** por errores de modelado que pudieron haberse evitado desde el principio

*(Gartner, 2024; SourceFuse, 2024)*

---

# 4. El costo de un modelo mal diseñado

Refactorizar el código de una vista tarda horas. Refactorizar el modelo de datos de un sistema en producción puede tardar semanas o meses, y requiere coordinar migraciones, equipos, downtime y rollback.

> Refactorizar una **vista** → horas
> Refactorizar un **modelo de datos** en producción → semanas o meses

---

### 📉 Datos reales de la industria

| Fuente | Hallazgo |
|--------|----------|
| CIO Dive, 2024 | **61%** de líderes TI reportan retrasos de 6+ meses por fatiga de migración |
| CIO Dive, 2024 | **70%** experimenta burnout de desarrolladores durante migraciones |
| CloudKitchens, 2024 | **80%** de sus caídas de producción fueron por problemas de esquemas de BD |
| DataFlowMapper, 2024 | **+80%** de proyectos de migración no cumplen sus objetivos |
| Ispirer, 2024 | **4 horas** de downtime = 0,2% de los ingresos anuales de una empresa |

---

### 🔧 Caso real: Lyft

La plataforma de transporte Lyft publicó en su blog de ingeniería que migrar de **una sola tabla de "viajes"** a un modelo distribuido con entidades separadas les costó:

- ⏱️ **14 meses** de trabajo continuo
- 👥 **8 ingenieros senior** dedicados
- ✅ El sistema **nunca dejó de funcionar** durante la cirugía

Lo que aprendieron hoy — separar modelos en archivos, usar `constraints`, definir `ForeignKey` con los `on_delete` correctos — son exactamente las decisiones que evitan esas migraciones traumáticas.

*(Lyft Engineering Blog)*

---

# 5. Managers = protección del negocio

Cuando definimos un Manager personalizado como `Plato.objects.disponibles()`, estamos creando un **contrato**: cuando alguien pide platos disponibles, siempre pasa por esta función.

```python
Plato.objects.disponibles()
```

Si las reglas de negocio cambian — por ejemplo, que disponible ahora también requiere que el stock sea mayor a cero — se cambia en **1 solo lugar** y todo el sistema se actualiza.

Esto se llama **encapsulamiento de la lógica de negocio.** En el Stack Overflow Developer Survey 2024 (**65.000+ developers encuestados**), los roles con habilidades de diseño de sistemas y abstracción son los **mejor remunerados** en todas las regiones.

*(Stack Overflow, 2024)*

---

# 6. Lo que sigue: de los modelos al mundo

En las próximas clases van a conectar estos modelos con vistas, formularios y APIs. Cada pieza que construyeron hoy va a tener un lugar específico en ese sistema.

Pero hay algo que vale la pena anticipar: el campo que más está creciendo hoy no es el análisis de datos — es la **ingeniería de datos.**

---

### 🤖 La IA necesita tus modelos

| Fuente | Hallazgo |
|--------|----------|
| McKinsey, 2024 | **65%** de organizaciones ya usan IA generativa regularmente |
| McKinsey, 2024 | **77%** de empresas carecen de talento de datos para tareas críticas |
| Gartner, 2024 | Empresas con IA estratégica superan a sus pares en un **80%** en 9 años |

El potencial económico de la IA generativa se estima en **billones de dólares anuales** a nivel global. Pero toda esa IA depende de datos abundantes, limpios y bien modelados.

---

### 💡 La oportunidad

El **77%** de las empresas no tienen
quien modele sus datos correctamente.

Esa es la brecha.
**Esa es la oportunidad.**

---

> Lo que parece técnico hoy
> es **estratégico** mañana.

---
