# Technical Challenge — Backend Developer

**Empresa:** Mystale Labs (ficticia)
**Posición:** Backend Developer Jr. — Python / Django
**Modalidad:** Take-home · Individual

---

## Descripción

Mystale Labs desarrolla plataformas de catalogación científica. Para esta posición buscamos desarrolladores capaces de construir funcionalidades completas con criterio técnico propio, sin supervisión.

Este challenge simula una tarea real del equipo: levantar un módulo nuevo en un proyecto Django existente.

**Tiempo estimado:** 90 minutos.

---

## El requerimiento

Nuestro equipo de investigación necesita un sistema web interno para catalogar **criaturas energéticas** relevadas en campo — entidades con atributos elementales y de combate, conceptualmente similares a lo que la industria del entretenimiento popularizó con franquicias como Pokémon. El sistema debe permitir registrar nuevas entradas y consultar el catálogo existente.

No hay wireframe. No hay diseño entregado. Se espera criterio de producto.

---

## Alcance funcional

El sistema debe cubrir como mínimo:

- Un catálogo navegable de criaturas con sus datos relevantes
- Un formulario para registrar nuevas entradas desde la interfaz web
- Capacidad de filtrar el catálogo por categoría elemental
- El esquema de base de datos debe evolucionar en al menos dos pasos de migración distintos y documentados

Cada criatura del catálogo tiene al menos: nombre, categoría elemental, nivel de amenaza, descripción de campo, y estadísticas de combate relevadas.

Las categorías elementales disponibles son: fuego, agua, tierra, rayo, sombra, cristal, viento, hielo.

### Referencia de producto

Nuestro equipo de producto describió la experiencia esperada como una **interfaz tipo Pokédex**: cada criatura exhibida como una ficha individual con identidad visual propia, donde los datos se leen de un vistazo. Cómo se traduce eso técnicamente al template es decisión del candidato.

---

## Requisitos técnicos

- Django como framework backend
- Base de datos: SQLite es aceptable para esta prueba
- Templates Django para el frontend (sin frameworks JS)
- El esquema de la base de datos debe quedar versionado a través del sistema de migraciones de Django
- Se evaluará que el historial de migraciones sea coherente y reversible
- El formulario debe manejar validaciones correctamente

---

## Criterios de evaluación

El equipo técnico revisará:

| Criterio | Peso |
| :--- | :--- |
| Modelado de datos (campos, tipos, restricciones) | 20% |
| Historial de migraciones limpio y funcional | 25% |
| Vistas y lógica backend | 20% |
| Calidad del template y experiencia de uso | 25% |
| Estructura general del proyecto y código legible | 10% |

---

## Entregable

- Repositorio público en GitHub con el código completo
- `README.md` con instrucciones claras para correr el proyecto localmente
- Cualquier decisión técnica no obvia debe estar explicada brevemente en el `README.md`

**No se aceptan entregas sin README funcional.**

---

> _Mystale Labs valora la claridad técnica sobre la velocidad. Preferiríamos ver menos funcionalidades bien ejecutadas que todo el alcance con código apresurado._

---
