import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px

# Carregar os dados
url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Limpeza e preparação dos dados
df['preco_por_m2'] = df['valor'] / df['area']  # Criar nova variável
# ... outras operações de limpeza

# Análise exploratória
sns.pairplot(df[['valor', 'area', 'quartos', 'banheiros']])  # Mapa de calor
sns.boxplot(x='tipo', y='valor', data=df)  # Boxplot por tipo de imóvel

# Visualizações interativas
fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='valor', zoom=10,
                        mapbox_style="open-street-map")
fig.show()

# Análise geográfica
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
# ... calcular distâncias, criar clusters


# ... outras funções

# Chamar as funções
