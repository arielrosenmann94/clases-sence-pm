# 🔍 Módulo 7 — Clase 8b

## Debugging Profesional: La Habilidad que Separa Juniors de Seniors

> **Transversal** — Esta clase aplica a Python, Django, JavaScript, y cualquier lenguaje o tecnología que usen en su carrera.
>
> ⚠️ Esta clase es 100% teórica y metodológica. No es sobre una herramienta — es sobre un **proceso mental** que van a usar el resto de su vida profesional.

---

## 🗺️ Índice

| #      | Tema                                                         |
| ------ | ------------------------------------------------------------ |
| **1**  | La Verdad Incómoda: Los Seniors También Tienen Bugs          |
| **2**  | ¿Qué es Debugging? (La Definición que Nadie les Va a Dar)    |
| **3**  | El Método R.E.P.L.A. — La Receta de los 5 Pasos              |
| 3.1    | Paso 1 — Reproducir: "¿Puedo hacer que pase de nuevo?"       |
| 3.2    | Paso 2 — Examinar: "¿Qué me dice el error?"                  |
| 3.3    | Paso 3 — Proponer: "¿Cuál es mi hipótesis?"                  |
| 3.4    | Paso 4 — Limitar: "¿Dónde exactamente está el problema?"     |
| 3.5    | Paso 5 — Aplicar y Verificar: "¿Funcionó mi solución?"       |
| **4**  | Cómo Leer un Traceback (El Mapa del Tesoro)                  |
| **5**  | Cómo Buscar en Google como un Senior                         |
| **6**  | Rubber Duck Debugging: La Técnica Más Tonta (y Más Efectiva) |
| **7**  | Cómo Pedir Ayuda Sin que Te Odien                            |
| **8**  | Los 7 Errores de Debugging que Todos Cometen                 |
| **9**  | Checklist: La Receta Completa en Una Página                  |
| **10** | Tabla de Herramientas de Debugging                           |

---

---

> _"Debugging es como ser un detective en una novela policial donde tú también eres el asesino."_
>
> — Filipe Fortes, ingeniero de software

---

---

# 💡 1. La Verdad Incómoda: Los Seniors También Tienen Bugs

---

Antes de empezar, necesitan saber algo que nadie les dice:

**Los programadores senior NO escriben código sin errores.** Escriben código con errores y los encuentran más rápido.

La diferencia entre un junior y un senior no es la cantidad de bugs que producen. Es el **tiempo que tardan en resolverlos**.

| Métrica                              | Desarrollador Junior | Desarrollador Senior |
| :----------------------------------- | :------------------- | :------------------- |
| Tiempo promedio para resolver un bug | 2-4 horas            | 15-45 minutos        |
| ¿Cómo busca la solución?             | Cambia cosas al azar | Sigue un proceso     |
| ¿Lee el error completo?              | Rara vez             | Siempre              |
| ¿Cuántas pestañas de Google abre?    | 15+                  | 2-3 precisas         |
| ¿Documenta la solución?              | Nunca                | Casi siempre         |
| Reacción emocional ante un bug       | Pánico / frustración | Curiosidad           |

> 💡 **Dato de la industria:** Según un estudio de la Universidad de Cambridge, los desarrolladores pasan entre el **35% y el 50%** de su tiempo haciendo debugging. Es decir, si te pagan por programar 8 horas, entre 3 y 4 horas son de debugging. Es tu actividad principal. _(Cambridge University, 2013, "The Economic Cost of Poor Code Quality")_

### Y con IA... ¿se acabó el debugging?

No. De hecho, apareció un **nuevo tipo** de debugging:

| Dato                                                                                                                                                      | Fuente                               | Año  |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- | :--- |
| El **45%** de los desarrolladores dice que debuggear código generado por IA **toma más tiempo** que debuggear código propio                               | Stack Overflow Developer Survey      | 2025 |
| El **85%** de los desarrolladores ya usa herramientas de IA, pero solo **44%** del código que genera la IA es aceptado sin cambios                        | JetBrains Developer Ecosystem Survey | 2025 |
| Desarrolladores experimentados con herramientas de IA **tardaron un 19% más** en completar tareas, en parte por el tiempo de revisar y corregir el output | METR (estudio publicado en arXiv)    | 2025 |

> ⚠️ **La paradoja de 2026:** La IA genera código más rápido, pero ese código necesita revisión humana. Resultado: los desarrolladores ahora hacen debugging de **su propio código** Y del **código que generó la IA**. Saber debuggear es más importante que nunca.

La buena noticia: el debugging **se aprende**. No es un talento mágico. Es un proceso con pasos que se pueden seguir como una receta de cocina.

---

---

# 🔧 2. ¿Qué es Debugging? (La Definición que Nadie les Va a Dar)

---

**Debugging NO es:**

- Cambiar cosas al azar hasta que funcione
- Copiar y pegar código de Google sin entenderlo
- Borrar y reescribir todo desde cero
- Pedirle a alguien que lo arregle

**Debugging ES:**

- Un proceso **sistemático** para encontrar la causa de un problema
- **El método científico** aplicado al código

```
MÉTODO CIENTÍFICO                     DEBUGGING

1. Observar un fenómeno        →    1. Observar el error
2. Formular una hipótesis      →    2. "Creo que el bug está en..."
3. Diseñar un experimento      →    3. Agregar un print / poner un breakpoint
4. Analizar los resultados     →    4. "¿El valor es lo que esperaba?"
5. Confirmar o rechazar        →    5. "Sí era eso" / "No, descarto y pruebo otra cosa"
6. Documentar                  →    6. Anotar para no repetir el error
```

### 🧹 El Origen del Nombre

En 1947, la ingeniera **Grace Hopper** encontró una polilla (un _bug_ literal) atrapada dentro de un relé del computador Harvard Mark II. La pegó en su cuaderno de notas con la inscripción: _"Primer caso real de bug encontrado."_

Desde entonces, encontrar y resolver errores se llama **debugging** — literalmente _"sacar el bicho"_.

> 💡 **Lo más poderoso de esta definición:** Si debugging es el método científico, entonces **cualquiera puede hacerlo**. No necesitas ser un genio. Necesitas ser metódico.

---

---

# 🧪 3. El Método R.E.P.L.A. — La Receta de los 5 Pasos

---

Cada vez que se encuentren con un error — en Django, en Python, en JavaScript, en lo que sea — sigan estos 5 pasos **en orden**. No se salten ninguno.

```
R  →  Reproducir      "¿Puedo hacer que el error pase de nuevo?"
E  →  Examinar        "¿Qué información me da el error?"
P  →  Proponer        "¿Cuál es mi hipótesis de la causa?"
L  →  Limitar         "¿Dónde exactamente está el problema?"
A  →  Aplicar         "¿Funcionó mi solución? ¿Lo verifico?"
```

---

## 3.1 Paso 1 — Reproducir: "¿Puedo Hacer que Pase de Nuevo?"

---

### ¿Por qué es el primer paso?

Porque un error que no puedes reproducir es un error que no puedes resolver. Si no sabes **cómo provocar el error**, no puedes saber si tu solución lo arregló.

### ¿Qué hacer?

1. **Intentar que el error vuelva a pasar** exactamente igual.
2. Anotar los **pasos exactos** que hiciste antes de que apareciera.
3. Identificar si el error es **consistente** (siempre pasa) o **intermitente** (a veces sí, a veces no).

### La Analogía del Mecánico

Si llevas tu auto al mecánico y le dices "hace un ruido raro", lo primero que te pregunta es: **"¿Cuándo? ¿Al arrancar? ¿Al frenar? ¿En frío o en caliente?"**

No empieza a desarmar el motor. Primero necesita **escuchar el ruido él mismo**.

### Preguntas que debes responder

| Pregunta                                             | ¿Por qué importa?                                           |
| :--------------------------------------------------- | :---------------------------------------------------------- |
| ¿Qué pasos exactos seguiste antes del error?         | Sin esto, no puedes reproducirlo                            |
| ¿Siempre pasa o solo a veces?                        | Un error intermitente requiere más investigación            |
| ¿Pasaba antes o es nuevo?                            | Si es nuevo, ¿qué cambió desde que funcionaba?              |
| ¿Pasa solo con ciertos datos?                        | Puede ser un caso borde (un dato vacío, un número negativo) |
| ¿Pasa en tu máquina o también en la de un compañero? | Si solo pasa en la tuya, es un problema de entorno          |

> ⚠️ **Regla de oro:** Si no puedes reproducir el error, **no te pongas a cambiar código**. Primero reproduce. El 80% de los bugs que parecen "imposibles" se resuelven cuando logras reproducirlos de forma consistente.

### 🤔 "Pero si el error ya está ahí... ¿qué voy a reproducir?"

Buena pregunta. Muchos piensan: _"Ya veo el error en pantalla, ¿para qué voy a reproducirlo?"_

La respuesta: **porque necesitas saber los pasos exactos para provocarlo.** Y eso tiene 3 razones:

1. **Para verificar tu solución.** Si arreglas algo pero no puedes repetir los pasos originales, ¿cómo sabes que realmente se arregló y no fue coincidencia?
2. **Porque a veces el error que ves no es el error real.** Puede que veas un error de template, pero la causa real es un error en la base de datos. Si solo miras la pantalla, arreglas el síntoma, no la enfermedad.
3. **Porque los pasos importan.** ¿Pasa con cualquier dato o solo con datos específicos? ¿Pasa siempre o solo a veces? ¿Pasa después de hacer clic una vez o dos veces? Esos detalles cambian completamente la solución.

> 💡 **Analogía:** Si te duele la cabeza, el doctor no te opera inmediatamente. Primero pregunta: _"¿Cuándo empezó? ¿Después de comer? ¿Al levantarte? ¿Con luz o sin luz?"_ Eso es reproducir: entender las **condiciones exactas** del problema, no solo que el problema existe.

---

## 3.2 Paso 2 — Examinar: "¿Qué Me Dice el Error?"

---

### ¿Por qué es crítico?

Porque **el error casi siempre te dice qué pasó y dónde**. El problema es que la mayoría de los juniors no leen el mensaje completo. Ven rojo, entran en pánico, y empiezan a buscar en Google sin siquiera leer qué dice.

### ¿Qué hacer?

1. **Lee el mensaje de error COMPLETO.** No solo la primera línea. No solo la última. Todo.
2. **Identifica** las 3 piezas clave de todo error:
   - **Tipo de error:** ¿Qué categoría de problema es? (SyntaxError, NameError, ValueError...)
   - **Mensaje:** ¿Qué dice en palabras humanas?
   - **Ubicación:** ¿En qué archivo y en qué línea?
3. **Traduce** el mensaje técnico a español. Si no entiendes una palabra, búscala.

### Ejemplo real en Python

```
Traceback (most recent call last):
  File "/home/usuario/proyecto/wallet/views.py", line 23, in crear_cliente
    cliente = Cliente.objects.create(nombre=nombre, email=email)
  File "/home/usuario/.venv/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
django.db.utils.IntegrityError: UNIQUE constraint failed: wallet_cliente.email
```

| Pieza         | Qué dice el error                                | Qué significa en español                                    |
| :------------ | :----------------------------------------------- | :---------------------------------------------------------- |
| **Tipo**      | `IntegrityError`                                 | Error de integridad de la base de datos                     |
| **Mensaje**   | `UNIQUE constraint failed: wallet_cliente.email` | Intentaste guardar un email que ya existe                   |
| **Ubicación** | `wallet/views.py, line 23, in crear_cliente`     | El problema está en la línea 23 de tu vista `crear_cliente` |

Con solo **leer** el error ya sabemos: el problema es que estamos intentando crear un cliente con un email duplicado. No necesitamos buscar en Google. No necesitamos cambiar nada al azar. La solución es agregar una validación en el formulario o manejar la excepción.

> 💡 **Dato profesional:** El 60% de los bugs se resuelven en este paso. Solo leyendo. El mensaje de error generalmente te dice exactamente qué pasó. No lo ignores.

---

## 3.3 Paso 3 — Proponer: "¿Cuál es Mi Hipótesis?"

---

### ¿Por qué formular una hipótesis?

Porque sin hipótesis haces cambios al azar. Con hipótesis, cada cambio es **un experimento** con un resultado esperado. Si el resultado no es el que esperabas, aprendiste algo. Sin hipótesis, no aprendiste nada — solo tuviste suerte (o no).

### ¿Qué hacer?

1. Basándote en lo que observaste (Paso 2), formula UNA hipótesis concreta:
   - ❌ "Algo está roto" → demasiado vago
   - ✅ "Creo que el formulario no valida si el email ya existe antes de enviar"
2. Escribe tu hipótesis. Sí, **escríbela**. Aunque sea en un post-it. Esto te obliga a formularla con claridad.
3. Define qué **evidencia** confirmaría o descartaría tu hipótesis.

### La Analogía del Doctor

Cuando vas al médico con dolor de cabeza, el doctor no te opera inmediatamente. Hace preguntas, examina, y dice: _"Mi hipótesis es que es una migraña por estrés. Vamos a probar con ibuprofeno y descanso. Si no mejora en 48 horas, hacemos estudios."_

Eso es una hipótesis + un plan de verificación. Exactamente lo que debes hacer con un bug.

### Plantilla para tu hipótesis

```
HIPÓTESIS:  "Creo que el error ocurre porque ___________."
EVIDENCIA:  "Para confirmarlo, voy a ___________."
SI FUNCIONA: "El error desaparece / el valor cambia a ___________."
SI NO FUNCIONA: "Descarto esta hipótesis y pruebo ___________."
```

> ⚠️ **Error fatal:** Tener 5 hipótesis a la vez y cambiar 5 cosas al mismo tiempo. Si algo se arregla, no sabes cuál de los 5 cambios lo resolvió. Cambia **una sola cosa** por intento.

---

## 3.4 Paso 4 — Limitar: "¿Dónde Exactamente Está el Problema?"

---

### ¿Por qué limitar?

Porque un proyecto puede tener miles de líneas de código y el error está en UNA. Tu trabajo es llegar a esa línea. Cuanto más rápido reduzcas el área de búsqueda, más rápido encuentras el bug.

### Técnicas para limitar

---

### Técnica 1: Búsqueda Binaria (la más poderosa)

Imagina que tienes un cable de 100 metros y en algún punto está cortado. ¿Cómo lo encuentras?

- ❌ Revisas centímetro por centímetro desde el inicio (lento)
- ✅ Pruebas en la mitad (metro 50). ¿Funciona o no?
  - Si funciona hasta el 50 → el corte está entre el 50 y el 100
  - Pruebas en el metro 75...
  - En 7 pruebas revisaste 100 metros.

En código es igual:

```python
# Tienes una función de 50 líneas que falla.
# En vez de leerlas todas, pon un print en la mitad:

def procesar_pedido(pedido):
    # ... 25 líneas de código ...

    print("CHECKPOINT: llegué hasta aquí")  # ← ¿Aparece este print?

    # ... 25 líneas más de código ...
```

Si el print aparece → el error está en la segunda mitad.
Si NO aparece → el error está en la primera mitad.
Pones otro print en la mitad de esa mitad. Y así sucesivamente.

**En 4-5 prints encuentras el error en cualquier función, sin importar el tamaño.**

---

### Técnica 2: Print Debugging (la más simple)

```python
def calcular_total(pedido):
    items = pedido.items.all()
    print(f"DEBUG: items = {items}")            # ¿Qué contiene 'items'?
    print(f"DEBUG: cantidad de items = {len(items)}")  # ¿Cuántos hay?

    total = 0
    for item in items:
        subtotal = item.cantidad * item.precio
        print(f"DEBUG: {item.producto} → {item.cantidad} x {item.precio} = {subtotal}")
        total += subtotal

    print(f"DEBUG: total final = {total}")      # ¿Es lo que esperabas?
    return total
```

> ⚠️ **Regla:** Siempre pon un prefijo como `DEBUG:` o `>>>` en tus prints de debugging. Así los encuentras fácilmente para borrarlos después. Un print olvidado en producción puede imprimir datos sensibles.

---

### Técnica 3: Aislar el Problema

Si no puedes encontrarlo en el proyecto completo, **aísla** el código sospechoso:

1. Copia la función sospechosa a un archivo nuevo.
2. Córrela con datos de prueba simples.
3. ¿Funciona sola? → El problema no es la función, es lo que le llega.
4. ¿Falla sola? → Encontraste la función rota. Ahora aplica búsqueda binaria dentro.

---

## 3.5 Paso 5 — Aplicar y Verificar: "¿Funcionó Mi Solución?"

---

### ¿Qué hacer?

1. **Aplica** tu solución (un solo cambio por vez).
2. **Reproduce** el error original (los mismos pasos del Paso 1).
3. **Verifica** que ya no ocurra.
4. **Verifica** que no rompiste otra cosa (efectos secundarios).
5. **Limpia** los prints de debugging que hayas dejado.

### La Lista de Verificación Post-Fix

```
[ ] El error original ya no ocurre
[ ] Probé con los mismos datos que causaban el error
[ ] Probé con otros datos similares (¿funciona para casos normales?)
[ ] Probé con datos extremos (vacíos, nulos, muy grandes)
[ ] No rompí nada que funcionaba antes
[ ] Limpié todos los prints de debugging
[ ] Entiendo POR QUÉ mi solución funciona (no es solo suerte)
```

> ⚠️ **El error más peligroso:** Que tu solución "funcione" pero solo porque enmascaras el problema. Ejemplo: `try: ... except: pass` — esto no arregla nada, solo esconde el error. Es como tapar la luz del check engine del auto con cinta adhesiva.

---

---

# 📖 4. Cómo Leer un Traceback (El Mapa del Tesoro)

---

Los tracebacks de Python y Django se leen **de abajo hacia arriba**. La última línea es la más importante.

```
Traceback (most recent call last):                          ← INICIO (ignora esto por ahora)
  File "/home/user/proyecto/config/urls.py", line 5
    path('clientes/', include('wallet.urls')),              ← Paso 3: Django enruta la URL
  File "/home/user/proyecto/wallet/views.py", line 23
    cliente = Cliente.objects.get(id=999)                   ← Paso 2: Tu código busca un cliente
  File "/home/user/.venv/lib/.../django/db/models/..."
    raise self.model.DoesNotExist(...)                      ← Paso 1: Django no lo encuentra
wallet.models.Cliente.DoesNotExist: Cliente matching        ← ⭐ LA LÍNEA MÁS IMPORTANTE
query does not exist.                                          (léela PRIMERO)
```

### Regla para leer un traceback

```
 1. VE A LA ÚLTIMA LÍNEA     → ¿Qué tipo de error es? ¿Qué dice?
 2. SUBE A TU CÓDIGO         → ¿Cuál es la PRIMERA línea que menciona TU archivo?
                                (ignora las líneas que dicen ".venv" o "site-packages")
 3. VE A ESA LÍNEA           → Abre el archivo, ve a esa línea exacta
 4. LEE EL CONTEXTO          → ¿Qué hace esa línea? ¿Con qué datos?
```

### Los errores más comunes y qué significan

| Error                     | Traducción                                 | Causa más frecuente                                  |
| :------------------------ | :----------------------------------------- | :--------------------------------------------------- |
| `NameError`               | "No conozco esa variable"                  | Typo en el nombre o variable no definida             |
| `TypeError`               | "Me pasaste un tipo de dato incorrecto"    | Sumar string + int, pasar 2 argumentos en vez de 3   |
| `ValueError`              | "El valor no tiene sentido"                | `int("hola")`, formato incorrecto                    |
| `KeyError`                | "Esa clave no existe en el diccionario"    | Acceder a `dict['clave']` que no existe              |
| `IndexError`              | "El índice está fuera de rango"            | Acceder a `lista[10]` cuando solo tiene 5            |
| `AttributeError`          | "Este objeto no tiene ese atributo/método" | Typo en el nombre del método, o el objeto es `None`  |
| `ImportError`             | "No puedo importar eso"                    | Módulo no instalado o ruta incorrecta                |
| `SyntaxError`             | "Tu código tiene un error de escritura"    | Falta `:`, paréntesis sin cerrar, indentación        |
| `IntegrityError`          | "Violaste una regla de la base de datos"   | Dato duplicado, campo requerido vacío                |
| `DoesNotExist`            | "No encontré el registro que buscas"       | `.get()` con un ID que no existe                     |
| `MultipleObjectsReturned` | "Esperabas uno solo pero hay varios"       | `.get()` con un filtro que tiene más de un resultado |
| `TemplateDoesNotExist`    | "No encuentro el template HTML"            | Ruta incorrecta, app no en `INSTALLED_APPS`          |

---

---

# 🔎 5. Cómo Buscar Soluciones como un Senior (IA + Búsqueda)

---

En 2023, la primera reacción de un desarrollador ante un error era abrir Google. En 2026, **la primera reacción es abrir una IA**. Pero hay una diferencia enorme entre **usar la IA bien** y usarla mal.

## ❌ Cómo usa la IA un junior (ineficiente)

```
"Mi código no funciona, arréglalo"
"Tengo un error en Django, ¿qué hago?"
(copia y pega 500 líneas de código sin contexto)
```

Resultado: La IA te da una respuesta genérica que no aplica a tu caso, o peor, te da una "solución" que introduce nuevos bugs.

## ✅ Cómo usa la IA un senior (preciso)

```
"Tengo un IntegrityError: UNIQUE constraint failed: wallet_cliente.email
al ejecutar Cliente.objects.create(nombre=nombre, email=email)
en una vista de Django 5.0 con SQLite.
Ya verifiqué que el email existe en la BD.
¿Cómo valido antes de crear para evitar el error?"
```

### La fórmula para hablarle a la IA

```
[error exacto] + [contexto de tu proyecto] + [qué ya probaste] + [qué necesitas]
```

Ejemplos:

| Prompt junior                        | Prompt senior                                                                                                                                         |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| "mi django no funciona"              | `IntegrityError UNIQUE constraint en email al crear cliente. Uso Django 5.0 con SQLite. ¿Cómo valido antes de crear?`                                 |
| "error en python"                    | `NameError: name 'cliente' is not defined en línea 23 de views.py. Importo el modelo en la línea 2. ¿Por qué no lo encuentra?`                        |
| "no me carga la página"              | `TemplateDoesNotExist: wallet/lista.html. Tengo el archivo en wallet/templates/wallet/lista.html. La app está en INSTALLED_APPS. ¿Qué más puede ser?` |
| "arréglame este código" (500 líneas) | `Esta vista debería listar clientes activos pero muestra todos. Adjunto solo la función de la vista (15 líneas). ¿Dónde está el filtro incorrecto?`   |

---

### ⚠️ La regla más importante al usar IA para debugging

**La IA es tu ayudante, no tu cerebro.** Si no entiendes la solución que te da, **no la apliques**.

Por qué:

- La IA **alucina**: puede inventar funciones que no existen o atributos que Django no tiene.
- La IA **no conoce tu proyecto**: no sabe tus modelos, tus relaciones, ni tu lógica de negocio.
- La IA **no prueba el código**: te da algo que _parece_ correcto pero puede no funcionar en tu contexto.

> 💡 **Regla de oro:** Usa la IA para entender el error y generar hipótesis. Pero **tú** verificas, **tú** pruebas, y **tú** decides si la solución es correcta. Eso es ser desarrollador en 2026.

---

### 🔍 Y cuando la IA no alcanza: búsqueda precisa

A veces la IA no tiene la respuesta (errores muy específicos, bugs de librerías, problemas de versiones). Ahí necesitas buscar:

```
[tecnología] + [tipo de error exacto] + [mensaje clave]
```

| Operador de búsqueda     | ¿Qué hace?                | Ejemplo                                        |
| :----------------------- | :------------------------ | :--------------------------------------------- |
| `"comillas"`             | Busca la frase **exacta** | `"UNIQUE constraint failed"` Django            |
| `site:stackoverflow.com` | Busca solo en ese sitio   | `site:stackoverflow.com django IntegrityError` |
| `site:github.com/issues` | Busca en issues de GitHub | `site:github.com django 5.0 migration bug`     |
| `after:2025`             | Solo resultados recientes | `django 5.0 migrations after:2025`             |

### Dónde buscar (en orden de prioridad 2026)

| Prioridad | Fuente                            | ¿Cuándo usarla?                                                |
| :-------- | :-------------------------------- | :------------------------------------------------------------- |
| 1°        | **El propio mensaje de error**    | SIEMPRE. Léelo primero, antes de abrir cualquier otra cosa     |
| 2°        | **IA (Claude, ChatGPT, Copilot)** | Para entender el error, generar hipótesis, proponer soluciones |
| 3°        | **Documentación oficial**         | Cuando la IA te sugiere algo y quieres verificar que existe    |
| 4°        | **Stack Overflow + Google**       | Para errores específicos que la IA no resuelve bien            |
| 5°        | **GitHub Issues**                 | Cuando sospechas que es un bug de la librería, no tuyo         |

> 💡 **Dato real (Stack Overflow, 2025):** El **76%** de los desarrolladores ya usa IA como primera herramienta de búsqueda, desplazando a Google y Stack Overflow del primer lugar por primera vez en la historia. Pero el **45%** dice que debuggear código generado por IA toma más tiempo que debuggear código propio. La IA no reemplaza tu criterio — lo amplifica.

---

---

# 🦆 6. Rubber Duck Debugging: La Técnica Más Tonta (y Más Efectiva)

---

Esta técnica fue popularizada por el libro _"The Pragmatic Programmer"_ (Hunt & Thomas, 1999) y funciona así:

1. Pon un objeto en tu escritorio (un patito de goma, una taza, lo que sea).
2. **Explícale en voz alta** qué hace tu código, línea por línea.
3. Al explicar, tu cerebro detecta la inconsistencia.

### ¿Por qué funciona?

Cuando piensas en silencio, tu cerebro **se salta pasos** porque asume que todo está bien. Cuando hablas en voz alta, te obligas a ser explícito en cada paso. Y en algún momento dices:

> _"...y entonces esta línea toma el email del formulario y lo guarda en... espera. Ahí no estoy validando si ya existe. ESO es el problema."_

### La versión sin patito

Si te da vergüenza hablarle a un patito (no debería, pero ok):

- **Escríbelo.** Abre un archivo vacío y escribe en español qué hace tu código paso a paso.
- **Dibújalo.** Un diagrama simple de flechas: "datos entran aquí → pasan por aquí → salen por allá."
- **Explícaselo a un compañero.** No le pidas que resuelva el bug. Solo que escuche. Tú mismo lo vas a encontrar al explicar.

> 💡 **Dato real:** En una encuesta de JetBrains (2024), el **56%** de los desarrolladores profesionales admitió usar alguna forma de rubber duck debugging regularmente. Es una práctica estándar en la industria, no un chiste.

---

---

# 🙋 7. Cómo Pedir Ayuda Sin que Te Odien

---

Hay una **diferencia enorme** entre pedir ayuda de forma profesional y pedir ayuda de forma que hace perder tiempo a todos. Esta diferencia puede determinar si te ayudan en 5 minutos o si te ignoran.

## ❌ Cómo NO pedir ayuda

```
"Oigan, mi código no funciona. ¿Alguien puede ayudarme?"
```

¿Qué debería responder alguien a eso? Nadie sabe qué intentas hacer, qué lenguaje usas, qué error te da, ni qué ya probaste. Es como llamar al mecánico y decir "mi auto está malo" sin decir ni la marca.

## ✅ Cómo pedir ayuda profesionalmente

Usa la **plantilla de 5 puntos**:

```
1. QUÉ INTENTO HACER:
   "Estoy creando un formulario para registrar clientes en Django."

2. QUÉ ESPERABA QUE PASARA:
   "Al enviar el formulario, debería crear un nuevo cliente en la base de datos."

3. QUÉ PASA EN VEZ DE ESO:
   "Recibo un IntegrityError: UNIQUE constraint failed: wallet_cliente.email"

4. QUÉ YA PROBÉ:
   "Verifiqué que el email no esté duplicado antes de enviar.
    Revisé la base de datos y sí hay un registro con ese email."

5. CÓDIGO RELEVANTE:
   (pegar solo las líneas importantes, no todo el proyecto)
```

### ¿Por qué esta plantilla funciona?

Porque la persona que te ayuda puede:

- Entender el contexto sin preguntar 10 cosas
- Ir directo al punto
- Darte una respuesta útil en el primer mensaje

> ⚠️ **Regla profesional:** Antes de pedir ayuda, debes haber completado **al menos** los Pasos 1-3 del método R.E.P.L.A. Si no puedes describir tu hipótesis, aún no estás listo para pedir ayuda — estás pidiendo que hagan el debugging por ti.

---

---

# ❌ 8. Los 7 Errores de Debugging que Todos Cometen

---

### Error 1: "Cambiar cosas al azar hasta que funcione"

**Por qué es malo:** Si funciona, no sabes por qué. No aprendiste nada. El mismo bug va a volver.

**Lo correcto:** Una hipótesis → un cambio → una verificación.

---

### Error 2: "No leer el mensaje de error"

**Por qué es malo:** El error te dice exactamente qué pasó y dónde. Ignorarlo es como tener un GPS y decidir ir por intuición.

**Lo correcto:** Siempre lee la última línea primero. Tradúcela a español.

---

### Error 3: "Buscar en Google antes de pensar"

**Por qué es malo:** Terminas con 15 soluciones que no aplican a tu caso porque no entendiste tu propio problema.

**Lo correcto:** Lee el error, formula una hipótesis, y DESPUÉS busca.

---

### Error 4: "Cambiar 10 cosas al mismo tiempo"

**Por qué es malo:** Si algo se arregla, no sabes cuál de los 10 cambios lo resolvió. Si algo se rompe peor, no sabes cuál deshacerlo.

**Lo correcto:** Un cambio por vez. Verificar después de cada cambio.

---

### Error 5: "try/except vacío para 'arreglar' el error"

```python
# ❌ NUNCA hagas esto:
try:
    resultado = calcular_algo()
except:
    pass  # "Ya no da error" — sí, porque lo ESCONDISTE
```

**Por qué es malo:** No arreglaste el bug. Lo hiciste invisible. Ahora tienes un error silencioso que puede causar daños peores.

**Lo correcto:** Si usas try/except, captura el error **específico** y haz algo con él.

---

### Error 6: "Asumir que el error está donde tú crees"

**Por qué es malo:** El 40% de las veces, el error no está donde piensas. El código que "se ve bien" puede ser el culpable.

**Lo correcto:** Usa prints o breakpoints para **verificar**, no para confirmar tu sesgo.

---

### Error 7: "No documentar la solución"

**Por qué es malo:** Dentro de 3 meses te va a pasar exactamente el mismo error y vas a pasar exactamente las mismas 2 horas resolviéndolo.

**Lo correcto:** Anota en algún lugar: "Error X → Causa Y → Solución Z." Tu futuro yo te lo va a agradecer.

---

---

# ✅ 9. Checklist: La Receta Completa en Una Página

---

```
┌──────────────────────────────────────────────────────────────────┐
│               🔍 MÉTODO R.E.P.L.A. — CHECKLIST                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  R — REPRODUCIR                                                  │
│  [ ] ¿Puedo hacer que el error pase de nuevo?                    │
│  [ ] ¿Anoté los pasos exactos para provocarlo?                   │
│  [ ] ¿Es consistente o intermitente?                             │
│                                                                  │
│  E — EXAMINAR                                                    │
│  [ ] ¿Leí el mensaje de error COMPLETO?                          │
│  [ ] ¿Identifiqué el tipo de error?                              │
│  [ ] ¿Identifiqué la línea exacta en MI código?                  │
│  [ ] ¿Puedo traducir el error a español?                         │
│                                                                  │
│  P — PROPONER                                                    │
│  [ ] ¿Tengo UNA hipótesis concreta?                              │
│  [ ] ¿Sé qué evidencia la confirmaría o descartaría?             │
│  [ ] ¿Tengo una hipótesis alternativa si esta falla?              │
│                                                                  │
│  L — LIMITAR                                                     │
│  [ ] ¿Reduje el área de búsqueda? (búsqueda binaria/prints)     │
│  [ ] ¿Encontré la línea exacta donde falla?                      │
│  [ ] ¿Verifiqué qué VALORES tienen las variables en ese punto?   │
│                                                                  │
│  A — APLICAR Y VERIFICAR                                         │
│  [ ] ¿Hice UN solo cambio?                                       │
│  [ ] ¿El error original ya no ocurre?                             │
│  [ ] ¿Probé con otros datos además del que fallaba?               │
│  [ ] ¿No rompí nada que funcionaba antes?                         │
│  [ ] ¿Limpié los prints de debugging?                             │
│  [ ] ¿Entiendo POR QUÉ funciona mi solución?                     │
│  [ ] ¿Anoté la solución para el futuro?                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

---

# 🛠️ 10. Tabla de Herramientas de Debugging

---

Estas son las herramientas que usan los profesionales para hacer debugging. No necesitan dominarlas todas ahora — pero sí saber que existen y dónde encontrarlas.

---

## 🐍 Herramientas de Python

| Herramienta        | ¿Qué hace?                                                                                  | Nivel      | Link                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------- |
| `print()`          | Imprime valores en la consola para verificar datos                                          | Básico     | [Documentación print](https://docs.python.org/3/library/functions.html#print)           |
| `type()` y `dir()` | Muestra el tipo de un objeto y sus métodos disponibles                                      | Básico     | [Funciones built-in](https://docs.python.org/3/library/functions.html)                  |
| `pdb`              | Debugger interactivo de Python: pausa el código y te deja inspeccionar                      | Intermedio | [Documentación pdb](https://docs.python.org/3/library/pdb.html)                         |
| `breakpoint()`     | Atajo moderno para activar `pdb` (desde Python 3.7)                                         | Intermedio | [Documentación breakpoint](https://docs.python.org/3/library/functions.html#breakpoint) |
| `logging`          | Sistema profesional de logs: reemplaza los prints con niveles (DEBUG, INFO, WARNING, ERROR) | Avanzado   | [Documentación logging](https://docs.python.org/3/library/logging.html)                 |
| `traceback`        | Módulo para capturar y formatear tracebacks programáticamente                               | Avanzado   | [Documentación traceback](https://docs.python.org/3/library/traceback.html)             |

---

## 🌐 Herramientas de Django

| Herramienta                   | ¿Qué hace?                                                                      | Nivel      | Link                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| Página de error de Django     | Cuando `DEBUG=True`, Django muestra el traceback completo con variables locales | Básico     | [Documentación DEBUG](https://docs.djangoproject.com/en/stable/ref/settings/#debug)               |
| `python manage.py shell`      | Consola interactiva para probar queries y lógica sin levantar el servidor       | Básico     | [Documentación shell](https://docs.djangoproject.com/en/stable/ref/django-admin/#shell)           |
| `python manage.py check`      | Verifica errores comunes en la configuración del proyecto                       | Básico     | [Documentación check](https://docs.djangoproject.com/en/stable/ref/django-admin/#check)           |
| Django Debug Toolbar          | Barra lateral que muestra queries SQL, tiempos, templates y más                 | Intermedio | [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)                    |
| `python manage.py sqlmigrate` | Muestra el SQL exacto que ejecutaría una migración                              | Intermedio | [Documentación sqlmigrate](https://docs.djangoproject.com/en/stable/ref/django-admin/#sqlmigrate) |
| `QuerySet.explain()`          | Muestra el plan de ejecución SQL de una consulta                                | Avanzado   | [Documentación explain](https://docs.djangoproject.com/en/stable/ref/models/querysets/#explain)   |

---

## 💻 Herramientas del Editor (VS Code)

| Herramienta                   | ¿Qué hace?                                                  | Nivel      | Link                                                                                              |
| ----------------------------- | ----------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| Debugger integrado de VS Code | Breakpoints visuales, inspección de variables, step-by-step | Intermedio | [Debugging en VS Code](https://code.visualstudio.com/docs/editor/debugging)                       |
| Extensión Python              | IntelliSense, linting, formateo automático para Python      | Básico     | [Extensión Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)          |
| Extensión Pylance             | Detección de errores de tipo en tiempo real                 | Básico     | [Extensión Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) |
| Terminal integrada            | Correr comandos sin salir del editor                        | Básico     | [Terminal en VS Code](https://code.visualstudio.com/docs/terminal/basics)                         |

---

## 🌍 Herramientas del Navegador

| Herramienta         | ¿Qué hace?                                                                | Nivel      | Link                                                                 |
| ------------------- | ------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------- |
| DevTools → Console  | Muestra errores de JavaScript y permite ejecutar código                   | Básico     | [Chrome DevTools](https://developer.chrome.com/docs/devtools/)       |
| DevTools → Network  | Muestra todas las peticiones HTTP: qué se envía, qué responde el servidor | Intermedio | [Panel Network](https://developer.chrome.com/docs/devtools/network/) |
| DevTools → Elements | Inspeccionar y modificar el HTML/CSS en tiempo real                       | Básico     | [Panel Elements](https://developer.chrome.com/docs/devtools/dom/)    |

---

## 🔍 Comunidades y Búsqueda

| Recurso        | ¿Qué es?                                                            | ¿Cuándo usarlo?                                        | Link                                                                |
| -------------- | ------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------- |
| Stack Overflow | Foro de preguntas y respuestas de programación más grande del mundo | Cuando buscas un error específico                      | [stackoverflow.com](https://stackoverflow.com/)                     |
| Django Forum   | Foro oficial de la comunidad Django                                 | Para preguntas específicas de Django                   | [forum.djangoproject.com](https://forum.djangoproject.com/)         |
| Python Docs    | Documentación oficial de Python                                     | Cuando necesitas entender un módulo o función          | [docs.python.org](https://docs.python.org/3/)                       |
| Django Docs    | Documentación oficial de Django                                     | Cuando necesitas entender un componente de Django      | [docs.djangoproject.com](https://docs.djangoproject.com/en/stable/) |
| GitHub Issues  | Sección de reportes de bugs de librerías open-source                | Cuando sospechas que es un bug de la librería, no tuyo | [github.com](https://github.com/)                                   |

---

---

# 🏁 Resumen de la Clase

---

## ✅ Lo que aprendimos hoy

| Concepto                    | La idea clave                                                        |
| :-------------------------- | :------------------------------------------------------------------- |
| **Debugging es un proceso** | No es arte ni magia — es el método científico aplicado al código     |
| **Método R.E.P.L.A.**       | Reproducir → Examinar → Proponer → Limitar → Aplicar                 |
| **Leer el traceback**       | De abajo hacia arriba. La última línea es la más importante.         |
| **Buscar en Google**        | `[tecnología] + [error exacto] + [mensaje clave]`                    |
| **Rubber Duck Debugging**   | Explica en voz alta. Tu cerebro detecta la inconsistencia al hablar. |
| **Pedir ayuda bien**        | 5 puntos: qué hago, qué esperaba, qué pasa, qué probé, código.       |
| **Un cambio por vez**       | Si cambias 10 cosas, no sabes cuál resolvió el problema.             |
| **Documentar la solución**  | Tu futuro yo te lo va a agradecer.                                   |

---

## 📚 Referencias (APA 7ª ed.)

Agans, D. J. (2002). _Debugging: The 9 indispensable rules for finding even the most elusive software and hardware problems_. AMACOM.

Hunt, A., & Thomas, D. (1999). _The Pragmatic Programmer: From journeyman to master_. Addison-Wesley. [Capítulo sobre Rubber Duck Debugging]

JetBrains. (2024). _Developer Ecosystem Survey 2024_. https://www.jetbrains.com/lp/devecosystem-2024/

Python Software Foundation. (2024). _pdb — The Python Debugger_. https://docs.python.org/3/library/pdb.html

Django Software Foundation. (2024). _Debugging Django_. https://docs.djangoproject.com/en/stable/

Zeller, A. (2009). _Why Programs Fail: A Guide to Systematic Debugging_ (2ª ed.). Morgan Kaufmann.

---
