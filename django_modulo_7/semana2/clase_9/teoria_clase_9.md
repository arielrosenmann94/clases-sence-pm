# 🏁 Módulo 7 — Clase 8b

## Tu Proyecto Terminado: Todo lo que Debe Tener Antes del Día de Deploy

> **Preparación** — La próxima clase haremos deploy real. Ese día NO es para arreglar cosas. Es para **publicar**. Todo lo que vamos a ver ahora es lo que tu proyecto debe traer **100% terminado** ese día.
>
> ⚠️ Esta clase es 100% teórica y conversacional. Es tu checklist de preparación. Si el día de deploy falta algo de esta lista, no vas a poder publicar.

---

## 🗺️ Índice

| #      | Tema                                                                   |
| ------ | ---------------------------------------------------------------------- |
| **1**  | La Mentalidad: ¿Qué Significa "Proyecto Terminado"?                    |
| **2**  | Estructura del Proyecto: Orden y Convenciones                          |
| **3**  | Modelos y Base de Datos: Todo Migrado y Funcional                      |
| **4**  | Vistas y URLs: Todo Conectado y Protegido                              |
| **5**  | Templates y Frontend: Completo, Responsive, Profesional                |
| **6**  | Formularios: Validados y Seguros                                       |
| **7**  | Autenticación y Permisos: ¿Quién Puede Hacer Qué?                     |
| **8**  | Archivos Estáticos y Media: CSS, JS, Imágenes                         |
| **9**  | Settings: Preparado para Dos Mundos                                    |
| **10** | Variables de Entorno: El `.env` Listo                                  |
| **11** | Git y `.gitignore`: Repositorio Limpio                                 |
| **12** | Dependencias: `requirements.txt` Actualizado                           |
| **13** | Datos Iniciales: ¿Qué Hay en la Base al Arrancar?                     |
| **14** | Testing: ¿Funciona Todo lo que Crees que Funciona?                     |
| **15** | Calidad de Código: Los Detalles Profesionales                          |
| **16** | README: El Manual de Tu Proyecto                                       |
| **17** | El Mega-Checklist: Todo en Una Página                                  |
| **18** | Los 10 Problemas que Siempre Aparecen el Día de Deploy                 |

---

---

> _"No sube a producción el proyecto perfecto. Sube el proyecto que está **terminado** y **verificado**. Perfecto no existe. Completo sí."_

---

---

# 🧠 1. La Mentalidad: ¿Qué Significa "Proyecto Terminado"?

---

Hay una diferencia enorme entre "funciona en mi computador" y "está listo para publicar". La mayoría de los problemas el día de deploy no son técnicos — son cosas que **quedaron a medias**.

### ¿Qué NO es un proyecto terminado?

```
❌ "Funciona pero el login a veces falla"
❌ "El formulario funciona pero no valida nada"
❌ "El CSS está casi listo, faltan unos detalles"
❌ "Los links del navbar van a páginas que no existen todavía"
❌ "Tengo el SECRET_KEY en el código pero después lo cambio"
❌ "Los templates tienen Lorem Ipsum en algunas partes"
```

### ¿Qué SÍ es un proyecto terminado?

```
✅ Todas las páginas cargan sin errores
✅ Todos los links funcionan y llevan a donde deben
✅ Todos los formularios validan, guardan y responden correctamente
✅ El diseño se ve bien en celular Y en escritorio
✅ Los datos sensibles están en variables de entorno
✅ No hay código "de prueba" ni prints de debugging
✅ Otra persona puede clonar el repo y hacerlo andar siguiendo el README
```

### La Analogía del Restaurante

```
ABRIR UN RESTAURANTE                    HACER DEPLOY DE TU PROYECTO
────────────────────                     ─────────────────────────────
La comida debe estar lista               Las funcionalidades deben funcionar
El menú no puede tener platos            Las páginas no pueden tener links
  que no existen                           que no existen
Los baños deben funcionar                Los formularios deben funcionar
La cocina debe cumplir normas            El código debe cumplir seguridad
El personal debe saber su rol           Cada view debe saber qué hace
Si no está listo, no abres              Si no está listo, no haces deploy
```

> 💡 **Nadie abre un restaurante "casi listo".** No hagas deploy de un proyecto "casi listo".

---

---

# 📁 2. Estructura del Proyecto: Orden y Convenciones

---

Tu proyecto debe tener una estructura **predecible y organizada**. Si alguien abre tu repositorio, debe entender en 30 segundos dónde está cada cosa.

## Estructura esperada

```
mi_proyecto/
├── config/                    ← Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py            ← O carpeta settings/ con base.py, dev.py, prod.py
│   ├── urls.py                ← URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── mi_app/                    ← Cada app en su propia carpeta
│   ├── __init__.py
│   ├── admin.py               ← Modelos registrados en el admin
│   ├── apps.py
│   ├── forms.py               ← Formularios (si usas)
│   ├── models.py              ← Modelos de datos
│   ├── urls.py                ← URLs de la app
│   ├── views.py               ← Vistas
│   ├── tests.py               ← Tests
│   ├── templates/             ← Templates HTML
│   │   └── mi_app/
│   │       ├── base.html
│   │       ├── lista.html
│   │       └── detalle.html
│   └── static/                ← Archivos estáticos de la app
│       └── mi_app/
│           ├── css/
│           ├── js/
│           └── img/
│
├── static/                    ← Archivos estáticos globales (opcional)
├── templates/                 ← Templates globales (base.html compartido)
├── media/                     ← Archivos subidos por usuarios
│
├── .env                       ← Variables de entorno (NO en git)
├── .env.example               ← Plantilla de variables (SÍ en git)
├── .gitignore                 ← Archivos ignorados por git
├── requirements.txt           ← Dependencias del proyecto
├── manage.py
└── README.md                  ← Instrucciones del proyecto
```

## Checklist de estructura

```
[ ] La carpeta del proyecto tiene nombre descriptivo (no "proyecto1" ni "test")
[ ] La carpeta de configuración se llama config/ (o el nombre que elegiste)
[ ] Cada app tiene su propia carpeta con todos sus archivos
[ ] Los templates siguen la convención app/templates/app/archivo.html
[ ] Los archivos estáticos siguen la convención app/static/app/
[ ] No hay archivos sueltos en la raíz que no deberían estar
[ ] No hay carpetas vacías sin propósito
[ ] No hay archivos __pycache__ en el repositorio
```

> ⚠️ **El día de deploy:** si tu estructura es un desorden, cada problema tarda el doble en arreglarse porque nadie encuentra nada.

---

---

# 🗄️ 3. Modelos y Base de Datos: Todo Migrado y Funcional

---

Los modelos son el **cimiento** de tu proyecto. Si los modelos están mal o incompletos, todo lo que depende de ellos (vistas, formularios, templates) va a fallar.

## ¿Qué debe estar listo?

### Todos los modelos definidos

```python
# Cada modelo debe tener:
class MiModelo(models.Model):
    # 1. Todos los campos que necesita con tipos correctos
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # 2. Relaciones correctas (FK, M2M, OneToOne)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    # 3. __str__ definido (para que el admin sea legible)
    def __str__(self):
        return self.nombre

    # 4. class Meta si es necesario (ordering, verbose_name, etc.)
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Mi Modelo'
        verbose_name_plural = 'Mis Modelos'
```

### Migraciones al día

```bash
# PASO 1: Verificar que no hay cambios sin migrar
python manage.py makemigrations --check
# Si dice "No changes detected" → ✅ OK
# Si crea algo → tienes cambios sin migrar ❌

# PASO 2: Verificar que todas las migraciones están aplicadas
python manage.py showmigrations
# Todas deben tener [X]:
# [X] 0001_initial
# [X] 0002_add_email_field
# Si alguna tiene [ ] → está pendiente ❌

# PASO 3: Aplicar las que falten
python manage.py migrate
```

### Admin registrado

```python
# admin.py — TODOS los modelos registrados
from django.contrib import admin
from .models import Cliente, Producto, Pedido

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
# O mejor aún, con ModelAdmin para personalizar la vista del admin
```

## Checklist de modelos y BD

```
[ ] Todos los modelos están definidos con todos sus campos
[ ] Cada modelo tiene __str__ definido
[ ] Las relaciones (FK, M2M) son correctas y tienen on_delete
[ ] python manage.py makemigrations --check dice "No changes detected"
[ ] python manage.py showmigrations muestra todo con [X]
[ ] Todos los modelos están registrados en admin.py
[ ] Puedo crear, editar y borrar registros desde el admin sin errores
[ ] Los datos que necesito para el sitio existen en la base de datos
```

### La Analogía

> 🏠 Si los modelos son los cimientos de una casa, no puedes poner el techo (templates) si los cimientos están incompletos. Verifica los cimientos **primero**.

---

---

# 🔗 4. Vistas y URLs: Todo Conectado y Protegido

---

Cada URL de tu proyecto debe llevar a una vista que funciona. No puede haber links rotos, páginas a medio hacer, ni URLs que devuelven errores.

## ¿Qué debe estar listo?

### Todas las URLs definidas y conectadas

```python
# config/urls.py — URLs principales
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mi_app.urls')),  # ← Cada app incluida
]

# mi_app/urls.py — URLs de la app
from django.urls import path
from . import views

app_name = 'mi_app'  # ← Namespace definido

urlpatterns = [
    path('', views.home, name='home'),
    path('lista/', views.lista, name='lista'),
    path('detalle/<int:pk>/', views.detalle, name='detalle'),
    path('crear/', views.crear, name='crear'),
    # ... cada funcionalidad tiene su URL con name
]
```

### Todas las vistas funcionan

```
┌─────────────────────────────────────────────────────────────────┐
│  PARA CADA VISTA DE TU PROYECTO, VERIFICA:                     │
│                                                                 │
│  [ ] ¿Responde sin error 500?                                  │
│  [ ] ¿Muestra los datos correctos?                              │
│  [ ] ¿El template existe y carga?                               │
│  [ ] ¿Los links dentro de la página funcionan?                  │
│  [ ] ¿Los formularios (si tiene) envían y procesan datos?       │
│  [ ] Si requiere login, ¿está protegida?                        │
│  [ ] Si recibe datos por POST, ¿tiene csrf_token?               │
└─────────────────────────────────────────────────────────────────┘
```

### Vistas protegidas

```python
# Toda vista que NO debe ser pública debe estar protegida:

# Para function-based views:
from django.contrib.auth.decorators import login_required

@login_required
def mi_vista_privada(request):
    ...

# Para class-based views:
from django.contrib.auth.mixins import LoginRequiredMixin

class MiVistaPrivada(LoginRequiredMixin, ListView):
    ...
```

## La prueba definitiva

Abre tu proyecto en el navegador y haz clic en **absolutamente todo**:

```
1. Abre la página principal               → ¿Carga?
2. Haz clic en cada link del navbar        → ¿Todos llevan a donde deben?
3. Haz clic en cada botón                  → ¿Todos hacen lo que deben?
4. Navega por cada sección                 → ¿Todas cargan sin error?
5. Intenta acceder a URLs que no existen   → ¿Muestra 404 decente o error feo?
6. Intenta acceder a vistas privadas       → ¿Te redirige al login?
   sin estar logueado
```

## Checklist de vistas y URLs

```
[ ] Cada funcionalidad tiene su URL con name definido
[ ] Cada URL lleva a una vista que funciona
[ ] Las URLs usan namespaces (app_name)
[ ] No hay links rotos en ninguna página
[ ] Las vistas que requieren login están protegidas
[ ] Los POST tienen {% csrf_token %}
[ ] Las páginas de error (404, 500) se ven decentes
```

---

---

# 🎨 5. Templates y Frontend: Completo, Responsive, Profesional

---

Esto es lo que el usuario **ve**. Puede que tu backend sea perfecto, pero si el frontend se ve roto, incompleto o feo, da la impresión de que nada funciona.

## ¿Qué debe estar listo?

### Template base funcional

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Sitio{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
    <!-- Bootstrap, Tailwind, o tu CSS -->
</head>
<body>
    <!-- Navbar -->
    {% include 'components/navbar.html' %}

    <!-- Contenido principal -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    {% include 'components/footer.html' %}

    <!-- Scripts -->
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Los 5 puntos que NO pueden fallar en el frontend

| #   | Punto                    | ¿Qué verificar?                                                                     |
| :-- | :----------------------- | :----------------------------------------------------------------------------------- |
| 1   | **Responsive**           | ¿Se ve bien en celular (360px)? ¿Y en tablet? ¿Y en escritorio? ¿Y en TV?           |
| 2   | **Contenido real**       | ¿Hay Lorem Ipsum en algún lado? ¿Hay imágenes placeholder? Todo debe ser contenido real |
| 3   | **Links funcionales**    | ¿TODOS los links del navbar, footer y botones llevan a algún lado?                   |
| 4   | **Diseño consistente**   | ¿Todas las páginas tienen el mismo estilo? ¿Mismos colores, tipografía, espaciado?   |
| 5   | **Sin errores visuales** | ¿Hay textos cortados? ¿Imágenes que no cargan? ¿Elementos encimados?                |

### Responsive: la prueba obligatoria

```
PRUEBA EN ESTOS ANCHOS:
─────────────────────────────────
📱 360px   → Celular pequeño (Galaxy, iPhone SE)
📱 390px   → Celular estándar (iPhone 14)
📱 414px   → Celular grande
📲 768px   → Tablet vertical
💻 1024px  → Tablet horizontal / laptop pequeña
🖥️ 1440px  → Escritorio estándar
📺 1920px  → Pantalla grande / TV

¿CÓMO PROBAR?
→ Chrome DevTools (F12) → Toggle Device Toolbar (Ctrl+Shift+M)
→ Seleccionar diferentes dispositivos
→ O arrastrar el borde de la ventana del navegador
```

### Lo que SIEMPRE se rompe en responsive

| Problema                          | Solución                                                         |
| :-------------------------------- | :--------------------------------------------------------------- |
| Navbar no es hamburguesa en móvil | Usar componente responsive (Bootstrap Navbar, CSS media queries) |
| Tablas se salen de la pantalla    | `overflow-x: auto` en el contenedor de la tabla                  |
| Texto demasiado grande en móvil   | Usar unidades relativas (`rem`, `%`, `vw`) no `px` fijos         |
| Imágenes se salen del ancho       | `img { max-width: 100%; height: auto; }`                         |
| Formularios muy anchos en móvil   | `input { width: 100%; box-sizing: border-box; }`                |
| Columnas lado a lado en móvil     | Usar flexbox/grid con `flex-wrap` o media queries                |

## Checklist de templates y frontend

```
[ ] Template base con DOCTYPE, meta viewport, bloque title, content, scripts
[ ] Navbar presente en todas las páginas con links funcionales
[ ] Footer presente (información de contacto, copyright, links)
[ ] TODAS las páginas extienden del template base
[ ] Responsive verificado en celular, tablet y escritorio
[ ] Sin Lorem Ipsum ni contenido placeholder
[ ] Sin imágenes rotas (el src apunta a archivos que existen)
[ ] Tipografía y colores consistentes en todo el sitio
[ ] Mensajes de éxito/error se muestran al usuario (django messages)
[ ] El título de la pestaña cambia en cada página ({% block title %})
```

---

---

# 📝 6. Formularios: Validados y Seguros

---

Si tu proyecto tiene formularios (y probablemente tiene), cada uno debe estar **completo**: funcional, validado y seguro.

## Lo que cada formulario debe tener

```
┌─────────────────────────────────────────────────────────────────┐
│  CADA FORMULARIO DEBE CUMPLIR:                                  │
│                                                                 │
│  [ ] Tiene {% csrf_token %}                                     │
│  [ ] Valida los datos en el servidor (no solo en JS)            │
│  [ ] Muestra errores al usuario cuando los datos son inválidos  │
│  [ ] Redirige correctamente después de enviar                   │
│  [ ] No permite enviar datos vacíos en campos obligatorios      │
│  [ ] No permite datos maliciosos (XSS, SQL injection)           │
│  [ ] Muestra un mensaje de éxito después de guardar             │
└─────────────────────────────────────────────────────────────────┘
```

### Formulario bien implementado

```python
# forms.py
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email
```

```python
# views.py
from django.contrib import messages

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente creado exitosamente!')
            return redirect('mi_app:lista')
        # Si no es válido, el form se re-renderiza con errores
    else:
        form = ClienteForm()
    return render(request, 'mi_app/crear.html', {'form': form})
```

```html
<!-- En el template -->
<form method="POST">
    {% csrf_token %}

    {% if form.errors %}
    <div class="alert alert-danger">
        Por favor corrige los errores indicados.
    </div>
    {% endif %}

    {{ form.as_p }}

    <button type="submit">Guardar</button>
</form>

<!-- Mostrar mensajes de éxito -->
{% for message in messages %}
<div class="alert alert-{{ message.tags }}">
    {{ message }}
</div>
{% endfor %}
```

### La prueba de cada formulario

| Prueba                               | Qué debe pasar                                |
| :----------------------------------- | :--------------------------------------------- |
| Enviar con todos los campos llenos   | Guarda y muestra mensaje de éxito              |
| Enviar con campos vacíos             | Muestra error, NO guarda                       |
| Enviar con datos inválidos (email malo) | Muestra error específico                    |
| Enviar el mismo formulario 2 veces   | No crea duplicados (o maneja el caso)          |
| Enviar con caracteres especiales     | No rompe la página (protección contra XSS)     |

## Checklist de formularios

```
[ ] Cada formulario tiene {% csrf_token %}
[ ] La validación ocurre en el servidor (forms.py), no solo en HTML/JS
[ ] Los errores se muestran al usuario de forma clara
[ ] Después de enviar exitosamente, redirige (patrón POST-redirect-GET)
[ ] Los mensajes de éxito se muestran (django.contrib.messages)
[ ] Probé cada formulario con datos buenos, malos y vacíos
```

---

---

# 🔐 7. Autenticación y Permisos: ¿Quién Puede Hacer Qué?

---

Si tu proyecto tiene usuarios (login, registro, perfiles), esta sección es **crítica**.

## ¿Qué debe funcionar?

```
FLUJO COMPLETO DE USUARIO:
──────────────────────────
[ ] Registro de nuevo usuario         → ¿Se crea la cuenta?
[ ] Login                             → ¿Entra correctamente?
[ ] Logout                            → ¿Sale y no puede acceder a páginas privadas?
[ ] Cambio de contraseña (si aplica)  → ¿Funciona?
[ ] Páginas privadas sin login        → ¿Redirige al login?
[ ] Páginas del admin                 → ¿Solo accede quien debe?
```

### Prueba de seguridad básica

```
PRUEBA MANUAL OBLIGATORIA:
──────────────────────────
1. Cierra sesión
2. Intenta acceder directamente a una URL privada
   (ej: /clientes/crear/, /admin/, /perfil/)
3. ¿Te redirige al login? → ✅
4. ¿Te muestra la página? → ❌ ERROR GRAVE — falta protección
```

## Checklist de autenticación

```
[ ] Login funciona correctamente
[ ] Logout funciona y redirige apropiadamente
[ ] Las páginas privadas redirigen al login si no estás autenticado
[ ] El usuario administrador puede acceder al admin
[ ] El panel de admin (/admin/) funciona y muestra los modelos
[ ] Si hay registro de usuarios, funciona sin errores
[ ] Las contraseñas cumplen las reglas de validación de Django
```

---

---

# 📁 8. Archivos Estáticos y Media: CSS, JS, Imágenes

---

Uno de los problemas más comunes el día de deploy: **el sitio carga sin estilos**. Todo el CSS, JavaScript e imágenes desaparecen. Esto pasa porque en producción Django NO sirve archivos estáticos automáticamente.

## ¿Qué debes tener listo?

### Archivos estáticos bien organizados

```
mi_app/
└── static/
    └── mi_app/              ← Siempre dentro de una subcarpeta con el nombre de la app
        ├── css/
        │   └── styles.css
        ├── js/
        │   └── main.js
        └── img/
            ├── logo.png
            └── hero.jpg
```

### En los templates, siempre usar `{% static %}`

```html
<!-- ✅ CORRECTO: usa {% static %} -->
{% load static %}
<link rel="stylesheet" href="{% static 'mi_app/css/styles.css' %}">
<img src="{% static 'mi_app/img/logo.png' %}" alt="Logo">
<script src="{% static 'mi_app/js/main.js' %}"></script>

<!-- ❌ INCORRECTO: ruta hardcodeada -->
<link rel="stylesheet" href="/static/mi_app/css/styles.css">
<!-- Esto puede romper si cambia la configuración de STATIC_URL -->
```

### Settings configurados

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # Para collectstatic en producción

# Si tienes archivos estáticos globales fuera de las apps:
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media (archivos subidos por usuarios):
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Verificar que collectstatic funciona

```bash
# Este comando recopila TODOS los estáticos en una sola carpeta
# Es necesario para producción
python manage.py collectstatic

# Si da errores → hay archivos estáticos mal configurados
# Si funciona → ✅ listo para producción
```

## Checklist de archivos estáticos y media

```
[ ] Los archivos estáticos están en app/static/app/
[ ] Los templates usan {% load static %} y {% static 'ruta' %}
[ ] No hay rutas de archivos hardcodeadas en los templates
[ ] STATIC_ROOT está configurado en settings.py
[ ] python manage.py collectstatic funciona sin errores
[ ] MEDIA_ROOT está configurado si hay uploads de usuarios
[ ] Las imágenes del sitio cargan correctamente
[ ] El CSS se aplica correctamente en todas las páginas
[ ] El JavaScript funciona en todas las páginas donde se usa
```

---

---

# ⚙️ 9. Settings: Preparado para Dos Mundos

---

Tu settings.py tiene que estar **preparado** para funcionar en desarrollo y en producción. El día de deploy no es para reconfigurar — es para cambiar variables de entorno.

El problema es que desarrollo y producción necesitan configuraciones **opuestas**:

| Setting                   | En desarrollo                | En producción                        |
| :------------------------ | :--------------------------- | :----------------------------------- |
| `DEBUG`                   | `True`                       | `False`                              |
| `SECRET_KEY`              | Cualquier string             | Clave única generada aleatoriamente  |
| `ALLOWED_HOSTS`           | `['localhost', '127.0.0.1']` | `['midominio.com']`                  |
| `DATABASES`               | SQLite                       | PostgreSQL                           |
| `SESSION_COOKIE_SECURE`   | `False`                      | `True`                               |
| `CSRF_COOKIE_SECURE`      | `False`                      | `True`                               |
| `SECURE_SSL_REDIRECT`     | `False`                      | `True`                               |
| Archivos estáticos        | Django los sirve             | Nginx o WhiteNoise los sirve         |

> ⚠️ **El problema:** si tienes todo en un solo `settings.py`, tendrías que estar cambiando valores cada vez que pasas de desarrollo a producción. Eso es un error esperando a pasar.

---

## Solución: Dividir settings en una carpeta

En vez de tener **un solo archivo** `settings.py`, lo convertimos en una **carpeta** con archivos separados:

```
ANTES (un solo archivo):              DESPUÉS (carpeta con archivos):
─────────────────────────              ─────────────────────────────────
config/                                config/
├── settings.py    ← todo junto       ├── settings/
├── urls.py                           │   ├── __init__.py  ← elige cuál cargar
├── wsgi.py                           │   ├── base.py      ← lo COMÚN a ambos
└── asgi.py                           │   ├── development.py ← solo desarrollo
                                      │   └── production.py  ← solo producción
                                      ├── urls.py
                                      ├── wsgi.py
                                      └── asgi.py
```

### ¿Qué va en cada archivo?

```
base.py          →  TODO lo que es igual en desarrollo y producción:
                    INSTALLED_APPS, MIDDLEWARE, TEMPLATES, AUTH_PASSWORD_VALIDATORS,
                    LANGUAGE_CODE, TIME_ZONE, STATIC_URL, etc.

development.py   →  Lo que SOLO necesitas en desarrollo:
                    DEBUG = True, SQLite, herramientas de debug

production.py    →  Lo que SOLO necesitas en producción:
                    DEBUG = False, PostgreSQL, seguridad, HTTPS
```

### La Analogía

> 🏠 Piensa en un uniforme escolar: todos tienen la **misma base** (pantalón, camisa). Pero en **invierno** le agregas la chaqueta y la bufanda, y en **verano** usas manga corta. No compras un uniforme completamente distinto para cada estación — cambias solo lo que necesita cambiar.

---

## Paso a Paso: Cómo Construirlo

---

### Paso 1: Crear la carpeta `settings/`

Dentro de tu carpeta `config/` (o como se llame tu carpeta de configuración), crea una carpeta llamada `settings`:

```bash
# Desde la raíz de tu proyecto:
mkdir config/settings
```

---

### Paso 2: Mover `settings.py` a `base.py`

Renombra (o copia) tu `settings.py` actual como `base.py` dentro de la nueva carpeta:

```bash
mv config/settings.py config/settings/base.py
```

---

### Paso 3: Crear `__init__.py`

Este archivo le dice a Python qué archivo de settings cargar. Crea `config/settings/__init__.py`:

```python
# config/settings/__init__.py

import os

# Lee la variable de entorno DJANGO_SETTINGS_MODULE
# Si no existe, usa development por defecto
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .development import *
```

> 💡 **¿Qué hace esto?** Si la variable de entorno `DJANGO_ENV` vale `"production"`, carga `production.py`. Si no existe o vale cualquier otra cosa, carga `development.py`. Así **por defecto siempre estás en desarrollo** — y solo en el servidor configuras producción.

---

### Paso 4: Limpiar `base.py`

En `base.py` deja **solo lo que es común** a ambos entornos. Saca todo lo que es específico de desarrollo o producción:

```python
# config/settings/base.py
# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN BASE — Común a desarrollo y producción
# ═══════════════════════════════════════════════════════════════

from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ──────────────────────────────────────────────
# Ruta base del proyecto
# ──────────────────────────────────────────────
# IMPORTANTE: como ahora settings está dentro de una subcarpeta,
# necesitamos subir UN nivel más (.parent extra)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
#                                         │       │      │
#                                         │       │      └── raíz del proyecto
#                                         │       └── config/
#                                         └── settings/

# ──────────────────────────────────────────────
# Clave secreta — SIEMPRE desde variable de entorno
# ──────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY')

# ──────────────────────────────────────────────
# Aplicaciones instaladas
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- Apps propias ---
    'mi_app',
    # 'otra_app',
]

# ──────────────────────────────────────────────
# Middleware
# ──────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ──────────────────────────────────────────────
# URLs y WSGI
# ──────────────────────────────────────────────
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ──────────────────────────────────────────────
# Templates
# ──────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ──────────────────────────────────────────────
# Validación de contraseñas
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────
# Internacionalización
# ──────────────────────────────────────────────
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
# Archivos estáticos y media
# ──────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ──────────────────────────────────────────────
# Primary key por defecto
# ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

> ⚠️ **MUY IMPORTANTE — `BASE_DIR`:** Fíjate que `BASE_DIR` ahora tiene **un `.parent` extra**. Antes, `settings.py` estaba en `config/settings.py` (2 niveles). Ahora, `base.py` está en `config/settings/base.py` (3 niveles). Si no agregas el `.parent` extra, todas las rutas del proyecto estarán mal.

```python
# ANTES (settings.py en config/):
BASE_DIR = Path(__file__).resolve().parent.parent
#          base.py → config/ → raíz

# AHORA (base.py en config/settings/):
BASE_DIR = Path(__file__).resolve().parent.parent.parent
#          base.py → settings/ → config/ → raíz
```

---

### Paso 5: Crear `development.py`

```python
# config/settings/development.py
# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE DESARROLLO — Solo para tu máquina local
# ═══════════════════════════════════════════════════════════════

from .base import *     # ← Importa TODO lo de base.py primero

# ──────────────────────────────────────────────
# Modo debug activado
# ──────────────────────────────────────────────
DEBUG = True

# ──────────────────────────────────────────────
# Hosts permitidos en desarrollo
# ──────────────────────────────────────────────
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ──────────────────────────────────────────────
# Base de datos: SQLite (simple, local, sin instalar nada)
# ──────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ──────────────────────────────────────────────
# Seguridad relajada para desarrollo
# (NO necesitamos HTTPS en localhost)
# ──────────────────────────────────────────────
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# ──────────────────────────────────────────────
# Apps adicionales de desarrollo (opcional)
# ──────────────────────────────────────────────
# Si usas django-debug-toolbar:
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']
```

> 💡 **Fíjate en la primera línea:** `from .base import *` importa **todo** lo que está en `base.py`. Después, solo **sobreescribes** lo que necesita ser diferente. No tienes que repetir `INSTALLED_APPS`, `MIDDLEWARE`, ni nada — ya están cargados desde `base`.

---

### Paso 6: Crear `production.py`

```python
# config/settings/production.py
# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PRODUCCIÓN — Para el servidor real
# ═══════════════════════════════════════════════════════════════

from .base import *     # ← Importa TODO lo de base.py primero
import os

# ──────────────────────────────────────────────
# Modo debug DESACTIVADO — OBLIGATORIO en producción
# ──────────────────────────────────────────────
DEBUG = False

# ──────────────────────────────────────────────
# Solo acepta requests de tu dominio real
# ──────────────────────────────────────────────
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# En el .env del servidor: ALLOWED_HOSTS=miapp.com,www.miapp.com

# ──────────────────────────────────────────────
# Base de datos: PostgreSQL (diseñada para producción)
# ──────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ──────────────────────────────────────────────
# Seguridad — TODO activado en producción
# ──────────────────────────────────────────────
SESSION_COOKIE_SECURE = True        # Cookie de sesión solo por HTTPS
CSRF_COOKIE_SECURE = True           # Cookie CSRF solo por HTTPS
SECURE_SSL_REDIRECT = True          # Redirige HTTP → HTTPS
SECURE_HSTS_SECONDS = 31536000      # Fuerza HTTPS por 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ──────────────────────────────────────────────
# Archivos estáticos con WhiteNoise
# ──────────────────────────────────────────────
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ──────────────────────────────────────────────
# Logging — registrar errores en archivo
# ──────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

---

### Paso 7: Actualizar `wsgi.py` y `asgi.py`

Estos archivos ya tienen la línea que dice qué settings usar. **No necesitan cambiar** porque el `__init__.py` se encarga de cargar el archivo correcto:

```python
# config/wsgi.py — generalmente ya dice esto:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 'config.settings' ahora es la carpeta, y __init__.py decide qué cargar
```

---

### Paso 8: Configurar el `.env` del servidor

En el servidor de producción, necesitas agregar una variable extra:

```bash
# .env en el SERVIDOR (producción):
DJANGO_ENV=production
SECRET_KEY=clave-ultra-segura-generada-aleatoriamente
ALLOWED_HOSTS=miapp.com,www.miapp.com
DB_NAME=mi_base_datos_prod
DB_USER=mi_usuario_prod
DB_PASSWORD=contraseña-super-segura
```

```bash
# .env en TU MÁQUINA (desarrollo):
# No necesitas DJANGO_ENV — si no existe, __init__.py carga development.py
SECRET_KEY=django-insecure-clave-de-desarrollo
```

---

## Resultado final: la estructura completa

```
mi_proyecto/
├── config/
│   ├── __init__.py
│   ├── settings/                    ← Carpeta de settings
│   │   ├── __init__.py              ← Decide cuál cargar (dev o prod)
│   │   ├── base.py                  ← Todo lo COMÚN
│   │   ├── development.py           ← Solo para desarrollo
│   │   └── production.py            ← Solo para producción
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── mi_app/
├── .env                             ← Valores locales
├── .env.example                     ← Plantilla
├── requirements.txt
└── manage.py
```

---

## ¿Cómo funciona en la práctica?

```
EN TU COMPUTADOR (desarrollo):
──────────────────────────────
1. No tienes DJANGO_ENV en tu .env (o dice "development")
2. __init__.py carga development.py
3. development.py importa base.py + agrega DEBUG=True, SQLite, etc.
4. Resultado: desarrollo cómodo con toda la ayuda de Django

EN EL SERVIDOR (producción):
──────────────────────────────
1. DJANGO_ENV=production en el .env del servidor
2. __init__.py carga production.py
3. production.py importa base.py + agrega DEBUG=False, PostgreSQL, seguridad
4. Resultado: producción segura y optimizada

EL CÓDIGO ES EL MISMO EN AMBOS → solo cambia el .env
```

---

## Diagrama visual

```
                    ┌─────────────────────┐
                    │     __init__.py     │
                    │  Lee DJANGO_ENV     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                  │
    DJANGO_ENV != production           DJANGO_ENV = production
              │                                  │
              ▼                                  ▼
    ┌─────────────────┐                ┌─────────────────┐
    │ development.py  │                │  production.py  │
    │                 │                │                 │
    │ from .base      │                │ from .base      │
    │   import *      │                │   import *      │
    │                 │                │                 │
    │ DEBUG = True    │                │ DEBUG = False   │
    │ SQLite          │                │ PostgreSQL      │
    │ Sin HTTPS       │                │ HTTPS forzado   │
    │ Sin seguridad   │                │ Seguridad total │
    │   extra         │                │                 │
    └────────┬────────┘                └────────┬────────┘
             │                                  │
             └──────────────┬───────────────────┘
                            │
                  ┌─────────▼─────────┐
                  │     base.py       │
                  │                   │
                  │ INSTALLED_APPS    │
                  │ MIDDLEWARE        │
                  │ TEMPLATES         │
                  │ AUTH_VALIDATORS   │
                  │ LANGUAGE_CODE     │
                  │ STATIC_URL       │
                  │ etc.              │
                  └───────────────────┘
```

---

## La alternativa simple: un solo `settings.py` con `if`

Si la carpeta te parece demasiado para tu proyecto actual, hay una alternativa más simple que también funciona. Un solo `settings.py` que lee todo de variables de entorno:

```python
# config/settings.py — versión con un solo archivo
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-de-desarrollo-insegura')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Base de datos: cambia según DEBUG
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Seguridad: solo en producción (cuando DEBUG es False)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
```

> 💡 **¿Cuál elegir?** Para proyectos pequeños, un solo `settings.py` con `if DEBUG` es suficiente. Para proyectos profesionales o con equipo, la carpeta `settings/` es el estándar de la industria.

| Enfoque                        | Cuándo usarlo                          |
| :----------------------------- | :------------------------------------- |
| Un solo `settings.py` con `if` | Proyectos personales, práctica, MVPs   |
| Carpeta `settings/`            | Proyectos profesionales, trabajo en equipo |

---

## Checklist de settings

```
[ ] SECRET_KEY se lee de variable de entorno (no está hardcodeada)
[ ] DEBUG se lee de variable de entorno o está en el archivo correcto
[ ] ALLOWED_HOSTS se configura correctamente para cada entorno
[ ] La base de datos puede cambiar entre SQLite (dev) y PostgreSQL (prod)
[ ] BASE_DIR tiene la cantidad correcta de .parent
[ ] python manage.py check funciona sin errores
[ ] python manage.py check --deploy muestra los warnings y los entiendo
[ ] Probé que el proyecto arranca correctamente con la nueva estructura
```

---

---

# 🔑 10. Variables de Entorno: El `.env` Listo

---

> Esto lo vimos en la **clase 6b**. Aquí verificamos que está **hecho**, no que lo sepan.

## Archivos que deben existir

```
tu_proyecto/
├── .env              ← Con valores REALES de desarrollo (NO en git)
├── .env.example      ← Con valores de EJEMPLO (SÍ en git)
└── .gitignore        ← Con .env incluido
```

### `.env` de desarrollo

```bash
SECRET_KEY=django-insecure-clave-local-de-desarrollo
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=mi_base_datos
DB_USER=mi_usuario
DB_PASSWORD=mi_password
```

### `.env.example` (plantilla para el equipo)

```bash
SECRET_KEY=cambiar-esta-clave-por-una-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
```

## Checklist de variables de entorno

```
[ ] .env existe con valores reales
[ ] .env.example existe con valores de ejemplo
[ ] .env está en .gitignore
[ ] settings.py lee las variables con os.environ.get() o django-environ
[ ] python-dotenv o django-environ está en requirements.txt
[ ] Puedo borrar el .env, copiar el .env.example, poner mis datos,
    y el proyecto arranca (así es como funcionará el día de deploy)
```

---

---

# 📂 11. Git y `.gitignore`: Repositorio Limpio

---

Tu repositorio de Git debe estar **limpio y profesional**. El día de deploy, posiblemente clones el repo en el servidor. Si tiene archivos basura, pesa más, es confuso, y puede ser inseguro.

## `.gitignore` mínimo para Django

```gitignore
# Entorno virtual
venv/
.venv/
env/

# Variables de entorno (SECRETOS)
.env

# Base de datos local
db.sqlite3
*.sqlite3

# Archivos compilados de Python
__pycache__/
*.py[cod]
*.pyc

# Archivos de media (subidos por usuarios)
media/

# Archivos estáticos recopilados
staticfiles/

# Editor / IDE
.vscode/
.idea/
*.swp

# Sistema operativo
.DS_Store
Thumbs.db

# Logs
*.log
```

## Checklist de Git

```
[ ] .gitignore existe con todo lo de arriba
[ ] git status está limpio (todo comiteado)
[ ] .env NO está en el historial de git
    → Verificar: git log --all -- .env
    → Si aparece algo, el secreto está comprometido
[ ] __pycache__/ NO está en el repo
[ ] db.sqlite3 NO está en el repo (o si lo necesitas, es consciente)
[ ] venv/ NO está en el repo
[ ] Los commits tienen mensajes descriptivos
    → "fix" ❌ → "Corregir validación de email en formulario de registro" ✅
[ ] El repo está subido a GitHub/GitLab y accesible
```

> ⚠️ **Recordatorio:** Lo que sube a Git **queda para siempre** en el historial. Si subiste el `.env` con un `SECRET_KEY` aunque sea una vez, esa clave está comprometida. Regenerala.

---

---

# 📦 12. Dependencias: `requirements.txt` Actualizado

---

El servidor donde hagas deploy no tiene nada instalado. El `requirements.txt` le dice **exactamente** qué instalar.

## Generar el archivo

```bash
pip freeze > requirements.txt
```

## ¿Cómo se ve un requirements.txt correcto?

```
Django==5.1.5
Pillow==10.2.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
whitenoise==6.6.0
gunicorn==21.2.0
```

### Puntos clave

| Regla                              | ¿Por qué?                                                           |
| :--------------------------------- | :------------------------------------------------------------------- |
| Versiones fijadas con `==`         | Para que en el servidor se instale **exactamente** lo mismo          |
| Sin librerías de desarrollo        | `django-debug-toolbar` NO debe estar en producción                   |
| `python-dotenv` incluido           | Si usas `.env`, la librería que lo lee debe estar                    |
| `gunicorn` incluido                | Es el servidor WSGI de producción (reemplaza `runserver`)            |
| `psycopg2-binary` incluido         | Si usarás PostgreSQL                                                 |

## Checklist de dependencias

```
[ ] requirements.txt existe
[ ] Las versiones están fijadas con == (no >= ni sin versión)
[ ] pip freeze > requirements.txt lo generé recientemente
[ ] Puedo crear un venv nuevo, instalar con pip install -r requirements.txt,
    y el proyecto arranca sin errores
[ ] No hay librerías de desarrollo innecesarias en el archivo
```

---

---

# 🌱 13. Datos Iniciales: ¿Qué Hay en la Base al Arrancar?

---

Cuando hagas deploy, la base de datos del servidor estará **vacía**. Solo tendrá las tablas (por las migraciones). ¿Tu proyecto necesita datos para funcionar?

## Pregúntate

```
¿Mi sitio necesita datos predefinidos para funcionar?
──────────────────────────────────────────────────────
→ ¿Categorías fijas? (ej: "Electrónica", "Ropa", "Alimentos")
→ ¿Roles de usuario? (ej: "Admin", "Editor", "Vendedor")
→ ¿Datos de demostración para que no se vea vacío?
→ ¿Un usuario administrador para acceder al panel de admin?
```

### Si necesitas datos iniciales, tienes 2 opciones

```
OPCIÓN 1: Cargarlos a mano desde el admin después de deploy
          → Funciona para pocos datos (categorías, roles, etc.)
          → Tedioso si son muchos registros

OPCIÓN 2: Management command personalizado
          → Un script que crea los datos automáticamente
          → python manage.py seed o python manage.py cargar_datos
          → Ideal para datos que siempre son los mismos
```

| Opción              | Cuándo usarla                                   |
| :------------------ | :---------------------------------------------- |
| Admin manual        | Pocos datos, datos que cambian según el proyecto |
| Management command  | Muchos datos, o datos que siempre son iguales    |

## Checklist de datos

```
[ ] Identifiqué qué datos necesita mi proyecto para funcionar al arrancar
[ ] Tengo un plan para cargar esos datos en producción
   (admin manual o management command)
[ ] Si uso management command, lo probé y funciona sin errores
[ ] Sé cómo crear un usuario administrador en el servidor
```

---

---

# 🧪 14. Testing: ¿Funciona Todo lo que Crees que Funciona?

---

No necesitas tests automatizados perfectos para deploy. Pero necesitas **verificar manualmente** que todo funciona.

## La prueba completa pre-deploy

```
┌──────────────────────────────────────────────────────────────────┐
│            🧪 PRUEBA MANUAL COMPLETA                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  VERIFICACIONES AUTOMÁTICAS (terminal)                           │
│  [ ] python manage.py check                    → Sin errores     │
│  [ ] python manage.py check --deploy           → Revisé warnings │
│  [ ] python manage.py makemigrations --check   → No changes      │
│  [ ] python manage.py collectstatic            → Funciona        │
│  [ ] python manage.py test (si tienes tests)   → Todos pasan     │
│                                                                  │
│  VERIFICACIONES MANUALES (navegador)                             │
│  [ ] Página principal carga correctamente                        │
│  [ ] TODOS los links del navbar funcionan                        │
│  [ ] TODOS los formularios envían y procesan datos               │
│  [ ] Login funciona                                              │
│  [ ] Logout funciona                                             │
│  [ ] Las páginas protegidas redirigen al login                   │
│  [ ] El admin de Django funciona (/admin/)                       │
│  [ ] Las imágenes cargan                                         │
│  [ ] El CSS se aplica correctamente                              │
│  [ ] Probé en celular (responsive)                               │
│  [ ] Probé en modo incógnito (sin caché)                         │
│  [ ] Las acciones CRUD funcionan (crear, ver, editar, borrar)    │
│                                                                  │
│  VERIFICACIONES DE DATOS                                         │
│  [ ] Los datos que necesita el sitio están cargados              │
│  [ ] No hay datos de prueba irrelevantes ("test", "asdf")        │
│  [ ] Los textos no tienen errores de ortografía graves           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> 💡 **La prueba más importante:** Abre tu proyecto en modo incógnito en el celular. Si se ve bien y funciona todo, estás listo.

---

---

# ✨ 15. Calidad de Código: Los Detalles Profesionales

---

Estos detalles no rompen tu proyecto, pero marcan la diferencia entre un proyecto de estudiante y uno profesional.

## Lo que debes limpiar

```
[ ] No hay print() en el código (salvo en management commands)
    → Buscar: grep -rn "print(" --include="*.py"

[ ] No hay código comentado "por si acaso"
    → Si está comentado, bórralo. Git lo recuerda.

[ ] No hay imports sin usar
    → VS Code los marca en gris, elimínalos

[ ] No hay variables sin usar

[ ] No hay contraseñas, tokens o claves en el código
    → Buscar: grep -rn "password\|secret\|token\|api_key" --include="*.py"

[ ] Los nombres de variables y funciones son descriptivos
    → x = queryset.get() ❌
    → cliente = Cliente.objects.get(pk=pk) ✅

[ ] No hay try/except vacíos que esconden errores
    → except: pass ← NUNCA en producción

[ ] Los archivos tienen un estilo consistente (indentación, espacios)
```

---

---

# 📖 16. README: El Manual de Tu Proyecto

---

Tu proyecto necesita un `README.md` que explique cómo instalarlo y correrlo. El día de deploy, posiblemente otra persona (o tú mismo desde otro computador) necesite entender cómo funciona.

## Estructura mínima del README

```markdown
# Nombre del Proyecto

Descripción breve de qué hace el proyecto.

## Requisitos

- Python 3.10+
- pip

## Instalación

1. Clonar el repositorio
   git clone https://github.com/usuario/proyecto.git
   cd proyecto

2. Crear y activar entorno virtual
   python -m venv venv
   source venv/bin/activate  (Linux/Mac)
   venv\Scripts\activate     (Windows)

3. Instalar dependencias
   pip install -r requirements.txt

4. Configurar variables de entorno
   cp .env.example .env
   (editar .env con tus valores)

5. Aplicar migraciones
   python manage.py migrate

6. Correr el servidor
   python manage.py runserver

## Uso

Abrir http://localhost:8000 en el navegador.
```

## Checklist del README

```
[ ] README.md existe en la raíz del proyecto
[ ] Describe qué hace el proyecto
[ ] Tiene instrucciones de instalación paso a paso
[ ] Menciona el .env.example
[ ] Si alguien sigue los pasos, el proyecto arranca sin errores
```

---

---

# ✅ 17. El Mega-Checklist: Todo en Una Página

---

```
┌──────────────────────────────────────────────────────────────────────────────┐
│           🏁 MEGA-CHECKLIST: ¿ESTÁ TU PROYECTO LISTO PARA DEPLOY?           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  📁 ESTRUCTURA                                                               │
│  [ ] Proyecto organizado con convenciones Django                             │
│  [ ] Cada app con sus archivos completos                                     │
│  [ ] Templates en app/templates/app/                                         │
│  [ ] Estáticos en app/static/app/                                            │
│                                                                              │
│  🗄️ MODELOS Y BASE DE DATOS                                                  │
│  [ ] Todos los modelos completos con __str__                                 │
│  [ ] Migraciones al día (makemigrations --check → "No changes")              │
│  [ ] Todas las migraciones aplicadas (showmigrations → todo [X])             │
│  [ ] Modelos registrados en admin.py                                         │
│  [ ] Datos necesarios para funcionar están cargados o hay plan               │
│                                                                              │
│  🔗 VISTAS Y URLS                                                            │
│  [ ] Cada URL tiene name y namespace                                         │
│  [ ] Cada vista funciona sin error 500                                       │
│  [ ] Vistas privadas protegidas con @login_required                          │
│  [ ] Todos los POSTs tienen {% csrf_token %}                                 │
│  [ ] No hay links rotos                                                      │
│                                                                              │
│  🎨 TEMPLATES Y FRONTEND                                                     │
│  [ ] Template base funcional (DOCTYPE, viewport, static)                     │
│  [ ] Responsive: probado en celular, tablet y escritorio                     │
│  [ ] Sin Lorem Ipsum ni contenido placeholder                                │
│  [ ] Diseño consistente en todas las páginas                                 │
│  [ ] Navbar y footer en todas las páginas                                    │
│  [ ] Sin imágenes rotas                                                      │
│                                                                              │
│  📝 FORMULARIOS                                                              │
│  [ ] Cada formulario tiene csrf_token y valida en el servidor                │
│  [ ] Errores se muestran al usuario                                          │
│  [ ] Redirect después de POST exitoso                                        │
│  [ ] Probados con datos buenos, malos y vacíos                               │
│                                                                              │
│  🔐 AUTENTICACIÓN                                                            │
│  [ ] Login y logout funcionan                                                │
│  [ ] Páginas privadas redirigen al login                                     │
│  [ ] Usuario administrador creado, admin funcional                           │
│                                                                              │
│  📁 ARCHIVOS ESTÁTICOS                                                       │
│  [ ] Templates usan {% static %} (no rutas hardcodeadas)                     │
│  [ ] STATIC_ROOT configurado                                                 │
│  [ ] collectstatic funciona sin errores                                      │
│                                                                              │
│  ⚙️ SETTINGS                                                                  │
│  [ ] SECRET_KEY lee de variable de entorno                                   │
│  [ ] DEBUG lee de variable de entorno                                        │
│  [ ] ALLOWED_HOSTS lee de variable de entorno                                │
│  [ ] python manage.py check → sin errores                                    │
│                                                                              │
│  🔑 VARIABLES DE ENTORNO                                                     │
│  [ ] .env existe y funciona                                                  │
│  [ ] .env.example existe en el repo                                          │
│  [ ] .env está en .gitignore                                                 │
│                                                                              │
│  📂 GIT                                                                      │
│  [ ] .gitignore completo (venv, .env, __pycache__, db.sqlite3)               │
│  [ ] Repo limpio, todo comiteado                                             │
│  [ ] .env nunca en el historial                                              │
│  [ ] Subido a GitHub/GitLab                                                  │
│                                                                              │
│  📦 DEPENDENCIAS                                                             │
│  [ ] requirements.txt actualizado con versiones fijadas                      │
│  [ ] Instalando desde requirements.txt, el proyecto arranca                  │
│                                                                              │
│  📖 DOCUMENTACIÓN                                                            │
│  [ ] README.md con instrucciones de instalación                              │
│                                                                              │
│  🧪 TESTING                                                                  │
│  [ ] Todas las páginas cargan sin errores                                    │
│  [ ] Todos los formularios funcionan                                         │
│  [ ] Responsive verificado en celular                                        │
│  [ ] Probado en modo incógnito                                               │
│                                                                              │
│  ✨ CÓDIGO LIMPIO                                                             │
│  [ ] Sin prints de debugging                                                 │
│  [ ] Sin código comentado innecesario                                        │
│  [ ] Sin contraseñas en el código                                            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

> 💡 **El día de deploy:** si todo esto tiene ✅, deploy va a ser rápido y sin drama. Si hay ❌, cada uno es un problema que **vas a tener que resolver bajo presión**.

---

---

# ❌ 18. Los 10 Problemas que Siempre Aparecen el Día de Deploy

---

Estos son los problemas que aparecen **cada vez**. Si los resuelves antes, el día de deploy es tranquilo.

### 1. "El sitio carga sin CSS"

**Causa:** No hiciste `collectstatic`, o los templates tienen rutas hardcodeadas en vez de `{% static %}`.

---

### 2. "Me da error 500 pero no sé por qué"

**Causa:** `DEBUG = False` y no configuraste logging. Sin logs, no hay información.

---

### 3. "Las migraciones fallan en el servidor"

**Causa:** Tienes migraciones que dependen de datos que no existen, o las migraciones no están al día.

---

### 4. "No puedo entrar al admin"

**Causa:** No creaste un usuario con permisos de administrador en el servidor.

---

### 5. "Los formularios dan error 403 Forbidden"

**Causa:** Falta `{% csrf_token %}` en los formularios POST.

---

### 6. "Los links me llevan a páginas que no existen"

**Causa:** URLs con nombres incorrectos o vistas que no están implementadas.

---

### 7. "En mi computador funciona pero en el servidor no"

**Causa:** Faltan dependencias en `requirements.txt`, o las variables de entorno no están configuradas.

---

### 8. "La base de datos está vacía"

**Causa:** Las migraciones crean las tablas, no los datos. Necesitas un plan para cargar datos iniciales.

---

### 9. "Se ve terrible en el celular"

**Causa:** No se verificó responsive. El meta viewport falta o el CSS no tiene media queries.

---

### 10. "Todo tarda mucho en cargar"

**Causa:** Imágenes sin optimizar (5MB cada una), o muchas queries innecesarias a la base de datos.

---

> 💡 **Los 10 problemas de arriba son 100% evitables.** Cada uno tiene una entrada en el mega-checklist. Si los verificaste antes, no aparecen el día de deploy.

---

---

# 🏁 Resumen de la Clase

---

## ✅ Lo que cubrimos hoy

| Área                     | La pregunta clave                                         |
| :----------------------- | :-------------------------------------------------------- |
| **Estructura**           | ¿Mi proyecto está organizado de forma predecible?         |
| **Modelos / BD**         | ¿Las migraciones están al día? ¿Los datos existen?       |
| **Vistas / URLs**        | ¿Todo está conectado y protegido?                         |
| **Templates / Frontend** | ¿Se ve completo, responsive y profesional?                |
| **Formularios**          | ¿Validan, guardan, y muestran errores?                    |
| **Autenticación**        | ¿Login/logout funciona? ¿Las vistas privadas están protegidas? |
| **Archivos estáticos**   | ¿Usan {% static %}? ¿collectstatic funciona?              |
| **Settings**             | ¿Lee de variables de entorno? ¿check --deploy da OK?      |
| **Variables de entorno** | ¿.env existe, funciona, y está en .gitignore?             |
| **Git**                  | ¿Repo limpio, .gitignore completo, subido a GitHub?       |
| **Dependencias**         | ¿requirements.txt actualizado con versiones fijadas?      |
| **Datos iniciales**      | ¿Hay plan para cargar datos en producción?                |
| **Testing**              | ¿Probé todo manualmente, incluyendo responsive?           |
| **Código limpio**        | ¿Sin prints, sin hardcodes, sin código muerto?            |
| **README**               | ¿Alguien puede clonar e instalar siguiendo el README?     |

---

> _"El día de deploy no es para terminar tu proyecto. Es para **publicarlo**. Llega con todo listo y ese día es una fiesta. Llega con cosas a medias y ese día es una pesadilla."_

---

## 📚 Referencias (APA 7ª ed.)

Django Software Foundation. (2025). _Deployment checklist_. https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

Django Software Foundation. (2025). _Managing static files_. https://docs.djangoproject.com/en/stable/howto/static-files/

Django Software Foundation. (2025). _Settings reference_. https://docs.djangoproject.com/en/stable/ref/settings/

Django Software Foundation. (2025). _How to deploy Django_. https://docs.djangoproject.com/en/stable/howto/deployment/

---
