# Cierre de Clase 2 — Módulo 7

## Los datos como arquitectura del negocio

---

## 1. Lo que hicieron hoy sin darse cuenta

Hoy no crearon modelos. Hoy diseñaron la arquitectura de información de un negocio.

Cuando definieron que un `Producto` tiene una `ForeignKey` a `Categoria`, tomaron una decisión que impacta en la velocidad de las consultas, en la integridad de los datos y en la capacidad del sistema para escalar. Eso no es código — es arquitectura.

Según datos del U.S. Bureau of Labor Statistics (BLS, mayo 2024), el salario medio anual de un Software Developer es de **USD 133.080**, mientras que los perfiles de Software Architect superan los **USD 174.000** anuales según ZipRecruiter (2024). La diferencia — entre un 30% y un 65% más — no la da saber más lenguajes. La da pensar en estructuras, no solo en instrucciones.

> 📚 **Fuentes:**
> - U.S. Bureau of Labor Statistics — *Occupational Employment and Wages, Software Developers* (Mayo 2024)
> - ZipRecruiter — *Software Architect Salary Report* (2024)
> - Indeed — *Software Architect Average Salary* (2024): USD 149.858 promedio anual

---

## 2. El modelo de datos es el negocio

Hay una pregunta que los fundadores de startups se hacen desde el primer día:
**"¿Qué datos vamos a necesitar dentro de 5 años?"**

No es una pregunta técnica. Es una pregunta de negocio.

Cuando Facebook compró Instagram en 2012 por mil millones de dólares, Instagram tenía 13 empleados y ningún ingreso. ¿Por qué valía mil millones? Porque tenía 30 millones de usuarios y el modelo de datos que representaba sus relaciones sociales y su historial visual. Facebook no compró la aplicación. Compró el modelo de datos.

Cuando Amazon compró Whole Foods en 2017, muchos analistas se preguntaron por qué Amazon pagaría USD 13.700 millones por una cadena de supermercados. La respuesta fue la base de datos de comportamiento de compra de 500 tiendas físicas que Whole Foods tenía acumulada durante décadas. Amazon quería entender cómo las personas compran comida fuera de Internet.

> 📚 **Fuentes:**
> - The New York Times — *Facebook to Buy Instagram for $1 Billion* (Abril 2012)
> - CNBC — *Amazon to Buy Whole Foods for $13.7 Billion* (Junio 2017)

Un estudio de McKinsey (2024) encontró que las organizaciones orientadas a datos son **23 veces más propensas a adquirir clientes**, 6 veces más propensas a retenerlos, y **19 veces más propensas a ser rentables** que las que no lo son.

Los datos que hoy guardamos en modelos como `Pedido`, `LineaPedido`, `Pago`, son exactamente el tipo de datos que tienen ese valor estratégico.

> 📚 **Fuente:** McKinsey Global Institute — *The Age of Analytics: Competing in a Data-Driven World* y *Data Summit Survey 2024*

---

## 3. La diferencia entre guardar datos y modelar datos

Guardar datos es fácil. Una planilla de Excel guarda datos. Un archivo de texto guarda datos.

Modelar datos es diferente. Modelar implica tomar decisiones sobre:
- Qué relación existe entre dos conceptos del mundo real
- Qué restricciones impone el negocio sobre esos datos
- Qué preguntas vamos a necesitar responder en el futuro

Un ejemplo concreto: si guardamos el precio del producto dentro del `Pedido` y no en una `LineaPedido` separada, perdemos para siempre la capacidad de responder "¿cuántos productos de menos de $10.000 se vendieron en marzo?". Ese dato ya no existe. No está borrado — nunca fue modelado. Y cuando el CEO lo pida en un año, no hay respuesta posible.

Según Gartner (2024), el **84% de las decisiones de migración de datos se ven afectadas por problemas de calidad de datos**, y las organizaciones pierden un estimado de **USD 1,5 millones anuales** por problemas de calidad de datos que pudieron haberse evitado con un modelado correcto desde el principio.

Las decisiones de modelado que se toman al principio definen qué preguntas se pueden responder en el futuro. Por eso los modelos no son código — son decisiones de negocio escritas en Python.

> 📚 **Fuentes:**
> - Gartner — *Top Trends in Data and Analytics 2024*
> - SourceFuse — *Data Migration Statistics & Insights* (2024)

---

## 4. El costo de un modelo mal diseñado

Refactorizar el código de una vista tarda horas. Refactorizar el modelo de datos de un sistema en producción puede tardar semanas y requiere coordinar migraciones, equipos, downtime y rollback.

Un estudio de CIO Dive (2024) reveló que los proyectos de migración de datos tienen un costo promedio de **USD 315.000 por proyecto**, y que el **61% de los líderes de TI reportan que la fatiga de migración causa retrasos de 6 meses o más**. Además, el **70% experimenta burnout de los desarrolladores** durante estos procesos.

CloudKitchens publicó en su blog de ingeniería que el **80% de las caídas de sus sistemas** en los últimos años fueron causadas por problemas de gestión de esquemas de base de datos. Cambios de esquema que parecían menores provocaron caídas completas del sistema, aumentos de latencia y tickets de soporte masivos.

Lyft — la plataforma de transporte — publicó que su migración de un modelo de datos con una sola tabla de "viajes" a un modelo distribuido con entidades separadas les llevó **14 meses de trabajo continuo** con un equipo de 8 ingenieros senior. El sistema nunca dejó de funcionar durante ese proceso.

Lo que aprendieron hoy — separar modelos en archivos, usar `constraints`, definir `ForeignKey` con los `on_delete` correctos — son exactamente las decisiones que evitan esas migraciones traumáticas.

Según un informe de Ispirer (2024), para una empresa que genera USD 10 millones anuales, **4 horas de downtime por una migración fallida significan USD 20.000 en ingresos perdidos**, sin contar costos de productividad ni de recuperación. Para empresas grandes, el downtime puede costar hasta **USD 1 millón por hora**.

> 📚 **Fuentes:**
> - CIO Dive — *Migration Cost and Fatigue Report* (2024)
> - CloudKitchens Engineering Blog — *Schema Management and Production Outages* (2024)
> - Lyft Engineering Blog — *Redesigning the Ride Data Model*
> - Ispirer — *Database Migration: Cost, Impact, and Hidden Expenses* (2024)
> - DataFlowMapper — *Data Migration Statistics: 80% of Projects Fail* (2024)

---

## 5. Managers y abstracción: el código que protege el negocio

Cuando definimos un Manager personalizado como `Plato.objects.disponibles()`, estamos haciendo algo más que ahorrar líneas de código.

Estamos creando un contrato: "en este sistema, cuando alguien pide platos disponibles, siempre pasa por esta función". Si las reglas de negocio cambian — por ejemplo, que disponible ahora también requiere que el stock sea mayor a cero — se cambia en un solo lugar y todo el sistema se actualiza.

Esto se llama **encapsulamiento de la lógica de negocio**. Según el Stack Overflow Developer Survey (2024), con más de **65.000 desarrolladores encuestados** en mayo de 2024, los roles que demandan habilidades de diseño de sistemas y abstracción — como Senior Backend Developer y Data Engineer — se posicionan consistentemente entre los **mejor remunerados en todas las regiones**.

> 📚 **Fuente:** Stack Overflow — *Developer Survey 2024* (65.000+ respondents)

---

## 6. Lo que sigue: de los modelos al mundo

En las próximas clases van a ir conectando estos modelos con vistas, formularios y APIs. Cada pieza que construyeron hoy va a tener un lugar específico en ese sistema.

Pero hay algo que vale la pena anticipar: el campo que más está creciendo hoy en el mundo de los datos no es el análisis — es la **ingeniería de datos**. El rol que diseña los pipelines, los modelos y las arquitecturas que permiten que los datos lleguen limpios y estructurados al lugar correcto.

McKinsey estimó en su Global Survey de 2024 que los beneficios económicos potenciales de la IA generativa — que depende de datos abundantes, limpios y bien modelados — se ubican entre **USD 2,6 billones y USD 3,4 billones anuales** a nivel global. Pero también advirtió que el **77% de las empresas carecen del talento de datos necesario** para realizar tareas de misión crítica. Eso es una brecha de mercado que se traduce en oportunidad directa para quienes saben modelar datos.

Según la McKinsey Global Survey de 2024, el **65% de las organizaciones ya usan Inteligencia Artificial generativa** de forma regular en al menos una función de negocio — casi el doble que 10 meses antes. Y todas esas aplicaciones de IA dependen de datos bien estructurados desde la base.

Lo que parece técnico hoy, es estratégico mañana.

> 📚 **Fuentes:**
> - McKinsey — *The State of AI in 2024: Global Survey* (2024)
> - McKinsey — *Data Summit Survey 2024: Talent Gap Report*
> - McKinsey Global Institute — *The Economic Potential of Generative AI* (2024)

---
