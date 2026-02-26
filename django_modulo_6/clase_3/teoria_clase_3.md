# 🐍 Django — Módulo 6 · Clase 3

### Teoría: Cómo piensa un programador Django (Resumen de Clase 1 y 2)

---

## Clase 3: qué vas a lograr hoy

Hoy no vamos a sumar una herramienta nueva de Django.

Hoy vas a hacer algo más importante para crecer como programador/a:

- ordenar lo aprendido en Clase 1 y Clase 2,
- entender cómo viaja la información en un proyecto Django,
- y preparar el terreno para ampliar el proyecto sin romper lo que ya funciona.

> Idea central: pasar de “seguir pasos” a “entender el sistema”.

---

## 1. Dónde estamos (qué ya construimos)

### En la Clase 1 construimos el flujo base de Django

Aprendimos a:

- crear proyecto y app,
- definir un modelo (`Producto`),
- hacer migraciones,
- usar el panel admin,
- crear vistas,
- conectar URLs,
- renderizar templates.

Eso nos dio el primer flujo completo **MVT** funcionando.

### En la Clase 2 profesionalizamos el proyecto

Aprendimos a:

- entender la anatomía del proyecto (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`),
- usar una estructura más clara (`config/`),
- mover lógica de negocio al modelo,
- trabajar con **sesiones** (carrito),
- usar **Forms** de Django,
- aplicar **herencia de templates** con `base.html`.

> Si la Clase 1 fue “hacer que funcione”, la Clase 2 fue “hacerlo mejor”.

---

## 2. Mapa del proyecto (pensar por capas)

Un proyecto Django básico se entiende mejor si lo lees por capas.

### A. Capa de configuración global (`config/`)

Aquí viven las reglas del proyecto completo.

- `settings.py`: configuración global (apps, base de datos, templates, idioma, seguridad, etc.)
- `urls.py`: enrutador principal del sitio
- `wsgi.py` / `asgi.py`: puntos de entrada del servidor

### B. Capa de aplicación (`productos/`)

Aquí vive la funcionalidad del negocio (nuestro catálogo).

- `models.py`: datos + lógica de negocio
- `views.py`: coordinación de solicitudes y respuestas
- `urls.py`: rutas específicas de la app
- `forms.py`: validación de formularios (si la app los usa)

### C. Capa de presentación (`templates/` y templates de app)

Aquí vive lo que ve el usuario.

- `templates/base.html`: estructura compartida (navbar, layout)
- templates hijos: catálogo, búsqueda, carrito, home, etc.

### Regla de oro de lectura

Cuando no entiendas un proyecto Django, pregúntate:

1. ¿Qué URL se pidió?
2. ¿Qué vista responde?
3. ¿Qué modelo consulta?
4. ¿Qué template renderiza?

---

## 3. El viaje de una petición (flujo MVT real)

El patrón MVT se entiende de verdad cuando sigues una petición real de principio a fin.

### Flujo general

```text
Navegador
   │
   ├── pide una URL (ej: /productos/)
   ▼
config/urls.py
   │
   ├── delega a productos/urls.py
   ▼
views.py
   │
   ├── consulta models.py (ORM)
   ├── prepara contexto
   └── llama a un template
   ▼
template.html
   │
   └── Django genera HTML
   ▼
Navegador (respuesta final)
```

### Ejemplo 1 — Catálogo (`/productos/`)

- El navegador pide `/productos/`
- Django revisa `config/urls.py`
- Se delega a `productos/urls.py`
- Se ejecuta `lista_productos`
- La vista consulta `Producto.objects...`
- Se renderiza `lista_productos.html`
- El usuario ve la lista

### Ejemplo 2 — Búsqueda (`/productos/buscar/?q=...`)

- El navegador envía un `GET` con un parámetro (`q`)
- La vista lee `request.GET`
- Filtra productos con el ORM
- Envía resultados al template `buscar.html`

### Ejemplo 3 — Carrito (sesión)

- El usuario hace clic en “Agregar al carrito”
- La vista modifica `request.session`
- Luego hace `redirect(...)`
- Otra vista (`ver_carrito`) lee esa sesión y muestra el contenido

> Observa que el carrito simple usa sesión: no necesitamos un modelo de carrito todavía.

---

## 4. Decisiones de Clase 2 que importan a nivel de programador

### 4.1 `config/` como organización profesional

Renombrar la carpeta de configuración a `config/` ayuda a separar:

- configuración global del proyecto,
- lógica de negocio de las apps.

No cambia “qué puede hacer Django”, pero sí mejora cómo se lee y mantiene el proyecto.

### 4.2 Fat Models, Thin Views

Idea clave:

- **Modelo**: sabe cosas del negocio (ej: `precio_final()`, `ahorro_monto()`)
- **Vista**: coordina la solicitud (recibe request, consulta, renderiza o redirige)

Esto reduce duplicación y mejora el mantenimiento.

### 4.3 Forms de Django

Un `Form` no es solo HTML.

También aporta:

- validación del lado del servidor,
- limpieza de datos,
- mensajes de error,
- estructura clara del formulario.

> Regla de seguridad: nunca confiar solo en validaciones del navegador.

### 4.4 Sesiones (`request.session`)

Las sesiones permiten guardar estado del usuario entre solicitudes.

En nuestro proyecto didáctico se usan para:

- guardar IDs de productos en carrito,
- mostrar el carrito después,
- mantener datos mientras el usuario navega.

### 4.5 Herencia de templates (`base.html`)

Con `base.html` evitamos repetir:

- `<head>`
- navbar
- estructura principal

Cada template hijo solo define lo específico.

Eso aplica el principio **DRY** (No te repitas).

### 4.6 `GET` vs `POST` (visión conceptual)

- `GET`: buscar, navegar, consultar
- `POST`: enviar datos o ejecutar acciones que modifican estado

En cursos iniciales a veces se simplifican acciones con links para enfocarse en el flujo. Lo importante por ahora es **entender la diferencia conceptual**.

---

## 5. Cómo leer código Django sin perderte

Cuando abras un archivo y no entiendas qué hace, usa este orden:

### Paso 1 — Buscar la ruta

Identifica el `name=` y la URL asociada en `urls.py`.

### Paso 2 — Leer la vista completa

En la vista, identifica:

- entradas (`request`, parámetros de URL)
- consultas al modelo
- si hace `render()` o `redirect()`
- qué template usa
- qué contexto envía

### Paso 3 — Revisar el template

Busca:

- variables (`{{ ... }}`)
- condicionales (`{% if %}`)
- loops (`{% for %}`)
- rutas (`{% url '...' %}`)

### Paso 4 — Volver al modelo (si hay lógica)

Si ves algo como `p.precio_final`, revisa `models.py` para entender la lógica real.

> Este hábito te ayuda a pensar como programador/a, no solo a copiar código.


---

## 6. Errores comunes (guía rápida)

| Error | Qué suele significar | Qué revisar primero |
| --- | --- | --- |
| `TemplateDoesNotExist` | Django no encuentra el template | nombre del archivo, ruta, carpeta `templates`, `TEMPLATES['DIRS']` |
| `NoReverseMatch` | Django no puede construir una URL por nombre | `name=` en `urls.py`, parámetros requeridos, `{% url %}` |
| `AttributeError` | Se intenta usar algo que no existe | nombre del atributo/campo/método en modelo o vista |
| `OperationalError` | Problema con la base de datos (a menudo migraciones) | cambios en `models.py`, `makemigrations`, `migrate` |
| `ImportError` | Import mal escrito o circular | rutas de import en `views.py`/`urls.py` |

---

## 7. Siguiente paso: práctica de consolidación

Vamos a completar el proyecto con una funcionalidad nueva, todavía dentro del nivel básico:

### Práctica final (consolidación)

- crear una **vista de detalle de producto**,
- usar una **URL dinámica** (`<int:producto_id>`),
- crear un **template nuevo** que herede de `base.html`,
- conectar navegación desde catálogo, búsqueda y carrito.

Con esto vas a recorrer otra vez el flujo completo de Django, pero ahora con más criterio.

> Meta de esta clase: que puedas leer, explicar y ampliar un proyecto Django básico sin perderte.
