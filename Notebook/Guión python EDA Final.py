# %%
import pandas as pd

# 1. Carga de datos
orders = pd.read_csv('olist_orders_dataset.csv')
items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')

# %%
# Unión de los archivos
# Esto crea el dataset principal con información del pedido y del producto, que es la parte de unión.
df = pd.merge(orders, items, on='order_id', how='inner')
df = pd.merge(df, products[['product_id', 'product_category_name']], on='product_id', how='left')

# %%
print(f"Dimensiones tras la unión: {df.shape}")

# %%
#GESTIÓN DE FECHAS (Para convertir a formato fecha en vez de texto)
date_cols = ['order_purchase_timestamp', 'order_approved_at', 
             'order_delivered_carrier_date', 'order_delivered_customer_date', 
             'order_estimated_delivery_date']

for col in date_cols:
    df[col] = pd.to_datetime(df[col])

# %%
#TRATAMIENTO DE NULOS
# Calculamos cuántos nulos hay por columna
print(df.isnull().sum())

# %%
# Eliminamos filas donde no hay fecha de entrega (pedidos no completados)
df = df.dropna(subset=['order_delivered_customer_date'])

# %%
#CONTROL DE DUPLICADOS
#A veces se puede cargar una misma dos veces por error, asi que comprobamos si hay duplicados para eliminarlos.
df = df.drop_duplicates()

# %%
#CREACIÓN DE NUEVAS COLUMNAS, QUE APORTEN MÁS VALOR AL ANALISIS
# 1. Tiempo de entrega real (en días)
df['days_to_delivery'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days

# 2. Diferencia entre entrega estimada y real (Delay)
# Si es positivo, llegó tarde. Si es negativo, llegó antes de lo previsto.
df['delivery_delay'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days

# 3. Valor total del pedido (Precio + Transporte)
df['total_value'] = df['price'] + df['freight_value']

# 4. Extracción de periodos para el análisis temporal.
df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M')
df['day_of_week'] = df['order_purchase_timestamp'].dt.day_name()
# 5. Clasificación del ticket
def segmentar_ticket(precio):
    if precio < 50: return 'Bajo'
    elif precio < 150: return 'Medio'
    else: return 'Alto'

df['ticket_segment'] = df['price'].apply(segmentar_ticket)
#Estado de entrega
# 0 = A tiempo o antes, 1 = Retrasado
df['is_late'] = (df['order_delivered_customer_date'] > df['order_estimated_delivery_date']).astype(int)

# %%
# Verificamos una última vez la forma del dataset
print(f"Dataset listo: {df.shape[0]} filas y {df.shape[1]} columnas.")

# %%
#Guardar en CSV
df.to_csv('olist_limpio_final.csv', index=False, encoding='utf-8-sig')

# %%
#ANALISIS DESCRIPTIVO DE LOS DATOS
# Estadísticas descriptivas de las variables numéricas clave
variables_interes = ['price', 'freight_value', 'total_value', 'days_to_delivery', 'delivery_delay']
resumen_stats = df[variables_interes].describe()
print("--- Resumen Estadístico ---")
print(resumen_stats.round(2))

# %%
#ANALISIS DE TENDENCIA CENTRAL Y DISPERSIÓN ESPECIFICO EN EL PRECIO
print(f"Media del precio: {df['price'].mean():.2f}")
print(f"Mediana del precio: {df['price'].median():.2f}")
print(f"Desviación Estándar del precio: {df['price'].std():.2f}")

# Coeficiente de Variación (CV) para ver qué tan dispersos están los datos
cv_precio = (df['price'].std() / df['price'].mean()) * 100
print(f"Coeficiente de Variación del Precio: {cv_precio:.2f}%")

# %%
#ANALISIS DESCRIPTIVO POR CATEGORÍAS 
# Ventas y transporte promedio por segmento de ticket
analisis_segmento = df.groupby('ticket_segment')[['price', 'freight_value']].agg(['mean', 'count', 'sum'])
print(analisis_segmento)

# Análisis de puntualidad: ¿Cuántos pedidos llegaron tarde?
puntualidad_resumen = df['is_late'].value_counts(normalize=True) * 100
print("\n--- Porcentaje de Pedidos ---")
print(f"A tiempo: {puntualidad_resumen[0]:.2f}%")
print(f"Con retraso: {puntualidad_resumen[1]:.2f}%")

# %%
#ANALISIS DE DISTRIBUCIÓN (Frecuencias)
# Conteo de pedidos por día de la semana
pedidos_por_dia = df['day_of_week'].value_counts()
print("\nPedidos por día de la semana:")
print(pedidos_por_dia)

# %%
#ANALISIS ESTADISTICO DE LOS DATOS
#Análisis de Correlación (Mapa de Calor)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 

# Seleccionamos las columnas numéricas relevantes para la correlación
# Usamos df.select_dtypes para asegurar que solo incluimos tipos numéricos
columnas_numericas_corr = df.select_dtypes(include=[np.number]).columns.tolist()

# Filtramos para asegurarnos de que solo incluimos las que realmente queremos analizar
variables_corr = ['price', 'freight_value', 'total_value', 'days_to_delivery', 
                  'delivery_delay', 'is_late', 'price_zscore', 'freight_ratio']

# Nos aseguramos de que solo existen en df
variables_corr = [col for col in variables_corr if col in df.columns]


plt.figure(figsize=(12, 10))
sns.heatmap(df[variables_corr].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Matriz de Correlación entre Variables Clave', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()

# %%
#Detección de Outliers (Boxplot)
#Para ver la dispersion y los valores atipicos
#Días de entrega
plt.figure(figsize=(12, 6))
sns.boxplot(x=df['days_to_delivery'], color='lightgreen', width=0.6)
plt.title('Boxplot de Días de Entrega (Detección de Outliers)', fontsize=16)
plt.xlabel('Días de Entrega', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# precio
plt.figure(figsize=(12, 6))
sns.boxplot(x=df['price'], color='orange', width=0.6)
plt.title('Boxplot de Precios (Detección de Outliers)', fontsize=16)
plt.xlabel('Precio (BRL)', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# %%
#Distribución de Variables Clave
#Para entender como se distribuyen los datos.
# Histograma del precio
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=50, kde=True, color='purple')
plt.title('Distribución de Precios de Productos', fontsize=16)
plt.xlabel('Precio (BRL)', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.xlim(0, df['price'].quantile(0.99)) # Limitar el eje x para mejor visualización
plt.show()

# Histograma de los días de entrega
plt.figure(figsize=(10, 6))
sns.histplot(df['days_to_delivery'].dropna(), bins=30, kde=True, color='teal')
plt.title('Distribución de Días de Entrega', fontsize=16)
plt.xlabel('Días de Entrega', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.show()

# %%
#Comparación de medias
#Para ver la diferencia entre el precio promedio entre los pedidos a tiempo y los con retraso.
avg_price_by_delivery = df.groupby('is_late')['price'].mean().reset_index()
avg_price_by_delivery['is_late'] = avg_price_by_delivery['is_late'].map({0: 'A tiempo', 1: 'Con Retraso'})

plt.figure(figsize=(8, 6))
sns.barplot(x='is_late', y='price', data=avg_price_by_delivery,)
plt.title('Precio Promedio por Estado de Entrega', fontsize=16)
plt.xlabel('Estado de Entrega', fontsize=12)
plt.ylabel('Precio Promedio (BRL)', fontsize=12)
plt.show()

# %%
#Agregue esto al final ya que el excel no me detectaba bien las cantidades y me daban cantidades astronomicas en los totales
df.to_csv('olist_limpio_final.csv', index=False, decimal=',', encoding='utf-8-sig')


