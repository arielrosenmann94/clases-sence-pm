# 📋 Evaluación Integradora: Alke Wallet

> **Módulo:** Fundamentos de Bases de Datos Relacionales
> **Proyecto:** Diseño e implementación de la base de datos de una billetera virtual (onda Mach o Tenpo)

---

## 🎯 Contexto del Proyecto

Eres parte de un equipo de desarrollo al que le cayó la mansa pega: **Alke Wallet** necesita que le diseñen su base de datos relacional. El sistema tiene que dejar que los usuarios puedan:

- Guardar y manejar sus lucas o criptos
- Pasarse plata entre ellos (hacerse transferencias)
- Tasar el historial de movimientos

Tu pega acá es armar el modelo, crear las tablas y tirarte las consultas necesarias para que esta cuestión ande joya.

---

## 📦 ¿Qué tengo que mandar?

### Archivos a entregar (Los entregables)

| Archivo                 | Formato aceptado                    | Contenido                                           |
| ----------------------- | ----------------------------------- | --------------------------------------------------- |
| **Documento principal** | `.docx` (Word) o `.md` (Markdown)   | Todas las sentencias SQL + los pantallazos          |
| **Script SQL**          | `.sql`                              | El archivo con todo el código listo para darle play |
| **Diagrama ER**         | `.png`, `.jpg`, `.pdf` o foto piola | El mono (Modelo Entidad-Relación) del sistema       |

> [!TIP]
> Podís subir tu tarea en **Word** (`.docx`) o en **Markdown** (`.md`), lo que te dé menos paja o te sea más cómodo. Si le ponís con Markdown, lo podís escribir al toque desde el mismo VS Code.

### Contenido obligatorio del documento (Las weás que no pueden faltar)

| #   | Elemento                 | ¿Qué tiene que llevar?                                                         |
| --- | ------------------------ | ------------------------------------------------------------------------------ |
| 1   | **Creación de la BD**    | La sentencia SQL pa' crear la base de datos `AlkeWallet`                       |
| 2   | **Creación de tablas**   | El DDL (`CREATE TABLE`) de las 3 tablas, con sus llaves y restricciones al día |
| 3   | **Inserción de datos**   | El DML (`INSERT`) con datos falsos (de prueba) en las 3 tablas                 |
| 4   | **Consultas requeridas** | Las 5 querys SQL que te detallo más abajo                                      |
| 5   | **Transaccionalidad**    | Mostrar que cachai usar `START TRANSACTION`, `COMMIT` y `ROLLBACK`             |
| 6   | **Diagrama ER**          | El diagrama completo pa' cachar cómo se conecta todo                           |
| 7   | **Pantallazos**          | Evidencia visual de que las weás corrieron sin dar jugo                        |

> [!IMPORTANT]
> El documento tiene que venir **ordenadito y bien etiquetado**, paso por paso. No me mandís un papiro sin forma, que se entienda la weá.

---

## 🗂️ Las 3 Entidades (Tablas)

Tenís que armar las siguientes tablas con sus atributos. Échale un buen ojo a los tipos de datos, llaves y cualquier restricción que creai que falte.

### Tabla `usuario`

| Atributo             | Rol            |
| -------------------- | -------------- |
| `user_id`            | Llave primaria |
| `nombre`             | —              |
| `correo_electronico` | —              |
| `contraseña`         | —              |
| `saldo`              | —              |

### Tabla `moneda`

| Atributo          | Rol            |
| ----------------- | -------------- |
| `currency_id`     | Llave primaria |
| `currency_name`   | —              |
| `currency_symbol` | —              |

### Tabla `transaccion` (La que mueve las lucas)

| Atributo           | Rol                       |
| ------------------ | ------------------------- |
| `transaction_id`   | Llave primaria            |
| `sender_user_id`   | Llave foránea → `usuario` |
| `receiver_user_id` | Llave foránea → `usuario` |
| `importe`          | —                         |
| `transaction_date` | —                         |

> [!TIP]
> **Pégate una buena cachá con las relaciones:** ¿Cómo chucha se amarra un usuario con la plata que está ocupando? Si una de las pruebas te pide "la moneda que eligió un loco", ¿qué columna extra le meterías a esto?

---

## ✅ Requerimientos Paso a Paso (Pa' que no te perdai)

### Paso 1 — Crear la Base de Datos

- Crear la base de datos `AlkeWallet` (con `CREATE DATABASE`)
- Seleccionarla pa' empezar a usarla
- Revisar que se haya creado bacán con `SHOW DATABASES;`

📸 **Pantallazo:** mostrando que la base de datos de verdad existe.

---

### Paso 2 — Crear las 3 Tablas (DDL)

Armar las tablas `usuario`, `moneda` y `transaccion` acordándote de:

- Achuntarle a los **tipos de datos** para cada columna
- Dejar claritas las **llaves primarias** (`PRIMARY KEY`)
- Amarrar las **llaves foráneas** (`FOREIGN KEY`) donde toque
- Aplicar restricciones pa' que no metan basura: `NOT NULL`, `UNIQUE`, `DEFAULT`, según veai conveniente
- Cachar el **orden de creación** (primero las tablas que mandan, después las parásitas que dependen de ellas)

📸 **Pantallazo:** resultado del `DESCRIBE` de cada tablita.

---

### Paso 3 — Chantarle Datos de Prueba (DML)

Meter chamullo en las 3 tablas pa' poder hacer las consultas después:

- Por lo menos **3 monedas** distintas
- Por lo menos **4 usuarios** con datos cualquiera
- Por lo menos **5 transacciones** entre los cabros

📸 **Pantallazo:** el resultado de hacerle un `SELECT * FROM` a cada tabla pa' tasar los datos ingresados.

---

### Paso 4 — Las 5 Consultas Obligatorias

Tírate las siguientes queries y ejecútalas:

| #   | Consulta                                                              | Tipo              |
| --- | --------------------------------------------------------------------- | ----------------- |
| 1   | Sacar el **nombre de la moneda** que eligió un usuario en particular  | `SELECT` + `JOIN` |
| 2   | Traer **todas las transacciones** que se han hecho                    | `SELECT`          |
| 3   | Ver todas las transacciones que ha hecho **un puro usuario**          | `SELECT` + filtro |
| 4   | **Cambiar** el correo electrónico de un loco                          | `UPDATE`          |
| 5   | **Pitearse** (eliminar) los datos de una transacción (la fila entera) | `DELETE`          |

📸 **Pantallazo:** el output de cada consulta corriendo filete.

> [!NOTE]
> Pa' las consultas 4 y 5 (el UPDATE y el DELETE), mándate un pantallazo del **antes** y el **después** pa' cachar que el cambio de verdad salvó.

---

### Paso 5 — Transaccionalidad (ACID)

Demuestra que cachai cómo funcionan las transacciones en SQL:

- Haz una **transferencia de lucas** entre dos socios usando:
  - `START TRANSACTION`
  - Las sentencias necesarias (descontarle a uno, sumarle al otro y registrar la movida)
  - `COMMIT` pa' dejar la weá firme
- Mándate un cagazo a propósito (ej. un **error de llave foránea**) y échate para atrás con un `ROLLBACK`

📸 **Pantallazo:** de la consola mostrando que el `COMMIT` o el `ROLLBACK` pasaron tiki taka.

---

### Paso 6 — Diagrama Entidad-Relación (ER)

Ármate el diagrama de cómo funciona la cuestión. Podís ocupar la mano que prefieras:

- **DBeaver** (salva caleta)
- [dbdiagram.io](https://dbdiagram.io)
- [drawSQL](https://drawsql.app)
- La extensión draw.io en el VS Code
- ✏️ **A lo vío (Dibujado a mano)** — pasa piola siempre y cuando tengai letra legible, no hagai un mamarracho y le saquís una buena foto a la weá.

**El diagrama tiene que mostrar sí o sí:**

- Las 3 tablas con todos sus campos
- Las relaciones entre ellas (cacha si es 1:N, N:M, etc.)
- Las PK y FK bien marcaditas pa' que no haya dudas

📸 **Pantallazo o exportación** del diagrama.

---

## 🔧 Herramientas apañadoras

| Herramienta                                | Pa' qué sirve                                         |
| ------------------------------------------ | ----------------------------------------------------- |
| DBeaver                                    | Pa' correr las sentencias SQL                         |
| Visual Studio Code                         | Pa' dejar ordenadito el archivo `.sql`                |
| Herramienta ER (dbdiagram, drawSQL, etc..) | Pa' puro hacer el mono (diagrama) de la base de datos |

---

## 📊 ¿Qué es lo que voy a tasar pa' la nota?

### Lo Técnico

| Criterio                   | Qué se revisa                                                            |
| -------------------------- | ------------------------------------------------------------------------ |
| **Diseño de la BD**        | Tablas bien armadas y que los tipos de datos no den jugo                 |
| **Integridad de datos**    | Buen uso del `NOT NULL`, `UNIQUE` y `DEFAULT`                            |
| **Llaves primarias**       | Tienen que estar todas las `PRIMARY KEY` presentes                       |
| **Integridad referencial** | Que las `FOREIGN KEY` estén bien puestas y las tablas conversen entre sí |
| **DDL**                    | Que los `CREATE DATABASE` y `CREATE TABLE` funquen                       |
| **DML**                    | Que los `INSERT`, `SELECT`, `UPDATE` y `DELETE` no se caigan             |

### Lo Estructural (ACID)

| Propiedad        | Qué significa                                            | Cómo me demuestras que cachai               |
| ---------------- | -------------------------------------------------------- | ------------------------------------------- |
| **A**tomicidad   | La transa se hace entera o cagaste, no hay medias tintas | `START TRANSACTION` + `COMMIT` / `ROLLBACK` |
| **C**onsistencia | Las reglas se respetan a lo maldito                      | Restricciones `FK`, `NOT NULL`, `UNIQUE`    |
| **I**solamiento  | Las transacciones ni se topan en mala                    | Usando bien la weá de transacciones         |
| **D**urabilidad  | Quedan guardadas hasta el fin de los tiempos             | Que la data viva después del `COMMIT`       |

---

> **💼 Portafolio:** Cabros, pónganle talento que este proyecto sirve caleta pa'l portafolio profesional. Déjenlo florcita y destaquen lo mejor de su pega pa' buscar la primera chamba o pa' mandarse las partes.
