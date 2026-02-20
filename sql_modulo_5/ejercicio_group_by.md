# 🏴‍☠️ Guía de Estudio Autónomo: El Tesoro del GROUP BY

¡Ahoy, estudiante de los datos! ⚓

Estás a punto de embarcarte en la aventura de aprender a usar `GROUP BY` y `HAVING`. Muchos han intentado entender cómo agrupar datos y han terminado en el fondo del mar, enredados entre sumas y filtros que no funcionan.

Pero tú tienes ventaja. Hoy usarás el **"Método de los Cofres Piratas"** para estudiar esto a tu propio ritmo.

Lee la teoría, imagina el proceso visualmente y luego resuelve los desafíos en tu motor SQL.

---

## 🛠️ Paso 1: Carga el Botín en tu Barco (Preparación)

Abre DBeaver, pgAdmin o la consola SQL que prefieras, copia este código y ejecútalo. Esto creará la tabla con los tesoros que saquearon 4 piratas en 3 barcos distintos:

```sql
CREATE TABLE lateral_botin_flota (
    id_saqueo SERIAL PRIMARY KEY,
    barco VARCHAR(50),
    pirata VARCHAR(50),
    tipo_tesoro VARCHAR(50),
    valor_monedas INT
);

INSERT INTO lateral_botin_flota (barco, pirata, tipo_tesoro, valor_monedas) VALUES
('La Perla Negra', 'Jack', 'Doblón de Oro', 500),
('La Perla Negra', 'Jack', 'Doblón de Plata', 100),
('La Perla Negra', 'Will', 'Doblón de Oro', 200),
('La Venganza', 'Barbanegra', 'Cáliz Sagrado', 1000),
('La Venganza', 'Barbanegra', 'Cáliz Sagrado', 1000),
('La Venganza', 'Anne', 'Doblón de Oro', 300),
('La Venganza', 'Anne', 'Doblón de Plata', 50),
('El Holandés', 'Davy', 'Perla Maldita', 800),
('El Holandés', 'Davy', 'Doblón de Oro', 400),
('El Holandés', 'Davy', 'Esmeralda', 600);
```

¡Listo! Todos los tesoros están revueltos en la cubierta. Ahora vamos a organizarlos.

---

---

## 📦 Nivel 1: El Arte de Hacer Cofres (GROUP BY Básico)

### 📖 La Teoría Visual

Imagina que el contramaestre grita: _"¡Quiero saber cuánto dinero recaudó CADA BARCO!"_

Si haces un `SELECT SUM(valor_monedas)` simple, SQL sumará TODO (4950 monedas) y te dará un solo número. Eso no te sirve para saber cuánto hizo cada barco. Necesitas separarlo.

El `GROUP BY` es como gritar: **"¡Traigan 3 cofres grandes! Escriban 'La Perla Negra' en el primero, 'La Venganza' en el segundo, y 'El Holandés' en el tercero. ¡Y ahora tiren cada fila (tesoro) adentro de su respectivo cofre!"**

Una vez que los cofres están armados y cerrados, SQL aplica la función matemática (`SUM`, `COUNT`, `AVG`) **SOLO al contenido que quedó dentro del cofre**.

### ⚔️ Desafío 1: El Botín por Barco

**Tu Misión:** Escribe una consulta SQL que devuelva dos columnas: el nombre del `barco` y su `botin_total` (la suma de sus `valor_monedas`).

_<details><summary>💡 Pista para el Desafío 1 (Haz clic para ver)</summary>_
_Selecciona las columnas barco y SUM(valor_monedas). Luego dile a SQL que agrupe explícitamente usando la orden `GROUP BY barco`._
_</details>_

---

## 🗃️ Nivel 2: Cofres dentro de Cofres (GROUP BY Múltiple)

### 📖 La Teoría Visual

El Capitán dice: _"¡Está excelente saber cuánto hizo cada barco, pero ahora quiero saber cuánto recolectó CADA PIRATA EN SU RESPECTIVO BARCO!"_

¿Qué cambia? Ahora no nos bastan 3 cofres grandes, necesitamos **subgrupos**. Si le dices a SQL `GROUP BY barco, pirata`, SQL dirá: _"¡Abran el cofre grande de La Perla Negra y metan dos cofres pequeños, uno etiquetado 'Jack' y otro 'Will'! Y metan los tesoros ahí."_

SQL crea un cofre nuevo por cada **combinación única** de barco y pirata.

> ⚠️ **LA LEY INQUEBRANTABLE:** Si en tu `SELECT` pides ver el `barco` y el `pirata`, **AMBAS columnas** deben estar escritas después del `GROUP BY`. Si le pides a SQL que te muestre al "pirata" pero solo le dijiste `GROUP BY barco`, SQL dará un error porque no sabrá de qué pirata sacar el nombre si la caja entera se llama "La Perla Negra".

### ⚔️ Desafío 2: La Cuenta Personal

**Tu Misión:** Muestra el `barco`, el `pirata` y su suma total de tesoros bajo el alias `botin_personal`.

---

## 🛡️ Nivel 3: El Guardia Ciego vs El Tasador (WHERE vs HAVING)

### 📖 La Teoría Visual (¡ESTO ES LO MÁS IMPORTANTE DEL TUTORIAL!)

El Capitán pide: _"Hazme un reporte de cuánto botín total tiene cada pirata. **PERO**, solo muéstrame a los piratas que sumen **más de 500 monedas en total**, el resto no me importa."_

Si tienes poca experiencia, la lógica te diría que uses un `WHERE`:
❌ `... WHERE valor_monedas > 500 GROUP BY pirata;`

**¡ESTO DESTRUIRÁ TUS DATOS! ¿Por qué?**
Porque el `WHERE` es un **Guardia Ciego**. Él trabaja patrullando la cubierta del barco _ANTES_ de que existan los cofres.
El Guardia Ciego mira el primer tesoro de Jack (500 de oro) y dice _"¿Es MAYOR a 500? No. ¡Tíralo al mar!"_. Luego mira las 100 de plata de Jack y también las tira al mar. En resumen, **los borra de la faz de la tierra antes de que se haga la suma real**.
Cuando se arma la caja de botín de Jack, la suma dará cero. Jack desapareció del reporte, a pesar de que en verdad sí superaba los 500 (500 + 100 = 600) y **debía** aparecer en tu lista final.

**La Solución: El HAVING**
Para evaluar "sumas matemáticas que ya están calculadas", necesitas un **Tasador** que llegue a trabajar **DESPUÉS** de que los cofres están cerrados. Ese tasador mágico se llama `HAVING`.
Se coloca _siempre_ después del `GROUP BY`. Él abre la caja final y dice: _"A ver Jack, ¿La suma completa de todas tus cosas adentro (`SUM(valor_monedas)`) suma más de 500? Perfecto, ¡pasas al reporte!"_

### ⚔️ Desafío 3: El Club de los 500

**Tu Misión:** Agrupa por `pirata`, suma todos sus tesoros e imprime el reporte. Usa la instrucción correcta al final para que **SOLO** aparezcan en pantalla los piratas que superaron las 500 monedas acumuladas (Deberían salirte solo Davy, Jack y Barbanegra).

---

## 💎 Nivel 4: Los 5 Monóculos Mágicos (Agregaciones Simultáneas)

### 📖 La Teoría Visual

Una vez que agrupaste en un cofre sellado (ej. por `barco`), puedes pedirle al analista que se ponga varios tipos de monóculos frente al ojo y revise el interior del cofre de **múltiples formas diferentes al mismo tiempo**, todo sin escribir otro query distinto:

- _"Súmalo todo"_ (`SUM`)
- _"Cuéntame cuántas unidades / pilas de tesoros hay en total"_ (`COUNT`)
- _"Dime cuánto vale la cosa más barata que hay aquí dentro"_ (`MIN`)
- _"Dime cuánto vale la cosa más valiosa"_ (`MAX`)
- _"Saca un promedio matemático de todo lo que robaron"_ (`AVG`)

### ⚔️ Desafío 4: El Gran Resumen Estadístico

**Tu Misión:** Agrupa por `barco` y en tu `SELECT` inicial, extrae estas 5 estadísticas (dales nombres bonitos usando `AS`):

1. El barco (obvio).
2. Cuántos objetos trajeron (`COUNT` al id_saqueo)
3. Suma total de ganancias.
4. El tesoro más mísero (mínimo).
5. El tesoro más valeroso (máximo).

---

## 🏴‍☠️ Nivel 5: Desafío Jefe - Lógica en Inversa (Pensamiento Lateral)

_Si resuelves esto solo, estás listo para dominar el mundo SQL analítico._

La Reina Pirata decreta lo siguiente:
_"Muéstrame a cada pirata y suma absolutamente todo su botín._
_¡PERO DETESTO LA PLATA! Si descubro que el cofre de un pirata contiene **AUNQUE SEA UN 'Doblón de Plata'** escondido adentro... ¡Tira TODO su cofre entero (incluso el oro) al mar y bórralo de la lista oficial!"_

### ⚔️ Desafío 5: Salvando los Cuellos

Este ejercicio es traicionero.

1. Si usas el Guardia Ciego (`WHERE tipo_tesoro != 'Doblón de Plata'`), cometerás el error novato. El guardia ciego quitará solo las moneditas de plata pero igual dejará entrar el oro de Anne y de Jack a sus cofres... Y tú **necesitas descartar el cofre de Jack COMPLETO**.
2. ¡Necesitas sumar el cofre de todos y luego hacer el descarte condicional en la fase del Tasador (`HAVING`) evaluando el interior!

**Tu Misión:** Escribe una consulta que agrupe por `pirata` mostrando su botín total. Su Usa `HAVING` para borrar de la cara de la tierra a cualquier pirata que haya traído plata, dejando finalmente listados **SOLO** a Will, Barbanegra y Davy, mostrando sus botines limpios e íntegros.

_<details><summary>☠️ El Truco Final (Haz clic aquí si te rinndest)</summary>_
_El Tasador (El `HAVING`) puede evaluar condicionales lógicas si sabes combinarlas con una función matemática (por ej SUM)._
_Intenta hacer que el Tasador invente un "filtro a la mala" adentro del cajón: **Cuenta cuántos tipos de tesoro eran de plata**. Si descubres que es igual a 0, estás a salvo y dejas pasar al pirata:_
_`HAVING SUM(CASE WHEN tipo_tesoro = 'Doblón de Plata' THEN 1 ELSE 0 END) = 0;`_
_</details>_
