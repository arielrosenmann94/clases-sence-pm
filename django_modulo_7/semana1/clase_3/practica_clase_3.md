# Práctica de Clase 3 — Módulo 7

# 🔨 Proyecto Real: Plataforma de Subastas de Antigüedades

---

_Felicitaciones. Una PYME dedicada a las subastas presenciales de antigüedades quiere dar el salto al mundo digital, pero no tiene plataforma web. Los contrataron a ustedes para crear su primera plataforma de subastas en línea desde cero. A continuación tienen el brief técnico exactamente como lo recibirían en un trabajo real._

---

# 📋 FASE 0 — Contexto del Negocio

**Cliente:** MartilloVirtualDjango — PYME chilena de subastas de antigüedades.

**Historia:** Don Roberto lleva 18 años organizando subastas presenciales de antigüedades en un galpón de Barrio Italia, Santiago. Cada sábado reúne entre 40 y 80 personas que ofertan a viva voz por relojes antiguos, muebles restaurados, vinilos, joyas de época y arte decorativo. El problema: solo llega gente que vive cerca. Don Roberto quiere llegar a coleccionistas de todo Chile (y eventualmente de Latinoamérica) sin perder la emoción de la puja en vivo.

**Problema:** El cliente necesita un MVP (Producto Mínimo Viable) donde los usuarios puedan publicar piezas de antigüedades, otros usuarios puedan ofertar, y el sistema determine automáticamente al ganador cuando se cierra la subasta.

**Stack tecnológico obligatorio:**

- Python + Django
- PostgreSQL (Supabase)
- HTML + CSS + JavaScript (Frontend)

**Fecha de entrega:** Final de esta clase.

---

# 📐 FASE 1 — Historias de Usuario (ANTES de escribir código)

> _"En una empresa real, NADIE escribe código antes de planificar. El 80% de los errores en producción se originan en una mala planificación, no en un mal código."_
> _(Fuente: IBM Systems Sciences Institute, 2020)_

Antes de tocar el teclado, lee estas historias de usuario. Representan lo que Don Roberto y sus clientes necesitan. Tu trabajo es traducir cada historia en modelos, vistas y lógica de Django.

---

### HU-01: Registro de Coleccionistas

> _"Como visitante del sitio, quiero poder registrarme con mi nombre, correo electrónico y una contraseña, para poder participar en las subastas."_

**Criterios de aceptación:**

- El nombre de usuario debe ser único en todo el sistema.
- El correo electrónico debe tener formato válido y no puede repetirse.
- Al registrarme, el sistema me asigna un perfil público que muestra mi reputación: cuántas subastas he ganado y cuántas he creado.
- Cualquier usuario puede actuar como **Vendedor** (publica piezas) y como **Comprador** (oferta en subastas) simultáneamente.

---

### HU-02: Publicar una Pieza en Subasta

> _"Como vendedor, quiero publicar una antigüedad para subasta, indicando todos sus detalles, para que los coleccionistas interesados puedan verla y ofertar."_

**Criterios de aceptación:**

- Debo ingresar: título descriptivo de la pieza, descripción detallada con la historia y condición del artículo, al menos una fotografía, precio base (monto mínimo desde donde empiezan las pujas), fecha y hora exacta de cierre de la subasta, y la categoría de la pieza.
- El sistema NO debe permitir crear una subasta con fecha de cierre en el pasado.
- Una subasta recién creada aparece con estado **"Activa"**.

**Ejemplo real de Don Roberto:**

> _"Tengo un gramófono Columbia de 1920 en excelente estado. Quiero publicarlo con un precio base de $85.000 y que la subasta cierre el viernes a las 20:00."_

---

### HU-03: Ofertar en una Subasta

> _"Como comprador, quiero poder ofertar en una subasta activa, para intentar ganar la pieza que me interesa."_

**Criterios de aceptación:**

- Solo usuarios registrados pueden ofertar (excepto el dueño de la pieza, que NO puede ofertar en su propia subasta).
- La oferta debe ser **estrictamente mayor** que la oferta más alta actual.
- Si no hay ofertas previas, la oferta debe ser **igual o mayor** al precio base.
- El sistema registra quién ofertó, cuánto ofertó y exactamente cuándo lo hizo.
- Un usuario puede ofertar múltiples veces en la misma subasta (superándose a sí mismo o a otros).
- El sistema rechaza ofertas en subastas que ya cerraron.

**Ejemplo real:**

> _"Mariana de Valparaíso ve el gramófono y oferta $90.000. Luego Carlos de Temuco oferta $105.000. Mariana vuelve y sube a $120.000. Esto es exactamente lo que pasa en el galpón de Don Roberto, pero ahora en línea."_

---

### HU-04: Cierre Automático de la Subasta

> _"Como sistema, debo cerrar automáticamente las subastas cuando llegue la fecha y hora de cierre, y determinar al ganador."_

**Criterios de aceptación:**

- El estado cambia a **"Cerrada"**.
- La **oferta más alta** determina al ganador.
- Si nadie ofertó, la subasta se marca como **"Desierta"**.
- Tanto el vendedor como el ganador deben poder ver claramente el resultado.

**Ejemplo real:**

> _"El viernes a las 20:00 la subasta del gramófono cierra. Mariana ganó con $120.000. Don Roberto ve en su panel que la pieza fue vendida. Mariana ve en su perfil que ganó la subasta."_

---

### HU-05: Historial Público de Ofertas

> _"Como visitante, quiero ver el historial completo de ofertas de una subasta, para saber si vale la pena entrar a competir."_

**Criterios de aceptación:**

- Cada subasta muestra públicamente todas las ofertas (quién, cuánto, cuándo), ordenadas de la más reciente a la más antigua.
- Cada usuario puede ver en su perfil: las subastas que creó, en las que ofertó y las que ganó.

---

### HU-06: Categorías de Antigüedades

> _"Como visitante, quiero filtrar las subastas por categoría, para encontrar rápido lo que me interesa."_

**Criterios de aceptación:**

- El sistema tiene un catálogo predefinido de categorías: Relojes, Muebles, Vinilos y Música, Joyería, Arte y Cuadros, Libros y Manuscritos, Porcelana y Cristalería, Juguetes Vintage, Otros.
- Cada subasta pertenece a exactamente una categoría.
- Los visitantes pueden filtrar por categoría desde la página principal.

---

### HU-07: Panel del Vendedor

> _"Como vendedor, quiero ver un resumen de mis subastas activas y cerradas, para saber cómo va mi negocio."_

**Criterios de aceptación:**

- Ver subastas activas con la oferta más alta actual.
- Ver subastas cerradas con el precio final y el ganador.
- Ver estadísticas: total de subastas creadas, porcentaje de subastas exitosas (con al menos una oferta).

---

### HU-08: Página Principal para Atraer Coleccionistas

> _"Como visitante, quiero llegar a una página principal atractiva que me muestre las subastas más interesantes."_

**Criterios de aceptación:**

- Mostrar las subastas que están por cerrar pronto (urgencia).
- Mostrar las subastas con más ofertas (prueba social).
- Mostrar las subastas recién publicadas (novedad).
- Incluir un buscador por título de pieza.

---

# 🎨 FASE 2 — Identidad Visual del Proyecto

Don Roberto contrató a un diseñador que definió la identidad visual de MartilloVirtualDjango. Debes usar estos elementos en tu implementación:

### Paleta de Colores

| Color | Código HEX | Uso |
| ----- | ---------- | --- |
| Negro Ébano | `#1A1A2E` | Fondo principal, transmite elegancia y seriedad |
| Dorado Antiguo | `#C9A84C` | Acentos, botones destacados, sensación de lujo |
| Blanco Hueso | `#F5F0E8` | Texto sobre fondo oscuro, tarjetas, espacios limpios |
| Borgoña | `#6B2D3E` | Alertas de urgencia, badges de "cerrando pronto" |
| Gris Ceniza | `#8C8C8C` | Texto secundario, bordes sutiles, información de apoyo |

### Tipografía (Google Fonts)

- **Títulos:** `Playfair Display` — Serif elegante que evoca tradición y prestigio.
- **Cuerpo:** `Inter` — Sans-serif moderna, altamente legible en pantallas.

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
```

---

# 🎯 FASE 3 — Requisitos de Frontend y Experiencia Visual

> _Don Roberto fue muy claro: "Si la página parece un formulario de gobierno, mis coleccionistas no van a confiar. Necesito que se vea como una casa de subastas de lujo."_

### Requisitos visuales obligatorios:

1. **Contador regresivo animado** en cada tarjeta de subasta activa (días, horas, minutos, segundos).
2. **Efecto hover** en las tarjetas de producto que las eleve visualmente (transform + shadow).
3. **Animación de entrada** (fade-in o slide-up) cuando las tarjetas cargan en pantalla.
4. **Botón "Ofertar" con efecto pulso** que atraiga la atención del ojo periférico.
5. **Confirmación visual animada** cuando una oferta es aceptada (checkmark + color verde).
6. **Diseño 100% responsivo** que funcione en celular, tablet y escritorio sin romper la experiencia.
7. **Diseño moderno y actual** 🔥 — Aunque la temática es de antigüedades, la plataforma debe verse como si hubiera sido diseñada HOY. Nada de interfaces que parezcan de 2015. Usa técnicas actuales: glassmorphism, gradientes sutiles, micro-animaciones, sombras suaves y espaciado generoso.
8. **Encuentra tus propios efectos WOW** 🤯 — Investiga, experimenta y agrega al menos 2 efectos visuales adicionales que NO estén en esta lista. Algo que cuando Don Roberto lo vea diga: _"Esto es exactamente lo que necesitaba."_ Sorprende al cliente.

---

# 🚀 ¡Manos a la obra!

1. Lee las 8 historias de usuario completas.
2. Construye los modelos, las migraciones, y las vistas.
3. Implementa la identidad visual entregada en la Fase 2.
4. Prueba. Itera. Sorprende.
