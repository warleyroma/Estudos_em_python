import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuração da página para layout "wide"
st.set_page_config(layout="wide")

# Carregar os dados
url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Remover 'R$' e converter a coluna 'rent amount' para numérico
df['rent amount'] = df['rent amount'].str.replace('R\$', '', regex=True)
df['rent amount'] = pd.to_numeric(df['rent amount'].str.replace(',', '').str.strip())

# Organizar os dados pela cidade
df = df.sort_values(["city"])

# Criar um filtro de cidade na barra lateral
city = st.sidebar.selectbox("Cidade", df["city"].unique())

# Filtrar os dados com base na cidade selecionada
df_filtered = df[df["city"] == city]

# Layout das colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico de distribuição de valores de aluguel para a cidade selecionada
fig = px.histogram(df_filtered, x='rent amount', nbins=20, title=f"Distribuição de Aluguel em {city}")
col1.plotly_chart(fig, use_container_width=True)

# Comparar o aluguel médio por número de quartos na cidade selecionada
# Garante que todos os números de quartos apareçam
rooms_range = pd.DataFrame({'rooms': range(1, 11)})
rent_by_rooms = df_filtered.groupby('rooms')['rent amount'].mean().reset_index()

# Merge com todos os números de quartos, preenchendo com 0 onde não houver dados
rent_by_rooms_full = rooms_range.merge(rent_by_rooms, on='rooms', how='left').fillna(0)

fig = px.bar(rent_by_rooms_full, x='rooms', y='rent amount', title="Média do Aluguel por Número de Quartos (1-10)")
col2.plotly_chart(fig, use_container_width=True)

# Correlação entre o valor do aluguel e o valor do condomínio (HOA) na cidade selecionada
fig = px.scatter(df_filtered, x='hoa', y='rent amount', title=f"Correlação: Aluguel vs Condomínio em {city}")
col3.plotly_chart(fig, use_container_width=True)

# Contar a frequência de cada valor na coluna 'animal' na cidade selecionada
animal_counts = df_filtered['animal'].value_counts().reset_index()

# Renomear as colunas para serem compatíveis com o Plotly Express
animal_counts.columns = ['animal_status', 'count']

# Criar o gráfico de pizza para animais permitidos na cidade selecionada
fig = px.pie(animal_counts, names='animal_status', values='count', title=f"Imóveis com e sem Animais Permitidos em {city}")
col4.plotly_chart(fig, use_container_width=True)

# Relação entre banheiros e vagas de estacionamento na cidade selecionada
heatmap_data = df_filtered.pivot_table(index='bathroom', columns='parking spaces', aggfunc='size', fill_value=0)
fig = px.imshow(heatmap_data, labels=dict(x="Vagas de Estacionamento", y="Banheiros", color="Contagem"),
                title=f"Relação entre Banheiros e Vagas de Estacionamento em {city}")
col5.plotly_chart(fig, use_container_width=True)
