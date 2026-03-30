# 🎯 Actividades — Módulo 8: Portafolio Profesional

---

---

# Actividad 1 — Test de los 10 Segundos

---

## Objetivo

Evaluar portafolios reales aplicando el criterio de los 6 patrones de análisis.

## Consigna

Abre cada uno de los siguientes 12 portafolios durante **10 segundos**:

| # | URL |
|---|-----|
| 1 | https://www.dharmatun.cl/portafolio/diseno-web/ |
| 2 | https://nexodigital.cl/portafolio/ |
| 3 | https://mediadream.cl/ |
| 4 | https://ladonorte.cl/portafolio-de-paginas-web/ |
| 5 | https://www.agencianaranja.cl/portafolio-web/ |
| 6 | https://bigbuda.cl/proyectos |
| 7 | https://www.diseñowebmiami.com/portafolio |
| 8 | https://www.cutedigitalmedia.com/es/nuestros-trabajos/ |
| 9 | https://suagencia.com/portafolio/ |
| 10 | https://papirogroup.com/portafolio/ |
| 11 | https://imaginity.com/es/portfolio/ |
| 12 | https://3pixelsmedia.com/es#Portfolio |


Para cada uno, responde mentalmente:

- ¿Qué hace esta persona/empresa?
- ¿Le darías una entrevista?
- ¿Qué fue lo primero que te llamó la atención?

Registra tus hallazgos usando los 6 criterios:

```
REGISTRO DE ANÁLISIS
────────────────────

Portafolio #___: _______________________

🔍 CLARIDAD:        ¿Entendí qué hace en 5 segundos?    □ Sí  □ No
🔍 PROYECTOS:       ¿Tienen nombre + descripción?        □ Sí  □ No
🔍 NAVEGACIÓN:      ¿Encontré todo en 3 clics?           □ Sí  □ No
🔍 CONTACTO:        ¿Hay forma de contacto visible?      □ Sí  □ No
🔍 DISEÑO:          ¿Se ve profesional?                  □ Sí  □ No
🔍 DIFERENCIACIÓN:  ¿Tiene algo que lo haga único?       □ Sí  □ No

Lo mejor: ___________________________________
Lo peor:  ___________________________________
```

---

---

# Actividad 2 — Construye tu Portafolio en Django

---

## Objetivo

Implementar tu portafolio profesional **dentro del mismo proyecto Django** que ya tienes funcionando (tu proyecto del curso). El portafolio será una sección más de tu aplicación.

## Consigna

Agrega una sección de **portafolio** a tu proyecto Django existente que incluya:

```
LO QUE DEBE TENER TU PORTAFOLIO EN DJANGO:
───────────────────────────────────────────

□ Página "Sobre Mí" con tu bio profesional
□ Sección de proyectos (mínimo 3) con:
   → Nombre del proyecto
   → Descripción breve
   → Tecnologías usadas
   → Imagen o captura del resultado
   → Enlace (si existe)
□ Sección de contacto (correo, redes)
□ Una sección diferenciada para tu CASO DE ESTUDIO
   → Los 8 puntos del caso de estudio (ver teoría)
□ Diseño responsivo (que funcione en celular)
```

## Guía técnica rápida

```
Pasos sugeridos en Django:
──────────────────────────

1. Crear una app "portafolio" (o agregar vistas al app existente)
   → python manage.py startapp portafolio

2. Crear los modelos necesarios:
   → Proyecto: nombre, descripción, tecnologías, imagen, enlace
   → CasoEstudio: los 8 campos del caso de estudio

3. Crear las vistas y templates:
   → portafolio/templates/portafolio/index.html
   → portafolio/templates/portafolio/proyecto_detalle.html
   → portafolio/templates/portafolio/caso_estudio.html

4. Agregar las URLs al proyecto principal

5. Cargar los datos (puede ser desde el admin o fixtures)

6. Aplicar estilos responsivos
```

## Entregable

- ✅ Portafolio funcional dentro de tu proyecto Django
- ✅ Mínimo 3 proyectos con descripción y captura
- ✅ Caso de estudio desarrollado con los 8 puntos
- ✅ Información de contacto visible
- ✅ Diseño responsivo

---

---

# Actividad 3 — Elevator Pitch

---

## Objetivo

Crear y practicar una presentación personal de **máximo 60 segundos** que complemente tu portafolio.

## Consigna

### Paso 1 — Escribe tu pitch usando la fórmula

```
"Hola, soy [NOMBRE].
Soy [ROL PROFESIONAL].
Desarrollo [TIPO DE PRODUCTOS/PROYECTOS].
Me especializo en [HABILIDADES / HERRAMIENTAS].
Lo que más me motiva es [TU DIFERENCIADOR].
Actualmente estoy buscando [TIPO DE OPORTUNIDAD]."

──────────────────────────
⏱️ Máximo: 60 segundos
──────────────────────────
```

### Paso 2 — Ejemplo de referencia

> _"Hola, soy Carolina Muñoz. Soy desarrolladora junior con enfoque en Python y Django. Durante mi formación desarrollé una app de gestión de inventario que redujo el tiempo de búsqueda de productos en un 60%. Me apasiona crear soluciones que simplifiquen procesos reales. Estoy buscando mi primera oportunidad en una empresa que valore el aprendizaje continuo."_

### Paso 3 — Autoevaluación

Revisa tu pitch con estos criterios:

| ✅ Bien | ❌ Evitar |
|--------|----------|
| "Soy desarrolladora Python" | "Hago muchas cosas de tecnología" |
| "Desarrollé una app de inventario" | "Hice varios proyectos" |
| "Redujo tiempos en un 60%" | "Funcionaba bien" |
| "Busco oportunidades en desarrollo web" | "Bueno, eso es todo" |

## Entregable

- ✅ Pitch escrito (puede estar en un documento o en la sección "Sobre Mí" de tu portafolio)

---

---

# Actividad 4 — Mejora tu Portafolio con IA

---

## Objetivo

Usar herramientas de inteligencia artificial para **pulir las descripciones** de tus proyectos en el portafolio.

## Consigna

### Paso 1 — Elige un proyecto de tu portafolio

Selecciona uno de los proyectos que ya cargaste y escribe una descripción básica.

### Paso 2 — Usa este prompt en ChatGPT o Gemini

```
PROMPT:
───────

"Tengo un proyecto llamado [NOMBRE] hecho con [TECNOLOGÍAS].
El proyecto [QUÉ HACE].
El desafío principal fue [DESAFÍO].
Redáctame una descripción profesional de 4 líneas
para mi portafolio, orientada a un reclutador de RRHH
que no es técnico."
```

### Paso 3 — Compara y personaliza

```
COMPARACIÓN:
────────────

Tu versión original:  ___________________________________
                      ___________________________________

Versión de la IA:     ___________________________________
                      ___________________________________

Tu versión final
(mezcla de ambas):    ___________________________________
                      ___________________________________
```

> ⚠️ **Recuerda:** La IA es una herramienta, no un reemplazo. Tu voz personal es tu marca. Personaliza siempre el resultado.

## Entregable

- ✅ Al menos 1 descripción de proyecto mejorada con IA y personalizada

---

---

# Actividad 5 — Tiempo de Trabajo en el ABP

---

## Objetivo

Avanzar en los entregables del proyecto integrador (ABP Módulos 8 y 9).

## Prioridades

```
¿Qué hacer ahora?
──────────────────

□  Completar el portafolio en Django con al menos 3 proyectos
□  Desarrollar el caso de estudio completo (los 8 puntos)
□  Asegurarse de que cada proyecto tenga descripción + imagen
□  Verificar que los enlaces funcionen
□  Probar que el portafolio se vea bien en celular
□  Agregar datos de contacto visibles
```

> 💡 Lo que hagas hoy en clase ya es avance directo en tu entregable del ABP. Aprovecha este espacio.

---
