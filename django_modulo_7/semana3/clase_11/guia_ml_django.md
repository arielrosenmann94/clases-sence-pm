# 🤖 Guía Completa: Machine Learning y Analisis de Datos con Django

## Inteligencia Artificial Aplicada en Proyectos Web — Actualizada 2026

> **Objetivo:** Aprender a integrar modelos de Machine Learning dentro de una aplicación Django, desde la instalación de librerías hasta el despliegue de predicciones en tiempo real a través de una API REST.

---

## 🗺️ Índice

| #      | Tema                                                     |
| :----- | :------------------------------------------------------- |
| **1**  | ¿Qué es Machine Learning y por qué integrarlo en Django? |
| **2**  | Ecosistema de Librerías ML en Python (2026)              |
| **3**  | Preparación del Entorno y Dependencias                   |
| **4**  | Estructura del Proyecto Django + ML                      |
| **5**  | Análisis de Datos: Fundamentos y Herramientas            |
| **6**  | Análisis Exploratorio de Datos (EDA) con pandas          |
| **7**  | Visualización de Datos con matplotlib y seaborn          |
| **8**  | Paso 1: Crear el Dataset y el Modelo ML                  |
| **9**  | Paso 2: Entrenar y Serializar el Modelo                  |
| **10** | Paso 3: Integrar el Modelo en Django                     |
| **11** | Paso 4: Crear la API REST con Django REST Framework      |
| **12** | Paso 5: Crear la Interfaz Web para Predicciones          |
| **13** | Paso 6: Validación y Métricas del Modelo                 |
| **14** | Paso 7: Buenas Prácticas y Producción                    |
| **15** | Glosario de Términos                                     |

---

---

# 🧠 1. ¿Qué es Machine Learning y por qué integrarlo en Django?

---

## Definición Simple

```
PROGRAMACIÓN TRADICIONAL                    MACHINE LEARNING
──────────────────────────                  ──────────────────────────
Tú escribes las REGLAS                      La máquina DESCUBRE las reglas
                                            a partir de los DATOS

Entrada: datos + reglas                     Entrada: datos + respuestas esperadas
Salida: respuestas                          Salida: reglas (el modelo)

Ejemplo:                                    Ejemplo:
"Si edad > 18 y sueldo > 500000             "Aquí tienes 10.000 solicitudes
 → aprobar crédito"                          aprobadas y rechazadas. Aprende
                                             a decidir tú solo."
```

## ¿Por qué Django + ML?

```
DJANGO                              +    MACHINE LEARNING
─────────────────                        ─────────────────
✅ Maneja usuarios y autenticación        ✅ Predice resultados futuros
✅ Gestiona bases de datos                ✅ Clasifica textos e imágenes
✅ Crea APIs robustas                     ✅ Detecta patrones en datos
✅ Sirve interfaces web                   ✅ Automatiza decisiones

JUNTOS = Aplicación web inteligente que toma decisiones basadas en datos
```

> 📊 **Dato:** Según el informe _"State of AI 2025"_ de Stanford HAI, el 78% de las empresas tecnológicas ya integran modelos ML directamente en sus aplicaciones web de producción, un aumento del 22% respecto a 2023.
>
> — _Fuente: Stanford University, Human-Centered AI Institute. (2025). "AI Index Report 2025". https://aiindex.stanford.edu/report/_

> 📊 **Dato Chile:** Según la Asociación Chilena de Empresas de Tecnologías de Información (ACTI), el 62% de las empresas tecnológicas chilenas planean incorporar ML en sus productos durante 2026, con Django y FastAPI como los frameworks más demandados para servir modelos.
>
> — _Fuente: ACTI Chile. (2025). "Estudio de Adopción de IA en Chile". https://www.acti.cl/estudios_

---

---

# 📦 2. Ecosistema de Librerías ML en Python (2026)

---

## Las librerías esenciales

| Librería                | Versión 2026 | ¿Para qué sirve?                                     |
| :---------------------- | :----------- | :--------------------------------------------------- |
| **scikit-learn**        | 1.6+         | Algoritmos clásicos de ML (clasificación, regresión) |
| **pandas**              | 2.2+         | Manipulación y análisis de datos tabulares           |
| **numpy**               | 2.1+         | Operaciones matemáticas con arrays                   |
| **joblib**              | 1.4+         | Serializar (guardar/cargar) modelos entrenados       |
| **matplotlib**          | 3.9+         | Visualización de datos y gráficos                    |
| **seaborn**             | 0.13+        | Gráficos estadísticos elegantes                      |
| **djangorestframework** | 3.15+        | Crear APIs REST en Django                            |

## Librerías avanzadas (opcionales)

| Librería         | ¿Para qué sirve?                                   |
| :--------------- | :------------------------------------------------- |
| **TensorFlow**   | Redes neuronales y deep learning (Google)          |
| **PyTorch**      | Redes neuronales y deep learning (Meta)            |
| **XGBoost**      | Algoritmos de boosting de alto rendimiento         |
| **LightGBM**     | Gradient boosting optimizado (Microsoft)           |
| **Hugging Face** | Modelos de lenguaje natural (NLP) preentrenados    |
| **ONNX Runtime** | Ejecutar modelos en producción de forma optimizada |

### La Analogía de la Cocina

```
LIBRERÍA            EQUIVALENTE EN COCINA
────────────────    ─────────────────────────
pandas              La tabla de cortar (preparar ingredientes/datos)
numpy               Las medidas y balanza (cálculos precisos)
scikit-learn        El libro de recetas (algoritmos probados)
joblib              El refrigerador (guardar el modelo para después)
matplotlib          La cámara de fotos (visualizar resultados)
Django              El restaurante (servir el plato al cliente)
DRF                 El mesero (entregar la comida vía API)
```

> 📚 **Fuente:** scikit-learn developers. (2026). _scikit-learn: Machine Learning in Python_. https://scikit-learn.org/stable/

---

---

# 🛠️ 3. Preparación del Entorno y Dependencias

---

## Paso 1: Crear el entorno virtual

```bash
# Crear un entorno virtual (SIEMPRE trabajar con entorno virtual)
python -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

## Paso 2: Instalar las dependencias

```bash
# Dependencias principales
pip install django==5.1
pip install djangorestframework==3.15.2
pip install scikit-learn==1.6.1
pip install pandas==2.2.3
pip install numpy==2.1.3
pip install joblib==1.4.2
pip install matplotlib==3.9.4
pip install seaborn==0.13.2

# Guardar las dependencias
pip freeze > requirements.txt
```

> ⚠️ **Importante:** Siempre usa `pip freeze > requirements.txt` después de instalar librerías. Esto permite que cualquier persona replique tu entorno con `pip install -r requirements.txt`.

## Paso 3: Verificar la instalación

```python
# verificar_instalacion.py — ejecutar con: python verificar_instalacion.py

import sklearn
import pandas
import numpy
import joblib
import django

print(f"scikit-learn: {sklearn.__version__}")
print(f"pandas:       {pandas.__version__}")
print(f"numpy:        {numpy.__version__}")
print(f"joblib:       {joblib.__version__}")
print(f"Django:       {django.__version__}")
print("\n✅ Todas las librerías instaladas correctamente.")
```

```
Output esperado:
────────────────
scikit-learn: 1.6.1
pandas:       2.2.3
numpy:        2.1.3
joblib:       1.4.2
Django:       5.1

✅ Todas las librerías instaladas correctamente.
```

### ¿Qué hace cada librería en nuestro proyecto?

```
FLUJO DEL PROYECTO:

1. pandas         → Cargar y limpiar los datos (CSV, Excel, BD)
2. numpy          → Transformar datos a formato numérico
3. scikit-learn   → Entrenar el modelo de Machine Learning
4. joblib         → Guardar el modelo entrenado en un archivo .pkl
5. Django         → Crear la aplicación web
6. DRF            → Exponer el modelo como API REST
7. matplotlib     → Generar gráficos de rendimiento del modelo
```

> 📚 **Fuente:** Python Packaging Authority. (2026). _pip documentation_. https://pip.pypa.io/en/stable/

---

---

# 📁 4. Estructura del Proyecto Django + ML

---

## Arquitectura recomendada

```
proyecto_ml_django/
├── manage.py
├── requirements.txt
├── proyecto_ml/                    ← Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── predictor/                      ← App principal de predicciones
│   ├── models.py                   ← Modelos de Django (guardar predicciones)
│   ├── views.py                    ← Vistas web
│   ├── serializers.py              ← Serializadores DRF
│   ├── api_views.py                ← Vistas de la API REST
│   ├── urls.py                     ← Rutas de la app
│   ├── forms.py                    ← Formularios para entrada de datos
│   └── templates/
│       └── predictor/
│           ├── inicio.html
│           ├── formulario.html
│           └── resultado.html
├── ml/                             ← Módulo de Machine Learning (NO es app Django)
│   ├── __init__.py
│   ├── entrenar.py                 ← Script de entrenamiento
│   ├── preprocesar.py              ← Funciones de limpieza de datos
│   ├── predecir.py                 ← Función para hacer predicciones
│   └── modelos/                    ← Modelos entrenados guardados
│       └── modelo_credito.pkl      ← Archivo del modelo serializado
├── datos/                          ← Datasets
│   └── solicitudes_credito.csv
├── static/
│   └── css/
│       └── style.css
└── templates/
    └── base.html
```

### ¿Por qué separar `ml/` de la app Django?

```
SEPARACIÓN DE RESPONSABILIDADES:

ml/                                 predictor/
────────────────                    ────────────────
Código puro de ML                   Código de Django
No depende de Django                Depende de Django Y de ml/
Se puede testear solo               Se testea como app web
Se puede reusar en otros proyectos  Es específico de este proyecto
Contiene: entrenar, predecir        Contiene: vistas, URLs, templates

El módulo ml/ es como un "motor" independiente.
La app predictor/ es el "volante" que conecta el motor con el usuario.
```

> 💡 **Buena práctica:** Nunca mezcles lógica de ML dentro de `views.py`. Siempre encapsula la lógica en un módulo separado. Esto facilita el testing, la actualización del modelo y la reutilización.

> 📚 **Fuente:** Huyen, C. (2024). _Designing Machine Learning Systems_ (2nd ed.). O'Reilly Media. https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/

---

---

# 📊 5. Análisis de Datos: Fundamentos y Herramientas

---

## ¿Qué es el Análisis de Datos?

```
ANÁLISIS DE DATOS:
──────────────────
El proceso de INSPECCIONAR, LIMPIAR, TRANSFORMAR y MODELAR datos
con el objetivo de descubrir información útil, llegar a conclusiones
y apoyar la toma de decisiones.

Es la PRIMERA etapa antes de cualquier proyecto de Machine Learning.
Sin análisis de datos, entrenar un modelo es como conducir con los ojos cerrados.
```

## Análisis de Datos vs. Machine Learning

```
ANÁLISIS DE DATOS                           MACHINE LEARNING
──────────────────────────                  ──────────────────────────
MIRA AL PASADO                              PREDICE EL FUTURO

"¿Cuántos créditos se aprobaron?"           "¿Se aprobará este crédito nuevo?"
"¿Cuál es el perfil típico del cliente?"    "¿Qué tipo de cliente es este?"
"¿Existe correlación entre edad e ingreso?" "Dado edad e ingreso, ¿qué pasará?"

Herramientas: pandas, SQL, Excel            Herramientas: scikit-learn, TensorFlow
Resultado: gráficos, reportes, tablas       Resultado: un modelo que decide solo
Rol: Data Analyst                           Rol: ML Engineer / Data Scientist

EL ANÁLISIS ES REQUISITO PREVIO DEL ML
Primero entiendes los datos → Luego entrenas un modelo
```

> 📊 **Dato:** Según el informe _"Data Science Job Market 2025"_ de LinkedIn, las habilidades en análisis de datos con Python (pandas, SQL, visualización) son las más demandadas en Latinoamérica, con un crecimiento del 45% en ofertas laborales respecto a 2023. En Chile, el salario promedio de un Data Analyst junior supera los $1.200.000 CLP mensuales.
>
> — _Fuente: LinkedIn Economic Graph. (2025). "Emerging Jobs Report Latin America". https://economicgraph.linkedin.com/_

## Los 5 tipos de análisis de datos

| Tipo             | Pregunta que responde | Ejemplo                                               |
| :--------------- | :-------------------- | :---------------------------------------------------- |
| **Descriptivo**  | ¿Qué pasó?            | "Se aprobaron 320 créditos en enero"                  |
| **Diagnóstico**  | ¿Por qué pasó?        | "Bajaron porque subió la tasa de interés"             |
| **Exploratorio** | ¿Qué patrones hay?    | "Los clientes mayores de 40 pagan mejor"              |
| **Predictivo**   | ¿Qué va a pasar?      | "El próximo mes habrá 15% más solicitudes"            |
| **Prescriptivo** | ¿Qué debemos hacer?   | "Ofrecer créditos a mayores de 40 con buen historial" |

> 💡 **Importante:** Los análisis descriptivo, diagnóstico y exploratorio son **Análisis de Datos puro**. El predictivo y prescriptivo suelen requerir **Machine Learning**. Por eso ambas disciplinas están conectadas pero no son iguales.

## El flujo del Análisis de Datos

```
DATOS CRUDOS
    │
    ▼
1. RECOLECCIÓN ──────► ¿De dónde vienen los datos? (CSV, BD, API, web scraping)
    │
    ▼
2. LIMPIEZA ─────────► ¿Hay valores faltantes? ¿Duplicados? ¿Errores?
    │
    ▼
3. TRANSFORMACIÓN ───► ¿Hay que cambiar formatos? ¿Crear nuevas columnas?
    │
    ▼
4. EXPLORACIÓN ──────► ¿Qué distribución tienen? ¿Correlaciones? ¿Patrones?
    │
    ▼
5. VISUALIZACIÓN ────► Gráficos que comunican los hallazgos
    │
    ▼
6. CONCLUSIONES ─────► Insights accionables para el negocio
    │
    ▼
7. (OPCIONAL) ML ────► Si se necesita predicción → entrenar un modelo
```

## pandas: La herramienta central del análisis

### ¿Qué es pandas?

```
pandas = "Panel Data" (datos de panel)

Es LA librería de Python para análisis de datos tabulares.
Si Excel es el cuchillo suizo del oficinista,
pandas es el cuchillo suizo del data scientist.

EXCEL                                   PANDAS
──────────────                          ──────────────
Filas y columnas                        DataFrame (filas y columnas)
Celdas                                  Series (una sola columna)
Filtros                                 .query(), .loc[], .filter()
Tablas dinámicas                        .pivot_table(), .groupby()
BUSCARV                                 .merge(), .join()
Gráficos                                .plot()
Límite: ~1 millón de filas              Sin límite práctico (solo tu RAM)
```

### Estructuras fundamentales de pandas

```python
import pandas as pd
import numpy as np

# ─── SERIES: Una sola columna de datos ───
edades = pd.Series([25, 32, 45, 28, 36], name='edad')
print(edades)
# 0    25
# 1    32
# 2    45
# 3    28
# 4    36
# Name: edad, dtype: int64

print(f"Promedio: {edades.mean()}")      # 33.2
print(f"Máximo: {edades.max()}")          # 45
print(f"Desv. estándar: {edades.std():.2f}")  # 7.85


# ─── DATAFRAME: Tabla completa (múltiples columnas) ───
datos = {
    'nombre': ['María', 'Carlos', 'Ana', 'Pedro', 'Lucía'],
    'edad': [25, 32, 45, 28, 36],
    'ingreso': [850000, 1200000, 2100000, 650000, 1500000],
    'ciudad': ['Santiago', 'Valparaíso', 'Santiago', 'Concepción', 'Santiago'],
}

df = pd.DataFrame(datos)
print(df)
#   nombre  edad  ingreso     ciudad
# 0  María    25   850000   Santiago
# 1 Carlos    32  1200000 Valparaíso
# 2    Ana    45  2100000   Santiago
# 3  Pedro    28   650000 Concepción
# 4  Lucía    36  1500000   Santiago
```

### Cargar datos desde diferentes fuentes

```python
# ─── Desde CSV ───
df = pd.read_csv('datos/clientes.csv')

# ─── Desde Excel ───
df = pd.read_excel('datos/reporte.xlsx', sheet_name='Hoja1')

# ─── Desde JSON ───
df = pd.read_json('datos/api_response.json')

# ─── Desde una base de datos SQL ───
import sqlite3
conn = sqlite3.connect('db.sqlite3')
df = pd.read_sql('SELECT * FROM clientes_cliente', conn)
conn.close()

# ─── Desde una URL (datos públicos) ───
url = 'https://datos.ejemplo.com/dataset.csv'
df = pd.read_csv(url)

# ─── Desde el clipboard (lo que copiaste) ───
df = pd.read_clipboard()  # Útil para pegar datos desde Excel
```

### Inspección rápida de los datos

```python
# Ver las primeras/últimas filas
df.head(5)      # Primeras 5 filas
df.tail(3)      # Últimas 3 filas
df.sample(10)   # 10 filas aleatorias

# Información general
df.shape        # (filas, columnas) → (1000, 6)
df.columns      # Lista de nombres de columnas
df.dtypes       # Tipo de dato de cada columna
df.info()       # Resumen completo: columnas, tipos, nulos
df.describe()   # Estadísticas: media, min, max, std, cuartiles

# Valores únicos
df['ciudad'].unique()        # ['Santiago', 'Valparaíso', 'Concepción']
df['ciudad'].nunique()       # 3
df['ciudad'].value_counts()  # Conteo por categoría
```

### Selección y filtrado de datos

```python
# ─── Seleccionar columnas ───
df['nombre']                         # Una columna (Series)
df[['nombre', 'edad']]              # Múltiples columnas (DataFrame)

# ─── Filtrar filas por condición ───
df[df['edad'] > 30]                 # Clientes mayores de 30
df[df['ciudad'] == 'Santiago']      # Solo de Santiago
df[df['ingreso'] >= 1000000]        # Ingreso >= 1 millón

# ─── Filtros combinados ───
df[(df['edad'] > 25) & (df['ciudad'] == 'Santiago')]     # AND
df[(df['ingreso'] > 2000000) | (df['edad'] < 25)]       # OR

# ─── Filtrar con .query() (más legible) ───
df.query('edad > 30 and ciudad == "Santiago"')

# ─── Filtrar con .isin() ───
df[df['ciudad'].isin(['Santiago', 'Valparaíso'])]

# ─── Selección por posición (.iloc) y por etiqueta (.loc) ───
df.iloc[0:5]           # Filas 0 a 4 por posición
df.loc[df['edad'] > 30, 'nombre']  # Nombres donde edad > 30
```

### Limpieza de datos

```python
# ─── Verificar valores nulos ───
df.isnull().sum()            # Cantidad de nulos por columna
df.isnull().sum().sum()      # Total de nulos en todo el DataFrame

# ─── Eliminar filas con nulos ───
df.dropna()                  # Elimina CUALQUIER fila con al menos un nulo
df.dropna(subset=['email'])  # Solo elimina si 'email' es nulo

# ─── Rellenar nulos ───
df['telefono'].fillna('Sin teléfono', inplace=True)
df['ingreso'].fillna(df['ingreso'].mean(), inplace=True)  # Con el promedio

# ─── Eliminar duplicados ───
df.duplicated().sum()        # Cantidad de filas duplicadas
df.drop_duplicates(inplace=True)
df.drop_duplicates(subset=['email'], keep='first', inplace=True)

# ─── Cambiar tipos de datos ───
df['edad'] = df['edad'].astype(int)
df['fecha'] = pd.to_datetime(df['fecha'])
df['precio'] = df['precio'].astype(float)

# ─── Renombrar columnas ───
df.rename(columns={
    'nombre': 'nombre_completo',
    'tel': 'telefono',
}, inplace=True)

# ─── Eliminar columnas innecesarias ───
df.drop(columns=['columna_basura', 'id_temporal'], inplace=True)
```

### La Analogía del Detective

```
EL ANÁLISIS DE DATOS ES COMO SER DETECTIVE:
────────────────────────────────────────────

1. RECOLECTAR EVIDENCIA    → Cargar datos (pd.read_csv)
2. EXAMINAR LA ESCENA      → Inspeccionar (df.info(), df.describe())
3. LIMPIAR PISTAS FALSAS   → Eliminar nulos y duplicados
4. BUSCAR PATRONES         → Filtrar, agrupar, correlacionar
5. CREAR EL MAPA DEL CASO  → Visualizar con gráficos
6. PRESENTAR CONCLUSIONES  → Reportes e insights
7. PREDECIR AL CULPABLE    → Machine Learning (si es necesario)
```

> 📊 **Dato:** Según el informe _"Big Data Analytics Market"_ de Grand View Research, el mercado global de análisis de datos alcanzará los USD $924.000 millones en 2032, con una tasa de crecimiento anual del 13.5%. Python con pandas es la herramienta más usada por analistas de datos en el mundo (72% de preferencia), superando a R (18%) y Excel (10%) en tareas complejas.
>
> — _Fuente: Grand View Research. (2025). "Big Data Analytics Market Size Report". https://www.grandviewresearch.com/industry-analysis/big-data-analytics-market_

> 📚 **Fuente:** McKinney, W. (2022). _Python for Data Analysis_ (3rd ed.). O'Reilly Media. https://wesmckinney.com/book/

> 📚 **Fuente:** pandas development team. (2026). _pandas documentation_. https://pandas.pydata.org/docs/

---

---

# 🔬 6. Análisis Exploratorio de Datos (EDA) con pandas

---

## ¿Qué es el EDA?

```
EDA = Exploratory Data Analysis (Análisis Exploratorio de Datos)

Es el proceso de INVESTIGAR los datos antes de hacer cualquier
modelado o predicción. El objetivo es entender:

1. ¿Cómo se distribuyen los datos?
2. ¿Hay valores atípicos (outliers)?
3. ¿Existen relaciones entre las variables?
4. ¿Qué variables son más importantes?
5. ¿Los datos están listos para el modelo?

Fue popularizado por John Tukey en 1977.
```

> 📊 **Dato:** John Tukey, estadístico de Princeton, publicó el libro _"Exploratory Data Analysis"_ en 1977, revolucionando el campo. Su famosa frase: _"An approximate answer to the right problem is worth a good deal more than an exact answer to an approximate problem"_ (Una respuesta aproximada al problema correcto vale mucho más que una respuesta exacta al problema equivocado).
>
> — _Fuente: Tukey, J. W. (1977). "Exploratory Data Analysis". Addison-Wesley._

## Estadísticas descriptivas completas

```python
# ─── Estadísticas básicas con describe() ───
import pandas as pd

df = pd.read_csv('datos/solicitudes_credito.csv')

print(df.describe())
#               edad   ingreso_mensual   deuda_actual  anios_empleo
# count    1000.000        1000.000       1000.000       1000.000
# mean       43.500        1650000.000    2500000.000     14.500
# std        15.000         780000.000    1450000.000      8.660
# min        18.000         300000.000          0.000      0.000
# 25%        30.000         975000.000    1250000.000      7.000
# 50%        44.000        1650000.000    2500000.000     15.000
# 75%        57.000        2325000.000    3750000.000     22.000
# max        69.000        3000000.000    5000000.000     29.000
```

### ¿Qué significa cada estadística?

| Estadística | Significado                  | Uso práctico                                  |
| :---------- | :--------------------------- | :-------------------------------------------- |
| `count`     | Cantidad de valores no nulos | Detectar datos faltantes                      |
| `mean`      | Promedio aritmético          | Valor central típico                          |
| `std`       | Desviación estándar          | Qué tan dispersos están los datos             |
| `min`       | Valor mínimo                 | Detectar errores (ej: edad = -5)              |
| `25%`       | Primer cuartil (Q1)          | El 25% de los datos está por debajo           |
| `50%`       | Mediana (Q2)                 | Valor central real (no afectado por extremos) |
| `75%`       | Tercer cuartil (Q3)          | El 75% de los datos está por debajo           |
| `max`       | Valor máximo                 | Detectar outliers extremos                    |

### La diferencia entre media y mediana

```
MEDIA vs MEDIANA:
─────────────────
Sueldos: $500.000, $600.000, $700.000, $800.000, $50.000.000

Media (promedio):     $10.520.000   ← ¡DISTORSIONADO por el sueldo alto!
Mediana (valor central): $700.000   ← Refleja mejor la realidad

La mediana es más robusta frente a valores extremos (outliers).
En Chile, el sueldo MEDIANO es más representativo que el promedio.
```

> 📊 **Dato Chile:** Según la Encuesta Suplementaria de Ingresos del INE (2024), el ingreso mediano en Chile es de $502.000 CLP, mientras que el promedio es de $757.000 CLP. La diferencia se debe a que unos pocos ingresos muy altos elevan el promedio pero no la mediana.
>
> — _Fuente: Instituto Nacional de Estadísticas (INE). (2024). "Encuesta Suplementaria de Ingresos". https://www.ine.gob.cl/estadisticas/sociales/ingresos-y-gastos_

## Agrupación y agregación con `.groupby()`

```python
# ─── Agrupar por una columna y calcular estadísticas ───
resumen = df.groupby('historial_crediticio').agg({
    'ingreso_mensual': ['mean', 'median', 'count'],
    'deuda_actual': ['mean', 'max'],
    'aprobado': ['sum', 'mean'],  # sum = total aprobados, mean = tasa
})

print(resumen)
#                     ingreso_mensual              deuda_actual        aprobado
#                            mean     median count        mean      max    sum   mean
# historial
# bueno              1700000.00  1650000   500   2300000.00  4900000   280  0.56
# malo               1580000.00  1500000   200   2800000.00  5000000    30  0.15
# regular            1640000.00  1600000   300   2500000.00  4800000   140  0.47
```

```python
# ─── Conteo por categorías ───
print(df['historial_crediticio'].value_counts())
# bueno      500
# regular    300
# malo       200

# ─── Porcentajes ───
print(df['historial_crediticio'].value_counts(normalize=True) * 100)
# bueno      50.0%
# regular    30.0%
# malo       20.0%

# ─── Agrupar por múltiples columnas ───
tabla = df.groupby(['historial_crediticio', 'aprobado']).size().reset_index(name='cantidad')
print(tabla)
#   historial_crediticio  aprobado  cantidad
# 0               bueno         0       220
# 1               bueno         1       280
# 2                malo         0       170
# 3                malo         1        30
# 4             regular         0       160
# 5             regular         1       140
```

### La Analogía de la Planilla Dinámica

```
.groupby() en pandas = Tabla Dinámica en Excel

EXCEL:                                 PANDAS:
──────────────                         ──────────────
1. Seleccionar datos                   df.groupby('columna')
2. Insertar → Tabla Dinámica
3. Arrastrar campo a "Filas"           .groupby('historial')
4. Arrastrar campo a "Valores"         .agg({'ingreso': 'mean'})
5. Elegir función (Promedio, Suma)     'mean', 'sum', 'count', 'median'
6. Ver resultado                       print(resultado)
```

## Tablas dinámicas con `.pivot_table()`

```python
# ─── Tabla dinámica: tasa de aprobación por historial y rango de edad ───

# Primero crear rangos de edad
df['rango_edad'] = pd.cut(
    df['edad'],
    bins=[17, 25, 35, 45, 55, 70],
    labels=['18-25', '26-35', '36-45', '46-55', '56-70']
)

# Tabla dinámica
tabla_pivot = df.pivot_table(
    values='aprobado',
    index='historial_crediticio',
    columns='rango_edad',
    aggfunc='mean'  # Tasa de aprobación (proporción)
)

print(tabla_pivot.round(2))
# rango_edad    18-25  26-35  36-45  46-55  56-70
# historial
# bueno          0.42   0.58   0.61   0.59   0.55
# malo           0.08   0.15   0.18   0.16   0.12
# regular        0.35   0.48   0.52   0.49   0.44
```

## Correlación entre variables numéricas

```python
# ─── Matriz de correlación ───
correlacion = df[['edad', 'ingreso_mensual', 'deuda_actual',
                  'anios_empleo', 'aprobado']].corr()

print(correlacion.round(2))
#                  edad  ingreso  deuda  anios_empleo  aprobado
# edad             1.00    0.05   0.02         0.85      0.10
# ingreso          0.05    1.00  -0.03         0.08      0.55
# deuda            0.02   -0.03   1.00        -0.01     -0.45
# anios_empleo     0.85    0.08  -0.01         1.00      0.12
# aprobado         0.10    0.55  -0.45         0.12      1.00
```

### ¿Cómo leer la correlación?

```
CORRELACIÓN: Mide la relación lineal entre dos variables

VALOR          SIGNIFICADO                     EJEMPLO
──────         ────────────                    ──────────
 +1.00         Correlación positiva perfecta   Más horas estudio → más nota
 +0.55         Correlación positiva moderada   Más ingreso → más aprobación
  0.00         Sin correlación                 Color favorito → estatura
 -0.45         Correlación negativa moderada   Más deuda → menos aprobación
 -1.00         Correlación negativa perfecta   Más altura → menos profundidad

REGLA GENERAL:
  |r| > 0.7  → Fuerte
  |r| 0.4-0.7 → Moderada
  |r| 0.2-0.4 → Débil
  |r| < 0.2  → Muy débil / inexistente
```

## Detección de outliers (valores atípicos)

```python
# ─── Método IQR (Rango Intercuartílico) ───

Q1 = df['ingreso_mensual'].quantile(0.25)
Q3 = df['ingreso_mensual'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[(df['ingreso_mensual'] < limite_inferior) |
              (df['ingreso_mensual'] > limite_superior)]

print(f"Rango normal: {limite_inferior:,.0f} — {limite_superior:,.0f}")
print(f"Outliers encontrados: {len(outliers)}")
print(f"Porcentaje: {len(outliers)/len(df)*100:.1f}%")
```

### ¿Qué son los outliers?

```
OUTLIERS (Valores Atípicos):
────────────────────────────
Son datos que están MUY lejos del resto.

Ejemplo de sueldos en una empresa:
$500.000, $600.000, $700.000, $800.000, $50.000.000
                                          ↑ OUTLIER

¿Son siempre errores?
NO. Pueden ser:
  ✅ Datos legítimos → El gerente gana mucho más (real)
  ❌ Errores de entrada → Alguien escribió un 0 de más (error)
  ⚠️ Fraudes → Un registro manipulado (sospechoso)

El analista debe INVESTIGAR cada outlier antes de eliminarlo.
```

## Transformaciones y nuevas columnas

```python
# ─── Crear nuevas columnas calculadas ───
df['relacion_deuda_ingreso'] = df['deuda_actual'] / df['ingreso_mensual']
df['ingreso_anual'] = df['ingreso_mensual'] * 12

# ─── Categorizar valores numéricos ───
df['nivel_ingreso'] = pd.cut(
    df['ingreso_mensual'],
    bins=[0, 500000, 1000000, 2000000, float('inf')],
    labels=['Bajo', 'Medio', 'Alto', 'Muy Alto']
)

# ─── Aplicar funciones personalizadas ───
def clasificar_riesgo(row):
    if row['deuda_actual'] > row['ingreso_mensual'] * 3:
        return 'Alto'
    elif row['deuda_actual'] > row['ingreso_mensual']:
        return 'Medio'
    else:
        return 'Bajo'

df['riesgo'] = df.apply(clasificar_riesgo, axis=1)

# ─── Operaciones con strings ───
df['nombre_upper'] = df['nombre'].str.upper()
df['email_dominio'] = df['email'].str.split('@').str[1]
df['tiene_gmail'] = df['email'].str.contains('gmail')
```

## Resumen de funciones pandas esenciales

| Categoría        | Función                    | ¿Qué hace?                             |
| :--------------- | :------------------------- | :------------------------------------- |
| **Cargar**       | `pd.read_csv()`            | Leer archivo CSV                       |
|                  | `pd.read_excel()`          | Leer archivo Excel                     |
|                  | `pd.read_sql()`            | Leer desde base de datos               |
| **Inspeccionar** | `df.head()`, `df.tail()`   | Ver primeras/últimas filas             |
|                  | `df.info()`                | Resumen de tipos y nulos               |
|                  | `df.describe()`            | Estadísticas descriptivas              |
|                  | `df.shape`                 | Dimensiones (filas, columnas)          |
| **Filtrar**      | `df[condicion]`            | Filtrar filas por condición            |
|                  | `df.query()`               | Filtro con sintaxis tipo SQL           |
|                  | `df.loc[]`, `df.iloc[]`    | Selección por etiqueta/posición        |
| **Limpiar**      | `df.dropna()`              | Eliminar filas con nulos               |
|                  | `df.fillna()`              | Rellenar nulos                         |
|                  | `df.drop_duplicates()`     | Eliminar duplicados                    |
|                  | `df.astype()`              | Cambiar tipo de dato                   |
| **Agrupar**      | `df.groupby()`             | Agrupar por categorías                 |
|                  | `df.pivot_table()`         | Tabla dinámica                         |
|                  | `df.value_counts()`        | Conteo por categoría                   |
| **Calcular**     | `df.corr()`                | Matriz de correlación                  |
|                  | `df.mean()`, `df.median()` | Promedio, mediana                      |
|                  | `df.std()`, `df.var()`     | Desviación estándar, varianza          |
| **Transformar**  | `df.apply()`               | Aplicar función personalizada          |
|                  | `pd.cut()`                 | Categorizar valores numéricos          |
|                  | `df.merge()`               | Unir dos DataFrames (como JOIN en SQL) |
| **Exportar**     | `df.to_csv()`              | Guardar como CSV                       |
|                  | `df.to_excel()`            | Guardar como Excel                     |
|                  | `df.to_json()`             | Guardar como JSON                      |

> 📚 **Fuente:** pandas development team. (2026). _pandas User Guide_. https://pandas.pydata.org/docs/user_guide/

> 📚 **Fuente:** VanderPlas, J. (2023). _Python Data Science Handbook_ (2nd ed.). O'Reilly Media. https://jakevdp.github.io/PythonDataScienceHandbook/

---

---

# 📉 7. Visualización de Datos con matplotlib y seaborn

---

## ¿Por qué visualizar datos?

```
DATOS EN UNA TABLA:                     DATOS EN UN GRÁFICO:
───────────────────                     ───────────────────
Ingreso promedio: $1.650.000            [Barra visual que muestra
Desv. estándar: $780.000                 la distribución al instante]
Min: $300.000
Max: $3.000.000                         Un gráfico comunica en 3 segundos
                                        lo que una tabla comunica en 30.
El cerebro humano procesa imágenes
60.000 veces más rápido que texto.
```

> 📊 **Dato:** Según investigaciones del MIT, el cerebro humano puede procesar una imagen en tan solo 13 milisegundos. La visualización de datos explota esta capacidad: un buen gráfico permite detectar patrones que serían invisibles en tablas numéricas.
>
> — _Fuente: Potter, M.C. et al. (2014). "Detecting meaning in RSVP at 13 ms per picture". MIT. Attention, Perception, & Psychophysics._

## matplotlib: La base de la visualización en Python

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('datos/solicitudes_credito.csv')
```

### Gráfico de barras

```python
# ─── Distribución de historial crediticio ───
conteo = df['historial_crediticio'].value_counts()

plt.figure(figsize=(8, 5))
conteo.plot(kind='bar', color=['#2ecc71', '#e74c3c', '#f39c12'])
plt.title('Distribución del Historial Crediticio', fontsize=14, fontweight='bold')
plt.xlabel('Historial')
plt.ylabel('Cantidad de Solicitudes')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('graficos/historial_barras.png', dpi=150)
plt.show()
```

### Histograma

```python
# ─── Distribución de ingresos ───
plt.figure(figsize=(10, 5))
plt.hist(df['ingreso_mensual'], bins=30, color='#3498db', edgecolor='white', alpha=0.8)
plt.axvline(df['ingreso_mensual'].mean(), color='red', linestyle='--', label=f'Media: ${df["ingreso_mensual"].mean():,.0f}')
plt.axvline(df['ingreso_mensual'].median(), color='green', linestyle='--', label=f'Mediana: ${df["ingreso_mensual"].median():,.0f}')
plt.title('Distribución de Ingresos Mensuales', fontsize=14, fontweight='bold')
plt.xlabel('Ingreso Mensual (CLP)')
plt.ylabel('Frecuencia')
plt.legend()
plt.tight_layout()
plt.savefig('graficos/ingresos_histograma.png', dpi=150)
plt.show()
```

### Gráfico de dispersión (Scatter Plot)

```python
# ─── Relación entre ingreso y deuda ───
plt.figure(figsize=(10, 6))

colores = df['aprobado'].map({1: '#2ecc71', 0: '#e74c3c'})

plt.scatter(
    df['ingreso_mensual'],
    df['deuda_actual'],
    c=colores,
    alpha=0.5,
    s=20
)

plt.title('Ingreso vs Deuda (Coloreado por Aprobación)', fontsize=14, fontweight='bold')
plt.xlabel('Ingreso Mensual (CLP)')
plt.ylabel('Deuda Actual (CLP)')

# Leyenda manual
from matplotlib.lines import Line2D
leyenda = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ecc71', label='Aprobado'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', label='Rechazado'),
]
plt.legend(handles=leyenda)
plt.tight_layout()
plt.savefig('graficos/ingreso_deuda_scatter.png', dpi=150)
plt.show()
```

### Gráfico circular (Pie Chart)

```python
# ─── Proporción de aprobados vs rechazados ───
conteo_aprobacion = df['aprobado'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(
    conteo_aprobacion,
    labels=['Rechazado', 'Aprobado'],
    autopct='%1.1f%%',
    colors=['#e74c3c', '#2ecc71'],
    startangle=90,
    explode=[0.05, 0],
    shadow=True,
    textprops={'fontsize': 13}
)
plt.title('Proporción de Aprobación de Crédito', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('graficos/aprobacion_pie.png', dpi=150)
plt.show()
```

## seaborn: Gráficos estadísticos elegantes

seaborn es una librería construida sobre matplotlib que genera gráficos más atractivos con menos código.

```python
import seaborn as sns

# Configurar estilo global
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)
```

### Heatmap de correlación

```python
# ─── Mapa de calor de correlaciones ───
plt.figure(figsize=(10, 8))

correlacion = df[['edad', 'ingreso_mensual', 'deuda_actual',
                  'anios_empleo', 'aprobado']].corr()

sns.heatmap(
    correlacion,
    annot=True,          # Mostrar números
    fmt='.2f',           # Formato decimal
    cmap='RdYlGn',       # Colores: Rojo-Amarillo-Verde
    center=0,            # Centro del color en 0
    square=True,         # Celdas cuadradas
    linewidths=1,
    vmin=-1, vmax=1
)

plt.title('Matriz de Correlación', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('graficos/correlacion_heatmap.png', dpi=150)
plt.show()
```

### Boxplot (Diagrama de cajas)

```python
# ─── Distribución de ingresos por historial ───
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x='historial_crediticio',
    y='ingreso_mensual',
    hue='aprobado',
    palette={0: '#e74c3c', 1: '#2ecc71'}
)

plt.title('Distribución de Ingresos por Historial y Aprobación',
          fontsize=14, fontweight='bold')
plt.xlabel('Historial Crediticio')
plt.ylabel('Ingreso Mensual (CLP)')
plt.legend(title='Aprobado', labels=['Rechazado', 'Aprobado'])
plt.tight_layout()
plt.savefig('graficos/ingresos_boxplot.png', dpi=150)
plt.show()
```

### ¿Cómo leer un Boxplot?

```
        ┌─────────────────────────────── Máximo (sin outliers)
        │
        │    ┌───────┐
        │    │       │─────────────────── Q3 (75%)
        │    │  ───  │─────────────────── Mediana (50%)
        │    │       │─────────────────── Q1 (25%)
        │    └───────┘
        │
        ├───────────────────────────────── Mínimo (sin outliers)

        ●   ● ─────────────────────────── Outliers (puntos individuales)

La "caja" contiene el 50% central de los datos.
Los "bigotes" llegan hasta 1.5 × IQR.
Los puntos fuera de los bigotes son outliers.
```

### Countplot (Conteo por categoría)

```python
# ─── Conteo de aprobados por historial crediticio ───
plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x='historial_crediticio',
    hue='aprobado',
    palette={0: '#e74c3c', 1: '#2ecc71'}
)

plt.title('Aprobación por Historial Crediticio', fontsize=14, fontweight='bold')
plt.xlabel('Historial')
plt.ylabel('Cantidad')
plt.legend(title='Resultado', labels=['Rechazado', 'Aprobado'])
plt.tight_layout()
plt.savefig('graficos/aprobacion_countplot.png', dpi=150)
plt.show()
```

### Pairplot (Todas las relaciones a la vez)

```python
# ─── Gráfico de todas las relaciones entre variables ───
sns.pairplot(
    df[['edad', 'ingreso_mensual', 'deuda_actual', 'anios_empleo', 'aprobado']],
    hue='aprobado',
    palette={0: '#e74c3c', 1: '#2ecc71'},
    diag_kind='hist',
    plot_kws={'alpha': 0.5, 's': 15}
)

plt.suptitle('Relaciones entre todas las Variables', y=1.02, fontsize=16)
plt.tight_layout()
plt.savefig('graficos/pairplot.png', dpi=150)
plt.show()
```

## Resumen de tipos de gráfico

| Gráfico                  | ¿Cuándo usarlo?                            | Función                               |
| :----------------------- | :----------------------------------------- | :------------------------------------ |
| **Barras**               | Comparar categorías                        | `plt.bar()` / `sns.barplot()`         |
| **Histograma**           | Ver distribución de una variable numérica  | `plt.hist()` / `sns.histplot()`       |
| **Scatter (Dispersión)** | Ver relación entre dos variables numéricas | `plt.scatter()` / `sns.scatterplot()` |
| **Pie (Circular)**       | Mostrar proporciones de un total           | `plt.pie()`                           |
| **Boxplot (Cajas)**      | Distribución + outliers por categoría      | `sns.boxplot()`                       |
| **Heatmap**              | Correlaciones entre múltiples variables    | `sns.heatmap()`                       |
| **Countplot**            | Conteo de ocurrencias por categoría        | `sns.countplot()`                     |
| **Pairplot**             | Todas las relaciones a la vez              | `sns.pairplot()`                      |
| **Line (Líneas)**        | Tendencias temporales (series de tiempo)   | `plt.plot()` / `sns.lineplot()`       |
| **Violin**               | Distribución + densidad por categoría      | `sns.violinplot()`                    |

## Buenas prácticas en visualización

```
✅ HACER                                    ❌ NO HACER
────────────                                ──────────────
Títulos descriptivos                        Gráficos sin título
Etiquetas en los ejes                       Ejes sin nombre
Colores con significado                     Colores aleatorios
Leyendas claras                             Sin leyenda
Un mensaje por gráfico                      Demasiada información
Guardar en alta resolución (dpi=150+)       Capturas de pantalla borrosas
Fuente del dato visible                     Sin indicar la fuente
```

> 📊 **Dato:** Edward Tufte, considerado el padre de la visualización de datos moderna, estableció el principio del _"data-ink ratio"_: maximizar la tinta dedicada a los datos y minimizar la decoración innecesaria. Un buen gráfico debe comunicar información, no impresionar con adornos.
>
> — _Fuente: Tufte, E. (2001). "The Visual Display of Quantitative Information" (2nd ed.). Graphics Press._

> 📚 **Fuente:** Hunter, J.D. (2007). _"Matplotlib: A 2D Graphics Environment"_. Computing in Science & Engineering. https://matplotlib.org/stable/

> 📚 **Fuente:** Waskom, M. (2021). _"seaborn: statistical data visualization"_. Journal of Open Source Software. https://seaborn.pydata.org/

---

---

# 📊 8. Paso 1: Crear el Dataset y el Modelo ML

---

## El problema ficticio: Predicción de Aprobación de Crédito

Vamos a construir un sistema que predice si una solicitud de crédito será **aprobada o rechazada** basándose en datos del solicitante. Este es un problema de **clasificación binaria**.

> ⚠️ **Nota:** Los datos y el proyecto son completamente ficticios, creados exclusivamente con fines educativos. No representan ninguna institución financiera real.

## Crear el dataset de ejemplo

```python
# datos/generar_dataset.py

import pandas as pd
import numpy as np

# Fijar semilla para reproducibilidad
np.random.seed(42)

# Generar 1000 registros ficticios
n = 1000

datos = {
    'edad': np.random.randint(18, 70, n),
    'ingreso_mensual': np.random.randint(300000, 3000000, n),
    'deuda_actual': np.random.randint(0, 5000000, n),
    'anios_empleo': np.random.randint(0, 30, n),
    'historial_crediticio': np.random.choice(
        ['bueno', 'regular', 'malo'], n, p=[0.5, 0.3, 0.2]
    ),
}

df = pd.DataFrame(datos)

# Crear la variable objetivo (lo que queremos predecir)
# Regla ficticia: se aprueba si ingreso alto, poca deuda, buen historial
df['aprobado'] = (
    (df['ingreso_mensual'] > 800000) &
    (df['deuda_actual'] < 2000000) &
    (df['anios_empleo'] >= 2) &
    (df['historial_crediticio'].isin(['bueno', 'regular']))
).astype(int)

# Agregar algo de ruido para hacerlo más realista
ruido = np.random.random(n) < 0.1  # 10% de ruido
df.loc[ruido, 'aprobado'] = 1 - df.loc[ruido, 'aprobado']

# Guardar como CSV
df.to_csv('datos/solicitudes_credito.csv', index=False)

print(f"Dataset generado: {len(df)} registros")
print(f"Aprobados: {df['aprobado'].sum()} ({df['aprobado'].mean()*100:.1f}%)")
print(f"Rechazados: {(1-df['aprobado']).sum():.0f} ({(1-df['aprobado']).mean()*100:.1f}%)")
print(f"\nPrimeras filas:")
print(df.head(10))
```

### ¿Qué contiene el dataset?

| Columna                | Tipo     | Descripción                            |
| :--------------------- | :------- | :------------------------------------- |
| `edad`                 | Numérico | Edad del solicitante (18-70)           |
| `ingreso_mensual`      | Numérico | Ingreso mensual en pesos chilenos      |
| `deuda_actual`         | Numérico | Deuda total actual en pesos            |
| `anios_empleo`         | Numérico | Años de empleo continuo                |
| `historial_crediticio` | Texto    | bueno / regular / malo                 |
| `aprobado`             | Binario  | 1 = aprobado, 0 = rechazado (OBJETIVO) |

### Conceptos clave

```
VARIABLE INDEPENDIENTE (Features/Características):
──────────────────────────────────────────────────
Los datos de ENTRADA que el modelo usa para aprender.
→ edad, ingreso_mensual, deuda_actual, anios_empleo, historial

VARIABLE DEPENDIENTE (Target/Objetivo):
──────────────────────────────────────────────────
Lo que queremos PREDECIR.
→ aprobado (1 o 0)

CLASIFICACIÓN BINARIA:
──────────────────────────────────────────────────
El modelo debe decidir entre DOS opciones: aprobado o rechazado.
Es como una pregunta de Sí o No.
```

> 📚 **Fuente:** Géron, A. (2023). _Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow_ (3rd ed.). O'Reilly Media.

---

---

# 🏋️ 9. Paso 2: Entrenar y Serializar el Modelo

---

## ¿Qué significa "entrenar" un modelo?

```
ENTRENAR UN MODELO:
───────────────────
1. Le das DATOS con las respuestas correctas
2. El modelo busca PATRONES en esos datos
3. Esos patrones quedan guardados como REGLAS internas
4. Cuando le das datos NUEVOS, aplica esas reglas para predecir

Es como estudiar para una prueba:
- Estudias (entrenas) con ejercicios resueltos (datos con respuestas)
- En la prueba (producción) te dan ejercicios nuevos
- Aplicas lo que aprendiste para resolverlos
```

## Script de entrenamiento completo

```python
# ml/entrenar.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
import joblib
import os


def entrenar_modelo():
    """Entrena el modelo de predicción de crédito y lo guarda en disco."""

    print("=" * 60)
    print("🏋️ ENTRENAMIENTO DEL MODELO DE PREDICCIÓN DE CRÉDITO")
    print("=" * 60)

    # ─── 1. Cargar los datos ───
    print("\n📂 Cargando datos...")
    df = pd.read_csv('datos/solicitudes_credito.csv')
    print(f"   Registros cargados: {len(df)}")

    # ─── 2. Preprocesar los datos ───
    print("\n🔧 Preprocesando datos...")

    # Convertir texto a números (LabelEncoder)
    le_historial = LabelEncoder()
    df['historial_num'] = le_historial.fit_transform(
        df['historial_crediticio']
    )
    # bueno=0, malo=1, regular=2 (orden alfabético)

    print(f"   Mapeo de historial: {dict(zip(le_historial.classes_, le_historial.transform(le_historial.classes_)))}")

    # Seleccionar features (X) y target (y)
    features = ['edad', 'ingreso_mensual', 'deuda_actual',
                'anios_empleo', 'historial_num']

    X = df[features]
    y = df['aprobado']

    # ─── 3. Dividir en entrenamiento y prueba ───
    print("\n✂️ Dividiendo datos...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,      # 20% para prueba
        random_state=42,     # Semilla para reproducibilidad
        stratify=y           # Mantener la proporción de clases
    )
    print(f"   Entrenamiento: {len(X_train)} registros")
    print(f"   Prueba:        {len(X_test)} registros")

    # ─── 4. Escalar los datos (normalizar) ───
    print("\n📏 Escalando datos...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ─── 5. Entrenar el modelo ───
    print("\n🤖 Entrenando modelo Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,       # 100 árboles de decisión
        max_depth=10,           # Profundidad máxima de cada árbol
        min_samples_split=5,    # Mínimo de muestras para dividir un nodo
        random_state=42,
        n_jobs=-1               # Usar todos los cores del CPU
    )

    modelo.fit(X_train_scaled, y_train)
    print("   ✅ Modelo entrenado exitosamente")

    # ─── 6. Evaluar el modelo ───
    print("\n📊 Evaluando modelo...")
    y_pred = modelo.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n   Exactitud (Accuracy): {accuracy * 100:.2f}%")
    print(f"\n   Reporte de Clasificación:")
    print(classification_report(
        y_test, y_pred,
        target_names=['Rechazado', 'Aprobado']
    ))

    # ─── 7. Guardar el modelo y los transformadores ───
    print("\n💾 Guardando modelo y transformadores...")

    os.makedirs('ml/modelos', exist_ok=True)

    # Guardar todo lo necesario para hacer predicciones
    artefactos = {
        'modelo': modelo,
        'scaler': scaler,
        'label_encoder': le_historial,
        'features': features,
        'version': '1.0.0',
    }

    joblib.dump(artefactos, 'ml/modelos/modelo_credito.pkl')

    tamano = os.path.getsize('ml/modelos/modelo_credito.pkl')
    print(f"   Archivo: ml/modelos/modelo_credito.pkl")
    print(f"   Tamaño: {tamano / 1024:.1f} KB")

    print("\n" + "=" * 60)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 60)

    return accuracy


if __name__ == '__main__':
    entrenar_modelo()
```

### ¿Qué hace cada paso?

```
PASO                    ¿QUÉ HACE?                         ¿POR QUÉ?
────                    ────────────                        ──────────
1. Cargar datos         Lee el CSV con pandas               Sin datos no hay ML
2. Preprocesar          Convierte texto a números           Los algoritmos solo
                        (bueno→0, malo→1, regular→2)        entienden números
3. Dividir              80% para aprender, 20% para         Para evaluar si el
                        evaluar                             modelo realmente aprendió
4. Escalar              Normaliza valores a la misma        Evita que campos con
                        escala                              valores grandes dominen
5. Entrenar             El modelo busca patrones            ES el paso de Machine
                        en los datos                        Learning propiamente tal
6. Evaluar              Prueba con datos que NUNCA vio      Mide qué tan bueno es
7. Guardar              Serializa el modelo a archivo       Para usarlo después en
                        .pkl                                Django sin reentrenar
```

### ¿Qué es Random Forest?

```
RANDOM FOREST (Bosque Aleatorio):
──────────────────────────────────
Es un conjunto de ÁRBOLES DE DECISIÓN que "votan" juntos.

Imagina 100 expertos (árboles) que analizan la solicitud:
  - Experto 1: "Apruebo" ✅
  - Experto 2: "Rechazo" ❌
  - Experto 3: "Apruebo" ✅
  - ...
  - Experto 100: "Apruebo" ✅

La decisión final = lo que diga la MAYORÍA.

¿Por qué funciona?
- Un solo árbol puede equivocarse → SOBREAJUSTE
- 100 árboles juntos se corrigen entre sí → GENERALIZACIÓN
- Es como pedir opinión a un comité en vez de a una sola persona
```

### ¿Qué es `joblib.dump()`?

```
SERIALIZACIÓN:
──────────────
Convertir un objeto de Python (el modelo entrenado)
en un archivo que se puede guardar en disco.

SIN serializar:                     CON serializar:
──────────────                      ──────────────
El modelo vive solo en RAM          El modelo se guarda como archivo
Se pierde al cerrar Python          Se puede cargar en cualquier momento
Hay que reentrenar cada vez         Se entrena UNA vez, se usa SIEMPRE

joblib.dump(modelo, 'archivo.pkl')  → Guarda en disco
joblib.load('archivo.pkl')          → Carga desde disco

.pkl = formato "pickle" de Python (serialización binaria)
```

> 📚 **Fuente:** scikit-learn developers. (2026). _Random Forest Classifier_. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

> 📚 **Fuente:** scikit-learn developers. (2026). _Model persistence_. https://scikit-learn.org/stable/model_persistence.html

---

---

# 🔌 10. Paso 3: Integrar el Modelo en Django

---

## Crear el módulo de predicción

```python
# ml/predecir.py

import joblib
import numpy as np
import os

# Variable global para cachear el modelo en memoria
_modelo_cargado = None


def cargar_modelo():
    """Carga el modelo desde disco (solo la primera vez)."""
    global _modelo_cargado

    if _modelo_cargado is None:
        ruta = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'ml', 'modelos', 'modelo_credito.pkl'
        )
        _modelo_cargado = joblib.load(ruta)
        print(f"✅ Modelo cargado (versión {_modelo_cargado['version']})")

    return _modelo_cargado


def predecir_credito(edad, ingreso_mensual, deuda_actual,
                     anios_empleo, historial_crediticio):
    """
    Realiza una predicción de aprobación de crédito.

    Args:
        edad (int): Edad del solicitante
        ingreso_mensual (int): Ingreso mensual en CLP
        deuda_actual (int): Deuda actual en CLP
        anios_empleo (int): Años de empleo continuo
        historial_crediticio (str): 'bueno', 'regular' o 'malo'

    Returns:
        dict: Resultado con predicción, probabilidad y detalles
    """
    artefactos = cargar_modelo()

    modelo = artefactos['modelo']
    scaler = artefactos['scaler']
    le_historial = artefactos['label_encoder']

    # Convertir historial a número
    historial_num = le_historial.transform([historial_crediticio])[0]

    # Preparar los datos en el formato que espera el modelo
    datos = np.array([[
        edad,
        ingreso_mensual,
        deuda_actual,
        anios_empleo,
        historial_num
    ]])

    # Escalar los datos (misma transformación que en entrenamiento)
    datos_escalados = scaler.transform(datos)

    # Hacer la predicción
    prediccion = modelo.predict(datos_escalados)[0]
    probabilidades = modelo.predict_proba(datos_escalados)[0]

    resultado = {
        'aprobado': bool(prediccion),
        'probabilidad_aprobacion': round(float(probabilidades[1]) * 100, 2),
        'probabilidad_rechazo': round(float(probabilidades[0]) * 100, 2),
        'confianza': round(float(max(probabilidades)) * 100, 2),
        'datos_entrada': {
            'edad': edad,
            'ingreso_mensual': ingreso_mensual,
            'deuda_actual': deuda_actual,
            'anios_empleo': anios_empleo,
            'historial_crediticio': historial_crediticio,
        }
    }

    return resultado
```

### Flujo completo de una predicción

```
USUARIO LLENA FORMULARIO WEB
         │
         ▼
DJANGO RECIBE LOS DATOS (views.py)
         │
         ▼
LLAMA A predecir_credito() (ml/predecir.py)
         │
         ▼
CARGA EL MODELO (solo la primera vez)
         │
         ▼
PREPROCESA LOS DATOS (escalar, encodear)
         │
         ▼
EL MODELO PREDICE (modelo.predict())
         │
         ▼
RETORNA: {aprobado: True, probabilidad: 87.3%}
         │
         ▼
DJANGO MUESTRA EL RESULTADO AL USUARIO
```

## Crear el Modelo Django para guardar predicciones

```python
# predictor/models.py

from django.db import models


class PrediccionCredito(models.Model):
    """Registra cada predicción realizada."""

    # Datos de entrada
    edad = models.IntegerField()
    ingreso_mensual = models.IntegerField(
        help_text='Ingreso mensual en pesos chilenos'
    )
    deuda_actual = models.IntegerField(
        help_text='Deuda total actual en pesos chilenos'
    )
    anios_empleo = models.IntegerField(
        help_text='Años de empleo continuo'
    )
    historial_crediticio = models.CharField(
        max_length=10,
        choices=[
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('malo', 'Malo'),
        ]
    )

    # Resultado de la predicción
    aprobado = models.BooleanField()
    probabilidad = models.FloatField(
        help_text='Probabilidad de aprobación (%)'
    )
    confianza = models.FloatField(
        help_text='Nivel de confianza de la predicción (%)'
    )

    # Metadata
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        estado = "Aprobado" if self.aprobado else "Rechazado"
        return f"Predicción #{self.pk} — {estado} ({self.probabilidad}%)"

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Predicción de Crédito'
        verbose_name_plural = 'Predicciones de Crédito'
```

> 💡 **¿Por qué guardar las predicciones?** Permite auditar las decisiones, detectar sesgos en el modelo, medir su rendimiento en producción y cumplir con regulaciones de transparencia en IA.

> 📚 **Fuente:** Django Software Foundation. (2026). _Models_. https://docs.djangoproject.com/en/5.1/topics/db/models/

---

---

# 🌐 11. Paso 4: Crear la API REST con Django REST Framework

---

## ¿Por qué una API?

```
SIN API                                     CON API REST
──────────────────                          ──────────────────
Solo usuarios con navegador                 Cualquier cliente puede consumirla
Un solo frontend (HTML)                     Múltiples frontends (web, móvil, IoT)
Acoplado: la vista genera todo              Desacoplado: datos separados del diseño
No se puede integrar con otros sistemas     Cualquier sistema externo puede usarla
```

## Configurar Django REST Framework

```python
# proyecto_ml/settings.py

INSTALLED_APPS = [
    # ...
    'rest_framework',     # ← Agregar DRF
    'predictor',          # ← Tu app
]

# Configuración básica de DRF
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

## Crear el Serializador

```python
# predictor/serializers.py

from rest_framework import serializers


class PrediccionInputSerializer(serializers.Serializer):
    """Valida los datos de entrada para la predicción."""

    edad = serializers.IntegerField(
        min_value=18, max_value=100,
        help_text='Edad del solicitante (18-100)'
    )
    ingreso_mensual = serializers.IntegerField(
        min_value=0,
        help_text='Ingreso mensual en CLP'
    )
    deuda_actual = serializers.IntegerField(
        min_value=0,
        help_text='Deuda actual total en CLP'
    )
    anios_empleo = serializers.IntegerField(
        min_value=0, max_value=50,
        help_text='Años de empleo continuo'
    )
    historial_crediticio = serializers.ChoiceField(
        choices=['bueno', 'regular', 'malo'],
        help_text='Historial: bueno, regular o malo'
    )


class PrediccionOutputSerializer(serializers.Serializer):
    """Estructura de la respuesta de predicción."""

    aprobado = serializers.BooleanField()
    probabilidad_aprobacion = serializers.FloatField()
    probabilidad_rechazo = serializers.FloatField()
    confianza = serializers.FloatField()
    datos_entrada = serializers.DictField()
```

### ¿Qué es un serializador?

```
SERIALIZADOR = TRADUCTOR entre Python y JSON

ENTRADA (JSON del cliente):              PYTHON (lo que Django entiende):
──────────────────────────               ──────────────────────────────
{                                        {
  "edad": 35,                              'edad': 35,
  "ingreso_mensual": 1200000,              'ingreso_mensual': 1200000,
  "historial_crediticio": "bueno"          'historial_crediticio': 'bueno'
}                                        }

Además VALIDA:
- ¿La edad está entre 18 y 100? ✅
- ¿El ingreso es un número? ✅
- ¿El historial es bueno/regular/malo? ✅
- Si algo falla → devuelve un error claro
```

## Crear la Vista de la API

```python
# predictor/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PrediccionInputSerializer, PrediccionOutputSerializer
from .models import PrediccionCredito

# Importar la función de predicción del módulo ML
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ml.predecir import predecir_credito


class PrediccionAPIView(APIView):
    """
    API endpoint para predicción de aprobación de crédito.

    POST /api/predecir/
    Body (JSON):
    {
        "edad": 35,
        "ingreso_mensual": 1200000,
        "deuda_actual": 500000,
        "anios_empleo": 5,
        "historial_crediticio": "bueno"
    }
    """

    def post(self, request):
        # 1. Validar los datos de entrada
        serializer = PrediccionInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        datos = serializer.validated_data

        # 2. Realizar la predicción
        try:
            resultado = predecir_credito(
                edad=datos['edad'],
                ingreso_mensual=datos['ingreso_mensual'],
                deuda_actual=datos['deuda_actual'],
                anios_empleo=datos['anios_empleo'],
                historial_crediticio=datos['historial_crediticio'],
            )
        except Exception as e:
            return Response(
                {'error': f'Error en la predicción: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3. Guardar la predicción en la base de datos
        PrediccionCredito.objects.create(
            edad=datos['edad'],
            ingreso_mensual=datos['ingreso_mensual'],
            deuda_actual=datos['deuda_actual'],
            anios_empleo=datos['anios_empleo'],
            historial_crediticio=datos['historial_crediticio'],
            aprobado=resultado['aprobado'],
            probabilidad=resultado['probabilidad_aprobacion'],
            confianza=resultado['confianza'],
        )

        # 4. Retornar el resultado como JSON
        output_serializer = PrediccionOutputSerializer(resultado)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
```

## Configurar las URLs de la API

```python
# predictor/urls.py

from django.urls import path
from . import views
from .api_views import PrediccionAPIView

app_name = 'predictor'

urlpatterns = [
    # Vistas web (HTML)
    path('', views.InicioView.as_view(), name='inicio'),
    path('predecir/', views.FormularioView.as_view(), name='formulario'),
    path('resultado/<int:pk>/', views.ResultadoView.as_view(), name='resultado'),
    path('historial/', views.HistorialView.as_view(), name='historial'),

    # API REST (JSON)
    path('api/predecir/', PrediccionAPIView.as_view(), name='api_predecir'),
]
```

## Probar la API con `curl`

```bash
# Desde la terminal, probar la API:
curl -X POST http://127.0.0.1:8000/predictor/api/predecir/ \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 35,
    "ingreso_mensual": 1500000,
    "deuda_actual": 300000,
    "anios_empleo": 8,
    "historial_crediticio": "bueno"
  }'
```

```json
// Respuesta esperada:
{
  "aprobado": true,
  "probabilidad_aprobacion": 92.3,
  "probabilidad_rechazo": 7.7,
  "confianza": 92.3,
  "datos_entrada": {
    "edad": 35,
    "ingreso_mensual": 1500000,
    "deuda_actual": 300000,
    "anios_empleo": 8,
    "historial_crediticio": "bueno"
  }
}
```

> 📊 **Dato:** Según el informe de Postman _"State of the API Report 2025"_, el 89% de los desarrolladores considera las APIs REST como el estándar principal de integración, y Django REST Framework es el tercer framework más usado para construirlas a nivel mundial.
>
> — _Fuente: Postman. (2025). "State of the API Report 2025". https://www.postman.com/state-of-api/_

> 📚 **Fuente:** Encode. (2026). _Django REST Framework_. https://www.django-rest-framework.org/

---

---

# 🖥️ 12. Paso 5: Crear la Interfaz Web para Predicciones

---

## Formulario de Django para entrada de datos

```python
# predictor/forms.py

from django import forms


class PrediccionForm(forms.Form):
    """Formulario web para solicitar una predicción."""

    edad = forms.IntegerField(
        min_value=18, max_value=100,
        label='Edad del Solicitante',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 35',
        })
    )

    ingreso_mensual = forms.IntegerField(
        min_value=0,
        label='Ingreso Mensual (CLP)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1200000',
        })
    )

    deuda_actual = forms.IntegerField(
        min_value=0,
        label='Deuda Actual Total (CLP)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 500000',
        })
    )

    anios_empleo = forms.IntegerField(
        min_value=0, max_value=50,
        label='Años de Empleo Continuo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 5',
        })
    )

    historial_crediticio = forms.ChoiceField(
        choices=[
            ('', '— Seleccionar —'),
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('malo', 'Malo'),
        ],
        label='Historial Crediticio',
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
```

## Vistas web (views.py)

```python
# predictor/views.py

from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import PrediccionForm
from .models import PrediccionCredito

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ml.predecir import predecir_credito


class InicioView(TemplateView):
    """Página de inicio con información del sistema."""
    template_name = 'predictor/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_predicciones'] = PrediccionCredito.objects.count()
        context['aprobadas'] = PrediccionCredito.objects.filter(aprobado=True).count()
        context['rechazadas'] = PrediccionCredito.objects.filter(aprobado=False).count()
        return context


class FormularioView(FormView):
    """Formulario para realizar una predicción."""
    template_name = 'predictor/formulario.html'
    form_class = PrediccionForm

    def form_valid(self, form):
        datos = form.cleaned_data

        # Realizar la predicción
        resultado = predecir_credito(
            edad=datos['edad'],
            ingreso_mensual=datos['ingreso_mensual'],
            deuda_actual=datos['deuda_actual'],
            anios_empleo=datos['anios_empleo'],
            historial_crediticio=datos['historial_crediticio'],
        )

        # Guardar en la base de datos
        prediccion = PrediccionCredito.objects.create(
            edad=datos['edad'],
            ingreso_mensual=datos['ingreso_mensual'],
            deuda_actual=datos['deuda_actual'],
            anios_empleo=datos['anios_empleo'],
            historial_crediticio=datos['historial_crediticio'],
            aprobado=resultado['aprobado'],
            probabilidad=resultado['probabilidad_aprobacion'],
            confianza=resultado['confianza'],
        )

        if resultado['aprobado']:
            messages.success(
                self.request,
                f'✅ Crédito APROBADO con {resultado["probabilidad_aprobacion"]}% de probabilidad.'
            )
        else:
            messages.warning(
                self.request,
                f'❌ Crédito RECHAZADO. Probabilidad de aprobación: {resultado["probabilidad_aprobacion"]}%.'
            )

        self.prediccion_pk = prediccion.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'predictor:resultado',
            kwargs={'pk': self.prediccion_pk}
        )


class ResultadoView(DetailView):
    """Muestra el resultado detallado de una predicción."""
    model = PrediccionCredito
    template_name = 'predictor/resultado.html'
    context_object_name = 'prediccion'


class HistorialView(ListView):
    """Lista de todas las predicciones realizadas."""
    model = PrediccionCredito
    template_name = 'predictor/historial.html'
    context_object_name = 'predicciones'
    paginate_by = 15
```

## Template del formulario

```html
<!-- templates/predictor/formulario.html -->

{% extends "base.html" %} {% block title %}Nueva Predicción{% endblock %} {%
block content %}
<div class="card">
  <h2>🤖 Predicción de Aprobación de Crédito</h2>
  <p>
    Ingrese los datos del solicitante para obtener una predicción basada en
    Machine Learning.
  </p>

  <form method="POST" class="prediction-form">
    {% csrf_token %} {% if form.non_field_errors %}
    <div class="alert alert-error">
      {% for error in form.non_field_errors %}
      <p>⚠️ {{ error }}</p>
      {% endfor %}
    </div>
    {% endif %} {% for field in form %}
    <div class="form-group">
      <label for="{{ field.id_for_label }}">{{ field.label }}</label>
      {{ field }} {% if field.errors %}
      <div class="field-error">
        {% for error in field.errors %}
        <small>{{ error }}</small>
        {% endfor %}
      </div>
      {% endif %} {% if field.help_text %}
      <small class="help-text">{{ field.help_text }}</small>
      {% endif %}
    </div>
    {% endfor %}

    <button type="submit" class="btn btn-primary">🔮 Obtener Predicción</button>
  </form>
</div>
{% endblock %}
```

## Template del resultado

```html
<!-- templates/predictor/resultado.html -->

{% extends "base.html" %} {% block title %}Resultado de Predicción{% endblock %}
{% block content %}
<div class="card resultado-card">
  <h2>📊 Resultado de la Predicción #{{ prediccion.pk }}</h2>

  <div
    class="resultado-badge {% if prediccion.aprobado %}aprobado{% else %}rechazado{% endif %}"
  >
    {% if prediccion.aprobado %} ✅ CRÉDITO APROBADO {% else %} ❌ CRÉDITO
    RECHAZADO {% endif %}
  </div>

  <div class="probabilidad">
    <h3>Probabilidad de aprobación: {{ prediccion.probabilidad }}%</h3>
    <div class="barra-progreso">
      <div
        class="barra-fill"
        style="width: {{ prediccion.probabilidad }}%"
      ></div>
    </div>
    <p>Confianza del modelo: {{ prediccion.confianza }}%</p>
  </div>

  <h3>📋 Datos del Solicitante</h3>
  <table>
    <tr>
      <td>Edad</td>
      <td>{{ prediccion.edad }} años</td>
    </tr>
    <tr>
      <td>Ingreso Mensual</td>
      <td>${{ prediccion.ingreso_mensual|floatformat:0 }} CLP</td>
    </tr>
    <tr>
      <td>Deuda Actual</td>
      <td>${{ prediccion.deuda_actual|floatformat:0 }} CLP</td>
    </tr>
    <tr>
      <td>Años de Empleo</td>
      <td>{{ prediccion.anios_empleo }} años</td>
    </tr>
    <tr>
      <td>Historial</td>
      <td>{{ prediccion.get_historial_crediticio_display }}</td>
    </tr>
  </table>

  <p class="fecha">
    Predicción realizada: {{ prediccion.fecha|date:"d/m/Y H:i" }}
  </p>

  <div class="acciones">
    <a href="{% url 'predictor:formulario' %}" class="btn btn-primary"
      >🔄 Nueva Predicción</a
    >
    <a href="{% url 'predictor:historial' %}" class="btn btn-secondary"
      >📜 Ver Historial</a
    >
  </div>
</div>
{% endblock %}
```

> 💡 **Dato pedagógico:** La separación entre API (JSON) e interfaz web (HTML) permite que el mismo modelo ML sea consumido por una aplicación web, una app móvil o cualquier sistema externo. Es el principio de **arquitectura desacoplada**.

> 📚 **Fuente:** Django Software Foundation. (2026). _Class-based views_. https://docs.djangoproject.com/en/5.1/topics/class-based-views/

---

---

# 📈 13. Paso 6: Validación y Métricas del Modelo

---

## ¿Cómo saber si el modelo es confiable?

```
MÉTRICAS DE EVALUACIÓN:
───────────────────────
No basta con que el modelo "funcione". Necesitamos MEDIR
qué tan bien funciona con datos que nunca antes vio.

Es como evaluar a un estudiante:
- No lo evalúas con los mismos ejercicios que estudió (eso es trampa)
- Lo evalúas con ejercicios NUEVOS para ver si realmente aprendió
```

## Las 4 métricas fundamentales

### 1. Accuracy (Exactitud)

```
                    Predicciones correctas
ACCURACY = ─────────────────────────────────────
                   Total de predicciones

Ejemplo: 200 predicciones, 180 correctas → 90% accuracy

⚠️ CUIDADO: Si el 95% de los créditos se aprueban, un modelo
que SIEMPRE dice "aprobado" tendría 95% accuracy... pero sería
INÚTIL. Por eso necesitamos más métricas.
```

### 2. Precisión y Recall

```
                                        Verdaderos Positivos
PRECISIÓN (Precision) = ──────────────────────────────────────────────
                        Verdaderos Positivos + Falsos Positivos

"De todos los que dije APROBADOS, ¿cuántos realmente eran aprobados?"
Alta precisión = pocas FALSAS aprobaciones


                                     Verdaderos Positivos
RECALL (Sensibilidad) = ──────────────────────────────────────────────
                        Verdaderos Positivos + Falsos Negativos

"De todos los que DEBÍAN ser aprobados, ¿cuántos detecté?"
Alto recall = pocos aprobados que se me ESCAPARON
```

### 3. F1-Score

```
                    2 × Precisión × Recall
F1-Score = ─────────────────────────────────
                  Precisión + Recall

Es el balance entre precisión y recall.
Un F1 alto significa que ambas métricas son buenas.
```

### 4. Matriz de Confusión

```
                        PREDICCIÓN DEL MODELO
                    ┌──────────────┬──────────────┐
                    │  Rechazado   │  Aprobado    │
        ┌───────────┼──────────────┼──────────────┤
REALIDAD │ Rechazado │  VN (80)     │  FP (5)      │
        │           │  Correcto ✅  │  Error ❌     │
        ├───────────┼──────────────┼──────────────┤
        │ Aprobado  │  FN (10)     │  VP (105)    │
        │           │  Error ❌     │  Correcto ✅  │
        └───────────┴──────────────┴──────────────┘

VN = Verdadero Negativo: Dije "rechazado" y SÍ debía rechazarse
VP = Verdadero Positivo: Dije "aprobado" y SÍ debía aprobarse
FP = Falso Positivo: Dije "aprobado" pero NO debía aprobarse (riesgo)
FN = Falso Negativo: Dije "rechazado" pero SÍ debía aprobarse (pérdida)
```

## Script de evaluación detallada

```python
# ml/evaluar.py

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
import matplotlib.pyplot as plt
import seaborn as sns


def evaluar_modelo():
    """Genera un reporte completo del rendimiento del modelo."""

    print("=" * 60)
    print("📊 EVALUACIÓN DETALLADA DEL MODELO")
    print("=" * 60)

    # Cargar datos y artefactos
    artefactos = joblib.load('ml/modelos/modelo_credito.pkl')
    modelo = artefactos['modelo']
    scaler = artefactos['scaler']
    le_historial = artefactos['label_encoder']
    features = artefactos['features']

    df = pd.read_csv('datos/solicitudes_credito.csv')
    df['historial_num'] = le_historial.transform(df['historial_crediticio'])

    X = df[features]
    y = df['aprobado']

    X_scaled = scaler.transform(X)

    # ─── Validación cruzada (5 folds) ───
    print("\n🔄 Validación Cruzada (5 folds):")
    cv_scores = cross_val_score(modelo, X_scaled, y, cv=5, scoring='accuracy')
    print(f"   Scores: {[f'{s:.3f}' for s in cv_scores]}")
    print(f"   Media:  {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # ─── Métricas completas ───
    y_pred = modelo.predict(X_scaled)

    print(f"\n📊 Métricas:")
    print(f"   Accuracy:  {accuracy_score(y, y_pred):.3f}")
    print(f"   Precision: {precision_score(y, y_pred):.3f}")
    print(f"   Recall:    {recall_score(y, y_pred):.3f}")
    print(f"   F1-Score:  {f1_score(y, y_pred):.3f}")

    print(f"\n📋 Reporte completo:")
    print(classification_report(
        y, y_pred,
        target_names=['Rechazado', 'Aprobado']
    ))

    # ─── Importancia de características ───
    print("\n🔑 Importancia de cada característica:")
    importancias = pd.Series(
        modelo.feature_importances_,
        index=features
    ).sort_values(ascending=False)

    for feat, imp in importancias.items():
        barra = '█' * int(imp * 50)
        print(f"   {feat:25s} {imp:.3f} {barra}")

    print("\n" + "=" * 60)
    print("✅ EVALUACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == '__main__':
    evaluar_modelo()
```

### ¿Qué es la Validación Cruzada?

```
VALIDACIÓN CRUZADA (Cross-Validation) con 5 folds:
───────────────────────────────────────────────────

Divide los datos en 5 partes iguales y entrena 5 veces:

Iteración 1: [TEST] [TRAIN] [TRAIN] [TRAIN] [TRAIN] → Score 1
Iteración 2: [TRAIN] [TEST] [TRAIN] [TRAIN] [TRAIN] → Score 2
Iteración 3: [TRAIN] [TRAIN] [TEST] [TRAIN] [TRAIN] → Score 3
Iteración 4: [TRAIN] [TRAIN] [TRAIN] [TEST] [TRAIN] → Score 4
Iteración 5: [TRAIN] [TRAIN] [TRAIN] [TRAIN] [TEST] → Score 5

Score final = promedio de los 5 scores

¿Por qué?
- Cada dato se usa para entrenamiento Y para prueba
- El resultado es más confiable que una sola división
- Detecta si el modelo solo funciona bien con ciertos datos
```

> 📚 **Fuente:** scikit-learn developers. (2026). _Cross-validation: evaluating estimator performance_. https://scikit-learn.org/stable/modules/cross_validation.html

> 📚 **Fuente:** Google Developers. (2025). _Machine Learning Crash Course: Classification Metrics_. https://developers.google.com/machine-learning/crash-course

---

---

# 🚀 14. Paso 7: Buenas Prácticas y Producción

---

## Checklist de producción

```
ANTES DE DESPLEGAR UN MODELO ML EN PRODUCCIÓN:
───────────────────────────────────────────────

✅ MODELO
  □ Entrenar con datos suficientes (mínimo cientos de registros)
  □ Evaluar con validación cruzada (no solo train/test)
  □ Documentar la versión del modelo y sus métricas
  □ Guardar el modelo serializado (.pkl) en un directorio seguro
  □ Incluir el scaler y encoders en el archivo serializado

✅ CÓDIGO
  □ Separar lógica ML de la lógica Django (módulo ml/)
  □ Cachear el modelo en memoria (no cargarlo en cada request)
  □ Manejar excepciones en las predicciones
  □ Validar TODOS los datos de entrada antes de predecir
  □ Registrar cada predicción en la base de datos (auditoría)

✅ SEGURIDAD
  □ No exponer el archivo .pkl en URLs públicas
  □ Validar tipos y rangos de todos los inputs
  □ Usar CSRF en formularios web
  □ Rate limiting en la API (evitar abuso)

✅ MONITOREO
  □ Registrar logs de predicciones y errores
  □ Monitorear drift del modelo (degradación con el tiempo)
  □ Plan de reentrenamiento periódico
  □ Alertas si el accuracy cae debajo de un umbral
```

## Patrón de carga del modelo (Singleton)

```python
# ml/predecir.py — Patrón recomendado

import threading

_lock = threading.Lock()
_modelo = None

def cargar_modelo():
    """Carga el modelo una sola vez, thread-safe."""
    global _modelo
    if _modelo is None:
        with _lock:
            if _modelo is None:  # Double-check locking
                _modelo = joblib.load('ml/modelos/modelo_credito.pkl')
    return _modelo
```

### ¿Por qué cachear el modelo?

```
SIN caché (MALO):                       CON caché (BUENO):
──────────────────                      ──────────────────
Request 1 → Carga modelo (200ms)        Request 1 → Carga modelo (200ms)
Request 2 → Carga modelo (200ms)        Request 2 → Ya está en RAM (1ms)
Request 3 → Carga modelo (200ms)        Request 3 → Ya está en RAM (1ms)
...                                     ...
Request 100 → 20 segundos total         Request 100 → 0.3 segundos total
```

## Versionado de modelos

```python
# ml/modelos/ — Mantener versiones

modelo_credito_v1.0.0.pkl    ← Primera versión
modelo_credito_v1.1.0.pkl    ← Mejorado con más datos
modelo_credito_v2.0.0.pkl    ← Nuevo algoritmo (XGBoost)

# En el archivo de artefactos:
artefactos = {
    'modelo': modelo,
    'scaler': scaler,
    'label_encoder': le_historial,
    'features': features,
    'version': '2.0.0',
    'fecha_entrenamiento': '2026-03-24',
    'accuracy': 0.943,
    'n_registros_entrenamiento': 10000,
}
```

## Management Command para reentrenar

```python
# predictor/management/commands/reentrenar_modelo.py

from django.core.management.base import BaseCommand
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)))
from ml.entrenar import entrenar_modelo


class Command(BaseCommand):
    help = 'Reentrena el modelo de predicción de crédito'

    def handle(self, *args, **options):
        self.stdout.write('🏋️ Iniciando reentrenamiento...')
        accuracy = entrenar_modelo()
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Modelo reentrenado. Accuracy: {accuracy:.2%}'
            )
        )
```

```bash
# Usar desde la terminal:
python manage.py reentrenar_modelo
```

## Resumen de arquitectura final

```
┌────────────────────────────────────────────────────────────┐
│                    USUARIO / CLIENTE                        │
│                                                            │
│  ┌──────────────┐          ┌──────────────┐                │
│  │ Navegador Web │          │ App Móvil    │                │
│  │  (HTML/CSS)   │          │ (JSON/API)   │                │
│  └──────┬───────┘          └──────┬───────┘                │
│         │                         │                         │
└─────────┼─────────────────────────┼─────────────────────────┘
          │                         │
          ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO (Servidor)                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐                       │
│  │  views.py    │    │ api_views.py │                       │
│  │  (HTML)      │    │  (JSON/DRF)  │                       │
│  └──────┬───────┘    └──────┬───────┘                       │
│         │                   │                                │
│         └─────────┬─────────┘                                │
│                   │                                          │
│                   ▼                                          │
│         ┌─────────────────┐                                  │
│         │  ml/predecir.py │  ← Módulo ML                     │
│         │  (predicción)   │                                  │
│         └────────┬────────┘                                  │
│                  │                                           │
│         ┌────────▼────────┐                                  │
│         │ modelo.pkl      │  ← Modelo entrenado en RAM       │
│         │ (serializado)   │                                  │
│         └─────────────────┘                                  │
│                                                             │
│  ┌──────────────┐                                           │
│  │ models.py    │  ← Registro de predicciones en BD          │
│  │ (Django ORM) │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

> 📊 **Dato:** Según Google Cloud, el 87% de los modelos ML nunca llegan a producción. Las causas principales son: falta de infraestructura (42%), problemas de integración (31%) y ausencia de monitoreo post-despliegue (27%). Dominar la integración Django+ML te posiciona en el grupo que sí logra desplegar.
>
> — _Fuente: Google Cloud. (2025). "MLOps: Continuous delivery and automation pipelines in ML". https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning_

> 📚 **Fuente:** Huyen, C. (2024). _Designing Machine Learning Systems_ (2nd ed.). O'Reilly Media.

---

---

# 📖 15. Glosario de Términos

---

| Término                      | Definición                                                                    |
| :--------------------------- | :---------------------------------------------------------------------------- |
| **Machine Learning**         | Rama de la IA donde los sistemas aprenden patrones a partir de datos          |
| **Modelo**                   | Resultado del entrenamiento; contiene las reglas aprendidas                   |
| **Feature (Característica)** | Variable de entrada que el modelo usa para predecir                           |
| **Target (Objetivo)**        | Variable que el modelo intenta predecir                                       |
| **Entrenamiento**            | Proceso donde el modelo aprende patrones de los datos                         |
| **Predicción / Inferencia**  | Usar el modelo entrenado para obtener un resultado con datos nuevos           |
| **Dataset**                  | Conjunto de datos usado para entrenar y evaluar el modelo                     |
| **Train/Test Split**         | Dividir datos en grupo de entrenamiento y grupo de prueba                     |
| **Overfitting**              | El modelo memoriza los datos de entrenamiento pero falla con datos nuevos     |
| **Underfitting**             | El modelo es demasiado simple y no captura los patrones                       |
| **Accuracy**                 | Porcentaje de predicciones correctas sobre el total                           |
| **Precision**                | De los positivos predichos, cuántos realmente lo son                          |
| **Recall**                   | De los positivos reales, cuántos fueron detectados                            |
| **F1-Score**                 | Media armónica entre precisión y recall                                       |
| **Random Forest**            | Algoritmo que combina múltiples árboles de decisión                           |
| **Serialización**            | Guardar un objeto Python (el modelo) como archivo en disco                    |
| **Scaler**                   | Transformador que normaliza los datos a una escala uniforme                   |
| **Label Encoder**            | Convierte datos categóricos (texto) a números                                 |
| **API REST**                 | Interfaz que permite a otros sistemas comunicarse con tu aplicación vía HTTP  |
| **Serializador (DRF)**       | Componente que convierte datos Python ↔ JSON y los valida                     |
| **Cross-Validation**         | Técnica de evaluación que rota datos entre entrenamiento y prueba             |
| **Confusion Matrix**         | Tabla que muestra aciertos y errores del modelo por categoría                 |
| **Drift**                    | Degradación del rendimiento del modelo cuando los datos cambian con el tiempo |
| **MLOps**                    | Conjunto de prácticas para desplegar y mantener modelos ML en producción      |

---

# 🏁 Resumen de la Guía

---

| Paso | Tema                         | Herramientas                               |
| :--- | :--------------------------- | :----------------------------------------- |
| 1    | Crear el dataset             | `pandas`, `numpy`                          |
| 2    | Entrenar y guardar el modelo | `scikit-learn`, `joblib`                   |
| 3    | Integrar el modelo en Django | `ml/predecir.py`, `models.py`              |
| 4    | Crear API REST               | `djangorestframework`, `serializers.py`    |
| 5    | Crear interfaz web           | `forms.py`, `views.py`, templates          |
| 6    | Evaluar el modelo            | `cross_val_score`, `classification_report` |
| 7    | Preparar para producción     | Caché, versionado, management commands     |

---

## 📚 Bibliografía y Fuentes

- Stanford University, Human-Centered AI Institute. (2025). _AI Index Report 2025_. https://aiindex.stanford.edu/report/
- ACTI Chile. (2025). _Estudio de Adopción de IA en Chile_. https://www.acti.cl/estudios
- scikit-learn developers. (2026). _scikit-learn: Machine Learning in Python_. https://scikit-learn.org/stable/
- scikit-learn developers. (2026). _Random Forest Classifier_. https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- scikit-learn developers. (2026). _Model persistence_. https://scikit-learn.org/stable/model_persistence.html
- scikit-learn developers. (2026). _Cross-validation_. https://scikit-learn.org/stable/modules/cross_validation.html
- Django Software Foundation. (2026). _Django documentation_. https://docs.djangoproject.com/en/5.1/
- Encode. (2026). _Django REST Framework_. https://www.django-rest-framework.org/
- Python Packaging Authority. (2026). _pip documentation_. https://pip.pypa.io/en/stable/
- Géron, A. (2023). _Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow_ (3rd ed.). O'Reilly Media.
- Huyen, C. (2024). _Designing Machine Learning Systems_ (2nd ed.). O'Reilly Media.
- Google Cloud. (2025). _MLOps: Continuous delivery and automation pipelines in ML_. https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- Google Developers. (2025). _Machine Learning Crash Course_. https://developers.google.com/machine-learning/crash-course
- Postman. (2025). _State of the API Report 2025_. https://www.postman.com/state-of-api/
