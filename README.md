# Proyecto-Final-EDA
Informe de Análisis Operativo: E-commerce Olist Brasil
1. Introducción y Objetivo
El presente análisis tiene como objetivo evaluar el desempeño comercial y operativo del ecosistema de e-commerce de Olist. Mediante la integración de herramientas de Ciencia de Datos (Python) y Visualización de Negocios (Excel), se busca transformar datos crudos en un Dashboard Operativo que facilite la toma de decisiones sobre ventas, logística y comportamiento del consumidor.

2. Metodología de Procesamiento (Python)
Antes de la visualización, se realizó una etapa de ETL (Extracción, Transformación y Carga) en Python para asegurar la integridad de la información:

Limpieza de Datos: Se gestionaron valores nulos en las categorías de productos y se eliminaron duplicados.

Ingeniería de Variables: Se crearon nuevas métricas como el total_value (Suma de precio y flete) y la variable binaria is_late para medir la puntualidad.

Segmentación: Se utilizó lógica de programación para categorizar los pedidos en tickets "Bajo", "Medio" y "Alto", permitiendo un análisis más granular en el dashboard.

3. Análisis de Resultados (Dashboard)
A. Desempeño Comercial (KPIs)
El volumen total de ventas procesado asciende a 15.41 Millones de BRL.

Ticket Promedio: Se sitúa en aproximadamente 139 BRL, lo que indica una dominancia de productos de consumo masivo y precio moderado.

Tendencia Temporal: Se observa una estacionalidad marcada (visibles mediante los segmentadores de año y mes), con picos de crecimiento sostenido hacia finales de 2017 y durante 2018.

B. Eficiencia Logística
Mediante el gráfico de anillo y la métrica de puntualidad, se identifica que el 92% de los pedidos llegan dentro del plazo estimado. Este indicador es vital, ya que el análisis de correlación realizado previamente sugiere que los retrasos en la entrega impactan directamente en la calificación de satisfacción del cliente.

C. Distribución por Categoría y Geografía
El mercado está liderado por categorías como "Cama, Mesa y Baño" y "Salud y Belleza". Geográficamente, existe una alta concentración de ingresos en la región sureste de Brasil (SP, RJ, MG), lo que sugiere oportunidades de optimización en los centros de distribución para reducir los costos de flete en estados más alejados.

4. Conclusiones y Recomendaciones
Optimización del Flete: Dado que el flete representa una porción significativa del valor total en tickets bajos, se recomienda establecer políticas de "Envío Gratis" por volumen de compra para aumentar el Ticket Promedio.

Control de Retrasos: Es necesario revisar la logística en los meses de mayor demanda, donde la tasa de puntualidad tiende a disminuir, para evitar la pérdida de confianza del consumidor.

Enfoque en Categorías Clave: Reforzar las alianzas con vendedores de las categorías líderes para asegurar stock y competitividad en precios durante las temporadas pico.

