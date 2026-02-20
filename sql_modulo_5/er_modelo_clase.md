<!-- =========================================================
Archivo: er_modelo_clase.md
Tema: Modelo Entidad-Relación — Teoría Completa
Partes: Parte 1 (ER base) + Parte 2 (Transformación y Normalización)
========================================================= -->

# 🗺️ El Modelo Entidad-Relación — De la Idea a la Base de Datos

---

---

# 📚 PARTE 1 — El Modelo Conceptual

---

## 🗺️ ¿Qué vamos a aprender hoy?

| Tema                           | Pregunta clave                                         |
| ------------------------------ | ------------------------------------------------------ |
| 🧩 Modelo ER                   | ¿Cómo represento la realidad en un diagrama?           |
| 🔎 Abstracción                 | ¿Cómo simplifico un problema complejo?                 |
| 🔗 Relaciones                  | ¿Cómo se conectan las cosas entre sí?                  |
| 🏷️ Atributos                   | ¿Qué información necesito guardar?                     |
| 💪 Entidades fuertes y débiles | ¿Cuáles son independientes y cuáles dependen de otras? |
| 🔄 Reglas de transformación    | ¿Cómo paso de un diagrama a tablas SQL?                |
| 📐 Normalización               | ¿Cómo evito datos repetidos y problemas?               |

---

---

## 1️⃣ ¿Qué es el Modelo Entidad-Relación?

---

### La analogía: El plano del arquitecto 🏗️

Imagina que quieres construir una casa. **¿Empezarías a poner ladrillos sin un plano?**

No. Primero dibujas un plano que muestra:

- Cuántas habitaciones hay
- Cómo se conectan entre sí
- Qué tamaño tiene cada una
- Dónde van las puertas y ventanas

**El Modelo Entidad-Relación (ER) es el PLANO de tu base de datos.**

Antes de escribir una sola línea de SQL, necesitas **diseñar** qué información vas a guardar y cómo se relaciona.

---

### Definición formal

> El modelo ER es un enfoque para representar de forma **visual y abstracta** la estructura de datos y las relaciones entre entidades de un sistema.

En español simple:

```
Modelo ER = un DIBUJO que muestra
             QUÉ cosas existen en tu sistema
             y CÓMO se conectan entre sí
```

---

### Los 3 componentes del modelo ER

Un diagrama ER tiene **solo 3 piezas**. Si entiendes estas 3, entiendes todo el diagrama:

| #   | Componente   | ¿Qué es?                                     | Se dibuja como…   | Ejemplo                   |
| --- | ------------ | -------------------------------------------- | ----------------- | ------------------------- |
| 1   | **Entidad**  | Un objeto o concepto del mundo real          | 📦 Rectángulo     | Estudiante, Curso, Pedido |
| 2   | **Atributo** | Una propiedad o característica de la entidad | ⭕ Óvalo / Elipse | nombre, email, precio     |
| 3   | **Relación** | Una conexión entre dos o más entidades       | 🔷 Rombo          | "inscribe", "compra"      |

> **Truco para recordar:** Piensa en una oración.
> _"El **estudiante** (entidad) con **nombre** Juan (atributo) **inscribe** (relación) un **curso** (entidad)"._
> Cada palabra en negrita es un componente del diagrama.

---

### Ejemplo visual: Biblioteca — Cómo leer un diagrama ER paso a paso

```
     ┌──────────┐          ┌──────────┐          ┌──────────┐
     │  AUTOR   │──────────│ escribió │──────────│  LIBRO   │
     └──────────┘          └──────────┘          └──────────┘
       │                                            │
       ├── nombre                                   ├── título
       ├── nacionalidad                             ├── ISBN
       └── fecha_nac                                ├── año
                                                    └── editorial
```

- **Rectángulos** (`AUTOR`, `LIBRO`) = las **entidades**
- **Recuadro del medio** (`escribió`) = la **relación** (el verbo que los une)
- Las líneas que **cuelgan** de cada rectángulo = los **atributos**

**¿Cómo leo este diagrama? Paso a paso:**

| Paso | Qué hago                                          | Qué veo                                                             |
| ---- | ------------------------------------------------- | ------------------------------------------------------------------- |
| 1    | Busco los **rectángulos**                         | `AUTOR` y `LIBRO` → son las **entidades** (las "cosas" que existen) |
| 2    | Busco qué los **conecta**                         | `escribió` → es la **relación** (el verbo que los une)              |
| 3    | Leo en voz alta formando una oración              | _"Un AUTOR **escribió** un LIBRO"_ → ¡tiene sentido!                |
| 4    | Miro qué **cuelga** de cada rectángulo            | Son los **atributos** (la info que guardamos de cada entidad)       |
| 5    | Verifico que cada atributo pertenece a su entidad | `nombre` es del Autor, `título` es del Libro → ✅ correcto          |

> **Consejo práctico:** Siempre lee el diagrama como una **oración en español**: `[Entidad A] + [relación] + [Entidad B]`. Si la oración suena natural, el diagrama está bien diseñado.

---

---

## 2️⃣ El Proceso de Abstracción

---

### ¿Qué es abstraer?

> Abstraer = **simplificar la realidad** quedándote solo con la información que importa para tu sistema.

---

### La analogía: El mapa 🗺️

Un mapa de Santiago NO muestra cada piedra, cada árbol, cada persona caminando. Muestra solo lo que necesitas: **calles, estaciones de metro, comunas.**

Cuando diseñas una base de datos, haces lo mismo:

```
Un auto Toyota Corolla 2022, patente ABCD-12:
  Color rojo, 45.000 km, motor 1.8L, asientos de tela,
  tiene un rayón en la puerta, huele a pino, suena un
  ruidito raro al frenar, el dueño le puso stickers...

Base de datos de un TALLER MECÁNICO:
  Toyota Corolla → patente, modelo, año, kilometraje
  (el color de los stickers NO importa para el taller)

Base de datos de un SEGURO DE AUTO:
  Toyota Corolla → patente, dueño, valor comercial, siniestros
  (el kilometraje NO importa para el seguro)
```

**Abstraer = quedarte SOLO con lo relevante para tu sistema.** El mismo auto guarda datos distintos según quién lo necesite.

---

### Niveles de abstracción en bases de datos

Cuando diseñas una base de datos, pasas por **3 niveles**, de lo más general a lo más técnico:

```
┌─────────────────────────────────────────┐
│  ① NIVEL CONCEPTUAL                    │  ← Modelo ER (diagramas)
│  "¿QUÉ datos necesito?"               │     Lo más abstracto
│                                         │     👤 Lo entiende CUALQUIER persona
├─────────────────────────────────────────┤
│  ② NIVEL LÓGICO                        │  ← Tablas, columnas, tipos
│  "¿CÓMO organizo los datos?"           │     Estructura concreta
│                                         │     👨‍💻 Lo entiende un técnico
├─────────────────────────────────────────┤
│  ③ NIVEL FÍSICO                        │  ← Archivos, índices, disco
│  "¿DÓNDE se guardan los datos?"        │     Lo más técnico
│                                         │     🔧 Lo maneja el motor de BD
└─────────────────────────────────────────┘
```

> **En esta clase** nos movemos entre el nivel **① conceptual** (diagramas ER) y el nivel **② lógico** (tablas SQL). El nivel ③ lo maneja internamente PostgreSQL/MySQL por nosotros.

---

### Los 4 pilares de una base de datos

| Pilar         | ¿Qué es?                                                        | Ejemplo sencillo                                      |
| ------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| **Tablas**    | Estructuras que almacenan datos en filas y columnas             | La tabla `clientes` con nombre, email, teléfono       |
| **Esquemas**  | La definición de la estructura (columnas, tipos, restricciones) | `nombre VARCHAR(80) NOT NULL`                         |
| **Consultas** | Instrucciones SQL para interactuar con los datos                | `SELECT * FROM clientes WHERE activo = true`          |
| **Vistas**    | Consultas guardadas que actúan como "tablas virtuales"          | Una vista que muestra solo clientes activos con deuda |

---

---

## 3️⃣ Entidades y Atributos en Detalle

---

### ¿Qué es una entidad?

Una entidad es **cualquier cosa del mundo real que queremos registrar** en nuestra base de datos.

```
🏢 Sistema de RRHH        →  Empleado, Departamento, Cargo
🏥 Sistema de Clínica      →  Paciente, Doctor, Cita, Diagnóstico
🛒 Sistema de E-commerce   →  Producto, Cliente, Orden, Pago
🏫 Sistema de Universidad  →  Estudiante, Profesor, Curso, Nota
```

**Regla de oro:** Si puedes decir _"necesito guardar información sobre **\_\_\_**"_, entonces **\_\_\_** es una entidad.

> **Ejercicio mental rápido:** ¿Cuáles serían las entidades de una app como Netflix?
> Respuesta: `Usuario`, `Película`, `Serie`, `Episodio`, `Plan`, `Pago`… ¿Se te ocurren más?

---

### ¿Qué es un atributo?

Un atributo es una **propiedad o característica** de una entidad. Es la información concreta que guardamos.

| Entidad       | Atributos                                  |
| ------------- | ------------------------------------------ |
| 👤 Estudiante | nombre, email, fecha_nacimiento, dirección |
| 👨‍🏫 Profesor   | nombre, título, especialidad               |
| 📘 Curso      | nombre, código, descripción, créditos      |

**Cada atributo tiene un TIPO DE DATO** (texto, número, fecha, booleano, etc.).

---

### Tipos de atributos — Los 4 sabores

| Tipo             | Descripción                  | Ejemplo                                        | Pista para identificarlo                |
| ---------------- | ---------------------------- | ---------------------------------------------- | --------------------------------------- |
| **Simple**       | Un solo valor indivisible    | `nombre = 'Juan'`                              | No se puede partir en partes            |
| **Compuesto**    | Se puede dividir en partes   | `dirección` → calle + número + comuna + ciudad | Podrías separarlo en columnas distintas |
| **Derivado**     | Se calcula a partir de otros | `edad` se calcula con `fecha_nacimiento`       | No se guarda, se calcula al momento     |
| **Multivaluado** | Puede tener varios valores   | `teléfonos` → puede tener varios               | El dato es una "lista"                  |

> **¿Por qué importa esto?** Porque cada tipo se implementa de forma diferente en SQL:
>
> - **Compuesto** → lo separas en columnas (`calle`, `numero`, `comuna`)
> - **Derivado** → NO creas columna, lo calculas con una consulta
> - **Multivaluado** → creas una tabla aparte (porque una celda = un valor)

---

### El Identificador Único (Clave Primaria)

Todo registro en una tabla necesita ser **identificable de forma única**. Para eso existe la **clave primaria (PK)**.

```
❓ ¿Puedo usar el nombre como identificador?

   María López   ← ¿Cuál María López? Puede haber 50
   María López   ← No sirve como identificador ❌

❓ ¿Y el RUT?

   12.345.678-9  ← Único en todo Chile ✅

❓ ¿Y un ID autoincremental?

   1, 2, 3, 4... ← Siempre único ✅ (la opción más común)
```

**Tres reglas de la PK:**

| Regla         | Significado                  | ¿Por qué?                                        |
| ------------- | ---------------------------- | ------------------------------------------------ |
| **Única**     | No puede repetirse           | Si se repite, no sabes qué fila es cuál          |
| **No nula**   | Siempre debe tener valor     | Si es NULL, no puedes buscar ese registro        |
| **Inmutable** | No debe cambiar en el tiempo | Si cambia, se rompen todas las referencias (FKs) |

---

---

## 4️⃣ Tipos de Relaciones

---

### ¿Qué es una relación?

Una relación describe **cómo se conectan dos entidades entre sí**.

Las relaciones se nombran con **verbos** que describen la conexión:

- Un cliente **realiza** pedidos
- Un profesor **enseña** cursos
- Un libro **pertenece a** una categoría

> **Dato clave:** El tipo de relación determina **dónde** ponemos la clave foránea (FK) cuando creamos las tablas SQL. Por eso es tan importante identificarlo bien.

---

### Los 4 tipos de relaciones — Una guía visual completa

---

### 🔗 Uno a Uno (1:1)

> Una entidad A se relaciona con **exactamente una** entidad B, y viceversa.

```
     ┌──────────┐    1              1    ┌──────────┐
     │ PERSONA  │────────────────────────│ PASAPORTE│
     └──────────┘                        └──────────┘
                  ↑                 ↑
                  │                 │
        "UNA persona tiene    UN pasaporte pertenece
         UN pasaporte"        a UNA persona"
```

**¿Cómo lo leo?** Pon tu dedo en cada número:

- Desde PERSONA → hay un `1` → "cada persona tiene **un** pasaporte"
- Desde PASAPORTE → hay un `1` → "cada pasaporte pertenece a **una** persona"

**Ejemplos reales:**

- Una persona tiene **un** pasaporte, y ese pasaporte pertenece a **una** persona
- Un país tiene **una** capital, y esa capital pertenece a **un** país
- Un empleado tiene **un** contrato vigente

**¿Cuándo se usa?** Cuando quieres separar información por seguridad o por organización, aunque podrían estar en la misma tabla.

---

### 🔗 Uno a Muchos (1:N) — ⭐ La más común

> Una entidad A se relaciona con **muchas** entidades B, pero cada B pertenece a **una sola** A.

```
     ┌──────────┐    1              N    ┌──────────┐
     │  CLIENTE │────────────────────────│  PEDIDO  │
     └──────────┘                        └──────────┘
                  ↑                 ↑
                  │                 │
        "UN cliente puede      "cada pedido pertenece
         tener MUCHOS           a UN SOLO cliente"
         pedidos"

     Ejemplo concreto:

       Juan Pérez  ───→  Pedido #001
                   ───→  Pedido #002
                   ───→  Pedido #003
       Ana Torres  ───→  Pedido #004
```

**¿Cómo lo leo?** El `1` y la `N` te dicen "cuántos":

- Desde CLIENTE → `1` : "un solo cliente..."
- Hacia PEDIDO → `N` : "...puede tener muchos pedidos"

**Ejemplos reales:**

- Un cliente tiene **muchos** pedidos, pero cada pedido pertenece a **un** cliente
- Un departamento tiene **muchos** empleados, pero cada empleado está en **un** departamento
- Una categoría tiene **muchas** películas, pero cada película tiene **una** categoría

> ⭐ **Es la relación más frecuente** en el mundo real. Si no estás seguro del tipo de relación, probablemente sea 1:N.

---

### 🔗 Muchos a Uno (N:1)

> Es lo mismo que 1:N pero visto desde el otro lado.

```
     ┌──────────┐    N              1    ┌──────────┐
     │  PEDIDO  │────────────────────────│  CLIENTE │
     └──────────┘                        └──────────┘

   "Muchos pedidos pertenecen a un mismo cliente"
```

Es simplemente la perspectiva inversa de 1:N. **Si A→B es 1:N, entonces B→A es N:1.**

> **Piénsalo así:** ¿Desde dónde empiezas a leer? Si empiezas desde "Pedido", es N:1. Si empiezas desde "Cliente", es 1:N. Mismo diagrama, diferente punto de vista.

---

### 🔗 Muchos a Muchos (N:M) — ⚠️ La que requiere tabla extra

> Muchas entidades A se relacionan con muchas entidades B.

```
     ┌──────────┐    N              M    ┌──────────┐
     │ESTUDIANTE│────────────────────────│  CURSO   │
     └──────────┘                        └──────────┘
                  ↑                 ↑
                  │                 │
        "cada estudiante         "cada curso tiene
         puede estar en           MUCHOS estudiantes"
         MUCHOS cursos"

     Ejemplo concreto:

       Juan  ───→  Matemáticas     ←───  Ana
             ───→  Física          ←───  Pedro
             ───→  Química         ←───  Ana
                   Historia        ←───  Pedro
```

**¿Cómo lo leo?** Ambos lados tienen "muchos":

- Un estudiante cursa **muchas** asignaturas
- Y cada asignatura tiene **muchos** estudiantes

**Ejemplos reales:**

- Un estudiante cursa **muchas** asignaturas, y cada asignatura tiene **muchos** estudiantes
- Un actor actúa en **muchas** películas, y cada película tiene **muchos** actores
- Un producto pertenece a **muchas** categorías, y cada categoría tiene **muchos** productos

---

### ¿Cómo se implementa N:M en SQL? — La tabla intermedia

**No se puede implementar directamente.** ¿Por qué? Porque no puedes poner una FK en ninguno de los dos lados sin crear duplicados.

La solución: crear una **tabla intermedia** (también llamada tabla pivote o tabla de unión):

```
     ANTES (N:M directo — NO se puede hacer en SQL):

     ┌──────────┐    N              M    ┌──────────┐
     │ESTUDIANTE│── ── ── ── ── ── ── ──│  CURSO   │
     └──────────┘                        └──────────┘

     DESPUÉS (con tabla intermedia — ✅ así se hace):

     ┌──────────┐         ┌──────────────┐         ┌──────────┐
     │ESTUDIANTE│────1:N──│ INSCRIPCIÓN  │──N:1────│  CURSO   │
     └──────────┘         └──────────────┘         └──────────┘
                             │
                             ├── id_estudiante (FK) ← apunta a ESTUDIANTE
                             ├── id_curso (FK)      ← apunta a CURSO
                             └── fecha_inscripcion  ← dato propio
```

**¿Qué pasó?** La tabla `INSCRIPCIÓN` convierte **una** relación N:M en **dos** relaciones 1:N. Es un "puente" entre ambas entidades.

```sql
-- La tabla intermedia en SQL:
CREATE TABLE inscripciones (
  id              SERIAL PRIMARY KEY,
  id_estudiante   INT NOT NULL REFERENCES estudiantes(id),
  id_curso        INT NOT NULL REFERENCES cursos(id),
  fecha           TIMESTAMP DEFAULT NOW()
);
```

> **Dato útil:** La tabla intermedia a menudo tiene **datos propios** (como `fecha` o `nota`). Eso es porque la inscripción **es algo** por sí misma: tiene una fecha, un estado, una nota. No es solo un "cable" conectando dos cosas.

---

### Resumen visual: ¿Cómo elijo el tipo de relación?

Hazte estas preguntas en orden:

```
Pregunta 1: ¿Puede A tener MUCHOS B?
  └── NO  → 1:1  (Persona ──── Pasaporte)
  └── SÍ  → Pregunta 2

Pregunta 2: ¿Puede B tener MUCHOS A?
  └── NO  → 1:N  (Cliente ──── Pedidos)         ⭐ más común
  └── SÍ  → N:M  (Estudiante ──── Curso)        ⚠️ tabla intermedia
```

| Tipo | Lectura                         | Ejemplo breve        | En SQL...                         |
| ---- | ------------------------------- | -------------------- | --------------------------------- |
| 1:1  | uno tiene uno                   | Persona ── Pasaporte | FK en cualquiera de las 2 tablas  |
| 1:N  | uno tiene muchos                | Cliente ── Pedidos   | FK en la tabla del lado N         |
| N:1  | muchos pertenecen a uno (= 1:N) | Pedidos ── Cliente   | (mismo que 1:N, otra perspectiva) |
| N:M  | muchos con muchos               | Estudiante ── Curso  | Se crea tabla intermedia          |

---

---

## 5️⃣ Entidades Fuertes y Débiles

---

### La analogía: El inquilino y el edificio 🏢

Un **edificio** existe por sí solo. Tiene dirección, nombre, dueño.

Un **departamento** dentro del edificio... ¿puede existir sin el edificio? **No.** El "Depto 501" no tiene sentido si no sabes DE QUÉ edificio.

- **Edificio** = Entidad fuerte (independiente)
- **Departamento** = Entidad débil (depende del edificio)

---

### Definición

| Tipo                  | Característica                                                                  | Ejemplo                                                |
| --------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Entidad fuerte** 💪 | Existe por sí sola. Tiene su propia PK independiente.                           | Cliente, Producto, Empleado                            |
| **Entidad débil** 🤝  | Depende de otra entidad para existir. Su PK incluye la FK de la entidad fuerte. | Detalle de pedido, Copia de libro, Habitación de hotel |

---

### ¿Cómo las distingo? — Prueba del borrado

> **Pregunta mágica:** _"Si borro la entidad padre, ¿la entidad hija sigue teniendo sentido?"_
>
> - Si **SÍ** → es **fuerte** (independiente)
> - Si **NO** → es **débil** (dependiente)

| Si borro…               | ¿Tiene sentido `Copia #3`?              | ¿Tiene sentido `Estudiante Juan`? |
| ----------------------- | --------------------------------------- | --------------------------------- |
| El libro "Harry Potter" | ❌ No sé copia de QUÉ libro             | ✅ Juan sigue existiendo          |
| **Conclusión**          | `Copia` es **débil** respecto a `Libro` | `Estudiante` es **fuerte**        |

---

### Diferencias clave

| Aspecto                     | Entidad Fuerte         | Entidad Débil                        |
| --------------------------- | ---------------------- | ------------------------------------ |
| **¿Existe sola?**           | ✅ Sí                  | ❌ No, depende de otra               |
| **Clave primaria**          | Propia e independiente | Combinada (su FK + un discriminante) |
| **Si se borra el padre...** | No afecta a nadie      | La entidad débil pierde sentido      |
| **Representación ER**       | Rectángulo simple      | Rectángulo con doble borde           |

---

### Ejemplo: Librería — Diagrama comparativo

```
   Entidad FUERTE                     Entidad DÉBIL
   (borde simple)                     (borde doble ══)

 ┌──────────────┐              ╔══════════════════╗
 │    LIBRO     │──── 1:N ─────║  COPIA DE LIBRO  ║
 │              │              ║                  ║
 │  libro_id PK │              ║  libro_id FK ──────→ apunta a LIBRO
 │  título      │              ║  nro_copia       ║
 │  autor       │              ║  estado          ║
 │  año         │              ║  ubicacion       ║
 └──────────────┘              ╚══════════════════╝

 ¿Cómo leo esto?:
   ▸ "Harry Potter" existe como concepto (entidad fuerte).
   ▸ "La copia #3 de Harry Potter" NO existe sin saber
      de qué libro hablamos (entidad débil).
   ▸ La PK de copia_libro = (libro_id + nro_copia)
     ← combina la FK del padre + un número propio
```

---

---

---

# 📚 PARTE 2 — Del Diagrama a la Base de Datos

---

---

## 6️⃣ Modelo Conceptual vs Modelo Relacional

---

### ¿Cuál es la diferencia?

Son **dos formas de ver lo mismo**, pero en distintos niveles de detalle:

| Aspecto         | Modelo Conceptual (ER)                | Modelo Relacional (SQL)                        |
| --------------- | ------------------------------------- | ---------------------------------------------- |
| **¿Qué es?**    | Diagrama abstracto                    | Tablas concretas                               |
| **Nivel**       | Alto nivel, sin detalles técnicos     | Bajo nivel, con tipos de datos y restricciones |
| **Público**     | Para TODOS (cliente, jefe, diseñador) | Para TÉCNICOS (desarrolladores, DBAs)          |
| **Muestra**     | Entidades, atributos, relaciones      | Tablas, columnas, PKs, FKs, tipos              |
| **Herramienta** | Dibujo (papel, Lucidchart, Draw.io)   | SQL (CREATE TABLE)                             |

> **Analogía:** Es como un **plano de arquitectura** vs la **orden de construcción**. El plano dice "aquí va una cocina". La orden de construcción dice "instalar una cocina de 3×4m con cerámica tipo X y grifería modelo Y".

---

### Ejemplo lado a lado — Del dibujo al código

**① MODELO CONCEPTUAL (Diagrama ER) — Lo que dibujas:**

```
  ┌──────────┐         ┌──────────┐         ┌──────────┐
  │ USUARIO  │──1:N───│  PEDIDO  │───N:1──│ PRODUCTO │
  └──────────┘         └──────────┘         └──────────┘
    nombre               fecha                nombre
    email                total                precio
                                              stock

 Lectura: "Un USUARIO hace muchos PEDIDOS.
           Cada PEDIDO tiene muchos PRODUCTOS."
```

**② MODELO RELACIONAL (SQL) — Lo que programas:**

```sql
-- MODELO RELACIONAL (SQL):

CREATE TABLE usuarios (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80) NOT NULL,
  email   VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE productos (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(100) NOT NULL,
  precio  NUMERIC(10,2) NOT NULL,
  stock   INT NOT NULL DEFAULT 0
);

CREATE TABLE pedidos (
  id          SERIAL PRIMARY KEY,
  id_usuario  INT NOT NULL REFERENCES usuarios(id),  -- FK al lado N
  fecha       TIMESTAMP DEFAULT NOW(),
  total       NUMERIC(10,2) NOT NULL
);
```

> **El modelo conceptual dice QUÉ.** El modelo relacional dice **CÓMO.**

---

---

## 7️⃣ Reglas de Transformación — La receta paso a paso

---

### ¿Qué son?

Son las **recetas** para convertir un diagrama ER en tablas SQL. Es un proceso **mecánico**: si sigues las reglas, el resultado es correcto.

> **Piénsalo como cocinar:** Si tienes la receta y los ingredientes, solo tienes que seguir los pasos. No necesitas creatividad, solo disciplina.

---

### Las 6 reglas — En orden

---

### Regla 1: Entidad → Tabla

> Cada entidad del diagrama se convierte en una tabla.

```
Diagrama ER:          SQL:
┌──────────┐          CREATE TABLE clientes (
│ CLIENTE  │    →       ...
└──────────┘          );
```

> **Tan simple como:** 1 rectángulo = 1 tabla.

---

### Regla 2: Atributo → Columna

> Cada atributo de la entidad se convierte en una columna con su tipo de dato.

```
Diagrama ER:                    SQL:
  nombre (texto)          →     nombre VARCHAR(80) NOT NULL
  email (texto único)     →     email VARCHAR(120) UNIQUE
  fecha_nac (fecha)       →     fecha_nac DATE
  activo (sí/no)          →     activo BOOLEAN DEFAULT TRUE
```

> **Fíjate:** Cada atributo además necesita un **tipo de dato** y posibles **restricciones**. En el diagrama ER no aparecen, pero al pasar a SQL sí debemos decidirlos.

---

### Regla 3: Identificador → Clave Primaria

> El identificador único de cada entidad se convierte en la PRIMARY KEY.

```
Diagrama ER:                    SQL:
  ID (identificador)      →     id SERIAL PRIMARY KEY
```

---

### Regla 4: Relación 1:N → Clave Foránea

> La relación se implementa poniendo una FK en la tabla del lado "muchos".

```
Diagrama ER:                    SQL:
  Cliente ──1:N── Pedido  →     CREATE TABLE pedidos (
                                  ...
                                  id_cliente INT NOT NULL,
                                  FOREIGN KEY (id_cliente)
                                    REFERENCES clientes(id)
                                );
```

> **¿Dónde va la FK?** Siempre en la tabla del lado **N** (el hijo, el "muchos").
>
> **Truco:** Pregúntate _"¿quién pertenece a quién?"_. El que **pertenece** lleva la FK. El pedido _pertenece a_ un cliente → la FK va en `pedidos`.

---

### Regla 5: Relación N:M → Tabla Intermedia

> Se crea una nueva tabla con las FKs de ambas entidades.

```
Diagrama ER:                        SQL:
  Estudiante ──N:M── Curso    →     CREATE TABLE inscripciones (
                                      id SERIAL PRIMARY KEY,
                                      id_estudiante INT REFERENCES estudiantes(id),
                                      id_curso INT REFERENCES cursos(id)
                                    );
```

---

### Regla 6: Nombres y convenciones

| Convención                           | ✅ Ejemplo bueno   | ❌ Ejemplo malo          |
| ------------------------------------ | ------------------ | ------------------------ |
| Tablas en **plural**, minúsculas     | `clientes`         | `Cliente`, `CLIENTES`    |
| Columnas en **singular**, snake_case | `fecha_registro`   | `FechaRegistro`, `FECHA` |
| PKs como `id` o `tabla_id`           | `id`, `cliente_id` | `ID_CLIENTE`, `pk`       |
| FKs con prefijo `id_`                | `id_cliente`       | `cliente`, `fk_cli`      |

---

### Ejemplo completo de transformación — Universidad

**Paso 1: El diagrama ER (modelo conceptual):**

```
 ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
 │  ESTUDIANTE  │──1:N─── │ INSCRIPCIÓN  │───N:1───│    CURSO     │
 │              │         │  (tabla      │         │              │
 │  id PK       │         │  intermedia) │         │  id PK       │
 │  nombre      │         │              │         │  nombre      │
 │  email       │         │ fecha        │         │  descripcion │
 └──────────────┘         │ nota         │         └──────────────┘
                          └──────────────┘               │
                                                        N:1
                                                         │
  ¿Cómo leo este diagrama?                        ┌──────────────┐
                                                   │   PROFESOR   │
  ▸ Un ESTUDIANTE puede inscribirse                │              │
    en MUCHOS cursos (N:M → tabla intermedia)      │  id PK       │
  ▸ Un CURSO es enseñado por UN profesor (N:1)     │  nombre      │
  ▸ INSCRIPCIÓN es la tabla puente que             │  titulo      │
    resuelve la relación N:M                       └──────────────┘
```

**Paso 2: Aplicamos las reglas de transformación:**

| Regla | Qué hago                                                           | Resultado                                                |
| ----- | ------------------------------------------------------------------ | -------------------------------------------------------- |
| R1    | Cada entidad → tabla                                               | 4 tablas: estudiantes, profesores, cursos, inscripciones |
| R2    | Cada atributo → columna                                            | nombre → VARCHAR, email → VARCHAR, etc.                  |
| R3    | Cada identificador → PK                                            | `id SERIAL PRIMARY KEY` en cada tabla                    |
| R4    | Relación N:1 (Curso→Profesor) → FK en Curso                        | `id_profesor INT REFERENCES profesores(id)` en cursos    |
| R5    | Relación N:M (Estudiante↔Curso) → tabla intermedia `inscripciones` | 2 FKs dentro de inscripciones                            |

**Paso 3: El resultado en SQL:**

```sql
-- Regla 1: Cada entidad → tabla
-- Regla 3: Identificador → PK
-- Regla 2: Atributos → columnas

CREATE TABLE estudiantes (
  id      SERIAL PRIMARY KEY,         -- R3: Identificador → PK
  nombre  VARCHAR(80) NOT NULL,       -- R2: Atributo → columna
  email   VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE profesores (
  id      SERIAL PRIMARY KEY,
  nombre  VARCHAR(80) NOT NULL,
  titulo  VARCHAR(50)
);

-- Regla 4: Relación N:1 → FK en el lado "muchos"
CREATE TABLE cursos (
  id            SERIAL PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  descripcion   TEXT,
  id_profesor   INT NOT NULL,                            -- R4: FK
  FOREIGN KEY (id_profesor) REFERENCES profesores(id)    -- ← apunta al profesor
);

-- Regla 5: Relación N:M → tabla intermedia con 2 FKs
CREATE TABLE inscripciones (
  id              SERIAL PRIMARY KEY,
  id_estudiante   INT NOT NULL,                                -- FK #1
  id_curso        INT NOT NULL,                                -- FK #2
  fecha           TIMESTAMP DEFAULT NOW(),
  nota            NUMERIC(3,1),
  FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id),      -- ← apunta al estudiante
  FOREIGN KEY (id_curso) REFERENCES cursos(id)                 -- ← apunta al curso
);
```

---

---

## 8️⃣ Normalización de Datos

---

### ¿Qué es normalizar?

> Normalizar = **organizar las tablas para eliminar datos repetidos** y evitar problemas de consistencia.

---

### La analogía: La mudanza 📦

Imagina que tienes UNA caja enorme con TODA tu ropa mezclada: poleras con calcetines, pantalones con gorros. ¿Qué haces?

**Organizas en cajas separadas:**

- Caja 1: Poleras
- Caja 2: Pantalones
- Caja 3: Calcetines

Normalizar una base de datos es lo mismo: **separar los datos en tablas lógicas** para que cada tabla tenga UN tema claro.

---

### ¿Qué pasa si NO normalizas? — Los 4 problemas

Imagina que guardas TODO en una sola tabla (datos del cliente + datos del pedido + datos del producto, todo junto):

```
Tabla "todo_junto" (MAL ❌):

| pedido | cliente  | email_cliente   | producto   | precio | cantidad |
|--------|----------|-----------------|------------|--------|----------|
| 001    | Juan     | juan@mail.com   | Notebook   | 599990 | 1        |
| 002    | Juan     | juan@mail.com   | Mouse      | 15990  | 2        |
| 003    | Ana      | ana@mail.com    | Notebook   | 599990 | 1        |
| 004    | Juan     | juan@mial.com   | Teclado    | 29990  | 1        |
                     ↑↑↑ alguien escribió "mial" en vez de "mail" ↑↑↑
```

> **¿Qué pasó?** Como los datos de Juan se copian en CADA pedido, alguien (o algún sistema) ingresó mal el email en el pedido 004: escribió `juan@mial.com` en vez de `juan@mail.com`. Es un **error de tipeo** que ahora parece un dato real.
>
> Si el email de Juan viviera en **una sola tabla aparte**, este error no podría ocurrir — habría UN solo lugar donde está ese dato.

**Los 4 problemas concretos que causa mezclar todo:**

| #   | Problema                      | ¿Qué pasa?                                                            | Ejemplo en la tabla                                         |
| --- | ----------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1   | **Redundancia**               | Los mismos datos se copian una y otra vez                             | "Juan" + "juan@mail.com" aparece en 3 filas                 |
| 2   | **Inconsistencia**            | Al copiar muchas veces, alguien puede escribirlo mal                  | Fila 004: `mial` en vez de `mail` → ¿cuál es el correcto?   |
| 3   | **Anomalía de eliminación**   | Si borro un pedido, puedo perder datos del cliente                    | Si borro pedido 003, pierdo TODA la info de Ana             |
| 4   | **Anomalía de actualización** | Si Juan cambia su email, debo buscarlo y cambiarlo en TODAS las filas | Hay que actualizar filas 001, 002 y 004 — ¿y si olvido una? |

> **Conclusión:** El problema de fondo es que **los datos del cliente están MEZCLADOS con los datos del pedido**. Si Juan estuviera en su propia tabla `clientes`, su email existiría en UN solo lugar y estos 4 problemas no ocurrirían. Eso es normalizar: **separar cada tema en su propia tabla**.

---

### Las 3 Formas Normales — ¿De dónde vienen y qué significan?

---

### Un poco de historia: ¿Quién inventó esto?

En **1970**, un matemático británico llamado **Edgar F. Codd** trabajaba en IBM y publicó un paper revolucionario: _"A Relational Model of Data for Large Shared Data Banks"_ (Un modelo relacional de datos para grandes bancos de datos compartidos).

En ese paper, Codd propuso que los datos se organizaran en **tablas** (lo que hoy es obvio, pero en 1970 era una idea radical). Y para asegurarse de que las tablas estuvieran **bien diseñadas**, definió un conjunto de reglas que llamó **"Formas Normales"**.

> **¿Por qué se llaman "Formas Normales"?**
>
> En matemáticas, "forma normal" significa **una forma estandarizada y simplificada** de representar algo. Es como decir "la forma correcta y ordenada". Codd tomó el término de la lógica matemática.
>
> Piénsalo así: cuando tu mamá te dice _"ordena tu pieza"_, hay niveles:
>
> - **1er nivel:** Al menos que no haya ropa en el piso
> - **2do nivel:** Que cada cosa esté en su cajón correspondiente
> - **3er nivel:** Que nada esté mal clasificado
>
> Cada "Forma Normal" es un **nivel de orden** más exigente que el anterior.

```
  ¿Quién lo inventó?     Edgar F. Codd (IBM, 1970)
  ¿Por qué "Normal"?     Viene de la lógica matemática = "forma ordenada/estándar"
  ¿Cuántas hay?           Codd definió 3 principales (existen más, pero con estas 3 basta)
```

---

### ¿Cómo funcionan? — Son niveles progresivos

Las formas normales son como **escalones**: para llegar al 2do piso, primero tienes que pasar por el 1ro. Para llegar al 3ro, primero pasas por el 2do.

```
  Sin normalizar  →  1NF  →  2NF  →  3NF
  (caos total)       │        │        │
                     │        │        └── 3️⃣ Que nada dependa de otro dato no-clave
                     │        └── 2️⃣ Que todo dependa de TODA la PK
                     └── 1️⃣ Un solo valor por celda

  Cada nivel INCLUYE las reglas del anterior:
    ▸ 2NF = cumple 1NF + su propia regla
    ▸ 3NF = cumple 1NF + 2NF + su propia regla
```

---

---

### 1️⃣ Primera Forma Normal (1NF) — "Una cosa por celda"

**Inventada por Codd en 1970** junto con el modelo relacional.

> **Regla**: Cada celda debe contener **un solo valor atómico** (indivisible).

**Analogía del locker 🔐:** Imagina que en el colegio tienes un casillero y metes TODO adentro: mochila, pelota, libros, almuerzo, todo apretado. ¿Puedes encontrar rápido tu libro de matemáticas? No. La 1NF dice: **un objeto por casillero**.

**❌ Mal (viola 1NF):**

| estudiante | cursos                       |
| ---------- | ---------------------------- |
| Juan       | Matemáticas, Física, Química |
| Ana        | Historia, Inglés             |

> **¿Cuál es el problema concreto?** La celda "Matemáticas, Física, Química" tiene **3 valores** metidos en una sola celda. ¿Cómo buscas a todos los que cursan Física? Tendrías que usar un `LIKE '%Física%'`, que es frágil (¿y si alguien escribió "fisica" sin tilde?) y lento.

**✅ Bien (cumple 1NF) — cada celda tiene UN solo valor:**

| estudiante | curso       |
| ---------- | ----------- |
| Juan       | Matemáticas |
| Juan       | Física      |
| Juan       | Química     |
| Ana        | Historia    |
| Ana        | Inglés      |

**Receta para 1NF:** Si una celda tiene una lista separada por comas → separa en filas individuales.

> **Dato:** Ahora puedes hacer `SELECT * FROM cursos WHERE curso = 'Física'` y funciona perfecto. Limpio y rápido.

---

### 2️⃣ Segunda Forma Normal (2NF) — "Todo depende de TODA la clave"

**También propuesta por Codd en 1971**, como refinamiento de la 1NF.

> **Regla**: Cumple 1NF + cada columna que **no es clave** debe depender de **toda** la clave primaria, no solo de una parte.

> **⚠️ Importante:** Este problema **solo existe** cuando la PK es **compuesta** (tiene más de una columna). Si tu PK es un solo `id` autoincremental, ya cumples 2NF automáticamente sin hacer nada.

**Analogía de la receta de cocina 🍳:** Imagina una receta que dice "para el plato de tallarines con salsa: usar sal fina". ¿La sal depende del plato completo (tallarines + salsa) o solo de la salsa? Solo de la salsa. Entonces la instrucción "usar sal fina" debería estar en la receta de la **salsa**, no en la del plato completo.

**❌ Mal (viola 2NF):**

La PK es **(nro_pedido + producto)** — o sea, la clave tiene **dos partes**:

| nro_pedido | producto | cantidad | nombre_cliente |
| ---------- | -------- | -------- | -------------- |
| 001        | Notebook | 1        | Juan           |
| 001        | Mouse    | 2        | Juan           |
| 002        | Notebook | 1        | Ana            |

> **¿Cuál es el problema?** Hagamos la pregunta:
>
> - `cantidad` → ¿de qué depende? Del pedido **Y** del producto (1 Notebook del pedido 001). ✅ Depende de **toda** la PK.
> - `nombre_cliente` → ¿de qué depende? Solo del `nro_pedido`. Juan es Juan sin importar si compró Notebook o Mouse. ❌ Depende de **solo una parte** de la PK.

**✅ Bien (cumple 2NF) → Separar en dos tablas:**

**Tabla `pedidos`** (lo que depende solo de `nro_pedido`):

| nro_pedido | nombre_cliente |
| ---------- | -------------- |
| 001        | Juan           |
| 002        | Ana            |

**Tabla `detalle_pedidos`** (lo que depende de `nro_pedido + producto`):

| nro_pedido | producto | cantidad |
| ---------- | -------- | -------- |
| 001        | Notebook | 1        |
| 001        | Mouse    | 2        |
| 002        | Notebook | 1        |

**Receta para 2NF:** Pregúntate _"¿este dato depende de TODA la clave o solo de una parte?"_. Si depende solo de una parte → muévelo a su propia tabla.

---

### 3️⃣ Tercera Forma Normal (3NF) — "Nada depende de otro dato que no sea la clave"

**Propuesta por Codd en 1971**, completando la trilogía de formas normales básicas.

> **Regla**: Cumple 2NF + ninguna columna no-clave debe depender de OTRA columna no-clave.

> Este tipo de problema se llama **"dependencia transitiva"**: A depende de B, y B depende de C. Es como una cadena: si tiras de un eslabón, se mueve el siguiente.

**Analogía del juego del teléfono 📞:** En el juego del teléfono, el mensaje pasa de persona en persona y se distorsiona. Lo mismo pasa en una tabla: si un dato depende de otro dato (que a su vez depende de la clave), la información rebota y se puede corromper.

**❌ Mal (viola 3NF):**

| empleado | departamento | ubicacion_depto |
| -------- | ------------ | --------------- |
| Juan     | Ventas       | Santiago        |
| Ana      | Marketing    | Valparaíso      |
| Pedro    | Ventas       | Santiago        |

> **¿Cuál es la cadena?** Sigamos las dependencias:
>
> ```
> empleado   →  departamento   →  ubicacion_depto
>  (PK)          (no es PK)        (no es PK)
>   Juan    →    Ventas       →    Santiago
> ```
>
> La `ubicacion_depto` **NO depende del empleado** directamente. Depende del **departamento**, que a su vez depende del empleado. Eso es una dependencia **transitiva** (indirecta).
>
> **Problema real:** Si "Ventas" se muda de Santiago a Concepción, tienes que actualizar TODAS las filas donde aparece "Ventas". ¿Y si olvidas una?

**✅ Bien (cumple 3NF) → Cada dato depende directamente de SU propia clave:**

**Tabla `empleados`:**

| empleado | departamento |
| -------- | ------------ |
| Juan     | Ventas       |
| Ana      | Marketing    |
| Pedro    | Ventas       |

**Tabla `departamentos`:**

| departamento | ubicacion  |
| ------------ | ---------- |
| Ventas       | Santiago   |
| Marketing    | Valparaíso |

Ahora si "Ventas" se muda, solo cambias **1 fila** en la tabla `departamentos`. Limpio.

**Receta para 3NF:** Si un dato depende de otro dato que NO es la clave → muévelo a su propia tabla.

---

---

### Resumen de las 3 Formas Normales

| Forma Normal | Año  | Problema que resuelve               | Regla en una frase                            | Pregunta para detectarlo                                   |
| ------------ | ---- | ----------------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| **1NF**      | 1970 | Listas metidas en una celda         | Cada celda = **un solo valor**                | _¿Hay comas o listas dentro de una celda?_                 |
| **2NF**      | 1971 | Datos que dependen de parte de PK   | Todo depende de **TODA** la PK                | _¿Este dato depende de toda la clave o solo de una parte?_ |
| **3NF**      | 1971 | Datos que dependen de otro no-clave | Nada depende de otra columna que no sea la PK | _¿Este dato depende de otro dato que no es PK?_            |

> **Frase clásica para recordar 3NF** (atribuida a Bill Kent, 1983):
> _"Cada dato debe depender de la clave, de toda la clave, y de nada más que la clave."_
>
> - "de la clave" → 1NF (existe una clave que identifica cada fila)
> - "de **toda** la clave" → 2NF
> - "de **nada más** que la clave" → 3NF

**Diagrama de decisión rápido:**

```
¿Tu tabla tiene listas en una celda?                → Aplica 1NF
               ↓ no
¿Un dato depende solo de PARTE de la PK?            → Aplica 2NF
               ↓ no
¿Un dato depende de otro dato que no es la clave?   → Aplica 3NF
               ↓ no
✅ ¡Tu tabla está normalizada!
```

---

---

## 📋 Resumen General

---

### Del problema real a la base de datos: El camino completo

```
 1. 👀 OBSERVAR la realidad
        ↓
 2. 🧠 ABSTRAER (quedarse con lo importante)
        ↓
 3. ✏️  MODELAR (diagrama ER: entidades + atributos + relaciones)
        ↓
 4. 🔄 TRANSFORMAR (aplicar reglas: entidades → tablas, relaciones → FKs)
        ↓
 5. 🧹 NORMALIZAR (eliminar redundancia: 1NF → 2NF → 3NF)
        ↓
 6. 💻 IMPLEMENTAR (escribir SQL: CREATE TABLE)
```

> **Recuerda:** Cada paso se apoya en el anterior. Si el diagrama ER está mal diseñado, las tablas SQL también lo estarán. ¡Por eso el diseño es tan importante!

---

### Tabla de conceptos clave

| Concepto              | Definición rápida                                   | ¿Dónde lo vimos?    |
| --------------------- | --------------------------------------------------- | ------------------- |
| **Modelo ER**         | Diagrama que representa datos y relaciones          | Sección 1           |
| **Entidad**           | Objeto del mundo real que queremos registrar        | Sección 3           |
| **Atributo**          | Propiedad de una entidad                            | Sección 3           |
| **Relación**          | Conexión entre entidades (1:1, 1:N, N:M)            | Sección 4           |
| **PK**                | Clave primaria: identifica cada fila de forma única | Sección 3           |
| **FK**                | Clave foránea: conecta una tabla con otra           | Sección 7 (Regla 4) |
| **Entidad fuerte**    | Independiente, tiene PK propia                      | Sección 5           |
| **Entidad débil**     | Depende de otra, PK incluye FK del padre            | Sección 5           |
| **Tabla intermedia**  | Resuelve relaciones N:M con dos FKs                 | Sección 4           |
| **1NF**               | Un valor por celda                                  | Sección 8           |
| **2NF**               | Todo depende de toda la PK                          | Sección 8           |
| **3NF**               | Nada depende de columnas no-clave                   | Sección 8           |
| **Modelo conceptual** | Diagrama abstracto (para todos)                     | Sección 6           |
| **Modelo relacional** | Tablas SQL concretas (para técnicos)                | Sección 6           |

---
