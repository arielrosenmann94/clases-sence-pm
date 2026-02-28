# 🏗️ Django — Módulo 6 · Clase 5

## Práctica A — "Arquitecto por un día"

---

> _"Antes de escribir código, los buenos desarrolladores diseñan. Esta práctica empieza exactamente ahí."_

---

## Consigna

Sos el/la desarrollador/a principal de un nuevo proyecto. El cliente te presentó el siguiente brief. Tu tarea es **leer el brief con atención** y completar el **Documento de Decisiones Arquitectónicas** que sigue a continuación.

**No hay código que escribir.** El foco está en razonar cada decisión y justificarla.

---

## 📄 Brief del proyecto: "ReservaFácil"

**ReservaFácil** es una plataforma web para que **restaurantes, peluquerías y centros de estética** gestionen sus turnos y reservas online.

**Funcionalidades del sistema:**

- Los **negocios** pueden registrarse, configurar sus servicios (nombre, duración, precio) y ver su agenda de reservas.
- Los **clientes** pueden buscar negocios, ver los servicios disponibles con sus precios, y hacer una reserva eligiendo fecha y horario.
- Los negocios pueden **confirmar, reprogramar o cancelar** una reserva.
- El sistema envía un **email de confirmación** automático cuando una reserva es creada o modificada.
- Hay un **panel de administración** interno para gestionar negocios habilitados y ver estadísticas globales.

**Información técnica adicional:**

- El sistema va a tener **tres tipos de usuario**: administrador de la plataforma, dueño de negocio y cliente.
- En una segunda fase se va a construir una **app móvil** que consumirá los mismos datos.
- El proyecto va a desplegarse en un servidor real desde el primer mes.
- Los negocios pueden subir **fotos de sus instalaciones** y **foto de perfil** del local.

---

## 📋 Completa el Documento de Decisiones

Completa cada campo con el valor que elegirías y, en los campos marcados con 💬, **justifica brevemente tu decisión** (1-2 líneas).

---

### Estructura

| Decisión                       | Tu elección | 💬 Justificación |
| ------------------------------ | ----------- | ---------------- |
| Tipo de estructura             |             |                  |
| Carpeta de configuración       |             |                  |
| Carpeta de apps                |             |                  |
| Ubicación de templates         |             |                  |
| Settings separados por entorno |             |                  |
| Requirements separados         |             |                  |

---

### Apps del proyecto

> Define las apps que necesita el sistema. Para cada una, indica su nombre (con la convención elegida) y su responsabilidad principal.

| App | Responsabilidad principal |
| --- | ------------------------- |
|     |                           |
|     |                           |
|     |                           |
|     |                           |
|     |                           |

---

### Código

| Decisión                  | Tu elección |
| ------------------------- | ----------- |
| Idioma del código fuente  |             |
| Idioma de los comentarios |             |
| Idioma del contenido UI   |             |
| Nomenclatura de apps      |             |
| Estilo de vistas          |             |
| Namespaces en URLs        |             |

---

### Modelos

| Decisión                   | Tu elección | 💬 Justificación |
| -------------------------- | ----------- | ---------------- |
| Campo `created_at`         |             |                  |
| Campo `updated_at`         |             |                  |
| Soft delete (`is_active`)  |             |                  |
| Tipo de campo para precios |             |                  |

---

### Autenticación y Permisos

| Decisión                        | Tu elección | 💬 Justificación |
| ------------------------------- | ----------- | ---------------- |
| Modelo de usuario               |             |                  |
| `AUTH_USER_MODEL`               |             |                  |
| Campos extra en User            |             |                  |
| Sistema de roles                |             |                  |
| Roles del sistema (lista todos) |             |                  |
| Método de protección de vistas  |             |                  |

---

### Archivos de Medios

| Decisión                   | Tu elección | 💬 Justificación |
| -------------------------- | ----------- | ---------------- |
| Maneja archivos de medios  |             |                  |
| `MEDIA_URL` / `MEDIA_ROOT` |             |                  |
| `upload_to` para fotos     |             |                  |

---

### Entorno y Configuración

| Decisión                 | Tu elección |
| ------------------------ | ----------- |
| Variables de entorno     |             |
| `.gitignore` configurado |             |
| Base de datos local      |             |
| Base de datos producción |             |

---

### Signals

| Decisión                 | Tu elección | 💬 Justificación |
| ------------------------ | ----------- | ---------------- |
| ¿Usas signals?           |             |                  |
| ¿Para qué evento/acción? |             |                  |

---

### Tests

| Decisión               | Tu elección |
| ---------------------- | ----------- |
| ¿Tests obligatorios?   |             |
| ¿Qué se testea mínimo? |             |

---

## ✍️ Pregunta de reflexión final

> Contestala en 3-5 líneas al pie de este documento.

**¿Cambiarías alguna decisión si el cliente te dijera que el proyecto "es solo para probar si la idea funciona" y no tiene presupuesto para un servidor por ahora? ¿Cuáles y por qué?**

---

_Guardá este documento con tus respuestas completas antes de que el instructor lo corrija en clase._
