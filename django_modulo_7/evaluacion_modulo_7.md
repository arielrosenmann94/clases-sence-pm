# 📋 Evaluación del Módulo 7 — Acceso a Datos con Django

# 🏦 Proyecto: Alke Wallet

---

> 📎 **Documento original de la evaluación:**
>
> [Abrir en Google Docs](https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true)
>
> `https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true`

---

## 🎯 ¿De qué se trata?

La empresa fintech ficticia **Alke Financial** necesita una aplicación web para gestionar información de usuarios y operaciones financieras básicas. Tu trabajo es construir esa aplicación desde cero usando **Django + SQLite**, aplicando todo lo aprendido en las clases del módulo.

---

## 📦 ¿Qué debes entregar al final?

| # | Entregable | Formato |
|---|------------|---------|
| 1 | Proyecto Django completo | Carpeta comprimida `.zip` o `.rar` |
| 2 | Documento explicativo de tu modelo de datos | `.md` (dentro del zip) o `.pdf` (archivo aparte) |
| 3 | Capturas de pantalla de la app funcionando | Dentro del documento |

> ⚠️ Si entregas un `.pdf` debe ir **fuera** del zip como archivo aparte. Los `.md` van **dentro** del mismo `.zip` que representa el repositorio. Si no se entrega dentro de un `.zip` o `.rar`, no se puede revisar por la naturaleza del entorno de evaluación.

---

---

# 🚶 Paso a Paso: Lo que Debes Hacer (En Orden)

---

## Paso 1 — Crear el Proyecto Django

Crea un proyecto Django nuevo. Dentro del proyecto, crea una aplicación (app) que represente la wallet.

> 💡 **¿Qué es un proyecto vs una app?** Un proyecto Django es el contenedor principal (creado con `django-admin startproject`). Una app es un módulo dentro del proyecto que maneja una funcionalidad específica (creada con `python manage.py startapp`). Un proyecto puede tener muchas apps.

**Lo que se va a revisar:**
- Que el proyecto exista y se pueda ejecutar con `python manage.py runserver` sin errores.

---

## Paso 2 — Verificar la Base de Datos

Tu proyecto debe usar **SQLite**, que es la base de datos que Django trae por defecto. No necesitas instalar nada adicional.

> 💡 **¿Qué es SQLite?** Es una base de datos liviana que se guarda en UN solo archivo dentro de tu proyecto (el archivo `.sqlite3`). No necesita un servidor externo como PostgreSQL o MySQL. Django la trae configurada por defecto, así que si no tocas nada en `settings.py`, ya la tienes funcionando.

**Lo que debes hacer:**
- Abre tu archivo `settings.py` y confirma que la sección `DATABASES` apunte a SQLite.
- Al ejecutar el proyecto por primera vez, Django generará automáticamente un archivo `.sqlite3`. Ese archivo ES tu base de datos.

**Lo que se va a revisar:**
- Que la configuración en `settings.py` sea correcta.
- Que el archivo `.sqlite3` exista y se incluya en la entrega.

---

## Paso 3 — Diseñar y Crear los Modelos

Los modelos son las clases Python que representan las tablas de tu base de datos. Piensa en qué datos necesita una empresa fintech tipo wallet para funcionar.

> 💡 **¿Qué es un modelo?** Es una clase de Python que hereda de `models.Model`. Cada atributo de la clase se convierte en una columna de la tabla. Django se encarga de traducir esa clase a SQL por ti. Si creas una clase `Usuario` con un campo `nombre`, Django crea una tabla con una columna `nombre` en la base de datos.

**Lo que debes hacer:**
- Crear los modelos necesarios dentro de `models.py` de tu aplicación.
- Cada modelo debe tener campos con los tipos de datos que correspondan (`CharField`, `IntegerField`, `DecimalField`, `DateTimeField`, `BooleanField`, etc.).
- Cada campo debe tener las restricciones apropiadas (largo máximo, si puede ser nulo, si debe ser único, valores por defecto).

> 💡 **¿Cómo elijo el tipo de campo?** Piensa en el dato real: ¿Es texto? → `CharField`. ¿Es un número con decimales (como dinero)? → `DecimalField`. ¿Es una fecha? → `DateTimeField`. ¿Es verdadero o falso (como "cuenta activa")? → `BooleanField`.

**Lo que se va a revisar:**
- Que los modelos representen correctamente el dominio de una wallet financiera.
- Que los tipos de campo y restricciones tengan sentido.
- Que el código sea legible y siga las convenciones de Django.

---

## Paso 4 — Establecer Relaciones entre Modelos

Los modelos no existen solos. En una aplicación real, las entidades se conectan entre sí.

> 💡 **¿Qué es una relación?** Es cuando un modelo necesita "apuntar" a otro. Por ejemplo: una Transacción pertenece a un Usuario. Eso se modela con un `ForeignKey` en el modelo Transacción que apunta al modelo Usuario. Si borras al usuario, ¿qué pasa con sus transacciones? Eso lo define el parámetro `on_delete`.

**Lo que debes hacer:**
- Conectar tus modelos usando los campos de relación de Django: `ForeignKey`, `OneToOneField` o `ManyToManyField`, según corresponda a la lógica de tu aplicación.
- Definir qué pasa cuando se elimina un registro relacionado (parámetro `on_delete`).

**Lo que se va a revisar:**
- Que las relaciones sean lógicas y coherentes.
- Que `on_delete` esté definido en cada relación que lo requiera.

---

## Paso 5 — Generar y Aplicar Migraciones

Las migraciones convierten tus modelos de Python en tablas reales dentro de la base de datos.

> 💡 **¿Qué es una migración?** Es un archivo que Django genera automáticamente y que contiene las instrucciones SQL para crear o modificar tablas. Funciona como un "control de versiones" de tu base de datos: cada cambio que haces en los modelos genera una nueva migración que se puede aplicar o revertir.

**Lo que debes hacer:**
- Ejecutar el comando que genera las migraciones a partir de tus modelos.
- Ejecutar el comando que aplica esas migraciones a la base de datos.
- Si después de la primera migración modificas un modelo, debes volver a generar y aplicar una nueva migración.

**Lo que se va a revisar:**
- Que los archivos de migración existan dentro de la carpeta `migrations/` de tu app.
- Que las migraciones se apliquen sin errores.
- Que las tablas en la base de datos correspondan a tus modelos.

---

## Paso 6 — Construir las Vistas y Templates para CRUD

Tu aplicación debe permitir realizar las 4 operaciones fundamentales desde la interfaz web.

> ⚠️ **IMPORTANTE: El CRUD debe funcionar desde templates propios, NO solo desde el Admin de Django.**
>
> El Admin de Django (`/admin/`) es una herramienta generada automáticamente. Usarlo no demuestra que sepas usar el ORM. El objetivo de esta evaluación es que TÚ construyas las vistas y los templates que interactúan con la base de datos a través del ORM.

### ➕ Crear (Create)
- Un formulario en el navegador (un template `.html` que tú diseñaste) que permita agregar nuevos registros.
- Al enviar el formulario, la vista debe recibir los datos, usar el ORM para guardarlos en la base de datos, y redirigir al usuario.

### 👁️ Leer (Read)
- Una página que liste los registros almacenados (un template con un loop que muestre los datos).
- Una página que muestre el detalle de un registro individual.

### ✏️ Actualizar (Update)
- Un formulario que permita editar un registro existente (pre-cargado con los datos actuales).
- Al guardar, los cambios deben reflejarse en la base de datos.

### 🗑️ Eliminar (Delete)
- Un mecanismo (botón o enlace) que permita borrar un registro.
- El registro debe desaparecer de la base de datos después de eliminar.

**Lo que se va a revisar:**
- Que las 4 operaciones funcionen desde templates propios en el navegador.
- Que las vistas usen el ORM de Django (`.objects.create()`, `.filter()`, `.save()`, `.delete()`).
- Que los templates muestren los datos correctamente.
- Que el flujo sea: Template → Vista → ORM → Base de Datos (y de vuelta).

---

## Paso 7 — Implementar Filtros o Búsqueda en un Template

> ⚠️ **Este paso es OBLIGATORIO.** Es la forma en que verificamos que realmente sabes usar el ORM para consultar datos y no dependes exclusivamente del Admin.

Tu aplicación debe tener **al menos un template** que permita al usuario filtrar o buscar registros. Este template demuestra que sabes construir consultas dinámicas con el ORM.

> 💡 **¿Qué significa "filtrar"?** Significa que el usuario puede escribir un término de búsqueda o seleccionar un criterio, y la página le muestra solo los registros que coinciden. Por ejemplo: buscar transacciones por nombre de usuario, filtrar cuentas por tipo, o buscar operaciones por rango de fechas.

**Lo que debes hacer:**
- Crear un template que tenga un campo de búsqueda, un selector de filtro, o ambos.
- La vista asociada debe tomar el criterio del usuario y usarlo para construir una consulta con el ORM (usando `.filter()`, `Q()`, `.exclude()`, o similar).
- Los resultados filtrados deben mostrarse en el mismo template.

**Lo que se va a revisar:**
- Que exista al menos un template con funcionalidad de filtro o búsqueda.
- Que el filtro funcione correctamente (no muestre todos los registros siempre).
- Que la vista use el ORM para construir la consulta, NO SQL directo.

---

## Paso 8 — Configurar las URLs

Cada vista necesita una URL que la conecte con el navegador.

> 💡 **¿Cómo funciona?** Cuando un usuario escribe una dirección en el navegador (ej. `/wallet/transacciones/`), Django busca esa ruta en `urls.py` y ejecuta la vista asociada. Si la ruta no existe, Django muestra un error 404.

**Lo que debes hacer:**
- Definir las rutas en el archivo `urls.py` de tu aplicación.
- Cada operación CRUD debe tener su propia URL.
- El template de filtros/búsqueda también debe tener su URL.

**Lo que se va a revisar:**
- Que todas las URLs funcionen y lleven a la vista correcta.
- Que las rutas sean limpias y descriptivas.

---

## Paso 9 — Probar Todo

Antes de entregar, verifica que todo funcione como esperas.

**Lista de verificación final:**

- [ ] ¿El proyecto se ejecuta sin errores con `runserver`?
- [ ] ¿Los modelos tienen campos y relaciones correctas?
- [ ] ¿Las migraciones se aplican sin errores?
- [ ] ¿Puedo CREAR un registro desde mi template?
- [ ] ¿Puedo VER una lista de registros en mi template?
- [ ] ¿Puedo ver el DETALLE de un registro?
- [ ] ¿Puedo EDITAR un registro existente desde mi template?
- [ ] ¿Puedo ELIMINAR un registro desde mi template?
- [ ] ¿Los datos persisten después de cada operación?
- [ ] ¿Funciona el filtro o búsqueda en mi template?
- [ ] ¿Mi app tiene templates PROPIOS, no solo el Admin de Django?

---

## Paso 10 — Escribir el Documento Explicativo

Crea un archivo `.md` o `.pdf` que contenga:

1. **Tu modelo de datos:** Qué modelos creaste, qué campos tiene cada uno y cómo se relacionan.
2. **Las operaciones que implementaste:** Describe brevemente cómo funciona cada operación CRUD y el filtro/búsqueda.
3. **Capturas de pantalla:** Evidencia visual de tu aplicación funcionando (la lista, el formulario de creación, la edición, la eliminación, y el filtro funcionando).

---

## Paso 11 — Comprimir y Entregar

Comprime toda la carpeta del proyecto en un archivo `.zip` o `.rar` y entrégalo junto con tu documento explicativo.

> ⚠️ Si entregas un `.pdf`, va **fuera** del zip como archivo aparte. Los `.md` van **dentro** del zip que representa el repositorio.

---

---

# ❓ Preguntas de Cierre (Respóndelas en tu Documento)

Estas preguntas deben estar respondidas en tu documento explicativo. Son parte de la evaluación.

### Sobre los Modelos
1. ¿Qué modelos definiste y por qué elegiste esos? Justifica tu decisión.
2. ¿Qué tipo de relación usaste entre tus modelos (ForeignKey, OneToOne, ManyToMany)? ¿Por qué esa y no otra?
3. ¿Qué valor le pusiste a `on_delete` en tus relaciones y por qué?

### Sobre el ORM
4. ¿Qué métodos del ORM usaste para cada operación CRUD? Nombra al menos uno por operación.
5. ¿Qué método usaste en tu vista de filtro/búsqueda para construir la consulta?
6. ¿Cuál es la diferencia entre `.get()` y `.filter()`? ¿Cuándo usarías cada uno?

### Sobre las Migraciones
7. ¿Qué pasaría si modificas un modelo pero NO generas una nueva migración?
8. ¿Dónde se almacenan los archivos de migración y para qué sirven?

### Sobre la Arquitectura
9. ¿Por qué es importante que la lógica de base de datos esté en las VISTAS y no en los TEMPLATES?
10. ¿Cuál es el flujo completo de una solicitud en Django? (desde que el usuario hace clic hasta que ve el resultado)

---

---

# ⚠️ Errores Frecuentes que Debes Evitar

| Error | Consecuencia |
|-------|-------------|
| Crear modelos pero no aplicar migraciones | La base de datos no tendrá tablas y la app fallará |
| Olvidar `on_delete` en las ForeignKey | Django no te deja crear la migración |
| Hacer CRUD solo desde el Admin de Django | No demuestra uso del ORM. El requerimiento pide templates propios |
| No tener un template de filtro/búsqueda | Falta evidencia de consultas dinámicas con el ORM |
| No incluir el archivo `.sqlite3` en la entrega | El evaluador no podrá ver tus datos de prueba |
| No incluir capturas de pantalla | Falta evidencia de funcionamiento |
| Poner lógica de base de datos en los templates | Rompe la arquitectura de Django |
| No responder las preguntas de cierre | Son parte de la nota |

---

> 📎 **Documento original de la evaluación:**
>
> [Abrir en Google Docs](https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true)
>
> `https://docs.google.com/document/d/1g0Hi7zKQxi3IHm34P2md33iIYpyPIjSq/edit?usp=sharing&ouid=101914187946976947102&rtpof=true&sd=true`

---
