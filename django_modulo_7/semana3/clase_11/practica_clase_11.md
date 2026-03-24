# 🛠️ Práctica Clase 11: Personalización Completa del Admin — Clínica Veterinaria "PatasFelices"

## Contexto del Proyecto

> _"El panel que Django te da es funcional desde el primer momento. Esta práctica lo convierte en tuyo."_

En la **Clase 10** construiste el proyecto `veterinaria_patasfelices` con la app `fichas` y tres modelos: `Dueno`, `Mascota` y `ConsultaMedica`. Configuraste el CRUD completo con vistas CBV, templates y rutas.

Hoy **continuamos sobre ese mismo proyecto** para convertir el panel de administración en una herramienta profesional, segura y 100% personalizada.

---

## ¿Qué vas a hacer?

1. Verificar que el proyecto de la Clase 9 esté funcionando correctamente.
2. Personalizar cómo se ven los modelos en el admin (columnas, filtros, buscador, ordenamiento).
3. Usar Inlines para editar mascotas y consultas desde la ficha del dueño.
4. Agregar acciones personalizadas al admin.
5. Cambiar el nombre, título y subtítulo del panel de administración.
6. Crear un usuario editor con permisos limitados.
7. Crear un grupo de permisos reutilizable.
8. Proteger vistas del CRUD con `@permission_required`.
9. Crear una página de error 403 personalizada.

---

---

# Paso 1 — Verificar que el proyecto de la Clase 9 funciona

---

**¿Por qué primero esto?** Antes de personalizar el admin, todo el proyecto anterior debe estar migrado y funcional. Si dejaste algo pendiente, este es el momento de corregirlo.

Con el entorno virtual activo, ejecuta:

```bash
python manage.py showmigrations
```

Todas las migraciones de la app `fichas` deben tener `[X]`. Si hay alguna pendiente:

```bash
python manage.py makemigrations
python manage.py migrate
```

Luego verifica que el servidor corre sin errores:

```bash
python manage.py runserver
```

Entra a `http://127.0.0.1:8000/duenos/` y a `http://127.0.0.1:8000/mascotas/` para confirmar que las listas del CRUD funcionan.

Cuando todo esté `[X]` y sin errores, continua.

---

---

# Paso 2 — Registro básico de modelos en el admin

---

**¿Por qué hace falta?** Los modelos existen en la base de datos, pero el admin de Django no los conoce hasta que los registras explícitamente en `admin.py`.

Abre `fichas/admin.py`. Debería tener un registro básico de la Clase 9. Si solo tiene `from django.contrib import admin`, debes importar tus modelos y registrarlos.

Lo que necesitas hacer:

1. Importar `Dueno`, `Mascota` y `ConsultaMedica` desde `models.py`.
2. Registrar cada uno con `admin.site.register()`.

**Verificación:** Corre el servidor, ve a `http://127.0.0.1:8000/admin/` e ingresa como superusuario. Debes ver una sección con la app `fichas` y los tres modelos listados.

> 💡 Si la lista muestra «Dueno object (1)», «Mascota object (1)»... significa que le falta el método `__str__` a tus modelos. Verifica que lo hayas agregado en la Clase 9.

---

---

# Paso 3 — Verificar los `__str__` de los modelos

---

**¿Por qué?** Sin `__str__`, el admin muestra nombres genéricos imposibles de distinguir. Con él, muestra texto legible y útil.

Abre `fichas/models.py` y verifica que **cada modelo** tenga su método `__str__` definido. Si alguno no lo tiene, agrégalo ahora. Por ejemplo:

- `Dueno` debería devolver el nombre del dueño.
- `Mascota` debería devolver algo como el nombre de la mascota junto con su especie.
- `ConsultaMedica` debería devolver el motivo junto con el nombre de la mascota.

> Agregar `__str__` no requiere nueva migración — es solo un método de Python, no crea columnas en la base de datos.

---

---

# Paso 4 — Personalizar la vista de cada modelo con `ModelAdmin`

---

**¿Por qué?** El registro básico funciona, pero la lista tiene una sola columna. Con `ModelAdmin` agregas columnas, buscador, filtros y ordenamiento en pocas líneas.

Ahora vamos a reemplazar el registro básico por uno personalizado usando el decorador `@admin.register()` y clases que hereden de `admin.ModelAdmin`.

### 4.1 — Personalizar `DuenoAdmin`

Para el modelo `Dueno`, configura:

| Opción          | Qué poner                                           | ¿Qué hace?                              |
| :-------------- | :-------------------------------------------------- | :-------------------------------------- |
| `list_display`  | Los campos más útiles: nombre, RUT, teléfono, email | Columnas visibles en la lista           |
| `search_fields` | Campos para buscar: nombre y RUT                    | Habilita el buscador arriba de la lista |
| `list_filter`   | (Opcional para Dueno)                               | Panel de filtros a la derecha           |
| `ordering`      | Por nombre alfabético                               | Orden por defecto de la lista           |

> 📖 **Referencia:** Documentación de [ModelAdmin.list_display](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)

### 4.2 — Personalizar `MascotaAdmin`

Para `Mascota`, configura:

| Opción          | Qué poner                                              |
| :-------------- | :----------------------------------------------------- |
| `list_display`  | nombre, especie, raza, y el **nombre del dueño**       |
| `search_fields` | nombre de la mascota y nombre del dueño                |
| `list_filter`   | especie (para poder filtrar por "Perro", "Gato", etc.) |
| `ordering`      | Por nombre alfabético                                  |

> 💡 Para mostrar el nombre del dueño como columna, necesitas definir un método dentro del `ModelAdmin` o usar la sintaxis `dueno__nombre` en `search_fields`. Para `list_display`, puedes poner directamente `'dueno'` — Django usará el `__str__` del modelo relacionado.

### 4.3 — Personalizar `ConsultaMedicaAdmin`

Para `ConsultaMedica`, configura:

| Opción            | Qué poner                                                    |
| :---------------- | :----------------------------------------------------------- |
| `list_display`    | mascota, motivo, fecha, costo                                |
| `search_fields`   | motivo, nombre de la mascota                                 |
| `list_filter`     | fecha (para filtrar por rango de fechas)                     |
| `ordering`        | Por fecha descendente (`-fecha`) — las más recientes primero |
| `readonly_fields` | fecha (porque usa `auto_now_add`, no se debe editar)         |

> 📖 **Referencia:** `readonly_fields` evita que un campo se pueda modificar desde el formulario del admin. Úsalo para campos automáticos. Documentación: [ModelAdmin.readonly_fields](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.readonly_fields)

**Verificación:** Guarda el archivo y recarga el admin. Cada modelo ahora muestra múltiples columnas, tiene buscador y filtros.

---

---

# Paso 5 — Agregar Inlines: editar mascotas desde la ficha del dueño

---

**¿Por qué?** Un Inline permite editar los registros hijos directamente desde la página del registro padre. En vez de ir a la lista de mascotas, buscar la mascota y editarla, puedes verlas **todas dentro de la ficha del dueño**.

### 5.1 — Inline de Mascotas en el Dueño

Crea una clase que herede de `admin.TabularInline` (formato tabla) o `admin.StackedInline` (formato apilado):

| Opción   | Qué configurar                                   |
| :------- | :----------------------------------------------- |
| `model`  | El modelo hijo: `Mascota`                        |
| `extra`  | Cuántos formularios vacíos mostrar (sugiero `1`) |
| `fields` | Los campos a mostrar en el inline                |

Luego agrégalo al `DuenoAdmin` con la opción `inlines`:

```
inlines = [MascotaInline]
```

### 5.2 — Inline de Consultas en la Mascota

Repite el proceso: crea un inline para `ConsultaMedica` y agrégalo a `MascotaAdmin`.

Para las consultas, usa `readonly_fields` en el inline para que el campo `fecha` no sea editable (ya que usa `auto_now_add`).

**Verificación:** Ve a la ficha de un dueño en el admin. Debajo de los campos del dueño deberías ver una tabla con sus mascotas y un formulario vacío para agregar una nueva. Lo mismo para las consultas dentro de la ficha de una mascota.

> 💡 **¿Cuándo usar `TabularInline` vs `StackedInline`?**
>
> - `TabularInline` → formato tabla, compacto, ideal cuando los hijos tienen pocos campos.
> - `StackedInline` → formato apilado, un formulario debajo del otro, mejor cuando hay muchos campos por registro.

---

---

# Paso 6 — Agregar acciones personalizadas al admin

---

**¿Por qué?** Django admin trae la acción "Eliminar seleccionados" por defecto. Pero puedes crear tus propias acciones para operaciones masivas.

### 6.1 — Acción: Marcar consultas como "Sin costo"

Dentro de `ConsultaMedicaAdmin`, crea un método que ponga el costo en `0` para todas las consultas seleccionadas:

1. Define un método que reciba `self`, `request` y `queryset`.
2. Dentro del método, usa `queryset.update(costo=0)` para actualizar masivamente.
3. Usa `self.message_user(request, "X consultas actualizadas")` para mostrar un mensaje de confirmación.
4. Dale un atributo `short_description` al método para que el admin muestre un nombre legible en el dropdown de acciones.
5. Agrega el método a la lista `actions` del `ModelAdmin`.

> 📖 **Referencia:** Documentación de [Admin actions](https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/)

### 6.2 — Acción: Exportar dueños seleccionados (texto)

Dentro de `DuenoAdmin`, crea una acción que imprima en consola (o muestre un mensaje) los nombres y RUTs de los dueños seleccionados. Esto es una introducción al concepto de exportación — más adelante podrían generar un CSV real.

**Verificación:** En la lista de consultas médicas, selecciona varias consultas, elige tu acción del dropdown y haz clic en "Ir". El costo debería ponerse en 0 y aparecerá el mensaje de confirmación.

---

---

# Paso 7 — Ponerle identidad al panel

---

**¿Por qué?** El admin dice «Django administration» por defecto. Tres líneas lo personalizan con la identidad de "PatasFelices".

Al **final** de `fichas/admin.py`, configura estas tres propiedades de `admin.site`:

| Propiedad     | ¿Qué controla?                                      | Ejemplo de valor                              |
| :------------ | :-------------------------------------------------- | :-------------------------------------------- |
| `site_header` | El encabezado grande en todas las páginas del admin | `"🐾 PatasFelices — Panel de Administración"` |
| `site_title`  | El título en la pestaña del navegador               | `"PatasFelices Admin"`                        |
| `index_title` | El subtítulo en la página de inicio del admin       | `"Gestión de Fichas Veterinarias"`            |

> ⚠️ **No uses nombres reales de personas en estos campos.** Usa el nombre de la empresa ficticia.

**Verificación:** Recarga el admin. El encabezado ahora muestra "PatasFelices" en vez de "Django administration".

---

---

# Paso 8 — Columnas calculadas (campos que no existen en el modelo)

---

**¿Por qué?** A veces necesitas mostrar información derivada que no es un campo directo del modelo. Por ejemplo, "cantidad de mascotas" de un dueño.

### 8.1 — Mostrar cantidad de mascotas en la lista de dueños

En `DuenoAdmin`, define un método que cuente las mascotas del dueño:

1. Crea un método llamado `cantidad_mascotas` que reciba `self` y `obj`.
2. Dentro, retorna `obj.mascota_set.count()`.
3. Dale un atributo `short_description = "Mascotas"` para la cabecera de la columna.
4. Agrega `'cantidad_mascotas'` a `list_display`.

### 8.2 — Mostrar costo total de consultas en la lista de mascotas

En `MascotaAdmin`, define un método similar que sume el costo de todas las consultas:

1. Crea un método `costo_total_consultas`.
2. Usa `obj.consultamedica_set.aggregate(total=Sum('costo'))` para sumar — necesitarás importar `Sum` desde `django.db.models`.
3. Retorna el total formateado como precio (ej: `$15.000`).
4. Agrégalo a `list_display`.

> 📖 **Referencia:** [ModelAdmin methods for list_display](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display)

**Verificación:** La lista de dueños ahora muestra una columna "Mascotas" con un número. La lista de mascotas muestra el costo total de sus consultas.

---

---

# Paso 9 — Crear un usuario editor con permisos limitados

---

**¿Por qué?** El superusuario tiene acceso total. Para dar acceso a un tercero (un asistente de la clínica, un pasante) es mejor crear un usuario específico con los permisos justos — sin poder borrar ni modificar usuarios.

**Desde el panel admin:**

1. Ve a `Admin → Autenticación y autorización → Usuarios → Agregar Usuario`.
2. Crea un usuario con nombre de usuario ficticio (ej: `asistente_clinica`) y contraseña segura.
3. Guarda — te llevará a la página de detalles del usuario.
4. Activa la casilla **"Es staff"** (sin esto, no puede entrar al admin).
5. **No** actives "Es superusuario".
6. Baja a la sección **Permisos del usuario**.
7. En el panel de permisos disponibles, busca los permisos de `fichas` y pasa solo estos a la derecha:
   - `fichas | dueno | Can view dueno`
   - `fichas | mascota | Can view mascota`
   - `fichas | consulta medica | Can view consultamedica`

> ⚠️ **No le des permisos de add, change ni delete todavía.** Solo `view`.

**Verificación:** Cierra sesión con el superusuario y entra con `asistente_clinica`. El panel mostrará los modelos pero sin botones de crear, editar ni eliminar.

---

---

# Paso 10 — Crear un grupo para los editores

---

**¿Por qué grupos?** Si en el futuro le das acceso a más personas de la clínica, no quieres repetir la asignación de permisos uno por uno. Un grupo centraliza los permisos.

**Desde el panel admin:**

1. Ve a `Admin → Autenticación y autorización → Grupos → Agregar Grupo`.
2. Nombre del grupo: `Editores Fichas`.
3. En el panel de permisos disponibles, busca y selecciona:
   - `fichas | dueno | Can view dueno` + `Can change dueno`
   - `fichas | mascota | Can add mascota` + `Can change mascota` + `Can view mascota`
   - `fichas | consulta medica | Can add consultamedica` + `Can change consultamedica` + `Can view consultamedica`
4. **No** incluyas permisos de `delete` — los editores no deben poder eliminar registros.
5. Guarda el grupo.

Ahora asigna el grupo al usuario editor:

1. Ve al usuario `asistente_clinica`.
2. En la sección `Grupos`, busca `Editores Fichas` y agrégalo.
3. Guarda.

El usuario ahora hereda todos los permisos del grupo. Si el grupo cambia, el usuario lo refleja automáticamente.

**Verificación:** Entra como `asistente_clinica`. Ahora puede ver y editar dueños, mascotas y consultas, pero **no puede eliminar** ningún registro. Tampoco ve la sección de usuarios ni grupos.

---

---

# Paso 11 — Proteger una vista del CRUD con permisos

---

**¿Por qué?** Las vistas CRUD que creaste en la Clase 9 son accesibles para cualquier persona. Ahora vamos a proteger la vista de eliminación para que solo quienes tengan el permiso adecuado puedan acceder.

### 11.1 — Proteger `DuenoDeleteView`

Abre `fichas/views.py`. Necesitas usar `PermissionRequiredMixin` (para CBV) en vez de decoradores.

Lo que debes hacer:

1. Importar `LoginRequiredMixin` y `PermissionRequiredMixin` desde `django.contrib.auth.mixins`.
2. Agregar ambos mixins a `DuenoDeleteView` **antes** de `DeleteView` en la herencia.
3. Definir `permission_required = 'fichas.delete_dueno'`.

El orden de herencia importa:

```
class DuenoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
```

> ⚠️ `LoginRequiredMixin` debe ir **primero** para que verifique la sesión antes que el permiso. Si `PermissionRequiredMixin` va primero, un usuario sin sesión recibiría un error de permisos en vez de ser redirigido al login.

### 11.2 — Repetir para `MascotaDeleteView`

Aplica la misma protección con `permission_required = 'fichas.delete_mascota'`.

**Verificación:**

| Prueba                                                          | Resultado esperado                     |
| :-------------------------------------------------------------- | :------------------------------------- |
| Entrar como `asistente_clinica` y visitar `/duenos/eliminar/1/` | Error 403 (acceso denegado)            |
| Entrar como superusuario y visitar `/duenos/eliminar/1/`        | Muestra la confirmación de eliminación |
| Sin sesión, visitar `/duenos/eliminar/1/`                       | Redirige al login                      |

---

---

# Paso 12 — Crear la página de error 403

---

**¿Por qué?** Sin un template propio, Django muestra una página genérica en inglés. Con un template personalizado, el error se integra al diseño de PatasFelices.

Crea el archivo `templates/403.html` que extienda de tu `base.html`:

El template debe contener:

- Un título grande "403".
- Un mensaje: "Acceso denegado — no tienes los permisos necesarios para ver esta página."
- Un botón o link que lleve de vuelta a la lista de dueños (`{% url 'fichas:dueno_lista' %}`).

> ⚠️ **Importante:** Para que Django use tu template personalizado, `DEBUG` debe estar en `False`. En modo desarrollo (`DEBUG=True`), Django muestra su propia página de error. Para probar el 403, cambia temporalmente `DEBUG = False` en `development.py` y agrega `'*'` a `ALLOWED_HOSTS`.

---

---

# Paso 13 — Prueba final del flujo completo

---

Realiza cada verificación antes de marcarla como completada:

**Con el superusuario:**

- [ ] Entrar al admin → ver los 3 modelos de `fichas` con columnas configuradas.
- [ ] La lista de `ConsultaMedica` muestra mascota, motivo, fecha y costo, ordenada por fecha descendente.
- [ ] La lista de `Dueno` muestra la columna calculada "Mascotas" con la cantidad.
- [ ] El encabezado del admin muestra "PatasFelices" (no «Django administration»).
- [ ] Al editar un dueño, se ven sus mascotas como inline.
- [ ] Al editar una mascota, se ven sus consultas como inline.
- [ ] La acción "Marcar como sin costo" funciona en la lista de consultas.
- [ ] Se puede crear, editar y eliminar en todos los modelos.
- [ ] Acceder a `/duenos/eliminar/1/` funciona correctamente.

**Con el usuario `asistente_clinica`:**

- [ ] Puede entrar al admin.
- [ ] Solo ve los modelos de `fichas` (no ve Usuarios ni Grupos).
- [ ] No ve el botón «Eliminar» en ningún modelo.
- [ ] Puede agregar y editar mascotas y consultas.
- [ ] Acceder a `/duenos/eliminar/1/` devuelve error 403.
- [ ] La página del 403 tiene el diseño de PatasFelices (no la página genérica).

**Sin sesión:**

- [ ] Intentar entrar a `/duenos/eliminar/1/` redirige al login.

---

---

# Checklist de entrega

---

- [ ] `admin.py` tiene los 3 modelos registrados con `@admin.register` y `ModelAdmin` personalizado.
- [ ] Cada `ModelAdmin` tiene `list_display`, `search_fields`, `list_filter` y `ordering` configurados.
- [ ] `ConsultaMedicaAdmin` tiene `readonly_fields` para el campo `fecha`.
- [ ] Existe un `TabularInline` de `Mascota` dentro de `DuenoAdmin`.
- [ ] Existe un `TabularInline` de `ConsultaMedica` dentro de `MascotaAdmin`.
- [ ] `DuenoAdmin` tiene una columna calculada `cantidad_mascotas`.
- [ ] Existe al menos una acción personalizada en `ConsultaMedicaAdmin`.
- [ ] El encabezado del admin muestra "PatasFelices" con `site_header`, `site_title` e `index_title`.
- [ ] Existe un usuario `asistente_clinica` (no superusuario) con permiso de staff.
- [ ] Existe el grupo `Editores Fichas` con los permisos correctos (sin delete).
- [ ] `DuenoDeleteView` y `MascotaDeleteView` usan `PermissionRequiredMixin`.
- [ ] Existe el template `templates/403.html` con el diseño del proyecto.
- [ ] Al entrar con `asistente_clinica` y visitar una URL de eliminación → muestra 403.
- [ ] Al entrar sin sesión y visitar una URL de eliminación → redirige al login.

---

---

# Puntos de extensión (opcionales)

---

Si terminaste antes de tiempo, prueba cualquiera de estas mejoras:

**Extensión A — Personalizar el admin de User**

Django registra el modelo `User` con su propio `UserAdmin`. Puedes personalizarlo desregistrando el default y registrando el tuyo:

1. Importa `UserAdmin` desde `django.contrib.auth.admin` y `User` desde `django.contrib.auth.models`.
2. Crea tu propia clase que herede de `UserAdmin` y modifica `list_display` y `list_filter`.
3. Desregistra `User` con `admin.site.unregister(User)` y re-registra con tu admin personalizado.

> 📖 **Referencia:** [Customizing the User admin](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#a-full-example)

**Extensión B — Señal que registra cambios**

Crea el archivo `fichas/signals.py` con una señal `post_save` para el modelo `Dueno` que imprima en la terminal si el dueño fue creado o actualizado. Activa la señal en el método `ready()` de `fichas/apps.py`.

> 📖 **Referencia:** Documentación de [Django signals](https://docs.djangoproject.com/en/stable/topics/signals/)

**Extensión C — Filtro personalizado en el admin**

Crea un filtro personalizado para la lista de mascotas que muestre "Con consultas" y "Sin consultas". Investiga `SimpleListFilter` en la documentación de Django.

---

## Preguntas para pensar después de terminar

- Si mañana le das acceso a un nuevo asistente de la clínica, ¿qué pasos harías para que tenga los mismos permisos? ¿Cuánto tiempo te tomaría con grupos vs. sin grupos?
- ¿Qué diferencia hay entre que la vista devuelva un 403 y que simplemente no muestre el botón?
- Si alguien tiene `view_dueno` pero no `change_dueno`, ¿puede editar desde el admin? ¿Y desde la vista pública?
- ¿En qué situación usarías un `TabularInline` en lugar de un `StackedInline`?
- ¿Por qué `readonly_fields` es importante para campos con `auto_now_add`?

---

> [!IMPORTANT]
> **Para la próxima clase:** Este proyecto seguirá creciendo. Asegúrate de tener el admin completamente personalizado y los permisos funcionando antes de avanzar.
