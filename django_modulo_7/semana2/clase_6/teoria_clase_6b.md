# 🤖 Módulo 7 — Clase 6b

## El Desarrollador Aumentado: Tu Rol en la Era de los Agentes de IA

> **AE 7.4** — Utiliza migraciones para la propagación de cambios al esquema de base de datos acorde al framework Django.
>
> ⚠️ Esta clase es 100% teórica y motivacional. Cierra la semana conectando todo lo aprendido con la realidad actual de la industria.

---

## 🗺️ Índice

| #     | Tema                                                           |
| ----- | -------------------------------------------------------------- |
| **1** | Lo que Está Pasando Ahora Mismo (No en el Futuro — AHORA)      |
| 1.1   | Los Números que Nadie les va a Mostrar en Otro Curso           |
| **2** | ¿Qué Están Haciendo las Grandes Empresas?                      |
| 2.1   | Microsoft                                                      |
| 2.2   | Google                                                         |
| 2.3   | Amazon                                                         |
| 2.4   | Meta (Facebook)                                                |
| 2.5   | Shopify — El caso más radical                                  |
| **3** | Las Empresas ya lo Exigen: No es Opcional                      |
| **4** | Entonces... ¿Para Qué Aprendimos Django?                       |
| **5** | Los 5 Errores que la IA Comete (y que Solo Tú Puedes Detectar) |
| **6** | Las 5 Preguntas Antes de Cualquier Modelo (Tu Arma Secreta)    |
| **7** | El Nuevo Perfil Profesional: De Programador a Arquitecto de IA |
| **8** | El Método P.I.D.E. — Cómo Orquestar Agentes de IA              |
| **9** | El Cierre: Lo que Realmente Aprendieron en Este Módulo         |

---

---

> _"La pregunta ya no es si la IA va a escribir código. La pregunta es: ¿quién va a verificar que ese código no destruya tu base de datos un viernes a las 6 de la tarde?"_

---

---

# 📊 1. Lo que Está Pasando Ahora Mismo (No en el Futuro — AHORA)

Mientras ustedes aprendían `ManyToManyField`, `prefetch_related` y migraciones en este módulo, el mundo de la programación cambió. No cambió un poco. Cambió **radicalmente**.

Pero antes de que les muestre los números, déjenme contarles una historia.

### 🎬 La Historia de Cursor

En 2023, cuatro estudiantes del **MIT** (sí, estudiantes, no una empresa gigante) decidieron crear un editor de código con IA integrada. Lo llamaron **Cursor**. La industria se rió: "Ya existe Copilot, ¿para qué otro más?"

Para noviembre de 2025 — apenas dos años después — Cursor superó los **$1.000 millones de ingresos anuales**. Más de la mitad de las Fortune 500 lo usa. Superaron a GitHub Copilot en satisfacción de usuario por 15 puntos.

**Cuatro estudiantes. Dos años. Mil millones de dólares.**

Eso les dice la velocidad a la que se mueve esta industria. Ahora sí, miren los números:

---

## 1.1 Los Números que Nadie les va a Mostrar en Otro Curso

| Dato                                                                                                 | Fuente                           | Año      |
| ---------------------------------------------------------------------------------------------------- | -------------------------------- | -------- |
| **El 90%** de las empresas Fortune 100 ya usan GitHub Copilot                                        | GitHub Blog                      | 2025     |
| **El 84%** de los desarrolladores ya usan o planean usar herramientas de IA para programar           | Stack Overflow Developer Survey  | 2025     |
| **El 41%** del código mundial está siendo generado por IA                                            | Netcorp Software Development     | 2026     |
| **El 46%** del código que escriben los usuarios de Copilot es generado por IA                        | GitHub / Quantumrun              | 2025     |
| GitHub Copilot superó los **20 millones de usuarios**                                                | GitHub Blog                      | Jul 2025 |
| Cursor (editor con IA) superó **$1.000 millones** de ingresos anuales                                | GetPanto / Informes financieros  | Nov 2025 |
| **Más de la mitad** de las Fortune 500 ya usan Cursor                                                | GetPanto                         | 2025     |
| **El 90%** de los equipos de ingeniería usan asistentes de IA (vs 61% el año anterior)               | Grow Fast Research               | Oct 2025 |
| Los desarrolladores que usan IA diariamente fusionan **60% más Pull Requests**                       | GitHub Research                  | 2025     |
| **Google** reportó que el **25%** de su código ya es asistido por IA                                 | Google / Sundar Pichai           | 2025     |
| **Microsoft**: entre el **20-30%** del código en sus repositorios es generado por IA                 | ITPro / Microsoft                | 2025     |
| El % de **desarrolladores que usan IA a diario** pasó del 18% (2024) al 41% (2025) al **73%** (2026) | ByteIota Research                | 2024-26  |
| El mercado de agentes de IA alcanzará **$52.620 millones** para 2030 (CAGR 46,3%)                    | Towards AI / Análisis de mercado | 2025     |

Lean esa tabla de nuevo. **El 41% del código del mundo lo está escribiendo IA.** No en un laboratorio. En producción. En las apps que ustedes usan todos los días.

> 💡 **Para ponerlo en perspectiva (% del código en producción escrito por IA):** Antes de que ustedes empezaran este programa de formación, el código generado por IA en producción era del 22%. Cuando arrancaron en diciembre de 2025, ya había subido a 27%. Hoy, apenas unos meses después, es 41%. La curva no es lineal — es exponencial.

---

---

# 🏢 2. ¿Qué Están Haciendo las Grandes Empresas?

Esto no es ciencia ficción. Y para que no piensen que estoy exagerando, voy a contarles qué están haciendo las empresas más grandes del planeta **hoy mismo**, mientras ustedes se sientan en esta clase:

---

## 2.1 🟦 Microsoft

- GitHub Copilot evolucionó de "autocompletar código" a un **agente autónomo** que puede resolver bugs, desarrollar features completas y generar Pull Requests solo.
- Más de **15 millones** de asientos pagos de Microsoft 365 Copilot (finales 2025).
- **4,7 millones** de suscriptores pagos de GitHub Copilot.
- En Build 2025 anunciaron la visión de una **"web agéntica abierta"**: agentes de IA que interactúan entre sí a través de internet.
- Windows 11 integró el **Model Context Protocol (MCP)** para que agentes de IA interactúen con aplicaciones nativas del sistema operativo.

---

## 2.2 🟢 Google

- Lanzó el **ADK (Agent Development Kit)** — un framework open-source en Python para crear agentes de IA que razonan, usan herramientas y toman acciones en el mundo real.
- Su reporte de tendencias 2026 predice que el **80% de las aplicaciones empresariales** tendrán agentes de IA integrados.
- Creó el protocolo **Agent2Agent (A2A)** para que agentes de diferentes empresas puedan colaborar entre sí — como un "internet de agentes".
- Los sistemas multi-agente (donde múltiples agentes especializados colaboran coordinados por un orquestador) se están convirtiendo en el nuevo estándar.

---

## 2.3 🟠 Amazon

- Obligó a sus propios desarrolladores a usar su asistente de IA **Kiro**, con un objetivo de **80% de uso semanal**. No es una sugerencia — es un **OKR corporativo** que se mide.
- Su herramienta **Q Developer** evolucionó a un agente capaz de planificar, ejecutar y depurar código de forma autónoma, incluyendo operaciones de archivos y ejecución de comandos.
- Lanzó **Bedrock AgentCore** en AWS para que empresas creen agentes de IA para tareas complejas de principio a fin.

### 💥 La Historia que Amazon No Quiere que Cuentes

A finales de 2025, un agente de IA de Amazon causó una **caída de servicio en AWS**. Sí, leyeron bien: un robot que escribe código tumbó parte de la infraestructura cloud más grande del mundo.

¿La respuesta de Amazon? No fue "dejemos de usar IA". Fue: implementaron **reglas de supervisión obligatorias** — cada cambio de código generado por IA en sistemas críticos ahora requiere revisión de **al menos dos ingenieros humanos**, y los juniors necesitan aprobación de un senior.

Esa historia les enseña dos cosas:

1. Los agentes de IA **ya están en producción real**, con consecuencias reales.
2. **Saber revisar código** se volvió más importante que saber escribirlo.

---

## 2.4 🔵 Meta (Facebook)

- Adquirió **Manus**, una tecnología de agentes autónomos (finales 2025).
- Compró **Moltbook**, una red social para que agentes de IA interactúen entre sí (2026).
- Mark Zuckerberg anunció que Meta planea entregar **"superinteligencia personal"** a los consumidores en 2026.
- Está desplegando agentes de IA para automatizar funciones de marketing: creación de anuncios, optimización de campañas y herramientas de compra agénticas.

---

## 2.5 🟡 Shopify — El Caso Más Radical

El CEO de Shopify, Tobi Lütke, emitió un memo interno en abril de 2025 que sacudió a toda la industria:

> _"Antes de pedir más personal o recursos, los equipos deben demostrar por qué la tarea NO puede ser realizada usando IA."_

Esto significa que en Shopify:

- **No puedes contratar gente nueva** si no demuestras primero que la IA no puede hacer ese trabajo.
- El **uso de IA es parte de las evaluaciones de desempeño** y revisiones de pares.
- Todos los empleados, desde juniors hasta directores, tienen la obligación de usar IA como "compañero de trabajo".
- Proveen herramientas como Copilot, Cursor, Claude Code y su propio `chat.shopify.io`.

---

> 💡 **Dato de Gartner (2026):** El **40% de las aplicaciones empresariales** tendrán agentes de IA integrados para fin de 2026. En 2025, ese número era menos del 5%. Pasamos del 5% al 40% en **un año**.

> 💡 **Dato de Gartner (predicción):** Para 2026, el **75% de las empresas** integrarán agentes de IA en sus flujos de trabajo e interacciones con clientes.

### 🤯 La Paradoja que Nadie Habla

Aquí viene lo más loco de todo. Presten atención a estos dos datos juntos:

- **El 84%** de los desarrolladores ya usan IA para programar.
- Pero solo el **29%** confía en lo que la IA genera.

Lean eso de nuevo. **8 de cada 10 programadores usan IA, pero solo 3 de cada 10 confían en ella.** ¿Entonces por qué la usan? Porque es **rápida**. Pero saben que lo que genera necesita revisión humana.

¿Y saben qué pasa con el 40-62% del código generado por IA? Contiene **fallos potenciales** según múltiples investigaciones (ByteIota, 2026).

Eso significa que **la habilidad más valiosa del futuro no es escribir código — es saber leerlo y detectar cuándo está mal.** Y eso es exactamente lo que aprendieron en este módulo.

---

---

# 📋 3. Las Empresas ya lo Exigen: No es Opcional

---

Esto ya no es una tendencia. Es una **exigencia corporativa**. Cada vez más empresas están pasando de "recomendamos usar IA" a **"es obligatorio usar IA"**:

| Empresa         | Política                                                                                            | Año  |
| --------------- | --------------------------------------------------------------------------------------------------- | ---- |
| **Amazon**      | Memo interno: 80% de uso semanal obligatorio de Kiro (su IA). Es un OKR corporativo rastreado.      | 2025 |
| **Shopify**     | Los equipos deben probar que la IA NO puede hacer una tarea antes de pedir contratación.            | 2025 |
| **Google**      | 25% de su código ya es asistido por IA. El ADK permite crear agentes internos en Python.            | 2025 |
| **Microsoft**   | 20-30% del código en sus repositorios es generado por IA. Copilot obligatorio en flujos internos.   | 2025 |
| **Oracle**      | Reestructuración de equipos para adoptar IA. Equipos más pequeños y ágiles potenciados por agentes. | 2025 |
| **SentinelOne** | GitHub Copilot desplegado a TODOS los desarrolladores. ChatGPT para desarrolladores clave.          | 2024 |

### 🧑‍💼 El Nuevo Estándar de Contratación

Además de exigir IA internamente, las empresas están cambiando **cómo contratan**:

- Para finales de 2026, se proyecta que las empresas evalúen **"habilidades de colaboración con IA"** en vez de memorización de sintaxis (Dev.to, 2025).
- Está emergiendo un nuevo rol llamado **"AI-First Developer"**: 80% del tiempo dirigiendo agentes de IA, 20% escribiendo lógica crítica (Dev.to, 2025).
- Se proyecta que los juniors **dejen de escribir código boilerplate** por completo, delegándolo a agentes (Intelligent Tools, 2025).

> ⚠️ **El mensaje es claro:** Saber programar sin saber usar IA será como saber escribir a mano pero no saber usar un procesador de texto. No estás mal, pero estás en desventaja.

---

---

# 🧠 4. Entonces... ¿Para Qué Aprendimos Django?

---

Esta es la pregunta que probablemente se están haciendo. Si la IA escribe código, ¿para qué aprender `ForeignKey`, `on_delete`, `select_related`, `makemigrations`?

La respuesta es simple y brutal:

> **La IA genera código. Pero genera código MALO si nadie la supervisa.**

No malo en el sentido de que no funciona. Malo en el sentido de que **funciona hoy y destruye tu empresa mañana**.

Algunos datos que respaldan esto:

- El **46% de los desarrolladores** desconfían de las salidas de la IA (2025).
- El **48%** suben datos sensibles a herramientas públicas de IA sin pensarlo.
- Las organizaciones que escalan IA exitosamente tienen **procesos bien estructurados de supervisión y validación** — no simplemente dejan que la IA haga todo.

La productividad con IA **se estanca** si no hay conocimiento humano detrás. Los equipos más exitosos no son los que usan más IA, sino los que **saben cuándo la IA se equivoca**.

---

---

# ❌ 5. Los 5 Errores que la IA Comete (y que Solo Tú Puedes Detectar)

---

Estos son errores reales que las herramientas de IA generan constantemente al escribir Django. Sin los conocimientos de este módulo, **no los verías**:

---

## ❌ Error 1: `on_delete=models.CASCADE` en todo

```python
# Lo que la IA genera:
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
```

**¿Por qué es peligroso?** Si alguien borra un cliente, se borran TODAS sus facturas. Eso es ilegal en muchos países (las facturas fiscales deben conservarse). Un `PROTECT` o `SET_NULL` sería lo correcto.

**Lo que aprendiste en la Clase 4:** Las 5 opciones de `on_delete` y cuándo usar cada una.

---

## ❌ Error 2: No usar `select_related` ni `prefetch_related`

```python
# Lo que la IA genera en una vista:
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista.html', {'pedidos': pedidos})
```

**¿Por qué es peligroso?** Funciona perfecto con 10 pedidos. Con 10.000 pedidos hace **10.001 queries SQL**. La app se cae en producción.

**Lo que aprendiste en la Clase 5:** `select_related` y `prefetch_related` resuelven esto con 1-2 consultas.

---

## ❌ Error 3: `ManyToMany` sin `through` cuando hay datos propios

```python
# Lo que la IA genera:
class Pedido(models.Model):
    productos = models.ManyToManyField(Producto)
```

**¿Por qué es peligroso?** No puedes guardar la cantidad, el precio unitario ni la fecha de cada producto en el pedido. Cuando el negocio pregunte "¿cuántos vendimos de cada uno?", no hay respuesta.

**Lo que aprendiste en la Clase 5:** El modelo `through` con `ItemPedido`.

---

## ❌ Error 4: Agregar un campo nuevo sin `default` ni `null=True`

```python
# Lo que la IA genera cuando le pides agregar un campo:
class Cliente(models.Model):
    nombre   = models.CharField(max_length=100)
    email    = models.EmailField()
    telefono = models.CharField(max_length=15)  # ← Sin default
```

**¿Por qué es peligroso?** La IA no sabe que ya hay 500 clientes en la base de datos sin teléfono. Al ejecutar `makemigrations`, Django pregunta: "¿qué valor le pongo a los registros existentes?" Si elegimos mal o la IA elige por nosotros, podemos corromper datos.

**Lo que aprendiste en la Clase 6:** Siempre `default=''` o `null=True` en campos nuevos. Y siempre revisar con `sqlmigrate` antes de aplicar.

---

## ❌ Error 5: Modificar una migración que ya fue aplicada

La IA a veces sugiere editar directamente el archivo `0002_cliente_telefono.py` para "arreglar" algo.

**¿Por qué es peligroso?** Esa migración ya fue aplicada. Ya está en la tabla `django_migrations`. Si la modificas, tu base de datos y tu código quedan desincronizados. Cuando alguien del equipo ejecute `migrate`, sus datos serán distintos a los tuyos.

**Lo que aprendiste en la Clase 6:** NUNCA modifiques una migración ya aplicada. Crea una nueva. Y usa `showmigrations` para diagnosticar el estado real.

---

> 🎯 **El patrón es claro:** La IA genera código que **funciona en el momento** pero que **falla en escala, en mantenimiento y en legalidad**. Los conocimientos de este módulo son exactamente lo que necesitas para detectar esos fallos.

---

---

# 🛡️ 6. Las 5 Preguntas Antes de Cualquier Modelo (Tu Arma Secreta)

---

Esto es algo que NO van a encontrar en ningún tutorial. Es un framework de pensamiento que usan los equipos senior antes de aprobar cualquier modelo en un Pull Request:

> **Antes de dar por terminado un modelo Django — ya sea que lo escribiste tú o lo generó una IA — pásalo por estas 5 preguntas:**

---

### 🗑️ 1. "¿Qué se rompe si se borra este dato?"

→ Revisa tu `on_delete`. ¿`CASCADE` realmente tiene sentido? ¿O deberías usar `PROTECT`, `SET_NULL` o `SET_DEFAULT`?

---

### 🔄 2. "¿Puede existir duplicado?"

→ ¿Necesitas `unique=True`? ¿`unique_together`? Un email duplicado puede significar dos cuentas para la misma persona. Una factura duplicada puede significar un cobro doble.

---

### 📈 3. "¿Y si esto crece x1000?"

→ ¿Hay índices en los campos que se filtran? ¿Las vistas usan `select_related` o `prefetch_related`? Un modelo que funciona con 50 registros puede destruir tu servidor con 50.000.

---

### 🤖 4. "¿Un agente de IA escribiría esto igual?"

→ Si la respuesta es "sí, exactamente igual", probablemente le falta contexto de negocio. La IA no sabe que en tu país las facturas no se pueden borrar, o que tu cliente necesita que "cantidad" nunca sea menor a 1. **Tu valor es el conocimiento del dominio.**

---

### 👀 5. "¿Alguien entiende esto sin leer el código?"

→ ¿Tiene `__str__`? ¿Tiene `verbose_name`? ¿Los `related_name` son descriptivos? El código se escribe una vez y se lee cien veces. Hazlo legible.

---

---

# 🚀 7. El Nuevo Perfil Profesional: De Programador a Arquitecto de Agentes

---

La industria está haciendo una transición clara. Miren esta evolución:

```
2020: "Necesito un programador que escriba código"

2023: "Necesito un programador que escriba código Y use IA para ir más rápido"

2025: "Necesito alguien que sepa DIRIGIR a la IA y verificar lo que produce"

2026: "Necesito un arquitecto que orqueste múltiples agentes de IA,
       diseñe los sistemas, y garantice que todo funcione correctamente"
```

---

### ¿Qué significa esto para ustedes?

| Habilidad del Pasado                | Habilidad del Presente y Futuro                             |
| ----------------------------------- | ----------------------------------------------------------- |
| Memorizar sintaxis de Django        | Entender **por qué** se usa cada herramienta                |
| Escribir todo el código manualmente | Saber **qué pedirle** a la IA y **verificar** el resultado  |
| Seguir tutoriales paso a paso       | Traducir **necesidades del negocio** a arquitectura técnica |
| Copiar y pegar de Stack Overflow    | Diseñar sistemas que **escalen** y sean **mantenibles**     |
| Saber un solo framework             | Entender **principios** que aplican en cualquier tecnología |

> 💡 **Dato clave:** Según investigaciones de 2025-2026, el rol de "desarrollador" está evolucionando hacia el de **"orquestador de IA"**. Esto no significa que programar sea irrelevante — significa que **programar es el piso mínimo**, no el techo.

---

### La Analogía del Director de Orquesta

Un director de orquesta no toca todos los instrumentos. Pero **sabe cuándo el violín suena mal**. Si no sabe música, no puede dirigir.

Lo mismo pasa con la IA:

- Si no sabes Django, no puedes validar si lo que generó Copilot está bien.
- Si no entiendes relaciones de base de datos, no puedes detectar un `CASCADE` peligroso.
- Si no conoces el problema N+1, no puedes explicar por qué la app se cae con carga real.

**Lo que aprendieron en este módulo no va a ser reemplazado por IA. Es lo que les permite controlar a la IA.**

Pero, ¿cómo se controla? ¿Hay un método? Sí. Y lo van a aprender ahora.

---

---

# 🎬 8. El Método P.I.D.E. — Cómo Orquestar Agentes de IA

---

Todo lo que hablamos suena bien: "orquestar agentes", "dirigir IA", "ser el arquitecto". Pero, ¿cómo se hace concretamente? ¿Hay un proceso?

Sí. Y curiosamente, **ya lo aprendieron en este módulo**. Solo que no sabían que lo estaban aprendiendo.

Se llama el **Método P.I.D.E.** — porque literalmente le "pides" a la IA, pero con estructura:

```
P  →  Planificar     (Descomponer el problema)
I  →  Instruir       (Dar contexto claro al agente)
D  →  Delegar        (Asignar cada tarea al agente correcto)
E  →  Evaluar        (Verificar con las 5 preguntas)
```

---

## 🗺️ P — Planificar (Descomponer como un Arquitecto)

Antes de tocar cualquier herramienta de IA, descompones el problema en piezas que **un humano entiende**. Exactamente como hacen con las Historias de Usuario:

> _"Necesito agregar un campo de 'dirección' al modelo Cliente y una vista que muestre los 5 productos más vendidos del mes."_

Lo descompones en:

- ¿Qué modelos necesito? → Sustantivos (Clase 5: Historias de Usuario)
- ¿Qué relaciones hay? → Flechas (Clase 5: M2M, through)
- ¿Qué query necesito? → QuerySet (Clase 5: prefetch_related)
- ¿Qué migración genera? → ¿El campo nuevo tiene default? (Clase 6: migraciones seguras)

**Conexión con Django:** Es el **Método de los 4 Pasos** de la Clase 5 combinado con el **flujo de migraciones** de la Clase 6. La misma técnica que usaron para traducir historias de usuario a código ahora la usan para planificar qué pedirle a la IA.

---

## 📋 I — Instruir (El Prompt es el Nuevo `urls.py`)

Así como una URL mal escrita lleva a un 404, **un prompt mal escrito lleva a código basura**. Instruir al agente significa darle 4 cosas:

1. **Contexto:** _"Estoy en un proyecto Django con estos modelos: Pedido, Producto, ItemPedido..."_
2. **Tarea específica:** _"Necesito una vista que muestre el top 5 de productos vendidos este mes."_
3. **Restricciones:** _"Debe usar `prefetch_related`. No uses `CASCADE` en facturas. Usa `through` para M2M."_
4. **Formato esperado:** _"Dame solo el código del view con comentarios explicativos."_

¿Ven el patrón? Las **restricciones** son exactamente los conocimientos de este módulo. Sin ellas, el agente genera código genérico. Con ellas, genera código profesional.

> 💡 **Regla de oro:** Cuanto más sabes de Django, mejores instrucciones le das a la IA. Cuanto mejores instrucciones, mejor código genera. **Tu conocimiento es el multiplicador.**

---

## 🤖 D — Delegar (Cada Agente es un "Modelo Especializado")

No le das todo a un solo agente. **Divides el trabajo** como se divide una app Django en archivos:

| Tarea             | Agente / Herramienta      | Analogía Django    |
| ----------------- | ------------------------- | ------------------ |
| Diseñar el modelo | Copilot / Cursor          | `models.py`        |
| Escribir la vista | Claude Code / Gemini      | `views.py`         |
| Generar los tests | Agente de testing         | `tests.py`         |
| Revisar seguridad | SonarCloud / Semgrep      | Middleware         |
| Documentar        | Agente de documentación   | `docstrings`       |
| Optimizar queries | Django Debug Toolbar + IA | `select_related()` |

**La clave:** Un agente no hace todo bien. Igual que un modelo no debería tener lógica de vista, **cada agente tiene su especialidad**. Darle todo a uno solo es como poner toda tu app en un solo archivo de 5000 líneas.

---

## ✅ E — Evaluar (Las 5 Preguntas como Code Review)

Aquí es donde el humano marca la diferencia. **Todo** lo que el agente genera pasa por las 5 preguntas de la sección anterior:

1. 🗑️ ¿Qué se rompe si se borra?
2. 🔄 ¿Puede existir duplicado?
3. 📈 ¿Y si crece x1000?
4. 🤖 ¿Le falta contexto de negocio?
5. 👀 ¿Alguien entiende esto sin leer el código?

Si alguna respuesta es "no", **vuelves a Instruir** con mejor contexto. El ciclo se repite hasta que el código pasa todas las preguntas.

---

## 🔁 El Ciclo Completo

```
    ┌──────────────────────────────────────┐
    │                                      │
    ▼                                      │
PLANIFICAR → INSTRUIR → DELEGAR → EVALUAR ─┘
                 ▲                    │
                 │  Si falla, vuelves │
                 │  con mejor contexto│
                 └────────────────────┘
```

> 🎯 **¿Por qué P.I.D.E. es poderoso?** Porque conecta todo lo que aprendieron en este módulo con el futuro de su carrera. **Planificar** es el Método de los 4 Pasos. **Instruir** es saber Django lo suficiente para dar restricciones. **Delegar** es entender que cada herramienta tiene su función. **Evaluar** es el checklist de las 5 Preguntas. No es un concepto nuevo — es la síntesis de todo el módulo.

---

---

# 🏁 9. El Cierre: Lo que Realmente Aprendieron en Este Módulo

---

Permítanme ser honesto con ustedes.

En este módulo les enseñé `ForeignKey`, `ManyToManyField`, `select_related`, `prefetch_related`, modelos intermedios con `through`, migraciones seguras con `makemigrations` y `migrate`, y a traducir historias de usuario en código Django. Todo eso es importante. Pero no es lo más importante que aprendieron.

**Lo más importante que aprendieron es a PENSAR como desarrolladores.**

- Cuando ven un modelo, ya no ven solo campos. Ven **relaciones, restricciones, y consecuencias**.
- Cuando ven una query, ya no ven solo código. Ven **viajes a la base de datos que pueden costar plata o tumbar un servidor**.
- Cuando ven una migración, ya no ven solo un archivo automático. Ven **el registro permanente de una decisión técnica** que afecta datos reales de personas reales.
- Cuando ven una historia de usuario, ya no ven solo texto. Ven **sustantivos que son modelos, verbos que son vistas, y flechas que son relaciones**.

Eso es exactamente lo que ninguna inteligencia artificial puede hacer por ustedes. La IA puede generar el código. Pero **ustedes deciden si ese código es correcto, seguro, escalable y apropiado para el negocio**.

En un mundo donde el 41% del código lo escribe IA, **el 100% de la responsabilidad sigue siendo humana**.

> _"Las herramientas cambian cada 2 años. Los principios duran toda la carrera."_

Ahora tienen ambos. Úsenlos bien. 🚀

---

---

## 🤖 10. Guía Rápida: ¿Qué IA Usar para Código?

No todas las IAs son iguales. Algunas son mejores para **generar código**, otras para **explicar conceptos**, y otras para **razonar sobre arquitectura**. Esta tabla les ayuda a elegir la herramienta correcta según la tarea.

### 🧠 Modelos de IA (el "cerebro")

| Modelo                | Empresa    | Benchmark Código       | Fortaleza Principal                                             | Ideal Para                                                     |
| --------------------- | ---------- | ---------------------- | --------------------------------------------------------------- | -------------------------------------------------------------- |
| **GPT-5.4**           | OpenAI     | LiveCodeBench ~89%     | Razonamiento configurable, uso nativo de computadora y terminal | Workflows agénticos, debugging con interacción de escritorio   |
| **GPT-5.2**           | OpenAI     | SWE-bench ~70%         | Líder en razonamiento abstracto, versátil                       | Tareas generales, planificación, arquitectura                  |
| **GPT-4o**            | OpenAI     | —                      | Rápido y multimodal (texto, imagen, audio)                      | Prototipos rápidos, explicaciones con código, pair programming |
| **Claude Opus 4.6**   | Anthropic  | SWE-bench 80.8%        | Contexto 1M tokens, código de altísima calidad                  | Refactoring masivo, analizar codebases de +25K líneas          |
| **Claude Sonnet 4.6** | Anthropic  | SWE-bench ~71%         | Equilibrio velocidad-calidad, excelente en código               | Desarrollo diario, Django/Python, pair programming             |
| **Gemini 3.1 Pro**    | Google     | ARC-AGI-2 77.1%        | Contexto 1M tokens, velocidad, integración Google Cloud         | Proyectos grandes, Firebase, Android, código con GCP           |
| **Gemini 2.5 Flash**  | Google     | —                      | Velocidad extrema con buena calidad                             | Autocompletado, respuestas rápidas, iteración veloz            |
| **DeepSeek V4**       | DeepSeek   | Compite con Claude/GPT | 1T parámetros MoE, "Engram Memory", open-source                 | Alternativa gratuita de nivel profesional, correr localmente   |
| **DeepSeek R1**       | DeepSeek   | —                      | Razonamiento paso a paso, open-source                           | Problemas algorítmicos, matemáticas, lógica compleja           |
| **Qwen 2.5 Coder**    | Alibaba    | —                      | Especializado 100% en código, open-source                       | Generación de código puro, completar funciones                 |
| **Mistral Large**     | Mistral AI | —                      | Multilingüe, buen código, open-weight                           | Proyectos en español, documentación bilingüe                   |
| **Llama 4**           | Meta       | —                      | Open-source potente, correable en GPU consumidor                | Privacidad total, sin conexión, experimentación local          |

### 🛠️ Herramientas de Desarrollo con IA (el "entorno")

| Herramienta            | Tipo            | Precio (USD/mes) | Fortaleza Principal                                      | Ideal Para                                                |
| ---------------------- | --------------- | ---------------- | -------------------------------------------------------- | --------------------------------------------------------- |
| **GitHub Copilot**     | Plugin IDE      | $10-39           | Autocompletado inline, Agent Mode, multi-modelo          | Escritura rápida en VS Code/JetBrains, equipos GitHub     |
| **Cursor**             | IDE completo    | $20              | Comprensión profunda del proyecto, edición multi-archivo | Desarrollo full-stack, refactoring complejo               |
| **Claude Code**        | Agente terminal | $20-100          | Agente autónomo, contexto 200K+, Git nativo              | Multi-file refactoring, debugging complejo desde terminal |
| **Codex CLI**          | Agente terminal | Incluido en Plus | Ejecuta código real, contexto del proyecto               | Automatización, scripts, tareas de DevOps                 |
| **Windsurf**           | IDE agéntico    | Gratis/Pro       | Alternativa a Cursor, agente estructurado                | Desarrollo agéntico con presupuesto limitado              |
| **Tabnine**            | Plugin IDE      | Gratis/Pro       | Privacidad extrema, deployment local                     | Empresas reguladas, datos sensibles                       |
| **Amazon Q Developer** | Plugin IDE      | Gratis           | Integración nativa con AWS                               | Equipos en ecosistema Amazon/AWS                          |
| **Gemini Code Assist** | Plugin IDE      | $20              | Integración Google Cloud, generación inline              | Equipos en ecosistema Google/GCP                          |

> 💡 **Consejo práctico:** No se casen con una sola IA. Los mejores desarrolladores en 2026 usan **2 o 3 herramientas** según la tarea:
>
> - **Copilot o Cursor** para escribir código en el IDE (velocidad)
> - **Claude Opus o GPT-5.4** para razonar sobre arquitectura y debugging complejo (profundidad)
> - **Gemini 3.1 Pro** para analizar proyectos enormes o documentación extensa (contexto)

> ⚠️ **Importante:** Los modelos cambian cada pocos meses. Esta tabla refleja el estado a **17 de marzo de 2026** con datos de SWE-bench, LiveCodeBench y ARC-AGI-2. Lo que NO cambia es el principio: **evalúen siempre el output con las 5 Preguntas del Checklist**.

---

---

## 📚 Referencias (APA 7ª ed.)

AnthropicTeam. (2025). _The evolution of AI coding agents_. Anthropic Research. https://www.anthropic.com/research

Bain & Company. (2025). _Technology report: The real impact of AI coding assistants on developer productivity_. https://www.bain.com/insights/technology-report-2025/

Benzinga. (2026, enero). Amazon implements new oversight rules for AI-assisted coding after service outages. _Benzinga_. https://www.benzinga.com/

ByteIota Research. (2026). _AI coding statistics 2026: Adoption, productivity, and trust gaps_. https://byteiota.com/ai-coding-statistics/

Forbes Technology Council. (2025). Amazon's AI coding mandate and the risks of AI-generated code in production. _Forbes_. https://www.forbes.com/

Gartner, Inc. (2025). _Predicts 2026: AI agents will transform 40% of enterprise applications_. https://www.gartner.com/en/articles/intelligent-agent-predictions

GitHub. (2025a). _GitHub Copilot surpasses 20 million users_. The GitHub Blog. https://github.blog/news-insights/

GitHub. (2025b). _Copilot generates an average of 46% of code for active developers_. GitHub Research. https://github.blog/news-insights/research/

GitHub. (2026, febrero). _Enterprise usage metrics for GitHub Copilot now generally available_. The GitHub Blog. https://github.blog/changelog/

Google. (2025). _25% of Google's code is now AI-assisted_ [Declaración de Sundar Pichai en earnings call Q1 2025]. Alphabet Investor Relations.

Google Cloud. (2026). _AI agent trends report 2026: From tools to teammates_. Google Blog. https://blog.google/technology/ai/

Grow Fast. (2025, octubre). _90% of engineering teams now use AI assistants — up from 61% in 2024_. https://grow-fast.co.uk/

ITPro. (2025). _Enterprise AI coding tools: How Ciena, SentinelOne, and Microsoft are deploying AI at scale_. https://www.itpro.com/

JetBrains. (2025). _Developer ecosystem survey 2025: 85% of developers regularly use AI tools_. https://www.jetbrains.com/lp/devecosystem-2025/

Lütke, T. (2025, abril). _Internal memo: AI expectations at Shopify_ [Publicado por Forbes y Entrepreneur]. https://www.forbes.com/sites/digital-assets/2025/04/shopify-ceo-ai-mandate/

Microsoft. (2025). _Microsoft Build 2025: Building the open agentic web_. https://build.microsoft.com/

Microsoft. (2025). _15 million paid seats for Microsoft 365 Copilot and 4.7 million GitHub Copilot subscribers_ [Earnings report Q4 FY2025]. Microsoft Investor Relations.

Netcorp Software Development. (2026). _AI code generation statistics 2026: 41% of worldwide code is now AI-generated_. https://netcorpsoftwaredevelopment.com/

Quantumrun Foresight. (2025). _GitHub Copilot statistics and enterprise adoption trends_. https://www.quantumrun.com/

Shift Magazine. (2026). _AI-authored code in production: 26.9% of merged code is AI-generated (Nov 2025 – Feb 2026)_. https://shiftmag.dev/

Stack Overflow. (2025). _Developer survey 2025: 84% of developers use or plan to use AI tools_. https://survey.stackoverflow.co/2025/

Towards AI. (2025). _AI agents market projected to reach $52.62 billion by 2030 (CAGR 46.3%)_. https://towardsai.net/

---
