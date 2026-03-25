# 🛒 Práctica — Módulo 7 · Clase 12

## Optimización de Rendimiento en Django ORM

---

## 🎯 Objetivo

En esta práctica vas a trabajar con **SlowMart**, un proyecto Django de e-commerce que funciona correctamente pero tiene **graves problemas de rendimiento** intencionales. Tu misión es diagnosticar los cuellos de botella, aplicar las técnicas de optimización vistas en la teoría, y documentar cada mejora que realices.

---

## 📦 Repositorio del Proyecto

Clona el repositorio con el siguiente comando:

```bash
git clone git@github.com:arielrosenmann94/django_ecommerce_optimization.git
```

O bien por HTTPS:

```
https://github.com/arielrosenmann94/django_ecommerce_optimization
```

> 📖 **Toda la documentación del proyecto** — estructura, modelos, configuración del entorno y datos de prueba — está disponible directamente en el `README.md` del repositorio. Lee el README completo antes de comenzar.

---

## 📋 Instrucciones

1. **Clona** el repositorio y configura el entorno virtual siguiendo las instrucciones del README
2. **Ejecuta las migraciones** y carga los datos de prueba con el script de seed incluido
3. **Navega** por las vistas del proyecto y observa los tiempos de carga
4. **Instala Django Debug Toolbar** para ver las consultas SQL que genera cada vista
5. **Identifica** los problemas de rendimiento en el código
6. **Aplica** las correcciones usando las técnicas de la teoría
7. **Documenta** cada cambio realizado

---

## ✅ Entregable

Un **documento breve** (máximo 2 páginas) que incluya:

| Sección                  | Qué debe contener                                                  |
| ------------------------ | ------------------------------------------------------------------ |
| **Bug encontrado**       | Descripción del problema y en qué archivo está                     |
| **Antes**                | Cantidad de queries y/o tiempo de carga antes de la corrección     |
| **Solución aplicada**    | Qué técnica usaste (`select_related`, `count()`, índices, etc.)    |
| **Después**              | Cantidad de queries y/o tiempo de carga después de la corrección   |

---

## 📊 Criterios de Evaluación

| Criterio                                                 | Peso |
| -------------------------------------------------------- | ---- |
| Reducción de queries (medido con Django Debug Toolbar)   | 30%  |
| Uso correcto de `select_related` / `prefetch_related`    | 20%  |
| Uso de `aggregate()` / `annotate()`                      | 15%  |
| Implementación de paginación                             | 10%  |
| Añadir índices a modelos                                 | 10%  |
| Uso de `.exists()`, `.count()`, `.only()`                | 10%  |
| Documentación de cambios                                 | 5%   |

---

> _"No se trata de que el sistema funcione — se trata de que funcione bien, incluso con miles de registros."_

---
