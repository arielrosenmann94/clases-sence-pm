# 📋 Evaluación Integradora: Alke Wallet

> **Módulo:** Fundamentos de Bases de Datos Relacionales
> **Proyecto:** Diseño e implementación de la base de datos de un monedero virtual

---

## 🎯 Contexto del Proyecto

Sos parte de un equipo de desarrollo que recibió el encargo de **Alke Wallet** para diseñar su base de datos relacional. El sistema debe permitir a los usuarios:

- Almacenar y gestionar sus fondos
- Realizar transacciones entre usuarios
- Consultar el historial de transacciones

Tu trabajo es diseñar el modelo, crear las tablas e implementar las consultas necesarias para que el sistema funcione.

---

## 📦 ¿Qué Tengo que Entregar?

### Archivos a entregar

| Archivo                 | Formato aceptado                      | Contenido                                             |
| ----------------------- | ------------------------------------- | ----------------------------------------------------- |
| **Documento principal** | `.docx` (Word) o `.md` (Markdown)     | Todas las sentencias SQL + capturas de pantalla       |
| **Script SQL**          | `.sql`                                | Archivo con todas las sentencias listas para ejecutar |
| **Diagrama ER**         | `.png`, `.jpg`, `.pdf` o foto legible | Modelo Entidad-Relación del sistema                   |

> [!TIP]
> Podés entregar en **Word** (`.docx`) o en **Markdown** (`.md`), lo que te resulte más cómodo. Si elegís Markdown, podés escribirlo directamente desde VS Code.

### Contenido obligatorio del documento

| #   | Elemento                 | ¿Qué debe incluir?                                                             |
| --- | ------------------------ | ------------------------------------------------------------------------------ |
| 1   | **Creación de la BD**    | Sentencia SQL para crear la base de datos `AlkeWallet`                         |
| 2   | **Creación de tablas**   | Sentencias DDL (`CREATE TABLE`) de las 3 tablas con sus claves y restricciones |
| 3   | **Inserción de datos**   | Sentencias DML (`INSERT`) con datos de prueba en las 3 tablas                  |
| 4   | **Consultas requeridas** | Las 5 consultas SQL que se detallan más abajo                                  |
| 5   | **Transaccionalidad**    | Demostración de uso de `START TRANSACTION`, `COMMIT` y `ROLLBACK`              |
| 6   | **Diagrama ER**          | Modelo Entidad-Relación del sistema completo                                   |
| 7   | **Capturas de pantalla** | Evidencia de ejecución exitosa de cada sentencia                               |

> [!IMPORTANT]
> El documento debe estar **claramente organizado y etiquetado**, sección por sección, para evidenciar el proceso completo.

---

## 🗂️ Las 3 Entidades (Tablas)

Debés crear las siguientes tablas con sus atributos. Prestá atención a los tipos de datos, claves y restricciones que consideres necesarias.

### Tabla `usuario`

| Atributo             | Rol            |
| -------------------- | -------------- |
| `user_id`            | Clave primaria |
| `nombre`             | —              |
| `correo_electronico` | —              |
| `contraseña`         | —              |
| `saldo`              | —              |

### Tabla `moneda`

| Atributo          | Rol            |
| ----------------- | -------------- |
| `currency_id`     | Clave primaria |
| `currency_name`   | —              |
| `currency_symbol` | —              |

### Tabla `transaccion`

| Atributo           | Rol                       |
| ------------------ | ------------------------- |
| `transaction_id`   | Clave primaria            |
| `sender_user_id`   | Clave foránea → `usuario` |
| `receiver_user_id` | Clave foránea → `usuario` |
| `importe`          | —                         |
| `transaction_date` | —                         |

> [!TIP]
> **Pensá en las relaciones:** ¿Cómo se conecta un usuario con la moneda que utiliza? Si una de las consultas pide "la moneda elegida por un usuario", ¿qué columna adicional podrías necesitar?

---

## ✅ Requerimientos Paso a Paso

### Paso 1 — Crear la Base de Datos

- Crear la base de datos `AlkeWallet`
- Seleccionarla para uso
- Verificar la creación con `SHOW DATABASES;`

📸 **Captura:** resultado mostrando la base de datos creada

---

### Paso 2 — Crear las 3 Tablas (DDL)

Crear las tablas `usuario`, `moneda` y `transaccion` teniendo en cuenta:

- Elegir los **tipos de datos** apropiados para cada columna
- Definir las **claves primarias** (`PRIMARY KEY`)
- Definir las **claves foráneas** (`FOREIGN KEY`) donde corresponda
- Aplicar restricciones de **integridad**: `NOT NULL`, `UNIQUE`, `DEFAULT` según sea necesario
- Respetar el **orden de creación** correcto (primero las tablas que no dependen de otras)

📸 **Captura:** resultado de `DESCRIBE` de cada tabla

---

### Paso 3 — Insertar Datos de Prueba (DML)

Insertar registros en las 3 tablas para poder realizar las consultas:

- Al menos **3 monedas** distintas
- Al menos **4 usuarios** con datos variados
- Al menos **5 transacciones** entre distintos usuarios

📸 **Captura:** resultado de `SELECT * FROM` de cada tabla mostrando los datos insertados

---

### Paso 4 — Las 5 Consultas Requeridas

Escribir y ejecutar las siguientes consultas:

| #   | Consulta                                                                 | Tipo              |
| --- | ------------------------------------------------------------------------ | ----------------- |
| 1   | Obtener el **nombre de la moneda** elegida por un usuario específico     | `SELECT` + `JOIN` |
| 2   | Obtener **todas las transacciones** registradas                          | `SELECT`          |
| 3   | Obtener todas las transacciones realizadas por **un usuario específico** | `SELECT` + filtro |
| 4   | **Modificar** el correo electrónico de un usuario específico             | `UPDATE`          |
| 5   | **Eliminar** los datos de una transacción (fila completa)                | `DELETE`          |

📸 **Captura:** resultado de cada consulta ejecutada exitosamente

> [!NOTE]
> Para las consultas 4 y 5 (UPDATE y DELETE), incluí una captura **antes** y **después** de ejecutar la sentencia para evidenciar el cambio.

---

### Paso 5 — Transaccionalidad (ACID)

Demostrar el manejo transaccional de la base de datos:

- Implementar una **transferencia de fondos** entre dos usuarios usando:
  - `START TRANSACTION`
  - Las sentencias necesarias (actualizar saldos + registrar la transacción)
  - `COMMIT` para confirmar
- Simular un **error de integridad referencial** y revertir con `ROLLBACK`

📸 **Captura:** consola mostrando el `COMMIT` y/o `ROLLBACK` exitoso

---

### Paso 6 — Diagrama Entidad-Relación (ER)

Crear el diagrama ER del sistema. Podés usar alguna de estas opciones:

- **DBeaver** (recomendado)
- [dbdiagram.io](https://dbdiagram.io)
- [drawSQL](https://drawsql.app)
- Extensión draw.io en VS Code
- ✏️ **Dibujado a mano** — es válido siempre que sea con **letra legible y prolija**, y se entregue como foto clara

**El diagrama debe mostrar:**

- Las 3 entidades con sus atributos
- Las relaciones entre ellas con su cardinalidad (1:N, N:M, etc.)
- Las claves primarias y foráneas claramente identificadas

📸 **Captura o exportación** del diagrama ER

---

## 🔧 Herramientas

| Herramienta                                  | Uso                                                  |
| -------------------------------------------- | ---------------------------------------------------- |
| DBeaver                                      | Ejecutar las sentencias SQL                          |
| Visual Studio Code                           | Organizar el archivo `.sql` con todas las sentencias |
| Herramienta ER (dbdiagram, drawSQL, draw.io) | Crear el diagrama entidad-relación                   |

---

## 📊 ¿Qué se Evalúa?

### Aspectos Técnicos

| Criterio                   | Qué se verifica                                                       |
| -------------------------- | --------------------------------------------------------------------- |
| **Diseño de la BD**        | Tablas bien estructuradas con tipos de datos correctos                |
| **Integridad de datos**    | Uso correcto de `NOT NULL`, `UNIQUE`, `DEFAULT`                       |
| **Claves primarias**       | Toda tabla tiene su `PRIMARY KEY` bien definida                       |
| **Integridad referencial** | Las `FOREIGN KEY` están correctamente definidas y conectan las tablas |
| **DDL**                    | Sentencias `CREATE DATABASE`, `CREATE TABLE` correctas                |
| **DML**                    | Sentencias `INSERT`, `SELECT`, `UPDATE`, `DELETE` correctas           |

### Aspectos Estructurales (ACID)

| Propiedad        | Significado                                        | Cómo demostrarlo                            |
| ---------------- | -------------------------------------------------- | ------------------------------------------- |
| **A**tomicidad   | La transacción se ejecuta completa o no se ejecuta | `START TRANSACTION` + `COMMIT` / `ROLLBACK` |
| **C**onsistencia | Los datos siempre cumplen las reglas definidas     | Restricciones `FK`, `NOT NULL`, `UNIQUE`    |
| **I**solamiento  | Las transacciones no interfieren entre sí          | Uso correcto de transacciones               |
| **D**urabilidad  | Los datos persisten después de confirmar           | Los datos se mantienen tras el `COMMIT`     |

---

> **💼 Portafolio:** Este proyecto puede ser un gran agregado a tu portafolio profesional. Presentalo de manera clara y destacá los aspectos más relevantes de tu trabajo.
