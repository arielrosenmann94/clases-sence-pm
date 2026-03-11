# Django — Módulo 7 · Clase 1

## Práctica: Menú Digital de Restaurante

---

> ⚠️ **PROHIBIDO ejecutar `migrate` sin la opción `--fake`. La base de datos ya existe y no puede ser modificada por Django bajo ninguna circunstancia.**

---

## El objetivo

Conectar un proyecto Django a una base de datos PostgreSQL existente, sin modificarla, y ver los datos del restaurante **"La Buena Mesa de Django"** en el panel de administración.

No se diseña la base de datos. No se corren consultas en el shell. La validación es simple: **abrir el admin en el navegador y ver los datos cargados**.

---

## Credenciales de la base de datos

El profesor te entrega los datos de conexión:

```
Motor:      PostgreSQL
Host:       db.pepuqhrltqfdagvhoxxc.supabase.co
Puerto:     5432
Nombre:     postgres
Usuario:    student_readonly
Contraseña: lectura123
```

> ℹ️ **NOTA IMPORTANTE:** El usuario `student_readonly` tiene permiso **solo de lectura**. El panel de administración de Django te mostrará botones para "Añadir" o "Eliminar" (porque eres Superusuario de Django), pero si intentas guardar cambios, la base de datos te dará un error de permiso denegado. Esta práctica es solo para visualizar datos existentes.

---

---

# Paso a paso

---

## Paso 1 — Crear el proyecto Django

Crea un proyecto Django nuevo. Luego crea dentro una aplicación que llamarás `menu`.

---

## Paso 2 — Configurar la conexión a la base de datos

En el archivo de configuración del proyecto (`settings.py`) hay que registrar dos cosas:

**Primera:** Agregar la aplicación `menu` a la lista de aplicaciones instaladas (`INSTALLED_APPS`).

**Segunda:** Configurar el bloque `DATABASES` con el motor PostgreSQL y las credenciales que te entregó el profesor.

---

## Paso 3 — Escribir los modelos

Dentro de la app `menu`, en el archivo `models.py`, debes definir cuatro clases. A continuación se describe cada una en palabras — el código lo escribes tú.

---

### Modelo 1 — Categoria

Representa una categoría del menú (Entradas, Principales, Postres, Bebidas).

**Campos:**

| Campo       | Tipo de dato               | Restricciones                |
| ----------- | -------------------------- | ---------------------------- |
| nombre      | Texto corto (máx 100 car.) | Obligatorio                  |
| descripcion | Texto largo                | Opcional — puede estar vacío |

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor              | Para qué sirve                                |
| ----------- | ------------------ | --------------------------------------------- |
| managed     | False              | Django no toca la tabla — ya existe           |
| db_table    | `'menu_categoria'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 2 — Alergeno

Representa un alérgeno (gluten, lácteos, mariscos, etc.).

**Campos:**

| Campo  | Tipo de dato               | Restricciones |
| ------ | -------------------------- | ------------- |
| nombre | Texto corto (máx 100 car.) | Obligatorio   |

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor             | Para qué sirve                                |
| ----------- | ----------------- | --------------------------------------------- |
| managed     | False             | Django no toca la tabla — ya existe           |
| db_table    | `'menu_alergeno'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 3 — Ingrediente

Representa un ingrediente. Cada ingrediente puede tener varios alérgenos, y un alérgeno puede estar en muchos ingredientes.

**Campos:**

| Campo     | Tipo de dato               | Restricciones                                                  |
| --------- | -------------------------- | -------------------------------------------------------------- |
| nombre    | Texto corto (máx 100 car.) | Obligatorio                                                    |
| alergenos | Relación muchos a muchos   | Apunta al modelo `Alergeno` — puede estar vacío (`blank=True`) |

Para la relación muchos a muchos, define el campo `ManyToManyField` apuntando al modelo `Alergeno`. Con `managed = False` activo, Django no va a intentar crear ni modificar ninguna tabla, por lo que la conexión se resolverá correctamente.

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor                | Para qué sirve                                |
| ----------- | -------------------- | --------------------------------------------- |
| managed     | False                | Django no toca la tabla — ya existe           |
| db_table    | `'menu_ingrediente'` | Nombre exacto de la tabla en la base de datos |

---

### Modelo 4 — Plato

El corazón del sistema. Cada plato es un ítem del menú.

**Campos:**

| Campo              | Tipo de dato                       | Restricciones y comportamiento                     |
| ------------------ | ---------------------------------- | -------------------------------------------------- |
| nombre             | Texto corto (máx 200 car.)         | Obligatorio                                        |
| descripcion        | Texto largo                        | Obligatorio                                        |
| precio             | Decimal (10 dígitos, 2 decimales)  | Obligatorio — usar DecimalField, no FloatField     |
| tiempo_preparacion | Número entero                      | Obligatorio — minutos de preparación               |
| disponible         | Booleano                           | Obligatorio — valor por defecto: True              |
| creado_en          | Fecha y hora                       | Se completa automáticamente al crear el registro   |
| categoria          | Relación muchos-a-uno (ForeignKey) | Apunta al modelo `Categoria` — `on_delete=PROTECT` |
| ingredientes       | Relación muchos a muchos           | Apunta al modelo `Ingrediente` — puede estar vacío |

Para la relación muchos a muchos con ingredientes, define el campo `ManyToManyField` apuntando al modelo `Ingrediente`. Con `managed = False` activo, Django no intentará crear ninguna tabla adicional.

**Configuración obligatoria (clase Meta):**

| Instrucción | Valor          | Para qué sirve                                |
| ----------- | -------------- | --------------------------------------------- |
| managed     | False          | Django no toca la tabla — ya existe           |
| db_table    | `'menu_plato'` | Nombre exacto de la tabla en la base de datos |

---

## Paso 4 — Registrar los modelos en el admin

En el archivo `admin.py` de la app `menu`, registra los cuatro modelos para que aparezcan en el panel de administración.

Para que la lista sea útil, configura cada modelo con al menos una columna visible. Las más útiles para cada uno:

| Modelo      | Columnas sugeridas para `list_display` |
| ----------- | -------------------------------------- |
| Categoria   | nombre                                 |
| Alergeno    | nombre                                 |
| Ingrediente | nombre                                 |
| Plato       | nombre, precio, disponible, categoria  |

---

## Paso 5 — Las migraciones

Genera las migraciones con el comando habitual. Como los modelos tienen `managed = False`, Django va a generar los archivos pero **no va a tocar las tablas** cuando apliques `migrate`.

Ejecuta las migraciones con la opción `--fake` para registrarlas como aplicadas sin ejecutar ningún SQL:

```
python manage.py makemigrations menu
python manage.py migrate --fake
```

---

## Paso 6 — Crear el superusuario

Para poder entrar al admin, necesitas una cuenta de administrador. Django tiene un comando para crearlo:

```
python manage.py createsuperuser
```

Elige el nombre de usuario, email y contraseña que quieras.

---

## Paso 7 — Instalar dependencias

Para que Django pueda hablar con una base de datos PostgreSQL, necesita un "traductor" o driver. El más común es `psycopg2`. Si no lo instalas, Django te dará un error al intentar conectar.

Ejecuta este comando en tu terminal (dentro de tu entorno virtual):

```bash
pip install psycopg2-binary
```

---

## Paso 8 — Iniciar el servidor y verificar

Inicia el servidor de desarrollo y abre el panel de administración en el navegador:

```
python manage.py runserver
```

Dirección del admin: `http://127.0.0.1:8000/admin/`

Ingresa con el superusuario que creaste. Si todo está bien configurado, deberías ver las cuatro secciones (Categorias, Alergenos, Ingredientes, Platos) con los datos del restaurante cargados.

---

## Validación

La práctica está completa cuando puedes mostrar al profesor:

- El admin abierto en el navegador con los cuatro modelos visibles
- Al hacer clic en "Platos", la lista muestra los 13 platos con sus categorías y precios
- Al hacer clic en cualquier plato, se ven todos sus datos incluyendo los ingredientes

No hay entrega de archivos. La validación es en pantalla.

---

## Solución de problemas comunes

Si al entrar al Admin y hacer clic en un modelo ves un error, no te asustes. Generalmente es uno de estos dos:

### 1. "Relation '...' does not exist"

**Qué significa:** Django está buscando una tabla que no existe con ese nombre.
**Solución:** Revisa el `db_table` dentro de la clase `Meta`. Debe ser exactamente igual al nombre de la tabla en Postgres (por ejemplo, `'menu_plato'`).

### 2. "Column '...' does not exist"

**Qué significa:** Django encontró la tabla, pero dentro de ella no hay una columna con el nombre que definiste en tu modelo.
**Solución:** Revisa el nombre del atributo en tu clase. Django usa el nombre del atributo como nombre de columna. Por ejemplo, si definiste `desc = models.TextField()` pero en la base de datos la columna se llama `descripcion`, fallará.

---
