# 🏗️ Django — Módulo 6 · Clase 5

## Segunda parte — El mundo real del software

---

> _"Saber programar no es suficiente para construir software que funcione en el mundo real. Esta segunda parte es sobre todo lo que pasa alrededor del código."_

---

---

# Por qué fracasan los proyectos de software

---

> _"Terminamos de hablar de arquitectura. Ahora hay que entender por qué todo eso importa — con números reales."_

---

## Las estadísticas

El Standish Group publica cada año el CHAOS Report, el informe de referencia más citado en la industria del software. Las cifras del informe de 2024, que analizó decenas de miles de proyectos a nivel global, muestran una leve mejoría respecto a años anteriores pero confirman el mismo patrón de fondo:

- **Entre el 35% y el 39% de los proyectos de software** se entregan a tiempo, dentro del presupuesto y con todas las funcionalidades prometidas.
- El resto se entrega tarde, caro, recortado, o directamente se cancela.

Es decir: **más del 60% de los proyectos de software no cumple lo que prometió**.

Eso es antes de considerar si lo que se entregó realmente solucionó el problema del negocio.

---

McKinsey, en investigaciones publicadas entre 2023 y 2025, sigue relevando los mismos patrones en proyectos grandes de IT:

- Los proyectos grandes de IT se pasan en promedio un **45% del presupuesto** y un **7% del tiempo**.
- Entregan **un 56% menos de valor** del que prometían al inicio.
- El **17% de los proyectos grandes** falla tan gravemente que pone en riesgo la existencia de la empresa.
  _(McKinsey & Company, "Delivering large-scale IT projects on time, on budget, and on value", actualizado 2024)_

---

Y el dato que más impacta:

> Los **proyectos pequeños** tienen hasta un **90% de probabilidad de salir bien**. Los **proyectos grandes** tienen **menos del 10%**.
> _(Standish Group CHAOS Report, 2024)_

La diferencia no es el talento del equipo. Es el alcance, la planificación, y la claridad de las decisiones que se tomaron antes de empezar.

---

## Por qué fallan — las causas reales

McKinsey identificó que los fracasos de proyectos de software casi nunca son por razones técnicas. Las causas más frecuentes son:

1. **Objetivos poco claros** — el equipo no sabe exactamente qué tiene que construir.
2. **Requisitos que cambian sin control** — el cliente pide algo, el equipo lo construye, el cliente quiere otra cosa. Sin proceso.
3. **Falta de comunicación** — el equipo técnico y el equipo de negocio hablan idiomas distintos y nadie traduce.
4. **Estimaciones irreales** — se promete en seis meses lo que necesita dieciocho.
5. **Sin definición de éxito** — el proyecto termina y nadie sabe si fue exitoso porque nunca se definió qué significaba eso.

---

## El caso real: Healthcare.gov (2013)

En octubre de 2013, el gobierno de los Estados Unidos lanzó Healthcare.gov, el sitio de inscripción al sistema de salud. Era el proyecto tecnológico más importante de la administración Obama.

Costó **600 millones de dólares**.

El día del lanzamiento, el sitio colapsó. No se podía crear una cuenta. No se podía ver un plan disponible. Millones de personas intentaron acceder y no pudieron.

¿Por qué falló? No fue por falta de presupuesto ni por falta de talento. Fue porque **55 empresas contratistas trabajaron en paralelo sin que nadie coordinara la arquitectura**. Cada una construyó su parte sin saber cómo encajaba con el resto. Nadie tomó las decisiones que vieron esta tarde antes de empezar.

El desenlace: después de semanas de crisis pública, un equipo pequeño de voluntarios especializados —llamados "the tech surge"— tomó el control y en tres meses rescató el sistema.

El proyecto no fracasó por código malo. Fracasó por decisiones de arquitectura y coordinación que nunca se tomaron.

---

## La conexión con la clase de hoy

Todo lo que se definió en esta clase —la estructura de carpetas, los namespaces, el `.env`, el documento de decisiones, el modelo de usuario antes de la primera migración— son exactamente las decisiones que no existieron en los proyectos que fracasan.

No es código avanzado. Es orden, claridad y documentación antes de arrancar.

El CHAOS Report lleva treinta años midiendo esto. Los números no mejoraron dramáticamente en tres décadas. No porque los desarrolladores sean peores. Sino porque el problema nunca fue el código.

---

---

# Deuda técnica: el costo invisible de las malas decisiones

---

> _"Toda decisión técnica que se posterga tiene un precio. La deuda técnica es ese precio, y se cobra con intereses."_

---

## La analogía del dinero prestado

El término "deuda técnica" fue acuñado en 1992 por Ward Cunningham, uno de los creadores del movimiento Agile. Y la analogía que eligió es perfecta:

Cuando un banco presta dinero, el que lo recibió puede usarlo para crecer más rápido de lo que hubiera podido sin ese dinero. Pero tiene que devolver el capital más los intereses. Si nunca paga la deuda, los intereses se acumulan hasta que la deuda se vuelve impagable.

En software pasa exactamente lo mismo.

Cuando un equipo decide "esto lo hacemos bien después" o "por ahora lo dejamos así porque hay que entregar", está contrayendo una deuda. Avanza más rápido hoy. Pero esa decisión simplificada —ese atajo— tiene un costo que se paga después con tiempo extra, bugs, reuniones para entender código confuso, y desarrolladores que tardan el doble porque nadie sabe cómo funciona eso que "lo dejamos para después".

---

## Los dos tipos de deuda técnica

No toda deuda técnica es igual. Hay que distinguirlas porque tienen causas distintas y soluciones distintas.

**Deuda técnica intencional**

Es la que se contrae conscientemente y con criterio. El equipo dice: "sabemos que esto no está bien hecho, pero el lanzamiento es en dos semanas y después lo refactorizamos." Lo documentan, lo registran, lo planifican.

Esta deuda puede ser estratégica. Hay momentos en que moverse rápido vale más que moverse perfecto. Un MVP que valida en tres meses si la idea funciona puede salir con deuda técnica controlada.

**Deuda técnica accidental**

Es la que nadie decidió contraer. Aparece porque el equipo no sabía hacerlo mejor. Porque no se documentó nada. Porque los requisitos cambiaron y el código no se actualizó. Porque alguien se fue y nadie entendió lo que dejó.

Esta deuda es la más peligrosa. No se controla porque nadie la registró. Crece sola.

---

## Los síntomas de la deuda técnica acumulada

Cuando la deuda técnica llega a un nivel crítico, el proyecto empieza a mostrar señales claras:

- **Velocidad en caída libre.** Al inicio, el equipo entregaba funcionalidades en días. Ahora una funcionalidad simple tarda semanas porque cada cambio rompe algo en otro lado.
- **Miedo a tocar el código.** Nadie quiere modificar ciertas partes del sistema porque "funciona y no se sabe por qué". Si se toca, explota algo.
- **Bugs que vuelven.** Se corrige un bug, aparece otro. El sistema está tan frágil que cada corrección genera una nueva rotura.
- **Incorporar alguien nuevo tarda meses.** No hay documentación. El código no se explica solo. El nuevo desarrollador necesita semanas solo para entender qué hace qué.
- **El equipo habla de "reescribirlo todo" constantemente.** Cuando el equipo llega a ese punto, la deuda técnica ganó.

---

## Los números de la deuda técnica hoy

McKinsey, en sus investigaciones más recientes sobre tecnología empresarial, cuantificó el impacto de la deuda técnica con datos que actualizó en 2024:

> La deuda técnica representa entre el **20% y el 40% del valor total** del inventario tecnológico de las organizaciones relevadas. Los CIOs estiman que entre el **10% y el 20% del presupuesto destinado a nuevos productos** se redirige a resolver problemas generados por deuda técnica existente.
> _(McKinsey Digital, "Demystifying digital dark matter", datos actualizados a 2024)_

En términos prácticos: **uno de cada cuatro dólares invertidos en tecnología no genera valor nuevo** — se gasta en mantener, reparar o compensar decisiones pasadas.

Un análisis de Gartner de 2025 proyecta que para 2027, **el 75% de las organizaciones enfrentará fallos sistémicos causados por deuda técnica no gestionada**.

Y desde la perspectiva del desarrollador: investigaciones recientes indican que los programadores dedican entre el **33% y el 42% de su tiempo de trabajo** a lidiar con deuda técnica — mantenimiento de código heredado, corrección de bugs y refactorización de atajos tomados en el pasado. Eso significa que casi **un día completo por semana** no se destina a construir funcionalidades nuevas.

---

## La conexión con la arquitectura

La deuda técnica no se elimina del todo. Siempre habrá. Pero hay una diferencia enorme entre un proyecto que la gestiona y uno que la ignora.

Todo lo que se definió esta tarde en el documento de decisiones es una inversión para reducir la deuda técnica futura:

- **Nomenclatura consistente:** dentro de seis meses, cualquier persona entiende el código sin preguntar.
- **Variables de entorno desde el inicio:** no hay que refactorizar después con el riesgo de exponer secretos.
- **AbstractUser antes de la primera migración:** no hay que hacer una cirugía de base de datos con datos reales.
- **Namespaces en URLs:** no hay que buscar en cincuenta plantillas cuál link está roto después de cambiar una ruta.

Cada decisión que se pospone es deuda. Cada decisión que se toma bien desde el inicio es capital ahorrado para el futuro.

---

## La frase para recordar

> _"La deuda técnica es como la grasa corporal. Un poco es normal y hasta saludable. Demasiada te impide moverte."_

---

---

# Cómo trabaja la industria real

---

> _"Lo que se aprende en un curso es el qué y el cómo. Lo que solo se aprende trabajando es el ritmo, la cultura, y la forma en que los proyectos se organizan. Este bloque es un adelanto de eso."_

---

## El día a día que nadie muestra en los tutoriales

En los tutoriales de YouTube, un desarrollador abre el editor, escribe código durante veinte minutos y todo funciona. En la industria real, el trabajo de un desarrollador incluye mucho más que escribir código.

El Stack Overflow Developer Survey de 2024, con más de 65.000 desarrolladores encuestados en todo el mundo, muestra que el 61% de los desarrolladores pasa más de 30 minutos diarios buscando respuestas a problemas que encuentra en su trabajo. Investigaciones complementarias del mismo período estiman que el tiempo real dedicado a escribir código nuevo no supera el 35-40% de la jornada laboral.

El resto se distribuye entre depuración, reuniones, documentación, code review y comunicación.

Casi **un tercio del trabajo** no tiene nada que ver con escribir código.
_(Stack Overflow Developer Survey, 2024)_

---

## Cómo se organiza el trabajo: Agile y Scrum

La mayoría de las empresas de software que contratan hoy trabajan con alguna variante de **metodologías ágiles**. El método más popular se llama **Scrum**.

La idea central es simple: en lugar de planificar todo el proyecto por adelantado (lo que raramente funciona), el trabajo se divide en ciclos cortos —típicamente de dos semanas— llamados **sprints**.

**Cómo funciona un sprint:**

En cada sprint, el equipo elige un conjunto de tareas del backlog de funcionalidades que puede completar en esas dos semanas. Al final del sprint, se entrega algo funcionando —aunque sea pequeño— para que el cliente lo vea y dé feedback.

Esto resuelve uno de los problemas más grandes de la industria: que el cliente no sepa exactamente lo que quiere hasta que lo ve funcionando. Con sprints cortos, el feedback llega rápido y los errores de interpretación se corrigen antes de que sean costosos.

El mismo CHAOS Report del Standish Group en su edición 2024 mantiene la misma conclusión que viene confirmando desde hace años:

> Los proyectos ágiles son **2,5 veces más probables de tener éxito** que los proyectos en cascada en sectores dinámicos como tecnología, finanzas y salud.
> _(Standish Group CHAOS Report, 2024)_

---

## Las reuniones que todo desarrollador va a tener

**Daily standup (o daily)**

Una reunión de quince minutos, todos los días, de pie. Cada persona del equipo responde tres preguntas:

1. ¿Qué hice ayer?
2. ¿Qué voy a hacer hoy?
3. ¿Hay algo que me está bloqueando?

El objetivo no es rendir cuentas. Es sincronizar al equipo y detectar bloqueos antes de que se vuelvan problemas.

**Sprint planning**

Al inicio de cada sprint, el equipo se junta para decidir qué tareas va a abordar en las próximas dos semanas, cómo se estiman en esfuerzo, y quién toma cada una.

**Sprint retrospectiva**

Al final del sprint, el equipo se junta para responder: ¿qué salió bien? ¿qué salió mal? ¿qué cambiamos para el próximo sprint? Es el mecanismo de mejora continua del equipo.

---

## Code review: el proceso que diferencia equipos maduros

Cuando un desarrollador termina una tarea, no va directo a producción. El código pasa por una **revisión** —code review— donde uno o más compañeros leen lo que se escribió y dan feedback.

El objetivo no es encontrar errores (aunque también los encuentra). El objetivo principal es que el conocimiento se distribuya en el equipo. Si solo una persona sabe cómo funciona algo crítico y se va, ese conocimiento se va con ella.

Un code review típico revisa:

- ¿El código hace lo que dice que hace?
- ¿Se puede leer y entender sin explicaciones?
- ¿Sigue las convenciones del proyecto?
- ¿Hay casos extremos que no se consideraron?
- ¿Podría romperse algo ya existente?

---

## Git en el trabajo real: ramas y flujo

En el trabajo individual, git se usa casi siempre en una sola rama. En un equipo, eso es imposible. Si todos trabajan en la misma rama al mismo tiempo, los conflictos son constantes.

El flujo más común en equipos pequeños y medianos:

- **`main`** — solo tiene código que ya está en producción. Nunca se trabaja directamente aquí.
- **`develop`** — rama de integración. El código aprobado se integra aquí antes de pasar a producción.
- **`feature/nombre-de-la-funcionalidad`** — cada nueva funcionalidad tiene su propia rama. Cuando está lista, se crea un Pull Request para que el equipo la revise y la merezca con `develop`.

Este sistema se llama **Git Flow** y es el estándar en la mayoría de los equipos.

---

## Lo que los empleadores miran más allá del código

El informe de LinkedIn sobre el mercado laboral tecnológico de 2025 señala que las habilidades técnicas son condición de entrada, pero lo que diferencia a los candidatos dentro de ese universo son las habilidades no técnicas:

- **Comunicación**: explicar qué se está haciendo y por qué, sin jerga técnica innecesaria.
- **Autonomía**: resolver bloqueos sin necesitar que alguien indique cada paso.
- **Documentación**: dejar el código en un estado que cualquiera pueda continuar.
- **Actitud hacia el feedback**: recibir una corrección como información útil, no como crítica personal.

_(LinkedIn Jobs on the Rise & Talent Solutions Report, 2025)_

---

## El cierre

Todo lo que se aprende en un curso de desarrollo web —Django, SQL, git, arquitectura— es el lenguaje con el que se participa en la industria. Pero la industria tiene su propia cultura, su propio ritmo, y sus propias formas de organizarse.

La buena noticia: esa cultura no es exclusiva ni misteriosa. Se aprende. Y el primer paso para aprenderla es saber que existe.

---

> _"El código que escribes hoy lo va a leer alguien mañana. Ese alguien puede ser otra persona del equipo. Puede ser el cliente. Puede ser una IA. O puedes ser tú mismo en seis meses, sin recordar nada de lo que pensabas cuando lo escribiste. Escribir bien, documentar bien, y tomar buenas decisiones no es ser perfeccionista. Es ser profesional."_

---
